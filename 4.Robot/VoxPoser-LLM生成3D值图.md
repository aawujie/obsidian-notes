---
title: VoxPoser
type: paper-note
created: 2026-06-01
tags: [embodied-ai, paper-note, llm, manipulation, zero-shot]
---

## 论文信息
- **标题**: VoxPoser: Composable 3D Value Maps for Robotic Manipulation with Language Models
- **作者/机构**: Wenlong Huang, Chen Wang, Ruohan Zhang, Yunzhu Li, Jiajun Wu, Li Fei-Fei (Stanford University)
- **发表时间**: 2023年7月 (CoRL 2023 Oral)
- **arXiv/链接**: https://arxiv.org/abs/2307.05973
- **项目页面**: https://voxposer.github.io/

## 核心问题
LLM（大语言模型）展现出丰富的关于物理世界的 actionable knowledge（可行动知识），但现有方法大多依赖**预定义的运动基元**（motion primitives）来执行物理交互，这成为关键瓶颈。VoxPoser 的目标是：给定自由形式的语言指令和开放集的物体，直接在**连续动作空间**中合成机器人的 6-DoF 末端执行器轨迹，而不需要额外的训练数据或预定义基元。

## 关键方法

1. **LLM 推理 Affordance 和约束**: 给定语言指令，LLM 被提示（prompt）去推断任务的 affordance（哪里吸引末端执行器）和 constraint（哪里排斥末端执行器），并**生成 Python 代码**来实现这些推断。

2. **LLM + VLM 协同构建 3D 值图（Voxel Value Map）**: LLM 生成的代码调用 VLM（如开放词表检测器 OWL-ViT）的感知 API，获取场景中物体的空间几何信息，然后通过 NumPy 操作在观测空间的 3D 体素网格中分配值。高值区域表示吸引力（目标位置），低值区域表示排斥力（障碍物/约束区）。

3. **无需训练，零样本合成轨迹**: 生成的 3D 值图作为运动规划器（motion planner）的代价函数，通过优化直接合成从当前状态到目标状态的连续 6-DoF 轨迹。整个过程**不涉及任何模型训练**，完全零样本。

4. **闭环重规划和动态鲁棒性**: 由于值图构建和轨迹合成速度很快，系统可以实时重规划，对动态扰动（如移动障碍物、目标位置变化）具有鲁棒性。

5. **在线经验学习**: 对于接触密集的任务，VoxPoser 还可以利用有限的在线交互数据，高效学习场景特定的动力学模型（dynamics model），进一步提升性能。

## 重要细节

- 输入为 RGB-D 观测，输出为密集的 6-DoF 末端执行器路径点序列
- 值图是 3D 体素网格 $V \in \mathbb{R}^{w \times h \times d}$，用平滑操作（smoothing）稠密化，鼓励更平滑的轨迹
- LLM 的角色不是直接输出动作，而是**编排代码**来处理感知和空间推理
- 对比 Baseline「Code as Policies」（通过 LLM 参数化预定义基元），VoxPoser 的联合空间优化范式更灵活、鲁棒
- 在 13 个真实世界日常操作任务上进行了定量评估（包括打开抽屉、扫地、摆桌子等），平均成功率较高

## 与面试50题的关系
- **对应 Q46**: 操作 affordance 与交互预测——VoxPoser 使用 LLM 推断 affordance 和约束，构建 3D 值图来指导连续动作空间的轨迹合成，是一种独特的零样本机器人操作范式

## 个人思考