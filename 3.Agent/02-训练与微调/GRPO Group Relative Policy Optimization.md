# GRPO Group Relative Policy Optimization

> DeepSeek 提出的强化学习方法，用组内相对奖励替代价值模型，专门用于提升大模型推理能力

---

## 核心思想

### 传统 PPO 的问题

PPO 需要训练一个**价值模型（Value Model）** 来估计状态价值，但在 LLM 场景下存在问题：
- 价值模型和策略模型一样大，显存占用翻倍
- 价值模型训练不稳定，容易过拟合
- 对于离散的语言生成任务，价值估计困难

### GRPO 的改进

**去掉价值模型，用组内相对奖励代替绝对价值估计**。

```
PPO: 需要 Value Model 估计 V(s)
GRPO: 不需要 Value Model，用同一问题的多个采样结果的相对奖励
```

---

## 数学原理

### 组内采样

对于每个问题 $q$，从旧策略 $\pi_{\theta_{old}}$ 采样一组回答 $\{o_1, o_2, ..., o_G\}$（通常 $G=16$）

### 奖励计算

每个回答获得奖励 $r_i = R(o_i)$，奖励可以是：
- **规则奖励**：答案是否正确（数学/代码）
- **过程奖励**：推理步骤的格式奖励（如 DeepSeek-R1 的 `\boxed{}` 标签）

### 组内相对优势

$$\bar{r} = \frac{1}{G}\sum_{i=1}^{G} r_i$$

$$A_i = \frac{r_i - \bar{r}}{\sqrt{\text{Var}(\{r_i\}) + \epsilon}}$$

**关键**：用组内均值作为基线，标准化后得到相对优势

### GRPO 目标函数

$$\mathcal{L}_{GRPO} = \mathbb{E}_{q \sim P(Q), \{o_i\}_{i=1}^G \sim \pi_{\theta_{old}}}\left[\frac{1}{G}\sum_{i=1}^{G}\left(\min\left(\frac{\pi_\theta(o_i|q)}{\pi_{\theta_{old}}(o_i|q)}A_i, \text{clip}(\cdot)A_i\right) - \beta \mathbb{D}_{KL}(\pi_\theta || \pi_{ref})\right)\right]$$

---

## 直观理解

```
问题 q: "1+1=?"

采样 16 个回答：
o1: "1+1=2"        → r=1  (正确)
o2: "1+1=2"        → r=1  (正确)
o3: "1+1=3"        → r=0  (错误)
...
o16: "让我想想...1+1=2" → r=1 (正确，有推理过程)

平均奖励 r̄ = 12/16 = 0.75
标准化优势：
A1 = (1 - 0.75) / std = 正优势 → 鼓励
A3 = (0 - 0.75) / std = 负优势 → 抑制
```

---

## GRPO vs PPO vs DPO

| 特性 | PPO | DPO | GRPO |
|------|-----|-----|------|
| **价值模型** | ✅ 需要 | ❌ 不需要 | ❌ 不需要 |
| **奖励模型** | ✅ 需要 | ❌ 不需要 | ⚠️ 规则/过程奖励 |
| **偏好数据** | ❌ 不需要 | ✅ 需要 | ❌ 不需要 |
| **组内采样** | ❌ 不需要 | ❌ 不需要 | ✅ 需要 |
| **显存占用** | 高（4x） | 中（2x） | 中（2x） |
| **适用场景** | 通用 RLHF | 偏好对齐 | 推理能力训练 |
| **代表模型** | InstructGPT | Zephyr | DeepSeek-R1 |

---

## DeepSeek-R1 中的应用

### 训练流程

```
Step 1: 冷启动 SFT
   - 用少量高质量 CoT 数据微调基础模型
   
Step 2: 推理导向 RL (GRPO)
   - 用 GRPO 训练，奖励 = 答案正确性 + 格式奖励
   - 出现"顿悟时刻"（Aha Moment）：模型学会自我纠正
   
Step 3: 拒绝采样 + SFT
   - 用训练后的模型生成高质量数据
   - 混合通用数据再次 SFT
   
Step 4: 全场景 RL
   - 用 GRPO 对齐人类偏好（有用性、无害性）
```

### 关键设计

| 组件 | 说明 |
|------|------|
| **准确性奖励** | 数学答案是否正确（规则判断） |
| **格式奖励** | 是否按要求放在 `\boxed{}` 中 |
| **组大小** | G=16，每个问题采样16个回答 |
| **KL 惩罚** | 防止模型偏离参考模型太远 |

---

## PyTorch 实现

```python
def grpo_loss(policy_model, ref_model, batch, beta=0.1, eps=1e-4):
    """
    batch: {
        'prompts': [q1, q1, ..., q2, q2, ...],  # 重复 G 次
        'responses': [o1, o2, ..., oG, ...],     # 组内采样
        'rewards': [r1, r2, ..., rG, ...]        # 规则奖励
    }
    """
    G = 16  # 组大小
    
    # 计算策略模型的 log 概率
    pi_logps = policy_model(batch['prompts'], batch['responses'])
    
    # 计算参考模型的 log 概率
    with torch.no_grad():
        ref_logps = ref_model(batch['prompts'], batch['responses'])
        old_pi_logps = pi_logps.detach()  # 旧策略
    
    # 按组计算相对优势
    rewards = batch['rewards'].view(-1, G)  # [N, G]
    mean_rewards = rewards.mean(dim=1, keepdim=True)
    std_rewards = rewards.std(dim=1, keepdim=True)
    advantages = (rewards - mean_rewards) / (std_rewards + eps)  # [N, G]
    advantages = advantages.view(-1)  # 展平
    
    # 重要性采样比率
    ratio = torch.exp(pi_logps - old_pi_logps)
    
    # PPO 裁剪
    surr1 = ratio * advantages
    surr2 = torch.clamp(ratio, 0.9, 1.1) * advantages
    policy_loss = -torch.min(surr1, surr2).mean()
    
    # KL 惩罚（防止偏离参考模型）
    kl_div = (pi_logps - ref_logps).mean()
    
    loss = policy_loss + beta * kl_div
    return loss
```

---

## 关键优势

1. **无需价值模型**：节省显存，训练更稳定
2. **规则奖励**：不需要训练奖励模型，直接用规则判断
3. **组内相对**：消除绝对奖励的偏差，更关注相对质量
4. **适合推理任务**：通过格式奖励引导模型展示思考过程

---

## 一句话总结

> **GRPO 通过组内相对奖励替代价值模型，专为提升 LLM 推理能力设计，是 DeepSeek-R1 "顿悟时刻"的关键技术。**

---

## 参考

- 论文：[DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning](https://arxiv.org/abs/2501.12948)
- 来源：OpenClaw 会话 2026-04-15
