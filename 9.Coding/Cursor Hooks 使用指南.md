# Cursor Hooks 使用指南

> 总结自官方文档：https://cursor.com/cn/docs/hooks
> 创建日期：2026-03-06

## 🎯 核心概念

**Hooks** 是 Cursor 的自定义脚本系统，允许你在 agent 循环的特定阶段观察、控制和扩展行为。它们通过 stdio 使用 JSON 双向通信，作为独立子进程运行。

### 主要用途

- 编辑后运行代码格式化工具
- 添加统计/分析
- 扫描敏感信息 (PII/密钥)
- 为高风险操作设置把关 (如 SQL 写入)
- 控制子代理执行
- 会话开始时注入上下文

---

## 📍 配置层级

优先级从高到低：

| 层级 | 路径 | 说明 |
|------|------|------|
| **Enterprise** | `/Library/Application Support/Cursor/hooks.json` | 系统级配置 |
| **Team** | 云端下发 | 企业版控制台配置 |
| **Project** | `<project>/.cursor/hooks.json` | 项目级，随代码提交 |
| **User** | `~/.cursor/hooks.json` | 用户级全局配置 |

---

## ⚡ Hook 类型

### 命令驱动 (默认)

执行 Shell 脚本，从 stdin 接收 JSON，向 stdout 输出 JSON。

```json
{
  "hooks": {
    "beforeShellExecution": [
      {
        "command": "./scripts/approve-network.sh",
        "timeout": 30,
        "matcher": "curl|wget|nc"
      }
    ]
  }
}
```

**退出码行为：**
- `0` - Hook 成功，使用 JSON 输出
- `2` - **阻止该操作** (等同于 `permission: "deny"`)
- 其他 - Hook 失败，但操作继续 (默认失败放行)

### Prompt 驱动

使用 LLM 判断自然语言条件，适合不写脚本的策略。

```json
{
  "hooks": {
    "beforeShellExecution": [
      {
        "type": "prompt",
        "prompt": "Does this command look safe to execute? Only allow read-only operations.",
        "timeout": 10
      }
    ]
  }
}
```

---

## 🔄 Hook 事件参考

### Agent (Cmd+K/Agent Chat)

| Hook 事件 | 触发时机 | 用途 |
|----------|----------|------|
| `sessionStart` | 会话创建时 | 注入上下文、设置环境变量 |
| `sessionEnd` | 会话结束时 | 审计日志、清理任务 |
| `preToolUse` | 工具执行前 | 验证工具调用 |
| `postToolUse` | 工具成功后 | 审计、分析 |
| `postToolUseFailure` | 工具失败时 | 错误跟踪、恢复 |
| `subagentStart` | 子代理创建前 | 控制子代理执行 |
| `subagentStop` | 子代理完成时 | 触发后续操作 |
| `beforeShellExecution` | Shell 命令前 | 命令审批 |
| `afterShellExecution` | Shell 命令后 | 审计、收集指标 |
| `beforeMCPExecution` | MCP 工具前 | 访问控制 (fail-closed) |
| `afterMCPExecution` | MCP 工具后 | 审计 |
| `beforeReadFile` | 文件读取前 | 访问控制 (fail-closed) |
| `afterFileEdit` | 文件编辑后 | 格式化、统计 |
| `beforeSubmitPrompt` | 提交提示前 | 阻止不当提交 |
| `stop` | Agent 循环结束 | 自动跟进消息 |

### Tab (行内补全)

| Hook 事件 | 触发时机 |
|----------|----------|
| `beforeTabFileRead` | Tab 读取文件前 |
| `afterTabFileEdit` | Tab 编辑文件后 |

---

## 📝 配置示例

### 基础配置 (~/.cursor/hooks.json)

```json
{
  "version": 1,
  "hooks": {
    "afterFileEdit": [
      { "command": "./hooks/format.sh" }
    ],
    "beforeShellExecution": [
      {
        "command": "./hooks/audit.sh",
        "matcher": "curl|wget|nc"
      }
    ]
  }
}
```

### 审计脚本示例 (audit.sh)

```bash
#!/bin/bash
# 将所有 JSON 输入写入审计日志

json_input=$(cat)
timestamp=$(date '+%Y-%m-%d %H:%M:%S')
mkdir -p "$(dirname /tmp/agent-audit.log)"
echo "[$timestamp] $json_input" >> /tmp/agent-audit.log
exit 0
```

### 拦截 Git 命令 (block-git.sh)

```bash
#!/bin/bash
input=$(cat)
command=$(echo "$input" | jq -r '.command // empty')

if [[ "$command" =~ git[[:space:]] ]]; then
    cat << EOF
{
  "continue": true,
  "permission": "deny",
  "user_message": "Git 命令已被拦截。请改用 gh 工具。"
}
EOF
else
    cat << EOF
{
  "continue": true,
  "permission": "allow"
}
EOF
fi
```

---

## 🛡️ 安全特性

### Fail-Closed 策略

以下 Hook 采用 **失败即拒绝** 策略（hook 失败则阻止操作）：
- `beforeReadFile` - 防止敏感文件泄露
- `beforeMCPExecution` - 防止 MCP 操作绕过

### 匹配器 (Matcher)

| Hook 类型 | 匹配对象 | 示例 |
|----------|----------|------|
| `preToolUse` | 工具类型 | `Shell`, `Read`, `Write`, `Grep` |
| `subagentStart` | 子代理类型 | `explore`, `shell`, `generalPurpose` |
| `beforeShellExecution` | 命令文本 | `curl|wget|nc` |

---

## 🔌 合作伙伴集成

| 类别 | 合作伙伴 | 功能 |
|------|----------|------|
| MCP 治理 | MintMCP, Oasis Security, Runlayer | MCP 服务器清单、审计日志 |
| 代码安全 | Corridor, Semgrep | 实时安全反馈、漏洞扫描 |
| 依赖安全 | Endor Labs | 恶意依赖检测 |
| Agent 安全 | Snyk | 提示注入检测 |
| 机密管理 | 1Password | 环境文件验证 |

---

## 🐛 调试技巧

1. **查看已配置的 Hooks** - Cursor 设置 → Hooks 选项卡
2. **查看执行日志** - Hooks 输出通道
3. **确认路径正确**：
   - Project hooks: `.cursor/hooks/script.sh` (相对于项目根目录)
   - User hooks: `./hooks/script.sh` (相对于 `~/.cursor/`)
4. **重启 Cursor** - 确保 hooks 服务正在运行

---

## 💡 实用场景

### 1. 自动格式化代码

```json
{
  "hooks": {
    "afterFileEdit": [
      { "command": "prettier --write" }
    ]
  }
}
```

### 2. 网络命令审批

```json
{
  "hooks": {
    "beforeShellExecution": [
      {
        "command": "./approve-network.sh",
        "matcher": "curl|wget|nc|ssh"
      }
    ]
  }
}
```

### 3. 敏感文件保护

```json
{
  "hooks": {
    "beforeReadFile": [
      {
        "command": "./check-sensitive.sh",
        "matcher": "\\.env|secrets|credentials"
      }
    ]
  }
}
```

### 4. 子代理循环控制

```json
{
  "hooks": {
    "stop": [
      {
        "command": "./auto-retry.sh",
        "loop_limit": 5
      }
    ]
  }
}
```

---

## 📚 相关资源

- [官方文档](https://cursor.com/cn/docs/hooks)
- [Partner Integrations](https://cursor.com/cn/docs/hooks.md#partner-integrations)
- [Third Party Hooks](https://cursor.com/cn/docs/hooks.md#third-party-hooks)
- [Hooks 合作伙伴博客](/blog/hooks-partners)

---

## 🏷️ 标签

#Cursor #AI 编程 #Hooks #开发工具 #自动化 #安全
