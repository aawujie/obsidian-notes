# 4.Robot 知识库索引

> 机器人 / 具身智能 — 控制算法、深度强化学习、大模型应用、调研报告

## 目录结构

```
4.Robot/
├── Control/              物理仿真人形控制、TeleHuman
├── DRL/                  深度强化学习笔记、KungfuBot
├── ML&DL/                大模型方向 Arxiv 周报、GVHMR、Kronos 等
└── 根目录                全身控制知识点、MuJoCo课程、Unitree调研
```

---

## Control — 物理仿真控制

- [[PBHC 基于物理的人形机器人控制]] — Physics-Based Humanoid Control
- [[TeleHuman]] — Teleoperation / 人形遥操作

## DRL — 深度强化学习

- [[RL_学习笔记]] — RL 基础学习笔记
- [[RL_学习笔记_整理版]] — RL 笔记整理版
- [[PBHC - KungfuBot 物理人形全身控制]] — KungfuBot 物理人形 DRL

## ML&DL — 大模型与深度学习

### Arxiv 周报 (大模型方向)

> 2024年10月—2025年1月的 LLM/Agent/Multimodal 周报，约 50 篇

#### 20241004-20241010 (6 篇)
- [[精准思考，智能分配算力]] — 算力分配
- [[利用 KG-RAG 提升病理解释性能，并保护隐私]] — KG-RAG
- [[零额外推理开销，提升RAG性能！]] — RAG 优化
- [[重要性采样，解锁Token级偏好对齐]] — Token级对齐
- [[TableRAG：让大模型轻松驾驭大规模表格数据]] — TableRAG
- [[TOOLGEN：探索Agent工具调用新范式！]] — Agent 工具调用

#### 20241011-20241017 (6 篇)
- [[北大 Parenting 方法登场]] — 参数魔法检索增强
- [[打破选择困局：多智能体带你高效选择预训练数据]] — 数据选择
- [[谷歌联合CMU提出超强奖励模型]] — 奖励模型
- [[自回归奖励模型让 LLM 对齐不再困难！]] — 自回归对齐
- [[Talker-Reasoner]] — Nobel Economics + LLM
- [[TPO：平民版 OpenAI-O1]] — 思维能力

#### 20241018-20241024 (7 篇)
- [[普林斯顿大学提出 TreeBoN]] — 推理效能提升
- [[DeepSeek最新多模态大模型]] — 多模态理解与生成
- [[LongRAG]] — 长文本问答导航
- [[NetSafe]] — 多智能体网络安全
- [[SSO：无需人工标注，自动对齐 LLM！]] — 自对齐
- [[WMA Web Agent]] — Agent 决策风险
- [[2D-DPO]] — 多维度偏好对齐

#### 20241025-20241031 (5 篇)
- [[AgentStore]] — 智能世界的超级 App Store
- [[CMU 与普林斯顿改进 BoN 算法]] — 推理效率
- [[Flow-DPO]] — 多智能体推理链
- [[PULSE 多模态大模型]] — 多模态

#### 20241101-20241107 (5 篇)
- [[颠覆Transformer，神经网络自演化的开端]] — 自演化
- [[谷歌出品 SLED 解码技术]] — 解码可靠性
- [[Adapting While Learning]] — 自适应智能工具
- [[SCPO：Meta 自我进化新方法]] — 自进化推理
- [[StepAgent]] — 过程奖励 Agent

#### 20241108-20241114 (3 篇)
- [[IOPO]] — 复杂指令处理
- [[Spider 2.0]] — Text-to-SQL 挑战
- [[UC Berkeley 和 CMU 大模型泛化]] — 泛化机制

#### 20241115-20241121 (3 篇)
- [[一键自动化：Claude 3.5与GUI Agent]] — GUI Agent
- [[LPO]] — 自适应解码温度
- [[XiYan-SQL]] — Text-to-SQL 突破

#### 20241206-20241212 (4 篇)
- [[迈向高效智能：能力密度增长与密度定律]] — 密度定律
- [[Coconut]] — 连续潜在空间推理
- [[RARE]] — 推理智慧导航
- [[VisionZip]] — 视觉 token 压缩

#### 20241213-20241219 (7 篇)
- [[大语言模型的幻觉克星 DePaC]] — 幻觉抑制
- [[Apollo 视频大模型]] — 视频理解
- [[Cal-DPO]] — DPO 改进
- [[大概念模型（LCM）]] — 词级突破
- [[ModernBERT]] — 编码器革新
- [[RetroLLM]] — 检索生成融合
- [[SHAD+RFT]] — Agent-Task 微调

#### 20241220-20241226 (5 篇)
- [[TALE 框架]] — 推理成本瘦身
- [[数据选择策略强化预训练]] — 数据选择
- [[GME]] — 通用多模态检索
- [[Mulberry]] — MCTS 多模型推理
- [[Proactive Agent]] — 主动读取需求

#### 20241227-20250102 (4 篇)
- [[加权偏好优化弥补自身短板]] — 偏好优化进化
- [[减少不必要的计算开销]] — 过度思考抑制
- [[任务偏好优化]] — 多模态精细视觉
- [[CCoT]] — 压缩链式思维

#### 20250103-20250109 (4 篇)
- [[MeCo]] — 元数据条件化加速预训练
- [[rStar-Math]] — 7B 数学能力
- [[LLaVA-Mini]] — 单视觉 token
- [[PPTAgent]] — AI PPT 生成

### 独立研究
- [[AK-Microgpt]] — MicroGpt 调研
- [[GVHMR - 重力视角坐标系的人体运动恢复]] — 人体运动恢复
- [[Kronos - 金融K线基础模型]] — 金融 K 线模型

## 根目录

- [[人形机器人全身控制-核心知识点]] — 全身控制要点概览
- [[具身智能课程推荐（MuJoCo）]] — MuJoCo 入门课程
- [[Unitree G1 WBT Dataset 调研报告]] — Unitree G1 调研