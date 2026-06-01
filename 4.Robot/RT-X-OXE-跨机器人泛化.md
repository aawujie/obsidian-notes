---
title: RT-X / Open X-Embodiment
type: paper-note
created: 2026-06-01
tags: [embodied-ai, paper-note, cross-embodiment, foundation-model]
---

## 论文信息
- **标题**: Open X-Embodiment: Robotic Learning Datasets and RT-X Models
- **作者/机构**: Google DeepMind + 34 个研究实验室联合
- **发表时间**: 2023年10月
- **arXiv/链接**: https://arxiv.org/abs/2310.08864
- **项目页面**: https://robotics-transformer-x.github.io/
- **GitHub**: https://github.com/google-deepmind/open_x_embodiment

## 核心问题
机器人学习长期受困于**数据孤岛**问题：每个实验室用自己的机器人、自己的数据格式训练专用模型，无法泛化到不同机器人形态。这篇工作试图通过构建一个跨机器人、跨任务的统一大规模数据集（Open X-Embodiment Dataset），并训练出能够跨多种机器人形态泛化的基础模型（RT-X），推动机器人领域的「ImageNet 时刻」。

## 关键方法

1. **Open X-Embodiment 数据集**: 整合了来自34个研究机构、22种不同机器人形态、60+个数据集的超过100万条真实机器人轨迹，覆盖527种技能。统一了数据格式和处理管线，是目前最大的开源机器人操作数据集。

2. **RT-1-X 模型**: 在 RT-1（Transformer-based Robotics Transformer）架构基础上，使用 Open X-Embodiment 数据集进行跨形态训练。输入为图像序列+文本指令，输出为离散化的末端执行器动作。

3. **RT-2-X 模型**: 基于 RT-2（Vision-Language-Action, VLA）的扩展版本。RT-2 将视觉语言模型（如 PaLI-X 或 PaLM-E）微调为输出机器人动作 token 的模型。RT-2-X 在 Open X-Embodiment 数据集上进行跨形态训练，展现了更强的语言理解能力和泛化能力。

4. **跨形态泛化的关键发现**: 在多样化的跨形态数据上训练不仅能学到多机器人技能，还能**提升单一形态上的表现**（正迁移）。模型展现出**涌现技能**——能够执行从未在训练集中出现的任务组合。

5. **零样本迁移**: RT-2-X 能够在完全未见过的机器人形态上执行语言指令驱动的操作任务，展现了强大的泛化能力。

## 重要细节

- 数据集包含从单臂到双臂、从桌面操作到移动操作的各种场景
- RT-1-X 的动作空间为 7-DoF 离散化末端执行器控制（x, y, z, roll, pitch, yaw, gripper）
- RT-2-X 使用与 ViT 相同的 tokenization 策略，将连续动作值离散化为 token
- 实验验证了一个反直觉的结论：即使训练数据中目标机器人形态的占比很小，跨形态训练仍然有助于提升该形态的表现
- 数据集和模型均开源，推动了整个领域的标准化进程

## 与面试50题的关系
- **对应 Q41**: VLA（Vision-Language-Action）模型的核心范式——RT-2 系列是 VLA 的标杆工作
- **对应 Q43**: 跨机器人泛化——RT-X 是跨形态泛化（cross-embodiment generalization）方向的开创性工作，探讨了不同机器人形态间知识的正迁移

## 个人思考