---
title: "The Longform Guide to Everything Claude Code"
source: "https://x.com/affaanmustafa/status/2014040193557471352"
author:
  - "[[cogsec]]"
published: 2026-01-17
created: 2026-04-02
description:
tags:
  - "clippings"
  - "translation-zh"
---

在《Claude Code 万能速查指南》里，我讲过基础搭建：技能（skills）与命令、hooks、子智能体、MCP、插件，以及构成高效 Claude Code 工作流骨架的配置模式。那篇是搭建指南与底层设施。

In "The Shorthand Guide to Everything Claude Code", I covered the foundational setup: skills and commands, hooks, subagents, MCPs, plugins, and the configuration patterns that form the backbone of an effective Claude Code workflow. Its a setup guide and the base infrastructure.

> Jan 17

本篇长文讲的是把高效会话和浪费型会话区分开的技巧。若你还没读过 [Shorthand Guide](https://x.com/affaanmustafa/status/2012378465664745795?s=20)**，**请先回去把配置搭好。下文默认你已把技能、智能体、hooks 和 MCP 配好并能正常工作。

This longform guide goes the techniques that separate productive sessions from wasteful ones. If you haven't read the [Shorthand Guide](https://x.com/affaanmustafa/status/2012378465664745795?s=20)**,** go back and set up your configs first. What follows assumes you have skills, agents, hooks, and MCPs already configured and working.

主题包括：token 经济、记忆持久化、验证模式、并行策略，以及可复用工作流带来的复利。这些是我十多月每日使用里打磨出的模式，决定你是第一小时内就被上下文腐烂折磨，还是能连续数小时保持高产。

The themes here: token economics, memory persistence, verification patterns, parallelization strategies, and the compound effects of building reusable workflows. These are the patterns I've refined over 10+ months of daily use that make the difference between being plagued by context rot within the first hour, versus maintaining productive sessions for hours.

速查与长文涉及的内容在 GitHub 这里：[everything-claude-code](https://github.com/affaan-m?tab=repositories)

Everything covered in the shorthand and longform articles are available on github here: [everything-claude-code](https://github.com/affaan-m?tab=repositories)

## Context & Memory Management

要在会话之间共享记忆，最好用技能或命令：总结并核对进度，然后写入 `.claude` 目录下的 `.tmp` 文件，并在本会话内持续追加，直到结束。第二天可用它作为上下文接着干；每个会话新建一个文件，避免把旧上下文污染到新工作里。最终会有一大堆会话日志——备份到稳妥的地方，或删掉不需要的会话记录。

For sharing memory across sessions, a skill or command that summarizes and checks in on progress then saves to a \`.tmp\` file in your \`.claude\` folder and appends to it until the end of your session is the best bet. The next day it can use that as context and pick up where you left off, create a new file for each session so you don't pollute old context into new work. Eventually you'll have a big folder of these session logs - just back it up somewhere meaningful or prune the session conversations you don't need.

Claude 会生成文件总结当前状态。你审阅后如需可要求修改，再开新对话；新对话里只需提供该文件路径。在逼近上下文上限、需要延续复杂工作时特别有用。文件里应包含：哪些做法有效（最好有可验证证据）、尝试过但无效的、尚未尝试的，以及还剩什么要做。

Claude creates a file summarizing current state. Review it, ask for edits if needed, then start fresh. For the new conversation, just provide the file path. Particularly useful when you're hitting context limits and need to continue complex work. These files should contain - what approaches worked (verifiably with evidence), which approaches that were attempted did not work, which approaches have not been attempted and what's left to do.

![Image](https://pbs.twimg.com/media/G_Jqmo5asAAc_w3?format=png&name=large)

会话存储示例 -> [https://github.com/affaan-m/everything-claude-code/tree/main/examples/sessions](https://github.com/affaan-m/everything-claude-code/tree/main/examples/sessions)

Example of session storage -> [https://github.com/affaan-m/everything-claude-code/tree/main/examples/sessions](https://github.com/affaan-m/everything-claude-code/tree/main/examples/sessions)

**有策略地清理上下文：**

**Clearing Context Strategically:**

计划已定且上下文已清（Claude Code 里计划模式现已有默认选项）后，你可以按计划执行。当积累大量与执行无关的探索型上下文时很有用。若要「策略性压缩」，关掉自动压缩；在逻辑节点手动压缩，或做一个技能替你压缩/在满足条件时提醒。

Once you have your plan set and context cleared (default option in plan mode in claude code now), you can work from the plan. This is useful when you've accumulated a lot of exploration context that's no longer relevant to execution. For strategic compacting, disable auto compact. Manually compact at logical intervals or create a skill that does so for you or suggests upon some defined criteria.

[Strategic Compact Skill](https://github.com/affaan-m/everything-claude-code/tree/main/skills/strategic-compact) **（直达链接）：**

[Strategic Compact Skill](https://github.com/affaan-m/everything-claude-code/tree/main/skills/strategic-compact) **(Direct Link):**

（内嵌供快速查阅）

(Embedded for quick reference)

```bash
#!/bin/bash
# Strategic Compact Suggester
# Runs on PreToolUse to suggest manual compaction at logical intervals
#
# Why manual over auto-compact:
# - Auto-compact happens at arbitrary points, often mid-task
# - Strategic compacting preserves context through logical phases
# - Compact after exploration, before execution
# - Compact after completing a milestone, before starting next

COUNTER_FILE="/tmp/claude-tool-count-$$"
THRESHOLD=${COMPACT_THRESHOLD:-50}

# Initialize or increment counter
if [ -f "$COUNTER_FILE" ]; then
  count=$(cat "$COUNTER_FILE")
  count=$((count + 1))
  echo "$count" > "$COUNTER_FILE"
else
  echo "1" > "$COUNTER_FILE"
  count=1
fi

# Suggest compact after threshold tool calls
if [ "$count" -eq "$THRESHOLD" ]; then
  echo "[StrategicCompact] $THRESHOLD tool calls reached - consider /compact if transitioning phases" >&2
fi
```

把它挂在 Edit/Write 的 PreToolUse 上——当工具调用积累到一定程度、压缩可能有帮助时，它会轻推你一下。

Hook it to PreToolUse on Edit/Write operations - it'll nudge you when you've accumulated enough context that compacting might help.

**进阶：动态注入系统提示（System Prompt）**

**Advanced: Dynamic System Prompt Injection**

我学到并在试跑的一种做法是：不要只把一切都塞进 CLAUDE.md（用户级）或 `.claude/rules/`（项目级）导致每次会话全量加载，而是用 CLI 参数按需注入上下文。

One pattern I picked up and am trial running is: instead of solely putting everything in CLAUDE.md (user scope) or \`.claude/rules/\` (project scope) which loads every session, use CLI flags to inject context dynamically.

```bash
claude --system-prompt "$(cat memory.md)"
```

这样你能更精细地控制「何时加载什么上下文」。可按当前工作为每个会话注入不同上下文。

This lets you be more surgical about what context loads when. You can inject different context per session based on what you're working on.

**相对 @ 文件引用为何重要：**

**Why this matters vs @ file references:**

当你用 `[@memory](https://x.com/@memory).md` 或把内容放在 `.claude/rules/` 时，Claude 会在对话里通过 Read 工具读取——作为工具输出进入。使用 `--system-prompt` 时，内容会在对话开始前注入真正的系统提示里。

When you use \`[@memory](https://x.com/@memory).md\` or put something in \`.claude/rules/\`, Claude reads it via the Read tool during the conversation - it comes in as tool output. When you use \`--system-prompt\`, the content gets injected into the actual system prompt before the conversation starts.

差别在于指令层级。系统提示里的内容权威高于用户消息，用户消息又高于工具结果。日常多数时候差别不大。但对严格行为规则、项目硬性约束、或你必须让 Claude 优先遵守的上下文——系统提示注入能确保权重合适。

The difference is instruction hierarchy. System prompt content has higher authority than user messages, which have higher authority than tool results. For most day-to-day work this is marginal. But for things like strict behavioral rules, project-specific constraints, or context you absolutely need Claude to prioritize - system prompt injection ensures it's weighted appropriately.

**实用配置：**

**Practical setup:**

一种可行做法是：用 `.claude/rules/` 放基线项目规则，再用 CLI alias 切换场景化上下文：

A valid way to do this is to utilize \`.claude/rules/\` for your baseline project rules, then have CLI aliases for scenario-specific context you can switch between:

```bash
# Daily development
alias claude-dev='claude --system-prompt "$(cat ~/.claude/contexts/dev.md)"'

# PR review mode
alias claude-review='claude --system-prompt "$(cat ~/.claude/contexts/review.md)"'

# Research/exploration mode
alias claude-research='claude --system-prompt "$(cat ~/.claude/contexts/research.md)"'
```

[System Prompt Context Example Files](https://github.com/affaan-m/everything-claude-code/tree/main/contexts) **（直达链接）：**

[System Prompt Context Example Files](https://github.com/affaan-m/everything-claude-code/tree/main/contexts) **(Direct Link):**

- dev.md 侧重实现
- review.md 侧重代码质量与安全
- research.md 侧重先探索再动手

- dev.md focuses on implementation
- review.md on code quality/security
- research.md on exploration before acting

再说一次，多数情况下 `.claude/rules/context1.md` 与直接把 `context1.md` 拼进系统提示差别不大。CLI 方式更快（无工具调用）、更可靠（系统级权威）、token 也略省。但这是小优化，对很多人来说额外负担大于收益。

Again, for most things the difference between using \`.claude/rules/context1.md\` and directly appending \`context1.md\` to your system prompt is marginal. The CLI approach is faster (no tool call), more reliable (system-level authority), and slightly more token efficient. But it's a minor optimization and for many its more overhead than its worth.

**进阶：记忆持久化 Hooks**

**Advanced: Memory Persistence Hooks**

还有一些多数人不知道或知道却没好好用的 hooks，能帮记忆：

There are hooks most people don't know about or do but just don't really utilize that help with memory:

```plaintext
SESSION 1                              SESSION 2
─────────                              ─────────

[Start]                                [Start]
   │                                      │
   ▼                                      ▼
┌──────────────┐                    ┌──────────────┐
│ SessionStart │ ◄─── reads ─────── │ SessionStart │◄── loads previous
│    Hook      │     nothing yet    │    Hook      │    context
└──────┬───────┘                    └──────┬───────┘
       │                                   │
       ▼                                   ▼
   [Working]                           [Working]
       │                               (informed)
       ▼                                   │
┌──────────────┐                           ▼
│  PreCompact  │──► saves state       [Continue...]
│    Hook      │    before summary
└──────┬───────┘
       │
       ▼
   [Compacted]
       │
       ▼
┌──────────────┐
│  Stop Hook   │──► persists to ──────────►
│ (session-end)│    ~/.claude/sessions/
└──────────────┘
```

- **PreCompact Hook：** 在上下文压缩前，把重要状态写入文件
- **SessionComplete Hook：** 会话结束时，把学到的东西持久化到文件
- **SessionStart Hook：** 新会话开始时，自动加载上一段上下文

- **PreCompact Hook:** Before context compaction happens, save important state to a file
- **SessionComplete Hook:** On session end, persist learnings to a file
- **SessionStart Hook:** On new session, load previous context automatically

[Memory Persistant Hooks](https://github.com/affaan-m/everything-claude-code/tree/main/hooks/memory-persistence/) **（直达链接）：**

[Memory Persistant Hooks](https://github.com/affaan-m/everything-claude-code/tree/main/hooks/memory-persistence/) **(Direct Link):**

（内嵌供快速查阅）

(Embedded for quick reference)

```json
{
  "hooks": {
    "PreCompact": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "~/.claude/hooks/memory-persistence/pre-compact.sh"
      }]
    }],
    "SessionStart": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "~/.claude/hooks/memory-persistence/session-start.sh"
      }]
    }],
    "Stop": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "~/.claude/hooks/memory-persistence/session-end.sh"
      }]
    }]
  }
}
```

它们的作用：

What these do:

- [pre-compact.sh](https://pre-compact.sh/)**：** 记录压缩事件，用压缩时间戳更新活跃会话文件
- [session-start.sh](https://session-start.sh/)**：** 检查最近会话文件（7 天内），提示可用上下文与已学技能
- [session-end.sh](https://session-end.sh/)**：** 按模板创建/更新当日会话文件，记录起止时间

- [pre-compact.sh](https://pre-compact.sh/)**:** Logs compaction events, updates active session file with compaction timestamp
- [session-start.sh](https://session-start.sh/)**:** Checks for recent session files (last 7 days), notifies of available context and learned skills
- [session-end.sh](https://session-end.sh/)**:** Creates/updates daily session file with template, tracks start/end times

串起来可在会话间连续记忆而无需手操。这建立在第一篇里的 hook 类型（PreToolUse、PostToolUse、Stop）之上，但针对会话生命周期。

Chain these together for continuous memory across sessions without manual intervention. This builds on the hook types from Article 1 (PreToolUse, PostToolUse, Stop) but targets the session lifecycle specifically.

## Continuous Learning / Memory

我们讲过以更新 codemap 等形式做连续记忆更新，这也适用于其他事，例如从错误中学习。若你不得不重复同一提示多次，而 Claude 反复踩同一坑或给你听过的答案，就适用于你。

We talked about continuous memory updating in the form of updating codemaps, but this applies to other things too such as learning from mistakes. If you've had to repeat a prompt multiple times and Claude ran into the same problem or gave you a response you've heard before this is applicable to you.

多半你需要第二条提示来「纠偏」、校准 Claude 的指南针。任何类似场景都适用——这些模式必须追加进 skills。

Most likely you needed to fire a second prompt to "resteer" and calibrate Claude's compass. This is applicable to any such scenario - those patterns must be appended to skills.

现在你可以直接让 Claude「记住」或写进 rules，也可以做一个专干这件事的技能。

Now you can automatically do this by simply telling Claude to remember it or add it to your rules, or you can have a skill that does exactly that.

**问题：** 浪费 token、浪费上下文、浪费时间；皮质醇飙升，你恼火地对 Claude 吼别再做你上会话已经禁止的事。

**The Problem:** Wasted tokens, wasted context, wasted time, your cortisol spikes as you frustratingly yell at claude to not do something that you already had told it not to do in a previous session.

**解法：** 当 Claude Code 发现非琐碎的东西——调试技巧、变通方案、某项目特有模式——就把这些知识存成新 skill。下次遇到类似问题，skill 会自动加载。

**The Solution:** When Claude Code discovers something that isn't trivial- a debugging technique, a workaround, some project-specific pattern - it saves that knowledge as a new skill. Next time a similar problem comes up, the skill gets loaded automatically.

[Continuous Learning Skill (Direct Link):](https://github.com/affaan-m/everything-claude-code/tree/main/skills/continuous-learning)

为何我用 **Stop hook** 而不是 **UserPromptSubmit**？**UserPromptSubmit** 在你每条消息都会跑——开销大、每条提示都增加延迟，对这事 frankly 过度。Stop 在会话结束只跑一次——轻量、会话中不拖慢你，且评估的是完整会话而非碎片。

Why did I use a **Stop hook** instead of **UserPromptSubmit**? **UserPromptSubmit** runs on every single message you send - that's a lot of overhead, adds latency to every prompt, and frankly overkill for this purpose. Stop runs once at session end - lightweight, doesn't slow you down during the session, and evaluates the complete session rather than piecemeal.

**安装：**

**Installation:**

```bash
# Clone to skills folder
git clone https://github.com/affaan-m/everything-claude-code.git ~/.claude/skills/everything-claude-code

# Or just grab the continuous-learning skill
mkdir -p ~/.claude/skills/continuous-learning
curl -sL https://raw.githubusercontent.com/affaan-m/everything-claude-code/main/skills/continuous-learning/evaluate-session.sh > ~/.claude/skills/continuous-learning/evaluate-session.sh
chmod +x ~/.claude/skills/continuous-learning/evaluate-session.sh
```

[Hook Configuration](https://github.com/affaan-m/everything-claude-code/tree/main/hooks) **（直达链接）：**

[Hook Configuration](https://github.com/affaan-m/everything-claude-code/tree/main/hooks) **(Direct Link):**

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/skills/continuous-learning/evaluate-session.sh"
          }
        ]
      }
    ]
  }
}
```

这用 **Stop hook** 在会话结束时运行评估脚本，审视整场对话里值得抽取的知识。技能也可通过语义匹配激活，但 hook 能保证稳定触发评估。（原文此处写 “on every prompt”，与 Stop hook 语义不符，译文按 Stop 的实际行为表述。）

This uses the **Stop hook** to run an activator script on every prompt, evaluating the session for knowledge worth extracting. The skill can also activate via semantic matching, but the hook ensures consistent evaluation.

**Stop hook** 在会话结束时触发——脚本分析会话中值得固化的模式（错误解决、调试技巧、变通、项目特有模式等），并存为 `~/.claude/skills/learned/` 下可复用的 skills。

The **Stop hook** triggers when your session ends - the script analyzes the session for patterns worth extracting (error resolutions, debugging techniques, workarounds, project-specific patterns etc.) and saves them as reusable skills in \`~/.claude/skills/learned/\`.

**用 `/learn` 手动抽取：**

**Manual Extraction with /learn:**

不必等到会话结束。仓库还提供 `/learn` 命令，可在会话中途刚解决非琐碎问题时运行。它会提示你当场抽取模式、起草 skill 文件，保存前征求确认。见 [此处](https://github.com/affaan-m/everything-claude-code/tree/main/commands/learn.md)。

You don't have to wait for session end. The repo also includes a \`/learn\` command you can run mid-session when you've just solved something non-trivial. It prompts you to extract the pattern right then, drafts a skill file, and asks for confirmation before saving. See [here](https://github.com/affaan-m/everything-claude-code/tree/main/commands/learn.md).

**会话日志模式：**

**Session Log Pattern:**

该技能期望会话日志在 `.tmp` 文件里。模式为：`~/.claude/sessions/YYYY-MM-DD-topic.tmp`——每会话一个文件，含当前状态、已完成项、阻塞、关键决策与下一会话上下文。示例见仓库 [examples/sessions/](https://github.com/affaan-m/everything-claude-code/tree/main/examples/sessions)。

The skill expects session logs in \`.tmp\` files. The pattern is: \`~/.claude/sessions/YYYY-MM-DD-topic.tmp\` - one file per session with current state, completed items, blockers, key decisions, and context for next session. Example session files are in the repo at [examples/sessions/](https://github.com/affaan-m/everything-claude-code/tree/main/examples/sessions).

**其他自改进记忆模式：**

**Other Self-Improving Memory Patterns:**

[@RLanceMartin](https://x.com/@RLanceMartin) 的一种做法是对会话日志做反思，提炼用户偏好——实质是建一本「什么管用、什么不管用」的日记。每会话结束后，反思智能体抽取哪些顺利、哪些失败、你做了哪些纠正；这些学习更新记忆文件，在后续会话加载。

One approach from [@RLanceMartin](https://x.com/@RLanceMartin) involves reflecting over session logs to distill user preferences - essentially building a "diary" of what works and what doesn't. After each session, a reflection agent extracts what went well, what failed, what corrections you made. These learnings update a memory file that loads in subsequent sessions.

[@alexhillman](https://x.com/@alexhillman) 的另一种做法是每 15 分钟主动建议改进，而非等你察觉模式。智能体回顾近期交互、提议记忆更新，你批准或拒绝；久而久之从你批准模式中学习。

Another approach from [@alexhillman](https://x.com/@alexhillman) has the system proactively suggest improvements every 15 minutes rather than waiting for you to notice patterns. The agent reviews recent interactions, proposes memory updates, you approve or reject. Over time it learns from your approval patterns.

## Token Optimization

很多对价格敏感或常撞限额的重度用户问过我。谈 token 优化时，可以玩几招。

I've gotten a lot of questions from price-elastic consumers, or those who run into limit issues frequently as power users. When it comes to token optimization there's a few tricks you can do.

**首要策略：子智能体架构**

**Primary Strategy: Subagent Architecture**

核心在于优化所用工具与子智能体架构：把任务交给「足够便宜且够用」的模型，减少浪费。你可以边试边调；摸清之后，再决定哪些给 Haiku、哪些给 Sonnet、哪些给 Opus。

Primarily in optimizing the tools you use and subagent architecture designed to delegate the cheapest possible model that is sufficient for the task to reduce waste. You have a few options here - you could try trial and error and adapt as you go. Once you learn what is what, you can delegate to Haiku versus what you can delegate to Sonnet versus what you can delegate to Opus.

**基准测试路径（更重）：**

**Benchmarking Approach (More Involved):**

更费事的一种做法是：让 Claude 搭一套 benchmark——仓库里目标与任务清晰、计划清晰。每个 git worktree 里所有子智能体固定同一模型。任务完成时记录日志——最好同时在 plan 与 tasks 里。每个子智能体至少要实际用一次。

Another way that's a little more involved is that you can get Claude to set up a benchmark where you have a repo with well-defined goals and tasks and a well-defined plan. In each git worktree, have all subagents be of one model. Log as tasks are completed - ideally in your plan and in your tasks. You will have to use each subagent at least once.

完整跑完一轮且 Claude 计划里任务已勾掉后，停下来审计进度。可对 diff、在各 worktree 间统一的单测/集成/E2E 测试对比。这样会得到基于通过/失败案例数的数值基准。若全过，需加更多边界用例或提高测试复杂度。值不值得因人而异。

Once you've completed a full pass and tasks have been checked off your Claude plan, stop and audit the progress. You can do this by comparing diffs, creating unit and integration and E2E tests that are uniform across all worktrees. That will give you a numerical benchmark based on cases passed versus cases failed. If everything passes on all, you'll need to add more test edge cases or increase the complexity of the tests. This may or may not be worth it, depending on how much this really even matters to you.

**模型选择速查：**

**Model Selection Quick Reference:**

![Image](https://pbs.twimg.com/media/G_KO-ICaoAAyNtt?format=jpg&name=large)

常见任务下子智能体的假设配置与选型理由

Hypothetical setup of subagents on various common tasks and reasoning behind the choices

90% 写代码任务默认 Sonnet。首次尝试失败、跨 5+ 文件、架构决策或安全关键代码时升到 Opus。任务重复、指令极清晰、或多智能体里当「工人」时降到 Haiku。坦白说 Sonnet 4.5 现价每百万 input $3、output $15，相对 Opus 省约 66.7%——绝对数字不错，但对多数人相对意义不大。Haiku + Opus 组合最合理：Haiku 对 Opus 约 5 倍价差，对 Sonnet 则约 1.67 倍。

Default to Sonnet for 90% of coding tasks. Upgrade to Opus when first attempt failed, task spans 5+ files, architectural decisions, or security-critical code. Downgrade to Haiku when task is repetitive, instructions are very clear, or using as a "worker" in multi-agent setup. Frankly Sonnet 4.5 currently sits in a weird spot at $3 per million input tokens and $15 per million output tokens, the cost savings are ~ 66.7% over Opus, absolutely speaking thats a good saving but relatively its more or less insignificant to most people. Haiku and Opus combo makes the most sense as Haiku vs Opus is a 5x cost difference, compared to a 1.67x price difference against Sonnet.

![Image](https://pbs.twimg.com/media/G_KSUOmaoAE-DVF?format=jpg&name=large)

来源：[https://platform.claude.com/docs/en/about-claude/pricing](https://platform.claude.com/docs/en/about-claude/pricing)

Source: [https://platform.claude.com/docs/en/about-claude/pricing](https://platform.claude.com/docs/en/about-claude/pricing)

在智能体定义里指定 model：

In your agent definitions, specify model:

```yaml
---
name: quick-search
description: Fast file search
tools: Glob, Grep
model: haiku # Cheap and fast
---
```

**按工具优化：**

**Tool-Specific Optimizations:**

想想 Claude 最常调用的工具。例如把 grep 换成 mgrep——不少任务上相对传统 grep 或 Claude 默认的 ripgrep，平均可有效减半 token。

Think about the tools that Claude calls the most frequently. For example, replace grep with mgrep - that on various tasks has an effective token reduction on average of around half compared to traditional grep or ripgrep, which is what Claude uses by default.

![Image](https://pbs.twimg.com/media/G_KQApzX0AA0o3u?format=jpg&name=large)

来源：[https://github.com/mixedbread-ai/mgrep/blob/main/README.md](https://github.com/mixedbread-ai/mgrep/blob/main/README.md)

Source: [https://github.com/mixedbread-ai/mgrep/blob/main/README.md](https://github.com/mixedbread-ai/mgrep/blob/main/README.md)

**后台进程：**

**Background Processes:**

在适用时，若不需要 Claude 处理完整输出并实时流式阅读，可在 Claude 外跑后台进程。用 tmux 很容易做到（见 [Shorthand Guide](https://x.com/affaanmustafa/status/2012378465664745795?s=20) 与 [Tmux Commands Reference (Direct Link)](https://tmuxcheatsheet.com/)）。把终端输出拿来总结，或只复制你需要的片段。能省大量 input token——成本大头在这里：Opus 4.5 每百万 input $5、output $25。

When applicable, run background processes outside Claude if you don't need Claude to process the entire output and be streaming live directly. This can be achieved easily with tmux (see [Shorthand Guide](https://x.com/affaanmustafa/status/2012378465664745795?s=20) and [Tmux Commands Reference (Direct Link)](https://tmuxcheatsheet.com/). Take the terminal output and either summarize it or copy the part you need only. This will save on a lot of input tokens, which is where the majority of cost comes from - $5 per million tokens for Opus 4.5 and output is $25 per million tokens.

**模块化代码库的好处：**

**Modular Codebase Benefits:**

更模块化的代码库——可复用工具函数、hooks 等，主文件几百行而非几千行——既利于 token 成本，也利于一次做对，二者相关。若反复提示 Claude，尤其它在超长文件上反复读，token 烧得快。你会看到它得很多次工具调用才读完；中途还会提示文件很长要继续读。过程中 Claude 可能丢信息；停下重读也费 token。更模块化可避免。示例如下 ->

Having a more modular codebase with reusable utilities, functions, hooks and more - with main files being in the hundreds of lines instead of thousands of lines - helps both in token optimization costs and getting a task done right on the first try, which correlate. If you have to prompt Claude multiple times you're burning through tokens, especially as it reads over and over on very long files. You'll notice it has to make a lot of tool calls to finish reading the file. Intermediary, it lets you know that the file is very long and it will continue reading. Somewhere along this process, Claude may lose some information. Also, stopping and rereading costs extra tokens. This can be avoided by having a more modular codebase. Example below ->

```plaintext
root/
├── docs/                   # Global documentation
├── scripts/                # CI/CD and build scripts
├── src/
│   ├── apps/               # Entry points (API, CLI, Workers)
│   │   ├── api-gateway/    # Routes requests to modules
│   │   └── cron-jobs/      
│   │
│   ├── modules/            # The core of the system
│   │   ├── ordering/       # Self-contained "Ordering" module
│   │   │   ├── api/        # Public interface for other modules
│   │   │   ├── domain/     # Business logic & Entities (Pure)
│   │   │   ├── infrastructure/ # DB, External Clients, Repositories
│   │   │   ├── use-cases/  # Application logic (Orchestration)
│   │   │   └── tests/      # Unit and integration tests
│   │   │
│   │   ├── catalog/        # Self-contained "Catalog" module
│   │   │   ├── domain/
│   │   │   └── ...
│   │   │
│   │   └── identity/       # Self-contained "Auth/User" module
│   │       ├── domain/
│   │       └── ...
│   │
│   ├── shared/             # Code used by EVERY module
│   │   ├── kernel/         # Base classes (Entity, ValueObject)
│   │   ├── events/         # Global Event Bus definitions
│   │   └── utils/          # Deeply generic helpers
│   │
│   └── main.ts             # Application bootstrap
├── tests/                  # End-to-End (E2E) global tests
├── package.json
└── README.md
```

**精简代码库 = 更省 Token：**

**Lean Codebase = Cheaper Tokens:**

这近乎常识：代码库越精简，token 成本越低。要用技能持续识别死代码并通过技能与命令重构清理。有时我也会通读代码库，找显眼或重复处，手动拼上下文，再连同 refactor skill 与 dead code skill 喂给 Claude。

This may be obvious, but the leaner your codebase is, the cheaper your token cost will be. It's crucial to identify dead code by using skills to continuously clean the codebase by refactoring using skills and commands. Also at certain points, I like to go through and skim the whole codebase looking for things that stand out to me or look repetitive, manually piece together that context, and then feed that into Claude alongside the refactor skill and dead code skill.

**系统提示瘦身（进阶）：**

**System Prompt Slimming (Advanced):**

对成本极敏感者：Claude Code 的系统提示约 ~18k tokens（200k 上下文的 ~9%）。打补丁可压到约 ~10k，省约 7300 tokens（静态开销的 41%）。若要走这条路见 YK 的 [system-prompt-patches](https://agenticcoding.substack.com/p/32-claude-code-tips-from-basics-to)；我个人不做。

For the truly cost-conscious: Claude Code's system prompt takes ~18k tokens (~9% of 200k context). This can be reduced to ~10k tokens with patches, saving ~7,300 tokens (41% of static overhead). See YK's [system-prompt-patches](https://agenticcoding.substack.com/p/32-claude-code-tips-from-basics-to) if you want to go this route, personally I don't do this.

## Verification Loops and Evals

评估与 harness 调参——视项目而定，你会需要某种可观测性与标准化。

Evaluations and harness tuning - depending on the project, you'll want to use some form of observability and standardization.

**可观测性手段：**

**Observability Methods:**

一种做法是 tmux 进程挂钩，在技能触发时追踪思维流与输出。另一种是 PostToolUse hook，记录 Claude 具体做了什么、改动与输出的确切内容。

One way to do this is to have tmux processes hooked to tracing the thinking stream and output whenever a skill is triggered. Another way is to have a PostToolUse hook that logs what Claude specifically enacted and what the exact change and output was.

**基准工作流：**

**Benchmarking Workflow:**

对比「同一任务不用该技能」的输出差异，以衡量相对表现：

Compare that to asking for the same thing without the skill and checking the output difference to benchmark relative performance:

```plaintext
[Same Task]
                         │
            ┌────────────┴────────────┐
            ▼                         ▼
    ┌───────────────┐         ┌───────────────┐
    │  Worktree A   │         │  Worktree B   │
    │  WITH skill   │         │ WITHOUT skill │
    └───────┬───────┘         └───────┬───────┘
            │                         │
            ▼                         ▼
       [Output A]                [Output B]
            │                         │
            └──────────┬──────────────┘
                       ▼
                  [git diff]
                       │
                       ▼
              ┌────────────────┐
              │ Compare logs,  │
              │ token usage,   │
              │ output quality │
              └────────────────┘
```

分叉对话，其中一个开新 worktree 且不用该技能，最后拉 diff、看日志。这与「持续学习与记忆」一节呼应。

Fork the conversation, initiate a new worktree in one of them without the skill, pull up a diff at the end, see what was logged. This ties in with the Continuous Learning and Memory section.

**评估模式类型：**

**Eval Pattern Types:**

更进阶的 eval 与循环协议在此分叉：基于检查点的 eval 与基于 RL/任务的连续 eval。

More advanced eval and loop protocols enter here. The split is between checkpoint-based evals and RL task-based continuous evals.

```plaintext
CHECKPOINT-BASED                         CONTINUOUS
─────────────────                        ──────────

  [Task 1]                                 [Work]
     │                                        │
     ▼                                        ▼
  ┌─────────┐                            ┌─────────┐
  │Checkpoint│◄── verify                 │ Timer/  │
  │   #1    │    criteria                │ Change  │
  └────┬────┘                            └────┬────┘
       │ pass?                                │
   ┌───┴───┐                                  ▼
   │       │                            ┌──────────┐
  yes     no ──► fix ──┐                │Run Tests │
   │              │    │                │  + Lint  │
   ▼              └────┘                └────┬─────┘
  [Task 2]                                   │
     │                                  ┌────┴────┐
     ▼                                  │         │
  ┌─────────┐                          pass     fail
  │Checkpoint│                          │         │
  │   #2    │                           ▼         ▼
  └────┬────┘                        [Continue] [Stop & Fix]
       │                                          │
      ...                                    └────┘

Best for: Linear workflows              Best for: Long sessions
with clear milestones                   exploratory refactoring
```

**基于检查点的 Eval：**

**Checkpoint-Based Evals:**

- 在工作流里设明确检查点
- 每点按既定标准验证
- 验证失败则 Claude 须先修复再继续
- 适合有清晰里程碑的线性工作流

- Set explicit checkpoints in your workflow
- Verify against defined criteria at each checkpoint
- If verification fails, Claude must fix before proceeding
- Good for linear workflows with clear milestones

**连续 Eval：**

**Continuous Evals:**

- 每 N 分钟或重大变更后运行
- 全量测试、构建状态、lint
- 立即报告回归
- 先停先修再继续
- 适合长会话

- Run every N minutes or after major changes
- Full test suite, build status, lint
- Report regressions immediately
- Stop and fix before continuing
- Good for long-running sessions

取舍取决于工作性质。检查点式适合阶段清晰的特性开发；连续式适合探索性重构或维护——没有清晰里程碑时。

The deciding factor is the nature of your work. Checkpoint-based works for feature implementation with clear stages. Continuous works for exploratory refactoring or maintenance where you don't have clear milestones.

稍加介入，验证思路足以规避多数技术债。任务完成后让 Claude 跑技能与 PostToolUse hooks 做校验有帮助。持续更新 codemap 也有帮助——记录变更与 codemap 演化，成为仓库之外的单一事实源。严格规则下，Claude 也少乱建 .md、少重复文件、少留死代码荒原。

I would say with some intervention, the verification approach is enough to avoid most tech debt. Having Claude validate after it completes tasks by running the skills and PostToolUse hooks aids in that. Having the continuous codemap updating also helps because it keeps a log of changes and how the codemap evolves over time, serving as a source of truth outside just the repo itself. With strict rules, Claude will avoid creating random .md files cluttering everything as well as duplicate files for similar code and leaving a wasteland of dead code.

[Grader Types (From Anthropic - Direct Link):](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)

**基于代码的 Grader：** 字符串匹配、二元测试、静态分析、结果验证。快、便宜、客观，但对合理变体脆弱。

**Code-Based Graders:** String match, binary tests, static analysis, outcome verification. Fast, cheap, objective, but brittle to valid variations.

**基于模型的 Grader：** 量表打分、自然语言断言、成对比较。灵活、能处理细微差别，但非确定性且更贵。

**Model-Based Graders:** Rubric scoring, natural language assertions, pairwise comparison. Flexible and handles nuance, but non-deterministic and more expensive.

**人工 Grader：** 专家审阅、众包判断、抽样检查。质量金标准，但贵且慢。

**Human Graders:** SME review, crowdsourced judgment, spot-check sampling. Gold standard quality, but expensive and slow.

**关键指标：**

**Key Metrics:**

```plaintext
pass@k: At least ONE of k attempts succeeds
        ┌─────────────────────────────────────┐
        │  k=1: 70%  k=3: 91%  k=5: 97%      │
        │  Higher k = higher odds of success  │
        └─────────────────────────────────────┘

pass^k: ALL k attempts must succeed
        ┌─────────────────────────────────────┐
        │  k=1: 70%  k=3: 34%  k=5: 17%      │
        │  Higher k = harder (consistency)    │
        └─────────────────────────────────────┘
```

只要「能跑通」、任意验证反馈即可时用 **pass@k**。需要高度一致、近乎确定性（结果/质量/风格）时用 **pass^k**。

Use **pass@k** when you just need it to work and any verifying feedback is enough. Use **pass^k** when consistency is essential and you need near deterministic output consistency (in terms of results/quality/style).

**构建 Eval 路线图（同一份 Anthropic 指南）：**

**Building an Eval Roadmap (from the same Anthropic guide):**

1. 尽早开始——从真实失败里抽 20–50 个简单任务
2. 把用户报的问题转成测试用例
3. 写无歧义任务——两位专家应得出相同结论
4. 构建平衡题集——测「该发生」与「不该发生」
5. 构建稳健 harness——每次试验从干净环境开始
6. 评智能体产出，而非路径
7. 多读多轮试验的 transcript
8. 监控饱和——100% 通过意味着要加更多测试

1. Start early - 20-50 simple tasks from real failures
2. Convert user-reported failures into test cases
3. Write unambiguous tasks - two experts should reach same verdict
4. Build balanced problem sets - test when behavior should AND shouldn't occur
5. Build robust harness - each trial starts from clean environment
6. Grade what agent produced, not the path it took
7. Read transcripts from many trials
8. Monitor for saturation - 100% pass rate means add more tests

## Parallelization

多 Claude 终端里分叉对话时，务必界定分叉与原会话各自动作范围。代码改动上尽量减少重叠。选彼此正交的任务，降低相互干扰可能。

When forking conversations in a multi-Claude terminal setup, make sure the scope is well-defined for the actions in the fork and the original conversation. Aim for minimal overlap when it comes to code changes. Choose tasks that are orthogonal to each other to prevent the possibility of interference.

**我更偏好的模式：**

**My Preferred Pattern:**

个人偏好：主聊天做代码改动；分叉用来问代码库与当前状态、或调研外部服务——拉文档、在 GitHub 搜适用的开源仓库，或其他有助任务的泛研究。

Personally, I prefer the main chat to be working on code changes and the forks I do are for questions I have about the codebase and its current state, or to do research on external services such as pulling in documentation, searching GitHub for an applicable open source repo that would help in the task, or other general research that would be helpful.

**关于「随便开几个终端」：**

**On Arbitrary Terminal Counts:**

Boris [@bcherny](https://x.com/@bcherny)（Claude Code 作者）有些并行化建议我有同有异。他提过本机 5 个 Claude、上游 5 个之类。我不建议为数字而数字。多加终端与实例应出于真实必要与目的。脚本能搞定就用脚本。若能留在主会话让 Claude 在 tmux 里起实例并在另一终端流式输出，就那样做。

Boris [@bcherny](https://x.com/@bcherny) (the legend who created claude code) has some tips on parallelization that I agree and disagree with. He's suggested things like running 5 Claude instances locally and 5 upstream. I advise against setting arbitrary terminal amounts like this. The addition of a terminal and the addition of an instance should be out of true necessity and purpose. If you can take care of that task using a script, use a script. If you can stay in the main chat and get Claude to spin up an instance in tmux and stream it in a separate terminal that way, do that.

> Jan 3
> 
> 1/ I run 5 Claudes in parallel in my terminal. I number my tabs 1-5, and use system notifications to know when a Claude needs input https://code.claude.com/docs/en/terminal-config#iterm-2-system-notifications…

目标应是：用「最小可行」的并行度完成尽量多的事。

Your goal really should be: how much can you get done with the minimum viable amount of parallelization.

多数新手我甚至建议先别并行，先习惯单实例里管全局。不是让你自废武功——只是要谨慎。多数时候我总共也就四五个终端；通常两三个 Claude 实例就够应付大部分事。

For most newcomers, I'd even stay away from parallelization until you get the hang of just running a single instance and managing everything within that. I'm not advocating to handicap yourself - I'm saying just be careful. Most of the time, even I only use 4 terminals or so total. I find I'm able to do most things with just 2 or 3 instances of Claude open usually.

**扩展实例时：**

**When Scaling Instances:**

若你要开始扩展实例，且多个 Claude 在彼此重叠的代码上干活，务必用 git worktree，且每个计划要极清晰。此外，恢复会话时别搞混哪个 worktree 干啥（不止树的名字），用 `/rename <name here>` 给聊天命名。

IF you are to begin scaling your instances AND you have multiple instances of Claude working on code that overlaps with one another, it's imperative you use git worktrees and have a very well-defined plan for each. Furthermore, to not get confused or lost when resuming sessions as to which git worktree is for what (beyond the names of the trees), use \`/rename <name here>\` to name all your chats.

**并行实例用 Git Worktrees：**

**Git Worktrees for Parallel Instances:**

```bash
# Create worktrees for parallel work
git worktree add ../project-feature-a feature-a
git worktree add ../project-feature-b feature-b
git worktree add ../project-refactor refactor-branch

# Each worktree gets its own Claude instance
cd ../project-feature-a && claude
```

**好处：**

**Benefits:**

- 实例间无 git 冲突
- 各自干净工作区
- 易对比输出
- 可跨不同方法对同一任务做基准

- No git conflicts between instances
- Each has clean working directory
- Easy to compare outputs
- Can benchmark same task across different approaches

**瀑布式（Cascade）方法：**

**The Cascade Method:**

多实例时可用「瀑布」组织：

- 新任务开新标签，往右排
- 从左扫到右，从旧到新
- 保持固定方向流
- 按需查看特定任务
- 同时最多盯 3–4 个任务——再多心智负担涨得比产出快

When running multiple Claude Code instances, organize with a "cascade" pattern:

- Open new tasks in new tabs to the right
- Sweep left to right, oldest to newest
- Maintain consistent direction flow
- Check on specific tasks as needed
- Focus on at most 3-4 tasks at a time - more than that and mental overhead increases faster than productivity

## Groundwork

从零开始时，地基非常重要。这该显而易见，但代码库越大越复杂，技术债也涨。按几条规则管起来并不难。此外要为手头项目把 Claude 配好（见速查指南）。

When starting fresh, the actual foundation matters a lot. This should be obvious but as complexity and size of codebase increases, tech debt also increases. Managing it is incredibly important and not as difficult if you follow a few rules. Besides setting up your Claude effectively for the project at hand (see the shorthand guide).

**双实例启动模式：**

**The Two-Instance Kickoff Pattern:**

就我个人工作流（非必须但有用），我喜欢空仓库开两个 Claude。

For my own workflow management (not necessary but helpful), I like to start an empty repo with 2 open Claude instances.

**实例 1：脚手架智能体**

**Instance 1: Scaffolding Agent**

- 搭脚手架与地基
- 创建项目结构
- 配置（CLAUDE.md、rules、agents——速查指南里全套）
- 建立约定
- 把骨架摆好

- Going to lay down the scaffold and groundwork
- Creates project structure
- Sets up configs (CLAUDE.md, rules, agents - everything from the shorthand guide)
- Establishes conventions
- Gets the skeleton in place

**实例 2：深度调研智能体**

**Instance 2: Deep Research Agent**

- 连接各类服务、网页搜索等
- 写详细 PRD
- 画架构 mermaid 图
- 从真实文档摘录整理引用

- Connects to all your services, web search, etc.
- Creates the detailed PRD
- Creates architecture mermaid diagrams
- Compiles the references with actual clips from actual documentation

![Image](https://pbs.twimg.com/media/G_KYgQYawAA9rXk?format=jpg&name=large)

启动布局：左终端写代码，右终端提问——用 `/rename` 与 `/fork`。

Starting Setup: Left Terminal for Coding, Right Terminal for Questions - use /rename and /fork.

最小够用即可起步——比每次都 Context7、喂链接爬取或 Firecrawl MCP 更快。那些适合已经深陷某事、Claude 明显写错语法或用旧函数/端点时。

What you need minimally to start is fine - it's quicker that way over Context7 every time or feeding in links for it to scrape or using Firecrawl MCP sites. All those work when you are already knee deep in something and Claude is clearly getting syntax wrong or using dated functions or endpoints.

**llms.txt 模式：**

**llms.txt Pattern:**

若文档站支持，很多文档在页面加 `/llms.txt` 可拿到 llms.txt。示例：[https://www.helius.dev/docs/llms.txt](https://www.helius.dev/docs/llms.txt)

If available, you can find an llms.txt on many documentation references by doing \`/llms.txt\` on them once you reach their docs page. Here's an example: [https://www.helius.dev/docs/llms.txt](https://www.helius.dev/docs/llms.txt)

这给你干净、面向 LLM 的文档版本，可直接喂给 Claude。

This gives you a clean, LLM-optimized version of the documentation that you can feed directly to Claude.

**理念：建可复用模式**

**Philosophy: Build Reusable Patterns**

[@omarsar0](https://x.com/@omarsar0) 的一点我完全赞同：「早期我花时间建可复用工作流/模式。搭建枯燥，但随着模型与 agent harness 变好，复利效应巨大。」

One insight from [@omarsar0](https://x.com/@omarsar0) that I fully endorse: "Early on, I spent time building reusable workflows/patterns. Tedious to build, but this had a wild compounding effect as models and agent harnesses improved."

**值得投入：**

**What to invest in:**

- Subagents（速查指南）
- Skills（速查指南）
- Commands（速查指南）
- 规划模式
- MCP 工具（速查指南）
- 上下文工程模式

- Subagents (the shorthand guide)
- Skills (the shorthand guide)
- Commands (the shorthand guide)
- Planning patterns
- MCP tools (the shorthand guide)
- Context engineering patterns

**为何复利（**[@omarsar0](https://x.com/@omarsar0)**）：** 「最棒的是这些工作流可迁移到其他智能体如 Codex。」一旦建好，可跨模型升级沿用。投模式 > 投某模型的奇技。

**Why it compounds (**[@omarsar0](https://x.com/@omarsar0)**):** "The best part is that all these workflows are transferable to other agents like Codex." Once built, they work across model upgrades. Investment in patterns > investment in specific model tricks.

## Best Practices for Agents & Sub-Agents

速查里列过子智能体结构——planner、architect、tdd-guide、code-reviewer 等。这里讲编排与执行层。

In the shorthand guide, I listed the subagent structure - planner, architect, tdd-guide, code-reviewer, etc. In this part we focus on the orchestration and execution layer.

**子智能体上下文问题：**

**The Sub-Agent Context Problem:**

子智能体为省上下文而存在——用摘要而非倾倒一切。但编排者有子智能体缺的语义上下文；子智能体只知道字面查询，不知道请求背后的目的/推理。摘要常漏关键细节。

Sub-agents exist to save context by returning summaries instead of dumping everything. But the orchestrator has semantic context the sub-agent lacks. The sub-agent only knows the literal query, not the PURPOSE/REASONING behind the request. Summaries often miss key details.

[@PerceptualPeak](https://x.com/@PerceptualPeak) 的类比：「老板派你去开会要摘要。你回来汇报。十有八九他还有追问。你的摘要不包含他需要的全部，因为你没有他的隐含上下文。」

The analogy from [@PerceptualPeak](https://x.com/@PerceptualPeak): "Your boss sends you to a meeting and asks for a summary. You come back and give him the rundown. Nine times out of ten, he's going to have follow-up questions. Your summary won't include everything he needs because you don't have the implicit context he has."

**迭代检索模式：**

**Iterative Retrieval Pattern:**

```plaintext
┌─────────────────┐
│  ORCHESTRATOR   │
│  (has context)  │
└────────┬────────┘
         │ dispatch with query + objective
         ▼
┌─────────────────┐
│   SUB-AGENT     │
│ (lacks context) │
└────────┬────────┘
         │ returns summary
         ▼
┌─────────────────┐      ┌─────────────┐
│   EVALUATE      │─no──►│  FOLLOW-UP  │
│   Sufficient?   │      │  QUESTIONS  │
└────────┬────────┘      └──────┬──────┘
         │ yes                  │
         ▼                      │ sub-agent
    [ACCEPT]              fetches answers
                                │
         ◄──────────────────────┘
              (max 3 cycles)
```

为此让编排者：

To fix this, make the orchestrator:

- 评估每次子智能体返回
- 接受前先追问
- 子智能体回源取答案再返回
- 循环直到足够（最多 3 轮防死循环）

- Evaluate every sub-agent return
- Ask follow-up questions before accepting it
- Sub-agent goes back to source, gets answers, returns
- Loop until sufficient (max 3 cycles to prevent infinite loops)

**传递目标上下文，别只传查询。** 派发子智能体时，同时给具体查询与更大目标，帮助其在摘要里排优先级。

**Pass objective context, not just the query.** When dispatching a subagent, include both the specific query AND the broader objective. This helps the subagent prioritize what to include in its summary.

**模式：分阶段顺序编排器**

**Pattern: Orchestrator with Sequential Phases**

```markdown
Phase 1: RESEARCH (use Explore agent)

- Gather context
- Identify patterns
- Output: research-summary.md

Phase 2: PLAN (use planner agent)

- Read research-summary.md
- Create implementation plan
- Output: plan.md

Phase 3: IMPLEMENT (use tdd-guide agent)

- Read plan.md
- Write tests first
- Implement code
- Output: code changes

Phase 4: REVIEW (use code-reviewer agent)

- Review all changes
- Output: review-comments.md

Phase 5: VERIFY (use build-error-resolver if needed)

- Run tests
- Fix issues
- Output: done or loop back
```

**关键规则：**

**Key rules:**

1. 每个智能体一个清晰输入、一个清晰输出
2. 输出即下一阶段输入
3. 不跳阶段——每阶段都有价值
4. 智能体之间用 `/clear` 保持上下文新鲜
5. 中间结果存文件（别只靠记忆）

1. Each agent gets ONE clear input and produces ONE clear output
2. Outputs become inputs for next phase
3. Never skip phases - each adds value
4. Use \`/clear\` between agents to keep context fresh
5. Store intermediate outputs in files (not just memory)

**智能体抽象分层（来自** [@menhguin](https://x.com/@menhguin)**）：**

**Agent Abstraction Tierlist (from** [@menhguin](https://x.com/@menhguin)**):**

**第一层：直接增益（易用）**

**Tier 1: Direct Buffs (Easy to Use)**

- **Subagents**——防上下文腐烂与临时专精的直接增益。效用约为多智能体一半，但复杂度低得多
- **Metaprompting**——「我花 3 分钟写提示，换 20 分钟任务。」直接增益，稳假设、做理智检查
- **开头多问用户**——总体是增益，不过计划模式里你得回答问题

- **Subagents** - Direct buff for preventing context rot and ad-hoc specialization. Half as useful as multi-agent but MUCH less complexity
- **Metaprompting** - "I take 3 minutes to prompt a 20-minute task." Direct buff - improves stability and sanity-checks assumptions
- **Asking user more at the beginning** - Generally a buff, though you have to answer questions in plan mode

**第二层：高技能门槛（要用好更难）**

**Tier 2: High Skill Floor (Harder to Use Well)**

- **长时运行智能体**——要理解 15 分钟 vs 1.5 小时 vs 4 小时任务的形态与权衡。要调参，明显长试错
- **并行多智能体**——方差极大，仅极复杂或切分极好的任务有用。「若两个任务各 10 分钟，你却花任意长时间写提示或合并改动，就适得其反」
- **角色多智能体**——「模型进化太快，硬编码启发式难跟上，除非套利极高。」难测
- **Computer use 智能体**——范式很早，要驯服。「你在让模型做一年前根本不该它做的事」

- **Long-running agents** - Need to understand shape and tradeoff of 15 min task vs 1.5 hour vs 4 hour task. Takes some tweaking and is obviously very long trial-and-error
- **Parallel multi-agent** - Very high variance, only useful on highly complex OR well-segmented tasks. "If 2 tasks take 10 minutes and you spend an arbitrary amount of time prompting or god forbid, merge changes, it's counterproductive"
- **Role-based multi-agent** - "Models evolve too fast for hard-coded heuristics unless arbitrage is very high." Hard to test
- **Computer use agents** - Very early paradigm, requires wrangling. "You're getting models to do something they were definitely not even meant to do a year ago"

结论：从第一层起步。只有基础扎实且真有需求时再上第二层。

The takeaway: Start with Tier 1 patterns. Only graduate to Tier 2 when you've mastered the basics and have a genuine need.

## Tips and Tricks

**部分 MCP 可替换，能腾出上下文窗口**

**Some MCPs are Replaceable and Will Free Up Your Context Window**

做法如下。

Here's how.

对 GitHub 等版本控制、Supabase 等数据库、Vercel/Railway 等部署类 MCP——多数平台已有很强 CLI，MCP 实质只是包一层。包装好用，但有代价。

For MCPs such as version control (GitHub), databases (Supabase), deployment (Vercel, Railway) etc. - most of these platforms already have robust CLIs that the MCP is essentially just wrapping. The MCP is a nice wrapper but it comes at a cost.

要让 CLI 更像 MCP 又不真的加载 MCP（以及随之而来的上下文收缩），可把能力打包进 skills 与 commands。剥出 MCP 暴露的「好用工具」做成命令。

To have the CLI function more like an MCP without actually using the MCP (and the decreased context window that comes with it), consider bundling the functionality into skills and commands. Strip out the tools the MCP exposes that make things easy and turn those into commands.

例：别一直挂 GitHub MCP，做一个 `/gh-pr` 命令封装 `gh pr create` 和你常用选项。别让 Supabase MCP 吃上下文，改用 Supabase CLI 的技能。能力相近、便利相近，但窗口留给真干活。

Example: instead of having the GitHub MCP loaded at all times, create a \`/gh-pr\` command that wraps \`gh pr create\` with your preferred options. Instead of the Supabase MCP eating context, create skills that use the Supabase CLI directly. The functionality is the same, the convenience is similar, but your context window is freed up for actual work.

这与最近收到的一些问题相关。原文发出后几天里，Boris 与 Claude Code 团队在记忆管理与优化上进展很大，主要是 MCP **懒加载**，不再一开会话就吃满窗口。早先我会建议能转 skills 就转 MCP，用两种方式「当 MCP 用」：当时启用（不理想，要离开/恢复会话）或用 CLI 同类能力的 skills 当包装——伪 MCP。

This ties in with some of the other questions I've been getting. Over the past few days since I posted the original article, Boris and the Claude Code team has made a lot of progress in memory management and optimization, primarily with lazy loading of MCPs so that they don't eat your window from the start anymore. Previously I would've recommended converting MCPs into skills where you can, offloading the functionality to enact an MCP in one of two ways: by enabling it at that time (less ideal since you need to leave and resume session) or by having skills that use the CLI analogues to the MCP (if they exist) and having the skill be the wrapper around it - essentially having it act as a pseudo-MCP.

有**懒加载**后，上下文窗口问题大体解决。但 token 用量与成本并非同样解决。CLI + skills 仍是 token 优化手段，效果可与 MCP 相近。还可把 MCP 操作用 CLI 在上下文外跑，显著省 token，对重操作（库查询、部署）尤甚。

With **lazy loading**, the context window issue is mostly solved. But token usage and cost is not solved in the same way. The CLI + skills approach is still a token optimization method that may have results on par or near the effectiveness of using an MCP. Furthermore you can run MCP operations via CLI instead of in-context which reduces token usage significantly, especially useful for heavy MCP operations like database queries or deployments.

## VIDEO?

如你所建议，我觉得配上视频能覆盖文中这些问题与其他提问。

As you suggested I'm thinking this paired with some of the other questions warrants a video to go alongside this article which covers these things.

**用两篇文章 tactics 走通一个端到端项目：**

**Cover an END-TO-END PROJECT utilizing tactics from both articles:**

- 速查指南里的完整项目配置
- 本长文进阶技巧实操
- 实时 token 优化
- 验证循环实践
- 跨会话记忆管理
- 双实例启动模式
- git worktrees 并行工作流
- 真实工作流截图与录屏

- Full project setup with configs from the shorthand guide
- Advanced techniques from this longform guide in action
- Real-time token optimization
- Verification loops in practice
- Memory management across sessions
- The two-instance kickoff pattern
- Parallel workflows with git worktrees
- Screenshots and recordings of actual workflow

我尽量安排。

I'll see what I can do.

## References

\- \[Anthropic: Demystifying evals for AI agents\]([https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)) (Jan 2026)

\- Anthropic: "Claude Code Best Practices" (Apr 2025)

\- Fireworks AI: "Eval Driven Development with Claude Code" (Aug 2025)

\- \[YK: 32 Claude Code Tips\]([https://agenticcoding.substack.com/p/32-claude-code-tips-from-basics-to](https://agenticcoding.substack.com/p/32-claude-code-tips-from-basics-to)) (Dec 2025)

\- Addy Osmani: "My LLM coding workflow going into 2026"

\- [@PerceptualPeak](https://x.com/@PerceptualPeak): Sub-Agent Context Negotiation

\- [@menhguin](https://x.com/@menhguin): Agent Abstractions Tierlist

\- [@omarsar0](https://x.com/@omarsar0): Compound Effects Philosophy

\- \[RLanceMartin: Session Reflection Pattern\]([https://rlancemartin.github.io/2025/12/01/claude\_diary/](https://rlancemartin.github.io/2025/12/01/claude_diary/))

\- [@alexhillman](https://x.com/@alexhillman): Self-Improving Memory System
