---
title: DESIGN.md设计系统调研
type: concept
created: 2026-05-11
updated: 2026-05-11
sources:
  - https://github.com/VoltAgent/awesome-design-md
  - https://github.com/google-labs-code/design.md
  - https://stitch.withgoogle.com/docs/design-md/overview/
  - https://designmd.app/what-is-design-md
tags:
  - design-system
  - AI-agent
  - DESIGN.md
  - AGENTS.md
  - Google-Stitch
  - vibe-design
  - design-tokens
---

# DESIGN.md 设计系统调研

## 1. DESIGN.md 概念：Google Stitch 的纯文本设计系统

### 1.1 起源

**DESIGN.md** 由 **Google Stitch** 团队于 2026 年 3 月提出，2026 年 4 月正式开源规范草案。它是一种**纯文本 Markdown 设计系统文档**，AI Agent 读取后生成一致的 UI——不需要 Figma 导出、JSON schema 或任何特殊工具。

核心思想：**YAML 设计 Token（机器可读）+ Markdown 设计散文（人类可读）**，两个维度在同一个文件中，Agent 能同时获得"精确数值"和"设计意图"。

### 1.2 与 AGENTS.md 的互补关系

| 文件 | 谁读 | 定义什么 |
|------|------|---------|
| `AGENTS.md` | 编码 Agent | 如何构建项目（架构、测试、规范） |
| `DESIGN.md` | 设计 Agent | 项目的外观和感觉（颜色、字体、间距） |

**三层架构**（2026 年形成共识）：

| 层级 | 文件 | 内容 | 平衡点 |
|------|------|------|--------|
| 行为层 | `AGENTS.md` / `CLAUDE.md` | 角色、规则、上下文 | 几乎全人类可读 |
| 任务层 | `SKILL.md` | 可复用任务、领域知识 | 部分结构化 |
| 外观层 | `DESIGN.md` | 设计系统、Token | 机器可读 + 人类可读 |

**关键区别**：
- AGENTS.md 回答"怎么建"——构建命令、代码风格、测试规则
- DESIGN.md 回答"长什么样"——颜色语义、排版层级、组件样式
- 两者不重叠。AGENTS.md 中用一行 `阅读 ./DESIGN.md 获取设计系统` 即可串联起来

### 1.3 Google Stitch 规范核心

开源仓库：`google-labs-code/design.md`，提供完整规范 + CLI 工具 + Linter。

**DESIGN.md 的两层结构**：
1. **YAML front matter** (`---` 包裹)：机器可读的设计 Token——颜色、排版、圆角、间距、组件
2. **Markdown body** (`##` 章节)：人类可读的设计散文——设计哲学、用法指南、Do's/Don'ts

**Token 类型**：

| 类型 | 格式 | 示例 |
|------|------|------|
| Color | `#` + hex (sRGB) | `"#cc785c"` |
| Dimension | number + unit | `48px`, `-0.02em` |
| Token Reference | `{path.to.token}` | `{colors.primary}` |
| Typography | object | `{fontFamily, fontSize, fontWeight, lineHeight, letterSpacing}` |

**Section 规范顺序**（`##` 章节，可省略但必须保持顺序）：
1. Overview / Brand & Style
2. Colors
3. Typography
4. Layout / Layout & Spacing
5. Elevation & Depth
6. Shapes
7. Components
8. Do's and Don'ts

**CLI 工具**：
```bash
npx @google/design.md validate DESIGN.md      # 校验 Token 引用、WCAG 对比度
npx @google/design.md export --format css-tailwind DESIGN.md  # → Tailwind v4 @theme
npx @google/design.md export --format dtcg DESIGN.md          # → W3C DTCG tokens.json
```

**Linter 规则**：broken-ref（引用断裂）、missing-primary、contrast-ratio（WCAG AA 4.5:1）、orphaned-tokens（孤立 Token）、section-order 等。

---

## 2. 项目规模

**awesome-design-md** 仓库截至 2026 年 5 月：
- **Stars**: ~73,000
- **收录品牌**: **71 个** DESIGN.md
- **每个品牌**：包含 `DESIGN.md` + `preview.html` + `preview-dark.html`
- **贡献者**: 4 人（necatiozmen, doanbactam, LeeDoYup, omeraplak）
- **创建时间**: 2026-03-31（一个多月即达到 7 万 star）

**分类分布**：

| 类别 | 数量 | 品牌示例 |
|------|------|---------|
| AI & LLM 平台 | 12 | Claude, Mistral AI, ElevenLabs, Runway, xAI, Ollama |
| 开发者工具 & IDE | 7 | Vercel, Cursor, Warp, Superhuman, Raycast |
| 后端/数据库/DevOps | 8 | Supabase, Sentry, ClickHouse, MongoDB, PostHog |
| 生产力 & SaaS | 7 | Linear, Notion, Intercom, Resend, Cal.com |
| 设计 & 创意工具 | 6 | Figma, Framer, Airtable, Miro, Webflow |
| 金融 & 加密货币 | 7 | Stripe, Coinbase, Binance, Revolut, Wise |
| 电商 & 零售 | 5 | Airbnb, Nike, Shopify, Starbucks, Meta |
| 媒体 & 消费科技 | 11 | Apple, Spotify, SpaceX, NVIDIA, IBM, Uber |
| 汽车 | 8 | Tesla, Ferrari, Lamborghini, BMW, Bugatti |

---

## 3. 代表性案例分析

### 3.1 Claude (Anthropic)

**设计定位**：温暖陶土 + 编辑风格（Warm terracotta accent, clean editorial layout）

**核心特征**：
- **温暖人本主义**：奶油色画布 `#faf9f5` 打底，珊瑚色 `#cc785c` 作 Primary CTA。故意区别于大多数 AI 品牌的冷蓝+石板灰配色
- **打字排版双重人格**：Display 用衬线体 `Copernicus / Tiempos Headline`（h1/h2），Body 用人文无衬线 `StyreneB / Inter`
- **深邃产品展示面**：代码编辑器 mockup、模型展示卡用深色面 `#181715`，对比温暖画布形成强烈的"产品 vs 内容"层次
- **圆角语义化**：xs(4px) → pill(9999px)，按场景精确控制
- **丰富的组件变体**：button-primary 有 default/active/disabled 三态，pricing card 有 default/featured 两种，category-tab 有 default/active 态
- **品牌电压**：来自 cream/coral 的温暖配对，Anthropic 黑色放射状标记锚定品牌识别

**Token 规模**：~23 颜色 Token、~13 排版层级、6 级圆角、7 级间距、~25 组件定义

**设计哲学**：温暖 > 冷峻，人本 > 技术感。用设计语言传达"这是一个友好的 AI 伙伴"。

### 3.2 Vercel

**设计定位**：黑白精确主义 + Geist 字体（Black and white precision, Geist font）

**核心特征**：
- **极限极简**：纯黑 `#000` 与纯白 `#fff` 的二元对比，Geist 字体族贯穿始终
- **代码美学**：大量使用等宽字体（Geist Mono）作为装饰和功能元素
- **高密度信息布局**：与 Claude 的宽松编辑风形成反差，Vercel 倾向紧凑的技术信息展示
- **微妙的蓝色信号**：极小范围使用强调蓝，大部分交互依赖黑白对比度

**设计哲学**："工具本身就是品牌"——不添加装饰，让产品的精确性通过排版和间距说话。

### 3.3 ElevenLabs

**设计定位**：暗色电影级 UI + 音频波形美学（Dark cinematic UI, audio-waveform aesthetics）

**核心特征**：
- **电影级暗色**：深黑画布 + 微妙的动态光影，营造"录音棚"般的沉浸感
- **音频语言视觉化**：波形、频率谱等音频元素融入 UI，形成独特的视觉语言
- **霓虹点缀**：少量高饱和度强调色在暗色背景上像音频 VU 表一样跳动
- **大尺寸排版**：标题极为醒目，类似电影海报的视觉层次

**设计哲学**：让声音"可见"——暗色背景让视觉焦点集中在音频内容和交互上。

### 3.4 Mistral AI

**设计定位**：法式极简 + 紫色调（French-engineered minimalism, purple-toned）

**核心特征**：
- **法国设计基因**：克制、优雅，用最少的元素表达最多的信息
- **紫色品牌色**：不同于典型 AI 品牌的蓝色系，紫色暗示"神秘、创造、非传统"
- **精确的排版**：欧洲现代主义传统——字体选择、字间距、对齐都极为讲究
- **开放式布局**：大量留白，让每个元素有呼吸空间

**设计哲学**：极简主义的法国诠释——用设计传达"我们做的是优雅的、不同于硅谷的 AI"。

### 3.5 Superhuman

**设计定位**：高级暗色 UI + 键盘优先 + 紫色光晕（Premium dark UI, keyboard-first, purple glow）

**核心特征**：
- **高端邮件客户端的暗色美学**：不是"开发者工具"的暗色，而是"高级商务"的暗色
- **紫色光晕系统**：从按钮 hover 到选中状态，紫色作为唯一的强调色，形成高度统一的视觉签名
- **键盘优先的交互暗示**：快捷键提示、命令面板等 UI 元素隐式引导用户脱离鼠标
- **极速视觉响应**：过渡动画短促精确，传达"速度"感
- **紧凑但不拥挤**：信息密度高但通过精确的间距和对齐保持可读性

**设计哲学**："邮件应该快到让 UI 消失"——暗色减少视觉噪音，紫色光晕提供最小但足够的视觉反馈。

### 3.6 Warp

**设计定位**：暗色 IDE 风 + 块状命令 UI（Dark IDE-like interface, block-based command UI）

**核心特征**：
- **温暖的暗色**（不是冷黑）：画布是暖近黑色，文字是暖羊皮纸色 `#faf9f6`，像篝火旁的林间空地
- **Matter 字体的秘密武器**：几何无衬线但有柔软感和人性化，Regular 权重几乎贯穿所有文字——连标题都不用 Bold，极为克制
- **自然摄影穿插**：终端截图与自然风景交替出现，把开发者工具营销得像生活方式品牌
- **块状命令 UI**：命令以块状组织，类似代码块的视觉隐喻
- **几乎单色**：几乎找不到强调色，交互状态靠透明度和下划线传达
- **大写标签 + 宽字间距**：小标签用 uppercase + 2.4px letter-spacing，制造编辑杂志般的分类系统

**设计哲学**："终端公司，生活方式品牌的营销"——用温暖和克制对抗传统开发者工具的冷峻蓝色系。

### 3.7 Runway

**设计定位**：电影级暗色 + 纸白阅读带 + 纯黑 Pill CTA（Cinematic dark heroes, paper-white reading bands, pure black pill CTAs）

**核心特征**：
- **电影节美学**：英雄区是影院级暗色，内容区切换为纸白阅读带，像电影节场刊
- **单一专有无衬线体**：只用一种字体完成所有排版层级
- **纯黑 Pill CTA**：按钮形状高度统一为 pill 形，纯黑背景，形成强烈的视觉锚点
- **全出血媒体**：视频/图片经常边缘到边缘，最大化视觉冲击

**设计哲学**：AI 视频工具应该看起来像电影节，而不是 SaaS 仪表盘。

### 3.8 Stripe

**设计定位**：标志性紫色渐变 + 300 字重优雅（Signature purple gradients, weight-300 elegance）

**核心特征**：
- **紫色渐变系统**：从深紫到亮紫的渐变贯穿整个品牌，是 Stripe 最鲜明的视觉资产
- **极细字重（300）**：标题大量使用 weight 300，传达"轻盈、现代、精密"
- **圆角无处不在**：按钮、卡片、输入框全部圆角，柔软友好
- **精密间距**：垂直节奏极为精确，像瑞士排版传统在数字时代的延续

**设计哲学**：支付基础设施不应该看起来像银行——用设计和美学降低"钱"的心理摩擦。

---

## 4. 结构解读：DESIGN.md 的标准结构

awesome-design-md 中的每个 DESIGN.md 在 Google Stitch 规范基础上扩展为 **9 个章节**：

| # | 章节 | 内容 | Agent 如何使用 |
|---|------|------|---------------|
| 1 | **Visual Theme & Atmosphere** | 情绪、密度、设计哲学 | 建立"感觉基调"，决定整体方向 |
| 2 | **Color Palette & Roles** | 语义化名称 + hex + 功能角色 | 精确取色，理解"什么颜色用于什么场景" |
| 3 | **Typography Rules** | 字体族 + 完整层级表 | 确定 fontSize、weight、lineHeight、letterSpacing |
| 4 | **Component Stylings** | 按钮/卡片/输入框/导航（含状态） | 渲染组件时直接引用 Token |
| 5 | **Layout Principles** | 间距尺度、网格、留白哲学 | 决定 padding/margin/布局节奏 |
| 6 | **Depth & Elevation** | 阴影系统、表面层级 | 理解 z-index 和视觉层次 |
| 7 | **Do's and Don'ts** | 设计护栏和反模式 | 避免 Agent 自作主张偏离设计语言 |
| 8 | **Responsive Behavior** | 断点、触摸目标、折叠策略 | 适配不同屏幕尺寸 |
| 9 | **Agent Prompt Guide** | 快速颜色参考、即用 Prompt | Agent 快速上手，无需通读全文 |

**YAML Token 的结构**（机器可读部分）：

```yaml
---
version: alpha
name: BrandName
description: "一句话描述设计语言"
colors:
  primary: "#cc785c"
  ink: "#141413"
  canvas: "#faf9f5"
  # ... 20-30 个语义化颜色
typography:
  display-xl:
    fontFamily: "FontName, fallback"
    fontSize: 64px
    fontWeight: 400
    lineHeight: 1.05
    letterSpacing: -1.5px
  # ... 10-15 个层级
rounded:
  xs: 4px
  sm: 6px
  md: 8px
  lg: 12px
  pill: 9999px
spacing:
  xs: 8px
  sm: 12px
  md: 16px
  lg: 24px
  xl: 32px
  section: 96px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.button}"
    rounded: "{rounded.md}"
    padding: 12px 20px
  # ... 15-25 个组件 + 状态变体
---
```

**每个品牌还附带**：
- `preview.html`：视觉目录（色板、排版尺度、按钮、卡片）
- `preview-dark.html`：暗色版视觉目录

---

## 5. 与我们的关联：DESIGN.md + huashu-md-html skill

### 5.1 直接集成方案

`huashu-md-html` skill 的核心能力是将 Markdown 内容渲染为品牌级 HTML 页面。引入 DESIGN.md 后可以做到：

1. **设计系统注入**：Agent 读取 `DESIGN.md` → 理解品牌设计语言 → 生成符合该品牌风格的 HTML
2. **一键换肤**：切换不同的 `DESIGN.md` 即可瞬间改变 HTML 输出的品牌风格
3. **品牌一致性保证**：Agent 不再"凭记忆猜颜色"，而是从 Token 精确取值

### 5.2 推荐工作流

```
输入 Markdown 内容
    +
选择 DESIGN.md（如 claude/DESIGN.md 或 stripe/DESIGN.md）
    ↓
Agent 读取 DESIGN.md Token（YAML 精确值 + Markdown 散文设计意图）
    ↓
生成品牌级 HTML（CSS 变量来自 DESIGN.md Token）
    ↓
输出：符合该品牌视觉语言的 HTML 页面
```

### 5.3 具体实现方式

**方式 A：选用现有 DESIGN.md**
- 从 awesome-design-md/design-md/ 选择与内容调性匹配的品牌
- Claude/Anthropic → 温暖人本；Stripe → 精密现代；Linear → 极简精确

**方式 B：创建定制 DESIGN.md**
- 分析目标审美 → 用 Google Stitch 规范编写专属 DESIGN.md
- 对于个人品牌页面或特殊项目，定制>选用

**方式 C：多品牌切换**
- 支持参数 `--design claude|stripe|linear|vercel` 切换品牌风格
- 每种风格对应一个 DESIGN.md，Agent 动态加载

### 5.4 huashu-md-html 的增强点

引入 DESIGN.md 后，huashu-md-html 可以：
- 从 YAML Token 自动生成 CSS 变量（`--color-primary`, `--font-display` 等）
- 排版层级映射：`h1` → `typography.display-xl`, `p` → `typography.body-md`
- 组件自动匹配：按钮 → `components.button-primary`，卡片 → `components.feature-card`
- 暗色/亮色双模式：DESIGN.md 的颜色语义天然支持 light/dark 切换（`canvas` vs `surface-dark`）

---

## 6. 实用价值评估

### 6.1 优势

| 维度 | 评价 |
|------|------|
| **Agent 友好度** | Markdown 是 LLM 原生训练格式，无需解析，直接理解 |
| **精确性** | YAML Token 提供精确 hex/px 值，避免 Agent "猜"颜色 |
| **语义完整性** | 散文部分解释"为什么"，Token 提供"是什么"，两者互补 |
| **跨工具通用** | 任何 Agent（Claude Code、Cursor、Codex）都能读取 |
| **版本可控** | 纯文本文件，Git diff 友好，无二进制 Figma 文件 |
| **生态工具** | CLI（validate/export）、Linter（WCAG 对比度检查）、导出到 Tailwind/DTCG |
| **开箱即用** | 71 个品牌 DESIGN.md 可直接使用，无须从零创建 |
| **品牌一致性** | Token 引用机制确保一处修改全局生效 |

### 6.2 局限性

| 维度 | 评价 |
|------|------|
| **规范早期** | 2026 年 4 月才开源，生态尚在构建 |
| **无法处理复杂交互** | 动画、过渡、微交互描述有限 |
| **品牌提取精度** | awesome-design-md 从公开 CSS 提取 Token，可能与官方设计系统有偏差 |
| **缺少插图/图标规范** | 图标系统、插图风格未有标准化描述 |
| **不替代 Figma** | 无法描述复杂组件状态和交互流程的全貌 |
| **上下文消耗** | 完整 DESIGN.md 约 2-5K tokens，加入 Agent 上下文有一定消耗 |

### 6.3 结论

DESIGN.md 是 AI 辅助 UI 生成的一个**关键拼图**：

- **对编码 Agent**：解决了"写出来的 UI 丑、不一致、没有品牌感"的核心痛点
- **对设计系统**：提供了比 JSON Token 更完整（含设计意图）、比 Figma 更轻量（纯文本）的第三种方案
- **对工作流**：AGENTS.md（行为规范）+ DESIGN.md（设计规范）+ SKILL.md（任务技能）= AI 开发的完整指令体系

**建议**：将 DESIGN.md 集成到 huashu-md-html skill 中，让 Markdown→HTML 的渲染管线具备品牌级设计能力。短期从选用现有品牌的 DESIGN.md 开始，中期建立定制 DESIGN.md 模板库，长期可实现"输入内容 + 选择风格 = 品牌级 HTML 页面"的完整自动化。