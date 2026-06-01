---
title: ALOHA-低成本双臂遥操作
type: paper-note
created: 2026-06-01
tags: [embodied-ai, paper-note, teleoperation, imitation-learning, hardware]
---

## 论文信息
- **标题**: ALOHA: A Low-cost Open-source Hardware System for Bimanual Teleoperation
- **作者/机构**: Tony Z. Zhao, Vikash Kumar, Sergey Levine, Chelsea Finn — Stanford University / UC Berkeley
- **发表时间**: 2023 (arXiv:2305.10868)
- **arXiv/链接**: https://arxiv.org/abs/2305.10868
- **后续工作**: Mobile ALOHA (2024, arXiv:2401.xxxxx)

## 核心问题
精细的双臂操作（如系鞋带、挂衣服、装电池）是机器人领域的长期挑战。现有的高端双臂操作平台成本极其昂贵（数十万美元），限制了研究的普及。**ALOHA 要解决的核心问题是：如何以极低成本（约 2 万美元）构建一个开源的双臂遥操作系统，同时保持足够高的精度来做精细操作，并通过模仿学习实现自主执行？**

## 关键方法

1. **低成本硬件架构**
   - 使用现成的 ViperX 300 6-DOF 机械臂（hobby 级伺服电机）
   - 两个 leader 臂（人类操作者使用）和两个 follower 臂（执行任务）
   - 总成本约 2 万美元，远低于传统双臂平台（通常 >20 万美元）
   - 完全开源：提供详细的组装指南、零件清单和代码

2. **主从遥操作 (Leader-Follower Teleoperation)**
   - 人类操作者直接操控 leader 臂
   - follower 臂实时复制 leader 臂的动作
   - 关节角度直接映射，延迟极低
   - 操作者可以直观地进行精细操作，无需特殊培训

3. **模仿学习 (Imitation Learning)**
   - 遥操作采集高质量演示数据（状态-动作对）
   - 使用行为克隆 (Behavioral Cloning, BC) 训练策略
   - 训练后的策略可以直接在 follower 臂上自主执行
   - 策略输入：视觉观测（摄像头图像）→ 输出：关节动作

4. **Mobile ALOHA (后续工作)**
   - 将 ALOHA 系统安装到轮式移动底座上
   - 实现了全身双臂移动操作
   - 仅需约 50 次人类演示即可学习复杂任务（如烹饪、清洁、按电梯）
   - 使用协同训练 (co-training) 与静态 ALOHA 数据集提升少样本性能

5. **开源生态**
   - 硬件设计、组装指南、软件全部开源
   - 催生了大量社区衍生项目和复现
   - 大大降低了机器人学习研究的门槛

## 重要细节

- **精细操作能力**: 可以完成系鞋带、挂T恤、装电池、叠毛巾等精细任务
- **Mobile ALOHA 任务**: 烹饪三道菜、清洁桌面、操作电梯、洗锅等全身移动操作
- **数据效率**: Mobile ALOHA 仅需 ~50 个演示即可学会复杂任务，得益于与其他 ALOHA 数据的协同训练
- **成本优势**: ALOHA ~$20K vs 传统双臂平台 ~$200K+，且精度接近
- **ACT (Action Chunking Transformer)**: ALOHA 的默认策略架构，使用 Transformer 预测动作序列块，有效处理时序依赖
- **局限性与改进**:
  - 初始版本使用行为克隆，对分布外状态敏感
  - 后续工作引入扩散策略 (Diffusion Policy) 和 ACT 来提升鲁棒性
  - 硬件精度受限于 hobby 级伺服电机
  - Mobile ALOHA 的移动底座需要人类操作者物理推动

## 与面试50题的关系
- **Q14**: 模仿学习与遥操作 — ALOHA 是低成本遥操作 + 模仿学习的标杆工作，定义了"低门槛高质量数据采集"的范式
- **Q45**: 具身智能硬件平台 — ALOHA 是目前最流行的开源双臂操作硬件平台

## 个人思考