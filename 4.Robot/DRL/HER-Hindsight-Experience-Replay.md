---
title: HER-Hindsight-Experience-Replay
type: paper-note
created: 2026-06-01
tags: [reinforcement-learning, paper-note, goal-conditioned-rl, robotics]
---

## 论文信息
- **标题**: Hindsight Experience Replay
- **作者/机构**: Marcin Andrychowicz, Filip Wolski, Alex Ray, Jonas Schneider, Rachel Fong, Peter Welinder, Bob McGrew, Josh Tobin, Pieter Abbeel, Wojciech Zaremba (OpenAI)
- **发表时间**: NeurIPS 2017
- **arXiv/链接**: https://arxiv.org/abs/1707.01495

## 核心问题
强化学习在稀疏奖励（sparse reward）任务中训练极其困难——在机器人操作任务中，随机探索几乎不可能碰巧完成目标（如将物体推到指定位置）。传统做法是设计密集的成形奖励（reward shaping），但这需要大量领域知识且容易引入偏差。HER 的核心问题是：能否在不设计密集奖励的情况下，只用二元的稀疏奖励来训练策略？

## 关键方法
1. **事后经验回放（核心思想）**：在一个 episode 没有达成原定目标时，不丢弃这些经验——既然智能体最终到达了某个状态 $s_T$，就把这个 $s_T$ 当作「本来就要达成的目标」，重新标记（relabel）该 episode 中的每一条 transition
2. **目标条件策略（Universal Policy）**：策略的输入不仅是当前状态，还包括目标 $g$：$\pi(s, g)$。这样同一策略可以处理不同的目标
3. **与环境无关**：目标只影响智能体的动作选择，不影响环境动力学，因此可以用任意目标重放任何轨迹（适用于所有 off-policy 算法）
4. **隐式课程学习**：初始阶段随机策略容易达成的目标（如近距离移动）会自动成为早期训练样本，随着策略改善，更远的目标逐步被达成和重放，形成自然的课程
5. **目标采样策略**：提供多种选择——`final`（用最终状态作为目标）、`future`（从该 transition 之后的未来状态中随机采样 k 个作为目标）、`episode`（从同 episode 中随机选状态）、`random`（随机生成目标）

## 重要细节
**HER 算法流程**：
1. 采样一个 episode（使用某种 exploration + off-policy RL 算法如 DDPG）
2. 对每个 transition $(s_t, a_t, r_t, s_{t+1})$ 以及原目标 $g$：
   - 存入 replay buffer 一条记录：$(s_t, a_t, r_t, s_{t+1}, g)$
   - 额外存入一条或多条记录（HER）：$(s_t, a_t, r'_t, s_{t+1}, g')$，其中 $g'$ 是重新选择的目标，$r'_t$ 是对应新目标的奖励

**奖励函数**（稀疏二元）：
$$r(s, a, g) = -\mathbb{1}[f_g(s') \neq 0]$$
即到达目标给 0，未到达给 -1（或使用 0/1 的到达指示）。

**实验任务**（MuJoCo Fetch Robotics 环境）：
- Pushing：将盒子推到桌面上的目标位置
- Sliding：击打冰球使其滑行到远处目标
- Pick-and-Place：将物体抓取并放到空中目标位置

**关键发现**：
- DDPG + HER 在三个任务上几乎完美解决，而纯 DDPG 完全失败
- HER 对稀疏奖励的性能优于成形奖励（出人意料）
- `future` 策略（k=4）在目标采样中效果最好
- Sim2Real：在仿真中训练的 pick-and-place 策略可直接部署到真实 Fetch 机器人

## 与面试50题的关系
对应 Q22（稀疏奖励问题的解决方法）。HER 是处理稀疏奖励最经典的技巧之一，也是目标条件 RL（goal-conditioned RL）的奠基性工作。

## 个人思考