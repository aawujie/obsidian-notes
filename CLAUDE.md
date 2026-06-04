# DeepRoute 知识库

> Schema document — Agent 每次会话开始必读，配合 wiki/index.md。
> 更新于: 2026-06-04

## Scope

覆盖:
- AI / LLM / Agent 理论与实践 (`3.Agent/`, 612 篇)
- 编程 / 深度学习 / 基础设施 (`7.Coding/`, 147 篇)
- 数学基础 (`2.Math/`, 78 篇)
- 机器人 / 具身智能 (`4.Robot/`, 170 篇)
- 金融 / 投资 (`5.Finance/`, 711 篇)
- 读书笔记 (`6.BookNotes/`, 404 篇)
- AI 摘要与跨领域洞察 (`7.AI Summary/`, 1 篇)
- 英语学习 (`1.English/`, 42 篇)
- 心智与成长 (`9.Mindset/`, 36 篇)
- 项目文档 (`8.Projects/`, 6 篇)

排除:
- 日常任务与计划 (`0.DailyTask/`) — 日志性质，非知识库
- Chaos/ — 未归类的草稿和实验性内容
- `.obsidian/` — Obsidian 配置，不属于知识库
- `Resources/` — 非 md 资源文件集中存放，不在知识库范围内
- `wiki/` — llm-wiki 编译产物，Agent 只读

## Operations

本知识库遵循 llm-wiki skill 的五大操作: `compile`, `ingest`, `query`, `lint`, `audit`。
每次操作在 `log/YYYYMMDD.md` 中追加一条记录。

## 目录映射

现有目录在 llm-wiki 模式中的角色:

| 现有目录                  | llm-wiki 角色               | Agent 权限         |
| --------------------- | ------------------------- | ---------------- |
| `3.Agent/`            | wiki/concepts (AI/LLM)    | 可读可写             |
| `7.Coding/`           | wiki/concepts (编程)        | 可读可写             |
| `2.Math/`             | wiki/concepts (数学)        | 可读可写             |
| `4.Robot/`            | wiki/concepts (机器人)       | 可读可写             |
| `5.Finance/`          | wiki/concepts (金融)        | 可读可写             |
| `7.AI Summary/`       | wiki/concepts + summaries | 可读可写             |
| `1.English/`          | wiki/concepts (英语)        | 可读可写             |
| `9.Mindset/`          | wiki/concepts (心智)        | 可读可写             |
| `8.Projects/`         | wiki/concepts (项目)        | 可读可写             |
| `6.BookNotes/《书名》/`   | wiki/summaries (书籍摘要)     | 可读可写             |
| `6.BookNotes/Weread/` | raw/papers (微信读书剪藏)       | **只读，Agent 不可写** |
| `Clippings/`          | raw/articles (网页剪藏)       | 可读可写             |
| `Chaos/`              | raw/notes (未归类草稿)         | **只读，Agent 不可写** |
| `wiki/`               | wiki/compile (编译产物)       | **只读，Agent 不可写** |
| `audit/`              | audit (人类反馈)              | 可写 (audit op)    |
| `log/`                | log (操作日志)                | 可写 (每次操作追加)      |
| `outputs/queries/`    | outputs (查询答案)            | 可写 (query op)    |
| `Resources/`          | resources (非md资源)         | **只读，Agent 不可写** |

**关键规则**: `6.BookNotes/Weread/`, `Chaos/`, `wiki/`, `Resources/` 是 raw/资源/编译区——Agent 只能读取引用，绝不能修改或覆盖其中的文件。

## 命名约定

### 页面命名
- **概念页** (3.Agent, 7.Coding, 2.Math 等): Title Case 混合中英文，如 "Embedding全面理解"、"注意力机制详解"、"Transformer架构从零理解"
- **书籍目录** (6.BookNotes/): 《书名》格式，如 《救猫咪》、《因子投资：方法与实践》
- **Folder-split 概念**: 当单页超过 ~1200 字，拆为 `concepts/<topic>/index.md` + 子页面
- **实体页**: Proper names，如 "Andrej Karpathy"、"PyTorch"、"Transformer"

### Wikilinks
- 使用 `[[Page Title]]` 精确匹配页面标题 (Obsidian 默认 shortest path 匹配)
- Folder-split 页面链接到 index: `[[3.Agent/index|3.Agent 索引]]`
- 每篇文章内，同一页面只链接前两次提及，不要重复链接

### Frontmatter
每个 wiki 页面应有 YAML frontmatter:
```yaml
---
title: <页面标题>
type: concept | entity | summary
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: [列出引用的 raw/ 来源]
tags: [相关标签]
---
```

### 图表和公式
- 流程/架构/层级图 → **mermaid**，不使用 ASCII art
- 数学公式 → **KaTeX**: inline `$...$` 或 block `$$...$$`

### Raw 文件策略
- 小文本源 (md, txt, 小 PDF) → 直接放入 `Clippings/` 或 `6.BookNotes/Weread/`
- 大文件 (>10MB) → 在 `Clippings/` 中创建指针 `.md` 文件，注明 `external_path`

### 资源文件规则

**所有非 md 文件统一放在 `Resources/` 下**，md 笔记中只做引用，不内嵌二进制资源。

| 目录 | 文件类型 | 说明 |
|------|---------|------|
| `Resources/images/` | png, jpg, jpeg | 所有配图，保留原始目录结构 |
| `Resources/marimo/` | .py | Python notebook (marimo) |
| `Resources/notebooks/` | .ipynb | Jupyter notebook |
| `Resources/html/` | .html | 交互式可视化 |
| `Resources/papers/` | .pdf | 论文 PDF |
| `Resources/slides/` | .pptx | PPT 课件 |
| `Resources/documents/` | .doc, .docx, .xlsx | Office 文档 |
| `Resources/text/` | .txt | 文本文件 |

**marimo 启动**: `marimo edit <file> --host 0.0.0.0 -p 8002 --headless`

**marimo 规则**: 每个 cell 是独立函数，**同一变量名不能在多个 cell 中定义**（含循环变量）。各 cell 用前缀区分，如 `F`/`F2`/`iF`。

**引用方式**: Obsidian wikilink 按文件名跨 vault 解析，推荐使用 `![[filename.ext]]` 或 `[[filename.ext]]`，无需写完整路径。

### Python 环境

项目使用 uv 管理 Python 环境：
- **虚拟环境**: `.venv/`（git 忽略）
- **依赖配置**: `pyproject.toml`
- **激活**: `source .venv/bin/activate` 或 `uv run <command>`
- **marimo 启动**: `uv run marimo edit Resources/marimo/<file> --host 0.0.0.0 -p 8002`

## 现有文章清单

### 3.Agent — AI/LLM 知识库 (612 篇)

#### 01-模型基础
- [[Transformer架构从零理解]] — Transformer 入门
- [[Transformer 注意力机制详解]] — 注意力核心原理
- [[Embedding全面理解]] — 嵌入层详解
- [[位置编码从零理解]] — Positional Encoding
- [[RoPE旋转位置编码详解]] — RoPE 旋转编码
- [[Flash Attention 详解 - 李宏毅]] — Flash Attention
- [[稀疏自编码器 Sparse Autoencoder]] — 可解释性
- [[Qwen3-8B 模型结构解析]] — 模型架构
- [[Gemma4-12B-调研报告]] — Gemma 4 12B 调研

#### 02-训练与微调
- LoRA / DPO / GRPO 等微调技术

#### 03-推理与部署
- KV Cache / MoE / 量化 (TurboQuant)

#### 04-Agent架构与模式
- Agent 设计模式、架构调研

#### 05-项目文档 ~ 06-OpenClaw
- minimind / EvoMap / OpenClaw-MC

#### 07-工具与平台
- Cursor / 提示词 / API 集成

> 完整清单见 [[3.Agent/_Index|3.Agent 索引]]

### 7.Coding — 编程知识库 (147 篇)

#### 01-深度学习
- CNN / RNN / PyTorch / NLP / 语音

#### 02-后端开发
- Nest.js / Supabase

#### 03-电商与建站

#### 04-项目文档

#### 05-基础设施
- Docker / Prometheus / Grafana

#### 06-工具与平台

#### 07-网络安全

#### 08-测试与质量

#### 09-杂项与参考

> 完整清单见 [[7.Coding/_Index|7.Coding 索引]]

### 2.Math — 数学基础 (78 篇)
- 01-线性代数: SVD / 特征值 / 傅里叶变换 / 行列式
- 02-微积分
- 04-泛函分析
- 05-机器学习数学

### 4.Robot — 机器人/具身智能 (170 篇)
- Control / DRL / ML&DL

### 5.Finance — 金融 (711 篇)
- 00-因子投资
- 01-交易与策略
- 02-加密货币
- 03-计量经济学
- 04-金融理论
- 05-理财与财富建设
- 06-股票与投资基础
- concepts / 投研日记 / PandaAI官方

### 7.AI Summary — 跨领域洞察 (1 篇)
- [[谋士为何不自己当主公]]

### 9.Mindset — 心智与成长 (36 篇)
- 财富自由 / 自信重塑 / 低谷与心态 / 生存真相

### 8.Projects — 项目文档 (6 篇)
- 水滴项链录音器 / hackingtool 调研 / PandaFactor 调研 / code 项目索引

### 6.BookNotes — 读书笔记 (404 篇)
- 《因子投资》 / 《救猫咪》 / 《故事经济学》 / 《九宫格写作》 / 《深度学习》 / 《关键对话》 / 《思考，快与慢》 等

> 完整清单见各书目录的 index 或主笔记

### 1.English — 英语学习 (42 篇)
- 口语提升 / 流利度框架 / 学习方法 / 听力 / GRE / 词汇辨析

## 开放研究问题

- 数学与深度学习概念之间的交叉引用尚不完整 (2.Math ↔ 7.Coding ↔ 3.Agent)
- 金融板块已大幅扩充 (711 篇)，需要质量审核和交叉引用
- 读书笔记中的关键概念未充分提取为独立 concept 页
- Clippings 中的文章尚未系统地 ingest 到 wiki 概念页
- 部分页面缺少 frontmatter
- 7.AI Summary 缩减为 1 篇，原内容可能已迁移至其他目录

## 研究缺口

待 ingest 的来源:
- [ ] 强化学习系统笔记 → 补充 4.Robot/DRL
- [ ] 金融内容质量审核 → 5.Finance 已大量扩充，需查漏补缺
- [ ] Transformer 最新进展论文 → 补充 3.Agent/01-模型基础
- [ ] 英语学习方法论整理 → 1.English 已有 42 篇，可提取系统性框架

## Audit backlog

待首次 lint 后填写统计。

## Polymarket 预测市场工具

当用户提到 Polymarket、预测市场、押注概率、市场价格等关键词时，使用 polymarket skill。

**脚本位置**: `/home/dr/.openclaw/workspace/skills/polymarket-api/scripts/polymarket.py`

**需要代理**: 调用前确保 `https_proxy=http://127.0.0.1:7890` 已设置（mihomo 运行中）。

**用法**:
```bash
export https_proxy=http://127.0.0.1:7890 http_proxy=http://127.0.0.1:7890
python3 /home/dr/.openclaw/workspace/skills/polymarket-api/scripts/polymarket.py --top          # 热门市场
python3 /home/dr/.openclaw/workspace/skills/polymarket-api/scripts/polymarket.py --search "关键词" # 搜索
python3 /home/dr/.openclaw/workspace/skills/polymarket-api/scripts/polymarket.py --slug "slug"    # 特定市场
python3 /home/dr/.openclaw/workspace/skills/polymarket-api/scripts/polymarket.py --events        # 事件列表
```

**价格含义**: outcomePrices 0-1 代表概率，0.65 = 65%概率。

## Notes for the LLM

- **语言**: 中文为主，技术术语保留英文原词。概念页标题可用中英混合
- **深度**: 假设读者技术素养较高，不需要过度通俗化，但应提供直觉解释
- **矛盾处理**: 当不同来源说法矛盾时，在页面中标注矛盾点，链接到各来源，不要只选一方
- **现有 _Index.md**: 3.Agent 和 7.Coding 已有 `_Index.md`，目前保留原名不改 `index.md`，后续可考虑统一
- **Notion 导入文件**: 部分文件来自 Notion 导入，带有 `notion-id` frontmatter，保留不动
- **文件创建规则**: 必须在现有目录映射中创建文件，禁止自创新目录（如 `docs/`）