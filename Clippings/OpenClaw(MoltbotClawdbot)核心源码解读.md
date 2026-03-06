---
title: "OpenClaw(Moltbot/Clawdbot)核心源码解读"
source: "https://zhuanlan.zhihu.com/p/2005243265952277112"
author:
  - "[[时光相机激励·竞争·公平的制度是三驾马车的全部。]]"
published:
created: 2026-03-04
description: "整体工作模式类似Manus，不同之处产品聚焦于个人助理场景，个人电脑环境是Agent的生活环境。 OpenClaw是一款运行在你自己的设备上的个人 AI 助手。它可以通过你常用的渠道（WhatsApp、Telegram、Slack、Discord、G…"
tags:
  - "clippings"
---
目录

收起

一、指挥官/调度(runEmbeddedPiAgent)

1\. 核心工作原理

2\. React 模式的实现原理

3\. Skills (工具) 的使用机制

4\. 记忆管理

5\. 自学习与进化

总结：Agent 的“大脑”结构

二、特种兵/执行器(runEmbeddedAttempt)

1\. runEmbeddedAttempt 的核心定位

2\. 详细工作流程

3\. Skills (工具) 的使用原理：从加载到执行

4\. 结合 runEmbeddedPiAgent 的完整协同视图

5\. 关键设计亮点

三、React模式适用性

1\. 架构定性：概率模型 vs. 状态机

2\. 存在的风险：多步推理中的“幻觉调用”

A. 上下文污染与注意力稀释

B. 缺乏状态锁定

C. 意图漂移

3\. 代码中的缓解机制 (Mitigations in Code)

4\. 改进建议：向“分层/混合架构”演进

方案 A：Router/Planner 模式 (分层)

方案 B：基于语义的动态工具检索 (RAG for Tools)

方案 C：意图槽位/状态机 (State Machine)

总结

**整体工作模式类似Manus，不同之处产品聚焦于个人助理场景，个人电脑环境是Agent的生活环境。**

**OpenClaw** 是一款运行在你自己的设备上的 *个人 AI 助手* 。它可以通过你常用的渠道（WhatsApp、Telegram、Slack、Discord、Google Chat、Signal、iMessage、Microsoft Teams、WebChat）以及 BlueBubbles、Matrix、Zalo 和 Zalo Personal 等扩展渠道为你提供帮助。它支持 macOS/iOS/Android 系统，并可渲染由你控制的实时 Canvas 界面。网关只是控制平台，产品本身才是真正的助手。如果你想要一个感觉像本地助手、速度快、始终在线的单人个人助理，那就是它了。

核心源码： [github.com/openclaw/ope](https://link.zhihu.com/?target=https%3A//github.com/openclaw/openclaw)

指挥官/调度器(runEmbeddedPiAgent)： [src/agents/pi-embedded-runner/run.ts#L137](https://link.zhihu.com/?target=https%3A//github.com/openclaw/openclaw/blob/b912d3992df9d381b10e4d59e8e6eca694f0171a/src/agents/pi-embedded-runner/run.ts%23L137)

特种兵/执行器(runEmbeddedAttempt)： [src/agents/pi-embedded-runner/run/attempt.ts#L141](https://link.zhihu.com/?target=https%3A//github.com/openclaw/openclaw/blob/b912d3992df9d381b10e4d59e8e6eca694f0171a/src/agents/pi-embedded-runner/run/attempt.ts%23L141)

## 一、指挥官/调度(runEmbeddedPiAgent)

这段代码 `runEmbeddedPiAgent` 是 OpenClaw（或类似 Agent 框架）的核心调度器函数。它并不直接执行每一个细微的 LLM 推理步骤，而是作为 **“大脑的指挥官”** ，负责协调资源、管理上下文、处理错误、维护记忆以及驱动 [ReAct](https://zhida.zhihu.com/search?content_id=270277490&content_type=Article&match_order=1&q=ReAct&zhida_source=entity) 循环。

以下是基于代码的详细深度解读：

### 1\. 核心工作原理

`runEmbeddedPiAgent` 的主要职责是 **在一个受控的环境中执行一次 Agent 的交互** 。它的工作流程像是一个健壮的操作系统进程：

- **并发控制 (Lane Management)**:
- 代码首先通过 `resolveSessionLane` 和 `resolveGlobalLane` 确定任务队列。
	- 这是为了防止同一个 Session（会话）同时处理两个请求，导致记忆错乱。它确保了“一次只思考一件事”。
- **上下文与资源检查 (Guardrails)**:
- **[Context Window](https://zhida.zhihu.com/search?content_id=270277490&content_type=Article&match_order=1&q=Context+Window&zhida_source=entity) Guard**: 在调用 LLM 之前，使用 `evaluateContextWindowGuard` 检查当前历史记录是否已经挤爆了模型的上下文窗口。如果太长，它会直接报错或警告，避免浪费 Token 和金钱。
	- **[Auth Rotation](https://zhida.zhihu.com/search?content_id=270277490&content_type=Article&match_order=1&q=Auth+Rotation&zhida_source=entity) (账号轮询)**: 这是该函数最复杂的逻辑之一。它管理 `AuthProfile` （API 密钥配置）。如果一个账号被限流（Rate Limit）或欠费，它会自动切换到下一个可用账号（ `advanceAuthProfile` ），保证服务高可用。
- **执行尝试 (The Attempt Loop)**:
- 核心逻辑包裹在一个 `while(true)` 循环中。这不仅仅是为了重试错误，也是为了处理 **记忆压缩** 和 **自适应降级** 。
	- 它调用 `runEmbeddedAttempt` 。这个函数才是真正构建 Prompt、发送给 LLM、解析 LLM 返回结果的地方。
- **结果处理与标准化**:
- 根据 LLM 的输出，构建标准化的 `payloads` （回复内容）和 `meta` （元数据，包含 Token 使用量、延迟等）。

### 2\. React 模式的实现原理

ReAct (Reasoning + Acting) 是 Agent 思考的核心。虽然 `runEmbeddedPiAgent` 是调度层，但它通过以下方式支持 ReAct：

- **工具调用识别 (Acting)**:
- 当 `runEmbeddedAttempt` 返回时，它会检查 `attempt.clientToolCall` 。
	- 如果在返回结果的 `meta` 中包含 `pendingToolCalls` ，这意味着 Agent 决定“行动”（调用工具），而不是直接“说话”。
	- **流程**: 用户输入 -> LLM 思考 -> LLM 返回工具调用指令 -> `runEmbeddedPiAgent` 捕获该指令 -> 返回给宿主环境 -> 宿主执行工具 -> 结果回填 -> 再次调用 Agent。
- **观察与反馈 (Observation)**:
- 代码中处理了 `toolMetas` 和 `lastToolError` 。这代表了 ReAct 循环中的 “Observation” 步骤。如果工具执行出错，错误信息会被捕获并作为下一轮对话的输入，让 Agent 进行自我修正。

### 3\. Skills (工具) 的使用机制

Skills 在这里被视为 Agent 的“手脚”。

- **快照注入 (Snapshot Injection)**:
- 参数 `params.skillsSnapshot` 将当前可用的工具列表传递进去。这通常是工具的定义（名称、描述、参数 Schema）。
	- `runEmbeddedAttempt` 会将这些 Skills 转化为 LLM 能理解的 `system prompt` 或 `function calling` 定义。
- **执行权限控制**:
- `params.disableTools`: 可以临时禁用工具。
	- `params.bashElevated`: 控制是否允许执行高权限的 Shell 命令（这是一个非常具体的 Skill 控制）。
- **结果格式化**:
- 代码通过 `resolvedToolResultFormat` (markdown 或 plain) 来决定如何将工具的执行结果展示给 LLM 和用户。
- **云端与本地协同**:
- 代码提到了 `[Cloud Code Assist](https://zhida.zhihu.com/search?content_id=270277490&content_type=Article&match_order=1&q=Cloud+Code+Assist&zhida_source=entity)` 和可能的格式错误处理。这说明它支持调用云端 Skill，并且具有容错机制：如果格式不对，它会标记并在重试时进行清理（Sanitize）。

### 4\. 记忆管理

这是该代码最精彩的部分，展示了 **动态记忆维护** 。

- **上下文溢出检测**:
- 如果在执行过程中，LLM 返回了 `isContextOverflowError` （上下文溢出错误），代码不会直接崩溃。
- **自动压缩 (Auto-Compaction)**:

代码逻辑：

```
if (isContextOverflowError(errorText) && overflowCompactionAttempts < 3) {   
    // 触发压缩     
    await compactEmbeddedPiSessionDirect({ ... });     
    // 重试 Prompt 
    continue; 
}
```
- **原理**: 当对话历史太长导致无法继续时，Agent 会调用 `compactEmbeddedPiSessionDirect` 。这个函数会读取历史记录，使用 LLM 将其 **摘要化 (Summarize)** 。
	- **效果**: 将 100 条对话压缩成一段“摘要” + 最近 10 条对话。释放了 Token 空间，让 Agent 能够“记起”很久以前的事，但只保留核心信息，从而继续对话。

### 5\. 自学习与进化

虽然这个脚本不涉及训练神经网络（那叫 Training），但它展示了 **运行时进化 ([Runtime Evolution](https://zhida.zhihu.com/search?content_id=270277490&content_type=Article&match_order=1&q=Runtime+Evolution&zhida_source=entity))** 和 **自适应 (Adaptation)** 行为：

- **思考等级自适应 (Adaptive Thinking Level)**:
- 代码中有 `thinkLevel` 。如果当前的 Model 不支持高等级的思考（例如 DeepSeek R1 模式或 CoT），或者报错，代码会调用 `pickFallbackThinkingLevel` 。
	- **进化点**: 如果 Agent 发现自己想得太复杂导致报错，它会自动“降智”重试，或者切换到更简单的思考模式，以保证任务完成。
- **故障转移 (Failover Intelligence)**:
- 如果遇到 `Rate Limit` (限流)、 `Timeout` (超时) 或 `Auth Failure` ，Agent 不会放弃。
	- 它会记录当前 Profile 的失败（ `markAuthProfileFailure` ），并在 `authStore` 中标记该账号冷却。
	- 然后自动切换到备用账号或备用模型（Fallback Model）。这是一种系统层面的“生存本能”。
- **错误纠正**:
- 针对特定错误（如 Image Size Too Large, Role Ordering Conflict），它有专门的逻辑来处理或给出用户友好的建议。
	- 针对 Cloud Code Assist 的格式错误，它会标记并在下一次尝试中修正工具调用的格式。

### 总结：Agent 的“大脑”结构

通过这段代码，我们可以勾勒出 OpenClaw Agent 的思维模型：

- **感知 (Input)**: 接收用户 Prompt，锁定 Session 队列。
- **前额叶 (Executive Function)**:
- 检查是否有足够的“脑容量”（Context Window）。
	- 选择最佳的“神经通路”（Auth Profile / API Key）。
- **思考与行动 (ReAct Loop - `runEmbeddedAttempt`)**:
- 尝试理解意图。
	- 如果需要外部数据，生成工具调用请求（Pending Tool Call）。
- **海马体 (Memory Consolidation)**:
- 如果发现记不住了（Context Overflow），立刻触发睡眠整理机制（Compaction），把短期记忆转为长期摘要。
- **应激反应 (Resilience)**:
- 遇到阻碍（Error/Timeout），立刻切换策略（降级思考模式）或资源（切换账号）。

这就是一个 Agent 运行时(Runtime)的典型实现：不仅仅是调 API，而是一个包含 **资源调度、容错、记忆维护和策略调整** 的完整系统。

## 二、特种兵/执行器(runEmbeddedAttempt)

如果说 `runEmbeddedPiAgent` 是 **大脑的指挥官（负责策略、资源和生存）** ，那么 `runEmbeddedAttempt` 就是 **执行任务的特种兵（负责具体的战术动作、技能使用和环境交互）** 。

以下是关于 `runEmbeddedAttempt` 的详细工作原理及其与 `runEmbeddedPiAgent` 协同工作的深度解读。

### 1\. runEmbeddedAttempt 的核心定位

`runEmbeddedAttempt` 的作用是 **在一个隔离的、受控的沙盒环境中，执行单一回合的 Agent 交互** 。

它不关心“如果失败了要换哪个账号”或者“历史记录太长要不要压缩”（这是 `runEmbeddedPiAgent` 的事），它只关心：

1. 准备好工作目录（Workspace）。
2. 装配好武器（Skills/Tools）。
3. 加载记忆（Session History）。
4. 构建人设（ [System Prompt](https://zhida.zhihu.com/search?content_id=270277490&content_type=Article&match_order=1&q=System+Prompt&zhida_source=entity) ）。
5. 向 LLM 发起冲锋（Prompting）并拿回结果。

### 2\. 详细工作流程

**第一阶段：环境与沙盒构建**

- **物理隔离**:
- 函数一上来就执行 `fs.mkdir(resolvedWorkspace)` 和 `process.chdir(effectiveWorkspace)` 。
	- **原理**: 强制将 Node.js 进程的 `CWD` (当前工作目录) 切换到用户的 Workspace。这确保了 Agent 执行的所有文件操作（写代码、读文件）都发生在这个目录下，而不是系统根目录。
- **[Sandbox 解析](https://zhida.zhihu.com/search?content_id=270277490&content_type=Article&match_order=1&q=Sandbox+%E8%A7%A3%E6%9E%90&zhida_source=entity)**:
- 调用 `resolveSandboxContext` 。如果配置了沙盒（如 Docker 或隔离环境），它会确定 Agent 实际能触碰到的路径。

**第二阶段：技能装配**

Agent 如何获得“手脚”？

- **加载本地技能**: `loadWorkspaceSkillEntries` 会扫描当前 Workspace 下的特定目录（通常是 `.pi/skills` 或类似），加载用户定义的脚本。
- **加载内置技能**: `createOpenClawCodingTools` 是核心。它创建了一套标准的编码工具（如 `readFile`, `writeFile`, `execCommand` ）。
- *权限控制*: 这里会传入 `bashElevated` ，决定 Agent 是否有权限执行 `sudo` 或高危命令。
- **技能混合**: `splitSdkTools` 将内置工具和自定义工具合并。
- **注入 LLM**: 这些工具最终被转化为 JSON Schema，通过 `tools: builtInTools` 参数传给 `createAgentSession` ，让 LLM 知道它有哪些能力。

**第三阶段：构建“潜意识”**

Agent 为什么知道它是谁？

- **动态构建**: `buildEmbeddedSystemPrompt` 生成一个巨大的 System Prompt。
- **包含内容**:
- **环境感知**: 当前时间、操作系统版本、机器名（由 `runtimeInfo` 提供）。
	- **技能说明书**: `skillsPrompt` 将加载的技能文档化，告诉 LLM “你可以用 `search_web` 来搜索”。
	- **记忆索引**: 告诉 LLM “你可以查看 `memory.md` ”。
- **Hook 介入**: 代码中出现了 `hookRunner.runBeforeAgentStart` 。这允许插件在 Agent 思考前强行插入一段 Prompt（例如：“注意：用户刚才提到他喜欢 Python”）。

**第四阶段：记忆加载与修复**

- **SessionManager**: 这是记忆的管家。它读取 `session.json` 文件，恢复之前的对话历史。
- **历史清洗**:
- `sanitizeSessionHistory`: 移除无效的 Token 或乱码。
	- **Orphaned User Message Repair**: 代码中有一段有趣的逻辑——如果历史记录的最后一条是 User 发的，且当前又要发 User Prompt，它会“移除”掉上一条孤立的消息，防止 `User -> User` 的非法对话顺序（许多 LLM 要求 `User -> Assistant -> User` ）。

**第五阶段：执行与观察 (The Attempt)**

- **视觉增强**: `detectAndLoadPromptImages` 会扫描 Prompt 和历史记录，如果发现图片路径，会将其转为 Base64 或 Image Object 注入给支持 Vision 的模型（如 GPT-4o, Claude 3.5）。
- **发起调用**: `activeSession.prompt(effectivePrompt)` 。这是真正的 LLM 推理时刻。
- **流式订阅**: `subscribeEmbeddedPiSession` 负责监听 LLM 的吐字。它会实时捕获：
- 文本输出。
	- **Tool Calls** (工具调用请求)。
	- 思考过程 (Reasoning/CoT)。

### 3\. Skills (工具) 的使用原理：从加载到执行

结合两份代码，Skill 的生命周期如下：

1. **定义 (Definition)**: 在 `runEmbeddedAttempt` 中， `createOpenClawCodingTools` 定义了 TypeScript 函数（例如 `exec({ command })` ）。
2. **声明 (Declaration)**: 这些函数被转换成 JSON Schema，放入 System Prompt 或 LLM 的 `tools` 参数中。LLM 看到了：“我有一个工具叫 `exec` ，参数是 `command` ”。
3. **决策 (Decision - ReAct 的 “Reasoning”)**: LLM 思考：“用户让我列出文件，我应该调用 `exec` 工具，参数是 `ls -la` ”。 LLM 返回一个特殊的结构： `ToolCall(name="exec", args="{command: 'ls -la'}")` 。
4. **执行 (Execution - ReAct 的 “Acting”)**:
- 这个过程在 `activeSession` 内部或 `subscribeEmbeddedPiSession` 中自动处理。
- Pi Agent 框架（底层库）检测到 ToolCall，匹配到 `runEmbeddedAttempt` 也就是第二阶段定义的那个 TypeScript 函数，并在 Workspace 目录下执行它。

5\. **反馈 (Observation):** 工具执行的结果（例如文件列表的字符串）被捕获，并在下一次 Prompt 中作为 `ToolResult` 角色发回给 LLM。

### 4\. 结合 runEmbeddedPiAgent 的完整协同视图

让我们把两个函数放在一起看，形成一个闭环：

**场景：用户输入 “帮我写一个 Hello World 并运行它”**

- **指挥官 (`runEmbeddedPiAgent`)**:
- 收到任务。
	- 检查账号余额，选择 Claude 3.5 模型。
	- 检查上下文窗口，发现还有空间。
	- 调用 `runEmbeddedAttempt` 。
- **特种兵 (`runEmbeddedAttempt`)**:
- `cd` 到用户目录。
	- 加载 `write_file` 和 `exec` 工具。
	- 读取历史记录（如果是新会话则为空）。
	- 发送 Prompt: “帮我写一个 Hello World 并运行它”。
	- **LLM 思考**: “好的，我需要先写文件。” -> 生成 ToolCall: `write_file("hello.py", "print('Hello')")` 。
	- **框架执行**: 在目录中创建了 `hello.py` 。
	- **LLM 再次思考** (自动或下一轮): “文件写好了，现在我运行它。” -> 生成 ToolCall: `exec("python hello.py")` 。
	- **框架执行**: 运行 Python，捕获输出 “Hello”。
	- **LLM 总结**: “运行成功，输出了 Hello。”
	- `runEmbeddedAttempt` 任务结束，打包结果返回。
- **指挥官 (`runEmbeddedPiAgent`) 回收**:
- 收到结果。
	- 检查是否有报错（如 Context Overflow）。
	- 如果一切正常，更新 Token 统计，标记账号为“健康”。
	- 结束本次运行。

### 5\. 关键设计亮点

1. **自愈性 (Self-Healing)**: `runEmbeddedAttempt` 中的 `repairSessionFileIfNeeded` 和 `Orphaned user message` 逻辑，表明系统可以自动修复损坏的记忆文件或非法的对话顺序，不需要人工干预。
2. **插件化 (Hook System)**: 通过 `getGlobalHookRunner` ，系统允许外部代码在 `before_agent_start` 和 `agent_end` 介入。这为“短期记忆注入”或“运行后分析”提供了接口。
3. **视觉原生 (Native Vision)**: 代码显式处理了 `injectHistoryImagesIntoMessages` 。这意味着 Agent 不仅能看当前的图，还能“回忆”起两轮对话前用户发的图。这是通过在发送给 LLM 的消息列表中回填 Image Object 实现的。
4. **原子化锁 (Session Locking)**: `acquireSessionWriteLock` 确保了在多线程或多进程环境下，不会有两个 Agent 同时修改同一个 `session.json` 文件，防止记忆错乱。

总结来说， `runEmbeddedAttempt` 是一个高度封装的、具有上下文感知能力的执行单元，它通过标准化的接口与 LLM 通信，并通过文件系统和工具集与物理世界交互。

## 三、React模式适用性

React模式不支持显式的判断意图并根据意图进行路由处理的逻辑，对于过程复杂的多步推理SOP任务，这种方式可能否存在意图一致性的问题，比如LLM幻觉调用其它隐式意图范畴下的skill或者出现调用的流程不遵循潜在的workflow流程要求。

目前的 `runEmbeddedPiAgent` 和 `runEmbeddedAttempt` 设计采用了一种 **“大一统” (Monolithic / Flat)** 的上下文管理方式，而不是 **分层/路由 (Hierarchical / Router-based)** 的架构。

从 Agent 架构设计的角度来看，这种设计存在 **意图一致性 (Intent Consistency)** 和 **SOP (Standard Operating Procedure) 执行偏移** 的风险。

### 1\. 架构定性：概率模型 vs. 状态机

当前的架构可以定义为 **“基于提示词工程的 ReAct 单体架构”** 。

- **隐式意图 (Implicit Intent)**: 它没有一个显式的分类器（Classifier）去判断“用户现在想要写代码”还是“用户想要画图”。它把所有可用的 Skill（工具）的定义全部扔进 Context Window（上下文窗口），依赖 LLM 自身的 Attention 机制去“注意”到正确的工具。
- **依赖模型智力**: 这种架构的稳定性极度依赖底座模型（Base Model）的能力（如 Claude 3.5 Sonnet 或 GPT-4o）。它假设模型足够聪明，能够在噪音中提取信号。

### 2\. 存在的风险：多步推理中的“幻觉调用”

在复杂的 SOP 场景下（例如：先搜索数据 -> 清洗数据 -> 存入数据库 -> 发送邮件），这种设计存在以下严重隐患：

### A. 上下文污染与注意力稀释

当 Agent 加载了 50 个工具（涵盖 Coding, AWS, HR, Slack 等），而当前的 SOP 只需要其中 3 个时：

- **干扰项**: 其它 47 个工具的定义占据了大量的 Token。
- **幻觉风险**: 如果用户指令稍微模糊（例如“把这个发出去”），LLM 可能会错误调用 `slack_send` 而不是 SOP 要求的 `email_send` ，仅仅因为这两个工具都在上下文里。
- **案例**: 在做数据清洗时，如果上下文里有一个 `delete_file` 工具，模型可能在遇到错误时为了“解决报错”而错误地删除了源文件，而不是修复代码。

### B. 缺乏状态锁定

在标准的 SOP 执行中，通常需要 **状态机 (FSM)** 来约束：

- *State 1*: 只能用 `Search` 工具。
- *State 2*: 只能用 `Process` 工具。

当前的 `runEmbeddedAttempt` 并没有这种状态锁。在任何一步，Agent 都可以访问所有工具。

- **跳步风险**: 模型可能觉得步骤 2 太难，直接尝试步骤 5 的工具。
- **回环死锁**: 模型可能在步骤 3 失败了，又退回去不断调用步骤 1 的工具，陷入死循环。

### C. 意图漂移

在长对话中，随着 Context Window 的滑动或压缩（Compaction），原本的 SOP 指令可能被挤到后面，或者被中间的报错信息冲淡。

- **后果**: Agent “忘记”了它正在执行一个严格的流程，退化成了一个普通的聊天机器人，开始随意调用工具。

### 3\. 代码中的缓解机制 (Mitigations in Code)

虽然架构是扁平的，但代码中包含了一些机制试图缓解这个问题，尽管它们不是完美的解决方案：

- **动态技能快照 (`params.skillsSnapshot`)**:
- 在 `runEmbeddedAttempt` 中，它允许传入 `skillsSnapshot` 。
	- **设计意图**: 上层调用者（如果有的话）其实可以先判断意图，然后只传入“该意图所需的工具子集”。
	- **现状**: 只要上层没做这个判断，默认就是加载 Workspace 下的所有工具。
- **思考等级 (`thinkLevel`)**:
- 代码支持 `thinkLevel` (Reasoning Level)。
	- **作用**: 强制模型在 Action 之前进行 CoT (Chain of Thought)。在思考阶段，模型更有可能自我纠正：“我虽然看到了 HR 工具，但我现在的任务是写代码，所以我应该忽略它。”
- **Hook 注入 (`hookRunner`)**:
- `runEmbeddedAttempt` 允许 `before_agent_start` 注入 Prompt。
	- **SOP 补丁**: 你可以通过 Hook 强行在 System Prompt 后面追加：“你当前正在执行 SOP 流程 X，目前在第 3 步， **严禁** 使用非相关工具。” 这是一种“软约束”。

### 4\. 改进建议：向“分层/混合架构”演进

如果为了解决复杂 SOP 的一致性问题，Agent 架构通常会向以下方向演进：

### 方案 A：Router/Planner 模式 (分层)

在 `runEmbeddedPiAgent` 之前增加一个 **Planner Agent** 。

- **Planner**: 接收用户请求，生成一个 DAG (有向无环图) 计划。
- *Plan*: Step 1 (Search), Step 2 (Coding).
- **Executor**: `runEmbeddedAttempt` 每次只执行 Plan 中的一步。
- **动态加载**: 在执行 Step 1 时，只挂载搜索工具；执行 Step 2 时，只挂载编码工具。
- *优点*: 彻底解决工具干扰和幻觉调用。
- *缺点*: 延迟高，不够灵活（难以应对计划外的突发情况）。

### 方案 B：基于语义的动态工具检索 (RAG for Tools)

如果工具有几百个，不能全塞进去。

1. 在 `runEmbeddedAttempt` 内部，先根据 User Prompt 做一次 Embedding 检索。
2. 从向量数据库中取出最相关的 Top-5 工具。
3. 只把这 5 个工具放入 `tools` 参数。
- *优点*: 保持单层架构，但大幅减少上下文污染。
- *缺点*: 如果检索失败（漏掉了关键工具），Agent 就彻底傻了。

### 方案 C：意图槽位/状态机 (State Machine)

在 System Prompt 中引入 **“Phase” (阶段)** 的概念，并要求 Agent 输出当前阶段。

- 强制 Agent 在返回 `payload` 时包含 `current_phase: "data_cleaning"` 。
- 代码层检查：如果 `current_phase` 是 `data_cleaning` ，拦截所有非相关工具的调用请求（在 `subscribeEmbeddedPiSession` 层做拦截）。

### 总结

目前的 `runEmbeddedPiAgent` 设计是 **通用型 (General-Purpose)** 的，它牺牲了“严格的一致性”来换取“最大的灵活性”和“最小的开发复杂度”。

对于 **开放式探索任务** （如：帮我写个贪吃蛇游戏），这种设计是优秀的，因为模型需要在写代码、运行、调试之间自由切换，很难预定义 SOP。

对于 **严谨的业务流程** （如：银行转账、服务器运维 SOP），这种设计是 **不安全** 的。如果你需要处理后者，必须在上层增加 **Planner** 或在底层增加 **工具权限范围控制 (Scope Guard)** 。

  

参考：

1、Anthropics Skills规范： [github.com/anthropics/s](https://link.zhihu.com/?target=https%3A//github.com/anthropics/skills) 、 [agentskills.io/what-are](https://link.zhihu.com/?target=https%3A//agentskills.io/what-are-skills)

2、AgenticFlow Skills： [agenticflow-skill/SKILL.md](https://link.zhihu.com/?target=https%3A//github.com/openclaw/skills/blob/main/skills/seanphan/agenticflow-skill/SKILL.md)

3、 [openclaw-skills](https://link.zhihu.com/?target=https%3A//github.com/VoltAgent/awesome-openclaw-skills) 样例： [https://github.com/VoltAgent/awesome-openclaw-skills](https://link.zhihu.com/?target=https%3A//github.com/VoltAgent/awesome-openclaw-skills%3Ftab%3Dreadme-ov-file)

4、其它 skills样例： [github.com/openclaw/ski](https://link.zhihu.com/?target=https%3A//github.com/openclaw/skills/blob/main/skills/am-will/remotion-best-practices/SKILL.md)

[所属专栏 · 2026-02-25 22:28 更新](https://zhuanlan.zhihu.com/c_1378680688061952000)

[![](https://pic1.zhimg.com/v2-c5be1695771c4f9b442b5bde56e5e8e0_720w.jpg?source=172ae18b)](https://zhuanlan.zhihu.com/c_1378680688061952000)

[AI智能化应用](https://zhuanlan.zhihu.com/c_1378680688061952000)

[

时光相机

101 篇内容 · 4811 赞同

](https://zhuanlan.zhihu.com/c_1378680688061952000)

[

最热内容 ·

构建一个大模型(LLM) 应用所需了解的一切

](https://zhuanlan.zhihu.com/c_1378680688061952000)

编辑于 2026-02-20 12:06・北京[OpenClaw123](https://www.zhihu.com/topic/2000657712221017695)[Agent](https://www.zhihu.com/topic/28352669)[智能体](https://www.zhihu.com/topic/20687238)