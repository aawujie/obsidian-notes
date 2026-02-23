# OpenClaw 权限体系

> 最后更新：2026-02-23
> 标签：#OpenClaw #权限 #安全 #配置

---

## 📚 核心文档位置

### 1. Exec Approvals（执行权限审批）
**路径**: `/opt/homebrew/lib/node_modules/openclaw/docs/tools/exec-approvals.md`

**核心内容**:
- Exec 审批策略：`deny` / `allowlist` / `full`
- 按 Agent 的允许列表（Allowlist）
- 安全模式（`security`）和询问模式（`ask`）
- 配置文件：`~/.openclaw/exec-approvals.json`

**配置示例**:
```json5
{
  defaults: {
    security: "allowlist",  // deny | allowlist | full
    ask: "on-miss",         // off | on-miss | always
    askFallback: "deny",    // 无 UI 时的回退策略
    autoAllowSkills: false, // 是否自动允许技能 CLI
  },
  agents: {
    main: {
      security: "allowlist",
      ask: "on-miss",
      allowlist: [
        {
          id: "B0C8C0B3-2C2D-4F8A-9A3C-5A4B3C2D1E0F",
          pattern: "~/Projects/**/bin/rg",
          lastUsedAt: 1737150000000,
          lastUsedCommand: "rg -n TODO",
          lastResolvedPath: "/Users/user/Projects/.../bin/rg"
        }
      ]
    }
  }
}
```

---

### 2. Elevated Mode（提升权限模式）
**路径**: `/opt/homebrew/lib/node_modules/openclaw/docs/tools/elevated.md`

**核心内容**:
- `/elevated on|off|ask|full` 指令
- 发送者白名单（`tools.elevated.allowFrom`）
- 按 Agent 的权限限制
- Discord 回退机制

**指令说明**:
| 指令 | 说明 |
|------|------|
| `/elevated on` | 在网关主机运行，保留执行审批 |
| `/elevated ask` | 同上（别名） |
| `/elevated full` | 在网关主机运行，**跳过**执行审批 |
| `/elevated off` | 禁用提升权限 |

**配置示例**:
```json5
{
  tools: {
    elevated: {
      enabled: true,
      allowFrom: {
        discord: ["user:123456789"],
        telegram: ["tg:987654321"],
        whatsapp: ["+15555550123"]
      }
    }
  }
}
```

---

### 3. Slash Commands（命令权限）
**路径**: `/opt/homebrew/lib/node_modules/openclaw/docs/tools/slash-commands.md`

**核心内容**:
- `commands.allowFrom` — 按渠道的命令授权白名单
- `commands.useAccessGroups` — 访问组控制（默认 `true`）
- 指令授权（Directives Authorization）
- 内联快捷命令（`/help`, `/status`, `/whoami`）

**配置示例**:
```json5
{
  commands: {
    native: "auto",        // auto | true | false
    text: true,            // 启用文本命令解析
    bash: false,           // 启用 ! <cmd> 主机命令
    allowFrom: {
      "*": ["user1"],      // 全局默认
      discord: ["user:123"],
      telegram: ["tg:456"]
    },
    useAccessGroups: true, // 强制执行访问组
  }
}
```

**授权逻辑**:
1. 如果 `commands.allowFrom` 配置 → **仅**使用该白名单
2. 否则 → 渠道白名单/配对 + `commands.useAccessGroups`

---

### 4. Exec Tool（执行工具权限）
**路径**: `/opt/homebrew/lib/node_modules/openclaw/docs/tools/exec.md`

**核心内容**:
- `host`: `sandbox` | `gateway` | `node`
- `security`: `deny` | `allowlist` | `full`
- `ask`: `off` | `on-miss` | `always`
- 安全 bins（`safeBins`）— 无需白名单的 stdin 专用命令

**安全 Bins 默认列表**:
```
jq, grep, cut, sort, uniq, head, tail, tr, wc
```

**会话覆盖（`/exec` 命令）**:
```bash
# 查看当前设置
/exec

# 设置会话级默认值
/exec host=gateway security=allowlist ask=on-miss node=mac-1
```

---

### 5. Configuration Reference（完整配置参考）
**路径**: `/opt/homebrew/lib/node_modules/openclaw/docs/gateway/configuration-reference.md`

**核心内容**:
- DM 和群组访问控制（`dmPolicy` / `groupPolicy`）
- 多渠道白名单配置
- 多 Agent 路由和权限
- 完整的字段参考

**DM 访问策略**:
```json5
{
  channels: {
    telegram: {
      dmPolicy: "pairing",    // pairing | allowlist | open | disabled
      allowFrom: ["tg:123"],  // allowlist/open 模式下需要
    }
  }
}
```

**群组提及规则**:
```json5
{
  agents: {
    list: [{
      id: "main",
      groupChat: {
        mentionPatterns: ["@openclaw", "openclaw"],
      }
    }]
  },
  channels: {
    whatsapp: {
      groups: {
        "*": { requireMention: true }
      }
    }
  }
}
```

---

### 6. Sandbox vs Tool Policy vs Elevated（权限对比）
**路径**: `/opt/homebrew/lib/node_modules/openclaw/docs/gateway/sandbox-vs-tool-policy-vs-elevated.md`

**核心对比**:

| 机制 | 作用域 | 用途 | 配置位置 |
|------|--------|------|---------|
| **Sandbox** | 会话隔离 | 在容器中运行 Agent | `agents.defaults.sandbox` |
| **Tool Policy** | 工具级别 | 允许/拒绝特定工具 | `tools.deny` / `tools.allow` |
| **Elevated** | 会话级别 | 提升执行权限 | `/elevated` 指令 |
| **Exec Approvals** | 命令级别 | 逐条审批执行请求 | `~/.openclaw/exec-approvals.json` |

---

## 🔑 权限层次结构

```
用户发送请求
    ↓
1. 渠道认证 (allowFrom / pairing)
    ↓
2. 命令权限 (commands.allowFrom)
    ↓
3. 工具策略 (tools.allow/deny)
    ↓
4. Elevated 检查 (tools.elevated)
    ↓
5. Exec 审批 (security + ask + allowlist)
    ↓
执行命令
```

---

## 🛡️ 安全最佳实践

### 1. 最小权限原则
```json5
{
  tools: {
    exec: {
      security: "allowlist",  // 不要用 full
      ask: "on-miss",         // 未知命令时询问
    }
  }
}
```

### 2. 渠道隔离
```json5
{
  channels: {
    whatsapp: {
      allowFrom: ["+15555550123"],  // 仅信任的号码
      groups: {
        "*": { requireMention: true }  // 群组需要提及
      }
    }
  }
}
```

### 3. 按 Agent 隔离
```json5
{
  agents: {
    list: [
      {
        id: "main",
        tools: {
          exec: {
            security: "allowlist",
            allowlist: ["~/bin/**"]
          }
        }
      },
      {
        id: "restricted",
        tools: {
          exec: { security: "deny" }  // 完全禁止执行
        }
      }
    ]
  }
}
```

### 4. 使用 Safe Bins
- 对于只处理 stdin 的命令（`jq`, `grep` 等），无需白名单
- 安全 bins 拒绝文件路径参数，防止文件读取

---

## 📋 快速检查清单

- [ ] 配置 `channels.<provider>.allowFrom` 限制谁能发消息
- [ ] 设置 `commands.allowFrom` 限制谁能用命令
- [ ] 配置 `tools.exec.security = "allowlist"` 而非 `full`
- [ ] 在 `exec-approvals.json` 中维护允许列表
- [ ] 群组启用 `requireMention: true`
- [ ] 敏感 Agent 禁用 `elevated` 权限
- [ ] 定期审查 `exec-approvals.json` 中的允许列表

---

## 🔗 相关文档

- [[OpenClaw 配置指南]]
- [[OpenClaw 多 Agent 架构]]
- [[OpenClaw 安全加固]]
- [OpenClaw 官方文档](https://docs.openclaw.ai)

---

*笔记来源：OpenClaw 文档整理*
