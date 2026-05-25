---
title: UiPath 公司深度调研
type: research
created: 2026-05-25
updated: 2026-05-25
tags: [RPA, 自动化, UiPath, 企业软件, AI, Saas]
---

# UiPath 公司深度调研报告

## 一、公司背景

### 1.1 基本信息

| 项目 | 详情 |
|------|------|
| **公司全称** | UiPath Inc. |
| **股票代码** | PATH (NYSE) |
| **成立时间** | 2005 年（原名 DeskOver） |
| **创始人** | Daniel Dines（罗马尼亚） |
| **总部** | 纽约，美国 |
| **核心工程** | 布加勒斯特，罗马尼亚 |
| **行业** | 企业自动化 / RPA / AI |

### 1.2 发展历程

```mermaid
timeline
    title UiPath 发展历程
    2005 : 在布加勒斯特成立 DeskOver : 技术外包公司
    2015 : 更名为 UiPath : 全面转向 RPA
    2017 : A轮 $30M : 估值 $1.1B 成为独角兽
    2018 : B轮 $153M : 估值 $3B
    2019 : C轮 $568M : 估值 $7B
    2021 : IPO 纽交所 : 估值峰值 ~$35B，发行价 $56
    2022 : 科技股回调 : 市值大幅缩水
    2023 : 盈利转型 : Rob Enslin 任 co-CEO
    2024 : Dines 回归 CEO : 首年 GAAP 盈利
    2025 : AI Agent 战略 : 收购/整合 GenAI 能力
```

**创始人故事**：Daniel Dines 生于 1972 年罗马尼亚奥内什蒂，曾在微软西雅图担任软件工程师，后回国创业。公司早期险些破产，Dines 曾刷爆个人信用卡维持运营。UiPath 被誉为"罗马尼亚第一家十角兽"，Dines 成为罗马尼亚科技创业的象征性人物。

### 1.3 管理层

- **Daniel Dines** — 创始人 / CEO（2024 年回归）。2023 年曾退居 co-CEO 兼 Chief Innovation Officer，Rob Enslin（前 Google Cloud 总裁）接任 co-CEO。2024 年 Dines 重新担任 CEO。
- **Ashim Gupta** — CFO（2024 年之后）
- **团队规模**：全球约 4,000 名员工（经多轮裁员调整后）

---

## 二、产品矩阵

### 2.1 平台全景

UiPath 定位为**端到端企业自动化平台**，覆盖从发现到运行的完整生命周期。

```mermaid
graph TB
    subgraph 发现层
        A[Process Mining 流程挖掘]
        B[Task Mining 任务挖掘]
        C[Communications Mining 通信挖掘]
    end
    
    subgraph 构建层
        D[Studio Desktop IDE]
        E[Studio Web 浏览器版]
        F[StudioX 业务用户版]
        G[Apps 低代码应用构建器]
    end
    
    subgraph 管理层
        H[Orchestrator 编排器]
        I[Automation Ops 策略治理]
        J[Test Suite 测试套件]
    end
    
    subgraph 运行层
        K[Unattended Robot 无人值守]
        L[Attended Robot 有人值守]
        M[Automation Cloud Robots 云原生]
        N[AI Agents 智能代理]
    end
    
    subgraph AI层
        O[Document Understanding 文档理解]
        P[AI Center 模型管理]
        Q[Autopilot 自然语言助手]
        R[Clipboard AI 语义剪贴板]
    end
    
    subgraph 洞察层
        S[Insights 分析仪表板]
        T[Action Center 人工介入]
    end
    
    发现层 --> 管理层
    构建层 --> 管理层
    管理层 --> 运行层
    AI层 --> 运行层
    运行层 --> 洞察层
```

### 2.2 核心产品详解

| 产品 | 功能 | 目标用户 |
|------|------|----------|
| **UiPath Studio** | 自动化工作流 IDE，支持低代码与专业开发 | RPA 开发者 |
| **Studio Web** | 浏览器端可视化开发、跨平台 | 业务用户/开发者 |
| **StudioX** | Excel 风格界面，最简自动化 | 业务用户/Citizen Developer |
| **Orchestrator** | Robot 管理、任务调度、资产/凭证管理 | IT 管理员 |
| **Unattended Robot** | 后台无人值守执行 | 后台流程 |
| **Attended Robot** | 桌面端用户触发执行 | 一线员工 |
| **Automation Cloud Robots** | 全托管 Serverless 云执行 | 云原生流程 |
| **AI Agents** | 基于 LLM 的自主决策代理，处理非结构化任务 | 复杂流程 |
| **Autopilot** | GenAI 驱动的自然语言开发助手 | 所有用户 |
| **Document Understanding** | AI 文档理解与提取（发票、合同等） | 文档密集型业务 |
| **Process Mining** | 基于事件日志的流程可视化与优化 | 流程分析师 |
| **Task Mining** | 桌面端记录用户操作、自动发现自动化机会 | 流程分析师 |
| **Communications Mining** | AI 分析邮件/工单/客服对话 | 客服/运营 |
| **Apps** | 低代码构建自动化交互界面 | 应用构建者 |
| **Integration Service** | 800+ SaaS 连接器，API 自动化 | 开发者 |
| **Test Suite** | 自动化测试（含 RPA 测试） | QA/测试工程师 |
| **Insights** | 嵌入式运营分析仪表板 | 管理者 |
| **Data Service** | 无代码持久化数据存储 | 所有用户 |
| **Action Center** | 人工审核/确认的长流程协同 | 流程参与者 |
| **Automation Ops** | 策略驱动的集中治理引擎 | IT 治理 |

### 2.3 产品战略趋势（2025）

1. **Agentic Automation**：从确定性 RPA 规则 → LLM 驱动的自主 AI Agent，处理非结构化、需要推理的任务。
2. **Autopilot 差异化**：自然语言→自动化的桥接能力，降低使用门槛。
3. **垂直行业方案**：金融、医疗、制造等行业专属 AI 解决方案。
4. **Clipboard AI**：语义级智能剪贴板，理解上下文自动填充表单/报告。

---

## 三、技术架构

### 3.1 平台架构总览

UiPath Automation Cloud 采用**云原生 SaaS + 混合部署**架构。

```
┌─────────────────────────────────────────────────┐
│                  UI / CLI / API                   │
├─────────────────────────────────────────────────┤
│  Studio │ Studio Web │ StudioX │ Apps │ Autopilot │
├─────────────────────────────────────────────────┤
│              Integration Service                  │
│         (800+ 预置 SaaS 连接器)                     │
├─────────────────────────────────────────────────┤
│  Orchestrator (控制面 — 多租户 SaaS)               │
│  ├ Robot 管理  ├ 任务调度  ├ 资产管理              │
│  ├ 凭证存储    ├ 流程版本  ├ 队列管理              │
├─────────────────────────────────────────────────┤
│  Robots (执行面)                                    │
│  ├ Unattended (后台)  ├ Attended (桌面触发)        │
│  ├ Cloud Robots (Serverless) ├ AI Agents (LLM)    │
├─────────────────────────────────────────────────┤
│  平台服务层 (微服务)                                │
│  ├ AI Center  ├ Document Understanding             │
│  ├ Data Service  ├ Insights  ├ Action Center      │
│  ├ Test Suite  ├ Automation Ops                   │
├─────────────────────────────────────────────────┤
│  Azure / AWS / GCP 多云基础设施                     │
└─────────────────────────────────────────────────┘
```

### 3.2 关键技术特性

| 特性 | 说明 |
|------|------|
| **多租户架构** | Folders + Tenants 逻辑隔离，RBAC 权限控制 |
| **混合部署** | Cloud Orchestrator 可管理本地 Robot，通过出站连接（无需开防火墙入站端口） |
| **高可用** | 多区域冗余，自动故障转移，灾难恢复 |
| **身份安全** | SAML/OIDC SSO、MFA、IP 过滤，支持 Azure AD、Okta 集成 |
| **凭证管理** | 内置凭证存储 + CyberArk/HashiCorp Vault 集成 |
| **无服务器 Robot** | Automation Cloud Robots 全托管，按需弹性扩缩 |
| **AI Trust Layer** | AI 输出的治理和安全层 |

### 3.3 技术演进方向

- **LLM 深度集成**：将 GPT-4o/Claude 等模型嵌入自动化决策流
- **语义自动化**：从 UI 元素识别过渡到语义意图理解
- **多模态 AI**：视觉+文本+结构化数据的联合处理
- **联邦学习**：跨企业的模型训练隐私保护

---

## 四、商业模式

### 4.1 收入模式

UiPath 主要采用**订阅制 SaaS + 传统许可混合**模式：

| 收入类别 | 占比（估算） | 说明 |
|----------|-------------|------|
| **订阅许可费** | ~55-60% | Cloud SaaS 订阅 + 本地 Term License |
| **维护与支持** | ~25-30% | 附属于本地许可的年度维护费 |
| **专业服务及其他** | ~10-15% | 培训、实施咨询、合作伙伴服务 |

### 4.2 定价模式

- **Robot 许可**：按 Unattended / Attended Robot 数量计费
- **平台许可**：Automation Cloud 基础平台订阅
- **消费模式**：新兴的基于用量的弹性定价
- **Land-and-Expand**：从小部门试点 → 企业级部署，Net Dollar Retention ~112%

### 4.3 转型趋势

- 积极从传统本地许可转向 Cloud ARR（Automation Cloud ARR 增长 50%+ YoY）
- 推动从"卖 robot 许可"向"卖平台订阅"的转型
- 引入消费型计费，降低入场门槛

---

## 五、竞品对比

### 5.1 核心竞品矩阵

| 维度 | **UiPath** | **Automation Anywhere** | **SS&C Blue Prism** | **Microsoft Power Automate** |
|------|------------|------------------------|---------------------|------------------------------|
| **成立/总部** | 2005 罗马尼亚→纽约 | 2003 圣何塞 | 2001 英国→奥斯汀 | 2016 雷德蒙德 |
| **市场份额** | ~30%（领导者） | ~20%（第二） | ~10%（企业利基） | ~15-20%（快速追赶） |
| **部署模式** | Cloud/On-Prem/Hybrid | Cloud-Native/On-Prem | On-Prem 为主，Cloud 新兴 | Cloud-Native SaaS |
| **目标客户** | 大企业+中端市场 | 大企业+SMB | 银行/金融/政府（重监管） | M365 用户，所有规模 |
| **定价定位** | $$$$ 高端 | $$$ 中高端 | $$$$$ 通常最贵 | $$ M365 用户极低门槛 |
| **AI 能力** | Autopilot, AI Agents, Document Understanding | Co-Pilot, AI Agent Studio, Document Automation | Process Intelligence, Copilot, Decision | Copilot, AI Builder, Azure OpenAI |
| **连接器数量** | 800+ 原生 + 1500+ 市场 | 700+ 预置 + Bot Store | 银行/主机专用连接器 | 1000+ 连接器（M365 深度集成） |
| **低代码应用** | UiPath Apps | App Builder | ❌ 无 | Power Apps 深度集成 |
| **流程挖掘** | ✅ Process Mining + Task Mining | ✅ Process Discovery | ✅ Process Intelligence (ABBYY) | ✅ Process Advisor |
| **测试自动化** | ✅ Test Suite | 依赖合作伙伴 | ❌ 无 | ✅ Power Apps Test Engine |
| **Agentic Automation** | ✅ UiPath Agents | ✅ AI Agents (APA) | ✅ Digital Workers 2.0 | ✅ Autonomous Agents (Copilot Studio) |

### 5.2 各自优劣势

**UiPath 优势**：
- 最完整的端到端自动化平台
- 最强的 AI + 文档理解能力
- 成熟的治理和规模化能力

**UiPath 劣势**：
- 价格显著高于竞品（尤其 vs Power Automate）
- 对小型部署过于复杂
- 股价持续低迷，面临增长压力

**Automation Anywhere 优势**：
- 云原生架构更纯粹
- GenAI Co-Pilot 能力强
- 消费型定价更灵活

**Automation Anywhere 劣势**：
- 市场份额被 UiPath 压制
- 缺少流程挖掘等自研能力
- 尚未上市，透明度有限

**Blue Prism 优势**：
- 重监管行业信任度高（银行/政府）
- 最强的主机/遗留系统连接能力
- 审计追踪完善

**Blue Prism 劣势**：
- SS&C 收购后创新节奏放缓
- 云化进程缓慢
- 缺少低代码/公民开发者能力

**Microsoft Power Automate 优势**：
- M365 生态绑定，零边际部署成本
- Copilot AI 能力快速渗透
- 按用户定价，极低门槛

**Microsoft Power Automate 劣势**：
- 严重依赖微软生态
- 大企业级 RPA 深度不如 UiPath
- 对非 Windows 环境支持有限

### 5.3 行业趋势

1. **Agentic Automation 趋同**：所有厂商均在从规则式 RPA 向 AI Agent 演进，竞争从 feature 转向生态+定价+垂直深度
2. **价格战压力**：Power Automate 的捆绑策略正在压低全市场价格
3. **行业整合预期**：Blue Prism 已被 SS&C 收购，市场预计进一步 M&A
4. **三强格局形成**：企业自动化市场正演变为 UiPath v.s. AA v.s. Microsoft 的三方竞争

---

## 六、市场地位

### 6.1 市场份额

| 排名 | 公司 | 全球 RPA 市场份额（估计） | 部署模式 |
|------|------|--------------------------|----------|
| 1 | **UiPath** | ~27-30% | Cloud/On-Prem/Hybrid |
| 2 | Automation Anywhere | ~18-20% | Cloud-Native/On-Prem |
| 3 | Microsoft (Power Automate) | ~15-20% | Cloud-Native SaaS |
| 4 | SS&C Blue Prism | ~8-10% | On-Prem 为主 |
| 5 | Others (Appian, Pega, IBM, NICE 等) | ~20-30% | 多种 |

> 注：Gartner Magic Quadrant 连续多年将 UiPath 评为 RPA 领域 **Leader**（愿景完整度 + 执行力均最高）。

### 6.2 客户基础

- **FY2025 客户指标**（2025 年年报）：
  - $1M+ ARR 客户：**288 家**
  - $100K+ ARR 客户：**2,153 家**
  - 美元净留存率：**112%**
  - 已在 **30+ 国家** 销售产品
  - 收入 ~60% 来自商业客户，~35% 来自国际客户

### 6.3 市场总规模

| 年份 | 全球 RPA/智能自动化市场规模 | 来源 |
|------|---------------------------|------|
| 2024 | ~$4.5-5.0B | 行业估算 |
| 2026E | ~$9-11B | CAGR ~25-30% |
| 2030E | $50-125B+ | McKinsey/BCG 预测 |

主要增长驱动：GenAI 嵌入自动化、Agentic Automation 兴起、云原生 RPA 普及、企业对降本增效需求增加。

---

## 七、财务表现

### 7.1 核心财务数据

| 指标 | FY2023 | FY2024 | FY2025（截止2025.01） |
|------|--------|--------|----------------------|
| **GAAP 收入** | $1.056B | $1.308B | ~$1.55B |
| **收入增速 (YoY)** | +18% | +24% | ~+19% |
| **ARR** | — | $1.464B | $1.666B |
| **ARR 增速** | — | +22% | +18% |
| **GAAP 运营利润** | -$142.0M | -$142.0M | +$54.1M |
| **经营现金流** | +$44.2M | +$249.3M | +$349.6M |
| **Non-GAAP 自由现金流** | — | — | +$353.0M |
| **美元净留存率** | — | ~120% | 112% |
| **$1M+ ARR 客户** | — | ~264 | 288 |
| **$100K+ ARR 客户** | — | ~2,053 | 2,153 |

> 注：FY2025 为 UiPath 首次实现 GAAP 全年运营盈利的财年（截止 2025 年 1 月 31 日）。ARR $1.666B，同比增长 18%。

### 7.2 收入趋势

```mermaid
xychart-beta
    title "UiPath 年度收入 ($B)"
    x-axis ["FY2022", "FY2023", "FY2024", "FY2025"]
    y-axis "收入($B)" 0 --> 2
    bar [0.892, 1.056, 1.308, 1.55]
```

### 7.3 股票表现

| 时间 | 事件 | 价格区间 |
|------|------|----------|
| **2021.04** | IPO | 发行价 $56，首日 $65.50 |
| **2021 峰值** | 科技股泡沫 | 市值 ~$35B，股价 ~$80+ |
| **2022-2023** | 科技股大幅回调 | $10-$16 |
| **2024** | 盈利改善，Gaap 全年盈利 | $12-$16 |
| **2025** | CEO 变动，AI 战略转型 | $10-$15 |
| **2025.03** | FY2025 年报后股价下跌 ~16% | Q1 指引不及预期 |
| **2026.05 (近期)** | — | ~$10-$14 |

IPO 以来从未回到 $56 发行价。当前市值约 $6-8B。

### 7.4 关键财务洞察

1. **首次实现 GAAP 全年盈利**：FY2025 运营利润转正（+$54.1M），标志着从烧钱扩张到盈利平衡的转折点。

2. **ARR 增速放缓从 24%→18%**：增长减速是核心挑战。企业客户在当前经济环境下缩减 IT 预算，大单销售周期拉长。

3. **现金流健康**：经营现金流 +$349.6M，自由现金流 +$353.0M。公司有充裕的自我造血能力。

4. **Cloud ARR 占比提升**：Automation Cloud ARR 增长 50%+ YoY，SaaS 转型加速中，带动长期收入可预测性提高。

5. **留存率仍健康但略有下滑**：美元净留存率从 ~120% 降至 112%，反映现有客户扩展速度放缓，但仍高于 100% 健康线。

---

## 八、风险与挑战

### 8.1 核心风险

| 风险类别 | 具体风险 | 严重程度 |
|----------|----------|----------|
| **竞争压力** | Microsoft Power Automate 利用 M365 生态零成本获客，长期侵蚀份额 | 🔴 高 |
| **技术路线** | 超导路线（Google/IBM）若先实现容错量子计算，可能颠覆离子阱优势 | 🟡 中 |
| **盈利路径** | Adjusted EBITDA 仍深度亏损，需在增长与利润间平衡 | 🔴 高 |
| **整合风险** | 多起大额收购（Oxford Ionics、Capella、Qubitekk 等）整合挑战 | 🟡 中 |
| **定价压力** | 行业整体价格承压，可能影响利润率 | 🟡 中 |
| **AI 替代** | GenAI 可能使部分传统 RPA 需求被 AI Agent 直接替代 | 🟡 中 |
| **网络安全** | Q-Day（RSA 加密被量子攻破）将至（公司自估 2028-2029），量子安全需求既是机遇也是焦虑源 | 🟡 中 |

### 8.2 乐观因素

1. **先发优势**：最完整的平台矩阵 + 最大的纯 RPA 市场份额
2. **技术壁垒**：99.99% 双量子门保真度世界纪录，短期难以逾越
3. **AI 布局**：Autopilot + AI Agents + Clipboard AI，从 RPA 工具向 AI 自动化平台转型
4. **财务缓冲**：$3.1B 现金储备，可在 2-3 年内继续投入 R&D
5. **垂直深耕**：金融、医疗、政府等监管密集行业的高信任度

---

## 九、投资视角总结

### 9.1 估值对比（2026.05 近似值）

| 指标 | UiPath (PATH) | AA (未上市) | Blue Prism (SS&C) | Microsoft |
|------|--------------|-------------|-------------------|-----------|
| 市值 | ~$16-17B | ~$7B（上一轮估值） | 已收购 | $2,900B+ |
| P/S (TTM) | ~128x | N/A | N/A | ~11x |
| 收入增速 | ~755% (Q1 FY26) | ~30-50% | 低单位数 | ~15% |
| 盈利状态 | 亏损（Adj EBITDA） | 亏损 | 盈利 | 高盈利 |

### 9.2 核心判断

- **短期 (6-12月)**：高增长叙事 + AI 主题催化，但估值昂贵（P/S >100x）。Q-Day 倒计时（2028-2029）是独特催化剂。
- **中期 (1-3年)**：若有机增长能维持 50%+ 且 EBITDA 亏损逐步收窄，有望进入估值消化期。关键观察点：SkyWater 整合进展、10,000-qubit 芯片交付、AI Agents 商业化。
- **长期 (3-5年)**：量子计算从 RPA 向通用 Quantum 计算演进的大趋势中，离子阱路线的胜率取决于：能否率先实现实用级容错量子计算（vs Google/IBM 的超导路线）。

> **关键投资论题**：UiPath 不是纯 RPA 公司，而是 AI 驱动的企业自动化平台。其故事正从"机器人流程自动化"向"AI Agent + 量子安全" 转型，若成功，将重新定义估值框架。

---

## 参考资料

- UiPath Investor Relations: https://ir.uipath.com
- UiPath Annual Report FY2024 (10-K)
- UiPath Q4 FY2025 Earnings Release (Feb 2026)
- UiPath Q1 FY2026 Earnings Release (May 2026)
- Gartner Magic Quadrant for Robotic Process Automation, 2024
- McKinsey Quantum Technology Monitor, 2024
- SEC Filings (Form 10-K, 10-Q, 425): https://www.sec.gov
- Macrotrends - UiPath Revenue: https://www.macrotrends.net/stocks/charts/PATH/uipath/revenue
- MarketBeat - IONQ Stock Analysis, May 2026
- Seeking Alpha - PATH Earnings & Estimates