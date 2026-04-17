# OpenClaw 多 Agent 配置完全指南

> **创建日期**: 2026-02-27  
> **最后更新**: 2026-02-27  
> **标签**: #OpenClaw #多 Agent #配置教程 #系统架构

---

## 🎯 教程目标

学完本教程，你将能够：

- ✅ 理解 OpenClaw 多 Agent 架构
- ✅ 配置多个独立 Agent（主 Agent、代码专家、写作助手等）
- ✅ 为不同 Agent 分配不同模型和权限
- ✅ 将 Agent 绑定到不同消息渠道（Telegram/ Discord/ 飞书）
- ✅ 保护敏感配置信息

---

## 📋 前置要求

| 要求 | 说明 |
|------|------|
| OpenClaw 已安装 | 版本 ≥ 2026.2.17 |
| 基础配置完成 | 至少一个渠道能正常收发消息 |
| 了解 JSON 配置 | 能编辑 `~/.openclaw/config.json` |

---

## 一、多 Agent 架构概览

### 1.1 为什么需要多 Agent？

```
❌ 单 Agent 的问题：
- 所有任务混在一起，上下文污染
- 无法针对不同场景优化
- 权限难以隔离（代码 Agent 需要 exec，写作 Agent 不需要）

✅ 多 Agent 的优势：
- 职责分离：主 Agent 聊天、代码 Agent 编程、写作 Agent 创作
- 独立配置：每个 Agent 有自己的模型、工具、工作区
- 成本优化：简单任务用便宜模型，复杂任务用强模型
- 安全隔离：敏感操作限制在特定 Agent
```

---

### 1.2 架构层次

```
┌─────────────────────────────────────────────────────┐
│                   消息渠道层                         │
│  Telegram Bot 1  │  Telegram Bot 2  │  Discord Bot  │
└────────┬────────┴─────────┬────────┴────────┬───────┘
         │                  │                  │
         ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────┐
│                   路由绑定层                         │
│  bindings: 根据渠道/账号 路由到对应 Agent            │
└────────┬─────────────────┬─────────────────┬────────┘
         │                  │                  │
         ▼                  ▼                  ▼
┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│   Agent 1   │   │   Agent 2   │   │   Agent 3   │
│   (main)    │   │   (code)    │   │   (write)   │
│  通用助手   │   │  代码专家   │   │  写作助手   │
└─────────────┘   └─────────────┘   └─────────────┘
         │                  │                  │
         ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────┐
│                   模型提供商层                       │
│  Bailian (阿里云)  │  DMXAPI  │  OpenAI  │  ...     │
└─────────────────────────────────────────────────────┘
```

---

## 二、配置文件结构

### 2.1 核心配置区块

OpenClaw 配置文件 (`~/.openclaw/config.json`) 包含以下关键区块：

| 区块         | 作用            | 必填  |
| ---------- | ------------- | --- |
| `models`   | 模型提供商和模型列表    | ✅   |
| `agents`   | Agent 定义和默认设置 | ✅   |
| `bindings` | 渠道→Agent 路由规则 | ✅   |
| `channels` | 各消息渠道配置       | 按需  |
| `gateway`  | 网关服务配置        | ✅   |
| `plugins`  | 插件启用列表        | ✅   |

---

### 2.2 完整配置示例（脱敏版）

```json5
{
  // ========== 1. 模型配置 ==========
  "models": {
    "mode": "merge",  // 合并模式：允许定义多个提供商
    "providers": {
      // 阿里云百炼
      "bailian": {
        "baseUrl": "https://coding.dashscope.aliyuncs.com/v1",
        "apiKey": "sk-***你的阿里云 API Key***",
        "api": "openai-completions",
        "models": [
          {
            "id": "qwen3-coder-plus",
            "name": "qwen3-coder-plus",
            "reasoning": false,
            "input": ["text"],
            "contextWindow": 1000000,
            "maxTokens": 65536
          },
          {
            "id": "qwen3.5-plus",
            "name": "qwen3.5-plus",
            "reasoning": false,
            "input": ["text"],
            "contextWindow": 1000000,
            "maxTokens": 65536
          }
        ]
      },
      // 第二提供商（备用或特殊模型）
      "dmxapi": {
        "baseUrl": "https://www.dmxapi.cn/v1",
        "apiKey": "sk-***你的 DMXAPI Key***",
        "api": "openai-completions",
        "models": [
          {
            "id": "claude-sonnet-4-6-cc",
            "name": "claude-sonnet-4-6-cc",
            "reasoning": false,
            "input": ["text"],
            "contextWindow": 1000000,
            "maxTokens": 200000,
            "cost": { "input": 0, "output": 0 }
          },
          {
            "id": "qwen3.5-plus",
            "name": "qwen3.5-plus",
            "reasoning": false,
            "contextWindow": 1000000,
            "maxTokens": 65536
          }
        ]
      }
    }
  },

  // ========== 2. Agent 配置 ==========
  "agents": {
    // 默认设置（所有 Agent 继承）
    "defaults": {
      "model": {
        "primary": "bailian/qwen3.5-plus",  // 默认模型
        "fallbacks": []  // 降级模型列表
      },
      "models": {
        // 允许使用的模型白名单
        "bailian/qwen3.5-plus": {},
        "bailian/qwen3-coder-plus": {},
        "dmxapi/claude-sonnet-4-6-cc": {},
        "dmxapi/qwen3.5-plus": {},
        "dmxapi/qwen-flash": {}
      },
      "workspace": "/Users/apple/clawd/agents/main",  // 默认工作区
      "compaction": { "mode": "safeguard" },
      "maxConcurrent": 4,  // 最大并发会话
      "subagents": { "maxConcurrent": 8 }  // 子代理并发数
    },
    // 自定义 Agent 列表
    "list": [
      {
        "id": "main",
        "name": "主 Agent",
        "workspace": "/Users/apple/clawd/agents/main"
        // 继承 defaults 的所有设置
      },
      {
        "id": "code",
        "name": "代码专家",
        "workspace": "/Users/apple/clawd/agents/code",
        "model": {
          "primary": "bailian/qwen3-coder-plus"  // 覆盖：代码专用模型
        },
        "identity": {
          "name": "代码助手",
          "emoji": "💻"
        }
      },
      {
        "id": "write",
        "name": "写作专家",
        "workspace": "/Users/apple/clawd/agents/write",
        "identity": {
          "name": "写作助手",
          "emoji": "✍️"
        }
        // 使用默认模型
      }
    ]
  },

  // ========== 3. 路由绑定 ==========
  "bindings": [
    // Telegram - 主 Bot → main Agent
    {
      "agentId": "main",
      "match": {
        "channel": "telegram",
        "accountId": "main"
      }
    },
    // Telegram - 代码 Bot → code Agent
    {
      "agentId": "code",
      "match": {
        "channel": "telegram",
        "accountId": "code"
      }
    },
    // Telegram - 写作 Bot → write Agent
    {
      "agentId": "write",
      "match": {
        "channel": "telegram",
        "accountId": "write"
      }
    },
    // 飞书 - 所有消息 → main Agent
    {
      "agentId": "main",
      "match": {
        "channel": "feishu",
        "peer": { "kind": "channel", "id": "feishu" }
      }
    }
  ],

  // ========== 4. 消息渠道配置 ==========
  "channels": {
    // Telegram（3 个独立 Bot）
    "telegram": {
      "enabled": true,
      "dmPolicy": "pairing",  // 私信需要配对
      "groupPolicy": "allowlist",  // 群组白名单
      "streaming": "partial",
      "proxy": "http://127.0.0.1:7897",  // 代理（如需）
      "accounts": {
        "main": {
          "dmPolicy": "pairing",
          "botToken": "***Bot Token 1***",
          "groupPolicy": "allowlist",
          "streaming": "off"
        },
        "code": {
          "dmPolicy": "pairing",
          "botToken": "***Bot Token 2***",
          "groupPolicy": "allowlist",
          "streaming": "off"
        },
        "write": {
          "dmPolicy": "pairing",
          "botToken": "***Bot Token 3***",
          "groupPolicy": "allowlist",
          "streaming": "off"
        }
      }
    },
    // Discord
    "discord": {
      "enabled": false,  // 暂时禁用
      "token": "***Discord Bot Token***",
      "groupPolicy": "allowlist",
      "dmPolicy": "pairing",
      "guilds": {
        "***服务器 ID***": {
          "requireMention": true,  // 必须@Bot 才响应
          "channels": {
            "dr_worker": { "allow": true }  // 允许的频道
          }
        }
      }
    },
    // 飞书
    "feishu": {
      "enabled": true,
      "appId": "cli_***",
      "appSecret": "***"
    }
  },

  // ========== 5. 网关配置 ==========
  "gateway": {
    "port": 18789,
    "mode": "local",  // local | remote
    "bind": "loopback",  // 仅本地访问
    "auth": {
      "mode": "token",
      "token": "***网关认证 Token***"
    },
    "trustedProxies": ["192.168.1.100"]  // 可信代理 IP
  },

  // ========== 6. 插件配置 ==========
  "plugins": {
    "allow": ["telegram", "discord", "feishu", "voice-call"],
    "entries": {
      "telegram": { "enabled": true },
      "discord": { "enabled": true },
      "feishu": { "enabled": true },
      "voice-call": { "enabled": true }
    }
  },

  // ========== 7. 消息行为 ==========
  "messages": {
    "ackReactionScope": "group-mentions",  // 群聊提及后加反应
    "tts": {
      "auto": "tagged",  // 仅当消息包含 [[tts]] 标签时
      "provider": "edge",
      "edge": {
        "enabled": true,
        "voice": "zh-CN-XiaoyiNeural",
        "lang": "zh-CN",
        "rate": "+10%"
      }
    }
  },

  // ========== 8. 命令配置 ==========
  "commands": {
    "native": "auto",  // 自动启用内置命令
    "nativeSkills": "auto",
    "restart": true,  // 允许 /restart 命令
    "ownerDisplay": "raw"
  }
}
```

---

## 三、逐步配置指南

### 步骤 1：规划 Agent 结构

在开始前，先规划你需要哪些 Agent：

| Agent ID | 用途 | 推荐模型 | 工作区 |
|----------|------|----------|--------|
| `main` | 通用对话、日常任务 | qwen3.5-plus | `~/clawd/agents/main` |
| `code` | 编程、代码审查 | qwen-coder-plus | `~/clawd/agents/code` |
| `write` | 内容创作、社交媒体 | qwen3.5-plus | `~/clawd/agents/write` |
| `research` | 深度研究、长上下文 | claude-sonnet-4-6-cc | `~/clawd/agents/research` |

---

### 步骤 2：创建工作区目录

```bash
# 为每个 Agent 创建独立工作区
mkdir -p ~/clawd/agents/{main,code,write,research}

# 为每个工作区初始化基础文件
for agent in main code write research; do
  cd ~/clawd/agents/$agent
  echo "# $agent Agent" > README.md
  mkdir -p skills memory
done
```

---

### 步骤 3：配置模型提供商

编辑 `~/.openclaw/config.json`，在 `models.providers` 中添加你的模型提供商：

```json5
{
  "models": {
    "mode": "merge",
    "providers": {
      "bailian": {
        "baseUrl": "https://coding.dashscope.aliyuncs.com/v1",
        "apiKey": "sk-你的 Key",
        "api": "openai-completions",
        "models": [
          {
            "id": "qwen3.5-plus",
            "name": "qwen3.5-plus",
            "contextWindow": 1000000,
            "maxTokens": 65536
          }
        ]
      }
    }
  }
}
```

> ⚠️ **安全提示**：API Key 不要提交到 Git！使用 `.gitignore` 排除配置文件。

---

### 步骤 4：定义 Agent 列表

在 `agents.list` 中定义每个 Agent：

```json5
{
  "agents": {
    "defaults": {
      "model": { "primary": "bailian/qwen3.5-plus" },
      "workspace": "/Users/apple/clawd/agents/main",
      "maxConcurrent": 4
    },
    "list": [
      {
        "id": "main",
        "name": "主 Agent"
      },
      {
        "id": "code",
        "name": "代码专家",
        "workspace": "/Users/apple/clawd/agents/code",
        "model": { "primary": "bailian/qwen3-coder-plus" },
        "identity": { "name": "代码助手", "emoji": "💻" }
      },
      {
        "id": "write",
        "name": "写作专家",
        "workspace": "/Users/apple/clawd/agents/write",
        "identity": { "name": "写作助手", "emoji": "✍️" }
      }
    ]
  }
}
```

---

### 步骤 5：配置路由绑定

在 `bindings` 中定义渠道→Agent 的映射：

```json5
{
  "bindings": [
    // Telegram 主 Bot → main Agent
    {
      "agentId": "main",
      "match": { "channel": "telegram", "accountId": "main" }
    },
    // Telegram 代码 Bot → code Agent
    {
      "agentId": "code",
      "match": { "channel": "telegram", "accountId": "code" }
    },
    // Telegram 写作 Bot → write Agent
    {
      "agentId": "write",
      "match": { "channel": "telegram", "accountId": "write" }
    }
  ]
}
```

---

### 步骤 6：配置 Telegram 多 Bot

在 Telegram 中创建多个 Bot（通过 [@BotFather](https://t.me/BotFather)）：

```
/newbot → 主助手 Bot → 获取 Token 1
/newbot → 代码助手 Bot → 获取 Token 2
/newbot → 写作助手 Bot → 获取 Token 3
```

然后配置到 `channels.telegram.accounts`：

```json5
{
  "channels": {
    "telegram": {
      "enabled": true,
      "accounts": {
        "main": {
          "botToken": "Token 1",
          "dmPolicy": "pairing"
        },
        "code": {
          "botToken": "Token 2",
          "dmPolicy": "pairing"
        },
        "write": {
          "botToken": "Token 3",
          "dmPolicy": "pairing"
        }
      }
    }
  }
}
```

---

### 步骤 7：重启网关

```bash
# 验证配置
openclaw gateway status

# 重启网关使配置生效
openclaw gateway restart
```

---

## 四、高级配置

### 4.1 按 Agent 隔离权限

为不同 Agent 设置不同的工具权限：

```json5
{
  "agents": {
    "list": [
      {
        "id": "main",
        "tools": {
          "exec": {
            "security": "allowlist",  // 需要白名单
            "ask": "on-miss"
          }
        }
      },
      {
        "id": "code",
        "tools": {
          "exec": {
            "security": "allowlist",
            "allowlist": [
              "~/Projects/**/bin/**",  // 允许项目目录
              "npm", "pnpm", "yarn",
              "git", "diff", "grep"
            ]
          }
        }
      },
      {
        "id": "write",
        "tools": {
          "exec": {
            "security": "deny"  // 完全禁止执行命令
          }
        }
      }
    ]
  }
}
```

---

### 4.2 模型降级策略

配置主模型失败时的降级方案：

```json5
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "bailian/qwen3.5-plus",
        "fallbacks": [
          "dmxapi/qwen3.5-plus",  // 第一降级
          "dmxapi/qwen-flash"     // 第二降级（更快更便宜）
        ]
      }
    }
  }
}
```

---

### 4.3 渠道特定行为

为不同渠道配置不同的消息行为：

```json5
{
  "channels": {
    "telegram": {
      "streaming": "partial",  // 部分流式输出
      "proxy": "http://127.0.0.1:7897"
    },
    "discord": {
      "streaming": "off",  // 禁用流式
      "requireMention": true  // 必须@Bot
    },
    "feishu": {
      "streaming": "full"  // 完整流式
    }
  }
}
```

---

### 4.4 TTS 语音配置

为不同 Agent 配置不同的语音：

```json5
{
  "messages": {
    "tts": {
      "auto": "tagged",
      "provider": "edge",
      "edge": {
        "enabled": true,
        "voice": "zh-CN-XiaoyiNeural",  // 默认语音
        "lang": "zh-CN",
        "rate": "+10%"
      }
    }
  }
}
```

在消息中使用 `[[tts]]` 标签触发语音：

```
[[tts]] 这是一条语音消息！
```

---

## 五、安全最佳实践

### 5.1 保护敏感信息

```bash
# 1. 配置文件不要提交到 Git
echo "~/.openclaw/config.json" >> ~/.gitignore_global

# 2. 使用环境变量（可选）
export OPENCLAW_BAILIAN_KEY="sk-***"
export OPENCLAW_DMXAPI_KEY="sk-***"

# 3. 限制网关访问
{
  "gateway": {
    "bind": "loopback",  // 仅本地
    "trustedProxies": ["192.168.1.100"]  // 只信任内网 IP
  }
}
```

---

### 5.2 权限最小化

| Agent | 推荐权限 |
|-------|---------|
| `main` | 允许 exec（白名单）、允许所有工具 |
| `code` | 允许 exec（项目目录）、允许 browser |
| `write` | **禁止 exec**、仅允许文件读写 |
| `research` | 允许 web_search、禁止 exec |

---

### 5.3 渠道访问控制

```json5
{
  "channels": {
    "telegram": {
      "dmPolicy": "pairing",  // 私信需要配对
      "groupPolicy": "allowlist",  // 群组白名单
      "allowFrom": ["tg:123456789"]  // 仅允许特定用户
    }
  }
}
```

---

## 六、故障排查

### 问题 1：Agent 不响应

```bash
# 检查网关状态
openclaw gateway status

# 查看日志
openclaw gateway logs --tail 100

# 验证绑定配置
openclaw config get bindings
```

---

### 问题 2：模型调用失败

```bash
# 测试模型连接
curl -H "Authorization: Bearer sk-***" \
  https://coding.dashscope.aliyuncs.com/v1/models

# 检查模型配置
openclaw config get models.providers
```

---

### 问题 3：Telegram Bot 无响应

```bash
# 测试 Bot Token
curl "https://api.telegram.org/bot<TOKEN>/getMe"

# 检查代理配置（如使用代理）
curl -x http://127.0.0.1:7897 \
  "https://api.telegram.org/bot<TOKEN>/getMe"
```

---

## 七、配置检查清单

配置完成后，逐项检查：

- [ ] 所有 API Key 已替换为真实值
- [ ] 每个 Agent 有独立的工作区目录
- [ ] `bindings` 中渠道→Agent 映射正确
- [ ] Telegram Bot Token 已正确配置
- [ ] 网关已重启 (`openclaw gateway restart`)
- [ ] 使用 `/status` 命令验证各 Agent 状态
- [ ] 测试每个渠道的消息收发

---

## 八、扩展阅读

| 主题 | 相关笔记 |
|------|---------|
| 权限体系 | [[OpenClaw 权限体系]] |
| Discord 配置 | [[Discord 私信 vs 群聊@Bot]] |
| 任务管理 | [[OpenClaw_Mission_Control/00-Overview]] |
| 技能开发 | [[OpenClaw Skills 和插件扩展路径详解]] |
| 官方文档 | [docs.openclaw.ai](https://docs.openclaw.ai) |

---

## 📝 配置模板下载

完整配置模板（脱敏版）已保存到：
`~/clawd/agents/write/templates/multi-agent-config.example.json`

---

**标签**: #OpenClaw #多 Agent #配置教程 #系统架构 #Telegram #Discord #飞书
