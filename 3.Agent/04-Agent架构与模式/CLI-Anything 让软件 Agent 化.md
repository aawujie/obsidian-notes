# CLI-Anything：让任意软件 Agent 化

> 项目路径：`/Users/apple/code/2.agent/CLI-Anything`
> 来源：HKUDS/CLI-Anything

## 一句话

**把 GUI 软件转成结构化 CLI，让 AI Agent 像用 `git` 一样操作 GIMP、Blender、LibreOffice 等专业软件。**

*Today's Software Serves Humans. Tomorrow's Users will be Agents.*

---

## 核心价值

| 痛点 | CLI-Anything 的方案 |
|------|---------------------|
| AI 无法可靠使用真实工具 | 直接对接真实软件后端（Blender、LibreOffice、FFmpeg），功能不打折 |
| UI 自动化脆弱易崩 | 不用截图、不点坐标，纯命令行，结构化接口 |
| Agent 需要结构化数据 | 每个命令支持 `--json` 输出 |
| 定制集成成本高 | 一个命令自动生成完整 CLI |

---

## 7 阶段自动化流水线

```bash
/cli-anything <软件路径或GitHub仓库>
```

| 阶段 | 内容 |
|------|------|
| Phase 1 | 分析源码 → 找后端引擎、GUI→API 映射、数据格式 |
| Phase 2 | 设计 CLI 架构 → 命令分组、状态模型、输出格式 |
| Phase 3 | 实现 → Click CLI、REPL、undo/redo、`--json` |
| Phase 4 | 测试计划 → 写 TEST.md |
| Phase 5 | 测试实现 → 单元 + E2E，调用真实软件验证 |
| Phase 6 | 测试文档 → pytest 结果写入 TEST.md |
| Phase 7 | 发布 → setup.py、pip install -e . |

---

## 使用示例

### 示例 1：Agent 生成 PDF 报告

```bash
cli-anything-libreoffice document new -o report.json --type writer
cli-anything-libreoffice --project report.json writer add-heading -t "Q1 报告" --level 1
cli-anything-libreoffice --project report.json writer add-table --rows 5 --cols 3
cli-anything-libreoffice --project report.json export render report.pdf -p pdf
```

### 示例 2：Agent 剪辑视频

```bash
cli-anything-shotcut project new -o edit.json
cli-anything-shotcut --project edit.json media add intro.mp4
cli-anything-shotcut --project edit.json timeline add-clip 0 0 10
cli-anything-shotcut --project edit.json transition add --type fade --duration 1
cli-anything-shotcut --project edit.json export render final.mp4
```

### 示例 3：Agent 做海报

```bash
cli-anything-gimp project new --width 1920 --height 1080 -o poster.json
cli-anything-gimp --project poster.json layer add -n "Background" --type solid --color "#1a1a2e"
cli-anything-gimp --project poster.json export render poster.png
```

---

## 项目结构

```
CLI-Anything/
├── cli-anything-plugin/     # Claude Code 插件
│   ├── HARNESS.md           # 方法论 SOP（必读）
│   ├── repl_skin.py         # 统一 REPL 界面
│   └── commands/
├── audacity/agent-harness/  # 音频编辑
├── shotcut/agent-harness/   # 视频编辑
├── obs-studio/agent-harness/# 直播推流
├── gimp/agent-harness/      # 图像编辑
├── blender/agent-harness/   # 3D
├── inkscape/agent-harness/  # 矢量图
├── libreoffice/agent-harness# 办公
├── kdenlive/agent-harness/  # 视频
└── drawio/agent-harness/   # 流程图
```

每个 harness：

```
agent-harness/
├── setup.py
└── cli_anything/<software>/
    ├── core/           # project, session, export...
    ├── utils/          # 后端封装、repl_skin
    ├── xxx_cli.py      # Click 入口
    └── tests/
```

---

## 技术要点

1. **真实软件后端**：生成 ODF/MLT XML/SVG 等标准格式，交给真实软件渲染，不造轮子
2. **双模式**：REPL（交互） + 子命令（脚本），无参数默认进 REPL
3. **ReplSkin**：统一 REPL，Banner、提示符、历史、彩色输出
4. **Agent 友好**：`--json` 输出，`--help` 自描述
5. **严格测试**：后端缺失时测试失败而非跳过，输出需做格式校验

---

## HARNESS.md 关键教训

| 教训 | 说明 |
|------|------|
| Use the real software | 必须调用真实应用，不能替代实现 |
| Rendering Gap | 只改项目文件而导出工具不原生，效果会丢 |
| Filter Translation | 格式映射（如 MLT→ffmpeg）注意重复滤镜、参数差异 |
| Timecode Precision | 29.97fps 用 `round()` 不用 `int()`，测试 ±1 帧容忍 |
| Output Verification | 不能只看 exit 0，要校验 magic bytes、结构 |

---

## 适用场景

- GitHub 仓库 → 转成 Agent 可用 CLI
- AI/ML 平台 → Stable Diffusion、ComfyUI、Fooocus
- 创意工具 → Blender、GIMP、OBS、Audacity、Shotcut
- 办公/企业 → LibreOffice、Grafana、GitLab

---

## 技术栈

- Python 3.10+
- Click ≥ 8.0
- prompt-toolkit
- pytest

---

## 快速开始

```bash
# Claude Code 插件
/plugin marketplace add HKUDS/CLI-Anything
/plugin install cli-anything

# 为任意软件生成 CLI
/cli-anything ./gimp
/cli-anything https://github.com/blender/blender

# 安装使用
cd gimp/agent-harness && pip install -e .
cli-anything-gimp --help
```

---

## 相关

- [[pyJianYingDraft - 剪映自动化草稿工具]] - 同属「Agent 操控专业软件」思路
- 方法论：`cli-anything-plugin/HARNESS.md`
