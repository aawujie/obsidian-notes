---
tags:
  - microduck
  - 强化学习
  - PPO
  - mujoco
  - 训练
created: 2026-08-31
---

# Microduck 强化学习 · 环境定义与训练方法详解

> 来源:microduck_rl 源码(`tasks/microduck_velocity_env_cfg.py`、`tasks/mdp.py`、`MicroduckRlCfg`)与 mjlab 模板。任务:`Mjlab-Velocity-Flat-MicroDuck`(速度追踪)。

## 一、环境定义

### MDP 结构

```
状态 s     = 61 维观测(50Hz 决策)
动作 a     = 14 维 = 14 个舵机目标位置(策略输出角度,舵机内部 PD 跟踪)
转移 P     = MuJoCo Warp GPU 仿真(4096 环境并行)
奖励 r     = 16 项加权组合
终止       = time_out / fell_over / out_of_terrain_bounds / nan_state
```

### 观测 61 维

| 槽位 | 维度 | 内容 |
|---|---|---|
| base_ang_vel | 3 | 机身角速度(IMU) |
| projected_gravity | 3 | 投影重力(判断站直) |
| joint_pos | 14 | 关节位置(相对默认姿态) |
| joint_vel | 14 | 关节速度 |
| actions | 14 | 上一步动作(历史) |
| twist command | 3 | 速度命令 [vx, vy, vtheta] |
| head_command | 4 | 头/脖命令 |
| body_command | 6 | 身体姿态命令 |

- Critic 观测 76 维(额外:线速度、脚高、脚离地时间、脚接触力等真值)
- 动作:目标 = 默认姿态 + action × scale(scale=1.0)

### 命令空间

- 速度:vx ∈ [-0.3, 0.3] m/s 等,**固定范围**(不用课程,注释:范围课程会让策略追不上)
- **15% 环境专门练原地转**(lin=0, |ang|∈[0.4,1.0])——独立均匀采样时原地转只占 2% 数据,学不会
- 头命令:neck/head_pitch ±1.1 rad、head_yaw ±1.4、head_roll ±0.31

### 观测噪声

| 观测 | 噪声(均匀) |
|---|---|
| 角速度 | ±0.03 |
| 投影重力 | ±0.01 |
| 关节位置 | ±0.001 |
| 关节速度 | ±0.25 |

IMU 安装误差:每环境 ≤6° 随机旋转(只加在 actor,critic 用真值)。

## 二、奖励 / 惩罚定义

### 正向奖励

| 奖励 | 权重 | 公式/说明 |
|---|---|---|
| track_linear_velocity | +2.0 | `exp(-‖v_cmd-v_actual‖²/σ²)`,σ²=0.1 高斯 |
| track_angular_velocity | +2.0 | 同上,σ²=0.5(转弯放宽) |
| upright | +2.0 | 投影重力高斯,σ²=0.05(收紧过:之前 4° 前倾免费) |
| pose | +1.0 | 关节位置高斯,站立 σ 紧(0.05-0.15)/走路 σ 松(0.25-0.4);仅腿部,头/脖归 head_pose_tracking |
| air_time | +3.0 | 脚离地时间,窗口 [0.125, 0.300]s,**摔倒时归零**(防抖腿 hack) |
| head_pose_tracking | +2.0 | 头部跟踪命令 |

### 惩罚项

| 惩罚 | 权重 | 作用 |
|---|---|---|
| dof_pos_limits | -1.0 | 关节超限 |
| self_collisions | -1.0 | 自碰撞 |
| action_rate_l2 | -0.1 → -1.0(课程) | 动作变化率,1500 iter 内加压 |
| foot_clearance | -2.0 | 离地高度偏离 2cm 目标(防拖脚) |
| foot_swing_height | -0.25 | 摆动脚高度 |
| foot_slip | -0.1 | 打滑(故意弱,强了限制转身) |
| body_ang_vel | -0.05 | 身体角速度 |
| angular_momentum | -0.02 | 角动量 |

body_pose_tracking / head_pose_bias 权重 0——保留观测槽但禁用。

### 设计哲学

1. **正向奖励只给行为本身,惩罚只给坏状态**——防 reward hacking
2. **potential-based shaping**(velstand 的 `upright_progress`、`height_progress`):奖 Δcos(tilt)——向站立移动才给钱,保持给 0;政策不变塑形,不创造新最优
3. **防 hack 是显式工程**:air_time 摔倒归零、fallen_state_penalty 带滞回(倒下才启动、真正站起来才解除)、自碰撞/超限/打滑硬惩罚

### 课程学习(7 项)

| 课程 | 内容 |
|---|---|
| action_rate_weight | -0.1 → -1.0 |
| standing_envs | 站立环境 2% → 25% |
| head_pose_range | 头命令范围 5% → 100% |
| com_range | CoM 随机化 ±3mm → ±8mm |

## 三、训练方法

### 算法

- **PPO**(rsl_rl `RslRlOnPolicyRunner`),on-policy,GAE(λ=0.95)
- 每轮:4096 环境 × 24 步 → 5 epoch × 4 mini-batch 更新
- MuJoCo Warp GPU,dt=0.005s,decimation=4 → 50Hz

### 超参数

| 参数 | 值 |
|---|---|
| learning_rate | 1e-3(adaptive) |
| clip_param / entropy_coef | 0.2 / 0.01 |
| gamma / lam | 0.99 / 0.95 |
| epochs / mini_batches | 5 / 4 |
| desired_kl / max_grad_norm | 0.01 / 1.0 |
| max_iterations | 50,000(1-2h 出可用步态) |
| save_interval | 250 |

### 域随机化(13 字段)

CoM ±3mm(课程到 ±8)、质量惯量 ±5%、关节摩擦 ±10%、armature ±10%、**速度推搡每 3-6s ±0.3 m/s**(原 ±0.5 审计后收紧)、IMU ≤6°、编码器偏置 ±0.86°、初始倾斜 ±10°/±5°、BAM 内电池电压/电压跌落/命令延迟。

### 执行器物理(BAM)

Dynamixel XL330 完整电压控制律:电压控制 + 反电动势 + 库仑/Stribeck/负载摩擦。**BAM 保真度 = sim2real 差距的一半**。

### 命令与流程

```bash
uv run train Mjlab-Velocity-Flat-MicroDuck --env.scene.num-envs 4096   # 需 CUDA
# 无 GPU:加 --hf-jobs 上 Hugging Face 云
```

训练 → 每 250 iter checkpoint + W&B → 选最佳 → `scripts/export.py` 导出 ONNX(归一化烘焙进图,禁止手转)→ 真机 robotd 用 onnxruntime 50Hz 纯推理。

### 一致性保障

- 训练 50Hz = 真机 50Hz;观测/动作契约 61→14 一致
- 训练时**不做动作低通滤波**,部署也不加——两边必须匹配,否则迁移断裂

## 相关笔记

- [[Microduck仿真-快捷键速查]] —— 本地跑仿真/键盘操作
