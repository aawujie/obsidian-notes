# OpenClaw 配置教程

> 创建日期:: 2026-02-27
> 标签:: #OpenClaw #配置教程 #入门指南

---

## 📋 目录

1. [安装配置](#安装)
2. [模型提供商配置](#模型提供商配置)
3. [初始化主 Agent](#初始化主-agent)
4. [多 Agent 配置](#多-agent-配置)
5. [记忆配置](#记忆配置)
6. [Skills 配置](#skills-配置)
7. [Subagent 配置](#subagent-配置)
8. [心跳配置](#心跳配置)
9. [绑定配置](#绑定配置)

---

## 安装

### 配置文件位置

OpenClaw 的主配置文件位于：

```bash
~/.openclaw/openclaw.json
```

### 初始配置生成

首次运行时会自动生成基础配置：

```bash
# 启动 Gateway 自动生成配置
openclaw gateway start

# 查看配置
openclaw config show
```

### 配置文件结构

```json5
{
  "version": 1,
  "agents": { ... },      // Agent 配置
  "models": { ... },      // 模型提供商配置
  "bindings": [ ... ],    // 通信绑定配置
  "channels": { ... },    // 通信配置
  "tools": { ... },       // 工具配置
  "plugins": { ... }      // 插件配置
}
```

---

## 模型提供商配置

### 配置位置

```json5
{
  "models": {
    "mode": "merge",  // 合并模式
    "providers": {
      // 提供商配置
    }
  }
}
```

### Bailian（通义千问）配置

```json5
{
  "models": {
    "mode": "merge",
    "providers": {
      "bailian": {
        "baseUrl": "https://dashscope.aliyuncs.com/v1",
        "apiKey": "sk-your-api-key-here",
        "api": "openai-compat",
        "models": [
          {
            "id": "qwen-max",
            "name": "Qwen Max",
            "reasoning": false,
            "input": ["text"],
            "contextWindow": 32000,
            "maxTokens": 8000
          },
          {
            "id": "qwen-plus",
            "name": "Qwen Plus",
            "reasoning": false,
            "input": ["text"],
            "contextWindow": 32000,
            "maxTokens": 8000
          }
        ]
      }
    }
  }
}
```

### Claude 配置

```json5
{
  "models": {
    "providers": {
      "anthropic": {
        "apiKey": "sk-ant-your-api-key",
        "models": [
          {
            "id": "claude-sonnet-4-5-20250929",
            "name": "Claude Sonnet 4.5",
            "reasoning": false,
            "input": ["text"],
            "contextWindow": 200000,
            "maxTokens": 64000
          },
          {
            "id": "claude-haiku-3-5",
            "name": "Claude Haiku 3.5",
            "reasoning": false,
            "input": ["text"],
            "contextWindow": 200000,
            "maxTokens": 64000
          }
        ]
      }
    }
  }
}
```

---

## 初始化主 Agent

### Agent 基础配置

```json5
{
  "agents": {
    "list": [
      {
        "id": "main",           // Agent ID（必须唯一）
        "name": "主 Agent",      // 显示名称
        "workspace": "/Users/apple/clawd/agents/main"  // 工作空间路径
      }
    ]
  }
}
```

### 工作空间文件结构

每个 Agent 的工作空间包含以下文件：

```
~/clawd/agents/main/
├── AGENTS.md          # 工作方式指导
├── SOUL.md            # 人格和回复风格
├── IDENTITY.md        # 身份标识（名称、emoji）
├── USER.md            # 用户信息
├── TOOLS.md           # 工具配置说明
├── HEARTBEAT.md       # 心跳任务配置
└── memory/            # 记忆文件目录
    ├── 2026-02-27.md  # 每日日志
    └── ...
```

### SOUL.md 配置示例

```markdown
# SOUL.md - Who You Are

## 沟通风格
- 直接切入主题，不需要礼貌性寒暄
- 允许表达观点，不必保持绝对中立
- 简洁优先，但涉及技术细节时不省略关键信息

## 工作方式
- 优先尝试自主解决，确实需要时再询问
- 主动提供相关背景信息和替代方案
```

### IDENTITY.md 配置示例

```markdown
# IDENTITY.md - Who Am I?

- **Name:** 龙虾助手
- **Creature:** AI 助手
- **Vibe:** 直接、高效、友好
- **Emoji:** 🦞
```

### USER.md 配置示例

```markdown
# USER.md - About Your Human

- **Name:** 张三
- **Timezone:** Asia/Shanghai
- **Notes:** 
  - 全栈开发者
  - 偏好 TypeScript 和 Python
  - 工作日 9:00-18:00 为工作时间
```

---

## 多 Agent 配置

### 基础多 Agent 配置

```json5
{
  "agents": {
    "list": [
      {
        "id": "main",
        "name": "主 Agent",
        "workspace": "/Users/apple/clawd/agents/main"
      },
      {
        "id": "code",
        "name": "代码专家",
        "workspace": "/Users/apple/clawd/agents/code",
        "model": {
          "primary": "bailian/qwen-max"
        }
      },
      {
        "id": "write",
        "name": "写作专家",
        "workspace": "/Users/apple/clawd/agents/write"
      }
    ]
  }
}
```

### 为不同 Agent 配置不同模型

```json5
{
  "agents": {
    "list": [
      {
        "id": "main",
        "model": { "primary": "claude-sonnet-4-5-20250929" }
      },
      {
        "id": "code",
        "model": { "primary": "bailian/qwen-max" },
        "skills": ["coding-agent", "github"]
      },
      {
        "id": "research",
        "model": { "primary": "claude-sonnet-4-5-20250929" },
        "skills": ["web-search", "summarize"]
      }
    ]
  }
}
```

### Agent 技能配置

```json5
{
  "agents": {
    "list": [
      {
        "id": "main",
        "skills": ["weather", "message"]  // 显式指定技能
      },
      {
        "id": "code",
        "skills": ["coding-agent", "github", "tmux"]
      }
    ]
  }
}
```

---

## 记忆配置

### MemorySearch 基础配置

```json5
{
  "agents": {
    "defaults": {
      "memorySearch": {
        "enabled": true,  // 启用语义检索
        "provider": "openai",
        "remote": {
          "baseUrl": "https://your-embedding-api.com/v1",
          "apiKey": "sk-embedding-key"
        },
        "model": "bge-m3"
      }
    }
  }
}
```

### 完整 MemorySearch 配置

```json5
{
  "agents": {
    "defaults": {
      "memorySearch": {
        "enabled": true,
        "provider": "openai",
        "remote": {
          "baseUrl": "https://www.dmxapi.cn/v1",
          "apiKey": "sk-your-key"
        },
        "model": "bge-m3",
        
        // 同步配置
        "sync": {
          "onSessionStart": true,    // 会话启动时同步
          "onSearch": true,          // 搜索时同步
          "watch": true,             // 文件监听
          "watchDebounceMs": 1500,   // 防抖延迟
          "intervalMinutes": 5       // 定时检查间隔
        },
        
        // 查询配置
        "query": {
          "maxResults": 5,
          "minScore": 0.5,
          "hybrid": {
            "enabled": true,         // 启用混合搜索
            "vectorWeight": 0.7,     // 向量权重
            "textWeight": 0.3        // 文本权重
          }
        },
        
        // 缓存配置
        "cache": {
          "enabled": true,
          "maxEntries": 50000
        }
      }
    }
  }
}
```

---

## Skills 配置

### 全局技能配置

```json5
{
  "skills": {
    "dir": "~/clawd/agents/main/skills"  // 技能目录
  }
}
```

### Agent 专属技能配置

```json5
{
  "agents": {
    "list": [
      {
        "id": "main",
        "skills": [
          "weather",
          "message",
          "web-search"
        ]
      },
      {
        "id": "code",
        "skills": [
          "coding-agent",
          "github",
          "tmux"
        ]
      }
    ]
  }
}
```

### 技能过滤配置

```json5
{
  "agents": {
    "list": [
      {
        "id": "main",
        "skills": []  // 空数组 = 禁用所有技能
      },
      {
        "id": "code",
        "skills": ["coding-agent"]  // 只允许特定技能
      }
    ]
  }
}
```

### 技能目录结构

```
skills/
└── my-skill/
    ├── SKILL.md          # 技能说明（必须）
    ├── execute.sh        # 执行脚本（可选）
    ├── README.md         # 使用说明（可选）
    └── config.json       # 技能配置（可选）
```

### SKILL.md 配置模板

```markdown
# Skill Name

## 触发条件
当用户提到「关键词 1」「关键词 2」时触发

## 执行流程
1. 第一步操作
2. 第二步操作
3. 输出结果

## 输出规范
- 结果格式要求
- 保存位置
```

---

## Subagent 配置

### 全局 Subagent 配置

```json5
{
  "agents": {
    "defaults": {
      "subagents": {
        // 子 agent 默认模型（推荐用便宜模型）
        "model": {
          "primary": "bailian/qwen-plus"
        },
        // 思考级别
        "thinking": "low",
        // 运行超时（秒）
        "runTimeoutSeconds": 600,
        // 最大并发数
        "maxConcurrent": 8,
        // 最大嵌套深度
        "maxSpawnDepth": 2,
        // 每个 agent 最大子 agent 数
        "maxChildrenPerAgent": 5,
        // 自动归档时间（分钟）
        "archiveAfterMinutes": 60
      }
    }
  }
}
```

### 分 Agent 的 Subagent 配置

```json5
{
  "agents": {
    "list": [
      {
        "id": "main",
        "subagents": {
          "model": { "primary": "bailian/qwen-plus" }
        }
      },
      {
        "id": "code",
        "subagents": {
          "model": { "primary": "claude-haiku-3-5" }  // 更便宜
        }
      }
    ]
  }
}
```

### Subagent 工具权限配置

```json5
{
  "tools": {
    "subagents": {
      "tools": {
        // 拒绝的工具
        "deny": ["gateway", "cron"],
        // 允许的工具（如果设置，则变为白名单模式）
        // "allow": ["read", "write", "edit", "exec"]
      }
    }
  }
}
```

### 成本优化配置示例

```json5
{
  "agents": {
    "defaults": {
      "subagents": {
        // 子 agent 统一用便宜模型
        "model": { "primary": "claude-haiku-3-5" },
        "thinking": "low",
        "runTimeoutSeconds": 300
      }
    },
    "list": [
      {
        "id": "main",
        // 主 agent 用高性能
        "model": { "primary": "claude-sonnet-4-5-20250929" }
      },
      {
        "id": "code",
        "model": { "primary": "claude-sonnet-4-5-20250929" },
        // 代码子 agent 用便宜模型
        "subagents": { "model": { "primary": "claude-haiku-3-5" } }
      }
    ]
  }
}
```

---

## 心跳配置

### HEARTBEAT.md 配置

```markdown
# HEARTBEAT.md

## 每次心跳时执行
- 检查核心服务健康状态
- 扫描待办事项

## 每日执行一次
- 整理对话日志
- 标记超时任务

## 每周执行一次
- 归档旧记忆
- 生成周报
```

### 心跳周期配置

```json5
{
  "agents": {
    "defaults": {
      "heartbeat": {
        "intervalMinutes": 30,  // 心跳间隔
        "enabled": true
      }
    }
  }
}
```

---

## 绑定配置

### 渠道绑定基础配置

```json5
{
  "bindings": [
    {
      "agentId": "main",
      "match": {
        "channel": "telegram",
        "accountId": "main"
      }
    },
    {
      "agentId": "code",
      "match": {
        "channel": "telegram",
        "accountId": "code"
      }
    }
  ]
}
```

### Discord 绑定配置

```json5
{
  "bindings": [
    {
      "agentId": "main",
      "match": {
        "channel": "discord",
        "guildId": "your-guild-id",
        "roles": ["role-id-1", "role-id-2"]
      }
    }
  ]
}
```

### 多渠道绑定

```json5
{
  "bindings": [
    {
      "agentId": "main",
      "match": { "channel": "telegram", "accountId": "main" }
    },
    {
      "agentId": "main",
      "match": { "channel": "discord", "guildId": "guild-123" }
    },
    {
      "agentId": "code",
      "match": { "channel": "telegram", "accountId": "code" }
    }
  ]
}
```

---

## 工具配置

### 全局工具配置

```json5
{
  "tools": {
    "profile": "full",  // 工具配置文件
    "allow": ["read", "write", "edit", "exec", "web_search"],
    "deny": []
  }
}
```

### Exec 工具配置

```json5
{
  "tools": {
    "exec": {
      "host": "sandbox",           // 执行主机
      "security": "allowlist",     // 安全模式
      "ask": "on-miss",            // 询问模式
      "timeoutSec": 300,           // 超时时间
      "backgroundMs": 10000,       // 后台执行阈值
      "safeBins": ["git", "npm", "pnpm", "yarn"]  // 安全命令
    }
  }
}
```

### 文件系统工具配置

```json5
{
  "tools": {
    "fs": {
      "workspaceOnly": false  // 限制在 workspace 内
    }
  }
}
```

---

## 渠道配置

### Telegram 配置

```json5
{
  "channels": {
    "telegram": {
      "enabled": true,
      "accounts": [
        {
          "id": "main",
          "token": "bot-token-here"
        }
      ]
    }
  }
}
```

### Discord 配置

```json5
{
  "channels": {
    "discord": {
      "enabled": true,
      "token": "bot-token",
      "threadBindings": {
        "enabled": true,
        "ttlHours": 24
      }
    }
  }
}
```

---

## 插件配置

### 插件启用配置

```json5
{
  "plugins": {
    "slots": {
      "memory": "memory-core",      // 记忆插件
      "media": "media-core",        // 媒体插件
      "web": "web-core"             // 网页插件
    }
  }
}
```

### 禁用插件

```json5
{
  "plugins": {
    "slots": {
      "memory": "none"  // 禁用记忆插件
    }
  }
}
```

---

## 配置验证

### 查看当前配置

```bash
# 查看完整配置
openclaw config show

# 查看特定部分
openclaw config show | jq '.agents'
openclaw config show | jq '.models'
```

### 验证配置语法

```bash
# 检查配置文件
cat ~/.openclaw/openclaw.json | jq .
```

### 测试配置

```bash
# 重启 Gateway 应用配置
openclaw gateway restart

# 查看 Gateway 状态
openclaw gateway status
```

---

## 配置最佳实践

### 1. 成本优化

```json5
{
  "agents": {
    "defaults": {
      "subagents": {
        "model": { "primary": "便宜模型" }
      }
    }
  }
}
```

### 2. 安全配置

```json5
{
  "tools": {
    "exec": {
      "security": "allowlist",
      "safeBins": ["git", "npm"]
    },
    "fs": {
      "workspaceOnly": true
    }
  }
}
```

### 3. 性能优化

```json5
{
  "agents": {
    "defaults": {
      "memorySearch": {
        "cache": { "enabled": true },
        "sync": { "watch": true }
      }
    }
  }
}
```

---

## 故障排查

### 配置不生效

```bash
# 1. 检查配置语法
cat ~/.openclaw/openclaw.json | jq .

# 2. 重启 Gateway
openclaw gateway restart

# 3. 查看日志
openclaw logs
```

### 模型调用失败

```bash
# 1. 检查 API Key
openclaw config show | grep apiKey

# 2. 测试模型
openclaw models list

# 3. 查看模型状态
openclaw models status
```

### Agent 不响应

```bash
# 1. 检查绑定
openclaw config show | jq '.bindings'

# 2. 检查渠道状态
openclaw channels status

# 3. 查看 Agent 状态
openclaw agents list
```
