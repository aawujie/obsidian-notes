---
title: Robotics CAD Skills 功能概览
type: summary
created: 2026-05-21
updated: 2026-05-21
tags: [skill, CAD, robotics, URDF, SDF, SRDF, STEP, rendering, manufacturing]
---

# Robotics CAD Skills 功能概览

> **状态**: `.claude/skills/` 下的 7 个 skill 全部为断裂 symlink，指向不存在的 `.agents/skills/`。
> 内容基于各格式/工具在 robotics 生态中的标准定义编写。

## 总览表

| Skill | 类型 | 一句话 | 典型输入 | 典型输出 |
|-------|------|--------|----------|----------|
| **urdf** | 格式 | 机器人运动学/动力学描述 | Xacro / CAD | URDF XML + meshes |
| **sdf** | 格式 | Gazebo 仿真世界描述 | URDF / 手写 | SDF XML + world |
| **srdf** | 格式 | 语义化机器人配置（MoveIt） | URDF | SRDF + MoveIt config |
| **cad** | 工具 | CAD 文件导入/导出/转换 | STP/IGES/SLDPRT | STL/mesh/URDF |
| **step-parts** | 格式 | STEP 零件库提取与管理 | STEP assembly | 单零件 STEP + BOM |
| **render** | 工具 | 3D 渲染与可视化 | URDF/mesh | PNG/GIF/MP4 渲染图 |
| **sendcutsend** | 服务 | 激光/CNC 加工订单 | DXF/SVG/STEP | 制造零件 |

---

## 逐个详解

### 1. URDF — Unified Robot Description Format

**核心能力**：
- 定义机器人的运动学树（link + joint 层级）
- 为每个 link 指定视觉几何、碰撞几何、惯性参数
- 支持 6 种关节类型：revolute / prismatic / fixed / continuous / floating / planar
- Xacro 宏扩展：参数化、宏复用、数学表达式

**典型工作流**：
```
CAD 设计 → Phobos/fusion2urdf → URDF + STL网格
                              → Xacro 参数化组装
                              → robot_state_publisher → TF tree
```

**局限性**：无世界描述、传感器支持有限、仅支持树状结构（非图）

> 完整指南见 [[URDF文件生成完整指南]]

---

### 2. SDF — Simulation Description Format

**核心能力**：
- **URDF 的超集**：Gazebo（Ignition）的原生格式
- 支持 `<world>` 元素：光照、物理引擎参数、地面、障碍物
- 传感器模拟：LiDAR、相机、IMU、力-扭矩
- 支持闭环运动学链（非树状结构）
- 插件系统：Gazebo 插件注入传感器/驱动器

**与 URDF 的关键区别**：

| 特性 | URDF | SDF |
|------|------|-----|
| 世界描述 | 无 | ✅ `<world>` |
| 闭环链 | 不支持 | ✅ |
| 传感器 | 有限 | 丰富（LiDAR/Camera/IMU） |
| 关节 | 树状 | 图状 |
| 仿真引擎 | 不绑定 | Gazebo 原生 |

**转换命令**：
```bash
# URDF → SDF
gz sdf -p model.urdf > model.sdf
```

**SDF 典型文件结构**：
```xml
<sdf version="1.9">
  <world name="default">
    <physics type="ode">
      <gravity>0 0 -9.81</gravity>
    </physics>
    <light name="sun" type="directional">...</light>
    <model name="robot">
      <link name="chassis">...</link>
      <joint name="wheel_joint" type="revolute">...</joint>
    </model>
  </world>
</sdf>
```

---

### 3. SRDF — Semantic Robot Description Format

**核心能力**：
- **MoveIt 运动规划框架**的配置文件格式
- 在 URDF 基础上添加**语义信息**：规划组、碰撞矩阵、末端执行器、关节配置
- 定义默认运动学求解器（KDL / TRAC-IK / IKFast）
- 预设姿态（如 "home"、"ready"、"grab"）

**SRDF 定义的内容**：
```xml
<robot name="my_arm">
  <!-- 规划组：哪些 joint 参与运动规划 -->
  <group name="arm">
    <joint name="shoulder_pan_joint"/>
    <joint name="shoulder_lift_joint"/>
    <joint name="elbow_joint"/>
    <joint name="wrist_1_joint"/>
    <joint name="wrist_2_joint"/>
  </group>

  <!-- 末端执行器定义 -->
  <end_effector name="gripper" parent_link="wrist_2_link" group="gripper"/>

  <!-- 碰撞免检矩阵：哪些 link 对之间不检测碰撞 -->
  <disable_collisions link1="base_link" link2="shoulder_link" reason="adjacent"/>

  <!-- 预设姿态 -->
  <group_state name="home" group="arm">
    <joint name="shoulder_pan_joint" value="0"/>
    <joint name="shoulder_lift_joint" value="-0.78"/>
    <joint name="elbow_joint" value="1.57"/>
  </group_state>
</robot>
```

**典型工作流**：
```
URDF 模型 → MoveIt Setup Assistant → SRDF + MoveIt Config Package
                                    → 运动规划/避障/抓取
```

> URDF + SRDF 是 MoveIt 的标准输入对。URDF 描述结构，SRDF 描述如何使用。

---

### 4. CAD — CAD 文件导入/导出/转换

**核心能力**：
- 多种 CAD 格式的读取与转换：STEP (.stp)、IGES (.igs)、SLDPRT、STL、OBJ
- CAD 装配体 → 简化网格的自动转换
- 网格简化/减面（为实时仿真优化）
- 惯性参数自动计算（基于体积+密度）
- 坐标轴对齐与原点设置

**支持的文件格式**：

| 格式 | 扩展名 | 类型 | 说明 |
|------|--------|------|------|
| STEP | .stp .step | 精确曲面 | 行业标准 CAD 交换 |
| IGES | .igs .iges | 精确曲面 | 较旧的交换格式 |
| STL | .stl | 三角网格 | 3D 打印/仿真常用 |
| OBJ | .obj | 三角网格 | 带材质支持 |
| DAE | .dae | Collada | ROS 推荐网格格式 |
| SLDPRT | .sldprt | SolidWorks 原生 | 需 SolidWorks 库 |

**典型用途**：
- 快速将供应商的 STEP 零件转为 STL 用于 URDF
- 批量转换装配体中的所有零件
- 简化高精度 CAD 网格以加速物理仿真

---

### 5. step-parts — STEP 零件库提取

**核心能力**：
- 解析 STEP AP203/AP214 装配体文件
- 提取单个零件为独立 STEP 文件
- 生成零件清单（BOM）
- 按名称/材质/尺寸筛选零件
- 批量导出为 STL/OBJ

**典型工作流**：
```
STEP 装配体（整机）
    ↓ step-parts 拆解
├── base.stp         ← 提取底盘
├── arm_upper.stp    ← 提取上臂
├── arm_lower.stp    ← 提取前臂
├── gripper.stp      ← 提取夹爪
├── BOM.csv          ← 零件清单
    ↓ cad skill 转换
├── base.stl → URDF link
├── arm_upper.stl → URDF link
...
```

**与 cad skill 的分工**：
- **step-parts**：从装配体中提取/筛选独立零件
- **cad**：单个零件格式转换（STEP → STL/OBJ）

---

### 6. render — 3D 渲染与可视化

**核心能力**：
- 将 URDF/机器人模型渲染为高质量图片/视频
- 支持多种渲染后端：Blender Eevee/Cycles、MuJoCo 内置渲染器、Pyrender
- 生成技术文档用图（带标注、尺寸、关节范围示意）
- 动画渲染（关节运动序列 → GIF/MP4）
- 多视角自动渲染（正面、侧面、俯视、45°）

**典型用途**：
```
robot.urdf + 关节角度
    ↓ render skill
├── robot_front.png       ← 正面渲染
├── robot_side.png        ← 侧面渲染
├── robot_animation.gif   ← 关节运动动画
├── exploded_view.png     ← 爆炸视图
└── render_scene.blend    ← Blender 场景文件（可二次编辑）
```

**技术栈**：
- **Blender**：最高质量，支持物理材质、光照、Cycles 光追
- **MuJoCo**：实时渲染，适合仿真截图
- **Pyrender**：Python 原生的轻量渲染

---

### 7. sendcutsend — 制造加工服务

**核心能力**：
- **SendCutSend** 是一家在线激光切割/CNC 加工服务商
- Skill 负责：生成加工文件 → 提交订单 → 跟踪状态
- 支持的材料：铝、钢、不锈钢、钛、碳纤维、亚克力、木材等
- 支持工艺：激光切割、CNC 铣削、折弯、攻丝、粉末涂层

**典型工作流**：
```
CAD 零件设计（Fusion 360 / SolidWorks）
    ↓ 展开为平板
DXF/SVG 2D 切割文件
    ↓ sendcutsend skill
├── 自动检查设计规则（最小孔径、材料厚度限制）
├── 即时报价（材料 + 切割 + 后处理 + 运费）
├── 提交订单
└── 跟踪生产/发货状态
```

**设计规则检查清单**：
- 最小孔径 ≥ 材料厚度的 50%
- 最小间距 ≥ 材料厚度
- 外部锐角需加圆角
- 折弯需标注折弯线

---

## 完整工作流串联

这 7 个 skill 组合起来覆盖了从 CAD 设计到物理制造的完整 pipeline：

```
┌─────────────────────────────────────────────────────────────┐
│                  Robot Hardware 全流程                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. CAD 设计 (Fusion 360 / SolidWorks)                       │
│       ↓                                                     │
│  2. STEP 装配体导出                                          │
│       ↓                                                     │
│  3. step-parts → 拆解零件 + BOM                              │
│       ↓                                                     │
│  4. cad → 格式转换 (STEP → STL/DAE)                          │
│       ↓                                                     │
│  5. urdf → 组装机器人模型 (link + joint + inertial)           │
│       ↓                                                     │
│  6. srdf → 配置运动规划 (MoveIt planning groups)              │
│       ↓                                                     │
│  7. sdf → 扩展为仿真世界 (Gazebo/Isaac Sim)                   │
│       ↓                                                     │
│  8. render → 生成可视化素材                                   │
│       ↓                                                     │
│  9. sendcutsend → 制造物理零件                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 技能健康状态

**所有 7 个 skill 的 symlink 均断裂**，指向的 `.agents/skills/` 目录不存在：

```bash
# 当前状态（全部红色）
.claude/skills/urdf        → ../../.agents/skills/urdf       ❌
.claude/skills/cad         → ../../.agents/skills/cad        ❌
.claude/skills/render      → ../../.agents/skills/render     ❌
.claude/skills/sdf         → ../../.agents/skills/sdf        ❌
.claude/skills/sendcutsend → ../../.agents/skills/sendcutsend ❌
.claude/skills/srdf        → ../../.agents/skills/srdf       ❌
.claude/skills/step-parts  → ../../.agents/skills/step-parts ❌
```

**修复建议**：
1. 如果这些 skill 来自 Skill Market → 安装 `skillctl` 并重新 install
2. 如果来自某个 git repo → 将 repo clone 到 `.agents/` 目录下
3. 如果不再需要 → 删除断裂的 symlink

> 详情见 [[URDF文件生成完整指南]]

## 相关笔记

- [[URDF文件生成完整指南]] — URDF 生成方法详解
- [[MuJoCo-建模]] — MJCF 与 URDF 对比
- [[MuJoCo-概览]] — MuJoCo 物理引擎架构
- [[开源机器人项目调研-2025-2026]] — 当前主流机器人项目实践