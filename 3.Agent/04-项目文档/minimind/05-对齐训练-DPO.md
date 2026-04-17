---
title: MiniMind — 对齐训练（DPO）
tags:
  - minimind
  - DPO
  - RLHF
  - alignment
---

# 对齐训练：DPO（`train_dpo.py`）

**DPO（Direct Preference Optimization）** 在一阶段内用 **偏好数据**（chosen 优于 rejected）对齐策略模型，**无需单独训练 Reward Model**，工程上比经典 RLHF（PPO + RM）更轻。

---

## 核心损失（公式）

设 $x$ 为上下文，$y_w$、$y_l$ 分别为 **chosen / rejected** 回复，$\pi_\theta$ 为策略模型，$\pi_{\text{ref}}$ 为冻结参考模型，$\beta$ 为温度系数。DPO 目标可写为：

$$
\mathcal{L}_{\text{DPO}}
=
-
\log \sigma \Big(
\beta \big(
(
\log \pi_\theta(y_w \mid x) - \log \pi_\theta(y_l \mid x)
)
-
(
\log \pi_{\text{ref}}(y_w \mid x) - \log \pi_{\text{ref}}(y_l \mid x)
)
\big)
\Big)
$$

直观理解：

- 鼓励 $\pi_\theta$ 在 chosen 上相对 rejected 的 **log 似然差** 超过 $\pi_{\text{ref}}$ 的同样差值；
- $\sigma$ 为 logistic，整体为 **binary classification** 形式的偏好学习。

---

## 实现要点（与代码结构对应）

### 1. 双模型

| 模型 | 角色 |
|------|------|
| **Policy model** | 带梯度，**训练对象** |
| **Ref model** | **冻结**，提供 $\log \pi_{\text{ref}}$ 基线 |

Ref 与 Policy **各调用一次** `init_model(lm_config, args.from_weight, ...)` 加载 **同一套起始权重**，随后对 Ref：`eval()` + `requires_grad_(False)`；前向算 ref logits 时包在 **`torch.no_grad()`** 内。

### 2. `logits_to_log_probs`

1. 对 logits 做 **`log_softmax`** 得到每个位置、每个词的对数概率；
2. 用 **`gather`** 取出 **目标 token**（labels 指定）在下一位置预测分布中的 log prob；
3. 在序列维上按 mask 求和，得到整段回复的 **log prob 和**（或等价聚合，以实现为准）。

### 3. `dpo_loss` 的 batch 组织

- 将 **chosen 与 rejected** 拼成 **同一 batch**：实现上 **`torch.cat([x_chosen, x_rejected], dim=0)`**，即 **前半 batch 为 chosen、后半为 rejected**（`dpo_loss` 里用 `batch_size // 2` 切开）。
- 分别计算 policy 与 ref 在对应样本上的 **log prob 序列按 mask 求和**，得到 `chosen_*` 与 `reject_*` 后构造 **`pi_logratios = chosen_policy − reject_policy`**、`ref_logratios = chosen_ref − reject_ref`，再令 **`logits = pi_logratios − ref_logratios`**（**注意**：$\beta$ **不**乘在这一差上）。
- 损失为 **`loss = −F.logsigmoid(beta * logits).mean()`**，与上节 DPO 公式等价。

### 4. `loss_mask`（仅 assistant 区域）

- 与 SFT 类似，只在 **assistant 回复** 的 token 上累计序列 log prob；
- 其它位置不参与 DPO 的似然差，避免把 prompt 或模板噪声当作偏好信号。

---

## 数据：`DPODataset`

| 项目 | 说明 |
|------|------|
| 字段 | **`chosen` / `rejected`** 各为 **完整对话列表** |
| 模板 | 两侧分别 **`apply_chat_template`** 转为模型输入 |
| Mask | **`generate_loss_mask`** 标记 assistant 段，用于 log prob 聚合 |

---

## 默认超参数（要点）

| 超参数 | 典型取值 | 备注 |
|--------|----------|------|
| `from_weight` | **`full_sft`** | 策略与 ref **同一**起始权重 |
| `beta` | **0.15** | 控制偏好强度；过大易过激 |
| `learning_rate` | **4e-8** | **极小**，减缓对预训练 / SFT 能力的 **灾难性遗忘** |
| `batch_size` | **4** | 偏好对两条序列，显存压力高于同宽 SFT |
| `max_seq_len` | **1024** | 长偏好对需要更大上下文 |

---

## 训练建议（实践向）

1. **Ref** 常取 **SFT 结束点** 或 **预训练 + SFT** 的稳定 checkpoint，且全程 **eval + no_grad**。
2. **$\beta$ 与 lr** 联动：$\beta$ 增大时，可适当减小有效更新步或更保守的 lr。
3. 监控 **chosen/rejected 长度差**；长度偏差过大时，DPO 可能隐含「偏好更长回答」的偏置，需在数据层或 mask 层修正。

---

## 相关笔记

- [[02-Tokenizer与数据处理]]
- [[03-预训练]]
- [[04-SFT微调]]
