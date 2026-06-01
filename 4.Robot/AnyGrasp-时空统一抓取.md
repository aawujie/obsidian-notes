---
title: AnyGrasp-时空统一抓取
type: paper-note
created: 2026-06-01
tags: [perception, robot-vision, grasping, paper-note]
---

## 论文信息
- **标题**: AnyGrasp: Robust and Efficient Grasp Perception in Spatial and Temporal Domains
- **作者/机构**: Hao-Shu Fang, Chenxi Wang, Hongjie Fang, Minghao Gou, Jirong Liu, Hengxu Yan, Wenhai Liu, Yichen Xie, Cewu Lu (上海交通大学 / NYU)
- **发表时间**: IEEE Transactions on Robotics (T-RO), 2023 (arXiv:2212.08333)
- **arXiv/链接**: https://arxiv.org/abs/2212.08333 | https://github.com/NYU-robot-learning/anygrasp

## 核心问题
人类的抓取系统具备快速、准确、灵活、时空连续的特性，而现有的机器人抓取方法很少同时覆盖所有这些特性。AnyGrasp 的目标是弥合机器人与人类在抓取感知能力上的差距，实现**空间密集、时间连续**的7-DoF抓取位姿生成。

## 关键方法

1. **两模块统一架构**：
   - **几何处理模块（Geometry Processing Module）**：基于 GSNet，从单帧部分点云中一次性生成密集的7-DoF抓取配置。将抓取参数分解为抓取点、视角、面内旋转、接近深度和宽度，用3D卷积backbone + MLP逐步预测。
   - **时序关联模块（Temporal Association Module）**：识别连续两帧之间大量抓取位姿的对应关系，通过计算抓取位姿特征向量的余弦相似度建立many-to-many关联矩阵，实现抓取跟踪。

2. **Graspable FPS + Graspable PVS**：引入可抓取最远点采样和可抓取概率视角选择机制，从场景中采样最有抓取潜力的种子点（默认1024个），对每个种子点评估最优抓取视角。

3. **质量意识（COG Awareness）**：在网络学习中显式融入物体质心（center of gravity）感知，通过监督信号使网络隐式学习哪些抓取位姿在物理上更稳定，提高抓取稳定性。

4. **障碍感知（Obstacle Awareness）**：模型隐式学习碰撞避免——直接排除没有足够手部放置空间的抓取候选，减少后续操作中显式碰撞检测的负担。

5. **生成-关联（Generation-Association）方法**：利用几何处理模块的空间连续性（相邻点云区域生成相似抓取），结合时序关联模块确保跨时间步的抓取一致性，实现动态抓取跟踪。

## 重要细节

- **真实数据训练**：仅使用144个物体的真实世界数据训练（非纯仿真），展示了极强的数据效率
- **bin-clearing实验**：在超过300个未见物体上达到 **93.3%抓取成功率**，与人类受试者在受控条件下的表现相当
- **抓取效率**：单臂系统报告超过 **900 MPPH**（Mean Picks Per Hour）
- **推理速度**：约100ms生成全场景抓取位姿
- **深度噪声鲁棒性**：对真实传感器的深度噪声（包括RealSense和Kinect）表现出强鲁棒性
- **动态抓取**：能抓取水中游动的机器鱼，展示真正的时间连续性应用
- **与GraspNet-1Billion的关系**：训练数据基于GraspNet-1Billion数据集，但在此基础上加入质心标注和真实感知数据

## 与面试50题的关系
对应 **Q15**：机器人抓取的主要方法——AnyGrasp 被描述为"基于旋转等变特征，泛化能力强"，是实现"抓取任意场景的任意物体"的实用系统。

## 个人思考