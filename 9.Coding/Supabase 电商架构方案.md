# Supabase 电商架构方案 v2 - 设计理念

**创建日期**: 2026-02-25  
**更新日期**: 2026-02-26  
**版本**: 2.0 (MVP 务实版)  
**标签**: #Supabase #电商 #架构设计 #EdgeFunctions #PostgreSQL #MVP #设计理念

---

> **📌 文档定位**: 本文档是**设计理念参考**，阐述支付插件化、库存预留等核心设计思路。  
> **🚀 实施指南**: 实际开发请参考 [[Supabase 电商架构方案 v3 - 整合版]]（复用现有项目 + 整合优化）

---

## 🎯 设计原则

### 核心理念

> **"不提前优化，不为不存在的规模开发"**

| 原则 | 说明 |
|------|------|
| ✅ **MVP 优先** | 先上线验证，再迭代优化 |
| ✅ **直接透明** | 直接调用 API，无黑盒抽象 |
| ✅ **模块化** | 领域分离，但不过度设计 |
| ✅ **可扩展** | 需要时再加功能，不提前实现 |
| ✅ **低成本** | 用 Supabase 免费 tier，$0 启动 |

---

## 🏗️ 整体架构

```
┌─────────────────────────────────────────────────────────────────┐
│                        前端 (Next.js)                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │ 商品列表  │  │ 购物车    │  │ 订单中心  │  │ 用户中心  │        │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Supabase Edge Functions                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    API Layer (直接调用)                   │   │
│  │  /api/products  /api/cart  /api/orders  /api/payment    │   │
│  └─────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    Service Layer (领域逻辑)               │   │
│  │  OrderService │ InventoryService │ PricingService       │   │
│  └─────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    Provider Layer (支付插件)              │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │   │
│  │  │   Stripe     │  │   Alipay     │  │   Wechat     │  │   │
│  │  │  (直接调用)   │  │  (直接调用)   │  │  (直接调用)   │  │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Supabase PostgreSQL                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │  products │  │  orders  │  │inventory │  │  users   │       │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                      │
│  │order_items│  │ payments │  │  notes   │                      │
│  └──────────┘  └──────────┘  └──────────┘                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📋 MVP 范围（Phase 1: 4-6 周）

### ✅ 要做（核心功能）

| 模块 | 功能 | 优先级 |
|------|------|--------|
| **商品** | 商品 + 变体 + 基础属性 | P0 |
| **购物车** | 添加/删除/修改数量 | P0 |
| **订单** | 创建订单 + 状态跟踪 | P0 |
| **库存** | 单仓库 + 预留机制 | P0 |
| **支付** | Stripe + 支付宝（二选一先） | P0 |
| **用户** | Supabase Auth（邮箱登录） | P0 |

### ❌ 不做（后期迭代）

| 功能 | 原因 | 替代方案 |
|------|------|----------|
| 优惠券系统 | MVP 不需要，手动改价 | 后台直接改订单金额 |
| 多仓库 | 单仓库足够验证 | 后期再加 |
| 部分发货 | 订单少可以一次发 | 人工处理 |
| 换货 RMA | 退款重拍即可 | 客服手动处理 |
| 客户组定价 | 统一价格简单 | 后期再加 |
| 完整管理后台 | 直接操作数据库 | 简单 Admin 页面 |
| 采购管理 | Excel 记录足够 | 后期再加 |
| 买赠/满减 | 规则复杂，MVP 不需要 | 后期再加 |

---

## 📁 项目结构（简化版）

```
supabase-ecommerce/
├── 📁 supabase/
│   ├── 📁 migrations/              # 数据库迁移
│   │   ├── 001-products.sql        # 商品表
│   │   ├── 002-orders.sql          # 订单表
│   │   ├── 003-inventory.sql       # 库存表
│   │   ├── 004-payments.sql        # 支付表
│   │   └── 005-rls-policies.sql    # 行级安全
│   │
│   ├── 📁 functions/               # Edge Functions
│   │   ├── 📁 api/                 # API 入口（薄层）
│   │   │   ├── create-order.ts
│   │   │   ├── get-order.ts
│   │   │   └── create-payment.ts
│   │   │
│   │   ├── 📁 services/            # 领域服务（核心逻辑）
│   │   │   ├── order-service.ts
│   │   │   └── inventory-service.ts
│   │   │
│   │   ├── 📁 providers/           # 支付提供商（插件式）
│   │   │   ├── payment-provider.ts  # 接口定义
│   │   │   ├── stripe-provider.ts   # Stripe 实现
│   │   │   └── alipay-provider.ts   # 支付宝实现
│   │   │
│   │   └── 📁 webhooks/            # 第三方回调
│   │       ├── stripe-webhook.ts
│   │       └── alipay-notify.ts
│   │
│   └── 📁 sql/                     # SQL 函数/触发器
│       ├── release-expired-reservations.sql
│       └── rls-policies.sql
│
├── 📁 frontend/                    # Next.js 前端
│   ├── 📁 app/
│   │   ├── 📁 products/
│   │   ├── 📁 cart/
│   │   ├── 📁 checkout/
│   │   └── 📁 orders/
│   │
│   ├── 📁 components/
│   │   ├── ProductCard.tsx
│   │   ├── Cart.tsx
│   │   ├── StripeCheckout.tsx
│   │   └── OrderStatus.tsx
│   │
│   └── 📁 lib/
│       └── supabase-client.ts
│
├── 📁 admin/                       # 简单管理后台（Phase 2）
│   └── （后期开发）
│
└── 📁 docs/
    ├── architecture.md
    ├── api-reference.md
    └── mvp-scope.md
```

---

## 🗄️ 数据库设计（MVP 精简版）

### 1️⃣ 商品表 (products)

```sql
CREATE TYPE product_status AS ENUM ('draft', 'active', 'archived');

CREATE TABLE products (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL,
  description text,
  status product_status DEFAULT 'draft',
  
  -- 价格（MVP 简化：无复杂定价）
  base_price numeric(10,2) NOT NULL,
  compare_at_price numeric(10,2),  -- 原价（显示折扣用）
  
  -- 库存（MVP：单仓库）
  track_inventory boolean DEFAULT true,
  inventory int DEFAULT 0,
  reserved_inventory int DEFAULT 0,
  
  -- SEO
  slug text UNIQUE,
  
  -- 元数据（动态属性，借鉴 WordPress）
  attributes jsonb DEFAULT '{}',
  metadata jsonb DEFAULT '{}',
  
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

CREATE INDEX idx_products_status ON products(status);
CREATE INDEX idx_products_slug ON products(slug);
```

**MVP 说明**：
- ✅ 无多币种定价（后期加 `prices` 表）
- ✅ 无客户组定价（后期加 `customer_groups`）
- ✅ 无批量定价（后期加 `pricing_rules`）

---

### 2️⃣ 商品变体表 (product_variants)

```sql
CREATE TABLE product_variants (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  product_id uuid REFERENCES products(id) ON DELETE CASCADE,
  
  sku text UNIQUE,
  name text,  -- "红色 / L"
  
  -- 价格覆盖（可选）
  price numeric(10,2),  -- null 则使用产品基础价
  
  -- 库存
  inventory int DEFAULT 0,
  reserved_inventory int DEFAULT 0,
  
  -- 规格
  options jsonb,  -- {"color": "red", "size": "L"}
  
  created_at timestamptz DEFAULT now()
);

CREATE INDEX idx_variants_product ON product_variants(product_id);
```

---

### 3️⃣ 购物车表 (carts + cart_items)

```sql
CREATE TABLE carts (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id text,              -- 匿名用户
  user_id uuid REFERENCES auth.users(id),
  status text DEFAULT 'active', -- 'active', 'converted', 'abandoned'
  currency text DEFAULT 'CNY',
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

CREATE TABLE cart_items (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  cart_id uuid REFERENCES carts(id) ON DELETE CASCADE,
  product_id uuid REFERENCES products(id),
  variant_id uuid REFERENCES product_variants(id),
  quantity int NOT NULL DEFAULT 1,
  
  -- 价格快照（防止调价）
  price_snapshot numeric(10,2) NOT NULL,
  
  created_at timestamptz DEFAULT now(),
  
  UNIQUE(cart_id, product_id, variant_id)
);
```

---

### 4️⃣ 订单表 (orders + order_items)

```sql
CREATE TYPE order_status AS ENUM (
  'pending',      -- 待支付
  'confirmed',    -- 已支付
  'processing',   -- 处理中
  'shipped',      -- 已发货
  'delivered',    -- 已完成
  'cancelled',    -- 已取消
  'refunded'      -- 已退款
);

CREATE TABLE orders (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  order_number text UNIQUE NOT NULL,  -- "ORD-20260226-001"
  
  user_id uuid REFERENCES auth.users(id),
  
  -- 状态
  status order_status DEFAULT 'pending',
  
  -- 价格（MVP 简化）
  subtotal numeric(10,2) NOT NULL,
  discount_amount numeric(10,2) DEFAULT 0,
  shipping_amount numeric(10,2) DEFAULT 0,
  total_amount numeric(10,2) NOT NULL,
  
  -- 收货地址
  shipping_address jsonb NOT NULL,
  
  -- 备注（借鉴 WooCommerce）
  customer_note text,
  internal_note text,  -- 内部备注
  
  -- 时间线
  paid_at timestamptz,
  shipped_at timestamptz,
  completed_at timestamptz,
  cancelled_at timestamptz,
  
  created_at timestamptz DEFAULT now()
);

CREATE TABLE order_items (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  order_id uuid REFERENCES orders(id) ON DELETE CASCADE,
  product_id uuid REFERENCES products(id),
  variant_id uuid REFERENCES product_variants(id),
  
  name text NOT NULL,           -- 快照
  sku text,
  quantity int NOT NULL,
  price numeric(10,2) NOT NULL,
  total numeric(10,2) NOT NULL,
  
  variant_options jsonb,
  
  created_at timestamptz DEFAULT now()
);
```

---

### 5️⃣ 库存预留表 (inventory_reservations)

```sql
-- 🎯 核心设计：防止超卖
CREATE TABLE inventory_reservations (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  product_id uuid REFERENCES products(id),
  variant_id uuid REFERENCES product_variants(id),
  quantity int NOT NULL,
  
  order_id uuid REFERENCES orders(id),
  
  expires_at timestamptz NOT NULL,  -- 30 分钟后过期
  status text DEFAULT 'active',     -- 'active', 'committed', 'released'
  
  created_at timestamptz DEFAULT now()
);

CREATE INDEX idx_reservations_order ON inventory_reservations(order_id);
CREATE INDEX idx_reservations_expires ON inventory_reservations(expires_at);
```

**自动释放逻辑**（Edge Function 定时调用）：

```typescript
// 📁 supabase/functions/cron/release-reservations.ts
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

export async function releaseExpiredReservations() {
  const supabase = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_SERVICE_KEY')!
  )
  
  // 找到过期预留
  const { data: expired } = await supabase
    .from('inventory_reservations')
    .select('*')
    .eq('status', 'active')
    .lt('expires_at', new Date().toISOString())
  
  // 释放库存
  for (const reservation of expired) {
    await supabase.rpc('release_inventory', {
      p_product_id: reservation.product_id,
      p_variant_id: reservation.variant_id,
      p_quantity: reservation.quantity
    })
    
    await supabase
      .from('inventory_reservations')
      .update({ status: 'released' })
      .eq('id', reservation.id)
  }
  
  return { released: expired?.length || 0 }
}
```

---

### 6️⃣ 支付表 (payments)

```sql
CREATE TYPE payment_status AS ENUM (
  'pending', 'authorized', 'captured', 'failed', 'refunded'
);

CREATE TABLE payments (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  order_id uuid REFERENCES orders(id),
  
  provider text NOT NULL,  -- 'stripe' | 'alipay' | 'wechat'
  provider_payment_id text,
  
  amount numeric(10,2) NOT NULL,
  currency text DEFAULT 'CNY',
  status payment_status DEFAULT 'pending',
  
  response_data jsonb,
  
  created_at timestamptz DEFAULT now()
);
```

---

### 7️⃣ 订单备注表 (order_notes)

```sql
-- 🎯 借鉴 WooCommerce：完整审计
CREATE TABLE order_notes (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  order_id uuid REFERENCES orders(id) ON DELETE CASCADE,
  
  note_type text NOT NULL,  -- 'customer', 'private', 'system'
  content text NOT NULL,
  created_by uuid REFERENCES auth.users(id),
  
  created_at timestamptz DEFAULT now()
);
```

---

## ⚡ 支付模块设计（插件式）

### 核心接口

```typescript
// 📁 supabase/functions/providers/payment-provider.ts

// 统一接口，所有支付插件必须实现
export interface PaymentProvider {
  readonly name: string;  // 'stripe' | 'alipay' | 'wechat'
  
  initiatePayment(data: PaymentInitData): Promise<PaymentInitResult>
  refundPayment(paymentId: string, amount: number): Promise<RefundResult>
  getPaymentStatus(paymentId: string): Promise<PaymentStatus>
}

export interface PaymentInitData {
  orderId: string
  amount: number
  currency: string
  returnUrl: string
  cancelUrl: string
}

export interface PaymentInitResult {
  providerPaymentId: string
  redirectUrl?: string    // 支付宝/微信
  clientSecret?: string   // Stripe
  qrCodeUrl?: string      // 微信扫码
}

export interface RefundResult {
  success: boolean
  refundId: string
  amount: number
}

export interface PaymentStatus {
  status: 'pending' | 'authorized' | 'captured' | 'failed' | 'refunded'
  amount: number
}
```

---

### Stripe 实现（直接调用，无黑盒）

```typescript
// 📁 supabase/functions/providers/stripe-provider.ts
import Stripe from 'https://esm.sh/stripe@14'
import type { PaymentProvider, PaymentInitData, PaymentInitResult, RefundResult, PaymentStatus } from './payment-provider.ts'

export class StripeProvider implements PaymentProvider {
  readonly name = 'stripe'
  private stripe: Stripe
  
  constructor(secretKey: string) {
    this.stripe = new Stripe(secretKey)
  }
  
  // 🎯 初始化支付
  async initiatePayment(data: PaymentInitData): Promise<PaymentInitResult> {
    const paymentIntent = await this.stripe.paymentIntents.create({
      amount: Math.round(data.amount * 100),  // 分
      currency: data.currency.toLowerCase(),
      metadata: { order_id: data.orderId },
      return_url: data.returnUrl,
    })
    
    return {
      providerPaymentId: paymentIntent.id,
      clientSecret: paymentIntent.client_secret!,
    }
  }
  
  // 🎯 退款（直接调用 API，透明可控）
  async refundPayment(paymentId: string, amount: number): Promise<RefundResult> {
    const refund = await this.stripe.refunds.create({
      payment_intent: paymentId,
      amount: Math.round(amount * 100),
    })
    
    return {
      success: refund.status === 'succeeded',
      refundId: refund.id,
      amount,
    }
  }
  
  // 🎯 查询状态
  async getPaymentStatus(paymentId: string): Promise<PaymentStatus> {
    const paymentIntent = await this.stripe.paymentIntents.retrieve(paymentId)
    
    const statusMap: Record<string, PaymentStatus['status']> = {
      'requires_payment_method': 'pending',
      'requires_confirmation': 'pending',
      'processing': 'authorized',
      'requires_capture': 'authorized',
      'succeeded': 'captured',
      'canceled': 'failed',
    }
    
    return {
      status: statusMap[paymentIntent.status] || 'pending',
      amount: paymentIntent.amount / 100,
    }
  }
}
```

---

### 支付宝实现

```typescript
// 📁 supabase/functions/providers/alipay-provider.ts
import type { PaymentProvider, PaymentInitData, PaymentInitResult, RefundResult, PaymentStatus } from './payment-provider.ts'

export class AlipayProvider implements PaymentProvider {
  readonly name = 'alipay'
  
  async initiatePayment(data: PaymentInitData): Promise<PaymentInitResult> {
    // 调用支付宝 API 生成支付链接
    const alipayUrl = await this.createPayUrl({
      outTradeNo: data.orderId,
      totalAmount: data.amount,
      returnUrl: data.returnUrl,
      notifyUrl: `${Deno.env.get('SUPABASE_URL')}/functions/v1/webhooks/alipay-notify`,
    })
    
    return {
      providerPaymentId: data.orderId,
      redirectUrl: alipayUrl,
    }
  }
  
  async refundPayment(paymentId: string, amount: number): Promise<RefundResult> {
    const result = await this.refund({
      tradeNo: paymentId,
      refundAmount: amount,
    })
    
    return {
      success: result.code === '10000',
      refundId: result.outRequestNo,
      amount,
    }
  }
  
  async getPaymentStatus(paymentId: string): Promise<PaymentStatus> {
    const result = await this.queryOrder(paymentId)
    
    const statusMap: Record<string, PaymentStatus['status']> = {
      'WAIT_BUYER_PAY': 'pending',
      'TRADE_SUCCESS': 'captured',
      'TRADE_FINISHED': 'captured',
      'TRADE_CLOSED': 'failed',
    }
    
    return {
      status: statusMap[result.tradeStatus] || 'pending',
      amount: parseFloat(result.totalAmount),
    }
  }
  
  // 内部方法
  private async createPayUrl(params: any): Promise<string> {
    // 支付宝签名逻辑
    return 'https://openapi.alipay.com/gateway.do?...'
  }
  
  private async queryOrder(tradeNo: string): Promise<any> {
    // 支付宝查询接口
    return {}
  }
  
  private async refund(params: any): Promise<any> {
    // 支付宝退款接口
    return {}
  }
}
```

---

### 支付服务（依赖注入）

```typescript
// 📁 supabase/functions/services/payment-service.ts
import type { PaymentProvider, PaymentInitData } from '../providers/payment-provider.ts'

export class PaymentService {
  private providers: Map<string, PaymentProvider> = new Map()
  private defaultProvider: string
  
  constructor(defaultProvider: string = 'stripe') {
    this.defaultProvider = defaultProvider
  }
  
  // 🎯 注册支付插件
  registerProvider(provider: PaymentProvider) {
    this.providers.set(provider.name, provider)
  }
  
  // 🎯 获取支付提供商
  getProvider(name?: string): PaymentProvider {
    const providerName = name || this.defaultProvider
    const provider = this.providers.get(providerName)
    
    if (!provider) {
      throw new Error(`Payment provider "${providerName}" not found`)
    }
    
    return provider
  }
  
  // 🎯 创建支付
  async createPayment(data: {
    orderId: string
    amount: number
    currency: string
    provider?: string
    returnUrl: string
    cancelUrl: string
  }) {
    const provider = this.getProvider(data.provider)
    
    const result = await provider.initiatePayment({
      orderId: data.orderId,
      amount: data.amount,
      currency: data.currency,
      returnUrl: data.returnUrl,
      cancelUrl: data.cancelUrl,
    })
    
    // 保存支付记录
    // ...
    
    return result
  }
}
```

---

### 配置与初始化

```typescript
// 📁 supabase/functions/config.ts
import { StripeProvider } from './providers/stripe-provider.ts'
import { AlipayProvider } from './providers/alipay-provider.ts'
import { PaymentService } from './services/payment-service.ts'

export function createPaymentService(): PaymentService {
  const paymentService = new PaymentService('stripe')
  
  // 注册 Stripe
  if (Deno.env.get('STRIPE_SECRET_KEY')) {
    paymentService.registerProvider(
      new StripeProvider(Deno.env.get('STRIPE_SECRET_KEY')!)
    )
  }
  
  // 注册支付宝
  if (Deno.env.get('ALIPAY_APP_ID')) {
    paymentService.registerProvider(
      new AlipayProvider({
        appId: Deno.env.get('ALIPAY_APP_ID')!,
        privateKey: Deno.env.get('ALIPAY_PRIVATE_KEY')!,
        alipayPublicKey: Deno.env.get('ALIPAY_PUBLIC_KEY')!,
      })
    )
  }
  
  return paymentService
}
```

---

### Webhook 处理（简单直接）

```typescript
// 📁 supabase/functions/webhooks/stripe-webhook.ts
import { serve } from 'https://deno.land/std/http/server.ts'
import Stripe from 'https://esm.sh/stripe@14'

const stripe = new Stripe(Deno.env.get('STRIPE_SECRET_KEY')!)
const webhookSecret = Deno.env.get('STRIPE_WEBHOOK_SECRET')!

serve(async (req: Request) => {
  const body = await req.text()
  const sig = req.headers.get('stripe-signature')!
  
  // 验证签名
  const event = stripe.webhooks.constructEvent(body, sig, webhookSecret)
  
  // 处理事件
  switch (event.type) {
    case 'payment_intent.succeeded':
      await handlePaymentSuccess(event.data.object)
      break
    case 'payment_intent.payment_failed':
      await handlePaymentFailed(event.data.object)
      break
    case 'charge.refunded':
      await handleRefund(event.data.object)
      break
  }
  
  return new Response('OK', { status: 200 })
})

async function handlePaymentSuccess(paymentIntent: any) {
  const supabase = createClient(...)
  
  // 更新支付记录
  await supabase
    .from('payments')
    .update({ 
      status: 'captured',
      response_data: paymentIntent,
      captured_at: new Date().toISOString()
    })
    .eq('provider_payment_id', paymentIntent.id)
  
  // 更新订单状态
  const order = await supabase
    .from('orders')
    .select('id')
    .eq('id', paymentIntent.metadata.order_id)
    .single()
  
  await supabase
    .from('orders')
    .update({ 
      status: 'confirmed',
      paid_at: new Date().toISOString()
    })
    .eq('id', order.id)
  
  // 提交库存（预留→实际扣减）
  await supabase.rpc('commit_inventory', { p_order_id: order.id })
  
  // 记录订单备注
  await supabase
    .from('order_notes')
    .insert({
      order_id: order.id,
      note_type: 'system',
      content: '支付成功，订单已确认'
    })
}
```

---

## 🔐 行级安全策略 (RLS)

```sql
-- 启用 RLS
ALTER TABLE products ENABLE ROW LEVEL SECURITY;
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE payments ENABLE ROW LEVEL SECURITY;

-- 商品：所有人可读，管理员可写
CREATE POLICY "Products viewable by everyone"
  ON products FOR SELECT USING (true);

CREATE POLICY "Only admins can modify products"
  ON products FOR INSERT WITH CHECK (
    auth.jwt() ->> 'role' = 'admin'
  );

-- 订单：用户只能看自己的
CREATE POLICY "Users can view own orders"
  ON orders FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can create own orders"
  ON orders FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- 支付：关联订单的权限
CREATE POLICY "Users can view own payments"
  ON payments FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM orders 
      WHERE orders.id = payments.order_id 
      AND orders.user_id = auth.uid()
    )
  );
```

---

## 📊 核心业务流程

### 订单创建流程（MVP）

```
┌─────────┐    ┌──────────────┐    ┌──────────────┐    ┌─────────┐
│  前端   │───▶│ Edge Function│───▶│  数据库     │───▶│  事件   │
│  提交   │    │  OrderService│    │  事务       │    │  Webhook│
└─────────┘    └──────────────┘    └──────────────┘    └─────────┘
                    │                    │                    │
                    │ 1. 获取购物车       │                    │
                    │───────────────────▶│                    │
                    │                    │                    │
                    │ 2. 计算价格         │                    │
                    │───────────────────▶│                    │
                    │                    │                    │
                    │ 3. 创建预留         │                    │
                    │───────────────────▶│                    │
                    │   (30 分钟)        │                    │
                    │                    │                    │
                    │ 4. 创建订单         │                    │
                    │───────────────────▶│                    │
                    │                    │                    │
                    │ 5. 创建订单项       │                    │
                    │───────────────────▶│                    │
                    │                    │                    │
                    │                    │ 6. 记录事件        │
                    │                    │───────────────────▶│
```

---

### 支付成功流程

```
┌─────────┐    ┌──────────────┐    ┌──────────────┐    ┌─────────┐
│ Stripe  │───▶│ Webhook     │───▶│  数据库     │───▶│  后续   │
│ 回调    │    │ Edge Function│    │  事务       │    │  操作   │
└─────────┘    └──────────────┘    └──────────────┘    └─────────┘
                    │                    │                    │
                    │ 1. 验证签名 ✅      │                    │
                    │                    │                    │
                    │ 2. 更新支付状态     │                    │
                    │───────────────────▶│                    │
                    │   captured         │                    │
                    │                    │                    │
                    │ 3. 更新订单状态     │                    │
                    │───────────────────▶│                    │
                    │   pending→confirmed│                    │
                    │                    │                    │
                    │ 4. 提交库存         │                    │
                    │───────────────────▶│                    │
                    │   (预留→扣减)      │                    │
                    │                    │                    │
                    │                    │ 5. 记录订单备注     │
                    │                    │───────────────────▶│
```

---

## 🎯 实施计划

### Phase 1: MVP（4-6 周）⭐ 当前阶段

**目标**: 上线验证商业模式

| 周次 | 任务 | 交付物 |
|------|------|--------|
| W1 | 数据库迁移 + RLS | 9 张表 + 安全策略 |
| W2 | OrderService + InventoryService | 核心服务 |
| W3 | Stripe 支付集成 | 支付流程打通 |
| W4 | 前端商品 + 购物车 | 可浏览可下单 |
| W5 | 前端结账 + 订单中心 | 完整购买流程 |
| W6 | 测试 + 部署 | 上线 |

**不做**: 优惠券、多仓库、管理后台、促销规则

---

### Phase 2: 增长（8-12 周）

**目标**: 支持业务增长

| 模块 | 功能 | 优先级 |
|------|------|--------|
| **促销** | 优惠券系统 | P1 |
| **促销** | 满减/满折规则 | P1 |
| **后台** | 商品管理 | P1 |
| **后台** | 订单管理 | P1 |
| **支付** | 支付宝集成 | P1 |
| **报表** | 基础销售数据 | P2 |

---

### Phase 3: 规模化（按需）

**目标**: 对标 Medusa 核心能力

| 功能 | 触发条件 |
|------|----------|
| 多仓库库存 | 真的需要多仓发货时 |
| 部分发货 | 订单量大到需要分批时 |
| 完整促销引擎 | 营销团队要求时 |
| 客户组定价 | 有 B2B/批发需求时 |
| 完整管理后台 | 运营团队扩大时 |

---

## 💰 成本估算

### 开发成本

| 阶段 | 人力 | 时间 | 总成本 |
|------|------|------|--------|
| Phase 1 (MVP) | 1-2 人 | 6 周 | 6-12 人周 |
| Phase 2 (增长) | 2 人 | 12 周 | 24 人周 |
| Phase 3 (按需) | 按需 | - | - |

### 运维成本

| 服务 | Supabase 免费 tier | 付费 tier |
|------|-------------------|-----------|
| 数据库 | 500MB (够用) | $25/月 (10GB) |
| Auth | 5 万 MAU | $25/月 (10 万) |
| Storage | 1GB | $10/月 (10GB) |
| Edge Functions | 50 万次/月 | $10/月 (200 万) |
| **总计** | **$0/月** | **$70/月** |

**对比 Medusa 自托管**: $50-110/月（服务器 + 数据库 + Redis）

---

## 🆚 vs Medusa 核心差异

| 维度 | 我们的方案 | Medusa |
|------|-----------|--------|
| **支付集成** | 直接调用 API（透明） | 插件（黑盒，有坑） |
| **代码量** | ~1000 行 | ~50 万行 |
| **学习曲线** | 低（标准技术栈） | 高（框架概念多） |
| **定制性** | 100% 可控 | 受框架约束 |
| **AI 集成** | Edge Function 直接调用 | 需要额外配置 |
| **部署** | Supabase 一键部署 | 自托管 VPS |
| **运维** | 0 运维 | 需要运维 |

---

## 📚 相关文档

- [[Supabase 电商 vs Medusa 差距分析]] - 功能对比
- [[电商方案对比 - Supabase vs WordPress vs Medusa]] - 选型分析
- [[Supabase Skill]] - 本地 CLI 操作

---

## 📝 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-02-25 | 初始架构设计 |
| v2.0 | 2026-02-26 | MVP 务实版：简化范围，明确 Phase 1 优先级，强化支付插件设计 |

---

*最后更新：2026-02-26*
