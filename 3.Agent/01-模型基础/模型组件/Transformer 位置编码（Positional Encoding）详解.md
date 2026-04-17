# Transformer 位置编码（Positional Encoding）详解

## 一句话总结

**位置编码 = 给每个位置一个唯一的 64 维（或 d_model 维）向量，加到词向量上，让模型知道"词在句子里的第几个位置"**

- 所有句子**共用同一套**位置编码表
- 只和"是第几个位置"有关，和"哪句话、什么词"无关
- 预计算好（如 5000 个位置），用时取前 L 行

---

## 核心概念：为什么要分开词向量和位置向量？

Transformer 需要知道两件事：

| 信息类型 | 问题 | 来源 | 是否依赖具体词 |
|---------|------|------|---------------|
| **词嵌入（Embedding）** | 这个词是什么意思？ | 词表查找 | ✅ 依赖（"猫"≠"狗"） |
| **位置编码（PE）** | 这个词在句子里第几个？ | 位置下标 | ❌ 不依赖（只看位置） |

### 两层叠加

```
最终输入 = 词向量 + 位置向量

┌─────────────────────┬───────────────────────────────────────────────┐
│ 组件                │ 作用                                          │
├─────────────────────┼───────────────────────────────────────────────┤
│ 词嵌入（embedding） │ 这个词语义上是什么（不同词不同向量）          │
│ 位置编码（PE）      │ 这个词在句子里是第几位（同一位置用同一条 PE） │
└─────────────────────┴───────────────────────────────────────────────┘
```

### 代码示例

```python
# 假设句子："The cat sat"
# 词嵌入（语义）
word_emb[0] = embedding("The")  # → [0.1, -0.3, 0.5, ...] (d_model 维)
word_emb[1] = embedding("cat")  # → [0.2, 0.1, -0.4, ...]
word_emb[2] = embedding("sat")  # → [-0.1, 0.4, 0.2, ...]

# 位置编码（位置）
pos_enc[0] = PE(0)  # → [0.0, 1.0, 0.0, 1.0, ...] (第 0 个位置)
pos_enc[1] = PE(1)  # → [0.5, 0.5, 0.5, 0.5, ...] (第 1 个位置)
pos_enc[2] = PE(2)  # → [1.0, 0.0, 1.0, 0.0, ...] (第 2 个位置)

# 最终输入
x[0] = word_emb[0] + pos_enc[0]  # "The" 在第 0 位
x[1] = word_emb[1] + pos_enc[1]  # "cat" 在第 1 位
x[2] = word_emb[2] + pos_enc[2]  # "sat" 在第 2 位
```

---

## 🔑 d_model 维度是什么？

### 常见误解

❌ **错误理解**：
> "64 个维度各代表一种位置含义，然后扔掉别的"

✅ **正确理解**：
> "**每个位置**对应一个**64 维向量**，用 sin/cos 函数填出来"

### 详细解释

```python
d_model = 64  # 每个 token 最终都是一个 64 维向量

# 位置编码表的结构
PE 表形状：(max_len, d_model) = (5000, 64)

# 每个位置有一整行 64 维向量
PE[0]  = [sin/cos 值 1, sin/cos 值 2, ..., sin/cos 值 64]  # 第 0 个位置
PE[1]  = [sin/cos 值 1, sin/cos 值 2, ..., sin/cos 值 64]  # 第 1 个位置
PE[2]  = [sin/cos 值 1, sin/cos 值 2, ..., sin/cos 值 64]  # 第 2 个位置
...
PE[4999] = [...]  # 第 4999 个位置
```

### 数学公式

对于位置 $pos$ 和维度 $i$：

$$\text{PE}(pos, 2i) = \sin\left(\frac{pos}{10000^{2i/d_{\text{model}}}}\right)$$

$$\text{PE}(pos, 2i+1) = \cos\left(\frac{pos}{10000^{2i/d_{\text{model}}}}\right)$$

- 偶数维度用 sin，奇数维度用 cos
- 不同维度使用不同频率（波长）
- 低频维度变化慢，高频维度变化快

---

## 为什么输入全零，输出仍有区别？

### 实验代码

```python
_pe = PositionalEncoding(d_model=64, dropout=0.0)
_x = torch.zeros(1, 10, 64)  # 全零输入
_enc = _pe(_x)

print(f"输入全零 {tuple(_x.shape)} -> 输出 {tuple(_enc.shape)}")
print(f"位置 0 前 8 维：{[f'{v:.3f}' for v in _enc[0,0,:8]]}")
print(f"位置 1 前 8 维：{[f'{v:.3f}' for v in _enc[0,1,:8]]}")
print(f"位置 9 前 8 维：{[f'{v:.3f}' for v in _enc[0,9,:8]]}")
```

### 输出示例

```
输入全零 (1, 10, 64) -> 输出 (1, 10, 64)
位置 0 前 8 维：['0.000', '1.000', '0.000', '1.000', '0.000', '1.000', '0.000', '1.000']
位置 1 前 8 维：['0.841', '0.540', '0.046', '0.999', '0.002', '1.000', '0.000', '1.000']
位置 9 前 8 维：['0.412', '-0.911', '0.406', '0.914', '0.021', '0.999', '0.001', '1.000']
```

### 原因

```
即使词向量全为零：
  位置 0: [0, 0, 0, ...] + PE[0] = PE[0]  ← 位置 0 的唯一编码
  位置 1: [0, 0, 0, ...] + PE[1] = PE[1]  ← 位置 1 的唯一编码
  位置 9: [0, 0, 0, ...] + PE[9] = PE[9]  ← 位置 9 的唯一编码

结果：不同位置的输出向量不同！
```

**结论**：模型能区分顺序，即使语义向量完全相同。

---

## 🔑 max_len=5000 是什么意思？

### 位置编码表的结构

```python
class PositionalEncoding(nn.Module):
    def __init__(self, d_model, dropout=0.1, max_len=5000):
        super().__init__()
        
        # 预计算所有位置编码 (5000, d_model)
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len).unsqueeze(1)  # (5000, 1)
        
        # 计算 sin/cos 值
        div_term = torch.exp(torch.arange(0, d_model, 2) * -(math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        
        # 注册为 buffer (1, max_len, d_model)
        self.register_buffer('pe', pe.unsqueeze(0))
```

### 实际使用

```python
# 预计算：5000 个位置，每个位置 d_model 维
PE 表形状：(1, 5000, 64)
           ↑    ↑     ↑
         batch  位置   维度

# 实际使用时，只取前 L 行（L = 序列长度）
def forward(self, x):
    # x 形状：(batch, seq_len, d_model)
    return x + self.pe[:, :x.size(1), :]  # ← 只取前 seq_len 个位置
```

### 示意图

```
预计算的 PE 表 (5000 行)：
┌─────────────────────────┐
│ PE[0]  ←───────────────┐ │
│ PE[1]  ←───────┐       │ │
│ PE[2]  ←───┐   │       │ │
│ ...      │   │   实际使用 │ │
│ PE[L-1] ←┘   │   的部分  │ │
│ ...          │         │ │
│ PE[4999]     │         │ │
└──────────────┴─────────┘

实际句子长度为 L 时，只用前 L 行
```

### 常见问题

**Q: 每次都要用满 5000 个位置吗？**

A: **不用！** 取决于句子长度：
- 句子长度 = 10 → 用前 10 行
- 句子长度 = 100 → 用前 100 行
- 句子长度 = 500 → 用前 500 行

**Q: 为什么是 5000？不够怎么办？**

A: 
- 5000 是经验值，覆盖绝大多数场景
- 常见任务：一句话通常 < 512 token
- 如果输入超过 5000，需要调大 `max_len` 或截断

**Q: 预计算 5000 个位置会浪费内存吗？**

A: 
- 不会，5000 × 512 × 4 字节 ≈ 10MB
- 注册为 buffer，不占可学习参数
- 一次性计算，重复使用

---

## 🔑 所有句子共用同一套位置编码吗？

### 答案：是的！

```
位置编码只和「是第几个位置」有关，和以下内容无关：
- ❌ 哪句话
- ❌ 什么语言
- ❌ 什么词
- ✅ 只看位置下标（第 0 个、第 1 个、第 2 个...）
```

### 示例

```python
# 句子 1: "The cat sat" (长度 3)
# 句子 2: "I love AI" (长度 3)
# 句子 3: "今天天气很好" (长度 5)

# 所有句子的第 0 个位置都用 PE[0]
句子 1[0] += PE[0]  # "The" 在第 0 位
句子 2[0] += PE[0]  # "I" 在第 0 位
句子 3[0] += PE[0]  # "今" 在第 0 位

# 所有句子的第 1 个位置都用 PE[1]
句子 1[1] += PE[1]  # "cat" 在第 1 位
句子 2[1] += PE[1]  # "love" 在第 1 位
句子 3[1] += PE[1]  # "天" 在第 1 位

# 以此类推...
```

### 可视化

```
所有句子共用同一套 PE 表：

PE 表 (5000, d_model)
┌──────────────────────┐
│ PE[0] ───────────────┼──→ 所有句子的第 0 个词都用这个
│ PE[1] ───────────────┼──→ 所有句子的第 1 个词都用这个
│ PE[2] ───────────────┼──→ 所有句子的第 2 个词都用这个
│ ...                  │
│ PE[4999]             │
└──────────────────────┘

句子 1: [词 0+PE[0], 词 1+PE[1], 词 2+PE[2], ...]
句子 2: [词 0+PE[0], 词 1+PE[1], 词 2+PE[2], ...]
句子 3: [词 0+PE[0], 词 1+PE[1], 词 2+PE[2], ...]
```

### 为什么可以共用？

因为位置编码的本质是**回答"这是第几个位置"**：
- 第 0 个位置永远是第 0 个位置（无论什么句子）
- 第 1 个位置永远是第 1 个位置
- ...

就像"第一排第一座"的座位号，不管今天放映什么电影，座位号都是一样的。

---

## 完整代码实现

### 标准实现（PyTorch 风格）

```python
import torch
import torch.nn as nn
import math

class PositionalEncoding(nn.Module):
    def __init__(self, d_model, dropout=0.1, max_len=5000):
        super().__init__()
        self.dropout = nn.Dropout(p=dropout)
        
        # 预计算所有位置编码
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len).unsqueeze(1)  # (max_len, 1)
        
        # 计算频率项
        div_term = torch.exp(
            torch.arange(0, d_model, 2) * -(math.log(10000.0) / d_model)
        )
        
        # 填充 sin/cos
        pe[:, 0::2] = torch.sin(position * div_term)  # 偶数维度
        pe[:, 1::2] = torch.cos(position * div_term)  # 奇数维度
        
        # 调整形状为 (1, max_len, d_model) 并注册为 buffer
        self.register_buffer('pe', pe.unsqueeze(0))
    
    def forward(self, x):
        """
        Args:
            x: Tensor, shape (batch, seq_len, d_model)
        """
        # 只取前 seq_len 个位置
        x = x + self.pe[:, :x.size(1), :]
        return self.dropout(x)
```

### 使用示例

```python
# 初始化
d_model = 64
pe_layer = PositionalEncoding(d_model=d_model, dropout=0.0)

# 模拟输入（batch=1, seq_len=10, d_model=64）
x = torch.zeros(1, 10, 64)

# 添加位置编码
x_with_pe = pe_layer(x)

print(f"输入形状：{tuple(x.shape)}")      # (1, 10, 64)
print(f"输出形状：{tuple(x_with_pe.shape)}")  # (1, 10, 64)

# 验证不同位置确实不同
print(f"位置 0 前 8 维：{x_with_pe[0, 0, :8].tolist()}")
print(f"位置 1 前 8 维：{x_with_pe[0, 1, :8].tolist()}")
print(f"位置 9 前 8 维：{x_with_pe[0, 9, :8].tolist()}")
```

### 在 Transformer 中的使用

```python
class TransformerModel(nn.Module):
    def __init__(self, vocab_size, d_model=512, n_heads=8, n_layers=6):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, d_model)
        self.pos_encoder = PositionalEncoding(d_model)
        self.encoder_layers = nn.ModuleList([
            TransformerBlock(d_model, n_heads) for _ in range(n_layers)
        ])
    
    def forward(self, src):
        # src: (batch, seq_len) - token IDs
        
        # 1. 词嵌入
        x = self.embedding(src)  # (batch, seq_len, d_model)
        
        # 2. 添加位置编码
        x = self.pos_encoder(x)
        
        # 3. 编码器层
        for layer in self.encoder_layers:
            x = layer(x)
        
        return x
```

---

## 位置编码的变体

### 1. 正弦位置编码（原始 Transformer）
```python
# 如上所示，用 sin/cos 函数
# 优点：可以外推到更长序列（未见过的位置）
# 缺点：固定，不可学习
```

### 2. 可学习位置编码（BERT 等）
```python
class LearnablePositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=512):
        super().__init__()
        # 直接作为可学习参数
        self.pe = nn.Parameter(torch.randn(1, max_len, d_model))
    
    def forward(self, x):
        return x + self.pe[:, :x.size(1), :]
```
- 优点：模型自己学最优位置表示
- 缺点：无法处理超过 max_len 的序列

### 3. RoPE（旋转位置编码，LLaMA 等）
```python
# 将位置信息编码到 Q/K 的旋转角度中
# 优点：更好的相对位置建模，支持长序列外推
# 用于：LLaMA、PaLM、Gemini 等
```

### 4. ALiBi（Attention with Linear Biases）
```python
# 在 Attention 分数中直接减去与距离成正比的偏置
# 优点：无需位置编码，天然支持任意长度
# 用于：MPT、一些开源大模型
```

---

## 常见误区

### ❌ "64 维代表 64 种不同的位置"
**错！** 64 维是**每个位置**的向量长度，不是位置数量。
- 位置数量 = max_len（如 5000）
- 每个位置用 d_model 维（如 64）表示

### ❌ "每个句子需要单独计算位置编码"
**错！** 所有句子共用同一套预计算的 PE 表。
- 预计算一次，重复使用
- 第 k 个位置永远用 PE[k]

### ❌ "位置编码会改变词向量的语义"
**不完全对！** 位置编码是**加法**，不是替换。
- 词向量保留语义信息
- 位置向量添加顺序信息
- 两者融合，互不覆盖

### ❌ "max_len=5000 意味着每条数据都要有 5000 个 token"
**错！** max_len 是**上限**，实际用多少取多少。
- 句子长度 = 10 → 用前 10 行
- 句子长度 = 100 → 用前 100 行

---

## 总结

| 问题 | 答案 |
|------|------|
| d_model 是什么？ | 每个位置向量的维度（如 64、512） |
| 位置编码表有多大？ | (max_len, d_model)，如 (5000, 64) |
| 所有句子共用吗？ | ✅ 是的，共用同一套 |
| 每次都用满 5000 吗？ | ❌ 不用，只取前 L 行（L=句子长度） |
| 位置编码可学习吗？ | 原始 Transformer 不可学习，BERT 等可学习 |
| 为什么输入全零输出不同？ | 因为位置编码本身就有值，不同位置不同 |
| 位置编码加在哪里？ | 词嵌入之后，输入编码器之前 |

### 核心要点

1. **位置编码 = 位置下标 → d_model 维向量**
2. **所有句子共用同一套 PE 表**
3. **第 k 个位置永远用 PE[k]**
4. **预计算 max_len 个位置，用时取前 L 行**
5. **最终输入 = 词向量 + 位置向量**

**记住**：位置编码就像电影院的座位号——不管今天放映什么电影（什么句子），"第一排第一座"永远是同一个位置。

---

**标签**: #Transformer #位置编码 #深度学习 #NLP #Attention 机制

**创建日期**: 2026-03-23
**相关**: [[Feed-Forward Network (FFN) - 前馈神经网络]] [[Transformer架构从零理解]] [[LayerNorm vs Softmax - 本质区别]]
