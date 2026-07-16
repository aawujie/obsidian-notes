---
title: Karpathy AutoResearch 调研
type: 技术笔记
created: 2026-07-11
updated: 2026-07-11
sources:
  - https://github.com/karpathy/autoresearch
  - https://www.mager.co/blog/2026-03-14-autoresearch-pattern
  - https://www.datacamp.com/tutorial/guide-to-autoresearch
tags:
  - AI
  - Agent
  - 自动化
  - 机器学习
  - Karpathy
---

## 一句话

AutoResearch = 让 AI Agent 在单 GPU 上自动跑 ML 实验，改代码 → 训练 5 分钟 → 测指标 → 保留/回滚，循环往复。

## 基本信息

| 项目 | 内容 |
|:---|:---|
| 作者 | Andrej Karpathy（前 Tesla AI 总监、OpenAI 联创） |
| 发布时间 | 2026 年 3 月 |
| 仓库 | github.com/karpathy/autoresearch |
| 代码量 | 极简，3 个文件 + 1 个配置 |
| 硬件要求 | 单 GPU（H100 测试），Python 3.10+ |

## 核心架构：三文件设计

```
prepare.py   — 只读。数据准备、tokenizer、评估工具
train.py     — 唯一可修改文件。模型、优化器、训练循环
program.md   — 人类编辑的指令文件，告诉 Agent 怎么做研究
```

**极简到极致**：Agent 只改 `train.py`，每次只改一个东西，跑 5 分钟，看 `val_bpb`（validation bits per byte），低了就保留 git commit，高了就 git reset 回滚。

## 核心循环（"Karpathy Loop" / "Ratchet Loop"）

```
LOOP:
  1. 读取当前 train.py
  2. 提出一个改动（改架构/超参/优化器/bs 等）
  3. git commit
  4. 跑 5 分钟训练
  5. 测 val_bpb
  6. 改善了 → 保留 commit，继续
  7. 没改善 → git reset，试下一个
```

**关键设计约束**：
- 固定 5 分钟时间预算 → 每次实验直接可比，约 12 次/小时，100 次/晚
- 唯一指标 `val_bpb` → 没有歧义
- 二元决策保留/丢弃 → 没有"可能以后有用"
- 永不停止 → 一直跑

## 实际效果

Karpathy 跑了一晚：37 次实验，8 小时，模型质量提升 **19%**。Agent 尝试了改架构、调学习率、换优化器、改 batch size 等，自动筛选出有效改动。

## 为什么重要

### 1. 不是"AI 写代码"，是"AI 做研究"

传统 AutoML（网格搜索、贝叶斯优化）是在固定搜索空间里调参。AutoResearch 的搜索空间是 **LLM 能想到的任何东西**——改架构、加正则化、换 tokenizer 策略，没有预设边界。

### 2. 通用模式，不限于 LLM 训练

抽象后的通用配方：

| 组件 | 含义 |
|:---|:---|
| 一个可修改的文件 | Agent 的"操作面" |
| 一个指标 | 优化目标，必须可量化 |
| 固定评估预算 | 每次实验公平可比 |
| 保留/丢弃规则 | 二元决策，防止漂移 |

**适用场景**：
- 因子挖掘（AlphaGen 类似思路！）
- A/B 测试优化
- 量化策略回测
- 系统性能调优
- 任何"有明确指标 + 可自动评估"的迭代任务

### 3. 从"Vibe Coding"到"Agentic Engineering"

Karpathy 的阶段性划分：
- **Vibe Coding（2024-2025）**：人 prompts，AI 写代码，人 review
- **Agentic Engineering（2026+）**：人指挥 Agent 团队，Agent 自主执行
- **Loopy Era**：Agent 闭环自改进，人睡觉，Agent 干活

## 局限性

1. **单 GPU 限制**：只能跑小模型，大规模分布式训练不适用
2. **需要明确指标**：开放式研究（如"让模型更有创造力"）无法量化
3. **Agent 质量依赖**：如果 Agent 不够聪明，会陷入局部最优或瞎改
4. **5 分钟窗口很小**：只能验证小幅改进，大改（如换架构）需要更多时间
5. **不是替代研究者**：研究方向、假设生成、创造性突破仍需人类

## 与 AlphaGen 的对比

| 维度 | AlphaGen | AutoResearch |
|:---|:---|:---|
| 领域 | 量化因子挖掘 | LLM 训练 |
| 搜索空间 | 公式表达式 | 任意代码改动 |
| 优化方式 | RL（MaskablePPO）| 爬山法（LLM 引导） |
| 指标 | IC / Rank IC | val_bpb |
| 评估 | 因子计算 | 5 分钟训练 |
| Agent 角色 | RL 策略网络 | 外部 LLM（Claude/Codex） |
| 核心差异 | 预定义表达式空间 | 开放搜索空间 |

**本质相同**：都是"Agent 自动迭代 → 评估 → 保留好的"，只是 AlphaGen 用 RL 在固定空间搜索，AutoResearch 用 LLM 在开放空间搜索。

## 关键判断

AutoResearch 不是又一个"AI 写代码"的 demo，它是一个**方法论宣言**：把"做实验"这个人类研究者的核心活动，变成 Agent 可以闭环执行的自动化流程。

对我们做量化有意义：AlphaGen 的 RL 因子挖掘 + AutoResearch 的开放搜索思路，可以结合——让 Agent 不仅挖因子，还能自动改模型架构、调超参、换数据预处理，真正实现"睡觉时跑回测、醒来看结果"。