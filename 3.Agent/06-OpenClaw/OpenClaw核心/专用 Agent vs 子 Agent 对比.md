# 专用 Agent vs 子 Agent 对比

> 创建日期:: 2026-02-27
> 标签:: #OpenClaw #Agent #架构设计 #SubAgent

---

## 🎯 两种方案

### 方案 A：专用 Code Agent

在 `openclaw.json` 中配置独立的代码专家 agent：

```json5
{
  "agents": {
    "list": [
      {
        "id": "main",
        "name": "主 Agent",
        "workspace": "~/.openclaw/workspace/main"
      },
      {
        "id": "code",
        "name": "代码专家",
        "workspace": "~/.openclaw/workspace/code",
        "model": { "primary": "claude-sonnet-4-5-20250929" },
        "identity": {
          "name": "代码助手",
          "emoji": "💻"
        },
        "skills": ["coding-agent", "github", "tmux"]
      }
    ]
  }
}
```

**调用方式**：通过 binding 路由或 `/agents` 切换

---

### 方案 B：通用 Agent + Code Subagent

只有一个通用 agent，需要时 spawn 子 agent：

```json5
{
  "agents": {
    "defaults": {
      "subagents": {
        "model": { "primary": "claude-haiku-3-5" },
        "tools": {
          "allow": ["read", "write", "edit", "exec"],
          "deny": ["gateway", "cron"]
        }
      }
    },
    "list": [
      {
        "id": "main",
        "name": "通用 Agent",
        "workspace": "~/.openclaw/workspace/main",
        "model": { "primary": "claude-sonnet-4-5-20250929" }
      }
    ]
  }
}
```

**调用方式**：`/subagents spawn code "分析这个项目的结构"`

---

## 📊 核心差异对比

| 维度 | 专用 Code Agent | 通用 Agent + Subagent |
|------|-----------------|----------------------|
| **提示词上下文** | 完整（SOUL + IDENTITY + USER + AGENTS + TOOLS） | 仅 AGENTS + TOOLS |
| **人格一致性** | ✅ 独立人格，风格稳定 | ❌ 无人格，纯任务执行 |
| **用户信息** | ✅ 知道 USER.md 中的背景 | ❌ 不知道用户信息 |
| **记忆系统** | ✅ 独立 memory/ 目录 | ❌ 无记忆，会话结束即遗忘 |
| **模型选择** | 固定配置 | 可动态指定（继承/覆盖） |
| **工具权限** | 完整配置 | 受限（默认无 session 工具） |
| **会话隔离** | 独立会话 | 临时会话，自动归档 |
| **成本** | 较高（完整上下文） | 较低（精简上下文） |
| **启动速度** | 较慢（加载完整上下文） | 较快（仅加载必要文件） |
| **适用场景** | 长期项目、复杂协作 | 一次性任务、快速执行 |

---

## 🔍 详细分析

### 1️⃣ 提示词上下文

#### 专用 Code Agent

加载完整的 workspace 文件：

```
~/.openclaw/workspace/code/
├── AGENTS.md       ✅
├── SOUL.md         ✅ 代码专家的行为准则
├── IDENTITY.md     ✅ "我是代码助手 💻"
├── USER.md         ✅ 用户的技术背景、偏好
├── TOOLS.md        ✅ 代码工具配置
├── HEARTBEAT.md    ✅ 定期检查任务
└── memory/         ✅ 长期项目记忆
```

**效果**：
- 有明确的"代码专家"身份认同
- 知道用户是前端/后端/全栈
- 记住用户的技术栈偏好（如"不用 TypeScript"）
- 有持续的项目记忆

#### Subagent

仅加载最小必要文件：

```
~/.openclaw/workspace/main/
├── AGENTS.md       ✅
└── TOOLS.md        ✅
```

**不加载**：
- ❌ SOUL.md（无人格）
- ❌ IDENTITY.md（无身份）
- ❌ USER.md（不知道用户是谁）
- ❌ HEARTBEAT.md（无定期检查）
- ❌ memory/（无长期记忆）

**效果**：
- 纯粹的任务执行者
- 没有"我是谁"的认知
- 不知道用户偏好
- 会话结束即遗忘

---

### 2️⃣ 记忆系统

#### 专用 Code Agent

```
~/.openclaw/workspace/code/memory/
├── 2026-02-27.md    ← 每日日志
├── projects.md      ← 项目状态
└── architecture.md  ← 架构决策记录
```

**优势**：
- ✅ 跨会话记忆
- ✅ 项目演进历史
- ✅ 技术决策可追溯
- ✅ memorySearch 语义检索

#### Subagent

```
无 memory 目录
```

**限制**：
- ❌ 会话结束即遗忘
- ❌ 无法积累项目知识
- ❌ 每次都是"从零开始"

---

### 3️⃣ 模型与成本

#### 专用 Code Agent

```json5
{
  "id": "code",
  "model": { "primary": "claude-sonnet-4-5-20250929" }
}
```

**特点**：
- 固定使用高性能模型
- 适合复杂代码分析、架构设计
- 成本较高但质量稳定

#### Subagent

```json5
{
  "defaults": {
    "subagents": {
      "model": { "primary": "claude-haiku-3-5" }
    }
  }
}
```

**特点**：
- 可使用更便宜的模型
- 适合简单任务（文件读取、格式转换）
- 成本可降低 60-70%

**模型选择优先级**：

```
sessions_spawn 显式指定
       ↓
agents.list[].subagents.model
       ↓
agents.defaults.subagents.model
       ↓
继承父 agent 模型
```

---

### 4️⃣ 工具权限

#### 专用 Code Agent

完整工具配置：

```json5
{
  "id": "code",
  "tools": {
    "allow": ["read", "write", "edit", "exec", "github", "tmux"],
    "exec": {
      "security": "allowlist",
      "safeBins": ["git", "npm", "pnpm"]
    }
  }
}
```

#### Subagent

受限工具配置：

```json5
{
  "defaults": {
    "subagents": {
      "tools": {
        "deny": ["gateway", "cron", "sessions_spawn"]
      }
    }
  }
}
```

**默认限制**：
- ❌ 无 `sessions_spawn`（不能 spawn 子子 agent）
- ❌ 无 `sessions_list/history/send`（无会话工具）
- ❌ 无 `gateway/cron`（无系统工具）

**深度限制**：

| 深度 | 角色 | 工具权限 |
|------|------|----------|
| 0 | Main Agent | 完整工具 |
| 1 | Subagent (leaf) | 无 session 工具 |
| 1 | Subagent (orchestrator, maxSpawnDepth≥2) | +sessions_spawn |
| 2 | Sub-sub-agent | 无 session 工具 |

---

### 5️⃣ 会话生命周期

#### 专用 Code Agent

```
创建 → 长期存在 → 多次对话 → 持续记忆
```

- 独立的 session key：`agent:code:main`
- 会话持久化
- 可跨天/跨周持续项目

#### Subagent

```
Spawn → 执行任务 → Announce 结果 → 自动归档 (60 分钟)
```

- 临时 session key：`agent:main:subagent:<uuid>`
- 任务完成即结束
- 自动归档到 `*.deleted.<timestamp>`

---

## 🎯 使用场景推荐

### ✅ 专用 Code Agent 适合

| 场景 | 原因 |
|------|------|
| **长期项目** | 需要记忆项目演进历史 |
| **复杂架构** | 需要理解用户技术偏好 |
| **多轮协作** | 需要人格一致性 |
| **代码审查** | 需要知道团队规范 |
| **技术决策** | 需要记录架构决策 |

**示例**：
```
"帮我重构这个项目的认证模块"
→ 需要知道：
  - 用户的技术栈（Node.js/Python?）
  - 现有架构（记忆中的 projects.md）
  - 历史决策（为什么用 JWT 不用 Session）
  - 团队规范（TOOLS.md 中的约定）
```

---

### ✅ Subagent 适合

| 场景 | 原因 |
|------|------|
| **一次性任务** | 无需长期记忆 |
| **快速查询** | "这个项目有多少个 TypeScript 文件？" |
| **批量处理** | "把所有.md 转成.pdf" |
| **隔离实验** | "试试用不同方式实现这个函数" |
| **并行任务** | 同时分析 5 个不同的 repo |

**示例**：
```
"分析 /Users/apple/code/project 的目录结构"
→ 不需要：
  - 用户偏好
  - 历史记忆
  - 人格一致性
  - 长期跟踪
```

---

## 💰 成本对比

### 场景：每日代码任务

| 方案 | 模型 | Token/天 | 成本/天 | 成本/月 |
|------|------|----------|---------|---------|
| 专用 Agent | Sonnet | 50K | $0.15 | $4.50 |
| Subagent | Haiku | 50K | $0.025 | $0.75 |
| **节省** | - | - | **83%** | **$3.75** |

**策略**：
- 复杂任务 → 专用 Agent（质量优先）
- 简单任务 → Subagent（成本优先）

---

## 🏗️ 混合架构（推荐）

最佳实践是**两者结合**：

```json5
{
  "agents": {
    "defaults": {
      "subagents": {
        "model": { "primary": "haiku" },  // 便宜模型处理简单任务
        "maxSpawnDepth": 2,               // 允许 orchestrator 模式
        "tools": {
          "allow": ["read", "write", "edit", "exec"],
          "deny": ["gateway", "cron"]
        }
      }
    },
    "list": [
      {
        "id": "main",
        "name": "通用 Agent",
        "model": { "primary": "sonnet" }
      },
      {
        "id": "code",
        "name": "代码专家",
        "model": { "primary": "sonnet" },
        "identity": {
          "name": "代码助手",
          "emoji": "💻"
        },
        "skills": ["coding-agent", "github"],
        "memorySearch": {
          "enabled": true  // 启用语义记忆
        }
      }
    ]
  }
}
```

### 工作流

```
用户请求
   ↓
通用 Agent 判断任务类型
   ├─ 复杂/长期 → 路由到 Code Agent
   │              (完整上下文 + 记忆)
   │
   └─ 简单/一次性 → Spawn Subagent
                    (快速执行 + 低成本)
```

---

## 📋 决策清单

### 选择专用 Agent 如果：

- [ ] 任务需要跨会话记忆
- [ ] 需要了解用户技术偏好
- [ ] 需要人格一致性（如代码审查风格）
- [ ] 项目周期 > 1 天
- [ ] 需要记录架构决策

### 选择 Subagent 如果：

- [ ] 一次性任务
- [ ] 不需要知道用户信息
- [ ] 成本敏感
- [ ] 需要并行执行多个任务
- [ ] 任务完成后无需跟踪

---

## 🔗 相关文档

- [OpenClaw Sub-Agents](/tools/subagents)
- [Agent Workspace](/concepts/agent-workspace)
- [Memory Search](/concepts/memory)
- [Configuration Reference](/gateway/configuration-reference)

---

## 💡 实践建议

1. **从通用 Agent 开始** — 初期不要过度设计
2. **观察使用模式** — 记录哪些任务需要长期记忆
3. **逐步拆分** — 当某个领域的任务频繁时，创建专用 Agent
4. **Subagent 用于优化成本** — 简单任务用便宜模型
5. **保持配置简洁** — 避免过早优化
