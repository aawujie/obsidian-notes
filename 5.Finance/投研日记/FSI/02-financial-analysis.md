---
title: financial-analysis 核心插件
type: research
created: 2026-05-11
updated: 2026-05-11
sources: [https://github.com/anthropics/financial-services/tree/main/plugins/vertical-plugins/financial-analysis]
tags: [FSI, financial-analysis, DCF, Comps, Excel, MCP]
---

# financial-analysis — 共享技能 + MCP 连接器

## 概述

`financial-analysis` 是整个 FSI 项目**必须先安装的核心插件**。它提供：
- 6 类金融建模技能（DCF / Comps / LBO / 3-statement / 竞争分析 / 模型审计）
- 3 类生产力技能（Excel审计 / 数据清洗 / Deck刷新）
- 2 类输出技能（PPTX生成 / XLSX生成）
- 1 个模板制作技能
- 1 个技能创建器（meta-skill）
- **11 个 MCP 数据连接器配置**

其他所有 Agent 插件和垂直插件都依赖此插件提供的共享技能和连接器。

## 技能体系

### 一、核心建模技能

#### 1. DCF Model (`dcf-model` / `/dcf`)

**机构级质量**的现金流折现模型。覆盖完整流程：

- **数据检索**：优先MCP → 用户提供 → Web搜索(SEC EDGAR)
- **历史分析**：3-5年 revenue CAGR、利润率趋势、资本密集度、ROIC
- **收入预测**：三年递进——Year 1-2高增长 → Year 3-4适度 → Year 5+趋近终端增长
- **运营费用**：按收入百分比建模（S&M/R&D/G&A），体现运营杠杆
- **FCF计算**：NOPAT + D&A - CapEx - ΔNWC
- **WACC**：CAPM方法，含债务成本、资本结构权重
- **终值**：永续增长法（首选）+ 退出倍数法（备选）
- **敏感性分析**：3张5×5表格（WACC vs g / 增长 vs 利润率 / Beta vs Rf）

**关键技术规范**：
- 三场景（Bear/Base/Bull）通过 INDEX 公式的 consolidation column 切换
- 所有敏感性格子用 Python/openpyxl 循环填充 **完整DCF重算公式**（75个cell）
- 颜色编码：蓝=输入、黑=公式、绿=跨表引用
- 蓝色系专业配色：深蓝 section header / 浅蓝 column header / 中蓝 key output
- 每个硬编码输入必须有 cell comment（"Source: [系统], [日期], [引用]"）
- 交付前运行 `recalc.py`

**关键约束**：
- Formula over Hardcode：`ws["D20"] = "=D19*(1+$B$8)"` ✓ / `ws["D20"] = calculated_revenue` ✗
- OpEx必须基于Revenue而非Gross Profit
- 终值<WACC（否则无限大）
- 终值占EV 50-70% 为合理

#### 2. Comps Analysis (`comps-analysis` / `/comps`)

**机构级可比公司分析**。分两个section：

**Operating Metrics**：
- Revenue, Revenue Growth %, Gross Profit, Gross Margin %, EBITDA, EBITDA Margin %
- 行业特定指标（SaaS: Rule of 40, ARR; 制造业: Asset Turnover; 金融: ROE/ROA）
- 统计行：Max, 75th, Median, 25th, Min（用 QUARTILE 公式）

**Valuation Multiples**：
- Market Cap, Enterprise Value, EV/Revenue, EV/EBITDA, P/E
- 统计行同上
- **交叉引用规则**：估值公式必须引用 Operating Metrics section 的单元格

**核心原则**：
- "5-10规则"：5个运营指标 + 5个估值指标 = 10列
- 所有比率 = 公式/Revenue 或 公式/本表其他单元格
- 每个hardcoded input有cell comment + 超链接

#### 3. LBO Model (`lbo-model` / `/lbo`)

**PE标准杠杆收购模型**。包含：
- Sources & Uses（资金来源与用途）
- Operating Model（运营模型）
- Debt Schedule（债务时间表，含优先瀑布）
- Returns Analysis（IRR/MOIC）
- Sensitivity Tables（5×5，Entry Multiple vs Exit Multiple, IRR/MOIC）

**关键技术决策**：
- 使用 **Beginning Balance** 计算利息（打破循环引用）
- 债务偿还优先级瀑布
- 余额不能为负（用MAX/MIN保护）
- 颜色：蓝=输入、黑=公式、紫=同表链接、绿=跨表链接

#### 4. 3-Statement Model (`3-statement-model` / `/3-statement-model`)

**三表联立财务模型**（利润表/资产负债表/现金流量表）。核心检查：
- BS Balance: Assets = Liabilities + Equity（每期）
- Cash Tie-Out: CF Ending Cash = BS Cash
- RE Rollforward: Prior RE + NI - Dividends = Ending RE
- 跨表一致性：所有值链接不复制

含场景分析（Base/Upside/Downside）和信用指标（杠杆率/覆盖率/流动性）。

#### 5. Audit XLS (`audit-xls` / `/debug-model`)

**三级审计**：
- **selection** → 公式错误检查
- **sheet** → +不一致公式/硬编码检测
- **model** → +财务模型完整性检查（BS平衡/现金对账/逻辑合理性）

针对不同模型类型的专项检查：DCF（折现期/FCF口径）、LBO（债务偿还/管理滚存）、Merger（增厚稀释/协同阶段）、3-statement（WC符号/折旧匹配）。

#### 6. Competitive Analysis (`competitive-analysis` / `/competitive-analysis`)

**两阶段流程**：先确认范围→获批outline→再构建。覆盖：
- 行业定义指标（SaaS: ARR/NRR/Rule of 40; 支付: GPV/take rate）
- 市场context（规模/增长/驱动因素）
- 行业经济学（价值链/平台生态/碎片整合）
- 目标公司profile + 竞争对手映射 + 定位可视化
- 深度对比分析（定量metrics + 定性评估）
- Moat评估（网络效应/转换成本/规模经济/无形资产）

### 二、生产力技能

| 技能 | 命令 | 功能 |
|------|------|------|
| `clean-data-xls` | — | 标准化清洗Excel表格数据 |
| `deck-refresh` | — | 重新链接和刷新deck中的图表/表格 |
| `ib-check-deck` | — | QC演示文稿（数字一致性、脚注、日期） |

### 三、输出技能

| 技能 | 功能 | 适用环境 |
|------|------|---------|
| `pptx-author` | 无头生成.pptx文件 | Managed Agent |
| `xlsx-author` | 无头生成.xlsx文件 | Managed Agent |

### 四、元技能

| 技能 | 命令 | 功能 |
|------|------|------|
| `ppt-template-creator` | `/ppt-template` | 创建可复用的PPT模板技能 |
| `skill-creator` | — | 创建新技能的指南 |

## MCP 连接器配置

所有连接器通过 `.mcp.json` 声明，类型为 `http`：

```json
{
  "mcpServers": {
    "daloopa":      "https://mcp.daloopa.com/server/mcp",
    "morningstar":  "https://mcp.morningstar.com/mcp",
    "sp-global":    "https://kfinance.kensho.com/integrations/mcp",
    "factset":      "https://mcp.factset.com/mcp",
    "moodys":       "https://api.moodys.com/genai-ready-data/m1/mcp",
    "mtnewswire":   "https://vast-mcp.blueskyapi.com/mtnewswires",
    "aiera":        "https://mcp-pub.aiera.com",
    "lseg":         "https://api.analytics.lseg.com/lfa/mcp",
    "pitchbook":    "https://premium.mcp.pitchbook.com/mcp",
    "chronograph":  "https://ai.chronograph.pe/mcp",
    "egnyte":       "https://mcp-server.egnyte.com/mcp"
  }
}
```

**注意**：MCP访问可能需要提供商订阅或API Key。

## 命令清单

| 命令 | 技能 | 功能 |
|------|------|------|
| `/comps` | comps-analysis | 可比公司分析+交易倍数 |
| `/dcf` | dcf-model | DCF估值+WACC+敏感性 |
| `/lbo` | lbo-model | 杠杆收购模型 |
| `/3-statement-model` | 3-statement-model | 三表财务模型 |
| `/debug-model` | audit-xls | Excel模型审计 |
| `/competitive-analysis` | competitive-analysis | 竞争格局与市场定位 |
| `/ppt-template` | ppt-template-creator | 创建PPT模板技能 |

## 量化投研启示

1. **Formula over Hardcode 原则可直接应用于量化模型构建**——所有派生值用公式链接，确保假设变更时模型自动更新
2. **数据源优先级体系**（MCP → 用户 → Web）是可复用的数据治理模式
3. **三场景切换的 consolidation column 模式**（INDEX公式）比嵌套IF更清晰，适用于因子多场景回测
4. **统计行（Max/75th/Median/25th/Min）自动化**模式适用于因子分位数分析
5. **Cell comment 作为数据溯源**的实践值得在量化模型文档化中采用