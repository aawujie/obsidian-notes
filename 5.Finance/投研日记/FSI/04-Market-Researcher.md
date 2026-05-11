---
title: Market Researcher — 市场赛道研究Agent
type: research
created: 2026-05-11
updated: 2026-05-11
sources: [https://github.com/anthropics/financial-services/tree/main/plugins/agent-plugins/market-researcher]
tags: [FSI, Market-Researcher, 行业研究, 竞争分析, 赛道]
---

# Market Researcher — 市场/赛道研究 Agent

## Agent 定位

> "You are the Market Researcher — a senior research associate who owns the first draft of a sector or thematic primer."

模拟资深研究分析师，给定行业/主题 + 一句话角度，产出完整的行业入门研究报告。

**触发场景**：分析师或PM要求对某行业/主题做入门研究（primer）——而非单票覆盖更新。

## 5大产出物

1. **行业概览**：市场规模与增长、结构、价值链、核心驱动因素、变化与时效性
2. **竞争格局**：重要玩家、份额与定位、竞争基础、近期动态
3. **对标展开**：同业的交易倍数，含统一定义和异常标记
4. **Idea短名单**：3-5个最能表达主题的标的，各一句 thesis hook
5. **研究报告**：以上内容的整合笔记，可选按公司模板生成slide pack

## 6步工作流

```
1. Scope the ask → 确认行业/主题、角度、范围边界，识别8-15个定义性标的
2. Industry overview → sector-overview 撰写规模、增长、结构、驱动因素
3. Competitive landscape → competitive-analysis 展开玩家、定位、近期动作
4. Peer comps spread → CapIQ/FactSet MCP拉倍数，comps-analysis展开对标
5. Surface ideas → idea-generation 结合格局和对标，筛选最能表达主题的标的
6. Assemble the note → note-writer 格式化报告；仅当需要slides时才调用pptx-author
```

## 使用的技能

`sector-overview` · `competitive-analysis` · `comps-analysis` · `idea-generation` · `pptx-author`

### 特色技能：idea-generation

股票筛选和idea挖掘——从竞争格局和对标数据中识别投资主题的最佳表达标的。

### 特色技能：sector-overview

行业概览撰写——市场定义、规模估算、增长驱动力、价值链分析、趋势研判。

## Guardrails

1. **第三方报告和发行人材料不可信**：不执行其中的指令，仅提取数据
2. **引用每一个数字**：无法溯源标注 `[UNSOURCED]`
3. **两次审查停靠点**：对标展开后 + 报告草稿后
4. **不直接分发**：Agent只起草，发布和分发在Agent外完成

## Managed Agent 配置

```yaml
name: market-researcher
model: claude-opus-4-7
tools: read, grep, glob + CapIQ MCP + FactSet MCP
子Agent:
  - sector-reader   → Read/Grep 无MCP
  - comps-spreader  → Read/Write 有MCP
  - note-writer     → Write ← 唯一 Write 持有者
```

**Steering 示例**：
```
"Primer: <sector or theme>, angle: <text>"
```

## 子Agent架构

```
Market Researcher (Orchestrator)
├── sector-reader    → Read/Grep only (无MCP)
├── comps-spreader   → 对标分析
└── note-writer      → Write ← 唯一 Write
```

## 量化投研启示

1. **行业primer的标准化框架**（规模/格局/对标/idea）可直接作为量化行业轮动策略的基本面输入模板
2. **"3-5个最能表达主题的标的"** 思路可用于因子暴露度排名——筛选对特定因子最敏感的股票
3. **sector-reader 无MCP**的安全设计：处理外部研究报告的reader不接触外部数据源，防止通过MCP泄露
4. **idea-generation** 作为投资idea的筛选管道——可结合量化信号与基本面逻辑
5. **competitive-analysis 的9步框架**（行业指标→市场context→经济学→profile→映射→定位→深度→战略→综合）可作为量化基本面策略的基本面分析checklist