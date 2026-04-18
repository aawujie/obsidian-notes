---
notion-id: 2e478d23-e296-80fe-991b-d03de0952764
---
> 云服务：[https://cloud.tencent.com/developer/article/2613158?referrer=grok.com](https://cloud.tencent.com/developer/article/2613158?referrer=grok.com)

![[imgs/image 238.png]]

| 项目 | NVIDIA OSMO | GitLab CI/CD (DevOps 平台) |
| --- | --- | --- |
| **主要用途** | 物理 AI / 机器人端到端工作流编排（合成数据生成 → 训练 → 模拟 → SIL/HIL 测试 → sim-to-real） | 通用软件开发 CI/CD：代码构建、测试、部署、代码审查、仓库管理 |
| **目标领域** | 专为机器人、人形机器人、自动驾驶、工业自动化（Physical AI）深度优化 | 通用软件工程、Web/App、ML 模型Ops，但非机器人专用 |
| **核心抽象层** | YAML 定义**多阶段、多容器、异构计算**的复杂 pipeline（无代码/低代码） | .gitlab-ci.yml 定义 job/stage，重点在构建/测试/部署脚本 |
| **计算环境支持** | 异构强：x86/Arm/Jetson/多 GPU 集群/云/边缘/混合，本地到云无缝 | 支持 GPU runner（GitLab.com 有 T4 等），但需手动配置 runner，异构弱 |
| **机器人痛点解决** | 直接解决 **“三台电脑问题”（训练 GPU + 模拟大算力 + 边缘实机）**，自动调度 Isaac Sim/Isaac Lab/GR00T 等 | 可跑 Jetson 测试，但需自己写脚本管理模拟/数据血统/大规模并行 |
| **数据血统/可重现** | 内置强：数据 lineage、版本追踪、审计、安全（OIDC、key rotation） | 基本依赖外部工具（如 DVC、MLflow） |
| **与 CI/CD 关系** | **可集成到 GitLab/GitHub CI** 中，作为子任务调度大规模物理 AI 负载（夜跑回归、benchmark） | 本身就是 CI/CD 主平台，可触发 OSMO 任务 |
| **上手难度** | YAML 写流程，几乎无 K8s 经验也能用（抽象底层） | YAML 写 job，但大规模 GPU/异构需 DevOps 经验 |
| **典型用户** | 机器人团队（Hexagon、NEURA、Figure AI 等） | 软件/DevOps 团队，也支持一些 ML，但机器人专用弱 |
| **开源/获取** | GitHub 开源（[https://github.com/NVIDIA/OSMO](https://github.com/NVIDIA/OSMO)），免费本地/云部署 | GitLab 开源版 + SaaS，GPU runner 需 Premium/Ultimate |

| Stage | 阶段名称（典型叫法） | 主要工具 / 容器镜像 | 具体做了什么 | 输入 → 输出 | 算力偏好 |
| --- | --- | --- | --- | --- | --- |
| 1 | 真实场景重建（**Real-to-Asset**） | NVIDIA **NuRec** + **3DGUT** | 用手机拍照片/视频 → 重建成 3D Gaussian Splats + collider mesh → 导出 USD | 真实照片/视频 → **USD 资产文件** | RTX 工作站 / 云 GPU |
| 2 | 场景导入 & 仿真环境搭建 | **Isaac Sim **(nvcr.io/nvidia/isaac-sim) | 导入 USD → 加机器人、物理（PhysX）、传感器 → 构建可交互仿真环境 | USD 资产 → 完整仿真 stage | RTX Pro / L40 多 GPU |
| 3 | 大规模合成数据生成（SDG） | Isaac Sim + **MobilityGen** / **Replicator** | 跑随机/控制轨迹 → 生成 RGB、深度、语义、占用地图等合成数据（headless 模式） | 仿真环境 → **大量合成视频/数据集** | 大规模 GPU 集群 |
| 4 | 数据增强 / Sim-to-Real 风格转移 | NVIDIA **Cosmos Transfer** (cosmos-transfer:latest) | **用 diffusion 模型 + prompt**（如“rainy night”）**对合成视频做 photorealistic 增强，缩小 sim-real 差距** | 合成视频 → **更真实风格的增强视频/数据** | 高端 GPU (A100/H100) |
| 5 | 模型/策略训练 | PyTorch (nvcr.io/nvidia/pytorch) 或 Isaac Lab | 用增强后的合成数据**训练视觉/运动/强化学习策略**（GR00T、模仿学习等） | 增强数据集 → **训练好的模型 checkpoint** | 训练集群 (H100/GB200) |
| 6 | 评估 / 验证（SIL/HIL） | Isaac Sim (SIL) + 自定义 ROS/Jetson 容器 | 软件在环**（SIL）**：模型回仿真验证；硬件在环**（HIL）**：部署到 Jetson 实机测试 | 训练模型 → 性能指标 / benchmark 报告 | 混合：云 + 边缘 Jetson |

## NVIDIA Isaac Sim

> [https://docs.isaacsim.omniverse.nvidia.com/latest/index.html](https://docs.isaacsim.omniverse.nvidia.com/latest/index.html)

![[imgs/image 239.png]]

从设计、训练、调优到部署的完整机器人开发工作流

---

### 🎨 **Design（设计环节）**

这部分负责定义机器人的**数字模型与仿真环境**，是开发的起点。

- **CAD**：计算机辅助设计，用于创建机器人的三维几何模型。
- **MJCF**：**MuJoCo 场景描述格式**，用来**定义机器人的关节、连杆和运动学结构**，是仿真环境的核心配置文件。
- **USD**：**通用场景描述格式**，用于整合不同工具创建的模型，支持复杂场景的跨平台协作。
- **URDF**：**统一机器人描述格式**，ROS 生态中定义机器人结构的标准格式，包含连杆、关节、传感器等信息。

---

### 🛠️ **Tune（调优环节）**

这部分负责在仿真环境中**训练机器人**的智能行为。

- **Sensors**：传感器模型，在仿真中模拟摄像头、激光雷达、IMU 等传感器，让虚拟机器人具备感知能力。
- **RTX - Ray Tracing Texel eXtreme**：NVIDIA **实时光线追踪技术**，用于生成高真实感的虚拟环境，提升仿真的视觉保真度。
- **PhysX - Physics Acceleration**：NVIDIA 物理引擎，用于**模拟机器人与环境的碰撞、摩擦等**物理交互，让虚拟运动更贴近现实。

---

### 🔬 **Train（训练环节）**

这部分负责优化机器人的控制策略与算法性能。

- **Isaac Lab**：NVIDIA 推出的**机器人学习与仿真框架**，提供了大量**预定义的机器人任务和环境**，可快速开展强化学习研究。
- **RL**：强化学习，通过智能体与环境的交互，让机器人自主学习最优动作策略，常用于复杂的运动控制任务。
- **Replicator**：NVIDIA **数据生成工具**，可生成大规模、多样化的合成数据集，用于训练和验证感知算法。

---

### 🚀 **Deploy（部署环节）**

这部分负责将训练好的模型与算法部署到真实机器人或应用中。

- **ROS**：机器人操作系统，提供了硬件抽象、设备驱动、通信框架等功能，是连接算法与实体机器人的桥梁。
- **Local App**：本地应用程序，用于在机器人本地运行控制逻辑或用户交互界面。
- **Database**：数据库，用于存储机器人运行过程中产生的感知数据、日志和模型参数。
- **Cloud**：云端服务，可提供大规模计算资源，用于在线训练、远程监控和数据备份。

---

![[imgs/image 240.png]]

## **Cosmos Transfer** 

1. **它是啥？**
一个**世界到世界转移模型**（world-to-world transfer model），基于扩散模型（diffusion-based），专门把“结构化但不够真实”的视频/数据，转成**照片级真实**的高保真视频。
2. **主要干嘛？**
解决物理 AI 的最大痛点：**sim-to-real 差距**。拿 Isaac Sim 等模拟器生成的“干净但卡通式”合成数据（RGB + 深度 + 分割等），通过文本 prompt（如“rainy night urban”）和多模态控制（深度图、分割图、边缘图等），生成多样化、真实风格的版本，同时**完美保留**物理结构、机器人运动轨迹、物体布局不变。
3. **关键优势（为什么牛）**
    - 多控制（multi-controlnet）：可以精细调节每个控制信号的权重，避免幻觉（hallucination），物理一致性超强。
    - 比单纯的风格转移更高级：不只换背景，还能变天气、光照、材质、时间段等，极大增加数据多样性。
    - 体积小、效率高（2.5 版比前代小 3.5 倍，但质量更好、prompt 遵守度更高）。
4. **在 pipeline 里怎么用？**
典型位置：在 Isaac Sim 生成物理精确合成数据后，作为下一步用 Cosmos Transfer 做**光真实增强**（photorealistic augmentation），然后喂给模型训练。配合 **OSMO** 可以大规模自动化跑（YAML 一键调度几千个变体）。
5. **一句话总结**
**Cosmos Transfer 就是模拟数据的“真实美颜师 + 变装大师”**：让卡通模拟瞬间变真实世界样子，保留所有物理逻辑，帮助机器人/自动驾驶模型从模拟直接跳到真实部署，性能大幅提升！

对比其他 Cosmos 家族成员：

- **Cosmos Predict**：从零生成新视频（预测未来帧，像“造世界”）。
- **Cosmos Reason**：看视频/图像后推理和理解（像“物理 AI 的 ChatGPT”）。
- **Transfer**：专攻已有视频的“真实升级 + 多样化”。

开源地址：[https://github.com/nvidia-cosmos/cosmos-transfer2.5](https://github.com/nvidia-cosmos/cosmos-transfer2.5)

## **MobilityGen & Replicator**

**MobilityGen 和 Replicator** 都是 **NVIDIA Isaac Sim** 内置/扩展的**合成数据生成（Synthetic Data Generation, SDG）工具**，但它们专注领域和使用场景完全不同。

6. **MobilityGen 是啥？**
一个专为**移动机器人（mobile robots）设计的数据采集工具集**（toolset/workflow），**内置在 Isaac Sim 扩展**（isaacsim.replicator.mobility_gen）。
核心输出：**机器人运动轨迹 + 占用地图（occupancy maps） + 传感器数据**（RGB、深度、关节位置/速度、姿态等），用于训练**导航、机动性（mobility）策略**。
7. **Replicator 是啥？**
Isaac Sim 的**通用感知数据生成框架**（Perception Data Generation），基于 omni.replicator 扩展。
核心输出：**大规模随机化图像/视频 + 丰富标注**（bounding box、语义分割、实例分割、深度、COCO/KITTI 格式等），用于训练**视觉感知模型**（物体检测、分割、姿态估计等）。
8. **主要区别（功能侧重）**
    - **MobilityGen**：专注**机器人本体运动 & 环境交互**数据（如轨迹生成、碰撞避免、占用地图、随机路径跟随）。支持手动遥操（键盘/手柄）或自动（随机加速度/路径），特别适合**差速轮、 quadruped、四足、人形**等多种机器人形态。
    - **Replicator**：专注**场景/物体随机化**（domain randomization）：光照、反射、颜色、位置、纹理随机变化，生成**高多样性感知数据**，更适合**视觉任务**（CV 模型训练），而非运动轨迹。
9. **典型使用场景 & 输出示例**
    - **MobilityGen**：仓库 AMR/人形机器人导航训练 → 生成 occupancy map + 机器人视角 RGB/深度 + 轨迹数据 → 喂给强化学习/模仿学习训练 mobility policy。
（常与 Cosmos Transfer 结合：**先用 MobilityGen 产生结构化运动数据，再增强成 photorealistic 视频**。）
    - **Replicator**：物体检测/语义分割训练 → 随机摆放物体 + 随机光照/背景 → 输出带精确标注的图像数据集（COCO 格式）。
更通用，常用于 perception-only 任务。
10. **在 pipeline 里的位置（与 OSMO 配合）**
    - 两者都可作为 **Isaac Sim** 的 stage 被 **OSMO** 调度（YAML 一键大规模跑）。
    - 主流流程：**NuRec 重建场景 → MobilityGen 生成运动轨迹/占用数据（Stage 3） → Cosmos Transfer 增强视觉真实性 → 训练。**
    - Replicator 常用于更早的**感知数据**生成，或**独立跑视觉** SDG。
    - 官方推荐：MobilityGen 更适合**物理 AI / 机器人机动性**项目，Replicator 更适合**传统 CV 数据**工厂。

**MobilityGen = “机器人怎么动”的数据专家**（轨迹 + 占用 + 运动状态，专治导航/ locomotion）。

**Replicator = “机器人看到啥”的数据专家**（随机化图像 + 标注，专治 perception）。

MobilityGen 文档：[https://docs.isaacsim.omniverse.nvidia.com/latest/synthetic_data_generation/tutorial_replicator_mobility_gen.html](https://docs.isaacsim.omniverse.nvidia.com/latest/synthetic_data_generation/tutorial_replicator_mobility_gen.html)

Replicator 文档：[https://docs.isaacsim.omniverse.nvidia.com/latest/replicator_tutorials/index.html](https://docs.isaacsim.omniverse.nvidia.com/latest/replicator_tutorials/index.html)

## **Omniverse Nucleus**

**Omniverse Nucleus** 是 NVIDIA 的云存储服务，**用于存储和共享大型文件**（如 3D 模型、机器人资产、神经网络模型等）。它是 NVIDIA Omniverse 平台的一部分。

**主要特点：**

11. 云端存储：资产存储在云端（AWS S3），而不是本地代码库
    - 减少代码库体积
    - 便于分发和共享资产
12. 在 Isaac Lab 中的作用：
    - 存储机器人模型（USD 文件）
    - 存储执行器网络模型（如 anydrive_3_lstm_jit.pt）
    - 存储策略文件、材质、对象等
13. 访问方式：
    - 通过 ISAACLAB_NUCLEUS_DIR 路径访问
    - 首次使用时从云端下载
    - 支持本地缓存以加速后续访问

**重要变化：**

**从 Isaac Sim 4.5 开始，Omniverse Nucleus 服务器已被弃用。现在资产通过 AWS S3 提供，并使用 Hub 进行本地缓存管理。**

**对于你的文件：**

ActuatorNets/ANYbotics/anydrive_3_lstm_jit.pt 存储在云端服务器上。当你运行代码时：

- 如果文件已缓存，会从本地缓存加载
- 如果未缓存，会从云端下载（首次运行可能较慢）

**如何查看/管理缓存：**

14. 启动 Isaac Sim 应用
15. 在右上角找到 CACHE: 图标
16. 点击启用 Hub 来管理本地缓存

## NVIDIA Brev

NVIDIA Brev（以前叫 Brev.dev）是 NVIDIA 在 2024 年收购的一个云端 AI/ML 开发平台，专为开发者提供一键式 GPU 沙盒环境，**让你快速运行、构建、训练、部署和扩展 AI 模型（包括物理 AI / 机器人项目）。它不是硬件，而是“GPU 容量聚合器 + 自动化配置工具”，跨多家云提供商（AWS、GCP、Azure 等）找最优 GPU 资源，省去繁琐的基础设施管理**。

**核心功能（为什么适合 Isaac Sim / OSMO 用户）**

- **一键启动 GPU 实例**：选 GPU（如 L40S、A100、H100），自动装好 CUDA、Python、Docker、Jupyter、VSCode 等，几分钟内就绪。
- **Launchables**：预配置“配方”（代码 + 容器 + 计算），一键部署完整环境。官方有 **Isaac Sim + Isaac Lab Launchable**（GitHub: isaac-sim/isaac-launchable），直接跑模拟、合成数据生成、训练，而不用自己拉容器。
- **跨云无缝**：聚合多家云，自动找便宜/可用 GPU；支持 VM 模式、容器模式、Docker Compose。
- **与 NVIDIA 生态深度集成**：直接拉 NGC 容器（nvcr.io/nvidia/isaac-sim），跑 OSMO pipeline、Cosmos Transfer、MobilityGen 等；适合大规模 SDG（合成数据生成）和机器人 benchmark。
- **监控 & 扩展**：实时 dashboard、SSH 访问、自动关机省钱；可 hook 到 OSMO YAML 作为计算后端。

官方文档：[https://docs.nvidia.com/brev/latest/](https://docs.nvidia.com/brev/latest/)
Isaac Sim on Brev 指南：[https://docs.isaacsim.omniverse.nvidia.com/5.0.0/installation/install_advanced_cloud_setup_brev.html](https://docs.isaacsim.omniverse.nvidia.com/5.0.0/installation/install_advanced_cloud_setup_brev.html)

## GR00T

NVIDIA 的 GR00T（全称 **Generalist Robot 00 Technology**，常写成 Project GR00T 或 Isaac GR00T）是 NVIDIA 为通用人形机器人（humanoid robots）推出的开源基础模型平台，被誉为“人形机器人的 ChatGPT 时刻”。它旨在让机器人具备类人推理、理解自然语言、模仿人类动作、快速适应新环境的能力，推动物理 AI 从实验室走向实际部署。

**核心是什么？**

Isaac GR00T 是一个开放的视觉-语言-动作（VLA）基础模型，专为人形机器人设计，能从多模态输入（摄像头视觉、机器人状态、自然语言指令）生成全身协调动作，支持跨不同机器人形态（cross-embodiment）迁移。

**最新版本（2026 年 1 月 CES 刚发布）**

- **Isaac GR00T N1.6**：当前主力版本（几天前发布），增强了：
    - **全身控制**（full body control）：机器人能同时移动、抓取物体、处理复杂交互。
    - **推理能力**：集成 Cosmos Reason 作为“大脑”，支持多步规划、理解复杂指令。
    - **多模态输入**：ego-centric 摄像头流 + 机器人关节状态 + 语言提示。
- 开源可用：GitHub（[https://github.com/NVIDIA/Isaac-GR00T](https://github.com/NVIDIA/Isaac-GR00T?referrer=grok.com)）和 Hugging Face 上可下载模型权重，完全可自定义微调。

**主要功能与优势**

- **通用性**：不像传统机器人策略只针对特定任务，GR00T 是“generalist”模型，能处理多样化任务（如仓库捡物、家庭助手、工业协作）。
- **训练方式**：大量用合成数据（Isaac Sim + MobilityGen + Cosmos Transfer 生成）+ 真实数据，结合 sim-to-real 转移，性能强。
- **与 NVIDIA 生态深度集成**：
    - **Isaac Sim / Lab**：模拟训练、基准测试。
    - **OSMO**：大规模 pipeline 调度（合成数据 → 训练 GR00T → 验证）。
    - **Cosmos**：提供世界理解和数据增强。
- **实际应用**：已被 Franka Robotics、NEURA Robotics、Humanoid 等公司用于开发下一代机器人，支持模拟-训练-验证-部署全流程。