# Cursor Cloud Agent 最佳实践

> 总结自官方文档：https://cursor.com/cn/docs/cloud-agent/best-practices
> 创建日期：2026-03-06

## 🎯 核心原则

**把 Agent 想象成一个聪明但上下文信息有限的人类开发者。** 要让它正确完成任务，<span style="color:rgb(255, 77, 77)">最好的方式是提供足够的上下文，让它明白该做什么</span>。

---

## ✅ 1. 先完成环境配置

使用 [Cloud Agent Setup](https://cursor.com/docs/cloud-agent/setup.md) 为 Cursor 完成环境配置。

> 💡 **环境配置正确时，Cursor 的表现会更好** — 就像人类开发者一样。

---

## 🔐 2. 确保 Agent 能访问所需资源

在运行 Cloud Agent 之前，确认以下前提条件已满足：

### Secrets（机密信息）

通过控制台中的 [Secrets 选项卡](https://cursor.com/dashboard?tab=cloud-agents) 确保 Agent 能访问：
- API keys
- 数据库凭证
- 其他敏感配置

### 出口访问控制 (Egress Controls)

如果启用了 [网络访问限制](https://cursor.com/docs/cloud-agent/security-network.md)：
- 确保本地开发所需的所有 URL 都已加入白名单
- 检查 Agent 是否能访问必要的外部服务

### 本地可测试性

你的代码仓库应配置为能够在本地良好运行：
- ✅ 不依赖虚拟机 (VM) 无法访问的外部服务
- ✅ 人类开发者可在本地测试 → Agent 也能测试
- ❌ 如果对人类开发者来说本地难以测试，对 Agent 来说也会同样困难

---

## 📚 3. 使用 Skills 和 agents.md 配置 Agent

如果 Cloud Agent 在测试其更改时遇到困难，建议使用：
- [Skills](https://cursor.com/docs/skills.md)
- `agents.md` 配置文件

### 实际案例（Cursor 团队）

**agents.md 内容：**
- 列出在 mono-repo 中运行和调试最常用微服务的技巧
- 提供清晰的说明

**Skills 内容：**
- 如何测试和调试关键服务
- 深入细节：如何调试某个特定微服务
- 测试需要时如何设置第三方依赖
- 每个 skill 都有何时使用的清晰说明

---

## 🛠️ 4. 为 Agent 提供所需的工具

Agent 的能力常受限于其可用的工具。

### 建议

- ✅ 使用 **MCP (Model Context Protocol)**
- ✅ 创建 **自定义工具**
- ✅ 让 Agent 能访问与人类开发者相同的系统

---

## 🔄 5. <span style="color:rgb(255, 77, 77)">根据 Agent 调整工具</span>

为 Agent 创建其擅长使用的工具非常重要。

### 迭代流程

```
1. 创建工具
   ↓
2. 观察 Agent 实际使用情况
   ↓
3. 改进工具设计
   ↓
4. 重复步骤 2-3
```

### 实际案例（Cursor 团队）

**问题发现：**
- 模型运行自定义开发命令（如 `package.json` 中的命令）时经常漏掉参数
- Agent 被嘈杂的构建日志分散注意力（人类开发者通常会忽略这些日志）

**解决方案：**
为模型创建自定义命令行界面（CLI）工具，用于在代码库中运行微服务。

**设计要点：**
- <span style="color:rgb(255, 77, 77)">简化参数传递</span>
- <span style="color:rgb(255, 77, 77)">过滤噪声日志</span>
- <span style="color:rgb(255, 77, 77)">输出清晰、结构化的结果</span>

---

## 📋 检查清单

在部署 Cloud Agent 之前，确认以下事项：

| 检查项                        | 状态  |
| -------------------------- | --- |
| 环境已正确配置（Cloud Agent Setup） | ☐   |
| Secrets 已添加到控制台            | ☐   |
| 必要 URL 已加入网络白名单            | ☐   |
| 代码库可在本地测试                  | ☐   |
| agents.md 已编写（如需要）         | ☐   |
| Skills 已创建并配置              | ☐   |
| MCP 服务器已连接                 | ☐   |
| 自定义工具已创建并测试                | ☐   |

---

## 💡 关键洞察

### <span style="color:rgb(195, 117, 255)">1. 环境即上下文<br></span>
<span style="color:rgb(255, 77, 77)">正确的环境配置 = 更多的隐式上下文</span>。Agent 不需要猜测依赖、命令或配置。

### <span style="color:rgb(195, 117, 255)">2. 工具设计决定能力上限</span>

<span style="color:rgb(255, 77, 77)">Agent 只能做它的工具允许它做的事。</span><span style="color:rgb(195, 117, 255)">投资于工具开发 = 投资于 Agent 能力。</span>

### 3. 迭代是必须的

<span style="color:rgb(255, 77, 77)">第一次创建的工具很少是完美的。</span><span style="color:rgb(195, 117, 255)">观察 Agent 如何使用，然后改进。</span>

### 4. 减少噪声

<span style="color:rgb(255, 77, 77)">Agent 容易被过多信息分散注意力。</span><span style="color:rgb(195, 117, 255)">过滤日志、简化输出、聚焦关键信息。</span>

---

## 🔗 相关资源

- [Cloud Agent Setup](https://cursor.com/docs/cloud-agent/setup.md)
- [Skills 文档](https://cursor.com/docs/skills.md)
- [MCP 文档](https://cursor.com/docs/mcp.md)
- [网络与安全](https://cursor.com/docs/cloud-agent/security-network.md)
- [Cloud Agent 概览](https://cursor.com/docs/cloud-agent.md)

---

## 🏷️ 标签

#Cursor #AI编程 #CloudAgent #最佳实践 #开发工具 #自动化
