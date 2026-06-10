---
title: "Claude Fable 5 实战 - Loop Engineering 模型能力验证"
type: reference
created: 2026-06-10
updated: 2026-06-10
sources:
  - "https://x.com/rlancemartin/status/2064397389189071163"
tags:
  - agent
  - fable-5
  - loop-engineering
  - anthropic
  - model-benchmark
---

## 原文信息

- 作者：Lance Martin (@RLanceMartin) - Anthropic
- 时间：2026-06-09
- 点赞：2,835 | 转发：312 | 浏览：489,117

> **Loop Engineering 的模型能力验证篇。** 前几篇讲"怎么建 loop"，这篇讲"Fable 5 跑 loop 比 Opus 强多少"。
> 相关笔记：[[Loop Engineering-Addy Osmani]] | [[Loop Engineering-14步指南]]

---

## 1. Self-correction loops（自纠正循环）

用 Fable 5 跑 Parameter Golf：开源 ML 挑战，16MB 模型 + 8xH100 + <10 分钟训练，类似 Karpathy 的 autoresearch。

测试环境：Claude Managed Agents (CMA) + 自托管 8xH100 + 8 小时时间限制。

### 对比结果

| 指标 | Fable 5 | Opus 4.7 |
|:---|:---|:---|
| 训练管线提升 | **~6x** | 基准 |
| 实验策略 | 大规模结构性改动，扛住回撤 | 第一次小赢后重复同模板（调标量 → 测 → 保留） |
| Verifier | 独立 grader sub-agent | 自我评分 |

### 关键洞察

**Verifier sub-agent 比 self-critique 好**，因为评分在独立 context window 里进行。Outcomes 功能自动生成 grader sub-agent。

Rubric（评分标准）是包含 9 个可检查标准的文件：跑 baseline、跑 20 个实验等。

## 2. Memory（跨会话记忆）

测试任务：Sequential SQL 问答，每个问题是独立 agent session，共享 memory 文件系统。

### 学习的五个阶段

```
Fail → Investigate → Verify → Distill → Consult
失败   →  诊断原因   →  核实事实  →  提炼规则 →  查阅规则（不再重新推导）
```

### 模型表现对比

| 模型 | 卡在哪个阶段 | 验证覆盖率 |
|:---|:---|:---|
| Sonnet 4.6 | 阶段1：只记失败笔记和猜测（"maybe prc instead of prc_usd?"），几乎不回顾 | ~0% |
| Opus 4.7 | 阶段3：建 schema 参考但"possibly prc in cents? Verify." 核实覆盖率低 | 7-33%（中位 17%） |
| **Fable 5** | 阶段5：完成完整循环 | **73%**（30 个问题中 22 个验证通过） |

Fable 5 会提炼通用规则供未来任务使用，形成渐进式的知识积累。

## 结论

> 直接 prompt 和引导 Fable 5 不如设计一个 loop：让模型自己根据环境反馈自纠正（`/goal` 或 Outcomes），自己管理上下文（memory）。

## 实操建议

- 用 Fable 5 跑长期任务时，提供明确的 rubric 文件
- 使用独立 grader sub-agent 而非 self-critique
- Memory 的五个阶段是设计跨 session 记忆系统的参考模板
- 参考 Claude Code 的内置 `/claude-api` skill 了解 Fable 5 最佳实践