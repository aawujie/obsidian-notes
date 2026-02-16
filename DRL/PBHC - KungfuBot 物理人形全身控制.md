# PBHC — KungfuBot: 基于物理仿真的人形机器人全身控制

> **论文**: KungfuBot: Physics-Based Humanoid Whole-Body Control for Learning Highly-Dynamic Skills
> **会议**: NeurIPS 2025
> **机构**: 中国电信 TeleAI + 上海交大
> **代码**: [TeleHuman/PBHC](https://github.com/TeleHuman/PBHC)
> **机器人**: 宇树 G1

## 一句话概括

用**多阶段动作处理 + 自适应运动追踪的 RL 策略**，让人形机器人复现功夫、舞蹈等高动态动作，并成功 sim2real 部署到 G1 真机。

---

## 整体架构

```
人类动作（视频/数据集）
    │
    ▼
┌─────────────────────────┐
│  动作处理流水线          │
│  采集→过滤→修正→重定向   │
└───────────┬─────────────┘
            │ 机器人格式动作数据
            ▼
┌─────────────────────────┐
│  RL 策略训练             │
│  IsaacGym 并行仿真       │
│  自适应课程 + 非对称AC   │
└───────────┬─────────────┘
            │ 训练好的策略
            ▼
┌─────────────────────────┐
│  部署                    │
│  MuJoCo Sim2Sim → 真机  │
└─────────────────────────┘
```

---

## 模块一：动作处理流水线

### 1. 动作采集 → SMPL 统一格式

- 来源：视频（GVHMR 提取）、LAFAN、AMASS 等数据集
- SMPL：参数化人体模型，统一表征人体姿态
- 目录：`motion_source/`

### 2. 动作过滤与修正

- 用 IPMAN 过滤物理不合理帧（穿透地面、悬浮等）
- 确保动作满足物理约束
- 目录：`smpl_retarget/motion_filter/`

### 3. 动作重定向 (Retargeting)

核心难点：人体 SMPL 和 G1 机器人的**关节结构、自由度、肢体长度**完全不同。

两条管线：
- **Mink 管线**：基于逆运动学 (IK)
- **PHC 管线**：基于 PHC 论文的方法

难点：
- 自由度不匹配（人体 ~23 关节 × 3 DOF vs 机器人不同数量的铰链关节）
- 关节限位（人能做的动作，机器人关节范围不一定覆盖）
- 物理可行性（力矩限制、接触约束）

目录：`smpl_retarget/`

### 4. 可视化验证

目录：`smpl_vis/`、`robot_motion_process/`

---

## 模块二：RL 策略训练

### 环境层级

```
BaseTask → LeggedRobotBase → LeggedRobotMotionTracking
                            → LeggedRobotGeneralTracking
```

### 核心创新 1：自适应运动追踪（双层优化）

> 这是论文的**第一核心贡献**。

**问题**：高动态动作（功夫踢腿、旋转）训练时，固定精度的跟踪奖励/终止条件要么太松（学不精）要么太紧（训练崩溃）。

**解决**：**Termination Curriculum — 终止阈值课程学习**

```
if 平均存活时间太短 → 放宽终止阈值（说明太难了）
if 平均存活时间足够长 → 收紧终止阈值（可以提更高要求了）
```

- 外层：动态调终止阈值
- 内层：PPO 策略优化
- 本质是**双层优化 (Bi-level optimization)**

**Adaptive Tracking Sigma — 自适应奖励温度**：
- 奖励函数的 sigma 根据跟踪误差 EMA 动态调整
- 误差大 → sigma 大（奖励宽容）；误差小 → sigma 小（奖励敏感）

**Soft Dynamic Correction (SDC) — 软动态修正**：
- 偏离参考动作时，不硬重置，而是把状态**朝参考做软插值**
- 位置/速度线性插值，旋转用 slerp
- alpha 通过课程学习调整：初期强拉回，后期逐渐放手

### 核心创新 2：非对称 Actor-Critic + Teacher-Student

> 这是 **sim2real 的关键**。

| | Actor (可部署) | Critic (仅训练) |
|---|---|---|
| 本体感知 | ✅ 关节角、角速度、IMU | ✅ |
| 未来动作目标 | ✅ 未来 N 步局部目标 | ✅ |
| 全局刚体位置 | ❌ | ✅ |
| 跟踪误差 | ❌ | ✅ |
| 接触力等 | ❌ | ✅ |

三件套机制：
1. **Privileged Encoder**：把特权信息压缩成隐向量（训练时 Actor 用）
2. **History Encoder**：从过去几步本体感知序列估计相同的隐向量（部署时用）
3. **DAgger 蒸馏**：定期用 Privileged Encoder 输出监督 History Encoder，让它学会从历史观测中**隐式估计**特权信息

### 核心创新 3：完整的动作处理流水线

垃圾进垃圾出——数据质量是一切的基础。从视频到可执行动作的完整管线保证了参考数据的物理合理性。

---

## 奖励函数设计

多维度跟踪奖励：
- **全局刚体位置跟踪**：全身关键点与参考动作的 L2 距离
- **关节角度跟踪**
- **Root 位姿跟踪**（位置 + 朝向）
- **速度跟踪**：Radial Velocity Potential

### Radial Velocity Potential

```python
potential = potential_cosine × potential_norm
```

- **方向奖励**：余弦相似度 → `exp(-cosine_error / sigma)`
- **幅度奖励**：归一化速度比 → `ratio × exp(α(1 - ratio^(1/α)))`
- 比简单 L2 距离更适合高动态动作

### 扩展关键点 (Extend Config)

在机器人原有关节基础上定义**虚拟关键点**（手尖、脚尖等），用于更精细的末端跟踪。

---

## 观测空间设计

**局部坐标系**：所有参考动作关键点都转换到**骨盆 (anchor) 的 body frame**。

策略看到的不是"走到世界坐标 (3.2, 1.5)"，而是"右手需要往前方 0.3m、上方 0.5m 移动"——对泛化性和训练稳定性至关重要。

**未来动作前瞻**：策略输入包含未来 N 步参考目标（局部坐标），让策略能提前"准备"高动态动作。

---

## 两种 PPO 实现

### PPO-Mimic

- 非对称 Actor-Critic
- History Encoder + Privileged Encoder + DAgger
- 支持 Teacher-Student 两阶段蒸馏
- 支持 MoE (Mixture of Experts) 网络

### MH-PPO

- 独立 Actor/Critic 架构
- **向量化奖励 (Vec Reward)**：每个奖励分量有独立 Value Head，避免不同量级的奖励互相干扰
- **L2C2 正则化**：在相邻时间步观测之间插值，强制策略输出平滑变化，防止真机抖动
- **Phase-Aware 网络**：用动作相位信息条件化，帮助区分周期动作中相似但不同的姿态

---

## 为什么能做高动态动作？

| 现有方法的失败原因 | PBHC 的解决方案 |
|---|---|
| 动作数据质量差 | 完整处理流水线（采集→过滤→修正→重定向） |
| 固定精度跟踪会崩溃 | 自适应课程：先学"大概对"，再逐步精确 |
| 策略看不到未来 | 未来 N 步动作前瞻 |
| 单一奖励信号不够 | 多维度跟踪奖励 + 向量化 Value 分解 |
| Sim2Real 断层 | 非对称 AC + History Encoder 蒸馏 |

---

## 项目结构

```
PBHC/
├── motion_source/          # 动作数据采集文档
├── smpl_retarget/          # SMPL → 机器人重定向
│   ├── mink_retarget/      # Mink IK 管线
│   ├── phc_retarget/       # PHC 管线
│   └── motion_filter/      # 动作过滤
├── smpl_vis/               # SMPL 可视化
├── robot_motion_process/   # 机器人动作处理与可视化
├── humanoidverse/          # RL 训练核心
│   ├── envs/               # 环境
│   │   ├── motion_tracking/    # 动作跟踪环境
│   │   └── legged_base_task/   # 腿足基础环境
│   ├── agents/             # 算法
│   │   ├── ppo/            # PPO-Mimic
│   │   ├── mh_ppo/         # MH-PPO
│   │   └── modules/        # 网络模块
│   ├── deploy/             # 部署
│   ├── simulator/          # 仿真器抽象层
│   └── config/             # Hydra 配置
├── description/            # SMPL & G1 描述文件
└── example/                # 示例动作数据 + 预训练权重
```

---

## 关键依赖 & 致谢

- **ASAP**: RL 代码基础框架
- **RSL_RL**: PPO 实现
- **IsaacGym**: GPU 并行物理仿真
- **MuJoCo**: Sim2Sim 验证 & 部署
- **GVHMR**: 视频→SMPL 动作提取
- **IPMAN**: 动作物理可行性过滤
- **PHC / MaskedMimic**: 动作重定向管线参考
