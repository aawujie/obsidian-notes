---
title: "Loop Engineering - 14步从Prompter到Loop Designer"
type: translation
created: 2026-06-10
updated: 2026-06-10
sources:
  - "https://x.com/0xcodez/status/2064374643729773029"
tags:
  - agent
  - loop-engineering
  - coding-agent
  - best-practice
  - translation
---

## 原文信息

- 作者：Codez (@0xCodez)
- 时间：2026-06-09
- 点赞：840 | 转发：136 | 浏览：168,610
- 原文标题：Loop engineering: the 14-step roadmap from prompter to loop designer

---

14 步。3 个层级。停止 prompt，开始设计。

## Part 1: 为什么 & 测试

### 01. Loop engineering 正在取代你作为 prompter 的位置

两年来，你从 coding agent 那里得到东西的方式是：写 prompt、分享上下文、读结果、写下一个 prompt。agent 是工具，你一直握着它。这部分正在结束。

Loop engineering 是构建一个小系统：自己发现工作、交给 agent、检查结果、记录发生了什么、决定下一步——自主运行。你设计这个系统一次，之后系统自己去 prompt agent。

Addy Osmani 把它拆成六个部分。Anthropic 工程师现在每天合并的代码量是 2024 年的 8 倍。

### 02. 四条件测试（建 loop 前必跑）

| 条件 | 含义 |
|:---|:---|
| 任务重复 | 每周至少一次。低于此频率 → 设置成本永远无法摊销 |
| 自动验证 | 测试/类型检查/build/lint 能无需人在场就拒绝烂代码 |
| Token 预算撑得住 | loop 重复读上下文、重试、探索，不管是否产出都烧 token |
| Agent 有高级工程师工具 | 日志、复现环境、能跑自己写的代码并看到哪里坏了 |

### 03. 谁赢谁输

**实际受益者：**
- 有重复、机器可验证工作且有预算的团队（CI triage、依赖升级、lint 修复）
- 已有强测试覆盖的代码库
- 已在使用多 agent 模式的异步优先团队

**今天应该跳过的人：**
- 消费计划的个人开发者——token 账单比生产力收益先到
- 无自动验证的代码上的任何人
- 真正瓶颈是审查能力而非打字速度的团队

### 04. 30 秒 loop 检查

1. 任务每周至少一次 → 少于每周 = 设置成本无法摊销
2. 测试/类型检查/build/lint 能拒绝坏输出 → 无自动门 = agent 给自己作业打分
3. Agent 能跑自己改的代码 → 无复现环境 = 盲目迭代
4. Loop 有硬性停止 → token 预算、迭代次数或时间限制
5. 合并/部署/依赖变更前有人审核 → 不可逆操作前需要人类批准

**好的第一个 loop：** CI 失败 triage、依赖升级 PR、lint 修复、flaky test 复现、强测试项目上 issue→PR
**坏的第一 loop：** 架构重写、认证/支付代码、生产部署、模糊的产品工作、"做得好了"是主观判断的任务

## Part 2: 五个构建块

### 05. Automations: 心跳
Automations 让 loop 成为真正的 loop。它们按计划/事件/触发条件启动。

- **Codex：** Automations 标签页
- **Claude Code：** `/loop`（会话内循环）、计划任务（重启后存活）、Routines（合上笔记本后继续）

两个关键 primitive：
- `/loop` — 按节奏重复运行
- `/goal` — 一直运行直到某个条件成立。一个单独的小模型检查完成状态，写代码的 agent 不是判卷的那个

### 06. Worktrees: 并行不混乱
运行不止一个 agent 时文件开始碰撞。git worktree 解决——独立工作目录 + 独立分支 + 共享 repo 历史。

两边工具都内置了。Worktree 消除了机械碰撞，但你仍是天花板——是审查带宽决定你能实际并行跑多少 agent。

### 07. Skills: 项目知识写一次，每次运行读取
Skill 是让你不用每次 session 都重新解释项目上下文的方式。两个工具使用相同格式：SKILL.md 文件夹。

对 loop 特别重要的原因：没有 skill 的 loop 每个周期从零重新推导项目上下文。有 skill 的意图会复合。约定、构建步骤、"我们不这么做因为那件事"——写在外部一次，每次运行读取。

### 08. Connectors: loop 通过 MCP 接触你的真实工具
只能看见文件系统的 loop 是很小的 loop。Connectors 基于 MCP，让 agent 读取 issue tracker、查询数据库、调用 staging API、在 Slack 发消息。

回报最快的 connectors：GitHub → Linear/Jira → Slack → Sentry/错误追踪器

> 这就是"agent 说这是修复方案"和"loop 打开 PR、链接 ticket、CI 变绿后 ping 频道"之间的区别。

### 09. Sub-agents: 把写的和查的分开
最有用的结构性设计：拆分写代码的 agent 和检查代码的 agent。

Osmani 的精准表述：写代码的模型"给自己的作业打分太友善了"。第二个不同 instructions、有时不同 model 的 agent 能抓住第一个说服自己忽略的问题。

这是 Anthropic 2024 年 12 月工程帖里的 evaluator-optimizer 模式。一个生成，一个批判，重复。

对 loop 特别重要的原因：loop 在你不看着的时候运行，所以你真正信任的 verifier 是你能走开的唯一理由。

常见拆分：一个探索 → 一个实现 → 一个根据 spec 验证。

## Part 3: 要么建对，要么别建

### 10. 状态文件：agent 忘记，文件不会
这听起来太简单以至于不重要，但它是每个工作 loop 的脊柱。一个 markdown 文件、一个 Linear board、一个 JSON 状态——任何存在于单次对话之外、记录了已完成和下一步的东西。

> agent 忘记，repo 不会。

两种存放模式：
- **仓库内 Markdown** — STATE.md，版本控制，diff 可读，适合个人/小团队
- **外部系统** — Linear、GitHub Issues、数据库，跨仓库存活，可查询，团队可见

对长期运行的 loop，把状态文件和 VISION.md 或 AGENTS.md 配对——agent 每次运行重读。状态告诉 agent 在哪。spec 告诉它去哪。

### 11. 最小可行 Loop
四部分，没有群涌：

1. **一个 Automation** — 按节奏触发，有明确停止条件
2. **一个 Skill** — 一个 SKILL.md 存储项目上下文
3. **一个 State File** — 记录已完成和下一步
4. **一个 Gate** — 测试/类型检查/build，自动拒绝坏工作

顺序重要：先让手动运行可靠 → 变成 skill → 包进 loop → 排程。跳步是 loop 在生产中失败的原因。

核心指标：每次被接受的变更的成本——不是 token 消耗，不是任务尝试数。接受率低于 50%，loop 在亏损。

### 12. Ralph Wiggum Loop：静默失败的 loop
Geoffrey Huntley 记录并命名了这种失败模式。Agent 本该在完成时才输出 completion token，但提前输出了，loop 在半成品上退出。没有硬性 gate，loop 静默失败并持续花费。

其他已知失败模式：
- **Goal Drift**：长会话中每次摘要都丢失信息，"别做X"在第 47 轮消失。缓解：每次运行重读 VISION.md
- **Self-preferential Bias**：写的 agent 给自己打分太友善。缓解：独立的 verifier subagent
- **Agentic Laziness**：loop 在部分完成时声明"够好了"。缓解：`/goal` + 新模型检查客观停止条件

### 13. 理解债和认知投降
两个命名的风险，都来自 Osmani：

**理解债**：loop 越快交付你没写的代码，仓库内容和你的理解之间的差距越大。痛的账单不是 token 账单，而是没人读过这个系统的你需要 debug 的那一天。

**认知投降**：停止形成判断、接受 loop 返回的一切的冲动。带判断力设计 loop = 解药，为了逃避思考设计 loop = 加速剂。同一个动作，相反结果。

缓解措施非技术性：
- 读 diff。不读就租了复利理解债
- 抽查 gate。挑几个 loop 开的 PR，确认批准的测试真的抓住了你关心的失败模式
- 禁止 loop 做架构工作。保持在小的、机器可验证的变更上
- 和队友配对设计 loop。第二双眼睛能抓住盲点

### 14. 安全税：无人值守 = 无人值守的攻击面

loop 必须防御的威胁模型：
1. **生成的代码未经审查就发运** → 需要 SAST、依赖审计、秘密扫描
2. **Skills 作为注入向量** → 安装前审计 skill 来源
3. **凭证在日志中** → 在生产 loop 中禁用详细日志
4. **权限范围悄悄扩大** → 每 30 天重新审计权限

## 十个常见坑

1. 没跑四条件测试就建
2. 没有客观 gate——第二个 agent "审查"只是第二个乐观者
3. 同一个 agent 又写又查——自偏好偏差
4. 没状态文件——明天从头开始
5. 模糊的停止条件——"看起来好了就行"
6. 没 token 预算上限——野心 loop 烧 5-10 倍预期
7. 消费计划上跑重验证——token 账单先到
8. 自动安装社区 skill——审计的 17,022 个 skill 中 520 个泄露凭据
9. 用 loop 做判断性工作——架构、认证、支付、模糊产品决策
10. 不读 diff——复利理解债

## 结论

> 两年来，和 coding agent 协作的杠杆在 prompt 上。更好的 prompt，更好的上下文，更好的一次性输出。那个阶段正在结束。agent 变得足够好了，下一个杠杆点上移了一层：那个决定它们做什么、什么时候做、用什么把关、什么状态在运行间存活的系统。
>
> 但这个故事的诚实版本不是每个人都应该冲去建 loop。大多数开发者还不需要——直到任务重复、验证自动化、预算能吸收浪费、agent 有高级工程师工具。缺一条，loop 成本超过回报。
>
> 如果通过了测试，建小的。一个 automation。一个 skill。一个 state file。一个 gate。先让手动运行可靠。变成 skill。包进 loop。排程。顺序重要。跳步就是在为一个没人理解的系统付钱。
>
> Cherny 的观点不是工作变简单了。是杠杆点移动了。建 loop。继续做工程师。