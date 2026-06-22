# Lark Coding Agent Bridge 完整教程

> 把 Claude Code 和 Codex 接入飞书，让 Coding Agent 成为飞书 Bot
>
> **Repo**: <https://github.com/zarazhangrui/lark-coding-agent-bridge>
>
> **更新日期**: 2026-06-22

---

## 一、简介

Lark Coding Agent Bridge 是一个桥接工具，可以把本地的 Claude Code 和 Codex 桥接到飞书/Lark 里，让它们成为飞书中的一个 bot。你可以像跟同事聊天一样，无缝与 Claude Code/Codex 协作。

**核心价值**：把 Coding Agent 从 Terminal 解放出来，融入飞书协作工作流。

---

## 二、快速开始

### 前置条件

- 已安装 Node.js（npx 可用）
- 已安装 Claude Code 或 Codex
- 有飞书/Lark 账号

### 安装 Lark CLI（推荐）

```bash
# 安装 Lark CLI
brew install larksuite/cli/lark
```

仓库：<https://github.com/larksuite/cli>

### 一行命令启动 Bridge

```bash
npx -y lark-channel-bridge@latest start
```

首次启动会引导你完成飞书应用配置（App ID / Secret 等），之后即可在飞书里跟你的 Coding Agent 对话。

### 升级

```bash
npx -y lark-channel-bridge@latest start
```

直接重新运行即可自动升级到最新版本。

---

## 三、核心功能

### 3.1 📱 移动端无缝协作

工作不再绑定在工位，可以在手机上跟 Claude Code/Codex 聊天，支持语音输入。

> **Mac 用户建议**：搭配 [Amphetamine](https://apps.apple.com/us/app/amphetamine/id937984704?mt=12) 使用，让电脑合盖时也保持 always on、永不休眠。

### 3.2 🗂️ 多 Session 管理

**用飞书会话取代 Terminal Tabs：**

| 概念 | 对应 |
|------|------|
| 一个群 | 一个 Project |
| 一个 Thread（话题/跟帖） | 一个 Session |
| `/new chat <话题>` | 自动创建新群聊 |

**优于 Terminal 的点：**
- 不再被一堆 Terminal Tab 搞乱
- 所有 session 一目了然
- 可以给群加标签，方便分类查找

### 3.3 🎨 富文本 / 多媒体沟通

Coding Agent 可以突破纯文字限制：

- ✅ **图文混排**消息
- ✅ **表格**渲染输出
- ✅ **长图**直接在飞书查看
- ✅ **飞书交互卡片**（按钮、选择器等）

### 3.4 🃏 可交互的飞书卡片

Agent 可以发送带按钮的交互卡片，而不是让你打字选择：

- 多选题 → 点按钮
- 确认操作 → 一键确认
- 状态切换 → 卡片内操作

比纯文本交互更符合直觉。

### 3.5 📄 飞书文档取代 Markdown

Agent 可以直接输出飞书文档，而不是 Markdown：

- 文档更易读、排版更好
- 反馈时直接**划词评论**，不需要手动描述"第几段第几行"
- 支持多人协作审阅

### 3.6 ↩️ 消息一键转发

飞书里收到的消息（用户反馈、Leader 布置的任务等），可以直接**合并转发**给 Claude Code/Codex 处理，不需要手动复制或截图。

### 3.7 💾 聊天记录完整留存

- 所有聊天记录保存在飞书，方便检索、回顾、分享
- 不依赖 Terminal 历史
- 可以合并转发 brainstrom 过程给同事

---

## 四、斜杠命令速查

在飞书里直接发斜杠命令即可生效。

### ⚙️ 偏好设置

| 命令 | 说明 |
|------|------|
| `/config` | 表单调整：消息回复方式（卡片/纯文本）、工具调用显示、并发上限、是否需要 @bot 才回复 |
| `/timeout <N>` | 当前 session 探活时间（分钟），优先级高于全局配置 |
| `/timeout off` | 关闭当前 session 探活 |
| `/timeout default` | 恢复跟随全局配置 |
| `/account` | 查看当前应用 |
| `/account change` | 换 App ID / Secret 并热重连 |

### 🗂️ 会话管理

| 命令 | 说明 |
|------|------|
| `/new` 或 `/reset` | 清空当前会话，从零开始 |
| `/new chat <名字>` | 新建一个群（自动拉你和 bot），继承当前工作目录后开新会话 |
| `/resume <N>` | 列出最近 N 个历史会话，点按钮一键恢复 |
| `/status` | 当前 cwd / session / agent 状态卡片 |
| `/help` | 命令速查卡片 |

### 📁 工作目录 & 工作空间

| 命令 | 说明 |
|------|------|
| `/cd <路径>` | 切换 Claude 的工作目录（会重置 session） |
| `/ws list` | 列出所有命名工作空间（卡片+按钮） |
| `/ws save <名字>` | 把当前 cwd 存为命名工作空间 |
| `/ws use <名字>` | 切到指定命名工作空间 |
| `/ws remove <名字>` | 删除命名工作空间 |

### ⏹️ 运行控制

| 命令 | 说明 |
|------|------|
| `/stop` | 终止当前正在跑的 Claude 任务 |
| `/reconnect` | 强制重连 WebSocket（网络抖动后 bot 没反应时用） |

### 🧭 进程管理

| 命令 | 说明 |
|------|------|
| `/ps` | 列出本机所有 lark-channel-bridge 进程，标识当前回复的是哪个 |
| `/exit <id\|#>` | 终止指定进程（关自己=graceful 退出；关别人=SIGTERM） |

### 🩺 诊断

| 命令 | 说明 |
|------|------|
| `/doctor <描述>` | 把最近日志+你的故障描述喂给 Claude 自助诊断，返回可能原因/关键日志/建议下一步 |

---

## 五、多 Profile：分别运行 Claude 和 Codex

默认情况下，bridge 使用当前激活的 profile。每个 profile 维护独立的应用凭据、会话、工作目录和日志。

### 创建多个 Profile

```bash
# 启动 Claude profile
lark-channel-bridge start --profile claude --agent claude

# 启动 Codex profile
lark-channel-bridge start --profile codex --agent codex
```

### 管理 Profile

```bash
# 重启特定 profile 的 bot
lark-channel-bridge restart --profile codex

# 查看 profile 状态
lark-channel-bridge status --profile codex
```

---

## 六、Claude 计费说明

> ⚠️ **重要变更（2026年6月15日起生效）**

Bridge 使用 `claude -p` 模式。自 2026 年 6 月 15 日起，Claude 订阅计划对 `claude -p` 和 Agent SDK 的使用**独立计费**，不再占用原有对话额度。

| 订阅档位 | 月度额度 | 月费 |
|----------|---------|------|
| Pro | 基础额度 | $20 |
| Max 5x | 5 倍额度 | $100 |
| Max 20x | 20 倍额度 | $200 |

- 当月未用完不滚存
- 超额需按 API 付费或升级套餐
- 轻度使用无影响；重度使用 `claude -p` 跑脚本的同学可能更快触顶

官方公告：[Use the Claude Agent SDK with your Claude plan](https://claude.ai/help)

---

## 七、常见问题

### Q: 手机上能用吗？
A: 可以。飞书支持语音输入，散步时也能跟 Agent 协作。

### Q: 多个项目怎么管理？
A: 一个群 = 一个 Project，一个 Thread = 一个 Session。用 `/new chat <项目名>` 自动创建新群。

### Q: 聊天记录会丢吗？
A: 不会。所有记录保存在飞书，可以随时检索、回顾、分享。

### Q: Claude Code 和 Codex 能同时用吗？
A: 可以。通过多 profile 分别启动，见第五章。

### Q: 怎么反馈问题？
A: GitHub 提 Issue/PR：<https://github.com/zarazhangrui/lark-coding-agent-bridge>

---

## 八、相关资源

- **GitHub Repo**: <https://github.com/zarazhangrui/lark-coding-agent-bridge>
- **Lark CLI**: <https://github.com/larksuite/cli>
- **Amphetamine**（Mac 防休眠）: <https://apps.apple.com/us/app/amphetamine/id937984704?mt=12>
- **Claude 计费公告**: <https://claude.ai/help>