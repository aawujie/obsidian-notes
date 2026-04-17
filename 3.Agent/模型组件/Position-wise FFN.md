# Position-wise Feed-Forward Network (FFN)

> Transformer 中每个位置独立处理的前馈网络
> 整理日期：2026-03-28

---

## 一句话解释

**Position-wise FFN** = 对每个位置的向量，独立过一个 2层神经网络（升维 → 激活 → 降维），增加表达能力。

---

## 核心问题：在做什么？

### 具体步骤

```
输入: x = [x₁, x₂, x₃]  (3个位置，每个是512维向量)

Step 1: 升维（扩大4倍）
  x₁ → Linear(512 → 2048) → [大向量1]
  x₂ → Linear(512 → 2048) → [大向量2]  
  x₃ → Linear(512 → 2048) → [大向量3]

Step 2: 激活（非线性）
  [大向量1] → ReLU → [激活后1]
  [大向量2] → ReLU → [激活后2]
  [大向量3] → ReLU → [激活后3]

Step 3: 降维（缩回原大小）
  [激活后1] → Linear(2048 → 512) → x₁'
  [激活后2] → Linear(2048 → 512) → x₂'
  [激活后3] → Linear(2048 → 512) → x₃'

输出: [x₁', x₂', x₃']
```

### 代码实现

```python
class PositionwiseFFN(nn.Module):
    def __init__(self, d_model=512, d_ff=2048, dropout=0.1):
        super().__init__()
        self.w1 = nn.Linear(d_model, d_ff)   # 升维: 512 → 2048
        self.w2 = nn.Linear(d_ff, d_model)   # 降维: 2048 → 512
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        # x: (batch, seq, d_model)
        return self.w2(self.dropout(F.relu(self.w1(x))))
```

---

## 关键问题：为什么升维能增加表达能力？

### 类比：高维空间更容易分离

```
低维空间（2D）：
  ●  ●    两个点挤在一起，很难分开
  ●●●

高维空间（100D）：
  ●      ●      ●      点分散开，容易分开
  每个点有更多"方向"可以区分
```

### 具体例子

```
输入: [1, 2]  (2维)

升到 4 维:
  [1, 2, 1×2, 1+2] = [1, 2, 2, 3]
  
可以学习: x₁, x₂, x₁×x₂, x₁+x₂, x₁², ...
```

**升维 = 创造更多特征组合的可能性**

---

## 关键问题：为什么最后要降维回来？

### 原因1：保持维度一致，方便堆叠

```
Transformer 设计: 每个子层输出维度相同
  Attention 输入: (batch, seq, 512)
  Attention 输出: (batch, seq, 512)
  FFN 输入:       (batch, seq, 512)
  FFN 输出:       (batch, seq, 512)

好处: 可以堆叠很多层！
```

如果 FFN 输出 2048：
```
Layer 1: 512 → 2048
Layer 2: 需要 2048 → ?  → 越来越大！
Layer 3: 更大...
```

### 原因2：降维保留精华

```
输入 x: [特征1, 特征2, ..., 特征512]  (512维)

Step 1: 升维 512 → 2048
  创造新特征: [原特征..., 组合特征..., 非线性特征...]
  表达能力 ↑↑↑

Step 2: ReLU 激活
  筛选重要特征，去掉负数
  非线性变换

Step 3: 降维 2048 → 512
  压缩回原始维度
  但: 压缩后的 512 维包含了高维空间的"精华"

输出 x': [新特征1, 新特征2, ..., 新特征512]
  维度相同，但内容更丰富！
```

---

## Position-wise 的含义

### 直观对比

**非 Position-wise（Attention）**：
```
"猫" 的输出 = f(猫, 追, 老鼠)  ← 看所有词
"追" 的输出 = f(猫, 追, 老鼠)  ← 看所有词  
"老鼠" 的输出 = f(猫, 追, 老鼠)  ← 看所有词
```

**Position-wise（FFN）**：
```
"猫" 的输出 = f(猫)   ← 只看"猫"
"追" 的输出 = f(追)   ← 只看"追"
"老鼠" 的输出 = f(老鼠)  ← 只看"老鼠"
```

### 图示

```
┌─────────────────────────────────────┐
│  输入: [猫] [追] [老鼠]              │
│                                     │
│  Attention（非 Position-wise）       │
│     ↓ 互相看                        │
│  [猫+追+老鼠] [猫+追+老鼠] [猫+追+老鼠]│  ← 混合了所有信息
│                                     │
│  FFN（Position-wise）                │
│     ↓ 各自处理                       │
│  [猫'] [追'] [老鼠']                  │  ← 每个位置独立变换
│     ↓ 各自处理                       │
│  [猫''] [追''] [老鼠'']               │  ← 每个位置独立变换
└─────────────────────────────────────┘
```

---

## 好处（为什么需要 Position-wise FFN？）

| 好处 | 说明 |
|------|------|
| **并行计算** | 每个位置独立，GPU 友好，速度快 |
| **非线性变换** | ReLU 增加表达能力，Attention 只是线性加权 |
| **大容量** | 4× 扩展，Transformer 大部分参数在 FFN |
| **稳定** | 位置独立，处理长序列更稳定 |

### 和 Attention 的关系

```
Transformer Block:
┌─────────────────────────┐
│  Attention              │  ← 负责"交流"（混合不同位置信息）
│  "猫" 看到 "追"、"老鼠"  │
└─────────────────────────┘
           ↓
┌─────────────────────────┐
│  FFN (Position-wise)    │  ← 负责"深度思考"（每个位置独立变换）
│  "猫" 自己过神经网络     │
│  "追" 自己过神经网络     │
│  "老鼠" 自己过神经网络   │
└─────────────────────────┘
```

**类比**：
- Attention = **开会讨论**（大家交换意见）
- Position-wise FFN = **会后各自深度思考**（每个人独立消化、产生新想法）

---

## 超参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `d_model` | 512 | 输入/输出维度 |
| `d_ff` | 2048 | 中间维度（通常是 d_model 的 4 倍）|
| `dropout` | 0.1 | 正则化 |

---

## 常见变体

### GELU 替代 ReLU

```python
# BERT、GPT 等使用 GELU 替代 ReLU
class PositionwiseFFN_GELU(nn.Module):
    def forward(self, x):
        return self.w2(self.dropout(F.gelu(self.w1(x))))
```

### GLU 变体

```python
# SwiGLU、GEGLU 等更现代的变体
class SwiGLU(nn.Module):
    def forward(self, x):
        x1 = self.w1(x)
        x2 = self.w2(x)
        return self.w3(F.silu(x1) * x2)
```

---

## 一句话总结

> **Position-wise FFN = 升维创造"工作空间"学习复杂特征，降维保留精华，每个位置独立处理，增加表达能力。**

---

## 相关笔记

- [[Transformer架构从零理解]] —— FFN 在 Transformer 中的位置
- [[Multi-Head Attention]] —— 与 FFN 互补的注意力机制
- [[激活函数]] —— ReLU、GELU、Swish 等
