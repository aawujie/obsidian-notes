# ZeroClaw 安装配置指南

> 创建日期：2026-03-11
> 标签：#AI/Agent #ZeroClaw #OpenClaw #配置指南

---

## 🦀 ZeroClaw 是什么

**ZeroClaw** 是 OpenClaw 的 Rust 重写版本，主打轻量级和高性能。

| 特性 | OpenClaw | ZeroClaw |
|------|----------|----------|
| **语言** | TypeScript | Rust |
| **内存占用** | >1GB | **<5MB** |
| **启动速度** | >500s | **<10ms** |
| **二进制大小** | ~28MB | **~8.8MB** |
| **配置文件** | JSON5 | TOML |

---

## 📦 安装方法

### 方法 1：Homebrew（推荐 macOS）

```bash
brew install zeroclaw
```

### 方法 2：一键安装脚本

```bash
curl -fsSL https://zeroclawlabs.ai/install.sh | bash
```

### 方法 3：源码编译

```bash
git clone https://github.com/zeroclaw-labs/zeroclaw.git
cd zeroclaw
./bootstrap.sh
```

---

## ⚙️ 配置文件

**配置路径：** `~/.zeroclaw/config.toml`

### 基本配置示例

```toml
# API 配置
api_key = "sk-xxx"
default_provider = "custom:https://api.example.com/v1"
provider_api = "open-ai-chat-completions"  # 关键！指定 API 模式
default_model = "qwen3.5-plus"
default_temperature = 0.7

# Agent 配置
[agent]
compact_context = true
max_tool_iterations = 20
max_history_messages = 50
parallel_tools = false

# Gateway 配置
[gateway]
port = 42617
host = "127.0.0.1"
```

### Provider 配置（自定义端点）

```toml
[model_providers."custom:https://api.example.com/v1"]
name = "openai"
base_url = "https://api.example.com/v1"
wire_api = "chat_completions"
api_key = "sk-xxx"
```

---

## 🚀 常用命令

| 命令 | 说明 |
|------|------|
| `zeroclaw agent -m "消息"` | 单次对话 |
| `zeroclaw agent` | 交互模式 |
| `zeroclaw gateway` | 启动 Gateway 服务 |
| `zeroclaw daemon` | 后台运行（Gateway + 心跳 + 调度） |
| `zeroclaw status` | 查看状态 |
| `zeroclaw config show` | 查看配置（JSON） |
| `zeroclaw config set key value` | 修改配置 |

---

## 🌐 Dashboard

启动 Gateway 后访问：

```bash
zeroclaw gateway
# Dashboard: http://127.0.0.1:42617/
```

**API 端点：**
- `POST /api/chat` — 聊天接口
- `POST /v1/chat/completions` — OpenAI 兼容接口
- `GET /v1/models` — 模型列表
- `GET /health` — 健康检查

---

## ⚠️ 踩坑记录

### 问题 1：阿里云 Coding 端点 405 错误

**错误信息：**
```
Coding Plan is currently only available for Coding Agents
```

**原因：** ZeroClaw 的 OpenAI provider 实现和 OpenClaw 不同，请求格式有差异。

**解决方案：**
1. 使用普通通义千问端点（非 coding 专用）
2. 或使用 DMXAPI 等第三方代理
3. 或在配置中指定 `provider_api = "open-ai-chat-completions"`

**配置示例：**
```toml
# 方案 1：用 DMXAPI
api_key = "sk-PShK70oQsuwjgffho0CEQAeoxwqk4LBQ1bdAmR7rXZWVYvZd"
default_provider = "custom:https://www.dmxapi.cn/v1"
provider_api = "open-ai-chat-completions"
default_model = "qwen3.5-plus"

# 方案 2：用阿里云普通端点
api_key = "sk-xxx"
default_provider = "custom:https://dashscope.aliyuncs.com/compatible-mode/v1"
provider_api = "open-ai-chat-completions"
```

### 问题 2：Gateway 端口被占用

**错误：** `Address already in use (os error 48)`

**解决：**
```bash
# 查看占用进程
ps aux | grep zeroclaw

# 杀掉进程
pkill -f zeroclaw

# 或换端口
zeroclaw config set gateway.port 42618
```

### 问题 3：后台运行

```bash
# 方法 1：nohup
nohup zeroclaw gateway > /tmp/zeroclaw.log 2>&1 &

# 方法 2：screen/tmux
screen -S zeroclaw
zeroclaw gateway
# Ctrl+A 然后 D 退出

# 方法 3：macOS LaunchAgent（永久）
# 创建 ~/Library/LaunchAgents/ai.zeroclaw.gateway.plist
```

---

## 🔄 从 OpenClaw 迁移

```bash
# 预览迁移内容
zeroclaw migrate openclaw --dry-run

# 正式迁移（配置 + 记忆 + Agents）
zeroclaw migrate openclaw
```

**迁移内容：**
- Agents 配置
- Memory 数据
- 会话历史

---

## 📊 与 OpenClaw 配置对比

| 配置项 | OpenClaw (JSON5) | ZeroClaw (TOML) |
|--------|------------------|-----------------|
| **API Key** | `auth.profiles.*.apiKey` | `api_key` |
| **Provider** | `models.providers.*.baseUrl` | `default_provider = "custom:..."` |
| **Model** | `agents.defaults.model.primary` | `default_model` |
| **工具限制** | `tools.deny` | `agent.denied_tools` |
| **端口** | `gateway.port` | `gateway.port` |

---

## 🎯 使用场景

### 适合 ZeroClaw
- 资源受限环境（树莓派、小内存 VPS）
- 需要快速启动的场景
- 追求轻量级部署

### 适合 OpenClaw
- 需要完整功能生态
- 已有 OpenClaw 工作流
- 需要更多中国本地化支持

---

## 📚 相关链接

- **官网**: https://zeroclawlabs.ai
- **GitHub**: https://github.com/zeroclaw-labs/zeroclaw
- **文档**: https://docs.openclaw.ai (部分通用)
- **Telegram**: @zeroclawlabs

---

## 💡 小贴士

1. **配置热重载**：修改 config.toml 后需要重启 Gateway
2. **日志查看**：`zeroclaw logs --follow`
3. **诊断工具**：`zeroclaw doctor`
4. **模型切换**：`zeroclaw models list`

---

*最后更新：2026-03-11*
