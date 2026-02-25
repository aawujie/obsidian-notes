# WooCommerce 技术架构详解

**创建时间**: 2026-02-25  
**标签**: #WooCommerce #技术架构 #PHP #WordPress #电商

---

## 🏗️ 整体架构概览

```
┌─────────────────────────────────────────────────────────────────┐
│                        用户浏览器                                │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP/HTTPS
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Web 服务器层                                │
│         Apache / Nginx + PHP-FPM                                │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    WordPress 核心层                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   路由系统   │  │   插件 API  │  │   主题系统   │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   WooCommerce 核心层                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │  商品系统   │  │  订单系统   │  │  支付系统   │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │  购物车系统  │  │  物流系统   │  │  客户系统   │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      数据持久层                                 │
│         MySQL / MariaDB 数据库                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📦 核心组件详解

### 1️⃣ WordPress 核心层（基础）

WooCommerce 是 WordPress 插件，依赖 WordPress 核心：

```
WordPress Core
├── wp-includes/              # 核心函数库
│   ├── class-wp-hook.php     # Hook 系统核心
│   ├── class-wp-query.php    # 查询系统
│   ├── class-wp-user.php     # 用户系统
│   └── ...
│
├── wp-admin/                 # 管理后台
│   ├── admin.php             # 后台入口
│   └── ...
│
└── wp-content/               # 用户内容
    ├── plugins/              # 插件目录
    │   └── woocommerce/      # WooCommerce 主插件
    └── themes/               # 主题目录
        └── your-theme/       # 你的主题
```

**关键机制**：
- **Hook 系统** (Actions & Filters) - 插件扩展的核心
- **自定义文章类型** (Custom Post Types) - 商品数据存储
- **自定义字段** (Custom Fields/Meta) - 商品属性存储

---

### 2️⃣ WooCommerce 插件结构

```
woocommerce/
├── woocommerce.php           # 主插件文件（入口）
├── includes/                 # 核心类库
│   ├── class-woocommerce.php # 主类（单例模式）
│   ├── abstracts/            # 抽象基类
│   │   ├── abstract-wc-product.php
│   │   ├── abstract-wc-payment-gateway.php
│   │   └── abstract-wc-shipping-method.php
│   │
│   ├── admin/                # 后台管理
│   │   ├── class-wc-admin.php
│   │   ├── meta-boxes/       #  metabox 定义
│   │   └── settings/         # 设置页面
│   │
│   ├── api/                  # REST API
│   │   ├── class-wc-rest-products-controller.php
│   │   ├── class-wc-rest-orders-controller.php
│   │   └── ...
│   │
│   ├── class-wc-product.php  # 商品类
│   ├── class-wc-cart.php     # 购物车类
│   ├── class-wc-order.php    # 订单类
│   ├── class-wc-customer.php # 客户类
│   │
│   ├── gateways/             # 支付网关
│   │   ├── paypal/
│   │   ├── stripe/
│   │   └── cod/ (货到付款)
│   │
│   ├── shipping/             # 物流方式
│   │   ├── class-wc-shipping-flat-rate.php
│   │   └── class-wc-shipping-free-shipping.php
│   │
│   └── templates/            # 模板文件
│       ├── single-product.php
│       ├── archive-product.php
│       ├── cart/
│       ├── checkout/
│       └── order/
│
├── assets/                   # 静态资源
│   ├── css/
│   ├── js/
│   ├── images/
│   └── fonts/
│
├── templates/                # 前端模板（可被主题覆盖）
│   ├── single-product/
│   ├── archive-product/
│   ├── cart/
│   ├── checkout/
│   └── myaccount/
│
└── i18n/                     # 国际化文件
    └── languages/
```

---

## 🗄️ 数据库架构

### 核心数据表

WooCommerce 使用 WordPress 的数据表结构，加上自己的自定义表：

```
WordPress 核心表：
├── wp_posts                  # 文章/商品/订单（多用途）
├── wp_postmeta               # 文章/商品元数据
├── wp_users                  # 用户
├── wp_usermeta               # 用户元数据
├── wp_terms                  # 分类/标签
├── wp_term_taxonomy          # 分类关系
├── wp_term_relationships     # 文章 - 分类关联
└── wp_options                # 选项配置

WooCommerce 自定义表 (3.0+):
├── wc_order_items            # 订单项
├── wc_order_itemmeta         # 订单项元数据
├── wc_customer_lookup        # 客户查找表
├── wc_order_stats            # 订单统计
├── wc_product_meta_lookup    # 商品元数据查找
└── wc_download_log           # 下载日志
```

---

### 商品数据存储方式

**WooCommerce 商品 = WordPress 自定义文章类型**

```sql
-- 商品存储在 wp_posts 表
SELECT * FROM wp_posts WHERE post_type = 'product';

-- 商品数据：
-- post_type = 'product'
-- post_status = 'publish' (已发布) / 'draft' (草稿)
-- post_title = 商品名称
-- post_content = 商品描述
```

**商品价格/库存等 = 存储在 wp_postmeta**

```sql
-- 商品价格
SELECT * FROM wp_postmeta 
WHERE post_id = 123 
AND meta_key IN ('_price', '_regular_price', '_sale_price');

-- 商品库存
SELECT * FROM wp_postmeta 
WHERE post_id = 123 
AND meta_key IN ('_stock', '_stock_status', '_manage_stock');

-- 商品类型
SELECT * FROM wp_postmeta 
WHERE post_id = 123 
AND meta_key = '_product_type'; 
-- 值：simple / variable / grouped / external
```

**可视化理解：**

```
┌─────────────────────────────────────────────────────────┐
│                    wp_posts 表                          │
│  ID  │ post_type  │ post_title    │ post_status        │
│──────┼────────────┼───────────────┼────────────────────│
│ 123  │ product    │ T-Shirt       │ publish            │
│ 124  │ product    │ Jeans         │ publish            │
│ 125  │ shop_order │ Order #1001   │ wc-completed       │
└─────────────────────────────────────────────────────────┘
                            │
                            │ post_id = 123
                            ▼
┌─────────────────────────────────────────────────────────┐
│                  wp_postmeta 表                         │
│  meta_id │ post_id │ meta_key          │ meta_value    │
│──────────┼─────────┼───────────────────┼───────────────│
│   1001   │   123   │ _price            │ 29.99         │
│   1002   │   123   │ _regular_price    │ 39.99         │
│   1003   │   123   │ _sale_price       │ 29.99         │
│   1004   │   123   │ _stock            │ 100           │
│   1005   │   123   │ _sku              │ TSH-001       │
│   1006   │   123   │ _product_image_id │ 456           │
└─────────────────────────────────────────────────────────┘
```

---

## 🔌 插件系统架构

### Hook 机制（核心扩展方式）

WooCommerce 通过 WordPress 的 Hook 系统实现扩展：

```php
// Action Hooks - 在特定点执行代码
add_action('woocommerce_before_add_to_cart_form', 'my_custom_function');

// Filter Hooks - 修改数据后返回
add_filter('woocommerce_product_get_price', 'modify_price', 10, 2);
```

**关键 Hook 位置：**

```
商品页面 Hook 流程：

woocommerce_before_main_content
    └── woocommerce_before_shop_loop
        └── [商品列表]
    └── woocommerce_after_shop_loop

woocommerce_before_single_product
    └── woocommerce_before_single_product_summary
        └── [商品图片]
    └── woocommerce_single_product_summary
        ├── [商品标题] (优先级 5)
        ├── [商品价格] (优先级 10)
        ├── [商品摘要] (优先级 20)
        ├── [加入购物车表单] (优先级 30)
        └── [商品元数据] (优先级 40)
    └── woocommerce_after_single_product_summary
        └── [商品描述]
```

---

## 🎨 主题系统

### 模板覆盖机制

WooCommerce 允许主题覆盖默认模板：

```
默认模板位置：
/woocommerce/templates/single-product.php

主题覆盖位置：
/your-theme/woocommerce/single-product.php
```

**目录结构：**

```
your-theme/
└── woocommerce/
    ├── single-product.php        # 商品详情页
    ├── archive-product.php       # 商品列表页
    ├── content-product.php       # 商品卡片
    │
    ├── cart/
    │   ├── cart.php              # 购物车页面
    │   └── cart-empty.php        # 空购物车
    │
    ├── checkout/
    │   ├── form-checkout.php     # 结账表单
    │   └── thankyou.php          # 感谢页面
    │
    └── myaccount/
        ├── dashboard.php         # 账户仪表板
        ├── orders.php            # 订单列表
        └── form-login.php        # 登录表单
```

---

## 🌐 REST API 架构

### API 端点

WooCommerce 提供完整的 REST API：

```
基础 URL: https://yoursite.com/wp-json/wc/v3/

认证：OAuth 1.0a 或 JWT

主要端点：
├── /products              # 商品
│   ├── GET    - 获取商品列表
│   ├── POST   - 创建商品
│   ├── PUT    - 更新商品
│   └── DELETE - 删除商品
│
├── /products/(?P<id>[\d]+)  # 单个商品
├── /orders                # 订单
├── /customers             # 客户
├── /coupons               # 优惠券
├── /reports               # 报告
└── /settings              # 设置
```

**API 请求示例：**

```bash
# 获取商品列表
curl -X GET "https://yoursite.com/wp-json/wc/v3/products" \
  -u consumer_key:consumer_secret

# 创建订单
curl -X POST "https://yoursite.com/wp-json/wc/v3/orders" \
  -u consumer_key:consumer_secret \
  -H "Content-Type: application/json" \
  -d '{
    "payment_method": "bacs",
    "payment_method_title": "Direct Bank Transfer",
    "status": "pending",
    "line_items": [
      {
        "product_id": 93,
        "quantity": 2
      }
    ]
  }'
```

---

## 🔄 数据流示例

### 用户下单流程

```
1. 用户访问商品页
   ↓
   WordPress 路由 → woocommerce/templates/single-product.php
   
2. 用户点击"加入购物车"
   ↓
   AJAX 请求 → WC_AJAX::add_to_cart()
   ↓
   更新 Session → WC()->cart->add_to_cart()
   ↓
   返回更新后的购物车片段
   
3. 用户去结账
   ↓
   加载 checkout 页面 → woocommerce/templates/checkout/form-checkout.php
   ↓
   显示表单 + 购物车内容
   
4. 用户提交订单
   ↓
   WC_Form_Handler::checkout_action()
   ↓
   验证数据 → 创建订单 → 处理支付
   ↓
   WC_Order::create() → wp_posts (post_type=shop_order)
   ↓
   保存订单项 → wc_order_items 表
   ↓
   减少库存 → 更新 wp_postmeta (_stock)
   
5. 支付成功
   ↓
   支付网关回调 → WC_Payment_Gateways::process_payment()
   ↓
   更新订单状态 → wc-completed
   ↓
   发送邮件通知 → WC_Emails
   ↓
   显示感谢页面
```

---

## ⚡ 性能优化点

### 缓存策略

```
对象缓存 (Object Cache):
├── 商品数据 → wp_cache_get('product-123', 'products')
├── 订单数据 → wp_cache_get('order-456', 'orders')
└── 查询结果 → wp_cache_get('query-hash', 'queries')

瞬态缓存 (Transients):
├── 过期时间设置
├── 适合缓存时效性数据
└── set_transient('wc_special_offer', $data, HOUR_IN_SECONDS)

页面缓存：
├── 商品列表页
├── 静态内容页
└── 使用插件：W3 Total Cache / WP Rocket
```

### 数据库优化

```sql
-- 常用索引优化
CREATE INDEX meta_key_value ON wp_postmeta(meta_key, meta_value);
CREATE INDEX post_type_status ON wp_posts(post_type, post_status);

-- 定期清理
DELETE FROM wp_options WHERE option_name LIKE '_transient_%';
DELETE FROM wp_postmeta WHERE meta_key LIKE '_wc_session_%';
```

---

## 🛠️ 扩展开发方式

### 1. 子主题（推荐）

```
child-theme/
├── style.css                 # 声明父主题
├── functions.php             # 自定义函数
└── woocommerce/              # 覆盖模板
    └── single-product.php
```

### 2. 自定义插件

```
my-woocommerce-extension/
├── my-woocommerce-extension.php  # 主文件
├── includes/
│   ├── class-my-feature.php
│   └── ...
└── templates/
    └── ...
```

### 3. 使用 Hook 扩展

```php
// 在商品页添加自定义内容
add_action('woocommerce_single_product_summary', 'add_custom_content', 25);
function add_custom_content() {
    echo '<div class="custom-info">Custom Info</div>';
}

// 修改商品价格
add_filter('woocommerce_product_get_price', 'custom_price', 10, 2);
function custom_price($price, $product) {
    return $price * 0.9; // 9 折优惠
}
```

---

## 📊 架构优缺点

### ✅ 优点

| 优点 | 说明 |
|------|------|
| 📦 **插件生态** | 5 万 + 插件，几乎任何功能都有 |
| 🎨 **主题丰富** | 数千个电商主题 |
| 🔌 **Hook 系统** | 无需改核心代码即可扩展 |
| 📚 **文档完善** | 10 年 + 积累，教程极多 |
| 💰 **成本低** | 基础功能免费 |
| 🌐 **SEO 友好** | WordPress SEO 成熟 |

### ❌ 缺点

| 缺点 | 说明 |
|------|------|
| 🐌 **性能瓶颈** | PHP + 多表 JOIN，大流量需优化 |
| 📦 **数据库臃肿** | wp_postmeta 表容易过大 |
| 🔒 **安全风险** | 插件多，漏洞风险高 |
| 🛠️ **技术旧** | PHP 不如 Node.js 现代 |
| 📈 **扩展性差** | 单体架构，水平扩展困难 |
| 🎯 **前端限制** | 模板系统不如现代前端灵活 |

---

## 🎯 总结

> **WooCommerce 架构本质 = WordPress 插件**
>
> 利用 WordPress 的内容管理系统能力，通过自定义文章类型存储商品，通过 Hook 系统实现扩展，通过模板系统实现前端定制。

**适合**：中小电商、内容 + 电商、非技术背景、快速上线

**不适合**：高并发、定制前端、多端复用、技术团队

---

## 🔗 相关链接

- WooCommerce 官网：https://woocommerce.com
- 开发者文档：https://developer.woocommerce.com
- GitHub: https://github.com/woocommerce/woocommerce
- Hook 参考：https://developer.woocommerce.com/docs/reference/hooks/
