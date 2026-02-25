# Supabase 本地开发 → 云端部署完整指南

> 版本：2026-02-24 | CLI: v2.39.2+

---

## 📦 前置检查

```bash
# 检查 CLI 安装
supabase --version

# 更新到最新版
brew update && brew upgrade supabase/tap/supabase

# 检查 Docker (本地开发必需)
docker --version
```

---

## 🏗️ 一、本地开发环境

### 1.1 初始化项目

```bash
# 创建项目目录
mkdir my-supabase-project && cd my-supabase-project

# 初始化 Supabase
supabase init
```

生成结构：
```
my-supabase-project/
├── supabase/
│   ├── config.toml          # 项目配置
│   ├── migrations/          # 数据库迁移
│   ├── seed.sql             # 种子数据
│   ├── functions/           # Edge Functions
│   └── schemas/             # 数据库 schema
└── README.md
```

### 1.2 启动本地服务

```bash
# 启动完整本地 Supabase 栈
supabase start
```

启动后输出：
```
- Database URL: postgresql://postgres:postgres@localhost:54322/postgres
- Studio URL:   http://localhost:54323
- API URL:      http://localhost:54321
```

### 1.3 本地开发工作流

```bash
# 1. 创建数据库迁移
supabase migration new create_users_table

# 编辑生成的迁移文件
# supabase/migrations/YYYYMMDDHHMMSS_create_users_table.sql

# 2. 应用迁移到本地
supabase db reset

# 3. 创建 Edge Function
supabase functions new hello-world

# 4. 本地测试 function
supabase functions serve hello-world

# 5. 查看本地状态
supabase status
```

### 1.4 常用本地命令

```bash
# 重启本地服务
supabase stop && supabase start

# 完全重置（删除所有数据）
supabase db reset

# 生成类型定义 (TypeScript)
supabase gen types typescript --local > src/types/supabase.ts

# 导出当前 schema
supabase db dump -f schema.sql

# 查看日志
supabase logs
```

---

## ☁️ 二、云端部署方式

### 方式 A：Supabase 官方云（推荐）

#### 2.1 创建项目

1. 访问 https://supabase.com
2. Sign in → New Project
3. 填写：
   - Organization
   - Project name
   - Database password
   - Region（选最近的）

#### 2.2 链接本地与云端

```bash
# 登录
supabase login

# 获取项目引用 ID (从 Dashboard URL 或 Settings → API)
# 格式：xxxxxxxxxxxxxxxxxxxx

# 链接项目
supabase link --project-ref xxxxxxxxxxxxxxxxxxxx

# 验证链接
supabase projects list
```

#### 2.3 部署到官方云

```bash
# 推送所有迁移
supabase db push

# 或者应用所有变更（包括未迁移的）
supabase db push --include-all

# 部署 Edge Functions
supabase functions deploy hello-world

# 部署存储策略
supabase storage push

# 一次性部署全部
supabase db push && supabase functions deploy
```

#### 2.4 获取云端凭证

在 Dashboard → Settings → API：
```bash
# Project URL
export SUPABASE_URL="https://xxxxxxxxxxxxx.supabase.co"

# Anon Key (客户端使用，受 RLS 限制)
export SUPABASE_ANON_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Service Role Key (服务端使用，绕过 RLS ⚠️)
export SUPABASE_SERVICE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

### 方式 B：自建服务器部署

#### 2.5 前置要求

- 服务器：4 核 8G+ (最小)，8 核 16G+ (推荐)
- Docker + Docker Compose
- 域名 + SSL 证书

#### 2.6 部署步骤

```bash
# 1. 克隆官方 Docker Compose
git clone https://github.com/supabase/supabase
cd supabase/docker

# 2. 复制环境变量模板
cp .env.example .env

# 3. 编辑配置
vim .env
# 修改：
# - POSTGRES_PASSWORD
# - JWT_SECRET
# - STUDIO_DEFAULT_ORGANIZATION
# - 其他敏感信息
```

#### 2.7 启动服务

```bash
# 启动所有服务
docker compose up -d

# 查看状态
docker compose ps

# 查看日志
docker compose logs -f
```

#### 2.8 配置反向代理 (Nginx 示例)

```nginx
server {
    listen 443 ssl;
    server_name supabase.yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;  # Kong API Gateway
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /studio {
        proxy_pass http://localhost:3000;  # Studio
        proxy_set_header Host $host;
    }
}
```

#### 2.9 链接自建实例

```bash
# 链接到自建项目
supabase link --project-ref local-self-hosted \
  --db-url postgresql://postgres:postgres@your-server:5432/postgres

# 或使用 API URL
supabase link --api-url https://supabase.yourdomain.com
```

---

## 🔄 三、本地 ↔ 云端 同步

### 3.1 同步策略对比

| 方向 | 命令 | 说明 |
|------|------|------|
| 本地 → 云端 | `supabase db push` | 推送迁移 |
| 云端 → 本地 | `supabase db pull` | 拉取 schema |
| 本地 → 云端 | `supabase functions deploy` | 部署函数 |
| 云端 → 本地 | `supabase functions download` | 下载函数 |

### 3.2 数据库同步

```bash
# 从云端拉取 schema 到本地
supabase db pull

# 生成迁移文件
supabase migration new sync_from_cloud

# 推送到云端
supabase db push

# 导出云端数据（用于备份）
supabase db dump -f backup.sql --data-only

# 导入数据到本地
psql postgresql://postgres:postgres@localhost:54322/postgres < backup.sql
```

### 3.3 Edge Functions 同步

```bash
# 部署单个函数
supabase functions deploy hello-world

# 部署所有函数
supabase functions deploy

# 下载云端函数到本地
supabase functions download

# 查看函数日志
supabase functions logs hello-world
```

### 3.4 存储策略同步

```bash
# 推送存储策略
supabase storage push

# 拉取存储策略
supabase storage pull
```

### 3.5 完整同步流程

```bash
# 1. 从云端拉取最新 schema
supabase db pull

# 2. 本地开发修改

# 3. 创建新迁移
supabase migration new feature_x

# 4. 本地测试
supabase db reset
supabase start

# 5. 推送到云端
supabase db push
supabase functions deploy

# 6. 生成新类型定义
supabase gen types typescript --linked > src/types/supabase.ts
```

---

## 🔐 四、配置管理

### 4.1 环境变量管理

```bash
# 创建 .env 文件（不要提交到 git）
cat > .env << EOF
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=eyJ...
SUPABASE_SERVICE_KEY=eyJ...
EOF

# 添加到 .gitignore
echo ".env" >> .gitignore
```

### 4.2 使用 .env.vault (推荐团队)

```bash
# 安装 dotenv-vault
npm install -g @dotenvx/dotenvx

# 初始化
dotenvx init

# 添加环境变量
dotenvx set SUPABASE_URL https://xxxxx.supabase.co

# 生成 .env.vault (加密)
dotenvx build

# 提交 .env.vault 到 git，不提交 .env
```

### 4.3 在代码中使用

```typescript
// src/lib/supabase.ts
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.SUPABASE_URL!
const supabaseKey = process.env.SUPABASE_ANON_KEY!

export const supabase = createClient(supabaseUrl, supabaseKey)
```

---

## 📊 五、数据迁移策略

### 5.1 生产数据 → 本地（用于调试）

```bash
# 1. 导出云端数据
supabase db dump -f prod-backup.sql --data-only \
  --db-url "postgresql://postgres:[PASSWORD]@db.xxxxx.supabase.co:5432/postgres"

# 2. 导入到本地
psql postgresql://postgres:postgres@localhost:54322/postgres < prod-backup.sql

# 或使用 pg_dump
pg_dump "postgresql://postgres:[PASSWORD]@db.xxxxx.supabase.co:5432/postgres" \
  --data-only --inserts > data.sql
```

### 5.2 本地种子数据 → 云端

```bash
# 1. 准备种子数据
# supabase/seed.sql

# 2. 推送到云端
psql "postgresql://postgres:[SERVICE_KEY]@db.xxxxx.supabase.co:5432/postgres" \
  < supabase/seed.sql
```

### 5.3 使用迁移工具

```bash
# 使用 Atlas (推荐)
atlas migrate diff --env dev
atlas migrate apply --env prod

# 使用 Sqitch
sqitch deploy
```

---

## 🚀 六、CI/CD 集成

### 6.1 GitHub Actions 示例

```yaml
# .github/workflows/supabase-deploy.yml
name: Deploy Supabase

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Supabase CLI
        uses: supabase/setup-cli@v1
        with:
          version: latest
      
      - name: Link project
        run: supabase link --project-ref ${{ secrets.SUPABASE_PROJECT_ID }}
      
      - name: Deploy migrations
        run: supabase db push
      
      - name: Deploy functions
        run: supabase functions deploy
      
      - name: Generate types
        run: supabase gen types typescript --linked > src/types/supabase.ts
```

### 6.2 环境变量配置

在 GitHub Settings → Secrets and variables：
```
SUPABASE_PROJECT_ID=xxxxxxxxxxxxxxxxxxxx
SUPABASE_ACCESS_TOKEN=sbp_xxxxxxxxxxxxx
```

---

## 🛠️ 七、常见问题

### 7.1 本地启动失败

```bash
# 检查 Docker
docker ps

# 清理旧容器
supabase stop && docker compose down

# 重置本地
supabase db reset

# 查看日志
supabase logs
```

### 7.2 推送失败

```bash
# 检查链接状态
supabase projects list

# 重新链接
supabase link --project-ref xxxxx

# 检查迁移冲突
supabase db pull
```

### 7.3 类型定义过期

```bash
# 重新生成
supabase gen types typescript --linked > src/types/supabase.ts

# 或使用本地
supabase gen types typescript --local > src/types/supabase.ts
```

### 7.4 数据同步冲突

```bash
# 1. 备份当前状态
supabase db dump -f backup.sql

# 2. 拉取云端 schema
supabase db pull

# 3. 手动解决冲突

# 4. 创建新迁移
supabase migration new resolve_conflicts

# 5. 推送
supabase db push
```

---

## 📋 八、最佳实践清单

### 开发前
- [ ] 安装最新 Supabase CLI
- [ ] 初始化项目 `supabase init`
- [ ] 配置 .gitignore (排除 .env)

### 开发中
- [ ] 所有 schema 变更通过迁移文件
- [ ] 本地测试后再推送
- [ ] 定期生成类型定义

### 部署前
- [ ] 备份生产数据
- [ ] 在 staging 环境测试
- [ ] 准备回滚方案

### 部署后
- [ ] 验证功能正常
- [ ] 检查日志
- [ ] 更新文档

---

## 🔗 参考资源

- [Supabase CLI 文档](https://supabase.com/docs/guides/cli)
- [本地开发指南](https://supabase.com/docs/guides/cli/local-development)
- [自托管部署](https://supabase.com/docs/guides/self-hosting)
- [迁移最佳实践](https://supabase.com/docs/guides/platform/migrations)

---

*最后更新：2026-02-24*
