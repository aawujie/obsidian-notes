---
title: MuJoCo 建模
type: summary
created: 2026-04-28
updated: 2026-04-28
sources: [https://mujoco.readthedocs.io/en/stable/modeling.html]
tags: [MuJoCo, MJCF, 建模, XML, 物理仿真]
---

# MuJoCo 建模（Modeling）

## MJCF 与 URDF

MuJoCo 支持两种模型格式：
- **MJCF**：原生 XML 格式，功能完整
- **URDF**：通用但功能有限

MJCF 结合了建模格式与编程语言特性，内置编译器自动完成复杂计算。类似 CSS 的默认设置机制使模型文件短小可读。

### 加载与编译

```
MJCF/URDF XML → TinyXML 解析 → DOM → mjSpec → 编译器 → mjModel
```

- 顶层元素：`<mujoco>`（MJCF）或 `<robot>`（URDF）
- 编译过程多步错误检查（parser 结构检查 + compiler 语义检查）
- 编译速度极快（< 1 秒，不含大网格/驱动长度范围计算）
- `Ctrl+L` 可在 simulate 中重载模型

### 保存模型

- `mj_saveModel`：保存为 MJB 二进制（自包含，加载更快）
- `mj_saveLastXML`：保存为 MJCF 规范子集（不保留原始结构但语义等价）

## 核心机制

### Kinematic Tree（运动学树）

- 嵌套 `body` 元素形成 XML 树
- 顶层体为 `worldbody`
- Joint 在体内创建运动自由度，不连接父子（与 URDF 不同）
- 无 joint 的体 = welded to parent
- 单体内可含多个 joint（无需 dummy body 创建复合关节）

### Default Settings（默认设置）

MJCF 支持**无限数量的 defaults class**，嵌套继承：

1. 每 class 有完整 dummy 元素集合
2. 子 class 继承父 class 所有属性值，可覆盖
3. 顶层 class（默认名 "main"）初始化为内部默认值
4. 实际元素创建时，从活动 class 复制属性

**激活规则**（优先级从高到低）：
1. 元素指定 `class` → 使用该类
2. 祖先 body 指定 `childclass` → 使用最近的
3. 否则 → 使用顶层 class

**注意**：属性一旦在 class 中定义就不能回到 undefined。Actuator 与 shortcuts 交互有特殊规则。

### Coordinate Frames（坐标框架）

所有运动学树元素位置/方向均为局部坐标。

**方向指定**五种方式（最多用一个，否则编译报错）：
- `quat`：四元数（推荐，直接使用）
- `axisangle`：$(x,y,z,angle)$，轴角表示
- `euler`：三轴欧拉角，序列由 `compiler/eulerseq` 决定
- `xyaxes`：X 轴 + Y 轴（自动正交化）
- `zaxis`：Z 轴方向（最小旋转映射）

`compiler/angle` 控制角度单位为度或弧度。

### Solver Parameters（求解器参数）

#### solimp（Impedance）

约束阻抗 $d(r)$：5 参数 `(d0, d_width, width, midpoint, power)`。

- $d(0) = d_0$，$d(\text{width}) = d_{\text{width}}$
- midpoint、power 控制 sigmoid 插值形状
- **可微性**：要完全光滑需 $d_0=0$ (`solimp[0]=0`)

#### solref（Reference）

两种格式：
- **正值** `(timeconst, dampratio)`：默认。`timeconst` 控制软硬度（越大越软），`dampratio=1` 临界阻尼
- **负值** `(-stiffness, -damping)`：直接格式。灵活，推荐用于系统辨识

时步约束：`timeconst` 至少为时步 2 倍。

#### Friction 特殊规则

- $r \equiv 0$，故 impedance 恒为 $d_0$（sigmoid 形状参数无效）
- 刚度 $k$ 恒为 0（一阶动力学，纯指数衰减）
- solref 中 dampratio 被忽略，damping 直接用
- $d_{\text{width}}$ 仍影响 $b$ 的缩放

### Contact Parameters（接触参数合并规则）

不同 geom 的接触参数冲突时：

| 参数 | 合并规则 |
| --- | --- |
| condim | 高 priority 的用其值；同 priority 用 max |
| friction | 高 priority 的用其值；同 priority 用逐元素 max |
| margin / gap | 求和（无视 priority） |
| solref / solimp | 高 priority 用其值；同 priority 按 solmix 加权平均 |

**solref 例外**：若任一侧为直接格式（非正），则用逐元素 min。

### Contact Override（接触覆盖）

通过 `option/o_margin`, `o_solref`, `o_solimp` 在运行时覆盖所有接触参数，用于：
- 交互式实验
- 数值优化中的 continuation methods（早期让接触远距离感知以帮助梯度，后期收紧）

## 执行器（Actuators）

### Group Disable（组禁用）

通过 `mjOption.disableactuator` 位域运行时切换执行器组。例如同一模型定义 torque-control 和 position-control 两组执行器，运行时切换。

### Actuator Shortcuts

便捷元素（`motor`, `position`, `velocity`, `intvelocity`, `damper`, `cylinder`, `muscle`, `adhesion`, `dcmotor`）均为 `general` 的语法糖，内部转换为 `general` 参数。

**与 defaults 的交互**：每个 defaults class 只有一个 `general` 元素，shortcuts 按处理顺序覆盖其属性。建议保持 defaults class 和实际元素使用相同 shortcut 类型。

### Force Limits（力限制）

三种钳制方式，可组合使用：

1. **ctrlrange**：钳制控制输入
2. **forcerange**：钳制执行器输出力
3. **joint/actuatorfrcrange**：钳制传入关节的力（多执行器作用于同关节时有用）
4. **tendon/actuatorfrcrange**：钳制传入腱的力

### Length Range（长度范围）

`mjModel.actuator_lengthrange` 是近似值，用于肌肉建模。三种设置方式：
1. 显式 `lengthrange` 属性
2. 从关节/腱限制复制
3. 自动计算（修改的物理仿真，无接触/重力/被动力的阻尼推进）

### Stateful Actuators

#### 积分速度执行器（intvelocity）

位置执行器 + 积分器耦合：控制信号是位置设定点的速度。需钳制激活状态（`actrange`）防止积分超关节限位。

## 肌肉模型（Muscles）

### 核心参数

- $L_T$：生物肌腱长度（假设不可伸缩）
- $L_0$：肌肉最佳静止长度
- $F_0$：峰值零速主动力
- 缩放操作范围：默认 `range="0.75 1.05"`

### FLV 函数

$$\text{FLV}(L, V, \text{act}) = F_L(L) \cdot F_V(V) \cdot \text{act} + F_P(L)$$

- $F_L$：长度-主动力
- $F_V$：速度-主动力
- $F_P$：被动力（始终存在）
- 输出力：$\text{actuator\_force} = -\text{FLV} \cdot F_0$（正激活产生拉力）

### 激活动力学

非线性一阶滤波：
$$\frac{\partial}{\partial t}\text{act} = \frac{\text{ctrl} - \text{act}}{\tau(\text{ctrl}, \text{act})}$$

控制信号钳制到 [0,1]。时间常数：$(\tau_{\text{act}}, \tau_{\text{deact}})$ 默认 (0.01, 0.04)。

可选 `tausmooth` 参数平滑切换。

### 调整层级

| 层级 | 调整内容 | 适用场景 |
| --- | --- | --- |
| 默认 | 不调任何参数 | 通用模型 |
| scale | 整体肌肉强弱 | 不知 $F_0$ |
| force | $F_0$ 峰值力 | 有实验数据 |
| range | 肌肉操作范围 | 有实验数据 |
| timeconst | 快/慢肌纤维比例 | 详细建模 |
| lmin, lmax... | FLV 曲线形状 | 高级用户 |

### 与 OpenSim 的关系

- 激活动力学模型相同
- FLV 函数近似（不精确相同）
- 假设不可伸缩肌腱（OpenSim 可伸缩）
- 不建模 pennation angle
- 肌腱 wrapping 更受限（sphere/cylinder，要求 wrapping 对象间有 site 分隔）

## 传感器（Sensors）

MuJoCo 模拟传感器数据写入 `mjData.sensordata`，不影响仿真。支持类型：
- 触摸、IMU、力-扭矩、关节/腱位置/速度、执行器、体坐标系、测距仪、相机（离屏渲染）等
- `user` 类型 + `mjcb_sensor` 回调实现自定义

## 求解器设置建议

| 场景 | 推荐设置 |
| --- | --- |
| 大多数模型 | Newton, 极小 tolerance (1e-10) |
| 大型模型 + elliptic + 多滑移接触 | CG |
| DOF > 约束数 + 低精度可接受 | PGS |
| 接触滑移问题 | Newton + elliptic + 大 impratio |
| 上仍不足 | 启用 NoSlip（注意可能不稳定） |

Jacobian 稠密/稀疏：小模型 dense（< 60 DOF），大模型 sparse。默认 'auto'。

摩擦锥选择：elliptic 更接近物理，pyramidal 可改善算法性能（不一定）。
