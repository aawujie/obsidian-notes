# DPO Direct Preference Optimization

> 直接偏好优化：无需奖励模型，直接用偏好数据对齐语言模型

---

## 核心思想

### 传统 RLHF 流程

```
SFT 模型 → 训练 RM → PPO 优化
           ↑___________|
         (需要大量计算)
```

### DPO 简化流程

```
SFT 模型 ──→ DPO 直接优化
```

**关键洞察**：最优奖励函数与最优策略之间存在闭式关系，可以直接用策略来定义损失。

---

## 数学原理

### Bradley-Terry 偏好模型

假设对于同一 prompt 的两个回答 $y_w$（胜）和 $y_l$（负），人类偏好的概率为：

$$p(y_w \succ y_l | x) = \sigma(r(x, y_w) - r(x, y_l))$$

其中 $\sigma$ 是 sigmoid 函数，$r$ 是奖励函数。

### DPO 的巧妙转换

根据 RL 理论，最优策略 $\pi^*$ 与奖励函数 $r$ 的关系：

$$\pi^*(y|x) = \frac{1}{Z(x)} \pi_{ref}(y|x) \exp\left(\frac{1}{\beta}r(x,y)\right)$$

**反解出奖励函数**：

$$r(x,y) = \beta \log\frac{\pi^*(y|x)}{\pi_{ref}(y|x)} + \beta \log Z(x)$$

### DPO 损失函数

将奖励表达式代入偏好模型，消去 $Z(x)$，得到**直接优化策略**的损失：

$$\mathcal{L}_{DPO} = -\mathbb{E}_{(x, y_w, y_l)}\left[\log \sigma\left(\beta \log\frac{\pi(y_w|x)}{\pi_{ref}(y_w|x)} - \beta \log\frac{\pi(y_l|x)}{\pi_{ref}(y_l|x)}\right)\right]$$

---

## 直观理解

```
对于每个偏好对 (y_win, y_lose)：

DPO 要最大化：π(y_win|x) / π(y_lose|x)
同时约束：π 不要太偏离 π_ref（通过 β 控制）

损失 = -log σ( β × [log(π_win/π_ref_win) - log(π_lose/π_ref_lose)] )
              ↑
         胜者对 vs 负者的"相对优势"
```

---

## DPO vs PPO

| 特性 | PPO (RLHF) | DPO |
|------|-----------|-----|
| **奖励模型** | 需要单独训练 | 不需要 |
| **显存占用** | 高（4个模型） | 低（2个模型） |
| **训练稳定性** | 需要调参，可能不稳定 | 更稳定 |
| **样本效率** | 需要大量采样 | 直接用离线偏好数据 |
| **过拟合风险** | 较低 | 较高（需正则化） |
| **泛化能力** | 通常更好 | 可能稍弱 |

---

## PyTorch 实现

```python
import torch
import torch.nn.functional as F

def dpo_loss(policy_model, ref_model, batch, beta=0.1):
    """
    policy_model: 正在训练的策略 π
    ref_model: 冻结的参考模型 π_ref (SFT模型)
    batch: {'prompt': ..., 'chosen': ..., 'rejected': ...}
    """
    # 计算策略模型的 log 概率
    pi_chosen_logps = policy_model(batch['prompt'], batch['chosen'])
    pi_rejected_logps = policy_model(batch['prompt'], batch['rejected'])
    
    # 计算参考模型的 log 概率（不计算梯度）
    with torch.no_grad():
        ref_chosen_logps = ref_model(batch['prompt'], batch['chosen'])
        ref_rejected_logps = ref_model(batch['prompt'], batch['rejected'])
    
    # DPO 损失
    pi_ratio = pi_chosen_logps - pi_rejected_logps
    ref_ratio = ref_chosen_logps - ref_rejected_logps
    
    logits = beta * (pi_ratio - ref_ratio)
    loss = -F.logsigmoid(logits).mean()
    
    return loss
```

---

## 变体与改进

| 方法 | 改进点 |
|------|--------|
| **IPO** | 用对比损失替代，解决 DPO 过拟合 |
| **KTO** | 只需要二元反馈（好/坏），不需要成对偏好 |
| **rDPO** | 添加长度正则化，防止模型变啰嗦 |
| **SimPO** | 移除参考模型，进一步简化 |
| **ORPO** | 将 SFT 和 DPO 合并为单阶段训练 |

---

## 一句话总结

> **DPO 通过数学推导把"训练奖励模型 + RL 优化"两步合并为一步，直接用偏好数据优化策略，更简单、更省资源。**

---

## 参考

- 论文：[Direct Preference Optimization: Your Language Model is Secretly a Reward Model](https://arxiv.org/abs/2305.18290)
- 来源：OpenClaw 会话 2026-04-15
