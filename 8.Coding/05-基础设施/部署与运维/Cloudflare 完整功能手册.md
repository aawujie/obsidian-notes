# Cloudflare 完整功能手册

> 创建时间：2026-02-24
> 最后更新：2026-02-24
> 标签：#Cloudflare #DevOps #API #CLI

---

## 📌 核心结论（TL;DR）

| 需求 | 能否自动化 | 推荐方式 |
|------|-----------|---------|
| **部署前端项目** | ✅ 能 | Wrangler CLI |
| **查看项目列表** | ✅ 能 | Wrangler CLI / Pages API |
| **管理域名 DNS** | ✅ 能 | cloudflare-toolkit / Zones API |
| **查看访问数据** | ❌ **不能** | **必须控制台** |
| **配置 SSL** | ✅ 能 | cloudflare-toolkit / SSL API |
| **配置防火墙** | ✅ 能 | cloudflare-toolkit / Firewall API |
| **查看实时日志** | ✅ 能 | Wrangler tail |
| **管理 Tunnel** | ✅ 能 | cloudflare-toolkit / Tunnel API |

---

## 🗺️ Cloudflare 功能全景图

```
Cloudflare
│
├── 1️⃣ 域名与 DNS          ← 基础服务
├── 2️⃣ CDN 与缓存          ← 加速服务
├── 3️⃣ 安全防护            ← DDoS/WAF/防火墙
├── 4️⃣ Workers & Pages     ← 无服务器部署 ⭐
├── 5️⃣ Tunnel (cloudflared) ← 内网穿透
├── 6️⃣ Analytics           ← 访问统计 ⚠️
├── 7️⃣ 数据库与存储        ← D1/KV/R2
└── 8️⃣ 其他服务            ← 域名注册/邮件路由等
```

---

## 📊 详细功能对照表

### 1️⃣ 域名与 DNS 管理

| 功能 | 控制台 | API | CLI | 自动化程度 |
|------|-------|-----|-----|-----------|
| 查看域名列表 | ✅ | ✅ Zones API | ✅ `cf.sh zones` | 🟢 完全可自动化 |
| 添加域名 | ✅ | ✅ Zones API | ❌ | 🟡 API 可自动化 |
| 查看 DNS 记录 | ✅ | ✅ DNS API | ✅ `cf.sh dns-list` | 🟢 完全可自动化 |
| 添加/修改 DNS | ✅ | ✅ DNS API | ✅ `cf.sh dns-create/update` | 🟢 完全可自动化 |
| 删除 DNS 记录 | ✅ | ✅ DNS API | ✅ `cf.sh dns-delete` | 🟢 完全可自动化 |
| 域名转移 | ✅ | ✅ Zones API | ❌ | 🟡 API 可自动化 |

**推荐工具**: `cloudflare-toolkit` skill

```bash
# 列出所有域名
bash ~/clawd/agents/main/skills/cloudflare-toolkit/scripts/cf.sh zones

# 查看 DNS 记录
bash ~/clawd/agents/main/skills/cloudflare-toolkit/scripts/cf.sh dns-list <zone_id>

# 添加 A 记录
bash ~/clawd/agents/main/skills/cloudflare-toolkit/scripts/cf.sh dns-create <zone_id> A www 1.2.3.4 true
```

---

### 2️⃣ CDN 与缓存

| 功能 | 控制台 | API | CLI | 自动化程度 |
|------|-------|-----|-----|-----------|
| 查看缓存状态 | ✅ | ✅ Cache API | ✅ `cf.sh cache-purge` | 🟢 完全可自动化 |
| 清除缓存 | ✅ | ✅ Cache API | ✅ `cf.sh cache-purge` | 🟢 完全可自动化 |
| 缓存规则配置 | ✅ | ✅ Cache Rules API | ❌ | 🟡 API 可自动化 |
| 页面规则 (Page Rules) | ✅ | ✅ Page Rules API | ✅ `cf.sh pagerules-list` | 🟢 完全可自动化 |

**推荐工具**: `cloudflare-toolkit` skill

```bash
# 清除所有缓存
bash ~/clawd/agents/main/skills/cloudflare-toolkit/scripts/cf.sh cache-purge <zone_id>

# 清除指定 URL 缓存
bash ~/clawd/agents/main/skills/cloudflare-toolkit/scripts/cf.sh cache-purge <zone_id> https://example.com/style.css
```

---

### 3️⃣ 安全防护

| 功能 | 控制台 | API | CLI | 自动化程度 |
|------|-------|-----|-----|-----------|
| SSL/TLS 模式 | ✅ | ✅ SSL API | ✅ `cf.sh ssl-get/set` | 🟢 完全可自动化 |
| 防火墙规则 | ✅ | ✅ Firewall API | ✅ `cf.sh firewall-list` | 🟢 完全可自动化 |
| DDoS 防护 | ✅ | ⚠️ 部分 API | ❌ | 🟡 部分可自动化 |
| WAF 规则 | ✅ | ✅ WAF API | ❌ | 🟡 API 可自动化 |
| 安全事件日志 | ✅ | ❌ | ❌ | 🔴 **必须控制台** |
| 机器人防护 | ✅ | ⚠️ 部分 API | ❌ | 🟡 部分可自动化 |

**推荐工具**: `cloudflare-toolkit` skill

```bash
# 查看 SSL 模式
bash ~/clawd/agents/main/skills/cloudflare-toolkit/scripts/cf.sh ssl-get <zone_id>

# 设置 SSL 为严格模式
bash ~/clawd/agents/main/skills/cloudflare-toolkit/scripts/cf.sh ssl-set <zone_id> strict

# 查看防火墙规则
bash ~/clawd/agents/main/skills/cloudflare-toolkit/scripts/cf.sh firewall-list <zone_id>
```

---

### 4️⃣ Workers & Pages（无服务器部署）⭐

| 功能 | 控制台 | API | CLI | 自动化程度 |
|------|-------|-----|-----|-----------|
| **查看项目列表** | ✅ | ✅ Pages API | ✅ `wrangler pages project list` | 🟢 完全可自动化 |
| **部署项目** | ✅ | ✅ Deployments API | ✅ `wrangler deploy` | 🟢 完全可自动化 |
| 查看部署历史 | ✅ | ✅ Deployments API | ✅ `wrangler deployments list` | 🟢 完全可自动化 |
| 回滚版本 | ✅ | ✅ Deployments API | ✅ `wrangler rollback` | 🟢 完全可自动化 |
| 删除项目 | ✅ | ✅ Pages API | ✅ `wrangler delete` | 🟢 完全可自动化 |
| 环境变量/Secrets | ✅ | ✅ Secrets API | ✅ `wrangler secret` | 🟢 完全可自动化 |
| 自定义域名绑定 | ✅ | ✅ Custom Domains API | ✅ `wrangler pages project domain` | 🟢 完全可自动化 |

**推荐工具**: `wrangler` CLI

```bash
# 列出所有 Pages 项目
wrangler pages project list

# 查看项目详情
wrangler pages project view <project-name>

# 部署前端项目
wrangler pages deploy ./dist --project-name=<project-name>

# 查看部署历史
wrangler deployments list --project-name=<project-name>

# 查看实时日志
wrangler tail --project-name=<project-name>

# 绑定自定义域名
wrangler pages project domain add <project-name> example.com
```

---

### 5️⃣ Tunnel（内网穿透）

| 功能 | 控制台 | API | CLI | 自动化程度 |
|------|-------|-----|-----|-----------|
| 查看 Tunnel 列表 | ✅ | ✅ Tunnel API | ✅ `cf.sh tunnels-list` | 🟢 完全可自动化 |
| 创建 Tunnel | ✅ | ✅ Tunnel API | ✅ `cf.sh tunnel-create` | 🟢 完全可自动化 |
| 配置 Ingress | ✅ | ✅ Tunnel API | ✅ `cf.sh update-ingress` | 🟢 完全可自动化 |
| 获取 Token | ✅ | ✅ Tunnel API | ✅ `cf.sh tunnel-token` | 🟢 完全可自动化 |
| 启动 Tunnel | ❌ | ❌ | ✅ `cloudflared tunnel run` | 🟢 CLI 可自动化 |
| 删除 Tunnel | ✅ | ✅ Tunnel API | ✅ `cf.sh tunnel-delete` | 🟢 完全可自动化 |

**推荐工具**: `cloudflare-toolkit` skill + `cloudflared` 二进制

```bash
# 列出所有 Tunnel
bash ~/clawd/agents/main/skills/cloudflare-toolkit/scripts/cf.sh tunnels-list

# 创建 Tunnel
bash ~/clawd/agents/main/skills/cloudflare-toolkit/scripts/cf.sh tunnel-create my-tunnel

# 配置 Ingress 规则
bash ~/clawd/agents/main/skills/cloudflare-toolkit/scripts/cf.sh update-ingress --hostname app.example.com --service http://localhost:3000

# 获取运行 Token
bash ~/clawd/agents/main/skills/cloudflare-toolkit/scripts/cf.sh tunnel-token my-tunnel

# 启动 Tunnel（需要 cloudflared 二进制）
cloudflared tunnel run --token <token>
```

---

### 6️⃣ Analytics（访问统计）⚠️

| 功能 | 控制台 | API | CLI | 自动化程度 |
|------|-------|-----|-----|-----------|
| **访问量 (PV/UV)** | ✅ | ✅ GraphQL API* | ⚠️ 复杂查询 | 🟡 **可自动化（但复杂）** |
| **带宽使用** | ✅ | ✅ GraphQL API* | ⚠️ 复杂查询 | 🟡 **可自动化（但复杂）** |
| **请求数** | ✅ | ✅ GraphQL API* | ⚠️ 复杂查询 | 🟡 **可自动化（但复杂）** |
| **缓存命中率** | ✅ | ✅ GraphQL API* | ⚠️ 复杂查询 | 🟡 **可自动化（但复杂）** |
| **错误率** | ✅ | ✅ GraphQL API* | ⚠️ 复杂查询 | 🟡 **可自动化（但复杂）** |
| **地理位置分布** | ✅ | ✅ GraphQL API* | ⚠️ 复杂查询 | 🟡 **可自动化（但复杂）** |
| **设备/浏览器分布** | ✅ | ✅ GraphQL API* | ⚠️ 复杂查询 | 🟡 **可自动化（但复杂）** |
| **防火墙事件** | ✅ | ✅ GraphQL API* | ⚠️ 复杂查询 | 🟡 **可自动化（但复杂）** |

> ⚠️ **重要说明**:
> - ✅ Cloudflare 提供 **GraphQL Analytics API** 可以访问分析数据
> - ⚠️ **但是**：需要 API Token 有 **Analytics:Read** 权限
> - ⚠️ GraphQL 查询语法复杂，不如控制台直观
> - ❌ 旧的 Zone Analytics API (`/zones/{id}/analytics/dashboard`) 已下线

**方式 1: 控制台（推荐）**
```
https://dash.cloudflare.com/
→ 点击域名 → Analytics & Logs
```

**方式 2: GraphQL API（需要权限）**

1. **创建 Token 时需要添加权限**:
   - 访问：https://dash.cloudflare.com/profile/api-tokens
   - 创建自定义 Token
   - 添加权限：**Analytics** → **Read**

2. **查询示例**:
```bash
curl -X POST "https://api.cloudflare.com/client/v4/graphql" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "query { viewer { zones(filter: {zoneTag: \"example.com\"}) { httpRequests1dGroups(limit: 7) { sum { requests pageViews } dimensions { date } } } } }"
  }'
```

3. **如果 Token 没有 Analytics 权限会返回**:
```json
{"errors": [{"message": "error parsing args for \"httpRequests1dGroups\": filter: not an object"}]}
```

---

### 7️⃣ 数据库与存储（D1/KV/R2）

| 功能 | 控制台 | API | CLI | 自动化程度 |
|------|-------|-----|-----|-----------|
| 查看 KV 命名空间 | ✅ | ✅ KV API | ✅ `wrangler kv:namespace list` | 🟢 完全可自动化 |
| KV 读写 | ✅ | ✅ KV API | ✅ `wrangler kv:key put/get` | 🟢 完全可自动化 |
| 查看 D1 数据库 | ✅ | ✅ D1 API | ✅ `wrangler d1 list` | 🟢 完全可自动化 |
| D1 SQL 查询 | ✅ | ✅ D1 API | ✅ `wrangler d1 execute` | 🟢 完全可自动化 |
| 查看 R2 存储桶 | ✅ | ✅ R2 API | ✅ `wrangler r2 bucket list` | 🟢 完全可自动化 |
| R2 对象操作 | ✅ | ✅ R2 API | ✅ `wrangler r2 object put/get` | 🟢 完全可自动化 |

**推荐工具**: `wrangler` CLI

```bash
# KV 操作
wrangler kv:namespace list
wrangler kv:key put <namespace> <key> <value>
wrangler kv:key get <namespace> <key>

# D1 操作
wrangler d1 list
wrangler d1 execute <database> --query="SELECT * FROM users"

# R2 操作
wrangler r2 bucket list
wrangler r2 object put <bucket>/<key> --file=./file.txt
```

---

### 8️⃣ 其他服务

| 功能 | 控制台 | API | CLI | 自动化程度 |
|------|-------|-----|-----|-----------|
| 域名注册 | ✅ | ✅ Registrar API | ❌ | 🟡 API 可自动化 |
| 邮件路由 | ✅ | ✅ Email Routing API | ❌ | 🟡 API 可自动化 |
| 流媒体 (Stream) | ✅ | ✅ Stream API | ❌ | 🟡 API 可自动化 |
| Images 优化 | ✅ | ✅ Images API | ❌ | 🟡 API 可自动化 |
| Logs 日志分析 | ✅ | ⚠️ Logpush API | ❌ | 🟡 部分可自动化 |
| 账单/用量 | ✅ | ❌ | ❌ | 🔴 **必须控制台** |

---

## 🛠️ 工具链总结

### 推荐的 CLI 工具

| 工具 | 用途 | 安装方式 |
|------|------|---------|
| **Wrangler** | Workers/Pages/KV/D1/R2 | `npm install -g wrangler` |
| **cloudflared** | Tunnel | `brew install cloudflared` |
| **cloudflare-toolkit** | DNS/SSL/防火墙/缓存 | ClawHub skill |

---

## 📦 OpenClaw Skills 功能对照表

你下载的 4 个 Cloudflare 相关 Skills：

| Skill | 状态 | 功能范围 | 推荐度 |
|-------|------|---------|--------|
| **cloudflare-toolkit** | ✅ 已安装 | DNS + SSL + 防火墙 + 缓存 + Tunnel | ⭐⭐⭐⭐⭐ 保留 |
| **wrangler** | ⏳ 待安装 | Workers + Pages + KV + D1 + R2 | ⭐⭐⭐⭐⭐ 推荐安装 |
| **cloudflare-api** | ⏳ 待安装 | DNS + Tunnel + Zones | ⭐⭐⭐ 可选（功能重叠） |
| **domain-dns-ops** | ⏳ 待安装 | 批量域名迁移（别人的定制） | ❌ 删除 |

---

### Skills 详细功能矩阵

| 功能 | cloudflare-toolkit | wrangler | cloudflare-api | domain-dns-ops |
|------|:-----------------:|:--------:|:--------------:|:--------------:|
| **查看域名列表** | ✅ | ❌ | ✅ | ✅ |
| **管理 DNS 记录** | ✅ | ❌ | ✅ | ✅ |
| **SSL 配置** | ✅ | ❌ | ❌ | ❌ |
| **防火墙规则** | ✅ | ❌ | ❌ | ❌ |
| **清除缓存** | ✅ | ❌ | ❌ | ❌ |
| **Tunnel 管理** | ✅ | ❌ | ✅ | ❌ |
| **部署 Workers** | ❌ | ✅ | ❌ | ❌ |
| **部署 Pages** | ❌ | ✅ | ❌ | ❌ |
| **查看项目列表** | ❌ | ✅ | ❌ | ❌ |
| **KV/D1/R2** | ❌ | ✅ | ❌ | ❌ |
| **查看访问数据** | ❌ | ❌ | ❌ | ❌ |

---

### 每个 Skill 的命令示例

#### cloudflare-toolkit（已安装）
```bash
# 路径：~/clawd/agents/main/skills/cloudflare-toolkit/scripts/cf.sh

# 查看域名列表
./cf.sh zones

# 查看 DNS 记录
./cf.sh dns-list <zone_id>

# 添加 DNS 记录
./cf.sh dns-create <zone_id> A www 1.2.3.4 true

# 查看 SSL 设置
./cf.sh ssl-get <zone_id>

# 设置 SSL 模式
./cf.sh ssl-set <zone_id> strict

# 清除缓存
./cf.sh cache-purge <zone_id>

# 查看防火墙规则
./cf.sh firewall-list <zone_id>

# Tunnel 管理
./cf.sh tunnels-list
./cf.sh tunnel-create <name>
./cf.sh tunnel-token <tunnel_id>
```

#### wrangler（待安装）
```bash
# 需要先安装：npm install -g wrangler

# 查看 Pages 项目列表
wrangler pages project list

# 查看项目详情
wrangler pages project view <project-name>

# 部署前端
wrangler pages deploy ./dist --project-name=<project-name>

# 查看部署历史
wrangler deployments list --project-name=<project-name>

# 查看实时日志
wrangler tail --project-name=<project-name>

# KV 操作
wrangler kv:namespace list
wrangler kv:key put <namespace> <key> <value>

# D1 数据库
wrangler d1 list
wrangler d1 execute <database> --query="SELECT * FROM users"

# R2 存储
wrangler r2 bucket list
wrangler r2 object put <bucket>/<key> --file=./file.txt
```

#### cloudflare-api（待安装）
```bash
# 路径：~/clawd/agents/main/skills/cloudflare-api/scripts/

# 查看域名
./scripts/zones/list.sh

# 查看 DNS
./scripts/dns/list.sh example.com

# 添加 DNS
./scripts/dns/create.sh example.com --type A --name www --content 1.2.3.4

# Tunnel 管理
./scripts/tunnels/list.sh
./scripts/tunnels/create.sh <name>
```

#### domain-dns-ops（不建议安装）
```bash
# ⚠️ 这是别人的定制技能
# 依赖 ~/Projects/manager/ 目录
# 不建议安装
```

### 推荐的 API 端点

| 功能 | API 端点 | 文档 |
|------|---------|------|
| Zones | `GET /zones` | [Zones API](https://developers.cloudflare.com/api/operations/zones-list-zones) |
| DNS | `GET/POST/PUT/DELETE /zones/{id}/dns_records` | [DNS API](https://developers.cloudflare.com/api/operations/dns-records-for-a-zone-list-dns-records) |
| Pages | `GET /accounts/{id}/pages/projects` | [Pages API](https://developers.cloudflare.com/api/operations/pages-project-get) |
| Workers | `GET/PUT /accounts/{id}/workers/scripts/{name}` | [Workers API](https://developers.cloudflare.com/api/operations/worker-script-get) |
| Tunnel | `GET/POST /accounts/{id}/cfd_tunnel` | [Tunnel API](https://developers.cloudflare.com/api/operations/tunnel-list) |
| SSL | `GET/PATCH /zones/{id}/ssl` | [SSL API](https://developers.cloudflare.com/api/operations/ssl-ssl-settings) |
| Firewall | `GET/POST /zones/{id}/firewall/rules` | [Firewall API](https://developers.cloudflare.com/api/operations/firewall-rules-list-firewall-rules) |
| Cache | `DELETE /zones/{id}/purge_cache` | [Cache API](https://developers.cloudflare.com/api/operations/purge-cache-purge-by-cache-tags) |

---

## 🚫 必须手动操作的功能（无法自动化）

以下功能**只能**通过 Cloudflare 控制台操作：

### 1. 账单与用量
- 当前周期用量
- 历史账单
- 配额使用情况

**访问方式**:
```
https://dash.cloudflare.com/
→ 右上角头像 → My Profile → Billing
```

### 2. 部分高级设置
- 账户级设置
- 团队成员管理
- API Token 管理
- 登录历史

**访问方式**:
```
https://dash.cloudflare.com/
→ 右上角头像 → My Profile
```

---

## ✅ 可以自动化但复杂的功能

### 1. 访问统计与分析（GraphQL API）⚠️

**可以自动化**，但查询复杂：

```bash
# 查询过去 7 天的请求数
curl -X POST "https://api.cloudflare.com/client/v4/graphql" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "
      query {
        viewer {
          zones(filter: { zoneTag: \"toykiller.shop\" }) {
            httpRequests1dGroups(
              limit: 7
              filter: { datetime_geq: \"2024-02-17T00:00:00Z\" }
              orderBy: [date_ASC]
            ) {
              sum { requests pageViews }
              dimensions { date }
            }
          }
        }
      }
    "
  }' | jq '.data.viewer.zones[0].httpRequests1dGroups'
```

**返回示例**:
```json
[
  {
    "sum": { "requests": 1234, "pageViews": 567 },
    "dimensions": { "date": "2024-02-17" }
  },
  {
    "sum": { "requests": 2345, "pageViews": 678 },
    "dimensions": { "date": "2024-02-18" }
  }
]
```

**常用查询模板**:

```bash
# 1. 按国家统计请求
query {
  viewer {
    zones(filter: { zoneTag: "example.com" }) {
      httpRequests1dGroups(
        limit: 100
        filter: { datetime_geq: "2024-01-01" }
      ) {
        sum { requests }
        dimensions { clientCountryName }
      }
    }
  }
}

# 2. 按状态码统计
query {
  viewer {
    zones(filter: { zoneTag: "example.com" }) {
      httpRequests1dGroups(
        limit: 100
      ) {
        sum { requests }
        dimensions { edgeResponseStatus }
      }
    }
  }
}

# 3. 带宽使用
query {
  viewer {
    zones(filter: { zoneTag: "example.com" }) {
      httpRequests1dGroups(
        limit: 7
      ) {
        sum { bytes }
        dimensions { date }
      }
    }
  }
}

# 4. 缓存命中率
query {
  viewer {
    zones(filter: { zoneTag: "example.com" }) {
      httpRequests1dGroups(
        limit: 7
      ) {
        sum {
          bytes
          cachedBytes
        }
        dimensions { date }
      }
    }
  }
}
# 缓存命中率 = cachedBytes / bytes * 100
```

### 2. 安全事件详情
- 受阻止的威胁详情
- WAF 触发记录
- DDoS 攻击详情
- 机器人活动报告

**访问方式**:
```
https://dash.cloudflare.com/
→ 选择域名 → Security → Events
```

### 3. 账单与用量
- 当前周期用量
- 历史账单
- 配额使用情况

**访问方式**:
```
https://dash.cloudflare.com/
→ 右上角头像 → My Profile → Billing
```

### 4. 部分高级设置
- 账户级设置
- 团队成员管理
- API Token 管理
- 登录历史

**访问方式**:
```
https://dash.cloudflare.com/
→ 右上角头像 → My Profile
```

---

## 📋 快速参考卡片

### 查看我的前端项目列表

```bash
# 方式 1: Wrangler CLI
wrangler pages project list

# 方式 2: 直接调用 API
curl -sS -H "Authorization: Bearer $TOKEN" \
  "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/pages/projects" \
  | jq '.result[] | {name, created_on}'
```

### 查看我的域名列表

```bash
# 方式 1: cloudflare-toolkit
bash ~/clawd/agents/main/skills/cloudflare-toolkit/scripts/cf.sh zones

# 方式 2: 直接调用 API
curl -sS -H "Authorization: Bearer $TOKEN" \
  "https://api.cloudflare.com/client/v4/zones" \
  | jq '.result[] | {name, id, status}'
```

### 查看访问数据

```
❌ 无法自动化！

必须访问：
https://dash.cloudflare.com/
→ 选择域名 → Analytics & Logs
```

---

## 🎯 我的建议

### 应该自动化 ✅
- DNS 记录管理
- SSL 证书配置
- 缓存清除
- Workers/Pages 部署
- Tunnel 配置
- 防火墙规则

### 必须手动 ❌
- 访问统计分析
- 安全事件查看
- 账单用量查询
- API Token 管理

### 可选自动化 🟡
- 域名注册（不常用）
- 邮件路由（一次性配置）
- 流媒体/图片服务（按需）

---

## 📚 参考链接

- [Cloudflare API 文档](https://developers.cloudflare.com/api/)
- [Wrangler CLI 文档](https://developers.cloudflare.com/workers/wrangler/)
- [Cloudflare 控制台](https://dash.cloudflare.com/)
- [Zone Analytics API 下线通知](https://developers.cloudflare.com/analytics/)

---

*最后更新：2026-02-24*
