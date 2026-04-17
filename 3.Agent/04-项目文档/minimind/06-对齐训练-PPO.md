---
title: MiniMind — 对齐训练（PPO）
tags:
  - minimind
  - PPO
  - RLHF
  - reinforcement-learning
---

# 对齐训练：PPO（Proximal Policy Optimization）

`train_ppo.py` 实现 **近端策略优化（PPO）** 的完整 RLHF 风格管线：在 rollout 阶段用当前策略采样回复，结合 **Reward Model** 与规则奖励；用 **GAE** 估计优势；在更新阶段对 Actor 与 Critic 做多轮 clipped surrogate 优化，并对策略相对 **Reference** 施加 KL 惩罚。

---

## 四模型架构

| 角色 | 类型 | 说明 |
|------|------|------|
| **Actor（policy）** | `MiniMindForCausalLM` | 可训练，生成动作分布 |
| **Critic** | `CriticModel(MiniMindForCausalLM)`：**新增** `value_head = nn.Linear(hidden_size, 1)`，**重写 `forward`** 用 `model` → `norm` → `value_head` 输出标量序列，**不经过** `lm_head` 的下一词 logits | 对每个 token 输出 **价值估计** \(V_t\) |
| **Reference** | 冻结的 `MiniMindForCausalLM` 副本 | 用于 KL(ref \| policy) 惩罚，稳定策略偏移 |
| **Reward Model** | `LMForRewardModel` 包装 **internlm2-1_8b-reward** | 对完整序列或片段打分，与规则奖励叠加 |

---

## Rollout 阶段

1. 用当前 **Actor** 对 batch 内 prompt **自回归生成**回复。
2. 在 **`torch.no_grad()`** 下记录：
   - **old_logp**：策略在已生成 token 上的对数概率（用于 PPO ratio）。
   - **old_values**：**Critic** 在同样位置的价值 \(V_t\)。

整段 rollout 不参与梯度，避免「用同一批数据既采样又更新」时的偏差处理由后续 PPO 目标与多 epoch 结构承担。

---

## Reward 计算（`calculate_rewards`）

综合 **启发式规则** 与 **RM 分数**（具体权重以代码为准）：

| 项 | 规则摘要 |
|----|----------|
| **长度奖励** | `len(response.strip())` 在 **20–800** → **+0.5**，否则 **-0.5** |
| **思考格式** | 若含 `</think>`：思考段（分隔前）长度 **20–300** → **+1.0**，否则 **-0.5** |
| **思考闭合** | `</think>` 出现次数 **恰好 1** → **+0.25**，否则 **-0.25** |
| **重复惩罚** | `rep_penalty(answer, n=3, cap=0.5)`：基于 **3-gram** 重复率，**上限 0.5** |
| **RM** | Reward Model 对序列打分 |

实现上 **`token_rewards` 仅在每条回复的最后一个有效 token 位置** 加上标量 `rewards`（其余生成步为 0），再与 **GAE** 结合；并非逐步稠密奖励。

---

## GAE（Generalized Advantage Estimation）

定义 **TD 残差**：

$$
\delta_t = r_t + \gamma V_{t+1} - V_t
$$

**优势**按 \(\gamma\) 与 \(\lambda\) 回溯：

$$
A_t = \sum_{l=0}^{\infty} (\gamma\lambda)^l \, \delta_{t+l}
$$

**回报**：

$$
\text{returns}_t = A_t + V_t
$$

对 **advantage** 做 **归一化**（例如按 batch 或序列内减均值除方差），减小尺度波动、稳定 PPO clip 区间内的更新。

---

## PPO 更新

- **外层**：`ppo_update_iters=2`（可配置）表示对同一批 rollout 数据做 **多轮** mini-batch 更新。
- **Policy loss**（实现为 **可最小化的标量**，对优势 `A` 与 `ratio = exp(new_logp - old_logp)`）：
  - 代码形式：`mean(max(-A*ratio, -A*clip(ratio, 1-eps, 1+eps)))`，等价于最小化 **\( -\min(\text{ratio}\cdot A,\ \text{clip}(\text{ratio},1-\varepsilon,1+\varepsilon)\cdot A) \)** 的样本均值；
  - \(\text{ratio} = \exp(\text{new\_logp} - \text{old\_logp})\)。
- **KL ref 惩罚**（对 ref 的近似 KL，「指数形式」一项，再乘 `kl_coef` 并入 `policy_loss`）：
  $$
  \exp(\text{ref\_logp} - \text{policy\_logp}) - (\text{ref\_logp} - \text{policy\_logp}) - 1
  $$
- **Value loss**：**clipped value loss**（限制 value 相对 old value 的变动，与标准 PPO 一致）。
- **Early stop**：当 **approx_kl > 0.25** 时停止本轮 PPO 更新；**DDP** 下对各卡 **all_reduce** 同步该条件。
- **DDP 安全**：early stop 时通过 **乘以 0** 等方式「压掉」梯度贡献，**避免直接 `break` 导致部分 rank 未执行 backward** 而通信死锁；保证所有进程 **backward 路径闭合**。

---

## 默认超参数（要点）

| 超参数 | 默认值 |
|--------|--------|
| `actor_lr` | `3e-7` |
| `critic_lr` | `5e-7` |
| `clip_epsilon` | `0.2` |
| `vf_coef` | `0.5` |
| `kl_coef` | `0.02` |
| `gamma` | `1.0` |
| `lam` | `0.95` |
| `ppo_update_iters` | `2` |
| `mini_batch_size` | `2` |
| `early_stop_kl` | `0.25` |

学习率调度：**CosineAnnealingLR**（`T_max` 由 `iters × epochs × ppo_update_iters × ceil(batch_size / mini_batch_size)` 与 `accumulation_steps` 共同决定，见脚本）。

---

## 小结

PPO 路径依赖 **Critic** 提供 \(V_t\) 与 GAE，依赖 **Reference** 约束偏离，依赖 **RM + 规则** 定义奖励；工程上需特别注意 **分布式下 early stop 与 backward 一致性**。
