---
title: "Claude Code 动态工作流：每个任务都可以有自己的 Harness【译】"
source: "https://x.com/MinLiBuilds/status/2062068646902689895"
author: "实践哥MinLi (@MinLiBuilds)｜原文 Thariq (@trq212, Anthropic)"
date: 2026-06-03
fetched: 2026-06-04
tags: [Claude-Code, workflow, dynamic-workflow, subagents, AI-engineering]
---

# Claude Code 动态工作流：每个任务都可以有自己的 Harness

**实践哥MinLi (@MinLiBuilds) · 2026-06-03**
**原文作者: Thariq (@trq212) · Anthropic 核心员工**
👍 78 | 🔁 13 | 🔖 142 | 👁 32,389

---

> **0.导读**
>
> **导读章节为实践哥批注。**
>
> **好文值得读，workflow 可能是自 skill 发明以来，最好的发明。是 goal 的加强版，非常值得学习的一篇文章。深入浅出描写了 workflow 的各种适用场景。**
>
> 原文作者 Thariq @trq212 是 Anthropic 核心员工，经常分享 Claude Code 技巧。
>
> **内容偏长，可以按兴趣跳读。想直观感受它能干什么，看第 1 节；想弄清为什么需要它，看第 3 到第 5 节；想直接照抄落地方案，跳到第 6 节。**
>
> 1. 示例提示词：8 个例子，先直观感受 workflow 能做什么
> 2. workflow 的原理，本质是一段脚本
> 3. 为什么需要 workflow
> 4. dynamic workflows 与 static workflows
> 5. 使用 workflow 时的实用模式：6 种可复用套路
> 6. 应用场景：迁移、研究、排序、排查、分类等九类落地场景
> 7. 何时不该使用 workflow：很费 token，常规编码不必硬上
> 8. 构建 workflow 的技巧：提示词、配合 /goal 和 /loop、token 预算、保存与分享
>
> 原文如下：

---

Claude Code 现在能即时写出属于它自己的 harness，为手头的任务量身定制。这套能力就叫 dynamic workflow：它会动态地编写编排脚本，在单个会话里运行数十到数百个并行的 subagents，并在任何结果送到你面前之前先自行检查一遍。

默认的 Claude Code harness 用来写代码很好，但研究、安全分析、agent teams、代码审查这类更专门的任务，过去需要在 Claude Code 之上搭一套定制 harness 才能达到最佳表现。

workflow 让你可以动态地创建这些定制 harness，它们可复用、可分享，能让 Claude 以比默认方式更原生的姿态去解决问题。

这篇文章我会分享自己使用 workflow 的初步体验和一些心得。要提醒的是，workflow 会消耗更多 token，更适合复杂、高价值的任务。

## 1. 示例提示词

下面这些例子展示了 workflow 能做什么。你可以直接向 Claude 提出类似的请求：

- 让多个相互竞争的理论各自尝试，复现时好时坏的 flaky tests。
- 从过往会话中挖掘反复出现的纠正。
- 在 Slack 的事故频道里定位问题根因。
- 为一份商业计划获取多个视角的批评意见。
- 对简历进行排名，并加以验证。
- 用锦标赛式的筛选，为一个 CLI 工具命名。
- 对整个代码库执行重构。
- 对照实际代码，核实博客草稿里的技术论断。

## 2. workflow 的运作方式

workflow 会执行 JavaScript 文件，文件里包含用于生成和协调 subagents 的特殊函数。JSON、Math、Array 这些标准 JavaScript 工具可以用来处理数据。workflow 可以选择 subagents 使用哪个模型，并决定它们是否在隔离的 worktree 里运行。如果运行被中断，恢复后 workflow 可以从中断处继续。

## 3. 为什么需要 workflow

默认的 harness 在单个 context window 内完成规划与执行。这对编码任务很有效，但碰到长时间运行、大规模并行、高度结构化或带对抗性质的任务就会出问题。具体会表现出三种失效模式：

- **智能体偷懒**：面对复杂的多部分任务，Claude 会过早停止，只做完一部分就宣布任务完成，比如 50 项安全审查只处理了其中 35 项。
- **自我偏好偏差**：当被要求对照 rubric 验证或评判结果时，Claude 会偏袒自己得出的结论。
- **目标漂移**：在多轮交互中保真度逐渐流失，每一次总结都会丢掉细节，包括边缘情况的需求和各种约束。

workflow 的对策，是编排一批彼此独立、各自拥有独立 context window、目标聚焦又互相隔离的 subagents。

## 4. dynamic workflows 与 static workflows

此前，用 Claude Agent SDK 或 `claude -p` 构建的 static workflows，是以通用方式协调多个 Claude Code 实例，这要求你把所有边缘情况都覆盖到。有了 Claude Opus 4.8 和 dynamic workflows，Claude 现在能写出针对具体场景量身定制的 harness。

## 5. 使用 workflow 时的实用模式

你可以直接请求一个 workflow，或在提示里用 `ultracode` 来确保 Claude Code 创建一个 workflow，从而触发它。常见的组合模式包括：

- **分类并执行**：由一个 classifier agent 判断任务类型，据此路由到不同的 agent 或行为；也可以在任务完成时确定输出的分类。
- **扇出并综合**：把任务拆成许多更小的步骤，每个步骤跑一个 agent，再综合所有结果。当大量步骤都能从干净、互不干扰的 context window 中受益时，这一模式尤其有用。综合这一步充当一个 barrier，它会等所有扇出的 agent 完成后，再合并它们的结构化输出。
- **对抗式验证**：每生成一个 agent，就再跑一个单独的 agent，以对抗的姿态对照 rubric 或判定准则来验证它的输出。
- **生成并筛选**：先就某个主题生成多个想法，再按 rubric 或验证来筛选，去重后只留下质量最高、经过检验的那些。
- **锦标赛**：让 N 个 agent 用不同方法在同一个任务上互相竞争，而不是把工作分摊下去。由成对评判的 agent 决出胜者，直到只剩一个。
- **循环至完成**：对工作量未知的任务，持续生成 agent，直到满足停止条件为止，比如不再有新发现、日志里不再有错误，而不是采用固定的遍数。

## 6. 应用场景

- **迁移与重构**：Bun 把 Zig 重写成 Rust 时就用了 workflow。把任务拆成一串串行步骤（调用点、失败的测试、模块），为每一处修复在 worktree 里生成 subagents，让 agent 做对抗式审查，然后再合并。要避开资源密集的命令，好让并行度最大化。
- **研究工作**：用"扇出并综合"模式同时探索多个方向。为每个假设生成独立的 agent，各自用自己的方式搜索和推理，再用一个综合 agent 对比分歧、归纳最一致的解释与更高层结论。这对于需要同时探索多条路径的开放性问题尤其合适。
- **安全审计**：在整个代码库里，对每项安全检查生成独立 agent 进行审查，再让验证 agent 对每个发现做验证，剔除误报。定期对无法解决的问题做聚类，推断是否有系统性的缺陷模式。
- **排名与排序**：当排序需要考虑多个因素时，用锦标赛或成对对比，让多个 agent 用一致的标准两两评判候选项。可以同时并行执行多组评判，最后汇总结果。
- **事故排查**：并行生成多个排查方向的 agent，每个 agent 沿不同的指标、日志或时间线向下深挖。有一个 classifier 判断发现是否具有"可操作性"，当 classifier 标记出一个可执行的修复建议时立即通知你。
- **代码审查**：把 PR 中每个文件（或每个关键关注点）分配给独立的 agent，对照你提供的风格指南逐项审查。综合 agent 合并建议并去重。
- **高级分类**：对每个样本生成两个 agent——一个判断类别，另一个独立对照 rubric 验证分类，二者意见不一致时引入第三个 agent 仲裁。分类结果通过后才输出结构化标签。
- **长文档写作**：先生成骨架大纲，然后对每一小节扇出 agent 分别填充，再加一个 agent 做全篇一致性审查。
- **测试生成**：对每个模块生成多个 agent，用不同测试策略分别生成测试用例，再用对抗式验证筛掉低质量用例，保持覆盖率的同时控制数量。

## 7. 何时不该使用 workflow

workflow 非常耗费 token，只适合高价值或高复杂度的工作。经验法则：

- 如果是一个直接的问题 → 直接用默认 harness
- 如果是一个复杂但能清晰分解的问题，且每个子问题都能从独立 context window 中受益 → 用 workflow

## 8. 构建 workflow 的技巧

- **提示词是关键**：尽可能具体地描述你想要的输出格式和验证标准。workflow 的强度直接取决于你给它的 rubric。
- **配合 /goal**：把 workflow 挂在一个 goal 下运行，让 Claude 可以长时间自主推进并持续保持在轨道上。
- **配合 /loop**：对于重复性任务，用 /loop 驱动 workflow 逐轮运行。
- **注意 token 预算**：关注每个 subagent 的 token 使用。用 --model 或模型选择来控制成本，简单任务不必上 Opus。
- **保存与分享**：好的 workflow 脚本可以保存下来，在不同项目和团队间复用。
- **worktree 隔离**：对需要修改文件的并行任务，启用 worktree 隔离以避免竞争冲突，workflow 最后会自动合并。

---

### 小结

这是 Claude Code dynamic workflow 最全的中文翻译。对于会用 Claude Code 的人来说，workflow 的价值不亚于之前 `/goal` 的出现——它从根本上改变了"一个 agent 干大事"的约束，用**编排取代单打独斗**。