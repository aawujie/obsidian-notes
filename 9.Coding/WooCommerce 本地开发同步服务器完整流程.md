# WooCommerce 本地开发同步服务器完整流程

## 📅 基本信息

- **创建日期**: 2026-02-25
- **开发环境**: LocalWP (本地)
- **生产环境**: 腾讯云服务器
- **同步工具**: rsync + SSH
- **适用场景**: WordPress + WooCommerce 网站

---

## 🎯 核心概念

### LocalWP 的正确定位

```
LocalWP 不是用来"配置好后迁移"的
LocalWP 是用来"开发和测试"的
```

**错误理解**:
```
LocalWP 配置 WooCommerce → 导出 → 迁移到服务器
❌ 数据库配置、URL 都要改，行不通
```

**正确理解**:
```
LocalWP 测试新功能 → 确认没问题 → 同步代码到服务器
✅ 只同步前端代码，数据库服务器重配
```

---

## 📦 什么可以同步？什么不可以？

### ✅ 可以同步的（前端代码）

| 类型 | 路径 | 同步频率 | 说明 |
|------|------|----------|------|
| **主题文件** | `wp-content/themes/` | 高 | 主题模板、CSS、JS |
| **自定义插件** | `wp-content/plugins/` | 中 | 自己开发的插件 |
| **上传文件** | `wp-content/uploads/` | 中 | 图片、视频等媒体 |
| **前端代码** | 所有 `.php` `.css` `.js` | 高 | 模板、样式、脚本 |
| **语言文件** | `wp-content/languages/` | 低 | 翻译文件 |

**同步方式**: rsync 增量同步
**时间**: 10-30 秒
**影响**: 立即生效，无需重启

---

### ❌ 不可以同步的（数据库配置）

| 类型 | 原因 | 解决方式 |
|------|------|----------|
| **WooCommerce 设置** | 数据库存储，URL 不同 | 服务器重新配置 |
| **支付配置 (Stripe)** | 敏感信息，环境不同 | 服务器重新填写密钥 |
| **配送设置** | 数据库存储 | 服务器重新配置 |
| **插件设置** | 数据库存储 | 服务器重新配置 |

**原因**:
- 数据库连接信息不同（本地 vs 服务器）
- 网站 URL 不同（local vs 公网 IP/域名）
- 敏感信息不应同步（API 密钥等）

---

### ⚠️ 可以但麻烦的（数据库内容）

| 类型 | 同步难度 | 推荐方式 |
|------|----------|----------|
| **商品数据** | ⭐⭐⭐ 中等 | 导出导入 CSV |
| **订单数据** | ⭐⭐⭐⭐ 困难 | mysqldump |
| **用户数据** | ⭐⭐⭐⭐ 困难 | mysqldump |
| **页面/文章** | ⭐⭐ 简单 | WordPress 导出工具 |

**建议**:
- 开发阶段：用测试数据
- 上线前：手动录入真实数据
- 大迁移：用 All-in-One WP Migration 插件

---

## 🚀 本地开发同步流程

### 首次部署（一次性）

```
1. LocalWP 熟悉流程（1 次）
   └─ 配置 WooCommerce
   └─ 测试主题/插件
   └─ 熟悉后台操作
   
2. 服务器重新配置（1 次）
   └─ 安装 WordPress
   └─ 安装 WooCommerce
   └─ 配置支付/配送
   └─ 填写 API 密钥
   
3. 创建同步脚本（1 次）
   └─ 配置 rsync
   └─ 测试同步
```

**时间**: 2-3 小时（仅首次）

---

### 日常开发（重复）

```
1. LocalWP 修改代码
   └─ 修改主题模板
   └─ 调试 CSS/JS
   └─ 测试新功能
   
2. 本地测试
   └─ 访问 http://my-store.local
   └─ 验证功能正常
   
3. 同步到服务器
   └─ 运行 sync 脚本（10 秒）
   └─ 访问服务器验证
   
4. 完成 ✅
```

**时间**: 5-30 分钟（取决于修改内容）

---

## 📋 同步脚本配置

### 创建同步脚本

```bash
#!/bin/bash

# WooCommerce 网站增量同步脚本
# 用法：./sync-to-server.sh

# 配置
LOCAL_PATH=~/code/8.practice/WooCommerceSite/shop/app/public
REMOTE_USER=ubuntu
REMOTE_HOST=43.133.40.16
REMOTE_PATH=/var/www/html/wordpress
SSH_KEY=~/.ssh/tenxunyun/Mac.pem

echo "🚀 开始同步到服务器..."
echo "本地：$LOCAL_PATH"
echo "服务器：$REMOTE_USER@$REMOTE_HOST:$REMOTE_PATH"
echo ""

# rsync 增量同步
rsync -avz --delete \
    --exclude 'wp-content/cache/*' \
    --exclude 'wp-content/updraft/*' \
    --exclude 'wp-config.php' \
    -e "ssh -i $SSH_KEY" \
    $LOCAL_PATH/ \
    $REMOTE_USER@$REMOTE_HOST:$REMOTE_PATH/

# 设置权限
ssh -i $SSH_KEY $REMOTE_USER@$REMOTE_HOST "sudo chown -R www-data:www-data $REMOTE_PATH && sudo chmod -R 755 $REMOTE_PATH"

echo ""
echo "✅ 同步完成！"
echo "访问：http://$REMOTE_HOST"
```

### 使用方式

```bash
# 赋予执行权限
chmod +x sync-to-server.sh

# 运行同步
./sync-to-server.sh
```

### 输出示例

```
🚀 开始同步到服务器...
本地：/Users/apple/code/8.practice/WooCommerceSite/shop/app/public
服务器：ubuntu@43.133.40.16:/var/www/html/wordpress

sending incremental file list
themes/storefront/style.css
plugins/woocommerce/templates/single-product.php

sent 1.2MB  received 128 bytes  234.56KB/s
total size is 50MB  speedup is 41.23

✅ 同步完成！
访问：http://43.133.40.16
```

---

## 🔧 rsync 参数说明

| 参数 | 说明 | 作用 |
|------|------|------|
| `-a` | archive | 归档模式，保留权限、时间等 |
| `-v` | verbose | 显示详细输出 |
| `-z` | compress | 传输时压缩 |
| `--delete` | 删除 | 删除服务器多余文件 |
| `--exclude` | 排除 | 不同步指定文件 |

### 推荐排除项

```bash
--exclude 'wp-content/cache/*'      # 缓存文件
--exclude 'wp-content/updraft/*'    # 备份文件
--exclude 'wp-config.php'           # 配置文件（服务器独立）
--exclude '.git/'                   # Git 仓库
--exclude 'node_modules/'           # Node 依赖
--exclude '*.log'                   # 日志文件
```

---

## 📊 同步场景对比

### 场景 1：修改主题样式

```
本地修改：wp-content/themes/storefront/style.css
   ↓
运行同步：./sync-to-server.sh
   ↓
同步内容：1 个文件（50KB）
   ↓
时间：5 秒
   ↓
生效：立即
```

---

### 场景 2：修改产品模板

```
本地修改：wp-content/themes/storefront/woocommerce/single-product.php
   ↓
运行同步：./sync-to-server.sh
   ↓
同步内容：1 个文件（20KB）
   ↓
时间：5 秒
   ↓
生效：立即
```

---

### 场景 3：安装新插件

```
本地安装：插件 → 安装 → 启用
   ↓
测试功能：✅ 正常
   ↓
运行同步：./sync-to-server.sh
   ↓
同步内容：整个插件目录（2MB）
   ↓
时间：30 秒
   ↓
服务器：手动启用插件
```

---

### 场景 4：上传产品图片

```
本地上传：媒体库 → 上传图片
   ↓
图片位置：wp-content/uploads/2026/02/
   ↓
运行同步：./sync-to-server.sh
   ↓
同步内容：新上传的图片（5MB）
   ↓
时间：1 分钟
   ↓
生效：立即
```

---

### 场景 5：更新 WooCommerce 配置

```
本地修改：WooCommerce → 设置 → 配送
   ↓
❌ 无法同步（数据库存储）
   ↓
服务器操作：
└─ 登录后台
└─ 重新配置相同设置
   ↓
时间：5 分钟
```

---

## 🎯 最佳实践

### 1. 开发环境隔离

```
LocalWP（开发）
├─ 开启调试模式
├─ 使用测试数据
├─ 随意测试功能
└─ 不影响线上

服务器（生产）
├─ 关闭调试模式
├─ 使用真实数据
├─ 稳定运行
└─ 对外服务
```

---

### 2. 同步前检查清单

```bash
# 同步前检查
□ 本地测试通过
□ 移除调试代码
□ 清除缓存文件
□ 备份重要数据
□ 通知团队成员（如有）
```

---

### 3. 版本控制（推荐）

```bash
# 使用 Git 管理代码
cd ~/code/WooCommerceSite/shop/app/public

# 提交修改
git add .
git commit -m "修改产品页面布局"
git push origin main

# 服务器拉取
ssh ubuntu@服务器 IP
cd /var/www/html/wordpress
git pull origin main
```

**优点**:
- ✅ 有版本记录
- ✅ 可以回滚
- ✅ 团队协作方便
- ✅ 自动部署集成

---

### 4. 数据库同步（谨慎）

```bash
# 仅在必要时同步数据库
# 导出本地数据库
mysqldump -u root -p local > backup.sql

# 上传到服务器
scp backup.sql ubuntu@服务器 IP:/tmp/

# 服务器导入
ssh ubuntu@服务器 IP
mysql -u wordpress -p wordpress < /tmp/backup.sql

# 更新 URL
wp search-replace 'http://my-store.local' 'http://服务器 IP' --all-tables
```

**警告**:
- ⚠️ 会覆盖服务器数据
- ⚠️ 订单、用户数据会丢失
- ⚠️ 仅在新站迁移时使用

---

## 📝 工作流程图

```
┌─────────────────────────────────────────────────────────┐
│  开发阶段 (LocalWP)                                      │
│                                                          │
│  1. 修改主题/插件代码                                     │
│     ↓                                                    │
│  2. 本地测试功能                                         │
│     ↓                                                    │
│  3. 确认没有问题                                         │
│     ↓                                                    │
│  4. 运行同步脚本                                         │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  同步过程 (rsync)                                        │
│                                                          │
│  • 只传输修改的文件                                      │
│  • 自动删除服务器多余文件                                │
│  • 保留文件权限                                          │
│  • 压缩传输                                              │
│  • 10-30 秒完成                                          │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  生产环境 (服务器)                                        │
│                                                          │
│  1. 接收新文件                                           │
│     ↓                                                    │
│  2. 自动生效                                             │
│     ↓                                                    │
│  3. 访问网站验证                                         │
│     ↓                                                    │
│  4. 完成 ✅                                               │
└─────────────────────────────────────────────────────────┘
```

---

## 🔍 常见问题

### Q1: 同步后网站打不开？

```bash
# 检查文件权限
ssh ubuntu@服务器 IP
sudo chown -R www-data:www-data /var/www/html/wordpress
sudo chmod -R 755 /var/www/html/wordpress

# 检查 Nginx 状态
sudo systemctl status nginx

# 查看错误日志
tail -f /var/log/nginx/error.log
```

---

### Q2: 样式修改没生效？

```bash
# 清除浏览器缓存
# 或强制刷新：Cmd+Shift+R (Mac) / Ctrl+F5 (Windows)

# 清除服务器缓存
ssh ubuntu@服务器 IP
sudo rm -rf /var/www/html/wordpress/wp-content/cache/*
```

---

### Q3: 同步太慢？

```bash
# 检查网络速度
ping 服务器 IP

# 排除大文件
rsync -avz --exclude 'wp-content/uploads/*' ...

# 使用增量同步（确保用 rsync 不是 scp）
```

---

### Q4: 数据库需要更新怎么办？

```bash
# 方式 1: 手动配置（推荐）
登录服务器后台 → 重新配置

# 方式 2: 导出导入（谨慎）
本地导出 → 上传 → 服务器导入 → 更新 URL

# 方式 3: 使用插件
All-in-One WP Migration
```

---

## 💡 经验总结

1. **LocalWP 用于开发** - 不要指望配置好后直接迁移
2. **代码可以同步** - 主题、插件、前端代码随便同步
3. **数据库要重配** - WooCommerce 设置、支付配置服务器重填
4. **rsync 是神器** - 增量同步，只传修改的文件
5. **Git 更专业** - 有条件用 Git 管理代码
6. **同步前备份** - 重要修改前先备份服务器
7. **测试再同步** - 本地测试好再同步到服务器
8. **避开高峰期** - 不要在访问高峰时同步

---

## 📋 快速参考

### 同步命令

```bash
# 快速同步
./sync-to-server.sh

# 手动 rsync
rsync -avz --delete -e "ssh -i ~/.ssh/key.pem" \
    ~/local/path/ \
    ubuntu@服务器 IP:/var/www/html/wordpress/

# SSH 登录
ssh -i ~/.ssh/key.pem ubuntu@服务器 IP

# 查看服务器状态
df -h && free -m
```

### 重要路径

| 位置 | 路径 |
|------|------|
| **本地网站** | `~/code/WooCommerceSite/shop/app/public` |
| **服务器网站** | `/var/www/html/wordpress` |
| **同步脚本** | `~/code/WooCommerceSite/sync-to-server.sh` |
| **SSH 密钥** | `~/.ssh/tenxunyun/Mac.pem` |

### 重要信息

| 项目 | 信息 |
|------|------|
| **服务器 IP** | 43.133.40.16 |
| **用户名** | ubuntu |
| **数据库名** | wordpress |
| **数据库用户** | wordpress |

---

## ✅ 检查清单

### 首次部署

- [ ] LocalWP 安装配置
- [ ] 熟悉 WooCommerce 流程
- [ ] 服务器环境搭建
- [ ] WordPress 安装
- [ ] WooCommerce 配置
- [ ] 支付配置
- [ ] 同步脚本创建
- [ ] 测试同步

### 日常开发

- [ ] 本地修改代码
- [ ] 本地测试通过
- [ ] 运行同步脚本
- [ ] 服务器验证
- [ ] 清除缓存（如需要）

---

## 🔗 相关资源

- **rsync 官方文档**: https://rsync.samba.org/
- **WordPress 编码规范**: https://developer.wordpress.org/coding-standards/
- **WooCommerce 开发文档**: https://woocommerce.com/development/
- **腾讯云文档**: https://cloud.tencent.com/document

---

## ⏱️ 时间对比

| 操作 | 传统方式 | rsync 同步 |
|------|----------|------------|
| **首次部署** | 1 小时 | 1 小时 |
| **日常更新（代码）** | 30 分钟（全量上传） | 10-30 秒 |
| **日常更新（数据库）** | 10 分钟 | 10 分钟（相同） |
| **主题修改** | 30 分钟 | 5 秒 |
| **插件更新** | 5 分钟 | 1 分钟 |

**效率提升**: 日常更新速度提升 **60-180 倍**！

---

## 🎯 总结

```
LocalWP 定位：开发和测试环境
同步内容：前端代码（主题、插件、模板）
不同步：数据库配置（WooCommerce 设置、支付）
同步工具：rsync 增量同步
同步时间：10-30 秒
工作流程：本地修改 → 测试 → 同步 → 验证
```

**核心理念**: 
> LocalWP 用来安全地开发和测试，服务器用来稳定地运行和服务用户。
> 代码可以同步，配置要重做。
