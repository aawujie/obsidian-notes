---
title: 具身智能&VLA学习计划
type: learning-plan
created: 2026-06-01
updated: 2026-06-01
sources:
  - "[[具身智能&VLA面试50题：一份够用的技术 cheat sheet]]"
  - "[[具身智能-VLA-学习清单]]"
tags:
  - embodied-ai
  - vla
  - learning-plan
  - robotics
share_link: https://share.note.sx/7b41yjvb#/dX9vjfCNnI2XqpuHYmEPPFdiFuCt3jIpee2iP+43js
share_updated: 2026-06-01T17:17:28+08:00
---

## 总览

- **总时长**: ~10 周（全日制）/ ~16 周（业余）
- **覆盖面试题**: 50/50 题
- **已创建论文笔记**: 35 篇
- **前置依赖**: Transformer 基础、RL 基础（PPO/TD3）、Python
- **注意**: 知识库有 TD3 深度笔记（[[DDPG与TD3深度强化学习算法详解 - L13]]），但 **SAC 缺少专门笔记**（仅在 RL_学习笔记中提过一次），SAC 是 CQL/IQL 的前置依赖，需在阶段三前补充

### 知识依赖图

```
┌─────────────────────────────────────────────────────────────┐
│  阶段一：基础补齐（2周）                                        │
│  IL + Sim-to-Real + 抓取 + ROS2 + 仿真                         │
│  产出: 建立具身智能全局认知                                      │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│  阶段二：VLA 核心（3周）                                        │
│  RT-2 → Diffusion Policy → OpenVLA/π0 → ACT → 推理部署       │
│  产出: 理解 VLA 从原理到部署的完整链路                            │
└──────────────────────────┬──────────────────────────────────┘
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ 阶段三:RL深度 │  │阶段四:感知前沿│  │阶段五:系统工程│
│ (2周)       │  │ (2周)       │  │ (1周)       │
│ HER/Offline │  │ 位姿/NeRF/  │  │ Pipeline/   │
│ Safe/Meta   │  │ SAM/World   │  │ 多平台/实时  │
│ EUREKA奖励  │  │ Model       │  │ 调试/消歧    │
└─────────────┘  └─────────────┘  └─────────────┘
          │                │                │
          └────────────────┼────────────────┘
                           ▼
                    ┌─────────────┐
                    │ 综合整合复习  │
                    │ 开放题准备    │
                    └─────────────┘
```

---

## 阶段一：具身智能全局认知（2 周，8 个主题）

> **目标**: 建立具身智能的完整知识框架，理解"问题域"——这个领域在解决什么、为什么难、有哪些基本方法。

### 1.1 模仿学习 (Imitation Learning) 🔴

**学什么**:
- Behavior Cloning (BC) 的数学原理：$\min_\theta \mathbb{E}_{(o,a)\sim\mathcal{D}} \| \pi_\theta(o) - a \|^2$
- 分布偏移 (Distribution Shift / Covariate Shift) —— 为什么 BC 会失败
- DAgger: 在线交互收集数据的迭代 BC
- GAIL (Generative Adversarial Imitation Learning): 用 GAN 框架做 IL
- IRL (Inverse Reinforcement Learning): 从演示中推断奖励函数

**论文**: ACT 论文笔记中已覆盖 BC 部分；DAgger/GAIL/IRL 需补充阅读

**为什么学**:
- 面试 Q7 直接考 BC、Q19 考 IL vs RL 对比
- BC 是所有 VLA 模型的训练基础（RT-2、OpenVLA、π0 全都用 BC 范式预训练）
- 不理解分布偏移，就无法理解为什么需要 Action Chunking、为什么需要 RL fine-tune
- 这是具身智能最基本的学习范式，后续所有内容都建立在这个基础之上

**前置**: 监督学习基础

### 1.2 Sim-to-Real Transfer 🔴

**学什么**:
- Reality Gap 的本质：物理差异（碰撞、摩擦、形变）+ 外观差异（光照、纹理）+ 感知差异（传感器噪声）
- Domain Randomization: 在仿真中随机化物理参数、纹理、光照 → 迫使策略学到不变特征
- Domain Adaptation: 用少量真实数据 fine-tune 仿真策略（如 fine-tune 视觉 encoder）
- 数字孪生 (Digital Twin): 用精确物理引擎（Isaac Sim）和 3D 扫描构建高保真仿真
- Photorealistic Rendering: 用 NeRF/3DGS 从真实场景构建可渲染模型

**论文**: 相关内容分散在 NeRF、3DGS、RT-X 等笔记中，需新建一篇系统性笔记

**为什么学**:
- 面试 Q13 直接考、Q49 间接考合成数据风险
- 具身智能的核心矛盾：真实数据昂贵 → 必须依赖仿真 → 仿真与真实有 gap
- 几乎所有 VLA 模型的训练都涉及 sim-to-real：RT-2 用真实数据、π0 用了大量真实机器人数据
- 在工程实践中，sim-to-real 是决定能否落地的关键

**前置**: 基础物理直觉、机器学习中的 domain shift 概念

### 1.3 机器人抓取 (Grasping) 🟡

**学什么**:
- 解析方法 vs 数据驱动方法的范式差异
- GraspNet-1Billion: 大规模数据集 + 点云 → 预测每个点的抓取分数和 6-DoF 位姿
- Contact-GraspNet: 基于接触点预测，更符合物理直觉
- AnyGrasp: 旋转等变特征，泛化能力强
- 评价指标：抓取成功率、抗扰动能力、透明/反光物体鲁棒性

**论文**: GraspNet-1Billion、Contact-GraspNet、AnyGrasp（已创建笔记）

**为什么学**:
- 面试 Q15 直接考
- 抓取是最基础的操作原语，几乎所有复杂操作都以抓取为前提
- 理解抓取 → 理解操作的基本范式（感知 → 规划 → 执行）
- GraspNet 系列展示了"大规模数据 + 深度学习"在机器人领域的成功范式，与 VLA 的思路一脉相承

**前置**: 3D 感知基础（点云、RGB-D）

### 1.4 ROS 2 核心架构 🔴

**学什么**:
- DDS (Data Distribution Service): 去中心化通信，无 ROS Master，支持实时性
- 核心概念：Node（计算单元）、Topic（发布/订阅）、Service（请求/响应）、Action（带反馈的长任务）
- ros2_control: 标准硬件接口抽象（硬件抽象层 → 控制器管理器 → 控制器）
- MoveIt 2: 运动规划框架（碰撞检测、路径规划、轨迹生成）
- ROS 1 vs ROS 2 关键差异：实时性、多机器人、安全通信（SROS2）

**论文**: 无特定论文，需参考 ROS 2 官方文档

**为什么学**:
- 面试 Q33 直接考
- ROS 2 是机器人软件栈的事实标准，面试中体现你的工程落地能力
- VLA 模型最终要通过 ROS 2 与真实机器人交互——理解通信机制和实时性约束是工程部署的前提
- 不学 ROS 2 = 只会纸上谈兵

**前置**: Linux 基础、网络通信基本概念

### 1.5 仿真平台对比 🟡

**学什么**:
- MuJoCo: 物理精度高（接触力建模出色）、轻量、学术界标准（DMControl, Gymnasium）
- Isaac Gym/Sim: GPU 并行仿真（数千环境并行）、适合大规模 RL 训练、支持光线追踪渲染
- PyBullet: 开源、轻量、适合快速原型
- 选型决策：大规模 RL → Isaac Gym；算法验证 → MuJoCo；数字孪生 → Isaac Sim

**论文**: 无特定论文

**为什么学**:
- 面试 Q37 直接考
- 仿真平台是具身智能的"实验室"——选错仿真平台会影响整个研发流程的效率
- 理解不同仿真器的物理引擎差异 → 理解 sim-to-real gap 的来源
- 实践中，Isaac Gym 用于大规模并行 RL、MuJoCo 用于精确物理验证，这是标准组合

**前置**: 基础物理概念、RL 训练流程

### 1.6 奖励函数设计 🟡

**学什么**:
- 稀疏奖励 vs 密集奖励的 tradeoff：稀疏奖励简单但探索困难；密集奖励加速收敛但可能 reward hacking
- Potential-based Shaping: $F(s, s') = \gamma\Phi(s') - \Phi(s)$，不改变最优策略的理论保证
- EUREKA: LLM 自动生成奖励函数代码，迭代优化（反思机制）
- IRL/RLHF: 从演示或人类反馈中学习奖励函数

**论文**: EUREKA（已创建笔记）

**为什么学**:
- 面试 Q20 直接考
- 奖励函数设计是 RL 中最依赖经验的部分——EUREKA 代表了用 LLM 自动化这一过程的趋势
- 理解 EUREKA 的反思机制 → 理解 LLM 如何辅助 RL → 联系 Q18（Foundation Model 在奖励层的应用）

**前置**: RL 基础（PPO/TD3），SAC 需在阶段三前补充

### 1.7 Open-Vocabulary 操作 🟡

**学什么**:
- 传统操作 vs Open-Vocabulary 操作的本质差异：前者只能操作训练见过的物体，后者可以操作任意语言描述的对象
- CLIP-Fields: 将 CLIP 语义嵌入与 NeRF-like 空间表示结合，构建可查询的 3D 语义地图
- OWL-ViT: 开集物体检测，用于定位任意语言描述的目标
- Referring Expression Resolution: 解决"把那个红色的东西拿过来"中的指代消歧

**论文**: CLIP-Fields（已创建笔记）；OWL-ViT 需补充

**为什么学**:
- 面试 Q16 直接考、Q42 间接考语言消歧
- Open-Vocabulary 是 VLA 泛化能力的核心体现——RT-2 的核心卖点就是"能理解从未见过的物体指令"
- CLIP-Fields 展示了"VLM 嵌入 + 3D 空间"的融合思路，直接影响后续的 VoxPoser 等工作

**前置**: CLIP 基础原理

### 1.8 Foundation Model 在具身智能中的分层应用 🔴

**学什么**:
- 五层架构：感知层（CLIP/DINOv2/SAM）→ 规划层（GPT-4/Claude）→ 策略层（RT-2/π0）→ 奖励层（EUREKA）→ 数据层（RoboGen）
- 每层的代表性工作及其关系
- 核心洞察：不需要一个大模型做所有事，而是用不同层级的模型做各自擅长的事

**论文**: 这是一个元认知框架，需整合多篇论文笔记

**为什么学**:
- 面试 Q18 直接考
- 这是具身智能的"架构图"——面试官通过这道题判断你是否有系统性思维
- 五层架构可以作为面试回答的框架：任何新工作都可以放到这个框架中定位
- 理解分层 → 理解为什么 π0 选择 VLM 做语义 + Flow 网络做动作（不是技术选型问题，是架构哲学问题）

**前置**: 完成阶段一其他主题，这是本阶段的总结性主题

---

### 阶段一 学习顺序建议

```
Day 1-2: 模仿学习 (IL)        ← 最基本的学习范式
Day 3-4: Sim-to-Real Transfer  ← 核心矛盾
Day 5-6: 机器人抓取            ← 基本操作原语
Day 7-8: ROS 2 核心架构        ← 工程基础
Day 9:   仿真平台对比          ← 工具选择
Day 10:  奖励函数设计          ← RL 视角
Day 11:  Open-Vocabulary 操作  ← VLM 视角
Day 12-14: Foundation Model 分层应用 + 阶段回顾
```

---

## 阶段二：VLA 核心架构（3 周，7 个主题）

> **目标**: 深入理解 VLA 模型从原理到部署的完整链路，能对比不同架构的设计取舍。

### 2.1 RT-2: VLA 的奠基之作 🔴

**学什么**:
- 动作 Token 化：将 7-DoF 连续动作离散化为 256 个 bin → 编码为文本 token → VLM 直接生成
- Co-fine-tuning: 互联网 VQA 数据 + 机器人轨迹数据联合训练 → 知识迁移
- 为什么这么做有效：VLM 的语义理解能力（如"拿起当锤子用的石头"）直接迁移到物理操作
- 局限：离散化损失精度（256 bin 的量化误差）、自回归推理延迟高

**论文**: [[RT-2-Robotic-Transformer-2]]（已创建笔记）

**为什么学**:
- 面试 Q1、Q2 直接考——这是最基础的 VLA 问题，答不好直接出局
- RT-2 是 VLA 概念的源头，定义了"VLM 直接输出动作"这个范式
- 理解 RT-2 的设计取舍（精度 vs 泛化），才能理解后续 OpenVLA 和 π0 的改进动机

**前置**: VLM 基本概念（CLIP、多模态 Transformer）

### 2.2 Diffusion Policy: 动作生成的另一种范式 🔴

**学什么**:
- 扩散模型用于动作建模的数学原理：$p(A_t | O_t)$ 通过 K 步去噪生成，天然建模多模态分布
- 为什么传统方法（高斯分布、分类头）无法处理多模态动作
- CNN-based vs Transformer-based 扩散网络：Transformer 对高频动作变化的建模更好
- Receding Horizon Control + Warm-starting: 预测长序列但只执行前几步
- 与 RT-2 自回归方式的对比：精度高但推理慢

**论文**: [[Diffusion-Policy-扩散策略]]（已创建笔记）

**为什么学**:
- 面试 Q3 直接考——Diffusion Policy vs 自回归的本质区别是高频考点
- 扩散模型是当前动作生成的主流方法之一：π0 的 Flow Matching 就是扩散模型的进化版
- 理解 Diffusion Policy → 理解为什么"动作精度"和"推理速度"是核心 tradeoff

**前置**: 扩散模型基础原理（DDPM 的 forward/reverse process）

### 2.3 Flow Matching & π0 🔴

**学什么**:
- Flow Matching 原理：学习向量场 $v_\theta(x_t, t)$ 定义从噪声到数据的最优传输 ODE
- Flow Matching vs Diffusion: ODE（确定性）vs SDE（随机），相同效果下步数更少
- π0 的混合架构：VLM backbone 做语义理解 + Flow Matching 动作头做精细动作输出
- 为什么解耦：语言理解能力与精细操作能力来自不同的数据分布，分开建模更有效
- π0 的数据规模：10,000+ 小时真实机器人数据、7 种机器人平台、68 个任务

**论文**: [[π0-Physical-Intelligence-VLA]]（已创建笔记）

**为什么学**:
- 面试 Q3（Flow Matching vs Diffusion）、Q4（π0 vs RT-2 对比）
- π0 代表了 VLA 的最新方向：混合架构 + 大规模真实数据 + Flow Matching
- 理解 π0 → 理解 VLA 架构的进化逻辑：RT-2(统一Token空间) → OpenVLA(开源+高效微调) → π0(混合架构+Flow Matching)

**前置**: RT-2、Diffusion Policy

### 2.4 OpenVLA: 开源化 + 高效微调 🔴

**学什么**:
- OpenVLA 的设计取舍：开源 7B、LLaVA 框架、更高效的动作分词
- LoRA 在 VLA 中的应用：只对 VLM backbone 做 LoRA，动作头全量训练
- 与 RT-2 的对比：RT-2 闭源 + PaLI-X/PaLM-E（50B+），OpenVLA 开源 + 7B + 单卡可微调
- 灾难性遗忘的缓解：机器人数据量远小于预训练数据，需低学习率 + 混合原始数据

**论文**: [[OpenVLA-开源VLA模型]]（已创建笔记）

**为什么学**:
- 面试 Q4、Q36 覆盖
- OpenVLA 是开源社区最活跃的 VLA 项目，是动手实践的最佳入口
- 理解 LoRA 在 VLA 中的特殊应用 → 理解大模型微调在机器人领域的工程挑战

**前置**: RT-2、LoRA 基础知识

### 2.5 ACT & Action Chunking 🔴

**学什么**:
- Action Chunking 的动机：减少推理频率 → 降低累积误差（compounding error）
- Temporal Ensemble: 多个预测 chunk 的加权融合 → 动作平滑
- Chunk size 的选择：太小失去优势（10-50 步典型），太大导致动作滞后
- ACT 的双臂应用：ALOHA 硬件 + ACT 算法 → 精细双臂操作
- CVAE 变分自编码器在 ACT 中的作用：建模动作的风格变化（不同的操作方式）

**论文**: [[ACT-Action-Chunked-Transformers]]、[[ALOHA-低成本双臂遥操作]]、[[Bimanual-ALOHA-ACT-双臂操作]]（已创建笔记）

**为什么学**:
- 面试 Q5 直接考、Q45 双臂操作间接涉及
- Action Chunking 是实用工程技巧——几乎所有部署的 VLA 都用某种形式的 chunking
- ACT + ALOHA 是双臂操作的标杆工作，理解它就理解了双臂方向的当前 SOTA

**前置**: Behavior Cloning

### 2.6 VLA 视觉 Backbone 选型 🟡

**学什么**:
- 常用 backbone 对比：CLIP ViT（语义丰富）、DINOv2（空间结构好）、SigLIP（OpenVLA 使用）
- 分辨率影响：操作任务需要精细空间信息，448×448 显著优于 224×224
- 多视角融合：腕部相机（局部）+ 全局相机（全局）→ 互补
- 时序信息处理：多帧 stack vs temporal attention

**论文**: 分散在 RT-2、OpenVLA、π0 等笔记中

**为什么学**:
- 面试 Q30 直接考
- 视觉 backbone 的选择直接影响策略的泛化能力和精细操作精度
- 面试中体现你对"模型组件选型"有工程判断力

**前置**: ViT 基础、CLIP 基础

### 2.7 VLA 推理部署优化 🔴

**学什么**:
- 延迟瓶颈分析：VLM backbone 的 prefill（视觉 token 处理）+ 自回归 decode，7B 模型典型 100-500ms
- 量化：INT8/INT4 (AWQ, GPTQ)，速度提升 2-4x
- 推理框架：vLLM、TensorRT-LLM、lmdeploy
- 模型蒸馏：7B → 1B，保持大部分效果
- 异步执行：推理与控制线程解耦，使用最新可用动作
- Action Chunking 的部署意义：低频推理 + 高频执行

**论文**: 无特定论文，工程实践知识

**为什么学**:
- 面试 Q34 直接考
- 部署是 VLA 落地的最后一公里——模型再好，跑不动也是白费
- 延迟直接影响控制频率，控制频率直接影响操作精度——这是工程核心

**前置**: 模型量化基础、系统架构基础

---

### 阶段二 学习顺序建议

```
Day 1-3:   RT-2 论文精读        ← VLA 范式的起源
Day 4-5:   Diffusion Policy      ← 动作生成的另一范式
Day 6-7:   Flow Matching + π0    ← 最新范式
Day 8-9:   OpenVLA + LoRA 微调   ← 开源实践入口
Day 10-11: ACT + Action Chunking ← 工程必学
Day 12-13: VLA 视觉 Backbone     ← 组件选型
Day 14-15: VLA 推理部署优化      ← 落地最后一公里
Day 16-21: 阶段回顾 + 架构对比总结
```

**关键节点**：学完 RT-2 和 π0 后，画一张 VLA 架构演进图（RT-2 → OpenVLA → π0），标注每次迭代解决了什么问题、引入了什么新 tradeoff。

---

## 阶段三：RL 深度（2 周，5 个主题）

> **目标**: 补齐 RL 在机器人场景的关键缺口——样本效率、安全性、离线利用。

### 3.1 HER (Hindsight Experience Replay) 🔴

**学什么**:
- 核心思想：失败的 episode 也可以学习——把实际到达的状态当作"虚构目标"重新计算奖励
- 为什么有效：在稀疏奖励下，随机探索几乎不可能成功 → HER 把每个失败变成"成功到达某处"
- 实现细节：goal-conditioned RL 框架，每个 transition $(s_t, a_t, r_t, s_{t+1}, g)$ 可以被重新标记为 $(s_t, a_t, r'_t, s_{t+1}, g')$
- 局限：需要 goal-conditioned 任务结构；多阶段任务效果有限

**论文**: [[HER-Hindsight-Experience-Replay]]（已创建笔记）

**为什么学**:
- 面试 Q22 直接考——经典算法，几乎必问
- HER 的思想贯穿整个具身智能：从失败中学习、稀疏奖励处理
- 与 Action Chunking 互补：HER 解决学习效率，Chunking 解决执行精度

**前置**: DQN、Experience Replay、Goal-Conditioned RL 概念

### 3.2 Offline RL 🔴

**学什么**:
- 核心挑战：分布外 (OOD) 动作的 Q 值过估计——Q 函数对训练数据中未覆盖的动作给出虚假高值
- CQL: 对 OOD 动作的 Q 值施加惩罚，保证 Q 函数是真值的下界
- IQL: 用 expectile regression 避免直接查询 OOD 动作，更稳定
- TD3+BC: 极简方案——在 TD3 上直接加 BC 正则化项
- 在具身智能中的意义：可直接从 OXE 大规模数据集离线学习策略

**论文**: [[CQL-Conservative-Q-Learning]]、[[IQL-Implicit-Q-Learning]]、[[TD3-BC-离线强化学习]]（已创建笔记）

**为什么学**:
- 面试 Q26 直接考
- Offline RL 是具身智能中数据利用的关键——OXE 有 100 万+条轨迹，不能在线交互，只能离线学习
- 离线 RL 三篇论文都基于 SAC 框架，不学 SAC 就无法真正理解 CQL/IQL
- SAC 是 Offline RL 三篇论文的前置依赖，**[缺少专门笔记，需补充]**
- 三篇论文代表了三种不同哲学：保守主义（CQL）、回避主义（IQL）、极简主义（TD3+BC）
- 面试中对比这三种方法的 tradeoff 是体现深度的好机会

**前置**: SAC（最大熵框架、双 Q、自动温度调节）、TD3、Bellman 方程

### 3.3 Safe RL 🔴

**学什么**:
- Control Barrier Function (CBF): 数学约束保证状态始终在安全集内，可与学习策略叠加
- Constrained MDP (CMDP): 在 MDP 中加入安全约束，用 Lagrangian 方法求解（CPO, PPO-Lagrangian）
- Conservative Policy Update: 限制策略更新步长
- Shielding: 外挂安全监控层，检测危险动作时覆盖
- 工程实践：关节力矩限制、软件急停、碰撞检测提前终止

**论文**: 需新建笔记

**为什么学**:
- 面试 Q24 直接考
- Safe RL 是真实机器人部署的刚需——仿真 crash 没有成本，真实机器人 crash 成本极高
- 体现你对"算法 → 真实系统"落地的安全意识

**前置**: RL 基础、CMDP 概念、Lagrangian 优化

### 3.4 Multi-Task RL & Meta-RL 🟡

**学什么**:
- Multi-Task RL: 同时训练多个任务，共享表示；挑战是负迁移（任务间干扰）
- Meta-RL: 学习"学习的能力"——MAML 学习初始参数，少量梯度步快速适应新任务
- MAML 的核心公式：$\theta' = \theta - \alpha \nabla_\theta \mathcal{L}_{\mathcal{T}_i}(f_\theta)$，内层在任务上更新，外层跨任务优化初始参数
- RL²: 用 RNN 将"学习过程"编码为隐状态

**论文**: [[MAML-模型无关元学习]]（已创建笔记）

**为什么学**:
- 面试 Q25 直接考
- Multi-Task RL 对应"一个机器人学会多种技能"，Meta-RL 对应"快速适应新物体/新环境"
- 在 VLA 语境下，Meta-RL 的"快速适应"思想与 LoRA fine-tune 异曲同工

**前置**: PPO、策略梯度

### 3.5 模仿学习补充 🟡

**学什么**:
- GAIL: Generator（策略）生成轨迹，Discriminator 区分专家/生成 → 对抗训练
- IRL: 最大熵 IRL → 从演示推断奖励函数 → 用推断的奖励训练策略
- IL + RL hybrid: BC 初始化策略 → RL fine-tune（如 BC + SAC）
- 这个范式在 VLA 中的应用：大规模 BC 预训练 → 在线 RL 微调

**论文**: GAIL、IRL 需补充阅读

**为什么学**:
- 面试 Q19 直接考 IL vs RL 对比、"IL 初始化 + RL fine-tune"是标准答案
- 这是连接阶段一（IL 基础）和阶段三（RL 深度）的桥梁

**前置**: 阶段一的模仿学习基础

---

### 阶段三 学习顺序建议

```
Day 1-2: HER                    ← 稀疏奖励经典解法
Day 3-5: Offline RL 三篇对比    ← 数据利用的核心
Day 6-7: Safe RL               ← 真实部署的刚需
Day 8-9: Multi-Task RL + MAML  ← 泛化与适应
Day 10-12: 模仿学习补充         ← IL+RL 混合范式
Day 13-14: 阶段回顾
```

---

## 阶段四：感知与世界模型（2 周，7 个主题）

> **目标**: 理解机器人如何"看"和如何在"脑内模拟"。

### 4.1 6D 物体位姿估计 🔴

**学什么**:
- 问题定义：从 RGB/RGB-D 图像估计物体的 3D 旋转 + 3D 平移
- 基于模板匹配（PoseCNN, DenseFusion）：需要 3D CAD 模型，精度高
- 基于关键点（PVNet, GDR-Net）：预测 2D 关键点 + PnP 求解
- 类别级位姿估计（NOCS, SPD）：同类物体泛化
- Foundation Model 方法（FoundPose, MegaPose）：零样本估计

**论文**: [[DenseFusion-6D位姿估计]]、[[FoundPose-零样本位姿估计]]（已创建笔记）

**为什么学**:
- 面试 Q28 直接考
- 位姿估计是抓取的"上游任务"——位置都不知道，不可能抓对
- FoundPose 代表了 Foundation Model 取代专用模型的大趋势

**前置**: 相机模型、刚体变换、PnP 算法基础

### 4.2 NeRF & 3DGS 在机器人中的应用 🔴

**学什么**:
- NeRF 原理：5D 函数 $F_\Theta(\mathbf{x}, \mathbf{d}) \to (\mathbf{c}, \sigma)$，用 MLP 隐式表示场景
- 3DGS 原理：用 3D 高斯原语显式表示场景 → 可微分光栅化 → 实时渲染 (100+ FPS)
- NeRF vs 3DGS: 隐式 vs 显式、慢 vs 快、训练小时级 vs 分钟级
- 机器人应用：场景重建 → 数据增强 → NeRF-based RL → GaussianGrasping

**论文**: [[NeRF-神经辐射场]]、[[3D-Gaussian-Splatting-三维高斯泼溅]]（已创建笔记）

**为什么学**:
- 面试 Q29 直接考
- 3DGS 的实时渲染能力使"在神经渲染场景中训练策略"成为现实
- 与 sim-to-real 衔接：用真实场景的 NeRF/3DGS 重建作为仿真环境 → 跨越 reality gap

**前置**: 体渲染基础、可微分渲染概念

### 4.3 World Model (Dreamer, UniSim, Genie) 🔴

**学什么**:
- Dreamer v3 的 RSSM 架构：确定性状态 $h_t$ + 随机状态 $z_t$ → 在"想象"中训练 Actor-Critic
- UniSim: 用视频生成模型作为通用模拟器，输入当前观测 + 动作 → 预测未来视频帧
- Genie: 从无标注视频中自主学习"动作"概念，实现交互式控制
- 三种路线的本质区别：Dreamer（潜在空间世界模型）vs UniSim（像素空间世界模型）vs Genie（无动作标注世界模型）

**论文**: [[Dreamer-v3-世界模型RL]]、[[UniSim-通用视频模拟器]]、[[Genie-可控世界模型]]（已创建笔记）

**为什么学**:
- 面试 Q17 直接考
- World Model 被视为解决"真实机器人数据昂贵"问题的终局方案：在脑海中试错
- 三种路线代表了不同的技术信仰：压缩派（潜在空间）、生成派（像素空间）、无监督派
- Q50 开放题中，"World Model + RL"是核心突破方向之一

**前置**: Dreamer v3 需要 VAE + RNN + Actor-Critic；UniSim/Genie 需要视频生成基础

### 4.4 SAM/SAM2 在机器人中的应用 🟡

**学什么**:
- SAM 原理：图像编码器 + Prompt 编码器（点/框/文本） + Mask 解码器
- 机器人应用：零样本实例分割 → 物体定位 → 结合 CLIP 做 referring segmentation → 为位姿估计提供 ROI
- SAM2: 扩展到视频/连续帧跟踪，更适合机器人场景
- 局限：2D mask 无深度、遮挡/透明物体效果差、原版推理速度慢

**论文**: [[SAM-Segment-Anything-Model]]（已创建笔记）

**为什么学**:
- 面试 Q31 直接考
- SAM 是感知层的 Foundation Model，配合 VLA 使用
- 体现你对"大模型能力如何在机器人 pipeline 中落地"的理解

**前置**: 图像分割基础

### 4.5 机器人 3D 感知方案对比 🟡

**学什么**:
- 深度相机（RealSense/Azure Kinect）：结构光/ToF，近距离精度好但受光照干扰
- 双目相机：被动式，远距离可用但近距离精度不如结构光
- RGB-D + 点云：用 PointNet/PointTransformer 处理
- 触觉传感器（GelSight）：接触时获取精细 3D 形状，补充视觉盲点

**论文**: 分布在多篇笔记中

**为什么学**:
- 面试 Q27 直接考
- 感知方案的选择直接影响策略性能的上限
- 理解传感器特性 → 理解 sim-to-real gap 中"感知差异"的成分

**前置**: 相机模型、点云处理基础

### 4.6 视觉-触觉融合 (Visuo-Tactile) 🔴

**学什么**:
- GelSight 原理：弹性体 + 反光膜 + LED 照明 + 微型相机 → 光度立体视觉恢复 3D 几何
- 应用场景：抓取稳定性判断（滑动检测）、精细操作（插孔、旋转）、软体/易碎物体操作
- 融合方式：Early Fusion（低级特征拼接）、Late Fusion（分别编码后决策层融合）、Cross-modal Attention（交互注意力）
- 挑战：触觉数据获取慢、数据集稀少、传感器成本

**论文**: [[GelSight-视觉触觉传感器]]（已创建笔记）

**为什么学**:
- 面试 Q48 直接考
- 触觉是当前具身智能的"最后一块拼图"——视觉无法感知力、手感、材质
- Q50 开放题中，触觉集成是重要突破方向

**前置**: 多模态学习基础

### 4.7 遮挡处理 + 形状补全 🟡

**学什么**:
- 多视角感知：增加相机数量，从不同角度消除遮挡
- 主动感知 (Active Perception): 机器人主动移动相机到更优视角
- 形状补全 (Shape Completion): 从部分点云预测完整 3D 形状（3D-EPN, GRNet）
- 历史帧融合 + 触觉辅助

**论文**: [[3D-EPN-形状补全]]（已创建笔记）

**为什么学**:
- 面试 Q32 直接考
- 遮挡是真实场景中的高频问题，涉及感知、规划、控制的协同

**前置**: 点云处理、3D 深度学习基础

---

### 阶段四 学习顺序建议

```
Day 1-2:  6D 位姿估计          ← 感知→抓取的桥梁
Day 3-4:  NeRF + 3DGS          ← 场景重建技术
Day 5-7:  World Model 三篇     ← 最核心的前沿方向
Day 8:    SAM/SAM2             ← 感知 Foundation Model
Day 9-10: 3D 感知方案 + 遮挡   ← 工程感知体系
Day 11-12: 视觉-触觉融合       ← 前沿方向
Day 13-14: 阶段回顾
```

---

## 阶段五：系统工程与前沿整合（1 周，8 个主题）

> **目标**: 连接"算法"与"系统"，理解 VLA 如何从实验室走向真实机器人。

### 5.1 训练数据 Pipeline 🔴

**学什么**:
- 数据格式：RLDS (TFRecord) = OXE 标准；LeRobot = HuggingFace 格式
- 多传感器同步：相机、力矩、关节角的时间戳对齐 → 通常用硬件同步信号
- 数据质量：自动过滤失败轨迹（基于任务成功检测）、人工审核采样
- 大规模存储与加载：分布式存储 + 异步 prefetch
- 在线-离线混合采样策略

**论文**: OXE 论文中有详细描述

**为什么学**:
- 面试 Q35 直接考
- 数据 pipeline 是具身智能的"基础设施"——OXE 的价值不仅在于数据本身，更在于统一了格式和基础设施
- 体现你的工程化思维

**前置**: OXE 数据集知识

### 5.2 多机器人平台训练框架 🟡

**学什么**:
- 动作空间标准化：不同机器人 DoF 不同 → 统一到末端执行器空间 (EEF) 或相对动作
- 观测空间标准化：统一图像分辨率和相机标定格式
- 模型适配层：针对不同硬件的动作头
- 代表框架：LeRobot (HuggingFace)、OpenVLA 代码库

**论文**: 分散在 OpenVLA、RT-X 等笔记中

**为什么学**:
- 面试 Q38 直接考
- 多平台泛化是 RT-X 的核心贡献，也是 Foundation Model 的前提

**前置**: ROS 2、OXE 数据集

### 5.3 实时控制系统设计 🟡

**学什么**:
- 控制频率分层：关节级 500-1000 Hz → 任务级 10-50 Hz → VLA 推理 1-10 Hz
- 分层控制架构：VLA 低频输出目标位姿 → 底层 PD 控制器高频执行
- Linux 实时补丁 (PREEMPT_RT) 保证低延迟调度
- Action Chunking 的部署意义：低频推理 + 高频执行
- 异步设计：推理线程与控制线程解耦

**论文**: 无特定论文

**为什么学**:
- 面试 Q39 直接考
- 实时性是机器人系统的核心约束——不理解控制频率分层就不理解 VLA 的部署挑战

**前置**: ROS 2、控制理论基础

### 5.4 VLA 失败分析与调试 🟡

**学什么**:
- 失败三分法：感知失败（识别错误）→ 规划失败（动作方向错误）→ 执行失败（精度不足）
- 注意力热图分析模型关注区域
- t-SNE 分析嵌入空间
- 消融实验：分别测试视觉/语言/动作头的贡献
- 成功 vs 失败轨迹的特征分布对比

**论文**: 无特定论文

**为什么学**:
- 面试 Q40 直接考
- 调试能力是面试官判断"真实经验 vs 纸上谈兵"的关键指标
- 体现系统性debug思维

**前置**: VLA 全链路理解

### 5.5 自然语言指令消歧 🟡

**学什么**:
- 指代消解 (Referring Expression): 语言中的"它""那个"需结合视觉确定指代对象
- MDETR/Grounding DINO: 用 VLM 做 referring expression grounding
- 多轮对话澄清：低置信时主动向用户提问
- 不确定性建模：输出置信度，触发澄清机制

**论文**: 分散在 CLIP-Fields 等笔记中

**为什么学**:
- 面试 Q42 直接考
- 自然语言模糊性是 VLA 在真实场景中的核心挑战之一

**前置**: VLM、CLIP

### 5.6 Curriculum Learning 🟡

**学什么**:
- 从简单到复杂：单步操作 → 双步 → 长程序列
- 自动课程 (ALP, PAIRED): 根据智能体能力自动调整任务难度
- 空间课程：从小范围 → 全工作空间
- 物理难度课程：规则物体 → 复杂形状/易碎/软体

**论文**: 需补充阅读

**为什么学**:
- 面试 Q44 直接考
- Curriculum Learning 是大规模训练中的效率杠杆

**前置**: RL、IL 基础

### 5.7 策略鲁棒性评估 🟡

**学什么**:
- 测试维度：外观扰动（光照/纹理）、物理扰动（推力/抖动）、初始状态扰动、OOD 物体
- 提升方法：数据增强、Domain Randomization、对抗训练、多模态融合

**论文**: 分散在多篇笔记中

**为什么学**:
- 面试 Q47 直接考
- 鲁棒性是区分"实验室 demo"和"真实可部署"的关键

**前置**: Sim-to-Real Transfer

### 5.8 合成数据 🟡

**学什么**:
- 来源：物理仿真 (Isaac/MuJoCo)、渲染引擎 (Blender)、生成模型 (SD/DiT)、NeRF/3DGS
- 应用：仿真预训练 + 真实 fine-tune
- 风险：sim-to-real gap 放大、数据偏差、物理不准确

**论文**: 分散在多篇笔记中

**为什么学**:
- 面试 Q49 直接考
- 合成数据是解决"数据稀缺"的主要手段，但风险也很明确

**前置**: Sim-to-Real Transfer、NeRF/3DGS

---

### 阶段五 学习顺序建议

```
Day 1: 训练数据 Pipeline
Day 2: 多机器人平台框架
Day 3: 实时控制系统
Day 4: 失败分析与调试
Day 5: 自然语言消歧
Day 6: Curriculum Learning + 鲁棒性 + 合成数据
Day 7: 全量回顾
```

---

## 最后：开放题准备

面试 Q50（"如何看待具身智能当前的瓶颈？未来3年最可能的突破方向？"）是展示视野的关键。

建议在全部阶段完成后，用自己的话重新组织以下分析框架：

```
当前瓶颈（四个维度）:
├── 数据瓶颈: 高质量演示数据远低于 NLP/CV → 怎么办?
├── Sim-to-Real Gap: 仿真物理不完美 → 怎么缩小?
├── 通用性 vs 精度: 大模型泛化好但操作不精细 → 怎么统一?
└── 部署成本: 7B+模型边缘端跑不动 → 怎么优化?

突破方向（五个方向）:
├── 大规模自主数据采集（机器人集群自主探索）
├── World Model + RL（减少真实交互依赖）
├── 更高效的 VLA 架构（Flow Matching、Mamba/SSM）
├── 硬件-软件协同设计（专用推理芯片 + 轻量化模型）
└── 触觉等多模态感知大规模集成
```

---

## 学习检查点

每完成一个阶段，用面试题自测：

| 阶段 | 自测题目 |
|------|---------|
| 阶段一 | Q7, Q13, Q15, Q19, Q33, Q37 |
| 阶段二 | Q1-Q6, Q8-Q10, Q30, Q34, Q36 |
| 阶段三 | Q20, Q22, Q24, Q25, Q26 |
| 阶段四 | Q17, Q27, Q28, Q29, Q31, Q32, Q48 |
| 阶段五 | Q35, Q38, Q39, Q40, Q42, Q44, Q47, Q49 |
| 综合 | Q11, Q12, Q16, Q18, Q41, Q43, Q45, Q46, Q50 |