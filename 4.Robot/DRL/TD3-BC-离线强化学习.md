---
title: TD3-BC-离线强化学习
type: paper-note
created: 2026-06-01
tags: [reinforcement-learning, paper-note, offline-rl]
---

## 论文信息
- **标题**: A Minimalist Approach to Offline Reinforcement Learning
- **作者/机构**: Scott Fujimoto, Shixiang Shane Gu (McGill University / Google Brain)
- **发表时间**: NeurIPS 2021
- **arXiv/链接**: https://arxiv.org/abs/2106.06860

## 核心问题
离线 RL 领域的方法（CQL、BEAR、BRAC 等）越来越复杂，引入大量组件和超参数。TD3+BC 提出一个核心问题：能否只对标准的 online RL 算法做极简修改，就在离线场景达到竞争性的效果？

## 关键方法
1. **极简设计**：只需在标准 TD3 的策略更新目标中加一个行为克隆（BC）正则化项，即让策略不仅最大化 Q 值，还要保持与数据集中动作的接近
2. **策略更新目标**：$\pi = \arg\max_\pi \ \mathbb{E}_{(s,a) \sim \mathcal{D}} \left[ \lambda Q(s, \pi(s)) - (\pi(s) - a)^2 \right]$
   - 第一项：标准 TD3 的 Q 值最大化
   - 第二项：BC 正则化，惩罚策略输出与数据集动作的偏差
3. **仅一个额外超参数 $\lambda$**：平衡 Q 值最大化和分布匹配，通常归一化后设为 2.5
4. **状态归一化**：对状态做均值-方差归一化，使得 Q 值和 BC 损失的尺度可比，从而 $\lambda$ 可以在不同任务间通用
5. **效果惊人**：在 D4RL MuJoCo 的 locomotion 任务上，这个极简方法达到或超过 CQL、BRAC 等复杂方法的效果。在 locomotion 任务上尤其强

## 重要细节
**策略更新（归一化后）**：
$$\pi = \arg\max_\pi \ \mathbb{E}_{(s,a) \sim \mathcal{D}} \left[ \lambda \frac{Q(s, \pi(s))}{\frac{1}{N}\sum_i |Q_i|} - (\pi(s) - a)^2 \right]$$

其中 Q 值用 batch 内 Q 值的绝对值均值做归一化，$\lambda$ 通常设为 2.5。

**关键设计选择**：
- 使用 TD3（而非 SAC），因为 TD3 的确定性策略使 BC 正则化更自然
- 不做任何修改地保留 TD3 的 clipped double Q-learning 和 target policy smoothing
- BC 正则化只在 state 上做（不额外约束 action noise）

**局限性**：TD3+BC 在 locomotion 任务上很强，但在 AntMaze 等稀疏奖励导航任务上远不如 IQL。因为 BC 正则化会拖累策略偏离数据集，而在需要推理性探索的任务中，纯 BC 约束过于保守。

## 与面试50题的关系
对应 Q26（离线强化学习算法）。TD3+BC 是理解离线 RL 的最简单入口——它证明了有时候简单的正则化就足够，是离线 RL 的重要 baseline。

## 个人思考