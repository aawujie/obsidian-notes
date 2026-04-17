# Batch Normalization —— 批归一化

> 深度学习中的归一化技术，对整个 batch 的每个特征维度进行归一化
> 整理日期：2026-03-28

---

## 一句话解释

**Batch Normalization** = 对整个 batch 的**每个特征**做归一化（减均值、除标准差），加速训练，允许更大学习率，有轻微正则化效果。

---

## 直观理解

### 为什么需要 BN？

**问题：Internal Covariate Shift（内部协变量偏移）**

```
网络层数多了，数据分布会漂移：

Layer 1:  输入 [0.1, 0.5, 1.0]     均值=0.53
Layer 2:  输出 [5.0, 10.0, 20.0]   均值=11.67  ← 分布变了！
Layer 3:  输出 [100, 500, 1000]    均值=533    ← 爆炸了！
```

**后果**：
- 上层网络需要不断适应下层的新分布
- 训练变慢，需要小心调学习率
- 容易梯度消失/爆炸

**解决**：每层后面加 BN，把数据拉回标准分布

```
BN 后: 均值≈0, 标准差≈1，分布稳定
```

---

## 公式

### 训练时

```
输入: x = [x₁, x₂, ..., x_m]  (batch size=m，某个特征)

1. 计算 batch 均值:    μ_B = (1/m) Σ xᵢ
2. 计算 batch 方差:    σ²_B = (1/m) Σ (xᵢ - μ_B)²
3. 归一化:            x̂ᵢ = (xᵢ - μ_B) / √(σ²_B + ε)
4. 缩放平移:          yᵢ = γ · x̂ᵢ + β

输出: y = [y₁, y₂, ..., y_m]
```

### 推理时

```
使用训练时保存的 running statistics：

y = γ · (x - μ_running) / √(σ²_running + ε) + β

μ_running = momentum · μ_running + (1-momentum) · μ_B
σ²_running = momentum · σ²_running + (1-momentum) · σ²_B
```

---

## 代码实现

### PyTorch 版

```python
import torch
import torch.nn as nn

# 创建 BN 层
batch_norm = nn.BatchNorm1d(num_features=512)     # 1D BN，用于全连接层
batch_norm2d = nn.BatchNorm2d(num_features=64)    # 2D BN，用于 CNN

# 使用
output = batch_norm(input)                        # 自动计算 batch 均值方差
```

### 手动实现

```python
import torch

def batch_norm_manual(x, gamma, beta, eps=1e-5):
    """
    x: (batch, features) 或 (batch, channels, H, W)
    gamma: 缩放参数，形状 (features,) 或 (channels,)
    beta: 平移参数，形状 (features,) 或 (channels,)
    """
    if len(x.shape) == 2:  # 全连接层
        mean = x.mean(dim=0, keepdim=True)            # 沿 batch 求均值
        var = x.var(dim=0, keepdim=True, unbiased=False)  # 沿 batch 求方差
    else:  # 卷积层
        mean = x.mean(dim=[0, 2, 3], keepdim=True)    # 沿 batch, H, W 求均值
        var = x.var(dim=[0, 2, 3], keepdim=True, unbiased=False)
    
    x_norm = (x - mean) / torch.sqrt(var + eps)       # 归一化
    return gamma * x_norm + beta                      # 缩放平移
```

### 完整示例

```python
import torch
import torch.nn as nn

# 输入: (batch=4, features=3)
x = torch.tensor([
    [1.0, 2.0, 3.0],
    [2.0, 3.0, 4.0],
    [3.0, 4.0, 5.0],
    [4.0, 5.0, 6.0]
])

print("输入形状:", x.shape)           # (4, 3)

# 计算每个特征的均值和方差（沿 batch 维度）
mean = x.mean(dim=0)                  # [2.5, 3.5, 4.5]
var = x.var(dim=0)                    # [1.25, 1.25, 1.25]

print(f"特征均值: {mean}")            # 每个特征一个均值
print(f"特征方差: {var}")             # 每个特征一个方差

# BN 层
bn = nn.BatchNorm1d(3)
x_norm = bn(x)

print(f"BN 后均值: {x_norm.mean(dim=0)}")   # ≈ [0, 0, 0]
print(f"BN 后方差: {x_norm.var(dim=0)}")    # ≈ [1, 1, 1]
```

---

## Batch Norm vs Layer Norm

| 对比项 | Batch Norm | Layer Norm |
|--------|-----------|------------|
| **归一化方向** | 沿 batch 维度 | 沿特征维度 |
| **计算均值/方差** | 整个 batch 一起计算 | 每个样本单独计算 |
| **依赖 batch size** | ✅ **依赖**（小 batch 效果差） | ❌ 不依赖 |
| **适合场景** | **CV（图像）**、大 batch | **NLP（文本）**、小 batch |
| **训练和推理** | 需要维护 running statistics | 一致 |
| **序列长度变化** | ❌ 不适合 | ✅ 适合 |

### 图示对比

```
输入形状: (batch=2, seq=3, features=4)

Batch Norm（沿 batch 方向）:
┌─────────────────────────┐
│  特征0    特征1    特征2    特征3  │
│ ┌────┐  ┌────┐  ┌────┐  ┌────┐ │
│ │样本0│  │样本0│  │样本0│  │样本0│ │
│ │样本1│  │样本1│  │样本1│  │样本1│ │ ← 计算这列的均值/方差
│ └────┘  └────┘  └────┘  └────┘ │
│   ↓       ↓       ↓       ↓     │
│  μ₀      μ₁      μ₂      μ₃    │
└─────────────────────────┘
每个特征位置，跨 batch 计算

Layer Norm（沿特征方向）:
┌─────────────────────────┐
│ 样本0: [f0, f1, f2, f3] │ ← 计算这行的均值/方差
│ 样本1: [f0, f1, f2, f3] │ ← 计算这行的均值/方差
└─────────────────────────┘
每个样本，跨特征计算
```

---

## 在 CNN 中的使用

### 位置

```
Conv Block:
┌─────────────────────────────────────┐
│  Conv2d                             │
│     ↓                               │
│  BatchNorm2d  ← BN 在这里！          │  # 卷积后归一化
│     ↓                               │
│  ReLU                               │
└─────────────────────────────────────┘
```

### 代码

```python
class ConvBlock(nn.Module):
    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.conv = nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1)
        self.bn = nn.BatchNorm2d(out_channels)              # 2D BN
        self.relu = nn.ReLU()
    
    def forward(self, x):
        x = self.conv(x)
        x = self.bn(x)                                      # BN
        x = self.relu(x)
        return x
```

---

## 优点

| 优点 | 说明 |
|------|------|
| **加速训练** | 允许使用更大学习率，收敛更快（6x 甚至更多） |
| **稳定分布** | 减少 Internal Covariate Shift |
| **正则化效果** | 每个样本依赖 batch 内其他样本，有轻微正则化 |
| **允许更高学习率** | 梯度更稳定，不容易爆炸 |
| **对初始化不敏感** | 不那么依赖精心的权重初始化 |

---

## 缺点

| 缺点 | 说明 |
|------|------|
| **依赖 batch size** | batch 太小（<32）时统计不稳定，效果差 |
| **训练和推理不一致** | 需要维护 running mean/var，容易出错 |
| **不适合 RNN** | 序列长度变化，难以应用 |
| **不适合小数据集** | 统计量估计不准 |

---

## 训练和推理的区别

### 训练时

```python
# 训练模式
model.train()
output = model(input)  # 使用当前 batch 的均值/方差

# 同时更新 running statistics
running_mean = momentum * running_mean + (1-momentum) * batch_mean
running_var = momentum * running_var + (1-momentum) * batch_var
```

### 推理时

```python
# 评估模式
model.eval()
with torch.no_grad():
    output = model(input)  # 使用 running mean/var，而不是当前 batch
```

**注意**：推理时一定要 `model.eval()`，否则会用当前 batch 统计，导致结果不一致！

---

## 超参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `eps` | 1e-5 | 防止除以0的小常数 |
| `momentum` | 0.1 | running statistics 的动量 |
| `affine` | True | 是否学习 γ 和 β |
| `track_running_stats` | True | 是否跟踪 running mean/var |

---

## 常见错误

### 错误1：推理时忘记 eval()

```python
# ❌ 错误
model.train()
output = model(test_data)  # 用了 test_data 的统计量，结果不对

# ✅ 正确
model.eval()
with torch.no_grad():
    output = model(test_data)  # 用训练时的 running statistics
```

### 错误2：batch size 太小

```python
# ❌ 小 batch（<32），统计不稳定
batch_norm = nn.BatchNorm1d(512)

# ✅ 使用 Layer Norm 替代
layer_norm = nn.LayerNorm(512)
```

### 错误3：RNN 中用 BN

```python
# ❌ 不推荐
rnn_output = batch_norm(rnn_output)

# ✅ 用 Layer Norm
rnn_output = layer_norm(rnn_output)
```

---

## 可视化

```python
import matplotlib.pyplot as plt
import torch
import torch.nn as nn

# 模拟不同 batch size 的效果
batch_sizes = [2, 4, 8, 16, 32, 64]
variances = []

for bs in batch_sizes:
    x = torch.randn(bs, 100) * 5 + 10  # 均值10，标准差5
    bn = nn.BatchNorm1d(100)
    x_norm = bn(x)
    variances.append(x_norm.var().item())

plt.plot(batch_sizes, variances, marker='o')
plt.axhline(y=1.0, color='r', linestyle='--', label='Target variance=1')
plt.xlabel('Batch Size')
plt.ylabel('Variance after BN')
plt.title('Batch Norm: Small batch = unstable')
plt.legend()
plt.show()
```

**结论**：batch size 越大，BN 越稳定。

---

## 一句话总结

> **Batch Norm = 跨 batch 对每个特征归一化，加速训练，适合 CNN 大 batch，不适合 NLP 小 batch。**

---

## 相关笔记

- [[Layer Normalization]] —— 层归一化对比
- [[Group Normalization]] —— 组归一化（BN 的替代）
- [[Instance Normalization]] —— 实例归一化
- [[Transformer架构从零理解]] —— 为什么 Transformer 用 LN 而不是 BN
