# RoFormer: Rotary Position Embedding (RoPE) 研究笔记

> 论文：RoFormer: Enhanced Transformer with Rotary Position Embedding  
> 作者：Jianlin Su 等 (追一科技)  
> arXiv：2104.09864  
> 发布时间：2021年4月，修订版2023年11月  
> 标签：#位置编码 #Transformer #LLM #RoPE

---

## 核心创新

> [!tip] 一句话总结
> **RoPE 用旋转矩阵编码位置信息，自然融入相对位置依赖，解决了传统位置编码的问题。**

| 传统方法 | RoPE 方法 |
|---------|----------|
| **加法式**（位置向量 + 词向量） | **乘法式**（旋转矩阵 × 词向量） |
| 绝对位置编码 | 自然融合相对位置信息 |
| 与线性注意力不兼容 | 与线性注意力兼容 |
| 序列长度受限 | 序列长度灵活（可外推） |

---

## 问题背景

### Transformer 的位置感知问题

> [!warning] 核心问题
> Transformer 的 self-attention 本质上是 **位置无关的（position-agnostic）**。

```
Self-Attention 计算：
- 输入：词向量序列 {x_i}
- 输出：加权求和
- 问题：无法区分 "我喜欢你" 和 "你喜欢我"
```

### 现有位置编码方法

| 方法 | 公式 | 问题 |
|------|------|------|
| **绝对位置编码（可训练）** | `x_i + p_i` | 序列长度受限，无法外推 |
| **绝对位置编码（Sinusoidal）** | `sin/cos 函数` | 相对位置信息隐式且弱 |
| **相对位置编码** | 改造 attention score | 与线性注意力不兼容 |

---

## RoPE 方法详解

### 核心思想

> [!quote] 设计目标
> 让 query 和 key 的内积 **只依赖于词向量和相对位置**：
> ```
> ⟨f_q(x_m, m), f_k(x_n, n)⟩ = g(x_m, x_n, m - n)
> ```

### 2D 情况下的推导

**关键洞察**：用复数形式表示 2D 向量

```math
f_q(x_m, m) = (W_q x_m) e^{imθ}
f_k(x_n, n) = (W_k x_n) e^{inθ}

内积结果：
⟨f_q, f_k⟩ = Re[(W_q x_m)(W_k x_n)^* e^{i(m-n)θ}]
```

**几何解释**：
- 位置 m 的向量旋转角度 `mθ`
- 位置 n 的向量旋转角度 `nθ`
- 相对位置 `(m-n)` 决定最终角度差

### 通用形式（d 维）

将 d 维空间分为 `d/2` 个 2D 子空间：

```math
f_{q,k}(x_m, m) = R_{d,Θ,m} W_{q,k} x_m
```

**旋转矩阵** `R_{d,Θ,m}`：

```
[cos mθ₁  -sin mθ₁  0        0       ...]
[sin mθ₁   cos mθ₁  0        0       ...]
[0         0        cos mθ₂  -sin mθ₂ ...]
[0         0        sin mθ₂   cos mθ₂ ...]
...
```

**θ 的设置**（继承 Sinusoidal 思路）：

```math
θ_i = 10000^{-2(i-1)/d}
```

---

## RoPE 的三大优势

### 1. 序列长度灵活性

> [!success] 核心优势
> RoPE 不依赖预定义的位置向量表，可以自然处理任意长度序列。

- 传统方法：最大长度 L → 需要训练 `L` 个位置向量
- RoPE：只需定义 `θ`，位置可以是任意整数

**应用**：LLaMA、GLM 等现代大模型都采用 RoPE

---

### 2. 长程衰减（Long-term Decay）

> [!note] 数学证明
> 随着相对距离增加，token 间的关联度自然衰减。

```
相对距离 ↑ → 内积值 ↓
```

这符合自然语言的直觉：距离越远的词，语义关联越弱。

**数学推导**（Abel 变换）：

```math
内积 ≤ max|h_{i+1} - h_i| × Σ|S_{i+1}|
```

其中 `S_i` 的值随相对距离增加而衰减。

---

### 3. 与线性注意力兼容

**线性注意力**（避免 O(N²) 复杂度）：

```math
Attention(Q,K,V) = Σ φ(q_m)^T φ(k_n) v_n
```

**RoPE + 线性注意力**：

```math
R_{d,Θ,m} φ(q_m)^T R_{d,Θ,n} φ(k_n) v_n
```

> [!important] 意义
> RoPE 是 **唯一能与线性注意力兼容的相对位置编码方法**。

---

## 与其他方法的对比

| 方法 | 绝对/相对 | 加法/乘法 | 长度外推 | 线性注意力 |
|------|----------|----------|---------|-----------|
| Sinusoidal | 绝对 | 加法 | ✓ | ✗ |
| Learnable | 绝对 | 加法 | ✗ | ✗ |
| Shaw et al. | 相对 | 加法 | ✗ | ✗ |
| T5 Bias | 相对 | 加法 | ✗ | ✗ |
| **RoPE** | **相对** | **乘法** | **✓** | **✓** |

---

## 实验结果

### 机器翻译（WMT 2014 EN-DE）

| 模型 | BLEU |
|------|------|
| Transformer-base | 27.3 |
| **RoFormer** | **27.5** |

### 预训练收敛速度

> [!success] 关键发现
> RoFormer 收敛速度明显快于 BERT（MLM loss 更快下降）

### GLUE 下游任务

| 任务 | BERT | RoFormer |
|------|------|----------|
| MRPC | 88.9 | **89.5** |
| STS-B | 85.8 | **87.0** |
| QQP | 71.2 | **86.4** |

### 长文本任务（CAIL2019-SCM）

| 模型 | 长度限制 | Accuracy |
|------|---------|----------|
| BERT-512 | 512 | 67.77% |
| RoFormer-512 | 512 | 68.29% |
| **RoFormer-1024** | **1024** | **69.79%** |

> [!success] 长文本优势明显
> 当序列长度从 512 扩展到 1024，RoFormer 提升 1.5%

---

## 代码实现要点

### 高效计算方式

利用旋转矩阵的稀疏性：

```python
# 分组旋转（d/2 组）
x_rotated = x * cos(mθ) + x_shifted * sin(mθ)

# 其中 x_shifted 是相邻维度交换：
# [x₁, x₂, x₃, x₄] → [-x₂, x₁, -x₄, x₃]
```

### PyTorch 实现（简化版）

```python
def apply_rotary_pos_emb(q, k, cos, sin):
    # q, k: [batch, seq_len, heads, d]
    # cos, sin: [seq_len, d/2]
    
    q_rot = (q * cos) + (rotate_half(q) * sin)
    k_rot = (k * cos) + (rotate_half(k) * sin)
    
    return q_rot, k_rot

def rotate_half(x):
    x1, x2 = x[..., ::2], x[..., 1::2]
    return torch.stack([-x2, x1], dim=-1).flatten(-2)
```

---

## 实际应用

### 采用 RoPE 的主流模型

| 模型 | 发布时间 | 说明 |
|------|---------|------|
| **LLaMA** | 2023 | Meta，最著名的开源大模型 |
| **GLM** | 2022 | 清华/智谱 |
| **PaLM** | 2022 | Google |
| **Falcon** | 2023 | TII |
| **Qwen** | 2023 | 阿里 |

> [!important] 行业标准
> RoPE 已成为大模型位置编码的主流选择。

---

## 局限性

作者承认的局限：

1. **缺乏理论解释**：为什么 RoPE 收敛更快？
2. **长文本优势的根因未明**：长程衰减特性与其他方法类似，但实际表现更好

---

## 我的理解

### 为什么 RoPE 更好？

> [!note] 个人分析
> 1. **乘法式更自然**：旋转是几何变换，比加法更符合"位置变化"的直觉
> 2. **相对位置显式化**：不需要额外的偏置项或可训练参数
> 3. **计算高效**：旋转矩阵稀疏，可高效实现
> 4. **外推能力强**：不依赖固定位置表，自然支持更长序列

### 与 DPO/PPO 的关系？

无关。RoPE 是架构层面的创新（位置编码），DPO/PPO 是训练方法层面的创新（对齐）。

---

## 相关概念

- [[Transformer架构从零理解]]
- [[注意力机制详解]]
- [[位置编码从零理解]] ← 直接相关
- [[长上下文技术]] ← RoPE 是关键技术
- [[15-位置编码]]（minimind 笔记）

---

## 参考文献

- 原论文：[arXiv:2104.09864](https://arxiv.org/abs/2104.09864)
- HuggingFace 实现：[RoFormer](https://huggingface.co/docs/transformers/model_doc/roformer)
- 代码仓库：[github.com/ZhuiyiTechnology/roformer](https://github.com/ZhuiyiTechnology/roformer)

---

*创建时间：2026-04-15*  
*论文下载：`Roformer-RoPE.pdf`（`Resources/papers/`）*