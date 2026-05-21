---
title: URDF文件生成完整指南
type: concept
created: 2026-05-21
updated: 2026-05-21
sources: [ros.org, mujoco.readthedocs.io, github.com/dfki-ric/phobos, github.com/Rhoban/onshape-to-robot]
tags: [URDF, ROS, 机器人, 建模, XML, CAD, SDF, MJCF, USD]
---

# URDF 文件生成完整指南

## 什么是 URDF

**URDF**（Unified Robot Description Format，统一机器人描述格式）是 ROS 生态中描述机器人模型的 XML 标准格式。一个 URDF 文件定义机器人的：

- **Links（连杆）**：刚体部件，含视觉几何、碰撞几何、惯性参数
- **Joints（关节）**：连杆之间的运动约束（revolute、prismatic、fixed、continuous、floating、planar）

编译与加载管线：
```
URDF XML → parser → mjSpec/URDF DOM → compiler → mjModel → 仿真/可视化
```

> URDF 功能有限，复杂场景可用 **MJCF**（[[MuJoCo-建模|MuJoCo原生格式]]）或 **SDF**（Gazebo格式）。更多对比见 [[MuJoCo-概览]]。

---

## 生成方式总览（6大方式）

```
┌──────────────────────────────────────────────────────────────────┐
│                     URDF 文件生成方式                              │
├─────────────┬──────────────┬─────────────┬───────────┬───────────┤
│  手动编写    │  CAD工具导出  │ 程序化生成   │ 格式转换   │ AI辅助    │
│             │              │             │           │           │
│ • 文本编辑器 │ • SolidWorks │ • urdfpy    │ • SDF→URDF│ • LLM生成  │
│ • Xacro宏   │ • Fusion 360 │ • yourdfpy  │ • MJCF→   │           │
│             │ • FreeCAD    │ • onshape-  │   URDF    │           │
│             │ • Onshape    │   to-robot  │ • USD→URDF│           │
│             │ • Blender/   │ • ROS 2 CLI │           │           │
│             │   Phobos     │             │           │           │
└─────────────┴──────────────┴─────────────┴───────────┴───────────┘
```

---

## 方式一：手动编写

### 1.1 纯 URDF XML

使用任意文本编辑器（VS Code、vim）直接编写 XML。适合简单模型或学习目的。

**最简示例**（单连杆）：
```xml
<?xml version="1.0"?>
<robot name="simple_robot">
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.6 0.4 0.2"/>
      </geometry>
      <material name="blue">
        <color rgba="0 0 1 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.6 0.4 0.2"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="10"/>
      <inertia ixx="0.1" ixy="0" ixz="0" iyy="0.1" iyz="0" izz="0.1"/>
    </inertial>
  </link>
</robot>
```

**两连杆+关节示例**：
```xml
<robot name="arm">
  <link name="base_link">
    <visual>
      <geometry><cylinder radius="0.2" length="0.1"/></geometry>
    </visual>
  </link>

  <link name="arm_link">
    <visual>
      <geometry><box size="0.1 0.5 0.1"/></geometry>
    </visual>
  </link>

  <joint name="shoulder" type="revolute">
    <parent link="base_link"/>
    <child link="arm_link"/>
    <origin xyz="0 0 0.1" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="-1.57" upper="1.57" effort="10" velocity="3"/>
  </joint>
</robot>
```

**优点**：完全控制，无依赖
**缺点**：大型模型难以维护，大量重复代码

### 1.2 Xacro 宏语言（推荐）

**Xacro** 是 URDF 的宏扩展语言，通过变量、宏、数学表达式消除重复。这是 ROS 社区的标准实践。

**安装**：
```bash
sudo apt install ros-<distro>-xacro
pip install xacro  # ROS 2 独立安装
```

**核心特性**：

```xml
<!-- 1. 属性/常量 -->
<xacro:property name="wheel_radius" value="0.05"/>
<xacro:property name="chassis_length" value="0.4"/>

<!-- 2. 数学表达式 -->
<origin xyz="${chassis_length/2} 0 ${wheel_radius}"/>

<!-- 3. 宏定义（可复用组件模板） -->
<xacro:macro name="wheel" params="name prefix radius:=0.05 mass:=0.1">
  <link name="${prefix}_${name}_wheel">
    <visual>
      <geometry>
        <cylinder radius="${radius}" length="0.02"/>
      </geometry>
    </visual>
    <inertial>
      <mass value="${mass}"/>
      <inertia ixx="0.001" ixy="0" ixz="0" iyy="0.001" iyz="0" izz="0.001"/>
    </inertial>
  </link>
</xacro:macro>

<!-- 4. 实例化宏 -->
<xacro:wheel name="front_left" prefix="robot" radius="0.05" mass="0.1"/>
<xacro:wheel name="front_right" prefix="robot" radius="0.05" mass="0.1"/>
<xacro:wheel name="rear_left" prefix="robot" radius="0.05" mass="0.1"/>
<xacro:wheel name="rear_right" prefix="robot" radius="0.05" mass="0.1"/>

<!-- 5. 文件包含 -->
<xacro:include filename="$(find my_robot)/urdf/common_macros.xacro"/>

<!-- 6. 条件块 -->
<xacro:if value="${use_gazebo}">
  <gazebo reference="${prefix}_${name}_wheel">
    <mu1>1.0</mu1><mu2>1.0</mu2>
  </gazebo>
</xacro:if>
```

**编译为 URDF**：
```bash
xacro model.urdf.xacro > model.urdf
xacro model.urdf.xacro use_gazebo:=true > model.urdf
```

**ROS 2 Launch 集成**：
```python
robot_description = {
    'robot_description': Command([
        'xacro ',
        FindPackageShare('my_robot'), '/urdf/robot.urdf.xacro',
        ' use_gazebo:=', LaunchConfiguration('use_gazebo')
    ])
}
```

**推荐文件结构**：
```
my_robot/
├── urdf/
│   ├── robot.urdf.xacro        # 主文件（组装所有组件）
│   ├── macros.xacro            # 可复用宏定义
│   ├── materials.xacro         # 材质/颜色定义
│   └── gazebo.xacro            # Gazebo 特定配置
├── meshes/                     # STL/DAE 网格文件
└── launch/
    └── display.launch.py
```

**优点**：参数化、可复用、简洁
**缺点**：需要额外编译步骤；调试需展开为纯 URDF

---

## 方式二：CAD 工具导出

### 2.1 SolidWorks → URDF

**工具**：`ros/solidworks_urdf_exporter`（最广泛使用的工业级方案）

**流程**：
1. 在 SolidWorks 中创建装配体
2. 使用 Mate 定义关节关系（同轴=旋转关节，平行+重合=滑动关节等）
3. 安装 SW URDF Exporter 插件
4. 在插件界面定义 link 名称、关节类型、轴方向、限位
5. 一键导出 URDF + STL/DAE 网格 + launch 文件

**输出**：完整的 ROS package（含 meshes/、urdf/、launch/ 目录）

**优点**：专业机械设计集成度高，自动惯性计算
**缺点**：需要 SolidWorks 许可证；复杂装配体 Mate 推断可能有误

### 2.2 Fusion 360 → URDF

**工具**：`fusion2urdf`（开源，Fusion 360 App Store 或 GitHub 安装）

**流程**：
1. 使用 Fusion 360 的 Joint 系统创建关节（As-Built Joint 或常规 Joint）
2. 为每个 Joint 指定正确的类型（Revolute、Slider、Rigid 等）
3. 运行 fusion2urdf 插件
4. 选择根 link，配置导出选项
5. 自动生成 URDF + STL 网格

**关键规则**：
- 关节命名要清晰，因为会直接映射到 URDF 的 joint name
- Rigid Joint → URDF fixed joint
- Revolute Joint → URDF revolute joint
- Rigid Group 内的多个零件合并为单个 link

**优点**：免费（个人/教育），云端 CAD 方便协作
**缺点**：惯性参数可能需要手动调整

### 2.3 FreeCAD → URDF

**工具**：FreeCAD URDF Workbench

**流程**：
1. 安装 FreeCAD（开源免费）
2. 通过 Addon Manager 安装 URDF Workbench
3. 在装配体中创建简单的 link-joint 结构
4. 通过工作台面板导出 URDF

**优点**：完全免费开源，跨平台
**缺点**：功能不如商业方案丰富，装配体功能较弱

### 2.4 Onshape → URDF

**工具**：`onshape-to-robot`（Python CLI，Rhoban 团队维护）

**安装**：
```bash
pip install onshape-to-robot
```

**流程**：
1. 在 Onshape（浏览器端 CAD）中设计机器人装配体
2. 获取 Onshape API Key 和 Secret
3. 编写 YAML 配置文件，指定 link 名称、关节、轴方向：

```yaml
# config.yaml
document_url: "https://cad.onshape.com/documents/xxxxx"
assembly_name: "robot_assembly"

links:
  base_link:
    meshes: [base_link]
  arm_link:
    meshes: [arm_link, arm_mount]  # 合并多个零件为一个 link

joints:
  shoulder:
    parent: base_link
    child: arm_link
    type: revolute
    origin: [0, 0, 0.1]
    axis: [0, 0, 1]
    limits: [-1.57, 1.57]
```

4. 运行导出：
```bash
onshape-to-robot config.yaml
```

**优点**：无需安装 CAD 软件，云端协作，支持批量导出
**缺点**：需要 Onshape 账户和 API 配置

### 2.5 Blender + Phobos

**工具**：Phobos（Blender 插件，DFKI 开发）

**安装**：
```bash
# 从 GitHub 下载 zip
# Blender → Edit → Preferences → Add-ons → Install
# 或直接用 git clone 到 Blender addons 目录
git clone https://github.com/dfki-ric/phobos.git
```

**核心功能**：
- 在 Blender 中完整定义 link 层级（visual + collision + inertial）
- 关节定义与属性编辑
- 惯性可视化
- 电机/传感器定义
- 多格式导出：URDF、SDF、SMURF、MJCF

**流程**：
1. 在 Blender 中导入/建模机器人几何体
2. 用 Phobos 面板为每个 Blender 对象指定类型（visual/collision/inertial）
3. 构建 link → joint → link 层级关系
4. 定义惯性参数、关节限位等
5. 导出为 URDF/xacro 包

**优点**：Blender 强大的建模能力 + 完整机器人模型编辑，支持多格式
**缺点**：学习曲线较陡

---

## 方式三：程序化生成（Python）

### 3.1 urdfpy

**安装**：`pip install urdfpy`

**核心 API**：

```python
import urdfpy

# 创建 robot
robot = urdfpy.Robot(name="my_robot")

# 创建 links
base = urdfpy.Link(
    name="base_link",
    visual=urdfpy.Visual(
        geometry=urdfpy.Geometry(box=urdfpy.Box(size=[0.5, 0.5, 0.1])),
        origin=[0, 0, 0.05]
    ),
    inertial=urdfpy.Inertial(
        mass=5.0,
        inertia=[0.1, 0.1, 0.1, 0, 0, 0],
        origin=[0, 0, 0]
    )
)

arm = urdfpy.Link(name="arm_link", ...)

# 创建 joint
joint = urdfpy.Joint(
    name="shoulder",
    parent="base_link",
    child="arm_link",
    joint_type="revolute",
    axis=[0, 0, 1],
    origin=[0, 0, 0.1],
    limit=urdfpy.JointLimit(lower=-1.57, upper=1.57, effort=100)
)

# 组装并导出
robot.add_link(base)
robot.add_link(arm)
robot.add_joint(joint)
robot.to_file("robot.urdf")
```

### 3.2 yourdfpy

`yourdfpy` 是 urdfpy 的现代化替代方案，支持 URDF 加载、可视化和修改。

```python
from yourdfpy import Robot, Link, Joint

# 加载已有 URDF 并修改
robot = Robot.load("base_model.urdf")
robot.scale(0.5)  # 缩放整个模型
robot.save("scaled_model.urdf")
```

### 3.3 onshape-to-robot Python API

```python
from onshape_to_robot import OnshapeRobot

robot = OnshapeRobot(
    document_url="https://cad.onshape.com/documents/xxx",
    api_key="...",
    api_secret="..."
)
robot.export_urdf("output_robot.urdf")
robot.export_stls("meshes/")
```

### 3.4 Build Your Own Generator

对于参数化机器人族（如不同尺寸的机械臂），直接生成 XML 最灵活：

```python
import xml.etree.ElementTree as ET
from xml.dom import minidom

def generate_robot(name, num_legs, leg_length, leg_radius):
    robot = ET.Element("robot", name=name)

    # 生成可重复的腿部结构
    for i in range(num_legs):
        angle = 2 * 3.14159 * i / num_legs
        # ... 创建 link 和 joint 元素
        pass

    return minidom.parseString(
        ET.tostring(robot)
    ).toprettyxml()
```

**优点**：完全参数化、可版本控制、适合生成大量变体
**缺点**：需要编程能力，不如 GUI 直观

---

## 方式四：格式转换

### 4.1 SDF ↔ URDF

Gazebo 的 SDF 与 URDF 结构相似。ROS 提供转换工具：

```bash
# URDF → SDF
gz sdf -p model.urdf > model.sdf

# SDF → URDF（部分支持）
# 手动或用脚本转换，注意 SDF 的部分特性在 URDF 中不支持
```

SDF 与 URDF 的主要差异：
| 特性 | URDF | SDF |
|------|------|-----|
| Joint 连接方式 | 树状（单父节点） | 图状（多父节点可） |
| 传感器 | 有限 | 丰富 |
| 世界描述 | 不支持 | 支持（光照、物理参数） |

### 4.2 MJCF（MuJoCo）↔ URDF

MuJoCo 可直接加载 URDF，也可用 `mj_saveLastXML` 将编译后的模型保存为 MJCF：

```python
import mujoco

# 加载 URDF 到 MuJoCo
model = mujoco.MjModel.from_xml_path("robot.urdf")

# 保存为 MJCF
mujoco.mj_saveLastXML("robot.xml", model)

# 或保存为二进制 MJB（加载更快）
mujoco.mj_saveModel("robot.mjb", model)
```

> MuJoCo 的 URDF 支持有限——复杂模型建议直接用 MJCF。详见 [[MuJoCo-建模]]。

### 4.3 USD（Isaac Sim / Omniverse）→ URDF

NVIDIA Isaac Sim 使用 USD 格式，提供 URDF 导入/导出工具：

```python
# Isaac Sim 中导入 URDF
from omni.isaac.core.utils.stage import add_reference_to_stage
add_reference_to_stage(usd_path="robot.usd", prim_path="/World/Robot")

# URDF → USD 转换
from omni.isaac.core.utils.urdf import URDF  # 或 isaac sim asset converter
```

> Isaac Sim 的 [[🎮 Isaac Sim（USD）& Unity]] 笔记中有关键概念对比。

---

## 方式五：AI 辅助生成

### 5.1 LLM 文本生成

对于简单的教学/原型模型，可以直接向 LLM 描述机器人结构生成 URDF：

```text
Prompt: "生成一个 4 轮差速驱动机器人的 URDF，底盘 0.4m×0.3m×0.1m，
轮子半径 0.05m，有 2 个主动轮和 2 个万向轮，含 LiDAR 传感器 link"
```

**限制**：
- 复杂运动学链可能出错
- 惯性参数通常需要手动调整
- 网格文件（.stl/.dae）仍需外部 CAD 工具生成

### 5.2 Text-to-CAD + URDF

新兴的 AI 辅助工具链：
1. Text-to-CAD（如 Zoo、Cascade）→ 3D 模型
2. 3D 模型 → Phobos/fusion2urdf → URDF

这项技术在快速演进中。详见 [[Text-to-CAD项目深度调研]]。

---

## 方式六：ROS 2 内置 CLI 工具

ROS 2 提供了便捷的命令行工具直接生成 URDF 宏/模板：

```bash
# 创建 URDF 宏（Xacro）
ros2 run xacro xacro model.urdf.xacro > model.urdf

# URDF 教程包（含各种示例模型）
sudo apt install ros-<distro>-urdf-tutorial
ros2 launch urdf_tutorial display.launch.py model:=urdf/01-myfirst.urdf

# robot_state_publisher 发布 URDF 到 TF
ros2 run robot_state_publisher robot_state_publisher --ros-args -p robot_description:="$(xacro robot.urdf.xacro)"
```

---

## 验证与调试

### 必备验证步骤

```bash
# 1. Xacro 语法检查
xacro --check-order model.urdf.xacro

# 2. URDF 结构验证
check_urdf model.urdf

# 3. 可视化检查（RViz）
ros2 launch urdf_tutorial display.launch.py model:=model.urdf

# 4. Gazebo/Isaac Sim 中加载测试
# 确保碰撞网格正常、关节可动、无穿透

# 5. MoveIt Setup Assistant 验证
ros2 launch moveit_setup_assistant setup_assistant.launch.py
```

### 常见问题排查

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 模型不显示 | mesh 路径错误 | 使用 `package://` 路径或绝对路径 |
| 关节不运动 | joint type 或 axis 错误 | 检查 type 和 axis 定义 |
| 模型穿透地面 | 缺少碰撞几何或惯性 | 确保每个 link 有 `<collision>` 和 `<inertial>` |
| 物理发散 | 质量/惯性不合理 | 使用 CAD 自动计算的惯性，避免随手填 |
| `check_urdf` 报错 | XML 结构问题 | 逐段注释排查，先检查 link-joint 树结构 |

### 检查清单

- [ ] 每个 `<link>` 都有 `<inertial>`（至少给 mass 值）
- [ ] 运动学树为无环图（只有一个 root link）
- [ ] mesh 文件路径正确，packages 声明完整
- [ ] joint 的 `<parent>` 和 `<child>` 指向存在的 link
- [ ] `<limit>` 中 effort/velocity 有合理值
- [ ] 无 `<robot>` 外部的游离 link

---

## 工具对比与选择建议

| 场景 | 推荐工具 | 原因 |
|------|----------|------|
| **专业机械设计** | SolidWorks URDF Exporter | 工业标准，Mate→Joint 自动推断 |
| **个人/教育项目** | fusion2urdf | 免费，Fusion 360 Joint 系统好用 |
| **开源/零预算** | FreeCAD URDF + Xacro | 完全免费，社区活跃 |
| **浏览器端协作** | onshape-to-robot | 无需安装软件 |
| **Blender 重度用户** | Phobos | 强大建模 + 完整机器人定义 |
| **参数化机器人族** | Xacro + Python | 编程控制，生成大量变体 |
| **仿真研究** | MJCF（MuJoCo原生） | 功能远超 URDF |
| **ROS 2 入门学习** | 手写 Xacro | 理解底层结构 |
| **快速原型** | LLM 生成 + 手动修正 | 最快出原型 |
| **游戏引擎机器人** | USD → URDF | Isaac Sim / Omniverse 集成 |

> **通用推荐**：Xacro + fusion2urdf / onshape-to-robot 的组合是当前最灵活的方案——CAD 导出模型+网格，Xacro 组装和参数化。

---

## 进阶阅读

- [[MuJoCo-建模]] — MJCF 建模语言详解，与 URDF 对比
- [[MuJoCo-概览]] — MuJoCo 引擎架构与 URDF 加载
- [[开源机器人项目调研-2025-2026]] — 当前主流开源机器人项目的建模实践
- [[Text-to-CAD项目深度调研]] — AI 驱动的 CAD 生成
- [ROS Wiki URDF](https://wiki.ros.org/urdf) — 官方文档
- [Xacro 文档](https://docs.ros.org/en/humble/Tutorials/Intermediate/URDF/Using-Xacro-to-Clean-Up-a-URDF-File.html) — ROS 2 Humble 教程