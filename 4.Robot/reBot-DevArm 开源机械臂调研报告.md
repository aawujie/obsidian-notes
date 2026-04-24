---
title: reBot-DevArm 开源机械臂调研报告
type: concept
created: 2026-04-23
updated: 2026-04-23
sources:
  - GitHub: Seeed-Projects/reBot-DevArm
  - Hackster.io 报道
  - cnx-software 报道
  - Seeed Wiki 文档
tags:
  - 开源机械臂
  - 具身AI
  - LeRobot
  - Pinocchio
  - 遥操作
  - 仿真
---

# reBot-DevArm 开源机械臂调研报告

## 项目概述

| 项目信息 | 详情 |
|----------|------|
| **项目名称** | reBot-DevArm |
| **发起方** | Seeed Studio (矽递科技) — 全球知名开源硬件供应商 |
| **GitHub** | `Seeed-Projects/reBot-DevArm` |
| **创建时间** | 2025-11-25 |
| **最后更新** | 2026-04-23 (活跃开发中) |
| **License** | CC BY-NC-SA 4.0 (非商用，商用需授权) |
| **定位** | 降低具身 AI 学习门槛的开源机械臂 |

项目口号：**"True Open Source"** — 不只开源代码，硬件图纸、BOM、3D 打印文件全部开放。

## 硬件规格

两个版本共享外观设计，电机方案不同：

| 参数 | reBot Arm B601-DM (Damiao 电机) | reBot Arm B601-RS (Robstride 电机) |
|------|------|------|
| **自由度** | 6 DOF + 1 夹爪 | 6 DOF + 1 夹爪 |
| **推荐负载** | 1.5 kg (70% 工作空间内) | 同 |
| **最大臂展** | 650 mm | 同 |
| **重量** | ~4.5 kg | 同 |
| **重复定位精度** | < 0.2 mm | 同 |
| **供电** | DC 24V | 同 |
| **电机方案** | Damiao (达妙) — MIT 模式 | Robstride — CAN 通信 |
| **开源进度** | STEP/BOM/性能测试 ✅ 完成 | STEP/BOM 🚧 进行中 |

### 关键设计特点

- **无内置控制器**：USB-CAN 板连接外部主机 (Jetson / PC)
- **MIT 模式**：支持位置+速度+力矩混合控制，单 CAN 包发送
- **深度相机兼容**：Intel D435i / D405 / Gemini 305 / Gemini 2 (配件支架已开源)
- **Leader Arm 兼容**：Star Arm 102-LD 可作为遥操作主臂

## 软件生态

| 生态 | DM 版状态 | RS 版状态 | 说明 |
|------|------|------|------|
| **Python SDK (MotorBridge)** | ✅ 持续优化 | ✅ | 统一多品牌电机 API |
| **ROS1** | ✅ | ⏳ | |
| **ROS2 (Humble)** | 🚧 进行中 | ⏳ | MoveIt2 优化中 |
| **LeRobot (HF)** | ✅ 完成 | ⏳ | HuggingFace 机器人学习框架 |
| **Pinocchio** | ✅ 完成 | ⏳ | 正/逆运动学 + 重力补偿 |
| **Isaac Sim** | 🚧 进行中 | ⏳ | USD 模型导入 + 仿真遥操作 |
| **深度相机抓取** | ✅ 完成 | ⏳ | YOLO + 深度相机视觉抓取 |
| **免费课程** | ⏳ 规划中 | ⏳ | |

## 仿真环境现状（重点评估）

**官方目前真正可用（✅ Completed）的只有 Pinocchio + MeshCat，但它不是仿真器，只是动力学数学库。**

| | Pinocchio | MuJoCo / Isaac Sim |
|---|---|---|
| **本质** | 数学计算库 | 物理仿真器 |
| **能做什么** | 算运动学、动力学方程 | 模拟碰撞、摩擦、重力、接触 |
| **有虚拟世界吗** | ❌ 没有 | ✅ 有完整3D物理世界 |
| **能跑RL吗** | ❌ 不行（没有环境） | ✅ 可以 |
| **可视化** | MeshCat 只是看骨骼 | 完整场景渲染 |

- **Pinocchio**：INRIA (法国国家信息与自动化研究所) 开发，Justin Carpentier 等人，BSD-2-Clause 开源。正/逆运动学求解、轨迹规划、重力补偿。MeshCat 可视化仅骨骼线框，无碰撞/物理环境。
- **Isaac Sim**：官方 🚧 进行中，预计 2026.04.20 但已延迟，尚未发布。
- **MuJoCo**：❌ 官方无任何计划，roadmap 中未提及。

### Pinocchio 来源说明

Pinocchio 不是仿真环境/虚拟世界，而是机器人动力学计算库（C++ 核心 + Python 绑定），类似于机器人的"数学引擎"。由 INRIA Paris 的 GRAPH team (Geometric and Robotic Algorithms team) 维护。Justin Carpentier 同时也是 Hugging Face LeRobot 的核心贡献者。

## 价格与购买

| Kit 选项 | 价格区间 |
|----------|----------|
| **Arm Body Motor Kit** (仅电机+线束) | — |
| **Arm Body Structural Kit** (仅结构件) | — |
| **Gripper Complete Kit** (夹爪全套) | — |
| **Full Kit** (本体+夹爪全套) | DIY ~$1,000 |
| **Pre-assembled** (成品) | ~$1,510 |
| **Star Arm 102-LD** (Leader Arm) | 单独购买 |

## 竞品对比

| 系统 | 价格 | DOF | 负载 | 精度 | 开源程度 | 特点 |
|------|------|-----|------|------|------|------|
| **reBot B601-DM** | ~$1,000 DIY / $1,510 成品 | 6+1 | 1.5 kg | <0.2mm | 硬件+软件全开源 | Seeed 供应链，多电机兼容 |
| **SO-ARM100** | ~$100 | 6 | 低负载 | 低 | 全开源 | 超低成本入门，塑料结构件 |
| **ALOHA (DIY)** | ~$20,500-22,700 | 双臂 14-DOF | 中等 | 中 | 开源 | 双臂协同，社区大 |
| **OpenArm DK1** | ~$12,000 | 双臂 | 高扭矩 | 高 | 开源 | 成品发货，ALOHA 兼容 |
| **OpenArm 101** | ~$4,500 | 单臂 | — | — | 开源 | 低成本单臂入口 |

## 仓库结构

```
reBot-DevArm/
├── README.md / zh / JP / Fr / es
├── LICENSE (CC BY-NC-SA 4.0)
├── hardware/
│   ├── reBot_B601_DM/
│   │   ├── 3D_Printed_Parts/        # 3D打印件 STEP 文件
│   │   ├── Metal_Parts/             # 钣金件 STEP 文件
│   │   ├── Purchased_Parts/         # 外购件清单 + 采购链接
│   │   ├── performance_testing/     # 性能测试参考
│   │   ├── reBot_B601_DM_v1.0_20260331.step  # 整机 STEP (~50MB)
│   │   └── readme.md / zh / jp / fr / es
│   └── reBot_B601_RS/              # RS 版 (进行中)
├── media/                           # 图片资源
```

## License 与商用风险

**CC BY-NC-SA 4.0** = 非商用许可：

| 活动 | 是否允许 |
|------|------|
| 个人学习/研究 | ✅ 允许 |
| 开发应用软件出售 | ✅ 可联系授权 |
| 开设付费课程 | ✅ 可联系授权 |
| 改壳换标销售 | ❌ 禁止 |
| 商用授权申请 | 联系 elaine.wu@seeed.cc |

## 核心结论

### 项目本质

reBot 的核心卖点是 **硬件全开源**（STEP 模型、BOM、采购链接、组装视频）。Seeed 是硬件公司，商业模式是卖机械臂套件 + 配件（Jetson、深度相机、Leader Arm）。软件生态尤其是仿真，基本是半成品。

### 无硬件仿真路径

| 方案 | 状态 | 能做什么 | 门槛 |
|------|------|------|------|
| Pinocchio + MeshCat | ✅ 可用 | 运动学计算、轨迹规划 | 低，纯 Python |
| LeRobot 内置仿真 | ✅ 可用 | 模仿学习训练 | 低 |
| URDF → MuJoCo 自建 | ❌ 需自做 | 完整 RL 训练环境 | 中，1-2天 |
| Isaac Sim | 🚧 未发布 | GPU 加速仿真 | 高，需 NVIDIA GPU |

**自建 MuJoCo 路径**：reBotArm_control_py 仓库已有 URDF 文件，可通过 `mujoco compile model.urdf` 自动生成 MJCF，但需手动调参（碰撞几何、关节阻尼、执行器配置）。

### 优势与不足

**优势**：
1. 全栈开源：硬件+软件+文档+BOM+采购链接，真正可复现
2. 精度领先：0.2mm 重复定位精度在同价位出色
3. 多电机兼容：MotorBridge SDK 统一 6+ 品牌电机
4. 供应链保障：Seeed Studio 全球供货
5. 性价比：$1,000 DIY 成本在 1.5kg 负载级别极具竞争力

**不足**：
1. License 非商用：CC BY-NC-SA 4.0 限制商用
2. RS 版滞后：多数功能还在规划中
3. ROS2/Isaac Sim 未完成：核心生态仍在开发
4. 单臂设计：不支持双臂协同
5. 无内置控制器：需额外 Jetson/PC + USB-CAN
6. 仿真严重不足：官方无真正的物理仿真环境，MuJoCo 无计划
7. 社区规模尚小：项目仅 5 个月

## 相关链接

- GitHub: https://github.com/Seeed-Projects/reBot-DevArm
- reBotArm_control_py (Pinocchio): https://github.com/vectorBH6/reBotArm_control_py
- Seeed Wiki: https://wiki.seeedstudio.com/robotics_page/
- LeRobot 教程: https://wiki.seeedstudio.com/rebot_arm_b601_dm_lerobot/
- Pinocchio 教程: https://wiki.seeedstudio.com/rebot_arm_b601_dm_pinocchio_meshcat/
- 购买: https://www.seeedstudio.com/reBot-Arm-B601-DM-Bundle.html