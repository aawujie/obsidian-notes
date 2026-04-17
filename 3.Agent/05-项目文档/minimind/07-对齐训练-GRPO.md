---
title: MiniMind — 对齐训练（GRPO / CISPO）
tags:
  - minimind
  - GRPO
  - CISPO
  - reinforcement-learning
---

# 对齐训练：GRPO 与 CISPO

`train_grpo.py` 实现 **GRPO（Group Relative Policy Optimization）**：由 DeepSeek-R1 相关工作推广的思路——**每个 prompt 采样一组回复**，用 **组内 reward 的统计量** 代替 Critic 网络来构造 **baseline**，从而 **无需训练价值网络**。

---

## GRPO 核心思想

对每个 prompt 生成 **\(G\)** 条独立 completion（默认 **`num_generations=6`**），对第 \(i\) 条样本：

$$
A_i = \frac{r_i - \mu_{\text{group}}}{\sigma_{\text{group}} + 10^{-4}}
$$

即用 **组内均值 / 标准差** 对 reward 做标准化，得到 **优势估计**。这与 PPO 中「Critic + GAE」的角色不同：**不估计 \(V(s)\)**，而是用 **同 prompt 下多样本的相对比较** 降低方差。

---

## 与 PPO 的关键区别

| 维度 | PPO（`train_ppo.py`） | GRPO（`train_grpo.py`） |
|------|----------------------|-------------------------|
| **Critic** | 需要，输出 per-token value | **不需要** |
| **Advantage** | GAE + returns − values | **(r − mean) / (std + ε)**，按组 |
| **采样** | 通常每 prompt 一条或按 batch 设计 | **每 prompt 固定 \(G\) 条**（如 6） |
| **参数量 / 训练** | 额外优化 Critic | **更轻**，只训 policy（+ ref 对照） |

---

## 两种 Loss 模式

### 1. GRPO（标准 PPO clip 形式）

与经典 PPO 相同地使用 ratio 与 clip：

$$
\mathcal{L} = \min\bigl(\text{ratio}\cdot A,\ \text{clip}(\text{ratio}, 1-\varepsilon, 1+\varepsilon)\cdot A\bigr) - \beta \cdot \mathrm{KL}
$$

### 2. CISPO（默认）

使用 **上界截断的 ratio**，且 **detach** 后仅作标量系数作用在 logprob 上：

- `clamped_ratio = torch.clamp(ratio, max=epsilon_high).detach()`（**仅上界** `max`，不设 `min`；对应文中 \(\varepsilon_{\text{high}}\)）
- 每 token loss：\(\mathcal{L}_{t} = -(\text{clamped\_ratio}\cdot A\cdot \text{per\_token\_logps} - \beta\cdot \mathrm{KL}_t)\)（再对有效 completion mask 归一、对 batch 求均值）

直觉：**限制过大 ratio 对梯度的放大**，同时通过 **detach** 让梯度主要流经 **log probs**（而非 ratio 内部复杂路径）。默认 **\(\varepsilon_{\text{high}} = 5.0\)**。

---

## KL 散度（per-token）

与 PPO 脚本中常见的 ref 对齐项一致，使用 **指数型近似 KL**（逐 token）：

$$
\text{per\_token\_kl} = \exp(\text{ref\_logp} - \text{policy\_logp}) - (\text{ref\_logp} - \text{policy\_logp}) - 1
$$

---

## Completion Mask

基于 **`eos_token`** 位置对序列 **截断**，仅在有效 completion token 上累计 loss / KL，避免 pad 污染梯度。

---

## Reward 与 PPO 对齐

长度、思考格式、思考闭合、3-gram 重复、RM 打分等 **与 PPO 侧 `calculate_rewards` 同一套逻辑**（便于对比实验）。

---

## 学习率调度

**CosineAnnealingLR**，总步数按实现约定为：

$$
\text{total\_steps} = \left\lceil \frac{\text{iters}}{\text{accum}} \right\rceil \times \text{epochs}
$$

与 `train_grpo.py` 中 **`total_optimizer_steps = ceil(iters / accumulation_steps) * epochs`** 一致（`CosineAnnealingLR(..., T_max=total_optimizer_steps, eta_min=lr/10)`）。

---

## 默认超参数（要点）

| 超参数 | 默认值 |
|--------|--------|
| `lr` | `3e-7` |
| `num_generations` | `6` |
| `beta` | `0.1` |
| `loss_type` | **`cispo`**（可选 **`grpo`**） |
| `epsilon` | **`0.2`**（GRPO 分支下对 `ratio` 的双侧 clip：`1±ε`） |
| `epsilon_high` | `5.0` |

---

## 小结

GRPO/CISPO 路线用 **组内 reward 归一化** 换掉 **Critic + GAE**，默认 **CISPO** 在 clip 形式上做 **detach 系数 + logprob 直接加权**；KL 与 completion mask 仍保证 **相对 ref 的稳定对齐** 与 **有效 token 上的训练信号**。
