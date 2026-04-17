# Layer Normalization —— 层归一化

> 深度学习中的归一化技术，对每个样本的特征维度进行归一化
> 整理日期：2026-03-28

---

## 一句话解释

**Layer Normalization** = 对每个样本的**所有特征**做归一化（减均值、除标准差），让数据分布稳定，加速训练。

---

## 直观理解

### 为什么需要归一化？

**问题**：神经网络层数多了，数据分布会漂移（Internal Covariate Shift）

```
输入:  [0.1, 0.5, 1.0, 2.0]     均值=0.9,  方差大
Layer1: [5.0, 10.0, 20.0, 50.0]  均值=21.25, 方差更大
Layer2: [100, 500, 1000, 5000]   爆炸了！
```

**解决**：每层后面加归一化，把数据拉回标准分布

```
Layer Norm 后: [−0.8, −0.2, 0.4, 1.2]  均值≈0, 标准差≈1
```

---

## 公式

### 计算步骤

```
输入: x = [x₁, x₂, ..., x_d]  (d 个特征)

1. 计算均值:    μ = (1/d) Σ xᵢ
2. 计算方差:    σ² = (1/d) Σ (xᵢ - μ)²
3. 归一化:      x̂ᵢ = (xᵢ - μ) / √(σ² + ε)
4. 缩放平移:    yᵢ = γ · x̂ᵢ + β

输出: y = [y₁, y₂, ..., y_d]
```

### 参数

| 符号 | 名称 | 作用 |
|------|------|------|
| ε (epsilon) | 小常数 | 防止除以0，通常 1e-5 |
| γ (gamma) | 缩放参数 | 可学习，恢复表达能力 |
| β (beta) | 平移参数 | 可学习，恢复表达能力 |

---

## 代码实现

### PyTorch 版

```python
import torch
import torch.nn as nn

# 方法1：使用 nn.LayerNorm
layer_norm = nn.LayerNorm(normalized_shape=512)  # 特征维度512
output = layer_norm(input)                       # 自动计算均值方差

# 方法2：手动实现
def layer_norm_manual(x, eps=1e-5):
    """
    x: (batch, seq, features) 或 (batch, features)
    """
    mean = x.mean(dim=-1, keepdim=True)           # 沿最后一维（特征维）求均值
    var = x.var(dim=-1, keepdim=True, unbiased=False)  # 求方差
    x_norm = (x - mean) / torch.sqrt(var + eps)   # 归一化
    return x_norm
```

### 手动实现详解

```python
import torch

# 输入: (batch=2, features=4)
x = torch.tensor([
    [1.0, 2.0, 3.0, 4.0],
    [0.5, 1.5, 2.5, 3.5]
])

# 计算
mean = x.mean(dim=-1, keepdim=True)               # [[2.5], [2.0]]
var = x.var(dim=-1, keepdim=True)                 # [[1.25], [1.25]]
std = torch.sqrt(var + 1e-5)                      # [[1.118], [1.118]]

# 归一化
x_norm = (x - mean) / std                         # [[-1.34, -0.45, 0.45, 1.34],
                                                  #  [-1.34, -0.45, 0.45, 1.34]]

print(f"均值: {x_norm.mean(dim=-1)}")             # [0., 0.]
print(f"标准差: {x_norm.std(dim=-1)}")            # [1., 1.]
```

---

## Layer Norm vs Batch Norm

| 对比项 | Layer Norm | Batch Norm |
|--------|-----------|------------|
| **归一化方向** | 沿特征维度（每样本） | 沿 batch 维度（每特征） |
| **计算均值/方差** | 每个样本单独计算 | 整个 batch 一起计算 |
| **依赖 batch size** | ❌ 不依赖 | ✅ 依赖（小 batch 效果差） |
| **适合场景** | NLP（序列长度变化） | CV（图像大小固定） |
| **训练和推理** | 一致 | 需要维护 running statistics |

### 图示对比

```
输入形状: (batch=2, seq=3, features=4)

Batch Norm（沿 batch 方向）:
┌─────────────────────────┐
│ 样本0  样本1            │  ← 计算这列的均值/方差
│ [0.1]  [0.2]            │
│ [0.3]  [0.4]            │
│ [0.5]  [0.6]            │
└─────────────────────────┘
每个特征位置，跨 batch 计算

Layer Norm（沿特征方向）:
┌─────────────────────────┐
│ 样本0: [0.1, 0.2, 0.3, 0.4] │  ← 计算这行的均值/方差
│ 样本1: [0.5, 0.6, 0.7, 0.8] │  ← 计算这行的均值/方差
└─────────────────────────┘
每个样本，跨特征计算
```

---

## 在 Transformer 中的使用

### 位置

```
Transformer Block:
┌─────────────────────────────────────┐
│  Input                              │
│     ↓                               │
│  Multi-Head Attention               │
│     ↓                               │
│  Add & Norm  ← Layer Norm 在这里！   │  # 残差连接后归一化
│     ↓                               │
│  Feed Forward                       │
│     ↓                               │
│  Add & Norm  ← Layer Norm 在这里！   │  # 残差连接后归一化
└─────────────────────────────────────┘
```

### 代码

```python
class AddNorm(nn.Module):                                   # 残差连接 + LayerNorm
    def __init__(self, d_model, dropout=0.1):               # 初始化
        super().__init__()                                  # 父类初始化
        self.norm = nn.LayerNorm(d_model)                   # LayerNorm 层
        self.dropout = nn.Dropout(dropout)                  # Dropout

    def forward(self, x, sublayer_output):                  # 前向传播
        # x: 原始输入（残差连接用）
        # sublayer_output: 子层输出（Attention 或 FFN 的输出）
        return self.norm(x + self.dropout(sublayer_output))  # 残差 + Dropout + LayerNorm
```

---

## 为什么 Transformer 用 Layer Norm？

| 原因 | 说明 |
|------|------|
| **序列长度变化** | NLP 句子长度不一，Batch Norm 统计不稳定 |
| **不依赖 batch size** | 小 batch 也能稳定训练 |
| **训练和推理一致** | 不需要维护 running mean/var |
| **并行友好** | 每个样本独立计算，容易并行 |

---

## 可视化

```python
import matplotlib.pyplot as plt
import torch

# 模拟经过多层后的数据分布
x = torch.randn(1000, 50) * torch.tensor([1, 2, 3, 4, 5] * 10)  # 不同特征不同尺度

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# 归一化前
axes[0].hist(x.numpy().flatten(), bins=50)
axes[0].set_title('Before Layer Norm')
axes[0].set_xlabel('Value')
axes[0].set_ylabel('Frequency')

# 归一化后
layer_norm = torch.nn.LayerNorm(50)
x_norm = layer_norm(x)
axes[1].hist(x_norm.detach().numpy().flatten(), bins=50)
axes[1].set_title('After Layer Norm')
axes[1].set_xlabel('Value')
axes[1].set_ylabel('Frequency')

plt.show()
```

**效果**：数据从各种分布变成标准正态分布（均值0，标准差1）。

---

## 常见变体

### Pre-LN vs Post-LN

```python
# Post-LN（原始 Transformer）
x = x + Attention(LayerNorm(x))     # 先归一化，再子层，再残差

# Pre-LN（更稳定，推荐）
x = x + Attention(x)                # 先子层，再残差，再归一化
x = LayerNorm(x)
```

| 类型 | 公式 | 特点 |
|------|------|------|
| **Post-LN** | `LayerNorm(x + Sublayer(x))` | 原始设计，需要 Warmup |
| **Pre-LN** | `x + Sublayer(LayerNorm(x))` | 更稳定，训练更快 |

---

## 一句话总结

> **Layer Norm = 每个样本内部做归一化，稳定分布，加速训练，特别适合 NLP 变长序列。**

---

## 相关笔记

- [[Batch Normalization]] —— 批归一化对比
- [[Transformer架构从零理解]] —— LayerNorm 在 Transformer 中的应用
- [[Add & Norm]] —— 残差连接与归一化
- [[Internal Covariate Shift]] —— 内部协变量偏移问题
