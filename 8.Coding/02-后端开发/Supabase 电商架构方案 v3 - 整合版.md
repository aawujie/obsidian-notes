# Supabase 电商架构方案 v3 - 整合版

**创建日期**: 2026-02-25  
**更新日期**: 2026-02-26  
**版本**: 3.0 (整合优化版)  
**标签**: #Supabase #电商 #架构设计 #EdgeFunctions #PostgreSQL #MVP

---

## 🎯 设计原则

> **"站在巨人肩膀上，不重复造轮子"**

| 原则 | 说明 |
|------|------|
| ✅ **复用现有项目** | 数据库设计 + Edge Functions 框架 |
| ✅ **保留核心理念** | 支付插件化 + 库存预留机制 |
| ✅ **MVP 优先** | 先上线验证，再迭代优化 |
| ✅ **直接透明** | 直接调用 API，无黑盒抽象 |
| ✅ **可扩展** | 需要时再加功能，不提前实现 |

---

## 📊 双方优缺点对比

### 现有项目 (`supabase-ecommerce-template`)

| 维度 | 优点 ✅ | 问题 ❌ |
|------|--------|--------|
| **数据库设计** | 完善（用户/角色/地址/分类） | 略复杂，MVP 用不上 |
| **Edge Functions** | 16 个函数，功能完整 | 命名不统一，风格混乱 |
| **事务处理** | 完整（begin/commit/rollback） | - |
| **错误处理** | 统一框架（error-handler.ts） | - |
| **支付集成** | Stripe 已验证可用 | ❌ 无插件抽象，无法切换 |
| **库存管理** | 直接扣减，简单 | ❌ 无预留，超卖风险 |
| **价格计算** | 基础计算 | ❌ 无促销引擎 |
| **用户系统** | 角色/权限完整 | ⚠️ MVP 过于复杂 |

---

### 我们的方案 (v2)

| 维度 | 优点 ✅ | 问题 ❌ |
|------|--------|--------|
| **支付设计** | 插件式（PaymentProvider 接口） | ❌ 未实现，仅设计 |
| **库存管理** | 预留机制（防超卖） | ❌ 未实现，仅设计 |
| **架构清晰** | 分层明确（Provider/Service/API） | ❌ 未验证 |
| **代码风格** | 统一规范 | ❌ 从零开始 |
| **MVP 范围** | 精简（4-6 周） | ❌ 可能遗漏必要功能 |
| **数据库** | 精简（9 张表） | ❌ 不如现有项目完善 |

---

## 🎯 v3.0 整合策略

### 核心思想

```
┌─────────────────────────────────────────────────────────┐
│                    v3.0 整合方案                         │
│                                                         │
│  数据库设计 → 复用现有项目（80%）+ 精简（20%）           │
│  Edge Functions → 复用现有项目 + 重构支付模块            │
│  支付架构 → 采用我们的插件式设计                         │
│  库存管理 → 现有项目 + 我们的预留机制                    │
│  代码规范 → 统一命名 + 现有项目的错误处理框架            │
└─────────────────────────────────────────────────────────┘
```

---

## 📋 整合清单

### 一、数据库设计（复用 + 精简）

#### ✅ 复用现有项目的表

| 表名 | 用途 | 说明 |
|------|------|------|
| `user_profiles` | 用户资料 | 保留（比纯 Auth 好用） |
| `products` | 商品表 | 保留（字段完善） |
| `product_categories` | 商品分类 | 保留（ltree 层级） |
| `product_variants` | 商品变体 | 保留 |
| `carts` + `cart_items` | 购物车 | 保留（有同步逻辑） |
| `orders` + `order_items` | 订单 | 保留（字段完善） |
| `user_addresses` | 地址簿 | 保留（结构化字段） |
| `payments` | 支付记录 | 保留 + 扩展 |
| `stripe_webhook_events` | Stripe 事件 | 保留 |
| `error_logs` | 错误日志 | 保留（调试有用） |
| `order_status_history` | 订单历史 | 保留（比 notes 更结构化） |

#### ❌ 精简的表（MVP 不做）

| 表名 | 原因 | 替代方案 |
|------|------|----------|
| `roles` + `user_roles` | MVP 不需要复杂权限 | 用 `is_admin` 字段足够 |
| `coupons` + `coupon_usage` | MVP 手动改价 | 后期再加 |
| `checkout_sessions` | 仅 Stripe Checkout 用 | 用 PaymentIntent 足够 |

#### ➕ 新增的表（我们的优势）

| 表名 | 用途 | SQL |
|------|------|-----|
| `inventory_reservations` | 库存预留 | 见下文 |

---

### 二、Edge Functions（复用 + 重构）

#### ✅ 直接复用的函数

| 函数 | 说明 | 改动 |
|------|------|------|
| `get-cart` | 获取购物车 | 无需改动 |
| `sync-cart` | 同步购物车 | 无需改动 |
| `list-products` | 商品列表 | 无需改动 |
| `get-order-detail` | 订单详情 | 无需改动 |
| `list-user-orders` | 订单列表 | 无需改动 |
| `stripe-webhook` | Stripe 回调 | 保留 + 扩展事件类型 |

#### 🔧 需要重构的函数

| 函数 | 问题 | 改进方案 |
|------|------|----------|
| `create-payment-intent` | 无插件抽象 | 实现 `PaymentProvider` 接口 |
| `create-order` | 无库存预留 | 添加预留逻辑 |
| `lock-product-stock` | 直接锁定 | 改为创建预留记录 |
| `restore-order-stock` | 直接恢复 | 改为释放预留记录 |

#### ❌ 删除的函数

| 函数 | 原因 |
|------|------|
| `createPaymentIntent` (重复) | 命名不统一，删除 |
| `getCart` (重复) | 命名不统一，删除 |
| `getOrderDetail` (重复) | 命名不统一，删除 |
| `listProducts` (重复) | 命名不统一，删除 |
| `listUserOrders` (重复) | 命名不统一，删除 |
| `syncCart` (重复) | 命名不统一，删除 |
| `placeOrder` | 用 `create-order` 足够 |

---

### 三、支付模块（采用我们的插件式设计）

#### 新增文件结构

```
supabase/functions/
├── 📁 providers/                    # 新增：支付提供商
│   ├── payment-provider.ts          # 接口定义
│   ├── stripe-provider.ts           # Stripe 实现
│   ├── alipay-provider.ts           # 支付宝实现（预留）
│   └── wechat-provider.ts           # 微信支付（预留）
│
├── 📁 services/                     # 新增：领域服务
│   └── payment-service.ts           # 支付服务（依赖注入）
│
├── 📁 api/                          # 新增：API 入口
│   └── create-payment-intent.ts     # 薄层，调用 Service
│
└── 📁 webhooks/                     # 重构：Webhook 处理
    └── stripe-webhook.ts            # 保留现有逻辑
```

---

### 四、库存管理（现有项目 + 我们的预留机制）

#### 现有项目的问题

```typescript
// 现有项目：下单时直接扣减
await supabaseClient.rpc('update_product_stock', {
  p_product_id: item.productId,
  p_quantity: -item.quantity  // ❌ 问题：未支付就扣减
})

// 问题场景：
// 1. 用户下单 → 库存扣减
// 2. 用户未支付，30 分钟后放弃
// 3. 库存无法恢复，其他用户无法购买
```

#### 我们的解决方案

```typescript
// v3.0: 下单时创建预留，支付成功后再扣减

// 步骤 1: 创建订单时
await supabase.from('inventory_reservations').insert({
  product_id: item.productId,
  quantity: item.quantity,
  order_id: order.id,
  expires_at: new Date(Date.now() + 30 * 60 * 1000), // 30 分钟
  status: 'active'
})

// 步骤 2: 支付成功（Webhook）
await supabase.rpc('commit_reservation', { p_order_id: order.id })
// → 预留记录标记为 'committed'
// → 实际扣减库存

// 步骤 3: 订单取消/超时
await supabase.rpc('release_reservation', { p_order_id: order.id })
// → 预留记录标记为 'released'
// → 库存自动恢复
```

---

## 🗄️ 数据库设计（v3.0 最终版）

### 新增表：库存预留表

```sql
-- 📁 migrations/20260226000000_create_inventory_reservations.sql

CREATE TABLE inventory_reservations (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  product_id uuid REFERENCES products(id) ON DELETE CASCADE,
  variant_id uuid REFERENCES product_variants(id) ON DELETE CASCADE,
  quantity int NOT NULL,
  
  -- 关联订单
  order_id uuid REFERENCES orders(id) ON DELETE CASCADE,
  
  -- 过期时间（自动释放）
  expires_at timestamptz NOT NULL,
  
  -- 状态
  status text DEFAULT 'active' CHECK (status IN ('active', 'committed', 'released')),
  
  created_at timestamptz DEFAULT now()
);

-- 索引
CREATE INDEX idx_reservations_order ON inventory_reservations(order_id);
CREATE INDEX idx_reservations_expires ON inventory_reservations(expires_at);
CREATE INDEX idx_reservations_status ON inventory_reservations(status);
CREATE INDEX idx_reservations_product ON inventory_reservations(product_id, variant_id);

-- 注释
COMMENT ON TABLE inventory_reservations IS '库存预留表：下单时预留，支付后扣减，超时自动释放';
```

---

### 新增函数：提交预留（支付成功后调用）

```sql
-- 📁 migrations/20260226000001_inventory_functions.sql

-- 提交预留（支付成功后）
CREATE OR REPLACE FUNCTION commit_reservation(p_order_id uuid)
RETURNS void AS $$
DECLARE
  res RECORD;
BEGIN
  -- 找到订单的所有预留记录
  FOR res IN 
    SELECT * FROM inventory_reservations 
    WHERE order_id = p_order_id AND status = 'active'
  LOOP
    -- 扣减实际库存
    UPDATE products 
    SET inventory = inventory - res.quantity
    WHERE id = res.product_id;
    
    -- 如果有变体，扣减变体库存
    IF res.variant_id IS NOT NULL THEN
      UPDATE product_variants 
      SET inventory = inventory - res.quantity
      WHERE id = res.variant_id;
    END IF;
    
    -- 标记预留为已提交
    UPDATE inventory_reservations 
    SET status = 'committed'
    WHERE id = res.id;
  END LOOP;
END;
$$ LANGUAGE plpgsql;

-- 释放预留（订单取消/超时）
CREATE OR REPLACE FUNCTION release_reservation(p_order_id uuid)
RETURNS void AS $$
BEGIN
  -- 标记预留为已释放（无需恢复库存，因为还没扣减）
  UPDATE inventory_reservations 
  SET status = 'released'
  WHERE order_id = p_order_id AND status = 'active';
END;
$$ LANGUAGE plpgsql;

-- 释放过期预留（定时调用）
CREATE OR REPLACE FUNCTION release_expired_reservations()
RETURNS TABLE (order_id uuid, released_count int) AS $$
BEGIN
  RETURN QUERY
  WITH expired AS (
    SELECT DISTINCT order_id
    FROM inventory_reservations
    WHERE status = 'active' AND expires_at < now()
  ),
  updated AS (
    UPDATE inventory_reservations r
    SET status = 'released'
    FROM expired e
    WHERE r.order_id = e.order_id AND r.status = 'active'
    RETURNING r.order_id
  )
  SELECT order_id, count(*)::int as released_count
  FROM updated
  GROUP BY order_id;
END;
$$ LANGUAGE plpgsql;
```

---

### 修改表：orders 表增加预留相关字段

```sql
-- 📁 migrations/20260226000002_add_reservation_fields.sql

ALTER TABLE orders
ADD COLUMN reservation_expires_at timestamptz,  -- 预留过期时间
ADD COLUMN reservation_committed_at timestamptz; -- 预留提交时间

-- 注释
COMMENT ON COLUMN orders.reservation_expires_at IS '库存预留过期时间';
COMMENT ON COLUMN orders.reservation_committed_at IS '库存预留提交时间（支付成功后）';
```

---

## ⚡ Edge Functions 设计（v3.0）

### 一、支付插件化架构

#### 1️⃣ 接口定义

```typescript
// 📁 supabase/functions/providers/payment-provider.ts

/**
 * 支付提供商统一接口
 * 所有支付渠道必须实现此接口
 */
export interface PaymentProvider {
  /** 支付渠道标识 */
  readonly name: string;  // 'stripe' | 'alipay' | 'wechat'
  
  /**
   * 初始化支付
   */
  initiatePayment(data: PaymentInitData): Promise<PaymentInitResult>;
  
  /**
   * 退款
   */
  refundPayment(paymentId: string, amount: number): Promise<RefundResult>;
  
  /**
   * 查询支付状态
   */
  getPaymentStatus(paymentId: string): Promise<PaymentStatus>;
}

export interface PaymentInitData {
  orderId: string;
  amount: number;
  currency: string;
  returnUrl: string;
  cancelUrl: string;
  metadata?: Record<string, any>;
}

export interface PaymentInitResult {
  providerPaymentId: string;
  redirectUrl?: string;    // 支付宝/微信需要跳转
  clientSecret?: string;   // Stripe Elements
  qrCodeUrl?: string;      // 微信扫码支付
}

export interface RefundResult {
  success: boolean;
  refundId: string;
  amount: number;
}

export interface PaymentStatus {
  status: 'pending' | 'authorized' | 'captured' | 'failed' | 'refunded';
  amount: number;
  capturedAmount?: number;
  refundedAmount?: number;
}
```

---

#### 2️⃣ Stripe 实现

```typescript
// 📁 supabase/functions/providers/stripe-provider.ts
import Stripe from 'https://esm.sh/stripe@14.21.0?target=deno'
import type { 
  PaymentProvider, 
  PaymentInitData, 
  PaymentInitResult,
  RefundResult,
  PaymentStatus 
} from './payment-provider.ts'

export class StripeProvider implements PaymentProvider {
  readonly name = 'stripe'
  private stripe: Stripe
  
  constructor(secretKey: string) {
    this.stripe = new Stripe(secretKey, {
      apiVersion: '2023-10-16',
      httpClient: Stripe.createFetchHttpClient()
    })
  }
  
  async initiatePayment(data: PaymentInitData): Promise<PaymentInitResult> {
    const paymentIntent = await this.stripe.paymentIntents.create({
      amount: Math.round(data.amount * 100),  // 转为分
      currency: data.currency.toLowerCase(),
      metadata: {
        order_id: data.orderId,
        ...data.metadata,
      },
      return_url: data.returnUrl,
    })
    
    return {
      providerPaymentId: paymentIntent.id,
      clientSecret: paymentIntent.client_secret!,
    }
  }
  
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
      capturedAmount: paymentIntent.amount_captured / 100,
      refundedAmount: (paymentIntent.amount_refunded || 0) / 100,
    }
  }
}
```

---

#### 3️⃣ 支付服务（依赖注入）

```typescript
// 📁 supabase/functions/services/payment-service.ts
import type { 
  PaymentProvider, 
  PaymentInitData, 
  PaymentInitResult,
  RefundResult,
  PaymentStatus 
} from '../providers/payment-provider.ts'

export class PaymentService {
  private providers: Map<string, PaymentProvider> = new Map()
  private defaultProvider: string
  
  constructor(defaultProvider: string = 'stripe') {
    this.defaultProvider = defaultProvider
  }
  
  /**
   * 注册支付提供商（插件式核心）
   */
  registerProvider(provider: PaymentProvider) {
    this.providers.set(provider.name, provider)
  }
  
  /**
   * 获取支付提供商
   */
  getProvider(name?: string): PaymentProvider {
    const providerName = name || this.defaultProvider
    const provider = this.providers.get(providerName)
    
    if (!provider) {
      throw new Error(`Payment provider "${providerName}" not found`)
    }
    
    return provider
  }
  
  /**
   * 创建支付
   */
  async createPayment(data: {
    orderId: string
    amount: number
    currency: string
    provider?: string
    returnUrl: string
    cancelUrl: string
    metadata?: Record<string, any>
  }): Promise<PaymentInitResult> {
    const provider = this.getProvider(data.provider)
    
    const result = await provider.initiatePayment({
      orderId: data.orderId,
      amount: data.amount,
      currency: data.currency,
      returnUrl: data.returnUrl,
      cancelUrl: data.cancelUrl,
      metadata: data.metadata,
    })
    
    return result
  }
  
  /**
   * 退款
   */
  async refundPayment(params: {
    paymentId: string
    amount: number
    provider: string
  }): Promise<RefundResult> {
    const provider = this.getProvider(params.provider)
    return await provider.refundPayment(params.paymentId, params.amount)
  }
}
```

---

#### 4️⃣ 配置与初始化

```typescript
// 📁 supabase/functions/config.ts
import { StripeProvider } from './providers/stripe-provider.ts'
import { PaymentService } from './services/payment-service.ts'

/**
 * 创建支付服务实例
 */
export function createPaymentService(): PaymentService {
  const paymentService = new PaymentService('stripe')
  
  // 注册 Stripe
  const stripeKey = Deno.env.get('STRIPE_SECRET_KEY')
  if (stripeKey) {
    paymentService.registerProvider(new StripeProvider(stripeKey))
  }
  
  // TODO: 注册支付宝
  // if (Deno.env.get('ALIPAY_APP_ID')) {
  //   paymentService.registerProvider(new AlipayProvider(...))
  // }
  
  // TODO: 注册微信支付
  // if (Deno.env.get('WECHAT_APP_ID')) {
  //   paymentService.registerProvider(new WechatProvider(...))
  // }
  
  return paymentService
}
```

---

#### 5️⃣ API 入口（薄层）

```typescript
// 📁 supabase/functions/api/create-payment-intent/index.ts
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'
import { createPaymentService } from '../../config.ts'
import { corsHeaders } from '../../_shared/cors.ts'
import { 
  successResponse, 
  errorResponse,
  validationErrorResponse,
  unauthorizedResponse,
  optionsResponse 
} from '../../_shared/api-response.ts'

serve(async (req) => {
  // 处理 CORS
  if (req.method === 'OPTIONS') {
    return optionsResponse()
  }

  try {
    // 验证用户
    const supabaseClient = createClient(
      Deno.env.get('SUPABASE_URL')!,
      Deno.env.get('SUPABASE_ANON_KEY')!,
      {
        global: {
          headers: { Authorization: req.headers.get('Authorization') || '' },
        },
      }
    )

    const { data: { user }, error: authError } = await supabaseClient.auth.getUser()
    if (authError || !user) {
      return unauthorizedResponse('需要登录')
    }

    // 解析请求
    const { amount, currency = 'CNY', orderId, metadata = {} } = await req.json()
    
    // 验证参数
    if (!amount || amount <= 0) {
      return validationErrorResponse({ amount: '金额必须为正数' })
    }

    // 创建支付服务
    const paymentService = createPaymentService()
    
    // 创建支付
    const result = await paymentService.createPayment({
      orderId,
      amount,
      currency,
      returnUrl: `${Deno.env.get('FRONTEND_URL')}/payment/success`,
      cancelUrl: `${Deno.env.get('FRONTEND_URL')}/payment/cancel`,
      metadata: {
        user_id: user.id,
        ...metadata,
      },
    })

    // 保存支付记录到数据库
    await supabaseClient.from('payments').insert({
      order_id: orderId,
      user_id: user.id,
      provider: 'stripe',
      provider_payment_id: result.providerPaymentId,
      amount,
      currency,
      status: 'pending',
      response_data: result,
    })

    return successResponse(result, {}, '支付意向创建成功')

  } catch (error) {
    console.error('Create payment intent error:', error)
    return errorResponse(
      error.code || 'PAYMENT_ERROR',
      error.message || '创建支付失败',
      null,
      500
    )
  }
})
```

---

### 二、订单创建（集成库存预留）

```typescript
// 📁 supabase/functions/create-order/index.ts (v3.0 改进版)

import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'
import { corsHeaders } from '../_shared/cors.ts'
import { 
  successResponse, 
  errorResponse,
  validationErrorResponse,
  unauthorizedResponse,
  optionsResponse 
} from '../_shared/api-response.ts'

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return optionsResponse()
  }

  try {
    const supabaseClient = createClient(
      Deno.env.get('SUPABASE_URL')!,
      Deno.env.get('SUPABASE_ANON_KEY')!,
      {
        global: {
          headers: { Authorization: req.headers.get('Authorization') || '' },
        },
      }
    )

    // 验证用户
    const { data: { user }, error: authError } = await supabaseClient.auth.getUser()
    if (authError || !user) {
      return unauthorizedResponse('需要登录')
    }

    // 解析请求
    const { cartId, shippingAddressId, paymentMethod, notes } = await req.json()

    // 验证参数
    if (!cartId || !shippingAddressId || !paymentMethod) {
      return validationErrorResponse({
        cartId: !cartId ? '购物车 ID 不能为空' : undefined,
        shippingAddressId: !shippingAddressId ? '收货地址不能为空' : undefined,
        paymentMethod: !paymentMethod ? '支付方式不能为空' : undefined,
      }.filter(Boolean))
    }

    // 开启事务
    await supabaseClient.rpc('begin_transaction')

    try {
      // 1. 验证购物车
      const { data: cart, error: cartError } = await supabaseClient
        .from('carts')
        .select('id, user_id')
        .eq('id', cartId)
        .eq('user_id', user.id)
        .single()

      if (cartError || !cart) {
        throw { code: 'CART_NOT_FOUND', message: '购物车不存在' }
      }

      // 2. 获取购物车项
      const { data: cartItems } = await supabaseClient
        .from('cart_items')
        .select(`
          id, product_id, variant_id, quantity,
          products (id, name, price, inventory),
          product_variants (id, inventory)
        `)
        .eq('cart_id', cartId)

      if (!cartItems || cartItems.length === 0) {
        throw { code: 'CART_EMPTY', message: '购物车为空' }
      }

      // 3. 检查库存
      for (const item of cartItems) {
        const availableStock = item.product_variants?.inventory || item.products.inventory
        if (availableStock < item.quantity) {
          throw { 
            code: 'INSUFFICIENT_STOCK', 
            message: `${item.products.name} 库存不足` 
          }
        }
      }

      // 4. 计算总价
      const totalAmount = cartItems.reduce(
        (sum, item) => sum + (item.products.price * item.quantity), 
        0
      )

      // 5. 获取收货地址
      const { data: address } = await supabaseClient
        .from('user_addresses')
        .select('*')
        .eq('id', shippingAddressId)
        .eq('user_id', user.id)
        .single()

      // 6. 创建订单
      const { data: order } = await supabaseClient
        .from('orders')
        .insert({
          user_id: user.id,
          status: 'pending',
          total_amount: totalAmount,
          shipping_address_snapshot: address,
          payment_method: paymentMethod,
          notes,
          reservation_expires_at: new Date(Date.now() + 30 * 60 * 1000).toISOString(),
        })
        .select()
        .single()

      // 7. 创建订单项
      const orderItems = cartItems.map(item => ({
        order_id: order.id,
        product_id: item.product_id,
        variant_id: item.variant_id,
        quantity: item.quantity,
        price: item.products.price,
        product_name: item.products.name,
      }))

      await supabaseClient.from('order_items').insert(orderItems)

      // 8. 创建库存预留（🎯 v3.0 核心改进）
      const reservations = cartItems.map(item => ({
        product_id: item.product_id,
        variant_id: item.variant_id,
        quantity: item.quantity,
        order_id: order.id,
        expires_at: new Date(Date.now() + 30 * 60 * 1000).toISOString(),
        status: 'active',
      }))

      await supabaseClient.from('inventory_reservations').insert(reservations)

      // 9. 清空购物车
      await supabaseClient.from('cart_items').delete().eq('cart_id', cartId)

      // 10. 记录订单历史
      await supabaseClient.from('order_status_history').insert({
        order_id: order.id,
        status: 'pending',
        notes: '订单创建，库存已预留（30 分钟）',
      })

      // 提交事务
      await supabaseClient.rpc('commit_transaction')

      return successResponse({
        order_id: order.id,
        order_number: order.order_number,
        total_amount: totalAmount,
        reservation_expires_at: order.reservation_expires_at,
      }, {}, '订单创建成功')

    } catch (error) {
      // 回滚事务
      await supabaseClient.rpc('rollback_transaction')
      throw error
    }

  } catch (error) {
    console.error('Create order error:', error)
    return errorResponse(
      error.code || 'ORDER_ERROR',
      error.message || '创建订单失败',
      null,
      500
    )
  }
})
```

---

### 三、Stripe Webhook（集成库存提交）

```typescript
// 📁 supabase/functions/webhooks/stripe-webhook/index.ts (v3.0 改进版)

import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'
import Stripe from 'https://esm.sh/stripe@14.21.0?target=deno'
import { corsHeaders } from '../../_shared/cors.ts'

const stripe = new Stripe(Deno.env.get('STRIPE_SECRET_KEY')!, {
  apiVersion: '2023-10-16',
  httpClient: Stripe.createFetchHttpClient()
})

const webhookSecret = Deno.env.get('STRIPE_WEBHOOK_SECRET')!

serve(async (req) => {
  const signature = req.headers.get('stripe-signature')!
  
  if (!signature) {
    return new Response('Missing signature', { status: 400 })
  }

  const body = await req.text()
  
  let event: Stripe.Event
  try {
    event = stripe.webhooks.constructEvent(body, signature, webhookSecret)
  } catch (err) {
    console.error('Webhook signature verification failed:', err)
    return new Response('Invalid signature', { status: 400 })
  }

  const supabase = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
  )

  // 记录事件
  await supabase.from('stripe_webhook_events').insert({
    stripe_event_id: event.id,
    event_type: event.type,
    event_data: event.data.object,
  })

  // 处理事件
  switch (event.type) {
    case 'payment_intent.succeeded':
      await handlePaymentSuccess(event.data.object, supabase)
      break
    
    case 'payment_intent.payment_failed':
      await handlePaymentFailed(event.data.object, supabase)
      break
  }

  return new Response('OK', { status: 200 })
})

async function handlePaymentSuccess(paymentIntent: any, supabase: any) {
  const orderId = paymentIntent.metadata.order_id
  
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
  await supabase
    .from('orders')
    .update({ 
      status: 'confirmed',
      paid_at: new Date().toISOString(),
      reservation_committed_at: new Date().toISOString(),
    })
    .eq('id', orderId)

  // 🎯 v3.0 核心改进：提交库存预留（实际扣减）
  await supabase.rpc('commit_reservation', { p_order_id: orderId })

  // 记录订单历史
  await supabase.from('order_status_history').insert({
    order_id: orderId,
    status: 'confirmed',
    notes: '支付成功，库存已扣减',
  })

  console.log(`Order ${orderId} payment success, inventory committed`)
}

async function handlePaymentFailed(paymentIntent: any, supabase: any) {
  const orderId = paymentIntent.metadata.order_id
  
  // 更新支付记录
  await supabase
    .from('payments')
    .update({ 
      status: 'failed',
      response_data: paymentIntent,
      failed_at: new Date().toISOString()
    })
    .eq('provider_payment_id', paymentIntent.id)

  // 更新订单状态
  await supabase
    .from('orders')
    .update({ 
      status: 'cancelled',
      cancelled_at: new Date().toISOString()
    })
    .eq('id', orderId)

  // 🎯 v3.0 核心改进：释放库存预留
  await supabase.rpc('release_reservation', { p_order_id: orderId })

  // 记录订单历史
  await supabase.from('order_status_history').insert({
    order_id: orderId,
    status: 'cancelled',
    notes: '支付失败，库存已释放',
  })

  console.log(`Order ${orderId} payment failed, inventory released`)
}
```

---

## 📁 最终项目结构

```
supabase-ecommerce/
├── 📁 supabase/
│   ├── 📁 migrations/
│   │   ├── 001-user-profiles.sql          # 复用现有项目
│   │   ├── 002-products.sql               # 复用现有项目
│   │   ├── 003-orders.sql                 # 复用现有项目
│   │   ├── 004-payments.sql               # 复用现有项目
│   │   ├── 005-inventory-reservations.sql # 🆕 新增
│   │   ├── 006-inventory-functions.sql    # 🆕 新增
│   │   └── 007-rls-policies.sql           # 复用 + 精简
│   │
│   ├── 📁 functions/
│   │   ├── 📁 _shared/                    # 复用现有项目
│   │   │   ├── cors.ts
│   │   │   ├── api-response.ts
│   │   │   ├── error-handler.ts
│   │   │   └── error-logging.ts
│   │   │
│   │   ├── 📁 providers/                  # 🆕 新增：支付插件
│   │   │   ├── payment-provider.ts
│   │   │   ├── stripe-provider.ts
│   │   │   ├── alipay-provider.ts         # 预留
│   │   │   └── wechat-provider.ts         # 预留
│   │   │
│   │   ├── 📁 services/                   # 🆕 新增：领域服务
│   │   │   └── payment-service.ts
│   │   │
│   │   ├── 📁 config.ts                   # 🆕 新增：配置
│   │   │
│   │   ├── 📁 api/                        # 🆕 新增：API 入口
│   │   │   └── create-payment-intent.ts
│   │   │
│   │   ├── 📁 create-order/               # 重构：集成预留
│   │   │   └── index.ts
│   │   │
│   │   ├── 📁 webhooks/                   # 重构：集成预留提交
│   │   │   └── stripe-webhook.ts
│   │   │
│   │   ├── 📁 get-cart/                   # 复用现有项目
│   │   ├── 📁 sync-cart/                  # 复用现有项目
│   │   ├── 📁 list-products/              # 复用现有项目
│   │   ├── 📁 get-order-detail/           # 复用现有项目
│   │   └── 📁 list-user-orders/           # 复用现有项目
│   │
│   └── config.toml
│
├── 📁 frontend/
│   └── （Next.js 前端，后续开发）
│
└── 📁 docs/
    ├── architecture.md
    ├── api-reference.md
    └── mvp-scope.md
```

---

## 🎯 实施计划

### Phase 1: 迁移现有项目（1 周）

| 任务 | 说明 | 状态 |
|------|------|------|
| 链接 Supabase 项目 | `npx supabase link` | ⬜ |
| 应用数据库迁移 | `npx supabase db push` | ⬜ |
| 部署 Edge Functions | `npx supabase functions deploy` | ⬜ |
| 配置环境变量 | `.env` 文件 | ⬜ |
| 测试 Stripe 支付 | 完整流程测试 | ⬜ |

---

### Phase 2: 支付插件化（1 周）

| 任务 | 说明 | 状态 |
|------|------|------|
| 创建 `PaymentProvider` 接口 | `providers/payment-provider.ts` | ⬜ |
| 实现 `StripeProvider` | 迁移现有逻辑 | ⬜ |
| 创建 `PaymentService` | 依赖注入 | ⬜ |
| 重构 `create-payment-intent` | 调用 Service | ⬜ |
| 测试支付流程 | 确保功能正常 | ⬜ |

---

### Phase 3: 库存预留（1 周）

| 任务 | 说明 | 状态 |
|------|------|------|
| 创建 `inventory_reservations` 表 | 新增迁移 | ⬜ |
| 实现 `commit_reservation` 函数 | SQL 函数 | ⬜ |
| 实现 `release_reservation` 函数 | SQL 函数 | ⬜ |
| 修改 `create-order` | 集成预留逻辑 | ⬜ |
| 修改 `stripe-webhook` | 集成提交/释放 | ⬜ |
| 测试预留流程 | 超时释放测试 | ⬜ |

---

### Phase 4: 前端对接（2 周）

| 任务 | 说明 | 状态 |
|------|------|------|
| 商品列表页 | 展示商品 | ⬜ |
| 购物车页面 | 添加/删除/修改 | ⬜ |
| 结账页面 | 地址选择 + 支付 | ⬜ |
| 订单中心 | 查看订单状态 | ⬜ |
| Stripe Elements | 前端支付集成 | ⬜ |

---

## 📊 功能对比（v3.0 最终版）

| 功能 | 现有项目 | 我们的 v2 | v3.0 整合版 |
|------|---------|----------|------------|
| **数据库设计** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ (复用) |
| **Edge Functions** | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ (复用 + 重构) |
| **支付插件化** | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ (整合) |
| **库存预留** | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ (整合) |
| **事务处理** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ (复用) |
| **错误处理** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ (复用) |
| **代码规范** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ (统一) |
| **MVP 范围** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ (精简) |

---

## 💰 成本估算

### 开发成本

| 阶段 | 人力 | 时间 | 总成本 |
|------|------|------|--------|
| Phase 1 (迁移) | 1 人 | 1 周 | 1 人周 |
| Phase 2 (支付) | 1 人 | 1 周 | 1 人周 |
| Phase 3 (库存) | 1 人 | 1 周 | 1 人周 |
| Phase 4 (前端) | 1-2 人 | 2 周 | 2-4 人周 |
| **总计** | - | **5 周** | **5-7 人周** |

**对比**:
- 从零实现 v2: 6 周
- 整合 v3.0: 5 周（节省 1 周，且质量更高）

### 运维成本

| 服务 | 免费 tier | 付费 tier |
|------|----------|-----------|
| Supabase | $0/月 | $25/月起 |
| Stripe | 2.9% + ¥0.3/笔 | 同左 |
| **总计** | **$0/月** | **$25/月 + 手续费** |

---

## 📚 相关文档

### 核心文档
- [[Supabase 电商架构方案 v2 - 设计理念]] - 设计理念参考（支付插件化/库存预留思路）
- [[Supabase 电商 vs Medusa 差距分析]] - 竞品对比
- [[电商方案对比 - Supabase vs WordPress vs Medusa]] - 选型分析

### 文档使用建议
| 文档 | 用途 |
|------|------|
| **v3 整合版** | 🚀 **主实施指南** - 实际开发参考这个 |
| **v2 设计理念** | 📖 辅助参考 - 理解为什么这样设计 |
| **差距分析** | 🔍 竞品对比 - 了解与 Medusa 的差异 |

---

## 📝 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-02-25 | 初始架构设计 |
| v2.0 | 2026-02-26 | MVP 务实版 |
| v3.0 | 2026-02-26 | 整合优化版（现有项目 + 我们的优势） |

---

*最后更新：2026-02-26*
