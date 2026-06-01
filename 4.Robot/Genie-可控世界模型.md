---
title: Genie-可控世界模型
type: paper-note
created: 2026-06-01
tags: [embodied-ai, paper-note, world-model, video-generation, foundation-model]
---

## 论文信息
- **标题**: Genie: Generative Interactive Environments
- **作者/机构**: Jake Bruce, Michael D. Dennis, Ashley Edwards, Jack Parker-Holder, Yuge Shi, Edward Hughes, Matthew Lai, Aditi Mavalankar, Richie Steigerwald, Chris Apps, Yusuf Aytar, Sarah Bechtle, Feryal Behbahani, Stephanie Chan, Nicolas Heess, Lucy Gonzalez, Simon Osindero, Sherjil Ozair, Scott Reed, Jingwei Zhang, Konrad Zolna, Jeff Clune, Nando de Freitas, Satinder Singh, Tim Rocktaschel — Google DeepMind / University of British Columbia
- **发表时间**: 2024 (arXiv:2402.15391)
- **arXiv/链接**: https://arxiv.org/abs/2402.15391

## 核心问题
训练交互式世界模型通常需要大量标注了动作标签的视频数据，而动作标签的获取成本极高。**Genie 要解决的核心问题是：能否仅从无标注的互联网视频中学习一个可交互的世界模型，让模型自行发现"动作"的概念，从而实现对任意输入图像的可控交互？**

## 关键方法

1. **无监督潜在动作学习 (Latent Action Learning)**
   Genie 最核心的创新：完全不需要动作标签，从视频帧之间的变化中自动学习一个离散的潜在动作空间：
   - 视频 tokenizer 将连续帧编码为离散 token
   - 潜在动作模型 (Latent Action Model) 学习哪些 token 变化对应"可控"的动作
   - 动作空间是模型自己发现的（如"向左移动"、"跳跃"等），不需要人类标注

2. **三阶段架构**
   - **Spatiotemporal Video Tokenizer**: 将视频压缩为离散 token 序列，大幅降低维度
   - **Latent Action Model (LAM)**: 编码相邻帧之间的变化，推断出潜在动作，输出离散动作编码
   - **Dynamics Model**: 以当前帧 token 和潜在动作为条件，自回归预测下一帧 token，然后解码为视频帧

3. **11B 参数规模**
   模型总参数量约 110 亿，展示了规模化训练在无监督世界模型学习中的重要性。

4. **零样本可控生成**
   给定任意从未见过的图像（照片、手绘草图、AI 生成图），Genie 都能生成可交互的环境：
   - 输入一张图片 → 用户可以按"动作键"控制环境中的角色
   - 支持从 2D 平台游戏视频中学习，泛化到各种视觉风格

5. **训练数据**
   仅使用互联网上的 2D 平台游戏视频（数十万小时），没有任何动作标签，也没有模拟器访问。

## 重要细节

- **训练数据**: 数十万小时的 2D 平台游戏视频（无标签）
- **模型规模**: ~11B 参数
- **关键突破**: 在没有任何动作标签的情况下学会了可交互的世界模型
- **潜在动作空间**: 模型自动发现的 8-16 个离散动作，与人类直觉的游戏动作（左、右、跳、攻击等）高度对应
- **应用前景**:
  - 游戏生成：从一张草图生成可玩的关卡
  - 机器人仿真：训练机器人在学习的世界中交互
  - AI 训练环境：为 AI agent 提供无限多样的训练环境
- **Genie 2**: 后续工作将方法扩展到 3D 交互式环境
- **局限性**: 目前限于 2D 环境；潜在动作的语义不可控（模型发现的"动作"可能与人类期望不同）；生成质量有限

## 与面试50题的关系
- **Q17**: 世界模型 (World Model) 在具身智能中的作用 — Genie 代表了"无监督动作发现 + 世界模型"的新范式，展示了从纯观察数据中学习交互能力的可能性

## 个人思考