---
title: capcut-cli 调研报告
type: concept
created: 2026-06-12
updated: 2026-06-12
tags: [capcut, jianying, 剪映, cli, agent, draft_content.json, 自动剪辑]
---

# capcut-cli 调研报告

## 一、项目概述

**capcut-cli** 是一个独立、社区维护的 CapCut / 剪映 草稿文件命令行工具，由 René Zander 开发，MIT 开源。

- **仓库**: https://github.com/renezander030/capcut-cli
- **语言**: TypeScript (Node.js)
- **版本**: v0.10.0（截至 2026-06-12）
- **安装**: `npm install -g capcut-cli`
- **运行时**: 零依赖，仅需 Node ≥ 18（全部使用 built-in API）
- **星标**: ~500+
- **npm 下载量**: 持续增长中

### 核心定位

> **"An independent CLI for CapCut / JianYing that any LLM agent can drive — zero dependencies, no server, both namespaces in one binary."**

这是一个专门为 **LLM Agent 驱动** 而设计的剪映/CapCut 命令行工具。每条命令都是 JSON 进、JSON 出，不做 MCP Server，不做 HTTP 守护进程，不做状态管理。使得任何能输出 JSON 的模型（Claude、DeepSeek、GLM、Kimi、Qwen 等）都能直接在 pipeline 中调用。

---

## 二、功能全景

### 2.1 工程 I/O（读/写草稿）

| 命令 | 功能 |
|------|------|
| `info` | 工程概要（时长、片段数、素材数） |
| `tracks` | 列出所有轨道 |
| `materials` | 列出素材类型和计数 |
| `segments` | 列出所有片段及时间信息 |
| `texts` | 列出所有文本/字幕内容 |
| `segment <id>` / `material <id>` | 渐进式深入查看单个项详细信息 |
| `timeline` | ASCII 时间线布局 |
| `export-srt` | 导出字幕为 SRT 文件 |
| `init` | 从零创建空白草稿 |
| `compile` | 从声明式 JSON spec 一次性构建完整草稿 |
| `describe` | 导出 JSON 工具规格（供 LLM/Agent 使用） |

### 2.2 添加素材

| 命令 | 功能 |
|------|------|
| `add-video` | 添加视频/图片（本地文件或 Wikimedia Commons URL） |
| `add-audio` | 添加音频（本地文件或 Wikimedia Commons URL） |
| `add-text` | 添加文本/标题 |
| `add-sticker` | 添加贴纸 |
| `add-effect` | 添加场景特效（vhs/shake/cinematic 等） |

### 2.3 编辑操作

| 命令 | 功能 |
|------|------|
| `set-text` | 修改文本内容 |
| `shift` | 平移单个片段 |
| `shift-all` | 平移整条轨道 |
| `speed` | 修改播放速度 |
| `volume` | 调整音量 |
| `opacity` | 调整透明度 |
| `trim` | 裁剪片段 |
| `batch` | 批量编辑（一次 IO，多条修改） |
| `restore` | 撤销（.bak 备份 + 多步历史快照） |

### 2.4 装饰与特效

| 命令 | 功能 |
|------|------|
| `keyframe` | 关键帧（缩放/位置/旋转/透明度/调色/音量） |
| `transition` | 转场效果 |
| `mask` | 蒙版（线性/圆形/心形/星形等） |
| `bg-blur` | 背景模糊 |
| `text-style` | 文本样式（阴影/描边/背景框） |
| `text-anim` / `image-anim` | 文本/图片入场出场动画 |
| `text-ranges` | 多样式文本（字级高亮字幕） |
| `mix-mode` | 混合模式（正片叠底/滤色/叠加等） |
| `audio-fade` | 音频淡入淡出 |
| `bubble-text` | 文本气泡/花字 |
| `add-filter` | 调色滤镜 |
| `add-cover` | 设置封面/缩略图 |
| `add-sfx` | 添加音效 |
| `chroma` | 绿幕/色度抠图 |

### 2.5 字幕与翻译

| 命令 | 功能 |
|------|------|
| `caption` | Whisper 自动生成字幕（真字幕对象，非文本伪装） |
| `import-srt` / `import-ass` | 导入 SRT/ASS 字幕 |
| `translate` | 多语言翻译克隆（Anthropic API） |

### 2.6 长视频切短

| 命令 | 功能 |
|------|------|
| `cut` | 从长视频切出指定时间段成为独立短片 |
| `concat` | 合并多个草稿到同一时间线 |
| `diff` | 比较两个草稿差异 |

### 2.7 模板系统

| 命令 | 功能 |
|------|------|
| `save-template` | 将片段保存为可复用模板 |
| `apply-template` | 将模板应用到另一工程 |

内置 6 个模板：`gold-title`、`end-card`、`subscribe-cta`、`hook-question`、`lower-third`、`caption-pop`

### 2.8 质量保障

| 命令 | 功能 |
|------|------|
| `lint` | Schema 感知的 CI 检查（字幕重叠/行长/缺失文件） |
| `version` | 检测草稿版本兼容性 |
| `migrate` | 跨版本 Schema 迁移 |
| `doctor` | 环境预检（Node/whisper/草稿目录） |
| `decrypt` | 解密（剪映 6.0+ 加密检测） |

### 2.9 枚举发现（AI Agent 友好）

| 命令 | 功能 |
|------|------|
| `enums --transitions` | 116 个转场效果 |
| `enums --masks` | 蒙版类型 |
| `enums --scene-effects` | 场景特效（912 个 slug） |
| `enums --image-intros` / `--image-outros` | 图片入场/出场动画 |
| `enums --text-intros` / `--text-outros` | 文本入场/出场动画 |
| `enums --filters` | 调色滤镜 |
| `enums --audio-effects` | 音效列表 |
| `enums --fonts` | 可用字体 |

共 **13 个分类 × 2 命名空间**（CapCut 国际版 + 剪映国内版），从 `enums.json`（~793KB）本地读取，无需联网。

### 2.10 集成方式

| 方式 | 说明 |
|------|------|
| **CLI** | `npm install -g capcut-cli`，全局可用 |
| **Library** | `import { loadDraft, lintDraft, saveDraft } from "capcut-cli"` 带类型、零依赖 |
| **Docker** | 官方 Dockerfile，挂载草稿目录即可运行 |
| **GitHub Action** | CI 中 lint 草稿文件 |
| **serve** | 无状态 JSONL 队列执行器（对接 n8n/Make/Coze） |
| **Claude Code Plugin** | `/plugin marketplace add` 一键集成 |
| **Shell Completions** | bash/zsh/fish 自动补全 |

---

## 三、技术架构

### 3.1 项目结构

```
capcut-cli/
├── src/
│   ├── index.ts          (118KB) CLI 入口，所有命令的 Commander 实现
│   ├── draft.ts          (9.4KB) 核心 Draft 类型定义 + 加载/保存/查找
│   ├── factory.ts        (42KB)  工厂方法：创建草稿/添加素材/模板/cut
│   ├── decorators.ts     (35KB)  装饰器：关键帧/转场/蒙版/动画/文本样式
│   ├── enums.ts          (2.7KB) 枚举发现逻辑
│   ├── enums.json        (793KB) 预提取的特效/转场/滤镜枚举数据
│   ├── lib.ts            (1.2KB) 公共库入口（可 import 使用）
│   ├── caption.ts        (7.7KB) Whisper 字幕生成
│   ├── translate.ts      (4.6KB) 多语言翻译
│   ├── render.ts         (11.6KB) ffmpeg 时间线代理渲染
│   ├── compile.ts        (8.6KB) 声明式 spec → 完整草稿
│   ├── lint.ts           (5.7KB) Schema 感知的 lint 检查
│   ├── srt.ts / ass.ts   SRT/ASS 字幕导入
│   ├── serve.ts          无状态 JSONL 队列执行器
│   ├── version.ts        版本检测
│   ├── decrypt.ts        解密逻辑
│   ├── time.ts           时间格式解析（1.5s/500ms/1:30 → 微秒）
│   ├── wikimedia.ts      Wikimedia Commons 素材抓取
│   └── ...
├── docs/draft-schema/    完整的 Schema 参考文档（7 个文件）
│   ├── 00-overview.md
│   ├── 01-tracks-and-segments.md
│   ├── 02-materials.md
│   ├── 03-keyframes-and-animations.md
│   ├── 04-effects-filters-stickers.md
│   └── 05-version-differences.md
├── skills/capcut-edit/   Claude Code Skill 文件
├── templates/            内置模板（gold-title/end-card 等）
├── examples/             端到端使用案例
└── test/                 36 个 node:test 测试用例
```

### 3.2 核心 TypeScript 类型定义

`draft.ts` 定义了完整的 draft_content.json 类型体系：

```typescript
// Draft 根结构
interface Draft {
  id: string;
  name: string;
  duration: number;       // 微秒
  fps: number;
  canvas_config: {
    width: number;
    height: number;
    ratio: string;        // "9:16" / "16:9" 等
  };
  tracks: Track[];
  materials: {
    videos: MaterialVideo[];
    audios: MaterialAudio[];
    texts: MaterialText[];
    speeds: Array<{ id: string; speed: number }>;
    material_animations: Array<Record<string, unknown>>;
    audio_fades: Array<Record<string, unknown>>;
    transitions: Array<Record<string, unknown>>;
    stickers?: Array<Record<string, unknown>>;
    video_effects?: Array<Record<string, unknown>>;
    [key: string]: Array<Record<string, unknown>>;
  };
  platform?: {
    app_source: string;   // "capcut" | "jianying_pro"
    app_version: string;
    os: string;
  };
}

// 轨道
interface Track {
  id: string;
  type: string;           // "video" | "audio" | "text" | "sticker" | "effect" | "filter"
  name: string;
  attribute: number;
  segments: Segment[];
}

// 片段（时间线上的每个元素）
interface Segment {
  id: string;
  material_id: string;            // 关联到 materials 中的具体素材
  target_timerange: Timerange;    // 在时间线上的位置
  source_timerange: Timerange;    // 从源素材中截取的范围
  speed: number;
  volume: number;
  visible: boolean;
  clip: {
    alpha: number;
    rotation: number;
    scale: { x: number; y: number };
    transform: { x: number; y: number };
  } | null;
  extra_material_refs: string[];  // 配套素材引用（speed/placeholder 等）
  render_index: number;
}
```

### 3.3 关键设计决策

1. **时间单位**：内部全部使用微秒（`start_us`、`duration_us`），CLI 接受 `1.5s`、`500ms`、`1:30` 等人类可读格式自动转换。

2. **轨道排序**：每次保存时自动将 tracks 数组规范化为 CapCut 期望的层顺序（video → audio → sticker → effect → filter → text），防止时间线布局错乱。

3. **文本内容编码**：文本素材的 `content` 字段是 JSON 字符串，内部包含 UTF-16LE 编码的字节范围。`updateTextContent()` 方法正确处理这种嵌套结构。

4. **备份机制**：每次写入前自动创建 `.bak` 备份，同时维护 `.capcut-cli-history/` 目录的多步快照（最近 20 次），支持 `restore --step N` 回滚。

5. **Dry-run 模式**：所有 mutating 命令支持 `--dry-run`，通过 `setDryRun()` 全局开关在 `saveDraft()` 层面拦截写入。

---

## 四、草稿 JSON 结构深度解析

### 4.1 文件位置

| 平台 | 路径 |
|------|------|
| **Windows (CapCut)** | `C:\Users\<用户名>\AppData\Local\CapCut\User Data\Projects\com.lveditor.draft\<id>\` |
| **macOS (CapCut)** | `~/Movies/CapCut/User Data/Projects/com.lveditor.draft/<id>/` |
| **macOS (剪映)** | `~/Movies/JianyingPro/User Data/Projects/com.lveditor.draft/<id>/` |
| **Linux (Wine/其他)** | 无官方支持，需手动指定路径 |

文件名：
- **CapCut 桌面版**：`draft_content.json`
- **macOS 剪映**：`draft_info.json`（实际内容结构相同）

### 4.2 顶层结构

```
draft_content.json
├── id                    UUID，工程唯一标识
├── name                  工程名称
├── duration              总时长（微秒）
├── fps                   帧率
├── canvas_config         画布配置（宽/高/比例）
├── platform              平台信息（app_source, app_version, os）
├── tracks[]              轨道数组（时间线的核心）
└── materials{}           素材字典（按类型分组）
```

### 4.3 轨道（Tracks）

轨道是时间线的组成单元，按类型分层：

```
tracks: [
  { type: "video",   segments: [...] },   // 主视频轨
  { type: "audio",   segments: [...] },   // 音频轨
  { type: "sticker", segments: [...] },   // 贴纸轨
  { type: "effect",  segments: [...] },   // 特效轨
  { type: "filter",  segments: [...] },   // 滤镜轨
  { type: "text",    segments: [...] },   // 文本/字幕轨
]
```

### 4.4 素材（Materials）

素材是实际媒体内容的仓库，按类型分组存储：

```
materials: {
  videos: [           // 视频/图片素材
    {
      id, path, material_name, type ("video"|"photo"),
      duration, width, height, has_audio, crop, ...
    }
  ],
  audios: [           // 音频素材
    {
      id, path, name, duration,
      type ("extract_music"|"music"|...), source_platform, ...
    }
  ],
  texts: [            // 文本素材（核心！内容在 content 字段）
    {
      id, type,
      content: "<JSON 字符串>",  // 包含 styles[] 和 text
      font_size, text_color, alignment,
      has_shadow, shadow_color, ...
    }
  ],
  speeds: [],         // 变速信息
  material_animations: [],  // 入场/出场动画
  audio_fades: [],    // 音频淡入淡出
  transitions: [],    // 转场效果
  stickers: [],       // 贴纸
  video_effects: [],  // 视频特效/滤镜
  ...
}
```

### 4.5 片段-素材关系（核心关联模型）

这是理解草稿结构最关键的部分。**Track.Segment** 和 **Material** 通过 `material_id` 关联：

```
Track.segments[i].material_id → Materials[videos|audios|texts|...].id
```

一个 Segment 包含：
- `material_id`：指向主素材
- `target_timerange`：在时间线上的位置（start, duration）
- `source_timerange`：从源素材中截取的范围（支持裁剪）
- `extra_material_refs[]`：指向配套素材（speed、placeholder_info、sound_channel_mapping、vocal_separation、canvas_color、material_color）

每个 Segment 创建时自动附带 4-6 个 companion materials。

### 4.6 文本内容的嵌套 JSON 结构

文本素材的 `content` 字段是一个 **JSON 字符串**（JSON-in-JSON），格式如下：

```json
{
  "styles": [
    {
      "range": [0, 14],          // UTF-16LE 字节范围
      "size": 24,                // 字号
      "bold": false,
      "italic": false,
      "underline": false,
      "fill": {
        "alpha": 1,
        "content": {
          "render_type": "solid",
          "solid": {
            "alpha": 1,
            "color": [1.0, 0.843, 0.0]  // RGB，0-1 范围
          }
        }
      }
    }
  ],
  "text": "实际的文字内容"
}
```

这解释了为什么 `capcut-cli` 的 `extractText()` 和 `updateTextContent()` 需要特殊处理——先 JSON.parse，修改后再 JSON.stringify。

### 4.7 版本兼容性

`capcut-cli` 通过 `platform.app_source` 和 `platform.app_version` 字段检测版本，在 `docs/draft-schema/05-version-differences.md` 中记录了不同版本间的 Schema 差异：

- **剪映 5.9 vs 6.0+**：6.0+ 对草稿文件加密，需解密后才能操作
- **CapCut 国际版**：`app_source: "capcut"`
- **剪映国内版**：`app_source: "jianying_pro"`，enum 命名空间不同

---

## 五、与 WelooAI 自动剪辑 Skill 的关系

### 5.1 WelooAI 的定位

经过广泛搜索，**未找到名为"WelooAI"的独立项目或产品**专门做剪映自动剪辑。这个名称可能是以下之一：

1. **waoowaoo (waooAI)** — GitHub 上 12K+ 星标的工业级 AI 影视生产平台（`github.com/waooAI/waoowaoo`），基于 Next.js + TypeScript，做短剧/漫画视频制作，从剧本→分镜→角色→视频生成，但与剪映草稿文件操作属于不同技术路线。

2. **用户自定义的 Skill 名称** — 可能是用户基于现有工具（如 capcut-cli、pyJianYingDraft、jianying-editor-skill 等）自行封装的 Skill，取了 "WelooAI" 这个名字。

### 5.2 剪映自动剪辑 Skill 生态

当前剪映/CapCut 自动化剪辑生态的主要玩家：

| 项目 | 语言 | 方式 | Agent 集成 |
|------|------|------|------------|
| **capcut-cli** (本报告对象) | TypeScript/Node | CLI 直接读写 draft_content.json | Claude Code Plugin + 任意 LLM |
| **pyJianYingDraft** (3K stars) | Python | Python 库写 draft_content.json | 无原生 Agent 集成 |
| **pyCapCut** | Python | CapCut 国际版 Python 库 | 无原生 Agent 集成 |
| **capcut-mate** (1.1K stars) | Python/FastAPI | HTTP API 服务器，后端调 pyJianYingDraft | OpenClaw Skill + Coze/n8n |
| **VectCutAPI** (原 CapCutAPI) | Python/Flask | HTTP + MCP Server | MCP 协议 |
| **jianying-editor-skill** | Python | pyJianYingDraft + UI Automation | Claude Code/OpenClaw Skill |
| **cutcli** | Go | 闭源 CLI + MCP Server | Cursor/Claude Code/OpenClaw |
| **JyDraft** | C# | C# SDK + 云端渲染 API | REST API |

### 5.3 共性原理

所有这些工具的核心原理一致：

```
大模型/Agent
    ↓ 生成 JSON 指令
工具/CLI/SDK
    ↓ 读写 draft_content.json
剪映/CapCut
    ↓ 读取草稿文件
GUI 打开草稿 → 人工审核 → 渲染导出
```

**关键洞察**：所有工具都是直接操作 `draft_content.json`，不经过任何官方 API。这是可行的因为：
- 剪映/CapCut 将工程文件以明文 JSON 存储在本地磁盘
- 关闭工程后，软件不再持有文件锁
- 修改 JSON 后重新打开工程，软件会重新读取

### 5.4 capcut-cli 在生态中的差异化优势

相比于同类工具，`capcut-cli` 的独特之处：

1. **零运行时依赖**：Node ≥ 18 内置 API，不需要 `pip install` 一堆包
2. **JSON-in/JSON-out**：天然适合 Agent pipeline，不需要解析自然语言输出
3. **不启动服务**：没有 HTTP 守护进程、没有 MCP Server、没有端口
4. **双命名空间**：CapCut 国际版 + 剪映国内版，一个二进制搞定
5. **可导入为库**：`import { loadDraft, saveDraft } from "capcut-cli"` 直接编程调用
6. **枚举发现**：13 类 × 2 命名空间的枚举数据，Agent 可以自发现可用特效
7. **声明式编译**：`compile` 命令可以直接从 JSON spec 生成完整草稿

---

## 六、改装为 Agent 可调用工具的可行性分析

### 6.1 结论：**高度可行，开箱即用**

`capcut-cli` 从设计之初就以 **"被 Agent 驱动"** 为目标，有几个层面已经准备好了：

### 6.2 现有的 Agent 集成方案

#### 方案一：Claude Code Plugin（官方已支持）

```bash
/plugin marketplace add https://github.com/renezander030/capcut-cli
/plugin enable capcut-cli
```

安装后 Agent 自动获得 `/capcut-cli:capcut-edit` Skill，理解所有命令、渐进式导航模式和草稿路径发现。

#### 方案二：直接 CLI 调用（任何 Agent）

任何能执行 shell 命令的 Agent 都可以直接调用：

```bash
# Agent 工作流示例
capcut info ./project                    # 获取概况
capcut segments ./project --track text   # 获取字幕列表
capcut set-text ./project <id> "新文字"  # 修改字幕
capcut cut ./project 1:00 2:00 --out ./short.json  # 切短视频
```

JSON 输出使得 Agent 无需解析人类语言，直接处理数据结构。

#### 方案三：作为 Node 库导入

```typescript
import { loadDraft, findSegment, saveDraft, updateTextContent } from "capcut-cli";

const { draft, filePath } = loadDraft("./project/draft_content.json");
const result = findSegment(draft, "a1b2c3");
if (result) {
  const { segment } = result;
  // 修改...
  saveDraft(filePath, draft);
}
```

#### 方案四：JSONL 队列执行器

```bash
echo '{"cmd":"set-text","id":"a1b2c3","text":"第一行"}
{"cmd":"shift-all","offset":"+0.3s","track":"text"}' | capcut serve
```

可集成到 n8n/Make/Coze 等自动化平台。

### 6.3 改装为 OpenClaw Agent 可调用工具的步骤

如果要封装成 OpenClaw Skill，只需以下几步：

```markdown
# 1. 安装 CLI
npm install -g capcut-cli

# 2. 创建 Skill 文件 (.openclaw/skills/capcut-edit/SKILL.md)
# 包含：
#   - 草稿目录自动发现逻辑 (macOS/Windows)
#   - 常用命令映射
#   - 渐进式导航模式 (info → tracks → segments → detail)
#   - 错误处理（草稿被锁定/文件不存在等）

# 3. 提供工具脚本
# tools/find_drafts.sh  — 列出本机所有草稿
# tools/inspect.sh      — 查看草稿详情
# tools/edit_text.sh    — 修改字幕
# tools/cut_short.sh    — 切短视频
```

### 6.4 注意事项

1. **草稿锁定**：编辑前必须关闭剪映/CapCut 中该工程。这是最常见的坑。
2. **素材路径**：`add-video/audio` 会将素材复制到草稿的 `assets/` 目录，需要确保素材文件存在。
3. **版本兼容**：剪映 6.0+ 对草稿加密，需要先解密（`capcut decrypt` 目前仅支持检测）。
4. **导出限制**：`export --batch` 目前仅 macOS（AppleScript），Windows 需要手动渲染。
5. **Node ≥ 18**：需要确保 Agent 运行环境有 Node 18+。

### 6.5 与其他方案的功能矩阵对比

| 能力 | capcut-cli (Node) | pyJianYingDraft (Python) | capcut-mate (FastAPI) | VectCutAPI (MCP) |
|------|:---:|:---:|:---:|:---:|
| **零依赖运行** | ✅ (仅 Node 18+) | ❌ (多个 Python 包) | ❌ (需起服务) | ❌ (Flask + MCP) |
| **Agent 自发现** | ✅ (enums 13 类) | ❌ | ❌ | 部分 |
| **JSON 输出** | ✅ (默认) | 需自行序列化 | REST JSON | MCP JSON |
| **双命名空间** | ✅ (--jianying) | JianYing only | ✅ | ✅ |
| **Schema 文档** | ✅ (完整) | 部分 | 部分 | 部分 |
| **声明式编译** | ✅ (compile) | ❌ | ❌ | ❌ |
| **ffmpeg 预览** | ✅ (render) | ❌ | ❌ | ❌ |
| **模板系统** | ✅ | 部分 | ❌ | ❌ |
| **代码库可导入** | ✅ | ✅ | ❌ | ❌ |
| **CI/CD 集成** | ✅ (GitHub Action) | ❌ | ❌ | ❌ |
| **Docker** | ✅ | ❌ | ✅ | ❌ |

---

## 七、关键代码逻辑摘录

### 7.1 加载草稿（draft.ts）

```typescript
export function loadDraft(path: string): { draft: Draft; filePath: string } {
  const filePath = findDraft(path);  // 自动探测 draft_content.json / draft_info.json
  rawOriginal = readFileSync(filePath, "utf-8");
  const draft = JSON.parse(rawOriginal) as Draft;
  return { draft, filePath };
}
```

### 7.2 保存草稿（draft.ts）

```typescript
export function saveDraft(filePath: string, draft: Draft): void {
  if (dryRun) { sortTracks(draft); return; }  // dry-run 不写磁盘
  const bakPath = `${filePath}.bak`;
  if (existsSync(filePath)) {
    const original = rawOriginal ?? readFileSync(filePath, "utf-8");
    writeFileSync(bakPath, original, "utf-8");  // 创建 .bak 备份
    writeHistorySnapshot(filePath, original);    // 写入多步历史
  }
  sortTracks(draft);  // 规范化轨道顺序
  const indent = detectIndent(rawOriginal);  // 保留原始缩进风格
  writeFileSync(filePath, JSON.stringify(draft, null, indent), "utf-8");
}
```

### 7.3 添加文本（factory.ts）

```typescript
export function addText(draft, _filePath, opts): { segmentId, materialId, trackId } {
  // 1. 生成 UUID
  // 2. 查找或创建 text 轨
  // 3. 创建 companion materials (speed/placeholder/scm/vocal)
  // 4. 构建 text material（content 是 JSON 字符串，UTF-16LE 编码）
  // 5. 创建 segment 关联 material_id + target_timerange
  // 6. 推入 track.segments
}
```

### 7.4 时间格式解析（time.ts）

CLI 接受多种格式自动转为微秒：
- `1.5s` → 1,500,000 us
- `500ms` → 500,000 us
- `1:30` → 90,000,000 us
- `+0.5s` / `-1s` → 相对偏移

### 7.5 文本内容处理（draft.ts）

```typescript
// 从 content JSON 字符串中提取纯文本
export function extractText(content: string): string {
  try {
    const parsed = JSON.parse(content);
    if (parsed.text) return parsed.text;
  } catch {
    return content.replace(/<[^>]*>/g, "").replace(/\[|\]/g, "").trim();
  }
  return content;
}

// 修改文本内容（保持样式不变，更新 range）
export function updateTextContent(content: string, newText: string): string {
  const parsed = JSON.parse(content);
  parsed.text = newText;
  if (parsed.styles?.length > 0) {
    const encoded = Buffer.from(newText, "utf16le");
    parsed.styles[0].range = [0, encoded.length];
  }
  return JSON.stringify(parsed);
}
```

---

## 八、总结与建议

### 8.1 项目评价

| 维度 | 评分 | 说明 |
|------|------|------|
| 功能完整度 | ★★★★★ | 覆盖了剪映 90%+ 的核心编辑功能 |
| Agent 友好度 | ★★★★★ | 原生 JSON 输出 + 枚举发现 + 渐进式导航 |
| 代码质量 | ★★★★★ | 完整 TypeScript 类型定义、36 个测试、Biome lint |
| 文档质量 | ★★★★★ | 中英双语 README、7 篇 Schema 文档、端到端示例 |
| 维护活跃度 | ★★★★★ | 活跃更新（已发布 10 个大版本）、社区投票决定路线图 |
| 可改装性 | ★★★★★ | CLI/Library/Docker/GitHub Action/Plugin 五种形态 |

### 8.2 改装为 Agent 工具的建议

1. **首选方案**：直接使用 CLI 调用，Agent 通过 `capcut <command>` 执行操作
2. **如果 Agent 在 Node 环境**：可直接 `import` library 函数，避免 `exec` 开销
3. **如果 Agent 需要批量处理**：使用 `capcut serve` 的 JSONL 队列模式
4. **如果需要快速原型**：已有 Claude Code Plugin 可参考，或基于 `jianying-editor-skill` 的架构改编

### 8.3 与现有知识库的关联

本报告应与以下笔记交叉引用：
- [[剪映草稿工程文件结构]] — 草稿文件路径、目录结构、JSON Schema 基础
- [[3.Agent/_Index|3.Agent 索引]] — AI Agent 相关概念
- [[7.Coding/_Index|7.Coding 索引]] — 编程工具与平台

---

## 参考来源

- [capcut-cli GitHub](https://github.com/renezander030/capcut-cli) — 主要调研对象
- [pyJianYingDraft](https://github.com/GuanYixuan/pyJianYingDraft) — Python 剪映草稿库(3K stars)
- [capcut-mate](https://github.com/Hommy-master/capcut-mate) — FastAPI 剪映自动化助手(1.1K stars)
- [jianying-editor-skill](https://github.com/luoluoluo22/jianying-editor-skill) — 剪映 Agent Skill
- [VectCutAPI](https://github.com/sun-guannan/VectCutAPI) — MCP 协议的剪映 API
- [cutcli](https://cutcli.com/) — Go 闭源剪映 CLI + MCP Server
- [JyDraft](https://github.com/HTWMedia/JyDraft) — C# 剪映草稿 + 云端渲染
- [waoowaoo](https://github.com/waooAI/waoowaoo) — AI 影视生产平台(12K stars)