---
title: FoundPose-零样本位姿估计
type: paper-note
created: 2026-06-01
tags: [perception, 6D-pose, zero-shot, foundation-model, paper-note]
---

## 论文信息
- **标题**: FoundPose: Unseen Object Pose Estimation with Foundation Features
- **作者/机构**: Evgenii Averianov 等 (ETH Zurich / Meta AI)
- **发表时间**: 2023年11月 (arXiv:2311.18809), ECCV 2024
- **arXiv/链接**: https://arxiv.org/abs/2311.18809

## 核心问题
传统的6D位姿估计方法通常需要针对每个物体训练专用模型（instance-specific），对未见过的物体需要重新采集数据并训练，无法泛化。FoundPose 要解决的核心问题：**如何在仅给定3D CAD模型、无需任何针对该物体的训练数据的情况下，估计新物体的6D位姿？**

## 关键方法

1. **DINOv2 基础特征提取**：核心洞察——使用 DINOv2（Vision Transformer 自监督预训练基础模型）作为通用视觉特征提取器。DINOv2 的特征具有极强的一般性和空间对应性，无需在特定物体类别上微调即可在未见物体上建立可靠的视觉对应关系。分别对输入RGB图像和物体CAD模型的渲染模板提取 DINOv2 特征。

2. **由粗到精的对应匹配（Coarse-to-Fine Matching）**：先在粗尺度上用 DINOv2 全局特征找到最相似的渲染模板（缩小搜索空间），然后在细尺度上建立密集的2D-3D对应关系——图像特征点 ↔ 模板特征点（已知3D坐标）。

3. **RANSAC + PnP 位姿求解**：从2D-3D对应关系中，用 RANSAC 剔除错误匹配（outlier），再用 Perspective-n-Point（PnP）算法求解6D位姿。这是从"特征匹配"到"几何求解"的经典pipeline。

4. **可选的精炼阶段**：在初始位姿估计后，可以进一步用基于特征的优化（feature-based refinement）来提升位姿精度，将渲染图像的特征与观测图像的特征对齐。

5. **模型无关性**：方法的关键是——所有组件（DINOv2、RANSAC、PnP）都不需要针对特体物体训练。输入只有 (a) 待测物体的CAD模型 (b) 一张RGB图像。

## 重要细节

- **BOP Challenge 2023**：在模型无关（model-based, unseen objects）赛道中获**第一名**，在多个BOP核心数据集（LM-O, T-LESS, YCB-V, ITODD, HB, IC-BIN等）上超越或接近instance-specific方法
- **数据**：使用 BOP 数据集中的 CAD 模型渲染模板，DINOv2 使用公开的 ViT-B/14 预训练权重
- **与MegaPose的区别**：MegaPose 也做零样本位姿估计，但依赖合成数据训练的专用网络；FoundPose 直接使用现成的基础模型，泛化性更纯粹
- **局限性**：对严重自遮挡或对称性强的物体仍有挑战；依赖CAD模型的质量

## 与面试50题的关系
对应 **Q28**：6D物体位姿估计主流方法——FoundPose 是"Foundation Model 方法，零样本估计"的代表。面试重点：如何使用foundation model实现对新物体的位姿估计，以及与传统方法的对比。

## 个人思考