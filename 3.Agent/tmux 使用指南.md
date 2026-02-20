# tmux 使用指南

> 创建时间：2026-02-20  
> 标签：#tmux #终端 #CLI #自动化

---

## 📌 什么是 tmux？

**tmux**（Terminal Multiplexer）是一个**终端复用器**，可以：

- 🪟 在一个窗口中运行多个终端会话
- 🔀 在多个会话之间切换
- 📌 让后台进程持续运行（即使关闭终端）
- 🤝 多人共享同一个终端会话

**核心用途：** 管理多个终端会话，让任务在后台持续运行。

---

## 🚀 安装

### macOS（Homebrew）

```bash
brew install tmux
```

### Ubuntu/Debian

```bash
sudo apt install tmux
```

### CentOS/RHEL

```bash
sudo yum install tmux
```

### 验证安装

```bash
tmux -V
```

应该显示版本号，如：
```
tmux 3.3a
```

---

## 🎯 基本概念

### 架构层级

```
Session（会话）
  └── Window（窗口）
        └── Pane（窗格）
```

| 层级 | 说明 |
|------|------|
| **Session** | 独立的终端会话，可以detach/attach |
| **Window** | 会话中的窗口，类似浏览器标签 |
| **Pane** | 窗口中的分屏，可以多个并排 |

---

## 📝 基本使用

### 1️⃣ 创建新会话

```bash
# 创建并命名会话
tmux new-session -s mysession

# 简写
tmux new -s mysession

# 不命名（自动编号）
tmux
```

---

### 2️⃣ 会话管理

```bash
# 列出所有会话
tmux ls

# 连接到已有会话
tmux attach -t mysession

# 简写
tmux a -t mysession

# 删除会话
tmux kill-session -t mysession

# 删除所有会话
tmux kill-server
```

---

### 3️⃣ 后台运行（Detach）

**tmux 的核心功能：** 让会话在后台运行

```bash
# 在会话中，按 Ctrl+B，然后按 D
# 或者
tmux detach
```

**效果：**
- ✅ 会话继续在后台运行
- ✅ 关闭终端也不影响
- ✅ 可以随时重新连接

---

### 4️⃣ 重新连接（Attach）

```bash
# 连接到最近的会话
tmux attach

# 连接到指定会话
tmux attach -t mysession
```

---

## ⌨️ 键盘快捷键

**所有快捷键都以 `Ctrl+B` 开头**

### 会话管理

| 快捷键 | 功能 |
|--------|------|
| `Ctrl+B, D` | 分离会话（detach） |
| `Ctrl+B, S` | 切换会话 |
| `Ctrl+B, $` | 重命名会话 |

---

### 窗口管理

| 快捷键 | 功能 |
|--------|------|
| `Ctrl+B, C` | 创建新窗口 |
| `Ctrl+B, N` | 下一个窗口 |
| `Ctrl+B, P` | 上一个窗口 |
| `Ctrl+B, L` | 切换到最后使用的窗口 |
| `Ctrl+B, W` | 窗口列表 |
| `Ctrl+B, ,` | 重命名窗口 |
| `Ctrl+B, &` | 关闭窗口 |
| `Ctrl+B, 0-9` | 切换到指定窗口 |

---

### 窗格管理

| 快捷键 | 功能 |
|--------|------|
| `Ctrl+B, %` | 垂直分屏（左右） |
| `Ctrl+B, "` | 水平分屏（上下） |
| `Ctrl+B, 方向键` | 切换窗格 |
| `Ctrl+B, X` | 关闭窗格 |
| `Ctrl+B, Z` | 最大化/还原窗格 |
| `Ctrl+B, Q` | 显示窗格编号 |
| `Ctrl+B, {` | 交换窗格（左） |
| `Ctrl+B, }` | 交换窗格（右） |

---

### 其他

| 快捷键 | 功能 |
|--------|------|
| `Ctrl+B, ?` | 快捷键帮助 |
| `Ctrl+B, :` | 命令模式 |
| `Ctrl+B, [` | 滚动模式 |
| `Ctrl+B, ]` | 粘贴缓冲区 |
| `Ctrl+B, T` | 显示时间 |

---

## 🔧 常用命令

### 在 tmux 命令模式下

按 `Ctrl+B, :` 进入命令模式，然后输入：

```bash
# 列出会话
list-sessions

# 列出窗口
list-windows

# 列出窗格
list-panes

# 重命名会话
rename-session newname

# 重命名窗口
rename-window newname

# 设置窗口选项
set-window-option synchronize-panes on
```

---

## 💻 实用场景

### 场景 1：后台运行长任务

```bash
# 1. 创建会话
tmux new-session -s task

# 2. 运行任务
python long_running_script.py

# 3. 分离会话（Ctrl+B, D）
# 任务继续在后台运行

# 4. 稍后重新连接
tmux attach -t task
```

---

### 场景 2：运行多个相关任务

```bash
# 1. 创建会话
tmux new-session -s dev

# 2. 垂直分屏（左边运行服务器，右边编辑代码）
Ctrl+B, %

# 3. 在右边窗格打开编辑器
vim src/app.py

# 4. 在左边窗格运行服务器
npm start

# 5. 随时切换窗格查看输出
Ctrl+B, 方向键
```

---

### 场景 3：监控多个日志

```bash
# 1. 创建会话
tmux new-session -s monitor

# 2. 水平分屏（上下）
Ctrl+B, "

# 3. 再分屏
Ctrl+B, "

# 4. 每个窗格监控不同日志
# 窗格 1: tail -f /var/log/app.log
# 窗格 2: tail -f /var/log/error.log
# 窗格 3: tail -f /var/log/access.log
```

---

### 场景 4：同步输入到多个窗格

```bash
# 1. 创建多个窗格

# 2. 开启同步模式
Ctrl+B, :
set-window-option synchronize-panes on

# 3. 在一个窗格输入，所有窗格都会执行相同命令

# 4. 关闭同步
Ctrl+B, :
set-window-option synchronize-panes off
```

---

## 🤖 自动化脚本

### 基础脚本

```bash
#!/bin/bash

# 创建会话
tmux new-session -d -s mysession

# 运行命令
tmux send-keys -t mysession "cd /path/to/project" Enter
tmux send-keys -t mysession "npm start" Enter

# 等待
sleep 5

# 分屏
tmux split-window -h -t mysession
tmux send-keys -t mysession "vim src/app.py" Enter

# 重新排列窗格
tmux select-layout -t mysession tiled

# 连接到会话
tmux attach -t mysession
```

---

### 自动化运行任务

```bash
#!/bin/bash

SESSION="cursor"
PROJECT="/path/to/project"
TASK="agent '修复所有 lint 错误'"

# 清理旧会话
tmux kill-session -t $SESSION 2>/dev/null || true

# 创建新会话
tmux new-session -d -s $SESSION

# 进入项目目录
tmux send-keys -t $SESSION "cd $PROJECT" Enter
sleep 1

# 运行任务
tmux send-keys -t $SESSION "$TASK" Enter

# 等待任务完成（根据任务调整时间）
sleep 60

# 捕获输出
tmux capture-pane -t $SESSION -p -S -100

# 可选：保持会话以便查看
# tmux attach -t $SESSION

# 或者清理
# tmux kill-session -t $SESSION
```

---

### 捕获输出到文件

```bash
#!/bin/bash

SESSION="task"

tmux new-session -d -s $SESSION
tmux send-keys -t $SESSION "cd /path/to/project" Enter
tmux send-keys -t $SESSION "npm test" Enter

# 等待完成
sleep 30

# 捕获输出到文件
tmux capture-pane -t $SESSION -p -S -1000 > output.txt

# 清理
tmux kill-session -t $SESSION

# 查看结果
cat output.txt
```

---

## 📋 配置文件

### 创建配置文件

```bash
# ~/.tmux.conf
```

---

### 常用配置

```bash
# 修改前缀键为 Ctrl+A（更像 screen）
set -g prefix C-a
unbind C-b
bind C-a send-prefix

# 启用鼠标支持
set -g mouse on

# 设置历史滚动行数
set -g history-limit 10000

# 窗口编号从 1 开始
set -g base-index 1

# 窗格编号从 1 开始
setw -g pane-base-index 1

# 设置状态栏
set -g status-bg colour236
set -g status-fg white
set -g status-left '[#S] '
set -g status-right '%Y-%m-%d %H:%M'

# 自动重命名窗口
setw -g automatic-rename on

# 设置窗口标题
set -g set-titles on
set -g set-titles-string '#T'

# 重新加载配置
bind r source-file ~/.tmux.conf \; display "Config reloaded!"
```

---

### 应用配置

```bash
# 重新加载配置
tmux source-file ~/.tmux.conf
```

---

## 🔍 故障排查

### 问题 1：会话已存在

```bash
# 先删除已有会话
tmux kill-session -t mysession

# 或者使用不同名称
tmux new-session -s mysession2
```

---

### 问题 2：无法连接

```bash
# 列出所有会话
tmux ls

# 检查会话是否存在
tmux has-session -t mysession
```

---

### 问题 3：快捷键不工作

```bash
# 检查是否与其他软件冲突
# 尝试使用命令模式
Ctrl+B, :
list-keys
```

---

## 💡 最佳实践

### 1. 命名规范

```bash
# 使用有意义的名称
tmux new-session -s dev      # 开发
tmux new-session -s prod     # 生产
tmux new-session -s monitor  # 监控
tmux new-session -s task     # 临时任务
```

---

### 2. 会话组织

```bash
# 按项目组织
tmux new-session -s project1
tmux new-session -s project2

# 按用途组织
tmux new-session -s coding
tmux new-session -s logs
tmux new-session -s servers
```

---

### 3. 快速切换

```bash
# 创建别名（~/.zshrc）
alias ta='tmux attach'
alias tl='tmux list-sessions'
alias tk='tmux kill-session -t'

# 使用
ta dev    # 连接到 dev 会话
tl        # 列出会话
tk old    # 删除 old 会话
```

---

### 4. 保存和恢复

```bash
# 使用 tmux-resurrect 插件
# ~/.tmux.conf
set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'tmux-plugins/tmux-resurrect'

# 保存：Ctrl+B, Ctrl+S
# 恢复：Ctrl+B, Ctrl+R
```

---

## 📚 插件推荐

### Tmux Plugin Manager (TPM)

```bash
# 安装 TPM
git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm

# 在 ~/.tmux.conf 中添加
set -g @plugin 'tmux-plugins/tpm'

# 安装插件
Ctrl+B, I
```

---

### 常用插件

| 插件 | 功能 |
|------|------|
| `tmux-plugins/tmux-resurrect` | 保存和恢复会话 |
| `tmux-plugins/tmux-continuum` | 自动保存 |
| `tmux-plugins/tmux-sensible` | 合理默认设置 |
| `tmux-plugins/tmux-copycat` | 搜索增强 |
| `tmux-plugins/tmux-yank` | 复制到系统剪贴板 |

---

## 🎯 实际用例

### 用例 1：远程开发

```bash
# SSH 到服务器
ssh user@server

# 创建 tmux 会话
tmux new-session -s dev

# 开始工作...

# 需要离开时
Ctrl+B, D

# 下次 SSH 上来
tmux attach -t dev

# 继续工作，就像没离开过
```

---

### 用例 2：长时间运行任务

```bash
# 创建会话运行任务
tmux new-session -d -s backup
tmux send-keys -t backup "rsync -av /source /backup" Enter

# 稍后检查进度
tmux attach -t backup

# 或者捕获输出
tmux capture-pane -t backup -p > backup.log
```

---

### 用例 3：多服务器管理

```bash
# 创建会话
tmux new-session -s servers

# 分屏管理多个服务器
tmux split-window -h
tmux split-window -v

# 每个窗格 SSH 到不同服务器
# 窗格 1: ssh server1
# 窗格 2: ssh server2
# 窗格 3: ssh server3

# 开启同步，同时执行命令
Ctrl+B, :
set-window-option synchronize-panes on
```

---

## 📊 命令速查表

### 会话命令

```bash
tmux new-session -s [name]     # 创建会话
tmux attach -t [name]          # 连接会话
tmux ls                        # 列出会话
tmux kill-session -t [name]    # 删除会话
tmux rename-session -t [old] [new]  # 重命名
```

---

### 窗口命令

```bash
tmux new-window -t [session]   # 创建窗口
tmux kill-window -t [window]   # 删除窗口
tmux rename-window -t [window] [name]  # 重命名
tmux list-windows              # 列出窗口
```

---

### 窗格命令

```bash
tmux split-window -h           # 垂直分屏
tmux split-window -v           # 水平分屏
tmux select-pane -t [pane]     # 选择窗格
tmux kill-pane -t [pane]       # 删除窗格
tmux list-panes                # 列出窗格
tmux resize-pane -U/D/L/R [size]  # 调整大小
```

---

### 发送命令

```bash
tmux send-keys -t [session] "command" Enter
tmux capture-pane -t [session] -p -S -[lines]
```

---

## 📚 相关资源

| 资源 | 链接 |
|------|------|
| **tmux 官网** | https://tmux.github.io |
| **GitHub 仓库** | https://github.com/tmux/tmux |
| **使用手册** | `man tmux` |
| **配置示例** | https://github.com/tmux/tmux/wiki |

---

## 💭 类比理解

| 类比 | 说明 |
|------|------|
| **tmux vs 普通终端** | 就像浏览器标签 vs 单个窗口 |
| **Detach/Attach** | 就像暂停/恢复游戏 |
| **Session** | 就像一个工作空间 |
| **Window** | 就像工作空间里的标签页 |
| **Pane** | 就像分屏显示 |

---

## 📝 快速参考

### 安装
```bash
brew install tmux
```

### 创建会话
```bash
tmux new-session -s name
```

### 分离会话
```
Ctrl+B, D
```

### 连接会话
```bash
tmux attach -t name
```

### 列出会话
```bash
tmux ls
```

### 删除会话
```bash
tmux kill-session -t name
```

### 分屏
```
Ctrl+B, %  (垂直)
Ctrl+B, "  (水平)
```

### 切换窗格
```
Ctrl+B, 方向键
```

---

## 📝 更新日志

- **2026-02-20**: 初始版本，整理 tmux 使用指南和自动化脚本
