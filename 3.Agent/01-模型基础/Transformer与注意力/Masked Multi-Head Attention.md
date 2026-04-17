# Masked Multi-Head Attention —— 掩码多头注意力

> Transformer 解码器中防止偷看未来的注意力机制
> 整理日期：2026-03-28

---

## 一句话解释

**Masked Multi-Head Attention** = 多头注意力 + **因果掩码**，只能看已生成的词，不能偷看未来。

---

## 直观对比

### 普通 Multi-Head Attention（编码器用）

```
输入: "我 是 学生"

"我"   看到 [我, 是, 学生]  ← 能看到所有词
"是"   看到 [我, 是, 学生]  ← 能看到所有词
"学生" 看到 [我, 是, 学生]  ← 能看到所有词
```

### Masked Multi-Head Attention（解码器用）

```
生成 "I am a student" 时：

第1步: 输入 [<bos>]       → 预测 "I"     （只能看 <bos>）
第2步: 输入 [<bos>, I]    → 预测 "am"    （只能看 <bos>, I）
第3步: 输入 [<bos>, I, am] → 预测 "a"     （只能看 <bos>, I, am）
第4步: 输入 [<bos>, I, am, a] → 预测 "student" （只能看前面4个）

不能偷看未来！
```

---

## 实现方式：下三角掩码

### 掩码矩阵

```
      位置0  位置1  位置2  位置3
位置0 [  1     0     0     0  ]  ← 只能看自己
位置1 [  1     1     0     0  ]  ← 能看位置0和自己
位置2 [  1     1     1     0  ]  ← 能看位置0、1和自己
位置3 [  1     1     1     1  ]  ← 能看所有已生成的

1 = 可以看（允许注意力）
0 = 不能看（mask掉）
```

### 代码实现

```python
def make_causal_mask(size):                                 # 创建因果掩码（下三角）
    """生成下三角掩码矩阵"""
    return torch.tril(torch.ones(size, size))               # tril = lower triangular

# 示例：size=3
# [[1., 0., 0.],
#  [1., 1., 0.],
#  [1., 1., 1.]]
```

---

## 在注意力计算中的应用

### 完整流程

```python
def scaled_dot_product_attention(Q, K, V, mask=None):       # 缩放点积注意力
    d_k = Q.size(-1)                                        # 获取每个头的维度
    scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(d_k)  # QK^T / sqrt(d_k)
    
    if mask is not None:                                    # 如果提供了掩码
        scores = scores.masked_fill(mask == 0, float('-inf'))  # mask位置设为负无穷
    
    weights = F.softmax(scores, dim=-1)                     # softmax，mask位置变成0
    output = torch.matmul(weights, V)                       # 加权求和
    return output, weights
```

### 掩码效果演示

```python
# 假设 scores = [[2.0, 1.0, 0.5],
#                [1.5, 2.5, 1.0],
#                [0.5, 1.0, 2.0]]

# 应用 mask = [[1, 0, 0],
#              [1, 1, 0],
#              [1, 1, 1]]

# masked_fill 后: [[2.0, -inf, -inf],
#                  [1.5,  2.5, -inf],
#                  [0.5,  1.0,  2.0]]

# softmax 后:     [[1.0,  0.0,  0.0],   ← 位置0只能看自己
#                  [0.27, 0.73,  0.0],   ← 位置1能看0和1
#                  [0.18, 0.33,  0.49]]  ← 位置2能看0、1、2
```

---

## 为什么需要 Mask？

### 训练时：防止偷看答案

| 场景 | 说明 |
|------|------|
| 有 Mask | 模型只能看已生成的词，模拟真实推理过程 |
| 无 Mask | 模型直接看到正确答案，训练作弊 |

### 推理时：自回归生成

```python
# 推理时逐词生成
def generate(model, src, max_len=50):
    tgt = [<bos>]                                           # 从 <bos> 开始
    for i in range(max_len):
        output = model(src, tgt)                            # 前向传播
        next_word = argmax(output[-1])                      # 取最后一个位置的预测
        tgt.append(next_word)                               # 添加到序列
        if next_word == <eos>:                              # 遇到 <eos> 停止
            break
    return tgt
```

**关键**：每次只能看到已生成的词，mask 保证这一点。

---

## 在 Transformer 中的位置

```
Decoder Layer:
┌─────────────────────────────────────┐
│  Masked Multi-Head Attention        │  ← 这里！只能看已生成的词
│  (Self-Attention with mask)         │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  Cross Multi-Head Attention         │  ← 看编码器输出（不需要mask）
│  (Encoder-Decoder Attention)        │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  Feed Forward Network               │
└─────────────────────────────────────┘
```

---

## 与其他 Mask 的区别

| Mask 类型 | 作用 | 位置 |
|-----------|------|------|
| **Causal Mask** | 防止看未来 | Decoder Self-Attention |
| **Padding Mask** | 忽略填充位置 | Encoder + Decoder |
| **Attention Mask** | 自定义注意力范围 | 可选 |

### Padding Mask

```python
def make_pad_mask(seq, pad_idx=0):                          # 创建填充掩码
    return (seq != pad_idx).unsqueeze(1).unsqueeze(2)       # 标记非填充位置

# 作用：让模型忽略 <pad> 位置，不计算注意力
```

---

## 可视化理解

```
生成 "I am a student" 时的注意力权重：

Step 1 (预测 "I"):
    [<bos>] → "I"
    注意力: [1.0, 0.0, 0.0, 0.0, 0.0]  ← 只能看 <bos>

Step 2 (预测 "am"):
    [<bos>, I] → "am"
    注意力: [0.3, 0.7, 0.0, 0.0, 0.0]  ← 看 <bos> 和 I

Step 3 (预测 "a"):
    [<bos>, I, am] → "a"
    注意力: [0.2, 0.3, 0.5, 0.0, 0.0]  ← 看前3个

Step 4 (预测 "student"):
    [<bos>, I, am, a] → "student"
    注意力: [0.1, 0.2, 0.3, 0.4, 0.0]  ← 看前4个
```

---

## 一句话总结

> **Masked Multi-Head Attention = 只能看左边，不能偷看右边，保证自回归生成，训练和推理一致。**

---

## 相关笔记

- [[多头注意力深入理解]] —— 多头注意力基础
- [[Transformer架构从零理解]] —— 完整架构解析
- [[transformer_training_marimo]] —— 训练代码实现
- [[Causal Mask]] —— 因果掩码详解
