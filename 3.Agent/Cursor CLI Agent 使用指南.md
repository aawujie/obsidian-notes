# Cursor CLI Agent 使用指南

> 创建时间：2026-02-20  
> 版本：2.1.0  
> 标签：#Cursor #AI #编程 #CLI

---

## 📌 什么是 Cursor Agent？

**Cursor Agent** 是一个基于命令行终端的 AI 编程助手，可以帮你：

- ✍️ 编写代码
- 🔍 审查代码
- 🔄 重构优化
- 🐛 调试问题
- ✅ 生成测试
- 📦 Git 操作
- 📊 代码分析

**本质：** 把 Cursor IDE 的 AI 能力带到终端，适合自动化和 CI/CD 场景。

---

## 🚀 安装

### 方式 1：官方安装（推荐）⭐

```bash
curl https://cursor.com/install -fsS | bash
```

### 方式 2：Homebrew（macOS）

```bash
brew install --cask cursor-cli
```

### 方式 3：手动下载

访问 [cursor.com](https://cursor.com) 下载对应平台的 CLI 工具。

---

### 配置 PATH

```bash
# 添加到 ~/.zshrc
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc

# 重新加载配置
source ~/.zshrc
```

---

### 验证安装

```bash
agent --version
# 或
cursor-agent --version
```

**系统要求：**
- macOS 10.15+（支持 Intel 和 Apple Silicon）
- Linux/Ubuntu
- Windows WSL

---

## 🔐 认证

### 方式 1：浏览器登录（推荐）⭐

```bash
agent login
```

会自动打开浏览器，登录你的 Cursor 账号。

---

### 方式 2：API Key

```bash
# 临时设置
export CURSOR_API_KEY="your_api_key_here"

# 永久设置（~/.zshrc）
echo 'export CURSOR_API_KEY="your_api_key"' >> ~/.zshrc
```

---

### 更新 CLI

```bash
agent update
# 或
agent upgrade
```

---

## 💻 使用方式

### 1️⃣ 交互式模式（最常用）⭐

```bash
agent
```

进入交互式对话界面，可以持续交流。

**示例对话：**
```
$ agent
┌─────────────────────────────────────┐
│  Cursor Agent                       │
└─────────────────────────────────────┘

> 帮我给这个 API 添加错误处理
```

---

### 带初始指令启动

```bash
agent "帮我检查这个文件的 bug"
```

---

### 2️⃣ 非交互式模式（CI/CD）

```bash
# 执行任务后退出
agent -p "运行测试并报告覆盖率"

# 强制模式（自动应用更改，无需确认）
agent -p "修复所有 lint 错误" --force

# JSON 输出（适合程序处理）
agent -p "查找 bug" --output-format json

# 流式 JSON 输出
agent -p "运行测试" --output-format stream-json --stream-partial-output
```

---

## 🎯 常用命令

### 模型管理

```bash
# 列出所有可用模型
agent models
# 或
agent --list-models

# 使用特定模型
agent --model gpt-5

# 在交互式会话中切换
/models
```

**可用模型：**
- `gpt-4`
- `gpt-5`
- `claude-3.5-sonnet`
- `claude-3.7-sonnet`
- `cursor-fast`
- `cursor-small`

---

### 会话管理

```bash
# 列出所有会话
agent ls

# 恢复最近的会话
agent resume

# 恢复特定会话
agent --resume="[chat-id]"
```

---

### 上下文选择

在交互式会话中，可以指定文件/文件夹作为上下文：

```
@filename.ts
@src/components/
@package.json
```

**示例：**
```bash
agent
> @src/api/user.ts 分析这个文件的代码结构
```

---

### 斜杠命令（交互式会话中）

| 命令 | 功能 |
|------|------|
| `/models` | 切换 AI 模型 |
| `/compress` | 压缩对话历史，释放上下文窗口 |
| `/rules` | 创建/编辑项目规则 |
| `/commands` | 创建自定义命令 |
| `/mcp enable [server]` | 启用 MCP 服务 |
| `/mcp disable [server]` | 禁用 MCP 服务 |

---

### 键盘快捷键

| 快捷键 | 功能 |
|--------|------|
| `Shift+Enter` | 换行（多行输入） |
| `Ctrl+D` | 退出 CLI（需按两次，防误触） |
| `Ctrl+R` | 查看/审查更改（按 `i` 看说明） |
| `↑` / `↓` | 浏览历史消息 |

---

## 🔧 实际工作流示例

### 1️⃣ 代码审查

```bash
# 审查当前分支的更改
agent -p "审查当前分支的更改，重点关注安全性和性能"

# 对比 main 分支
agent -p "对比当前分支和 main 的差异，找出不一致的地方"
```

---

### 2️⃣ 代码重构

```bash
# 重构特定文件
agent -p "重构 src/utils.ts，降低复杂度并提高类型安全"

# 优化性能
agent -p "分析这个函数的性能瓶颈并优化"
```

---

### 3️⃣ 调试

```bash
# 交互式调试
agent
> 分析这个错误日志并提供修复方案：
> [粘贴错误日志]

# 单次调试
agent -p "分析以下错误：TypeError: Cannot read property 'x' of undefined"
```

---

### 4️⃣ Git 操作

```bash
# 生成提交消息
agent -p "为暂存的更改生成符合 conventional commits 的提交信息"

# 审查 PR
agent -p "审查这个 PR 的更改，列出潜在问题"
```

---

### 5️⃣ 测试

```bash
# 生成测试
agent -p "为 src/auth.ts 生成单元测试"

# 运行测试
agent -p "运行测试并生成覆盖率报告" --output-format json
```

---

### 6️⃣ 批量处理（CI/CD）

```bash
# 安全检查
agent -p "审计代码库的安全漏洞" --output-format json --force

# 代码质量
agent -p "检查代码规范问题并修复" --force

# 文档生成
agent -p "为所有 API 端点生成文档"
```

---

## 📋 配置文件

### 规则文件

Cursor 会自动加载以下配置：

| 文件 | 说明 |
|------|------|
| `.cursor/rules` | Cursor 专用规则 |
| `AGENTS.md` | Agent 通用规则 |
| `CLAUDE.md` | Claude 风格规则 |

---

### 规则示例

创建 `.cursor/rules/security.mdc`：

```markdown
# 安全规则

- 永远不要硬编码 API Key
- 所有用户输入必须验证
- 使用参数化查询防止 SQL 注入
- 敏感操作需要日志记录
```

---

### MCP 集成

MCP（Model Context Protocol）服务器配置在 `mcp.json`：

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem"]
    }
  }
}
```

**在会话中管理：**
```
/mcp enable filesystem
/mcp disable server-name
```

---

## 📊 输出格式

### 纯文本（默认）

```bash
agent -p "分析代码" --output-format text
```

**适合：** 人工阅读

---

### JSON

```bash
agent -p "查找 bug" --output-format json
```

**输出示例：**
```json
{
  "type": "diagnostic",
  "severity": "error",
  "file": "src/app.ts",
  "line": 42,
  "message": "Potential null pointer exception"
}
```

**适合：** 程序处理、CI/CD

---

### 流式 JSON

```bash
agent -p "运行测试" --output-format stream-json --stream-partial-output
```

**适合：** 实时进度显示

---

## 🔍 故障排查

### 问题 1：命令找不到

```bash
# 检查 PATH
echo $PATH

# 重新加载配置
source ~/.zshrc

# 验证安装
agent --version
```

---

### 问题 2：认证失败

```bash
# 重新登录
agent login

# 或检查 API Key
echo $CURSOR_API_KEY
```

---

### 问题 3：工作区不信任

第一次运行时会提示信任工作区，按 `a` 键信任即可。

---

## 💡 最佳实践

### 1. 使用规则文件

创建项目规则，让 AI 理解你的代码风格：

```markdown
# .cursor/rules/project.mdc

## 代码风格
- 使用 TypeScript
- 优先使用函数式编程
- 所有函数必须有类型注解

## 测试
- 所有公共方法必须有单元测试
- 测试覆盖率 > 80%
```

---

### 2. 组合使用模式

```bash
# 交互式开发
agent

# 快速任务
agent -p "格式化这个文件"

# 复杂任务
agent -p "重构整个模块"
```

---

### 3. CI/CD 集成

```yaml
# .github/workflows/cursor-check.yml
name: Cursor Code Review

on: [push, pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Install Cursor
        run: curl https://cursor.com/install | bash
      
      - name: Run Security Audit
        env:
          CURSOR_API_KEY: ${{ secrets.CURSOR_API_KEY }}
        run: |
          agent -p "Audit for security vulnerabilities" \
            --output-format json \
            --force
```

---

## 📚 相关资源

| 资源 | 链接 |
|------|------|
| **Cursor 官网** | https://cursor.com |
| **CLI 文档** | https://docs.cursor.com/cli |
| **GitHub 仓库** | https://github.com/getcursor/cursor |
| **MCP 协议** | https://modelcontextprotocol.io |

---

## 💭 类比理解

| 类比 | 说明 |
|------|------|
| **Cursor CLI vs Cursor IDE** | 就像 `git` vs GitHub Desktop |
| **交互式模式** | 像和同事 pair programming |
| **非交互式模式** | 像运行 linter/checker |

---

## 📝 快速参考

### 安装
```bash
curl https://cursor.com/install | bash
```

### 登录
```bash
agent login
```

### 交互模式
```bash
agent
```

### 单次任务
```bash
agent -p "任务描述"
```

### 强制模式
```bash
agent -p "任务" --force
```

### 查看模型
```bash
agent models
```

### 恢复会话
```bash
agent resume
```

---

## 📝 更新日志

- **2026-02-20**: 初始版本，整理 Cursor CLI 使用指南
