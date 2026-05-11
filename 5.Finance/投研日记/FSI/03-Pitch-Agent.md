---
title: Pitch Agent — 投行Pitch全流程
type: research
created: 2026-05-11
updated: 2026-05-11
sources: [https://github.com/anthropics/financial-services/tree/main/plugins/agent-plugins/pitch-agent]
tags: [FSI, Pitch-Agent, 投行, 估值, PitchDeck]
---

# Pitch Agent — 投行 Pitch 端到端自动化

## Agent 定位

> "You are the Pitch Agent — a senior investment banking associate who owns the first draft of a client pitch end to end."

模拟投行资深分析师，从目标公司ticker + 一句话战略场景出发，**自动完成完整Pitch的两大产出物**：Excel估值工作簿 + 品牌化Pitch Deck。

**触发场景**：MD或高级银行家要求对某公司出第一稿Pitch——而非编辑已有Deck。

## 产出物

1. **Excel估值工作簿**：交易对标、先例交易、DCF、Football Field总结。每个输出单元格都是可追溯到输入单元格的活公式。
2. **Pitch Deck**：使用银行PPT模板填充——情景概览、公司快照、估值总结（Football Field）、对标详情、先例交易详情、示意性流程。每个图表绑定Excel模型。

## 9步工作流

```
1. Scope the ask → 确认目标、行业、场景，识别5-8个对标 + 5-10个先例交易
2. Situation overview → sector-overview skill 撰写公司快照和战略叙事
3. Pull data → CapIQ MCP 获取交易倍数、先例数据、最新披露
4. Spread peers → comps-analysis skill 展开对标和先例交易
5. Sponsor case → lbo-model skill 建立示例LBO（市场杠杆水平）
6. Build model → dcf-model + 3-statement-model + audit-xls
7. Football field → 各方法论的min/median/max，含当前价格标记
8. Populate deck → pitch-deck skill 填充银行模板
9. Deck QC → ib-check-deck 验证数字一致性
```

## 使用的技能

`sector-overview` · `comps-analysis` · `lbo-model` · `dcf-model` · `3-statement-model` · `audit-xls` · `pitch-deck` · `ib-check-deck` · `deck-refresh`

### 特色技能：pitch-deck

位于 `skills/pitch-deck/`，包含4个参考文件：
- `calculation-standards.md` — 计算标准
- `formatting-standards.md` — 格式标准
- `slide-templates.md` — 幻灯片模板
- `xml-reference.md` — XML参考

### 特色技能：ib-check-deck

投行Deck QC专用：
- `ib-terminology.md` — 投行术语参考
- `report-format.md` — 报告格式标准
- `scripts/extract_numbers.py` — 数字提取脚本

## Guardrails（安全约束）

1. **无外部通信**：没有邮件或消息工具，客户触达在Agent外完成
2. **引用每一个数字**：若无法从CapIQ或披露文件找到来源，标记 `[UNSOURCED]` 而非估算
3. **两次审查停靠点**：Excel模型建成后 + Deck生成后——银行家审批每个产出物后才能继续
4. Formula over Hardcode：每个推导值必须是公式

## Managed Agent 配置

```yaml
name: pitch-agent
model: claude-opus-4-7
tools: read, grep, glob + CapIQ MCP + Daloopa MCP
skills: 从 agent-plugins/pitch-agent 加载
子Agent:
  - researcher (研究对标+先例)
  - modeler (建模)
  - deck-writer (写Deck，唯一的Write持有者)
```

**Steering 示例**：
```
"Build pitch book: <target> / <acquirer>, thesis: <text>"
```

## 子Agent架构

```
Pitch Agent (Orchestrator)
├── researcher    → Read/Grep + CapIQ MCP
├── modeler       → Write (Excel) + 建模技能
└── deck-writer   → Write (PPTX) ← 唯一 Write 持有者
```

安全模式：Orchestrator不直接写文件；deck-writer是唯一有Write权限的叶子节点。

## 量化投研启示

1. **端到端自动化范式**：从数据拉取→建模→QC→产出物的完整流水线，可直接用于量化研报自动生成
2. **Football Field 可视化**：多方法论估值区间的min/median/max汇总，可复用于多因子打分汇总
3. **"引用每一个数字"** 的数据溯源原则：量化信号输出同样可标注数据来源与置信度
4. **两次审查停靠点** 的设计：量化模型中可设置"数据预处理完成"和"信号生成完成"两个人工检查点
5. **deck-writer 唯一 Write 权限**的安全隔离模式：适用于生产环境的信号输出模块