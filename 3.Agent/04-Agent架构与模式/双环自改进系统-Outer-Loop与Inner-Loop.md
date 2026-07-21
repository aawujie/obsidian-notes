---
title: 双环自改进系统-Outer Loop与Inner Loop
type: notes
created: 2026-07-15
updated: 2026-07-15
tags:
  - AI
  - Agent
  - 自改进
  - 架构设计
---

# 双环自改进系统（Dual-Loop Self-Improvement）

## 架构

### <span style="color:rgb(255, 77, 77)">外循环（Outer Loop）—— 装备升级师</span>

用更强 AI（如 Claude）专门改 "内层 AI 的工具代码"，像老板给员工升级装备。

### <span style="color:rgb(255, 77, 77)">内循环（Inner Loop）—— 执行者</span>

用 AI（如 Gemini）拿着升级后的装备去实际写代码、测任务、找更好方案。

### 循环过程

```
外循环 → 改代码/改工具/改提示词
  ↓
内循环 → 跑任务 → 测分 → 反馈
  ↓
外循环 ← 接收分数 → 再改 → 再跑
  ↓
重复 100 次 → 挑出最好的改进版本
```

## 核心设计逻辑

1. **分工明确**：强模型（Claude）不做执行，只做装备设计；快模型（Gemini）不做决策，只做跑分
2. **量化反馈**：内循环必须输出可比较的分数，外循环才有优化方向
3. **迭代收敛**：100 次循环后挑最优版本，本质是 genetic algorithm 的变体

## 应用方向

- **工具代码优化**：让 Claude 改 agent 用的工具函数，Gemini 跑 benchmark 验证
- **提示词进化**：外循环改 system prompt，内循环跑一组任务打分
- **Skill 自动调优**：扫参数、跑回测、挑最优

## 风险

- 成本：100 次循环如果每次调用 Claude Opus，单次可能 $0.5-2
- 打分函数设计不好会导致优化到错误方向（reward hacking）