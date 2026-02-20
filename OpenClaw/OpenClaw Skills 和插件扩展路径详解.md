# OpenClaw Skills 和插件扩展路径详解

> 创建时间：2026-02-19  
> 标签：#OpenClaw #Skills #Plugins #配置

---

## 📊 核心概念对比

| 类型 | 全局 | 用户级 | 工作空间 |
|------|------|--------|----------|
| **Skills（技能）** | ✅ | ❌ | ✅ |
| **Extensions（插件）** | ✅ | ✅ | ❌ |

---

## 📁 路径总览

### Skills（技能）

```
全局 Skills:  /opt/homebrew/lib/node_modules/openclaw/skills/
              └── 54 个内置 Skills（weather, github, discord 等）

工作空间 Skills: /Users/apple/clawd/skills/
                 └── 项目专属 Skills（如 obsidian）
```

### Extensions（插件/扩展）

```
全局 Extensions: /opt/homebrew/lib/node_modules/openclaw/extensions/
                 └── 内置扩展（只读，默认禁用）

用户级 Extensions: ~/.openclaw/extensions/
                   └── 用户安装的插件（如 feishu）

工作空间 Extensions: <workspace>/.openclaw/extensions/
                     └── 工作空间专属扩展（较少用）
```

---

## 🔍 详细说明

### 1️⃣ Skills（技能）

**特点：**
- 提供具体任务能力（天气查询、GitHub 操作、PDF 编辑等）
- 每个 Skill 有独立的 `SKILL.md` 说明文件
- 分为 **全局** 和 **工作空间** 两级

**全局 Skills：**
```bash
/opt/homebrew/lib/node_modules/openclaw/skills/
├── weather/          # 天气查询
├── github/           # GitHub 操作
├── discord/          # Discord 集成
├── coding-agent/     # 代码代理
├── nano-pdf/         # PDF 编辑
└── ... (共 54 个)
```

**工作空间 Skills：**
```bash
/Users/apple/clawd/skills/
└── obsidian/         # 仅当前工作空间可用
    ├── SKILL.md
    ├── _meta.json
    └── .clawhub/
```

**<span style="color:rgb(255, 77, 77)">设计原因：</span>**
- 不同项目可能需要不同的 Skills
- <span style="color:rgb(255, 77, 77)">项目隔离，便于版本控制</span>
- <span style="color:rgb(255, 77, 77)">可随项目一起 Git 提交</span>

---

### 2️⃣ Extensions（插件/扩展）

**特点：**
- 底层功能扩展（消息渠道、认证模块、系统功能）
- TypeScript 模块，运行时加载
- 分为 **全局** 和 **用户级** 两级

**全局 Extensions（内置，只读）：**
```bash
/opt/homebrew/lib/node_modules/openclaw/extensions/
├── telegram/         # Telegram 集成
├── discord/          # Discord 集成
├── qwen-portal-auth/ # Qwen 认证
└── ... (官方内置)
```

⚠️ **注意：** <span style="color:rgb(255, 77, 77)">全局路径用户<b>无法写入</b>，只能 OpenClaw 官方管理</span>

**用户级 Extensions（用户安装）：**
```bash
~/.openclaw/extensions/
└── feishu/           # 飞书插件（用户安装）
    ├── index.ts
    ├── package.json
    ├── node_modules/
    ├── skills/
    └── openclaw.plugin.json
```

**安装命令：**
```bash
# 从 npm 安装
openclaw plugins install @m1heng-clawd/feishu

# 安装到：~/.openclaw/extensions/feishu/

# 查看已安装插件
openclaw plugins list

# 启用/禁用插件
openclaw plugins enable <id>
openclaw plugins disable <id>
```

<span style="color:rgb(255, 77, 77)"><b>设计原因：</b></span>
- <span style="color:rgb(195, 117, 255)">不需要 `sudo` 权限</span>
- 用户级别隔离，不影响其他用户
- <span style="color:rgb(195, 117, 255)">重装 OpenClaw 时插件不受影响</span>
- 配置和代码分离

---

## 📖 插件加载顺序（优先级从高到低）

根据官方文档，OpenClaw 加载插件的顺序：

```
1. Config paths
   plugins.load.paths (自定义路径)

2. Workspace extensions
   <workspace>/.openclaw/extensions/*.ts
   <workspace>/.openclaw/extensions/*/index.ts

3. Global extensions (用户级)
   ~/.openclaw/extensions/*.ts
   ~/.openclaw/extensions/*/index.ts

4. Bundled extensions (全局，内置)
   <openclaw>/extensions/*
```

**优先级规则：** 如果多个插件有相同 ID，第一个匹配的获胜，后面的被忽略。

---

## 🛠️ 实际操作示例

### 安装飞书插件

```bash
# 安装
openclaw plugins install @m1heng-clawd/feishu

# 安装位置
~/.openclaw/extensions/feishu/

# 配置更新
~/.openclaw/openclaw.json
# plugins.entries.feishu.enabled = true

# 重启 Gateway
openclaw gateway restart
```

### 查看全局 Skills

```bash
ls /opt/homebrew/lib/node_modules/openclaw/skills/
# 输出 54 个内置 Skills
```

### 查看工作空间 Skills

```bash
ls /Users/apple/clawd/skills/
# 输出 obsidian (工作空间专属)
```

### 查看用户级插件

```bash
ls ~/.openclaw/extensions/
# 输出 feishu (用户安装)
```

---

## 📋 配置文件位置

| 配置类型 | 路径 |
|---------|------|
| 用户配置 | `~/.openclaw/openclaw.json` |
| 旧版配置 | `~/.openclaw/clawdbot.json` |
| 插件配置 | `plugins.entries.<id>` |
| 渠道配置 | `channels.<id>` |
| 模型配置 | `models.providers` |

---

## 🌟 重要场景：多 Agent 共享 Skills

### 问题背景

当你有多个 Agent，每个 Agent 有不同的工作空间时：

```
Agent A (main)        → /Users/apple/clawd/
Agent B (manager)     → /Users/apple/clawd-manager/
Agent C (dev-assistant) → /Users/apple/dev-workspace/

需求：安装一个 Skill 让所有 Agent 都能使用
```

### 解决方案对比

| 方案 | 操作 | 优点 | 缺点 | 推荐度 |
|------|------|------|------|--------|
| **全局安装** | 安装到全局 Skills 目录 | 一次安装，所有 Agent 可用 | 可能需要特殊权限 | ⭐⭐⭐⭐⭐ |
| **每个空间安装** | 在每个工作空间分别安装 | 简单直接 | 重复劳动，难维护 | ⭐⭐ |
| **符号链接** | 创建共享目录 + 符号链接 | 灵活，易更新 | 链接可能失效 | ⭐⭐⭐⭐ |

---

### <span style="color:rgb(195, 117, 255)">方案 1：全局安装 Skills（推荐）⭐</span>

**适用场景：** 通用 Skills（如 weather、github、nano-pdf 等）

**安装方法：**

```bash
# 方法 A：使用 ClawHub 全局安装（如果支持）
clawhub install <skill-name> --global

# 方法 B：手动复制到全局目录（需要 sudo）
sudo cp -r /path/to/skill /opt/homebrew/lib/node_modules/openclaw/skills/

# 方法 C：使用 openclaw 命令（如果支持）
openclaw skills install <skill-name> --global
```

**安装位置：**
```
/opt/homebrew/lib/node_modules/openclaw/skills/<skill-name>/
```

**验证：**
```bash
# 检查是否安装成功
ls /opt/homebrew/lib/node_modules/openclaw/skills/<skill-name>/

# 所有 Agent 都应该能访问
```

**优点：**
- ✅ 一次安装，所有 Agent 自动可用
- ✅ 更新时只需更新一次
- ✅ 管理简单，不易出错

**缺点：**
- ⚠️ 可能需要 `sudo` 权限
- ⚠️ 重装 OpenClaw 时可能被覆盖

---

### 方案 2：符号链接方案（灵活）⭐⭐⭐⭐

**适用场景：** 开发中的 Skills、频繁更新的 Skills

**操作步骤：**

```bash
# 1. 创建共享 Skills 目录
mkdir -p ~/openclaw-shared-skills/
cd ~/openclaw-shared-skills/

# 2. 安装 Skill 到共享目录
clawhub install <skill-name>
# 或手动复制 Skill 文件

# 3. 为每个工作空间创建符号链接
ln -s /Users/apple/openclaw-shared-skills/<skill-name> \
      /Users/apple/clawd/skills/<skill-name>

ln -s /Users/apple/openclaw-shared-skills/<skill-name> \
      /Users/apple/clawd-manager/skills/<skill-name>

ln -s /Users/apple/openclaw-shared-skills/<skill-name> \
      /Users/apple/dev-workspace/skills/<skill-name>
```

**验证符号链接：**
```bash
# 检查链接是否有效
ls -la /Users/apple/clawd/skills/<skill-name>
# 应显示：-> /Users/apple/openclaw-shared-skills/<skill-name>

# 测试是否能访问
cat /Users/apple/clawd/skills/<skill-name>/SKILL.md
```

**检查失效链接：**
```bash
find /Users/apple/clawd/skills/ -type l -exec test ! -e {} \; -print
```

**优点：**
- ✅ 只需安装一次
- ✅ 更新时所有工作空间同步生效
- ✅ 便于开发和调试
- ✅ 不需要 sudo 权限

**缺点：**
- ⚠️ 源目录移动会导致链接失效
- ⚠️ Git 版本控制可能有问题
- ⚠️ 需要定期检查链接状态

**最佳实践：**
```bash
# 使用绝对路径（不要用相对路径）
ln -s /Users/apple/openclaw-shared-skills/<skill-name> \
      /Users/apple/clawd/skills/<skill-name>

# 确保源目录位置稳定，不要随意移动
# 放在用户目录下，如 ~/openclaw-shared-skills/

# 在文档中记录符号链接关系
```

---

### 方案 3：每个工作空间分别安装

**适用场景：** 项目专属 Skills、不同版本需求

**操作步骤：**

```bash
# 工作空间 A
cd /Users/apple/clawd/
clawhub install <skill-name>

# 工作空间 B
cd /Users/apple/clawd-manager/
clawhub install <skill-name>

# 工作空间 C
cd /Users/apple/dev-workspace/
clawhub install <skill-name>
```

**优点：**
- ✅ 简单直接
- ✅ 每个空间独立管理
- ✅ 可以安装不同版本

**缺点：**
- ❌ 重复劳动
- ❌ 更新时要更新所有空间
- ❌ 容易忘记某个空间

---

## 🎯 最佳实践建议

| Skill 类型 | 推荐方案 | 原因 |
|-----------|---------|------|
| **通用 Skills** (weather, github, nano-pdf) | 全局安装 | 所有项目都需要，一次安装 |
| **开发中 Skills** | 符号链接 | 便于调试，更新同步 |
| **项目专属 Skills** | 工作空间安装 | 项目隔离，版本独立 |
| **测试/实验 Skills** | 符号链接 | 快速部署，易于清理 |

---

## ⚠️ 常见问题

### Q: 为什么插件不安装到全局路径？

**A:** 
1. 全局路径需要 `sudo` 权限，不方便
2. 用户级更安全，不会影响系统
3. 多用户支持，互不干扰
4. 更新灵活，不需要等系统更新

### Q: Skills 和 Plugins 有什么区别？

**A:**
- **Skills** = 上层应用能力（具体能做什么事）
- **Plugins** = 底层基础设施（管道、连接器）

### Q: 如何彻底卸载插件？

```bash
# 1. 禁用插件
openclaw plugins disable feishu

# 2. 卸载插件
openclaw plugins uninstall feishu

# 3. 手动删除（可选）
rm -rf ~/.openclaw/extensions/feishu

# 4. 重启 Gateway
openclaw gateway restart
```

### Q: 多 Agent 环境下如何管理 Skills？

**A:** 
- **通用 Skills** → 全局安装（推荐）
- **项目专属** → 工作空间安装
- **开发调试** → 符号链接方案

---

## 🔗 相关链接

- [OpenClaw 官方文档](https://docs.openclaw.ai)
- [插件开发指南](https://docs.openclaw.ai/plugins/manifest)
- [ClawHub 技能市场](https://clawhub.com)

---

## 📝 更新日志

- **2026-02-19 22:38**: 新增「多 Agent 共享 Skills」章节，补充三种解决方案对比
- **2026-02-19 22:30**: 初始版本，整理 Skills 和插件扩展路径详解
