# Unitree G1 WBT Dataset 深度调研报告

> 调研时间：2026-03-31  
> 数据来源：Hugging Face、GitHub、Unitree 官方  
> 标签：#机器人 #人形机器人 #数据集 #模仿学习 #遥操作

---

## 1. 概述

**UnifoLM-WBT-Dataset** 是 Unitree Robotics 发布的开源全身遥操作（Whole-Body Teleoperation）数据集集合，专为 **Unitree G1 人形机器人** 设计。该数据集用于训练视觉-语言-动作（VLA）模型，支持复杂的全身移动操作任务。

### 核心特点
- **真实机器人数据**：全部来自真实 G1 机器人遥操作录制，非仿真数据
- **全身协调**：同时包含上肢操作 + 下肢移动的数据
- **LeRobot 格式**：采用 Hugging Face LeRobot V2.1 标准格式
- **Apache 2.0 开源**：可自由用于研究和商业用途

---

## 2. 数据集构成

### 2.1 数据集列表（8个子集）

| 数据集名称 | 规模 | 遥操作设备 | 任务描述 | 视角 |
|-----------|------|-----------|---------|------|
| G1_WBT_Inspire_Put_Clothes_into_Washing_Machine | 486k | Inspire | 衣物放入洗衣机 | 多视角 |
| G1_WBT_Brainco_Make_The_Bed | 207k | Brainco | 铺床整理 | 多视角 |
| G1_WBT_Inspire_Put_Clothes_Into_Basket | 228k | Inspire | 衣物放入篮子 | 多视角 |
| G1_WBT_Brainco_Collect_Plates_Into_Dishwasher | 427k | Brainco | 盘子放入洗碗机 | 多视角 |
| G1_WBT_Inspire_Pickup_Pillow_MainCamOnly | 157k | Inspire | 拾取枕头 | 主摄单视角 |
| G1_WBT_Inspire_Collect_Clothes_MainCamOnly | 89.1k | Inspire | 收集衣物 | 主摄单视角 |
| G1_WBT_Inspire_Put_Clothes_into_Washing_Machine_MainCamOnly | 119k | Inspire | 衣物放入洗衣机 | 主摄单视角 |
| G1_WBT_Brainco_Pickup_Pillow | 178k | Brainco | 拾取枕头 | 多视角 |

### 2.2 数据格式详情

**存储格式**：Apache Parquet

**数据字段结构**：
```
observation.state.ee_state      # 末端执行器状态 (12维)
observation.state.hand_state    # 手部状态 (12维)
observation.state.robot_q_current # 机器人关节当前位置
action.ee_action                # 末端执行器动作指令
action.hand_cmd                 # 手部控制指令
action.robot_q_desired          # 期望关节位置
timestamp                       # 时间戳
frame_index                     # 帧索引
episode_index                   # 片段索引
task_index                      # 任务索引
```

**单条数据示例**（末端执行器状态）：
```python
[0.048, 0.224, -0.114, 0.859, 1.073, 0.527,  # 位置+姿态
 0.065, -0.218, -0.111, -1.052, 1.069, -0.674]  # 旋转矩阵/四元数
```

**手部状态示例**（12维）：
```python
[0.899, 0.900, 0.899, 0.900, 0.800, 0,  # 左手
 0.899, 0.900, 0.900, 0.899, 0.799, 0]   # 右手
```

---

## 3. 遥操作设备对比

### 3.1 Inspire 手套
- **类型**：数据手套式遥操作
- **特点**：高精度手指追踪，适合精细操作
- **适用任务**：衣物处理、枕头抓取等柔性物体操作

### 3.2 Brainco 设备
- **类型**：脑机接口/肌电信号设备
- **特点**：意念控制，低延迟
- **适用任务**：铺床、洗碗等需要协调性的任务

---

## 4. 技术生态

### 4.1 数据采集流程

```
Apple Vision Pro (视觉)
        ↓
  avp_teleoperate (遥操作)
        ↓
  OpenWBC/OpenHomie (全身控制)
        ↓
  G1 Robot (执行)
        ↓
  JSON 格式存储
        ↓
  OpenWBC_to_LeRobot (格式转换)
        ↓
  LeRobot V2.1 格式
```

### 4.2 相关开源项目

| 项目 | 用途 | 链接 |
|-----|------|------|
| unitree_il_lerobot | 基于 LeRobot 的训练框架 | [GitHub](https://github.com/unitreerobotics/unitree_lerobot) |
| avp_teleoperate | Apple Vision Pro 遥操作 | [GitHub](https://github.com/unitreerobotics/avp_teleoperate) |
| OpenWBC | 全身控制与数据采集 | [GitHub](https://github.com/jiachengliu3/OpenWBC) |
| OpenHomie | 下肢运动算法 | [GitHub](https://github.com/OpenRobotLab/OpenHomie) |
| unitree_sim_isaaclab | IsaacLab 仿真环境 | [GitHub](https://github.com/unitreerobotics/unitree_sim_isaaclab) |
| any4lerobot | 数据集格式转换工具 | [GitHub](https://github.com/Tavish9/any4lerobot) |

### 4.3 支持的算法

- **Diffusion Policy (DP)**：扩散策略
- **ACT** (Action Chunking with Transformers)
- **PI0.5** / **π₀.5**
- **GROOT** (NVIDIA)
- **GR00T N1.5** (NVIDIA Isaac GR00T)

---

## 5. 应用场景

### 5.1 家庭生活任务
- 洗衣：收集衣物 → 放入洗衣机
- 整理：铺床、叠被
- 清洁：收拾盘子、放入洗碗机
- 收纳：物品分类、放入篮子

### 5.2 研究用途
- **模仿学习** (Imitation Learning)
- **视觉-语言-动作模型** (VLA)
- **全身协调控制**
- **移动操作** (Mobile Manipulation)

---

## 6. 使用指南

### 6.1 加载数据集

```python
from lerobot.datasets.lerobot_dataset import LeRobotDataset

# 加载数据集
dataset = LeRobotDataset(
    repo_id="unitreerobotics/G1_WBT_Inspire_Put_Clothes_into_Washing_Machine"
)

# 获取指定片段
episode_index = 1
from_idx = dataset.meta.episodes["dataset_from_index"][episode_index]
to_idx = dataset.meta.episodes["dataset_to_index"][episode_index]

# 遍历数据
for step_idx in range(from_idx, to_idx):
    step = dataset[step_idx]
    # step 包含 observation, action, timestamp 等
```

### 6.2 可视化数据

```bash
cd unitree_lerobot/lerobot

python src/lerobot/scripts/lerobot_dataset_viz.py \
    --repo-id unitreerobotics/G1_WBT_Inspire_Put_Clothes_into_Washing_Machine \
    --episode-index 0
```

---

## 7. 数据特点分析

### 7.1 规模统计
- **总数据量**：约 189 万帧（8个数据集合计）
- **单片段长度**：约 30 秒（@ 30Hz）
- **分辨率**：最高 256x256（视频）
- **频率**：30Hz 控制频率

### 7.2 数据质量
- **真实场景**：真实家庭环境录制
- **多样性**：不同光照、背景、物体摆放
- **全身协调**：上肢操作与下肢移动同步
- **多模态**：视觉 + 本体感觉 + 动作指令

### 7.3 与仿真数据对比

| 维度 | WBT 真实数据 | 仿真数据 |
|-----|-------------|---------|
| 真实性 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| 多样性 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 采集成本 | 高 | 低 |
| 安全性 | 需实体机器人 | 无风险 |
| sim-to-real 差距 | 无 | 存在 |

---

## 8. 相关论文/项目

- **TrajBooster** (ICRA 2026)：基于轨迹中心的 VLA 增强方法
- **UniTracker**：通用全身运动追踪器
- **AMO** (Adaptive Motion Optimization)：超灵巧人形全身控制

---

## 9. 总结与建议

### 优势
1. **真实机器人数据**：直接用于真实 G1 部署
2. **全身协调**：同时学习移动和操作
3. **家庭场景**：贴近实际应用需求
4. **完整生态**：从采集到训练到部署的完整工具链

### 局限
1. **数据量相对较小**：单任务 90k-486k 帧，可能需要更多数据
2. **单机器人平台**：仅针对 G1，迁移性有限
3. **特定遥操作设备**：Inspire/Brainco 特定

### 使用建议
- 适合作为 **VLA 预训练** 数据
- 可与 **仿真数据混合** 使用
- 建议配合 **数据增强** 技术
- 用于 **全身移动操作** 任务研究

---

## 参考链接

- **数据集主页**：https://huggingface.co/collections/unitreerobotics/unifolm-wbt-dataset
- **Unitree 开源页面**：https://www.unitree.com/mobile/opensource/
- **LeRobot 文档**：https://github.com/huggingface/lerobot
- **OpenWBC 项目**：https://github.com/jiachengliu3/OpenWBC

---

*报告生成时间：2026-03-31*  
*调研工具：OpenClaw Web Search + Web Fetch*
