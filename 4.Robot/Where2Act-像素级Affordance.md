---
title: Where2Act
type: paper-note
created: 2026-06-01
tags: [embodied-ai, paper-note, affordance, manipulation]
---

## 论文信息
- **标题**: Where2Act: From Pixels to Actions for Articulated 3D Objects
- **作者/机构**: Kaichun Mo, Leonidas J. Guibas (Stanford), Mustafa Mukadam, Abhinav Gupta (FAIR), Shubham Tulsiani (CMU)
- **发表时间**: 2021年 (ICCV 2021)
- **arXiv/链接**: https://arxiv.org/abs/2101.02892
- **代码/数据**: https://github.com/daerduoCarey/where2act

## 核心问题
机器人如何仅通过视觉观察（RGB-D 图像），学会对未见过的铰接物体（抽屉、门、开关等）预测应该在哪里操作以及如何操作？传统方法需要为每种物体手工标注可操作点，无法泛化。Where2Act 提出了一种通过**自监督交互学习**从像素直接预测 affordance 的方法。

## 关键方法

1. **像素级 Affordance 预测**: 对于输入的部分点云，网络为每个像素/点预测三个量：
   - **actionability score**: 该点是否适合进行操作（如推/拉）
   - **action proposal**: 具体的动作参数（平移方向+旋转轴/角度）
   - **success probability**: 执行该动作后成功的概率

2. **自监督数据收集**: 在 SAPIEN 物理仿真环境中，智能体随机采样候选动作并实际执行，通过物理仿真结果自动标注成功/失败。无需人工标注，可大规模扩展。

3. **闭环交互与适应**: 网络可以处理动态场景——执行一次动作后，物体状态改变，网络基于新观察重新预测下一步最优操作位置和动作。

4. **类别内泛化**: 训练在几个物体实例上，但在同类别新的、未见过的物体实例上进行测试，展现出强大的泛化能力。

5. **多步任务分解**: 对于复杂任务（如「打开安全箱」需要先推开关再掀盖），智能体能够自主分解为多个子步骤并顺序执行。

## 重要细节

- 使用 PartNet-Mobility 数据集（基于 ShapeNet），涵盖抽屉、门、冰箱、窗户等多种铰接类别
- 网络架构基于 PointNet++ 编码点云特征，输出三个分支（actionability、action proposal、success）
- 训练时采用行为克隆（imitation learning）和监督学习的混合策略
- 物理仿真考虑了碰撞、摩擦力等真实物理约束
- 动作空间包含推（push）和拉（pull）两种基本交互，通过 6D 位姿参数化

## 与面试50题的关系
- **对应 Q46**: 操作 affordance 与交互预测——Where2Act 是像素级 affordance 从视觉输入直接预测操作点和动作参数的代表性工作

## 个人思考