---
title: KYC Screener — KYC尽调筛查
type: research
created: 2026-05-11
updated: 2026-05-11
sources: [https://github.com/anthropics/financial-services/tree/main/plugins/agent-plugins/kyc-screener]
tags: [FSI, KYC, 尽调筛查, 合规, AML]
---

# KYC Screener — KYC尽调筛查 Agent

## Agent 定位

> "You are the KYC Screener — a client-onboarding analyst who assembles and screens a KYC file."

客户准入分析师角色——解析入件文档包、运行公司KYC/AML规则引擎、筛查制裁和PEP名单、标记缺口供升级处理。

**用于新客户准入或定期刷新——非交易监控。**

## 4大产出物

1. **提取的实体档案**：法定名称、受益所有人、地址、标识符、文件清单
2. **规则引擎结果**：每条KYC/AML规则的 通过/不通过、证据引用
3. **筛查结果**：制裁名单、PEP（政治人物）、负面媒体命中，含匹配置信度
4. **升级包**：缺口、命中、建议风险评级，格式化供合规签字

## 4步工作流

```
1. Read the packet → doc-reader从准入PDF中提取结构化字段（无MCP访问）
2. Run the rules → 对提取字段评估每条公司KYC规则
3. Screen → Screening MCP对每个命名方做制裁/PEP/负面媒体筛查
4. Package escalations → escalator格式化缺口和命中包供合规审核
```

## 使用的技能

`kyc-doc-parse` · `kyc-rules` · `xlsx-author`

| 技能 | 功能 |
|------|------|
| **kyc-doc-parse** | KYC文档解析——从PDF/扫描件中提取结构化实体信息 |
| **kyc-rules** | KYC规则引擎——对提取字段执行公司KYC/AML规则评估 |
| **xlsx-author** | 生成升级包Excel |

## Guardrails — 多层安全

1. **准入文件不可信**：doc-reader仅有Read/Grep，返回**长度上限的结构化JSON**——不返回原始文档内容
2. **编排者绝不写**：只有escalator子Agent持有Write
3. **不做风险评级决策**：Agent建议；合规官决定

## Managed Agent 配置

```yaml
name: kyc-screener
tools: read, grep, glob + Screening MCP
子Agent:
  - doc-reader    → Read/Grep only (无MCP, 无Write)
  - rules-engine  → 规则评估
  - escalator     → Write ← 唯一 Write (合规包)
```

**Steering 示例**：
```
"Screen onboarding packet <id>"
```

## 子Agent架构

```
KYC Screener (Orchestrator) ← 无Write
├── doc-reader    → Read/Grep only (无MCP, 无Write) → 输出长度上限的结构化JSON
├── rules-engine  → 规则评估
└── escalator     → Write ← 唯一 Write (仅格式化，不接触原始文档)
```

**安全设计的层次深度**：
1. doc-reader 读外部PDF但无MCP/Write → 只输出长度上限的结构化JSON
2. rules-engine 只接触结构化JSON，不接触原始文档
3. escalator 只做格式化输出，不接触外部数据

## 量化投研启示

1. **"长度上限的结构化JSON"** 作为安全中间格式：处理外部非结构化数据时，reader仅输出受限长度+有schema的结构化数据——防止注入和数据泄露
2. **规则引擎->筛查->升级** 三层合规流水线：可复用于量化交易中的合规前置检查
3. **"建议而非决定"** 的决策模式：量化模型可输出风险评分建议，最终决策由风控系统执行
4. **匹配置信度标注**：制裁/PEP的模糊匹配confidence——量化数据匹配中的模糊去重可借鉴
5. **新客户准入+定期刷新双场景**：量化策略的参数校准（初始+定期刷新）类似的双模式设计