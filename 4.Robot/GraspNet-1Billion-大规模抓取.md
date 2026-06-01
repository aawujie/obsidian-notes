---
title: GraspNet-1Billion-大规模抓取
type: paper-note
created: 2026-06-01
tags: [perception, robot-vision, grasping, paper-note, dataset]
---

## 论文信息
- **标题**: GraspNet-1Billion: A Large-Scale Benchmark for General Object Grasping
- **作者/机构**: Hao-Shu Fang, Chenxi Wang, Minghao Gou, Cewu Lu (上海交通大学)
- **发表时间**: CVPR 2020
- **arXiv/链接**: https://arxiv.org/abs/1912.13444 | https://graspnet.net/

## 核心问题
之前的抓取数据集要么聚焦单个孤立物体，要么只标注每个场景一个抓取位姿，规模太小（通常仅数百到数千个标注），且多采用基于2D矩形框的表示，限制了抓取位姿空间。GraspNet-1Billion 旨在建立一个大规模、多物体、多抓取的通用抓取基准，解决训练数据不足和缺乏统一评估体系的问题。

## 关键方法

1. **大规模数据集构建**：包含190个杂乱场景、88个日常物体（有高质量3D网格模型），用 Kinect Azure 和 RealSense D435 两种相机采集，共97,280张RGB-D图像。每帧密集标注6-DoF抓取位姿，总计超过**11亿**个抓取位姿，比之前数据集大5个数量级。

2. **两阶段自动标注管线**：结合真实世界图像和仿真力闭合（force closure）分析，通过解析计算自动生成抓取标签，无需人工逐帧标注。同时提供物体6D位姿、矩形抓取框、物体mask和bounding box等丰富标注。

3. **端到端点云抓取预测网络**：以点云为输入，将抓取预测解耦为 **ApproachNet**（预测接近方向和抓取分数）、**OperationNet**（预测操作参数：面内旋转、接近深度、宽度）和 **ToleranceNet**（鲁棒性评分），三个子网络共享特征提取层。

4. **Grasp Affinity Field（抓取亲和场）**：一种新颖的抓取表示，通过学习抓取位姿对抗扰动的鲁棒性，使网络对传感器噪声更鲁棒。预测的抓取分数与真实抓取成功率高度相关（score=1.0 对应96%真实成功率）。

5. **统一评估系统**：在线评估平台可以直接报告抓取是否成功（通过解析力闭合计算），无需穷举标注ground-truth。评估指标包括不同抓取分数阈值下的精度和召回率。

## 重要细节

- **抓取表示**：6-DoF抓取位姿 $[\mathbf{R}, \mathbf{t}, w]$，而非传统2D矩形框，充分覆盖抓取空间
- **网络架构**：基于PointNet++的点云特征提取，共享backbone后接三个轻量MLP头
- **训练数据**：从每个场景的300万-900万个抓取位姿中采样训练
- **Collision处理**：数据集标注时简化了夹爪模型和碰撞检测，将运动规划和机器人特化的碰撞问题留给运行时处理
- **实际验证**：用 Flexiv Rizon 机械臂 + RealSense 435 进行真实抓取实验，验证标注质量与真实世界对齐

## 与面试50题的关系
对应 **Q15**：机器人抓取的主要方法及 GraspNet 类方法核心思路。GraspNet-1Billion 是 GraspNet 系列的基石，后续 AnyGrasp 等方法均基于此数据集训练。

## 个人思考