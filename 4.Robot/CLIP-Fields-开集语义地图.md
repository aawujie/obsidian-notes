---
title: CLIP-Fields
type: paper-note
created: 2026-06-01
tags: [embodied-ai, paper-note, semantic-mapping, nerf, vlm]
---

## 论文信息
- **标题**: CLIP-Fields: Weakly Supervised Semantic Fields for Robotic Memory
- **作者/机构**: Nur Muhammad (Mahi) Shafiullah, Chris Paxton, Lerrel Pinto (NYU), Soumith Chintala (Meta), Arthur Szlam (Meta)
- **发表时间**: 2022年10月 (LangRob 2022 Spotlight)
- **arXiv/链接**: https://arxiv.org/abs/2210.05663
- **项目页面**: https://mahis.life/clip-fields/

## 核心问题
机器人需要能理解所处的 3D 环境，包括物体的语义信息（这是什么？）和空间位置（在哪？）。传统语义地图需要大量人工标注，无法扩展到开放词表场景。CLIP-Fields 提出了一种**弱监督**的方法，仅利用互联网规模预训练模型（CLIP、Detic、Sentence-BERT）作为监督信号，构建可以根据自然语言查询的 3D 语义场景表示。

## 关键方法

1. **隐式语义场**: 学习一个从 3D 空间坐标到语义嵌入向量的映射函数（基于神经网络），类似 NeRF 的思想，但输出的是语义向量而非颜色/密度。

2. **弱监督训练**: 训练信号完全来自预训练的 web-scale 模型，**不需要任何直接的人工标注**：
   - **CLIP**: 提供视觉语义嵌入（vision-language alignment）
   - **Detic**: 提供开放词表物体检测
   - **Sentence-BERT**: 提供文本语义嵌入

3. **多视角一致语义融合**: 通过隐式场的可微渲染，将多个视角的语义信息融合到统一的 3D 表示中，实现跨视角的语义一致性。

4. **自然语言查询 3D 场景**: 训练完成后，机器人可以用自然语言对场景进行查询，如"红色的椅子在哪里？"系统通过计算文本嵌入与各位置的语义向量的相似度来定位目标。

5. **机器人语义导航**: 在 Hello Robot Stretch 平台上实现了「Go and look at X」任务，机器人根据自然语言指令在真实环境中导航到指定物体前。

## 重要细节

- 在 HM3D 数据集上测试，在少样本实例识别和语义分割任务上超越 Mask-RCNN 等基线
- 使用对比损失（contrastive loss）训练，鼓励同一空间位置的嵌入向量与对应的 CLIP/Detic 标签嵌入相似
- 支持多种下游任务：语义分割、实例识别、空间语义搜索、视角定位（view localization）
- 实验中验证了在实验室厨房和图书馆两个真实场景中的语义导航效果
- 本质上是一种可查询的空间-语义数据库

## 与面试50题的关系
- **对应 Q16**: 开集语义地图与导航——CLIP-Fields 利用 VLM 构建开放词表的 3D 语义场，为机器人提供自然语言可查询的空间记忆，是弱监督语义建图的代表工作

## 个人思考