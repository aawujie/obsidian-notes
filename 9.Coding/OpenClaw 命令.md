---
share_link: https://share.note.sx/uljjcv9i#5X+HR+sfmqcFjRd2M1eoc975O3PSpI9YzjZ2NYX+iAY
share_updated: 2026-02-27T17:04:55+08:00
---
# OpenClaw 命令手册

> 作者：吴杰
> 版本：2026.2.23 | 最后更新：2026-02-27

---

## 📋 全局选项

```bash
openclaw [选项] [命令]

# 常用全局选项
--dev                    # 开发模式：隔离状态目录 ~/.openclaw-dev
--profile <name>         # 使用命名配置（隔离状态）
--log-level <level>      # 日志级别：silent|fatal|error|warn|info|debug|trace
--no-color               # 禁用 ANSI 颜色
-h, --help               # 显示帮助
-V, --version            # 显示版本号
```

---

## 🦞 Gateway（网关服务）

网关是 OpenClaw 的核心 WebSocket 服务，管理所有 Agent 和频道连接。

### 基本控制
```bash
openclaw gateway run              # 前台运行网关
openclaw gateway start            # 启动网关服务（后台）
openclaw gateway stop             # 停止网关服务
openclaw gateway restart          # 重启网关服务
openclaw gateway status           # 查看服务状态 + 可达性探测
```

### 高级选项
```bash
openclaw gateway run --port 18789           # 指定端口
openclaw gateway run --force                # 强制杀死占用端口的进程
openclaw gateway run --verbose              # 详细日志
openclaw gateway run --ws-log compact       # 紧凑的 WebSocket 日志
openclaw gateway run --dev                  # 开发模式运行
openclaw gateway run --auth token           # 认证模式：token 或 password
openclaw gateway run --bind lan             # 绑定模式：loopback|lan|tailnet|auto
```

### 服务管理
```bash
openclaw gateway install        # 安装为系统服务（launchd/systemd/schtasks）
openclaw gateway uninstall      # 卸载系统服务
```

### 诊断工具
```bash
openclaw gateway discover       # 通过 Bonjour 发现网关
openclaw gateway health         # 获取网关健康状态
openclaw gateway call <method>  # 直接调用网关 RPC 方法
openclaw gateway probe          # 显示网关可达性 + 发现 + 健康摘要
openclaw gateway usage-cost     # 从会话日志获取使用成本摘要
```

---

## 🤖 Agent 管理

### 查看与管理
```bash
openclaw agents list            # 列出配置的 Agent
openclaw agents add             # 添加新的隔离 Agent
openclaw agents delete          # 删除 Agent 并清理工作区
openclaw agents set-identity    # 更新 Agent 身份（名称/主题/表情/头像）
```

### 运行 Agent
```bash
openclaw agent                  # 运行一次 Agent 轮次
```

---

## 💬 频道管理 (Channels)

管理连接的聊天频道（Telegram、Discord、WhatsApp 等）。

```bash
openclaw channels list          # 列出配置的频道和认证配置
openclaw channels status        # 显示频道状态
openclaw channels status --probe  # 运行状态检查和探测
openclaw channels add           # 添加或更新频道账户
openclaw channels remove        # 禁用或删除频道账户
openclaw channels login         # 链接频道账户（如支持）
openclaw channels logout        # 登出频道会话
openclaw channels logs          # 显示最近的频道日志
openclaw channels resolve       # 解析频道/用户名为 ID
openclaw channels capabilities  # 显示提供者能力（意图/范围/功能）
```

---

## 📩 消息管理

```bash
# 发送消息
openclaw message send --target <目标> --message "内容"
openclaw message send --channel telegram --target @mychat --message "Hi"
openclaw message send --target +15555550123 --message "Hi" --media photo.jpg

# 读取消息
openclaw message read           # 读取最近消息

# 消息操作
openclaw message edit           # 编辑消息
openclaw message delete         # 删除消息
openclaw message react          # 添加/移除反应
openclaw message reactions      # 列出消息的反应
openclaw message pin            # 置顶消息
openclaw message unpin          # 取消置顶
openclaw message pins           # 列出置顶消息

# 投票
openclaw message poll --channel discord --target channel:123 \
  --poll-question "零食？" --poll-option 披萨 --poll-option 寿司

# 广播
openclaw message broadcast      # 向多个目标广播消息

# 搜索（Discord）
openclaw message search         # 搜索 Discord 消息

# 频道/成员/角色管理
openclaw message channel        # 频道操作
openclaw message member         # 成员操作
openclaw message role           # 角色操作
openclaw message permissions    # 获取频道权限
openclaw message ban            # 禁止成员
openclaw message kick           # 踢出成员
openclaw message timeout        # 限时禁言成员

# 线程/表情/贴纸
openclaw message thread         # 线程操作
openclaw message emoji          # 表情操作
openclaw message sticker        # 贴纸操作
openclaw message event          # 事件操作
openclaw message voice          # 语音操作
```

---

## 📚 记忆索引 (Memory)

```bash
# 状态查看
openclaw memory status          # 显示索引和提供者状态
openclaw memory status --json   # 输出机器可读 JSON

# 索引操作
openclaw memory index           # 增量索引（只索引变更的文件）
openclaw memory index --force   # 强制全量重新索引
openclaw memory index --verbose # 详细日志

# 搜索
openclaw memory search --query "你的搜索词"
```

---

## 🌐 浏览器控制 (Browser)

### 基本控制
```bash
openclaw browser status         # 显示浏览器状态
openclaw browser start          # 启动浏览器
openclaw browser stop           # 停止浏览器
openclaw browser tabs           # 列出打开的标签页
openclaw browser profiles       # 列出所有浏览器配置文件
```

### 导航与操作
```bash
openclaw browser open <URL>           # 在新标签页打开 URL
openclaw browser navigate <URL>       # 导航当前标签页
openclaw browser focus <targetId>     # 聚焦标签页
openclaw browser close [targetId]     # 关闭标签页
openclaw browser resize <宽> <高>     # 调整视口大小
```

### 截图与快照
```bash
openclaw browser screenshot           # 截取屏幕截图
openclaw browser screenshot --full-page  # 完整页面截图
openclaw browser screenshot --ref <ref>  # 截取指定元素
openclaw browser snapshot             # 捕获页面快照（默认 AI 格式）
openclaw browser snapshot --format aria  # 无障碍树格式
openclaw browser snapshot --efficient    # 高效模式
openclaw browser snapshot --labels       # 显示标签
```

### 交互操作
```bash
openclaw browser click <ref> [--double]    # 点击元素
openclaw browser type <ref> "文本" [--submit]  # 输入文本
openclaw browser press <键>                # 按键
openclaw browser hover <ref>               # 悬停
openclaw browser drag <startRef> <endRef>  # 拖拽
openclaw browser select <ref> <选项>       # 选择下拉选项
openclaw browser fill --fields '[{"ref":"1","value":"文本"}]'  # 填充表单
openclaw browser scrollintoview <ref>      # 滚动到视图中
```

### 高级功能
```bash
openclaw browser evaluate --fn '(el) => el.textContent' --ref 7  # 执行 JS
openclaw browser console --level error    # 获取控制台消息
openclaw browser errors                   # 获取页面错误
openclaw browser requests                 # 获取网络请求
openclaw browser responsebody             # 等待网络响应并返回内容
openclaw browser pdf                      # 保存页面为 PDF
openclaw browser download <ref>           # 点击下载并保存
openclaw browser waitfordownload          # 等待下载完成
openclaw browser dialog --accept          # 处理模态对话框
openclaw browser upload <文件路径>        # 准备文件上传
openclaw browser cookies                  # 读写 Cookie
openclaw browser storage                  # 读写 localStorage/sessionStorage
openclaw browser extension                # Chrome 扩展助手
openclaw browser trace                    # 录制 Playwright 追踪
openclaw browser tab                      # 标签页快捷操作
openclaw browser wait                     # 等待（时间/选择器/URL/加载状态）
```

### 配置文件管理
```bash
openclaw browser create-profile <名称>   # 创建新配置文件
openclaw browser delete-profile <名称>   # 删除配置文件
openclaw browser reset-profile <名称>    # 重置配置文件（移到回收站）
```

---

## 🗂️ 会话管理 (Sessions)

```bash
openclaw sessions                       # 列出所有会话
openclaw sessions --agent <id>          # 列出指定 Agent 的会话
openclaw sessions --all-agents          # 聚合所有 Agent 的会话
openclaw sessions --active 120          # 仅显示最近 120 分钟的会话
openclaw sessions --json                # 输出 JSON 格式
openclaw sessions cleanup               # 运行会话存储维护
```

---

## ⏰ 定时任务 (Cron)

```bash
openclaw cron list          # 列出定时任务
openclaw cron add           # 添加定时任务
openclaw cron edit          # 编辑定时任务
openclaw cron enable        # 启用定时任务
openclaw cron disable       # 禁用定时任务
openclaw cron rm            # 删除定时任务
openclaw cron run           # 立即运行定时任务（调试用）
openclaw cron runs          # 显示运行历史（JSONL）
openclaw cron status        # 显示调度器状态
```

---

## 🤖 模型管理 (Models)

```bash
openclaw models list            # 列出配置的模型
openclaw models status          # 显示配置的模型状态
openclaw models status --json   # JSON 输出
openclaw models scan            # 扫描 OpenRouter 免费模型
openclaw models set <模型名>    # 设置默认模型
openclaw models set-image <模型名>  # 设置图像模型

# 别名管理
openclaw models aliases         # 管理模型别名

# 认证管理
openclaw models auth            # 管理模型认证配置

# 降级列表
openclaw models fallbacks       # 管理模型降级列表
openclaw models image-fallbacks # 管理图像模型降级列表
```

---

## 🔌 插件管理 (Plugins)

```bash
openclaw plugins list           # 列出发现的插件
openclaw plugins info <插件名>  # 显示插件详情
openclaw plugins install <路径 | 归档 | npm>  # 安装插件
openclaw plugins update         # 更新已安装插件（仅 npm）
openclaw plugins uninstall      # 卸载插件
openclaw plugins enable         # 启用插件
openclaw plugins disable        # 禁用插件
openclaw plugins doctor         # 报告插件加载问题
```

---

## 🛠️ 技能管理 (Skills)

```bash
openclaw skills list            # 列出所有可用技能
openclaw skills info <技能名>   # 显示技能详情
openclaw skills check           # 检查哪些技能已就绪/缺少依赖
```

---

## 📱 设备配对 (Devices & Pairing)

### 设备管理
```bash
openclaw devices list           # 列出待处理和已配对的设备
openclaw devices approve        # 批准待处理的配对请求
openclaw devices reject         # 拒绝待处理的配对请求
openclaw devices remove         # 移除已配对的设备
openclaw devices clear          # 清除配对设备表
openclaw devices revoke         # 撤销角色的设备令牌
openclaw devices rotate         # 轮换角色的设备令牌
```

### 安全 DM 配对
```bash
openclaw pairing list           # 列出待处理的配对请求
openclaw pairing approve        # 批准配对码并允许发送者
```

### 生成配对二维码
```bash
openclaw qr                     # 生成 iOS 配对二维码和设置码
openclaw qr --json              # JSON 输出
openclaw qr --setup-code-only   # 仅输出设置码
openclaw qr --remote            # 使用 gateway.remote.url 和令牌
```

---

## 🌍 目录查询 (Directory)

```bash
# 自我查询
openclaw directory self --channel <频道>  # 显示当前账户身份

# 联系人查询
openclaw directory peers list --channel <频道> --query "名字"  # 搜索联系人

# 群组查询
openclaw directory groups list --channel <频道>           # 列出群组
openclaw directory groups members --channel <频道> --group-id <ID>  # 列出成员
```

---

## 🔐 安全审计 (Security)

```bash
openclaw security audit         # 运行本地安全审计
openclaw security audit --deep  # 包含实时网关探测检查
openclaw security audit --fix   # 应用安全修复和权限修复
openclaw security audit --json  # JSON 输出
```

---

## 🔄 更新管理 (Update)

```bash
openclaw update                 # 更新 OpenClaw
openclaw update status          # 显示更新渠道和版本状态
openclaw update wizard          # 交互式更新向导

# 选项
openclaw update --channel stable|beta|dev  # 切换更新渠道
openclaw update --tag <标签 | 版本>        # 一次性更新到指定版本
openclaw update --dry-run       # 预览操作（不实际更改）
openclaw update --no-restart    # 更新后不重启网关
openclaw update --json          # JSON 输出
openclaw update --yes           # 非交互式（接受降级提示）
```

---

## 📦 Node 节点管理

```bash
openclaw node run               # 前台运行无头节点主机服务
openclaw node status            # 检查节点主机状态
openclaw node install           # 安装节点主机服务
openclaw node stop              # 停止节点主机服务
openclaw node restart           # 重启节点主机服务
openclaw node uninstall         # 卸载节点主机服务
```

---

## 🧪 沙箱管理 (Sandbox)

```bash
openclaw sandbox list           # 列出沙箱容器及其状态
openclaw sandbox list --browser # 仅列出浏览器容器
openclaw sandbox recreate --all # 重建所有容器
openclaw sandbox recreate --session <会话>  # 重建指定会话
openclaw sandbox recreate --agent <Agent>   # 重建 Agent 容器
openclaw sandbox explain        # 解释有效的沙箱配置
```

---

## 🔗 Webhooks 集成

```bash
openclaw webhooks gmail         # Gmail Pub/Sub 钩子（通过 gogcli）
```

---

## 🪝 Hooks 管理

```bash
openclaw hooks list             # 列出所有钩子
openclaw hooks info <钩子名>    # 显示钩子详情
openclaw hooks check            # 检查钩子资格状态
openclaw hooks install <路径>   # 安装钩子包
openclaw hooks update           # 更新已安装钩子
openclaw hooks enable           # 启用钩子
openclaw hooks disable          # 禁用钩子
```

---

## 🌐 DNS 助手

```bash
openclaw dns setup              # 设置 CoreDNS 服务于发现域名（广域 Bonjour）
```

---

## 📊 系统工具

```bash
openclaw system event           # 入队系统事件并触发心跳
openclaw system heartbeat       # 心跳控制
openclaw system presence        # 列出系统存在条目
```

---

## ✅ Exec 审批管理

```bash
openclaw approvals get          # 获取 exec 审批快照
openclaw approvals set          # 用 JSON 文件替换 exec 审批
openclaw approvals allowlist    # 编辑每 Agent 允许列表
```

---

## 🔧 配置管理

```bash
openclaw config                 # 启动交互式配置向导
openclaw config get <key>       # 获取配置值
openclaw config set <key> <值>  # 设置配置值
openclaw config unset <key>     # 删除配置值
```

---

## 🏥 健康检查与诊断

```bash
openclaw doctor               # 健康检查 + 快速修复
openclaw health               # 从运行中的网关获取健康状态
openclaw logs                 # 追踪网关文件日志
openclaw status               # 显示频道健康和最近会话接收者
openclaw dashboard            # 打开控制 UI（使用当前令牌）
openclaw tui                  # 打开连接到网关的终端 UI
```

---

## 🎯 常用场景

### 场景 1：首次设置
```bash
openclaw configure            # 交互式设置向导
openclaw gateway start        # 启动网关
openclaw channels login       # 登录频道
openclaw memory index         # 建立记忆索引
```

### 场景 2：日常使用
```bash
openclaw gateway status       # 检查网关状态
openclaw memory index         # 更新索引
openclaw sessions             # 查看会话
openclaw cron list            # 查看定时任务
```

### 场景 3：调试问题
```bash
openclaw doctor                       # 健康检查
openclaw gateway status --verbose     # 详细网关状态
openclaw channels logs                # 查看频道日志
openclaw --log-level trace agent      # 追踪级别日志运行 Agent
```

### 场景 4：开发测试
```bash
openclaw --dev gateway                # 开发模式运行网关
openclaw --dev agent                  # 开发模式运行 Agent
openclaw gateway run --force          # 强制重启网关
openclaw sandbox recreate --all       # 重建所有沙箱
```

### 场景 5：安全审计
```bash
openclaw security audit               # 运行安全审计
openclaw security audit --fix         # 应用修复
openclaw devices list                 # 检查配对设备
```

### 场景 6：更新维护
```bash
openclaw update status                # 检查更新状态
openclaw update                       # 执行更新
openclaw update --channel beta        # 切换到测试渠道
openclaw plugins update               # 更新插件
openclaw hooks update                 # 更新钩子
```

---

## 📖 文档链接

- **官方文档**: https://docs.openclaw.ai
- **CLI 文档**: https://docs.openclaw.ai/cli
- **社区 Discord**: https://discord.com/invite/clawd
- **ClawHub（技能市场）**: https://clawhub.com
- **GitHub 源码**: https://github.com/openclaw/openclaw

---

## 🔑 快速参考表

| 类别 | 常用命令 |
|------|----------|
| **网关** | `gateway status/start/stop/restart` |
| **Agent** | `agents list/agent` |
| **频道** | `channels list/login/status` |
| **消息** | `message send/read/react` |
| **记忆** | `memory status/index/search` |
| **浏览器** | `browser status/start/screenshot/snapshot` |
| **会话** | `sessions [--active 分钟]` |
| **定时** | `cron list/add/run` |
| **模型** | `models list/set/scan` |
| **插件** | `plugins list/install/update` |
| **技能** | `skills list/info/check` |
| **安全** | `security audit` |
| **更新** | `update status/update` |
| **诊断** | `doctor/health/logs` |

---

*最后更新：2026-02-27*
