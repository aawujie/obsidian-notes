---
title: GL Reconciler — 总账对账
type: research
created: 2026-05-11
updated: 2026-05-11
sources: [https://github.com/anthropics/financial-services/tree/main/plugins/agent-plugins/gl-reconciler]
tags: [FSI, GL-Reconciler, 总账对账, 基金行政, 对账]
---

# GL Reconciler — 总账对账 Agent

## Agent 定位

> "You are the GL Reconciler — a fund-accounting controller who owns the daily GL ↔ subledger reconciliation."

基金会计主管角色——负责每日总账(GL)与子账(subledger)的对账。**不涉及日记账分录过账（由Month-End Closer负责）**。

## 3大产出物

1. **Break清单**：每个超过阈值的GL/子账差异——含账户、余额、差异金额、疑似原因
2. **根因追踪**：每个break的交易层面证据 + 分类（时序差异/系统漂移/重分类/未知）
3. **异常报告**：格式化的主管签字报告，含每个break的建议处理方案

## 5步工作流

```
1. Pull balances → GL和子账MCP获取交易日+资产类别的余额
2. Compare and isolate breaks → 每个资产类别派发一个reader识别超过阈值的差异
3. Trace root cause → 对每个break提取底层交易并分类原因
4. Independent re-verify → critic独立重新核实每个报告的break
5. Draft exception report → resolver格式化异常报告供签字
```

## 使用的技能

`gl-recon` · `break-trace` · `audit-xls` · `xlsx-author`

| 技能 | 功能 |
|------|------|
| **gl-recon** | GL与子账的对账方法论——余额比较、阈值过滤、差异分类 |
| **break-trace** | 交易层面的break根因追踪——追溯到源交易并分类 |
| **audit-xls** | 对账工作簿审计 |
| **xlsx-author** | 生成异常报告Excel |

## Guardrails — 最严格的安全设计

1. **托管方和对家对账单不可信**：处理它们的reader子Agent无MCP访问、无Write工具
2. **编排者绝不写**：只有resolver子Agent持有Write——且它从不接触原始外部内容
3. **不过账到总账**：Agent产出的是报告；总账调整需Agent外人类审批

## Managed Agent 配置

```yaml
name: gl-reconciler
tools: read, grep, glob + GL MCP + Subledger MCP
子Agent:
  - reader   → Read/Grep only (无MCP, 无Write) —— 读外部对账单
  - critic   → Read only (独立验证reader发现)
  - resolver → Write ← 唯一 Write (格式化报告)
```

**Steering 示例**：
```
"Reconcile GL vs subledger, trade date <D>, classes: <list>"
```

## 子Agent架构

```
GL Reconciler (Orchestrator) ← 无Write
├── reader   → Read/Grep only (无MCP, 读外部文档)
├── critic   → Read only (独立验证, 无MCP, 无Write)
└── resolver → Write ← 唯一 Write (仅格式化，不接触原始外部内容)
```

**安全设计核心**：三层隔离——

| 层级 | 角色 | 接触外部数据 | MCP访问 | Write |
|------|------|:---:|:---:|:---:|
| Reader | 读外部文档 | ✓ | ✗ | ✗ |
| Critic | 独立复核 | ✗ | ✗ | ✗ |
| Resolver | 格式化输出 | ✗ | ✗ | ✓ |

外部对账单可能包含恶意内容——reader在无MCP无Write环境下处理，输出经schema验证后再传递。Resolver只做格式化，从不接触原始外部内容。

## 量化投研启示

1. **三层独立验证架构**（reader → critic → resolver）是金融数据管道的最佳安全实践——可用于量化数据ETL
2. **"编排者绝不写"** 原则：核心调度逻辑不应有数据修改权限——适用于量化交易系统的风险控制
3. **Break分类体系**（时序/漂移/重分类/未知）可用于量化数据的异常检测和根因分类
4. **按资产类别parallel dispatch reader** 的并发模式：量化数据处理中可按板块/因子/数据源并行派发worker
5. **阈值过滤 + 交易级追踪** 的两级精度对账：先粗筛再精查，适用于大数据量对账场景