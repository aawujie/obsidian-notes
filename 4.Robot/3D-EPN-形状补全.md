---
title: 3D-EPN（形状补全）
type: paper-note
created: 2026-06-01
tags: [embodied-ai, paper-note, 3d-vision, shape-completion]
---

## 论文信息
- **标题**: 3D-EPN: Learning Fully-Complete 3D Shapes from a Single-View Point Cloud
- **作者/机构**: Angela Dai, Charles Ruizhongtai Qi, Matthias Niessner (Stanford University)
- **发表时间**: 2016/2017 (CVPR 2017)
- **arXiv/链接**: https://arxiv.org/abs/1611.08069
- **GitHub**: https://github.com/angeladai/3D-EPN

## 核心问题
深度传感器（如 RGB-D 相机）每次只能捕捉物体的一个视角的部分点云。对于机器人操作任务，需要知道物体的完整 3D 形状以规划抓取和操作策略。3D-EPN 要解决的问题是：**仅给定单视角的部分点云，推断完整的 3D 形状**。

## 关键方法

1. **编码器-预测器架构（Encoder-Predictor Network）**: 网络分为两个核心组件：
   - **编码器（Encoder）**: 将部分输入的 3D 体素网格编码为紧凑的隐式特征向量
   - **预测器（Predictor）**: 从特征向量解码出完整的 3D 体素网格（补全被遮挡部分）

2. **体素化表示**: 将点云转换为固定分辨率的 3D 体素网格（如 32x32x32），每个体素编码该位置是否被物体占据。使用 3D 卷积网络（3D CNN）进行编码和解码。

3. **从部分到完整的端到端学习**: 网络以自监督方式训练——在 ShapeNet 等 CAD 模型数据集上，从完整模型渲染不同视角的部分点云，训练网络从部分观测重建完整形状。

4. **逐体素交叉熵损失**: 对体素网格的每个单元使用二分类交叉熵损失（被占据 vs 未被占据），同时监督可见区域的重建精度和非可见区域的补全质量。

5. **数据增强策略**: 使用不同相机视角、不同遮挡程度的部分输入进行训练，增强泛化能力。

## 重要细节

- 训练数据来自 ShapeNet 数据集，涵盖多种物体类别（椅子、桌子、飞机等）
- 网络使用 3D 卷积层，类似 VoxNet 但具有对称的编码-解码结构
- 输入是部分体素网格（从单个深度视图投影得到），输出是完整体素网格
- 在当时（2016年）是最早将深度学习应用于 3D 形状补全的工作之一
- 后续工作如 PCN（Point Completion Network）直接处理点云而非体素，提升了效率
- 该工作来自 PointNet/PointNet++ 作者组，与 Charles Qi 后续的点云深度学习工作一脉相承

## 与面试50题的关系
- **对应 Q32**: 3D 视觉与点云处理——3D-EPN 是早期深度学习方法进行 3D 形状补全的代表性工作，从部分点云推断完整几何结构，对机器人操作中的物体感知至关重要

## 个人思考