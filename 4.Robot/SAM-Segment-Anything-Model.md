---
title: SAM-Segment-Anything-Model
type: paper-note
created: 2026-06-01
tags: [perception, segmentation, foundation-model, robot-vision, paper-note]
---

## 论文信息
- **标题**: Segment Anything
- **作者/机构**: Alexander Kirillov, Eric Mintun, Nikhila Ravi, Hanzi Mao, Chloe Rolland, Laura Gustafson, Tete Xiao, Spencer Whitehead, Alexander C. Berg, Wan-Yen Lo, Piotr Dollár, Ross Girshick (Meta AI Research, FAIR)
- **发表时间**: ICCV 2023 (Oral)
- **arXiv/链接**: https://arxiv.org/abs/2304.02643 | https://github.com/facebookresearch/segment-anything

## 核心问题
传统图像分割模型针对特定任务和固定类别训练，无法泛化到新类别或新场景。SAM 要解决的核心问题：**能否构建一个可提示（promptable）的分割基础模型，通过 zero-shot 泛化处理任意分割任务？**

## 关键方法

1. **可提示分割范式（Promptable Segmentation）**：SAM将分割任务重新定义为"给定提示 → 输出掩码"的通用框架。支持四种提示类型：
   - **点提示**：单个或多点（前景/背景）
   - **框提示**：边界框
   - **掩码提示**：粗糙掩码
   - **文本提示**：（实验中）结合CLIP等做语言引导

2. **三组件架构**：
   - **图像编码器（Image Encoder）**：ViT（MAE预训练），一次前向生成整张图像的特征嵌入。有三种规格：ViT-B（91M）、ViT-L（308M）、ViT-H（636M）。
   - **提示编码器（Prompt Encoder）**：轻量级，将点/框/掩码编码为提示token嵌入。点用位置编码，框用对角点编码，掩码用卷积嵌入后与图像特征相加。
   - **掩码解码器（Mask Decoder）**：轻量级Transformer decoder（两层），用交叉注意力关注图像特征，自注意力处理提示token。每次提示生成3个有效掩码（处理歧义：一个点落在衬衫上，可能指衬衫/人/全身）。

3. **歧义感知输出**：当提示模糊时（如单个点），SAM输出3个分层掩码（whole/part/subpart），每个附有信心分数。如果用多提示消除歧义，网络学会输出一致掩码。

4. **SA-1B数据集与数据引擎（Data Engine）**：最大分割数据集——1100万图像，11亿掩码。通过三阶段数据引擎构建：
   - **阶段1 辅助人工**：标注员点击物体，模型实时辅助
   - **阶段2 半自动**：模型预标注，标注员修正
   - **阶段3 全自动**：网格点提示全图，保留高置信度掩码

5. **"Segment Everything"模式**：在图像上采样规则网格点（32×32），每个点独立提示模型，NMS去重后得到图中所有可能的分割掩码。

## 重要细节

- **推理速度**：图像编码约0.15s（单次），每个提示约50ms，支持浏览器端实时交互
- **Zero-shot 泛化**：在23个不同领域的分割数据集（医学、卫星、显微等）上不微调即达到或超过全监督方法
- **SAM 2（2024年7月）**：扩展到视频分割，用记忆机制跨帧跟踪对象
- **衍生工作**：MobileSAM（移动端蒸馏）、HQ-SAM（高质量边缘）、EfficientSAM（提高效率）、GroundingSAM（结合文本提示）

## 与面试50题的关系
对应 **Q31**：SAM在机器人操作中的应用和局限。应用包括：零样本实例分割定位物体、结合CLIP/GLIP做referring segmentation、为6D位姿估计提供ROI mask。局限：输出2D mask无深度/3D信息、遮挡/透明物体差、原版推理不够实时。

## 个人思考