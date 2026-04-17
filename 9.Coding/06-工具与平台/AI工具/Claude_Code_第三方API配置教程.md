# Claude Code 第三方 API 配置教程

> 基于 QNAI GC (api.qnaigc.com) 的 Claude API 代理配置

---

## 方案概述

通过本地 Node.js 代理，将 Claude Code 的请求转发到第三方 API 平台（QNAI GC），实现：
- 不直接使用 Anthropic 官方 API
- 通过国内/第三方平台访问 Claude
- 可能的成本优势或网络优化

**架构：**
```
Claude Code → localhost:18080 → anthropic-proxy.js → api.qnaigc.com/bypass/anthropic → Claude 模型
```

---

## 步骤一：安装 Claude Code

### 1.1 安装官方 CLI

```bash
# 使用 npm 安装
npm install -g @anthropic-ai/claude-code

# 或使用 npx 直接运行
npx @anthropic-ai/claude-code
```

### 1.2 验证安装

```bash
claude --version
```

---

## 步骤二：创建 API 代理

### 2.1 创建代理脚本

创建文件 `~/.local/bin/anthropic-proxy.js`：

```bash
mkdir -p ~/.local/bin
cat > ~/.local/bin/anthropic-proxy.js << 'EOF'
#!/usr/bin/env node
// Proxy that intercepts /models endpoint for Claude Code compatibility
const http = require('http');
const https = require('https');

// ============ 配置区域 ============
const TARGET_HOST = 'api.qnaigc.com';           // 第三方 API 平台
const TARGET_BASE = '/bypass/anthropic';        // API 路径前缀
const PORT = parseInt(process.env.PROXY_PORT || '18080');  // 本地监听端口
// ==================================

// 假模型列表（用于响应 /models 请求）
const FAKE_MODELS = {
  data: [
    { id: 'claude-sonnet-4-6', type: 'model', display_name: 'Claude Sonnet 4.6' },
    { id: 'claude-sonnet-4-20250514', type: 'model', display_name: 'Claude Sonnet 4' },
    { id: 'claude-opus-4-6', type: 'model', display_name: 'Claude Opus 4.6' },
    { id: 'claude-4.6-sonnet', type: 'model', display_name: 'Claude 4.6 Sonnet' },
    { id: 'claude-4.6-opus', type: 'model', display_name: 'Claude 4.6 Opus' },
  ],
  has_more: false,
  first_id: 'claude-sonnet-4-6',
  last_id: 'claude-4.6-opus',
};

const server = http.createServer((req, res) => {
  const url = req.url || '/';
  console.log(`[${req.method}] ${url}`);

  // 拦截 /models 请求，返回假模型列表
  if (url === '/models' || url.startsWith('/models?')) {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(FAKE_MODELS));
    return;
  }

  // 转发其他请求到上游 API
  const targetPath = TARGET_BASE + url;
  const headers = { ...req.headers, host: TARGET_HOST };
  delete headers['connection'];

  const options = {
    hostname: TARGET_HOST,
    port: 443,
    path: targetPath,
    method: req.method,
    headers,
  };

  const proxyReq = https.request(options, (proxyRes) => {
    res.writeHead(proxyRes.statusCode || 500, proxyRes.headers);
    proxyRes.pipe(res);
  });

  proxyReq.on('error', (err) => {
    console.error('Proxy error:', err.message);
    res.writeHead(502);
    res.end('Proxy Error: ' + err.message);
  });

  req.pipe(proxyReq);
});

server.listen(PORT, '127.0.0.1', () => {
  console.log(`Anthropic API proxy on http://127.0.0.1:${PORT}`);
  console.log(`Forwarding to https://${TARGET_HOST}${TARGET_BASE}/...`);
});
EOF

chmod +x ~/.local/bin/anthropic-proxy.js
```

### 2.2 自定义配置（可选）

如需修改上游 API 或端口，编辑脚本中的配置区域：

```javascript
// ============ 配置区域 ============
const TARGET_HOST = 'your-api-provider.com';    // 你的第三方 API 平台
const TARGET_BASE = '/v1/anthropic';            // API 路径前缀
const PORT = 18080;                             // 本地端口
// ==================================
```

---

## 步骤三：配置 Claude Code

### 3.1 创建配置文件

```bash
mkdir -p ~/.claude
cat > ~/.claude/settings.json << 'EOF'
{
  "env": {
    "ANTHROPIC_BASE_URL": "http://127.0.0.1:18080"
  },
  "permissions": {
    "allow": [],
    "deny": []
  },
  "model": "sonnet[1m]",
  "skipDangerousModePermissionPrompt": true
}
EOF
```

### 3.2 配置说明

| 配置项 | 说明 |
|--------|------|
| `ANTHROPIC_BASE_URL` | 指向本地代理地址 |
| `model` | 使用的模型（`sonnet[1m]` 表示 1M 上下文的 Sonnet）|
| `skipDangerousModePermissionPrompt` | 跳过危险操作确认提示 |

---

## 步骤四：配置 API Key

### 4.1 获取 API Key

从 QNAI GC 平台（或你的第三方 API 提供商）获取 API Key。

### 4.2 设置环境变量

**临时设置（当前终端）：**
```bash
export ANTHROPIC_API_KEY="your-api-key-from-qnaigc"
```

**永久设置（推荐）：**
```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
echo 'export ANTHROPIC_API_KEY="your-api-key-from-qnaigc"' >> ~/.bashrc
source ~/.bashrc
```

---

## 步骤五：启动代理并测试

### 5.1 启动代理

```bash
# 前台运行（测试时使用）
node ~/.local/bin/anthropic-proxy.js

# 后台运行（推荐）
nohup node ~/.local/bin/anthropic-proxy.js > ~/.local/share/anthropic-proxy.log 2>&1 &
```

### 5.2 验证代理运行

```bash
# 检查端口监听
ss -tlnp | grep 18080

# 测试代理响应
curl http://127.0.0.1:18080/models
```

预期输出：
```json
{"data":[{"id":"claude-sonnet-4-6",...}],"has_more":false,...}
```

### 5.3 启动 Claude Code

```bash
claude
```

---

## 步骤六：配置开机自启（可选）

### 6.1 Systemd 服务（Linux）

创建服务文件：

```bash
sudo tee /etc/systemd/system/anthropic-proxy.service << 'EOF'
[Unit]
Description=Anthropic API Proxy for Claude Code
After=network.target

[Service]
Type=simple
User=dr
ExecStart=/usr/bin/node /home/dr/.local/bin/anthropic-proxy.js
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# 启用并启动服务
sudo systemctl daemon-reload
sudo systemctl enable anthropic-proxy
sudo systemctl start anthropic-proxy
```

### 6.2 验证服务状态

```bash
sudo systemctl status anthropic-proxy
```

---

## 故障排查

### 问题：Claude Code 无法连接

**检查步骤：**
1. 代理是否运行：`ss -tlnp | grep 18080`
2. 代理是否可访问：`curl http://127.0.0.1:18080/models`
3. 配置是否正确：`cat ~/.claude/settings.json`
4. API Key 是否设置：`echo $ANTHROPIC_API_KEY`

### 问题：API 返回 401/403

- 检查 API Key 是否正确
- 确认第三方平台账户余额/权限
- 查看代理日志：`tail -f ~/.local/share/anthropic-proxy.log`

### 问题：模型不可用

- 检查 `FAKE_MODELS` 中的模型 ID 是否与上游平台匹配
- 可能需要根据实际支持的模型调整假模型列表

---

## 进阶配置

### 多平台切换

创建多个代理脚本，使用不同端口：

```bash
# 平台 A
PROXY_PORT=18080 node ~/.local/bin/anthropic-proxy-a.js

# 平台 B
PROXY_PORT=18081 node ~/.local/bin/anthropic-proxy-b.js
```

切换时修改 `~/.claude/settings.json` 中的 `ANTHROPIC_BASE_URL` 端口。

### 日志记录

修改代理脚本，添加详细日志：

```javascript
// 在 createServer 中添加
const fs = require('fs');
const logFile = fs.createWriteStream('/var/log/anthropic-proxy.log', { flags: 'a' });

// 在请求处理中
logFile.write(`[${new Date().toISOString()}] ${req.method} ${url}\n`);
```

---

## 参考

- **Claude Code 官方文档**：https://docs.anthropic.com/en/docs/claude-code/overview
- **Anthropic API 文档**：https://docs.anthropic.com/en/api/getting-started
- **QNAI GC 平台**：https://api.qnaigc.com（需注册获取 API Key）

---

## 总结

| 组件 | 路径/命令 |
|------|-----------|
| 代理脚本 | `~/.local/bin/anthropic-proxy.js` |
| Claude 配置 | `~/.claude/settings.json` |
| 环境变量 | `ANTHROPIC_API_KEY` |
| 启动代理 | `node ~/.local/bin/anthropic-proxy.js` |
| 启动 Claude | `claude` |
