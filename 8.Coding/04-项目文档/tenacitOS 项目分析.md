# tenacitOS 项目分析

> 创建时间：2026-02-24  
> 最后更新：2026-02-24  
> 标签：#OpenClaw #Dashboard #Next.js #ProjectAnalysis

---

## 📌 项目概览

| 属性 | 值 |
|------|-----|
| **项目名称** | tenacitOS (Mission Control Dashboard) |
| **作者** | carlosazaustre |
| **仓库** | https://github.com/carlosazaustre/tenacitOS |
| **用途** | OpenClaw AI Agent 实时监控仪表盘 |
| **技术栈** | Next.js + React 19 + Tailwind CSS v4 |
| **定位** | OpenClaw 任务控制中心 |

---

## 🎯 核心功能

### 1️⃣ 系统监控 📊
- 实时 VPS 指标（CPU、内存、磁盘、网络）
- PM2/Docker 状态监控
- 资源使用趋势图

### 2️⃣ Agent 仪表盘 🤖
- 所有 Agent 列表
- 会话状态、Token 使用量
- 模型信息、活动状态
- 自动发现 Agent（从 openclaw.json）

### 3️⃣ 成本追踪 💰
- 实时成本分析
- SQLite 数据库存储
- 按 Agent 分类统计
- 每日成本趋势

### 4️⃣ Cron 管理器 ⏰
- 可视化 Cron 管理
- 每周时间线视图
- 运行历史记录
- 手动触发执行

### 5️⃣ 活动反馈 📋
- 实时 Agent 行动日志
- 活动热力图
- 统计图表
- 时间线展示

### 6️⃣ 记忆浏览器 🧠
- 探索 Agent 记忆文件
- 全文搜索
- 在线编辑
- 分类浏览

### 7️⃣ 文件浏览器 📁
- 工作区文件导航
- 文件预览
- 在线编辑
- 树形结构

### 8️⃣ 3D 办公室 🏢
- React Three Fiber 构建
- 每个 Agent 一个虚拟办公桌
- 可自定义 3D 头像（GLB 格式）
- 交互式场景

### 9️⃣ 终端查看器 📺
- 只读终端
- 安全状态命令
- 实时输出

### 🔟 认证系统 🔐
- 密码保护
- 速率限制
- 安全 Cookie
- HTTPS 自动检测

---

## 🏗️ 架构设计

### 数据流

```
OpenClaw 运行时
    ↓
openclaw.json + workspace 文件 + SQLite 日志
    ↓
TenacitOS API 路由 (自动发现)
    ↓
Next.js 前端 (实时展示)
    ↓
用户浏览器
```

### 目录结构

```
OpenClaw 安装目录 (~/.openclaw/)
├── openclaw.json          ← Agent 配置
├── workspace/             ← 主工作区
│   └── mission-control/   ← TenacitOS 安装位置
├── workspace-studio/      ← 子 Agent 工作区
├── workspace-infra/
└── logs/                  ← 日志文件
```

### 项目结构

```
mission-control/
├── src/
│ ├── app/
│ │ ├── (dashboard)/     # 仪表盘页面（受保护）
│ │ ├── api/             # API 路由
│ │ ├── login/           # 登录页面
│ │ └── office/          # 3D 办公室（未保护）
│ ├── components/
│ │ ├── TenacitOS/       # OS 风格 UI 外壳
│ │ └── Office3D/        # React Three Fiber 3D 办公室
│ ├── config/
│ │ └── branding.ts      # 品牌配置（从环境变量读取）
│ ├── hooks/
│ ├── lib/
│ └── styles/
├── public/
│ ├── models/            # 3D 头像文件 (GLB)
│ └── images/
├── data/
│ ├── cron-jobs.json
│ ├── activities.json
│ └── notifications.json
├── scripts/
│ ├── collect-usage.ts   # 成本数据收集
│ └── setup-cron.sh      # 定时任务设置
├── .env.example
├── .env.local           # 实际配置（gitignore）
└── package.json
```

---

## 📦 安装指南

### 前置要求

| 要求 | 版本 | 说明 |
|------|------|------|
| **Node.js** | 18+ | 测试通过 v22 |
| **OpenClaw** | 最新版 | 必须已安装并运行 |
| **PM2** | 可选 | 生产环境进程管理 |
| **Caddy/Nginx** | 可选 | HTTPS 反向代理 |

### 快速安装

```bash
# 1. 克隆到 OpenClaw 工作区
cd ~/.openclaw/workspace
git clone https://github.com/carlosazaustre/tenacitOS.git mission-control
cd mission-control

# 2. 安装依赖
npm install

# 3. 配置环境变量
cp .env.example .env.local
vim .env.local

# 4. 初始化数据文件
cp data/cron-jobs.example.json data/cron-jobs.json
cp data/activities.example.json data/activities.json
cp data/notifications.example.json data/notifications.json
cp data/configured-skills.example.json data/configured-skills.json
cp data/tasks.example.json data/tasks.json

# 5. 运行
npm run dev          # 开发模式 → http://localhost:3000
npm run build && npm start  # 生产模式
```

---

## 🔧 配置说明

### 环境变量 (.env.local)

```bash
# --- 认证（必需）---
# 登录密码
ADMIN_PASSWORD=your-secure-password-here

# Cookie 签名密钥（32 字符）
# 生成：openssl rand -base64 32
AUTH_SECRET=your-random-32-char-secret-here

# --- OpenClaw 路径（可选）---
# OPENCLAW_DIR=/root/.openclaw

# --- 品牌定制 ---
NEXT_PUBLIC_AGENT_NAME=Mission Control
NEXT_PUBLIC_AGENT_EMOJI=🤖
NEXT_PUBLIC_AGENT_DESCRIPTION=Your AI co-pilot, powered by OpenClaw
NEXT_PUBLIC_AGENT_LOCATION=Madrid, Spain
NEXT_PUBLIC_BIRTH_DATE=2026-01-01
NEXT_PUBLIC_AGENT_AVATAR=/avatar.jpg

# --- 所有者信息 ---
NEXT_PUBLIC_OWNER_USERNAME=your-username
NEXT_PUBLIC_OWNER_EMAIL=your-email@example.com
NEXT_PUBLIC_TWITTER_HANDLE=@username
NEXT_PUBLIC_COMPANY_NAME=MISSION CONTROL, INC.
NEXT_PUBLIC_APP_TITLE=Mission Control
```

### 生成安全密钥

```bash
# Auth Secret
openssl rand -base64 32

# 密码（或使用密码管理器）
openssl rand -base64 18
```

### 3D 办公室配置

编辑 `src/components/Office3D/agentsConfig.ts`:

```typescript
export const AGENTS: AgentConfig[] = [
  {
    id: "main",           // 必须匹配 workspace ID
    name: "Main Agent",   // 显示名称
    emoji: "🤖",
    position: [0, 0, 0],  // 3D 位置
    color: "#FFCC00",
    role: "Main Agent",
  },
  // 添加你的子 Agent
  {
    id: "code",
    name: "代码专家",
    emoji: "💻",
    position: [2, 0, 0],
    color: "#4CAF50",
    role: "Coding Agent",
  }
];
```

### 自定义 3D 头像

```
public/models/
├── main.glb    ← main agent 头像
├── studio.glb  ← workspace-studio agent
└── infra.glb   ← workspace-infra agent
```

**要求**: Ready Player Me GLB 格式，文件名必须匹配 Agent ID。

---

## 🚀 部署方案

### 方案 1: PM2（推荐）

```bash
# 构建
npm run build

# 启动
pm2 start npm --name "mission-control" -- start

# 保存配置
pm2 save

# 开机自启
pm2 startup
```

### 方案 2: Systemd

创建 `/etc/systemd/system/mission-control.service`:

```ini
[Unit]
Description=TenacitOS — OpenClaw Mission Control
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/.openclaw/workspace/mission-control
ExecStart=/usr/bin/npm start
Restart=always
RestartSec=10
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable mission-control
sudo systemctl start mission-control
```

### 方案 3: Caddy 反向代理

创建 `Caddyfile`:

```
mission-control.yourdomain.com {
    reverse_proxy localhost:3000
}
```

HTTPS 会自动启用，Cookie 的 `secure` 标志会自动设置。

---

## 📊 功能截图

| 功能 | 说明 |
|------|------|
| **Dashboard** | 活动概览、Agent 状态、天气组件 |
| **Session History** | 所有 OpenClaw 会话、Token 使用量 |
| **Costs & Analytics** | 每日成本趋势、按 Agent 分类 |
| **System Monitor** | 实时 CPU、内存、磁盘、网络 |
| **Office 3D** | 交互式 3D 办公室、虚拟化身 |

---

## ✅ 优点分析

| 优势 | 说明 |
|------|------|
| **零配置** | 自动发现 Agent，无需手动配置 |
| **轻量** | 无额外数据库，直接读文件 |
| **实时** | WebSocket 实时更新 |
| **美观** | 3D 办公室、热力图、图表 |
| **安全** | 密码保护、速率限制、HTTPS |
| **可扩展** | 自定义 Agent 头像、颜色、位置 |
| **集成度高** | 与 OpenClaw 深度集成 |

---

## ⚠️ 注意事项

| 项目 | 说明 |
|------|------|
| **Node.js 版本** | 需要 18+ (测试通过 v22) |
| **OpenClaw 依赖** | 必须先安装并运行 OpenClaw |
| **内存占用** | Next.js + 3D 渲染，约 200-500MB |
| **端口** | 默认 3000，可能冲突 |
| **首次构建** | 约 2-5 分钟 |
| **数据收集** | 需要运行 `scripts/collect-usage.ts` |

---

## 💡 使用场景推荐

| 场景 | 推荐度 | 理由 |
|------|-------|------|
| **多 Agent 管理** | ⭐⭐⭐⭐⭐ | 一目了然所有 Agent 状态 |
| **成本监控** | ⭐⭐⭐⭐⭐ | 实时追踪 Token 使用成本 |
| **生产环境** | ⭐⭐⭐⭐ | 完整的监控和告警 |
| **个人开发** | ⭐⭐⭐ | 可能过于重量级 |
| **团队协作** | ⭐⭐⭐⭐⭐ | 多人共享监控面板 |

---

## 🔗 相关资源

- **GitHub**: https://github.com/carlosazaustre/tenacitOS
- **OpenClaw**: https://openclaw.ai
- **文档**: `/docs/` 目录
- **成本追踪**: `docs/COST-TRACKING.md`
- **3D 头像**: `public/models/README.md`

---

## 📝 安装检查清单

- [ ] OpenClaw 已安装并运行
- [ ] Node.js 18+ 已安装
- [ ] 克隆项目到正确位置
- [ ] 安装 npm 依赖
- [ ] 配置 `.env.local`
- [ ] 生成 `AUTH_SECRET`
- [ ] 设置 `ADMIN_PASSWORD`
- [ ] 初始化数据文件
- [ ] 测试开发模式运行
- [ ] 配置生产部署（PM2/Systemd）
- [ ] 配置反向代理（可选）
- [ ] 设置成本数据收集脚本
- [ ] 自定义 Agent 配置（可选）
- [ ] 上传 3D 头像（可选）

---

## 🎯 下一步行动

1. **评估需求**: 是否需要这个 Dashboard？
2. **测试安装**: 开发模式试运行
3. **配置定制**: 品牌、Agent、3D 头像
4. **生产部署**: PM2 或 Systemd
5. **监控配置**: 成本收集、Cron 任务

---

*最后更新：2026-02-24*
