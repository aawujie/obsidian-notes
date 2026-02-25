# Medusa 电商系统部署与架构笔记

## 📅 基本信息

- **创建日期**: 2026-02-25
- **项目**: Medusa 开源电商系统 v2
- **部署环境**: macOS (Apple Silicon M 系列)
- **技术栈**: Next.js 15 + PostgreSQL + Redis + Medusa v2

---

## 🎯 官方推荐的两种部署方式

### 方案对比

| 特性 | **纯客户端渲染 (SPA)** | **服务端渲染 (SSR)** |
|------|----------------------|---------------------|
| **运行环境** | 浏览器 | Node.js + 浏览器 |
| **SEO** | ❌ 较差 | ✅ 友好 |
| **首屏速度** | ⚠️ 较慢 | ✅ 快 |
| **配置复杂度** | ✅ 简单 | ❌ 复杂 |
| **兼容性问题** | ✅ 无 | ⚠️ 有 (如 localStorage) |
| **部署成本** | ✅ 低 (Vercel/Netlify) | ❌ 高 (需要服务器) |
| **适用场景** | 后台系统、内部工具 | 电商平台、内容站 |

---

### 方案 1：纯客户端渲染 (官方推荐新手)

```
┌─────────────────────────────────────────────────────────┐
│  浏览器                                                   │
│  ┌────────────────────────────────────────────────────┐ │
│  │  Next.js (SPA 模式)                                 │ │
│  │  - 静态 HTML 加载                                   │ │
│  │  - 浏览器执行 JavaScript                            │ │
│  │  - 直接调用 Medusa API                              │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
         ▲
         │
         │ HTTP
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│  Medusa 后端 (Node.js)                                   │
│  PostgreSQL + Redis                                      │
└─────────────────────────────────────────────────────────┘
```

**优点**:
- ✅ 简单，不需要 SSR 配置
- ✅ 没有 localStorage 兼容问题
- ✅ 部署容易（可以托管到 Vercel/Netlify）

**缺点**:
- ❌ SEO 较差
- ❌ 首屏加载慢

**代码示例** (不需要 Polyfill):
```typescript
// ✅ 纯客户端，直接用 localStorage
useEffect(() => {
  const cart = localStorage.getItem('cart')
}, [])
```

---

### 方案 2：服务端渲染 (我们用的方案)

```
┌─────────────────────────────────────────────────────────┐
│  Next.js 服务器 (Node.js)                                │
│  ┌────────────────────────────────────────────────────┐ │
│  │  SSR 渲染                                           │ │
│  │  - 服务端生成 HTML                                  │ │
│  │  - 预加载数据                                       │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
         ▲                        ▲
         │ HTTP                   │ HTTP
         │                        │
┌────────┴────────┐      ┌────────┴────────┐
│    浏览器        │      │  Medusa 后端     │
│  (Hydration)    │      │  PostgreSQL     │
└─────────────────┘      └─────────────────┘
```

**优点**:
- ✅ SEO 友好
- ✅ 首屏加载快
- ✅ 用户体验好

**缺点**:
- ❌ 配置复杂
- ❌ 有 SSR 兼容性问题（比如 localStorage）

**代码示例** (需要 Polyfill):
```typescript
// ❌ 需要处理 SSR 兼容
if (typeof window === 'undefined') {
  global.localStorage = {...}  // Polyfill
}
```

---

### 🤔 为什么我们选择 SSR？

**因为电商网站需要 SEO！**

| 场景 | 推荐方案 | 原因 |
|------|----------|------|
| **电商平台** | SSR | 商品页面需要被 Google 索引 |
| **后台管理系统** | 纯客户端 | 不需要 SEO，内部使用 |
| **内部工具** | 纯客户端 | 不需要 SEO |
| **博客/内容站** | SSR | 内容需要被搜索引擎收录 |

---

## 🏗️ 混合架构详解

### 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                        你的 MacBook Pro                          │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                    服务端 (Node.js v25)                     │ │
│  │                                                             │ │
│  │  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐   │ │
│  │  │ Medusa 后端  │   │ Next.js 前端 │   │   PostgreSQL │   │ │
│  │  │   端口 9000   │◄─►│   端口 8000   │   │    端口 5432   │   │ │
│  │  │              │   │   (SSR 部分)   │   │              │   │ │
│  │  └──────────────┘   └──────┬───────┘   └──────────────┘   │ │
│  │                            │                               │ │
│  │                    ┌───────▼───────┐                       │ │
│  │                    │     Redis     │                       │ │
│  │                    │    端口 6379    │                       │ │
│  │                    └───────────────┘                       │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              ▲                                   │
│                              │ HTTP/WS                           │
│                              ▼                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                    客户端 (浏览器)                           │ │
│  │                                                             │ │
│  │  ┌──────────────────────────────────────────────────────┐  │ │
│  │  │  Chrome / Safari / Firefox                            │  │ │
│  │  │                                                        │  │ │
│  │  │  - 渲染 HTML                                            │  │ │
│  │  │  - 执行 JavaScript (Hydration)                          │  │ │
│  │  │  - localStorage / sessionStorage                        │  │ │
│  │  │  - 用户交互                                             │  │ │
│  │  └──────────────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

### 各组件职责

#### 1️⃣ Medusa 后端 (Node.js)

**端口**: `9000`

**职责**:
- 📦 **商品管理** - CRUD 操作、库存管理
- 🛒 **订单处理** - 订单创建、状态跟踪
- 👤 **用户系统** - 注册、登录、权限
- 💰 **支付集成** - Stripe、PayPal 等
- 🚚 **物流管理** - 配送、跟踪
- 📊 **数据分析** - 销售统计、报表

**技术实现**:
```typescript
// 核心配置：medusa-config.ts
export default defineConfig({
  projectConfig: {
    databaseUrl: process.env.DATABASE_URL,
    http: {
      storeCors: 'http://localhost:8000',
      adminCors: 'http://localhost:9000',
    },
  },
})
```

**数据流**:
```
HTTP 请求 → Express 路由 → Service 层 → MikroORM → PostgreSQL
```

---

#### 2️⃣ Next.js 前端 (混合运行)

**端口**: `8000`

**运行模式**: SSR (服务端渲染) + CSR (客户端渲染)

**服务端职责 (Node.js)**:
- 📄 **页面渲染** - 生成初始 HTML
- 🔍 **SEO 优化** - 服务端渲染利于搜索引擎
- 🚀 **首屏加速** - 预加载数据
- 🔌 **API 聚合** - 合并多个后端请求

**客户端职责 (浏览器)**:
- 🎨 **交互逻辑** - 点击、表单、动画
- 💾 **本地存储** - localStorage、sessionStorage
- 🔄 **数据更新** - 无需刷新页面
- 📱 **响应式** - 适配不同设备

**技术实现**:
```typescript
// 服务端组件 (在 Node.js 执行)
async function ProductPage() {
  const products = await fetch('http://localhost:9000/store/products')
  return <div>{/* 渲染 HTML */}</div>
}

// 客户端组件 (在浏览器执行)
'use client'
function CartButton() {
  const [count, setCount] = useState(0)
  useEffect(() => {
    localStorage.setItem('cart', count)  // ✅ 只在浏览器
  }, [count])
  return <button>{count}</button>
}
```

---

#### 3️⃣ PostgreSQL 数据库

**端口**: `5432`

**职责**:
- 💾 **持久化存储** - 所有业务数据
- 🔗 **关系管理** - 表关联、外键约束
- 🔍 **复杂查询** - SQL 查询、索引优化
- 🔒 **事务支持** - ACID 保证

**核心表结构**:
```sql
-- 商品表
products (id, title, description, price, created_at)

-- 订单表
orders (id, customer_id, status, total, created_at)

-- 用户表
auth_identity (id, email, password_hash, created_at)

-- 库存表
inventory (id, product_id, quantity, reserved)
```

---

#### 4️⃣ Redis 缓存

**端口**: `6379`

**职责**:
- ⚡ **会话缓存** - 用户登录状态
- 🔄 **任务队列** - 后台任务处理
- 📊 **频率限制** - API 限流
- 💨 **临时数据** - 验证码、临时 Token

**使用场景**:
```
用户登录 → 生成 Token → 存 Redis → 后续请求验证
订单创建 → 发送邮件 → 加入队列 → 异步处理
```

---

### 🔄 请求处理流程

#### 场景：用户访问商品页面

```
1. 浏览器发起请求
   GET http://localhost:8000/products/123
         ↓
2. Next.js 服务器 (Node.js) 接收
   ├─ 执行页面组件 (SSR)
   ├─ 调用 Medusa API 获取商品数据
   │   GET http://localhost:9000/store/products/123
   ├─ Medusa 查询 PostgreSQL
   │   SELECT * FROM products WHERE id = '123'
   └─ 生成 HTML
         ↓
3. 返回 HTML + JavaScript 到浏览器
         ↓
4. 浏览器渲染页面
   ├─ 显示商品信息
   ├─ 执行 JavaScript (Hydration)
   └─ 绑定事件处理器
         ↓
5. 用户交互 (点击"加入购物车")
   ├─ 浏览器执行 onClick
   ├─ 保存到 localStorage
   └─ 调用 API 更新购物车
```

---

## 🐛 遇到的问题：localStorage 兼容性错误

### 错误现象

```
[TypeError: localStorage.getItem is not a function]
GET / 500 in 527ms
```

### 根本原因

**Medusa JS SDK 在模块初始化时直接访问 `localStorage`，但服务端渲染 (SSR) 环境（Node.js）没有 `window` 对象。**

```typescript
// ❌ Medusa SDK 的问题代码
class MedusaClient {
  constructor(config) {
    // 不管环境，直接访问
    this.locale_ = window.localStorage.getItem('locale') || ""
  }
}
```

### 执行时机分析

```
Next.js 启动
    ↓
导入页面组件 (src/app/page.tsx)
    ↓
导入 SDK 配置 (src/lib/config.ts)
    ↓
执行 new Medusa()  ←── ❌ 这里访问 localStorage
    ↓
Node.js 环境没有 window.localStorage
    ↓
报错：localStorage is not defined
```

---

### ✅ 解决方案：添加 Polyfill

**文件**: `src/app/layout.tsx`

```typescript
// localStorage polyfill for SSR
if (typeof window === 'undefined') {
  const store = new Map<string, string>()
  Object.defineProperty(global, 'localStorage', {
    value: {
      getItem: (key: string) => store.get(key) || null,
      setItem: (key: string, value: string) => { store.set(key, value) },
      removeItem: (key: string) => { store.delete(key) },
      clear: () => { store.clear() },
      key: (index: number) => Array.from(store.keys())[index] || null,
      get length() { return store.size }
    },
    writable: true,
    configurable: true
  })
}
```

### 工作原理

| 环境                | `typeof window` | 执行 Polyfill? | 使用的 localStorage |
| ----------------- | --------------- | ------------ | ---------------- |
| **Node.js (SSR)** | `'undefined'`   | ✅ 执行         | ❌ 假的（内存 Map）     |
| **浏览器**           | `'object'`      | ❌ 跳过         | ✅ 真的（浏览器原生）      |

### 为什么不影晌功能？

```
┌─────────────────────────────────────────────────────────┐
│ 1. 服务端渲染 (Node.js)                                  │
│    ├─ 使用假 localStorage (Polyfill)                     │
│    └─ 目的：不报错，能生成 HTML                           │
│                                                          │
│ 2. 客户端渲染 (浏览器)                                   │
│    ├─ 跳过 Polyfill                                     │
│    └─ 使用真 localStorage                               │
│       - 购物车数据                                       │
│       - 用户偏好                                         │
│       - 登录状态                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🌐 浏览器 vs Node.js 环境对比

### 核心差异表

| 特性 | 浏览器环境 | Node.js 环境 |
|------|------------|--------------|
| **全局对象** | `window` | `global` |
| **DOM API** | ✅ (`document`, `element`) | ❌ 无 |
| **localStorage** | ✅ 有 | ❌ 无 |
| **sessionStorage** | ✅ 有 | ❌ 无 |
| **fetch** | ✅ 原生支持 | ⚠️ v18+ 支持 |
| **XMLHttpRequest** | ✅ 有 | ❌ 无 |
| **模块系统** | ES Modules | CommonJS + ESM |
| **文件系统** | ❌ 受限 (File API) | ✅ 完整 (`fs`) |
| **网络请求** | ✅ 受 CORS 限制 | ✅ 无 CORS 限制 |
| **运行时机** | 页面加载后 | 请求到达时 |
| **生命周期** | 页面关闭前 | 请求结束止 |

### Next.js 中的执行位置判断

```typescript
// 1. 模块顶层代码 → 服务端 + 客户端都会执行
const config = loadConfig()  // ⚠️ 注意环境兼容性

// 2. 服务端组件 → 只在服务端执行
async function ServerComponent() {
  const data = await db.query()  // ✅ 安全
  return <div>{data}</div>
}

// 3. 客户端组件 → 只在客户端执行
'use client'
function ClientComponent() {
  useEffect(() => {
    localStorage.getItem('key')  // ✅ 安全
  }, [])
  return <div>...</div>
}

// 4. 事件处理器 → 只在客户端执行
const handleClick = () => {
  window.alert('Hello')  // ✅ 安全
}

// 5. 环境检查 → 安全访问浏览器 API
if (typeof window !== 'undefined') {
  localStorage.getItem('key')  // ✅ 安全
}
```

---

## 📋 服务端口汇总

| 服务 | 端口 | 地址 | 运行环境 |
|------|------|------|----------|
| **Medusa 后端** | 9000 | http://localhost:9000 | Node.js |
| **Admin 后台** | 9000 | http://localhost:9000/app | Node.js (React SPA) |
| **商店前端** | 8000 | http://localhost:8000 | Node.js SSR + 浏览器 |
| **PostgreSQL** | 5432 | localhost:5432 | 独立进程 |
| **Redis** | 6379 | localhost:6379 | 独立进程 |

---

## 🚀 启动命令

```bash
# 后端
cd ~/Code/8.practice/medusa-store
npm run dev

# 前端
cd ~/Code/8.practice/medusa-store-storefront
npm run dev
```

---

## 📝 重要配置

### 后端配置 (`medusa-config.ts`)

```typescript
export default defineConfig({
  projectConfig: {
    databaseUrl: process.env.DATABASE_URL,
    http: {
      storeCors: process.env.STORE_CORS,
      adminCors: process.env.ADMIN_CORS,
      authCors: process.env.AUTH_CORS,
      jwtSecret: process.env.JWT_SECRET,
      cookieSecret: process.env.COOKIE_SECRET,
    },
  },
})
```

### 环境变量 (`.env`)

```bash
STORE_CORS=http://localhost:8000
ADMIN_CORS=http://localhost:9000
AUTH_CORS=http://localhost:9000
DATABASE_URL=postgres://postgres@localhost/medusa-medusa-store
JWT_SECRET=supersecret
COOKIE_SECRET=supersecret
```

---

## 💡 经验总结

### 架构选择

1. **电商网站优先选 SSR**
   - SEO 对电商至关重要
   - 商品页面需要被搜索引擎索引
   - 首屏速度影响转化率

2. **纯客户端适合后台系统**
   - 不需要 SEO
   - 配置简单，开发快
   - 没有 SSR 兼容性问题

3. **根据团队能力选择**
   - 新手/小团队 → 纯客户端
   - 有经验/重 SEO → SSR

### 技术实践

4. **Next.js 15 + 第三方库要注意 SSR 兼容性**
   - 检查库是否支持服务端渲染
   - 必要时添加 Polyfill

5. **访问浏览器 API 前先检查环境**
   ```typescript
   if (typeof window !== 'undefined') {
     // 安全访问浏览器 API
   }
   ```

6. **Polyfill 是解决 SSR 兼容的常用方案**
   - 只在服务端生效
   - 不影响客户端功能

7. **Medusa v2 还在快速迭代中**
   - 有些坑需要自己填
   - 关注官方 GitHub Issues

---

## 🔗 相关资源

- [Medusa 官方文档](https://docs.medusajs.com/)
- [Next.js SSR 文档](https://nextjs.org/docs/app/building-your-application/rendering/server-and-client-components)
- [GitHub Issue: localStorage error](https://github.com/medusajs/medusa/issues/14306)

---

## ✅ 验证清单

- [x] 后端 API 正常运行
- [x] Admin 后台可访问
- [x] 商店前端正常渲染
- [x] localStorage Polyfill 生效
- [x] 数据库连接正常
- [x] 无控制台错误
- [x] 架构文档完整
