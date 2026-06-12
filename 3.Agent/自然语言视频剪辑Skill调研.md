---
title: 自然语言视频剪辑Skill调研——jianying-editor-skill
type: concept
created: 2026-06-12
updated: 2026-06-12
sources:
  - "B站视频 BV1V3d2BoE1G: 用自然语言剪视频，这个 Skill 太牛了"
  - "https://github.com/luoluoluo22/jianying-editor-skill"
  - "https://jianyingskill.netlify.app/"
tags: [AI剪辑, 剪映, Skill, Agent, 自然语言, jianying-editor, pyJianYingDraft, 自动剪辑]
---

# 自然语言视频剪辑Skill调研——jianying-editor-skill

## 一、视频概述

**B站视频**: [用自然语言剪视频，这个 Skill 太牛了](https://www.bilibili.com/video/BV1V3d2BoE1G)
**UP主**: 我老萝卜 (luoluoluo22，GitHub同名)
**播放量**: 数万（该UP主系列视频累计播放超18万）

该视频属于UP主"我老萝卜"的**剪映剪辑Skill系列**，系列视频包括：
- [全网首发] 我写了个剪映剪辑skill，一句话全自动接管剪映！代码已开源
- 剪映剪辑skill新功能：录个屏就自动生成缩放效果
- 【AI全自动接管剪映V3~V7】系列
- 【国内用户安装剪映skill保姆级教程】
- 【AI全自动接管剪映V6】openClaw接管剪映全自动剪辑

---

## 二、Skill 介绍

### 2.1 基本信息

| 项目 | 内容 |
|------|------|
| **名称** | jianying-editor-skill（剪映剪辑Skill） |
| **作者** | luoluoluo22（我老萝卜） |
| **GitHub** | https://github.com/luoluoluo22/jianying-editor-skill |
| **星标** | ~1,000+ |
| **语言** | Python |
| **许可证** | 开源 |
| **官网** | https://jianyingskill.netlify.app/ |
| **定位** | 赋予 AI "手眼"，使其能通过 Python 代码全自动生成、编辑和导出剪映视频草稿 |

### 2.2 一句话描述

> 剪辑师只需用自然语言告诉 AI 你想做什么视频，它就能帮你完成从**写文案、配音、加字幕、选音乐、上特效到最终导出**的整套流程。

### 2.3 支持的 AI 编辑器

| 编辑器 | 安装方式 |
|--------|----------|
| **Claude Code** | `git clone` 到 `.claude/skills/jianying-editor` |
| **Antigravity** | `git clone` 到 `.agent/skills/jianying-editor` |
| **Trae IDE** | `git clone` 到 `.trae/skills/jianying-editor` |
| **Cursor / VSCode** | `git clone` 到 `skills/jianying-editor` |
| **OpenClaw** | 直接安装 Skill 目录 |

---

## 三、功能全景

### 3.1 核心功能

| 功能 | 说明 |
|------|------|
| **素材导入** | 视频、音频、图片一句话丢进时间轴，自动排列 |
| **AI 配音** | 输入文案自动生成语音，支持剪映原生音色和微软语音 |
| **字幕生成** | 根据配音自动拆句、逐句对齐字幕，支持打字机等动画效果 |
| **自动配乐** | 本地音乐或剪映素材库的云端音乐 |
| **特效/转场/滤镜** | 按名字搜索剪映自带的特效库，一句话应用 |
| **网页动效转视频** | 用 HTML/JS/Canvas 写动画，自动录屏变成视频素材导入剪映 |
| **录屏 + 智能变焦** | 录制屏幕操作，自动给鼠标点击位置加缩放和红圈标记 |
| **影视解说** | AI 分析视频内容，自动生成分镜脚本并合成解说视频 |
| **自动导出** | 剪完直接导出 MP4，支持 1080P 到 4K |
| **关键帧动画** | 缩放、位移、透明度等关键帧，做出运镜效果 |
| **复合片段** | 像嵌套工程一样，把多个子项目组合成一个完整视频 |
| **花字/样式文本** | 支持剪映的花字效果（渐变、描边、阴影、动画外观） |
| **模板批量生产** | 从模板克隆 + 批量替换素材，适合100条个性化广告 |

### 3.2 自然语言交互示例

```
用户: "来一个简单的剪辑"
→ AI 自动执行：导入素材 → 添加配乐 → 加标题 → 保存草稿

用户: "帮我把 assets/ 里的视频导入，配上 BGM，最后加一个带打字机动画的标题"
→ AI 精准搜索素材 → 组合轨道 → 应用动画 → 保存

用户: "帮我用网页写一个'红心粒子爆炸'的动效，并导入到剪映"
→ AI 生成 HTML/JS Canvas 动画 → 自动录屏 → 导入剪映

用户: "分析视频 assets/video.mp4 制作 60 秒影视解说"
→ AI 分析视频内容 → 生成分镜脚本 → 合成解说视频
```

### 3.3 功能限制

- **不是剪映替代品**：最终渲染、预览回放靠剪映本身完成，工具负责"自动搭时间轴"
- **不能用剪映的实时特效**：不支持"一键成片""图文成片"等剪映内置AI功能按钮
- **自动导出依赖老版本**：仅支持**剪映 5.9 及以下版本**（6.0+ 弹窗太多会干扰自动化）
- **仅支持桌面版**：不支持手机版剪映，仅 Windows/Mac 桌面版剪映专业版
- **导出仅 Windows**：自动导出（uiautomation）仅支持 Windows 平台

---

## 四、技术架构

### 4.1 核心原理：文件注入驱动

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  AI 思考      │ ──→ │  Skill 引擎   │ ──→ │  剪映草稿     │ ──→ │  剪映软件     │
│ Claude/Cursor │     │ Python       │     │  JSON 修改    │     │  自动识别工程  │
│ 生成指令流     │     │ Wrapper解析   │     │  无需官方API  │     │  专业级控制    │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
```

**核心洞察**：AI 不需要直接操作鼠标点击，而是直接操作剪映底层的草稿数据（`draft_content.json`）。这不仅绕过了软件交互的延迟，更实现了对时间轴、素材坐标、滤镜参数的 **100% 精确控制**。

### 4.2 技术栈

```
jianying-editor-skill/
├── SKILL.md                    # AI Agent 读取的 Skill 定义文件
├── README.md                   # 人类阅读的项目说明
├── docs/
│   ├── agent-playbook.md       # Agent 任务路由矩阵
│   └── minimal-command-sop.md  # 最小化命令标准操作流程
├── rules/                      # 分层规则文件（AI 按需读取）
│   ├── setup.md                # 强制初始化代码
│   ├── core.md                 # 核心操作：保存、导出、草稿管理
│   ├── cli.md                  # CLI 工具和机器可读输出约定
│   ├── media.md                # 素材导入 + AI 视频分析优化
│   ├── text.md                 # 字幕、文本、花字
│   ├── keyframes.md            # 关键帧动画
│   ├── effects.md              # 特效、转场、滤镜
│   ├── recording.md            # 录屏 + 智能变焦
│   ├── web-vfx.md              # Web 动效转视频
│   ├── generative.md           # 生成式编辑思维链
│   └── audio-voice.md          # TTS 配音 + BGM
├── scripts/
│   ├── vendor/pyJianYingDraft/ # 核心依赖：剪映草稿 Python 库
│   ├── jy_wrapper.py           # 高级封装 API (JyWrapper)
│   ├── auto_exporter.py        # 自动导出脚本
│   ├── draft_inspector.py      # 草稿检查器
│   ├── asset_search.py         # 素材搜索
│   ├── movie_commentary_builder.py  # 影视解说生成器
│   └── ...
├── tools/recording/            # 录屏工具集
│   └── recorder.py             # GUI 录屏助手
├── assets/                     # 演示素材
├── data/                       # 枚举数据
│   ├── cloud_text_styles.csv   # 花字样式索引
│   └── text_animations.csv     # 文本动画索引
├── examples/                   # 示例脚本
└── prompts/                    # LLM 提示词模板
    └── movie_commentary.md     # 影视解说提示词
```

### 4.3 核心依赖

| 依赖 | 用途 | 说明 |
|------|------|------|
| **pyJianYingDraft** | 剪映草稿 JSON 读写 | 核心引擎，直接操作 draft_content.json |
| **uiautomation** | Windows UI 自动化 | 自动导出时模拟点击操作 |
| **playwright** | 浏览器自动化 | Web 动效录屏 |
| **pynput** | 键盘鼠标监听 | 录屏时的操作采集 |
| **edge-tts** | 微软语音合成 | AI 配音（免费） |
| **pymediainfo** | 媒体文件信息 | 读取视频元数据 |

### 4.4 Agent 执行流程

```
用户自然语言指令
    │
    ▼
Agent 读取 SKILL.md + 相关 rules/*.md
    │
    ▼
Agent 生成 Python 脚本（使用 JyWrapper API）
    │
    ├── JyProject("项目名")
    ├── add_media_safe("video.mp4", "0s")
    ├── add_media_safe("bgm.mp3", "0s", track_name="Audio")
    ├── add_text_simple("标题", start_time="1s", anim_in="打字机")
    ├── add_tts_intelligent("旁白文案")
    ├── add_narrated_subtitles()
    └── project.save()
    │
    ▼
JyWrapper → pyJianYingDraft → 修改 draft_content.json
    │
    ▼
剪映读取草稿 → 用户审核 → 手动/自动导出 MP4
```

### 4.5 关键设计决策

1. **分层规则文件**：AI 不需要一次性加载所有规则，而是按任务类型按需读取对应 rule 文件，节省上下文窗口
2. **Agent Playbook**：定义了 7 种任务路由矩阵（快速剪辑/云端素材/旁白字幕/录屏/特效/影视解说/导出），确保可靠执行
3. **验收检查清单**：每次执行后强制验证：草稿目录存在、save 成功、至少一个 video segment、BGM 在 audio 轨道等
4. **时间精度**：AI 生成的时间线使用秒为单位的浮点数，保留 2-3 位小数，内部转换为微秒
5. **防碰撞自动分层**：多个文本片段时间重叠时，自动创建新轨道避免碰撞崩溃

---

## 五、与 WelooAI 自动剪辑 Skill 对比

### 5.1 相同点

| 维度 | 共同特征 |
|------|----------|
| **核心原理** | 都通过直接操作剪映草稿 JSON 文件实现自动剪辑 |
| **运行方式** | 都是本地 Skill，被 Agent（Claude Code/OpenClaw）调用 |
| **输出形式** | 都是生成剪映草稿工程，非最终视频文件 |
| **交互方式** | 都支持自然语言描述剪辑需求 |
| **依赖剪映** | 都需要本地安装剪映专业版 |
| **技术路线** | 都绕过了"剪映有没有官方 API"的问题，走文件注入路线 |

### 5.2 差异点

| 维度 | jianying-editor-skill | WelooAI 自动剪辑 Skill |
|------|----------------------|------------------------|
| **视频内容理解** | 依赖 AI 分析视频（30min/360p 优化），无专用视频理解API | 使用 **Twelve Labs API** 做专业视频内容理解（识别主体/动作/场景/情绪） |
| **功能广度** | **极广**：素材导入、配音、字幕、特效、转场、滤镜、关键帧、录屏、Web动效、影视解说、模板批量生产 | **聚焦**：素材理解 → 筛选片段 → 剪辑规划 → 生成草稿 |
| **编辑精细度** | **极高**：支持关键帧动画、花字样式、多轨管理、复合片段 | 相对粗粒度：自动筛选+规划，细节调整依赖剪映手动 |
| **自动导出** | 支持（Windows + 剪映5.9，uiautomation） | 未明确提及 |
| **AI 编辑器支持** | Claude Code / Antigravity / Trae / Cursor / OpenClaw | OpenClaw / Claude Code |
| **社区生态** | 开源 ~1K stars，活跃开发，系列视频教程 | 抖音视频推广，相对小众 |
| **安装复杂度** | 需安装 Python 依赖 + 剪映 5.9 | 需 Twelve Labs API Key + 剪映 |
| **成本** | 免费（edge-tts 免费，分析用本地模型） | 需 Twelve Labs API 费用 |

### 5.3 互补关系

两者并非竞争关系，而是**互补关系**：

- **WelooAI 强在"理解"**：通过 Twelve Labs 真正读懂视频内容，适合有大量素材需要智能筛选的场景
- **jianying-editor-skill 强在"操作"**：提供最全面的剪映草稿操作能力，适合需要精细编辑控制的场景

理想组合：WelooAI 做素材理解与筛选 → jianying-editor-skill 做精细编辑与导出。

---

## 六、与 capcut-cli 项目的关系

### 6.1 共同点

| 维度 | 共同特征 |
|------|----------|
| **操作对象** | 都是 CapCut/剪映的 `draft_content.json` 草稿文件 |
| **核心机制** | 都是直接读写 JSON 文件，不经过官方 API |
| **Agent 友好** | 都是为 AI Agent 驱动而设计 |
| **开源** | 都是开源项目 |

### 6.2 差异点

| 维度 | jianying-editor-skill | capcut-cli |
|------|----------------------|------------|
| **语言** | Python | TypeScript (Node.js) |
| **形态** | Agent Skill（Python 库 + 规则文件） | CLI 工具（150+ 命令） |
| **安装** | git clone + pip install | `npm install -g capcut-cli` |
| **依赖** | pyJianYingDraft + uiautomation + playwright + ... | 零依赖（仅 Node ≥ 18） |
| **平台** | Windows/Mac（导出仅 Windows） | Windows/Mac/Linux |
| **跨版本** | 仅剪映国内版 | CapCut 国际版 + 剪映国内版，双命名空间 |
| **枚举发现** | CSV 文件 | 13 类 × 2 命名空间，793KB enums.json |
| **Agent 集成** | Skill 文件（AI 读取 rules 自行决策） | JSON-in/JSON-out CLI + Plugin + Library |
| **功能覆盖** | 侧重高级编辑（花字、Web动效、智能变焦、影视解说） | 侧重全面性（字幕/翻译/模板/关键帧/蒙版/混合模式/色度抠图等） |
| **声明式编译** | 无 | 支持 `compile` 从 JSON spec 直接生成草稿 |
| **CI/CD** | 不支持 | GitHub Action + Docker |
| **底层引擎** | pyJianYingDraft | 自研 TypeScript draft 引擎 |

### 6.3 关系总结

```
capcut-cli (TypeScript CLI)          jianying-editor-skill (Python Skill)
        │                                        │
        ├── 底层：自研 draft_content.json 引擎     ├── 底层：pyJianYingDraft
        ├── 形态：CLI + Library                   ├── 形态：Agent Skill
        ├── 优势：零依赖、跨平台、双命名空间         ├── 优势：高级编辑、录屏、Web动效
        └── 互补：可作为后端的 JSON 操作层           └── 互补：提供高级编辑能力和 Skill 模板
```

两者是**互补关系**而非替代关系：
- capcut-cli 更适合作为**通用底层工具**，被任何语言的 Agent 调用
- jianying-editor-skill 更适合作为**完整 Skill 方案**，提供从规则到执行的端到端体验
- 理论上可以将 capcut-cli 作为 jianying-editor-skill 的底层引擎，替换 pyJianYingDraft

---

## 七、改装为 Agent 可调用工具的可行性

### 7.1 结论：**已经是 Agent 可调用工具，无需改装**

jianying-editor-skill 从设计之初就是一个 Agent Skill，安装即用。

### 7.2 安装方式

#### Windows 一键安装（推荐）

```powershell
irm is.gd/rpb65M | iex
```

#### 各 IDE 手动安装

```bash
# Claude Code
git clone https://github.com/luoluoluo22/jianying-editor-skill.git .claude/skills/jianying-editor

# Antigravity
git clone https://github.com/luoluoluo22/jianying-editor-skill.git .agent/skills/jianying-editor

# Trae IDE
git clone https://github.com/luoluoluo22/jianying-editor-skill.git .trae/skills/jianying-editor

# Cursor / VSCode
git clone https://github.com/luoluoluo22/jianying-editor-skill.git skills/jianying-editor
```

#### 环境准备

```bash
# 重要：使用剪映 5.9 版本
pip install uiautomation playwright pynput edge-tts pymediainfo
playwright install chromium
```

### 7.3 在 Claude Code 中使用

安装后，直接在 Claude Code 中用自然语言发出指令：

```
"帮我做一个产品介绍视频，用 assets/ 里的素材，加个打字机标题"
"分析这个视频，做一个60秒的影视解说"
"录个屏，自动给点击位置加缩放效果"
"把这个视频配上BGM，加字幕，导出1080P"
```

Claude Code 会自动读取 `SKILL.md` → 根据任务类型读取对应 `rules/*.md` → 生成 Python 脚本 → 执行 → 验证。

### 7.4 改装为 OpenClaw Skill 的注意事项

如果要在 OpenClaw 中使用，需要确保：

1. **Python 环境**：OpenClaw 运行环境需安装上述 Python 依赖
2. **剪映版本**：需安装剪映 5.9（6.0+ 弹窗干扰自动化）
3. **草稿路径**：Windows 默认路径 `C:\Users\<用户名>\AppData\Local\JianyingPro\User Data\Projects\com.lveditor.draft`
4. **文件锁定**：编辑前需关闭剪映中该工程
5. **导出限制**：自动导出仅 Windows 平台

---

## 八、生态中的其他同类项目

| 项目 | 语言 | 定位 | 与本文关系 |
|------|------|------|-----------|
| **pyJianYingDraft** (3K stars) | Python | 剪映草稿 Python 库 | jianying-editor-skill 的底层引擎 |
| **capcut-cli** (~500 stars) | TypeScript | LLM Agent 驱动的剪映 CLI | 互补，详见 [[capcut-cli调研]] |
| **capcut-mate** (1.1K stars) | Python/FastAPI | HTTP API 服务器 | 后端调 pyJianYingDraft |
| **VectCutAPI** | Python/Flask | MCP 协议的剪映 API | 通过 MCP 协议集成 |
| **cutcli** | Go | 闭源 CLI + MCP Server | 商业方案 |
| **videocut-skills** | Python | Claude Code 口播视频剪辑 Agent | 专注口播场景 |
| **video_cut_skill** | Python | OpenClaw 视频剪辑 Skill | FFmpeg + Whisper + AI 分析 |
| **FireRed-OpenStoryline** (2.8K stars) | Python | AI 视频编辑 Agent | 意图驱动的自然语言视频编辑 |
| **video-use** | Python | Claude Code 视频编辑 | browser-use 团队出品 |
| **X-Cut** | TypeScript | 对话式视频编辑 Agent | Remotion 实时渲染 |
| **BibiGPT Skill** | - | AI 音视频助理 Skill | 侧重内容理解而非编辑 |

---

## 九、总结与建议

### 9.1 核心结论

1. **视频介绍的 Skill 是 jianying-editor-skill**，由 UP 主"我老萝卜"(luoluoluo22) 开发，开源在 GitHub，~1K stars
2. **核心能力**：自然语言 → AI Agent 生成 Python 脚本 → 操作剪映草稿 JSON → 覆盖从素材导入到导出的全流程
3. **技术架构**：基于 pyJianYingDraft 的文件注入机制，无需官方 API，通过修改 draft_content.json 实现精确控制
4. **与 WelooAI 互补**：WelooAI 强于素材理解（Twelve Labs），jianying-editor-skill 强于编辑操作（全功能覆盖）
5. **与 capcut-cli 互补**：capcut-cli 是通用底层工具（CLI + Library），jianying-editor-skill 是完整 Skill 方案
6. **已是 Agent 可调用工具**：安装即用，无需改装，支持 Claude Code / Cursor / Trae / Antigravity / OpenClaw

### 9.2 对知识库的建议

- 本笔记应与 [[capcut-cli调研]]、[[WelooAI自动剪辑Skill]] 形成交叉引用
- 三个工具覆盖了"剪映自动剪辑"的三个维度：**底层操作**(capcut-cli) → **上层Skill**(jianying-editor) → **智能理解**(WelooAI)
- 后续可考虑整合方案：WelooAI 做素材理解 + capcut-cli 做底层操作 + jianying-editor-skill 做 Skill 模板

---

## 参考来源

- [jianying-editor-skill GitHub](https://github.com/luoluoluo22/jianying-editor-skill) — 主要调研对象
- [jianying-editor-skill 官网](https://jianyingskill.netlify.app/) — 官方文档
- [B站视频 BV1V3d2BoE1G](https://www.bilibili.com/video/BV1V3d2BoE1G) — 调研起点
- [UP主 我老萝卜 B站主页](https://space.bilibili.com/491691175) — 系列视频
- [pyJianYingDraft](https://github.com/GuanYixuan/pyJianYingDraft) — 底层引擎
- [capcut-cli](https://github.com/renezander030/capcut-cli) — 对比参考
- [[WelooAI自动剪辑Skill]] — 对比参考
- [[capcut-cli调研]] — 对比参考