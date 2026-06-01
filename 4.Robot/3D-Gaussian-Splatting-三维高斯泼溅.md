---
title: 3D-Gaussian-Splatting-三维高斯泼溅
type: paper-note
created: 2026-06-01
tags: [perception, 3D-reconstruction, 3DGS, neural-rendering, real-time, paper-note]
---

## 论文信息
- **标题**: 3D Gaussian Splatting for Real-Time Radiance Field Rendering
- **作者/机构**: Bernhard Kerbl, Georgios Kopanas, Thomas Leimkühler, George Drettakis (Inria, Université Côte d'Azur)
- **发表时间**: SIGGRAPH 2023 (ACM Transactions on Graphics)
- **arXiv/链接**: https://arxiv.org/abs/2308.04079 | https://github.com/graphdeco-inria/gaussian-splatting

## 核心问题
NeRF 开创了用神经辐射场进行高质量视图合成的方法，但其隐式 MLP 表示导致训练和渲染都极其缓慢（训练以小时/天计，渲染以秒/帧计），无法满足实时应用（如VR、机器人交互）的需求。3D Gaussian Splatting 的核心问题：**如何实现与NeRF相当甚至更好的渲染质量，同时达到实时渲染速度（30+ FPS）？**

## 关键方法

1. **显式3D高斯原语表示**：用数百万个各向异性3D高斯（anisotropic 3D Gaussians）显式表示场景，每个高斯原语包含：
   - 均值 $\mu$（3D位置）
   - 协方差矩阵 $\Sigma = RSS^TR^T$（$R$ 旋转四元数 $\to$ 旋转矩阵，$S$ 对角缩放矩阵）
   - 不透明度 $\alpha \in [0,1]$
   - 视角依赖颜色（球谐函数 Spherical Harmonics 系数，degree 3，共16个3维系数 = 48个参数）
   - 共约 59 个可优化参数/原语

2. **基于瓦片的可微光栅化器（Tile-based Differentiable Rasterizer）**：
   - 将图像划分为 16x16 像素的瓦片
   - 每个瓦片根据高斯2D投影的包围盒筛选相关高斯
   - 瓦片内按深度排序高斯（用 radix sort）
   - 逐像素从前往后进行 alpha 混合：$C = \sum_i c_i \cdot \alpha_i \cdot \prod_{j=1}^{i-1}(1-\alpha_j)$
   - **梯度通过 alpha 混合回传**，可同时更新所有高斯参数
   - 用 CUDA 实现，极致高效

3. **3D→2D投影**：用 EWA Splatting（Zwicker et al.）将3D高斯投影到2D屏幕空间。投影的2D协方差为 $\Sigma' = J W \Sigma W^T J^T$，其中 $W$ 是世界到相机的变换，$J$ 是投影变换的雅可比矩阵的仿射近似。

4. **自适应密度控制（Adaptive Density Control）**：
   - 每约3000次迭代检查：小梯度区域 → 克隆高斯（填补空洞），大梯度区域 → 分裂大高斯（增加细节）
   - 移除不透明度太低（$\alpha < \epsilon$）或世界空间尺寸过大的高斯
   - 定期重置不透明度避免陷入局部最小值

5. **从SfM点云初始化**：用 COLMAP 的稀疏SfM点云（约5000点）作为初始高斯中心，避免随机初始化。训练中密度控制会逐步增加到数百万个高斯。

## 重要细节

- **训练速度**：典型场景 20-30分钟（单张GPU），vs NeRF的数小时/天
- **渲染速度**：1080p 下 30+ FPS 实时渲染，vs NeRF的秒/帧
- **质量**：PSNR/SSIM/LPIPS 指标上匹配或超越 Mip-NeRF360
- **损失函数**：$\mathcal{L} = (1-\lambda)\mathcal{L}_1 + \lambda\mathcal{L}_{\text{SSIM}}$，$\lambda=0.2$
- **显式 vs 隐式**：显式表示的优点是可直接操作和编辑场景，缺点是存储量大（数百MB/场景）
- **3DGS的后续工作**：Dynamic 3DGS（4D场景）、Gaussian SLAM（SplaTAM/MonoGS）、压缩3DGS、抗锯齿Mip-Splatting

## 与面试50题的关系
对应 **Q29**：NeRF和3D Gaussian Splatting在具身智能中的应用。3DGS的优势在于实时渲染（100+ FPS）、可编辑场景、适合在线策略训练。GaussianGrasping等方法直接从3DGS表示中提取几何信息用于抓取规划。

## 个人思考