---
title: MuJoCo 物理计算
type: summary
created: 2026-04-28
updated: 2026-04-28
sources: [https://mujoco.readthedocs.io/en/stable/computation/index.html]
tags: [MuJoCo, 物理引擎, 仿真, 约束求解, 凸优化]
---

# MuJoCo 物理计算（Computation）

## 核心符号

| 符号 | 大小 | 含义 | MuJoCo 字段 |
| --- | --- | --- | --- |
| $n_q$ | 位置坐标数 | | `mjModel.nq` |
| $n_v$ | 自由度数 | | `mjModel.nv` |
| $n_c$ | 活跃约束数 | | `mjData.nefc` |
| $q$ | $n_q$ | 关节位置 | `mjData.qpos` |
| $v$ | $n_v$ | 关节速度 | `mjData.qvel` |
| $\tau$ | $n_v$ | 施加力（被动+驱动+外部） | `qfrc_passive + qfrc_actuator + qfrc_applied` |
| $c(q,v)$ | $n_v$ | 偏置力（Coriolis+离心+重力） | `mjData.qfrc_bias` |
| $M(q)$ | $n_v \times n_v$ | 关节空间惯量矩阵 | `mjData.qM` |
| $J(q)$ | $n_c \times n_v$ | 约束 Jacobian | `mjData.efc_J` |
| $r(q)$ | $n_c$ | 约束残差 | `mjData.efc_pos` |
| $f(q,v,\tau)$ | $n_c$ | 约束力 | `mjData.efc_force` |

## 运动方程

连续时间下的通用运动方程：

$$M \dot{v} + c = \tau + J^T f$$

Jacobian $J$ 映射关节坐标到约束坐标：$Jv$ 为约束空间速度，$J^T f$ 为关节空间力。

一旦约束力 $f$ 已知，正/逆动力学完成：

$$\begin{aligned} \text{forward:} & & \dot{v} &= M^{-1} (\tau + J^T f - c) \\ \text{inverse:} & & \tau &= M \dot{v} + c - J^T f \end{aligned}$$

## 软接触模型（Soft Contact Model）

### 为何软接触

MuJoCo 放弃严格 complementarity（LCP 核心假设），理由：
1. **物理真实**：所有材料都有变形。软接触下 complementarity 必须违反（穿透时法向力和速度同时为正）。
2. **计算效率**：LCP + 摩擦 = NP-hard。凸优化有完善优势。实践中 10 次 PGS 扫掠即可充分收敛。
3. **连续时间**：模型定义在连续时间（力/加速度），适合控制理论和高级数值积分。
4. **逆动力学**：soft contact 使逆动力学可计算。逆动力学比正动力学容易（优化问题对角化，分解为独立接触问题，可解析求解）。

## 驱动模型（Actuation Model）

MuJoCo 驱动为 SISO（单入单出）。每个驱动器 $i$：
- 输入：控制信号 $u_i$（`mjData.ctrl`）
- 输出：标量力 $p_i$（`mjData.actuator_force`）
- 可选激活状态 $w_i$（`mjData.act`），使系统升为三阶

三个组件：

### 1. Transmission（传动）

标量长度 $l_i(q)$，其梯度 $\nabla l_i$ 为力臂，映射标量力到关节力。

| 类型 | 说明 |
| --- | --- |
| **joint** | 施加力/扭矩到目标关节 |
| **tendon** | 施加力到腱 |
| **jointinparent** | 旋转在父坐标系中测量（ball/free 关节专用） |
| **slider-crank** | 直线力→扭矩（如活塞发动机曲柄） |
| **site** | 在 site 坐标系施加 Cartesian 力/扭矩（喷射器/螺旋桨） |
| **site + refsite** | 参考 site 坐标系的 Cartesian 末端控制 |
| **body** | 施加力到体接触点（真空抓手/生物粘附） |

### 2. 激活动力学（Activation Dynamics）

驱动器内部动态状态 $w$，一阶动力学：

$$\dot{w}_i (u_i, w_i, l_i, \dot{l}_i)$$

| 激活类型 | 公式 |
| --- | --- |
| **integrator** | $\dot{w}_i = u_i$ |
| **filter** | $\dot{w}_i = (u_i - w_i)/t$（Euler 积分） |
| **filterexact** | 解析积分，$t < h$ 稳定 |
| **muscle** | 肌肉特定的非线性滤波 |

`actearly="true"` 使力基于 $w_{i+1}$ 计算，减少一步延迟。

### 3. 力生成（Force Generation）

力对激活/控制是仿射的：

$$p_i = (a w_i \text{ 或 } a u_i) + b_0 + b_1 l_i + b_2 \dot{l}_i$$

可通过参数化实现：直接力控制、位置伺服、速度伺服。

总关节空间力：

$$\sum_i \nabla l_i(q) \; p_i(u_i, w_i, l_i(q), \dot{l}_i(q, v))$$

## 被动力（Passive Forces）

仅依赖位置和速度，不依赖控制/加速。存储于 `mjData.qfrc_passive`，物理意义上不增加能量（用户回调可打破此约束）。

三类：
1. **弹簧-阻尼**（关节和腱）
2. **重力补偿**（`body/gravcomp`）
3. **流体力学**（Fluid forces）

### 多项式力

非线性刚度（关节/腱）和阻尼用多项式 $f$（阶数 mjNPOLY+1），实际力为 $-f$。

$$\begin{aligned} \text{刚度:} & & f(x) &= a x + b x^2 + c x^3 + \dots \\ \text{阻尼:} & & f(v) &= a v + b v|v| + c v^3 + \dots \end{aligned}$$

阻尼多项式使用反对称化（$v^2 \to v|v|$），以保持奇函数。系数需满足符号保持条件 $z \cdot f(z) \geq 0$。

## 数值积分（Numerical Integration）

### 积分器类型

| 积分器 | 特点 |
| --- | --- |
| **Euler** | 半隐式 Euler + 隐式关节阻尼 |
| **implicit** | 隐式速度（含 Coriolis/离心） |
| **implicitfast** | 快速隐式速度（不含 RNE 导数，对称化 $D$）☆推荐 |
| **RK4** | 四阶 Runge-Kutta（保守系统最优） |

### implicit-in-velocity Euler

速度为未知的非线性方程，用 Newton 法一阶展开：

$$v_{t+h} = v_t + h a(v_{t+h}) \approx v_t + h a_t + h M^{-1}D \cdot (v_{t+h}-v_t)$$

解得：

$$v_{t+h} = v_t + h \widehat{M}^{-1} M a_t, \quad \widehat{M} = M - hD$$

### Midpoint 积分（自由体旋转）

对自由体旋转动力学使用中点方法，保守动能和角动量（二次第一积分），是辛积分器。仅在无子体的自由体上应用。

## 约束模型（Constraint Model）

### 约束类型

| 类型 | 说明 | 维度 |
| --- | --- | --- |
| **Equality** | $r(q) = 0$，可微分标量/向量函数 | $\dim(r)$ |
| **Friction loss** | 干摩擦，力上限约束 | 1/3/6 |
| **Limit** | 关节/腱限位，单边不等式 | 1/2 |
| **Contact** | 接触（法向力+摩擦+扭转+滚动） | condim |

### Contact 维度 condim

| condim | 含义 | 椭圆锥 | 金字塔锥 |
| --- | --- | --- | --- |
| 1 | 无摩擦接触 | 1 | 1 |
| 3 | 摩擦接触（法向+切向） | 3 | 4 |
| 4 | + 扭转摩擦 | 4 | 6 |
| 6 | + 滚动摩擦 | 6 | 10 |

### 摩擦锥

椭圆锥：
$$\mathcal{K} = \left\{ f \in \mathbb{R}^n : f_1 \geq 0, f_1^2 \geq \sum_{i=2}^n {f_i^2 / \mu_{i-1}^2} \right\}$$

金字塔锥：
$$\mathcal{K} = \left\{ f \in \mathbb{R}^{2(n-1)} : f \geq 0 \right\}$$

## 约束求解器（Constraint Solver）

### 数学模型

### Primal Problem（Gauss 最小约束原理推广）

$$(\dot{v}, \dot{\omega}) = \arg \min_{(x,y)} \|x-M^{-1}(\tau-c)\|^2_M + \|y-\ar\|^{\text{Huber}(\eta)}_{R^{-1}}$$

约束条件：$J_\mathcal{E} x_\mathcal{E} - y_\mathcal{E} = 0$, $J_\mathcal{F} x_\mathcal{F} - y_\mathcal{F} = 0$, $J_\mathcal{C} x_\mathcal{C} - y_\mathcal{C} \in \mathcal{K}^*$

- $R > 0$：对角正则化器（使约束软化）
- $\ar$：约束空间参考加速度（弹簧-阻尼稳定化，类似 Baumgarte stabilization）
- Huber norm：用于 friction loss 的区间约束

### Augmented Dynamics

增加形变状态 $(z, \omega)$ 形成增广系统：

$$\begin{aligned} M \dot{v} + c &= \tau + J^T f \\ \dot{\omega} &= \ar - R f \end{aligned}$$

### Dual Problem（对偶问题）

$$f = \arg\min_\lambda \frac{1}{2} \lambda^{T} (A+R) \lambda + \lambda^T (\au - \ar) \quad \text{s.t.} \; \lambda \in \Omega$$

其中：
- $A = J M^{-1} J^T$：约束空间逆惯量
- $\au = J M^{-1} (\tau-c) + \dot{J} v$：约束空间无约束加速度
- $\Omega$：约束集（equality 无约束，friction loss 区间约束，contact 在摩擦锥内）

**关键性质**：逆动力学中 $A$ 矩阵完全抵消！对偶问题对角化，分解为独立标量约束，可解析求解。

### 求解算法

| 算法 | 收敛 | 特点 |
| --- | --- | --- |
| **Newton**（默认） | 二次 | Cholesky 分解 Hessian，rank-1 增量更新 |
| **CG** | 线性 | Polak-Ribière-Plus，精确线搜索 |
| **PGS** | 亚线性-线性 | 逐分量更新，顺序更新破坏对称性 |

**推荐**：Newton + 极小 tolerance（如 1e-10）+ elliptic cones + 大 impratio。

### NoSlip 求解器

后处理步骤：对摩擦维度重解 $R=0$（硬约束），抑制软模型固有滑移。但不再求解单一优化问题，可能不稳定。

### Warmstart

从上一时步的约束力热启动，与零力解比较成本，取成本低者初始化。

## Constraint Islands（约束岛）

以 kinematic tree 为顶点、约束为边构成图。独立子图（岛）可分别求解：

- 不同岛所需迭代数不同，避免过度求解
- 无约束 DOF 完全跳过
- 岛间可多线程并行

## 求解器参数

关键参数 $d$（impedance）、$k$（stiffness）、$b$（damping）：

约束空间动力学：
$$\ac + d \cdot (b v + k r) = (1 - d)\cdot \au$$

- $d \in (0,1)$：约束强度，$d \to 0$ 弱约束，$d \to 1$ 强约束
- $k, b$：由 `solref` 属性控制（两种格式：`(timeconst, dampratio)` 或直接 `(-stiffness, -damping)`）
- $d(r)$：由 `solimp` 属性控制位置依赖形状（5 参数：$d_0, d_{width}, width, midpoint, power$）

## 碰撞检测（Collision Detection）

两步：**生成** + **过滤**

### 生成
- Broad-phase：改进 sweep-and-prune（选主成分轴排序）
- Mid-phase：AABB 包围盒层次树（BVH）
- 显式 `exclude` 排除体对

### 过滤
1. 碰撞函数存在且非 NULL
2. 包围球测试（含 margin）
3. 不能同体、不能父子（除非父为 world）
4. `contype & conaffinity` 兼容性

### 窄相碰撞
- 原始体：analytic colliders
- 网格：convex hull（qhull 库）
- **Native CCD**（默认）：GJK/EPA 算法
- **libccd**（遗留）：MPR 算法
- 支持 multiccd（一对接返回多点，如盒-盒 8 点）

## Sleeping Islands

性能优化：将静止的可动单元暂时从管线移除：
- 最大速度 < 阈值 持续 mjMINAWAKE 步 → 标记 "ready to sleep"
- 被醒着的树接触时自动唤醒
- 最大的加速来自减少接触数

## 仿真管线总结

| 阶段 | 函数 |
| --- | --- |
| **Position** | `mj_kinematics` → `mj_comPos` → `mj_tendon` → `mj_makeM` → `mj_factorM` → `mj_collision` → `mj_makeConstraint` → `mj_transmission` |
| **Velocity** | `mj_fwdVelocity` → `mj_comVel` → `mj_passive` → `mj_referenceConstraint` → `mj_rne` |
| **Control** | `mjcb_control` |
| **Force/Accel** | `mj_fwdActuation` → `mj_fwdAcceleration` → `mj_fwdConstraint` → integrator |

顶层函数：
- `mj_step`：完整管线（1-26 步）
- `mj_forward`：仅 2-23 步（连续时间正动力学）
- `mj_step1` + `mj_step2`：分为两阶段（允许控制器介入）

## 可导性与逆动力学

整个管线理论上可微。当前提供两个有限差分函数：
- `mjd_transitionFD`：离散时间状态/控制转移 Jacobian
- `mjd_inverseFD`：连续/离散时间逆动力学 Jacobian

## 引用

主要理论基础：
- E. Todorov (2014). Analytically-invertible dynamics with contacts and constraints: Theory and implementation in MuJoCo
- Featherstone (2008). Rigid Body Dynamics Algorithms
- 约束模型源于 Gauss principle 的推广（Udwadia & Kalaba 1992, Redon et al. 2002, Anitescu 2006）
