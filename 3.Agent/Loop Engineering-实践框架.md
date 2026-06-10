---
title: "Loop Engineering 实践框架"
type: framework
created: 2026-06-10
updated: 2026-06-10
sources:
  - "[[Loop Engineering-Addy Osmani]]"
  - "[[Loop Engineering-14步指南]]"
  - "[[Fable 5-模型能力验证]]"
tags:
  - agent
  - loop-engineering
  - framework
  - best-practice
---

## 核心原则：干中学

**先跑起来 → 踩坑 → 沉淀 → 再优化。** 不先搭全栈。

## 四条件测试（建 Loop 前必过）

| 条件 | 判断 |
|:---|:---|
| 任务每周至少重复一次 | 低于此频率 = 脚本，不是 loop |
| 有自动验证能拒绝坏结果 | 测试/lint/build/客观指标 |
| Token 预算撑得住重试 | loop 会重复读上下文 |
| Agent 有工具（日志/复现环境） | 能跑自己写的代码 |

缺一条就别建。

## 最小可行 Loop

```
1 Automation + 1 Skill + 1 State File + 1 Gate
```

## 搭建顺序（铁律）

```
手动跑通 → 写成 Skill → 包进 Loop → 排程
```

跳步 = 生产事故。

## 已知失败模式速查

| 模式 | 症状 | 修复 |
|:---|:---|:---|
| Ralph Wiggum | agent 提前完成，半成品退出 | 硬性 gate |
| Goal Drift | 长 session 每次丢信息 | 每轮重读 VISION |
| Self-preferential | maker 给自己打分过高 | 独立 verifier |
| Comprehension Debt | 不读 diff，系统坏了没人懂 | 保持审查 |
| Cognitive Surrender | 停止判断，全盘接受 | 带着判断力设计 |

## 当前 Loop 清单

| Loop | 状态 | 频率 | since |
|:---|:---|:---|:---|
| 龙虎榜评分 | 🟢 运行中 | 工作日盘后 17:00 | 2026-06-10 |
| 市场择时 | 🟢 运行中 | 工作日盘后 15:30 | 2026-06-10 |

## 原则

- 一个 loop 跑稳再开下一个
- 每个 loop 必须有 state file 记录进度
- 每次失败都是沉淀机会——更新 skill，不重复犯错
- 最小可行优先——4 件套就够了，不加多余