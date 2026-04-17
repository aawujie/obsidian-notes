# Homebrew Services 完全指南

## 📅 基本信息

- **创建日期**: 2026-02-25
- **用途**: 管理 macOS 后台服务
- **工具**: Homebrew services 命令
- **适用**: PostgreSQL, Redis, MySQL, Nginx 等

---

## 🎯 什么是 Homebrew Services

**Homebrew Services** 是 Homebrew 的扩展命令，用于管理 macOS 的后台服务。

**作用**:
- ✅ 启动/停止服务
- ✅ 设置开机自启
- ✅ 查看服务状态
- ✅ 管理 LaunchAgent

---

## 📦 安装 Homebrew Services

```bash
# Homebrew 自带，无需单独安装
# 如果找不到命令，更新 Homebrew
brew update
```

---

## 🚀 常用命令速查

### 查看所有服务

```bash
# 列出所有服务状态
brew services list

# 输出示例：
# Name          Status User  File
# postgresql@15 started apple ~/Library/LaunchAgents/homebrew.mxcl.postgresql@15.plist
# redis         none
# nginx         started root  /Library/LaunchDaemons/homebrew.mxcl.nginx.plist
```

**状态说明**:

| 状态 | 说明 |
|------|------|
| `started` | 正在运行 |
| `stopped` | 已停止 |
| `none` | 未安装/未配置 |
| `error` | 出错 |

---

### 启动服务

```bash
# 启动服务（立即 + 开机自启）
brew services start <服务名>

# 示例
brew services start postgresql@15
brew services start redis
brew services start mysql
brew services start nginx
```

**效果**:
- ✅ 立即启动服务
- ✅ 创建 LaunchAgent
- ✅ 开机自动启动

---

### 停止服务

```bash
# 停止服务（但保留配置）
brew services stop <服务名>

# 示例
brew services stop postgresql@15
brew services stop redis
```

**效果**:
- ✅ 停止运行进程
- ✅ 移除 LaunchAgent
- ❌ 不开机自启
- ✅ 保留安装

---

### 重启服务

```bash
# 重启服务
brew services restart <服务名>

# 示例
brew services restart postgresql@15
```

**效果**:
- ✅ 先停止再启动
- ✅ 重新加载配置

---

### 查看服务信息

```bash
# 查看服务详细信息
brew info <服务名>

# 示例
brew info postgresql@15
brew info redis
```

**输出包含**:
- 版本号
- 安装位置
- 配置文件路径
- 数据目录
- 依赖项

---

## 📋 完整示例：PostgreSQL 管理

### 1. 安装 PostgreSQL

```bash
brew install postgresql@15
```

### 2. 启动服务

```bash
brew services start postgresql@15
```

### 3. 检查状态

```bash
brew services list
# 应该显示：postgresql@15 started
```

### 4. 连接数据库

```bash
# 使用 psql 连接
/opt/homebrew/opt/postgresql@15/bin/psql -h localhost -U <用户名>
```

### 5. 停止服务

```bash
brew services stop postgresql@15
```

### 6. 重新启动（需要时）

```bash
brew services start postgresql@15
```

---

## 📋 完整示例：Redis 管理

### 1. 安装 Redis

```bash
brew install redis
```

### 2. 启动服务

```bash
brew services start redis
```

### 3. 检查状态

```bash
brew services list
# 应该显示：redis started
```

### 4. 测试连接

```bash
redis-cli ping
# 应该返回：PONG
```

### 5. 停止服务

```bash
brew services stop redis
```

---

## 🔧 高级用法

### 以 root 用户启动（系统级服务）

```bash
# 需要管理员权限，服务对所有用户可用
sudo brew services start nginx
```

**区别**:
| 类型 | 命令 | 位置 | 权限 |
|------|------|------|------|
| **用户级** | `brew services start` | `~/Library/LaunchAgents/` | 当前用户 |
| **系统级** | `sudo brew services start` | `/Library/LaunchDaemons/` | 所有用户 |

---

### 清理服务配置

```bash
# 清理所有已停止服务的配置
brew services cleanup
```

**作用**:
- 删除不再需要的 LaunchAgent 文件
- 清理残留配置

---

### 导出服务配置

```bash
# 查看 LaunchAgent 文件位置
brew services list | grep <服务名>

# 文件位置示例：
# ~/Library/LaunchAgents/homebrew.mxcl.postgresql@15.plist
```

---

## 📊 常见服务管理

### 数据库服务

```bash
# PostgreSQL
brew services start postgresql@15
brew services stop postgresql@15
brew services restart postgresql@15

# MySQL
brew services start mysql
brew services stop mysql

# MongoDB
brew services start mongodb-community
brew services stop mongodb-community

# Redis
brew services start redis
brew services stop redis
```

### Web 服务器

```bash
# Nginx
sudo brew services start nginx
sudo brew services stop nginx

# Apache
sudo brew services start httpd
sudo brew services stop httpd

# PHP
brew services start php
brew services stop php
```

### 其他服务

```bash
# Elasticsearch
brew services start elasticsearch

# RabbitMQ
brew services start rabbitmq

# Memcached
brew services start memcached
```

---

## 🔍 故障排查

### 问题 1：服务启动失败

```bash
# 查看详细日志
brew services info <服务名>

# 查看系统日志
tail -f /usr/local/var/log/<服务名>.log

# PostgreSQL 日志示例
tail -f /opt/homebrew/var/log/postgresql@15.log
```

---

### 问题 2：服务状态显示 error

```bash
# 停止服务
brew services stop <服务名>

# 清理配置
brew services cleanup

# 重新启动
brew services start <服务名>
```

---

### 问题 3：权限问题

```bash
# 用户级服务（推荐）
brew services start <服务名>

# 系统级服务（需要 sudo）
sudo brew services start <服务名>

# 修复权限
sudo chown -R $(whoami) /opt/homebrew/*
```

---

### 问题 4：端口被占用

```bash
# 查看端口占用
lsof -i :<端口号>

# PostgreSQL 默认端口 5432
lsof -i :5432

# Redis 默认端口 6379
lsof -i :6379

# 杀死占用端口的进程
kill -9 <PID>
```

---

## 📁 重要文件位置

### macOS 用户级服务

```
~/Library/LaunchAgents/
└── homebrew.mxcl.<服务名>.plist
```

### macOS 系统级服务

```
/Library/LaunchDaemons/
└── homebrew.mxcl.<服务名>.plist
```

### Homebrew 服务配置

```
/opt/homebrew/opt/<服务名>/
├── bin/          # 可执行文件
├── lib/          # 库文件
├── etc/          # 配置文件
└── var/          # 数据目录
```

---

## 💡 最佳实践

### 1. 优先使用用户级服务

```bash
# ✅ 推荐（不需要 sudo）
brew services start redis

# ❌ 避免（除非必须）
sudo brew services start redis
```

**原因**:
- 更安全
- 不需要管理员权限
- 不影响其他用户

---

### 2. 定期清理

```bash
# 每月清理一次
brew services cleanup
```

---

### 3. 记录服务配置

```bash
# 导出当前服务状态
brew services list > ~/Documents/brew-services-backup.txt

# 记录配置文件位置
brew services list | grep started | awk '{print $3}'
```

---

### 4. 开机自启管理

```bash
# 查看开机自启服务
brew services list | grep started

# 禁用开机自启（但保持运行）
brew services stop <服务名>
# 然后手动启动
/opt/homebrew/opt/<服务名>/bin/<服务名>
```

---

## 📝 常用命令速查表

| 命令 | 说明 | 示例 |
|------|------|------|
| `list` | 列出所有服务 | `brew services list` |
| `start` | 启动服务 | `brew services start redis` |
| `stop` | 停止服务 | `brew services stop redis` |
| `restart` | 重启服务 | `brew services restart redis` |
| `info` | 查看服务信息 | `brew services info redis` |
| `cleanup` | 清理配置 | `brew services cleanup` |

---

## 🆚 与其他管理方式对比

| 方式 | 优点 | 缺点 |
|------|------|------|
| **brew services** | ✅ 简单，集成 Homebrew | ⚠️ 仅限 Homebrew 安装的服务 |
| **手动启动** | ✅ 完全控制 | ❌ 每次都要手动 |
| **LaunchAgent** | ✅ 系统原生 | ❌ 配置复杂 |
| **Docker** | ✅ 隔离环境 | ❌ 资源占用大 |

---

## 🔗 相关资源

- **Homebrew 官网**: https://brew.sh
- **Homebrew Services GitHub**: https://github.com/Homebrew/homebrew-services
- **macOS LaunchAgent 文档**: https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPSystemStartup/

---

## 📋 实际案例：Medusa 电商系统

### 启动依赖服务

```bash
# 启动 PostgreSQL
brew services start postgresql@15

# 启动 Redis
brew services start redis

# 检查状态
brew services list

# 输出：
# postgresql@15 started
# redis started
```

### 停止服务（不使用）

```bash
# 停止 PostgreSQL
brew services stop postgresql@15

# 停止 Redis
brew services stop redis

# 检查状态
brew services list

# 输出：
# postgresql@15 none
# redis none
```

### 重新启动（需要时）

```bash
# 需要时随时启动
brew services start postgresql@15
brew services start redis
```

---

## ✅ 检查清单

- [ ] 理解 brew services 的作用
- [ ] 掌握 start/stop/restart 命令
- [ ] 知道如何查看服务状态
- [ ] 了解用户级 vs 系统级服务
- [ ] 学会故障排查方法
- [ ] 知道重要文件位置
- [ ] 备份服务配置

---

## 💡 经验总结

1. **优先用户级服务** - 不需要 sudo
2. **定期清理** - 避免配置堆积
3. **记录配置** - 方便恢复
4. **查看日志** - 快速定位问题
5. **按需启动** - 不用的服务及时停止

---

## 🎯 快速参考

```bash
# 一句话总结
brew services start <服务名>  # 启动
brew services stop <服务名>   # 停止
brew services list            # 查看状态
```

**记住这三个命令就够了！** 🎉
