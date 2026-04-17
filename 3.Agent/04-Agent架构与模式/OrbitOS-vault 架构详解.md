# OrbitOS-vault 架构详解

> **来源**：AI 助手分析整理  
> **仓库位置**：`~/Documents/OrbitOS-vault/`  
> **类型**：个人知识管理（PKM）框架模板  
> **分析日期**：2026-02-21

---

## 📊 整体架构图

```
OrbitOS-vault/
│
├── 📥 输入层 (Input)
│   ├── 00_Inbox/              # 快速收集箱
│   └── 10_Daily/              # 每日笔记（时间线入口）
│
├── 📚 知识层 (Knowledge)
│   ├── 20_Project/            # 项目（行动导向）
│   ├── 30_Research/           # 研究（永久参考）
│   ├── 40_Wiki/               # 概念（原子知识）
│   └── 50_Resources/          # 资源（curated 内容）
│
├── 📋 输出层 (Output)
│   ├── 90_Plans/              # 执行计划
│   └── 99_System/             # 系统配置
│       ├── Bases/             # 数据视图定义
│       ├── Templates/         # 笔记模板
│       └── Prompts/           # AI 提示词
│
└── 🤖 AI 配置层 (AI Config)
    ├── AGENTS.md              # AI 行为规范
    ├── CLAUDE.md              # Claude 专用配置
    └── GEMINI.md              # Gemini 专用配置
```

---

## 🏗️ 核心设计原则

### 1️⃣ 扁平结构 > 层级结构

```
❌ 传统笔记（层级分类）
Projects/
  └── Finance/
      └── FactorInvesting/
          └── 项目.md

✅ OrbitOS（扁平 + 链接）
20_Project/
  └── 因子投资研究.md  ← frontmatter: area: "[[金融]]"
```

**为什么？**
- 文件夹层级一旦建立就很难改
- 链接可以随时调整，更灵活
- 一个项目可以链接到多个领域

---

### 2️⃣ Frontmatter 元数据驱动

每个笔记都有结构化元数据：

```yaml
---
type: project           # 类型：project/inbox/wiki/research
status: active          # 状态：active/on-hold/done/processed
area: "[[金融]]"        # 所属领域（wikilink）
priority: P2            # 优先级：P0/P1/P2/P3
due: 2026-03-01         # 截止日期
tags: [因子投资，量化]   # 标签
---
```

**作用**：
- Bases 插件根据这些字段过滤、排序、分组
- AI 根据这些字段理解笔记用途

---

### 3️⃣ 双向链接网络

```
每日笔记 ←[[链接]]→ 项目 ←[[链接]]→ 概念
    ↓                    ↓
  进展更新            相关研究
```

**示例**：
```markdown
# 2026-02-21 (每日笔记)

## 今天做了什么
- 推进了 [[因子投资研究]] 项目
- 学习了 [[MM 定理]] 和 [[有效市场假说]]

# 因子投资研究 (项目)

## 进展
- 2026-02-21: [[2026-02-21]] - 完成 [[MM 定理]] 笔记
```

---

## 📁 各层详细架构

### 📥 输入层 (Input Layer)

#### `00_Inbox/` - 收集箱

**用途**：快速捕获想法，稍后处理

**模板** (`Inbox_Template.md`)：
```yaml
---
type: inbox
status: captured        # captured → processing → processed
topic:                  # 主题
priority:               # 优先级
due:                    # 截止日期
source:                 # 来源（链接/书名/人名）
related:                # 相关笔记（wikilink）
tags:
  - inbox
---
```

**工作流**：
```
1. 有想法 → 快速记录到 00_Inbox/xxx.md
2. 定期处理 → 用 /kickoff 转为项目，或移动到 Research/Wiki
3. 标记 status: processed → 从 Inbox 视图消失
```

---

#### `10_Daily/` - 每日笔记

**用途**：时间线枢纽，连接所有笔记

**模板** (`Daily_Note.md`)：
```yaml
---
date: {{date}}
day: {{date:dddd}}
week: {{date:ww}}
---
# {{date:YYYY-MM-DD}}

## Priorities
- [ ] 最重要任务 1
- [ ] 最重要任务 2
- [ ] 最重要任务 3

## Log
* 时间线日志（随时记录）

## Notes
* 临时笔记

## AI Digest
* AI 生成的摘要/建议

## Related Projects
- [[项目 1]] - 今天做了什么
- [[项目 2]] - 遇到什么问题

---

**Energy:** ⚡⚡⚡⚡⚡ | **Focus:** 🎯🎯🎯🎯🎯
```

**作用**：
- 📅 时间线索引（按日期回顾）
- 🔗 项目进展追踪
- 📝 快速日志（bullet journal）

---

### 📚 知识层 (Knowledge Layer)

#### `20_Project/` - 项目

**用途**：行动导向的任务集合

**模板** (`Project_Template.md`)：
```yaml
---
title: 因子投资研究
type: project
status: active
area: "[[金融]]"
priority: P2
due: 2026-06-30
created: 2026-02-21
---
# 因子投资研究

## Context

**Objective:** 构建 A 股因子回测系统

**Success Metrics:**
- [ ] 复现 Fama-French 三因子
- [ ] 回测年化收益 > 15%
- [ ] 最大回撤 < 20%

**Key Constraints:**
- Timeline: 4 个月
- Resources: 聚宽数据、Python
- Dependencies: 需要先学 [[MM 定理]]

---

## Actions

### Phase 1: 理论学习
- [ ] 阅读《因子投资：方法与实践》
- [ ] 学习 [[EMH]] 和 [[MM 定理]]
- [ ] 理解 Fama-French 三因子

### Phase 2: 数据收集
- [ ] 获取 A 股历史数据
- [ ] 清洗财务数据
- [ ] 计算因子值

### Phase 3: 回测实现
- [ ] 编写回测框架
- [ ] 实现因子计算
- [ ] 性能分析

---

## Progress

- 2026-02-21: [[2026-02-21]] - 项目启动，完成 [[MM 定理]] 笔记

---

## Related
- [[有效市场假说]]
- [[资本资产定价模型]]

---

## Notes
* 自由记录区
```

**C.A.P. 布局**：
- **Context** - 目标、成功标准、约束
- **Actions** - 分阶段任务清单
- **Progress** - 进展日志（链接到每日笔记）

---

#### `30_Research/` - 永久参考

**用途**：长期有价值的参考资料

**示例**：
```
30_Research/
├── 有效市场假说.md
├── MM 定理.md
├── Python 编程规范.md
└── 机器学习算法大全.md
```

**特点**：
- 📖 完整、系统的知识
- 🔗 链接到相关项目和概念
- 📅 长期维护更新

---

#### `40_Wiki/` - 原子概念

**用途**：短小精悍的单一概念解释

**示例**：
```
40_Wiki/
├── 资本结构.md
├── 加权平均资本成本.md
├── 利息税盾.md
└── 财务困境成本.md
```

**特点**：
- 🎯 一个概念 = 一个笔记
- 📝 500-2000 字
- 🔗 大量双向链接

---

#### `50_Resources/` - curated 资源

**用途**：收集的外部内容

**结构**：
```
50_Resources/
├── Newsletters/         # 行业周报
│   └── 2026-02-21 AI 行业周报.md
├── ProductLaunches/     # 产品发布
│   └── NotebookLM 新功能.md
└── Screenshot.png       # 截图等素材
```

---

### 📋 输出层 (Output Layer)

#### `90_Plans/` - 执行计划

**用途**：具体的执行计划（完成后归档）

**与 Project 的区别**：
| 维度 | Project | Plan |
|------|---------|------|
| **焦点** | 持续进行 | 一次性事件 |
| **时间** | 长期（月/年） | 短期（天/周） |
| **归档** | 完成后移入 99_System/Archives/Projects/ | 完成后移入 99_System/Archives/Plans/ |

---

#### `99_System/` - 系统配置

##### `Bases/` - 数据视图定义

**文件**：
- `Knowledge.base` - 知识库视图
- `Projects.base` - 项目视图
- `Projects_Archive.base` - 归档视图

**作用**：Obsidian Bases 插件的配置文件

**示例** (`Projects.base`)：
```yaml
filters:
  and:
    - file.ext == "md"
    - type == "project"
    - status == "active"

formulas:
  urgency_icon: if(due < today && status != "done", "🔴", "🟢")
  priority_label: if(priority == "P0", "🔥 Critical", ...)

views:
  - type: table
    name: 📁 Projects
    groupBy: priority
    sort: urgency_icon DESC
```

**效果**：在 Obsidian 中显示项目表格：

| Urgency | Title | Priority | Due | Area |
|---------|-------|----------|-----|------|
| 🔴 | 因子回测 | 🔥 Critical | 2026-03-01 | [[金融]] |
| 🟢 | 学习笔记 | 📋 Low | - | [[教育]] |

---

##### `Templates/` - 笔记模板

**文件**：
| 模板 | 用途 | 大小 |
|------|------|------|
| `Daily_Note.md` | 每日笔记 | 242B |
| `Project_Template.md` | 项目 | 633B |
| `Content_Template.md` | 内容 | 1050B |
| `Wiki_Template.md` | 概念 | 381B |
| `Inbox_Template.md` | 收集箱 | 133B |

---

##### `Prompts/` - AI 提示词

**结构**：
```
Prompts/
├── Finance_*.md       # 金融领域提示词
│   ├── Finance_Crypto.md
│   ├── Finance_Debt.md
│   ├── Finance_Portfolio.md
│   ├── Finance_StockMarket.md
│   └── Finance_Tax.md
├── General_*.md       # 通用思维模型
│   ├── General_FirstPrinciples.md
│   ├── General_Latticework.md
│   └── General_SecondOrderThinking.md
├── Health_*.md        # 健康领域
│   ├── Health_General.md
│   ├── Health_Medication.md
│   ├── Health_Nutrition.md
│   └── Health_Sympton.md
└── SE_*.md            # 软件工程
    ├── SE_Architect.md
    ├── SE_CodeBase.md
    └── SE_Interview.md
```

**用途**：AI 在特定领域的行为指南

---

### 🤖 AI 配置层 (AI Config Layer)

#### `AGENTS.md` / `CLAUDE.md` / `GEMINI.md`

**用途**：告诉不同 AI 应该怎么行为

**内容**：
```markdown
# CLAUDE.md

## 角色
Knowledge Manager and Daily Planner

## 工作流
- `/start-my-day` - 每日规划
- `/kickoff` - 想法 → 项目
- `/research` - 深度研究
- `/ask` - 快速问答

## 规则
- 项目通过 frontmatter 链接到领域
- 大量使用 wikilinks
- 用用户语言回复
```

**区别**：
| 文件 | 目标 AI | 特点 |
|------|--------|------|
| `AGENTS.md` | 通用 | 所有 AI 都适用 |
| `CLAUDE.md` | Claude | Claude 专用优化 |
| `GEMINI.md` | Gemini | Gemini 专用优化 |

---

## 🔄 核心工作流

### 工作流 1：新想法 → 项目

```
1. 捕获
   00_Inbox/新想法.md
   type: inbox, status: captured

2. 处理（/kickoff）
   ↓
3. 创建项目
   20_Project/新项目.md
   type: project, status: active

4. 每日更新
   10_Daily/2026-02-21.md
   → 链接到 [[新项目]]
```

---

### 工作流 2：每日规划

```
1. 早上运行 /start-my-day
   ↓
2. AI 读取：
   - 昨天的每日笔记
   - 未完成的项目任务
   - 日历事件
   ↓
3. 生成今日计划
   10_Daily/2026-02-21.md
   - Priorities（3 个最重要任务）
   - Related Projects（今天要推进的项目）
```

---

### 工作流 3：深度学习

```
1. 运行 /research "MM 定理"
   ↓
2. AI 研究并创建：
   - 30_Research/MM 定理.md（详细笔记）
   - 40_Wiki/资本结构.md（原子概念）
   - 40_Wiki/利息税盾.md（原子概念）
   ↓
3. 链接到现有知识：
   - [[有效市场假说]]
   - [[因子投资研究]]（项目）
```

---

## 🎯 架构优势

| 优势 | 说明 |
|------|------|
| **灵活性** | 扁平结构 + 链接，随时调整 |
| **可搜索** | Frontmatter 元数据，Bases 视图过滤 |
| **AI 友好** | 结构化模板，AI 知道怎么读写 |
| **时间维度** | 每日笔记作为时间线索引 |
| **行动导向** | 项目驱动，不是知识囤积 |

---

## 📊 与主 Vault 对比

| 维度 | 主 Vault (`~/Documents/Obsidian Vault/`) | OrbitOS-vault |
|------|----------------------------------------|---------------|
| **结构** | 领域分层（16 个一级目录） | 扁平 + frontmatter |
| **项目** | 分散在各领域 | 集中在 20_Project/ |
| **每日笔记** | 无 | 核心枢纽（10_Daily/） |
| **AI 集成** | 无 | 内置工作流命令 |
| **视图** | 手动整理 | Bases 插件自动视图 |
| **理念** | 知识分类存储 | 知识围绕行动运转 |
| **适用场景** | 长期知识库 | 项目管理 + 每日追踪 |

---

## 💡 使用方案

### 方案 A：手动使用（推荐入门）

```
1. 安装 Obsidian Bases 插件
2. 复制 Templates/*.md 创建笔记
3. 按 frontmatter 填写元数据
4. 用 Bases 视图查看所有项目
```

**优点**：
- ✅ 立刻能用，无需配置
- ✅ 理解 OrbitOS 核心理念
- ✅ 轻量级启动

**缺点**：
- ❌ 没有 AI 工作流自动化
- ❌ 需要手动维护元数据

---

### 方案 B：AI 辅助（需要配置）

```
1. 用 Cursor/Claude Desktop 打开 Vault
2. 配置 MCP Server 连接 Obsidian
3. 用 `/kickoff`, `/research` 等命令
```

**优点**：
- ✅ AI 自动创建工作流
- ✅ 智能链接现有知识
- ✅ 每日规划自动化

**缺点**：
- ❌ 配置复杂（MCP Server）
- ❌ 需要 API Key
- ❌ 依赖特定 AI 工具

---

### 方案 C：混合使用（推荐）

```
- 主 Vault 继续用（领域分层）→ 长期知识库
- OrbitOS 做项目管理（20_Project/）→ 行动追踪
- 每日笔记用 OrbitOS（10_Daily/）→ 时间线索引
- 双向链接跨 Vault → 知识互联
```

**优点**：
- ✅ 保留现有知识库
- ✅ 增加项目管理能力
- ✅ 渐进式迁移

**缺点**：
- ❌ 两个 Vault 需要维护
- ❌ 链接跨 Vault 可能失效

---

## 🔧 快速开始指南

### Step 1: 安装必要插件

在 Obsidian 中安装：
- ✅ **Bases** - 数据视图（核心）
- ✅ **Templates** - 笔记模板
- ✅ **Daily Notes** - 每日笔记
- ✅ **Wiki Links Plus** - 双向链接增强

---

### Step 2: 配置 Bases

1. 打开 `99_System/Bases/Projects.base`
2. 在 Obsidian Bases 插件中加载
3. 调整过滤条件和视图

---

### Step 3: 创建第一篇每日笔记

```bash
# 复制模板
cp 99_System/Templates/Daily_Note.md 10_Daily/2026-02-21.md

# 编辑内容
- 填写 Priorities（3 个最重要任务）
- 链接到相关项目
```

---

### Step 4: 创建第一个项目

```bash
# 复制模板
cp 99_System/Templates/Project_Template.md 20_Project/我的项目.md

# 填写 frontmatter
type: project
status: active
area: "[[你的领域]]"

# 填写 C.A.P.
- Context: 目标、成功标准
- Actions: 分阶段任务
- Progress: 初始进展
```

---

## 📝 元数据规范

### 通用字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `type` | string | ✅ | inbox/project/wiki/research |
| `status` | string | ✅ | captured/active/on-hold/done/processed |
| `area` | wikilink | ⚠️ | 所属领域 `[[金融]]` |
| `priority` | string | ⚠️ | P0/P1/P2/P3 |
| `due` | date | ⚠️ | 截止日期 YYYY-MM-DD |
| `tags` | array | ❌ | 标签列表 |

### 类型说明

| type | 用途 | 位置 |
|------|------|------|
| `inbox` | 快速收集 | 00_Inbox/ |
| `project` | 行动项目 | 20_Project/ |
| `wiki` | 原子概念 | 40_Wiki/ |
| `research` | 永久参考 | 30_Research/ |

---

## 📚 推荐学习路径

```
Week 1: 理解理念
- 阅读 AGENTS.md 和 CLAUDE.md
- 理解扁平结构 + frontmatter 设计

Week 2: 手动使用
- 安装 Bases 插件
- 创建每日笔记 + 第一个项目

Week 3: 建立习惯
- 每天早上写 Priorities
- 每天结束时更新 Progress

Week 4: 优化工作流
- 调整 Bases 视图
- 自定义模板
- 考虑 AI 集成
```

---

## 🔗 相关笔记

- [[因子投资 - 系统学习路线图]]
- [[MM 定理 - Modigliani_Miller Theorem]]
- [[有效市场假说 - EMH 详解]]
- [[NotebookLM CLI 命令清单]]

---

## 📖 参考资料

- **OrbitOS 官方**：仓库位置 `~/Documents/OrbitOS-vault/`
- **Obsidian Bases 插件**：https://github.com/obsidianmd/obsidian-bases
- **MCP Protocol**：https://modelcontextprotocol.io/
- **Cursor IDE**：https://cursor.sh/

---

**标签**：#OrbitOS #知识管理 #PKM #Obsidian #笔记系统 #AI 工作流

**创建日期**：2026-02-21  
**最后更新**：2026-02-21  
**来源**：AI 助手基于 OrbitOS-vault 仓库分析整理
