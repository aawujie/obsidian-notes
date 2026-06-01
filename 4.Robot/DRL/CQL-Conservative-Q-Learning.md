---
title: CQL-Conservative-Q-Learning
type: paper-note
created: 2026-06-01
tags: [reinforcement-learning, paper-note, offline-rl]
---

## 论文信息
- **标题**: Conservative Q-Learning for Offline Reinforcement Learning
- **作者/机构**: Aviral Kumar, Aurick Zhou, George Tucker, Sergey Levine (UC Berkeley / Google Research)
- **发表时间**: NeurIPS 2020
- **arXiv/链接**: https://arxiv.org/abs/2006.04779

## 核心问题
离线强化学习中，标准的 Q-learning 算法（如 SAC、TD3）会因分布偏移（distributional shift）导致对 OOD（out-of-distribution）动作的 Q 值过高估计，从而使学到的策略在真实环境中表现差。CQL 的目标是在不访问环境的情况下，从固定的离线数据集中学到安全且有效的策略。

## 关键方法
1. **保守的 Q 值估计**：在标准 Bellman 误差的基础上，增加一个正则化项，对数据集中未出现的动作的 Q 值进行惩罚（压低 OOD 动作的 Q 值），同时提升数据集中动作的 Q 值
2. **下界保证**：CQL 在理论上保证学到的 Q 函数是对真实 Q 函数的下界（lower bound），从而避免过高估计导致的策略崩溃
3. **与 SAC 兼容**：CQL 可以直接作为 SAC 的 Q 函数学习部分插入，称为 CQL-SAC，改动小但效果显著
4. **多种变体**：CQL($\mathcal{H}$) 加入熵正则化，CQL($\rho$) 对策略分布进行约束，均是在贝尔曼误差基础上加正则化项
5. **在 D4RL 基准上达到 SOTA**：在 HalfCheetah、Hopper、Walker2d 等 MuJoCo 任务上，CQL 显著优于 BCQ、BEAR、BRAC 等离线 RL 方法

## 重要细节
CQL 的核心公式是在 Q 函数更新时加入惩罚项：

$$\min_Q \ \alpha \left( \mathbb{E}_{s \sim \mathcal{D}, a \sim \pi} [Q(s,a)] - \mathbb{E}_{s,a \sim \mathcal{D}} [Q(s,a)] \right) + \frac{1}{2} \mathbb{E}_{s,a,s' \sim \mathcal{D}} \left[ (Q(s,a) - \mathcal{B}^\pi\hat{Q}(s,a))^2 \right]$$

其中 $\mathcal{B}^\pi$ 是贝尔曼算子。第一项鼓励对数据集内动作的 Q 值升高、对当前策略可能产生的 OOD 动作的 Q 值压低；第二项是标准 TD 误差。

CQL 的关键超参数是 $\alpha$（保守程度），$\alpha$ 越大越保守。实践中通常将 $\alpha$ 设为固定值（如 5.0 或 10.0），在 D4RL 任务上表现良好。

## 与面试50题的关系
对应 Q26（离线强化学习算法），CQL 是离线 RL 中最经典的算法之一，通过添加保守惩罚项解决分布偏移问题。

## 个人思考