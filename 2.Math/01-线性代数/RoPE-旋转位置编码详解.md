# RoPE：旋转位置编码详解

> 视频来源：YouTube SMBkImDWOyQ
> 标题：How Rotary Position Embedding Supercharges Modern LLMs [RoPE]
> 观看日期：2026-04-18
> 视频时长：约 15 分钟

---

## 一、为什么需要位置编码？

### 1.1 核心问题：Attention 的置换等变性

打乱句子中的单词顺序会完全改变其含义。例如：
- "I walk my dog every day" vs "Every day I walk my dog"
- 即使语义相近，单词 "dog" 在不同位置含义可能不同

**问题**：Transformer 的 attention mechanism 具有 **置换等变性（Permutation Equivariance）**

> **定义**：打乱输入 token 的顺序，输出的 contextual features 保持不变。

### 1.2 具体例子

假设句子："I walk my dog every day"，对 token "dog" 计算 attention：

1. 计算 Query 向量 $Q_{dog}$
2. 与所有 Key 向量 $K_1, K_2, ..., K_5$ 做点积
3. Softmax 得到 attention weights
4. 加权求和 Value 向量

**关键发现**：如果打乱 tokens（如变成 "Every day I walk my dog"），"dog" 的 contextual features **完全相同**。

这意味着 attention **无法区分单词在不同位置的含义**。

---

## 二、绝对位置编码的问题

### 2.1 原始 Transformer 的方案

**Sinusoidal Positional Encoding**（Vaswani et al., 2017）：

每个位置分配一个唯一的向量，由不同频率的周期性组件组成：
$$PE_{(pos, 2i)} = \sin(pos / 10000^{2i/d})$$
$$PE_{(pos, 2i+1)} = \cos(pos / 10000^{2i/d})$$

**注入方式**：将位置向量加到 word embedding 上：
$$x_{pos} = word\_embedding + PE_{pos}$$

### 2.2 问题

改写句子时（如把 "every day" 移到前面），tokens 获得全新的位置编码，但句子语义并未改变。

**理想方案**：编码相对位置，而非绝对位置。

---

## 三、RoPE 的核心思想

### 3.1 基本原理：旋转 Query/Key 向量

RoPE（Rotary Position Embedding）通过**旋转向量**来编码位置：

| Token | 位置 | 旋转角度 |
|-------|------|---------|
| "dog" | 第1位 | θ |
| "dog" | 第2位 | 2θ |
| "dog" | 第4位 | 4θ |

**关键**：旋转量只依赖于 token 在句子中的位置。

### 3.2 为什么这有用？

计算 attention score 时（Query 和 Key 的点积）：

假设：
- Query 向量来自位置 $m$，旋转 $m\theta$
- Key 向量来自位置 $n$，旋转 $n\theta$

**点积结果** = $R(m\theta) \cdot R(n\theta) = R((m-n)\theta)$

> **核心性质**：Attention score 只依赖于**相对位置** $(m-n)$，而非绝对位置。

---

## 四、数学推导

### 4.1 2D 向量的旋转

旋转矩阵：
$$R(\theta) = \begin{bmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{bmatrix}$$

### 4.2 Attention Score 的推导

Query（位置 $m$）：
$$q_m = R(m\theta) \cdot x_m$$

Key（位置 $n$）：
$$k_n = R(n\theta) \cdot x_n$$

Attention score（点积）：
$$q_m^T k_n = (R(m\theta) x_m)^T (R(n\theta) x_n)$$
$$= x_m^T R(m\theta)^T R(n\theta) x_n$$

**关键性质**：旋转矩阵的逆等于其转置：
$$R(\theta)^T = R(-\theta)$$

因此：
$$R(m\theta)^T R(n\theta) = R(-m\theta) R(n\theta) = R((n-m)\theta)$$

> **结论**：Attention score 只依赖相对位置 $n-m$，不受绝对位置影响。

---

## 五、高维向量处理

### 5.1 分块策略

对于 $d$ 维向量（如 $d=8$），RoPE 将其分成 $d/2$ 组：

```
[q1, q2, q3, q4, q5, q6, q7, q8]
     ↓ 分组 ↓
第1组: [q1, q2] → 旋转 θ1
第2组: [q3, q4] → 旋转 θ2
第3组: [q5, q6] → 旋转 θ3
第4组: [q7, q8] → 旋转 θ4
```

### 5.2 不同频率组件

**旋转速度**在不同组中变化：
- **第1组**（高频）：θ 变化快，敏感位置变化
- **最后一组**（低频）：θ 变化慢，对位置偏移不敏感

数学上，RoPE 可写成**分块对角矩阵**乘法：
$$\begin{bmatrix} R(\theta_1) & 0 & 0 & 0 \\ 0 & R(\theta_2) & 0 & 0 \\ 0 & 0 & R(\theta_3) & 0 \\ 0 & 0 & 0 & R(\theta_4) \end{bmatrix}$$

### 5.3 实现优化

**不要用矩阵乘法实现**（内存和计算开销大）！

**实际实现**：用 element-wise 操作：
```python
# 复数形式（更高效）
q_rotated = q * cos(θ) + rotate_half(q) * sin(θ)
```

---

## 六、高频 vs 低频组件的作用

### 6.1 高频组件

- **特点**：对位置变化高度敏感
- **作用**：构建 **position-specific attention heads**
- **示例**：
  - Diagonal attention（关注相邻 token）
  - Previous token attention（关注前一个 token）

### 6.2 低频组件

- **特点**：对相对位置不敏感
- **作用**：在长距离上保持 **semantic attention**
- **意义**：即使 tokens 相隔很远，仍能维持语义关联

---

## 七、为什么增大 base frequency？

### 7.1 实例：Llama 2 → Llama 3

| Model | Base frequency (θ的基数) |
|-------|------------------------|
| Llama 1 | 10,000 |
| Llama 2 | 10,000 |
| Llama 3 | **500,000** |

**原因**：
增大 base frequency 进一步**减慢低频组件的旋转速度**，使 Transformer 能关注更大相对距离的 tokens，捕捉**长程依赖**。

---

## 八、长上下文扩展方法

### 8.1 问题

模型在训练上下文长度内表现良好（如 Llama 2 的 4K），但超出后性能急剧下降。

**原因**：推理时遇到未见过的旋转角度模式。

### 8.2 Position Interpolation

**核心思想**：将推理时的位置缩放到训练窗口内。

例如：4K → 20K，缩放因子 = 1/5
$$pos' = pos / 5$$

**效果**：相当于将所有频率减慢 5 倍。

**问题**：高频组件也被减慢，但这些对构建 position-specific attention 很关键。

### 8.3 NTK-aware Scaling

**核心思想**：频率自适应缩放。

| 频率类型 | 缩放方式 |
|---------|---------|
| 高频 | 缩放因子 ≈ 1（保持不变） |
| 低频 | 缩放因子 = 1/5（类似 position interpolation） |

> **为什么有效**：高频组件保持位置敏感性，低频组件扩展长距离语义能力。

---

## 九、实验结果

### 9.1 Perplexity 测试

基准：Llama 2（4K 训练上下文）

| 方法 | 4K | 32K | 64K |
|------|----|----|-----|
| Baseline | ✓ | ✗ | ✗ |
| PI (Position Interpolation) | ✓ | ✓（需微调） | ✗ |
| YaRN | ✓ | ✓（需微调） | ✗ |
| NTK-32K | ✓ | ✓ | ✓（泛化） |
| NTK-64K | ✓ | ✓ | ✓（需更多数据） |

**亮点**：NTK-based 方法无需在 64K 数据上微调就能泛化。

### 9.2 Needle in Haystack 测试

**测试设计**：
- 在长文档中嵌入一个 "needle"（特定信息）
- 评估模型能否检索该信息
- X轴：上下文长度
- Y轴：needle 嵌入位置

**结果**：
- Baseline：超过 4K 完全失败
- Approximate attention（如 LM-Infinite）：只能在文档底部检索
- NTK-32K：在 64K 范围内成功泛化

---

## 十、核心要点总结

| 主题 | 关键结论 |
|------|---------|
| **位置编码必要性** | Attention 天然置换等变，需注入位置信息 |
| **绝对位置编码缺陷** | 改写句子时语义不变但位置编码变化 |
| **RoPE 核心** | 通过旋转向量编码相对位置 |
| **数学本质** | 点积只依赖相对位置 $(m-n)$ |
| **高频组件** | 构建 position-specific attention heads |
| **低频组件** | 保持长距离语义 attention |
| **Base frequency增大** | 减慢低频旋转，扩展长程依赖能力 |
| **长上下文扩展** | NTK-aware scaling 最有效 |

---

## 十一、代码示例

### 11.1 RoPE 的简化实现

```python
import torch

def rotate_half(x):
    """将向量的一半旋转"""
    x1 = x[..., :x.shape[-1]//2]
    x2 = x[..., x.shape[-1]//2:]
    return torch.cat([-x2, x1], dim=-1)

def apply_rotary_pos_emb(q, k, cos, sin):
    """应用旋转位置编码"""
    q_embed = (q * cos) + (rotate_half(q) * sin)
    k_embed = (k * cos) + (rotate_half(k) * sin)
    return q_embed, k_embed

# 示例：计算不同频率的 cos/sin
def precompute_freqs_cis(dim, seq_len, base=10000):
    """预计算旋转频率"""
    freqs = 1.0 / (base ** (torch.arange(0, dim, 2).float() / dim))
    t = torch.arange(seq_len)
    freqs = torch.outer(t, freqs)
    cos = torch.cos(freqs)
    sin = torch.sin(freqs)
    return cos, sin
```

### 11.2 可视化旋转

```python
import matplotlib.pyplot as plt
import numpy as np

theta = np.linspace(0, 2*np.pi, 100)
x = np.cos(theta)
y = np.sin(theta)

plt.figure(figsize=(6, 6))
plt.plot(x, y, 'b-', linewidth=2)
plt.scatter([1, 0], [0, 1], c='red', s=100, label='Positions 0, 1')
plt.title('2D Rotation Visualization')
plt.xlabel('x')
plt.ylabel('y')
plt.axis('equal')
plt.legend()
plt.grid(True)
plt.show()
```

---

## 十二、与其他位置编码对比

| 方法 | 类型 | 优点 | 缺点 |
|------|------|------|------|
| **Sinusoidal** | 绝对 | 简单，无需学习 | 长序列泛化差 |
| **Learned Absolute** | 绝对 | 可学习 | 最大长度受限 |
| **Relative PE** | 相对 | 直接编码相对位置 | 计算复杂 |
| **RoPE** | 相对（隐式） | 数学优雅，长序列友好 | 需要理解旋转 |
| **ALiBi** | 相对 | 简单线性衰减 | 表达能力有限 |

---

## 十三、采用 RoPE 的模型

| 模型 | 公司 | 上下文长度 |
|------|------|-----------|
| Llama 1/2/3 | Meta | 2K → 4K → 8K+ |
| Gemma | Google | 8K |
| Mistral | Mistral AI | 32K |
| Qwen | 阿里 | 32K+ |
| DeepSeek | DeepSeek | 64K+ |

---

## 十四、延伸阅读

### 关键论文

1. **RoPE 原论文**：Su et al. (2021) "RoFormer: Enhanced Transformer with Rotary Position Embedding"
2. **长上下文扩展**：Chen et al. (2023) "Extending Context Window of LLMs via Positional Interpolation"
3. **NTK-aware scaling**：blog post by /u/kaiokendev
4. **YaRN**：Peng et al. (2023) "YaRN: Efficient Context Window Extension"

### 相关笔记

- [[RoPE 旋转位置编码研究笔记]]
- [[YaRN 上下文扩展研究笔记]]
- [[LEX Transformer 长度外推研究笔记]]

---

## 十五、FAQ

### Q1: RoPE 和绝对位置编码的区别？

**绝对**：每个位置固定编码，改写句子编码变化。
**RoPE**：编码相对位置，改写句子不影响 attention score。

### Q2: 为什么高频组件重要？

高频组件敏感位置变化，用于构建 position-specific attention（如关注相邻 token）。如果减慢高频，会破坏这种能力。

### Q3: 如何选择 base frequency？

短上下文：10,000（标准）
长上下文：增大到 50,000-500,000，减慢低频旋转

### Q4: RoPE 能完全替代绝对位置编码吗？

是的。RoPE 已成为 LLM 的主流选择（Llama、Gemma 等）。

---

#位置编码 #RoPE #Transformer #LLM #线性代数 #旋转矩阵