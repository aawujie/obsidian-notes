# Cursor Subagents 使用指南

> 总结自官方文档：https://cursor.com/cn/docs/subagents
> 创建日期：2026-03-06

## 🎯 核心概念

**子代理 (Subagents)** 是专门化的 AI 助手，Cursor 的代理可以将任务委派给它们。每个子代理在自己的上下文窗口中运行，处理特定类型的工作，并将结果返回给父代理。

### 核心优势

| 优势        | 说明                        |
| --------- | ------------------------- |
| **上下文隔离** | 长调研任务不占用主对话空间，中间结果保留在子代理中 |
| **并行执行**  | 同时启动多个子代理，处理代码库不同部分       |
| **专业化能力** | 自定义提示词、工具访问权限和模型配置        |
| **可复用性**  | 定义自定义子代理，在多个项目间复用         |

---

## 🔄 子代理的工作原理

当 Agent 遇到复杂任务时，它可以自动启动一个子代理。子代理会接收一个包含所有必要上下文的提示，自主运行，并在完成后返回一条包含其结果的最终消息。

**重要**：子代理在全新的上下文中启动，无法访问先前的会话历史。

### 运行模式

| 模式 | 行为 | 适用场景 |
|------|------|----------|
| **Foreground (前台)** | 阻塞直到子代理完成，立即返回结果 | 需要立即获取输出的串行任务 |
| **Background (后台)** | 立即返回，子代理在后台独立运行 | 长时间任务或并行工作流 |

---

## 📦 内置子代理

Cursor 包含三个内置子代理，Agent 会在合适场景下自动使用，无需配置：

| 子代理         | 作用             | 为什么设计为子代理                                                           |
| ----------- | -------------- | ------------------------------------------------------------------- |
| **Explore** | 搜索并分析代码库       | 产生大量中间输出，使用更快模型并行运行多次搜索                                             |
| **Bash**    | 运行一系列 shell 命令 | <span style="color:rgb(255, 77, 77)">命令输出冗长，隔离后父代理专注决策</span>       |
| **Browser** | 通过 MCP 工具控制浏览器 | <span style="color:rgb(195, 117, 255)">过滤噪声 DOM 快照和截图，返回相关结果</span> |

### 设计原因

这三类操作的共同特点：
- 生成<span style="color:rgb(255, 77, 77)">噪声较多的中间结果</span>
- 受益于<span style="color:rgb(255, 77, 77)">专用提示词和工具</span>
- 可能<span style="color:rgb(255, 77, 77)">消耗大量上下文</span>

**解决方案**：
- 上下文隔离 → <span style="color:rgb(255, 77, 77)">父代理只接收最终摘要</span>
- 模型灵活性 → <span style="color:rgb(255, 77, 77)">explore 默认使用更快模型</span>
- 专用配置 → 针对特定任务优化
- 成本效率 → <span style="color:rgb(255, 77, 77)">高 token 开销工作隔离到合适模型</span>

---

## 🆚 子代理 vs Skills

| 适合使用子代理的场景        | 适合使用 Skill 的场景                                                          |
| ----------------- | ----------------------------------------------------------------------- |
| 需要为长时间研究任务进行上下文隔离 | <span style="color:rgb(255, 77, 77)">任务是单一用途的</span>（生成 changelog、格式化等） |
| 需要并行运行多个工作流       | 想要一个快速、可重复的操作                                                           |
| 任务在多个步骤中需要专业知识    | 任务可以一次性完成                                                               |
| 希望对工作结果进行独立验收/校验  | 不需要单独的上下文窗口                                                             |

---

## 📁 自定义子代理

### 文件位置

| 类型        | 位置                  | 适用范围                                                  |
| --------- | ------------------- | ----------------------------------------------------- |
| **项目子代理** | `.cursor/agents/`   | 仅限当前项目                                                |
|           | `.claude/agents/`   | 仅限当前项目 (Claude 兼容)                                    |
|           | `.codex/agents/`    | 仅限当前项目 (Codex 兼容)                                     |
| **用户子代理** | `~/.cursor/agents/` | <span style="color:rgb(255, 77, 77)">当前用户的所有项目</span> |
|           | `~/.claude/agents/` | 当前用户的所有项目 (Claude 兼容)                                 |
|           | `~/.codex/agents/`  | 当前用户的所有项目 (Codex 兼容)                                  |

**优先级**：项目子代理 > 用户子代理；`.cursor/` > `.claude/` > `.codex/`

### 文件格式

每个子代理都是带有 YAML 头信息的 Markdown 文件：

```markdown
---
name: security-auditor
description: Security specialist. Use when implementing auth, payments, or handling sensitive data.
model: inherit
readonly: false
background: false
---

You are a security expert auditing code for vulnerabilities.

When invoked:
1. Identify security-sensitive code paths
2. Check for common vulnerabilities (injection, XSS, auth bypass)
3. Verify secrets are not hardcoded
4. Review input validation and sanitization

Report findings by severity:
- Critical (must fix before deploy)
- High (fix soon)
- Medium (address when possible)
```

### 配置字段

| 字段 | 必填 | 描述 |
|------|------|------|
| `name` | 否 | 唯一标识符，小写字母 + 连字符，默认为文件名 |
| `description` | 否 | 何时使用此子代理，Agent 据此决定是否委派 |
| `model` | 否 | `fast`、`inherit` 或特定模型 ID，默认 `inherit` |
| `readonly` | 否 | `true` 时子代理以受限写入权限运行 |
| `background` | 否 | `true` 时子代理在后台运行，不等待完成 |

---

## 🚀 使用子代理

### 自动委派

Agent 会根据以下因素主动委派任务：
- 任务的复杂度和范围
- 自定义子代理的 description
- 当前上下文和可用工具

**技巧**：在 description 中包含 "use proactively" 或 "always use for" 可促进自动委派。

### 显式调用

使用 `/name` 语法调用指定子代理：

```text
> /verifier confirm the auth flow is complete
> /debugger investigate this error
> /security-auditor review the payment module
```

或自然语言提及：

```text
> Use the verifier subagent to confirm the auth flow is complete
> Have the debugger subagent investigate this error
```

### 并行执行

在一条消息中<span style="color:rgb(255, 77, 77)">发送多个 Task 工具调用</span>，子代理会并行运行：

```text
> Review the API changes and update the documentation in parallel
```

### 恢复子代理

继续之前的子代理对话（适用于长时任务）：

```text
> Resume agent abc123 and analyze the remaining test failures
```

<span style="color:rgb(255, 77, 77)">后台子代理会将状态记录到 `~/.cursor/subagents/`</span>。

---

## 💡 常见模式

### 1. 验证代理 (Verifier)

验证声称已完成的工作是否真正完成，解决 AI 标记任务完成但实现不完整的问题。

```markdown
---
name: verifier
description: Validates completed work. Use after tasks are marked done to confirm implementations are functional.
model: fast
---

You are a skeptical validator. Your job is to verify that work claimed as complete actually works.

When invoked:
1. Identify what was claimed to be completed
2. Check that the implementation exists and is functional
3. Run relevant tests or verification steps
4. Look for edge cases that may have been missed

Be thorough and skeptical. Report:
- What was verified and passed
- What was claimed but incomplete or broken
- Specific issues that need to be addressed

Do not accept claims at face value. Test everything.
```

**适用场景**：
- 工单标记完成前验证端到端功能
- 发现部分实现的功能
- 确保测试真正通过

### 2. Orchestrator 模式

父级 Agent 按顺序协调多个专业子代理：

1. **Planner** → 分析需求，制定技术方案
2. **Implementer** → 根据方案实现功能
3. **Verifier** → 确认实现满足需求

每次交接包含结构化输出，下一个 Agent 拥有清晰上下文。

---

## 📋 子代理示例

### 调试器 (debugger.md)

```markdown
---
name: debugger
description: Debugging specialist for errors and test failures. Use when encountering issues.
---

You are an expert debugger specializing in root cause analysis.

When invoked:
1. Capture error message and stack trace
2. Identify reproduction steps
3. Isolate the failure location
4. Implement minimal fix
5. Verify solution works

For each issue, provide:
- Root cause explanation
- Evidence supporting the diagnosis
- Specific code fix
- Testing approach

Focus on fixing the underlying issue, not symptoms.
```

### 测试运行器 (test-runner.md)

```markdown
---
name: test-runner
description: Test automation expert. Use proactively to run tests and fix failures.
---

You are a test automation expert.

When you see code changes, proactively run appropriate tests.

If tests fail:
1. Analyze the failure output
2. Identify the root cause
3. Fix the issue while preserving test intent
4. Re-run to verify

Report test results with:
- Number of tests passed/failed
- Summary of any failures
- Changes made to fix issues
```

---

## ✅ 最佳实践

### 推荐做法

- **编写专注的子代理** — 每个子代理只负责一件事，职责清晰
- **投入精力写好描述** — `description` 决定 Agent 何时委派，花时间打磨
- **保持提示简洁** — 冗长提示会削弱聚焦度，要具体直接
- **将子代理纳入版本控制** — 把 `.cursor/agents/` 提交到代码仓库
- **从 Agent 生成的代理开始** — 先让 Agent 起草初始配置，再自定义

### <span style="color:rgb(255, 77, 77)">反模式（避免）</span>

| 反模式                  | 问题                                                               | 改进               |
| -------------------- | ---------------------------------------------------------------- | ---------------- |
| **几十个通用型子代理**        | <span style="color:rgb(195, 117, 255)">Agent 不知道何时用，维护成本高</span> | 从 2-3 个聚焦明确的开始   |
| **描述含糊**             | "Use for general tasks" 无指导意义                                    | 具体说明使用场景         |
| **提示词过长**            | <span style="color:rgb(255, 77, 77)">2000+ 字让子代理更慢、难维护</span>    | 保持简洁聚焦           |
| **重复 slash command** | 单一用途任务不需要上下文隔离                                                   | 改用 slash command |

---

## ⚙️ 管理子代理

### 创建子代理

**方法 1：让 Agent 帮你创建**

```text
在 .cursor/agents/security-reviewer.md 创建一个子代理文件，
在 YAML 头部信息中包含 name 和 description。
security-reviewer 子代理应检查代码中的常见漏洞，
例如注入、XSS 和硬编码的机密信息。
```

**方法 2：手动创建**

在 `.cursor/agents/` (项目) 或 `~/.cursor/agents/` (用户) 中添加 Markdown 文件。

### 查看子代理

检查项目中的 `.cursor/agents/` 目录查看配置了哪些子代理。

---

## 💰 性能与成本

### 权衡对比

| 优点 | 代价 |
|------|------|
| 上下文隔离 | 启动开销（每个子代理需独立收集上下文） |
| 并行执行 | 更高的 Token 消耗（多个上下文同时运行） |
| 专注特定任务 | 延迟（简单任务可能比主代理更慢） |

### Token 和成本注意事项

- **子代理独立消耗 Token** — 并行运行 5 个子代理 ≈ 单个代理的 5 倍 Token
- **评估额外开销** — 快速简单任务用主代理更快
- **子代理可能更慢** — 优势在上下文隔离，不在速度

---

## ❓ 常见问题

### 内置子代理有哪些？
`explore`（代码库搜索）、`bash`（shell 命令）、`browser`（浏览器自动化）。自动处理上下文密集型操作，无需配置。

### 子代理可以启动其他子代理吗？
不支持嵌套子代理，仅单层辅助运行。

### 如何查看子代理在做什么？
后台子代理输出写入 `~/.cursor/subagents/`，父代理可读取检查进度。

### 如果子代理失败会发生什么？
子代理返回错误状态给父代理，父代理可重试、补充上下文后继续或另行处理。

### 可以在子代理中使用 MCP 工具吗？
可以，子代理继承父代理的所有工具，包括已配置服务器的 MCP 工具。

### 如何调试行为异常的子代理？
检查 description 和提示词确保指令具体明确，或显式调用子代理并给出简单任务测试。

### 为什么我的子代理使用不同的模型？
旧版按请求计费套餐未启用 Max Mode 时，子代理始终使用 Composer。请在模型选择器中启用 Max Mode。按用量计费套餐默认使用已配置模型。

---

## 📚 相关资源

- [官方文档](https://cursor.com/cn/docs/subagents)
- [Max Mode](https://cursor.com/help/ai-features/max-mode.md)
- [Skills 文档](https://cursor.com/docs/skills.md)
- [Hooks 文档](https://cursor.com/docs/hooks.md)
- [自定义 Rules](https://cursor.com/help/customization/rules.md)

---

## 🏷️ 标签

#Cursor #AI编程 #Subagents #多代理系统 #开发工具 #自动化
