---
title: NeRF-神经辐射场
type: paper-note
created: 2026-06-01
tags: [perception, 3D-reconstruction, NeRF, neural-rendering, paper-note]
---

## 论文信息
- **标题**: NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis
- **作者/机构**: Ben Mildenhall, Pratul P. Srinivasan, Matthew Tancik, Jonathan T. Barron, Ravi Ramamoorthi, Ren Ng (UC Berkeley / Google Research / UCSD)
- **发表时间**: ECCV 2020 (Best Paper Honorable Mention)
- **arXiv/链接**: https://arxiv.org/abs/2003.08934 | https://www.matthewtancik.com/nerf

## 核心问题
给定一组稀疏的2D图像（已知相机位姿），如何合成任意新视角下的逼真渲染图像？传统方法（光场插值、多视图几何、基于mesh的重建）在复杂几何结构和视角依赖效果（如镜面反射、半透明）上表现不佳。NeRF 的核心思路：用神经网络隐式表示场景的连续辐射场。

## 关键方法

1. **神经辐射场表示**：将场景表示为连续5D函数 $F_\Theta: (\mathbf{x}, \mathbf{d}) \to (\mathbf{c}, \sigma)$，其中：
   - $\mathbf{x} = (x, y, z)$：3D空间坐标
   - $\mathbf{d} = (\theta, \phi)$：2D视角方向
   - $\mathbf{c} = (r, g, b)$：该点的发射颜色（view-dependent）
   - $\sigma$：该点的体积密度（view-independent，只依赖位置）
   - 用 MLP 参数化此函数

2. **体渲染（Volume Rendering）**：沿每条相机射线采样点，按经典体渲染方程积分颜色：
   $$C(\mathbf{r}) = \sum_{i=1}^{N} T_i (1 - \exp(-\sigma_i \delta_i)) \mathbf{c}_i$$
   其中 $T_i = \exp(-\sum_{j=1}^{i-1} \sigma_j \delta_j)$ 是累积透射率，$\delta_i$ 是采样间距。

3. **位置编码（Positional Encoding）**：高频映射 $\gamma(p) = (\sin(2^0\pi p), \cos(2^0\pi p), ..., \sin(2^{L-1}\pi p), \cos(2^{L-1}\pi p))$ 将输入坐标映射到高频空间。这是关键技巧——MLP更擅长拟合低频函数，位置编码将低频坐标提升到高频，使网络能表达细腻的几何和纹理细节。

4. **层次化采样（Hierarchical Sampling）**：用两个网络（粗网络 + 细网络）协同工作。粗网络在射线上均匀采样，输出密度分布；细网络根据粗网络的密度分布在重要区域（物体表面附近）进行重点采样。这避免了在空白区域浪费采样预算。

5. **视角依赖效果**：将视角方向 $\mathbf{d}$ 作为网络输入，使模型能学习镜面反射、光泽等视角依赖的视觉效果，同时用体密度 $\sigma$ 编码几何（与视角无关），实现几何和外观的解耦。

## 重要细节

- **训练**：每张训练图像采样一批射线，用 L2 渲染损失（渲染颜色 vs 真实颜色）优化 MLP 参数
- **网络结构**：8层256维 MLP（坐标输入），跳跃连接到第4层，最后输出 $\sigma$ 和 256维特征向量，再与视角方向拼接，经128维 MLP 输出颜色
- **位置编码维度**：$\mathbf{x}$ 用 $L=10$（60维），$\mathbf{d}$ 用 $L=4$（24维）
- **训练时间**：原版NeRF在单张V100上需要1-2天训练一个场景
- **基础要求**：需要COLMAP等SfM工具预先估计相机位姿

## 与面试50题的关系
对应 **Q29**：NeRF 和 3D Gaussian Splatting 在具身智能中的应用。NeRF 的贡献是开创性思路（隐式神经场 + 体渲染），但限制是训练慢、渲染慢。在具身智能中用于场景重建、数据增强、NeRF-based RL等。

## 个人思考