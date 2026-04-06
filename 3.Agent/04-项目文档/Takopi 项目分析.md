# Takopi 项目分析

**创建时间**: 2026-03-03  
**来源**: https://github.com/banteg/takopi  
**标签**: #AI-Agent #Telegram #开发工具 #多Agent 调度

---

## 🎯 项目概述

**Takopi** 是一个 Telegram 桥接工具，用于连接和管理多个 AI 编程助手（Codex、Claude Code、OpenCode、Pi）。

**核心口号**: *"he just wants to help-pi!"* 🐙

---

## 🔑 核心功能

| 功能 | 说明 |
|------|------|
| **多项目管理** | 同时处理多个 repo/分支，分支作为 git worktrees 管理 |
| **无状态恢复** | 在聊天中继续会话，或复制 resume 行在终端恢复 |
| **进度流** | 实时 streaming 命令、工具调用、文件变更、耗时 |
| **并行运行** | 支持多个 Agent 会话并行执行，每个会话独立队列 |
| **Telegram 集成** | 支持语音消息、定时消息、群组聊天、话题映射 |
| **文件传输** | 发送文件到 repo 或取回文件/目录 |
| **多引擎支持** | 通过 `/codex`、`/claude`、`/opencode`、`/pi` 切换引擎 |

---

## 🏗️ 架构层次

```
CLI 层 → 插件层 → 编排层 → 桥接层 → Runner 层 → 传输层 → 外部 Agent CLI
```

| 层级 | 组件 | 职责 |
|------|------|------|
| **CLI** | `cli.py` | 入口点、配置加载、锁文件 |
| **插件** | `plugins.py`, `engines.py` | 入口点发现、插件懒加载 |
| **编排** | `router.py`, `scheduler.py` | 引擎选择、任务队列 |
| **桥接** | `telegram/bridge.py` | 消息处理、执行协调 |
| **Runner** | `runner.py`, `runners/*.py` | Agent CLI 子进程、JSONL 解析 |
| **传输** | `telegram/client.py` | Telegram API、消息渲染 |

---

## 🔧 工作原理

### 1️⃣ 消息接收与解析

```
用户发送 Telegram 消息
    ↓
Takopi Bot 轮询接收
    ↓
解析指令：/项目名 @分支 引擎 命令
    ↓
提取 Resume Token（如果有）
```

**指令格式示例：**
- `/happy-gadgets @feat/login 修复登录 bug`
- `/codex 帮我写测试`
- 回复某条消息 → 自动提取 resume token 继续会话

---

### 2️⃣ 上下文解析

| 元素 | 解析方式 | 作用 |
|------|----------|------|
| **项目** | `/项目名` | 定位 git repo 路径 |
| **分支** | `@分支名` | 自动创建/切换到 git worktree |
| **引擎** | `/claude` `/codex` 等 | 选择后端 Agent CLI |
| **Resume** | 回复消息中的 token | 恢复之前的会话上下文 |

---

### 3️⃣ 任务调度

```
ThreadScheduler（线程调度器）
    ↓
每个聊天线程 = 独立队列
    ↓
同线程消息 → 顺序执行（保持上下文）
不同线程 → 并行执行（互不阻塞）
    ↓
Worker 调用 Runner.run()
```

---

### 4️⃣ Agent 执行

```bash
# 以 Claude 为例
claude --print --output-format stream-json --resume abc123 "修复登录 bug"
```

**关键点：**
- 启动 Agent CLI 作为**子进程**
- 监听 stdout 的 **JSONL 流**
- 使用 `msgspec` 高效解码每条事件
- 转换为统一的 `TakopiEvent` 格式

---

### 5️⃣ 进度 Streaming

```
Agent CLI 输出 JSONL 事件
    ↓
Runner 解码并转换为 TakopiEvent
    ↓
RunnerBridge 编辑 Telegram 消息
    ↓
用户看到实时进度（工具调用、文件变更、耗时）
    ↓
完成后发送最终答案，删除进度消息
```

**事件类型：**
- `started` - 会话开始
- `action` - 工具调用/文件变更/命令执行
- `completed` - 会话完成，带答案和新的 resume token

---

### 6️⃣ 会话恢复机制

```
完成时生成 Resume Token
    ↓
附加到最终消息：claude --resume abc123
    ↓
用户回复时自动提取 token
    ↓
下次调用带上 --resume abc123
    ↓
Agent 继续之前的上下文
```

---

### 7️⃣ Git Worktree 管理

```
用户指定 @分支名
    ↓
检查 worktree 是否存在
    ↓
不存在则创建：git worktree add .worktrees/feat-login feat/login
    ↓
在该 worktree 中运行 Agent
    ↓
分支隔离，互不干扰
```

---

## 📐 架构优势

| 设计 | 好处 |
|------|------|
| **插件化** | 轻松添加新引擎/传输/命令 |
| **流式处理** | 用户不用等待，实时看到进度 |
| **线程队列** | 同对话顺序执行，保持上下文连贯 |
| **Resume Token** | 会话可移植，可在终端/聊天任意恢复 |
| **Worktree 隔离** | 多分支并行开发不冲突 |

---

## 🚀 使用流程

```bash
# 安装
uv tool install -U takopi

# 运行并跟随设置向导
takopi

# 在项目目录中运行
cd ~/dev/happy-gadgets
takopi
```

---

## 📁 代码结构

```
takopi/
├── src/takopi/
│   ├── cli/              # CLI 命令
│   ├── runners/          # 各引擎 Runner
│   ├── schemas/          # JSONL Schema 解码器
│   ├── telegram/         # Telegram 集成
│   ├── router.py         # 自动路由
│   ├── scheduler.py      # 线程调度器
│   ├── config.py         # 配置管理
│   └── runner.py         # Runner 协议
├── docs/                 # 完整文档
└── pyproject.toml        # Python 项目配置
```

---

## 🔗 相关链接

- **GitHub**: https://github.com/banteg/takopi
- **官网**: https://takopi.dev/

---

## 💡 启发与思考

1. **Agent 编排层** 是个有价值的方向 —— 不是替代 Agent，而是让它们更好地协作
2. **流式反馈** 极大提升用户体验，避免"黑盒等待"
3. **会话恢复** 机制让上下文可移植，打破单一平台限制
4. **Telegram 作为 UI** 轻量化，适合移动场景

---

*笔记由 OpenClaw 自动整理*
