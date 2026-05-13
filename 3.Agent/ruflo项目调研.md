---
title: Ruflo项目调研
type: research
created: 2026-05-09
updated: 2026-05-09
tags: [AI-Agent, Multi-Agent, Claude-Code, Swarm, ECC, MCP, RAG]
sources: [https://github.com/ruvnet/ruflo]
---

# Ruflo 项目深度调研

## 概述

**项目地址**: [github.com/ruvnet/ruflo](https://github.com/ruvnet/ruflo)
**作者**: rUv (ruv.io)
**版本**: 3.7.0-alpha.18 (npm: ruflo@3.6.24 稳定版)
**语言**: TypeScript
**协议**: MIT
**Stars**: 47,423 | **Forks**: 5,253 (截至 2026-05-09)
**定位**: Claude Code 的多 Agent 编排平台，口号"🌊 The leading agent orchestration platform for Claude"

**历史演进**: 项目前身为 Claude Flow → 更名为 Ruflo (Ru = rUv, flo = flow)。底层由 Cognitum.One 提供 agentic 架构，核心是一个 Rust-based AI 引擎，提供 embeddings、memory 和插件系统。

---

## 1. 项目架构与技术栈

### 1.1 整体架构（四层结构）

```
User → Claude Code / CLI
        ↓
  Orchestration Layer (MCP Server, Router, 27 Hooks)
        ↓
  Swarm Coordination (Queen, Topology, Consensus)
        ↓
  100+ Specialized Agents (coder, tester, reviewer, architect, security...)
        ↓
  Memory & Learning (AgentDB, HNSW, SONA, ReasoningBank)
        ↓
  LLM Providers (Claude, GPT, Gemini, Cohere, Ollama)
```

### 1.2 技术栈详解

| 层级 | 核心技术 | 说明 |
|------|---------|------|
| **CLI/入口** | TypeScript, Node.js ≥20 | npm 包 `ruflo@latest`，通过 `npx ruflo init` 安装 |
| **MCP 服务器** | `@claude-flow/mcp@^3.0.0` | 暴露 300+ MCP tools 给 Claude Code |
| **路由层** | Q-Learning + MoE (8 Experts) | 智能任务路由，89% 准确率 |
| **模型路由** | Thompson Sampling Multi-Armed Bandit | 成本自适应模型选择，~50 次反馈后自校准 |
| **Swarm 编排** | Raft / Byzantine / Gossip | 分布式共识算法 |
| **向量数据库** | AgentDB + HNSW | HNSW 索引，150x-12,500x 加速 |
| **神经学习** | SONA, EWC++, MicroLoRA, 9 RL Algorithms | 自优化神经架构 |
| **本地嵌入** | ONNX Runtime + MiniLM | 无 API 调用的本地向量化 |
| **WASM 加速** | `@ruvector/rabitq-wasm`, Rust→WASM | 策略引擎、嵌入、证明系统 |
| **加密** | AES-256-GCM, Ed25519 (@noble/ed25519) | 静态加密 + 密码学验证 |
| **Web UI** | Svelte (flo.ruv.io), Docker | 自托管多模型聊天 UI |
| **Goal Planner** | Vite + React + Supabase (goal.ruv.io) | GOAP A* 规划器 |

### 1.3 核心 package 依赖

```
ruflo (claude-flow@3.7.0-alpha.18)
├── @claude-flow/cli-core@^3.7.0-alpha.5    # 核心 CLI
├── @claude-flow/mcp@^3.0.0-alpha.8         # MCP 服务器
├── @claude-flow/neural@^3.0.0-alpha.8      # 神经学习引擎
├── @claude-flow/shared@^3.0.0-alpha.7      # 共享模块
├── @ruvector/rabitq-wasm@^0.1.0            # WASM 向量加速
├── @noble/ed25519@^2.1.0                   # 密码学
├── zod@^3.22.4                             # 运行时类型验证
└── semver@^7.6.0                           # 版本管理
```

### 1.4 代码组织（DDD 分层架构）

项目采用 Domain-Driven Design 结构:

```
v3/@claude-flow/
├── agents/           # Agent 定义 (YAML)
│   ├── architect.yaml
│   ├── coder.yaml
│   ├── reviewer.yaml
│   ├── security-architect.yaml
│   └── tester.yaml
├── browser/          # 浏览器自动化插件
│   └── src/
│       ├── domain/       # 领域实体 & 服务
│       ├── application/  # 应用服务层
│       ├── infrastructure/ # 基础设施 (hooks, memory, security adapters)
│       ├── mcp-tools/    # MCP 工具定义
│       ├── agent/        # Agent 适配器
│       └── skill/        # Skill 定义
├── aidefence/        # AI 安全防御模块
│   └── src/domain/
│       ├── entities/threat.ts
│       └── services/
│           ├── threat-detection-service.ts
│           └── threat-learning-service.ts
├── cli/              # CLI 工具和命令
└── cli-core/         # 轻量版 CLI (无 SQLite/HNSW/ONNX)
```

---

## 2. 多 Agent Swarm 编排机制

### 2.1 三种编排拓扑

| 拓扑 | 机制 | 适用场景 |
|------|------|---------|
| **Hierarchical** | Queen 主导，Worker 执行，分层决策 | 复杂项目、多文件修改、新功能开发 |
| **Mesh** | 点对点协作，无中心节点 | 独立任务并行、去中心化交互 |
| **Adaptive** | 动态切换拓扑，基于任务特征优化 | 混合场景、性能自适应 |

### 2.2 Queen-Worker Hive Mind 系统

```
Strategic Queen (战略层)
  ├── Tactical Queen (战术层)
  │   ├── Researcher (研究员)
  │   ├── Coder (编码)
  │   ├── Analyst (分析)
  │   └── Tester (测试)
  └── Adaptive Queen (自适应层)
      ├── Architect (架构)
      ├── Reviewer (审查)
      ├── Optimizer (优化)
      └── Documenter (文档)
```

**Queen 类型**:
- **Strategic Queen**: 高层目标分解和规划
- **Tactical Queen**: 中层执行管理
- **Adaptive Queen**: 基于性能动态调整策略

**投票权重**: Queen 投票权重为 Worker 的 3 倍

### 2.3 三种共识算法

| 算法 | 容错能力 | 性能 | 使用场景 |
|------|---------|------|---------|
| **Majority** | 简单多数 | 最快 | 低风险决策 (代码格式、命名) |
| **Weighted** | Queen 3x权重 | 快 | 有明确专家意见的决策 |
| **Byzantine** | f < n/3 恶意节点 | 较慢 | 安全关键决策、代码审查通过 |

### 2.4 任务路由机制

```
Q-Learning Router (强化学习)
    ↓
MoE (Mixture of Experts, 8 个专家)
    ↓
Thompson Sampling Router (成本自适应)
    ↓
Task → Agent Assignment

路由策略:
- Simple tasks  → WASM Agent Booster (<1ms, $0)
- Medium tasks  → Haiku/Sonnet (~500ms)
- Complex tasks → Opus + Swarm (2-5s)
```

系统声称可以**延长 Claude Code 订阅用量 250%**（通过将简单任务跳过 LLM）。

### 2.5 Claims 机制

Ruflo 引入了 "Claims" 概念，用于人-Agent 协调:
- 在 `swarm init` 时需要人工审批关键步骤
- 支持 `on-failure`、`on-request`、`never` 等审批策略
- 在配置中通过 `approval_policy` 控制

### 2.6 反漂移 (Anti-Drift) 控制

- 每 10 个任务设置 checkpoint（`checkpoint_interval = 10`）
- 任务漂移检测和自动纠正
- 层级化拓扑防止 Agent 偏离目标

---

## 3. RAG 和自学习能力

### 3.1 向量存储：AgentDB

```
AgentDB Architecture:
  ├── HNSW Index (分级可导航小世界图)
  │   ├── M = 16 (每层连接数)
  │   ├── efConstruction = 200
  │   └── efSearch = 100
  ├── SQLite Persistence (WAL 模式)
  ├── LRU Cache (内存压力管理)
  └── ONNX Embeddings (MiniLM, 本地运行)
```

**性能数据**:
- HNSW 检索: 150x-12,500x 快于暴力搜索
- 子毫秒级向量检索
- 每向量 0.447ms (Micro-LoRA 模式)
- 支持 3 种 memory scope: per-agent / cross-agent / global

### 3.2 SONA 自学习系统

**SONA (Self-Optimizing Neural Architecture)** 是核心学习引擎:

```
Learning Loop:
  RETRIEVE → JUDGE → DISTILL → CONSOLIDATE → ROUTE
      ↑                                        ↓
      └──────────── 反馈循环 ←──────────────────┘
```

**学习流程**:
1. **RETRIEVE**: 检索 k=3 个相似历史模式 (HNSW, 761 decisions/sec)
2. **JUDGE**: 评估当前策略效果
3. **DISTILL**: 提取成功模式为可复用知识
4. **CONSOLIDATE**: 整合到 ReasoningBank
5. **ROUTE**: 应用到未来的任务路由

**Pre/Post Hook 学习**:
```bash
# Pre-task: 初始化学习轨迹
npx claude-flow@alpha hooks pre-task --description "$TASK"

# Post-task: 记录结果并学习
npx claude-flow@alpha hooks post-task --task-id "$ID" --success true
```

### 3.3 持续学习技术

| 技术 | 功能 | 性能提升 |
|------|------|---------|
| **EWC++** | 弹性权重巩固，防止灾难性遗忘 | 保持已学模式不变 |
| **MicroLoRA** | 低秩适配，99% 参数减少 | 10-100x 更快训练 |
| **Flash Attention** | 优化注意力计算 | 2.49-7.47x 加速 |
| **Int8 量化** | 内存高效存储 | ~4x 内存减少 |
| **Thompson Sampling** | 多臂老虎机模型选择 | ~50 次反馈后自动调优 |

#### 核心技术原理速查

| 技术 | 解决的问题 | 原理 |
|---|---|---|
| **SONA** | 怎么从历史中学习 | RETRIEVE→JUDGE→DISTILL→CONSOLIDATE→ROUTE 五步闭环，每次任务后自动提取成功模式并存储复用 |
| **EWC++** | 学新忘旧（灾难性遗忘） | 用 Fisher 信息矩阵评估参数重要性，给重要参数加弹性约束，学新任务时不覆盖旧知识。++ 版用滚动平均合并多任务矩阵，内存恒定 |
| **MicroLoRA** | 微调成本太高 | Low-Rank Adaptation：只更新权重矩阵的低秩分解部分（~1% 参数），99% 参数冻结不动 |
| **Thompson Sampling** | 该用哪个模型 | 多臂老虎机：每个模型维护 Beta(α,β) 分布，每次采样 θ~Beta 取最大值对应的模型。~50 次反馈后分布收敛到最优 |
| **HNSW** | 向量检索太慢 | 分层可导航小世界图：多层跳表式结构，高层粗定位+低层精搜索，从 O(n) 降到 O(log n)，子毫秒级 |

### 3.4 ReasoningBank

- 存储任务执行轨迹 (trajectory learning)
- 模式匹配和复用
- 支持 serialize/deserialize (进程重启不丢失状态)
- 连接 AgentDB 做图+向量+SQL 联合操作

### 3.5 知识图谱

- PageRank 分析识别关键知识点
- 社区检测发现知识簇 (ADR-049)
- 和 ReasoningBank 联动：`RETRIEVE → JUDGE → DISTILL → CONSOLIDATE`

### 3.6 支持的强化学习算法

系统内置 9 种 RL 算法: Q-Learning, SARSA, A2C, PPO, DQN, Decision Transformer 等，用于不同场景的任务级学习。

---

## 4. 与 Claude Code 的集成方式

### 4.1 两种安装路径

| | Plugin Path (lite) | CLI Full Path |
|---|---|---|
| **安装命令** | `/plugin marketplace add ruvnet/ruflo` → `/plugin install ruflo-core@ruflo` | `npx ruflo@latest init wizard` |
| **文件侵入性** | 零文件写入工作区 | 写入 .claude/, CLAUDE.md, helpers 等 |
| **MCP Server** | ❌ 不注册 | ✅ 注册 300+ tools |
| **Hooks** | ❌ 无 | ✅ 27 hooks |
| **Agent 数量** | 少量 (per-plugin) | 100+ 全量 |
| **适用场景** | 试用单个功能 | 生产使用 |

### 4.2 MCP 集成

```bash
# MCP server 注册方式（写入 Claude Code settings）
claude mcp add ruflo -- npx ruflo@latest mcp start

# MCP 工具分类 (300+ tools):
├── Core (核心编排)
├── Intelligence (智能路由 & 学习)
├── Agents (Agent 管理)
├── Memory (向量存储 & 检索)
├── DevTools (开发工具)
├── GitHub (PR/Issue 管理)
├── Browser (浏览器自动化)
└── Federation (跨机器协作)
```

### 4.3 Hooks 系统（27 个钩子）

```
PreToolUse:
  └── Bash → 命令审查、安全检查
  └── Write|Edit|MultiEdit → 文件变更拦截

PostToolUse:
  └── Bash → 指标追踪、结果存储
  └── Write|Edit|MultiEdit → 自动格式化、memory 更新

PreCompact:
  └── manual → 提示 agent 使用指南
  └── auto → 上下文压缩指导

Stop:
  └── 会话结束：状态持久化、摘要生成、指标导出
```

### 4.4 Plugin 生态系统（32 个插件）

**Core & Orchestration** (6): ruflo-core, ruflo-swarm, ruflo-autopilot, ruflo-loop-workers, ruflo-workflows, ruflo-federation

**Memory & Knowledge** (5): ruflo-agentdb, ruflo-rag-memory, ruflo-rvf, ruflo-ruvector, ruflo-knowledge-graph

**Intelligence & Learning** (4): ruflo-intelligence, ruflo-daa, ruflo-ruvllm, ruflo-goals

**Code Quality & Testing** (4): ruflo-testgen, ruflo-browser, ruflo-jujutsu, ruflo-docs

**Security & Compliance** (2): ruflo-security-audit, ruflo-aidefence

**Architecture & Methodology** (3): ruflo-adr, ruflo-ddd, ruflo-sparc

**DevOps & Observability** (3): ruflo-migrations, ruflo-observability, ruflo-cost-tracker

**Extensibility** (2): ruflo-wasm, ruflo-plugin-creator

**Domain-Specific** (3): ruflo-iot-cognitum, ruflo-neural-trader, ruflo-market-data

### 4.5 Agent 定义格式

Agent 使用 YAML 定义，保存在 `.claude/agents/` 和 `.agents/`:

```yaml
# 示例: v3/@claude-flow/agents/coder.yaml
name: coder
type: specialized
capabilities:
  - code_generation
  - code_refactoring
  - debugging
```

---

## 5. 本地部署可行性

### 5.1 安装方式

```bash
# 方式一：一行安装（推荐）
curl -fsSL https://cdn.jsdelivr.net/gh/ruvnet/ruflo@main/scripts/install.sh | bash

# 方式二：交互式安装
npx ruflo@latest init wizard

# 方式三：全局安装
npm install -g ruflo@latest
```

### 5.2 环境要求

| 依赖 | 要求 |
|------|------|
| Node.js | ≥ 20.0.0 |
| npm | 最新版本 |
| 磁盘空间 | ~520MB (含 git history) |
| 网络 | 安装时需要；运行时可离线 (Ollama) |

### 5.3 本地组件

| 组件 | 本地化能力 | 说明 |
|------|----------|------|
| **MCP Server** | ✅ 完全本地 | npx 启动，无外部依赖 |
| **向量数据库** | ✅ 完全本地 | SQLite + HNSW，文件存储 |
| **Embeddings** | ✅ 完全本地 | ONNX Runtime + MiniLM |
| **LLM 推理** | ✅ 支持 | Ollama 集成，可完全离线 |
| **Web UI** | ✅ Docker 自托管 | ruflo/src/ruvocal/Dockerfile |
| **Goal Planner** | ✅ 自托管 | v3/goal_ui/ Vite+Supabase |

### 5.4 冷启动性能

| 路径 | 冷缓存耗时 |
|------|----------|
| 完整 CLI (`@claude-flow/cli`) | ~35s |
| 轻量 CLI (`@claude-flow/cli-core`) | ~1.5s (22.9x 加速) |

### 5.5 加密与安全

- AES-256-GCM 静态加密 (opt-in: `CLAUDE_FLOW_ENCRYPT_AT_REST=1`)
- Ed25519 代码签名验证 (`ruflo verify`)
- 82 个已验证的修复 (verification manifest)
- PII 检测管线 (14 种类型)
- 输入验证、路径遍历防护、CVE 扫描

### 5.6 部署限制

1. **大体积**: 仓库 ~519MB，npm 包也较大
2. **强依赖 Node.js 生态**: 深度耦合 npm/npx
3. **npx 冷启动慢**: 完整版首次加载 ~35s
4. **SQLite 依赖**: 不适合高并发场景
5. **Claude Code 特定**: 虽然支持多 LLM，但编排核心是 Claude Code 专属

---

## 6. 与 ECC (Everything Claude Code) 对比分析

### 6.1 能力矩阵对比

| 维度 | Ruflo | ECC (当前安装) |
|------|-------|---------------|
| **Agent 数量** | 100+ | 1 (code-reviewer) |
| **Skill 数量** | 31+ SKILL.md | 31 (symlinked from Cursor) |
| **MCP Tools** | 300+ | ~~0~~ (通过 skills 间接调用) |
| **Swarm 编排** | ✅ 3 种拓扑 + 3 种共识 | ❌ 无 |
| **向量记忆** | ✅ HNSW + AgentDB | ❌ 无 |
| **自学习** | ✅ SONA + RL + EWC++ | ❌ 无 |
| **跨 session 记忆** | ✅ AgentDB 持久化 | ✅ MEMORY.md (文件级) |
| **多模型路由** | ✅ 5 providers + failover | ❌ 仅 Claude |
| **Hooks 系统** | ✅ 27 hooks | ❌ 少量配置 |
| **代码验证** | ✅ Ed25519 密码学验证 | ❌ 无 |
| **Web UI** | ✅ flo.ruv.io | ❌ 无 |
| **Federation** | ✅ 跨机器协作 | ❌ 无 |
| **安装复杂度** | 高 (520MB, 300+ tools) | 低 (symlinks, 纯文件) |
| **侵入性** | 高 (修改 CLAUDE.md, hooks, settings) | 中 (symlinks, rules) |
| **学习曲线** | 陡峭 (300 tools + 49 commands) | 平缓 (skill = prompt) |

### 6.2 Ruflo 相对 ECC 的优势

1. **真正的 Multi-Agent 系统**: 非简单的 prompt template，而是有编排拓扑、共识算法、反漂移控制的 Agent 网络
2. **向量记忆**: HNSW 索引的语义搜索 vs ECC 的纯文本文件记忆
3. **自学习闭环**: SONA + RL 算法自动从每次任务中学习，ECC 主要靠人工积累 rules
4. **Multi-Provider**: 自动 failover 和成本优化路由，ECC 绑定 Claude
5. **完整性**: 300+ MCP tools 覆盖开发全流程，ECC 主要靠 skill 组合
6. **Federation**: Agent 跨机器/组织协作，ECC 无此概念
7. **密码学验证**: `ruflo verify` 可验证代码完整性
8. **可视化**: Web UI + Goal Planner 提供图形化交互

### 6.3 ECC 相对 Ruflo 的优势

1. **轻量级**: 无需安装大型 npm 包，纯文本 skill 定义，零运行时开销
2. **透明度高**: Skill = SKILL.md + 规则文件，行为完全可预测和可审计
3. **领域专精**: 针对 Deeproute 的飞书、GitLab、Grafana、DRP API 等专用技能
4. **无 vendor lock-in**: 不绑定特定编排框架，每个 skill 独立可替换
5. **渐进式采用**: 可以一个 skill 一个 skill 地使用，不需要"all-in"
6. **可组合性**: Skills 之间松耦合，可以自由组合
7. **冷启动快**: 无 npm install 开销，直接可用
8. **维护简单**: 纯 Markdown 文件，任何编辑器可修改

### 6.4 定位差异总结

| | Ruflo | ECC |
|---|---|---|
| **哲学** | "全自动 Agent 工厂" | "智能工具箱" |
| **目标用户** | 需要大规模 Agent 编排的团队 | 需要领域知识增强的个体开发者 |
| **复杂度** | 高（需要理解 swarm/consensus/RL） | 低（理解 prompt engineering 即可） |
| **代价** | 重安装、冷启动慢、学习曲线陡 | 功能覆盖面有限、无自动学习 |
| **核心价值** | 让 100+ Agent 自动协作完成复杂任务 | 为 Claude Code 补充领域专精知识 |

### 6.5 互补性分析

两者并非完全竞争关系，而是可以在不同层面互补:

1. **Ruflo 做编排层**: 大规模代码生成、测试、审查的自动化
2. **ECC 做知识层**: 特定领域的知识注入（飞书文档搜索、GitLab CI 诊断、Grafana 监控查询等）
3. **结合方式**:
   - Ruflo 的 Agent 可以调用 ECC skills 获取领域知识
   - ECC 可以借鉴 Ruflo 的 memory 机制实现更好的跨 session 记忆
   - ECC 可以作为 Ruflo 的 "domain plugin" 扩展

---

## 7. 关键风险与担忧

### 7.1 技术风险

1. **过度工程化**: 300+ MCP tools + 49 CLI commands + 9 RL algorithms + 3 consensus algorithms，大部分用户实际可能只用 10%
2. **维护负担**: 520MB 仓库、多个 alpha 版本并存 (3.7.0-alpha.18)，版本管理复杂
3. **依赖链脆弱**: 依赖 @ruvector/rabitq-wasm (Rust→WASM)、ONNX Runtime 等重依赖
4. **"Magic" 风险**: 太多的自动化（自动路由、自动学习、自动优化）可能导致行为不可预测
5. **质量不稳定**: alpha 版本号说明仍在快速迭代，API 可能频繁变动

### 7.2 实用性质疑

1. **是否真需要 100 个 Agent？** 当前我们只有 1 个 code-reviewer agent 也工作良好
2. **自学习效果存疑**: SONA 声称 +55% 质量提升，但当 benchmark 只有 +1.2%~5.0% 的 domain improvement
3. **47k stars 但活跃度不明**: 高 star 数可能来自早期的 Claude Flow 时期积累
4. **文档 vs 代码一致性**: 大量功能在 SKILL.md 中描述，但实际的 TS 实现可能不同步

### 7.3 集成风险

1. **CLAUDE.md 改写**: `ruflo init` 会修改项目的 CLAUDE.md，可能与现有配置冲突
2. **Hooks 冲突**: 27 hooks 可能与现有的 hooks 设置冲突
3. **Token 消耗**: 300+ tool definitions 会占用 Claude Code context window
4. **成本不可控**: 多 Agent 自动协作可能导致大量 LLM 调用，成本难以预算

---

## 8. 结论与建议

### 8.1 评估结论

Ruflo 是目前 **Claude Code 生态中最全面、最激进的多 Agent 编排方案**。它在技术架构上展现了极强的工程能力：DDD 分层设计、WASM 加速、HNSW 向量搜索、自学习闭环、密码学验证，这些都是真正的技术创新。

但它的全面性也是它的弱点：**过重的架构、陡峭的学习曲线、以及"黑盒"式的自动化**，使得它的实际价值高度取决于使用场景的复杂度和团队的技术能力。

### 8.2 建议

**短期建议（当前阶段）**:
- **不推荐全面采用 Ruflo**。当前的 ECC 体系已经覆盖核心需求（代码审查、领域知识、规则管理）
- **可以关注 Ruflo 的以下模块**，作为 ECC 的增量参考:
  1. Memory 机制 → 参考实现更好的跨 session 记忆
  2. SPARC 方法论 → 可借鉴其开发流程
  3. Hooks 设计 → 参考 PreCompact/Stop hook 的设计思路

**中期观望**:
- 等待 Ruflo 进入稳定版 (3.7 → 4.0)
- 评估是否需要 Swarm 编排能力（当前单 Agent + skills 模式够用）
- 如果项目复杂度上升到需要多 Agent 自动协作，再考虑集成

**长期策略**:
- ECC 继续深耕**领域专精**方向（Deeproute 特定工具链）
- 如果 Ruflo 社区成熟且稳定，可以作为 ECC 的编排层，保留 ECC skills 作为领域知识注入层

### 8.3 值得借鉴的设计

| 特性                     | 借鉴价值    | 实现难度 |
| ---------------------- | ------- | ---- |
| HNSW 向量记忆              | ⭐⭐⭐⭐⭐ 高 | 中    |
| 跨 session 状态持久化        | ⭐⭐⭐⭐⭐ 高 | 低    |
| PreCompact hook 指导     | ⭐⭐⭐⭐    | 低    |
| Thompson Sampling 模型路由 | ⭐⭐⭐     | 中    |
| WASM Agent Booster     | ⭐⭐⭐     | 高    |
| 密码学验证                  | ⭐⭐      | 高    |

---

## 9. 实际使用指南（How-To）

### 9.1 快速上手（只需 2 步）

官方在 Issue #1196 中明确回复：**你不需要学 300+ MCP 工具或 26 个 CLI 命令**。init 之后正常使用 Claude Code 即可，hooks 系统会自动在后台路由任务、学习模式、协调多 Agent。

```bash
# Step 1: 在项目目录初始化
npx ruflo@latest init wizard
# 交互式向导，选择 preset（minimal / full），
# 自动生成 .claude/settings.json, hooks, CLAUDE.md 等

# Step 2: 注册 MCP Server 到 Claude Code（或 Cursor）
claude mcp add ruflo -- npx ruflo@latest mcp start

# Step 3: 正常使用 Claude Code / Cursor
# hooks 系统会自动：
#   - 路由任务到最合适的 Agent
#   - 学习成功模式并复用
#   - 在需要时协调多 Agent 协作
```

### 9.2 两种安装路径选择

| | **Path A: Plugin（轻量试用）** | **Path B: CLI Full（生产使用）** |
|---|---|---|
| **安装** | `/plugin marketplace add ruvnet/ruflo` | `npx ruflo@latest init wizard` |
| **侵入性** | 零文件写入 | 写入 .claude/, CLAUDE.md, helpers |
| **功能** | 斜杠命令 + 少量 skill | 98 agents, 60+ commands, MCP, hooks |
| **MCP** | 不注册 | 注册 300+ tools |
| **适合** | 试单个 plugin 功能 | 需要完整编排能力 |

#### Path A: Plugin 安装（推荐先试这个）

```bash
# 在 Claude Code 中执行
/plugin marketplace add ruvnet/ruflo

# 安装你需要的 plugin
/plugin install ruflo-core@ruflo       # 基础核心
/plugin install ruflo-swarm@ruflo      # Swarm 编排
/plugin install ruflo-autopilot@ruflo  # 自动循环
/plugin install ruflo-rag-memory@ruflo # HNSW 记忆
```

#### Path B: 完整 CLI 安装

```bash
# 方式一：一行安装脚本
curl -fsSL https://cdn.jsdelivr.net/gh/ruvnet/ruflo@main/scripts/install.sh | bash

# 方式二：全套安装（global + MCP + 诊断）
curl -fsSL https://cdn.jsdelivr.net/gh/ruvnet/ruflo@main/scripts/install.sh | bash -s -- --full

# 方式三：npx 交互式
npx ruflo@latest init wizard

# 方式四：全局安装
npm install -g ruflo@latest
ruflo init
```

### 9.3 Cursor IDE 集成

在 `.cursor/mcp.json` 中添加：

```json
{
  "mcpServers": {
    "ruflo": {
      "command": "npx",
      "args": ["ruflo@latest", "mcp", "start"],
      "env": {
        "ANTHROPIC_API_KEY": "sk-ant-..."
      }
    }
  }
}
```

> **注意**：Cursor 必须在 Agent Mode 下才能访问 MCP tools。Cursor 最多支持 40 个 MCP tools，而 Ruflo 有 300+，需要通过环境变量筛选 tool group。

```bash
# 控制加载哪些 tool group（减少 token 消耗）
export CLAUDE_FLOW_TOOL_GROUPS=implement,test,fix,memory

# 或使用预设模式
export CLAUDE_FLOW_TOOL_MODE=develop  # develop / pr-review / devops / triage
```

### 9.4 Ruflo 工作流程图解

#### 9.4.1 复杂任务流程（以 JWT 认证为例）

```
用户输入: "实现 JWT 用户认证"
         │
         ▼
┌─────────────────────────┐
│  Pre-task Hook 分析      │
│  复杂度: 高              │
│  推荐: Opus + Swarm     │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│  memory_search (HNSW)   │
│  检索: "JWT auth"        │
│  命中 3 个历史模式:       │
│   • Express JWT (0.89)  │
│   • bcrypt hash (0.82)  │
│   • Role guard (0.78)   │
│  → 注入 Agent 上下文      │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────────────────────────┐
│  Swarm 初始化 (hierarchical topology)        │
│                                              │
│  Queen (strategic)                           │
│    ├── architect → 设计架构      (Opus, 3s)  │
│    ├── coder     → User model   (Sonnet, 1.5s) ← 简单,便宜模型│
│    ├── coder     → controller   (Opus, 2.8s)   ← 复杂,强模型  │
│    ├── coder     → middleware   (Sonnet, 1.2s) ← 模式化       │
│    └── tester    → 测试用例     (Haiku, 0.8s)  ← 最便宜       │
│                                              │
│  Queen checkpoint 验证:                       │
│    ✓ 文件结构符合设计                           │
│    ✓ 覆盖 register/login/refresh             │
│    ✗ 缺少 rate limiting → 自动分配补充         │
└──────────┬──────────────────────────────────┘
           │
           ▼
┌─────────────────────────┐
│  Post-task Hook 学习     │
│  存储成功模式到 AgentDB  │
│  更新路由权重             │
│  下次复用此流水线         │
└─────────────────────────┘
```

**对比效果**:

| 维度 | 纯 Claude Code | 有 Ruflo |
|---|---|---|
| 耗时 | ~45s（串行） | ~8s（并行 Agent） |
| Token | 全程 Opus | 混合模型，省 ~60% |
| 遗漏检查 | 依赖人工 review | Queen 自动检测 |
| 复用性 | 每次从头 | 检索历史模式 |

#### 9.4.2 简单任务流程（var → const 替换）

```
用户输入: "把 var 全换成 const"
         │
         ▼
┌─────────────────────────┐
│  Pre-task Hook 分析      │
│  复杂度: 极低             │
│  Intent: var-to-const   │
│  路由: WASM Booster     │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│  Agent Booster (WASM)    │
│  regex 替换: var → const │
│  耗时: 0.3ms             │
│  Token: 0                │
│  → 完全跳过 LLM          │
└─────────────────────────┘
```

#### 9.4.3 智能路由决策树

```
任务进入
  │
  ├── 简单 (var→const, remove-console, add-types)
  │     └── WASM Agent Booster: <1ms, $0
  │
  ├── 中等 (bug fix, 单文件重构, 测试生成)
  │     └── Haiku/Sonnet: ~500ms, $0.0002-0.003
  │
  └── 复杂 (新功能, 多文件架构, 安全设计)
        └── Opus + Swarm: 2-5s, $0.015
              │
              ├── hierarchical (防漂移,推荐)
              ├── mesh (独立并行)
              └── adaptive (动态切换)
```

#### 9.4.4 自学习闭环

```
RETRIEVE                    ROUTE
  检索 k=3 相似模式            应用到未来路由
  (HNSW, 0.87ms)              │
       │                      │
       ▼                      ▲
    JUDGE                 CONSOLIDATE
  评估当前策略效果          整合到 ReasoningBank
       │                      │
       ▼                      ▲
    DISTILL ──────────────────┘
  提取成功模式为可复用知识

每次任务完成后:
  memory_store() → SONA 提取模式 → EWC++ 防遗忘 → 更新路由权重
```

### 9.5 常用操作场景

#### 场景一：正常开发（最简单）

init 之后直接使用 Claude Code / Cursor，hooks 自动工作：

- **简单任务**（变量重命名等）→ WASM Agent Booster 处理，<1ms，不消耗 token
- **中等任务**（bug 修复）→ 路由到 Haiku/Sonnet
- **复杂任务**（新功能开发）→ Opus + Swarm 协调

#### 场景二：启动 Hive-Mind 完成大任务

```bash
# 初始化 hive-mind
npx ruflo@latest hive-mind init

# 启动 swarm 并给出目标
npx ruflo@latest hive-mind spawn "Implement user authentication with JWT"

# 查看状态
npx ruflo@latest hive-mind status

# 查看性能指标
npx ruflo@latest hive-mind metrics
```

#### 场景三：手动生成和管理 Agent

```bash
# 查看可用 agent 类型
npx ruflo@latest agent list

# 生成特定类型的 agent
npx ruflo@latest agent spawn -t coder --name my-coder
npx ruflo@latest agent spawn -t tester --name my-tester
npx ruflo@latest agent spawn -t reviewer --name my-reviewer

# 查看 agent 状态
npx ruflo@latest agent status
```

#### 场景四：使用向量记忆

```bash
# 存储模式
# (通过 MCP tool) memory_store(key="auth-pattern", value="JWT refresh flow", namespace="patterns")

# 搜索相似模式
npx ruflo@latest memory search --query "authentication patterns"

# 查看记忆统计
npx ruflo@latest memory stats
```

#### 场景五：初始化 Swarm 进行多 Agent 协作

```bash
# 初始化 hierarchical swarm（推荐，防漂移）
npx ruflo@latest swarm init --topology hierarchical --maxAgents 8

# 或通过 MCP tool（在 Claude Code/Cursor 中）
# swarm_init({ topology: "hierarchical", maxAgents: 8, strategy: "specialized" })
```

#### 场景六：安全审计

```bash
npx ruflo@latest security scan
npx ruflo@latest security audit
npx ruflo@latest security cve
```

### 9.5 初始化后的诊断

```bash
# 检查安装是否正确
npx ruflo@latest doctor

# 查看系统状态
npx ruflo@latest status

# 查看 MCP 工具列表
npx ruflo@latest mcp tools

# 查看 hooks 状态
npx ruflo@latest hooks intelligence --status
```

### 9.6 关键 MCP Tools（Claude Code / Cursor 中可用）

| MCP Tool | 用途 | 何时使用 |
|---|---|---|
| `memory_search` | 语义向量搜索已存模式 | **任务开始前**搜索相似模式 |
| `memory_store` | 存储成功模式 | **任务完成后**保存经验 |
| `swarm_init` | 初始化 Swarm 协调 | 复杂多文件任务开始时 |
| `agent_spawn` | 注册 Agent 角色 | 多 Agent 工作流 |
| `neural_train` | 训练模式 | 周期性改进 |
| `hooks_route` | 智能任务路由 | 不确定用哪个 agent 时 |

### 9.7 配置环境变量

```bash
# 必需（使用 Claude 模型时）
export ANTHROPIC_API_KEY="sk-ant-..."

# 可选：其他 LLM 提供商
export OPENAI_API_KEY="sk-..."
export GOOGLE_API_KEY="..."

# 可选：日志级别
export CLAUDE_FLOW_LOG_LEVEL=info  # debug / info / warn / error

# 可选：加密（生产环境推荐）
export CLAUDE_FLOW_ENCRYPT_AT_REST=1
```

### 9.8 社区反馈的关键注意点

来自 Issue #1196 和 #1251，实际用户踩过的坑：

1. **不需要手动启动什么** — `init` 之后正常用 Claude Code，hooks 自动工作
2. **ruflo = claude-flow** — 只是改了个名字，底层完全一样
3. **状态栏数字** — 显示 Agent 数量、内存用量、Swarm 拓扑、学习进度，可以在 settings.json 中关闭
4. **冷启动慢** — 完整版首次 npx 约 35s，使用 `--omit=optional` 可缩小到 45MB / ~15s
5. **不要一开始就用 hive-mind** — 先用 hooks 自动模式体验，再按需使用高级功能

### 9.9 升级

```bash
# 更新 helpers 和 statusline（保留数据）
npx ruflo@latest init upgrade

# 更新并添加新版本的 skills/agents/commands
npx ruflo@latest init upgrade --add-missing
```

---

## 10. 我们环境的适用性评估

### 10.1 当前环境

- **Claude Code**: 通过 Cursor IDE 使用
- **已有体系**: ECC skills + Agent Learning System + Engram 语义搜索
- **工作区类型**: 本地 + SSHFS 远程

### 10.2 可以尝试的路径

**最低成本试用**：使用 Path A（Plugin 方式）安装 `ruflo-core` + `ruflo-rag-memory`，不影响现有配置，体验向量记忆和基础编排能力。

**中等投入试用**：在一个隔离的测试项目中执行 `npx ruflo@latest init wizard`，完整体验 hooks 自动路由 + Swarm 编排 + 自学习闭环。

**生产集成**（不推荐当前阶段）：Ruflo 仍在 alpha 阶段（3.7.0-alpha），与现有 ECC 体系有 hooks 冲突风险，且 CLAUDE.md 覆写问题未完全解决。

### 10.3 与当前体系的冲突点

| 冲突点 | 说明 | 规避方案 |
|---|---|---|
| CLAUDE.md 覆写 | `ruflo init` 会修改 CLAUDE.md | 备份后 init，或用 Plugin 路径 |
| Hooks 冲突 | 27 hooks vs 现有 hooks | 在测试项目中隔离试用 |
| MCP tool 过多 | 300+ tools 占 context window | 用 CLAUDE_FLOW_TOOL_MODE 过滤 |
| 记忆系统冲突 | AgentDB vs Engram/MEMORY.md | 可共存，但需明确分工 |

---

## 11. 实机测试记录 (2026-05-13)

### 11.1 安装过程

| 步骤 | 命令 | 结果 |
|---|---|---|
| npm 镜像 | `npm config set registry https://registry.npmmirror.com` | ✓ |
| 全局安装 | `npm install -g ruflo@latest --omit=optional` | ✓ v3.7.0-alpha.27 |
| 初始化 (minimal) | `ruflo init wizard` → minimal preset | ✓ 但只生成配置，无 hooks 脚本 |
| 重新初始化 (force) | `npx ruflo@latest init --force` | ✓ 85 文件, 98 agents, 7 hook types |
| MCP 注册 | `claude mcp add ruflo -- npx -y ruflo@latest mcp start` | ✓ 写入 .claude.json |
| 诊断 | `ruflo doctor` | ✓ 11 passed, 6 warnings |

**关键发现**: `init wizard` 的 minimal preset 不安装实际 hooks 脚本，必须用 `init --force` 才能获得完整功能。

### 11.2 记忆系统测试

```bash
ruflo memory init                                    # ✓ 15 controllers activated, 885ms
ruflo memory store -k "key" --value "..." --namespace "patterns"  # ✓ 384-dim vector
ruflo memory search -q "query"                       # ✓ 0-1ms 检索
ruflo memory stats                                   # ✓ sql.js + HNSW backend
```

**注意**: Transformers.js 初始化失败 (fetch failed)，使用了 mock embeddings。真实语义搜索需要先下载模型 (~90MB)：
```bash
npx agentdb install-embeddings
```

### 11.3 智能路由测试

```bash
ruflo hooks route --task "Fix a bug in login auth"
# → security-architect (90% confidence), coder (80%), tester (70%)
# 路由延迟: 0.733ms, 方法: keyword matching

ruflo hooks route --task "Refactor test framework for parallel execution"  
# → architect (44%), coder (34%), tester (24%)
# 复杂度: MEDIUM, 预估: 30-60 min

ruflo hooks route --task "rename variable from x to count"
# → performance-engineer (58%) ← mock embedding 导致不准确
# 复杂度: LOW
```

### 11.4 Swarm & Agent 测试

```bash
ruflo swarm init --topology hierarchical    # ✓ ID: swarm-xxx, max 15 agents
ruflo agent spawn -t coder --name c1        # ✓ registered, capabilities: code-generation, refactoring, debugging
ruflo agent spawn -t tester --name t1       # ✓ registered, capabilities: unit-testing, integration-testing
ruflo agent spawn -t reviewer --name r1     # ✓ registered, capabilities: code-review, security-audit
ruflo agent list                            # ✓ 3 agents, all idle
ruflo swarm status                          # ✓ 5% progress, 0 tasks
```

### 11.5 Neural Training 测试

```bash
ruflo neural train -p coordination
# ✓ 50 epochs in 0.9s
# Backend: WASM (native)
# MicroLoRA: 256-dim, <1μs adaptation
# ReasoningBank: 7 patterns
# Persisted to: .claude-flow/neural/patterns.json

ruflo neural status
# SONA Coordinator: Active (1.12μs avg)
# ReasoningBank: 7 patterns
# Flash Attention: Available
# Int8 Quantization: Available
```

### 11.6 与 Claude CLI 集成测试

```bash
claude --permission-mode bypassPermissions
# → RuFlo V3.6 状态栏正常显示
# → 16/16 hooks 已启用
# → AgentDB MCP 1/1 连接正常
```

**核心发现**: 使用 DeepSeek 模型时，hooks/Swarm/AgentDB 不会被自动调用。Ruflo 的自动化体系 (CLAUDE.md 指导 + MCP tools 调用) 是为 Claude 模型设计的。使用其他模型需要手动调用 CLI 命令。

### 11.7 生成的文件结构

```
/tmp/hil_auto_test/
├── CLAUDE.md                          # Claude Code 指导文件 (Ruflo 重写)
├── .mcp.json                          # MCP server 配置
├── .claude/
│   ├── settings.json                  # hooks + env + permissions
│   ├── helpers/                       # 43 个脚本文件
│   │   ├── statusline.cjs             # 状态栏
│   │   ├── hook-handler.cjs           # hook 处理器
│   │   ├── intelligence.cjs           # 智能路由
│   │   ├── learning-service.mjs       # 学习服务
│   │   ├── swarm-hooks.sh             # Swarm hooks
│   │   └── ...
│   ├── commands/                      # 10 个命令目录
│   │   ├── analysis/
│   │   ├── automation/
│   │   ├── github/
│   │   ├── hooks/
│   │   ├── sparc/
│   │   └── ...
│   └── agents/                        # 98 个 agent 定义
│       ├── core/
│       ├── development/
│       ├── architecture/
│       ├── consensus/
│       ├── sparc/
│       └── ...
├── .claude-flow/
│   ├── config.yaml                    # Ruflo 配置
│   ├── data/                          # 运行时数据
│   ├── logs/                          # 日志
│   ├── sessions/                      # 会话数据
│   ├── neural/                        # 神经学习数据
│   │   └── patterns.json              # 训练后的模式
│   └── embeddings.json                # 嵌入配置
└── .swarm/
    └── memory.db                      # SQLite 记忆数据库
```

---

## 12. 最佳实践总结

### 12.1 安装建议

1. **始终用 `init --force`**，不要用 `init wizard` 的 minimal preset（缺少 hooks 脚本）
2. **先设 npm 镜像**（国内环境）：`npm config set registry https://registry.npmmirror.com`
3. **在隔离目录试用**，避免污染现有项目的 CLAUDE.md 和 hooks
4. **安装 ONNX 嵌入模型**以获得真实语义搜索：`npx agentdb install-embeddings`

### 12.2 日常使用建议

1. **不需要记命令**——init 后正常用 Claude Code，hooks 自动工作（前提是用 Claude 模型）
2. **非 Claude 模型用户**需要手动调用 CLI 命令来使用 Ruflo 功能
3. **先用路由测试**验证 Ruflo 的分析是否合理：`ruflo hooks route --task "你的任务"`
4. **定期训练**以保持学习效果：`ruflo neural train -p coordination`

### 12.3 适合的场景

| 场景 | 推荐用法 | 理由 |
|---|---|---|
| 大规模代码生成 | Hive-Mind + hierarchical | Queen 协调防漂移 |
| Bug 修复 | hooks 自动路由 | 自动选最合适的 Agent |
| 简单重构 | 自动 WASM Booster | 零 token 消耗 |
| 跨项目知识复用 | memory store/search | 向量检索历史模式 |
| 安全审计 | security scan | 自动 CVE 检测 |

### 12.4 不适合的场景

1. 使用非 Claude 模型（DeepSeek 等）——自动化体系不生效
2. 小型简单任务——Ruflo 的开销（状态栏、hooks、MCP）大于收益
3. 需要精确控制 prompt 的场景——Ruflo 的 CLAUDE.md 会注入大量指导
4. 对 context window 敏感的场景——300+ MCP tools 定义占用大量 token

### 12.5 我们环境的最终结论

**当前不建议在生产项目中使用 Ruflo**。原因：
1. 我们主要用 DeepSeek 模型，Ruflo 的自动化体系不生效
2. 现有 ECC + Engram 体系已满足需求
3. Ruflo 仍在 alpha 阶段，API 不稳定

**值得借鉴并自行实现的能力**：
1. **hooks 自动路由**——可以在我们的 rules 中实现类似的任务复杂度分析
2. **向量记忆自动学习**——Engram 已有语义搜索，但缺少 SONA 式的自动学习闭环
3. **状态栏**——Ruflo 的 statusline 设计很好，可以参考

---

*调研完成时间: 2026-05-09 · 实际使用指南更新: 2026-05-13 · 实机测试: 2026-05-13*
*数据来源: GitHub API, README.md, USERGUIDE.md, STATUS.md, verification.md, .agents/config.toml, hooks.json, SKILL.md, Issue #1196, Issue #1251, 本地安装实测*