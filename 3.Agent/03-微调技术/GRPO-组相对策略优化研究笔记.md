# GRPO：Group Relative Policy Optimization 研究笔记

> 论文：DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning  
> 作者：DeepSeek-AI  
> arXiv：2501.12948  
> 发布时间：2025年1月  
> GRPO 提出：Shao et al., 2024  
> 标签：#RLHF #对齐 #强化学习 #DeepSeek #PPO替代

---

## 核心创新

> [!tip] 一句话总结
> **GRPO 用组内 reward 统计量替代 Critic 网络，无需训练价值函数，简化 PPO 训练。**

| 方法 | Critic | 采样方式 | 复杂度 |
|------|--------|---------|--------|
| PPO | 需要 | 单样本 | 高 |
| **GRPO** | **不需要** | **组采样（G个）** | **低** |

---

## 问题背景

### PPO 的痛点

> [!warning] PPO 的三大问题
> 1. **需要 Critic 网络**：额外参数、额外训练
> 2. **价值估计困难**：Critic 需要准确估计 V(s)，训练复杂
> 3. **资源消耗大**：PPO 需要同时优化 Policy + Critic + Reward Model

---

## GRPO 核心思想

### 组采样 + 相对比较

**核心流程**：

```
每个问题 q → 采样 G 个输出 {o₁, o₂, ..., o_G}
→ 计算每个 reward {r₁, r₂, ..., r_G}
→ 用组内统计量构造 baseline
→ 无需 Critic 网络
```

---

### 优势估计公式

```math
A_i = (r_i - μ_group) / (σ_group + ε)

其中：
μ_group = mean({r₁, r₂, ..., r_G})
σ_group = std({r₁, r₂, ..., r_G})
```

> [!important] 
> 用**组内均值做 baseline**，用**组内标准差做归一化**。

---

### 目标函数

```math
J_GRPO(θ) = E[q ~ P(Q), {o_i} ~ π_θ_old]
            [Σ (clip(ratio) × A_i - β × KL)]
```

**与 PPO 的区别**：
- PPO：`A = GAE(Returns - V(s))`
- GRPO：`A = (r - group_mean) / group_std`

---

## 与 PPO 的详细对比

| 维度 | PPO | GRPO |
|------|-----|------|
| **Critic 网络** | 需要 | **不需要** |
| **Advantage 计算** | GAE + V(s) | 组内 reward 归一化 |
| **采样方式** | 每问题1条 | 每问题 G 条 |
| **参数量** | Policy + Critic | **只 Policy** |
| **训练复杂度** | 高 | **低** |
| **KL 约束** | 需要 | 需要 |
| **clip ratio** | 双侧 (1±ε) | 大 clip 策略 |

---

## GRPO 的优势

### 1. 无需 Critic

> [!success] 
> - 减少参数量
> - 避免 Critic 训练不稳定
> - 简化训练流程

### 2. 组内相对比较

> [!success] 
> - 同一问题多个回答 → 自然对比
> - 高 reward 回答被强化
> - 低 reward 回答被抑制

### 3. 计算效率

> [!success] 
> - 只优化 policy 网络
> - 节省 Critic 训练开销
> - 更适合大规模 RL

---

## DeepSeek-R1 的应用

### 训练设置

| 参数 | 值 |
|------|-----|
| 学习率 | 3e-6 |
| KL 系数 | 0.001 |
| 组大小 G | 16 |
| 最大长度 | 32k → 65k tokens |
| clip ratio ε | 10（大 clip） |

### 训练流程

```
DeepSeek-V3-Base
    ↓
GRPO RL 训练（无 SFT 前置）
    ↓
DeepSeek-R1-Zero（纯 RL）
    ↓
+SFT 数据蒸馏
    ↓
DeepSeek-R1（完整版）
```

---

### 关键发现

> [!important] "Aha Moment"
> DeepSeek-R1-Zero 在训练中自然学会了：
> - 反思（"Wait, let me rethink..."）
> - 验证
> - 长 Chain-of-Thought

> [!quote] 论文原文
> "The model learns to rethink using an anthropomorphic tone. This is also an aha moment for us, allowing us to witness the power and beauty of reinforcement learning."

---

## 数学细节

### 组内 reward 处理

```math
给定：{r₁, r₂, ..., r_G}

均值：μ = (1/G) Σ r_i
标准差：σ = sqrt((1/G) Σ (r_i - μ)²)

归一化 advantage：
A_i = (r_i - μ) / (σ + 10⁻⁴)
```

### KL 散度（per-token）

```math
KL = exp(ref_logp - policy_logp) - (ref_logp - policy_logp) - 1
```

---

## 大 Clip 策略

DeepSeek-R1 使用 **大 clip ratio（ε = 10）**：

> [!note] 
> 传统 PPO：ε = 0.2（双侧 clip）
> DeepSeek GRPO：ε = 10（大 clip，允许更大更新）

**原因**：
- RL 训练初期需要更大探索
- 避免 clip 过严导致收敛慢

---

## CISPO 变体

> minimind 笔记中提到的变体

**CISPO**（Clipped Importance Sampling Policy Optimization）：

| GRPO | CISPO |
|------|-------|
| 双侧 clip (1±ε) | **只上界 clip** (max=ε_high) |
| ratio 参与 gradient | **ratio detach**，只作系数 |
| ε = 0.2 | **ε_high = 5.0** |

**CISPO 特点**：
- 限制过大 ratio 放大梯度
- 梯度主要流经 log probs
- 训练更稳定

---

## 实验结果（DeepSeek-R1）

### AIME 2024 性能

| 模型 | pass@1 |
|------|--------|
| DeepSeek-V3-Base | 15.6% |
| DeepSeek-R1-Zero（RL训练后） | **77.9%** |
| + self-consistency | **更高** |

---

## 代码实现要点

### GRPO 训练循环

```python
# 每个 prompt
for prompt in prompts:
    # 采样 G 个输出
    outputs = model.sample(prompt, num=G)
    
    # 计算 reward
    rewards = [compute_reward(o) for o in outputs]
    
    # 组内统计
    mean_r = rewards.mean()
    std_r = rewards.std() + 1e-4
    
    # Advantage
    advantages = (rewards - mean_r) / std_r
    
    # GRPO loss
    loss = grpo_loss(outputs, advantages)
```

---

## 与其他方法的对比

| 方法 | 需要 Critic | 需要 Reward Model | 训练复杂度 |
|------|-----------|------------------|-----------|
| PPO | ✓ | ✓ | 高 |
| DPO | ✗ | ✗ | 低（离线） |
| **GRPO** | **✗** | **可选** | **中** |
| RLAIF | ✗ | ✓（AI生成） | 中 |

---

## 相关概念

- [[DPO vs RLHF 对比笔记]] ← GRPO 是 RLHF 的简化版
- [[07-对齐训练-GRPO]]（minimind 笔记）← 详细实现
- [[PPO]] ← GRPO 的前身
- [[DeepSeek-R1]] ← 应用案例

---

## 参考文献

- DeepSeek-R1 论文：[arXiv:2501.12948](https://arxiv.org/abs/2501.12948)
- GRPO 原始论文：Shao et al., 2024
- PPO 论文：Schulman et al., 2017

---

*创建时间：2026-04-16*  
*论文下载：`DeepSeek-R1-GRPO.pdf`（同目录）*