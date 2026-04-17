---
tags: [transformer, RoPE, positional-encoding, attention, LLM]
date: 2026-04-14
source: https://youtu.be/GQPOtyITy54
---

# RoPE 旋转位置编码详解

> 来源：YouTube 视频 "RoPE(Rotary positional embeddings)旋转位置编码"  
> 原链接：https://youtu.be/GQPOtyITy54  
> 整理时间：2026-04-14

---

## 一、为什么需要位置编码

### Transformer 的位置无关性问题

Transformer 的核心计算是 Self-Attention，但 Attention 本身是**位置无关**的：

```
输入 A: [我, 爱, 你]
输入 B: [你, 爱, 我]

对 Attention 来说，这两个输入完全一样！
因为 Attention 只关心"谁和谁有关系"，不关心"谁在谁前面"
```

**解决方案**：给每个位置一个独特的"指纹"——位置编码。

---

## 二、Sinusoidal 位置编码的问题

### 2.1 原始做法

Transformer 原版使用正弦/余弦函数生成位置编码：

$$
PE_{(pos, 2i)} = \sin\left(\frac{pos}{10000^{2i/d}}\right)
$$

然后将位置编码**加到** token 嵌入上：

```
X_pos = TokenEmbedding + PositionalEmbedding
```

### 2.2 问题所在

**向量运动"混乱"**：

以 2D 向量为例，假设 token 嵌入是 `[1, 1]`：

| 位置 | 加上位置编码后的向量 |
|------|---------------------|
| 0 | [1.0, 2.0] |
| 1 | [1.88, 1.61] |
| 2 | [1.08, 0.42] |
| 3 | [0.15, 1.29] |

**观察**：向量的**模长**和**角度**都在剧烈变化，没有明显规律。

### 2.3 导致的后果

1. **模型被迫"死记硬背"**
   - 由于位置编码模式难以学习，模型只能记住"位置 5 对应什么数值"
   - 类似考前临时抱佛脚，背答案而不是理解概念

2. **无法泛化到训练长度之外**
   - 如果训练时最大长度是 2048，推理时输入 2049
   - 模型完全没见过这个位置，输出会变得混乱
   - 研究证实：使用 Sinusoidal 的模型在超出训练长度时困惑度（perplexity）爆炸

---

## 三、RoPE 的核心思想

### 3.1 关键洞察

**不添加，而是旋转**。

与其把位置编码加到 token 上，不如**旋转** Query 和 Key 向量。

### 3.2 极坐标视角

将 Q/K 向量看作极坐标：

```
向量 = (r, θ)
- r (径向): 由 token 内容决定 → 捕捉语义相似性
- θ (角度): 由位置决定 → 捕捉位置关系
```

**关键分离**：
- **径向分量** → Token 相似性（语义）
- **角度分量** → 位置相似性（距离）

### 3.3 旋转公式

对于位置 m，将向量旋转角度 `m × θ`：

$$
R(m\theta) = \begin{bmatrix} \cos(m\theta) & -\sin(m\theta) \\ \sin(m\theta) & \cos(m\theta) \end{bmatrix}
$$

旋转后的向量：

$$
q_m = R(m\theta) \cdot q
$$

**效果**：每次位置 +1，向量就旋转固定角度 θ，非常规律！

---

## 四、高维扩展（D > 2）

### 4.1 分块旋转

实际 Transformer 中，Q/K 维度通常是 64、96、128 等。

**解决方案**：将向量分成 D/2 个二维块，每块独立旋转。

```
4D 向量 [a, b, c, d] 分成：
- 块 1: [a, b]，旋转角度 θ₁
- 块 2: [c, d]，旋转角度 θ₂
```

### 4.2 块对角旋转矩阵

$$
R = \begin{bmatrix}
R(\theta_1) & 0 \\
0 & R(\theta_2)
\end{bmatrix}
$$

其中每个 θᵢ 取决于维度索引：

$$
\theta_i = \text{base}^{-2i/d}
$$

### 4.3 多频率旋转的直观效果

```
位置 0: [■, ▲, ●, ★]
位置 1: [◤, △, ◐, ☆]  (块1旋转快，块2旋转慢...)
位置 2: [◣, ▷, ●, ★]
...
```

不同块以不同速度旋转，组合起来形成独特的"位置指纹"。

---

## 五、RoPE 的数学优雅性

### 5.1 相对位置编码

RoPE 的一个惊人性质：

$$
q_m^T k_n = q^T R((m-n)\theta) k
$$

**含义**：Q 和 K 的点积**只依赖于它们的相对距离 (m-n)**！

这就是"相对位置编码"的本质：
- 不是 "token A 在位置 5"
- 而是 "token A 和 token B 相距 3 个位置"

### 5.2 与 Sinusoidal 的公式对比

| 步骤 | Sinusoidal | RoPE |
|------|-----------|------|
| 1 | 计算位置编码 PE | 准备旋转矩阵 R(θ) |
| 2 | X = Token + PE | 不修改输入 |
| 3 | Q = X · Wq, K = X · Wk | Q = X · Wq, K = X · Wk |
| 4 | Attention = Q^T · K | **Q' = R(mθ) · Q, K' = R(nθ) · K** |
| 5 | - | Attention = Q'^T · K' |

### 5.3 最终公式

$$
\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{(R(m\theta)Q)^T (R(n\theta)K)}{\sqrt{d_k}}\right)V
$$

等价于：

$$
= \text{softmax}\left(\frac{Q^T R((m-n)\theta) K}{\sqrt{d_k}}\right)V
$$

---

## 六、RoPE 的优势总结

### 6.1 规律的位置变化

```
Sinusoidal: 位置 0 → 1 → 2 → 3  (向量乱跳)
RoPE:       位置 0 → 1 → 2 → 3  (向量平滑旋转)
```

### 6.2 更好的外推能力

| 特性 | Sinusoidal | RoPE |
|------|-----------|------|
| 训练长度 | 2048 | 2048 |
| 推理长度 | 2048 (超出则混乱) | 32768+ (仍可工作) |
| 原因 | 死记硬背位置数值 | 学习旋转规律，可泛化 |

### 6.3 性能优势

- 在标准基准测试中，RoPE 的困惑度（perplexity）普遍低于 Sinusoidal
- 长上下文任务上优势更明显

---

## 七、长上下文扩展技术

### 7.1 问题

RoPE 虽然外推能力比 Sinusoidal 好，但超出训练长度太多仍然效果下降。

### 7.2 主流扩展方案

| 方案 | 核心思想 | 效果 |
|------|---------|------|
| **线性插值 (PI)** | 把位置直接除以缩放因子，压进训练范围 | 简单但外推倍数大了效果差 |
| **NTK-aware** | 只缩放 RoPE 的低频分量，高频不动 | 比线性插值好 |
| **YaRN** | NTK 基础上加注意力缩放 + 平滑过渡 | 效果最好的免训练方案之一 |
| **LongRoPE** | 搜索最优的频率缩放因子 | 效果好但需搜索 |

### 7.3 YaRN 详解

**Y**et **A**nother **R**oPE extensio**N**

核心思想：
1. **分段缩放**：高频少压缩，低频多压缩
2. **平滑过渡**：用 ramp 函数避免硬边界
3. **注意力温度缩放**：调整 attention 的 softmax 温度

公式：

$$
f'_i = f_i \cdot \left( (1-\gamma_i) + \frac{\gamma_i}{s} \right)
$$

其中 γ 是线性 ramp，s 是缩放因子。

---

## 八、RoPE vs 其他位置编码

| 方案 | 类型 | 外推能力 | 复杂度 | 主流使用 |
|------|------|---------|--------|---------|
| **Sinusoidal** | 绝对 | ❌ 差 | 低 | 原版 Transformer |
| **Learnable** | 绝对 | ❌ 差 | 低 | BERT, GPT-2 |
| **RoPE** | 相对 | ✅ 好 | 中 | **LLaMA, Qwen, 现代 LLM** |
| **ALiBi** | 相对 | ✅ 极好 | 低 | MPT, BLOOM |
| **YaRN** | 相对 | ✅✅ 极好 | 中 | 长上下文模型 |

### ALiBi 简介

**Attention with Linear Biases**

不在 Q/K 上加位置编码，而是在 Attention Score 上直接加位置偏置：

```
score = Q @ K.T / sqrt(d) + bias
bias = -|i - j| * slope  # 距离越远，偏置越负
```

**优点**：外推能力极强，实现简单  
**缺点**：长距离衰减太快，可能丢失远距离依赖

---

## 九、关键公式速查

### 二维旋转矩阵

$$
R(\theta) = \begin{bmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{bmatrix}
$$

### RoPE 旋转

$$
q_m = R(m\theta) \cdot q
$$

### 频率计算

$$
\theta_i = \text{base}^{-2i/d}
$$

### 相对位置性质

$$
q_m^T k_n = q^T R((m-n)\theta) k
$$

---

## 十、总结

### 一句话概括

> RoPE 通过**旋转** Q/K 向量来编码位置，而非**添加**位置向量，使位置变化更规律，外推能力更强。

### 核心优势

1. **规律的位置变化** → 模型容易学习
2. **相对位置编码** → 天然表达 token 间距离
3. **外推能力强** → 支持比训练时更长的上下文
4. **性能更好** → 困惑度普遍低于 Sinusoidal

### 现代 LLM 的标准选择

RoPE 已成为大多数现代大语言模型的默认位置编码方案：
- LLaMA 系列
- Qwen 系列
- ChatGLM
- Mistral
- 等

---

## 参考链接

- 原视频：https://youtu.be/GQPOtyITy54
- RoPE 论文：RoFormer: Enhanced Transformer with Rotary Position Embedding
