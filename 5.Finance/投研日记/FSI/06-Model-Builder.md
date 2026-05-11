---
title: Model Builder — DCF/LBO/3-statement建模
type: research
created: 2026-05-11
updated: 2026-05-11
sources: [https://github.com/anthropics/financial-services/tree/main/plugins/agent-plugins/model-builder]
tags: [FSI, Model-Builder, DCF, LBO, 财务建模, Excel]
---

# Model Builder — DCF/LBO/三表建模 Agent

## Agent 定位

> "You are the Model Builder — a financial modeling specialist who builds institutional-quality valuation models from scratch."

纯粹的财务建模专家——从ticker和假设集出发，从零开始构建机构级估值模型。**不同于Earnings Reviewer**（更新现有模型），Model Builder是从空白构建全新模型。

## 4种模型产出

给定ticker、模型类型和假设集：

1. **DCF**：预测期 + 终值 + WACC构建 + 敏感性表格
2. **LBO**：Sources & Uses + 债务时间表 + 收益瀑布 + IRR/MOIC敏感性
3. **三表模型**：集成IS/BS/CF + 营运资本 + 债务时间表
4. **Comps**：交易倍数表 + 摘要统计

## 5步工作流

```
1. Pull inputs → CapIQ/Daloopa MCP获取历史数据、一致预期、披露文件
2. Build the model → 调用对应技能(dcf/lbo/3-statement/comps)，蓝/黑/绿色编码，计算cell无硬编码
3. Audit → audit-xls检查平衡、循环引用、每项输出可追溯到输入
4. Sensitize → 构建该模型类型的标准敏感性表格
5. Surface for review → 建模完成后暂停，用户审查后才能继续使用
```

## 使用的技能

`dcf-model` · `lbo-model` · `3-statement-model` · `comps-analysis` · `audit-xls`

## Guardrails

1. **每个输出都是公式**：计算单元格中不能有手动键入的数值
2. **引用每一个输入**：硬编码假设标注来源或标记 `[ASSUMPTION]`
3. **两次停靠审查**：构建完成后 + 审计完成后——用户审批后才进入敏感性分析

## Managed Agent 配置

```yaml
name: model-builder
model: claude-opus-4-7
tools: read, grep, glob + CapIQ MCP + Daloopa MCP
子Agent:
  - data-puller → Read/Grep + MCP
  - builder     → Write (主要建模者)
  - auditor     → Read only (独立审计)
```

**Steering 示例**：
```
"Build <dcf|lbo|3-stmt> for <ticker>, assumptions: {...}"
```

**安全设计**：auditor只有Read权限——独立审查builder的工作，不引入新错误。

## 子Agent架构

```
Model Builder (Orchestrator)
├── data-puller → Read/Grep + CapIQ/Daloopa MCP
├── builder     → Write ← 唯一 Write (建模)
└── auditor     → Read only (独立审计builder产出)
```

## 与其他Agent的区别

| 特性 | Model Builder | Earnings Reviewer |
|------|--------------|-------------------|
| **起点** | 从零构建 | 更新现有覆盖模型 |
| **产出** | 全新Excel工作簿 | 更新工作簿+报告 |
| **场景** | 初始化覆盖/新交易 | 财报季常规更新 |
| **子Agent** | data-puller/builder/auditor | transcript-reader/model-updater/note-writer |

## 量化投研启示

1. **"从零构建"vs"更新现有"的Agent分工**：量化系统中可区分"新建策略"和"参数刷新"两个Agent
2. **independent auditor** 设计：只读权限的独立审计Agent——可应用于量化模型的回测结果核查
3. **audit-xls的模型类型专项检查**：DCF/LBO/Merger各有针对性审计项——量化策略也应有不同策略类型的专项回测检查
4. **敏感性表格作为最后一步**：在审计通过后才构建敏感性——保证基础模型正确后再做假设变化分析
5. **data-puller-builder-auditor三段式架构**：数据获取→构建→独立审计，可用于量化策略开发流水线