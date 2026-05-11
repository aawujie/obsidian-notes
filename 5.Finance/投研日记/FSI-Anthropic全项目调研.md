---
title: FSI-Anthropic全项目调研汇总
type: research
created: 2026-05-11
updated: 2026-05-11
sources: [https://github.com/anthropics/financial-services, 01~14 子笔记]
tags: [FSI, Anthropic, 量化投研, 汇总, AI-Agent, 调研]
---

# FSI-Anthropic 全项目调研汇总：对我们量化投研可借鉴的点

## 项目全貌

Anthropic Financial Services 是一个**文件驱动的 AI Agent 金融工作流参考实现**，覆盖投行、权益研究、PE、财富管理、基金行政五大垂直领域。包含 10 个命名 Agent、7 个垂直插件、11 个 MCP 数据连接器、10 套 Managed Agent 部署模板。纯 Markdown + YAML + JSON，无构建步骤。

---

## 一、架构设计层面

### 1. "单一源 + 两类交付" 范式

**核心理念**：同一套 system prompt + skills 文件，通过不同 wrapper 在两种环境中运行。

```
source (agents/<slug>.md + skills/)
    ├── Cowork Plugin wrapper → 交互式桌面使用
    └── CMA YAML wrapper       → 无头 API 部署
```

**量化借鉴**：量化策略的核心逻辑（因子定义、信号生成规则、风控参数）作为"单一源"，打包为 Jupyter Notebook（交互式研究）+ Airflow DAG（生产执行）。

### 2. 技能/命令/连接器三层分离

| 层 | 量化对应 |
|---|---|
| Skills（自动触发）| 因子计算函数库（上下文自动加载） |
| Commands（显式调用）| CLI 命令（`/backtest`, `/optimize`） |
| Connectors（数据源）| 数据 vendor API + 内部数据库 |

**量化借鉴**：将因子定义、回测引擎、数据适配器分离为独立模块，通过声明式配置组合。

### 3. 垂直插件组织方式

```
shared core (financial-analysis)
    ├── 基础建模技能 (DCF/Comps/LBO/3-statement)
    ├── 生产力技能 (audit/clean/deck QC)
    └── 11个 MCP 数据连接器

vertical specializations
    ├── equity-research  (earnings/initiation/thesis)
    ├── private-equity   (sourcing/screening/DD/IC memo)
    ├── investment-banking (CIM/teaser/merger model)
    └── wealth-management (planning/rebalance/TLH)
```

**量化借鉴**：构建 `quant-core`（数据层 + 回测引擎 + 因子库）→ 各策略插件（动量/价值/套利/事件驱动）引用 core。

---

## 二、Agent 设计层面

### 4. "深度1"的多Agent委托架构

每个 Agent 的 orchestration 模式：

```
Orchestrator (无Write)
├── Reader    → Read/Grep only (无MCP, 无Write)
├── Worker    → 核心计算
└── Writer    → Write (唯一，不接触外部数据)
```

**量化借鉴**：
- 数据采集 Agent（只读，无交易权限）
- 信号计算 Agent（核心逻辑）
- 订单生成 Agent（唯一有交易API权限）← **关键安全边界**

### 5. "Section-by-Section 验证" 的增量构建

DCF/LBO建模的核心理念：**每完成一节即验证，获用户确认后才继续**。

```
数据检索 → show & confirm
收入预测 → show & confirm
FCF构建 → show & confirm
WACC计算 → show & confirm
终值+估值 → show & confirm
敏感性表格 → show & confirm
```

**量化借鉴**：策略开发流水线设置检查点——
1. 数据清洗完成 → 验证数据质量
2. 因子计算完成 → 验证因子分布
3. 回测完成 → 验证收益/风险指标
4. 参数优化完成 → 验证过拟合检测
5. 纸交易 → 验证实盘一致性

### 6. Agent 边界清晰化

| Agent | 不做的事 | 替代Agent |
|-------|---------|----------|
| Model Builder | 更新现有模型 | Earnings Reviewer |
| GL Reconciler | 过账JE | Month-End Closer |
| Pitch Agent | 编辑已有Deck | pitch-deck skill直接调用 |

**量化借鉴**："新建策略" vs "参数刷新"分离为不同Agent——避免一个Agent承担过多职责。

---

## 三、安全设计层面

### 7. "不可信输入"处理模式

**统一模式**：任何外部来源的文档/数据必须先经权限受限的 Reader 处理。

| 外部源 | Reader 权限 | 输出格式 | 下游消费 |
|--------|:---:|------|------|
| 电话会转录 | Read/Grep | 结构化JSON | model-updater |
| GP估值包 | Read/Grep | 结构化JSON | valuation-runner |
| 客户邮件 | Read/Grep | 结构化JSON | pack-writer |
| 外部对账单 | Read/Grep | 结构化JSON | reconciler |
| KYC准入文件 | Read/Grep | **长度上限**结构化JSON | rules-engine |

**量化借鉴**：
- 外部数据源（vendor API、web scrape）→ 数据清洗层（仅解析+验证，不执行业务逻辑）
- 清洗后的结构化数据 → 因子计算层
- **长度上限** 的中间格式防止注入攻击

### 8. 三层独立验证（GL Reconciler 模式）

```
Reader → 发现差异
Critic → 独立重新验证（不同的Agent、不同的视角）
Resolver → 格式化输出
```

**量化借鉴**：
- 信号生成 Agent → 产生交易信号
- 独立风控 Agent → 仅读取信号，验证合规性、持仓限制、集中度
- 订单执行 Agent → 格式化并发送订单

### 9. Handoff 安全路由

```
Agent A 输出 → handoff_request JSON
    → 硬白名单验证（ALLOWED_TARGETS）
    → Schema验证（jsonschema.validate）
    → 路由到 Agent B
```

**量化借鉴**：策略间信号传递通过白名单+Schema验证的消息队列——防止未授权策略触发交易。

---

## 四、工程实践层面

### 10. "Formula over Hardcode"（公式优于硬编码）

DCF 模型强制规则：每个派生值必须是 Excel 公式，不能是 Python 计算后写入的数值。

```python
# 正确
ws["D20"] = "=D19*(1+$B$8)"

# 错误
ws["D20"] = 12500  # Python计算的结果
```

**量化借鉴**：
- 因子值 = 源数据的函数（可追溯），不是静态快照
- 信号 = 因子组合的函数（可回放），不是黑箱输出
- 参数从配置加载（可复现），不硬编码

### 11. Cell Comment 作为数据溯源

DCF 模型中每个硬编码输入必须有 cell comment：
```
"Source: 10-K FY2024, Page 32, Consolidated Statements"
```

**量化借鉴**：每个因子的数据源标注——`data_lineage: { vendor: "FactSet", field: "price_close", date: "2025-05-11" }`——支撑完整的审计追踪。

### 12. 敏感性表格的对称设计

```
ODD维度 (5×5或7×7) → 保证真正的中心cell
中心cell = base case → 验证表格接线正确
axis = [base-2Δ, base-Δ, base, base+Δ, base+2Δ] → 对称
```

**量化借鉴**：参数敏感性分析——围绕base case参数对称构建网格，中心点验证回测结果一致性。

### 13. 代码同步机制

```
编辑源：vertical-plugins/<vertical>/skills/
    ↓ sync-agent-skills.py
同步副本：agent-plugins/<slug>/skills/
    ↓ check.py (pre-commit)
验证：无 drift，所有引用解析正确
```

**量化借鉴**：因子定义统一维护在 `factors/` 目录，通过脚本同步到各策略目录，pre-commit hook 验证一致性。

---

## 五、量化投研可直接迁移的模块

### A. 可复用的核心模式

| FSI 模式 | 量化对应 | 优先级 |
|----------|---------|:---:|
| 三场景切换（INDEX consolidation column）| 多市场状态（牛市/震荡/熊市）因子权重切换 | 高 |
| 统计行自动化（Max/75th/Median/25th/Min）| 因子分位数分析、行业中性化 | 高 |
| variance commentary（差异分析）| 策略归因分析（performance attribution） | 高 |
| roll-forward 模式 | 持仓变化追踪（期初→交易→期末） | 中 |
| Football Field 多方法论汇总 | 多因子打分汇总可视化 | 中 |
| earning-analysis 语气分析 | NLP 情感因子 | 中 |
| Moat评估框架 | 公司质量因子（护城河评分） | 中 |
| competitor mapping 多维度可视化 | 行业聚类分析（2×2矩阵/radar/tier） | 低 |
| TLH 合规自动化 | 做空限制/持仓限额合规检查 | 中 |
| Monte Carlo 财务规划 | VaR/CVaR/压力测试 | 高 |

### B. 可复用的工程基础设施

| FSI 设施 | 量化对应 |
|----------|---------|
| `.mcp.json` 统一数据源声明 | `datasources.yaml` 统一数据vendor配置 |
| `agent.yaml` 标准化部署配置 | `strategy.yaml` 策略声明式配置 |
| `deploy-managed-agent.sh` 一键部署 | `deploy-strategy.sh` 一键部署到执行引擎 |
| `orchestrate.py` 事件路由 | 策略间信号传递的 event bus |
| `steering-examples.json` | 策略触发事件模板 |
| `check.py` pre-commit lint | CI/CD pipeline 的策略配置验证 |

### C. 可直接复制使用的 Skill 设计

以下 FSI 技能的设计可经适配后用于量化：

1. **dcf-model** → 现金流预测流水线 → 预期现金流因子
2. **comps-analysis** → 横截面比较框架 → 行业中性化+分位数
3. **competitive-analysis** → 行业分析checklist → 行业轮动策略的定性输入
4. **audit-xls** → 模型完整性检查 → 回测结果验证（无未来函数、无存活偏差）
5. **variance-commentary** → 波动分析自动化 → 策略异常检测（drawdown根因分析）

---

## 六、综合评估

### 项目成熟度
- **完整性**：★★★★★ — 10个端到端Agent覆盖FSI主要工作流
- **工程化程度**：★★★★☆ — 脚本化部署、同步、验证，但缺CI/CD和监控
- **安全设计**：★★★★★ — 多层隔离、不可信输入处理、权限最小化
- **可移植性**：★★★★★ — 纯文件驱动，零依赖建筑，易于fork和改编
- **量化适配**：★★★☆☆ — 面向传统金融工作流，需转化为量化场景

### 核心差距（需要我们自己补充）
1. **实时数据管道**：FSI Agent 是事件驱动（steering event），不处理实时流数据
2. **高频/日内能力**：所有工作流假设日频或更低频率
3. **市场微观结构**：无订单簿、流动性、交易成本建模
4. **回测框架**：无历史回测和样本外验证机制
5. **另类数据**：MCP 连接器面向传统金融数据，缺 satellite imagery/信用卡交易/social sentiment 等

### 最适合借鉴的方向
1. **多Agent安全架构**：Reader→Worker→Writer 的权限分离模型
2. **声明式配置体系**：agent.yaml + plugin.json + .mcp.json 的组合
3. **文件驱动的工作流引擎**：无需重型基础设施即可运行的Agent系统
4. **不可信输入的统一处理模式**：适用于量化系统中处理外部数据和报告的模块

---

## 子笔记索引

| # | 文件 | 内容 |
|---|------|------|
| 1 | [01-项目架构](01-项目架构.md) | 目录结构、设计哲学、10 Agent总览、11 MCP连接器 |
| 2 | [02-financial-analysis](02-financial-analysis.md) | DCF/Comps/LBO/3-statement/Audit/竞争分析技能详解 |
| 3 | [03-Pitch-Agent](03-Pitch-Agent.md) | 投行Pitch端到端：9步工作流+安全设计 |
| 4 | [04-Market-Researcher](04-Market-Researcher.md) | 行业/赛道研究：5产出物+6步流程 |
| 5 | [05-Earnings-Reviewer](05-Earnings-Reviewer.md) | 财报分析+模型更新：3产出物+批量扇出 |
| 6 | [06-Model-Builder](06-Model-Builder.md) | 四类模型(从零构建) vs Earnings Reviewer(更新现有) |
| 7 | [07-Meeting-Prep-Agent](07-Meeting-Prep-Agent.md) | 客户会前简报：CRM+市场数据融合 |
| 8 | [08-Valuation-Reviewer](08-Valuation-Reviewer.md) | GP估值审查：不可信输入→独立验证→LP报告 |
| 9 | [09-GL-Reconciler](09-GL-Reconciler.md) | 总账对账：三层独立验证架构(最严格安全设计) |
| 10 | [10-Month-End-Closer](10-Month-End-Closer.md) | 月结流程：应计+滚动+差异分析 |
| 11 | [11-Statement-Auditor](11-Statement-Auditor.md) | LP对账单审计：field-level比对+pass/hold决策 |
| 12 | [12-KYC-Screener](12-KYC-Screener.md) | KYC尽调：长度上限JSON中间格式防注入 |
| 13 | [13-垂直领域技能集](13-垂直领域技能集.md) | IB/ER/PE/WM/FA/Ops 全部commands+skills详解 |
| 14 | [14-Managed-Agent-部署](14-Managed-Agent-部署.md) | CMA部署+orchestrate.py handoff+check.py验证 |