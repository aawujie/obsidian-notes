---
title: wx-cli微信本地数据CLI调研
type: research
created: 2026-05-11
updated: 2026-05-11
sources:
  - https://github.com/jackwener/wx-cli
  - wx-cli 源码 (main.rs, cli/mod.rs, daemon/, crypto/, scanner/, ipc.rs, config.rs, cache.rs)
tags:
  - 微信
  - CLI
  - Rust
  - SQLCipher
  - Agent工具
  - 本地数据
  - 进程内存扫描
---

## 概述

wx-cli 是一个 Rust 实现的命令行工具，能从本地微信桌面版（4.x）的加密数据库中解密并查询聊天记录、联系人、朋友圈、收藏等数据。核心思路：**扫描微信进程内存提取 SQLCipher 密钥 → daemon 常驻后台按需解密 → CLI 通过 Unix socket 查询**。

- **仓库**: https://github.com/jackwener/wx-cli
- **版本**: v0.1.10
- **许可证**: Apache-2.0
- **平台**: macOS (Apple Silicon / Intel) / Linux / Windows
- **语言**: Rust (edition 2021)
- **依赖**: tokio (异步), clap (CLI 解析), rusqlite (SQLite 查询), serde_yaml/serde_json (输出序列化), aes/cbc/hmac/sha2/pbkdf2 (解密)

---

## 1. 项目架构

### 1.1 进程模型

```
wx (CLI 前端) ──Unix socket──▶ wx-daemon (后台进程)
                                   │
                         ┌─────────┴──────────┐
                    DBCache               联系人缓存
                (mtime 感知复用)
```

入口统一在 `src/main.rs`，通过 `WX_DAEMON_MODE` 环境变量分流：

```rust
fn main() {
    if std::env::var("WX_DAEMON_MODE").is_ok() {
        daemon::run();  // daemon 模式
    } else {
        cli::run();     // CLI 模式
    }
}
```

**CLI 前端**（`src/cli/`）：解析命令行参数，通过 transport 模块向 daemon 发送 JSON 请求，接收响应后格式化输出。

**Daemon 后端**（`src/daemon/`）：常驻后台进程，维护数据库缓存和联系人缓存，监听 Unix socket（Linux/macOS）或 Windows named pipe。

### 1.2 源码目录结构

| 目录/文件 | 职责 |
|-----------|------|
| `src/main.rs` | 入口分流（CLI vs Daemon） |
| `src/config.rs` | 配置管理（数据目录检测、密钥文件位置、平台适配） |
| `src/ipc.rs` | IPC 协议定义（Request/Response 枚举，JSON 行协议） |
| `src/cli/mod.rs` | CLI 命令定义（clap derive）与分发 |
| `src/cli/transport.rs` | CLI → daemon 通信（自动启动 daemon，保活检测，超时处理） |
| `src/cli/output.rs` | 输出格式化（YAML / JSON 两种模式） |
| `src/cli/*.rs` | 各子命令的入口函数（17 个命令模块） |
| `src/daemon/server.rs` | IPC server（Unix socket / Windows named pipe），请求分发 |
| `src/daemon/cache.rs` | DBCache：mtime 感知的解密数据库缓存，原子化密钥管理 |
| `src/daemon/query.rs` | 核心查询逻辑（会话、消息、联系人、朋友圈、收藏、统计） |
| `src/crypto/mod.rs` | SQLCipher 4 页级解密（AES-256-CBC） |
| `src/crypto/wal.rs` | WAL 日志应用（将未提交的 WAL 帧合并到解密后的 DB） |
| `src/scanner/mod.rs` | 密钥扫描器公共逻辑（salt 收集、匹配） |
| `src/scanner/macos.rs` | macOS 进程内存扫描（Mach VM API） |
| `src/scanner/linux.rs` | Linux 进程内存扫描（/proc/PID/mem） |
| `src/scanner/windows.rs` | Windows 进程内存扫描（Win32 API） |

### 1.3 IPC 协议

CLI 与 daemon 之间使用 **换行符分隔的 JSON 行协议**（JSON Lines），与 Python 版兼容。请求和响应各占一行。

**请求格式**（`src/ipc.rs`）：
```json
{"cmd": "sessions", "limit": 20}
{"cmd": "history", "chat": "张三", "limit": 50}
```

**响应格式**：
```json
{"ok": true, "data": {...}}
{"ok": false, "error": "错误信息"}
```

支持的 Request 类型（17 种）：`Ping`, `Sessions`, `History`, `Search`, `Contacts`, `Unread`, `Members`, `NewMessages`, `Stats`, `Favorites`, `SnsNotifications`, `SnsFeed`, `SnsSearch`

### 1.4 Daemon 启动流程

1. CLI 发送请求前调用 `ensure_daemon()` → `is_alive()` 检查 socket 连通性
2. 若 daemon 未运行：以 `WX_DAEMON_MODE=1` 环境变量 spawn 同一二进制
3. Daemon 进程：加载配置 → 加载 `all_keys.json` → 初始化 DBCache → 预热（加载联系人 + 解密 session.db / sns.db）→ 启动 IPC server
4. Unix 上用 `setsid()` 脱离控制终端，日志写入 `~/.wx-cli/daemon.log`
5. CLI 侧最多等待 15 秒 daemon 就绪，超时报错

---

## 2. 解密原理

### 2.1 微信数据库加密机制

微信 4.x 使用 **SQLCipher 4** 加密本地 SQLite 数据库：

- **加密算法**: AES-256-CBC
- **认证**: HMAC-SHA512
- **密钥派生**: PBKDF2-HMAC-SHA512，256,000 次迭代
- **页大小**: 4096 字节
- **每页结构**: `[数据区 (4096-80)] + [IV (16)] + [HMAC (64)]`（末尾 80 字节为保留区）

### 2.2 密钥提取流程

WCDB（微信自研的 SQLite 封装）在进程内存中缓存派生后的 raw key，格式为：

```
x'<64位hex密钥><32位hex盐值>'
```

即内存中表现为字符串 `x'` + 96 个 hex 字符 + `'`。

**扫描步骤**：

1. **macOS**: 通过 Mach VM API（`task_for_pid` → `mach_vm_region` → `mach_vm_read`）逐区域读取 WeChat 进程内存
   - **前提条件**: 需要对 WeChat.app 做 ad-hoc 签名（`codesign --force --deep --sign -`），否则 `task_for_pid` 会被 macOS SIP 拒绝
   - 使用 2MB chunk 分块读取，逐字节匹配 `x'<96hex>'` 模式

2. **Linux**: 通过 `/proc/<pid>/maps` 枚举可读写内存区域，通过 `/proc/<pid>/mem` 逐区域读取
   - **权限要求**: root（或 `CAP_SYS_PTRACE`）
   - 只扫描 `rw` 权限的区域，同样用 2MB chunk + 重叠窗口避免跨边界遗漏

3. **Windows**: 通过 `CreateToolhelp32Snapshot` + `OpenProcess` + `ReadProcessMemory` 枚举和读取进程内存

4. **密钥匹配**: 从内存中提取出 (key_hex, salt_hex) 对后，与各 `.db` 文件头 16 字节（salt）进行匹配，建立 `rel_path → enc_key` 的映射，保存到 `~/.wx-cli/all_keys.json`

### 2.3 数据库解密（`src/crypto/mod.rs`）

**页级解密算法**：

```
for each page in encrypted_db:
    iv = page[4096-80 .. 4096-64]   // 末尾保留区的前16字节
    ciphertext = page[0 .. 4096-80]  // 数据区
    plaintext = AES-256-CBC-Decrypt(key, iv, ciphertext)
    if page == 1:
        plaintext[0..16] = "SQLite format 3\0"  // 替换 SQLite 魔数
    write plaintext to output
```

- SQLCipher 不使用 PKCS#7 padding，直接解密原始块
- 第一页（pgno=1）跳过 salt 区域（前 16 字节），解密后手动写入 SQLite 文件头

**WAL 处理**（`src/crypto/wal.rs`）：

- SQLCipher 4 的 WAL 帧也被加密
- 解密流程：读取 WAL 头（32 字节）→ 逐帧解密 → 验证 salt1/salt2 匹配 → 将解密后的帧覆盖写入目标页
- salt 不匹配的帧属于已检查点或旧事务，跳过

### 2.4 密钥存储

解密后的密钥保存在 `~/.wx-cli/all_keys.json`，格式：

```json
{
  "message/message_0.db": {"enc_key": "hex..."},
  "session/session.db": "hex...",
  "sns/sns.db": "hex..."
}
```

支持两种格式：简化格式（直接 hex 字符串）和完整格式（含 `enc_key` 字段的对象）。

---

## 3. 命令体系全览

### 3.1 会话与消息

| 命令 | 功能 | 关键参数 |
|------|------|---------|
| `wx sessions` | 最近 N 个会话 | `-n` 数量(默认20), `--json` |
| `wx unread` | 有未读消息的会话 | `-n`, `--filter` (private/group/official/folded), `--json` |
| `wx new-messages` | 增量获取新消息（上次检查后的） | `-n` (默认200), `--json` |
| `wx history <chat>` | 查看聊天记录 | `-n` 条数(默认50), `--offset`, `--since/--until` 日期, `--type` 消息类型过滤, `--json` |
| `wx search <keyword>` | 全库搜索消息 | `-n`, `--in` 限定聊天, `--since/--until`, `--type`, `--json` |

**消息类型过滤** (`--type`): text / image / voice / video / sticker / location / link / file / call / system

**chat_type 字段**（所有会话/消息输出均包含）：

| 取值 | 含义 | username 特征 |
|------|------|--------------|
| `private` | 真人私聊 | `wxid_*` 或自定义短号 |
| `group` | 群聊 | `*@chatroom` |
| `official_account` | 公众号/订阅号/服务号/系统通知 | `gh_*`, `biz_*`, `mphelper`, `qqsafe` |
| `folded` | 折叠入口（订阅号折叠/折叠群聊聚合） | `brandsessionholder`, `@placeholder_foldgroup` |

### 3.2 朋友圈（SNS）

三个独立命令，精确定位不同查询场景：

| 命令 | 功能 | 输出内容 |
|------|------|---------|
| `wx sns-notifications` | 互动通知（点赞/评论） | `type`(like/comment), `from_nickname`, `content`(评论正文), `feed_preview`, `feed_author` |
| `wx sns-feed` | 本地缓存的朋友圈时间线 | `author`, `content`, `media`, `media_count`, `location`, `timestamp` |
| `wx sns-search <keyword>` | 全文搜索朋友圈正文 | 同 sns-feed |

**关键限制**: 只能查到本地刷到过的朋友圈帖子（微信 app 按需下载），未刷到的帖子不在本地数据库中。

**media 字段**: 含每张图的 `url/thumb/key/token/md5/enc_idx/size`，可供下游做图片代理或离线渲染。`media_count = media.len()`，按 DOM 解析的合法 `<media>` 子节点计数。

### 3.3 联系人与群组

| 命令 | 功能 |
|------|------|
| `wx contacts` | 联系人列表 (`-q` 按名字搜索, `-n` 数量) |
| `wx members <chat>` | 群成员列表 |

chat 参数支持昵称、备注名、微信 ID 的模糊匹配。

### 3.4 收藏与统计

| 命令 | 功能 |
|------|------|
| `wx favorites` | 查看收藏内容，支持 `--type` (text/image/article/card/video) 和 `-q` 关键词搜索 |
| `wx stats <chat>` | 聊天统计（发言人、消息类型分布、活跃时段），支持 `--since/--until` |

### 3.5 导出

| 命令 | 功能 |
|------|------|
| `wx export <chat>` | 导出聊天记录到文件 |

支持格式: markdown (默认) / txt / json / yaml
支持参数: `-n` 条数, `-o` 输出文件, `--since/--until` 时间范围

### 3.6 Daemon 管理

| 命令 | 功能 |
|------|------|
| `wx daemon status` | 查看 daemon 运行状态 |
| `wx daemon stop` | 停止 daemon |
| `wx daemon logs` | 查看 daemon 日志（`-f` 持续输出, `-n` 最近 N 行） |

### 3.7 初始化

```bash
wx init           # 首次初始化：检测数据目录 + 扫描密钥
wx init --force   # 强制重新扫描（微信更新/重启后密钥变化时使用）
```

---

## 4. 输出格式：YAML vs JSON

**默认 YAML**，省 token & 易读。**`--json`** 切换为 JSON，方便 `jq` 处理和程序化解析。

实现（`src/cli/output.rs`）：

```rust
pub enum Fmt {
    Yaml,  // 默认
    Json,  // --json
}

pub fn print_value(value: &serde_json::Value, fmt: &Fmt) -> Result<()> {
    match fmt {
        Fmt::Json => println!("{}", serde_json::to_string_pretty(value)?),
        Fmt::Yaml => print!("{}", serde_yaml::to_string(value)?),
    }
    Ok(())
}
```

**Agent 使用建议**: 查询结果需要程序处理时统一加 `--json`，如 `wx new-messages --json`。

---

## 5. 缓存机制

### 5.1 核心设计

DBCache（`src/daemon/cache.rs`）实现了**基于文件修改时间（mtime）的智能缓存**：

```
加密 DB (.db + .db-wal) mtime 未变 → 直接复用已解密的缓存文件
加密 DB mtime 发生变化 → 重新解密 + 应用 WAL → 覆盖缓存
```

### 5.2 详细流程

1. **首次访问**：解密 `foo.db` + 应用 `foo.db-wal`，写入 `~/.wx-cli/cache/<md5hash>.db`，记录 mtime
2. **后续访问**：比较当前 .db 和 .db-wal 的 mtime 与缓存记录
   - 一致 → 直接返回缓存路径（O(1)）
   - 不一致 → 触发重新解密
3. **持久化**：mtime 记录持久化到 `~/.wx-cli/cache/_mtimes.json`，daemon 重启后复用

### 5.3 缓存文件结构

```
~/.wx-cli/
├── config.json         # db_dir, keys_file 等配置
├── all_keys.json       # 数据库密钥映射（敏感，勿分享）
├── daemon.sock         # Unix socket（macOS/Linux）
├── daemon.pid          # 进程 PID
├── daemon.log          # 运行日志
├── last_check.json     # new-messages 增量状态
└── cache/
    ├── _mtimes.json    # mtime 索引 {rel_key: {db_mt, wal_mt, path}}
    └── <md5hash>.db    # 解密后的数据库文件
```

### 5.4 并发安全

- DBCache 内部使用 `tokio::sync::Mutex` 保护 `HashMap<String, CacheEntry>`
- 解密操作通过 `tokio::task::spawn_blocking` 放到专用线程池，不阻塞 async runtime
- IPC 请求取 Names guard 后做 `Arc::clone`（O(1)），立即 drop 锁，允许并发查询

---

## 6. 安装方式对比

| 方式 | 命令 | 适用场景 |
|------|------|---------|
| **npm**（推荐） | `npm install -g @jackwener/wx-cli` | 全平台，有 Node.js 环境 |
| **curl** | `curl -fsSL https://.../install.sh \| bash` | macOS/Linux，一键安装 |
| **PowerShell** | `irm https://.../install.ps1 \| iex` | Windows |
| **手动下载** | [Releases 页面](https://github.com/jackwener/wx-cli/releases) | 离线/特定版本 |
| **源码构建** | `git clone && cargo build --release` | 开发者，需要 Rust 工具链 |
| **skills add** | `npx skills add jackwener/wx-cli` | Claude Code/Cursor/Codex agent 集成 |

**预编译二进制**：

| 平台 | 文件 |
|------|------|
| macOS Apple Silicon | `wx-macos-arm64` |
| macOS Intel | `wx-macos-x86_64` |
| Linux x86_64 | `wx-linux-x86_64` |
| Linux arm64 | `wx-linux-arm64` |
| Windows x86_64 | `wx-windows-x86_64.exe` |

Release 构建配置：`opt-level=3`, `lto=true`, `codegen-units=1`, `strip=true`（最小体积、最快速度）。

---

## 7. 安全评估

### 7.1 密钥提取机制

| 方面 | 评估 |
|------|------|
| **权限要求** | `wx init` 需要 root/Administrator 权限（读进程内存），后续命令不需要 |
| **macOS 安全** | 需要 ad-hoc 签名 WeChat.app 使 `task_for_pid` 可用，签名后其他安全机制（SIP、AMFI）不受影响 |
| **密钥存储** | `~/.wx-cli/all_keys.json` 明文存储密钥，文件权限应为 0600（socket 已设置 0600，密钥文件也可手动设置） |
| **内存扫描** | 只读操作，不修改微信进程内存，不会被检测为注入或篡改 |

### 7.2 数据安全

| 方面 | 评估 |
|------|------|
| **数据不出本机** | 所有操作均为本地文件读取和内存扫描，无网络通信 |
| **按需解密** | 只在查询时解密需要的数据库，不是全量预解密 |
| **缓存安全** | 解密后的 DB 缓存仅存储在 `~/.wx-cli/cache/`，与原始加密 DB 同用户权限 |
| **Socket 权限** | Unix socket 权限设为 0600，仅当前用户可连接 |

### 7.3 风险提示

1. **`all_keys.json` 泄露风险**: 如果密钥文件被他人获取，结合加密 DB 文件即可解密全部微信数据。建议定期清理或加密存储。
2. **`sudo wx init` 遗留权限**: 旧版本用 sudo 运行后 `~/.wx-cli/` 目录属主可能是 root，导致非 root daemon 无法写入。新版已修复此问题，旧版本需手动 `sudo chown -R $(whoami) ~/.wx-cli/`。
3. **macOS 签名副作用**: ad-hoc 签名会替换 WeChat 原有的开发者签名，可能影响部分企业 MDM 策略的合规性。

---

## 8. 对我们调度系统的价值

### 8.1 核心能力映射

| 场景 | wx-cli 命令 | 价值 |
|------|------------|------|
| Agent 查询微信消息 | `wx search "关键词" --json` | 让 AI agent 直接检索聊天记录，无需人工复制粘贴 |
| 自动归档聊天记录 | `wx export <chat> -o archive.md` | 定期导出关键会话，建立知识库 |
| 增量获取新消息 | `wx new-messages --json` | 基于 `last_check.json` 状态快照，只拉取上次检查后的新消息 |
| 联系人发现 | `wx contacts --query "关键词"` | Agent 自动匹配聊天对象 |
| 群组信息 | `wx members <群名>` | 获取群成员列表 |
| 未读消息监控 | `wx unread --filter private,group` | 过滤真人未读，忽略公众号噪音 |

### 8.2 增量消息机制

`new-messages` 命令维护了一个 **per-session 时间戳快照**（`~/.wx-cli/last_check.json`）：

```json
{
  "sessions": {
    "wxid_xxx": 1715432000,
    "123456@chatroom": 1715432001
  }
}
```

每次调用 `new-messages`：
1. 客户端传入上次的 state（`HashMap<username, timestamp>`）
2. Daemon 查询每个会话中 `createTime > last_ts` 的消息
3. 返回新消息列表 + 更新后的 `new_state`

**首次运行**: state 为 None → daemon 返回所有会话的最新一条消息 + new_state，不会拉全量历史。

### 8.3 调度集成建议

```
调度系统 (cron / systemd timer)
    │
    ├─ 每 N 分钟: wx new-messages --json
    │   → 增量获取 → 写入消息队列 / 通知系统
    │
    ├─ 每日: wx export <关键群> -f markdown -o daily/<date>.md
    │   → 归档到知识库
    │
    └─ 按需: wx search "XXX" --json
        → Agent 直接查询，填充上下文
```

**注意事项**：
- daemon 必须保持运行（`wx daemon status` 确认）
- daemon 在首次调用时自动启动，无需手动管理
- 微信关闭后数据库 WAL 不会更新，new-messages 返回为空（正常行为）

### 8.4 Agent 集成

wx-cli 通过 [skills CLI](https://github.com/vercel-labs/skills) 提供了 SKILL.md，支持一键安装到 Claude Code、Cursor、Codex 等 agent 环境：

```bash
npx skills add jackwener/wx-cli    # 项目级安装
npx skills add jackwener/wx-cli -g # 全局安装
```

安装后 agent 自动读取 SKILL.md 中的触发词、命令速查表和使用建议，Agent 在用户提及微信相关查询时自动调用 wx-cli。

---

## 9. 关键设计决策

### 9.1 为什么用 daemon 而不是直接 CLI 解密

1. **解密开销**: SQLCipher 全量解密一个 DB 需要 O(N) 时间（N = 页数），每条命令都解密不可接受
2. **WAL 合并**: 每次解密都需要将 WAL 日志帧应用到解密后的 DB，这个操作需要随机写入
3. **缓存复用**: daemon 常驻后，解密一次 + mtime 检测变更，后续查询零解密开销
4. **并发安全**: daemon 通过 Mutex 保护缓存，多个 CLI 并发调用不会重复解密

### 9.2 为什么默认 YAML 而不是 JSON

- YAML 无需引号和括号，字符数比 JSON 少约 15-20%
- 对 LLM token 计数更友好
- 人类可读性优于 JSON
- 保留了 `--json` 选项用于程序化处理

### 9.3 为什么用 spawn_blocking 处理解密

- 解密是 CPU 密集型操作（AES-CBC 逐页解密 + WAL 随机写），不适合在 tokio 的 async worker 线程上运行
- `spawn_blocking` 将解密放到专用的阻塞线程池，不阻塞其他 IPC 请求的处理

---

## 10. 依赖关系

```
wx-cli
├── clap 4              # CLI 参数解析
├── tokio 1 (full)      # 异步运行时 + IPC server
├── serde / serde_json   # 序列化 / IPC 协议
├── serde_yaml 0.9       # YAML 输出
├── rusqlite 0.31        # SQLite 查询（bundled 模式，自带 libsqlite3）
├── aes 0.8 / cbc 0.1    # AES-256-CBC 解密
├── hmac 0.12 / sha2 0.10 / pbkdf2 0.12  # SQLCipher 密钥派生（备用/验证）
├── zstd 0.13            # 微信部分数据使用 zstd 压缩
├── md5 0.7              # 联系人数据库文件名 = Msg_<md5(微信ID)>
├── roxmltree 0.20       # 朋友圈 XML 内容解析
├── regex 1              # 内存密钥模式匹配
├── dirs 5 / libc 0.2    # 跨平台路径 / Unix 系统调用
└── [Windows] interprocess 2, windows 0.58  # Windows named pipe / 进程内存读取
```

**总计依赖**: ~22 个 crate（不含传递依赖），精简且专注。

---

## 总结

wx-cli 是目前最成熟的微信本地数据 CLI 方案，核心优势：

1. **零依赖安装** — 单一 Rust 二进制，npm/curl/prebuilt 三种方式
2. **毫秒级响应** — daemon + mtime 缓存，首次解密后几乎零开销
3. **AI 友好** — 默认 YAML 输出，skills 一键集成到 agent 环境
4. **完全本地** — 数据不出本机，安全可控
5. **功能完整** — 覆盖消息/朋友圈/联系人/群组/收藏/统计/导出全部场景
6. **跨平台** — macOS/Linux/Windows 统一接口
7. **增量子系统** — `new-messages` 基于 last_check 快照实现真正的增量获取