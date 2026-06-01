---
title: DenseFusion-6D位姿估计
type: paper-note
created: 2026-06-01
tags: [perception, 6D-pose, pose-estimation, paper-note]
---

## 论文信息
- **标题**: DenseFusion: 6D Object Pose Estimation by Iterative Dense Fusion
- **作者/机构**: Chen Wang, Danfei Xu, Yuke Zhu, Roberto Martín-Martín, Cewu Lu, Li Fei-Fei, Silvio Savarese (Stanford Vision & Learning Lab)
- **发表时间**: CVPR 2019
- **arXiv/链接**: https://arxiv.org/abs/1901.04780

## 核心问题
传统6D位姿估计方法要么只用RGB（对光照和纹理敏感），要么只用深度（对无纹理物体效果好但丢失颜色信息），RGB-D融合方法则多采用全局特征拼接，丢失了每个像素级别的精细对应关系。DenseFusion 的核心问题是：**如何在像素级别密集融合RGB和深度信息**，以处理严重遮挡和传感器噪声下的6D位姿估计？

## 关键方法

1. **密集逐像素融合（Dense Per-Pixel Fusion）**：核心创新——对每个像素，将其RGB特征和对应的点云几何特征进行**逐像素融合**，而非全局池化后拼接。具体做法：用CNN提取RGB特征，用PointNet提取每个3D点的几何特征，然后对每个像素执行 $\text{fusion} = f([\text{color}_i, \text{geometry}_i])$，生成像素级的全局-局部感知特征。

2. **迭代位姿精炼（Iterative Pose Refinement）**：得到初始位姿估计后，进入迭代精炼循环。每一步用当前估计的位姿将3D模型点投影到图像平面，与观测点关联，计算残差位姿 $\Delta \mathbf{R}, \Delta \mathbf{t}$ 更新估计。这类似于图像配准中的LK光流思想，但作用于6-DoF空间。

3. **异构数据处理**：RGB分支用2D CNN（颜色信息在规则网格上有空间连续性），深度分支用PointNet（点云是非结构化的3D数据），两条路径生成的特征在统一维度的嵌入空间中逐像素融合。

4. **对称物体处理**：专门设计了针对对称物体的损失函数，使用最小化点到最近对称点的距离（而非直接的位姿差），避免因物体对称性导致的训练歧义。

5. **端到端训练**：整个 pipeline（RGB编码、深度编码、融合、位姿预测、迭代精炼）可端到端训练，梯度通过迭代精炼循环回传。

## 重要细节

- **评估数据集**：LineMOD（13个物体，重度遮挡）和 YCB-Video（21个物体，92个视频序列）
- **性能**：在LineMOD上达到当时SOTA，尤其在有遮挡场景下显著优于 PoseCNN+ICP 和 PointFusion 等方法
- **输入**：RGB图像 + 对应深度图转成的点云
- **输出**：物体6D位姿 $[\mathbf{R} | \mathbf{t}] \in SE(3)$
- **速度**：端到端推理无需后处理ICP精炼，比ICP-based方法快一个数量级以上
- **遮挡鲁棒性**：逐像素融合意味着即使只有少量像素可见，也能用这些像素的特征投票

## 与面试50题的关系
对应 **Q28**：6D物体位姿估计的主流方法——DenseFusion 是"基于模板匹配/learning方法"的代表，面试中常问其如何融合RGB和深度信息。

## 个人思考