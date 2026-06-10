---
title: "Loop Engineering (Addy Osmani 原文)"
type: reference
created: 2026-06-10
updated: 2026-06-10
sources:
  - "https://x.com/addyosmani/status/2064127981161959567"
tags:
  - agent
  - loop-engineering
  - coding-agent
  - addy-osmani
---

## 原文信息

- 作者：Addy Osmani (@addyosmani)
- 时间：2026-06-08
- 点赞：5,466 | 转发：768 | 浏览：1,022,673

> **这是 Loop Engineering 话题的源头文章。** Cell 的翻译版和 Codez 的 14 步指南均基于此文扩展。
> 相关笔记：[[Loop Engineering-14步指南]]（Codez 实操版）

---

Loop engineering is replacing yourself as the person who prompts the agent. You design the system that does it instead. A loop here can be thought of a recursive goal where you define a purpose and the AI iterates until complete. It's roughly five building blocks and Claude Code and Codex both have all five now.

I believe this may be the future of how we work with coding agents. However, its still early, I'm skeptical and you absolutely have to be careful about token costs (usage patterns can vary wildly if you are token rich or poor). You also still need some way to ensure quality doesn't drop and concerns re: slop are valid. That said, let's explore what this is all about.

## 核心观点

@steipete recently said: "You shouldn't be prompting coding agents anymore. You should be designing loops that prompt your agents."

Similarly, @bcherny, head of Claude Code at Anthropic, said: "I don't prompt Claude anymore. I have loops running that prompt Claude and figuring out what to do. My job is to write loops".

For like two years the way you got something out of a coding agent was you wrote a good prompt and shared enough context. You type a thing, you read what came back, you type the next thing. The agent is a tool and you are holding it the entire time, one turn after the other. That part is kind of over, or at least some think it's going to be.

Now you build a small system that finds the work, hands it out, checks it, writes down what is done and then decides the next thing, and you let that system poke the agents instead of you.

## 五个构建块 + Memory

### 1. Automations（自动化）
按计划触发，自己做 discovery 和 triage。Codex 的 Automations 标签页，Claude Code 的 `/loop` 和 `/goal`。

`/goal` 一直运行直到条件成立——单独的小模型检查完成状态，写代码的不是给自己打分的那个。

### 2. Worktrees
并行 agents 互不踩文件。git worktree 独立工作目录 + 独立分支 + 共享 repo 历史。两边都内置。

### 3. Skills
项目知识写一次，每次运行读取。SKILL.md 格式两边通用。没有 skill，loop 每个周期从零重新推导。

### 4. Plugins 和 Connectors
MCP 让 agent 接触真实工具——issue tracker、数据库、staging API、Slack。这是"agent 说这是修复方案"和"loop 自己开 PR、链接 ticket、CI 绿了 ping 频道"的区别。

### 5. Sub-agents
把"写的人"和"检查的人"拆开。写代码的模型给自己作业打分太友善了。常见拆分：探索 → 实现 → 验证。

### 6. Memory
> 模型每次运行之间忘记一切，所以 memory 必须存在磁盘上，不在 context 里。agent 忘记，repo 不会。

## 一个 loop 长什么样

每天早上，automation 运行。prompt 调用 triage skill，读昨天 CI failures、open issues、recent commits，把 findings 写入 markdown 或 Linear board。

对每个值得处理的 finding，开隔离 worktree，派 sub-agent draft fix，再派第二个 sub-agent 审查。connectors 开 PR、更新 ticket。处理不了的落到 triage inbox。state file 是脊柱。

> 你只设计了一次。你没有亲自 prompt 其中任何一个步骤。

## Loop 不能替你做的三件事

### 1. Verification 仍然在你身上
无人值守运行 = 无人值守犯错。你的工作是交付你确认过能运行的代码。

### 2. 理解仍然会腐烂
loop 越快交付你没写的代码，存在的东西和你的理解的差距越大。这就是 **comprehension debt（理解债）**。

### 3. 最舒服的姿势最危险
带判断力设计 loop = 解药。逃避思考用 loop = 加速剂。同一个动作，相反结果。这就是 **cognitive surrender（认知投降）**。

## 结尾

> Build the loop. Stay the engineer.
>
> 如果我不亲自 review 代码，或者完全依赖自动化 loops 修复问题，产品质量一定会下降。我很可能陷入持续下滑的螺旋。
>
> 去设置你的 loops，但别忘记直接 prompt agents 仍然有效。关键在于找到正确的平衡。
>
> 两个人可以建完全一样的 loop 但得到截然相反的结果。一个用来在深刻理解的工作上跑得更快。另一个用来逃避理解工作本身。loop 不知道区别。你知道。
>
> 这就是 loop design 比 prompt engineering 更难的原因。Cherny 的观点不是工作变简单了，是杠杆点移动了。