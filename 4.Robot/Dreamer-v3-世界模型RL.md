---
title: Dreamer-v3-世界模型RL
type: paper-note
created: 2026-06-01
tags: [embodied-ai, paper-note, world-model, reinforcement-learning, rl]
---

## 论文信息
- **标题**: Mastering Diverse Domains through World Models
- **作者/机构**: Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, Timothy Lillicrap — Google DeepMind / University of Toronto
- **发表时间**: 2023 (arXiv:2301.04104)
- **arXiv/链接**: https://arxiv.org/abs/2301.04104
- **发表会议**: NeurIPS 2023 (Oral)

## 核心问题
强化学习算法通常需要针对每个任务手动调整超参数，且很难在多种不同类型的任务上同时表现良好。**Dreamer v3 要解决的核心问题是：能否设计一个通用的 RL 算法，使用同一组固定超参数，在从简单控制到复杂 3D 世界的各种任务上都取得好效果？**

## 关键方法

1. **世界模型架构 — RSSM (Recurrent State-Space Model)**
   世界模型是 Dreamer 的核心，它学习环境的紧凑潜在表示并预测未来状态：
   - **编码器 (Encoder)**: CNN 将原始像素图像编码为潜在表示
   - **确定性状态** $h_t$: 通过 GRU 循环网络聚合历史信息
   - **随机状态** $z_t$: 从学习的类别分布中采样，捕捉多模态不确定性
   - **动态预测器**: 预测下一时刻的潜在状态分布 $p(z_{t+1} | h_t, z_t)$
   - **奖励/继续预测器**: MLP 从潜在状态预测奖励和 episode 是否结束

2. **在想象中训练 (Imagination Training)**
   Actor 和 Critic 完全在世界模型的"想象"中训练，不需要额外的环境交互：
   - 从世界模型生成想象 rollout
   - Actor 学习最大化想象 rollout 中的预测奖励
   - Critic 估计状态价值以降低 Actor 梯度更新的方差
   - 这大大提高了样本效率

3. **Symlog 预测**
   使用对称对数变换 (symlog) 处理奖励和价值的预测：
   $$symlog(x) = sign(x) \cdot \ln(|x| + 1)$$
   这使单个模型能处理不同任务中奖励尺度的巨大差异（从 Atari 的个位数到 Minecraft 的数千）。

4. **离散潜在变量 + Straight-Through 梯度**
   使用类别潜在变量 (categorical latents) 而非连续高斯分布，能更好地表示多模态分布。Straight-Through 估计器保证梯度可以反向传播。

5. **固定超参数，跨域泛化**
   同一组超参数在 150+ 任务上表现良好：
   - DMControl Suite（连续控制）
   - Atari 游戏（离散动作、像素输入）
   - DMLab（3D 导航）
   - Minecraft（开放世界、稀疏奖励）— **首个从零开始收集钻石的算法**

## 重要细节

- **Minecraft 钻石挑战**: Dreamer v3 是第一个无需人类演示或手工课程就能在 Minecraft 中从零收集钻石的算法，这是 RL 领域的一个里程碑
- **可扩展性**: 模型性能随参数增加而自然提升，不需要改变超参数
- **世界模型 vs 无模型**: Dreamer v3 的样本效率远高于无模型方法（如 PPO），因为世界模型可以在想象中学习
- **与 Dreamer v1/v2 的对比**: v3 主要改进了 symlog 预测、更大的模型容量、更好的离散潜在表示
- **局限性**: 世界模型的训练需要大量计算；在极高维度的观测空间（如 3D 渲染）中，视频预测质量可能下降；长序列的想象 rollout 可能累积误差

## 与面试50题的关系
- **Q17**: 世界模型 (World Model) 在具身智能中的作用 — Dreamer v3 是当前最先进的基于世界模型的 RL 算法，展示了世界模型如何实现跨域泛化和高效样本利用

## 个人思考