---
title: "The Shorthand Guide to Everything Claude Code"
source: "https://x.com/affaanmustafa/status/2012378465664745795"
author:
  - "[[cogsec]]"
published: 2025-09-16
created: 2026-04-02
description:
tags:
  - "clippings"
  - "translation-zh"
---

这是我经过约 10 个月每日使用后的完整配置：skills、hooks、子智能体、MCP、插件，以及真正管用的部分。

Here's my complete setup after 10 months of daily use: skills, hooks, subagents, MCPs, plugins, and what actually works.

从二月实验性推出起我就是重度 Claude Code 用户，并与 [@DRodriguezFX](https://x.com/@DRodriguezFX) 完全用 Claude Code 做了 [Zenith](https://zenith.chat/)，拿下 Anthropic x Forum Ventures 黑客松。

Been an avid Claude Code user since the experimental rollout in Feb, and won the Anthropic x Forum Ventures hackathon with [Zenith](https://zenith.chat/) alongside [@DRodriguezFX](https://x.com/@DRodriguezFX) completely using Claude Code.

> Sep 16, 2025
> 
> took the W at the @AnthropicAI x @forumventures hackathon in NYC thanks for hosting guys was a great event (and for the 15k in Anthropic Credits) @DRodriguezFX and I built PMFProbe to take founders from 0 -> 1, validate your idea at the pre MVP stage more to come soon

## Skills and Commands

Skills 像 rules，但限定在特定范围与工作流里；需要执行某条工作流时，它们就是提示词的简写。

Skills operate like rules, constricted to certain scopes and workflows. They're shorthand to prompts when you need to execute a particular workflow.

用 Opus 4.5 写了一长段代码后想清死代码和散落的 .md？跑 **/refactor-clean**。要测试？** /tdd**、**/e2e**、**/test-coverage**。Skills 与 commands 可以在一条提示里链式使用。

After a long session of coding with Opus 4.5, you want to clean out dead code and loose .md files?

Run **/refactor-clean**. Need testing? **/tdd**, **/e2e**, **/test-coverage**. Skills and commands can be chained together in a single prompt

![Image](https://pbs.twimg.com/media/G-0-_fZagAA9Kqk?format=jpg&name=large)

把命令链在一起

chaining commands together

我可以做一个在检查点更新 codemap 的技能——让 Claude 快速浏览代码库，少烧探索用的上下文。

I can make a skill that updates codemaps at checkpoints - a way for Claude to quickly navigate your codebase without burning context on exploration.

**~/.claude/skills/codemap-updater.md**

Commands 是通过斜杠执行的 skill；与 skills 重叠但存放位置不同：

Commands are skills executed via slash commands. They overlap but are stored differently:

- **Skills：** ~/.claude/skills —— 更宽泛的工作流定义
- **Commands：** ~/.claude/commands —— 可快速执行的提示

- **Skills:** ~/.claude/skills - broader workflow definitions
- **Commands:** ~/.claude/commands - quick executable prompts

```bash
# Example skill structure
~/.claude/skills/
  pmx-guidelines.md      # Project-specific patterns
  coding-standards.md    # Language best practices
  tdd-workflow/          # Multi-file skill with README.md
  security-review/       # Checklist-based skill
```

## Hooks

Hooks 是基于触发的自动化，在特定事件时触发。与 skills 不同，它们绑定在工具调用与生命周期事件上。

Hooks are trigger-based automations that fire on specific events. Unlike skills, they're constricted to tool calls and lifecycle events.

**Hook 类型**

**Hook Types**

1. **PreToolUse** —— 工具执行前（校验、提醒）
2. **PostToolUse** —— 工具结束后（格式化、反馈环）
3. **UserPromptSubmit** —— 你发送消息时
4. **Stop** —— Claude 结束回复时
5. **PreCompact** —— 上下文压缩前
6. **Notification** —— 权限请求

1. **PreToolUse** - Before a tool executes (validation, reminders)
2. **PostToolUse** - After a tool finishes (formatting, feedback loops)
3. **UserPromptSubmit** - When you send a message
4. **Stop** - When Claude finishes responding
5. **PreCompact** - Before context compaction
6. **Notification** - Permission requests

**示例：长耗时命令前的 tmux 提醒**

**Example: tmux reminder before long-running commands**

```json
{
  "PreToolUse": [
    {
      "matcher": "tool == \"Bash\" && tool_input.command matches \"(npm|pnpm|yarn|cargo|pytest)\"",
      "hooks": [
        {
          "type": "command",
          "command": "if [ -z \"$TMUX\" ]; then echo '[Hook] Consider tmux for session persistence' >&2; fi"
        }
      ]
    }
  ]
}
```

![Image](https://pbs.twimg.com/media/G-1Gwvab0AM7Xr9?format=png&name=large)

在跑 PostToolUse hook 时 Claude Code 里你会看到的反馈示例

Example of what feedback you get in Claude Code, while running a PostToolUse hook

**专业提示：** 用 `hookify` 插件对话式生成 hooks，不必手写 JSON。运行 **/hookify** 并描述你想要的。

**Pro tip:** Use the \`hookify\` plugin to create hooks conversationally instead of writing JSON manually. Run **/hookify** and describe what you want.

## Subagents

子智能体是编排器（主 Claude）可委派任务、且范围受限的进程；可在后台或前台跑，给主智能体腾出上下文。

Subagents are processes your orchestrator (main Claude) can delegate tasks to with limited scopes. They can run in background or foreground, freeing up context for the main agent.

子智能体与 skills 很搭——能执行你 skills 子集的子智能体可被委派任务并自主用那些技能。也可用特定工具权限做沙箱。

Subagents work nicely with skills - a subagent capable of executing a subset of your skills can be delegated tasks and use those skills autonomously. They can also be sandboxed with specific tool permissions.

```bash
# Example subagent structure
~/.claude/agents/
  planner.md           # Feature implementation planning
  architect.md         # System design decisions
  tdd-guide.md         # Test-driven development
  code-reviewer.md     # Quality/security review
  security-reviewer.md # Vulnerability analysis
  build-error-resolver.md
  e2e-runner.md
  refactor-cleaner.md
```

按子智能体分别配置允许的工具、MCP 与权限，做好范围隔离。

Configure allowed tools, MCPs, and permissions per subagent for proper scoping.

## Rules and Memory

`.rules` 文件夹放 `.md`，写 Claude **应始终遵守** 的最佳实践。两种做法：

Your \`.rules\` folder holds \`.md\` files with best practices Claude should ALWAYS follow. Two approaches:

1. **单一 CLAUDE.md** —— 一个文件装全部（用户级或项目级）
2. **Rules 文件夹** —— 按主题拆成多个 `.md`

1. **Single CLAUDE.md** - Everything in one file (user or project level)
2. **Rules folder -** Modular \`.md\` files grouped by concern

```bash
~/.claude/rules/
  security.md      # No hardcoded secrets, validate inputs
  coding-style.md  # Immutability, file organization
  testing.md       # TDD workflow, 80% coverage
  git-workflow.md  # Commit format, PR process
  agents.md        # When to delegate to subagents
  performance.md   # Model selection, context management
```

**规则示例：**

**Example rules:**

- 代码库里不要用 emoji
- 前端避免紫色调
- 部署前务必测试
- 优先模块化，避免巨型单文件
- 不要提交 console.log

- No emojis in codebase
- Refrain from purple hues in frontend
- Always test code before deployment
- Prioritize modular code over mega-files
- Never commit console.logs

## MCPs (Model Context Protocol)

MCP 把 Claude 直接连到外部服务。不是 API 的替代品——是用提示驱动的封装，浏览信息更灵活。

MCPs connect Claude to external services directly. Not a replacement for APIs - it's a prompt-driven wrapper around them, allowing more flexibility in navigating information.

**示例：** Supabase MCP 让 Claude 拉特定数据、在上游直接跑 SQL，无需复制粘贴。数据库、部署平台等同理。

**Example**: Supabase MCP lets Claude pull specific data, run SQL directly upstream without copy-paste. Same for databases, deployment platforms, etc.

![Image](https://pbs.twimg.com/media/G-1KHqfawAA-PPK?format=jpg&name=large)

Supabase MCP 列出 public schema 里表示例

Example of the supabase mcp listing the tables within the public schema

**Chrome in Claude：** 内置插件 MCP，让 Claude 自主控制浏览器——点击、查看实际行为。

**Chrome in Claude:** is a built-in plugin MCP that lets Claude autonomously control your browser - clicking around to see how things work.

**关键：上下文窗口管理**

**CRITICAL: Context Window Management**

对 MCP 要挑剔。我把 MCP 都放在用户配置里，但**未用的全部禁用**。打开 **/plugins** 往下滚，或运行 **/mcp**。

Be picky with MCPs. I keep all MCPs in user config but **disable everything unused**. Navigate to **/plugins** and scroll down or run **/mcp**.

压缩前你有 200k 上下文，若开太多工具可能只剩约 70k。性能会明显下降。

Your 200k context window before compacting might only be 70k with too many tools enabled. Performance degrades significantly.

![Image](https://pbs.twimg.com/media/G-1K2ZJawAAQnV3?format=jpg&name=large)

用 /plugins 查看已装 MCP 及状态

using /plugins to navigate to MCPs to see which ones are currently installed and their status

**经验法则：** 配置里可以有 20–30 个 MCP，但保持 **启用少于 10 个 / 活跃工具少于 80**。

**Rule of thumb:** Have 20-30 MCPs in config, but keep under 10 enabled / under 80 tools active.

## Plugins

插件把工具打包，安装省事，不用逐项手搓。插件可以是 skill + MCP 组合，或 hooks/工具打捆。

Plugins package tools for easy installation instead of tedious manual setup. A plugin can be a skill + MCP combined, or hooks/tools bundled together.

**安装插件：**

**Installing plugins:**

```bash
# Add a marketplace
claude plugin marketplace add https://github.com/mixedbread-ai/mgrep

# Open Claude, run /plugins, find new marketplace, install from there
```

![Image](https://pbs.twimg.com/media/G-1Loo1bYAAI_tz?format=jpg&name=large)

新装的 Mixedbread-Grep 市场

displaying the newly installed Mixedbread-Grep marketplace

**LSP 插件：** 若你经常不在编辑器里跑 Claude Code 特别有用。Language Server Protocol 给 Claude 实时类型检查、跳转定义、智能补全，不必开 IDE。

**LSP Plugins:** are particularly useful if you run Claude Code outside editors frequently. Language Server Protocol gives Claude real-time type checking, go-to-definition, and intelligent completions without needing an IDE open.

```bash
# Enabled plugins example
typescript-lsp@claude-plugins-official  # TypeScript intelligence
pyright-lsp@claude-plugins-official     # Python type checking
hookify@claude-plugins-official         # Create hooks conversationally
mgrep@Mixedbread-Grep                   # Better search than ripgrep
```

与 MCP 同样提醒：留意上下文窗口。

Same warning as MCPs - watch your context window.

## Tips and Tricks

**键盘快捷键**

**Keyboard Shortcuts**

- **Ctrl+U** —— 删整行（比狂按退格快）
- **!** —— 快速 bash 命令前缀
- **@** —— 搜文件
- **/** —— 触发斜杠命令
- **Shift+Enter** —— 多行输入
- **Tab** —— 切换思考展示
- **Esc Esc** —— 中断 Claude / 恢复代码

- **Ctrl+U** - Delete entire line (faster than backspace spam)
- **!** - Quick bash command prefix
- **@** - Search for files
- **/** - Initiate slash commands
- **Shift+Enter** - Multi-line input
- **Tab** - Toggle thinking display
- **Esc Esc** - Interrupt Claude / restore code

**并行工作流**

**Parallel Workflows**

**/fork** —— 分叉对话，并行做互不重叠的任务，而不是堆一堆排队消息

**/fork** - Fork conversations to do non-overlapping tasks in parallel instead of spamming queued messages

**Git Worktrees** —— 多 Claude 改重叠代码时用，避免冲突。每个 worktree 是独立检出

**Git Worktrees** - For overlapping parallel Claudes without conflicts. Each worktree is an independent checkout

```bash
git worktree add ../feature-branch feature-branch
# Now run separate Claude instances in each worktree
```

**tmux 跑长命令：** 流式查看 Claude 跑的日志/bash 进程。

**tmux for Long-Running Commands:** Stream and watch logs/bash processes Claude runs.

<video preload="none" tabindex="-1" playsinline="" aria-label="Embedded video" poster="https://pbs.twimg.com/amplify_video_thumb/2012355175609188352/img/W8EylFWmB9IKfdTV.jpg" style="width: 100%; height: 100%; position: absolute; background-color: black; top: 0%; left: 0%; transform: rotate(0deg) scale(1.005);"><source type="video/mp4" src="blob:https://x.com/b9c6312b-6a40-4299-92bd-bc8bd1574d12"></video>

![](https://pbs.twimg.com/amplify_video_thumb/2012355175609188352/img/W8EylFWmB9IKfdTV.jpg?name=large)

让 Claude Code 起前后端，用 tmux attach 会话看日志

letting claude code spin up the frontend and backend servers and monitoring the logs by attaching to the session using tmux

```bash
tmux new -s dev
# Claude runs commands here, you can detach and reattach
tmux attach -t dev
```

**mgrep > grep：** `mgrep` 相对 ripgrep/grep 提升明显。从插件市场安装后用 **/mgrep** skill。本地搜索与联网搜索都支持。

**mgrep > grep:** \`mgrep\` is a significant improvement from ripgrep/grep. Install via plugin marketplace, then use the **/mgrep** skill. Works with both local search and web search.

```bash
mgrep "function handleSubmit"  # Local search
mgrep --web "Next.js 15 app router changes"  # Web search
```

**其他实用命令**

**Other Useful Commands**

- **/rewind** —— 回到先前状态
- **/statusline** —— 自定义分支、上下文百分比、todos 等
- **/checkpoints** —— 文件级撤销点
- **/compact** —— 手动触发上下文压缩

- **/rewind** - Go back to a previous state
- **/statusline** - Customize with branch, context %, todos
- **/checkpoints** - File-level undo points
- **/compact** \- Manually trigger context compaction

用 GitHub Actions 给 PR 做代码审查；配置好后 Claude 可自动审 PR。

**GitHub Actions CI/CD**

Set up code review on your PRs with GitHub Actions. Claude can review PRs automatically when configured.

![Image](https://pbs.twimg.com/media/G-1U7nSbAAAK7hf?format=jpg&name=large)

Claude 批准修复 bug 的 PR

claude approving a bug fix PR

**沙箱**

**Sandboxing**

风险操作用 sandbox 模式——Claude 在受限环境跑，不影响真机。（用 `--dangerously-skip-permissions` 则相反，权限全开，不慎可毁数据。）

Use sandbox mode for risky operations - Claude runs in restricted environment without affecting your actual system. (Use --dangerously-skip-permissions - to do the opposite of this and let claude roam free, this can be destructive if not careful.)

## On Editors

不必用编辑器，但选对编辑器会明显影响 Claude Code 工作流。终端里都能用，配上好编辑器可有实时文件跟踪、快速跳转、集成执行命令。

While an editor isn't needed it can positively or negatively impact your Claude Code workflow. While Claude Code works from any terminal, pairing it with a capable editor unlocks real-time file tracking, quick navigation, and integrated command execution.

**Zed（我的首选）**

**Zed (My Preference)**

我用 [Zed](https://zed.dev/)——Rust 写的编辑器，轻、快、可定制性强。

I use [Zed](https://zed.dev/) - a Rust-based editor that's lightweight, fast, and highly customizable.

**Zed 与 Claude Code 合拍之处：**

**Why Zed works well with Claude Code:**

- **Agent 面板集成** —— Zed 的 Claude 集成可实时看 Claude 改的文件，引用文件间跳转不必离开编辑器
- **性能** —— Rust 编写，秒开，大仓库不卡
- **CMD+Shift+R 命令面板** —— 斜杠命令、调试器、工具集中可搜；不必切终端也能跑短命令
- **资源占用低** —— 重负载时不会和 Claude 抢资源
- **Vim 模式** —— 需要的话全 Vim 键位

- **Agent Panel Integration** - Zed's Claude integration lets you track file changes in real-time as Claude edits. Jump between files Claude references without leaving the editor
- **Performance** - Written in Rust, opens instantly and handles large codebases without lag
- **CMD+Shift+R Command Palette** - Quick access to all your custom slash commands, debuggers, and tools in a searchable UI. Even if you just want to run a quick command without switching to terminal
- **Minimal Resource Usage** - Won't compete with Claude for system resources during heavy operations
- **Vim Mode** - Full vim keybindings if that's your thing

![Image](https://pbs.twimg.com/media/G-1Cy8gbAAA2fE-?format=jpg&name=large)

Zed 里用 CMD+Shift+R 打开自定义命令下拉；右下角靶心为 Following 模式

Zed Editor with custom commands dropdown using CMD+Shift+R.

Following mode shown as the bullseye in the bottom right.

1. **分屏** —— 一侧终端跑 Claude Code，另一侧编辑器
2. **Ctrl + G** —— 在 Zed 里快速打开 Claude 正在编辑的文件
3. **自动保存** —— 开启 autosave，Claude 读到的文件始终最新
4. **Git 集成** —— 用编辑器 git 功能在提交前审 Claude 的改动
5. **文件监视** —— 多数编辑器会自动重载外部改动，确认已开启

1. **Split your screen** - Terminal with Claude Code on one side, editor on the other using
2. **Ctrl + G** \- quickly open the file Claude is currently working on in Zed
3. **Auto-save** - Enable autosave so Claude's file reads are always current
4. **Git integration** - Use editor's git features to review Claude's changes before committing
5. **File watchers** - Most editors auto-reload changed files, verify this is enabled

**VSCode / Cursor**

也可行，和 Claude Code 配合不错。可纯终端用 **\ide** 与编辑器自动同步、开 LSP（与插件部分略重复）；或用与编辑器 UI 更一体的扩展。

**VSCode / Cursor**

This is also a viable choice and works well with Claude Code. You can use it in either terminal format, with automatic sync with your editor using **\\ide** enabling LSP functionality (somewhat redundant with plugins now). Or you can opt for the extension which is more integrated with the Editor and has a matching UI.

![Image](https://pbs.twimg.com/media/G-1b3F_aMAApve3?format=jpg&name=large)

文档截图来源 [https://code.claude.com/docs/en/vs-code](https://code.claude.com/docs/en/vs-code)

from the docs directly at [https://code.claude.com/docs/en/vs-code](https://code.claude.com/docs/en/vs-code)

## My Setup

**插件**

**Plugins**

已安装：（我一般同时只开其中 4–5 个）

Installed: (I usually only have 4-5 of these enabled at a time)

```markdown
ralph-wiggum@claude-code-plugins       # Loop automation
frontend-design@claude-code-plugins    # UI/UX patterns
commit-commands@claude-code-plugins    # Git workflow
security-guidance@claude-code-plugins  # Security checks
pr-review-toolkit@claude-code-plugins  # PR automation
typescript-lsp@claude-plugins-official # TS intelligence
hookify@claude-plugins-official        # Hook creation
code-simplifier@claude-plugins-official
feature-dev@claude-code-plugins
explanatory-output-style@claude-code-plugins
code-review@claude-code-plugins
context7@claude-plugins-official       # Live documentation
pyright-lsp@claude-plugins-official    # Python types
mgrep@Mixedbread-Grep                  # Better search
```

**MCP 服务器**

**MCP Servers**

已配置（用户级）：

Configured (User Level):

```json
{
  "github": { "command": "npx", "args": ["-y", "@modelcontextprotocol/server-github"] },
  "firecrawl": { "command": "npx", "args": ["-y", "firecrawl-mcp"] },
  "supabase": {
    "command": "npx",
    "args": ["-y", "@supabase/mcp-server-supabase@latest", "--project-ref=YOUR_REF"]
  },
  "memory": { "command": "npx", "args": ["-y", "@modelcontextprotocol/server-memory"] },
  "sequential-thinking": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
  },
  "vercel": { "type": "http", "url": "https://mcp.vercel.com" },
  "railway": { "command": "npx", "args": ["-y", "@railway/mcp-server"] },
  "cloudflare-docs": { "type": "http", "url": "https://docs.mcp.cloudflare.com/mcp" },
  "cloudflare-workers-bindings": {
    "type": "http",
    "url": "https://bindings.mcp.cloudflare.com/mcp"
  },
  "cloudflare-workers-builds": { "type": "http", "url": "https://builds.mcp.cloudflare.com/mcp" },
  "cloudflare-observability": {
    "type": "http",
    "url": "https://observability.mcp.cloudflare.com/mcp"
  },
  "clickhouse": { "type": "http", "url": "https://mcp.clickhouse.cloud/mcp" },
  "AbletonMCP": { "command": "uvx", "args": ["ableton-mcp"] },
  "magic": { "command": "npx", "args": ["-y", "@magicuidesign/mcp@latest"] }
}
```

按项目禁用（管上下文窗口）：

Disabled per project (context window management):

```markdown
# In ~/.claude.json under projects.[path].disabledMcpServers
disabledMcpServers: [
  "playwright",
  "cloudflare-workers-builds",
  "cloudflare-workers-bindings",
  "cloudflare-observability",
  "cloudflare-docs",
  "clickhouse",
  "AbletonMCP",
  "context7",
  "magic"
]
```

关键在此：我配了 14 个 MCP，但每个项目大约只开 5–6 个，上下文才健康。

This is the key - I have 14 MCPs configured but only ~ 5-6 enabled per project. Keeps context window healthy.

**核心 Hooks**

**Key Hooks**

```json
{
  "PreToolUse": [
    // tmux reminder for long-running commands
    { "matcher": "npm|pnpm|yarn|cargo|pytest", "hooks": ["tmux reminder"] },
    // Block unnecessary .md file creation
    { "matcher": "Write && .md file", "hooks": ["block unless README/CLAUDE"] },
    // Review before git push
    { "matcher": "git push", "hooks": ["open editor for review"] }
  ],
  "PostToolUse": [
    // Auto-format JS/TS with Prettier
    { "matcher": "Edit && .ts/.tsx/.js/.jsx", "hooks": ["prettier --write"] },
    // TypeScript check after edits
    { "matcher": "Edit && .ts/.tsx", "hooks": ["tsc --noEmit"] },
    // Warn about console.log
    { "matcher": "Edit", "hooks": ["grep console.log warning"] }
  ],
  "Stop": [
    // Audit for console.logs before session ends
    { "matcher": "*", "hooks": ["check modified files for console.log"] }
  ]
}
```

**自定义状态栏**

**Custom Status Line**

显示用户、目录、带脏标记的 git 分支、剩余上下文百分比、模型、时间、todo 数量：

Shows user, directory, git branch with dirty indicator, context remaining %, model, time, and todo count:

![Image](https://pbs.twimg.com/media/G-1iYlHaEAAbS0C?format=jpg&name=large)

我 Mac 根目录下的 statusline 示例

example statusline in my Mac root directory

**Rules 结构**

**Rules Structure**

```markdown
~/.claude/rules/
  security.md      # Mandatory security checks
  coding-style.md  # Immutability, file size limits
  testing.md       # TDD, 80% coverage
  git-workflow.md  # Conventional commits
  agents.md        # Subagent delegation rules
  patterns.md      # API response formats
  performance.md   # Model selection (Haiku vs Sonnet vs Opus)
  hooks.md         # Hook documentation
```

**子智能体**

**Subagents**

```markdown
~/.claude/agents/
  planner.md           # Break down features
  architect.md         # System design
  tdd-guide.md         # Write tests first
  code-reviewer.md     # Quality review
  security-reviewer.md # Vulnerability scan
  build-error-resolver.md
  e2e-runner.md        # Playwright tests
  refactor-cleaner.md  # Dead code removal
  doc-updater.md       # Keep docs synced
```

## Key Takeaways

1. 别过度复杂——配置像微调，不是造架构
2. 上下文窗口很宝贵——关掉不用的 MCP 与插件
3. 并行执行——分叉对话、用 git worktrees
4. 重复劳动自动化——格式化、lint、提醒用 hooks
5. 子智能体要限范围——工具越少执行越聚焦

1. Don't overcomplicate - treat configuration like fine-tuning, not architecture
2. Context window is precious - disable unused MCPs and plugins
3. Parallel execution - fork conversations, use git worktrees
4. Automate the repetitive - hooks for formatting, linting, reminders
5. Scope your subagents - limited tools = focused execution

## References

\- [Plugins Reference](https://code.claude.com/docs/en/plugins-reference)

\- [Hooks Documentation](https://code.claude.com/docs/en/hooks)

\- [Checkpointing](https://code.claude.com/docs/en/checkpointing)

\- [Interactive Mode](https://code.claude.com/docs/en/interactive-mode)

\- [Memory System](https://code.claude.com/docs/en/memory)

\- \[[Subagents](https://code.claude.com/docs/en/sub-agents)\]

\- \[[MCP Overview](https://code.claude.com/docs/en/mcp-overview)\]

**说明：** 这只是细节子集。若有人感兴趣我可能再写更细的帖。

**Note**: This is a subset of detail. I might make more posts on specifics if people are interested.
