# Cursor Automations 使用指南

> 总结自官方文档：https://cursor.com/cn/docs/cloud-agent/automations
> 创建日期：2026-03-06

## 🎯 核心概念

**Cursor Automations** 在后台运行 [云端 Agent](https://cursor.com/docs/cloud-agent.md)，可以按计划执行，或在收到来自 GitHub、Slack 等的事件时触发。

### 适用场景

- 🧹 繁琐的代码维护（如清理功能标志）
- 🔒 深入审查安全漏洞
- 🐛 在 Slack 中对缺陷进行分级处理
- 🔄 自动化代码审查和修复

---

## 🚀 快速入门

在 [cursor.com/automations/new](/automations/new) 创建新的自动化流程，或使用 [marketplace](/marketplace/automations) 中的模板。

### 创建步骤

1. **选择触发条件** — 如每小时运行一次，或 PR 打开时触发
2. **编写提示词和执行说明** — 定义 agent 应该做什么
3. **选择工具** — 如 Send to Slack、Comment on Pull Request、MCP 工具等
4. **创建并观察运行** — 启动自动化并监控执行

### 计费

Automations 创建 Cloud Agent，根据 [Cloud Agent 用量](https://cursor.com/docs/models-and-pricing.md#model-pricing) 计费。

---

## ⏰ 触发器

触发器决定何时运行自动化流程。一个自动化可有多个触发器，**任意一个触发**即运行。

> ⚠️ 对于 Scheduled 或 Slack 触发器，需选择仓库和分支（Cursor 无法从 PR 推断）。

### 定时触发器 (Scheduled)

按周期性计划运行，可从预设选项选择或输入 cron 表达式。

```
# cron 表达式示例
0 * * * *      # 每小时
0 0 * * *      # 每天午夜
0 9 * * 1-5    # 工作日早上 9 点
```

**注意**：定时触发器可能延迟运行，但不会早于指定时间。

### GitHub 触发器

| 触发事件 | 说明 |
|----------|------|
| **草稿已打开** | 创建草稿拉取请求时 |
| **拉取请求已打开** | 创建非草稿 PR，或草稿标记为可供审查时 |
| **拉取请求有新推送** | 新提交推送到现有 PR 时 |
| **拉取请求已合并** | PR 被合并时 |
| **拉取请求有评论** | 有人在 PR 上发表评论时 |
| **推送到分支** | 向特定分支推送提交时（PR 之外） |
| **CI 已完成** | GitHub Check 运行完成时 |

### Slack 触发器

需连接 [Cursor Slack 集成](https://cursor.com/docs/integrations/slack.md)，目前只能看到公开频道。

| 触发事件 | 说明 |
|----------|------|
| **频道新消息** | 消息发送到已连接的 Slack 频道时 |
| **频道已创建** | 工作区中创建新的公开 Slack 频道时 |

**消息过滤器**：不设置时仅在顶层消息触发；添加关键字或正则表达式可让线程回复也触发。

### Webhook 触发器

为自动化创建私有 HTTP 端点，发送 POST 请求即可启动运行。

**用途**：连接内部系统、CI 流水线、监控工具或自定义应用。

**获取方式**：保存自动化后生成 webhook URL 和 API 密钥。

### Linear 触发器

需连接 [Cursor Linear 集成](https://cursor.com/docs/integrations/linear.md)。

| 触发事件 | 说明 |
|----------|------|
| **Issue created** | 创建新的 issue 时 |
| **Status changed** | issue 状态变化时 |
| **End of cycle** | Linear cycle 结束时 |

### PagerDuty 触发器

在事故状态变更时运行，用于自动分级或处理事故。

| 触发事件 | 说明 |
|----------|------|
| **事故已创建** | 创建新事故时 |
| **事故已确认** | 事故被确认时 |
| **事故已解决** | 事故被解决时 |
| **任意事故事件** | 匹配所有事故事件类型 |

---

## 🛠️ 工具

Automations 包含与其他 Cloud Agent 相同的基础工具集，还可启用额外工具增强能力。

### 创建 Pull Request

允许 agent 在 GitHub 上创建新的 pull request（编写代码、创建分支、打开 PR）。

**使用时机**：自动化需要进行代码更改时。

**目标仓库**：
- GitHub 触发器 → 触发器中的仓库
- 非 GitHub 触发器 → 触发器设置中选择的仓库

### 在拉取请求中发表评论

在触发的 PR 上发表评论，支持顶层评审评论和代码行内评论。

**要求**：需要 pull request 触发器。

**批准功能**：启用后 agent 可批准、请求更改并撤销评审；否则只能发表评论。

### 请求评审者

在触发的 PR 上请求评审者。Agent 可使用 `git`、记忆和其他工具识别领域专家。

**要求**：需要 pull request 触发器。

### 发送到 Slack

向 Slack 频道发送消息，可指定频道或让 agent 动态选择。

**注意**：允许使用任意频道时，Cursor 会包含发现可用公共频道所需的只读访问权限。

**Slack 触发场景**：agent 自动在触发消息的线程中回复。

### 读取 Slack 频道

为 agent 提供对公共 Slack 频道消息的只读访问权限（列出和读取消息）。

**使用时机**：回复或发起 PR 之前需要更多上下文时。

### MCP 服务器

连接 [MCP (Model Context Protocol)](https://cursor.com/docs/mcp.md) 服务器，让 agent 使用外部工具和数据源。

> ⚠️ 只连接你信任且权限匹配的服务器。

### Memories

允许 agent 在同一自动化的多次运行中读取和写入持久化备注，构建能够记忆并随时间优化的 agent。

**默认**：启用，可在工具配置 UI 中查看和编辑。

> ⚠️ **安全注意**：Memories 在多次运行之间保留，处理不可信输入时应谨慎使用（输入可能产生误导性或恶意的 Memories）。

---

## ⚙️ 自动化设置

### 模型 (Model)

选择 Agent 使用的模型，与云端 Agent 保持一致，针对自主运行场景优化。创建时 Cursor 会自动选择默认模型。

### 环境 (Environment)

从 [Cloud Agents 仪表盘](https://cursor.com/dashboard?tab=cloud-agents) 和 [Cloud Agent 设置](https://cursor.com/docs/cloud-agent/setup.md) 继承环境配置。

| 设置 | 说明 |
|------|------|
| **启用** | Agent 运行前先安装依赖，适用于需要构建、测试或执行代码的任务 |
| **禁用** | Agent 跳过依赖安装，适用于只需读取或审查代码的场景 |

在 Cloud Agents 仪表盘中配置环境设置和密钥，自动化对所选仓库使用相同设置。

### 权限 (Permissions)

| 权限级别 | 说明 |
|----------|------|
| **私有** | 只有你可以管理，团队管理员可查看并禁用 |
| **团队可见** | 只有你可以管理，团队成员可查看，团队管理员可禁用 |
| **团队拥有** | 团队成员可查看，只有团队管理员可管理（需团队管理员权限创建） |

### 身份 (Identity)

自动化在外部服务上执行操作时使用的身份：

| 操作 | 身份 |
|------|------|
| GitHub 评论、审核批准、评审请求 | `cursor` |
| 团队级自动化打开 PR | `cursor` |
| 私有自动化打开 PR | 你的 GitHub 账号 |
| Slack 消息 | Cursor 机器人 |

---

## 📝 编写提示词

提示词定义 agent 应该做什么，编写方式与 cloud agent 运行说明相同。

### 最佳实践

- ✅ **明确说明** — agent 应该检查、修改或生成什么
- ✅ **参考已启用的 Actions** — 可 @ 提及工具或直接提到名称
- ✅ **包含决策规则** — 不同情况下该怎么做
- ✅ **设定质量标准** — 何时创建 PR、发表评论或不执行任何操作
- ✅ **说明期望输出格式** — 结构化输出便于后续处理

### 示例结构

```markdown
你是一个代码审查专家。

当触发时：
1. 检查 PR 中的代码变更
2. 识别潜在的安全问题（注入、XSS、认证绕过）
3. 检查是否有硬编码的密钥
4. 验证输入验证和清理

如果发现问题：
- 在相关代码行发表评论
- 按严重程度标注（Critical/High/Medium）

如果没有问题：
- 发表评论表示批准
```

---

## 💡 使用场景示例

### 1. 自动清理功能标志

**触发器**：定时（每周日凌晨）
**工具**：创建 Pull Request
**提示词**：扫描代码库中已过期或未使用的功能标志，创建清理 PR。

### 2. 安全漏洞审查

**触发器**：拉取请求已打开
**工具**：在 PR 中发表评论、MCP 服务器（安全扫描工具）
**提示词**：审查新 PR 的安全问题，在代码行内评论发现的问题。

### 3. Slack Bug 分级

**触发器**：Slack 频道新消息（含关键字 "bug" 或 "error"）
**工具**：读取 Slack 频道、发送到 Slack、创建 Issue（Linear）
**提示词**：分析 Slack 中报告的 bug，收集上下文，创建 Linear issue 并回复频道。

### 4. CI 失败自动修复

**触发器**：CI 已完成（状态：失败）
**工具**：创建 Pull Request、读取日志
**提示词**：分析 CI 失败原因，尝试自动修复，创建修复 PR。

### 5. 事故自动响应

**触发器**：PagerDuty 事故已创建
**工具**：MCP 服务器、发送到 Slack
**提示词**：接收事故通知，收集相关日志，在 Slack 频道中发布事故摘要。

---

## 🔗 相关资源

- [Cloud Agent 概览](https://cursor.com/docs/cloud-agent.md)
- [Cloud Agent 设置](https://cursor.com/docs/cloud-agent/setup.md)
- [Cloud Agent 定价](https://cursor.com/docs/models-and-pricing.md#model-pricing)
- [GitHub 集成](https://cursor.com/docs/integrations/github.md)
- [Slack 集成](https://cursor.com/docs/integrations/slack.md)
- [Linear 集成](https://cursor.com/docs/integrations/linear.md)
- [MCP 文档](https://cursor.com/docs/mcp.md)

---

## 🏷️ 标签

#Cursor #AI 编程 #Automations #自动化 #CloudAgent #CI/CD #DevOps
