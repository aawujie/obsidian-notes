# OpenClaw 配置 — 自定义 API 和 Skills

> OpenClaw 是开源 AI coding agent，支持多模型提供商、自定义 API、技能系统。

## 安装

```bash
npm install -g openclaw@latest
openclaw --version
```

需要 Node 22+。

## 自定义 OpenAI 兼容 API

配置文件：`~/.openclaw/openclaw.json`

```json
{
  "gateway": { "mode": "local", "auth": { "mode": "none" } },
  "models": {
    "mode": "merge",
    "providers": {
      "deeproute": {
        "baseUrl": "https://ai-coding-ali.deeproute.cn/v1",
        "apiKey": "YOUR_KEY",
        "api": "openai-completions",
        "models": [
          { "id": "qwen-coder-plus", "name": "Qwen Coder+" },
          { "id": "deepseek-v3", "name": "DeepSeek V3" }
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": { "primary": "deeproute/qwen-coder-plus" }
    }
  }
}
```

关键字段：
- `baseUrl` — OpenAI 兼容 API 地址
- `api` — 必须是 `"openai-completions"`（OpenAI 兼容协议）
- `models` — 手动列出可用模型（API 可能不暴露 `/v1/models`）

## 加载 Cursor Skills

使用 `skills.load.extraDirs` 让 OpenClaw 加载 Cursor 的 skills 目录：

```json
{
  "skills": {
    "load": {
      "extraDirs": ["/home/dr/.cursor/skills"],
      "watch": true
    }
  }
}
```

**不要用软链**——OpenClaw 有安全检查，会拦截解析到配置目录外部的软链。`extraDirs` 是官方推荐方式。

## 常用命令

```bash
openclaw gateway --force          # 启动 Gateway
openclaw tui                      # 终端交互
openclaw models list              # 查看模型
openclaw models set <provider/model>  # 切换默认模型
openclaw skills list              # 查看 skills
openclaw config validate          # 验证配置
openclaw status                   # 查看整体状态
```

## 踩坑

1. `gateway.auth` 必须是对象 `{ "mode": "none" }`，不能是字符串 `"none"`
2. 软链 skill 到 `~/.openclaw/skills/` 会被安全检查拦截，必须用 `extraDirs`
3. API 不暴露 `/v1/models` 时需要手动列出 models
4. 权限：`chmod 600 ~/.openclaw/openclaw.json && chmod 700 ~/.openclaw/`
