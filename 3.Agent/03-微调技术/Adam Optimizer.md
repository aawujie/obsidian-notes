# Adam Optimizer —— 自适应学习率优化算法

> 结合 Momentum 和 RMSProp 的优化算法，为每个参数单独调整学习率
> 整理日期：2026-03-28

---

## 一句话

**Adam = 动量（Momentum）+ 自适应学习率（RMSProp），为每个参数单独调整学习率。**

---

## 核心思想

### 传统 SGD 的问题

```
参数更新 = -学习率 × 梯度

问题：
- 所有参数用同一个学习率
- 梯度大的参数震荡，梯度小的参数更新慢
- 容易陷入局部最优
```

### Adam 的解决

```
参数更新 = -自适应学习率 × 动量梯度

优势：
- 每个参数有自己的学习率
- 动量加速收敛
- 自适应调整步长
```

---

## 三个关键超参数

| 参数          | 符号  | 默认值   | 作用                |
| ----------- | --- | ----- | ----------------- |
| **Beta1**   | β₁  | 0.9   | 一阶矩估计（动量）的衰减率     |
| **Beta2**   | β₂  | 0.999 | 二阶矩估计（自适应学习率）的衰减率 |
| **Epsilon** | ε   | 1e-8  | 防止除以0的小常数         |

---

## 更新公式

### 算法步骤

```python
# 1. 计算梯度
g_t = ∇L(θ_t)                    # 当前梯度

# 2. 更新一阶矩（动量）
m_t = β₁ × m_{t-1} + (1-β₁) × g_t    # 梯度的指数移动平均

# 3. 更新二阶矩（自适应学习率）
v_t = β₂ × v_{t-1} + (1-β₂) × g_t²   # 梯度平方的指数移动平均

# 4. 偏差修正（初期 t 较小，需要修正）
m̂_t = m_t / (1-β₁^t)            # 修正一阶矩
v̂_t = v_t / (1-β₂^t)            # 修正二阶矩

# 5. 更新参数
θ_{t+1} = θ_t - α × m̂_t / (√v̂_t + ε)
          ↑学习率  ↑动量方向  ↑自适应调整
```

### 直观理解

```
更新步长 = 学习率 × 动量方向 / (梯度方差的开方 + ε)

- 动量方向：之前梯度的平均（往哪走）
- 梯度方差：梯度变化的大小（走多快）
- 分母大（梯度变化大）→ 步长小（小心）
- 分母小（梯度稳定）→ 步长大（大胆）
```

---

## 两个组成部分

### 1. Momentum（一阶矩）

```
m_t = β₁ × m_{t-1} + (1-β₁) × g_t

想象滚下山：
- 没有动量：每步只看当前坡度，容易震荡
- 有动量：考虑之前的速度，滚得更快更稳

β₁ = 0.9 表示：90% 靠惯性，10% 靠当前梯度
```

### 2. Adaptive Learning（二阶矩）

```
v_t = β₂ × v_{t-1} + (1-β₂) × g_t²

自适应调整：
- 梯度大的参数 → 学习率自动变小（小心走）
- 梯度小的参数 → 学习率自动变大（大胆走）

β₂ = 0.999 表示：99.9% 靠历史，0.1% 靠当前
```

---

## 代码实现

### PyTorch 版

```python
import torch
import torch.nn as nn
import torch.optim as optim

# 创建模型
model = nn.Linear(10, 1)

# 创建 Adam 优化器
optimizer = optim.Adam(
    model.parameters(),      # 模型参数
    lr=0.001,               # 初始学习率 α
    betas=(0.9, 0.999),     # (β₁, β₂)
    eps=1e-8,               # ε
    weight_decay=0          # L2 正则化（可选）
)

# 训练循环
for epoch in range(100):
    for batch in dataloader:
        optimizer.zero_grad()   # 1. 清零梯度
        output = model(batch)   # 2. 前向传播
        loss = criterion(output, target)  # 3. 计算损失
        loss.backward()         # 4. 反向传播
        optimizer.step()        # 5. 更新参数
```

### 手动实现

```python
class Adam:
    def __init__(self, params, lr=0.001, betas=(0.9, 0.999), eps=1e-8):
        self.params = list(params)
        self.lr = lr
        self.beta1, self.beta2 = betas
        self.eps = eps
        
        self.m = [torch.zeros_like(p) for p in self.params]  # 一阶矩
        self.v = [torch.zeros_like(p) for p in self.params]  # 二阶矩
        self.t = 0  # 时间步
    
    def step(self):
        self.t += 1
        for i, p in enumerate(self.params):
            if p.grad is None:
                continue
            
            g = p.grad  # 梯度
            
            # 更新一阶矩和二阶矩
            self.m[i] = self.beta1 * self.m[i] + (1 - self.beta1) * g
            self.v[i] = self.beta2 * self.v[i] + (1 - self.beta2) * (g ** 2)
            
            # 偏差修正
            m_hat = self.m[i] / (1 - self.beta1 ** self.t)
            v_hat = self.v[i] / (1 - self.beta2 ** self.t)
            
            # 更新参数
            p.data -= self.lr * m_hat / (torch.sqrt(v_hat) + self.eps)
    
    def zero_grad(self):
        for p in self.params:
            if p.grad is not None:
                p.grad.zero_()
```

---

## Adam vs SGD 对比

| 对比项 | SGD | Adam |
|--------|-----|------|
| **学习率** | 固定 | 自适应（每个参数不同）|
| **动量** | 可选（SGD with Momentum） | 内置 |
| **收敛速度** | 慢，需要调学习率 | 快，自动调整 |
| **内存占用** | 小（只存参数和梯度） | 大（存一阶、二阶矩）|
| **泛化能力** | 通常更好 | 可能过拟合（需要早停）|
| **调参难度** | 难（学习率敏感） | 容易（默认参数好用）|
| **适用场景** | CV 大模型、图像分类 | NLP、Transformer、推荐系统 |

### 收敛速度对比

```
Loss
  ↑
  │    ╲ Adam（快）
  │     ╲
  │      ╲
  │       ╲    ╱ SGD（慢但稳）
  │        ╲  ╱
  │         ╲╱
  └────────────────→ Step

Adam：前期快速下降，后期可能震荡
SGD：前期慢，后期更稳定，泛化更好
```

---

## Transformer 为什么用 Adam？

### 原论文参数

```python
optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0,                   # 初始为0，配合 Warmup
    betas=(0.9, 0.98),      # β₁=0.9, β₂=0.98（注意！不是0.999）
    eps=1e-9                # 比默认 1e-8 更小
)
```

### 为什么 β₂=0.98？

```
默认 β₂=0.999：非常保守，历史权重99.9%
Transformer β₂=0.98：更激进，历史权重98%

原因：
- Transformer 梯度不稳定（Attention 权重变化大）
- β₂=0.98 让二阶矩更新更快，适应变化
- 配合 Warmup 学习率调度，训练更稳定
```

### 为什么配合 Warmup？

```
Adam 初期问题：
- m 和 v 都初始化为0
- 初期梯度大，v 很小 → 步长巨大 → 爆炸

Warmup 解决：
- 前 N 步学习率很小
- 让 m 和 v 积累足够历史
- 再正常训练
```

---

## 变体算法

| 算法 | 改进点 | 适用场景 |
|------|--------|---------|
| **AdamW** | 解耦权重衰减 | 推荐默认使用 |
| **Adamax** | 用 max 替代 sqrt | 更稳定 |
| **RAdam** | 修正 Warmup | 无需手动 Warmup |
| **LAMB** | 支持超大 batch | 预训练大模型 |
| **NAdam** | Nesterov 动量 | 更快收敛 |

### AdamW（推荐）

```python
# AdamW 将权重衰减和 L2 正则化解耦
optimizer = torch.optim.AdamW(
    model.parameters(),
    lr=0.001,
    betas=(0.9, 0.999),
    eps=1e-8,
    weight_decay=0.01  # 真正的权重衰减，不是 L2
)
```

---

## 常见问题

### Q: Adam 需要学习率调度吗？
**A:** 需要！Adam 配合 Warmup + Decay 效果更好，单纯 Adam 可能收敛到次优点。

### Q: Adam 会过拟合吗？
**A:** 会。Adam 收敛快但泛化可能不如 SGD，建议：
- 使用 AdamW
- 早停（Early Stopping）
- 学习率衰减

### Q: 什么情况下不用 Adam？
**A:** 
- CV 大模型（ResNet、VGG）用 SGD + Momentum 更好
- 需要极致泛化时，SGD + 仔细调参可能更好

### Q: β₁、β₂ 怎么调？
**A:** 通常用默认值（0.9, 0.999），Transformer 用（0.9, 0.98）。

---

## 一句话总结

> **Adam = 动量加速 + 自适应学习率，为每个参数定制更新策略，训练快但可能过拟合，推荐用 AdamW。**

---

## 相关笔记

- [[SGD优化器]] —— 传统梯度下降
- [[Momentum]] —— 动量原理
- [[RMSProp]] —— 自适应学习率
- [[学习率调度]] —— Warmup + Decay
- [[AdamW]] —— Adam 的改进版
