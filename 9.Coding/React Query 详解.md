# React Query (TanStack Query) 详解

> 创建时间：2026-02-27  
> 标签：#React #前端 #数据管理 #TanStack  
> 项目：nest-wander-ui

---

## 📚 什么是 React Query？

**React Query**（现名 **TanStack Query**）是一个用于 React 的**服务端状态管理库**。

**简单说**：帮你自动管理 API 数据的工具，让你少写 80% 的数据获取代码。

---

## 🎯 解决什么问题？

### ❌ 没有 React Query 时

```typescript
function ProductsPage() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [stale, setStale] = useState(false);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        setLoading(true);
        const response = await fetch('/api/products');
        const data = await response.json();
        setProducts(data);
        setStale(false);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();

    // 手动实现轮询刷新
    const interval = setInterval(fetchProducts, 60000);
    return () => clearInterval(interval);
  }, []);

  // 手动实现缓存
  const getCachedData = () => {
    const cached = localStorage.getItem('products');
    return cached ? JSON.parse(cached) : null;
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div>
      {stale && <div>Data is stale, refreshing...</div>}
      {products.map(product => <ProductCard key={product.id} product={product} />)}
    </div>
  );
}
```

**问题**：
- ❌ 代码冗长（80+ 行）
- ❌ 手动管理缓存
- ❌ 手动管理 Loading/Error
- ❌ 手动实现刷新
- ❌ 容易内存泄漏
- ❌ 难以复用

---

### ✅ 有了 React Query

```typescript
function ProductsPage() {
  const { data, isLoading, error, isStale } = useProducts();

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div>
      {isStale && <div>Refreshing...</div>}
      {data.products.map(product => <ProductCard key={product.id} product={product} />)}
    </div>
  );
}

// Hook 定义
function useProducts(params) {
  return useQuery({
    queryKey: ['products', params],
    queryFn: () => fetchProducts(params),
    staleTime: 1000 * 60 * 5, // 5 分钟
    retry: 1,
  });
}
```

**优势**：
- ✅ 代码精简（10 行）
- ✅ 自动缓存
- ✅ 自动管理 Loading/Error
- ✅ 自动刷新
- ✅ 无内存泄漏
- ✅ 易于复用

---

## 🔧 核心概念

### 1. Query（查询）

用于**获取数据**（GET 请求）

```typescript
import { useQuery } from '@tanstack/react-query';

function useProducts(params) {
  return useQuery({
    // 唯一标识（用于缓存）
    queryKey: ['products', params],
    
    // 获取数据的函数
    queryFn: async () => {
      const response = await fetch('/api/products', {
        method: 'POST',
        body: JSON.stringify(params)
      });
      return response.json();
    },
    
    // 配置选项
    staleTime: 1000 * 60 * 5,  // 5 分钟内数据有效
    retry: 1,                   // 失败重试 1 次
    refetchOnWindowFocus: false, // 窗口聚焦时不自动刷新
  });
}
```

**返回值**：
```typescript
{
  data: any,           // 返回的数据
  isLoading: boolean,  // 是否首次加载
  isFetching: boolean, // 是否正在获取（包括后台刷新）
  isError: boolean,    // 是否错误
  error: Error,        // 错误对象
  isStale: boolean,    // 数据是否过期
  refetch: () => void, // 手动刷新函数
  status: string       // 'loading' | 'error' | 'success'
}
```

---

### 2. Mutation（变更）

用于**修改数据**（POST/PUT/DELETE 请求）

```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query';

function useAddToCart() {
  const queryClient = useQueryClient();

  return useMutation({
    // 修改数据的函数
    mutationFn: async (item) => {
      const response = await fetch('/api/cart', {
        method: 'POST',
        body: JSON.stringify(item)
      });
      return response.json();
    },
    
    // 成功回调
    onSuccess: (data, variables) => {
      // 刷新购物车数据
      queryClient.invalidateQueries({ queryKey: ['cart'] });
      
      // 显示提示
      toast.success('Added to cart!');
    },
    
    // 错误回调
    onError: (error) => {
      toast.error('Failed to add to cart');
    },
  });
}

// 使用
function ProductCard({ product }) {
  const addToCart = useAddToCart();

  const handleAdd = () => {
    addToCart.mutate({
      product_id: product.id,
      quantity: 1
    });
  };

  return (
    <button 
      onClick={handleAdd}
      disabled={addToCart.isPending}
    >
      {addToCart.isPending ? 'Adding...' : 'Add to Cart'}
    </button>
  );
}
```

**返回值**：
```typescript
{
  mutate: (data) => void,      // 触发变更
  mutateAsync: (data) => Promise, // 异步版本
  isPending: boolean,          // 是否进行中
  isError: boolean,            // 是否错误
  isSuccess: boolean,          // 是否成功
  data: any,                   // 返回数据
  error: Error,                // 错误对象
  reset: () => void            // 重置状态
}
```

---

### 3. QueryClient（客户端）

管理所有查询的全局配置

```typescript
import { QueryClient } from '@tanstack/react-query';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5,    // 5 分钟
      retry: 1,                     // 失败重试 1 次
      refetchOnWindowFocus: false,  // 窗口聚焦时不刷新
      retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
    },
    mutations: {
      retry: 0, // 变更失败不重试
    },
  },
});
```

---

### 4. QueryClientProvider（提供者）

在应用根组件包裹

```typescript
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient();

ReactDOM.createRoot(document.getElementById('root')).render(
  <QueryClientProvider client={queryClient}>
    <App />
  </QueryClientProvider>
);
```

---

## 📦 常用配置

### 缓存策略

```typescript
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      // 数据新鲜时间（超过这个时间标记为 stale）
      staleTime: 1000 * 60 * 5, // 5 分钟
      
      // 缓存时间（超过这个时间从缓存删除）
      gcTime: 1000 * 60 * 60,   // 1 小时
      
      // 失败重试次数
      retry: 1,
      
      // 重试延迟（毫秒）
      retryDelay: (attemptIndex) => 
        Math.min(1000 * 2 ** attemptIndex, 30000),
      
      // 窗口聚焦时是否刷新
      refetchOnWindowFocus: false,
      
      // 网络恢复时是否刷新
      refetchOnReconnect: true,
    },
  },
});
```

---

### 条件查询

```typescript
// 只在有 userId 时查询
const { data } = useQuery({
  queryKey: ['user', userId],
  queryFn: () => fetchUser(userId),
  enabled: !!userId, // 条件
});

// 手动触发
const { data, refetch } = useQuery({
  queryKey: ['search', keyword],
  queryFn: () => searchProducts(keyword),
  enabled: false, // 不自动查询
});

// 用户点击搜索按钮时
<button onClick={() => refetch()}>Search</button>
```

---

### 依赖查询

```typescript
// 先获取用户，再获取用户订单
const { data: user } = useQuery({
  queryKey: ['user', userId],
  queryFn: fetchUser,
});

const userId = user?.id;

const { data: orders } = useQuery({
  queryKey: ['orders', userId],
  queryFn: fetchUserOrders,
  enabled: !!userId, // 等 user 获取完成后再查询
});
```

---

## 🎯 实战示例

### 示例 1：商品列表

```typescript
// hooks/use-products.ts
import { useQuery } from '@tanstack/react-query';
import { getProducts } from '@/services/product-api';

export function useProducts(params = {}) {
  return useQuery({
    queryKey: ['products', params],
    queryFn: () => getProducts(params),
    staleTime: 1000 * 60 * 5, // 5 分钟
  });
}

// pages/Products.tsx
export default function ProductsPage() {
  const { data, isLoading, error } = useProducts({ limit: 20 });

  if (isLoading) return <SkeletonLoader />;
  if (error) return <ErrorDisplay error={error} />;

  return (
    <div>
      <h1>Products</h1>
      <ProductGrid products={data.data.products} />
    </div>
  );
}
```

---

### 示例 2：商品详情

```typescript
// hooks/use-product.ts
export function useProduct(productId) {
  return useQuery({
    queryKey: ['product', productId],
    queryFn: () => getProductDetail(productId),
    enabled: !!productId,
    staleTime: 1000 * 60 * 10, // 10 分钟
  });
}

// pages/ProductDetail.tsx
export default function ProductDetailPage() {
  const { id } = useParams();
  const { data, isLoading } = useProduct(id);

  if (isLoading) return <ProductSkeleton />;
  if (!data) return <NotFound />;

  const product = data.data;

  return (
    <div>
      <h1>{product.name}</h1>
      <p>{product.description}</p>
      <span>${product.price}</span>
    </div>
  );
}
```

---

### 示例 3：购物车

```typescript
// hooks/use-cart.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

export function useCart() {
  const queryClient = useQueryClient();

  // 查询购物车
  const { data, isLoading } = useQuery({
    queryKey: ['cart'],
    queryFn: getCart,
    staleTime: 1000 * 60 * 2, // 2 分钟
  });

  // 添加到购物车
  const addToCart = useMutation({
    mutationFn: (item) => addToCartAPI(item),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['cart'] });
      toast.success('Added to cart!');
    },
  });

  // 更新数量
  const updateQuantity = useMutation({
    mutationFn: ({ itemId, quantity }) => 
      updateQuantityAPI(itemId, quantity),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['cart'] });
    },
  });

  // 删除商品
  const removeFromCart = useMutation({
    mutationFn: (itemId) => removeFromCartAPI(itemId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['cart'] });
    },
  });

  return {
    cart: data?.data,
    isLoading,
    addToCart: addToCart.mutateAsync,
    updateQuantity: updateQuantity.mutateAsync,
    removeFromCart: removeFromCart.mutateAsync,
  };
}
```

---

## 🔍 DevTools（开发工具）

React Query 提供开发工具，方便调试：

```typescript
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <App />
      {/* 开发工具 */}
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}
```

**功能**：
- 查看所有查询状态
- 查看缓存数据
- 手动刷新查询
- 查看查询配置

**注意**：生产环境建议移除或按需加载。

---

## ⚠️ 常见错误

### 1. 忘记包裹 Provider

```typescript
// ❌ 错误
function App() {
  return <ProductsPage />;
}

// ✅ 正确
function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ProductsPage />
    </QueryClientProvider>
  );
}
```

---

### 2. QueryKey 不稳定

```typescript
// ❌ 错误 - 每次渲染都创建新数组
useQuery({
  queryKey: ['products', { page: 1, limit: 10 }],
  queryFn: fetchProducts,
});

// ✅ 正确 - 使用稳定引用
const params = useMemo(() => ({ page: 1, limit: 10 }), []);
useQuery({
  queryKey: ['products', params],
  queryFn: fetchProducts,
});
```

---

### 3. 忘记处理 Loading/Error

```typescript
// ❌ 错误
function ProductsPage() {
  const { data } = useProducts();
  return <div>{data.products.map(...)}</div>;
}

// ✅ 正确
function ProductsPage() {
  const { data, isLoading, error } = useProducts();
  
  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  
  return <div>{data.products.map(...)}</div>;
}
```

---

## 📊 性能优化

### 1. 分页查询

```typescript
function useProducts(page) {
  return useQuery({
    queryKey: ['products', page],
    queryFn: () => getProducts({ page }),
    keepPreviousData: true, // 保留上一页数据
  });
}
```

---

### 2. 无限滚动

```typescript
import { useInfiniteQuery } from '@tanstack/react-query';

function useInfiniteProducts() {
  return useInfiniteQuery({
    queryKey: ['products'],
    queryFn: ({ pageParam = 0 }) => getProducts({ offset: pageParam }),
    getNextPageParam: (lastPage) => lastPage.nextOffset,
  });
}

// 使用
const {
  data,
  fetchNextPage,
  hasNextPage,
  isFetchingNextPage,
} = useInfiniteProducts();

// 加载更多
<button 
  onClick={() => fetchNextPage()}
  disabled={!hasNextPage || isFetchingNextPage}
>
  {isFetchingNextPage ? 'Loading...' : 'Load More'}
</button>
```

---

### 3. 预加载

```typescript
// 在用户点击前预加载
function ProductCard({ product }) {
  const queryClient = useQueryClient();

  const handleMouseEnter = () => {
    // 预加载商品详情
    queryClient.prefetchQuery({
      queryKey: ['product', product.id],
      queryFn: () => getProductDetail(product.id),
    });
  };

  return (
    <div onMouseEnter={handleMouseEnter}>
      {product.name}
    </div>
  );
}
```

---

## 🎯 最佳实践

### 1. 自定义 Hooks

```typescript
// ✅ 推荐：封装成自定义 Hook
function useProducts(params) {
  return useQuery({
    queryKey: ['products', params],
    queryFn: () => getProducts(params),
    staleTime: 1000 * 60 * 5,
  });
}

// 页面中使用
function ProductsPage() {
  const { data, isLoading } = useProducts({ limit: 20 });
  // ...
}
```

---

### 2. 错误边界

```typescript
class ErrorBoundary extends React.Component {
  state = { hasError: false };

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  render() {
    if (this.state.hasError) {
      return <ErrorFallback />;
    }
    return this.props.children;
  }
}

// 使用
<ErrorBoundary>
  <ProductsPage />
</ErrorBoundary>
```

---

### 3. 类型安全（TypeScript）

```typescript
interface Product {
  id: string;
  name: string;
  price: number;
}

interface ProductsResponse {
  success: boolean;
  data: {
    products: Product[];
    meta: { total: number };
  };
}

function useProducts(): UseQueryResult<ProductsResponse> {
  return useQuery({
    queryKey: ['products'],
    queryFn: getProducts,
  });
}
```

---

## 📚 学习资源

- **官方文档**: https://tanstack.com/query
- **GitHub**: https://github.com/TanStack/query
- **DevTools**: Chrome 扩展 "React Query Devtools"

---

## 🎉 总结

**React Query = 自动管理 API 数据的工具**

**核心价值**：
- ✅ 减少 80% 数据获取代码
- ✅ 自动缓存和刷新
- ✅ 自动管理 Loading/Error
- ✅ 性能优化（预取、无限加载）
- ✅ 开发体验好（DevTools）

**适用场景**：
- ✅ 需要频繁获取数据的应用
- ✅ 需要缓存和后台刷新的场景
- ✅ 复杂的表单提交和乐观更新

**不适用**：
- ❌ 纯客户端状态（用 Zustand/Redux）
- ❌ 表单输入状态（用 React Hook Form）

---

*笔记版本：v1.0*  
*创建时间：2026-02-27*  
*项目：nest-wander-ui*
