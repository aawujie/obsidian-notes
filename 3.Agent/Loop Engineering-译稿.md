---
title: "Loop Engineering"
type: translation
created: 2026-06-10
updated: 2026-06-10
sources:
  - "https://x.com/cellinlab/status/2064144608242679822"
tags:
  - agent
  - loop-engineering
  - coding-agent
  - translation
---

## 原文信息

- 作者：Cell 细胞 (@cellinlab)
- 时间：2026-06-09
- 点赞：268 | 转发：50 | 浏览：125,017
- 原文标题：[译] Loop Engineering

---

Loop Engineering 正在取代"你亲自给 agent 写 prompt"这件事。它的核心是：你不再直接 prompt agent，而是设计一个系统，让这个系统去 prompt agent。

这里的 loop，可以理解为一种递归目标：你定义一个目的，然后让 AI 不断迭代，直到任务完成。它大致由五个构建块组成，而 Claude Code 和 Codex 现在都已经具备了这五个能力。

我认为，这可能是我们未来与 coding agent 协作的方式。不过，现在仍然很早期。我对此也保持怀疑，而且你必须非常注意 token 成本，因为不同使用模式下的消耗差异可能非常大，尤其取决于你是 token 富裕还是 token 紧张。你仍然需要某种方式来确保质量不会下降，对"AI slop"的担忧也完全合理。话虽如此，我们还是来看看它到底是什么。

## 核心观点

最近有人说：

> 你不应该再去 prompt coding agent 了。你应该设计 loops，让 loops 去 prompt 你的 agents。

类似地，Anthropic 的 Claude Code 负责人也说过：

> 我现在已经不直接 prompt Claude 了。我有一套 loops 在运行，它们会去 prompt Claude，并判断接下来要做什么。我的工作是写 loops。

过去大约两年里，你想让 coding agent 做事，基本方式就是写一个好的 prompt，并提供足够多的上下文。你输入一段内容，阅读它返回的结果，再输入下一段。agent 是一个工具，而你一直握着这个工具，一轮接一轮地操作。

这部分工作某种程度上已经结束了，或者至少有些人认为它正在结束。

现在，你构建的是一个小系统。这个系统会自己发现工作、分发工作、检查工作、记录完成情况，然后决定下一步要做什么。你让这个系统去触发 agents，而不是你亲自触发。

## 五个构建块 + Memory

一个 loop 需要五样东西，以及一个用来记住状态的地方。

### 1. Automations
按计划自动触发，自己做 discovery 和 triage。

### 2. Worktrees
让两个并行工作的 agents 不会互相踩到对方。

### 3. Skills
把项目知识写下来，避免 agent 靠猜。

### 4. Plugins 和 Connectors
把 agent 接入你已经在用的工具。

### 5. Sub-agents
让一个 agent 负责提出想法，另一个 agent 负责检查它。

### 6. Memory
这个 memory 可以是一个 markdown 文件，也可以是一个 Linear board，或者任何存在于单次 conversation 之外、能够保存"已完成事项"和"下一步事项"的地方。

> 模型在每次运行之间会忘记一切，所以 memory 必须存在磁盘上，而不是只存在 context 里。agent 会忘记，但 repo 不会。

## 细节展开

### Automations
Automations 是让 loop 成为真正 loop 的东西，而不是只运行一次的任务。

Claude Code：用 `/loop` 按间隔运行，安排 cron task，还可以推到 GitHub Actions。`/goal` 则会一直运行，直到某个条件成立——一个单独的小模型检查完成状态，写代码的 agent 不是给自己打分的那个。

### Worktrees
同时运行不止一个 agent，文件就会开始冲突。git worktree 解决——独立 working directory + 独立 branch + 共享 repo history。两边都内置了。

### Skills
skill 的作用，是让你不用每次 session 都重新解释同一个项目上下文。两个工具都使用相同的格式：SKILL.md。没有 skills，loop 每个周期都要从零重新推导你的整个项目。

### Connectors
Connectors 基于 MCP，让 agent 可以读取 issue tracker、查询数据库、调用 staging API、在 Slack 里发消息。plugins 还可以把 connectors 和 skills 打包在一起。

### Sub-agents
最有用的结构性设计，是把"写的人"和"检查的人"拆开。写代码的模型，在给自己的作业打分时太友善了。一个带有不同 instructions、甚至有时使用不同 model 的第二个 agent，能抓住第一个 agent 自我说服后忽略的问题。

两个工具里常见的拆分方式都是：一个 agent 负责探索；一个 agent 负责实现；一个 agent 负责根据 spec 验证结果。

## 组合起来

每天早上，一个 automation 会在 repo 上运行。

它的 prompt 会调用一个 triage skill。这个 skill 会读取昨天的 CI failures、open issues、recent commits，然后把 findings 写进一个 markdown 文件，或者写进 Linear board。

对于每个值得处理的 finding，这个 thread 会打开一个隔离的 worktree，并派一个 sub-agent 去 draft fix，再派第二个 sub-agent 根据项目 skills 和现有 tests 去 review 这个 draft。

connectors 让 loop 可以打开 PR，并更新 ticket。

任何 loop 无法处理的事情，都会落到 triage inbox。

state file 是整套东西的脊柱。

> 你只设计了一次。你没有亲自 prompt 其中任何一个步骤。

## 三个尖锐问题

### 1. Verification 仍然在你身上
无人值守运行的 loop，也是在无人值守地犯错。你的工作，是交付你确认过能运行的代码。

### 2. 理解会腐烂
loop 越快地交付那些不是你亲手写的代码，真实存在的系统和你实际理解的系统之间的差距就越大。

### 3. 最舒服的姿势最危险
当你带着判断力去设计 loop 时，设计 loop 是解药。当你为了逃避思考而设计 loop 时，它就是加速剂。同一个动作，会产生相反的结果。

## 结尾

> 构建 loop。但要像一个仍然打算做 engineer 的人那样去构建它，而不是像一个只会按下"go"按钮的人。

> Cherny 的观点并不是说工作变简单了。而是杠杆点移动了。