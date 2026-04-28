---
title: MuJoCo 概览
type: summary
created: 2026-04-28
updated: 2026-04-28
sources: [https://mujoco.readthedocs.io/en/stable/overview.html]
tags: [MuJoCo, 机器人, 仿真, 物理引擎, DeepMind]
---

# MuJoCo 概览（Overview）

## 简介（Introduction）

**MuJoCo** = **Mu**lti-**Jo**int dynamics with **Co**ntact（多关节接触动力学）。它是一个通用物理引擎，旨在服务机器人、生物力学、图形与动画、机器学习等需要快速精确仿真关节结构与环境的领域。最初由 Roboti LLC 开发，2021 年 10 月被 Google DeepMind 收购并免费开放，2022 年 5 月开源。

MuJoCo 是 C/C++ 库，提供 C API。运行时仿真模块最大化性能，操作预分配的低级数据结构。模型使用 MJCF（Native XML scene description language）定义，也可加载 URDF 文件。

## 核心特性（Key Features）

### 1. generalized coordinates + 现代接触动力学

传统物理引擎分两类：
- **机器人/生物力学引擎**：使用 generalized coordinates（广义坐标/关节坐标），递归算法高效精确，但不处理接触或依赖 spring-damper 方法（需极小时步）。
- **游戏引擎**：Cartesian coordinates（笛卡尔坐标），通过优化求解接触力，但关节约束数值化施加导致不精确。

**MuJoCo 首创二者结合**：generalized coordinates + optimization-based contact dynamics。

### 2. 软性、凸且解析可逆的接触动力学

传统方法将摩擦接触建模为 LCP（Linear Complementarity Problem）或 NCP（Nonlinear Complementarity Problem），均为 **NP-hard**。

MuJoCo 使用不同公式，将接触物理简化为 **convex optimization problem（凸优化问题）**。支持：
- 软接触（soft contacts）
- 统一处理：摩擦接触（含 torsional/rolling friction）、无摩擦接触、关节/腱限位、干摩擦、多种 equality constraints
- 默认 Newton solver（二次收敛），备选 CG（conjugate gradient）和 PGS（Projected Gauss-Seidel）

### 3. 腱几何（Tendon Geometry）

3D 腱模型——最短路径线，支持 wrapping（缠绕）和 via-point 约束。类似 OpenSim 但提供封闭形式的 wrapping 选项以加速计算。支持滑轮（pulleys）和耦合自由度。作为驱动或施加不等式/等式约束使用。

### 4. 通用驱动模型（General Actuation Model）

抽象驱动模型，支持不同 transmission（传动）、force generation（力生成）、internal dynamics（内部动力学，使系统升为三阶）：
- 电机、气缸（气动/液压）、PD 控制器、生物肌肉

### 5. 可重配置计算管线（Reconfigurable Pipeline）

顶层函数 `mj_step` 运行完整正向动力学。提供大量 flag 组合重配置管线，低层函数可直调。用户回调可实现自定义力场、驱动、碰撞、反馈控制。

### 6. 模型编译（Model Compilation）

MJCF XML → 内置编译器 → `mjModel`（交叉索引、运行时优化）。编译后可保存为二进制 MJB 文件。

### 7. 模型与数据分离（Model vs Data）

| 结构 | 作用 |
| --- | --- |
| `mjModel` | 模型描述（常量），含仿真/可视化选项 |
| `mjData` | 动态变量、中间结果、预分配堆栈 |

运行时零内存分配。支持多模型、多状态并行仿真。

```c
void mj_step(const mjModel* m, mjData* d);
```

### 8. 性能（Performance）

- 零运行时内存分配（`mjData` 预分配）
- 单步单线程（默认），constraint islands 支持岛内并行
- 大数据并行采样：多 `mjData` 共享一个 `mjModel`，多线程运行

### 9. 交互式仿真与可视化

原生 OpenGL 3D 可视化：网格、纹理、反射、阴影、雾、透明度、线框、天空盒、立体视觉。GUI 支持"伸手"扰动仿真，选体施加外力/扭矩，实时查看响应。

### 10. 强大的建模语言（MJCF）

类似 CSS（Cascading Style Sheets）的默认设置机制：丰富的元素和属性，模型文件中大部分可省略，使文件短小可读。

### 11. 复合柔性对象自动生成

软约束可建模绳索（ropes）、布料（cloth）、可变形 3D 对象。使用高层宏自动展开为标准模型元素的集合，能与仿真其余部分交互。

### 12. Constraint Islands 与 Sleeping

- 自动发现独立约束岛，独立求解，支持岛级并行
- 无约束自由度完全跳过
- Island sleeping：冻结静止岛，大幅减少计算

### 13. 插件系统

引擎插件通过共享库扩展自定义传感器、驱动器和被动力，无需修改核心引擎。

### 14. GPU 加速后端

- **MJX**（JAX 后端）
- **MuJoCo Warp**（NVIDIA Warp）
- 与 CPU 共享 `mjModel`/`mjData` 结构，CPU/GPU 无缝切换

## 模型实例（Model Instances）

| | 高层 | 低层 |
| --- | --- | --- |
| **文件** | MJCF/URDF (XML) | MJB (二进制) |
| **内存** | mjSpec (C struct) | mjModel (C struct) |

获取 `mjModel` 的路径：
1. 编辑器 → MJCF/URDF → 解析器 → mjSpec → 编译器 → mjModel
2. 用户代码 → mjSpec → 编译器 → mjModel
3. MJB 文件 → 加载器 → mjModel

## 模型元素（Model Elements）

### Options
- `mjOption`：物理仿真选项（算法、参数、重力等）
- `mjVisual`：可视化选项
- `mjStatistic`：模型统计（平均质量、空间范围等）

### Assets（资源）
- **Mesh**：OBJ/STL 三角网格，碰撞检测用 convex hull
- **Skin**：可变形蒙皮网格（纯可视化，不影响物理）
- **Height field**：PNG 高程数据，用于地形建模
- **Texture**：PNG 纹理，支持 2D/cube 映射
- **Material**：控制 geom/site/tendon 外观（RGBA、反射等）

### Kinematic Tree（运动学树）
- **Body**：刚体，有质量/惯性，无几何属性
- **Joint**：创建自由度（ball/slide/hinge/free）
- **DOF**：速度/力空间坐标
- **Tree**：可动体及其所有后代
- **Geom**：3D 形状（plane/sphere/capsule/ellipsoid/cylinder/box/mesh/hfield）
- **Site**：轻量 geom，用于传感器/腱路径/滑轨端点
- **Camera**：多摄像头（固定或附着体上）
- **Light**：OpenGL 光照模型

### Stand-alone（独立元素）
- **Tendon**：标量长度元素（驱动/限位/等式约束/弹簧阻尼）
- **Actuator**：灵活的驱动模型（transmission + 激活动力学 + 力生成）
- **Sensor**：模拟传感器数据（触摸/IMU/力-扭矩/关节/腱/相机...）
- **Equality**：等式约束（连接/焊接/锁定关节/耦合多项式）
- **Flex**：可变形网格（1D/2D/3D），绳索/布料/软体
- **Contact pair / exclude**：指定/排除碰撞对
- **Custom numeric/text/tuple**：用户自定义数据
- **Keyframe**：状态快照（关节位置/速度/驱动/控制/时间）

## 重要概念

### 单位（Units）
MuJoCo **不指定基本物理单位**，用户自行保持一致性。建议使用 MKS（米-千克-秒）：
- 默认重力：`(0, 0, -9.81)`（MKS 地表重力）
- 默认密度：`1000`（水在 MKS 下的密度）
- 角度：MJCF 可用度，但 `mjModel`/`mjData` 中均为弧度

### 发散（Divergence）
当状态元素快速趋向无穷时发生。通常是时步过大导致，不是模型错误。减小 timestep 或切换更稳定积分器可解决。

### 数据导向设计（Data-Oriented Design）
MuJoCo 采用数据导向架构（非面向对象）。实体是整个物理仿真器，不是带私有状态的独立对象。模型（`mjModel`）与数据（`mjData`）分离，所有顶层函数接受二者指针。天然支持多线程。

### 软性与滑移（Softness and Slip）
MuJoCo 的约束模型本质上是软的——更大的力导致更大的加速，因此 inverse dynamics 可唯一定义。**逐渐接触滑移是不可避免的**，不是摩擦力不足，而是参数需调整。抑制滑移推荐方法：Newton solver + elliptic friction cones + 大 impratio。

### 类型、名称、ID
元素由类型枚举 `mjtObj` 标识。命名可选，但需引用时必须命名。函数 `mj_name2id` / `mj_id2name` 进行名称与整数 ID 互转。ID 为 0-based。

### Bodies、Geoms、Sites 的区别
- **Body**：运动学树节点，有惯量、无外观/碰撞几何
- **Geom**：指定外观和碰撞几何，多个 geom 可附同一 body
- **Site**：轻量 geom，无碰撞、不影响惯量，用于传感器/腱路由

### Joint coordinates vs Cartesian coordinates
| 关节坐标 | 笛卡尔坐标 |
| --- | --- |
| 适合复杂运动学结构（机器人） | 适合大量碰撞体（分子动力学、堆叠） |
| Joints 添加自由度 | Joints 移除自由度 |
| 关节约束隐式，不可违反 | 关节约束数值化强制，可违反 |
| 体位置由正向运动学得出 | 体位置显式存储，可直改 |
