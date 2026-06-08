---
title: SONIC与BFM-0——人形机器人行为基础模型
type: concept
created: 2026-06-07
updated: 2026-06-07
sources: [B站 BV1tNGq6mEug, NVIDIA GEAR Lab 伯克利讲座]
tags: [人形机器人, 行为基础模型, motion-tracking, 强化学习, NVIDIA, BFM-0, SONIC, humanoid]
---

# SONIC与BFM-0——人形机器人行为基础模型

> 演讲者：Zen (NVIDIA GEAR Lab 研究科学家)
> 地点：伯克利
> 原视频：https://www.bilibili.com/video/BV1tNGq6mEug

## 一、背景与动机

### 核心挑战：让人形机器人移动并有用

- 人形机器人的优势：能使用人类工具、进入人类空间
- 但让人形机器人**稳定移动和执行有用任务**仍是一个未完全解决的问题
- 演讲者从 2021-2022 年开始探索人形机器人控制，经历从"人类视觉伺服"到"物理仿真"的演进

### 行为基础模型（Behavior Foundation Model, BFM）的定义

- 行为基础模型 = 一个基础模型，用于人形机器人与动态环境交互
- 与 VLA（Vision-Language-Action）的区别：BFM 侧重**控制层面**（系统一/系统零），解决 bipedal 和 quadruped 的控制问题
- 系统分层：
  - **系统零**：底层运动控制（最近的新研究方向）
  - **系统一**：机械智能/运动技能
  - **系统二**：高级推理/规划
- BFM 的目标：**零样本（zero-shot）** 执行多种行为，无需为每个任务重新训练

---

## 二、BFM-0：无监督 RL 行为基础模型

> 与 Meta FAIR Lab 合作，基于 Forward-Backward (FB) 表征

### 2.1 核心思想：用奖励函数直接控制

- BFM-0 的接口是**奖励函数（reward function）**
- 用户只需编写一个奖励函数，描述期望的行为（如"胸部保持在某个高度"、"以某速度侧走"），策略就能自动执行
- 这是"魔法"级别的能力：不需要重新训练策略，只需在测试时指定新奖励

### 2.2 FB（Forward-Backward）表征

**核心组件：**

- **Forward Representation F(s, a, z)**：从前向角度学习，预测从状态-动作对出发的未来访问分布
- **Backward Representation B(s)**：从后向角度学习，仅依赖状态，映射到 forward 的 latent space
- **Latent Task Embedding Z**：任务的隐式编码，定义在奖励空间
- **Successor Measure**：基于测度论，表示访问概率

**关键公式：**

Q 函数通过 FB 分解为：
$$Q(s, a, z) = F(s, a, z)^\top B(s)$$

进一步，Z 可分解为：
$$Z_R = \mathbb{E}_{p(s)}[B(s)] \cdot R$$

其中 R 是奖励函数。这意味着：
- 只要掌握 F 和 B，就能在任何奖励函数下计算 Q 函数
- **策略条件化在 Z 上**：$\pi(a|s, z)$

### 2.3 无监督 RL 的本质

BFM-0 训练时：

- **不需要奖励函数**：训练阶段只学习 F 和 B（无监督），不定义任何任务
- **不需要终止条件**：除了超时，没有 episode 终止
- 训练初期，人形机器人只是在地上"扑腾"（flopping），随机探索状态空间
- 通过探索，策略学会状态转移，建立了丰富的 latent 表征

**为什么能在无监督下学到有用行为？**

- 人形机器人的状态空间极其巨大，但"类人状态"的空间很小
- 需要加入**运动捕捉数据**和**判别器（discriminator）**（类似 GAN/AMP），将策略引导向类人运动区域
- 训练几小时后，策略开始学会站立——因为"站立"是判别器偏好的状态

### 2.4 训练细节

- **Off-Policy**：使用 DDPG/TD3 等 Q-learning 算法
- 三个目标混合优化：
  1. **FB loss**：无监督学习 forward/backward
  2. **Style reward（判别器）**：让动作看起来像人类
  3. **Regularization reward**：Sim2Real 约束（避免自碰撞、限制加速度等）
- 使用 Online Buffer 获取最新状态

### 2.5 能力与限制

**能力：**
- 目标到达（Goal Reaching）
- 运动跟踪（Motion Tracking）
- 奖励优化（Reward Optimization）
- **出色的失败恢复**：从地面站起非常自然
- **平滑过渡**：从当前状态到目标 latent code 的过渡非常平滑

**限制：**
- **精度不够高**：无法超越专门的 motion tracker
- 不适合精确运动控制
- 要从研究到生产，还需要加入 motion tracking reward 等额外组件

### 2.6 Bingo Card 总结

- Off-Policy
- Unsupervised RL（核心）
- 无终止条件
- 学习丰富的 latent 表征
- 支持 latent space 中的 fine-tuning 和 adaptation
- 鲁棒的失败恢复

---

## 三、SONIC：规模化运动跟踪

> NVIDIA GEAR Lab 最新工作，将 motion tracking 扩展到极致

### 3.1 设计动机

- Motion tracking 是人形机器人控制的**超集（superscalar）**：
  - 如果能让机器人复现人类动捕的所有动作，就获得了非常有用的策略
  - 支持**遥操作（teleoperation）**：这是构建 VLA/机器人基础模型的核心数据采集手段
  - 行为克隆需要人形机器人执行有趣任务的数据，motion tracking 是实现这一点的关键

### 3.2 规模化三要素

**数据：**
- **700 小时**高质量运动捕捉数据（NVIDIA 内部游戏数据集）
- 7 亿帧，35 万条运动序列
- 极其多样化：倒地、手势、动态跳跃、运动、局部移动等

**计算：**
- 出人意料的发现：**更多 GPU 不只是训练更快，而是得到更好的策略**
- 8 GPU vs 64 GPU 有**质变**差异（不仅仅是速度差异）
- 更多并行环境 → 策略质量提升

**模型：**
- 更大的网络容量 → 能容纳更多运动模式
- 数据、计算、模型三者需要**同时扩展**才能获得最佳效果

### 3.3 通用 Token 隐空间（Universal Token Latent Space）

**核心创新：** 学习一个共享的隐空间，容纳多种输入模态

**三种编码器：**

| 编码器 | 输入 | 用途 |
|--------|------|------|
| **Robot Motion Encoder** | 机器人关节运动（来自 VR/手柄生成） | 标准 motion tracking |
| **Human Motion Encoder (SMPL)** | 人体运动捕捉数据 | 直接人体→机器人，无需 retargeting |
| **Hybrid Encoder** | VR 三点 + 下半身规划 | 上半身快速运动 + 下半身控制 |

- 三种编码器的输出被**量化到同一个 token latent space**
- 共享同一个解码器
- 在 latent space 中，人体运动、机器人运动、遥操作信号**可互换**

**关键突破：无需 Retargeting**

- 传统方法：人体动捕 → retargeting（运动学重定向）→ 机器人关节
- SONIC：人体动捕**直接输入** human motion encoder → latent tokens → 机器人动作
- 策略在训练时学习隐式 retargeting（训练时仍需要配对数据）

### 3.4 交互式运动学规划器（Motion Bricks）

- 名为 **Motion Bricks** 的实时生成式运动模型
- 工作在 latent token 空间上
- 输入：手柄控制（joystick）→ 输出：人形机器人运动序列
- 将其与 SONIC tracker 结合 → 手柄控制机器人执行各种运动（跑步、跳跃、拳击等）
- 本质上是**游戏角色控制**：手柄输入 → 机器人执行对应动作

### 3.5 应用场景

**遥操作（Teleoperation）：**
- **VR 全身遥操作**：VR 头显 + 脚部追踪器 → 人形机器人实时跟随
- **视频遥操作**：通过姿态估计从视频中提取人体运动 → 机器人执行
- **手柄控制**：通过游戏手柄 + 运动学规划器控制机器人

**数据采集闭环：**
- 遥操作采集数据 → 训练 VLA/基础模型 → 机器人自主执行任务
- 展示了用全身遥操作采集 pick-and-place 数据，fine-tune GR00T 1.5 模型

**多模态生成：**
- Text-to-Motion：文本 → 人体运动生成 → SONIC → 机器人执行
- 理论上可以接入任何人体运动生成模型

### 3.6 训练细节

- **On-Policy**：使用 PPO 优化
- **Supervised RL**：运动跟踪作为监督信号
- 正在准备开源发布

---

## 四、行业影响：Figure Helix 02

- Figure 公司的 Helix 02 展示中，机器人使用**全身运动**（包括用臀部关抽屉）
- 演讲者确认：**这背后是 motion tracking 技术驱动的**
- Figure 使用了 1000 小时的数据，进一步放大了规模化效果
- 这表明 motion tracking 技术正在从学术研究进入**工业生产和创造价值**

---

## 五、Q&A 要点

### BFM-0 无终止条件的影响

- 训练时没有"任务"，只是学习状态转移
- 对于简单的 2D MuJoCo 环境，仅靠随机探索无法覆盖所有状态
- 但对于人形机器人，状态空间巨大，"类人空间"很小
- 需要动捕数据 + 判别器引导策略进入有趣的区域
- 纯随机探索 + 判别器可能永远学不会后空翻（难度太高）→ 需要更好的状态初始化

### 规划与运动生成的关系

- 演讲者过去做分层 RL，但因缺乏运动生成能力而受限
- 现在在 NVIDIA 有运动生成专家团队，可以推进此方向
- **VLA 本质上就是规划器**（对移动操作机器人而言），对人形机器人来说，全身控制规划更困难（全运动学空间）
- **关键缺失环节**：运动学规划器与底层运动 tracker 之间的接口
  - 当前运动学规划器基本是**开环**的，不感知动力学
  - 规划器需要与 tracker **双向通信**：规划器传达意图，tracker 反馈动力学约束
  - 运动学姿态不是好的接口——它不传递动力学信息
  - 需要**更好的 latent 表征**作为规划器与 tracker 之间的通信接口

### 未来方向

- 探索 motion diffusion model 在运动学空间中的潜力
- 构建规划器与 tracker 之间的协同（synergy），而非分离
- 规划器需要具备 dynamics-aware 能力

---

## 六、关键论文与项目

| 项目 | 描述 | 特点 |
|------|------|------|
| **PHC** | Perpetual Humanoid Controller | 早期工作，基于物理仿真的人形控制 |
| **BFM-0** | Behavior Foundation Model 0 | 无监督 RL，FB 表征，奖励函数接口 |
| **SONIC** | 规模化运动跟踪 | 700h 动捕数据，通用 latent space，多编码器 |
| **Motion Bricks** | 实时生成式运动模型 | latent token 上的运动生成，手柄控制 |
| **GR00T 1.5** | NVIDIA 机器人基础模型 | 与 SONIC 配合，遥操作采集数据 → 训练 VLA |

---

## 七、核心洞察

1. **Motion tracking 是规模化人形机器人智能的可行路径**：采集数据 → 学习基础模型 → 自主执行
2. **接口设计是关键问题**：BFM-0 的奖励函数 vs SONIC 的运动参考轨迹，两者各有优劣，未来可能融合
3. **规模化真的有质变**：更多 GPU 不只是更快，而是得到更好的策略（环境多样性带来泛化性）
4. **隐空间作为通用接口**：SONIC 的 universal token latent space 让不同输入模态共享同一控制策略
5. **规划与控制的协同**：当前缺失的一环是 dynamics-aware 的规划器，需要更好的 latent 通信接口