---
title: ACT-Action-Chunked-Transformers
type: paper-note
created: 2026-06-01
tags: [imitation-learning, bimanual, paper-note, action-chunking]
---

## 论文信息
- **标题**: Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware (aka Action Chunking with Transformers, ACT)
- **作者/机构**: Tony Z. Zhao, Vikash Kumar, Sergey Levine, Chelsea Finn (Stanford University)
- **发表时间**: 2023年4月 (RSS 2023)
- **arXiv**: https://arxiv.org/abs/2304.13705
- **项目主页**: https://tonyzhaozh.github.io/aloha/
- **引用**: Zhao et al., "Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware", RSS 2023

## 核心问题
行为克隆(Behavior Cloning)的一个核心痛点是**复合误差(compounding errors)**——模型预测的小误差会随时间累积导致状态漂移，最终任务失败。ACT要解决的问题是：**如何设计一种模仿学习策略，使其能学习精细的双手操作任务(如插入电池、拉上拉链)，同时缓解复合误差问题？**

第二个同等重要的贡献是：**如何用低成本硬件(总价<$5000)实现双手远程操作的数据采集？**——这就是ALOHA平台。

## 关键方法
1. **Action Chunking (动作分块)**：核心创新——不预测单一动作，而是预测未来k个动作的序列(chunk，如100个时间步@50Hz)。这减少了有效控制频率从而降低了复合误差。直觉：如果每次预测覆盖2秒的动作，每2秒才重新规划一次，累积错误的机会大大减少。
2. **CVAE架构 + Transformer**：使用条件变分自编码器(CVAE)生成动作块。编码器看到当前关节状态和未来动作块，生成隐变量z(风格变量)；解码器仅根据当前状态和z重建动作块。Transformer作为CVAE的编码器和解码器，捕捉时序依赖。
3. **Temporal Ensemble(时间集成)**：推理时，重叠预测的动作块通过加权平均(time-weighted averaging)聚合，产生平滑的动作序列。越靠近当前时刻的预测权重越大。
4. **ALOHA低成本硬件平台**：两个6DoF桌面机械臂(Interbotix ViperX)组成leader-follower系统。Leader臂用于人工遥操作采集演示数据，Follower臂执行策略。加上摄像头和配件，总价<$5000。
5. **从少量演示学习**：每个任务仅需10-30分钟的人类遥操作演示数据即可学会。

## 重要细节
- **动作块长度**：预测100步(2秒@50Hz)，其中只执行前部分步数后重新规划
- **CVAE的z维度**：通常为32或64维，编码动作的"风格"——比如接近物体的路径选择
- **损失函数**：重建损失(chunk中每个动作的L1/L2) + KL散度(z分布与先验的KL散度)
- **任务案例**：插电池、拉拉链、拧瓶盖、穿针引线、叠毛巾等精细双手操作
- **硬件关键**：Leader-Follower同构设计使得遥操作采集的动作和机器人执行的动作处于相同空间，不需要复杂的重定向(retargeting)
- **与Diffusion Policy的关系**：两者都预测动作序列，但ACT用CVAE一次性生成，Diffusion Policy用迭代去噪。ACT更轻量但建模能力略弱于扩散模型

## 与面试50题的关系
- **Q5 (ACT的Action Chunking原理)**：这是直接考点。需要解释清楚为什么预测动作块能缓解复合误差——降低重规划频率 + 时间集成平滑。还需要理解CVAE中隐变量z的作用(捕捉动作多模态性/风格变化)和Temporal Ensemble的加权方式。

## 个人思考