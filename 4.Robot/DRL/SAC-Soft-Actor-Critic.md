---
title: SAC-Soft-Actor-Critic
type: paper-note
created: 2026-06-01
tags: [reinforcement-learning, paper-note, off-policy, continuous-control]
---

## 论文信息
- **标题**: Soft Actor-Critic: Off-Policy Maximum Entropy Deep Reinforcement Learning with a Stochastic Actor
- **作者/机构**: Tuomas Haarnoja, Aurick Zhou, Pieter Abbeel, Sergey Levine (UC Berkeley)
- **发表时间**: ICML 2018
- **arXiv**: https://arxiv.org/abs/1801.01290
- **后续改进**: "Soft Actor-Critic Algorithms and Applications" (arXiv:1812.05905, 2018) — 引入自动温度调节

## 核心问题

深度强化学习在连续控制任务中面临三个核心挑战：(1) **样本效率低**——on-policy 方法（如 PPO、TRPO）每次更新后需要重新采样，在真实机器人场景中数据采集成本极高；(2) **超参数敏感**——RL 算法对超参数极其敏感，不同任务需要不同的探索策略；(3) **收敛脆弱**——确定性策略（如 DDPG、TD3）虽然样本效率高，但对初始化和超参数极为敏感，往往需要大量调参。

SAC 的核心思路：**将最大熵（Maximum Entropy）原则融入 actor-critic 框架，在最大化回报的同时最大化策略的熵，既保证探索又保证样本效率。**

## 为什么 SAC 在机器人学习中如此重要

在具身智能中，SAC 是**最常用的 off-policy RL 算法**，原因有三：

1. **样本效率**：off-policy + experience replay → 真实机器人数据昂贵，SAC 最大程度复用每条数据
2. **自动探索**：最大熵框架天然鼓励探索，不需要手动设计探索噪声（对比 DDPG 需要人工加 OU 噪声）
3. **CQL 和 IQL 的基础**：这两篇离线 RL 核心论文直接基于 SAC 框架构建——CQL 在 SAC 的 Q 函数更新上加保守正则化，IQL 在 SAC 的 critic 上改用 expectile regression。不学 SAC 就无法理解离线 RL。

## 关键方法

### 1. 最大熵目标函数

标准 RL 最大化 $\sum_t \mathbb{E}_{(s_t, a_t)}[\gamma^t r(s_t, a_t)]$

SAC 最大化 $\sum_t \mathbb{E}_{(s_t, a_t)}[\gamma^t (r(s_t, a_t) + \alpha \mathcal{H}(\pi(\cdot | s_t)))]$

其中 $\mathcal{H}$ 是策略的熵（衡量动作的随机性），$\alpha$ 是温度参数（tradeoff 探索 vs 利用）。

**直觉**：策略不仅要选能获得高奖励的动作，还要保持动作的多样性（高熵）。这迫使策略在不确定时保持探索，在确定时收敛到最优。

### 2. 三个核心组件

**Actor（策略网络）**: $\pi_\phi(a|s)$，输出高斯分布的均值和方差，通过重参数化技巧采样

**Critic（双 Q 网络）**: $Q_{\theta_1}(s, a)$, $Q_{\theta_2}(s, a)$，取两者的较小值作为目标 Q 值（Clipped Double Q-learning，来自 TD3）

**Temperature（温度参数）**: $\alpha$，控制熵项权重。v1 版手动设定；v2 版自动调节：$\alpha$ 通过梯度下降最小化 $-\alpha(\log \pi(a|s) + \bar{\mathcal{H}})$，其中 $\bar{\mathcal{H}}$ 是目标熵（通常设为 $-dim(\mathcal{A})$）

### 3. Soft Q-learning 的 Bellman 方程

标准的 Q-learning Bellman 方程：

$$Q(s, a) \leftarrow r + \gamma \max_{a'} Q(s', a')$$

SAC 的 Soft Bellman 方程：

$$Q(s, a) \leftarrow r + \gamma \mathbb{E}_{a' \sim \pi} \left[ \min_{j=1,2} Q_{\bar{\theta}_j}(s', a') - \alpha \log \pi_\phi(a' | s') \right]$$

关键区别：不是取 $\max_{a'} Q$，而是从策略采样并减去熵项。这避免了 max 操作的高估偏差，同时鼓励探索。

### 4. Actor 更新：重参数化技巧

Actor 通过**最小化 KL 散度**来更新，等价于最大化：

$$J_\pi(\phi) = \mathbb{E}_{s \sim \mathcal{D}} \left[ \min_{j=1,2} Q_{\theta_j}(s, \tilde{a}_\phi(s)) - \alpha \log \pi_\phi(\tilde{a}_\phi(s) | s) \right]$$

其中 $\tilde{a}_\phi(s)$ 使用重参数化技巧：$\tilde{a} = \mu_\phi(s) + \sigma_\phi(s) \cdot \epsilon$，$\epsilon \sim \mathcal{N}(0, 1)$。这使得梯度可以通过采样动作反向传播到策略参数。

### 5. 自动温度调节（SAC v2）

$\alpha$ 的损失函数：

$$J(\alpha) = \mathbb{E}_{a \sim \pi} \left[ -\alpha \log \pi(a|s) - \alpha \bar{\mathcal{H}} \right]$$

- 当策略熵低于目标熵 $\bar{\mathcal{H}}$ 时 → 增大 $\alpha$ → 加强探索
- 当策略熵高于目标熵时 → 减小 $\alpha$ → 加强利用
- 目标熵通常设为 $\bar{\mathcal{H}} = -\dim(\mathcal{A})$（动作维度的负值）

## 重要细节

- **双 Q 网络**：与 TD3 一致，使用两个 Q 网络取 min 来缓解高估偏差
- **目标网络软更新**：$\bar{\theta} \leftarrow \tau \theta + (1-\tau) \bar{\theta}$，$\tau \ll 1$（如 0.005），比 DQN 的硬更新更稳定
- **经验回放**：标准 replay buffer，随机采样 mini-batch
- **策略形式**：高斯分布，$\pi_\phi(a|s) = \mathcal{N}(\mu_\phi(s), \sigma_\phi(s)^2)$，tanh 压缩到动作空间边界
- **连续动作空间**：这是 SAC 的设计目标，离散版本有单独的工作

## SAC vs TD3 vs PPO 对比

| | SAC | TD3 | PPO |
|------|------|------|------|
| 策略类型 | 随机（高斯） | 确定性 + 噪声 | 随机（高斯） |
| On/Off-policy | Off-policy | Off-policy | On-policy |
| 探索机制 | 最大熵（自动） | 手动加噪声 | 随机策略 |
| 样本效率 | 高 | 高 | 低 |
| 超参数敏感度 | 低（自动调 α） | 中 | 中 |
| 机器人场景 | 真实机器人首选 | 仿真/操控任务 | 仿真大规模并行 |

## 在 VLA / 具身智能中的角色

- **CQL 直接基于 SAC**：CQL 在 SAC 的 Q 更新上加了一项保守正则化——对 OOD 动作的 Q 值惩罚
- **IQL 基于 SAC 的 critic 结构**：用 expectile regression 替代标准 Bellman 更新
- **BC + SAC 混合范式**：先用 BC 从演示数据初始化策略，再用 SAC fine-tune——这是面试 Q19 的标准答案
- **真实机器人 RL 的首选算法**：因为 off-policy 样本效率高，最大熵自动探索，不需要大量并行环境

## 与面试50题的关系

- **Q19**: IL vs RL 对比 → BC + SAC 是标准混合范式
- **Q21**: On-policy vs Off-policy → SAC 是 off-policy 代表，适合真实机器人
- **Q26**: Offline RL → CQL/IQL 均基于 SAC 框架
- **Q20**: 奖励函数设计 → SAC 的最大熵目标本身是一种隐式的奖励 shaping

## 个人思考

<留空>