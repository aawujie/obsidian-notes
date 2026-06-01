---
title: 具身智能&VLA学习清单
type: roadmap
created: 2026-06-01
updated: 2026-06-01
sources: ["[[具身智能&VLA面试50题：一份够用的技术 cheat sheet]]"]
tags: [embodied-ai, vla, learning-roadmap, robotics]
---

## 使用说明

基于 [[具身智能&VLA面试50题：一份够用的技术 cheat sheet]] 逆向整理。每题标注了难度（🔵基础 🟡进阶 🔴深入），对应面试预期深度。

状态标记：
- ✅ 知识库已有 → 可直接复习
- ⚠️ 部分覆盖 → 需补充特定方向
- ❌ 缺口 → 需要新建笔记

---

## 模块一：VLA 模型 (Q1-Q10)

### 前置知识

| 知识点 | 状态 | 已有资源/说明 |
|--------|------|--------------|
| Transformer 架构 | ✅ | [[Transformer架构从零理解]]、[[Transformer 注意力机制详解]] |
| Vision-Language Model (VLM) 基础 | ⚠️ | 3.Agent 有 LLM 知识但缺少 VLM 专项（CLIP、LLaVA、Flamingo） |
| 自回归生成 vs 扩散生成 | ❌ | 需新建：扩散模型原理、Flow Matching 原理 |
| 模仿学习 (Behavior Cloning) | ⚠️ | 4.Robot/DRL 有 RL 基础但缺少 BC 专项 |
| 分布偏移 (Distribution Shift) | ❌ | 需在 BC 或具身学习笔记中覆盖 |

### 核心论文/工作

| 工作 | 对应题目 | 状态 | 说明 |
|------|---------|------|------|
| **RT-2** (Google DeepMind) | Q1, Q2 | ❌ | 动作 token 化、VLM→VLA、联合训练 |
| **OpenVLA** | Q4 | ❌ | 开源 7B VLA、LLaVA 框架、LoRA 微调 |
| **π0** (Physical Intelligence) | Q3, Q4 | ❌ | Flow Matching 动作头、混合架构 |
| **ACT** (Action Chunked Transformers) | Q5 | ❌ | Action Chunking、Temporal Ensemble |
| **Diffusion Policy** | Q3 | ❌ | 扩散建模动作分布、多模态动作 |
| **RoboFlamingo** | Q9 | ❌ | OpenFlamingo + 策略头 |
| **RoboAgent** | Q9 | ❌ | 语义数据增强、多任务泛化 |

### 关键概念

| 概念 | 状态 | 对应题目 |
|------|------|---------|
| Action Tokenization (离散化/连续) | ❌ | Q2 |
| Flow Matching | ❌ | Q3 |
| Action Chunking + Temporal Ensemble | ❌ | Q5 |
| LIBERO / SimplerEnv / OXE benchmark | ❌ | Q6 |
| Long-horizon 分层规划 (SayCan, Inner Monologue, Code as Policies) | ❌ | Q10 |
| Causal Masking 在 VLA 中的应用 | ⚠️ | Q8 (Transformer 部分已有) |

---

## 模块二：具身智能基础 (Q11-Q18)

### 前置知识

| 知识点 | 状态 | 已有资源/说明 |
|--------|------|--------------|
| 具身智能定义与范式 | ⚠️ | 4.Robot/index.md 有概述但不够系统 |
| 机器人运动学/动力学基础 | ⚠️ | [[URDF文件生成完整指南]]、[[人形机器人全身控制-核心知识点]] |
| 经典规划方法 (TAMP) | ❌ | 需新建 |
| 模仿学习 (IL) | ⚠️ | 4.Robot/DRL 缺少 IL 专项（BC, DAgger, GAIL, IRL） |

### 需要新建的笔记

| 主题 | 对应题目 | 优先级 |
|------|---------|--------|
| **Sim-to-Real Transfer 完整方法论** | Q13 | 🔴 高 |
| - Domain Randomization / Domain Adaptation / 数字孪生 | | |
| **Teleoperation 数据采集体系** | Q14 | 🔴 高 |
| - ALOHA、VR 遥操作、数据质量控制 | | |
| **机器人抓取 (Grasping) 方法综述** | Q15 | 🟡 中 |
| - GraspNet-1Billion, Contact-GraspNet, AnyGrasp | | |
| **Open-Vocabulary 机器人操作** | Q16 | 🟡 中 |
| - CLIP-Fields, OWL-ViT, referring expression | | |
| **World Model 在具身智能中的应用** | Q17 | 🔴 高 |
| - Dreamer 系列, UniSim, Genie | | |
| **Foundation Model 在具身智能中的分层应用** | Q18 | 🔴 高 |
| - 感知层/规划层/策略层/奖励层/数据层 | | |
| **TAMP 与端到端学习** | Q12 | 🟡 中 |

---

## 模块三：强化学习 & 控制 (Q19-Q26)

### 已有基础

| 知识点 | 状态 | 已有资源 |
|--------|------|---------|
| MDP / 价值函数 / Bellman 方程 | ✅ | [[强化学习基础：MDP、价值函数与迭代算法 - L5]]、[[Bellman 贝尔曼最优性原理]] |
| PPO | ✅ | [[策略梯度方法与PPO优化详解 - L12]]、[[从零实现PPO：11个关键工程化细节与实践指南]] |
| SAC / TD3 | ✅ | [[DDPG与TD3深度强化学习算法详解 - L13]] |
| On-policy vs Off-policy | ✅ | 上述笔记已覆盖 |
| MPC / PID / 经典控制 | ✅ | [[MPC与强化学习的差异、互补及结合路径 - L16]]、[[模型预测控制（MPC）的工作原理详解]] 等 |
| IL vs RL 对比 | ⚠️ | 部分覆盖，缺少 IL 专项 |

### 需要新建的笔记

| 主题 | 对应题目 | 优先级 |
|------|---------|--------|
| **Hindsight Experience Replay (HER)** | Q22 | 🔴 高 |
| - goal-conditioned RL、虚构目标、稀疏奖励 | | |
| **Safe RL 方法论** | Q24 | 🔴 高 |
| - CBF, CMDP, CPO, Shielding, Lagrangian 方法 | | |
| **Offline RL 完整综述** | Q26 | 🔴 高 |
| - CQL, IQL, TD3+BC, OOD 过估计问题 | | |
| **Multi-Task RL vs Meta-RL** | Q25 | 🟡 中 |
| - MAML, RL², 任务干扰/负迁移 | | |
| **奖励函数设计** | Q20 | 🟡 中 |
| - Reward Shaping, Potential-based, EUREKA, IRL/RLHF | | |
| **模仿学习 (IL) 完整方法** | Q19 | 🔴 高 |
| - BC, DAgger, GAIL, IRL, 分布偏移 | | |

---

## 模块四：视觉感知 (Q27-Q32)

### 已有基础

| 知识点 | 状态 | 已有资源 |
|--------|------|---------|
| 深度学习视觉基础 | ✅ | 8.Coding/01-深度学习 |
| Transformer 注意力 | ✅ | 3.Agent/01-模型基础 |
| 3DGS | ⚠️ | 可能有相关笔记但未在 Robot 目录下 |

### 需要新建的笔记

| 主题 | 对应题目 | 优先级 |
|------|---------|--------|
| **机器人 3D 感知方案对比** | Q27 | 🟡 中 |
| - 深度相机/双目/触觉/多视角融合 | | |
| **6D 物体位姿估计综述** | Q28 | 🔴 高 |
| - PoseCNN, DenseFusion, PVNet, NOCS, FoundPose, MegaPose | | |
| **NeRF & 3DGS 在具身智能中的应用** | Q29 | 🔴 高 |
| - 场景重建、数据增强、NeRF-based RL、GaussianGrasping | | |
| **VLA 视觉 Backbone 选型** | Q30 | 🟡 中 |
| - CLIP ViT, DINOv2, SigLIP, 分辨率影响, 多视角融合 | | |
| **SAM/SAM2 在机器人中的应用** | Q31 | 🟡 中 |
| - 零样本分割、referring segmentation、局限 | | |
| **遮挡处理策略** | Q32 | 🟡 中 |
| - 多视角、主动感知、形状补全、触觉 | | |

---

## 模块五：系统 & 工程 (Q33-Q40)

### 已有基础

| 知识点 | 状态 | 已有资源 |
|--------|------|---------|
| 机器人仿真 | ⚠️ | [[Isaac-Lab-Arena.md]]、[[Isaac-Lab-VLA-Benchmark.md]]、MuJoCo/ 目录 |
| LoRA 微调 | ✅ | 3.Agent/02-训练与微调 有 LoRA 相关笔记 |

### 需要新建的笔记

| 主题 | 对应题目 | 优先级 |
|------|---------|--------|
| **ROS 2 核心架构** | Q33 | 🔴 高 |
| - DDS, Node/Topic/Service/Action, ros2_control, MoveIt 2 | | |
| **VLA 推理部署优化** | Q34 | 🔴 高 |
| - 量化(AWQ/GPTQ), vLLM/TensorRT-LLM, 蒸馏, 异步执行 | | |
| **机器人训练数据 Pipeline** | Q35 | 🔴 高 |
| - RLDS/TFRecord, 多传感器同步, 数据质量, 混合采样 | | |
| **VLA Fine-tuning 实践** | Q36 | 🔴 高 |
| - LoRA 在 VLA 中的特殊应用, 灾难性遗忘, 评估策略 | | |
| **仿真平台对比** | Q37 | 🟡 中 |
| - Isaac Gym/Sim vs MuJoCo vs PyBullet 选型 | | |
| **多机器人平台训练框架设计** | Q38 | 🟡 中 |
| - 动作/观测空间标准化, LeRobot, OpenVLA 代码库 | | |
| **实时控制系统设计** | Q39 | 🟡 中 |
| - 控制频率分层, PREEMPT_RT, 异步推理 | | |
| **VLA 失败分析与调试** | Q40 | 🟡 中 |
| - 失败分类, 注意力热图, 消融实验, 轨迹对比 | | |

---

## 模块六：综合与前沿 (Q41-Q50)

### 需要新建的笔记

| 主题 | 对应题目 | 优先级 |
|------|---------|--------|
| **Open X-Embodiment (OXE) 数据集** | Q41 | 🔴 高 |
| - 22 平台、100万+轨迹、RLDS 格式、RT-X | | |
| **自然语言指令消歧** | Q42 | 🟡 中 |
| - referring expression grounding, MDETR, Grounding DINO | | |
| **Scaling Law 在机器人学习中的证据** | Q43 | 🔴 高 |
| - RT-2/RT-X 证据, 数据多样性 > 数据量, 动作精度瓶颈 | | |
| **Curriculum Learning 在具身智能中的应用** | Q44 | 🟡 中 |
| - ALP, PAIRED, 自动课程, 空间/物理难度课程 | | |
| **双臂操作 (Bimanual Manipulation)** | Q45 | 🔴 高 |
| - ALOHA, ACT, 协调性, 碰撞避免, 动作空间爆炸 | | |
| **Affordance 学习** | Q46 | 🔴 高 |
| - Where2Act, SayCan affordance, VoxPoser | | |
| **策略鲁棒性评估与提升** | Q47 | 🟡 中 |
| - 对抗训练, Domain Randomization, 多模态融合 | | |
| **视觉-触觉融合 (Visuo-Tactile)** | Q48 | 🔴 高 |
| - GelSight, BioTac, Early/Late/Cross-modal Fusion | | |
| **合成数据在具身智能中的应用** | Q49 | 🟡 中 |
| - 仿真数据, NeRF/3DGS 生成, 生成模型, sim-to-real gap | | |
| **具身智能瓶颈与未来方向** | Q50 | 🟡 中 |
| - 数据/Sim-to-Real/通用性vs精度/部署成本 | | |

---

## 学习路线建议

### 第一阶段：基础补齐 (约 2 周)

优先建立具身智能 + VLA 的完整知识框架：

1. **模仿学习 (IL)** → 覆盖 Q7, Q19
2. **Sim-to-Real Transfer** → 覆盖 Q13
3. **机器人抓取综述** → 覆盖 Q15
4. **ROS 2 核心架构** → 覆盖 Q33
5. **仿真平台对比** → 覆盖 Q37

### 第二阶段：VLA 核心 (约 3 周)

深入 VLA 模型和关键方法：

1. **RT-2 论文精读** → 覆盖 Q1, Q2
2. **Diffusion Policy + Flow Matching** → 覆盖 Q3
3. **OpenVLA + π0 对比** → 覆盖 Q4
4. **ACT + Action Chunking** → 覆盖 Q5
5. **VLA 视觉 Backbone** → 覆盖 Q30
6. **VLA Fine-tuning 实践** → 覆盖 Q36
7. **VLA 推理部署优化** → 覆盖 Q34

### 第三阶段：RL 深度 (约 2 周)

补齐 RL 关键缺口：

1. **HER** → 覆盖 Q22
2. **Offline RL (CQL, IQL, TD3+BC)** → 覆盖 Q26
3. **Safe RL** → 覆盖 Q24
4. **Multi-Task RL & Meta-RL** → 覆盖 Q25
5. **奖励函数设计 (含 EUREKA)** → 覆盖 Q20

### 第四阶段：感知与前沿 (约 2 周)

1. **6D 位姿估计** → 覆盖 Q28
2. **NeRF/3DGS 在机器人中的应用** → 覆盖 Q29
3. **World Model (Dreamer, UniSim, Genie)** → 覆盖 Q17
4. **Foundation Model 分层应用** → 覆盖 Q18
5. **OXE 数据集 + Scaling Law** → 覆盖 Q41, Q43
6. **双臂操作 + Affordance** → 覆盖 Q45, Q46
7. **视觉-触觉融合** → 覆盖 Q48

### 第五阶段：综合与系统 (约 1 周)

1. **训练数据 Pipeline** → 覆盖 Q35
2. **多机器人平台框架** → 覆盖 Q38
3. **实时控制系统** → 覆盖 Q39
4. **失败分析与调试** → 覆盖 Q40
5. **自然语言消歧** → 覆盖 Q42
6. **Curriculum Learning** → 覆盖 Q44
7. **鲁棒性评估** → 覆盖 Q47
8. **合成数据** → 覆盖 Q49

---

## 推荐资源

| 方向 | 资源 |
|------|------|
| VLA 论文 | RT-2, π0, OpenVLA, ACT, Diffusion Policy, RoboAgent |
| 数据集 | Open X-Embodiment, LIBERO, LeRobot, BridgeData V2 |
| 仿真 | Isaac Gym, MuJoCo, RoboSuite |
| 代码 | LeRobot (HuggingFace), OpenVLA GitHub |
| 综述 | A Survey on Robot Learning from Demonstrations |
| 课程 | CS 285 (Deep RL), CS 224R (Deep RL for Robotics), 具身智能课程 (MuJoCo) |

---

## 统计

- 总计需新建笔记：**~40 篇**
- 已有可复用：**~20 篇** (Transformer, RL基础, MPC, PPO, SAC 等)
- 🔴 高优先级缺口：**19 个**
- 🟡 中优先级缺口：**16 个**