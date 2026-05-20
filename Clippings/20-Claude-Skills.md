---
title: 20 Claude Skills Most Builders Don't Know Exist
type: clipping
created: 2026-05-20
source: https://x.com/sairahul1/status/2056665329305256232
author: Rahul (@sairahul1)
tags: [Claude, AI, Skills, Prompt工程, 效率工具]
---

## 核心观点

> **Prompt 是一次性的。Skill 永不过期。**

Skill 是 `.md` 文件，给 Claude 一份永久的「职位描述」——不是告诉它做什么，而是告诉它**每次遇到特定任务时应该成为谁**。一次构建，自动加载，每次都从你的标准开始。

## 安装方式

- **Claude.ai**：Settings → Sub-Agents → Add，粘贴 Skill 内容
- **Claude Code**：创建 `.claude/agents/` 目录，每个 skill 存为 `.md` 文件
- **Claude Desktop**：Settings → Sub-Agents → Add

---

## 20个 Skill 分类

### Category 1: Content & Writing（内容与写作）

**01. The Hook Forge** — 钩子工厂
- 输入任意主题，生成10个基于不同心理触点的钩子（好奇心、损失、对比、特指、争议等）
- 使用时机：有想法但没开场白时，写正文之前先跑这个

**02. The Voice Locker** — 语气锁定
- 分析你的写作样本，永久锁定你的个人风格到 Claude
- 使用时机：新建 Claude Project 时第一个要跑的 Skill

**03. The Thread Architect** — 推文线程建筑师
- 将任意想法构建为结构化的 Twitter/X 线程（钩子→张力→回报→CTA）
- 每条推文必须让读者想看下一条

**04. The Repurpose Engine** — 内容复用引擎
- 一篇长文输入 → 6种平台原生输出：Twitter线程、LinkedIn帖子、Newsletter段落、3个独立钩子、引用图配文、短视频脚本开头
- 使用时机：完成任何长文后，需要分发但不想花3小时重新排版

**05. The Headline Lab** — 标题实验室
- 生成15个标题，覆盖8种格式（How-to、数字列表、提问、对比、秘密、警告、结果、身份），评分排序，给出前3
- 使用时机：写完了但标题在猜——标题决定200读者还是2万

### Category 2: Research & Analysis（研究与分析）

**06. The Brief Builder** — 简报构建器
- 将模糊研究需求转化为可执行的研究简报：核心问题、5个具体信源、5个信号指标、待验证假设、一个决定性发现
- 使用时机：先做简报再做研究，顺序不能反

**07. The Contradiction Finder** — 矛盾发现器
- 找出多个来源之间的矛盾、最薄弱的论断、表象共识之下的真正争议
- 使用时机：构建论点前，先知道自己的信源弱在哪

**08. The Signal Scanner** — 信号扫描器
- 处理一周行业内容，分离信号与噪音，识别底层趋势和早期指标
- 使用时机：每周处理行业信息时，在周一开始之前

**09. The Assumption Auditor** — 假设审计师
- 找出计划中所有假设（显性的和隐性的），标记最危险的假设（如果错了整个计划崩溃）
- 使用时机：发布/投入前前一天跑，不是之后

**10. The Source Ranker** — 信源排序器
- 按可信度、时效性、相关性排列信源，标记该用、该验证、该砍掉的
- 使用时机：收集完信源后，先排序再写作

### Category 3: Business & Operations（商业与运营）

**11. The SOP Writer** — SOP编写器
- 将粗糙的流程描述（甚至语音转文字）变成可执行的SOP，含触发条件、步骤、负责人、工具、输出、质量检查点、不可自动化环节
- 使用时机：流程只存在你脑子里时

**12. The Decision Framer** — 决策框架器
- 将纠结的决策重新框定：真正在决定什么、3个真正选项、3个核心标准、你不知道的2件事、什么都不做的默认结果
- 使用时机：一个决策想了一周还没做决定

**13. The Meeting Extractor** — 会议提取器
- 从会议录音/笔记中只提取四样：决定、行动项（含负责人+截止日）、阻塞项、未言明的关键问题
- 使用时机：每次会议结束后，无例外

**14. The Pricing Stress Tester** — 定价压力测试
- 从三个视角压力测试定价：怀疑型买家、价值型买家、竞争对手
- 使用时机：准备推出新定价或丢单而不明原因时

**15. The Offer Sharpener** — 产品打磨器
- 找出「你以为在卖的」和「买家以为在买的」之间的差距，重新打磨直到价值无法被误解
- 使用时机：人们说"有意思"但不买的时候，说明有差距

### Category 4: Coding & Dev（编码与开发）

**16. The Code Explainer** — 代码解释器
- 两层解释：Level 1给使用者（非技术人员能懂），Level 2给修改者（架构决策、脆弱点、核心假设）
- 使用时机：接手别人代码、新人入职、准备改6个月没碰的代码

**17. The PR Reviewer** — PR审查器
- 审查 Pull Request：bug、缺失测试、安全问题、风格违规、一个值得讨论的架构决策
- 使用时机：任何PR合并前，90秒抓80%问题

**18. The Debug Partner** — 调试搭档
- 系统性诊断：错误实际在说什么→3个最可能根因→诊断步骤→修复方案→回归测试
- 使用时机：盯着bug超过20分钟，停止猜测

### Category 5: Strategy & Thinking（战略与思维）

**19. The Second Order Thinker** — 二阶思考器
- 映射决策的一阶→二阶→三阶效应，找出意外后果和反馈回路
- 使用时机：做影响超过30天的决策时

**20. The Mental Model Applier** — 思维模型应用器
- 为具体问题选择最匹配的3个思维模型，逐一应用，输出洞察和行动建议
- 使用时机：从同一角度思考一个问题太久，需要视角转换

---

## 最终观点

> 你一直构建的是会过期的 Prompt。每场会话从零开始。每次通用输出都是 Claude 不知道你是谁、你怎么想、你的标准是什么的结果。
>
> 产出10倍效率的构建者不是更聪明——他们只是把 Skills 建好了，每场会话不再重建。
>
> 20个 Skills。一个下午的设置。之后每场会话 Claude 都按你的标准、你的语气、你的规则工作。
>
> **打开文件夹，粘贴文件，不再从零开始。**