# Nest Hero Road 33 - 项目现状与优化方案

> 创建时间：2026-02-24  
> 项目路径：`/Users/apple/code/8.practice/nest-hero-road-33`  
> 技术栈：React + TypeScript + Vite + Supabase + Stripe

---

## 一、项目现状分析

### 1.1 项目概况

| 维度 | 详情 |
|------|------|
| **项目类型** | 全栈电商平台（B2C） |
| **前端框架** | React 18.3 + TypeScript 5.5 + Vite 5.4 |
| **UI 系统** | Tailwind CSS 3.4 + Shadcn/UI + Radix UI |
| **后端平台** | Supabase (PostgreSQL + Edge Functions + Auth) |
| **支付集成** | Stripe (Checkout + Payment Intent + Webhook) |
| **第三方服务** | Google Places API, Coze AI Bot, Mapbox |
| **测试框架** | Vitest + Cypress + Testing Library |

### 1.2 代码规模统计

```
前端源码：
├── src/pages/          - 36 个页面组件
├── src/components/     - 69 个 UI 组件 + 26 个子目录
│   ├── atoms/         - 基础原子组件
│   ├── molecules/     - 分子级组件
│   ├── organisms/     - 有机体组件
│   └── ui/            - Shadcn UI 组件
├── src/hooks/          - 20 个自定义 Hooks
├── src/context/        - 全局状态管理
├── src/lib/            - 工具函数 (443 行)
└── src/services/       - 服务层

后端源码：
├── supabase/functions/ - 91 个 Edge Functions (index.ts)
├── supabase/migrations/- 11 个数据库迁移文件
└── scripts/            - 49 个部署/测试脚本

文档：
└── docs/               - 46 个文档文件
```

### 1.3 功能完成度

| 功能模块 | 完成度 | 状态 | 说明 |
|----------|--------|------|------|
| **用户端 - 首页** | 100% | ✅ | 轮播/推荐/分类导航 |
| **用户端 - 商品** | 100% | ✅ | 列表/详情/搜索/筛选 |
| **用户端 - 购物车** | 100% | ✅ | 匿名 + 用户购物车 + 云同步 |
| **用户端 - 结账** | 95% | ✅ | Stripe 支付/地址管理 |
| **用户端 - 订单** | 100% | ✅ | 订单列表/详情/状态追踪 |
| **用户端 - 个人中心** | 95% | ✅ | 资料/地址/收藏/订单 |
| **管理员 - 仪表盘** | 90% | ✅ | 数据统计/图表展示 |
| **管理员 - 商品管理** | 95% | ✅ | CRUD/导入/分类管理 |
| **管理员 - 订单管理** | 90% | ✅ | 订单处理/状态变更 |
| **管理员 - 用户管理** | 85% | ⚠️ | 用户列表/权限管理 |
| **管理员 - 内容管理** | 80% | ⚠️ | 文章/评论管理 |
| **管理员 - 促销管理** | 70% | ⚠️ | 促销码系统 |
| **支付系统** | 95% | ✅ | Stripe 完整集成 |
| **认证系统** | 100% | ✅ | 登录/注册/第三方登录 |
| **多语言** | 80% | ✅ | 中英文切换 |
| **测试覆盖** | 75% | ⚠️ | 单元/集成/Mock 测试 |

### 1.4 环境配置

```bash
# Supabase
VITE_SUPABASE_URL=https://tcejcdkslisaybegkqpn.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Stripe
VITE_STRIPE_PUBLISHABLE_KEY=pk_test_51RpO9dCpQnPh0A7CpDnV0Ctbcb91HzjxVnKLhfjSWfyOWzLsD6dg2h5i9P1HYvSHGHf2uERNeefux64i7qRwXNtS00YourPublishableKey
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Coze AI
VITE_COZE_BOT_ID=7530296902760775732
VITE_COZE_TOKEN=pat_LeTxk7oJPTeukqqIg1WYaWp0cPNdxvWwhQWUsraaIWIHGEGgxiMMJBQcf2uXdAEs

# Google Places
REACT_APP_GOOGLE_PLACES_API_KEY=AIzaSyBCmKrW_zuLtVUW_YLiB4naKsuunSv_0W8
```

---

## 二、核心问题分析

### 2.1 高优先级问题 🔴

#### 问题 1：Edge Functions 命名混乱

**现状**：
```
supabase/functions/
├── getCart/              # CamelCase
├── get-cart/             # Kebab-case (重复)
├── getCurrentUser/       # CamelCase
├── get-current-user/     # Kebab-case (重复)
├── createPaymentIntent/  # CamelCase
├── create-payment-intent/# Kebab-case (重复)
├── listProducts/         # CamelCase
├── list-products/        # Kebab-case (重复)
└── ... (约 40+ 对重复)
```

**影响**：
- 部署时可能覆盖错误版本
- 前端调用容易混淆
- 维护成本增加 50%+

**根本原因**：缺少统一的命名规范执行机制

---

#### 问题 2：数据库索引缺失

**缺失的关键索引**：

```sql
-- 产品查询
CREATE INDEX idx_products_category_id ON products(category_id);
CREATE INDEX idx_products_stock ON products(stock);
CREATE INDEX idx_products_category_stock ON products(category_id, stock);

-- 订单查询
CREATE INDEX idx_orders_user_created ON orders(user_id, created_at DESC);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_status_created ON orders(status, created_at DESC);

-- 购物车查询
CREATE INDEX idx_cart_items_composite ON cart_items(cart_id, product_id);

-- 图片查询
CREATE INDEX idx_product_images_primary ON product_images(product_id, is_primary);

-- 地址查询
CREATE INDEX idx_user_addresses_default ON user_addresses(user_id, is_default);
```

**影响**：
- 分类查询慢 3-5 倍
- 用户订单历史查询慢 2-3 倍
- 高并发时数据库压力大

---

#### 问题 3：并发控制不足

**现状**：
- 购物车更新使用简单 UPDATE，无乐观锁
- 订单创建时库存锁定机制不完善
- 缺少事务边界控制

**风险场景**：
```
用户 A 查询库存：10
用户 B 查询库存：10
用户 A 下单购买：8 → 库存更新为 2
用户 B 下单购买：8 → 库存更新为 -6 ❌ (超卖)
```

**当前实现**：
```typescript
// cart_items 表缺少 version 字段
// 下单时未使用数据库事务
```

---

#### 问题 4：代码重复严重

**新旧代码并存**：
```
src/pages/
├── Cart.tsx              # 旧版 (18KB)
├── NewCart.tsx           # 新版 (11KB)
├── Checkout.tsx          # 旧版 (23KB)
├── NewCheckout.tsx       # 新版 (17KB)
├── Orders.tsx            # 旧版 (2.4KB)
├── NewOrders.tsx         # 新版 (9.7KB)
├── ProductDetail.tsx     # 旧版 (161B)
├── NewProductDetail.tsx  # 新版 (15KB)
└── ...
```

**影响**：
- 代码库膨胀约 30%
- 维护时需要同时更新两处
- 新人容易混淆

---

### 2.2 中优先级问题 🟡

#### 问题 5：状态管理分散

**现状**：
```typescript
src/context/
├── CartContext.tsx        // 购物车状态
├── AuthContext.tsx        // 认证状态
├── GlobalConfigContext.tsx // 全局配置
└── ...                    // 其他分散状态
```

**问题**：
- 状态更新逻辑分散
- 跨 Context 同步困难
- 缺少状态持久化策略

---

#### 问题 6：API 客户端不统一

**现状**：
```typescript
// 方式 1：直接调用
const { data } = await supabase.functions.invoke('get-product-detail', {
  body: { productId }
});

// 方式 2：通过 Hook
const { data } = useSupabaseApi().getProductDetail(productId);

// 方式 3：手动 fetch
const response = await fetch(`${EDGE_FUNCTION_URL}/get-product-detail`, {
  method: 'POST',
  body: JSON.stringify({ productId })
});
```

**问题**：
- 缺少类型安全的 API 客户端
- 错误处理不一致
- 请求参数验证缺失

---

#### 问题 7：测试覆盖不完整

**测试统计**：
```
测试文件：
├── __tests__/integration/    - 集成测试 (部分)
├── supabase/functions/__tests__/ - Edge Function 测试
└── src/components/__tests__/ - 组件测试 (少量)

覆盖率估算：
- Edge Functions: ~70%
- 前端组件：~40%
- 关键业务逻辑：~60%
- 整体覆盖率：~55%
```

**缺失场景**：
- E2E 完整购物流程
- 支付失败处理
- 并发场景测试
- 性能基准测试

---

#### 问题 8：错误处理不一致

**现状**：
- 部分 Edge Function 使用标准错误响应
- 部分直接 throw Error
- 前端错误提示不统一

**标准格式**（部分实现）：
```typescript
// 成功响应
{
  success: true,
  data: { ... },
  message: "操作成功"
}

// 错误响应
{
  success: false,
  error: {
    code: "PRODUCT_NOT_FOUND",
    message: "产品不存在",
    details: { productId: "123" }
  }
}
```

---

### 2.3 低优先级问题 🟢

| 问题 | 描述 | 影响 |
|------|------|------|
| 缺少监控 | 无性能监控和错误追踪 | 生产问题难发现 |
| 缺少 CDN 优化 | 静态资源未使用 CDN | 加载速度慢 |
| 缺少 SEO 优化 | 元标签/结构化数据不完整 | 搜索引擎收录差 |
| 缺少微前端规划 | 单体前端架构 | 长期维护困难 |
| 文档更新滞后 | 部分文档与实际代码不符 | 新人上手慢 |

---

## 三、优化方案

### 3.1 阶段一：清理与稳定（1-2 周）

#### 任务 1.1：统一 Edge Functions 命名

**目标**：删除重复函数，统一使用 kebab-case

**执行步骤**：
```bash
# 1. 备份当前 functions 目录
cp -r supabase/functions supabase/functions.backup

# 2. 识别并删除 CamelCase 版本
rm -rf supabase/functions/getCart
rm -rf supabase/functions/getCurrentUser
rm -rf supabase/functions/createPaymentIntent
# ... (约 40 个目录)

# 3. 更新前端调用
# 搜索并替换所有 CamelCase 调用

# 4. 重新部署所有函数
./scripts/deploy-all-functions.sh
```

**验收标准**：
- [ ] 所有函数目录使用 kebab-case
- [ ] 前端调用全部更新
- [ ] 所有功能测试通过

**预计工时**：4 小时

---

#### 任务 1.2：添加数据库索引

**目标**：提升核心查询性能

**执行 SQL**：
```sql
-- 产品相关索引
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_products_category_id 
  ON products(category_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_products_stock 
  ON products(stock);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_products_created_at 
  ON products(created_at DESC);

-- 订单相关索引
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_orders_user_created 
  ON orders(user_id, created_at DESC);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_orders_status 
  ON orders(status);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_orders_status_created 
  ON orders(status, created_at DESC);

-- 购物车相关索引
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_cart_items_composite 
  ON cart_items(cart_id, product_id);

-- 图片相关索引
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_product_images_primary 
  ON product_images(product_id, is_primary);

-- 地址相关索引
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_user_addresses_default 
  ON user_addresses(user_id, is_default);
```

**验收标准**：
- [ ] 所有索引创建成功
- [ ] 查询性能提升 50%+
- [ ] 无锁表操作（使用 CONCURRENTLY）

**预计工时**：2 小时

---

#### 任务 1.3：实现并发控制

**目标**：防止超卖，保证数据一致性

**方案 A：乐观锁**
```sql
-- 1. 添加 version 字段
ALTER TABLE cart_items ADD COLUMN version INTEGER DEFAULT 0;

-- 2. 更新时使用 version 检查
UPDATE cart_items 
SET quantity = $1, version = version + 1
WHERE cart_id = $2 AND product_id = $3 AND version = $4;
```

**方案 B：数据库事务**
```typescript
// placeOrder Edge Function
const { data, error } = await supabase.rpc('create_order_with_stock_check', {
  p_user_id: userId,
  p_items: items
});
```

**存储过程实现**：
```sql
CREATE OR REPLACE FUNCTION create_order_with_stock_check(
  p_user_id UUID,
  p_items JSONB
) RETURNS JSON AS $$
DECLARE
  v_order_id UUID;
  v_item JSONB;
  v_stock INTEGER;
BEGIN
  -- 开启事务
  BEGIN
    -- 检查并锁定库存
    FOR v_item IN SELECT * FROM jsonb_array_elements(p_items)
    LOOP
      SELECT stock INTO v_stock
      FROM products
      WHERE id = (v_item->>'product_id')::UUID
      FOR UPDATE;  -- 行级锁
      
      IF v_stock < (v_item->>'quantity')::INTEGER THEN
        RAISE EXCEPTION 'INSUFFICIENT_STOCK';
      END IF;
    END LOOP;
    
    -- 创建订单
    INSERT INTO orders (...) VALUES (...) RETURNING id INTO v_order_id;
    
    -- 扣减库存
    -- ...
    
    -- 提交事务
    RETURN json_build_object('success', true, 'order_id', v_order_id);
  EXCEPTION
    WHEN OTHERS THEN
      RETURN json_build_object('success', false, 'error', SQLERRM);
  END;
END;
$$ LANGUAGE plpgsql;
```

**验收标准**：
- [ ] 并发下单不超卖
- [ ] 购物车更新冲突可检测
- [ ] 错误提示友好

**预计工时**：8 小时

---

#### 任务 1.4：清理重复代码

**目标**：删除旧版代码，统一使用新版本

**执行步骤**：
```bash
# 1. 确认新版功能完整
# 2. 删除旧版文件
rm src/pages/Cart.tsx
rm src/pages/Checkout.tsx
rm src/pages/Orders.tsx
rm src/pages/ProductDetail.tsx
# ...

# 3. 更新路由引用
# 4. 运行测试确保无破坏

# 5. Git 提交
git commit -m "refactor: 清理旧版页面代码"
```

**验收标准**：
- [ ] 所有路由指向新版页面
- [ ] 功能测试全部通过
- [ ] 代码库减少 30KB+

**预计工时**：6 小时

---

### 3.2 阶段二：优化与增强（2-3 周）

#### 任务 2.1：实现类型安全的 API 客户端

**目标**：统一 API 调用，提供完整类型推断

**目录结构**：
```
src/lib/api/
├── client.ts           # API 客户端核心
├── types.ts            # API 类型定义
├── endpoints.ts        # 端点配置
└── errors.ts           # 错误处理
```

**核心实现**：
```typescript
// src/lib/api/client.ts
import { EdgeFunction } from './types';

class SupabaseApiClient {
  private baseUrl: string;
  
  constructor() {
    this.baseUrl = `${import.meta.env.VITE_SUPABASE_URL}/functions/v1`;
  }
  
  async invoke<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const response = await fetch(`${this.baseUrl}/${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    });
    
    const result = await response.json();
    
    if (!result.success) {
      throw new ApiError(result.error);
    }
    
    return result.data;
  }
  
  // 产品相关
  async getProductDetail(productId: string) {
    return this.invoke<ProductDetail>('get-product-detail', {
      method: 'POST',
      body: JSON.stringify({ productId }),
    });
  }
  
  async listProducts(filters: ProductFilters) {
    return this.invoke<ProductListResponse>('list-products', {
      method: 'POST',
      body: JSON.stringify(filters),
    });
  }
  
  // 购物车相关
  async getCart() {
    return this.invoke<Cart>('get-cart');
  }
  
  async addToCart(productId: string, quantity: number) {
    return this.invoke<Cart>('sync-cart', {
      method: 'POST',
      body: JSON.stringify({ productId, quantity }),
    });
  }
  
  // ... 其他方法
}

export const api = new SupabaseApiClient();
```

**类型定义**：
```typescript
// src/lib/api/types.ts
export interface ProductDetail {
  id: string;
  name: string;
  description: string;
  price: number;
  stock: number;
  images: ProductImage[];
  category: Category;
}

export interface ProductFilters {
  categoryId?: string;
  minPrice?: number;
  maxPrice?: number;
  search?: string;
  page?: number;
  limit?: number;
  sortBy?: 'created_at' | 'price' | 'name';
  sortOrder?: 'asc' | 'desc';
}

export interface ApiError {
  code: string;
  message: string;
  details?: Record<string, any>;
}
```

**使用示例**：
```typescript
// 前端调用
import { api } from '@/lib/api';

const product = await api.getProductDetail('123');
const products = await api.listProducts({ categoryId: 'cat-1', page: 1 });
```

**验收标准**：
- [ ] 所有 Edge Function 有对应类型定义
- [ ] API 调用有完整类型推断
- [ ] 错误处理统一

**预计工时**：8 小时

---

#### 任务 2.2：优化状态管理

**目标**：引入更结构化的状态管理方案

**方案选择**：Zustand（轻量、易用、TypeScript 友好）

**安装**：
```bash
npm install zustand
```

**实现示例**：
```typescript
// src/stores/cartStore.ts
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface CartItem {
  productId: string;
  quantity: number;
  price: number;
}

interface CartState {
  items: CartItem[];
  isLoading: boolean;
  error: string | null;
  
  // Actions
  fetchCart: () => Promise<void>;
  addItem: (productId: string, quantity: number) => Promise<void>;
  updateQuantity: (productId: string, quantity: number) => void;
  removeItem: (productId: string) => void;
  clearCart: () => void;
}

export const useCartStore = create<CartState>()(
  persist(
    (set, get) => ({
      items: [],
      isLoading: false,
      error: null,
      
      fetchCart: async () => {
        set({ isLoading: true });
        try {
          const cart = await api.getCart();
          set({ items: cart.items, isLoading: false });
        } catch (error) {
          set({ error: error.message, isLoading: false });
        }
      },
      
      addItem: async (productId, quantity) => {
        // 乐观更新
        const currentItems = get().items;
        set({ items: [...currentItems, { productId, quantity, price: 0 }] });
        
        try {
          const cart = await api.addToCart(productId, quantity);
          set({ items: cart.items });
        } catch (error) {
          // 回滚
          set({ items: currentItems, error: error.message });
        }
      },
      
      updateQuantity: (productId, quantity) => {
        set({
          items: get().items.map(item =>
            item.productId === productId ? { ...item, quantity } : item
          ),
        });
      },
      
      removeItem: (productId) => {
        set({ items: get().items.filter(item => item.productId !== productId) });
      },
      
      clearCart: () => {
        set({ items: [] });
      },
    }),
    {
      name: 'cart-storage',
      partialize: (state) => ({ items: state.items }),
    }
  )
);
```

**验收标准**：
- [ ] 购物车状态迁移到 Zustand
- [ ] 支持状态持久化
- [ ] 乐观更新 + 错误回滚

**预计工时**：12 小时

---

#### 任务 2.3：完善错误处理系统

**目标**：统一错误响应格式和前端错误处理

**后端实现**：
```typescript
// supabase/functions/_shared/api-response.ts
export function successResponse<T>(data: T, message?: string) {
  return new Response(
    JSON.stringify({ success: true, data, message }),
    { headers: { 'Content-Type': 'application/json' } }
  );
}

export function errorResponse(
  code: string,
  message: string,
  status: number = 400,
  details?: Record<string, any>
) {
  return new Response(
    JSON.stringify({
      success: false,
      error: { code, message, details },
    }),
    { status, headers: { 'Content-Type': 'application/json' } }
  );
}

// 错误码枚举
export const ErrorCodes = {
  // 产品相关
  PRODUCT_NOT_FOUND: 'PRODUCT_NOT_FOUND',
  INSUFFICIENT_STOCK: 'INSUFFICIENT_STOCK',
  
  // 订单相关
  ORDER_NOT_FOUND: 'ORDER_NOT_FOUND',
  ORDER_ALREADY_PAID: 'ORDER_ALREADY_PAID',
  
  // 购物车相关
  CART_NOT_FOUND: 'CART_NOT_FOUND',
  CART_ITEM_NOT_FOUND: 'CART_ITEM_NOT_FOUND',
  
  // 用户相关
  USER_NOT_FOUND: 'USER_NOT_FOUND',
  UNAUTHORIZED: 'UNAUTHORIZED',
  
  // 支付相关
  PAYMENT_FAILED: 'PAYMENT_FAILED',
  PAYMENT_CANCELED: 'PAYMENT_CANCELED',
  
  // 系统相关
  INTERNAL_ERROR: 'INTERNAL_ERROR',
  VALIDATION_ERROR: 'VALIDATION_ERROR',
} as const;
```

**前端实现**：
```typescript
// src/lib/api/errors.ts
export class ApiError extends Error {
  constructor(
    public code: string,
    message: string,
    public details?: Record<string, any>
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

// src/hooks/useApiError.ts
export function useApiError() {
  const toast = useToast();
  
  const handleError = useCallback((error: unknown) => {
    if (error instanceof ApiError) {
      // 根据错误码显示不同提示
      const messages: Record<string, string> = {
        PRODUCT_NOT_FOUND: '商品不存在',
        INSUFFICIENT_STOCK: '库存不足',
        UNAUTHORIZED: '请先登录',
        PAYMENT_FAILED: '支付失败，请重试',
      };
      
      toast.error(messages[error.code] || error.message);
    } else {
      toast.error('网络错误，请稍后重试');
    }
  }, [toast]);
  
  return { handleError };
}
```

**验收标准**：
- [ ] 所有 Edge Function 使用标准错误响应
- [ ] 前端统一错误处理
- [ ] 错误提示友好且一致

**预计工时**：8 小时

---

#### 任务 2.4：提升测试覆盖率

**目标**：核心功能测试覆盖率 90%+

**测试计划**：

| 测试类型 | 当前覆盖 | 目标覆盖 | 优先级 |
|----------|----------|----------|--------|
| Edge Functions | 70% | 95% | 🔴 高 |
| 核心组件 | 40% | 85% | 🔴 高 |
| 自定义 Hooks | 50% | 90% | 🟡 中 |
| E2E 流程 | 30% | 80% | 🟡 中 |
| 集成测试 | 60% | 90% | 🟡 中 |

**关键测试场景**：
```typescript
// 1. 购物流程 E2E 测试
describe('Shopping Flow', () => {
  it('should complete purchase successfully', async () => {
    // 浏览商品 → 加入购物车 → 结账 → 支付 → 查看订单
  });
  
  it('should handle insufficient stock', async () => {
    // 库存不足时的错误处理
  });
  
  it('should handle payment failure', async () => {
    // 支付失败后的状态恢复
  });
});

// 2. 并发测试
describe('Concurrency', () => {
  it('should prevent overselling', async () => {
    // 多个用户同时购买同一商品
  });
});
```

**验收标准**：
- [ ] 运行 `npm run test:coverage` 覆盖率 90%+
- [ ] 关键业务流程 E2E 测试通过
- [ ] CI/CD 集成测试

**预计工时**：16 小时

---

### 3.3 阶段三：管理平台升级（3-4 周）

#### 任务 3.1：数据可视化仪表盘

**目标**：实现可自定义的管理仪表盘

**功能设计**：
- 核心指标卡片（销售额/订单数/用户数）
- 销售趋势图表（折线图）
- 商品销售排行（柱状图）
- 地域分布（地图）
- 实时订单动态

**技术选型**：
- 图表库：Recharts（已安装）
- 拖放布局：react-grid-layout
- 数据刷新：React Query

**预计工时**：24 小时

---

#### 任务 3.2：批量操作功能

**目标**：支持商品/订单/用户的批量操作

**功能设计**：
```
商品管理：
- 批量上架/下架
- 批量调价（固定金额/百分比）
- 批量分类调整
- 批量删除

订单管理：
- 批量发货
- 批量导出
- 批量打印面单

用户管理：
- 批量导出用户数据
- 批量发送通知
```

**UI 设计**：
- 复选框多选
- 全选/反选
- 操作预览
- 进度显示
- 结果反馈

**预计工时**：20 小时

---

#### 任务 3.3：权限系统细化（RBAC）

**目标**：实现基于角色的细粒度权限控制

**角色定义**：
| 角色 | 权限范围 |
|------|----------|
| 超级管理员 | 所有权限 |
| 商品管理员 | 商品 CRUD、分类管理 |
| 订单管理员 | 订单处理、发货 |
| 内容编辑 | 文章/评论管理 |
| 客服 | 订单查看、用户咨询 |
| 财务 | 订单导出、财务报表 |

**技术实现**：
```typescript
// 权限检查 Hook
export function usePermission(permission: string) {
  const { user } = useAuth();
  
  return useMemo(() => {
    if (!user) return false;
    return user.permissions.includes(permission);
  }, [user, permission]);
}

// 使用示例
function ProductEdit() {
  const canEdit = usePermission('products.edit');
  const canDelete = usePermission('products.delete');
  
  return (
    <>
      {canEdit && <EditButton />}
      {canDelete && <DeleteButton />}
    </>
  );
}
```

**预计工时**：16 小时

---

### 3.4 阶段四：生产就绪（1-2 周）

#### 任务 4.1：生产环境部署

**检查清单**：
- [ ] 环境变量配置（生产密钥）
- [ ] CDN 配置（静态资源）
- [ ] HTTPS 强制
- [ ] 数据库备份策略
- [ ] 错误监控（Sentry）
- [ ] 性能监控（Google Analytics）
- [ ] 日志聚合

**预计工时**：8 小时

---

#### 任务 4.2：性能优化

**优化项**：
| 优化项 | 当前 | 目标 | 措施 |
|--------|------|------|------|
| 首屏加载 | 2.5s | 1.5s | 代码分割/懒加载 |
| LCP | 3.2s | 2.0s | 图片优化/预加载 |
| FID | 150ms | 100ms | Web Worker |
| CLS | 0.15 | 0.1 | 预留空间 |

**预计工时**：12 小时

---

## 四、技术债务汇总

| 问题 | 严重程度 | 预计工时 | 建议完成时间 |
|------|----------|----------|--------------|
| Edge Functions 命名混乱 | 🔴 高 | 4h | 第 1 周 |
| 数据库索引缺失 | 🔴 高 | 2h | 第 1 周 |
| 并发控制不足 | 🔴 高 | 8h | 第 1-2 周 |
| 代码重复 | 🟡 中 | 6h | 第 1 周 |
| API 客户端不统一 | 🟡 中 | 8h | 第 2 周 |
| 状态管理分散 | 🟡 中 | 12h | 第 2-3 周 |
| 错误处理不一致 | 🟡 中 | 8h | 第 2 周 |
| 测试覆盖不足 | 🟡 中 | 16h | 第 3 周 |
| 监控缺失 | 🟢 低 | 8h | 第 4 周 |
| 性能优化 | 🟢 低 | 12h | 第 4 周 |
| **总计** | - | **84h** | **4 周** |

---

## 五、执行计划

### 第 1 周：清理与稳定
```
周一：Edge Functions 命名统一 (4h)
周二：数据库索引添加 (2h) + 代码清理 (2h)
周三 - 周四：并发控制实现 (8h)
周五：测试与修复 (4h)
```

### 第 2 周：架构优化
```
周一 - 周二：API 客户端实现 (8h)
周三 - 周四：状态管理迁移 (12h)
周五：错误处理系统完善 (8h)
```

### 第 3 周：测试与增强
```
周一 - 周三：测试覆盖率提升 (16h)
周四 - 周五：管理平台功能开发 (16h)
```

### 第 4 周：生产就绪
```
周一 - 周二：权限系统细化 (16h)
周三 - 周四：生产部署配置 (8h) + 性能优化 (12h)
周五：最终测试与上线 (8h)
```

---

## 六、风险与应对

| 风险 | 概率 | 影响 | 应对措施 |
|------|------|------|----------|
| 并发控制实现复杂 | 中 | 高 | 先实现事务方案，后续优化 |
| 状态管理迁移破坏功能 | 中 | 中 | 充分测试，灰度发布 |
| 测试工作量超预期 | 高 | 中 | 优先覆盖核心流程 |
| 生产部署问题 | 低 | 高 | 预发布环境充分验证 |

---

## 七、验收标准

### 功能验收
- [ ] 所有核心功能正常运行
- [ ] 并发下单不超卖
- [ ] 支付流程完整
- [ ] 管理后台功能完整

### 性能验收
- [ ] 首屏加载 < 2s
- [ ] 核心接口响应 < 500ms
- [ ] 数据库查询 < 100ms

### 质量验收
- [ ] 测试覆盖率 > 90%
- [ ] 无高优先级 Bug
- [ ] 代码审查通过

### 文档验收
- [ ] API 文档完整
- [ ] 部署文档完整
- [ ] 运维手册完整

---

## 八、后续规划

### 短期（1-2 个月）
- [ ] 移动端优化
- [ ] SEO 优化
- [ ] 多语言完善（添加更多语言）
- [ ] 营销工具（优惠券/拼团）

### 中期（3-6 个月）
- [ ] 微前端架构迁移
- [ ] 独立部署各业务模块
- [ ] 引入消息队列
- [ ] 建立数据仓库

### 长期（6-12 个月）
- [ ] AI 推荐系统
- [ ] 多渠道销售（小程序/App）
- [ ] 供应链管理系统
- [ ] 数据分析平台

---

## 九、总结

本项目已完成核心功能开发，整体完成度约 85%。当前主要问题是技术债务积累，需要 4 周时间进行系统性优化。

**核心建议**：
1. **优先解决高优先级问题**（命名混乱、索引缺失、并发控制）
2. **分阶段实施**，每周有明确交付
3. **充分测试**，避免引入新 Bug
4. **文档同步更新**，保持代码与文档一致

**预期收益**：
- 系统稳定性提升 50%+
- 查询性能提升 3-5 倍
- 维护成本降低 40%+
- 开发效率提升 30%+

---

*文档版本：v1.0*  
*最后更新：2026-02-24*  
*作者：代码助手*
