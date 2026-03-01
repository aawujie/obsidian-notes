# QuantumNous/new-api 项目分析

**创建时间**: 2026-02-25  
**来源**: https://github.com/QuantumNous/new-api  
**标签**: #AI #API #网关 #开源项目

---

## 🏷️ 项目定位

**统一的 AI 模型聚合与分发网关**，支持将各种 LLM 转换为 OpenAI/Claude/Gemini 兼容格式，用于个人和企业模型管理。

> ⚠️ **重要声明**
> - 仅用于**个人学习**，无稳定性或技术支持保证
> - 需遵守 OpenAI 条款及当地法律法规
> - 根据中国《生成式 AI 服务管理暂行办法》，**不得向公众提供未注册的生成式 AI 服务**

---

## 🚀 核心功能

| 功能 | 描述 |
|------|------|
| 🎨 新 UI | 现代化界面设计 |
| 🌍 多语言 | 简中/繁中/英/法/日 |
| 📈 数据看板 | 可视化控制台 + 统计分析 |
| 🔒 权限管理 | Token 分组、模型限制、用户管理 |
| 💰 计费系统 | 在线充值、按量计费、缓存计费 |
| 🔐 多种登录 | Discord/Telegram/LinuxDO/OIDC |

---

## 🔄 支持的 API 格式

| 类型 | 支持 |
|------|------|
| OpenAI Chat Completions | ✅ |
| OpenAI Responses | ✅ |
| OpenAI Realtime API | ✅ (含 Azure) |
| Claude Messages | ✅ |
| Google Gemini | ✅ |
| Rerank | ✅ (Cohere, Jina) |
| Midjourney | ✅ (通过 midjourney-proxy) |
| Suno 音乐 | ✅ |
| Dify ChatFlow | ✅ |

---

## 🧠 推理模式支持

### OpenAI 系列
- `o3-mini-high/medium/low`
- `gpt-5-high/medium/low`

### Claude
- `claude-3-7-sonnet-20250219-thinking`

### Gemini
- `gemini-2.5-flash-thinking/nothinking`
- `gemini-2.5-pro-thinking`
- 支持 `-low/-medium/-high` 后缀

---

## 🛠️ 部署方式

### Docker (推荐)
```bash
# SQLite 版本
docker run --name new-api -d --restart always \
  -p 3000:3000 \
  -e TZ=Asia/Shanghai \
  -v ./data:/data \
  calciumion/new-api:latest
```

### Docker Compose
```bash
git clone https://github.com/QuantumNous/new-api.git
cd new-api
nano docker-compose.yml
docker-compose up -d
```

---

## 📋 技术栈

| 组件 | 要求 |
|------|------|
| 数据库 | SQLite / MySQL ≥5.7.8 / PostgreSQL ≥9.6 |
| 容器 | Docker / Docker Compose |
| 缓存 | Redis (可选) |

---

## 🔑 关键环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `SESSION_SECRET` | 会话密钥 (多机部署必需) | - |
| `SQL_DSN` | 数据库连接字符串 | - |
| `REDIS_CONN_STRING` | Redis 连接字符串 | - |
| `STREAMING_TIMEOUT` | 流式超时 (秒) | 300 |
| `MAX_REQUEST_BODY_MB` | 最大请求体 (MB) | 32 |
| `AZURE_DEFAULT_API_VERSION` | Azure API 版本 | 2025-04-01-preview |

---

## 📚 文档资源

- 🚀 部署指南：https://docs.newapi.pro
- 📡 API 文档：https://docs.newapi.pro/en/docs/api
- 💬 社区：https://docs.newapi.pro/en/docs/support/community-interaction

---

## 🏗️ 架构本质（重要！）

### 核心答案：**API 聚合网关，不部署模型**

```
┌─────────────────────────────────────────────────────────────┐
│                     你的应用/客户端                          │
│              (前端/APP/其他服务)                             │
└─────────────────────┬───────────────────────────────────────┘
                      │ 请求：标准 OpenAI 格式
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  new-api (这个 repo)                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  渠道管理   │  │  计费系统   │  │  限流/鉴权  │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ 格式转换    │  │ 负载均衡    │  │ 失败重试    │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────┬───────────────────────────────────────┘
                      │ 转发请求
        ┌─────────────┼─────────────┬──────────────┐
        ▼             ▼             ▼              ▼
   ┌────────┐   ┌────────┐   ┌────────┐    ┌──────────┐
   │ OpenAI │   │ Claude │   │ Gemini │    │ 其他 API │
   │ 官方   │   │ 官方   │   │ 官方   │    │ 渠道...  │
   └────────┘   └────────┘   └────────┘    └──────────┘
   (远程 API)   (远程 API)   (远程 API)    (远程 API)
```

### ❌ 这个项目**不**做什么

| 误解 | 真相 |
|------|------|
| ❌ 本地部署 AI 模型 | ✅ **不部署模型**，只转发 API 请求 |
| ❌ 免费用 AI | ✅ 你还是要给 OpenAI/Claude 付费 |
| ❌ 破解/绕过限制 | ✅ 只是聚合管理，不破解任何东西 |
| ❌ 替代官方 API | ✅ 是官方 API 的**代理层** |

### 🏠 部署在哪里？

**必须部署在你自己的服务器/本地：**
- 本地电脑 (`localhost:3000`)
- 云服务器 (VPS)
- 内网服务器 (公司/家里)

**数据存在哪？**
- SQLite（默认）：存在本地 `./data` 目录
- MySQL/PostgreSQL：存在你自己的数据库
- Redis（可选）：缓存用

---

## 🎯 典型使用场景

### 场景 1：你有多个 API Key，想统一管理
```
你买了：
- 3 个 OpenAI Key（不同账号）
- 2 个 Claude Key
- 1 个 Gemini Key

配置进 new-api 后：
- 你的应用只调用 new-api 的 1 个 Key
- new-api 自动在后台轮换/负载均衡
- 某个 Key 超限了自动切换其他 Key
```

### 场景 2：团队共享，但要计费/限流
```
你是团队负责人：
- 买了 10 个 OpenAI Key
- 团队 20 人要用

用 new-api：
- 给每人发一个 Token
- 可以限制每人每天调用次数
- 可以统计每人用了多少 token
- 可以设置不同人访问不同模型
```

### 场景 3：格式统一
```
你的应用只想用 OpenAI 格式：
- 但想用 Claude 模型（更便宜/更好）
- new-api 把 Claude 响应转成 OpenAI 格式
- 你的代码不用改
```

---

## 🤔 决策指南：你需要它吗？

| 需求 | 需要吗？ |
|------|---------|
| 个人用 1 个 OpenAI Key | ❌ 不需要（直接用官方） |
| 个人有多个 Key 想轮换 | ✅ 需要 |
| 团队共享 API，要计费 | ✅ 需要 |
| 想统一不同 API 的格式 | ✅ 需要 |
| 想本地运行 AI 模型 | ❌ 没用（这是网关，不是模型） |

---

## 💡 总结

> **new-api = API 管理后台 + 代理网关**
>
> 你提供 API Key，它帮你**统一管理、计费、限流、格式转换**，但**不运行任何 AI 模型**。

这是一个 **One API 的现代化 fork 版本**，主要改进：

1. ✅ 全新 UI 界面
2. ✅ 更多模型格式支持 (Gemini/Claude/Rerank)
3. ✅ 完善的计费系统
4. ✅ 多种社交登录
5. ✅ 推理模式精细控制

**适用场景**: 需要统一管理多个 AI 模型 API 的个人或团队。

---

## 🔗 相关链接

- GitHub: https://github.com/QuantumNous/new-api
- Docker 镜像：`calciumion/new-api:latest`
- 赞助商：[JetBrains](https://www.jetbrains.com/?from=new-api) (提供开源开发许可)
