---
title: "Anthropic Claude for Financial Analysis 发布会笔记"
type: 投研笔记
created: 2026-05-27
updated: 2026-05-27
sources:
  - "https://x.com/RohOnChain/status/2058980993693061200"
tags:
  - AI
  - 金融科技
  - Claude
  - Anthropic
  - 量化投资
---

## 基本信息

- **事件**：The Future of Finance, powered by Claude — Anthropic 金融产品发布会
- **时长**：~62 分钟
- **核心发布**：Claude for Financial Analysis（Anthropic 首个金融行业专属方案）

---

## 一、开场（Kate Jensen, Head of Revenue）

> "世界正在分叉——只有两种投资公司：系统性使用 AI 的，和正在把顶尖人才输给前者的。"

**核心论点**：
- 现代市场的复杂度、信息速度、数据量已超人类智力上限
- 管着几十亿资产，"够好"是不够的
- 自 2021 年起 Anthropic 构建 helpful/harmless/honest 的 AI 系统

**已有客户案例**：

| 客户 | 用途 | 效果 |
|:---|:---|:---|
| Bridgewater | 投资分析师助手，求解复杂模型 | 2023 年起使用 |
| Commonwealth Bank (澳洲) | 大规模 AI 投资 | CTO 视为全球 AI 战略基础 |
| AIG (纽约) | 重塑承保流程 | 时间压缩 5×（周→天），准确率 75%→90% |

---

## 二、生态与合作伙伴

### 基础设施
- **AWS & GCP**：企业级安全可扩展部署
- Claude for Enterprise（含金融方案）**已上线 AWS Marketplace**，即将上线 GCP Marketplace

### 外部市场数据（首发集成）

| 数据商 | 提供内容 |
|:---|:---|
| **FactSet** | 基本面数据 + 一致预期 |
| **S&P Global（CapIQ）** | 财务数据、市场数据、电话会议记录 |
| **Delpha** | AI 验证的基本面 + 源引用 |
| **Morningstar** | 公开市场投资研究 |
| **PitchBook** | 私募市场情报 |

### 企业数据平台
- Box、Databricks、Palantir、Snowflake → 内部数据接入 Claude

### 咨询服务商
- **Deloitte / KPMG**：组织现代化 + AI agent 规模化部署
- **PwC / Turing**：监管合规挑战
- **Slalom / Tribe AI**：实时决策支持

---

## 三、合作伙伴对话：S&P Kensho + Deloitte

### Peter Lucurzi（Kensho CTO, S&P Global 的 AI 创新中心）

**核心洞察**：
- GenAI 的最大惊喜是**采用速度**——客户不再问"AI 能做什么"，而是问"怎么让我成为 AI 优先的组织"
- 客户需要**可信数据**，这就是 S&P 推出 LLM-Ready API 的原因
- Kensho 构建了 "grounding agent"，确保 LLM 对数据的引用可验证、有来源

### Vikram Bhat（Deloitte 金融行业副主席）

**核心洞察**：
- 价值定位从**纯生产率**扩展到：新产品开发、分销重构、风控优化、员工/客户体验
- 金融服务业的最大挑战：**创新与风管的平衡**——不能让 20 个检查者卡 1 个做事的
- 变革需要多杠杆：高管学院、黑客松、AI Academy、开发者培训 + 全员培训

### Peter 补充
- 文化变革必须**自上而下 + 自下而上**：领导层买断 AI-first + 一线员工提出创新
- 关键：在可接受风险的领域创造**实验空间**
- 平衡：既要鼓励实验，又要确保输出基于**可验证事实**

---

## 四、产品演示（Nick Linton, Product Lead for Financial Services）

> "我们今天互动的模型，是所有未来版本中最差的版本。"

### 三大产品支柱

**1. 模型**
- Claude Opus/Sonnet 在金融推理任务（Vowels.ai Finance Agent Benchmark）大幅领先竞品
- Fundamental Labs 基于 Opus 构建的 Excel Agent（Shortcut）在 Financial Modeling World Cup 7 级中通过 5 级，金融推理和 Excel 任务准确率 83%+
- 研究-产品飞轮：与客户合作识别模型强弱项，持续 "hill climb"

**2. Agent 能力（Research Preview）**
- 多模态报告生成：Pitch Deck、投资备忘录
- 数据可视化：基准分析、股价/成交量图表
- 原生读写 Excel
- 扩展使用限制 + Claude Code 集成（大数据集、Monte Carlo 模拟）

**3. 平台**
- 首个跨所有核心金融数据源的统一智能 Agent
- 白手套级别的金融专属实施与 onboarding
- SOC2 Type II 认证，默认不在客户数据上训练

### 场景演示：Hedge Fund 分析师的一天

**场景设定**：
- Sarah，Acme Capital 分析师
- 下午 2 点，PM 冲进来：目标公司 Velocity Athletic 营收降 12%，股价却涨 17%（$71/股）
- 问题：这反弹是基本面支撑还是泡沫？市场收盘前需要答案

**传统流程**：4-5 小时，跨 14 个浏览器标签页

**Claude 流程（< 30 分钟）**：

1. **多源数据统一查询**：
   - S&P Global → 电话会议记录
   - Morningstar → 研报
   - Box → 内部分析
   - Deloopa → 8 季度财务数据
   - 输出：**综合情报**（不是原始数据堆砌）

2. **发现关键线索**：
   - 财报 Q&A 中 CFO 披露关税导致 400bp 利润率损失
   - 竞对 Pace Running 2019 年已布局越南
   - CFO 内部减持

3. **自动生成分析**：
   - **事件标注股价图**：标注 17% 跳涨对应的关键事件（紧急董事会、CFO 减持、业绩超预期）
   - **可比公司估值表**：Velocity 21× EBITDA vs 同行 16×，基本面更差
   - **可审计 DCF 模型**：含情景选择器、假设链接、自动计算 WACC → 公允价 $54，$71 过高

4. **交付物生成**：
   - 调用 Box 内的公司模板
   - 30 秒生成专业投资备忘录：建议 "fade the rally"（趁着反弹出货），完整引用来源
   - 结论：市场过度定价了运营挑战，现在卖出，等回调更低再买回

### 效果总结

| 维度 | 传统 | Claude |
|:---|:---|:---|
| 耗时 | 4-5 小时 | < 30 分钟 |
| 数据平台 | 14 个标签页 | 1 个工作区 |
| 遗漏风险 | 高（CFO 减持、竞对优势） | 低（全源综合） |
| 可审计性 | 手动查证 | 一键溯源 |

---

## 五、案例：挪威主权财富基金（NBIM）

- **规模**：$2 万亿，全球最大主权基金
- **人员**：仅 700 名员工（人均管理资产全球最高）
- **配置**：70% 股票，30% 固收

**CEO Nicolai Tangen 评价**：
- "Claude 从根本上改变了我们的工作方式"
- 实现 **20% 生产率提升** = 年节省 **213,000 小时**
- "Claude 已经不可或缺"

---

## 六、Panel 讨论（行业领袖圆桌）

### 嘉宾

| 嘉宾 | 机构 | 角色 |
|:---|:---|:---|
| **Michael** | DE Shaw | COO Group Co-Head，负责全公司转型 |
| **Lloyd Hilton** | HG Capital | AI Lead，全球 Top 10 PE |
| **Don Vu** | New York Life | Chief Data Analytics Officer，Fortune 70 保险 |
| **Frode** | 挪威主权基金 NBIM | 北美权益投资团队 |
| **Jonathan Pelosi** | Anthropic | Head of Financial Services（主持） |

### 议题一：AI 投入的触发点

**Frode（NBIM）**：
- 由 CEO Nikolai Tangen（"AI maniac"）自上而下强力推动
- 策略：成为投资管理中 AI 的领先使用者，嵌入一切工作
- 已建立专职 AI 团队，全组织协调推进

**Lloyd（HG Capital）**：
- 合伙人多有技术背景，早期就识别出平台级变革（类比 on-prem→SaaS）
- 2021 年已有 GPT-3 权限；催化剂是一次硅谷 AI 沉浸活动（Mike Krieger 到场）
- 起初目标 10-20% 生产率提升，现在焦点变成**全面 AI 转型 50 家被投公司**
- 120,000 FTE 覆盖

### 议题二：Build vs Buy

**Don（New York Life）**：
- 选择**买而不是自己造**——Anthropic 的创新速度太快，自研 UI 层跟不上
- 把内部工程师资源聚焦于**真正有竞争优势**的定制方案
- 通用能力和 connectors 交给平台

**Michael（DE Shaw）**：
- DE Shaw 以自研文化闻名，但这次不同
- **技术迭代速度**改变了 build vs buy 的平衡
- 当前做法：两者并行，但**极其谨慎选择哪里 build、哪里 buy**
- 一个洞见：客户自己开发了某个 AI 功能，等见到 Anthropic 时发现已经过时了

### 议题三：变革管理 & 文化

**Don（New York Life）**：
- "Everything, Everywhere, All at Once" 策略
- 三层：针对性用例（直接价值）→ 全员赋能 → 业务域重塑（Agentic AI）
- 关键是**思维转变**：给每个人发跑步机不等于治愈心脏病
- AI 不是 Google 搜索框——是真的人机协作伙伴
- 类比：去哥斯达黎加旅游，Google 给推荐列表，Claude 以旅游局长身份给定制行程

**Lloyd（HG Capital）**：
- 50 家公司统一转型：来自 HG 的 20 名 AI 专家 + 150 名外包/合作伙伴
- 一次突破：某被投公司部署 **1,000 个 Agentic Software Engineer** 实例，开发产能 +50%
- 平均软件开发生产率提升 30%；部分团队从 9 人减到 2 人
- 强调：**不裁人**——产出增益用于偿还技术债和构建 AI 产品

**Frode（NBIM）**：
- 团队很多内向的人，喜欢编码和做事
- Claude 的 project 和协作功能正加速文化转变
- 主权基金的独特优势：无客户压力，更自由地采用 AI

### 议题四：从哪开始？

**Michael（DE Shaw）**：
- **不要找一个"最佳起点"**——你不需要知道怎么用才给工具
- 给你的人工具，他们会发现你想象不到的用途
- DE Shaw 的实践：分散赋权 + 使用密度追踪 → 呈现对数正态曲线（越多用越想用）
- 两条具体建议：
  1. 团队例会做 30 秒 "AI 闪电分享"——每人说一个这周用 AI 尝试的奇怪东西
  2. 鼓励个人生活中实验——不丢人，更容易迈出第一步
- **每 6 个月回访**之前觉得不行的用例，技术进步可能已经完全改变结果

**Lloyd（HG Capital）**：
- 投资于**提示词/上下文工程能力**——懒 prompt vs 精心设计差距巨大
- 找出组织中的 **AI champions（超级用户）**作为放大器
- 优先选择：高频机械性重复任务（结构化数据、标准化流程）

**JP（Anthropic）总结**：
- 不用找第一个用例——先让员工用起来
- 想建培训方案？问 Claude
- 员工不知道从哪开始？让他们描述工作，问 AI 给 3 个可以试的方向

### 议题五：如果重来一次？"跑得更快"

**Frode**：早一点开始。即使犯了错，学到教训，继续前进。

**Don**：更早抓**心态和文化转变**——不只是工具部署，是从"Google 式单次问答"到"AI 作为协作伙伴"的范式转换。

**Lloyd**：跑得更快。模型和生态的指数级进步是前所未有的。

**Michael**：
- 使用强度呈对数正态分布（用得越多越会用）
- 鼓励多咬一口苹果：工作场景 + 个人生活
- 他让团队每周围绕 AI 做知识分享

### JP 的收尾个人故事
- 2 岁儿子有严重健康问题
- 医院给 1,100 页 NICU 和神经科病历
- 全部上传 Claude，生成时间线分析
- 拿给医生，医生震惊："你怎么整理出来的？"
- 核心理念：**先用在自己生活中**，工作中的应用就会爆发

---

## 七、关键 Takeaways

1. **Claude for Financial Analysis 正式发布**——Anthropic 首次推出行业专属产品，集成 FactSet / S&P CapIQ / Morningstar / PitchBook / Deloopa 等金融数据

2. **从工具到统一智能层**：不是又一个 AI chat，而是打通所有金融数据源的 Agent 平台

3. **真正的生产力飞跃**：
   - 挪威主权基金：年省 213,000 小时，20% 生产率提升
   - AIG 承保：周→天，准确率 75%→90%
   - HG Capital：开发产能 +50%（部署 1,000 个 AI 软件工程师）

4. **行业共识：跑得更快**——四大机构（DE Shaw / HG Capital / New York Life / NBIM）一致结论：早一天用就早一天领先

5. **AI 引入不是工具部署，是文化变革**：
   - 自上而下 buy-in + 自下而上创新
   - 个人生活先用 → 工作再用
   - 每半年重新评估（不要让去年的印象限制今年的决策）
   - 培养 "AI champion" 超级用户

6. **Build vs Buy 的天平正在改变**：技术迭代太快，自建 UI 的性价比下降

7. **1 个月免费试用**：发布会现场观众可获得

---

## 八、个人思考

待补充。