---
title: Dexter项目深度调研报告
type: concept
created: 2026-05-02
updated: 2026-05-02
tags: [AI-Agent, 金融研究, 代码架构, 调研报告]
---


## 项目概况

Dexter 是 [virattt](https://github.com/virattt) 开发的一个面向金融研究的自主 AI Agent 项目，定位是 "金融研究领域的 Claude Code"。项目自 2025 年 10 月首次公开，到 2026 年 5 月已经积累了 **22,075 Stars** 和 **2,680 Forks**，当前有 **81 个 Open Issues**。

| 指标 | 数值 |
|------|------|
| Stars | 22,075 |
| Forks | 2,680 |
| Open Issues | 81 |
| 语言 | TypeScript |
| 运行时 | Bun |
| 创建日期 | 2025-10-14 |
| 最近更新 | 2026-05-02 |
| 当前版本 | 2026.5.1 |
| 许可证 | MIT |

**核心依赖栈**：
- **AI SDK**：LangChain (`@langchain/core`, `@langchain/openai`, `@langchain/anthropic`, `@langchain/google-genai`, `@langchain/ollama`)
- **TUI**：`@mariozechner/pi-tui` 提供终端 UI
- **数据源**：Financial Datasets API (`financialdatasets.ai`)
- **搜索**：Exa (主)、Perplexity / Tavily (备选)
- **WhatsApp**：`@whiskeysockets/baileys`
- **评估**：LangSmith
- **内存/持久化**：better-sqlite3 + 向量嵌入

项目代码量约 **20,000 行 TypeScript**，结构清晰，约 136 个源文件，按模块划分明确。


## 代码架构深度分析

### 1. 整体架构概览

```
src/
├── agent/          # Agent 核心循环、Scratchpad、Prompt、上下文管理
├── model/           # LLM 多提供商抽象层
├── tools/           # 工具系统 (金融/搜索/文件/浏览器/内存/Cron)
├── skills/          # Skill 系统 (工作流级别的复合操作)
├── memory/          # 持久化记忆系统 (向量搜索 + 文本搜索 + 时间衰减)
├── controllers/     # CLI 前端控制器 (AgentRunnerController)
├── gateway/         # WhatsApp 网关 (多通道支持)
├── evals/           # 评估系统 (LangSmith + LLM-as-Judge)
├── cron/            # 定时任务系统
├── utils/           # 工具函数
└── components/      # TUI 组件
```

### 2. Agent 循环实现 (ReAct 变体)

**文件**：`src/agent/agent.ts` (681行)

Agent 类是项目的核心，实现了一个增强版的 ReAct (Reasoning + Acting) 循环。

#### 2.1 初始化流程

```typescript
// agent.ts:72-99
static async create(config: AgentConfig = {}): Promise<Agent> {
  const model = config.model ?? DEFAULT_MODEL;        // 默认 gpt-5.4
  const tools = getTools(model);                      // 按模型加载工具
  const concurrencyMap = getToolConcurrencyMap(model); // 并发安全映射
  const soulContent = await loadSoulDocument();       // 加载 SOUL.md 人格
  const rulesContent = await loadRulesDocument();     // 加载用户自定义规则
  
  // 加载持久化记忆上下文
  if (config.memoryEnabled !== false) {
    const memoryManager = await MemoryManager.get();
    memoryFiles = await memoryManager.listFiles();
    const session = await memoryManager.loadSessionContext();
    if (session.text.trim()) memoryContext = session.text;
  }
  
  const systemPrompt = buildSystemPrompt(...);
  return new Agent(config, tools, systemPrompt, concurrencyMap);
}
```

**亮点**：Agent 初始化时便将 SOUL.md（人格）、RULES.md（用户规则）、持久化记忆全部注入 system prompt，使得 Agent 从一开始就"知道自己是谁"、"了解用户偏好"。

#### 2.2 主循环结构 (Generators + Streaming)

```typescript
// agent.ts:105-266
async *run(query: string, inMemoryHistory?: InMemoryChatHistory): AsyncGenerator<AgentEvent> {
  // 构建消息数组：SystemMessage + 历史 + HumanMessage
  let messages: BaseMessage[] = [
    new SystemMessage(this.systemPrompt),
    ...historyMessages,
    new HumanMessage(query),
  ];
  
  while (ctx.iteration < this.maxIterations) {  // 默认最多 10 次迭代
    ctx.iteration++;
    
    // 1. Microcompact: 每轮轻量级裁剪旧 ToolMessage 内容
    const mcResult = microcompactMessages(messages);
    
    // 2. 清除旧轮次的 reasoning 文本（保留最近 2 轮）
    this.stripOldThinking(messages, 2);
    
    // 3. 调用 LLM（流式，失败时回退到阻塞调用）
    const result = yield* this.callModelWithStreaming(messages);
    
    // 4. 无 tool_calls = 最终答案
    if (!hasToolCalls(response)) {
      yield* this.handleDirectResponse(responseText, ctx);
      return;
    }
    
    // 5. 并发执行工具调用
    let { toolMessages, denied } = yield* this.executeToolsAndCollectMessages(response, ctx);
    
    // 6. 大结果持久化到磁盘（超过 50KB 的结果存入文件，消息中只保留预览）
    toolMessages = toolMessages.map(tm => { ... });
    
    // 7. 每轮结果总量控制（单轮总计不超过 200KB）
    toolMessages = enforceResultBudget(toolMessages);
    
    // 8. Context 阈值管理 -> Memory Flush -> Compaction -> Truncate
    yield* this.manageContextThreshold(ctx, query, memoryFlushState, messageState);
    
    // 9. 注入工具调用警告（接近限制时）
    const toolUsageWarning = ctx.scratchpad.formatToolUsageForPrompt();
    if (toolUsageWarning) messages.push(new HumanMessage(toolUsageWarning));
    
    // 10. Drain 消息队列（用户可能在 Agent 工作时发送跟进消息）
    const drainResult = this.drainQueue();
  }
}
```

#### 2.3 流式 LLM 调用

```typescript
// agent.ts:294-338
private async *streamAndAccumulate(messages: BaseMessage[]) {
  yield { type: 'stream_progress', charDelta: 0, mode: 'requesting' };
  
  let accumulated: AIMessageChunk | null = null;
  for await (const chunk of streamLlmWithMessages(messages, {...})) {
    accumulated = accumulated ? accumulated.concat(chunk) : chunk;
    const { charDelta, mode } = inspectChunkContent(chunk);
    // 实时报告当前模式：thinking | responding | tool-input | tool-use
    yield { type: 'stream_progress', charDelta, mode };
  }
}
```

**关键设计决策**：
- 使用 `AsyncGenerator` 模式，每次工具调用都通过 `yield` 事件实时推送给 UI
- 流式优先，失败时自动降级到阻塞调用（兼容不支持 streaming 的 provider）
- 支持多种流模式检测：`requesting` → `thinking` → `responding` → `tool-input` → `tool-use`

#### 2.4 工具并发执行

```typescript
// agent/tool-executor.ts:65-80
async *executeAll(response: AIMessage, ctx: RunContext) {
  const batches = this.partitionToolCalls(response.tool_calls!, ctx);
  
  for (const batch of batches) {
    if (batch.concurrent && batch.calls.length > 1) {
      // 读操作工具并发执行（最多 10 个并发）
      yield* this.executeBatchConcurrently(batch.calls, ctx);
    } else {
      // 写操作工具串行执行
      for (const call of batch.calls) {
        yield* this.executeSingleWithId(call, ctx);
      }
    }
  }
}
```

**并发策略**：通过 `concurrencySafe` 标志区分工具类型。所有读操作（搜索、查询、fetch）并发执行；写操作（write_file、edit_file、memory_update）串行执行，且需要用户审批。

### 3. Scratchpad 设计与实现

**文件**：`src/agent/scratchpad.ts` (487行)

Scratchpad 是 Dexter 的核心数据结构和状态追踪器，设计极为精良。

#### 3.1 持久化格式

```typescript
// scratchpad.ts:84-101
constructor(query: string, limitConfig?: Partial<ToolLimitConfig>) {
  // 文件命名: "2026-05-02-153045_a1b2c3d4e5f6.jsonl"
  const hash = createHash('md5').update(query).digest('hex').slice(0, 12);
  const timestamp = now.toISOString().slice(0, 19).replace('T', '-').replace(/:/g, '');
  this.filepath = join(scratchpadDir, `${timestamp}_${hash}.jsonl`);
  
  // 写入初始条目
  this.append({ type: 'init', content: query, timestamp: new Date().toISOString() });
}
```

#### 3.2 条目类型

```typescript
// scratchpad.ts:15-24
interface ScratchpadEntry {
  type: 'init' | 'tool_result' | 'thinking';
  timestamp: string;
  content?: string;
  toolName?: string;
  args?: Record<string, unknown>;
  result?: unknown; // 自动解析 JSON
}
```

三个条目类型构建完整的 Agent trace：
1. `init` — 原始查询
2. `tool_result` — 每次工具调用，保留完整结果
3. `thinking` — 模型推理文本

#### 3.3 工具限制系统 (graceful exit)

```typescript
// scratchpad.ts:131-175
canCallTool(toolName: string, query?: string): { allowed: boolean; warning?: string } {
  const currentCount = this.toolCallCounts.get(toolName) ?? 0;
  
  // 超过建议限制 → 警告但允许
  if (currentCount >= maxCalls) {
    return { allowed: true, warning: `Tool '${toolName}' called ${currentCount} times...` };
  }
  
  // 重复查询检测（Jaccard 相似度 ≥ 0.7）
  if (query) {
    const similarQuery = this.findSimilarQuery(query, previousQueries);
    if (similarQuery) return { allowed: true, warning: `Very similar to previous call...` };
  }
  
  // 接近限制 → 警告
  if (currentCount === maxCalls - 1) {
    return { allowed: true, warning: `Approaching suggested limit...` };
  }
}
```

**设计哲学**：永远不阻止工具调用，只提供"建议性警告"——将循环避免的责任交给 LLM 的判断力，而非硬编码的阻断逻辑。

#### 3.4 Compaction 集成

```typescript
// scratchpad.ts:393-406
setCompactionSummary(summary: string): void {
  this.compactionSummary = summary;
  // 记录 compact 边界：summary 之后新增的 tool_result 正常展示
  this.compactionBoundaryIndex = toolResultCount - 1;
  this.clearedToolIndices.clear();
}

// getToolResults() 在 compact 模式下返回:
// summary + "---\n\nNew data retrieved after compaction:\n\n" + 新结果
```

### 4. 工具注册和调用机制

**文件**：`src/tools/registry.ts` (229行)

#### 4.1 RegisteredTool 结构

```typescript
// registry.ts:22-33
interface RegisteredTool {
  name: string;                    // 工具名称
  tool: StructuredToolInterface;   // LangChain 工具实例
  description: string;             // 富文本描述（给 system prompt）
  compactDescription: string;      // 紧凑描述（token 优化版本，1-2句）
  concurrencySafe: boolean;        // 是否支持并发的标志
}
```

**双描述设计**是个聪明优化：system prompt 用 `compactDescription`（大幅减少 token 消耗），LLM 本身通过 `bindTools()` 已经获得了完整的 tool schema。

#### 4.2 工具生命周期

1. **注册**：`getToolRegistry(model)` 构建完整工具列表
2. **条件加载**：仅当相应 API key 存在时才包含特定工具（web_search、x_search）
3. **动态绑定**：`llm.bindTools(tools)` 将工具列表注入 LLM 调用
4. **并发执行**：`toolExecutor.executeAll()` 按 `concurrencySafe` 拆分为批
5. **结果处理**：大结果持久化 → 预算控制 → 推入消息数组

#### 4.3 已注册工具清单

| 工具名称 | 类型 | 并发 | 说明 |
|---------|------|------|------|
| `get_financials` | Meta | ✓ | 财务数据智能路由（财务报表/指标/估计/收益/分段） |
| `get_market_data` | Meta | ✓ | 市场数据智能路由（股价/加密/新闻/内幕交易） |
| `read_filings` | Meta | ✓ | SEC 文件读取（10-K/10-Q/8-K） |
| `stock_screener` | Meta | ✓ | 股票筛选器 |
| `web_search` | Direct | ✓ | Web 搜索（Exa → Perplexity → Tavily 优先级） |
| `web_fetch` | Direct | ✓ | URL 内容抓取 + Readability 提取 |
| `browser` | Direct | ✓ | Playwright 浏览器自动化 |
| `read_file` | Direct | ✓ | 读本地文件 |
| `write_file` | Direct | ✗ | 写文件（需审批） |
| `edit_file` | Direct | ✗ | 编辑文件（需审批） |
| `skill` | Direct | ✗ | 调用 Skill 工作流 |
| `memory_search` | Direct | ✓ | 搜索持久化记忆 |
| `memory_get` | Direct | ✓ | 读取记忆文件 |
| `memory_update` | Direct | ✗ | 更新记忆（需审批） |
| `heartbeat` | Direct | ✓ | 定期心跳清单 |
| `cron` | Direct | ✓ | 定时任务管理 |
| `x_search` | Conditional | ✓ | X/Twitter 搜索（需要 X_BEARER_TOKEN） |

### 5. LLM 多提供商抽象层

**文件**：`src/model/llm.ts` (376行) + `src/providers.ts` (105行)

#### 5.1 提供商注册

```typescript
// providers.ts:21-84
PROVIDERS = [
  { id: 'openai',    prefix: '',          fastModel: 'gpt-4.1',         contextWindow: 1_047_576 },
  { id: 'anthropic', prefix: 'claude-',   fastModel: 'claude-haiku-4-5',contextWindow: 200_000 },
  { id: 'google',    prefix: 'gemini-',   fastModel: 'gemini-3-flash',  contextWindow: 1_000_000 },
  { id: 'xai',       prefix: 'grok-',     fastModel: 'grok-4-1-fast',   contextWindow: 131_072 },
  { id: 'moonshot',  prefix: 'kimi-',     fastModel: 'kimi-k2-5',       contextWindow: 131_072 },
  { id: 'deepseek',  prefix: 'deepseek-', fastModel: 'deepseek-v4-flash',contextWindow: 1_000_000 },
  { id: 'openrouter',prefix: 'openrouter:',fastModel: 'openrouter:openai/gpt-4o-mini', contextWindow: 128_000 },
  { id: 'ollama',    prefix: 'ollama:',   contextWindow: 128_000 },
];
```

#### 5.2 模型工厂模式

```typescript
// llm.ts:68-135
const MODEL_FACTORIES = {
  anthropic: (name, opts) => new ChatAnthropic({ model: name, ...opts }),
  google:    (name, opts) => new ChatGoogleGenerativeAI({ model: name, ...opts }),
  xai:       (name, opts) => new ChatOpenAI({ baseURL: 'https://api.x.ai/v1' }),
  deepseek:  (name, opts) => new ChatOpenAI({ 
    baseURL: 'https://api.deepseek.com',
    reasoning_effort: 'high',          // 启用深度思考模式
    extraBody: { thinking: { type: 'enabled' } },
  }),
  ollama:    (name, opts) => new ChatOllama({ baseUrl: process.env.OLLAMA_BASE_URL }),
  // ...
};
```

#### 5.3 Anthropic Prompt Caching

```typescript
// llm.ts:265-286
function annotateSystemMessageForCaching(messages: BaseMessage[]) {
  const annotated = new SystemMessage({
    content: [{
      type: 'text',
      text,
      cache_control: { type: 'ephemeral' },  // 标记为可缓存
    }],
  });
  return [annotated, ...messages.slice(1)];
}
```

为 Anthropic 提供商标注 `cache_control` 以利用 prompt caching，减少 ~90% 的输入 token 成本。

#### 5.4 三步 API 接口

| 函数 | 用途 | 返回 |
|------|------|------|
| `callLlm()` | 单轮文本调用 + 可选 structured output | AIMessage / string |
| `callLlmWithMessages()` | 多轮消息数组调用（工具调用场景） | AIMessage |
| `streamLlmWithMessages()` | 流式多轮调用 | AsyncGenerator |

### 6. Skill 系统的加载和执行流程

**文件**：`src/skills/` 目录

这是 Dexter 最有创新性的架构设计之一——Skill 是工作流级别的复合操作。

#### 6.1 Skill 定义格式

每个 Skill 是一个目录，包含 `SKILL.md` 文件，使用 YAML frontmatter：

```yaml
# skills/dcf/SKILL.md
---
name: dcf-valuation
description: Performs DCF valuation analysis...
---
# DCF Valuation Skill
## Workflow Checklist
## Step 1: Gather Financial Data
...
```

#### 6.2 发现和加载流程

```typescript
// skills/registry.ts:15-18
const SKILL_DIRECTORIES = [
  { path: __dirname, source: 'builtin' },       // 内置 skills
  { path: dexterPath('skills'), source: 'project' }, // 项目级 skills
];

// registry.ts:62-78
export function discoverSkills(): SkillMetadata[] {
  // 扫描所有 skill 目录 → 按名称去重 → 支持覆盖
  for (const { path, source } of SKILL_DIRECTORIES) {
    const skills = scanSkillDirectory(path, source);
    for (const skill of skills) {
      skillMetadataCache.set(skill.name, skill); // later overrides earlier
    }
  }
}
```

#### 6.3 执行时机

Skill 的调用是 **LLM 自治决策** 的——system prompt 中列出可用 skills，LLM 判断是否匹配用户查询并调用 `skill` 工具。Skill 工具返回完整指令文本，Agent 随后按照指令逐步执行工具调用。

```typescript
// tools/skill.ts:37-74
export const skillTool = new DynamicStructuredTool({
  name: 'skill',
  func: async ({ skill, args }) => {
    const skillDef = getSkill(skill);
    // 解析相对链接为绝对路径（Agent 的 read_file 可以访问）
    const resolved = skillDef.instructions.replace(
      /\[([^\]]+)\]\(([^)]+\.md)\)/g,
      (_match, label, relPath) => resolve(skillDir, relPath)
    );
    return `## Skill: ${skillDef.name}\n\n${resolved}`;
  },
});
```

#### 6.4 内置 Skills

| Skill | 触发条件 | 描述 |
|-------|---------|------|
| **dcf-valuation** | 公允价值/内在价值/DCF/估值 | 8步完整 DCF 工作流，含敏感度分析 |
| **x-research** | X/Twitter 情绪/市场意见 | 搜索 → 迭代优化 → 主题摘要 → 综合 |

DCF Skill 设计尤其精良，包含：
- 数据采集清单（现金流量表、资产负债表、利润表、分析师预测、股价、公司信息）
- 增长率和 WACC 计算指南
- 验证步骤（EV 交叉验证、终值比率检查、每股交叉检查）
- 敏感度分析矩阵（WACC ±1% vs 终端增长率 2.0%-3.0%）

### 7. 上下文管理三层体系

Dexter 实现了业界最优秀的上下文管理方案之一，采用三层递进策略：

```
Layer 1: Microcompact   (每轮触发) → 轻量级：清除旧 ToolMessage 内容，保留标记
Layer 2: Memory Flush   (接近阈值) → 结构化：LLM 提取关键信息写入记忆文件
Layer 3: Full Compaction (超阈值)   → 重量级：LLM 总结所有工具结果，重置上下文
Layer 0: Truncate       (兜底)     → 直接截断最旧的回合
```

#### 7.1 Microcompact

```typescript
// agent/microcompact.ts:51-114
export function microcompactMessages(messages: BaseMessage[]) {
  // 触发条件：
  //   - COUNT: 可压缩的 ToolMessages > 8
  //   - TOKEN: 可压缩内容 > 80,000 tokens
  // 策略：保留最新的 4 条，其余替换为 "[Old tool result content cleared]"
}
```

#### 7.2 Memory Flush

在 compaction 之前，先把工具结果中的关键信息写入持久化记忆：

```typescript
// agent/agent.ts:551-573
// Step 1: Memory flush — before compaction, persist findings to memory
const flushResult = await runMemoryFlush({
  model, systemPrompt, query, toolResults, signal,
});
```

#### 7.3 Full Compaction

使用快速模型（如 gpt-4.1 / claude-haiku-4-5）进行 LLM 总结：

```typescript
// agent/compact.ts:194-227
export async function compactContext(params) {
  const fastModel = provider.fastModel ?? model;
  const prompt = buildCompactionPrompt(query, toolResults);
  const result = await callLlm(prompt, { model: fastModel, systemPrompt });
  const summary = buildCompactSummaryMessage(rawSummary);
  return { summary, rawSummary, usage: result.usage };
}
```

总结包含 9 个固定 section：原始查询、关键概念、已检索数据、错误和重试、分析进展、数字数据、待需数据、当前工作状态、建议下一步。

#### 7.4 模型感知阈值

```typescript
// utils/tokens.ts:39-52
export function getEffectiveContextWindow(model: string): number {
  const contextWindow = provider.contextWindow ?? 128_000;
  return contextWindow - 20_000;  // 保留 20K 给模型输出
}

export function getAutoCompactThreshold(model: string): number {
  return getEffectiveContextWindow(model) - 13_000;  // 再留 13K 缓冲
}
```

不同模型的 compaction 阈值因 context window 大小而异：GPT-5.4 (~1M window) 的阈值远比 Claude Sonnet (200K) 宽松。

### 8. 持久化记忆系统

**文件**：`src/memory/` 目录

Dexter 的持久化记忆是一个完整的子系统，而非简单的 KV 存储。

#### 8.1 架构组件

```
MemoryManager (单例)
├── MemoryStore      — 文件系统操作（读/写/编辑/删除 .md 文件）
├── MemoryDatabase   — SQLite 索引（存储向量嵌入 + 块元数据）
├── MemoryIndexer    — 文件变更检测 + 自动重索引（debounce 1.5s）
└── Chunker          — 递归文本分块（400 tokens/块, 80 tokens 重叠）
```

#### 8.2 混合搜索

```typescript
// memory/index.ts:138-164
async search(query, options?) {
  return hybridSearch({
    db, embeddingClient, query,
    defaults: {
      maxResults: 6,
      minScore: 0.1,
      vectorWeight: 0.7,  // 向量维度权重
      textWeight: 0.3,    // 文本维度权重
    },
    temporalDecay: { enabled: true, halfLifeDays: 30 },  // 时间衰减
    mmr: { enabled: true, lambda: 0.7 },                  // MMR 去重
  });
}
```

**混合搜索 = 向量相似度 (70%) + BM25 文本匹配 (30%) + MMR 多样性重排 + 时间衰减**

#### 8.3 Provider 指纹

```typescript
// memory/index.ts:97-101
const fingerprint = `${client.provider}:${client.model}`;
if (db.getProviderFingerprint() !== fingerprint) {
  db.clearEmbeddings();  // 切换 provider 时自动清除旧向量
  db.setProviderFingerprint(fingerprint);
}
```

切换 embedding provider 时自动重建索引，避免不同模型的向量空间不兼容导致的错误。


## 金融工具能力评估

### 数据源

Dexter 的所有金融数据通过 **Financial Datasets API** (`https://api.financialdatasets.ai`) 获取，这是一个商业化的金融数据 API 服务。

| API 端点 | 功能 | 缓存 TTL |
|---------|------|----------|
| `/financials/income-statements/` | 利润表 | 24h |
| `/financials/balance-sheets/` | 资产负债表 | 24h |
| `/financials/cash-flow-statements/` | 现金流量表 | 24h |
| `/financials/` | 三大报表合一 | 24h |
| `/financial-metrics/snapshot/` | 估值比率、利润率、ROE 等 | 1h |
| `/financial-metrics/` | 历史指标序列 | 6h |
| `/analyst-estimates/` | 分析师预测 | 6h |
| `/earnings/` | 最新财报数据（含 beat/miss） | 24h |
| `/financials/revenue-segments/` | 收入细项 | 24h |
| `/prices/snapshot/` | 股票即时价格 | 无缓存 |
| `/prices/` | 股票历史价格 | 有条件缓存 |
| `/prices/snapshot/tickers/` | 可用的股票代码 | 24h |
| `/crypto/prices/snapshot/` | 加密货币价格 | 无缓存 |
| `/crypto/prices/` | 加密货币历史价格 | 无缓存 |
| `/crypto/prices/tickers/` | 可用的加密货币代码 | 24h |
| `/news/` | 公司/市场新闻 | 无缓存 |
| `/insider-trades/` | 内部人交易 | 无缓存 |
| `/filings/` | SEC 文件列表 | 无缓存 |
| `/filings/10-K/items/` | 10-K 文件内容 | 无缓存 |
| `/filings/10-Q/items/` | 10-Q 文件内容 | 无缓存 |
| `/filings/8-K/items/` | 8-K 文件内容 | 无缓存 |
| `/financials/search/screener/` | 股票筛选器 | 内存缓存 |

### Meta-Tool 设计模式

`get_financials` 和 `get_market_data` 是两个 **meta-tool**，采用 **LLM-as-router** 模式：

```
用户查询 "compare AAPL and MSFT P/E and revenue growth"
  ↓
get_financials(query)
  ↓ 内部 LLM 调用（router prompt + finance sub-tools）
  ↓ 路由到 get_key_ratios(AAPL) + get_key_ratios(MSFT)
  ↓ 并发执行
  ↓ 格式化输出（markdown tables）
  ↓
返回结构化结果
```

**优势**：
- 用户/Agent 只需发一条自然语言查询
- 内部自动路由、并发执行、结果合并
- 格式化输出极大减少 token 消耗（formatter 将原始 JSON 压缩为紧凑 markdown table，5-10x 压缩比）

### 数据质量评估

**优势**：
- 覆盖财务报表、市场数据、SEC 文件三大类金融数据
- 支持多公司/多指标并发查询
- 内置 ticker 解析和日期推断
- 数据实时性分层缓存（价格/新闻无缓存，财务报表 24h 缓存）

**不足**：
- 完全依赖单一商业 API (Financial Datasets)，无多源交叉验证
- 不支持 A股、港股等非美股市场
- 没有历史回测能力（仅查询，无统计分析）
- 无自定义因子计算能力
- 技术指标缺失（无 RSI、MACD、布林带等）

### 与 panda_factor 对比

| 维度 | Dexter | panda_factor (推测) |
|------|--------|---------------------|
| 定位 | 对话式金融研究 Agent | 量化因子计算/回测平台 |
| 数据获取 | NLP 驱动的 API 调用 | 直接的数据查询 / 计算 |
| 因子能力 | 依赖 API 返回的内置指标 | 自定义因子公式/多因子组合 |
| 回测 | 无 | 应具备 |
| 推理能力 | LLM 驱动的多步推理 | 确定性计算 |
| 自主性 | 高（可自主决定研究路径） | 低（用户指定计算逻辑） |
| 使用场景 | 探索性研究、快速问答 | 系统性量化分析、策略验证 |

**两者是互补关系而非竞争关系。** Dexter 擅长"探索性研究"（"帮我看看 AAPL 是否便宜"），panda_factor 擅长"系统性计算"（"计算全市场动量因子并回测"）。


## 评估系统

**文件**：`src/evals/run.ts` (361行)

### 数据集

数据集位于 `src/evals/dataset/finance_agent.csv`，是一个 CSV 文件，包含以下字段：
- **Question** — 自然语言金融问题
- **Answer** — 专家标注的标准答案
- **Question Type** — 题型分类：Market Analysis / Trends / Beat or Miss / Complex Retrieval / Qualitative Retrieval
- **Expert time (mins)** — 专家回答所需时间 (5-30分钟)
- **Rubric** — 详细评分标准（JSON 格式的操作符和条件）

### 问题类型分布

从 CSV 数据可见问题覆盖：
- **Market Analysis**：并购/战略/市场事件（如 US Steel 与 Nippon Steel 的合并）
- **Trends**：时间序列趋势分析（如 Netflix ARPU 变化）
- **Beat or Miss**：业绩 beat/miss 判断（如 TJX 税前利润率指引）
- **Complex Retrieval**：需要多步复杂查询（如 AMD 各季度营收指引范围、FAAMG Capex 对比）
- **Qualitative Retrieval**：定性信息提取（如董事提名名单）

### 评估方法

```
评估流程:
1. Agent.run(question) → 得到答案
2. CorrectnessEvaluator(预期答案 vs 实际答案) → LLM-as-Judge
3. 输出 score (0/1) + comment
4. 记录到 LangSmith
```

```typescript
// evals/run.ts:172-211
async function correctnessEvaluator({ outputs, referenceOutputs }) {
  const prompt = `Compare the actual answer to the expected answer...
  - score: 1 if correct (contains key information), 0 if incorrect
  - comment: brief explanation`;
  
  const result = await structuredLlm.invoke(prompt);  // gpt-5.4 with structured output
  return { key: 'correctness', score: result.score, comment: result.comment };
}
```

### 评估质量分析

**优势**：
- 使用业界标准的 LLM-as-Judge 方法
- 与 LangSmith 集成，可追踪每次评估
- 实时 TUI 显示进度和统计
- 支持采样模式（`--sample N`）快速验证

**不足**：
- **仅评估正确答案（correctness）一个维度**，缺少完整性、推理质量、效率等多维度
- **二元评分（0/1）过于粗糙**，无法区分"部分正确"和"完全错误"
- **评估数据集规模小**（CSV 文件约 30-50 条），统计显著性不足
- **缺少一致性指标**（同一问题多次运行结果是否一致）
- **没有成本/efficiency 指标**（token 消耗、工具调用次数、总耗时）
- **评估者模型与目标模型相同**（gpt-5.4），存在自评偏差风险


## 优缺点总结

### 技术架构亮点

1. **上下文管理三层体系是业界最佳实践**
   Microcompact → Memory Flush → Compaction 的递进设计优雅且实用。特别是 fast model compaction（用便宜模型做总结），兼顾了信息保留和成本控制。

2. **Skill 系统是一种轻量级 Agent 复合模式**
   将复杂工作流（如 DCF 估值）封装为可复用的 Skill，LLM 自主决定何时调用——既不增加工具列表的复杂度，又保留了工作流的专业性。

3. **Meta-Tool 设计降低 Agent 的工具选择负担**
   `get_financials` 和 `get_market_data` 内部有完整的 router LLM，外部 Agent 只需发一条查询，无需直接操作 20+ 个子工具。

4. **Generator-based 事件流**
   全异步 Generator 模式的 Agent 循环，支持实时 UI 更新、流式思考展示、工具进度追踪。

5. **持久化记忆系统超越了简单的 RAG**
   混合搜索（向量+文本+MMR+时间衰减）提供了真正有用的长期记忆，而非简单的"最近对话摘要"。

6. **SOUL.md 设计让 Agent 有一致人格**
   1500+ 字的投资哲学定义（Buffett/Munger 价值投资框架），让 Agent 不只是工具调用器。

7. **多通道设计**
   CLI 和 WhatsApp 两种交互通道，channel profile 控制响应格式和行为风格。

### 技术不足

1. **完全依赖单一商业 API (Financial Datasets)**
   无数据冗余、无交叉验证。API 宕机 = Agent 完全不可用。

2. **缺乏量化计算能力**
   Dexter 更像"金融 ChatGPT"，没有真正的数值计算引擎（无 numpy/pandas 等效能力，无时间序列分析，无统计检验）。

3. **评估系统简陋**
   仅二元 correctness，缺少多维度评测和一致性验证。

4. **不支持 A股/港股市场**
   数据源仅覆盖美股和加密货币。

5. **TypeScript/Bun 生态系统**
   对于量化分析任务，Python 生态系统（pandas、numpy、scipy、statsmodels）远超 TypeScript 能提供的。

6. **无并行 Agent 协作**
   单 Agent 循环，无多 Agent 分解-聚合模式。

7. **依赖 LangChain 重型框架**
   LangChain 带来了多提供商兼容性，但也引入了抽象泄漏和调试困难的问题。


## 对我们的参考价值

### 可直接借鉴的设计

1. **三层上下文管理体系 (Microcompact → Memory Flush → Compaction)**
   - 这对长时间运行的诊断 Agent 极为重要
   - 可以适配到日志分析场景：用 fast model 对大量日志输出做阶段性总结
   - `agent/compact.ts` 的 prompt 模板可直接参考

2. **Scratchpad 的持久化 + 限制系统**
   - `scratchpad.ts` 的 JSONL 格式、工具调用追踪、重复查询检测（Jaccard 相似度）都可复用
   - 对于诊断 Agent，可追踪"已检查哪些模块/配置"，避免无限循环

3. **Skill 系统——工作流级别的复合操作**
   - 将常见诊断流程（如 OOM 排查、性能瓶颈分析）封装为 Skill
   - 量化场景：因子计算流程、数据清洗流程、回测流程

4. **Meta-Tool 的 LLM-as-Router 模式**
   - `get_financials` 的实现是优秀范例：外部 Agent 只需明确"意图"，内部自动路由
   - 诊断场景可对应：`diagnose(query)` → 内部路由到日志搜索/配置检查/指标查询/代码搜索等

5. **SOUL.md 人格定义**
   - 让 Agent 具有一致的分析风格和价值观，在长时间会话中保持行为一致性
   - 量化 Agent 可定义为"审慎的数据科学家"，投资 Agent 可定义为"价值投资者"

6. **多提供商抽象 + 分层次模型使用**
   - 核心推理用最强模型，compaction/summarization 用 fast model
   - 对于我们的场景：诊断推理用 Sonnet/Opus，日志总结用 Haiku，成本最优

### 不建议照搬的部分

1. **LangChain 依赖** — 建议直接使用各 provider 的原生 SDK，减少抽象层
2. **单一数据源** — 我们的量化/诊断项目需要多源数据交叉验证
3. **TypeScript 生态** — 量化分析天然适合 Python，不建议为统一语言而牺牲生态

### 架构改进建议（如果我们做类似项目）

1. **Agent 协作**：引入 supervisor-worker 多 Agent 模式，每个 worker 专注一类工具
2. **多源交叉验证**：至少 2 个独立数据源，结果交叉验证
3. **量化计算引擎**：嵌入 Python 子进程或用 WASM 运行 pandas/numpy
4. **多维度评估**：除 correctness 外，增加 completeness、reasoning_quality、efficiency、consistency
5. **结构化输出中间层**：在工具结果和 LLM 之间增加结构化中间表示，减少 token 消耗
6. **增量式 Skill 学习**：Agent 能自动从成功执行中提取新的 Skill
