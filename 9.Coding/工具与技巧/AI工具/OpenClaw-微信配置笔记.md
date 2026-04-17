# OpenClaw 微信配置笔记

> 记录 OpenClaw 接入微信（WeChat）的完整配置流程

---

## 配置概览

| 项目 | 值 |
|-----|-----|
| 账号 ID | `bf0f22f2bac7-im-bot` |
| 用户 ID | `o9cq803b6DrCh5LqQr85vojqnbJI@im.wechat` |
| 基础 URL | `https://ilinkai.weixin.qq.com` |
| 配置路径 | `~/.openclaw/openclaw-weixin/` |

---

## 配置步骤

### 1. 前提条件

- 已安装 OpenClaw Gateway
- 已创建微信应用（通过[微信对话开放平台](https://openai.weixin.qq.com/)）

### 2. 获取微信 Token

1. 访问 [微信对话开放平台](https://openai.weixin.qq.com/)
2. 创建应用并获取：
   - **Token**（格式：`xxx@im.bot:xxx`）
   - **User ID**（格式：`xxx@im.wechat`）

### 3. OpenClaw 配置

#### 3.1 初始化微信账号

```bash
# 方式1：通过 OpenClaw CLI
openclaw weixin add --token "YOUR_TOKEN" --user-id "YOUR_USER_ID"

# 方式2：直接编辑配置文件
mkdir -p ~/.openclaw/openclaw-weixin/accounts
```

#### 3.2 配置文件结构

```
~/.openclaw/openclaw-weixin/
├── accounts.json              # 账号列表
└── accounts/
    └── bf0f22f2bac7-im-bot.json    # 单个账号配置
```

#### 3.3 账号配置文件

**文件**：`~/.openclaw/openclaw-weixin/accounts/bf0f22f2bac7-im-bot.json`

```json
{
  "token": "bf0f22f2bac7@im.bot:0600004932709385a4c2eeba2a80b9913092c7",
  "savedAt": "2026-03-26T23:58:16.793Z",
  "baseUrl": "https://ilinkai.weixin.qq.com",
  "userId": "o9cq803b6DrCh5LqQr85vojqnbJI@im.wechat"
}
```

#### 3.4 账号列表文件

**文件**：`~/.openclaw/openclaw-weixin/accounts.json`

```json
[
  "bf0f22f2bac7-im-bot"
]
```

---

## 验证配置

### 检查 Gateway 状态

```bash
openclaw gateway status
```

### 查看微信账号

```bash
openclaw weixin list
```

### 测试消息收发

直接在微信中向配置的账号发送消息，OpenClaw 应该能收到并回复。

---

## 常见问题

### Q1: Token 过期怎么办？

需要重新从[微信对话开放平台](https://openai.weixin.qq.com/)获取新的 Token。

### Q2: 收不到消息？

检查：
1. Gateway 是否运行：`openclaw gateway status`
2. Token 是否正确
3. 微信应用是否已发布

### Q3: 如何配置多个微信账号？

在 `accounts.json` 中添加多个账号 ID，每个账号对应一个配置文件。

---

## 相关链接

- [OpenClaw 文档](https://docs.openclaw.ai)
- [微信对话开放平台](https://openai.weixin.qq.com/)
- [OpenClaw Gateway 配置](../OpenClaw配置-自定义API和Skills.md)

---

## 更新记录

| 日期 | 内容 |
|-----|------|
| 2026-03-27 | 初始配置完成，账号 `bf0f22f2bac7-im-bot` 已接入 |
