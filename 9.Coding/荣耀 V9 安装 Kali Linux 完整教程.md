# 荣耀 V9 安装 Kali Linux 完整教程 - LinuxDeploy 方案

**创建日期**:: 2026-02-23  
**设备**:: 荣耀 V9 (Honor V9)  （需 Root）
**系统**:: Kali Linux on Android  
**方案**:: LinuxDeploy（无需 Root）  
**难度**:: ⭐⭐ 中等  
**标签**:: #Kali #LinuxDeploy #安卓 #荣耀V9 #网络安全

---

## 📱 设备要求

| 硬件 | 荣耀 V9 规格 | 是否满足 |
|------|-------------|----------|
| **CPU** | 麒麟 960 (8 核) | ✅ 足够 |
| **内存** | 4/6GB | ✅ 足够 |
| **存储** | 64/128GB | ✅ 足够 |
| **电池** | 4000mAh | ✅ 还行 |
| **USB** | Type-C (支持 OTG) | ✅ 可接外设 |

---

## 🎯 方案概述

```
┌─────────────────────────────────────────────────┐
│  LinuxDeploy 方案特点                           │
├─────────────────────────────────────────────────┤
│ ⚠️ 需 Root 权限                                │
│ ✅ 完整 Kali Linux 环境                         │
│ ✅ 100+ 安全工具                                 │
│ ✅ 支持图形界面（XFCE 桌面）                     │
│ ✅ 可外接 USB 网卡做 WiFi 攻击（需要 Root）       │
│ ⚠️ 资源占用：内存 1-2GB，存储 6-8GB             │
└─────────────────────────────────────────────────┘
```

---

## 🏗️ 架构原理解析

### 整体架构图

```
┌─────────────────────────────────────────────────────────┐
│                    荣耀 V9 手机                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────┐      ┌─────────────────────┐      │
│  │  LinuxDeploy    │      │   VNC Viewer        │      │
│  │                 │      │                     │      │
│  │  ┌───────────┐  │      │  ┌──────────────┐  │      │
│  │  │ Kali      │  │      │  │  图形界面    │  │      │
│  │  │ Linux     │  │      │  │  客户端      │  │      │
│  │  │ 系统      │  │      │  │              │  │      │
│  │  │ (后端)    │  │      │  │              │  │      │
│  │  └─────┬─────┘  │      │  └──────┬───────┘  │      │
│  │        │        │      │         │          │      │
│  │  ┌─────▼─────┐  │      │  ┌──────▼───────┐  │      │
│  │  │ VNC Server│◄─┼──────┼─►│ VNC Client   │  │      │
│  │  │ :5900     │  │      │  │ localhost    │  │      │
│  │  └───────────┘  │      │  └──────────────┘  │      │
│  │                 │      │                     │      │
│  └─────────────────┘      └─────────────────────┘      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 组件职责

| 组件 | 角色 | 职责 | 类比 |
|------|------|------|------|
| **LinuxDeploy** | 后端服务 | 创建容器、运行 Kali、启动 VNC Server | 云服务器提供商 |
| **Kali 镜像** | 操作系统 | 提供黑客工具和环境 | 云服务器系统 |
| **VNC Server** | 服务端 | 监听 5900 端口、发送屏幕图像 | 远程桌面服务 |
| **VNC Viewer** | 客户端 | 连接 Server、显示桌面、发送操作 | 远程桌面客户端 |

### 为什么这样设计？

**原因 1：安卓系统限制**
```
安卓不允许：
❌ 直接运行 Linux 二进制
❌ 直接显示其他系统的 GUI
❌ 直接访问底层硬件

所以需要：
✅ chroot 容器隔离
✅ VNC 协议传输图像
✅ 客户端应用显示
```

**原因 2：性能优化**
```
分离设计的好处：
✅ LinuxDeploy 专注系统运行
✅ VNC Viewer 专注图像显示
✅ 可以替换其他客户端（SSH/Terminal）
✅ 降低资源占用
```

### chroot 环境是什么？

```
chroot = "change root"（改变根目录）

正常安卓：
/
├── system/
├── data/
└── sdcard/

chroot 后（Kali）：
/sdcard/kali.img  ← 虚拟的根目录
├── bin/
├── usr/
├── home/kali/
└── ...

在 Kali 里看：
/  ← 实际是 /sdcard/kali.img
```

**效果：**
- Kali 认为自己运行在独立的 Linux 系统
- 实际是安卓上的"容器"
- 共享安卓内核，但用户空间隔离

### VNC 协议工作原理

```
┌─────────────┐         ┌─────────────┐
│ VNC Server  │         │ VNC Client  │
│ (Kali 里)    │         │ (Viewer)    │
└──────┬──────┘         └──────┬──────┘
       │                       │
       │  1. 客户端连接        │
       │──────────────────────►│
       │                       │
       │  2. 发送屏幕图像      │
       │◄──────────────────────│
       │   (压缩的像素数据)     │
       │                       │
       │  3. 发送操作指令      │
       │──────────────────────►│
       │   (鼠标/键盘事件)     │
       │                       │
       │  4. 更新屏幕          │
       │◄──────────────────────│
       │                       │
       │  持续循环 2-4 步       │
```

**关键特性：**
- 只传输**变化的像素**（高效）
- 压缩算法（RRE/Hextile/ZRLE）
- 本地渲染（Client 端显示）

### 其他连接方式对比

| 连接方式 | 图形界面 | 资源占用 | 速度 | 适用场景 |
|----------|----------|----------|------|----------|
| **VNC Viewer** | ✅ 完整桌面 | 中等 | 中等 | 新手/图形工具 |
| **SSH** | ❌ 命令行 | 低 | 快 | 老手/脚本 |
| **NoVNC** | ✅ 网页版 | 中等 | 中等 | 临时使用 |
| **内置终端** | ❌ 命令行 | 低 | 快 | 快速操作 |

**SSH 连接示例：**
```bash
# 在 Kali 中安装 SSH
apt install openssh-server

# 用手机终端应用连接（ConnectBot / Termux）
ssh kali@localhost -p 22
```

**NoVNC 浏览器访问：**
```bash
# 在 Kali 中安装
apt install novnc

# 手机浏览器访问
http://localhost:6080
```

---

## 💡 类比理解

**就像云服务器：**
```
阿里云 ECS（LinuxDeploy + Kali）
    ↓
开放 3389 端口（VNC Server）
    ↓
Windows 远程桌面连接（VNC Viewer）
    ↓
操作服务器
```

**就像虚拟机：**
```
VMware（LinuxDeploy）
    ↓
运行 Windows（Kali）
    ↓
虚拟机窗口（VNC Viewer）
    ↓
操作 Windows
```

---

## 📦 准备工作

### 1️⃣ 下载必备应用

| 应用              | 用途         | 下载方式             |
| --------------- | ---------- | ---------------- |
| **LinuxDeploy** | 部署 Kali 系统 | Play 商店 / GitHub |
| **VNC Viewer**  | 远程桌面连接     | Play 商店          |
| **终端模拟器**       | 命令行操作      | Play 商店          |

### 2️⃣ 下载地址

```bash
# LinuxDeploy（GitHub 最新版）
https://github.com/meefik/linuxdeploy/releases

# VNC Viewer（RealVNC 官方）
https://play.google.com/store/apps/details?id=com.realvnc.viewer.android

# 终端模拟器（Jackpal）
https://play.google.com/store/apps/details?id=jackpal.androidterm
```

### 3️⃣ 手机准备

```
✅ 确保存储空间 ≥10GB 空闲
✅ 确保电量 ≥50%（建议插电）
✅ 连接稳定 WiFi（下载约 2GB）
✅ 开启"未知来源应用"安装权限
✅ 开启"开发者选项"（可选）
```

---

## 🔧 详细安装步骤

### 第 1 步：安装 LinuxDeploy

```
1. 下载 LinuxDeploy APK（从 GitHub 或 Play 商店）
2. 安装应用
3. 打开应用，授予权限：
   - 存储权限 ✅
   - 网络权限 ✅
   - 其他权限 ✅
```

### 第 2 步：配置 LinuxDeploy

**打开 LinuxDeploy → 点击右下角"设置"图标**

```
┌─────────────────────────────────────────────┐
│ 基础配置                                    │
├─────────────────────────────────────────────┤
│ 发行版 (Distribution): Kali Linux           │
│ 架构 (Architecture): arm64                  │
│ 源地址 (Source path):                       │
│   http://http.kali.org/kali                 │
│ 镜像路径 (Image path):                      │
│   /sdcard/kali.img                          │
│ 镜像大小 (Image size): 8192 MB (8GB)        │
│ 用户名称 (Username): kali                   │
│ 用户密码 (Password): kali                   │
│   ⚠️ 记住这个密码！后面要用                 │
└─────────────────────────────────────────────┘
```

```
┌─────────────────────────────────────────────┐
│ 桌面环境配置                                │
├─────────────────────────────────────────────┤
│ 桌面环境 (Desktop environment): XFCE        │
│ 分辨率 (Resolution): 1280x720               │
│   （适合手机屏幕，也可设 1920x1080）         │
│ 颜色深度 (Color depth): 24                  │
│ DPI: 160                                    │
└─────────────────────────────────────────────┘
```

```
┌─────────────────────────────────────────────┐
│ 性能配置（根据荣耀 V9 优化）                 │
├─────────────────────────────────────────────┤
│ CPU 核心数：4                               │
│   （麒麟 960 有 8 核，留 4 核给安卓系统）      │
│ 内存大小：2048 MB                           │
│   （V9 有 4/6GB，分配 2GB 给 Kali）           │
│ 交换文件：512 MB                            │
│   （防止内存不足）                           │
└─────────────────────────────────────────────┘
```

```
┌─────────────────────────────────────────────┐
│ 其他配置                                    │
├─────────────────────────────────────────────┤
│ 本地化 (Locale): en_US.UTF-8                │
│ 时区 (Timezone): Asia/Shanghai              │
│ 启动类型 (Init type): SysVinit              │
│ 端口 (Port): 5900（VNC 默认端口）           │
└─────────────────────────────────────────────┘
```

### 第 3 步：开始部署

```
1. 返回 LinuxDeploy 主界面
2. 点击右上角"..."菜单
3. 选择"部署 (Deploy)"
4. 确认配置 → 点击"确定"
5. 开始下载和安装（约 30-60 分钟）
```

**部署过程：**
```
┌─────────────────────────────────────────────┐
│ 部署进度                                    │
├─────────────────────────────────────────────┤
│ 1. 下载基础系统（约 10 分钟）                 │
│ 2. 解压镜像（约 5 分钟）                     │
│ 3. 配置软件源（约 2 分钟）                   │
│ 4. 安装 XFCE 桌面（约 10 分钟）               │
│ 5. 安装 Kali 工具（约 15-30 分钟）            │
│ 6. 最终配置（约 3 分钟）                     │
└─────────────────────────────────────────────┘
```

**等待提示：**
```
✅ 部署完成！
点击"启动"按钮运行 Kali
```

### 第 4 步：安装 VNC Viewer

```
1. 从 Play 商店下载 VNC Viewer
2. 打开应用
3. 点击右下角"+"新建连接
4. 配置连接：
   ┌─────────────────────────────────┐
   │ 地址 (Address): localhost:5900  │
   │ 名称 (Name): Kali Linux         │
   │ 用户名 (Username): kali         │
   │ 密码 (Password): kali           │
   └─────────────────────────────────┘
5. 点击右上角"✓"保存
6. 点击连接名称进入 Kali 桌面
```

### 第 5 步：首次进入 Kali

```
✅ 成功！你现在看到了 XFCE 桌面

界面说明：
- 顶部：状态栏 + 应用菜单
- 左侧：快速启动栏
- 桌面：右键菜单
- 终端：点击终端图标打开
```

---

## 🛠️ 基础配置

### 1. 更新软件源

```bash
# 打开终端，运行：
sudo su
kali

# 更换国内源（更快）
echo "deb https://mirrors.aliyun.com/kali kali-rolling main non-free contrib" > /etc/apt/sources.list

# 更新系统
apt update && apt upgrade -y
```

### 2. 安装常用工具

```bash
# 基础工具包
apt install -y kali-linux-core

# 网络扫描
apt install -y nmap netcat-traditional wireshark

# 密码破解
apt install -y hydra john hashcat

# Web 渗透
apt install -y sqlmap nikto burpsuite

# WiFi 攻击
apt install -y aircrack-ng reaver pixiewps

# 其他工具
apt install -y metasploit-framework git python3-pip
```

### 3. 中文支持（可选）

```bash
# 安装中文语言包
apt install -y kali-linux-l10n zh_CN.UTF-8

# 配置中文
echo "LANG=zh_CN.UTF-8" >> ~/.bashrc
source ~/.bashrc
```

---

## 📡 WiFi 攻击配置

### 外接 USB 网卡

**需要设备：**
- USB OTG 转接线（Type-C 转 USB-A）
- 支持监听模式的网卡：
  - ALFA AWUS036NHA（推荐）
  - TP-Link TL-WN722N v1
  - 任何 Atheros AR9271 芯片网卡

**连接步骤：**
```
1. 手机开启 OTG 功能（部分手机需要）
2. 插入 USB 网卡
3. 在 LinuxDeploy 中运行：

# 查看网卡
ifconfig -a

# 应该看到 wlan0 或 wlan1

# 开启监听模式
airmon-ng start wlan0

# 扫描 WiFi
airodump-ng wlan0mon
```

**⚠️ 注意：**
- 荣耀 V9 可能需要 Root 才能识别外接网卡
- 部分网卡驱动需要手动编译

---

## ⚙️ 性能优化

### 减少资源占用

```bash
# 1. 降低 XFCE 特效
设置 → 窗口管理器微调 → 关闭"显示阴影"

# 2. 减少启动服务
systemctl disable bluetooth
systemctl disable NetworkManager-wait-online

# 3. 清理缓存
apt clean
apt autoremove -y

# 4. 调整 LinuxDeploy 配置
- CPU 核心数：2（更省电）
- 内存：1024 MB（如果卡顿再调高）
```

### 提高运行速度

```bash
# 1. 使用轻量级桌面
# 将 XFCE 改为 LXDE（更轻量）
apt install -y lxde

# 2. 关闭不必要的视觉效果
# 设置 → 外观 → 样式 → 选择"简洁"

# 3. 使用命令行模式（无桌面）
# 在 LinuxDeploy 配置中设置：
# 桌面环境：none
# 然后用 SSH 连接
```

---

## 🔌 常用操作

### 启动/停止 Kali

```
在 LinuxDeploy 主界面：
- 点击"启动" → 运行 Kali
- 点击"停止" → 关闭 Kali
- 长按"启动" → 重启 Kali
```

### 连接方式

| 方式 | 命令 | 用途 |
|------|------|------|
| **VNC 桌面** | localhost:5900 | 图形界面操作 |
| **SSH** | ssh kali@localhost -p 22 | 命令行远程 |
| **终端** | 直接打开终端应用 | 本地命令行 |

### 文件传输

```bash
# Kali 访问安卓存储
cd /sdcard/

# 安卓访问 Kali 文件
# 需要 Root，路径：/data/data/ru.meefik.linuxdeploy/files/
```

---

## 🐛 常见问题

### Q1: 部署失败/卡住

**原因：** 网络问题或存储不足

**解决：**
```bash
# 1. 检查存储空间（需要≥10GB）
# 2. 更换软件源（用阿里云）
# 3. 重启手机重试
# 4. 删除旧镜像重新部署
rm /sdcard/kali.img
```

### Q2: VNC 连接失败

**原因：** Kali 未启动或端口错误

**解决：**
```bash
# 1. 确保 LinuxDeploy 显示"运行中"
# 2. 检查端口是否正确（默认 5900）
# 3. 重启 Kali 服务
# 4. 查看日志：
tail -f /sdcard/kali.log
```

### Q3: 运行卡顿

**原因：** 资源分配不足

**解决：**
```bash
# 1. 在 LinuxDeploy 中增加内存到 2048MB
# 2. 减少 CPU 核心数到 2-4 核
# 3. 关闭 XFCE 特效
# 4. 改用 LXDE 桌面
```

### Q4: 外接网卡不识别

**原因：** 需要 Root 或驱动不支持

**解决：**
```bash
# 1. 检查手机是否 Root
# 2. 尝试其他网卡型号
# 3. 手动编译驱动（高级）
# 4. 用 Mac/PC 虚拟机代替
```

### Q5: 耗电太快

**原因：** Kali 后台运行

**解决：**
```bash
# 1. 不用时停止 Kali（在 LinuxDeploy 点"停止"）
# 2. 减少 CPU 核心数
# 3. 降低屏幕亮度
# 4. 启用省电模式
```

---

## 📊 资源占用监控

### 查看资源使用

```bash
# 在 Kali 终端运行：

# 查看内存
free -h

# 查看 CPU
top

# 查看存储
df -h

# 查看进程
ps aux
```

### 荣耀 V9 实际占用

| 状态 | 内存 | CPU | 存储 |
|------|------|-----|------|
| **空闲** | ~1.2GB | 5% | 6GB |
| **运行工具** | ~1.5GB | 15% | 6GB |
| **扫描攻击** | ~1.8GB | 40% | 6GB |
| **多任务** | ~2.2GB | 60% | 7GB |

---

## 🎓 学习路线建议

### 第 1 周：熟悉环境

```
- 安装 LinuxDeploy + Kali
- 熟悉 XFCE 桌面
- 学习基础 Linux 命令
- 更新系统 + 安装工具
```

### 第 2 周：网络扫描

```
- 学习 nmap 使用
- 网络拓扑发现
- 端口扫描技术
- 服务识别
```

### 第 3 周：密码破解

```
- hydra 暴力破解
- hashcat GPU 加速
- 字典制作
- 社会工程学
```

### 第 4 周：Web 渗透

```
- sqlmap SQL 注入
- nikto 网站扫描
- burpsuite 抓包
- XSS/CSRF 攻击
```

### 第 5 周：WiFi 攻防（需要外接网卡）

```
- aircrack-ng 套件
- WPA/WPA2 破解
- PMKID 攻击
- 中间人攻击
```

---

## ⚠️ 法律警告

> **仅限学习和授权测试使用！**
>
> - ✅ 破解自己的网络 = 合法
> - ✅ 授权渗透测试 = 合法（需书面授权）
> - ❌ 破解他人网络 = **违法行为**
> - ❌ 未授权攻击 = 可能面临刑事责任
>
> **遵守《网络安全法》，做合法的安全研究员！**

---

## 📚 延伸阅读

- [[Kali Linux 工具大全]]
- [[WiFi 破解原理 - 通俗讲解]]
- [[Termux 黑客工具安装]]
- [[网络安全学习路线]]
- [[渗透测试方法论]]

---

## 🔗 相关资源

| 资源 | 链接 |
|------|------|
| **LinuxDeploy 官网** | https://github.com/meefik/linuxdeploy |
| **Kali 官方文档** | https://www.kali.org/docs/ |
| **NetHunter 支持设备** | https://www.kali.org/docs/nhunter/nhunter-devices/ |
| **XDA 荣耀 V9 论坛** | https://forum.xda-developers.com/c/honor-8-pro.6633/ |

---

*教程版本：v1.0 | 最后更新：2026-02-23 | 设备：荣耀 V9*
