---
title: MuJoCo 编程
type: summary
created: 2026-04-28
updated: 2026-04-28
sources: [https://mujoco.readthedocs.io/en/stable/programming/index.html]
tags: [MuJoCo, 编程, C API, OpenGL, 仿真]
---

# MuJoCo 编程（Programming）

## 代码库结构

```
Engine/    仿真引擎（C）——运行时计算
Parser/    XML 解析器（C++）——解析 MJCF/URDF → mjCModel/mjSpec
Compiler/  编译器（C++） ——mjCModel → mjModel
Visualizer/ 抽象可视化器（C）——生成抽象几何实体
Renderer/  渲染器（C）——fixed-function OpenGL
Thread/    线程框架（C++, C 暴露）——mjThreadPool
UI/        UI 框架（C）——OpenGL 渲染的 UI 元素
```

## 快速入门

### 预编译库

从 GitHub Releases 下载预编译库（x86_64/arm64, Win/Linux/macOS）。预编译库自包含，隐藏所有非公开符号。

```bash
# 解压即可运行
simulate ../model/humanoid/humanoid.xml
```

目录结构：
```
bin/     动态库、可执行文件、MUJOCO_LOG.TXT
doc/     README.txt, REFERENCE.txt
include/ 头文件
model/   模型集合
sample/  代码示例 + CMakeLists.txt
```

### 从源码构建

```bash
git clone https://github.com/google-deepmind/mujoco.git
mkdir build && cd build
cmake $PATH_TO_REPO -DCMAKE_BUILD_TYPE=Release
cmake --build .
cmake --install .
```

## 头文件（Header Files）

| 头文件 | 说明 |
| --- | --- |
| **mujoco.h** | 主头文件（必含），定义所有 API 函数和全局变量 |
| **mjmodel.h** | `mjModel` 结构定义 |
| **mjdata.h** | `mjData` 结构定义 |
| **mjvisualize.h** | 抽象可视化器类型/结构 |
| **mjrender.h** | OpenGL 渲染器类型/结构 |
| **mjui.h** | UI 框架类型/结构 |
| **mjtnum.h** | `mjtNum` 浮点类型（double/float） |
| **mjspec.h** | 程序化模型编辑的枚举和结构 |
| **mjplugin.h** | 引擎插件数据结构 |
| **mjthread.h** | 线程数据结构与函数 |
| **mjxmacro.h** | X Macros（可选，用于脚本语言映射） |

## 命名约定

所有 API 符号以 `mj` 开头：

| 前缀 | 含义 | 示例 |
| --- | --- | --- |
| `mj` | 核心数据结构 | `mjModel`, `mjMIN` |
| `mjt` | 原始类型（大多为 enum） | `mjtGeom` |
| `mjf` | 回调函数类型 | `mjfGeneric` |
| `mjv` | 抽象可视化 | `mjvCamera` |
| `mjr` | OpenGL 渲染 | `mjrContext` |
| `mjui` | UI 框架 | `mjuiSection` |
| `mjs` | 程序化模型编辑 | `mjsJoint` |
| `mj_` | 核心仿真函数 | `mj_step` |
| `mju_` | 工具函数（不依赖 mjModel/mjData） | `mju_mulMatVec` |
| `mjv_` | 抽象可视化函数 | `mjv_updateScene` |
| `mjr_` | OpenGL 渲染函数 | `mjr_render` |
| `mjcb_` | 全局回调函数指针 | `mjcb_control` |
| `mjd_` | 导数计算函数 | `mjd_transitionFD` |
| `mjs_` | 程序化模型编辑函数 | `mjs_addJoint` |

## 版本兼容

```c
// 头文件版本 vs 库版本检查
if (mjVERSION_HEADER != mj_version())
    // 不匹配！
```

使用整数比较避免浮点问题。版本编码公式见 VERSIONING.md。

## 使用 OpenGL

- MuJoCo 使用兼容模式的 OpenGL 1.5
- 通过 GLAD 第一次调用 `mjr_makeContext` 时加载 OpenGL 符号
- 库本身无显式 OpenGL 依赖（不调用 `mjr_` 函数可用无 GPU 系统）
- Linux 支持：GLX (X11 窗口), OSMesa (无头软件渲染), EGL (硬件加速无头渲染)

## 仿真管线关键函数

| 函数 | 作用 |
| --- | --- |
| `mj_step` | 完整正向动力学一步 |
| `mj_forward` | 连续时间正向动力学（得加速度） |
| `mj_step1` | 第一阶段（position-dependent 部分） |
| `mj_step2` | 第二阶段（加速+积分） |
| `mj_inverse` | 逆动力学（得施加力） |
| `mj_resetData` | 重置 mjData |
| `mj_kinematics` | 仅正向运动学 |

## 管线阶段详解

```
1. mj_checkPos/mj_checkVel    ——检查发散
2. mj_kinematics              ——正向运动学
3. mj_comPos                  ——全局坐标系体惯量/关节轴
4. mj_tendon                  ——腱长度和力臂
5. mj_makeM                   ——关节空间惯量矩阵
6. mj_factorM                 ——M 的稀疏分解
7. mj_collision               ——碰撞检测
8. mj_makeConstraint          ——构建约束 Jacobian
9. mj_transmission            ——执行器长度/力臂
10. mj_projectConstraint      ——约束求解器准备
11. mj_fwdVelocity            ——腱/执行器速度
12. mj_comVel                 ——体速度
13. mj_passive                ——被动力
14. mj_referenceConstraint    ——参考约束加速度
15. mj_rne                    ——Coriolis/离心/重力（RNE）
16. mjcb_control              ——用户控制回调
17. mj_fwdActuation           ——执行器力
18. mj_fwdAcceleration        ——无约束加速度
19. mj_fwdConstraint          ——约束求解（得qacc）
20. 积分器                    ——Euler/implicit/RK4
```

## mjData 一致性

- **设置状态后**：状态派生量不会自动更新，需手动调用所需阶段函数
- **mj_step 后**：mjData 中某些量对应前一个状态（如位置相关传感器值）
- 管线完全 imperative，无自动行为

## 可复现性

- MuJoCo 完全确定性（同状态、同版本、同架构 → 同输出）
- 需保存完整积分状态（含 warmstart 加速度，如需要位级相等）
- **接触事件 Lyapunov 指数高**（刚性体仿真本体属性，非 MuJoCo 特有）
- 跨版本、跨 OS 不保证位级复现

## 逆动力学管线

`mj_inverse` 调用序列基本同正动力学，但：
- 约束力**解析计算**，无数值求解器
- 最终输出：`mjData.qfrc_inverse`（外部力 + 执行器力之和）

## 导数（Derivatives）

### 可用函数

- **mjd_transitionFD**：离散时间正动力学状态/控制转移 Jacobian（mj_step）
- **mjd_inverseFD**：逆动力学 Jacobian（mj_inverse）

利用可配置管线避免重复计算，支持前向/中心差分。正确处理 warmstart、四元数、控制钳制。

**注意**：默认 solver impedance 下接触**不可微**，需设 `solimp[0]=0`（d0=0）使接触力开始平滑。

## 构建文档

```bash
cd mujoco/doc
pip install -r requirements.txt
make html
# 打开 _build/html/index.html
```
