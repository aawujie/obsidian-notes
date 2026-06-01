---
title: IQL-Implicit-Q-Learning
type: paper-note
created: 2026-06-01
tags: [reinforcement-learning, paper-note, offline-rl]
---

## 论文信息
- **标题**: Offline Reinforcement Learning with Implicit Q-Learning
- **作者/机构**: Ilya Kostrikov, Ashvin Nair, Sergey Levine (UC Berkeley)
- **发表时间**: ICLR 2022
- **arXiv/链接**: https://arxiv.org/abs/2110.06169

## 核心问题
CQL 等离线 RL 方法在训练时需要显式地对 OOD 动作的 Q 值进行保守估计，这引入了额外的超参数和复杂性。IQL 的目标是：能否完全避免查询 OOD 动作，仅在数据分布内完成 Q 函数和策略的学习？

## 关键方法
1. **完全避免 OOD 查询**：IQL 的核心洞察是：不需要显式查询 OOD 动作来压它们的 Q 值，而是通过 expectile regression 在数据分布内直接估计最优策略对应的价值函数
2. **Expectile Regression 估计 V 函数**：使用 $\tau$-expectile 回归（$\tau \in (0.5, 1)$）来逼近 $\max_a Q(s,a)$。τ 越接近 1，越接近最大值；τ=0.5 退化为均值。关键是只用数据集中的动作，无需采样策略动作
3. **解耦训练**：先训练 $V_\psi$（用 expectile regression），再训练 $Q_\theta$（用标准 MSE + V 目标），最后用 advantage-weighted regression (AWR) 提取策略 $\pi_\phi$，三步独立
4. **超参数简单**：只需要一个关键超参数 $\tau$（expectile 分位数，通常设为 0.7-0.9），远少于 CQL（需要调 α、温度等）
5. **在稀疏奖励任务上表现突出**：IQL 在 AntMaze（大型迷宫的稀疏奖励导航）上显著优于 CQL 和 TD3+BC，因为 expectile 不会像保守惩罚那样过度压低价值

## 重要细节
IQL 的三个损失函数：

**V 函数（Expectile Regression）**：
$$L_V(\psi) = \mathbb{E}_{(s,a) \sim \mathcal{D}} \left[ L_2^\tau (Q_{\hat{\theta}}(s,a) - V_\psi(s)) \right]$$
其中 $L_2^\tau(u) = |\tau - \mathbb{1}(u < 0)| \cdot u^2$ 是 expectile loss。

**Q 函数（标准 TD）**：
$$L_Q(\theta) = \mathbb{E}_{(s,a,s') \sim \mathcal{D}} \left[ (Q_\theta(s,a) - (r + \gamma V_\psi(s')))^2 \right]$$

**策略提取（AWR）**：
$$L_\pi(\phi) = \mathbb{E}_{(s,a) \sim \mathcal{D}} \left[ \exp\left( \beta (Q_\theta(s,a) - V_\psi(s)) \right) \cdot \log \pi_\phi(a|s) \right]$$

关键参数：$\tau$ 控制保守程度（expectile），$\beta$ 控制 AWR 的温度。

## 与面试50题的关系
对应 Q26（离线强化学习算法）。IQL 通过 expectile regression 避免 OOD 查询，是离线 RL 中设计理念与 CQL 截然不同的重要方法。

## 个人思考