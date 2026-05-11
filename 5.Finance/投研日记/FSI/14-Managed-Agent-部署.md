---
title: Managed Agent Cookbook + 部署脚本
type: research
created: 2026-05-11
updated: 2026-05-11
sources: [https://github.com/anthropics/financial-services/tree/main/managed-agent-cookbooks, https://github.com/anthropics/financial-services/tree/main/scripts]
tags: [FSI, Managed-Agent, CMA, 部署, 编排]
---

# Managed Agent Cookbook + 部署脚本

## 一、Managed Agent Cookbook 架构

### 目录结构

每个Agent一个目录：
```
managed-agent-cookbooks/<slug>/
├── agent.yaml              # 主配置（system prompt + skills + tools + 子Agent）
├── subagents/              # depth-1 叶子 workers
│   ├── *.yaml              # 各子Agent的配置
│   └── ...
├── steering-examples.json  # Steering event 示例
└── README.md               # 安全等级 + handoff 说明
```

### 核心设计模式

**Only bold leaf = Write**：在每个Agent的3个子Agent中，只有**粗体标记的那一个**（最后一个）持有 Write 权限：

| Agent | Reader/Worker 1 | Worker 2 | Writer |
|-------|:---:|:---:|:---:|
| Pitch Agent | researcher | modeler | **deck-writer** |
| Market Researcher | sector-reader | comps-spreader | **note-writer** |
| Earnings Reviewer | transcript-reader | model-updater | **note-writer** |
| Meeting Prep | profiler | news-reader | **pack-writer** |
| Model Builder | data-puller | **builder** | auditor |
| GL Reconciler | reader | critic | **resolver** |
| KYC Screener | doc-reader | rules-engine | **escalator** |
| Valuation Reviewer | package-reader | valuation-runner | **publisher** |
| Month-End Closer | ledger-reader | rollforward | **poster** |
| Statement Auditor | statement-reader | reconciler | **flagger** |

> Model Builder 是个例外——builder（中间worker）持有Write，auditor仅有Read做独立审计。

### agent.yaml 结构

```yaml
name: pitch-agent
model: claude-opus-4-7

system:
  file: ../../plugins/agent-plugins/pitch-agent/agents/pitch-agent.md
  append: "You are running headless. Produce files in ./out/..."

tools:
  - type: agent_toolset_20260401
    configs:
      - { name: read, enabled: true }
      - { name: grep, enabled: true }
      - { name: glob, enabled: true }
  - { type: mcp_toolset, mcp_server_name: capiq }

mcp_servers:
  - { type: url, name: capiq, url: "${CAPIQ_MCP_URL}" }

skills:
  - { from_plugin: ../../plugins/agent-plugins/pitch-agent }

callable_agents:
  - { manifest: ./subagents/researcher.yaml }
  - { manifest: ./subagents/modeler.yaml }
  - { manifest: ./subagents/deck-writer.yaml }
```

### Manifest 约定 vs API 实际字段

| Manifest 约定 | 解析后 |
|---|---|
| `system: {file: ..., append: "..."}` | `system: "<内联内容 + append>"` |
| `system: {text: "..."}` | `system: "<text>"` |
| `skills: [{from_plugin: ...}]` | 上传skills/*下的每个skill → `[{type: custom, skill_id: ...}]` |
| `skills: [{path: ...}]` | `skills: [{type: custom, skill_id: <已上传ID>}]` |
| `callable_agents: [{manifest: ...}]` | 先创建子Agent → `[{type: agent, id: <created-id>, version: latest}]` |

**重要限制**：`callable_agents` 是预览功能，仅支持**一层委托**——Orchestrator可调用workers；workers不能调用更深的子Agent。

---

## 二、部署脚本

### deploy-managed-agent.sh

**功能**：一键部署Agent模板到 CMA API (`POST /v1/agents`)。

```bash
export ANTHROPIC_API_KEY=sk-ant-...
scripts/deploy-managed-agent.sh gl-reconciler
```

**处理流程**：
1. 解析 `agent.yaml` 中的 `system: {file: ...}` → 内联 system prompt
2. 解析 `skills: [{from_plugin: ...}]` → 发现skills/下所有目录 → 逐个上传到 `/v1/skills` → 替换为skill_id引用
3. 递归创建 `callable_agents` → 先创建叶子workers → 然后创建orchestrator（引用子Agent ID）
4. POST `/v1/agents` 使用解析后的配置

**依赖**：jq + python3 (pyyaml)

**环境变量**：
- `ANTHROPIC_API_KEY` — 必需
- `ANTHROPIC_API_BASE` — 默认 `https://api.anthropic.com`
- `DEPLOY_DEBUG` — 打印详细调试信息
- `SKILL_TITLE_PREFIX` — Skill 标题前缀

### orchestrate.py

**参考实现**——跨Agent handoff的事件循环。

**核心流程**：
```
Agent A 完成工作 → 输出 handoff_request JSON → orchestrate.py 解析
→ 验证目标白名单 + schema验证payload → steering event 发送到 Agent B
```

**Handoff 格式**：
```json
{"type": "handoff_request", "target_agent": "earnings-reviewer", "payload": {"event": "Process earnings: AAPL Q2 2025"}}
```

**安全设计**：
- **硬白名单**：`ALLOWED_TARGETS` 集合——只有已部署的10个Agent slug可通过
- **Schema验证**：每个handoff payload经 `jsonschema.validate` 检查
- **已知威胁模型注释**：攻击者可通过文档内容注入 handoff_request 文本——用白名单+schema缓解

### 其他脚本

| 脚本 | 功能 |
|------|------|
| `check.py` | **提交前必须运行**——lint 所有 manifest，验证所有交叉引用解析正确，检测bundled skills与vertical source drift |
| `validate.py` | 验证交叉文件引用 |
| `sync-agent-skills.py` | 从 `vertical-plugins/` → `agent-plugins/` 同步skills |
| `test-cookbooks.sh` | 测试cookbook配置 |

---

## 三、安全等级与Handoff

每个Agent的 README.md 标注了安全等级和处理说明。

### 统一安全模式

1. **Reader子Agent**（处理外部文档）：仅有 Read/Grep，无 MCP，无 Write
2. **Orchestrator**：有 Read/Grep/MCP，**无 Write**（不直接修改文件）
3. **单一Writer**：每个Agent只有一个子Agent持有Write——且它不接触外部数据源

### Handoff 设计

- 命名Agent之间**不直接互相调用**
- 当一个Agent需要另一个Agent时，在输出中发出 `handoff_request`
- 由外部编排层（orchestrate.py / Temporal / Airflow）路由到目标Agent
- 路由层强制进行目标白名单验证和payload schema验证

---

## 四、MCP 配置方式

环境变量注入：`mcp_servers[].url` 支持 `${CAPIQ_MCP_URL}` 格式的变量替换。

```yaml
mcp_servers:
  - { type: url, name: capiq, url: "${CAPIQ_MCP_URL}" }
  - { type: url, name: daloopa, url: "${DALOOPA_MCP_URL}" }
```

部署时注入实际URL。

---

## 量化投研启示

1. **Agent.yaml 的标准化声明格式**：system + model + tools + skills + subagents 的五要素声明——量化策略的部署配置可借鉴此结构
2. **Manifest约定 vs API字段** 的抽象层：部署脚本做文件→API的转换——量化策略的"策略定义文件"→"执行引擎配置"可类似转换
3. **Handoff硬白名单**：Agent间通信必须经过白名单验证——量化交易中策略信号传递也应经过白名单路由
4. **环境变量注入MCP URL**：数据源URL通过变量注入而非硬编码——量化数据管道的配置管理
5. **单一Write叶子节点**的安全架构：只允许最下游的格式化节点写文件——量化策略中只允许最终信号输出模块写数据库/发订单
6. **sync-agent-skills.py的skill同步机制**：维护单一源+自动同步——量化策略代码的factor定义统一管理+自动分发
7. **check.py的pre-commit lint**：强制验证交叉引用——量化策略上线前强制验证所有参数引用完整性