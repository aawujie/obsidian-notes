---
share_link: https://share.note.sx/lonebfch#KTabc1bxXCLb92pTiJzHaqHEYU7OqdV/btuQZPJ3Xz8
share_updated: 2026-04-09T15:27:53+08:00
---
# 具身智能课程推荐（MuJoCo 仿真）

> 整理时间：2026-04-09
> 关键词：Embodied AI, MuJoCo, Reinforcement Learning, Sim-to-Real, Robot Learning

---

## 一、顶尖大学课程

### 1. CMU 16-831: Introduction to Robot Learning
- **学校**：卡内基梅隆大学 Robotics Institute
- **讲师**：David Held / Guanya Shi
- **内容**：强化学习（model-based/free, on/off-policy, offline）、模仿学习（Behavior Cloning, DAgger, 逆RL）、视觉学习、Sim-to-Real 迁移
- **课件**：https://16-831.github.io/spring25/lectures
- **推荐理由**：CMU 机器人所出品，覆盖机器人学习全链路

### 2. UC Berkeley CS 294-277: Robots That Learn (Spring 2026)
- **讲师**：Jitendra Malik（计算机视觉大牛）
- **内容**：生物运动控制基础 → 机器人运动技能获取范式 → locomotion / navigation / manipulation 案例
- **网站**：http://robots-that-learn.github.io/
- **前置要求**：深度学习 + 强化学习基础

### 3. Stanford CS422: Interactive and Embodied Learning (Winter 2026)
- **内容**：Agent 通过交互学习、内在动机、Model-based RL、多智能体 RL
- **网站**：http://cs422interactive.stanford.edu/

### 4. Stanford XCS224R: Deep Reinforcement Learning（在线付费）
- **形式**：100% 在线、按需学习
- **内容**：Policy Gradient、Actor-Critic、Q-Learning、Model-based RL、Goal-conditioned RL、Meta-RL
- **费用**：$1,950（含证书）
- **网站**：https://online.stanford.edu/courses/xcs224r-deep-reinforcement-learning

### 5. RWTH Aachen: AI for Robotics (Summer 2026)
- **特色**：直接用 MuJoCo 构建完整自主性栈
- **内容**：导航、任务与运动规划 (TAMP)、深度强化学习，第二阶段复现论文
- **网站**：https://ml.rwth-aachen.de/teaching/2026-ss/ai_for_robotics/

### 6. Purdue ME392: Robotics with MuJoCo
- **讲师**：Pranav Bhounsule
- **特色**：专门以 MuJoCo 为教学平台，从零开始教机器人仿真
- **网站**：https://pab47.github.io/mujoco2022.html

### 7. JHU 665.713: Embodied Intelligence: Robotics in Unstructured Worlds
- **内容**：多模态感知、深度学习、生成式 AI、视觉语言导航、具身任务完成
- **网站**：https://ep.jhu.edu/courses/665713-embodied-intelligence-robotics-in-unstructured-worlds

---

## 二、免费开源课程 / 教程

### 8. 🤗 HuggingFace Robotics Course + LeRobot
- **形式**：完全免费、在线自学
- **内容**：经典机器人学 + 现代学习方法，集成 MuJoCo 仿真环境
- **亮点**：
  - ACT（Action Chunking Transformer）策略训练
  - SmolVLA（Vision-Language-Action）模型
  - Colab Notebook 直接运行
- **课程**：https://huggingface.co/learn/robotics-course
- **GitHub**：https://github.com/huggingface/lerobot （22k+ stars）
- **上手**：`pip install lerobot`

### 9. MuJoCo Playground（Google DeepMind）
- **内容**：GPU 加速的机器人学习框架，支持四足 / 双足 / 灵巧手 / 机械臂
- **亮点**：免费 Colab Notebook，可直接训练策略；RSS 2025 最佳 Demo 论文奖
- **GitHub**：https://github.com/google-deepmind/mujoco_playground （1.8k stars）
- **网站**：https://playground.mujoco.org/

### 10. RL Robotic Simulation Tutorials
- **形式**：GitHub 开源教程，三级递进
  - Level 1：基础（表格方法）
  - Level 2：深度 RL（神经网络）
  - Level 3：机器人应用（MuJoCo 环境）
- **技术栈**：Gymnasium + MuJoCo + PyTorch + Stable-Baselines3
- **GitHub**：https://github.com/duncancalvert/rl_robotic_simulation_tutorials

### 11. MuJoCo 具身智能实战（中文·六周制）
- **课程结构**：
  - Week 1-2：MuJoCo 基础 + 高级建模与传感器
  - Week 3-4：强化学习 + 控制理论
  - Week 5-6：多智能体 + Sim-to-Real 迁移
- **实战项目**：
  1. 智能机械臂控制系统（正逆运动学 + PID）
  2. 视觉引导的抓取系统
  3. 强化学习驱动的运动技能
  4. 自适应控制与轨迹优化（MPC）
  5. 多机器人协作系统
  6. Sim-to-Real 迁移验证
- **搜索关键词**：微信搜"MuJoCo具身智能实战"

### 12. 格物具身智能仿真平台
- **特色**：基于 Unity，跨平台（Win/Linux/Mac），无特殊硬件要求
- **包含**：逆运动学、模仿学习、多足机器人例程 + 完整视频教程
- **GitHub**：https://github.com/loongOpen/Unity-RL-Playground

---

## 三、推荐学习路径

| 阶段 | 推荐资源 | 重点 |
|---|---|---|
| **入门** | Purdue ME392 + MuJoCo 官方 Colab | 熟悉 MJCF 模型、物理引擎 |
| **强化学习** | RL Robotic Simulation Tutorials | PPO → SAC 算法实操 |
| **系统学习** | CMU 16-831 / HuggingFace Course | 模仿学习、视觉策略、Sim2Real |
| **前沿实战** | MuJoCo Playground + LeRobot | GPU 训练、零样本迁移、VLA 模型 |

---

## 四、核心技术路径

```
PPO → SAC → 模仿学习 → 分层强化学习
                ↓
    多模态感知融合（视觉 + 本体感知）
                ↓
    连续动作空间控制
                ↓
    领域随机化 → Sim-to-Real 迁移
```

---

## 五、关键开源项目

| 项目 | Stars | 用途 |
|---|---|---|
| [MuJoCo](https://github.com/google-deepmind/mujoco) | 12.5k | 物理仿真引擎核心 |
| [MuJoCo Playground](https://github.com/google-deepmind/mujoco_playground) | 1.8k | GPU 加速训练框架 |
| [LeRobot](https://github.com/huggingface/lerobot) | 22k | 端到端机器人学习库 |
| [mujoco_menagerie](https://github.com/google-deepmind/mujoco_menagerie) | - | 开源机器人模型集合 |
| [Stable-Baselines3](https://github.com/DLR-RM/stable-baselines3) | - | RL 算法工具箱 |
