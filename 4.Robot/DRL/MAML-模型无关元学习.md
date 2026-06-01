---
title: MAML-模型无关元学习
type: paper-note
created: 2026-06-01
tags: [reinforcement-learning, paper-note, meta-learning, few-shot-learning]
---

## 论文信息
- **标题**: Model-Agnostic Meta-Learning for Fast Adaptation of Deep Networks
- **作者/机构**: Chelsea Finn, Pieter Abbeel, Sergey Levine (UC Berkeley)
- **发表时间**: ICML 2017
- **arXiv/链接**: https://arxiv.org/abs/1703.03400

## 核心问题
元学习（meta-learning）的目标是让模型「学会学习」（learn to learn）——在少量新任务样本上快速适应。然而之前的元学习方法（如 Meta-LSTM、Matching Networks、Siamese Networks）都对模型架构有特定要求（如需要 RNN 或特殊的特征提取结构）。MAML 提出的问题是：能否设计一种通用的、与模型架构无关的元学习算法，只需梯度下降即可适用于分类、回归、强化学习等各种任务？

## 关键方法
1. **优化初始参数**：MAML 的核心思想是学习一组模型初始参数 $\theta$，使得在该参数基础上仅用少量梯度步（1-5 步）就能在新任务上达到高性能
2. **双层优化**：
   - **内循环（Inner Loop）**：对每个任务 $\mathcal{T}_i$，用 support set 做 1 到 K 步梯度下降得到任务特定参数 $\theta_i' = \theta - \alpha \nabla_\theta \mathcal{L}_{\mathcal{T}_i}(f_\theta)$
   - **外循环（Outer Loop/Meta-Update）**：在所有任务上优化元目标 $\min_\theta \sum_{\mathcal{T}_i} \mathcal{L}_{\mathcal{T}_i}(f_{\theta_i'})$，即优化初始参数使适应后的参数在 query set 上表现好
3. **二阶梯度**：外循环的梯度需要计算 $\nabla_\theta \mathcal{L}(f_{\theta_i'})$，这涉及二阶导数（梯度穿过内循环的梯度步骤）。MAML 使用 Hessian-vector 积来实现；也提供了忽略二阶项的一阶近似版本 FOMAML
4. **模型无关**：不限制模型架构——全连接网络、CNN、RNN 都可以用；不增加额外参数——Meta-LSTM 需要额外 LSTM 作为 meta-learner，MAML 完全不需要
5. **适用于 RL**：在强化学习中，MAML 学习一个初始策略参数，使得在新任务上仅需少量策略梯度步骤就能学会，实验显示显著快于随机初始化或预训练的 fine-tuning

## 重要细节
**MAML 算法（监督学习）**：
1. 采样一批任务 $\{\mathcal{T}_i\}$
2. 对每个任务，用 support set 计算：$\theta_i' = \theta - \alpha \nabla_\theta \mathcal{L}_{\mathcal{T}_i}(f_\theta)$
3. 用 query set 计算 meta-loss 并更新：$\theta \leftarrow \theta - \beta \nabla_\theta \sum_i \mathcal{L}_{\mathcal{T}_i}(f_{\theta_i'})$

**MAML 的 RL 版本**：
- 内循环：$\theta_i' = \theta + \alpha \nabla_\theta J_{\mathcal{T}_i}(\theta)$（策略梯度上升）
- 外循环：$\theta \leftarrow \theta + \beta \nabla_\theta \sum_i J_{\mathcal{T}_i}'(\theta_i')$
- $J_{\mathcal{T}_i}$ 和 $J_{\mathcal{T}_i}'$ 分别是 support 和 query rollout 的期望回报

**实验结果**：
- **Few-shot 分类**：在 Omniglot（5-way 1-shot/5-shot）和 MiniImageNet 上达到或超越专门设计的 few-shot 方法
- **Few-shot 回归**：用 5-10 个点准确拟合正弦波
- **RL 适应**：在 MuJoCo 的 2D Navigation 和 HalfCheetah 多任务（不同速度和方向）上，MAML 的速度远快于预训练 baseline

**一阶近似 MAML（FOMAML）**：
$$\theta \leftarrow \theta - \beta \sum_i \nabla_{\theta_i'} \mathcal{L}_{\mathcal{T}_i}(f_{\theta_i'})$$
忽略 $\nabla_\theta \theta_i'$ 中的二阶项，计算量大幅减少且实际效果相近。

## 与面试50题的关系
对应 Q25（元学习/Meta-Learning 在 RL 中的应用）。MAML 是元学习领域引用量最高的论文之一，其「优化初始参数使其易于快速适应」的思想影响了后续 RL$^2$、PEARL 等一系列工作。

## 个人思考