# GSPO：Group Sequence Policy Optimization 研究笔记

> 提出：Qwen Team, Alibaba Inc. (Zheng et al., 2025)  
> 参考论文：SAPO (arXiv:2511.20347) — Qwen 团队论文，详细介绍 GSPO  
> 标签：#RLHF #对齐 #强化学习 #Qwen #PPO改进 #sequence-level

---

## 核心创新

> [!tip] 一句话总结
> **GSPO 用 sequence-level importance ratio 替代 token-level，提升长序列训练稳定性。**

| 方法 | Importance Ratio | 适用场景 |
|------|-----------------|---------|
| GRPO | token-level $\frac{\pi_\theta}{\pi_{old}}$ | 短序列 |
| **GSPO** | **sequence-level** $s_i(\theta)$ | **长序列、JSON输出** |

---

## 问题背景

### Token-level 的高方差问题

> [!warning] GRPO 的痛点
> - **Token-level importance ratio 高方差**：每个 token 的 $\frac{\pi_\theta}{\pi_{old}}$ 波动大
> - **MoE 模型更严重**：routing heterogeneity 放大偏差
> - **长序列不稳定**：token 数多 → 累积方差大

---

## GSPO 核心思想

### Sequence-level Importance Ratio

**核心公式**：

```math
s_i(θ) = geometric_mean(π_θ/π_old over entire sequence y_i)
```

> [!important] 
> 用**整个序列的几何平均**代替逐 token 的 importance ratio。

---

### 目标函数

```math
J_GSPO(θ) = E[q, {y_i}] [
    1/G Σ min(s_i(θ)·A_i, clip(s_i(θ), 1-ε, 1+ε)·A_i)
]
```

**对比 GRPO**：

| GRPO | GSPO |
|------|------|
| `min(r_t, clip(r_t))·A` | `min(s_i, clip(s_i))·A` |
| 每个 token 一个 ratio | **整个序列一个 ratio** |
| clip 每个 token | **clip 整个序列** |

---

## Sequence-level Importance Ratio 定义

```math
s_i(θ) = (∏_{t=1}^{|y_i|} π_θ(y_{i,t}|q, y_{i,<t}) / π_{old}(y_{i,t}|q, y_{i,<t}))^{1/|y_i|}
```

> [!note] 
> **几何平均**：对整个序列的 likelihood ratio 取指数平均，数值更稳定。

---

## 为什么 Sequence-level 更稳定？

### 1. 降低方差

> [!success] 
> - 单个 token ratio 波动大
> - 整个序列的几何平均 → **平滑波动**
> - 类似"批量归一化"的效果

### 2. 结构化输出友好

> [!success] 
> - JSON、Scene Graph 等需要**完整序列一致**
> - Token-level clip 可能破坏结构
> - Sequence-level 保持整体 coherence

### 3. 长序列优化

> [!success] 
> - 长序列 → 更多 token → 更多 variance 累积
> - Sequence-level aggregation → **全局视角**

---

## 与 GRPO 的详细对比

| 维度 | GRPO | GSPO |
|------|------|------|
| **Importance Ratio** | token-level | **sequence-level** |
| **Clip 方式** | 每个 token clip | **整序列 clip** |
| **方差控制** | 较差 | **较好** |
| **MoE 适用性** | 一般 | **更好** |
| **长序列** | 不稳定 | **稳定** |
| **结构化输出** | 可能破坏结构 | **保持整体性** |

---

## GSPO 的问题

> [!warning] Hard Clipping 的缺陷
> - **序列内少数异常 token → 整序列梯度被抑制**
> - "When a sequence contains a few highly off-policy tokens, GSPO suppresses **all gradients** for that sequence"
> - 这导致 **sample efficiency 降低**

---

## SAPO：GSPO 的改进版

> Qwen 团队在 SAPO 论文中提出的改进

**核心改进**：用 **soft gate** 替代 hard clipping

| GSPO | SAPO |
|------|------|
| hard clip (1±ε) | **soft sigmoid gate** |
| 整序列要么用要么弃 | **选择性 down-weight 异常 token** |
| 梯度突变 | **连续 trust region** |

**SAPO 公式**：

```math
gate(r) = sigmoid(-τ(r - 1))  # 温度控制的软门控
```

> [!tip] 
> - 近 on-policy (r≈1) → gate≈1，梯度保留
> - 偏离大 → gate 小，梯度平滑衰减（而非截断）

---

## 应用场景

### 1. Scene Graph Generation (SGG)

论文 arXiv:2603.07961 使用 GSPO：

> "GSPO enhances optimization robustness for the generation of **long-form, structured JSON outputs**."

### 2. Multimodal Reasoning

论文 arXiv:2512.11872 使用 GSPO：

> "Online RL using GSPO to optimize **sequence-level driving rewards**."

### 3. Qwen3-VL Training

SAPO 论文用改进版训练 Qwen3-VL：

> "SAPO yields consistent performance gains across diverse tasks and different model sizes."

---

## 代码实现要点

### GSPO 训练循环

```python
# 每个 prompt
for prompt in prompts:
    # 采样 G 个输出
    outputs = model.sample(prompt, num=G)
    
    # 计算 reward
    rewards = [compute_reward(o) for o in outputs]
    
    # 组内统计（与 GRPO 相同）
    mean_r = rewards.mean()
    std_r = rewards.std() + 1e-4
    advantages = (rewards - mean_r) / std_r
    
    # Sequence-level importance ratio
    for i, output in enumerate(outputs):
        # 整序列 likelihood ratio（几何平均）
        seq_ratio = compute_sequence_ratio(model, ref_model, output)
        
        # GSPO loss
        loss = min(seq_ratio * advantages[i],
                   clip(seq_ratio, 1-eps, 1+eps) * advantages[i])
```

### Sequence Ratio 计算

```python
def compute_sequence_ratio(policy, ref_policy, output):
    """
    计算整个序列的 importance ratio（几何平均）
    """
    log_ratios = []
    for t, token in enumerate(output):
        # 当前 policy vs behavior policy
        log_ratio = policy.log_prob(token) - ref_policy.log_prob(token)
        log_ratios.append(log_ratio)
    
    # 几何平均 = exp(mean(log ratios))
    seq_ratio = torch.exp(torch.stack(log_ratios).mean())
    return seq_ratio
```

---

## 技术演进路径

```
PPO (2017)
    ↓
GRPO (2024, DeepSeek) — token-level, 无 Critic
    ↓
GSPO (2025, Qwen) — sequence-level, 更稳定
    ↓
SAPO (2025, Qwen) — soft gate, token-adaptive
```

---

## 与其他方法的关系

| 方法 | 提出 | Critic | Ratio Level | Clipping |
|------|------|--------|------------|----------|
| PPO | OpenAI | 需要 | token | hard |
| GRPO | DeepSeek | 不需要 | token | hard |
| **GSPO** | **Qwen** | 不需要 | **sequence** | hard |
| SAPO | Qwen | 不需要 | hybrid | **soft** |
| DPO | 多方 | 不需要 | — | 离线 |

---

## 相关概念

- [[GRPO-组相对策略优化研究笔记]] ← GRPO 是 GSPO 的前身
- [[07-对齐训练-GRPO]]（minimind 笔记）← GRPO 实现
- [[DPO vs RLHF 对比笔记]] ← 整体框架
- [[SAPO]] ← GSPO 的改进版（同一团队）

---

## 参考文献

- **SAPO 论文**（详细介绍 GSPO）：arXiv:2511.20347  
  作者：Qwen Team, Alibaba Inc.  
  GSPO 原始引用：Zheng et al., 2025
- **SGG-R³ 论文**（应用 GSPO）：arXiv:2603.07961
- **GRPO 论文**：Shao et al., 2024 (DeepSeek)

---

*创建时间：2026-04-16*  
*论文下载：`SAPO-GSPO-Qwen.pdf`（同目录）*