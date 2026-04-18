# 腾讯云 SSH 命令行部署 WooCommerce 完整指南

## 📅 基本信息

- **创建日期**: 2026-02-25
- **部署方式**: 纯 SSH 命令行
- **云服务商**: 腾讯云 (Tencent Cloud)
- **技术栈**: Nginx + MySQL + PHP + WordPress + WooCommerce
- **适用**: 专业运维/开发者

---

## 🎯 为什么选择纯命令行

### 优势

| 优势 | 说明 |
|------|------|
| ✅ **高效** | 脚本化，可重复部署 |
| ✅ **可控** | 完全掌握每个配置 |
| ✅ **轻量** | 无图形界面，资源占用少 |
| ✅ **专业** | 标准运维流程 |
| ✅ **自动化** | 便于 CI/CD 集成 |

### 工具链

```
SSH → 远程连接
Vim → 文件编辑
Systemd → 服务管理
Git → 版本控制
WP-CLI → WordPress 命令行
```

---

## 📋 部署流程总览

```
1. 购买云服务器 (10 分钟)
   ↓
2. SSH 连接服务器 (5 分钟)
   ↓
3. 系统初始化 (10 分钟)
   ↓
4. 安装 LEMP 栈 (20 分钟)
   ↓
5. 配置 WordPress (15 分钟)
   ↓
6. 安装 WooCommerce (10 分钟)
   ↓
7. 迁移本地数据 (30 分钟)
   ↓
8. 配置域名和 SSL (20 分钟)
   ↓
9. 安全加固 (15 分钟)
   ↓
10. 性能优化 (15 分钟)
   ↓
总计：约 2.5 小时
```

---

## 第 1 步：购买腾讯云服务器

### 1.1 推荐配置

```bash
# 最小配置（测试）
CPU: 2 核
内存：2GB
带宽：3Mbps
系统：CentOS 7.9 或 Ubuntu 20.04
磁盘：50GB SSD

# 生产配置（推荐）
CPU: 4 核
内存：4GB
带宽：5Mbps
系统：Ubuntu 20.04 LTS
磁盘：100GB SSD
```

### 1.2 安全组配置

```bash
# 必须放行的端口
80    # HTTP
443   # HTTPS
22    # SSH

# 可选（内网访问）
3306  # MySQL（不建议对外）
```

### 1.3 获取服务器信息

```bash
# 记录以下信息：
服务器公网 IP: xxx.xxx.xxx.xxx
SSH 端口：22
SSH 用户名：root
SSH 密码：******（或 SSH 密钥）
```

---

## 第 2 步：SSH 连接服务器

### 2.1 本地连接

```bash
# 密码登录
ssh root@服务器 IP

# 首次连接会提示确认指纹
# 输入 yes 确认

# 输入密码（不显示）
# 登录成功
```

### 2.2 配置 SSH 密钥（推荐）

```bash
# 本地生成密钥（如果没有）
ssh-keygen -t ed25519 -C "your_email@example.com"

# 复制公钥到服务器
ssh-copy-id root@服务器 IP

# 测试免密登录
ssh root@服务器 IP
```

### 2.3 配置 SSH 别名（可选）

```bash
# 本地编辑 ~/.ssh/config
vim ~/.ssh/config

# 添加配置
Host tencent
    HostName 服务器 IP
    User root
    Port 22
    IdentityFile ~/.ssh/id_ed25519

# 以后可以这样登录
ssh tencent
```

---

## 第 3 步：系统初始化

### 3.1 更新系统

```bash
# 更新软件包
yum update -y

# 或 Ubuntu
apt update && apt upgrade -y
```

### 3.2 创建交换空间（小内存服务器）

```bash
# 创建 2GB 交换空间
dd if=/dev/zero of=/swapfile bs=1M count=2048
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile

# 永久生效
echo '/swapfile none swap sw 0 0' >> /etc/fstab
```

### 3.3 创建普通用户（安全）

```bash
# 创建新用户
adduser deploy

# 设置密码
passwd deploy

# 添加 sudo 权限
usermod -aG wheel deploy  # CentOS
usermod -aG sudo deploy   # Ubuntu

# 复制 SSH 密钥
mkdir -p /home/deploy/.ssh
cp -r /root/.ssh/* /home/deploy/.ssh/
chown -R deploy:deploy /home/deploy/.ssh
chmod 700 /home/deploy/.ssh
chmod 600 /home/deploy/.ssh/authorized_keys

# 测试新用户登录
ssh deploy@服务器 IP
```

### 3.4 禁用 root 登录（安全）

```bash
# 编辑 SSH 配置
vim /etc/ssh/sshd_config

# 修改以下配置
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes

# 重启 SSH 服务
systemctl restart sshd
```

### 3.5 配置防火墙

```bash
# 安装 firewalld（CentOS）
yum install -y firewalld
systemctl start firewalld
systemctl enable firewalld

# 开放端口
firewall-cmd --permanent --add-service=http
firewall-cmd --permanent --add-service=https
firewall-cmd --permanent --add-service=ssh

# 重载配置
firewall-cmd --reload

# 查看状态
firewall-cmd --list-all
```

### 3.6 安装必要工具

```bash
# 安装工具包
yum install -y \
    vim \
    git \
    curl \
    wget \
    unzip \
    zip \
    htop \
    net-tools \
    bash-completion

# Ubuntu
apt install -y vim git curl wget unzip zip htop net-tools bash-completion
```

---

## 第 4 步：安装 LEMP 栈

### 4.1 安装 Nginx

```bash
# 安装 Nginx
yum install -y nginx

# 启动并设置开机自启
systemctl start nginx
systemctl enable nginx

# 检查状态
systemctl status nginx

# 验证安装
curl -I http://localhost
```

### 4.2 安装 MySQL (MariaDB)

```bash
# 安装 MariaDB
yum install -y mariadb-server mariadb

# 启动并设置开机自启
systemctl start mariadb
systemctl enable mariadb

# 安全初始化
mysql_secure_installation

# 按提示：
# 设置 root 密码
# 移除匿名用户
# 禁止 root 远程登录
# 移除测试数据库
# 重载权限表
```

### 4.3 创建 WordPress 数据库

```bash
# 登录 MySQL
mysql -u root -p

# 执行 SQL
CREATE DATABASE wordpress DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE USER 'wordpress'@'localhost' IDENTIFIED BY '强密码';

GRANT ALL PRIVILEGES ON wordpress.* TO 'wordpress'@'localhost';

FLUSH PRIVILEGES;

EXIT;
```

### 4.4 安装 PHP 及扩展

```bash
# 安装 Remi 仓库（CentOS）
yum install -y \
    https://repo.remirepo.net/enterprise/remi-release-7.rpm

# 启用 PHP 7.4
yum-config-manager --enable remi-php74

# 安装 PHP 和扩展
yum install -y \
    php \
    php-fpm \
    php-mysqlnd \
    php-gd \
    php-curl \
    php-mbstring \
    php-xml \
    php-xmlrpc \
    php-zip \
    php-intl \
    php-bcmath \
    php-json

# 启动 PHP-FPM
systemctl start php-fpm
systemctl enable php-fpm
```

### 4.5 配置 Nginx

```bash
# 编辑 Nginx 配置
vim /etc/nginx/conf.d/wordpress.conf

# 添加配置
server {
    listen 80;
    server_name 服务器 IP;
    root /var/www/html;
    index index.php index.html index.htm;

    # 日志
    access_log /var/log/nginx/wordpress_access.log;
    error_log /var/log/nginx/wordpress_error.log;

    # 最大上传
    client_max_body_size 64M;

    # WordPress 规则
    location / {
        try_files $uri $uri/ /index.php?$args;
    }

    # PHP 处理
    location ~ \.php$ {
        include fastcgi_params;
        fastcgi_pass unix:/run/php-fpm/www.sock;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        fastcgi_index index.php;
        include fastcgi_params;
    }

    # 隐藏文件
    location ~ /\. {
        deny all;
    }

    # 静态资源
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|pdf|txt)$ {
        expires 30d;
        access_log off;
    }
}

# 测试配置
nginx -t

# 重载 Nginx
systemctl reload nginx
```

### 4.6 设置目录权限

```bash
# 创建网站目录
mkdir -p /var/www/html

# 设置所有权
chown -R deploy:deploy /var/www/html

# 设置权限
chmod -R 755 /var/www/html
```

---

## 第 5 步：安装 WordPress

### 5.1 下载 WordPress

```bash
# 进入网站目录
cd /var/www/html

# 下载 WordPress（中文）
wget https://cn.wordpress.org/latest-zh_CN.zip

# 解压
unzip latest-zh_CN.zip

# 移动文件
mv wordpress/* .
mv wordpress/.htaccess .

# 清理
rm -rf wordpress latest-zh_CN.zip

# 设置权限
chown -R deploy:deploy .
find . -type d -exec chmod 755 {} \;
find . -type f -exec chmod 644 {} \;
```

### 5.2 配置 wp-config.php

```bash
# 复制配置文件
cp wp-config-sample.php wp-config.php

# 编辑配置
vim wp-config.php

# 修改数据库配置
define('DB_NAME', 'wordpress');
define('DB_USER', 'wordpress');
define('DB_PASSWORD', '你设置的密码');
define('DB_HOST', 'localhost');
define('DB_CHARSET', 'utf8mb4');
define('DB_COLLATE', '');

# 生成安全密钥
# 访问：https://api.wordpress.org/secret-key/1.1/salt/
# 复制生成的内容替换下面的密钥

# 保存退出
```

### 5.3 使用 WP-CLI 安装（推荐）

```bash
# 安装 WP-CLI
curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
chmod +x wp-cli.phar
mv wp-cli.phar /usr/local/bin/wp

# 验证安装
wp --info

# 安装 WordPress
wp core install \
    --url="http://服务器 IP" \
    --title="你的商店名称" \
    --admin_user="admin" \
    --admin_password="强密码" \
    --admin_email="your@email.com"

# 查看安装信息
wp core version
```

### 5.4 传统方式安装

```bash
# 浏览器访问
http://服务器 IP

# 按向导填写：
# 数据库名：wordpress
# 用户名：wordpress
# 密码：你设置的
# 数据库主机：localhost
# 表前缀：wp_

# 运行安装
# 填写站点信息
```

---

## 第 6 步：安装 WooCommerce

### 6.1 使用 WP-CLI 安装

```bash
# 安装 WooCommerce
wp plugin install woocommerce --activate

# 查看已安装插件
wp plugin list

# 运行 WooCommerce 安装向导
wp wc tool run install_pages --user=admin
```

### 6.2 配置 WooCommerce

```bash
# 基本设置
wp option update woocommerce_store_address "你的地址"
wp option update woocommerce_store_address_2 ""
wp option update woocommerce_store_city "你的城市"
wp option update woocommerce_default_country "CN:Guangdong"
wp option update woocommerce_store_postcode "邮编"
wp option update woocommerce_currency "CNY"
wp option update woocommerce_currency_pos "left"
wp option update woocommerce_price_thousand_sep ","
wp option update woocommerce_price_decimal_sep "."
wp option update woocommerce_price_num_decimals "2"

# 启用支付
wp option update woocommerce_gateway_order 'a:1:{s:6:"bacs";i:0;}'

# 查看配置
wp option get woocommerce_store_address
```

### 6.3 安装主题

```bash
# 安装 Storefront 主题
wp theme install storefront --activate

# 查看主题
wp theme list
```

---

## 第 7 步：迁移本地数据

### 7.1 本地导出

```bash
# 本地使用 WP-CLI 导出
cd ~/Library/Application\ Support/Local/runs/my-store/app
wp db export backup.sql
wp export --dir=content-export
```

### 7.2 上传到服务器

```bash
# 本地压缩
tar -czf woocommerce-backup.tar.gz wp-content

# 上传到服务器（本地执行）
scp woocommerce-backup.tar.gz deploy@服务器 IP:/tmp/
scp backup.sql deploy@服务器 IP:/tmp/
```

### 7.3 服务器导入

```bash
# 解压
cd /var/www/html
tar -xzf /tmp/woocommerce-backup.tar.gz

# 导入数据库
mysql -u wordpress -p wordpress < /tmp/backup.sql

# 更新 URL
wp search-replace 'http://my-store.local' 'http://服务器 IP' --all-tables

# 清除缓存
wp cache flush

# 重新保存固定链接
wp rewrite flush
```

---

## 第 8 步：配置域名和 SSL

### 8.1 域名 DNS 配置

```bash
# 在域名商处添加 A 记录
# 主机记录：@
# 记录值：服务器 IP
# TTL: 600
```

### 8.2 安装 Certbot

```bash
# 安装 EPEL 仓库
yum install -y epel-release

# 安装 Certbot
yum install -y certbot python3-certbot-nginx
```

### 8.3 申请 SSL 证书

```bash
# 申请证书
certbot --nginx -d your-domain.com -d www.your-domain.com

# 按提示输入邮箱
# 同意条款
# 选择是否重定向到 HTTPS

# 自动续期测试
certbot renew --dry-run
```

### 8.4 更新 WordPress URL

```bash
# 使用 WP-CLI
wp option update home 'https://your-domain.com'
wp option update siteurl 'https://your-domain.com'

# 或编辑 wp-config.php
vim wp-config.php
# 添加：
define('WP_HOME', 'https://your-domain.com');
define('WP_SITEURL', 'https://your-domain.com');
```

---

## 第 9 步：安全加固

### 9.1 配置 Fail2ban

```bash
# 安装
yum install -y fail2ban

# 配置
vim /etc/fail2ban/jail.local

# 添加：
[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/secure
maxretry = 3
bantime = 3600

# 启动
systemctl start fail2ban
systemctl enable fail2ban
```

### 9.2 WordPress 安全配置

```bash
# 限制登录尝试
wp plugin install limit-login-attempts-reloaded --activate

# 安装安全插件
wp plugin install wordfence --activate

# 禁用文件编辑
wp config set 'DISALLOW_FILE_EDIT' true --raw

# 禁用 XML-RPC
wp config set 'DISABLE_WP_XML_RPC' true --raw
```

### 9.3 数据库安全

```bash
# 修改 MySQL 端口（可选）
vim /etc/my.cnf
# 添加：port = 3307

# 重启 MySQL
systemctl restart mariadb
```

### 9.4 定期更新

```bash
# 创建更新脚本
vim /usr/local/bin/wp-update.sh

# 添加内容：
#!/bin/bash
cd /var/www/html
wp core update
wp plugin update --all
wp theme update --all
wp db optimize

# 设置权限
chmod +x /usr/local/bin/wp-update.sh

# 添加到 crontab
crontab -e
# 添加：0 3 * * 1 /usr/local/bin/wp-update.sh
```

---

## 第 10 步：性能优化

### 10.1 启用 OPcache

```bash
# 编辑 PHP 配置
vim /etc/php.ini

# 添加/修改：
[opcache]
opcache.enable=1
opcache.memory_consumption=128
opcache.interned_strings_buffer=8
opcache.max_accelerated_files=4000
opcache.revalidate_freq=60

# 重启 PHP-FPM
systemctl restart php-fpm
```

### 10.2 安装 Redis 缓存

```bash
# 安装 Redis
yum install -y redis

# 启动
systemctl start redis
systemctl enable redis

# 安装 PHP Redis 扩展
yum install -y php-pecl-redis

# 重启 PHP-FPM
systemctl restart php-fpm

# 安装 WordPress Redis 插件
wp plugin install redis-cache --activate
wp redis enable
```

### 10.3 配置 Nginx 缓存

```bash
# 编辑 Nginx 配置
vim /etc/nginx/conf.d/wordpress.conf

# 添加缓存配置：
# 静态资源缓存
location ~* \.(jpg|jpeg|png|gif|ico|css|js|pdf|txt)$ {
    expires 30d;
    access_log off;
}

# Gzip 压缩
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;
```

### 10.4 监控配置

```bash
# 安装监控工具
yum install -y htop iotop nethogs

# 查看资源使用
htop

# 查看磁盘 IO
iotop

# 查看网络流量
nethogs
```

---

## 📋 运维管理命令

### WordPress 管理

```bash
# 查看版本
wp core version

# 更新核心
wp core update

# 更新插件
wp plugin update --all

# 更新主题
wp theme update --all

# 备份数据库
wp db export backup-$(date +%Y%m%d).sql

# 恢复数据库
wp db import backup.sql

# 创建用户
wp user create username email@example.com --role=administrator

# 重置密码
wp user update admin --user_pass=newpassword

# 查看错误日志
tail -f /var/log/nginx/wordpress_error.log
```

### 系统管理

```bash
# 查看磁盘空间
df -h

# 查看内存
free -h

# 查看进程
ps aux | grep -E 'nginx|php|mysql'

# 查看端口
netstat -tulpn

# 查看日志
journalctl -u nginx -f
journalctl -u php-fpm -f
journalctl -u mariadb -f

# 重启服务
systemctl restart nginx
systemctl restart php-fpm
systemctl restart mariadb
```

### 备份脚本

```bash
# 创建备份脚本
vim /usr/local/bin/wp-backup.sh

# 添加内容：
#!/bin/bash
BACKUP_DIR="/backup/wordpress"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# 备份数据库
wp db export $BACKUP_DIR/db-$DATE.sql

# 备份文件
tar -czf $BACKUP_DIR/files-$DATE.tar.gz /var/www/html

# 删除 7 天前的备份
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Backup completed: $DATE"

# 设置权限
chmod +x /usr/local/bin/wp-backup.sh

# 添加到 crontab（每天 3 点）
crontab -e
# 添加：0 3 * * * /usr/local/bin/wp-backup.sh
```

---

## 🔍 故障排查

### 网站无法访问

```bash
# 检查服务状态
systemctl status nginx
systemctl status php-fpm
systemctl status mariadb

# 检查端口
netstat -tulpn | grep -E '80|443|3306'

# 检查防火墙
firewall-cmd --list-all

# 查看错误日志
tail -100 /var/log/nginx/error.log
tail -100 /var/log/php-fpm/error.log
```

### 数据库连接失败

```bash
# 检查 MySQL 状态
systemctl status mariadb

# 测试连接
mysql -u wordpress -p wordpress -e "SELECT 1"

# 检查配置
grep DB /var/www/html/wp-config.php
```

### 502 Bad Gateway

```bash
# 检查 PHP-FPM
systemctl status php-fpm

# 检查 socket
ls -la /run/php-fpm/

# 查看 Nginx 配置
nginx -t

# 重启服务
systemctl restart php-fpm
systemctl restart nginx
```

### 权限问题

```bash
# 修复权限
chown -R deploy:deploy /var/www/html
find /var/www/html -type d -exec chmod 755 {} \;
find /var/www/html -type f -exec chmod 644 {} \;
```

---

## 📊 监控脚本

```bash
# 创建监控脚本
vim /usr/local/bin/wp-monitor.sh

# 添加内容：
#!/bin/bash

echo "=== WordPress Server Status ==="
echo ""

# CPU
echo "CPU Usage:"
top -bn1 | grep "Cpu(s)" | awk '{print $2 + $4 "%"}'
echo ""

# 内存
echo "Memory Usage:"
free -h | grep Mem
echo ""

# 磁盘
echo "Disk Usage:"
df -h /var/www
echo ""

# 服务状态
echo "Service Status:"
systemctl is-active nginx
systemctl is-active php-fpm
systemctl is-active mariadb
echo ""

# WordPress 状态
cd /var/www/html
echo "WordPress Version: $(wp core version)"
echo "Plugin Count: $(wp plugin list --format=count)"
echo "Theme: $(wp theme list --status=active --field=name)"
echo ""

# 最近错误
echo "Recent Errors:"
tail -5 /var/log/nginx/error.log

# 设置权限
chmod +x /usr/local/bin/wp-monitor.sh
```

---

## ✅ 部署检查清单

- [ ] 服务器购买完成
- [ ] SSH 密钥配置
- [ ] 防火墙配置
- [ ] Nginx 安装配置
- [ ] MySQL 安装配置
- [ ] PHP 安装配置
- [ ] WordPress 安装
- [ ] WooCommerce 安装
- [ ] 域名 DNS 配置
- [ ] SSL 证书配置
- [ ] 安全加固
- [ ] 性能优化
- [ ] 备份脚本配置
- [ ] 监控脚本配置
- [ ] 购物流程测试

---

## 💡 经验总结

1. **使用 WP-CLI** - 命令行管理 WordPress 效率高
2. **定期备份** - 数据库 + 文件，自动化备份
3. **监控资源** - CPU、内存、磁盘、带宽
4. **及时更新** - 核心、插件、主题保持最新
5. **安全加固** - Fail2ban、强密码、禁用 root
6. **启用缓存** - OPcache、Redis、Nginx 缓存
7. **日志分析** - 定期查看错误日志
8. **性能监控** - 使用 htop、iotop 等工具

---

## 🔗 相关资源

- **WP-CLI 官方**: https://wp-cli.org
- **Nginx 文档**: https://nginx.org/en/docs/
- **MariaDB 文档**: https://mariadb.com/docs/
- **PHP 文档**: https://www.php.net/docs.php
- **腾讯云文档**: https://cloud.tencent.com/document

---

## ⏱️ 时间估算

| 任务 | 预计时间 |
|------|----------|
| 服务器购买 | 10 分钟 |
| SSH 连接配置 | 10 分钟 |
| 系统初始化 | 15 分钟 |
| LEMP 栈安装 | 30 分钟 |
| WordPress 安装 | 15 分钟 |
| WooCommerce 配置 | 15 分钟 |
| 数据迁移 | 30 分钟 |
| 域名 SSL 配置 | 20 分钟 |
| 安全优化 | 20 分钟 |
| **总计** | **约 2.5-3 小时** |
