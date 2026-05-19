---
title: Claude Code 创建者 Boris — Prompt 实战全指南
type: lecture-notes
created: 2026-05-20
updated: 2026-05-20
sources:
  - https://x.com/AnatoliKopadze/status/2056362875195686927
tags:
  - Claude-Code
  - prompt-engineering
  - agentic-AI
  - coding-agent
  - Anthropic
---

## 来源

Claude Code 创建者 **Boris**（Anthropic 技术团队成员）在 Anthropic 内部活动的分享，28 分钟。

推文评价：**"I've seen $300 courses that don't cover what he shows in the first 10 minutes."**

---

## 一、什么是 Claude Code

新一代 **agentic** 编程助手。区别于传统代码补全工具：

- 传统工具：逐行补全、补几行
- Claude Code：**构建整个功能、写完整文件、修复整个 bug**
- 通用终端工具——VS Code、Xcode、JetBrains、Vim、Emacs、SSH、Tmux 全覆盖

> 它不强迫你改变工作流。你用什么 IDE 都行。

### 首次启动设置

```bash
# 多行输入支持
/terminal-setup

# 主题
/theme

# GitHub App（@ClaudeCode 可被 @mention 在 issue/PR 中）
/install-github-app
```

- 自定义允许工具列表（常用命令设为 auto-approve）
- macOS 上可用语音输入：`系统设置 → 辅助功能 → 听写`，双击 Ctrl 说话即可

---

## 二、第一步：从代码库 Q&A 开始（不是写代码）

### 核心原则

**新用户、团队入职时，第一步不是让 AI 改代码，而是提问。**

> At Anthropic, onboarding used to take 2–3 weeks for technical hires. It's now 2–3 days.

### Q&A 示例

- "这个类是怎么被实例化的？哪些地方用了它？" → Claude 不是文本搜索，会深度探索
- "为什么这个函数有 15 个参数？参数名为什么这么奇怪？" → 查 Git 历史，找到引入的 commit、关联的 issue
- "查看 GitHub issue #1234" → web fetch 获取上下文

> Claude 知道怎么查 Git 历史**不是因为我们 system prompt 了它**——是模型自己够聪明，知道怎么用这些工具。

### 实战：每周 Standup 总结

```
"What did I ship this week?"
```

Claude 自动查 Git log → 按用户名过滤 → 组织成列表 → 直接复制粘贴到文档。

---

## 三、第二步：先出方案再写代码

### 常见错误

直接说 "implement this 3000-line feature" → 有时一次成功，有时出来的是完全不想要的东西。

### 正确做法

```
"Before you write code, make a plan. Run it by me. Ask for approval."
```

**不需要任何特殊模式或工具**——Claude 自动理解这句话并执行。

### 进阶：让 Claude 自我验证

给 Claude 一个可以看到自己工作结果的工具：

- 单元测试 → 跑测试 → 看结果 → 自动迭代
- Puppeteer 截图 → 看 UI → 对比 → 修正
- iOS 模拟器截图 → 同上

> Whatever your domain is — unit tests, integration tests, screenshots — give it a way to see its result and it'll iterate and get better.

### 提交和 PR 一步搞定

```
"Commit this, push, and make a PR"
```

Claude 自动：查代码 → 查 Git log → 识别 commit 格式 → 写 commit message → 创建分支 → push → 开 PR。

---

## 四、第三步：CLAUDE.md — 团队共享上下文的核心

### 文件层级

```
/CLAUDE.md            ← 项目根，自动加载每个 session
  CLAUDE.local.md     ← 个人配置，不提交到 Git
  /subdir/CLAUDE.md   ← 子目录专用，按需加载
```

### CLAUDE.md 内容

- 常用 bash 命令
- MCP 工具说明
- 架构决策记录
- 核心文件路径
- 代码风格指南

**保持简短**——太长了浪费上下文窗口。

### 嵌套目录 CLAUDE.md

放在子目录的 CLAUDE.md 在 Claude 操作该目录时**自动拉取**，不需要手动指定。

---

## 五、企业级配置

### 层级系统

| 层级 | 范围 | 示例 |
|:---|:---|:---|
| 企业策略 | 全公司 | 全局 auto-approve / block |
| 项目 | Git repo | CLAUDE.md, .mcp.json |
| 用户 | 个人 | CLAUDE.local.md |

### 企业策略文件

- **Auto-approve**：所有员工都用的测试命令 → 签入策略文件 → 自动放行
- **Block**：永远不能 fetch 的 URL → 签入策略文件 → 员工不可覆盖
- **共享 MCP**：`.mcp.json` 签入代码库 → 任何人运行 Claude Code 时提示安装

### 推荐起步方式

> Start with shared project context. You write it once and share it with everyone — network effect: someone does a little work, everyone benefits.

### 管理工具

```bash
# 查看所有已加载的 memory 文件
/memory

# 编辑指定 memory 文件
/memory edit

# 记住某件事到指定 memory 文件
# which-memory
```

---

## 六、工具集成

### Batch 工具

```bash
"Use `claude-code-cli` to do X. You can use --help to figure out how to use it."
```

如果经常用 → 放进 CLAUDE.md。

### MCP 工具

直接告诉 Claude 有某个 MCP 工具，Claude 会用。

**Anthropic 内部实例**：apps repo 中签入了 Puppeteer MCP 服务器 → 任何工程师 checkout 后自动可用 → 端到端测试 + 截图迭代。

---

## 七、快捷键速查

| 快捷键 | 功能 |
|:---|:---|
| `Shift+Tab` | 自动接受编辑模式（bash 仍需确认） |
| `#` | 让 Claude 记住某事 → 自动写入对应 memory 文件 |
| `!` | 直接执行 bash 命令（不通过 Claude） |
| `Escape` | 随时安全中断 Claude 当前操作 |
| `Escape ×2` | 跳回对话历史 |
| `Ctrl+R` | 查看 Claude 看到的完整输出 |
| `Ctrl+C` | 粘贴/拖拽图片到终端（多模态） |

> Escape doesn't corrupt the session. It's always safe. 如果 Claude 写了一个 20 行的 edit，19 行完美但 1 行不对 → Escape → 告诉它改那 1 行 → 让它重做。

---

## 八、Claude Code SDK（CLI SDK）

### 基础用法

```bash
claude -p "prompt" \
  --allowedTools "Bash(git:*)" \
  --output-format json
```

### 管道

```bash
# 管道输入
git log | claude -p "summarize recent changes"

# 从云存储读取
cat gs://bucket/log.txt | claude -p "find anomalies"

# 从 Sentry 读取
sentry-cli events list | claude -p "categorize errors"

# 管道输出 + jq 处理
claude -p "..." --output-format json | jq '.result'
```

> It's a **super intelligent UNIX utility**. We've barely scratched the surface.

### Anthropic 内部用法

- CI 流水线
- 事件响应
- GitHub Actions 自动打标签
- 各类 pipeline 自动化

---

## 九、高级用户用法

### 并行 Claude

Anthropic 内外的高级用户模式：

- **多个 Git worktree** → 同一 repo 多份 checkout → 多个 Claude 并行
- **Tmux 隧道** → 远程 SSH 会话中运行 Claude → 持续连接
- **同时运行任意数量的 Claude session**

> We're working on making this easier, but for now these are the patterns.

---

## 十、Q&A 精选

### Q: 为什么做 CLI 而不是 IDE 插件？

**两个原因：**

1. **Anthropic 内部 IDE 碎片化** — VS Code / Xcode / ZED / Vim / Emacs 都有人用，终端是最大公约数
2. **模型进步太快** — "By the end of the year, people aren't using IDEs anymore. We want to avoid over-investing in UI."

> 如果年底前没人用 IDE 了，那在 UI 上投入太多是浪费。

### Q: 构建中最难的部分？

**Bash 安全系统** — 要在"安全"和"不打断工程师心流"之间取平衡。最终方案：

- 只读命令自动放行
- 静态分析判断哪些命令组合安全
- 分级权限系统（企业级 → 项目级 → 用户级）

### Q: Claude Code 支持多模态吗？

是的，从第一天起就支持。三种方式：

- 拖拽图片到终端
- 粘贴图片路径
- 直接复制粘贴图片

> I'll take a mock, drag it in, tell it to implement it, give it a Puppeteer server so it can iterate.

### Q: 用 Claude Code 做 ML 建模吗？

Anthropic 内部 **80% 技术人员每天用 Claude Code**，包括研究者——用 notebook 工具编辑和运行 Jupyter notebook。

---

## 核心要点总结

1. **入职先 Q&A，别直接写代码** — 入职时间从周速降到天速
2. **先出 plan 再动手** — 就一句话的事，不需要工具
3. **给 Claude 自我验证的工具** — 单元测试 / 截图 / 集成测试
4. **CLAUDE.md 是团队的集体 IQ** — 写一次，全团队受益
5. **企业策略 + 共享 MCP 服务器** — 一次配置，安全与效率兼得
6. **CLI SDK 是超级 UNIX 工具** — 管道输入/输出，CI/CD 原生
7. **并行是高级玩法** — Git worktree + 多个 Claude session
8. **终端优先不是妥协** — 是因为 UI 层年底前可能就不需要了