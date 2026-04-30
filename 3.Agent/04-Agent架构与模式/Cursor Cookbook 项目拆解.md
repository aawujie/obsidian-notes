# Cursor Cookbook 项目拆解

> 仓库: [cursor/cookbook](https://github.com/cursor/cookbook) | 1255 stars | TypeScript 95%
> 创建: 2026-04-27 | 4 贡献者 (cursoragent, leerob 等)

---

## 项目定位

Cursor 官方的 SDK 示例厨房——用 4 个小项目展示怎么在自己的应用里嵌入 Cursor 的 Coding Agent。

**核心依赖**: `@cursor/sdk` (TypeScript API)——通过几行代码创建 Agent、发 prompt、stream 结果。

---

## 项目结构

```
sdk/
├── quickstart/          # 1. 最小示例 (6 文件, ~20 行核心代码)
├── coding-agent-cli/    # 2. 终端 CLI (带 TUI 界面)
├── app-builder/         # 3. Web 应用构建器 (Next.js + iframe 预览)
└── agent-kanban/        # 4. Cloud Agent 看板 (Linear 风格)
```

---

## 示例拆解

### 1. quickstart — 最小起点

**一句话**: 创建 Agent → 发一句话 → 流式输出结果。

```typescript
const agent = await Agent.create({
  apiKey: process.env.CURSOR_API_KEY,
  model: { id: "composer-2" },
  local: { cwd: process.cwd() },  // 在当前目录工作
})

const run = await agent.send("Explain this project in one paragraph.")
for await (const event of run.stream()) { /* 打印文本 */ }
await run.wait()
```

**技术栈**: Node.js + TypeScript，零框架依赖。
**学什么**: SDK 最基本的调用模式——`create` → `send` → `stream` → `wait`。

---

### 2. coding-agent-cli — 终端交互

**一句话**: 把 Agent 塞进终端，支持 local/cloud 切换 + 模型选择。

**核心设计**:
- `CodingAgentSession` 类——封装 Agent 生命周期（创建/切换模式/重置/销毁）
- 支持两种执行模式:
  - `local`: 在本地 cwd 跑（`Agent.create({ local: { cwd } })`）
  - `cloud`: 云端跑，自动检测 git remote URL（`Agent.create({ cloud: { repos } })`）
- TUI 界面用的 OpenTUI (Bun native renderer)
- 命令系统: `/local` `/cloud` `/model` `/reset`

**技术栈**: Bun + TypeScript + OpenTUI
**学什么**: Agent 会话管理、local/cloud 切换、模型列表拉取（`Cursor.models.list`）。

---

### 3. app-builder — Web 应用构建器

**一句话**: 一个能直接"建 App"的聊天应用——Agent 在后台写代码，前端 iframe 实时预览。

**工作流**:
```
用户输入 "做个待办事项App"
→ Agent.create({ local: { cwd: projectPath } })
→ agent.send(buildPrompt("做个待办事项App"))
→ stream 事件（thinking / tool_call / assistant_delta）
→ npm create vite + 热更新
→ iframe 预览 http://127.0.0.1:{port}
```

**核心架构** (`src/lib/app-builder/server.ts`):
- `createSession(apiKey)` → 创建独立项目目录 + 分配端口 + 启动 Vite dev server
- `streamAgentResponse(sessionId, message)` → 把用户消息发给 Agent，流式返回
- `generateProjectName(sessionId, context)` → 用 AI 自动给项目起名（XML 标签解析）
- 模型配置编码: 把 `effort`/`thinking`/`fast` 等参数编码进 model id 字符串

**技术栈**: Next.js + React + shadcn/ui + @cursor/sdk
**学什么**: 多 session 管理（Map-based）、iframe 预览热更新、AI 辅助命名、SDK 模型参数编码。

---

### 4. agent-kanban — Cloud Agent 看板

**一句话**: Linear 风格的看板，管理 Cursor Cloud Agents 的状态、artifacts、PR。

**核心功能**:
- **列表**: `Agent.list({ runtime: "cloud" })` → 按状态/repo/branch 分组
- **创建**: `Agent.create({ cloud: { repos, autoCreatePR } })` → 自动开 PR
- **Artifact 预览**: 图片/视频卡片预览，通过本地 API route 代理鉴权
- **Repository 管理**: `Cursor.repositories.list` 拉取 + 内存缓存 (55s TTL)

**数据流**:
```
API route (Next.js) → server.ts (SDK 封装) → @cursor/sdk → Cursor Cloud API
     ↑                      ↑
  React 组件          请求鉴权 + 缓存
```

**技术栈**: Next.js + React + shadcn/ui + @cursor/sdk
**学什么**: Cloud Agent 批量管理、artifact 鉴权代理、REST API 封装模式。

---

## SDK API 速查（从源码反推）

```typescript
// Agent
Agent.create({ apiKey, model, local?: { cwd, force, envVars }, cloud?: { repos, autoCreatePR } })
Agent.list({ apiKey, runtime: "cloud", limit, cursor, includeArchived })
agent.send(prompt)           → Run
agent.listArtifacts()        → artifacts
agent.downloadArtifact(path) → bytes | URL

// Run
run.stream()  → AsyncIterable<SDKMessage>
run.wait()    → { status, durationMs, usage }
run.cancel()  → void
run.supports("cancel") → boolean

// Cursor
Cursor.me({ apiKey })           → { name, email }
Cursor.models.list({ apiKey })  → SDKModel[]
Cursor.repositories.list(...)   → repos
```

**SDKMessage 类型**: `assistant` | `thinking` | `tool_call` | `status` | `task`

---

## 通用模式总结

| 模式 | 出现在 | 做法 |
|------|--------|------|
| **Session 管理** | CLI / app-builder / kanban | Map<string, Session> 存内存，apiKey 持久化到本地 JSON |
| **API Key 流程** | app-builder / kanban | 首次输入 → validate (Cursor.me) → 存本地 `~/.xxx/settings.json` |
| **Stream 处理** | 全部 | `for await (const event of run.stream())` + switch event.type |
| **Agent 销毁** | 全部 | `agent[Symbol.asyncDispose]()` 或 `agent.close()` |
| **错误分类** | app-builder / kanban | 自定义 Error 子类 + `code` 字段，前端按 code 处理 |

---

## 上手路径

1. 先跑 **quickstart** — 理解 `create → send → stream` 循环
2. 再看 **coding-agent-cli** — 理解 local vs cloud 模式切换
3. 深入 **app-builder** — 理解真实 Web 应用集成（session 管理、iframe 预览）
4. 最后 **agent-kanban** — 理解 Cloud Agent 批量管理

> 全部用 `pnpm install && pnpm dev` 启动，需要 `CURSOR_API_KEY=crsr_...`。

---

## 相关笔记

- [[CLI-Anything 让软件 Agent 化]] — Agent 嵌入工具的通用思路
- [[OpenClaw多Agent调度实战]] — 多 Agent 编排对比
