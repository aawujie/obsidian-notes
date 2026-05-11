---
title: Statement Auditor — LP对账单审计
type: research
created: 2026-05-11
updated: 2026-05-11
sources: [https://github.com/anthropics/financial-services/tree/main/plugins/agent-plugins/statement-auditor]
tags: [FSI, Statement-Auditor, LP对账单, PE, 审计]
---

# Statement Auditor — LP对账单审计

## Agent 定位

> "You are the Statement Auditor — the last set of eyes on LP statements before they leave the firm."

LP对账单在公司对外发出前的最后一关审查。审计一批预生成的LP资本账户对账单，与基金NAV包核对，标记差异。

## 3大产出物

1. **核对表**：每个LP对账单字段 vs NAV包源数据的 匹配/不匹配 对照
2. **异常清单**：每个差异及其疑似原因
3. **签字表**：每份对账单的 通过/暂缓 建议

## 3步工作流

```
1. Read the statements → statement-reader提取每个LP的报告余额（对账单不可信）
2. Reconcile → 通过NAV MCP将每个字段与NAV包对比
3. Flag → flagger格式化异常清单和签字表
```

## 使用的技能

`nav-tieout` · `audit-xls` · `xlsx-author`

| 技能 | 功能 |
|------|------|
| **nav-tieout** | NAV核对——LP对账单字段与基金NAV包的逐一比对 |
| **audit-xls** | 审计工作簿检查 |
| **xlsx-author** | 生成签字表Excel |

## Guardrails

1. **对账单不可信**：statement-reader仅有Read/Grep且无MCP访问（它们可能由不可控的上游系统生成）
2. **不分发**：Agent建议pass/hold；IR在人类签字后分发

## Managed Agent 配置

```yaml
name: statement-auditor
tools: read, grep, glob + NAV MCP
子Agent:
  - statement-reader → Read/Grep only (无MCP, 无Write)
  - reconciler       → NAV MCP 对账
  - flagger          → Write ← 唯一 Write (异常清单+签字表)
```

**Steering 示例**：
```
"Tie out statement batch <id> against <fund> NAV pack"
```

## 子Agent架构

```
Statement Auditor (Orchestrator)
├── statement-reader → Read/Grep only (无MCP)
├── reconciler       → NAV MCP (核对)
└── flagger          → Write ← 唯一 Write
```

## 与其他审计Agent的对比

| Agent | 审计对象 | 数据源 | 信任模型 |
|-------|---------|--------|---------|
| **Statement Auditor** | LP对账单 | NAV pack (可信) vs 对账单 (不可信) | 对账单不可信 |
| **Valuation Reviewer** | GP估值包 | 估值模板 (可信) vs GP包 (不可信) | GP包不可信 |
| **GL Reconciler** | GL vs 子账 | 内部GL (可信) vs 外部对账单 (不可信) | 外部对账单不可信 |
| **audit-xls技能** | Excel模型 | 公式逻辑 | 公式可能出错 |

## 量化投研启示

1. **"最后一关审查"**的角色定位：量化交易中可设置"信号发布前的最后自动审查"关卡
2. **对账单不可信的假设**：对上游系统生成的数据保持怀疑——量化数据管道中对数据vendor提供的"预计算"结果应验证
3. **pass/hold的二分类决策输出**：适用于量化信号的"执行/暂停"二元建议
4. **field-level一一比对**的审计粒度：量化数据质量检查中的字段级验证而非表级