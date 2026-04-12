# 投影矩阵 Projection Matrix

## 直观理解

想象一束光垂直照射到一个平面上，物体在平面上的**影子**就是投影。

| 类型 | 类比 | 数学含义 |
|------|------|----------|
| **上投影矩阵** (U) | 从低维空间 → 高维空间 | 升维、扩展、Embedding |
| **下投影矩阵** (D) | 从高维空间 → 低维空间 | 降维、压缩、Pooling |

---

## 具体例子

### 1. 上投影矩阵 (Up-projection)

```python
# 把 10 维向量映射到 100 维
U = torch.randn(10, 100)  # 上投影矩阵: (低维, 高维)
x_low = torch.randn(5, 10)  # 输入: (batch, 低维)
x_high = x_low @ U  # 输出: (5, 100) 升维了!
```

**应用场景**：
- Transformer 的 FFN 第一层：`d_model → 4*d_model`
- 从 hidden dim 升维到更大空间做非线性变换

---

### 2. 下投影矩阵 (Down-projection)

```python
# 把 100 维向量映射到 10 维
D = torch.randn(100, 10)  # 下投影矩阵: (高维, 低维)
x_high = torch.randn(5, 100)  # 输入: (batch, 高维)
x_low = x_high @ D  # 输出: (5, 10) 降维了!
```

**应用场景**：
- Transformer 的 FFN 第二层：`4*d_model → d_model`
- 从升维后的空间压缩回原始维度

---

## 在 FFN 中的完整流程

```
Input (d_model) 
    ↓
[上投影] W1: (d_model, 4*d_model)  ← 扩展 4 倍
    ↓
Activation (GELU/ReLU)
    ↓
[下投影] W2: (4*d_model, d_model)  ← 压缩回原始维度
    ↓
Output (d_model)
```

---

## 为什么需要这样设计？

| 目的 | 解释 |
|------|------|
| **增加表达能力** | 先升维到更大空间，可以学习更复杂的特征 |
| **非线性变换** | 在中间维度做激活，增加非线性 |
| **参数效率** | 两个矩阵的参数总量比单个大矩阵少 |
| **残差连接** | 最终输出维度与输入相同，方便残差连接 |

---

## 代码示例

```python
import torch
import torch.nn as nn

d_model = 512
d_ff = 2048  # 4 * d_model

# FFN 的两层
W1 = nn.Linear(d_model, d_ff)  # 上投影: 512 → 2048
W2 = nn.Linear(d_ff, d_model)  # 下投影: 2048 → 512

x = torch.randn(2, 10, d_model)  # (batch, seq_len, d_model)

# 前向传播
h = W1(x)      # 上投影: (2, 10, 2048)
h = torch.relu(h)
out = W2(h)    # 下投影: (2, 10, 512)

print(f"输入: {x.shape}")
print(f"中间: {h.shape}")
print(f"输出: {out.shape}")
```

---

## 总结

| | 上投影 | 下投影 |
|--|--------|--------|
| **方向** | 低维 → 高维 | 高维 → 低维 |
| **形状** | (小, 大) | (大, 小) |
| **作用** | 扩展、增加表达能力 | 压缩、回到目标维度 |
| **典型用例** | FFN 第一层 | FFN 第二层 |

---

*Created: 2026-04-12*
