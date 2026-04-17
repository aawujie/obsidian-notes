# rsync 命令详解

**创建时间**: 2026-02-25  
**标签**: #rsync #Linux #命令行 #文件同步 #备份 #运维

---

## 📌 什么是 rsync？

**rsync** = **Remote Sync**（远程同步）

一个**超快的文件复制/同步工具**，支持本地和远程文件传输。

> **核心优势**：增量传输，只传变化的部分，不是整个文件。

---

## 🎯 核心特点

| 特点 | 说明 |
|------|------|
| 🚀 **增量传输** | 只传变化的部分，不是整个文件 |
| 🔍 **智能对比** | 比较文件大小和修改时间 |
| 🔒 **支持 SSH** | 远程传输加密安全 |
| 📦 **保留属性** | 权限、时间戳、软链接等都保留 |
| 🗑️ **可删除同步** | 目标目录可以删除源目录没有的文件 |
| 💀 **断点续传** | 传输中断可以继续 |

---

## 📋 基本语法

```bash
rsync [选项] 源文件/目录 目标文件/目录
```

---

## 🔑 常用选项

| 选项 | 说明 | 记忆技巧 |
|------|------|---------|
| `-a` | 归档模式（递归 + 保留属性） | **a**rchive |
| `-v` | 显示详细过程 | **v**erbose |
| `-z` | 传输时压缩 | **z**ip |
| `-r` | 递归复制目录 | **r**ecursive |
| `-P` | 显示进度 + 断点续传 | **P**rogress |
| `--delete` | 删除目标多余文件 | 保持同步 |
| `--exclude` | 排除文件/目录 | 忽略某些文件 |
| `-e ssh` | 使用 SSH 传输 | 加密安全 |
| `-n` | 测试运行（不实际复制） | **n**o-op |

---

## 🎯 常用场景

### 1️⃣ 本地文件复制

```bash
# 复制文件
rsync file.txt /backup/file.txt

# 复制目录（递归）
rsync -r /source/dir /backup/dir

# 推荐：归档模式（保留所有属性）
rsync -a /source/dir /backup/dir

# 带进度显示
rsync -avP /source/dir /backup/dir
```

---

### 2️⃣ 远程文件传输（最常用）

```bash
# 本地 → 远程服务器
rsync -avz /local/dir user@remote:/remote/dir

# 远程服务器 → 本地
rsync -avz user@remote:/remote/dir /local/dir

# 指定 SSH 端口
rsync -avz -e "ssh -p 2222" /local/dir user@remote:/remote/dir

# 使用 SSH 密钥免密登录
rsync -avz -e "ssh -i ~/.ssh/id_rsa" /local/dir user@remote:/remote/dir
```

---

### 3️⃣ 增量备份

```bash
# 只传输变化的文件
rsync -av --delete /source/ /backup/

# --delete 选项：删除目标目录中源目录没有的文件
# 保持完全同步

# 带进度显示
rsync -avzP --delete /source/ user@remote:/backup/
```

---

### 4️⃣ 排除特定文件

```bash
# 排除 node_modules 和 .git
rsync -av --exclude='node_modules' --exclude='.git' /source/ /backup/

# 排除多个模式
rsync -av --exclude='*.log' --exclude='tmp/' --exclude='.env' /source/ /backup/

# 使用排除文件列表
rsync -av --exclude-from='exclude-list.txt' /source/ /backup/

# exclude-list.txt 内容示例：
# .git
# node_modules/
# *.log
# .env
```

---

### 5️⃣ 测试运行（不实际复制）

```bash
# 预览会发生什么（不实际复制）
rsync -avzn /source/ /backup/

# -n = --dry-run 测试模式
# 先测试再实际运行，避免误操作
```

---

## 💡 经典用法组合

### 黄金组合（最常用）

```bash
# 本地备份
rsync -av /source/ /backup/

# 远程同步
rsync -avz /source/ user@remote:/destination/

# 带进度显示
rsync -avzP /source/ user@remote:/destination/

# 完全同步（删除多余文件）
rsync -avz --delete /source/ user@remote:/destination/

# 排除某些文件
rsync -avz --exclude='*.log' --exclude='tmp/' /source/ /backup/
```

---

## 🆚 rsync vs cp vs scp

| 命令 | 速度 | 增量传输 | 远程 | 推荐场景 |
|------|------|---------|------|---------|
| `cp` | 快 | ❌ 否 | ❌ 否 | 本地简单复制 |
| `scp` | 慢 | ❌ 否 | ✅ 是 | 远程小文件 |
| `rsync` | 🚀 最快 | ✅ 是 | ✅ 是 | **任何场景** |

**示例对比：**

```bash
# 第一次传输 1GB 文件
cp file.txt /backup/          # 复制 1GB
scp file.txt user@remote:/    # 传输 1GB
rsync file.txt user@remote:/  # 传输 1GB

# 第二次传输（文件只改了 1MB）
cp file.txt /backup/          # 复制 1GB ❌
scp file.txt user@remote:/    # 传输 1GB ❌
rsync file.txt user@remote:/  # 传输 1MB ✅ 快！
```

---

## 🎬 实际应用场景

### 场景 1：网站备份

```bash
# 每天备份网站到远程服务器
rsync -avz --delete \
  /var/www/html/ \
  user@backup-server:/backups/website/

# 添加到 crontab 每天凌晨 2 点执行
0 2 * * * rsync -avz --delete /var/www/html/ user@backup:/backups/website/
```

---

### 场景 2：代码部署

```bash
# 部署代码到生产服务器（排除 .git 和 node_modules）
rsync -avz \
  --exclude='.git' \
  --exclude='node_modules' \
  --exclude='.env' \
  --exclude='*.log' \
  ./ user@production:/var/www/myapp/

# 部署后重启服务
rsync -avz --exclude='.git' --exclude='node_modules' ./ user@prod:/var/www/app/ && \
  ssh user@prod "sudo systemctl restart myapp"
```

---

### 场景 3：同步照片

```bash
# 把相机照片同步到电脑
rsync -avz /mnt/camera/DCIM/ ~/Pictures/Camera/

# 同步后删除源文件（移动而非复制）
rsync -avz --remove-source-files /mnt/camera/DCIM/ ~/Pictures/Camera/
```

---

### 场景 4：服务器迁移

```bash
# 把旧服务器数据迁移到新服务器
rsync -avz -e ssh /home/ user@new-server:/home/

# 迁移整个网站（含数据库）
rsync -avz -e ssh /var/www/ user@new-server:/var/www/
mysqldump -u root -p --all-databases > all-databases.sql
rsync -avz -e ssh all-databases.sql user@new-server:/tmp/
```

---

### 场景 5：Time Machine 式备份

```bash
# 创建带时间戳的备份
BACKUP_DIR="/backups/$(date +%Y%m%d_%H%M%S)"
rsync -av --link-dest=/backups/latest /source/ $BACKUP_DIR/
rm /backups/latest
ln -s $BACKUP_DIR /backups/latest

# --link-dest：硬链接未变化的文件，节省空间
```

---

## ⚠️ 注意事项

### 1. 末尾斜杠的区别

```bash
# 复制目录内容（推荐）
rsync -a /source/ /backup/
# 结果：/backup/file1, /backup/file2

# 复制目录本身
rsync -a /source /backup/
# 结果：/backup/source/file1, /backup/source/file2
```

**记忆技巧**：
- `/source/` = 复制**内容**（"进入"目录）
- `/source` = 复制**目录本身**（"拿着"目录）

---

### 2. --delete 危险

```bash
# ⚠️ 会删除目标目录中源目录没有的文件
rsync -av --delete /source/ /backup/

# 建议先测试
rsync -avn --delete /source/ /backup/

# 或使用 --delete-after（复制完再删除）
rsync -av --delete-after /source/ /backup/
```

---

### 3. 权限问题

```bash
# 远程需要有写入权限
rsync -avz /local/ user@remote:/remote/

# 如果需要 sudo
rsync -avz --rsync-path="sudo rsync" /local/ user@remote:/remote/
```

---

### 4. SSH 密钥配置

```bash
# 生成密钥
ssh-keygen -t ed25519

# 复制到远程
ssh-copy-id user@remote

# 测试免密登录
ssh user@remote

# 现在 rsync 不需要密码了
rsync -avz /local/ user@remote:/remote/
```

---

## 📊 性能优化

### 1. 跳过压缩（大文件）

```bash
# 如果文件已经是压缩格式（zip/jpg/mp4）
rsync -av /source/ /backup/
# 不加 -z，避免浪费 CPU
```

### 2. 限制带宽

```bash
# 限制带宽为 1000KB/s
rsync -avz --bwlimit=1000 /source/ user@remote:/backup/
```

### 3. 并行传输

```bash
# 使用多个 SSH 连接并行传输大文件
rsync -avz --partial --progress /source/ user@remote:/backup/
```

---

## 🔍 故障排查

### 查看详细信息

```bash
# 显示更多调试信息
rsync -avvv /source/ /backup/

# 查看传输统计
rsync -av --stats /source/ /backup/
```

### 常见问题

| 问题 | 解决方案 |
|------|---------|
| 权限被拒绝 | 检查远程用户权限或使用 sudo |
| 连接超时 | 检查 SSH 端口和防火墙 |
| 磁盘空间不足 | `df -h` 检查空间 |
| 文件被占用 | 停止相关服务再同步 |

---

## 📚 学习资源

```bash
# 查看帮助
rsync --help

# 查看手册
man rsync

# 在线文档
https://rsync.samba.org/documentation.html

# 中文教程
https://www.ruanyifeng.com/blog/2020/08/rsync.html
```

---

## 💡 速查表

```bash
# 本地复制
rsync -a /source/ /backup/

# 远程同步
rsync -avz /source/ user@remote:/destination/

# 带进度
rsync -avzP /source/ user@remote:/destination/

# 排除文件
rsync -avz --exclude='*.log' /source/ /backup/

# 测试运行
rsync -avzn /source/ /backup/

# 完全同步
rsync -avz --delete /source/ user@remote:/destination/

# 指定端口
rsync -avz -e "ssh -p 2222" /source/ user@remote:/destination/
```

---

## 🎯 总结

> **rsync = 智能的文件复制工具，只传变化的部分，本地远程都能用。**

**核心优势**：
- ✅ 第一次全量，之后增量
- ✅ 速度快，省流量
- ✅ 支持 SSH 加密
- ✅ 保留文件属性
- ✅ 可排除特定文件

**一句话**：任何文件复制/同步场景，优先考虑 rsync！🚀

---

## 🔗 相关链接

- 官方网站：https://rsync.samba.org
- GitHub: https://github.com/WayneD/rsync
- 阮一峰教程：https://www.ruanyifeng.com/blog/2020/08/rsync.html
