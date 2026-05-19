---
title: The Founder's Playbook — Anthropic 官方 AI-Native 创业指南
type: reading-notes
created: 2026-05-20
updated: 2026-05-20
sources:
  - https://cdn.prod.website-files.com/6889473510b50328dbb70ae6/69fe2a55b93bb0732b1fe33c_The-Founders-Playbook-05062026_v3.pdf
  - published by Anthropic, May 14 2026
tags:
  - startup
  - AI-native
  - Anthropic
  - agentic-coding
  - founder
  - product-market-fit
  - Claude-Code
  - Claude-Cowork
---

## 基本信息

- **出版方**：Anthropic
- **发布日期**：2026 年 5 月 14 日
- **页数**：35 页
- **背景**：Claude for Small Business 发布次日推出

---

## 核心论点

AI 彻底重启了创业生命周期。**技术能力不再是门槛，判断力才是。**

> In 2026, a good idea gets founders further than ever. Agentic coding compresses what used to take a team of engineers into work a founder can ship themselves.

---

## 一、创始人角色已变

过去创始人被分为"能写代码的"和"能谈业务的"。现在这条线消失了。

创始人从 **执行者** 变为 **AI agent 的指挥者**，注意力上移到更高阶的工作：

1. **研究能力** — Claude 作为每领域即时专家（竞争分析、财务建模、投资者备忘录）
2. **Agentic 编码** — Claude Code 代替整个工程团队
3. **工作流自动化** — Claude Cowork 处理 CRM、调度、报告、合规跟踪

> 10 人独角兽不再是被迫无奈，而是刻意的设计。

---

## 二、四大阶段全景

### 阶段 1：Idea（创意验证）

**目标**：在写任何一行代码之前，确认问题真实存在且方案有效。

**退出条件**（三个问题全答 Yes）：
1. 问题真实且具体——能准确说出谁受影响、频率、严重度
2. 方案解决的是验证出的**真实问题**，不是最初假设的问题
3. 有足够信号证明值得构建 MVP

**核心挑战**：
- **混淆构建与验证** — 用 AI 瞬间搭出原型≠已验证。42% 初创失败是因为做了没人要的东西
- **过早规模化** — AI 让你在验证前就跑出完整产品路线
- **确认偏误放大器** — AI 能找到证据支持任何观点，需要主动让它当魔鬼代言人

**Claude 使用要点**：
- 用 Claude 将模糊问题细化到可测试的假设
- **让 Claude 扮演反对角色**，找反驳证据
- Claude Cowork 做竞争分析、TAM/SAM/SOM 建模、趋势分析
- 设计客户发现访谈（找谁、问什么、分析结果）
- Claude Cowork 自动化联系人搜集、外联、面试日程
- Claude Code 构建**极轻量原型**用于真实用户反馈

---

### 阶段 2：MVP（最小可行产品）

**目标**：将有验证的问题转化为有真实 PMF 证据的产品。

**退出条件**：真实的留存、付费或推荐信号。

**核心挑战**：

1. **Agentic 技术债** — AI 去除了所有自然瓶颈，太快会积累无法偿还的技术债。每新开一个 Claude Code session 可能从头推导基础架构决策
2. **虚假 PMF** — 日活/注册量好看可能是朋友支持、HackerNews 效应，不持久
3. **零摩擦范围蔓延** — AI 让加功能太容易，每个单独看都合理，汇总是灾难
4. **安全盲区** — AI 生成能跑的代码 ≠ 安全的代码。上线前必须做安全审查

**Claude 使用要点**：
- **先定义架构再写代码**：开 Claude Code 前，先用 Claude 做架构决策文档 → 存为 CLAUDE.md
- 定义 MVP scope 文档：写清楚做什么、**故意不做什么**、什么证据能触发新增功能
- Claude Code 构建 MVP，每次 session 结束时更新 CLAUDE.md
- **安全审查**：部署前用 Claude Code Security 扫描认证、数据暴露、注入风险
- 上线前定义度量框架——留存基准、激活标准、Day 7 / Day 30 目标
- Claude Cowork 管理用户反馈循环（外联、反馈会议、bug 分类、周度摘要）
- **权衡**：三个以上迭代周期无进展 → 用 Claude 诊断：是客户群错了、定位错了还是产品错了？

---

### 阶段 3：Launch（上线）

**目标**：将早期牵引力转化为可重复、渠道驱动的增长引擎。

**退出条件**（三项俱全）：
1. 增长可重复、由渠道驱动，**CAC / LTV / 回收期**可量化和辩护
2. 产品能承受生产级负载，安全合规就绪
3. 运营不再依赖创始人个人

**核心挑战**：
- **技术债到期** — MVP 代码的快捷方式在生产流量下暴露
- **创始人成瓶颈** — 决策堆积、支持积压、运营只在创始人记得时才发生
- **安全与合规不再可推迟** — 真实用户数据、支付、受监管行业 = 真金白银的暴露风险

**Claude 使用要点**：
- Claude Code **全架构审计** → Claude 排序修复优先级 → 写回 CLAUDE.md
- Claude Cowork 审计创始人当前运营负荷 → 分类：可全自动/需要人但不一定是创始人/需要创始人
- Claude Code 安全审计（SOC2/GDPR/HIPAA 标准）
- **企业合规文档生成**：SOC2 要求什么 → Claude 生成需要的文档/审计日志/访问管理
- Claude 设计轻量产品管理流程 → Claude Cowork 执行（周期会议、bug 路由、周度指标汇总）
- **三种 Claude 同时使用，效果叠加**：Claude Code 建产品、Claude Cowork 建公司、Claude 将知识运营化

---

### 阶段 4：Scale（规模化）

**目标**：企业级扩张 + 建立可防御的护城河。

**退出条件**：公司在创始人不再跑日常业务的情况下仍能持续运转——可持续盈利 / IPO-ready / 被收购。

**核心挑战**：
- **将运营系统交出去** — 不是技术问题，是心理问题
- **规模化技术运营** — 企业客户要的不是功能清单，是 SLA + 文档 + 可靠性保证
- **规模化组织功能** — 薪资、法务、合规、合同管理
- **构建 GTM 引擎** — 创始人个人销售触达天花板，需要全套 go-to-market

**Claude 使用要点**：
- Claude Cowork 接手日常运营任务，创始人专注只有自己能做的事（董事会、大客户、产品叙事）
- Claude Code 按企业标准加固代码 + 构建日志/监控/事件响应
- Claude 起草产品文档、支持手册、SLA 文件
- Claude 从零搭建 GTM：市场细分 → 信息架构 → 分析师策略 → 销售手册
- Claude Cowork 执行 GTM 战术层：内容推送、外联序列、CRM 维护、管线报告
- Claude Code 构建交互式演示环境 + 集成文档 → 让 GTM 在创始人开会时自动跑

---

## 三、护城河构建策略

### 领域专长 → 产品特异性

创始人将行业知识通过 Claude 做成结构化上下文 → Skills 编码可复用流程 → 数月积累形成**专有知识基底**，通用 AI 无法匹敌。

### 累积用户行为数据

用户使用数据是**时间锁定、上下文特定、不可复制**的。`每次改进 → 更好用 → 更多使用 → 更多反馈 → 更多改进` 形成飞轮。

### 工作流锁定（Workflow Lock-in）

用户在你的产品上构建自动化、训练团队使用、连接数据源 → **切换成本从"换产品"变成"组织级运营项目"**。

最深度的锁定 = 让客户在你的产品上**构建**，而不只是使用。

---

## 四、全文核心语录

- "创业者不该搞错的第一件事：把做出来当成验证了。"
- "AI 会用完全相同的热情为一个正确和一个错误的前提生成代码——聪明的那个是你。"
- "42% 的初创公司死因是做没人要的东西。AI 让这个比例只会更高。"
- "如果 IDEs 年底前就被淘汰，现在在 UI 上过度投资就是浪费时间。"
- "The bottlenecks are no longer what you can build, but what you choose to build."
- "创始人角色没变：找到真问题，做解决它的东西，做成一家重要的公司。变的是路径。"

---

## 五、评价

这是一份**产品手册，也是战略文档，更是 Anthropic 的 B2B 销售物料**。

它有三层身份：
1. **真诚的创业方法论** — 对 AI 时代创业风险的认知非常清醒（虚假 PMF、安全、技术债），这些警告真实有效
2. **Claude 全家桶的产品展示** — Chat / Cowork / Code / Security 每个都在对应阶段被巧妙植入为解决方案
3. **意识形态宣言** — "一人十亿"的创业模型是 Anthropic 的核心叙事

**最有价值的洞见**（非推销部分）：
- "混淆构建与验证"是一个极精确的诊断
- Agentic technical debt 的概念：每新开 session 可能不知不觉重新推导架构
- 安全盲区警告：生成能跑的代码 vs 安全的代码之间有巨大 gap
- 创始人 bottleneck 的自我诊断框架

**值得警惕的**（推销部分）：
- Tech Times 指出：playbook 建议在 Launch 阶段用 Claude Cowork 处理合规，但 Anthropic 官方文档写明 Cowork 活动**不在审计日志、合规 API 或数据导出中捕获**——所以不应该用于受监管工作负载
- 全部案例来自 Claude 生态，没有独立验证