# Discord 私信 vs 群聊@Bot

> 创建时间：2026-02-20  
> 标签：#Discord #OpenClaw #消息处理

---

## 📬 两种消息类型

### 1️⃣ 私信 (DM)

**场景：** 直接在 Discord 里和 Bot 私聊

**处理流程：**
```
收到私信 → 检查是否配对 → 已配对✅回复 / 未配对❌拒绝
```

**配置：**
```json
{
  "dm": {
    "enabled": true,
    "groupEnabled": false
  },
  "dmPolicy": "pairing"  // 需要配对
}
```

---

### 2️⃣ 群聊 @Bot

**场景：** 在服务器频道里 @Bot

**处理流程：**
```
收到群消息 → 检查是否@Bot → 检查频道白名单 → 通过✅回复 / 失败❌跳过
```

**配置：**
```json
{
  "guilds": {
    "1324011180921983078": {
      "requireMention": true,  // 必须@Bot
      "channels": {
        "dr_worker": {
          "allow": true  // 允许的频道
        }
      }
    }
  },
  "groupPolicy": "allowlist"  // 白名单模式
}
```

---

## 🔍 关键区别

| 对比项 | 私信 (DM) | 群聊@Bot |
|--------|----------|----------|
| **触发方式** | 直接发消息 | 必须@Bot |
| **安全机制** | pairing 配对 | allowlist 白名单 |
| **频道限制** | 无 | 可限制特定频道 |
| **requireMention** | 不适用 | 必须@才响应 |

---

## ✅ 响应规则

| 场景 | 位置 | 是否@ | 配对 | 结果 |
|------|------|-------|------|------|
| 私信 | DM | - | ✅ 已配对 | ✅ 回复 |
| 私信 | DM | - | ❌ 未配对 | ❌ 拒绝 |
| 群聊 | dr_worker | ✅ @Bot | - | ✅ 回复 |
| 群聊 | dr_worker | ❌ 不@ | - | ❌ 跳过 |
| 群聊 | general | ✅ @Bot | - | ❌ 频道不在白名单 |

---

## 🔧 配置命令

### 修改私信策略

```bash
# 允许所有私信（不安全）
openclaw config set channels.discord.dmPolicy "allow"

# 需要配对（推荐）
openclaw config set channels.discord.dmPolicy "pairing"

# 禁止私信
openclaw config set channels.discord.dmPolicy "deny"
```

---

### 修改群聊策略

```bash
# 白名单模式（推荐）
openclaw config set channels.discord.groupPolicy "allowlist"

# 黑名单模式
openclaw config set channels.discord.groupPolicy "blocklist"

# 允许所有（不安全）
openclaw config set channels.discord.groupPolicy "allow"
```

---

### 添加允许的频道

```bash
# 添加 general 频道
openclaw config set channels.discord.guilds.1324011180921983078.channels.general.allow true
```

---

## 📋 当前配置

```json
{
  "dm": {
    "enabled": true,
    "groupEnabled": false
  },
  "dmPolicy": "pairing",
  "guilds": {
    "1324011180921983078": {
      "requireMention": true,
      "channels": {
        "dr_worker": {
          "allow": true
        }
      }
    }
  },
  "groupPolicy": "allowlist"
}
```

**允许的频道：** 仅 `dr_worker`

---

## 💡 最佳实践

| 场景 | 推荐配置 |
|------|---------|
| **个人使用** | dmPolicy: pairing + 白名单 |
| **小团队** | 白名单 + requireMention: true |
| **公开服务器** | 只允许特定频道 + 严格白名单 |
| **测试环境** | 可以临时放宽 |

---

## 📊 日志示例

### ✅ 成功处理

```
processing mention: userId=1282978424482299956 
channelId=1465629871609745481 
content="@Bot 帮我查天气"
```

---

### ❌ 跳过（没@）

```
discord: skipping guild message (reason: no-mention)
```

---

### ❌ 跳过（频道不允许）

```
discord: skipping guild message (reason: channel-not-allowed)
```

---

## 🎯 总结

| 消息类型 | 响应条件 |
|---------|---------|
| **私信** | 需要配对 |
| **群聊@Bot** | 频道在白名单 |
| **群聊不@** | 永远不响应 |

**推荐用法：** 在 `dr_worker` 频道 @Bot，不需要配对！

---

## 📝 更新日志

- **2026-02-20**: 初始记录，Discord 私信 vs 群聊@Bot 机制详解
