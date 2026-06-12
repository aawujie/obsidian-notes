# OpenClaw 达芬奇 MCP 配置入门

> 创建日期：2026-06-13  
> 达芬奇版本：DaVinci Resolve Studio 21.0.0b.20  
> MCP 版本：davinci-resolve-mcp v2.51.0

---

## 📌 什么是 MCP？

**MCP (Model Context Protocol)** 是一种让 AI 助手与外部软件通信的标准协议。

通过 MCP，你可以用**自然语言**让 AI 助手直接控制 DaVinci Resolve，实现：
- 自动导入素材
- 创建时间线
- 批量调色
- 自动字幕
- 渲染输出

---

## 🛠️ 前置要求

| 要求 | 说明 |
|------|------|
| **DaVinci Resolve Studio** | 必须是 Studio 版（免费版不支持外部脚本） |
| **版本** | 18.5+（推荐 21+） |
| **Python** | 3.10-3.12（推荐 3.12） |
| **系统** | macOS / Windows / Linux |
| **OpenClaw** | 已安装的 OpenClaw 环境 |

---

## 📦 安装步骤

### 步骤 1：安装达芬奇 MCP 服务器

```bash
# 使用官方安装脚本自动安装
npx -y davinci-resolve-mcp setup
```

安装完成后，运行检测：

```bash
npx -y davinci-resolve-mcp doctor
```

✅ 成功输出示例：
```
Connected: DaVinci Resolve Studio 21.0.0b.20
Setup complete!
```

---

### 步骤 2：配置 OpenClaw MCP

编辑 `~/.openclaw/openclaw.json`，添加 MCP 服务器配置：

```json
{
  "mcp": {
    "servers": {
      "davinci-resolve": {
        "command": "/opt/homebrew/opt/python@3.12/bin/python3.12",
        "args": [
          "/Users/apple/Library/Application Support/davinci-resolve-mcp/src/server.py"
        ],
        "env": {
          "RESOLVE_SCRIPT_API": "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting",
          "RESOLVE_SCRIPT_LIB": "/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so",
          "PYTHONPATH": "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules"
        }
      }
    }
  }
}
```

> ⚠️ 路径可能因系统而异，请以 `doctor` 命令输出为准。

---

### 步骤 3：重启 OpenClaw Gateway

```bash
# 在 OpenClaw 中执行
gateway restart
```

或在 OpenClaw 聊天中让助手执行重启。

---

## ⚙️ 达芬奇设置

打开 DaVinci Resolve Studio：

1. 菜单栏 → `DaVinci Resolve` → `Preferences`
2. `General` → `External scripting`
3. 设置为 **`Local`**（不是 Cloud）
4. 保持达芬奇运行状态

---

## 🎬 基础功能与命令

### 1. 项目管理

| 自然语言命令 | 功能 |
|-------------|------|
| "列出所有达芬奇项目" | 显示当前数据库中的所有项目 |
| "创建一个新项目叫 'XXX'" | 创建新项目 |
| "打开 XXX 项目" | 加载指定项目 |
| "保存当前项目" | 保存项目 |
| "切换到剪辑页面" | 切换工作页面 |

---

### 2. 媒体池管理

| 自然语言命令 | 功能 |
|-------------|------|
| "导入桌面的视频文件" | 导入指定路径的素材 |
| "创建一个分箱叫 'XXX'" | 创建素材分箱 |
| "显示媒体池里的所有内容" | 列出媒体池内容 |
| "把所有 4K 素材整理到一个分箱" | 按条件整理素材 |

---

### 3. 时间线编辑

| 自然语言命令 | 功能 |
|-------------|------|
| "创建一个 1080p 30fps 的时间线" | 创建新时间线 |
| "把媒体池的第一个视频放到时间线" | 添加片段到时间线 |
| "显示当前时间线的片段" | 列出时间线内容 |
| "检测时间线上的间隙" | 查找空隙 |
| "删除所有重叠的片段" | 清理重叠 |

---

### 4. 调色功能

| 自然语言命令 | 功能 |
|-------------|------|
| "显示这个片段的调色节点" | 查看节点结构 |
| "复制这个镜头的调色到所有镜头" | 批量应用调色 |
| "导出当前调色为 LUT" | 导出 LUT 文件 |
| "创建一个新版本" | 创建调色版本 |

---

### 5. 音频处理

| 自然语言命令 | 功能 |
|-------------|------|
| "显示音频轨道映射" | 查看轨道配置 |
| "启用语音隔离" | 开启 AI 语音隔离 |
| "检查哪些片段没有音频" | 检测静音片段 |

---

### 6. 渲染输出

| 自然语言命令 | 功能 |
|-------------|------|
| "列出所有可用的编码格式" | 查看支持的编码 |
| "设置渲染为 ProRes 422 HQ" | 配置渲染格式 |
| "验证当前渲染设置" | 检查渲染参数 |
| "用 H.264 导出到桌面" | 开始渲染 |

---

## 🔍 故障排查

### 问题 1：MCP 无法连接达芬奇

**症状**：
```
Error: Cannot connect to DaVinci Resolve
```

**解决**：
1. 确认达芬奇正在运行
2. 检查 `Preferences > General > External scripting = Local`
3. 确认是 Studio 版本（免费版不支持）

---

### 问题 2：找不到 Python

**症状**：
```
Command failed: python3.12: command not found
```

**解决**：
```bash
# 安装 Python 3.12
brew install python@3.12

# 更新配置中的 Python 路径
which python3.12
```

---

### 问题 3：环境变量错误

**症状**：
```
ModuleNotFoundError: No module named 'DaVinciResolve'
```

**解决**：
检查 `openclaw.json` 中的环境变量是否正确：
- `RESOLVE_SCRIPT_API`
- `RESOLVE_SCRIPT_LIB`
- `PYTHONPATH`

运行 `doctor` 获取正确路径。

---

## 📊 配置检查清单

安装完成后，逐项检查：

- [ ] DaVinci Resolve Studio 已安装并激活
- [ ] 达芬奇正在运行
- [ ] External scripting 设置为 Local
- [ ] Python 3.10-3.12 已安装
- [ ] `npx -y davinci-resolve-mcp doctor` 显示 Connected
- [ ] `~/.openclaw/openclaw.json` 已配置 MCP 服务器
- [ ] OpenClaw Gateway 已重启
- [ ] 能用自然语言命令控制达芬奇

---

## 📖 进阶资源

| 资源 | 链接 |
|------|------|
| **GitHub 仓库** | https://github.com/samuelgursky/davinci-resolve-mcp |
| **API 文档** | https://github.com/samuelgursky/davinci-resolve-mcp/blob/main/docs/reference/api-coverage.md |
| **控制面板指南** | https://github.com/samuelgursky/davinci-resolve-mcp/blob/main/docs/guides/control-panel.md |
| **媒体分析指南** | https://github.com/samuelgursky/davinci-resolve-mcp/blob/main/docs/guides/media-analysis-guide.md |

---

## 💡 使用技巧

### 技巧 1：先用简单命令测试
```
"列出所有项目" → 确认连接正常
```

### 技巧 2：复杂任务分步骤
```
❌ "帮我剪辑整个视频"
✅ "导入素材" → "创建时间线" → "添加片段" → "导出"
```

### 技巧 3：保持达芬奇运行
MCP 不能自动启动达芬奇，使用前必须先打开。

### 技巧 4：使用 Studio 版本
免费版不支持外部 Scripting API，MCP 无法工作。

---

## 🎯 典型工作流示例

### 自动化粗剪流程

```
1. "导入 /Videos 文件夹的所有素材"
2. "创建一个分箱叫 '原始素材'"
3. "创建一个 1080p 30fps 的时间线"
4. "把所有素材按顺序添加到时间线"
5. "删除所有间隙"
6. "添加交叉淡入淡出转场"
7. "用 H.264 导出到桌面"
```

### 批量调色流程

```
1. "打开 '旅行视频' 项目"
2. "切换到调色页面"
3. "显示第一个镜头的节点图"
4. "复制这个调色到所有镜头"
5. "创建新版本保存"
6. "导出 LUT 文件"
```

---

## ⚠️ 注意事项

1. **源素材安全** — MCP 默认只读分析，不会修改原始文件
2. **备份项目** — 执行批量操作前建议备份项目
3. **权限控制** — MCP 只能操作达芬奇 API 允许的功能
4. **性能影响** — 大量操作可能影响达芬奇性能

---

*最后更新：2026-06-13*
