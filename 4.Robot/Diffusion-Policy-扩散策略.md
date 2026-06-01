---
title: Diffusion-Policy-扩散策略
type: paper-note
created: 2026-06-01
tags: [imitation-learning, diffusion, paper-note, visuomotor]
---

## 论文信息
- **标题**: Diffusion Policy: Visuomotor Policy Learning via Action Diffusion
- **作者/机构**: Cheng Chi, Siyuan Feng, Yilun Du, Zhenjia Xu, Eric Cousineau, Benjamin Burchfiel, Shuran Song (Columbia University & Toyota Research Institute)
- **发表时间**: 2023年3月 (IJRR 2024)
- **arXiv**: https://arxiv.org/abs/2303.04137
- **项目主页**: https://diffusion-policy.cs.columbia.edu
- **引用**: Chi et al., "Diffusion Policy: Visuomotor Policy Learning via Action Diffusion", RSS 2023 / IJRR 2024

## 核心问题
机器人行为克隆面临的核心挑战来自机器人动作空间的独特性质：(1) **多模态分布**——给定相同观测，可能有多种合理动作(如避障左绕或右绕)；(2) **高精度需求**——微小动作误差导致任务失败；(3) **时序相关**——动作序列必须平滑连续。传统方法(高斯分布、分类、隐式模型)无法充分表达复杂的多模态动作分布。Diffusion Policy提出：**用条件去噪扩散过程来表达机器人视觉运动策略**。

## 关键方法
1. **扩散模型用于动作生成**：将机器人策略表述为条件去噪扩散概率模型(DDPM)。给定观测O_t，策略不是直接输出动作，而是通过K步随机Langevin动力学，从噪声中逐步去噪生成动作A_t。核心优势：天然表达任意多模态分布。
2. **闭环动作序列预测**：策略预测未来T_p步的动作序列，但只执行前T_a步后就重新规划(receding horizon control)。这种设计在长时规划一致性和实时响应之间取得平衡。
3. **视觉条件化(Conditioning而非Joint)**：将视觉观测作为条件p(At|Ot)，而非联合分布p(At, Ot)。这意味着视觉特征仅需提取一次(而非每个去噪步骤都提取)，大幅降低计算量，使实时推理成为可能。
4. **时域扩散Transformer**：提出基于Transformer的扩散网络，替代传统CNN U-Net。CNN存在过平滑(over-smoothing)问题，导致高频动作变化(如速度控制)不精确。Transformer能更好捕捉长时间依赖。
5. **极简训练**：训练极其稳定，几乎不需要任务特定的超参数调优。这与之前的隐式行为克隆方法(如IBC)形成鲜明对比——其训练不稳定，需要精心设计负采样。

## 重要细节
- **观测窗口T_o**：最近的若干帧观测(如2-3帧)
- **动作预测窗口T_p**：预测未来多步动作(如16步)
- **动作执行窗口T_a**：每次执行几步后才重新推理(如8步)，T_a < T_p
- **Receding Horizon + Warm-starting**：当T_a < T_p时，未执行的动作预测可作为下一次推理的warm-start初始化，进一步提升动作平滑性
- **推理加速**：视觉特征只提取一次(conditioning方式)，而非每个去噪步骤都处理图像(joint方式)
- **实验覆盖**：15个任务、4个benchmark(Florence et al., Gupta et al., Mandlekar et al., Shafiullah et al.)、仿真+真实环境
- **性能提升**：相比之前SOTA方法，**平均成功率提升46.9%**
- **控制模式**：支持末端执行器位置控制和速度控制

## 与面试50题的关系
- **Q3 (扩散/Flow Matching用于机器人)**：Diffusion Policy是扩散模型用于机器人动作生成的开创性工作，必须深入理解。核心考点：(1) 为什么扩散适合机器人动作？——多模态分布；(2) Conditioning vs Joint的差异和计算优势；(3) 闭环序列预测中T_p和T_a的关系；(4) 与Flow Matching(π0)的本质区别——SDE vs ODE。

## 个人思考