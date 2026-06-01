---
title: RT-2-Robotic-Transformer-2
type: paper-note
created: 2026-06-01
tags: [vla, embodied-ai, paper-note, google-deepmind]
---

## 论文信息
- **标题**: RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control
- **作者/机构**: Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, Quan Vuong, Vincent Vanhoucke, Huong Tran, Radu Soricut, 等 (Google DeepMind)
- **发表时间**: 2023年7月 (CoRL 2023, PMLR 229:2165-2183)
- **arXiv**: https://arxiv.org/abs/2307.15818
- **项目主页**: https://robotics-transformer2.github.io
- **引用**: Zitkovich et al., "RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control", CoRL 2023

## 核心问题
如何将互联网规模训练的视觉-语言模型(VLM)直接融入端到端机器人控制，使机器人策略不仅能映射观测到动作，还能受益于大规模网络预训练中蕴含的语义知识和推理能力？

以前的方法要么需要为机器人设计全新的架构，要么只是把VLM作为高级规划器。RT-2的核心问题是：**能不能让VLM直接输出低层机器人动作**，从而把网络知识直接"转移"到物理操控中？

## 关键方法
1. **动作Token化 (Action Tokenization)**：将机器人动作(7DoF移动机械臂的末端执行器位移、旋转、夹爪开合等)离散化为文本token，与自然语言token放入同一词汇表，形成"多模态句子"。这是VLA(Vision-Language-Action)模型的核心创新。
2. **Co-fine-tuning**：在机器人轨迹数据和互联网VQA(视觉问答)数据上联合微调预训练VLM，不做任何架构修改，不增加新参数。
3. **两个Backbone实例化**：RT-2-PaLI-X(基于5B/55B PaLI-X)和RT-2-PaLM-E(基于12B PaLM-E)，证明了方法的通用性。
4. **Chain-of-Thought推理**：将推理步骤作为文本token插入到动作生成之前(如"pick up the rock as an improvised hammer")，实现多阶段语义推理。
5. **使用RT-1协议的数据集**：约13万条真实机器人演示数据，来自之前的RT-1工作。

## 重要细节
- **动作表示**：7个自由度(6DoF末端执行器位姿 + 1维夹爪开合)，每维离散化为256个bin
- **推理流程**：输入RGB图像 + 自然语言指令 → VLM backbone → 输出动作token序列 → 解析为机器人控制命令
- **实验规模**：约6000次真实世界评估试验
- **涌现能力**：显著提升对未见物体的泛化、能解释训练数据中未出现的指令(如"放到数字3上"、"拿起最小的物体")、能做基本推理(如"给疲倦的人适合的饮料")
- **与RT-1对比**：RT-1是纯机器人数据训练的Transformer(不涉及互联网数据)，RT-2的核心改进就是引入互联网知识
- **局限性**：推理速度受大模型影响，不适用于需要毫秒级响应的场景

## 与面试50题的关系
- **Q1 (VLA核心概念)**：RT-2首次提出VLA(Vision-Language-Action)模型的定义和范式，是VLA领域的开创性工作，必须掌握
- **Q2 (RT-2与RT-1对比)**：面试直接会问RT-2相比RT-1的核心改进——答案就是"将互联网知识融入机器人控制"，具体通过动作token化+co-fine-tuning实现

## 个人思考