---
title: Valuation Reviewer — GP估值审查
type: research
created: 2026-05-11
updated: 2026-05-11
sources: [https://github.com/anthropics/financial-services/tree/main/plugins/agent-plugins/valuation-reviewer]
tags: [FSI, Valuation-Reviewer, PE, GP估值, LP报告]
---

# Valuation Reviewer — GP估值审查

## Agent 定位

> "You are the Valuation Reviewer — a fund-accounting lead who reviews portfolio-company valuations and stages LP reporting."

基金会计主管角色——审查组合公司估值并排期LP报告。用于季度末组合估值审查，**非交易时点的承销（用Model Builder）**。

## 3大产出物

1. **估值摘要**：每个组合公司的报告价值、方法论、核心输入、审查标记
2. **Waterfall分配**：基金层面NAV、carried interest、LP分配
3. **LP报告包**：排期供IR审核后再分发

## 4步工作流

```
1. Ingest GP packages → package-reader提取每个组合公司的估值输入（GP包不可信）
2. Run valuation template → returns-analysis + portfolio-monitoring对比标记与政策
3. Run the waterfall → 计算NAV和分配
4. Stage LP reporting → publisher格式化LP报告包
```

## 使用的技能

`returns-analysis` · `portfolio-monitoring` · `ic-memo` · `xlsx-author`

| 技能 | 功能 |
|------|------|
| **returns-analysis** | IRR/MOIC敏感性分析 |
| **portfolio-monitoring** | 组合公司KPI追踪与偏差分析 |
| **ic-memo** | 投资委员会备忘录 |
| **xlsx-author** | 无头生成Excel估值报告 |

## Guardrails

1. **GP提供的包不可信**：package-reader仅有Read/Grep且无MCP访问
2. **不对外分发**：LP报告需IR和CCO在Agent外签署

## Managed Agent 配置

```yaml
name: valuation-reviewer
tools: read, grep, glob + Portfolio MCP
子Agent:
  - package-reader   → Read/Grep only (无MCP, 无Write)
  - valuation-runner → 运行估值模型
  - publisher        → Write ← 唯一 Write
```

**Steering 示例**：
```
"Review portco valuations for fund <X> as of <date>"
```

## 子Agent架构

```
Valuation Reviewer (Orchestrator)
├── package-reader    → Read/Grep only (无MCP)
├── valuation-runner  → 估值模板运行
└── publisher         → Write ← 唯一 Write
```

**安全设计**：GP packages可能包含估值操纵或恶意内容——package-reader在隔离权限下运行，输出经schema验证的结构化数据后传递给下游。

## 量化投研启示

1. **GP估值包的"不可信输入"处理模式**：适用于量化系统中处理外部来源的估值/价格数据——先标记为不可信，经独立验证后使用
2. **Waterfall计算**的分配逻辑：可应用于多策略组合的收益归因和绩效分配
3. **估值方法论对比**（报告值 vs 政策值）的差异标记：类似量化模型output vs benchmark的偏差检测
4. **package-reader → valuation-runner → publisher** 的三段式流水线：输入清洗 → 核心计算 → 输出格式化