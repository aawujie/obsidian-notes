# NotebookLM CLI 完整命令清单

> **快速开始**：`notebooklm login` → `notebooklm list` → `notebooklm use "笔记名"` → `notebooklm ask "问题"`
> 
> **提示**：支持部分 ID 匹配（如 `notebooklm use abc` 可匹配 `abc123...`）

---

## 🔐 会话管理

| 命令 | 说明 | 示例 |
|------|------|------|
| `login` | 登录 Google 账号 | `notebooklm login` |
| `use` | 切换到指定笔记 | `notebooklm use "Grokking"` |
| `status` | 查看当前笔记状态 | `notebooklm status` |
| `clear` | 清除当前笔记上下文 | `notebooklm clear` |

---

## 📚 笔记管理

| 命令 | 说明 | 示例 |
|------|------|------|
| `list` | 列出所有笔记 | `notebooklm list` |
| `create` | 创建新笔记 | `notebooklm create "我的学习"` |
| `delete` | 删除笔记 | `notebooklm delete "笔记名"` |
| `rename` | 重命名笔记 | `notebooklm rename "旧名" "新名"` |
| `summary` | 获取 AI 生成的笔记摘要 | `notebooklm summary` |

---

## 💬 对话与提问

| 命令 | 说明 | 示例 |
|------|------|------|
| `ask` | 向笔记提问 | `notebooklm ask "这本书讲了什么？"` |
| `configure` | 配置 AI 人设和回答风格 | `notebooklm configure --persona "专业导师"` |
| `history` | 查看/清除对话历史 | `notebooklm history` |

---

## 📄 Source 管理（核心功能）

| 命令 | 说明 | 示例 |
|------|------|------|
| `source list` | 列出所有 source | `notebooklm source list` |
| `source add` | 添加 URL/PDF/文本 | `notebooklm source add "https://docs.openclaw.ai"` |
| `source add-drive` | 从 Google Drive 添加 | `notebooklm source add-drive "file.pdf"` |
| `source add-research` | 自动研究并导入 | `notebooklm source add-research "强化学习"` |
| `source delete` | 删除 source | `notebooklm source delete "文件名"` |
| `source refresh` | 刷新 source 内容 | `notebooklm source refresh` |
| `source fulltext` | 获取 source 完整文本 | `notebooklm source fulltext "文件名"` |
| `source guide` | 获取 source 导读 | `notebooklm source guide` |
| `source stale` | 查找过时的 source | `notebooklm source stale` |

---

## 🎨 内容生成（Artifact）

### 生成内容

| 命令 | 说明 | 示例 |
|------|------|------|
| `generate audio` | 生成播客/音频 | `notebooklm generate audio --format deep-dive` |
| `generate video` | 生成视频教程 | `notebooklm generate video --style whiteboard` |
| `generate quiz` | 生成测验题 | `notebooklm generate quiz --difficulty hard` |
| `generate flashcards` | 生成闪卡 | `notebooklm generate flashcards --quantity 20` |
| `generate mind-map` | 生成思维导图 | `notebooklm generate mind-map` |
| `generate infographic` | 生成信息图 | `notebooklm generate infographic --orientation portrait` |
| `generate slide-deck` | 生成幻灯片 | `notebooklm generate slide-deck` |
| `generate report` | 生成报告/学习指南 | `notebooklm generate report --type study-guide` |
| `generate data-table` | 生成数据表格 | `notebooklm generate data-table "对比关键概念"` |

### 下载内容

| 命令 | 说明 | 示例 |
|------|------|------|
| `download audio` | 下载音频（MP3） | `notebooklm download audio ./podcast.mp3` |
| `download video` | 下载视频（MP4） | `notebooklm download video ./tutorial.mp4` |
| `download quiz` | 下载测验题 | `notebooklm download quiz --format markdown ./quiz.md` |
| `download flashcards` | 下载闪卡 | `notebooklm download flashcards --format json ./cards.json` |
| `download mind-map` | 下载思维导图（JSON） | `notebooklm download mind-map ./mindmap.json` |
| `download infographic` | 下载信息图（PNG） | `notebooklm download infographic ./info.png` |
| `download slide-deck` | 下载幻灯片（PDF） | `notebooklm download slide-deck ./slides.pdf` |

### 管理已生成的内容

| 命令 | 说明 | 示例 |
|------|------|------|
| `artifact list` | 列出所有已生成的内容 | `notebooklm artifact list` |
| `artifact get` | 获取某个 artifact 详情 | `notebooklm artifact get "ID"` |
| `artifact delete` | 删除 artifact | `notebooklm artifact delete "ID"` |
| `artifact export` | 导出 artifact | `notebooklm artifact export "ID"` |
| `artifact poll` | 轮询生成状态 | `notebooklm artifact poll` |
| `artifact wait` | 等待生成完成 | `notebooklm artifact wait` |

---

## 📝 笔记功能（Note）

| 命令 | 说明 | 示例 |
|------|------|------|
| `note list` | 列出所有笔记 | `notebooklm note list` |
| `note create` | 创建新笔记 | `notebooklm note create "学习笔记"` |
| `note get` | 获取笔记内容 | `notebooklm note get "笔记名"` |
| `note save` | 保存笔记 | `notebooklm note save "笔记名"` |
| `note delete` | 删除笔记 | `notebooklm note delete "笔记名"` |
| `note rename` | 重命名笔记 | `notebooklm note rename "旧名" "新名"` |

---

## 🔗 分享功能

| 命令 | 说明 | 示例 |
|------|------|------|
| `share status` | 查看分享状态 | `notebooklm share status` |
| `share public` | 创建公开链接 | `notebooklm share public` |
| `share add` | 添加协作者 | `notebooklm share add "user@email.com"` |
| `share remove` | 移除协作者 | `notebooklm share remove "user@email.com"` |
| `share update` | 更新分享设置 | `notebooklm share update` |
| `share view-level` | 设置查看权限 | `notebooklm share view-level editor` |

---

## 🌐 研究功能

| 命令 | 说明 | 示例 |
|------|------|------|
| `research status` | 查看研究任务状态 | `notebooklm research status` |
| `research wait` | 等待研究完成 | `notebooklm research wait` |

---

## ⚙️ 其他功能

| 命令 | 说明 | 示例 |
|------|------|------|
| `language` | 设置输出语言 | `notebooklm language zh-CN` |
| `skill` | 管理 Claude Code Skill | `notebooklm skill install` |
| `auth` | 认证管理 | `notebooklm auth status` |

---

## 🎯 常用场景示例

### 场景 1：学习 DRL 笔记

```bash
# 1. 切换到 DRL 笔记
notebooklm use "Grokking"

# 2. 提问
notebooklm ask "这本书的核心概念有哪些？"

# 3. 生成测验题
notebooklm generate quiz --difficulty hard --quantity 10

# 4. 下载测验题
notebooklm download quiz --format markdown ./drl-quiz.md

# 5. 生成思维导图
notebooklm generate mind-map

# 6. 下载思维导图
notebooklm download mind-map ./drl-mindmap.json
```

---

### 场景 2：批量导入文档站

```bash
# 1. 添加整个文档站
notebooklm source add "https://docs.openclaw.ai"

# 2. 查看 source 列表
notebooklm source list

# 3. 删除重复的 source
notebooklm source delete "重复的文件名"

# 4. 运行审计
notebooklm source stale
```

---

### 场景 3：自动生成学习材料

```bash
# 1. 生成播客
notebooklm generate audio --format deep-dive --wait

# 2. 下载播客
notebooklm download audio ./drl-podcast.mp3

# 3. 生成视频教程
notebooklm generate video --style whiteboard --wait

# 4. 下载视频
notebooklm download video ./drl-video.mp4

# 5. 生成幻灯片
notebooklm generate slide-deck

# 6. 下载幻灯片
notebooklm download slide-deck ./drl-slides.pdf
```

---

### 场景 4：从 Google Drive 导入

```bash
# 从 Drive 添加 PDF
notebooklm source add-drive "My Documents/RL_Notes.pdf"

# 从 Drive 添加研究任务
notebooklm source add-research "深度强化学习最新进展"
```

---

### 场景 5：协作学习

```bash
# 添加协作者
notebooklm share add "study-group@example.com"

# 设置编辑权限
notebooklm share view-level editor

# 创建公开链接
notebooklm share public

# 查看分享状态
notebooklm share status
```

---

## 💡 输出目录建议

建议统一输出到 `~/clawd/output/` 目录：

```bash
# 创建输出目录
mkdir -p ~/clawd/output/notebooklm

# 下载时指定路径
notebooklm download quiz --format markdown ~/clawd/output/notebooklm/drl-quiz.md
notebooklm download mind-map ~/clawd/output/notebooklm/drl-mindmap.json
notebooklm download infographic ~/clawd/output/notebooklm/drl-infographic.png
notebooklm download audio ~/clawd/output/notebooklm/drl-podcast.mp3
notebooklm download video ~/clawd/output/notebooklm/drl-video.mp4
notebooklm download slide-deck ~/clawd/output/notebooklm/drl-slides.pdf
```

---

## 📊 生成的文件格式

| 类型 | 格式 | 说明 |
|------|------|------|
| **音频** | MP3 | 播客/音频概述 |
| **视频** | MP4 | 视频教程 |
| **测验题** | JSON/Markdown/HTML | 可导入 Anki 或其他工具 |
| **闪卡** | JSON/Markdown/HTML | 可导入 Anki 或其他工具 |
| **思维导图** | JSON | 层级结构数据 |
| **信息图** | PNG | 高清图片 |
| **幻灯片** | PDF | 可导出 PowerPoint |
| **数据表格** | CSV | 可导入 Excel/Sheets |
| **报告** | Markdown | 可导入 Obsidian/Notion |

---

## 🔗 参考链接

- **GitHub 仓库**：https://github.com/teng-lin/notebooklm-py
- **PyPI 包**：https://pypi.org/project/notebooklm-py/
- **官方文档**：https://github.com/teng-lin/notebooklm-py/tree/main/docs

---

**标签**：#NotebookLM #CLI #命令清单 #AI 学习 #知识管理

**创建日期**：2026-02-21  
**版本**：notebooklm-py v0.3.2
