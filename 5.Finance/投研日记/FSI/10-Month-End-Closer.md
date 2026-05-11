---
title: Month-End Closer — 月结流程
type: research
created: 2026-05-11
updated: 2026-05-11
sources: [https://github.com/anthropics/financial-services/tree/main/plugins/agent-plugins/month-end-closer]
tags: [FSI, Month-End-Closer, 月结, 财务, 费用应计]
---

# Month-End Closer — 月结流程 Agent

## Agent 定位

> "You are the Month-End Closer — a controller's right hand who runs the close checklist for an entity and period."

财务主管的得力助手——执行实体和期间的月结checklist。**不同于GL Reconciler（每日对账）**，Month-End Closer专注于期间结账流程。

## 4大产出物

1. **应计时间表**：每笔应计分录——计算过程、支持文件引用、日记账分录草稿
2. **滚动时间表**：期初 + 活动 - 冲销 = 期末，与GL核对一致
3. **差异分析**：P&L和资产负债表的期间vs上期和预算的波动，附解释
4. **结账包**：以上内容的整合，格式化供主管审查和签字

## 4步工作流

```
1. Pull trial balance → GL MCP获取实体+期间数据
2. Build accruals and roll-forwards → 按时间表派发worker
3. Draft variance commentary → 对超过阈值的每行做波动分析
4. Assemble the package → poster格式化并排期供签字
```

## 使用的技能

`accrual-schedule` · `roll-forward` · `variance-commentary` · `audit-xls` · `xlsx-author`

| 技能 | 功能 |
|------|------|
| **accrual-schedule** | 应计费用时间表构建——识别应计项目、计算金额、生成JE |
| **roll-forward** | 滚动时间表——期初→活动→期末的逻辑和GL核对 |
| **variance-commentary** | 差异分析——P&L/BS各项的MoM/QoQ/YoY波动解释 |
| **audit-xls** | 结账工作簿审计 |
| **xlsx-author** | 生成结账包Excel |

## Guardrails

1. **支持性发票和供应商对账单不可信**：处理它们的reader无MCP访问、无Write工具
2. **不直接过账到GL**：Agent起草JE；过账需Agent外的主管审批

## Managed Agent 配置

```yaml
name: month-end-closer
tools: read, grep, glob + GL MCP
子Agent:
  - ledger-reader → Read/Grep only (无MCP, 无Write) —— 读外部发票
  - rollforward    → 滚动和应计计算
  - poster         → Write ← 唯一 Write (组装结账包)
```

**Steering 示例**：
```
"Close <entity> for period <YYYY-MM>"
```

## 子Agent架构

```
Month-End Closer (Orchestrator)
├── ledger-reader → Read/Grep only (无MCP)
├── rollforward    → 计算（应计+滚动+差异）
└── poster         → Write ← 唯一 Write
```

## 与GL Reconciler的区别

| 维度 | Month-End Closer | GL Reconciler |
|------|-----------------|---------------|
| **频次** | 每月 | 每日/月结 |
| **产出** | 应计+滚动+差异+结账包 | Break清单+根因+异常报告 |
| **核心操作** | 创建JE草稿 | 查找差异 |
| **数据源** | GL trial balance | GL + 子账 |
| **过账** | 起草JE（不过账） | 不出JE（只报告） |

## 量化投研启示

1. **差异分析的自动化**：P&L/BS的波动检测和解释生成——可用于量化组合的归因分析（performance attribution）
2. **滚动时间表模式**（期初+活动-冲销=期末）：适用于持仓变化的滚动追踪
3. **应计识别逻辑**：周期性费用的自动识别和计算——可用于量化模型中的季节性调整
4. **checklist驱动的流程管理**：月结的标准化步骤清单——量化策略的上线/调仓checklist自动化