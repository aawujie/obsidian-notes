---
title: EUREKA-LLM奖励函数设计
type: paper-note
created: 2026-06-01
tags: [reinforcement-learning, paper-note, llm, reward-design, robotics]
---

## 论文信息
- **标题**: EUREKA: Human-Level Reward Design via Coding Large Language Models
- **作者/机构**: Yecheng Jason Ma, William Liang, Guanzhi Wang, De-An Huang, Osbert Bastani, Dinesh Jayaraman, Yuke Zhu, Linxi "Jim" Fan, Anima Anandkumar (NVIDIA, UPenn, Caltech, UT Austin)
- **发表时间**: NeurIPS 2024 (Oral, 首次发布于 2023 年 10 月)
- **arXiv/链接**: https://arxiv.org/abs/2310.12931

## 核心问题
强化学习中的奖励函数设计（reward engineering）是一个高度依赖专家经验的试错过程，尤其是在机器人操作等复杂任务中。EUREKA 探索的问题是：能否利用 LLM 的代码生成能力来自动化奖励函数设计，并且达到甚至超越人类专家的水平？

## 关键方法
1. **LLM 生成奖励函数代码**：给 GPT-4 提供环境源代码（Observation/Action 定义等）和任务的自然语言描述，LLM 直接生成 Python 格式的奖励函数代码
2. **环境上下文作为 Prompt**：不需要手动编写任务描述——直接将 Gymnasium/IsaacGym 环境的源代码（不含奖励函数部分）作为 prompt 的一部分，让 LLM 理解状态空间和物理语义
3. **迭代优化 + 反思机制**：LLM 先批量生成多个候选奖励函数，用每个候选训练一个简短策略，根据训练曲线（reward trace）自动生成反思文本，指导下一轮奖励函数的改进
4. **零样本泛化到新形态机器人**：EUREKA 可以生成针对人形机器人、四足机器人、灵巧手等不同形态的奖励函数，无需针对每种形态重新设计
5. **超越人类设计的奖励**：在 29 个开源 RL 环境中的 83% 任务上，EUREKA 生成的奖励函数训练出的策略优于人类专家设计的奖励

## 重要细节
**EUREKA 工作流程**：
1. **输入**：环境源代码 + 高层任务描述（如 "make the humanoid run as fast as possible"）
2. **初始生成**：GPT-4 生成 N 个独立的奖励函数候选（如 N=16），每个是独立的 Python 函数
3. **GPU 并行训练**：对每个候选奖励函数，在 Isaac Gym 上并行训练一个简短 RL 策略
4. **自动评估与反思**：根据训练曲线和关键指标（如速度、稳定性等），LLM 自动生成反思文本，分析哪些设计有效、哪些失败
5. **迭代改进**：基于反思和上次的最佳奖励函数，LLM 生成下一批改进版本
6. **输出**：最佳奖励函数 + 训练好的策略

**关键设计**：
- 使用 `gymnasium` / `IsaacGym` 的 `env.step()` 和 `env.reset()` 等标准 API
- 奖励函数以 `compute_reward(obs, action, ...)` 的函数签名输出
- 环境源代码直接作为 prompt（而非人工抽象），减少信息损失
- 支持从简单到复杂任务的 curriculum

**实验覆盖**：
- IsaacGym 的 10 种机器人环境（Ant, Humanoid, Quadcopter 等）
- dexterous manipulation（灵巧手操作）：ShadowHand 转笔、开锁等
- 总计 29 个不同难度级别的任务

## 与面试50题的关系
对应 Q20（强化学习中的奖励函数设计问题）。EUREKA 展示了 LLM 在自动化 RL 工程流程中的巨大潜力，是 RL + LLM 交叉领域的代表性工作。

## 个人思考