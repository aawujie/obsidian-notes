# MuJoCo 零基础入门 — 14 天学习路线图

> **目标**：从零开始掌握 MuJoCo 仿真，能用 Python 建模、控制、训练简单机器人
> **创建日期**：2026-04-29
> **前置条件**：Python 熟练、基本深度学习知识、RL 概念了解
> **核心原则**：先玩起来再看文档，每天跑通能看的代码

---

## 环境准备（Day 0，今天完成）

- [ ] 安装 conda 虚拟环境 `mujoco-learn`
- [ ] `pip install mujoco gymnasium[mujoco] stable-baselines3 pybullet`
- [ ] 验证：`python -c "import mujoco; print(mujoco.__version__)"` 能跑通
- [ ] 验证：`python -c "import gymnasium as gym; env = gym.make('HalfCheetah-v4'); print('OK')"` 能跑通
- [ ] 打开 [Purdue ME392 课程页](https://pab47.github.io/mujoco2022.html)，收藏 + clone 配套代码仓库

---

## Phase 1：看见东西动起来（Day 1-3）

### Day 1 — 第一个仿真 + 理解模型结构

**上午（2h）**：
- [ ] 跑通 HalfCheetah-v4 渲染 demo（5行代码）
- [ ] 跑通 Ant-v4 渲染 demo，对比两个环境的区别
- [ ] 阅读笔记 [[MuJoCo-概览]] 的 "Bodies、Geoms、Sites 的区别" 一节
- [ ] 用 `print(env.observation_space.shape)` 和 `print(env.action_space.shape)` 查看状态/动作维度

**下午（2h）**：
- [ ] Purdue ME392 Video 1：Intro + 环境搭建
- [ ] Purdue ME392 Video 2：Pendulum 建模（MJCF）
- [ ] 跟着写第一个 MJCF 文件：带 1 个 hinge joint 的单摆
- [ ] 用 `mujoco.viewer` 跑自己写的单摆模型，看到它受重力落下

### Day 2 — 理解 model/data + 建复杂模型

**上午（2h）**：
- [ ] Purdue ME392 Video 3：Cart-Pole 建模
- [ ] 阅读笔记 [[MuJoCo-建模]]，重点理解 site/camera/tendon 的用法
- [ ] 自己建一个 cart-pole，添加 actuator（滑块电机），用正弦信号驱动看效果

**下午（2h）**：
- [ ] Purdue ME392 Video 4：Acrobot（双摆）
- [ ] Purdue ME392 Video 5：添加碰撞体（geom 的碰撞属性）
- [ ] 练习：给 acrobot 添加地板，看碰撞效果
- [ ] 尝试修改 geom 的 `friction` 参数，观察滑动的变化

### Day 3 — 传感器 + Python API 深度

**上午（2h）**：
- [ ] 阅读笔记 [[MuJoCo-Python绑定]]，重点理解 Passive Viewer vs Active Viewer
- [ ] 写 Python 脚本：加载 acrobot 模型 → 施加外力 `mjModel.actuator_force` → 用 viewer 实时交互
- [ ] 练习：给模型添加力传感器和位置传感器

**下午（2h）**：
- [ ] 阅读笔记 [[MuJoCo-物理计算]]，重点理解 forward/inverse dynamics 的区别
- [ ] 练习：用 `mj_step1` + `mj_step2` 分步执行，手动在两步之间插入自定义代码
- [ ] **小项目**：建一个带地板的 pendulum，写 Python 程序让它从顶部释放，记录关节角度轨迹，用 matplotlib 画出来

---

## Phase 2：控制接入（Day 4-6）

### Day 4 — PID 控制

**上午（2h）**：
- [ ] 实现 cart-pole 的 PID 控制器：输入 cart 位置误差，输出力
- [ ] 手动调参（Kp、Ki、Kd），让杆立起来至少 5 秒不倒
- [ ] 用 matplotlib 实时画出 cart 位置和杆角度的时间曲线

**下午（2h）**：
- [ ] 实现 pendulum 的 swing-up + PID 平衡控制器（两级控制）
- [ ] 对比：能量控制法（swing-up）settling time vs 纯 PID 的差异
- [ ] 阅读笔记 [[线性二次调节器与代数Riccati方程解析]]（可选，为后续 LQR 做铺垫）

### Day 5 — MuJoCo + Gymnasium 环境

**上午（2h）**：
- [ ] 阅读 [Gymnasium 官方文档 MuJoCo 部分](https://gymnasium.farama.org/environments/mujoco/)
- [ ] 跑通所有 MuJoCo 标准环境：HalfCheetah, Ant, Hopper, Walker2d, Humanoid
- [ ] 每个环境跑 1000 步随机动作，观察各机器人的运动自由度

**下午（2h）**：
- [ ] 学习如何注册自定义 Gymnasium 环境（基于自己的 MJCF 模型）
- [ ] **小项目**：把 Day 3 建的 acrobot 注册为 Gymnasium 环境
- [ ] 验证：`env = gym.make("MyAcrobot-v0")` 能正常 reset/step

### Day 6 — 位置控制 + 轨迹跟踪

**上午（2h）**：
- [ ] 学习 MuJoCo 的 position actuator（伺服电机）：`position`、`kp`、`kv` 参数
- [ ] 实现机械臂的轨迹跟踪：定义一组 waypoints → 每个 joint 用 PD 跟踪目标角度
- [ ] 用 viewer 实时观察机械臂末端轨迹

**下午（2h）**：
- [ ] 实现简单的阻抗控制（impedance control）demo
- [ ] 对比 position control vs torque control 的差异和适用场景
- [ ] 阅读笔记 [[模型预测控制（MPC）入门与核心原理]]（为后续做准备）

---

## Phase 3：RL 接入（Day 7-10）

### Day 7 — 用 Stable-Baselines3 训练第一个 RL agent

**上午（2h）**：
- [ ] 安装 SB3：`pip install stable-baselines3[extra] tensorboard`
- [ ] 用 PPO 训练 HalfCheetah-v4，10 万个 timestep（约 5 分钟）
- [ ] 用 `tensorboard --logdir ./ppo_halfcheetah_tensorboard/` 查看训练曲线

**下午（2h）**：
- [ ] 加载训练好的模型，用 viewer 观察效果
- [ ] 对比：随机动作 vs 训练后 PPO 策略的区别
- [ ] 阅读笔记 [[从零实现PPO：11个关键工程化细节与实践指南]]

### Day 8 — PPO 深入 + SAC

**上午（2h）**：
- [ ] 用 PPO 训练 Ant-v4（100 万 timestep，约 20 分钟）
- [ ] 修改 PPO 超参数（learning rate、n_steps、batch_size），观察对收敛速度的影响
- [ ] 用 SAC 训练同样的环境，对比 PPO vs SAC 的效果

**下午（2h）**：
- [ ] 学习 [RL Robotic Simulation Tutorials](https://github.com/duncancalvert/rl_robotic_simulation_tutorials) Level 1-2
- [ ] 阅读笔记 [[DDPG与TD3深度强化学习算法详解 - L13]]
- [ ] **小项目**：在自己注册的 acrobot 环境上用 PPO 训练，看 RL 能不能学会荡起来

### Day 9 — MuJoCo Playground（GPU 加速训练）

**上午（2h）**：
- [ ] Clone [mujoco_playground](https://github.com/google-deepmind/mujoco_playground)
- [ ] 跑通 Go1 四足机器人的 locomotion 训练 Colab
- [ ] 理解 ManiBERT / teacher-student distillation 的基本概念

**下午（2h）**：
- [ ] 在 MuJoCo Playground 里训练双足机器人 (H1/G1) 站立和行走
- [ ] 理解 domain randomization 在 playground 中的配置方式
- [ ] 阅读笔记 [[具身智能课程推荐（MuJoCo）]] Phase 4 的 Sim-to-Real 部分

### Day 10 — 从 simulation 到自己的任务

**上午（2h）**：
- [ ] 定义自己的 RL 任务：设计 reward function（如 "让四足机器人按指定方向走"）
- [ ] 在 MuJoCo Playground 中修改 reward 配置，重新训练
- [ ] 对比新旧 reward 下机器人行为的差异

**下午（2h）**：
- [ ] 阅读笔记 [[Unitree G1 WBT Dataset 调研报告]]
- [ ] 了解 mujoco_menagerie 里的 Unitree 模型（H1、G1、Go2）
- [ ] 跑通一个 Unitree 模型的仿真 demo

---

## Phase 4：项目实战（Day 11-14）

### Day 11 — 项目选题 + 建模

**上午（2h）**：
- [ ] 从以下项目选一个方向（或自己定义）：
  1. **机械臂抓取**：3-DOF 机械臂 + 物块，视觉引导抓取
  2. **双足步行**：基于 Unitree G1 模型训练 walking policy
  3. **倒立摆**：cart-pole 用 RL + LQR 对比控制效果

**下午（2h）**：
- [ ] 设计项目用的 MJCF 模型（从零写或基于 mujoco_menagerie 修改）
- [ ] 添加必要的传感器（IMU、力传感器、触摸传感器）
- [ ] 定义观测空间和动作空间

### Day 12 — 训练 + 调参

**上午（2h）**：
- [ ] 编写训练脚本：环境注册 → PPO/SAC → TensorBoard 监控
- [ ] 首轮训练（至少 50 万 timestep）
- [ ] 分析训练曲线，识别问题（reward 不收敛？抖动？）

**下午（2h）**：
- [ ] 常见问题诊断：
  - reward 不收敛 → 检查 reward shaping 是否合理
  - 动作抖动 → 加 action penalty / smoothness reward
  - 提前终止 → 检查 termination condition 是否过严
- [ ] 迭代调参至少 3 轮

### Day 13 — 评估 + 可视化

**上午（2h）**：
- [ ] 录制训练过程的视频（用 `gymnasium.wrappers.RecordVideo`）
- [ ] 画训练曲线：episode reward / success rate / episode length
- [ ] 对比 baseline（随机策略 / PID 控制器）

**下午（2h）**：
- [ ] 写项目总结笔记，放到 `4.Robot/` 下
- [ ] 包含：任务描述、MJCF 结构、reward 设计、训练曲线、视频链接
- [ ] 记录踩坑清单（哪些参数需要调、什么 trick 管用）

### Day 14 — 回顾 + 下一步

**上午（2h）**：
- [ ] 回顾全部 MuJoCo 笔记（概览/建模/物理计算/Python绑定），补充实战中遇到的新理解
- [ ] 整理"MuJoCo 常见坑"清单（timestep 选择、碰撞参数调优、solver 选择）
- [ ] 更新 `4.Robot/index.md`，添加新写的笔记链接

**下午（2h）**：
- [ ] 确定下一步学习方向（三选一）：
  1. **人形机器人全身控制** → 继续 [[人形机器人全身控制-核心知识点]] + PBHC 笔记
  2. **Sim-to-Real 迁移** → HuggingFace LeRobot + 领域随机化
  3. **MPC + RL 融合** → [[MPC与强化学习的差异、互补及结合路径 - L16]]
- [ ] 制定下一阶段学习计划

---

## 每日固定动作

每天学习结束后：
- [ ] 在 `0.DailyTask/2026/` 下写当日学习日志（5 分钟）
- [ ] 回答三个问题：
  1. 今天最关键的 1 个收获是什么？
  2. 今天卡在哪里？怎么解决的？
  3. 明天最重要的 1 件事是什么？

---

## 参考资源速查

| 资源 | 用途 | 时机 |
|------|------|------|
| [Purdue ME392](https://pab47.github.io/mujoco2022.html) | MJCF 从零建模 | Day 1-3 |
| [[MuJoCo-概览]] | 概念速查 | 全程 |
| [Gymnasium MuJoCo](https://gymnasium.farama.org/environments/mujoco/) | 标准环境列表 | Day 5-8 |
| [SB3 文档](https://stable-baselines3.readthedocs.io/) | PPO/SAC API | Day 7-12 |
| [MuJoCo Playground](https://github.com/google-deepmind/mujoco_playground) | GPU 训练 | Day 9-10 |
| [mujoco_menagerie](https://github.com/google-deepmind/mujoco_menagerie) | 开源机器人模型 | Day 10-11 |
| [[具身智能课程推荐（MuJoCo）]] | 进阶课程索引 | Day 14+ |

---

## 学习原则提醒

1. **先跑代码，再看文档** — 看到机器人动了才有动力继续
2. **每天必须有可运行的产出** — 不追求完美，追求迭代
3. **遇到报错不卡壳** — 15 分钟解决不了就跳过，先推进进度
4. **Phase 1-2 必须动手写** — 复制粘贴无效，自己敲出来才理解
5. **Phase 3 可以改参数跑** — RL 调参本身就是学习过程
