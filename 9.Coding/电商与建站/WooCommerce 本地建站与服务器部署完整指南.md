# WooCommerce 本地建站与服务器部署完整指南

## 📅 基本信息

- **创建日期**: 2026-02-25
- **适用场景**: 快速搭建电商网站
- **技术栈**: WordPress + WooCommerce
- **部署方式**: LocalWP 本地开发 → 云服务器生产

---

## 🏠 第一部分：LocalWP 本地开发

### 1.1 什么是 LocalWP

**LocalWP** 是一款专为 WordPress 开发者设计的本地开发工具：

| 特性 | 说明 |
|------|------|
| **平台** | macOS / Windows / Linux |
| **价格** | 免费 |
| **官网** | https://localwp.com |
| **优点** | 一键创建、自动配置、图形界面 |

---

### 1.2 安装 LocalWP

#### macOS 安装

```bash
# 1. 访问官网
https://localwp.com

# 2. 点击 "Download for Mac"

# 3. 下载完成后：
#    - 打开 DMG 文件
#    - 拖拽 Local 到 Applications 文件夹
#    - 打开 Local.app
```

#### 安装位置

```
/Applications/Local.app          # 应用程序
~/Library/Application Support/Local/  # 数据和配置
```

---

### 1.3 创建 WooCommerce 网站

#### 步骤 1：启动 LocalWP

```
打开 Local.app
   ↓
首次使用会要求登录（可跳过）
   ↓
进入主界面
```

#### 步骤 2：创建新网站

```
点击 "+" 或 "Create a new site"
   ↓
选择 "Custom" 或 "WooCommerce" 模板
   ↓
输入网站名称：my-store
   ↓
设置用户名/密码（后台登录用）
   ↓
点击 "Add Site"
```

#### 步骤 3：等待创建（约 1-2 分钟）

```
LocalWP 自动完成：
├─ 下载 WordPress
├─ 配置 MySQL 数据库
├─ 配置 PHP 环境
├─ 安装 WooCommerce 插件
└─ 启动本地服务器
```

#### 步骤 4：访问网站

```
网站创建完成后：
├─ 点击 "Open Site" → 访问前台
├─ 点击 "WP Admin" → 访问后台
└─ 点击 "Open Site Shell" → 终端访问
```

**默认地址**:
- 前台：`http://my-store.local`
- 后台：`http://my-store.local/wp-admin`

---

### 1.4 配置 WooCommerce

#### 后台设置

```
登录后台 → WooCommerce → 设置

1. 常规设置
   ├─ 商店地址
   ├─ 货币（CNY 人民币）
   └─ 销售地区

2. 产品设置
   ├─ 商品单位
   ├─ 库存管理
   └─ 下载商品

3. 支付设置
   ├─ 银行转账（默认开启）
   ├─ Stripe（需要密钥）
   ├─ PayPal（需要密钥）
   └─ 支付宝/微信（第三方插件）

4. 配送设置
   ├─ 配送区域
   ├─ 运费计算
   └─ 配送方式
```

#### 添加商品

```
产品 → 添加新产品
├─ 商品名称
├─ 商品描述
├─ 价格
├─ 商品图片
├─ 库存数量
└─ 发布
```

---

### 1.5 选择主题

#### 免费主题

```
外观 → 主题 → 添加

推荐：
├─ Storefront（WooCommerce 官方）
├─ Astra（轻量快速）
├─ OceanWP（功能丰富）
└─ Kadence（现代化）
```

#### 付费主题

```
ThemeForest: https://themeforest.net
价格：$50-60
推荐：
├─ Flatsome
├─ WoodMart
└─ Porto
```

---

### 1.6 本地文件位置

```
~/Library/Application Support/Local/runs/my-store/
├── app/                    # WordPress 文件
│   ├── wp-content/
│   │   ├── plugins/        # 插件
│   │   ├── themes/         # 主题
│   │   └── uploads/        # 上传文件
│   ├── wp-config.php       # 配置文件
│   └── ...
├── services/               # 服务配置
│   └── mysql/              # 数据库文件
└── conf/                   # Local 配置
```

**快速访问**:
```bash
# 在 LocalWP 中右键网站 → "Open Site Folder"
```

---

## 🌐 第二部分：部署到生产服务器

### 2.1 服务器选择

#### 方案对比

| 服务商 | 月费 | 适合场景 | 难度 |
|--------|------|----------|------|
| **SiteGround** | $3.99 | 新手/小站 | ⭐ 简单 |
| **Bluehost** | $2.95 | 新手/小站 | ⭐ 简单 |
| **Vultr** | $6 | 中级用户 | ⭐⭐ 中等 |
| **DigitalOcean** | $6 | 中级用户 | ⭐⭐ 中等 |
| **阿里云** | ¥30 | 国内用户 | ⭐⭐ 中等 |
| **腾讯云** | ¥25 | 国内用户 | ⭐⭐ 中等 |

#### 推荐配置

| 流量 | CPU | 内存 | 存储 | 推荐 |
|------|-----|------|------|------|
| **< 1000/天** | 1 核 | 1GB | 25GB SSD | 入门款 |
| **1000-5000/天** | 2 核 | 2GB | 40GB SSD | 标准款 |
| **> 5000/天** | 4 核 | 4GB | 80GB SSD | 专业款 |

---

### 2.2 部署方式对比

| 方式 | 优点 | 缺点 | 适合 |
|------|------|------|------|
| **一键迁移插件** | 简单快速 | 大站可能超时 | 小站 |
| **手动 FTP** | 可控性强 | 步骤多 | 中站 |
| **托管服务** | 最省心 | 贵 | 商业站 |

---

### 2.3 方式 1：使用迁移插件（推荐新手）

#### 步骤 1：安装 All-in-One WP Migration

**本地**:
```
后台 → 插件 → 安装插件
搜索：All-in-One WP Migration
安装并激活
```

#### 步骤 2：导出网站

```
All-in-One WP Migration → 导出到 → 文件
   ↓
下载 .wpress 文件（包含所有内容）
```

#### 步骤 3：购买并设置服务器

**以 SiteGround 为例**:
```
1. 注册 SiteGround 账号
2. 购买 WordPress 主机
3. 在 SiteGround 后台创建网站
4. 获取 FTP/SFTP 信息
```

#### 步骤 4：安装 WordPress

```
SiteGround 后台 → WordPress → 安装
   ↓
自动安装 WordPress
   ↓
获取后台登录信息
```

#### 步骤 5：导入网站

```
生产环境后台 → 安装 All-in-One WP Migration
   ↓
导入 → 选择 .wpress 文件
   ↓
等待导入完成（大文件可能需要时间）
   ↓
保存固定链接设置（后台 → 设置 → 固定链接 → 保存）
```

---

### 2.4 方式 2：手动迁移（推荐中级用户）

#### 步骤 1：导出数据库

**本地**:
```bash
# 在 LocalWP 中打开 Site Shell
# 或直接用 phpMyAdmin

mysqldump -u root -p my_store > backup.sql
```

#### 步骤 2：打包文件

```bash
cd ~/Library/Application\ Support/Local/runs/my-store/app
tar -czf woocommerce-backup.tar.gz .
```

#### 步骤 3：上传到服务器

```bash
# 使用 SFTP 上传
sftp user@your-server.com
put woocommerce-backup.tar.gz /var/www/html/
put backup.sql /var/www/html/
```

#### 步骤 4：服务器配置

**SSH 登录服务器**:
```bash
ssh user@your-server.com

# 解压文件
cd /var/www/html
tar -xzf woocommerce-backup.tar.gz

# 导入数据库
mysql -u wordpress_user -p wordpress_db < backup.sql
```

#### 步骤 5：修改 wp-config.php

```php
// 更新数据库配置
define('DB_NAME', '生产数据库名');
define('DB_USER', '生产数据库用户');
define('DB_PASSWORD', '生产数据库密码');
define('DB_HOST', 'localhost');

// 更新网站 URL
define('WP_HOME', 'https://your-domain.com');
define('WP_SITEURL', 'https://your-domain.com');
```

#### 步骤 6：更新数据库中的 URL

```sql
-- 登录 MySQL
mysql -u wordpress_user -p wordpress_db

-- 更新 URL
UPDATE wp_options SET option_value = 'https://your-domain.com' 
WHERE option_name IN ('home', 'siteurl');

UPDATE wp_posts SET post_content = REPLACE(post_content, 'http://my-store.local', 'https://your-domain.com');
UPDATE wp_posts SET guid = REPLACE(guid, 'http://my-store.local', 'https://your-domain.com');
UPDATE wp_postmeta SET meta_value = REPLACE(meta_value, 'http://my-store.local', 'https://your-domain.com');
```

---

### 2.5 方式 3：使用托管服务（最省心）

#### 推荐服务商

| 服务商 | 月费 | 特点 |
|--------|------|------|
| **WP Engine** | $25 | 专业 WordPress 托管 |
| **Kinsta** | $30 | Google Cloud 基础设施 |
| **Flywheel** | $15 | 适合开发者 |

#### 流程

```
1. 注册账号
2. 创建网站
3. 使用官方迁移插件
4. 自动完成迁移
```

---

## 🔒 第三部分：域名和 SSL 配置

### 3.1 购买域名

| 服务商 | 价格/年 | 特点 |
|--------|---------|------|
| **Namecheap** | $10 | 便宜，好用 |
| **GoDaddy** | $12 | 最大注册商 |
| **阿里云** | ¥55 | 国内备案方便 |

---

### 3.2 域名解析

#### 获取服务器 IP

```
服务器控制面板 → 查看 IP 地址
例如：123.45.67.89
```

#### 添加 DNS 记录

```
登录域名管理后台 → DNS 设置

添加 A 记录：
├─ 主机记录：@
├─ 记录类型：A
├─ 记录值：123.45.67.89
└─ TTL：自动

添加 www 记录：
├─ 主机记录：www
├─ 记录类型：CNAME
├─ 记录值：your-domain.com
└─ TTL：自动
```

**生效时间**: 5 分钟 - 48 小时

---

### 3.3 配置 SSL 证书

#### 方式 1：Let's Encrypt（免费）

**SiteGround 自动配置**:
```
SiteGround 后台 → Security → SSL
   ↓
选择 Let's Encrypt
   ↓
点击 Activate
```

**手动配置**（VPS）:
```bash
# 安装 Certbot
sudo apt install certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# 自动续期
sudo certbot renew --dry-run
```

#### 方式 2：购买商业证书

| 类型 | 价格/年 | 适合 |
|------|---------|------|
| **单域名** | $50 | 个人/小站 |
| **多域名** | $100 | 企业 |
| **通配符** | $200 | 多子域名 |

---

## 💳 第四部分：支付配置

### 4.1 Stripe（国际信用卡）

#### 获取密钥

```
1. 注册 Stripe: https://stripe.com
2. 进入 Dashboard → Developers → API keys
3. 复制 Publishable key 和 Secret key
```

#### 配置 WooCommerce

```
后台 → WooCommerce → 设置 → 支付 → Stripe
   ↓
启用 Stripe
   ↓
填写 API 密钥
   ↓
保存
```

**测试模式**:
```
测试卡号：4242 4242 4242 4242
过期：任意未来日期
CVC: 任意 3 位
```

---

### 4.2 支付宝/微信（国内支付）

#### 安装插件

```
后台 → 插件 → 添加插件
搜索：Alipay for WooCommerce
安装并激活
```

#### 配置

```
后台 → WooCommerce → 设置 → 支付 → Alipay
   ↓
填写支付宝商户信息
   ↓
保存
```

**需要**:
- 支付宝商户账号
- APP ID
- 公钥/私钥

---

### 4.3 银行转账（最简单）

```
后台 → WooCommerce → 设置 → 支付 → 银行转账
   ↓
启用
   ↓
填写银行账户信息
   ↓
保存
```

---

## 📊 第五部分：性能优化

### 5.1 缓存插件

| 插件 | 价格 | 推荐 |
|------|------|------|
| **WP Rocket** | $49/年 | ⭐⭐⭐⭐⭐ |
| **W3 Total Cache** | 免费 | ⭐⭐⭐⭐ |
| **WP Super Cache** | 免费 | ⭐⭐⭐ |

---

### 5.2 图片优化

```
安装插件：Smush 或 ShortPixel
   ↓
自动压缩上传的图片
   ↓
启用懒加载
```

---

### 5.3 CDN 配置

| 服务商 | 价格 | 特点 |
|--------|------|------|
| **Cloudflare** | 免费 | 基础 CDN |
| **KeyCDN** | $0.04/GB | 按量付费 |
| **StackPath** | $10/月 | 固定费用 |

---

## 🔐 第六部分：安全配置

### 6.1 基础安全

```
1. 使用强密码
2. 启用双因素认证
3. 定期更新 WordPress 和插件
4. 限制登录尝试次数
```

### 6.2 安全插件

| 插件 | 功能 |
|------|------|
| **Wordfence** | 防火墙 + 恶意软件扫描 |
| **Sucuri** | 安全监控 |
| **iThemes Security** | 综合安全 |

---

### 6.3 备份策略

```
安装插件：UpdraftPlus

配置自动备份：
├─ 频率：每天
├─ 存储：Google Drive / Dropbox
├─ 保留：最近 7 个备份
└─ 包含：数据库 + 文件
```

---

## 📝 第七部分：检查清单

### 上线前检查

- [ ] 域名解析完成
- [ ] SSL 证书配置
- [ ] WooCommerce 设置完整
- [ ] 支付方式测试
- [ ] 配送设置配置
- [ ] 商品图片和描述完整
- [ ] 联系页面信息
- [ ] 隐私政策页面
- [ ] 备份插件配置
- [ ] 安全插件配置
- [ ] 缓存插件配置
- [ ] 测试订单流程
- [ ] 移动端适配测试
- [ ] 页面加载速度测试

---

## 🆚 本地 vs 生产环境对比

| 项目 | 本地 (LocalWP) | 生产 (服务器) |
|------|----------------|---------------|
| **域名** | my-store.local | your-domain.com |
| **协议** | HTTP | HTTPS |
| **数据库** | 本地 MySQL | 服务器 MySQL |
| **文件路径** | ~/Library/... | /var/www/html |
| **访问速度** | 快（本地） | 取决于服务器 |
| **用途** | 开发测试 | 正式运营 |

---

## 💡 经验总结

1. **本地开发用 LocalWP** - 简单快速
2. **生产环境选托管** - 省心省力
3. **迁移用插件** - 避免手动出错
4. **SSL 必须配置** - 影响 SEO 和信任
5. **定期备份** - 防止数据丢失
6. **支付先测试** - 用测试模式验证
7. **性能要优化** - 缓存 + CDN
8. **安全不忽视** - 防火墙 + 强密码

---

## 🔗 相关资源

- **LocalWP 官网**: https://localwp.com
- **WooCommerce 官方**: https://woocommerce.com
- **WordPress 官方**: https://wordpress.org
- **ThemeForest 主题**: https://themeforest.net
- **Stripe 文档**: https://stripe.com/docs

---

## ⏱️ 时间估算

| 任务 | 预计时间 |
|------|----------|
| LocalWP 安装 | 5 分钟 |
| 创建网站 | 2 分钟 |
| WooCommerce 配置 | 30 分钟 |
| 主题选择和定制 | 1-2 小时 |
| 商品上架 | 取决于数量 |
| 服务器购买 | 10 分钟 |
| 网站迁移 | 30 分钟 |
| 域名和 SSL | 30 分钟 |
| 支付配置 | 30 分钟 |
| **总计** | **约 4-6 小时** |

---

## ✅ 完成状态

- [x] LocalWP 安装指南
- [x] 本地网站创建
- [x] WooCommerce 配置
- [x] 服务器选择指南
- [x] 三种部署方式
- [x] 域名和 SSL 配置
- [x] 支付配置指南
- [x] 性能优化建议
- [x] 安全配置指南
- [x] 检查清单
