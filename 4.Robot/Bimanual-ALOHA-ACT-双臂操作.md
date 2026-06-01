---
title: ALOHA + ACT (双臂操作)
type: paper-note
created: 2026-06-01
tags: [embodied-ai, paper-note, bimanual-manipulation, imitation-learning]
---

## 论文信息
- **标题**: Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware
- **作者/机构**: Tony Z. Zhao (Stanford), Vikash Kumar (Meta), Sergey Levine (UC Berkeley), Chelsea Finn (Stanford)
- **发表时间**: 2023年 (RSS 2023)
- **arXiv/链接**: https://arxiv.org/abs/2304.13705
- **项目页面**: https://tonyzhaozh.github.io/aloha/

## 核心问题
精细双臂操作任务（如穿线、装电池、打开透明的调料杯盖）需要在力的控制和视觉反馈之间精确协调，传统上需要昂贵的高精度机器人和传感器。能否用**低成本硬件+模仿学习**实现这些精细操作？模仿学习在精确任务中面临的主要挑战是**组合误差（compounding errors）**——预测误差随时间累积导致策略偏离训练分布。

## 关键方法

1. **ALOHA 硬件系统** (A Low-cost Open-source Hardware System for Bimanual Teleoperation):
   - 总成本 < $20,000，使用市售 ViperX 机械臂和 3D 打印组件
   - Leader-Follower 架构：操作者通过反向驱动（backdriving）leader 臂来遥控 follower 臂
   - 系统包含 4 个摄像头（用于不同视角的视觉反馈）、2 个 ViperX 300 臂（6-DoF + 1-DoF 夹爪）、Dynamixel 伺服电机

2. **Action Chunking（动作分块）**: 策略不预测单个下一步动作，而是预测未来 $k$ 步的连续动作序列（a chunk）。这减少了有效任务时间范围的 $k$ 倍，缓解了组合误差问题。此外，chunk 内的动作可以建模人类演示中的非马尔可夫行为（如暂停）。

3. **Temporal Ensembling（时序集成）**: 在每个时间步都查询策略，重叠的 action chunks 通过指数加权平均组合，以产生平滑的机器人运动。关键改进：是对同一时间步的多个预测做平均（而非对相邻时间步做平滑），避免了偏差。

4. **Conditional VAE + Transformer 架构**: 策略被训练为条件 VAE（CVAE），使用 Transformer 来编码多视角图像和关节位置，生成 action chunk：
   - **Encoder**: BERT-style Transformer，将 action chunk 压缩为 style variable $z$
   - **Decoder/Policy**: ResNet 图像编码器 + Transformer Encoder（融合视觉、关节状态、$z$）+ Transformer Decoder（生成目标关节位置序列）
   - 测试时 $z$ 设为零（先验均值），不采样

5. **少量演示，高效学习**: 仅需 ~10 分钟的遥操作演示数据，即可以 80-90% 的成功率学习 6 种复杂任务（如打开调料杯、装电池、套扎带）。

## 重要细节

- 观测空间：4 张 480x640 RGB 图像 + 14 维关节位置（双臂各 7 DoF）
- 动作空间：14 维绝对目标关节位置（非增量位置，实验发现增量位置导致性能下降）
- Chunk 大小 $k$ 通常设为 100（对应约 2 秒）
- 使用 L1 loss（而非 L2）训练，L1 对精确建模动作序列更有效
- 在模拟和真实世界任务中显著优于 BC、IBC、Behavior Cloning LSTM 等基线
- ALOHA 系统完全开源（硬件设计 + 软件），被社区广泛采用和扩展

## 与面试50题的关系
- **对应 Q45**: 双臂操作与遥操作——ALOHA 提供了低成本的双臂遥操作硬件方案，ACT 给出了处理组合误差的创新学习算法，是双臂精细操作方向的标杆工作

## 个人思考