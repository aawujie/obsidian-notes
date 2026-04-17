# YaRN: 高效的大模型上下文窗口扩展

> 论文：YaRN: Efficient Context Window Extension of Large Language Models  
> 作者：Bowen Peng 等 (Nous Research)  
> arXiv：2309.00071  
> 发布时间：2023年9月  
> 标签：#长上下文 #RoPE #LLaMA #位置编码

---

## 核心创新

> [!tip] 一句话总结
> **YaRN 是一种高效扩展 RoPE 模型上下文窗口的方法，只需 10 倍更少的 tokens 和 2.5 倍更少的训练步数。**

| 方法 | 训练数据量 | 训练步数 | 扩展能力 |
|------|-----------|---------|---------|
| Position Interpolation (PI) | ~1% 原数据 | ~1000 步 | 最多 8x |
| **YaRN** | **~0.1% 原数据** | **~400 步** | **32x+** |

---

## 问题背景

### RoPE 的长度限制

> [!warning] 核心问题
> RoPE 模型（如 LLaMA）在训练时见过最大长度 L，无法泛化到更长的序列 L' > L。

```
训练长度 L = 4096
推理长度 L' = 128000
→ 模型困惑度爆炸，输出质量急剧下降
```

### 为什么 RoPE 不能外推？

**关键观察**：

| 维度 d | 波长 λ_d | 特性 |
|--------|---------|------|
| λ < L（短波长） | 旋转多次 | 编码**相对位置**信息 |
| λ > L（长波长） | 未完成一次旋转 | 编码**绝对位置**信息 |

> [!important] 
> 不同维度的 RoPE 编码不同类型的位置信息，需要**分维度处理**。

---

## 方法演进路径

```
原始 RoPE
    ↓
Position Interpolation (PI) — 等比例压缩所有维度
    ↓
NTK-aware Interpolation — 考虑高频信息丢失
    ↓
NTK-by-parts Interpolation — 分维度处理
    ↓
YaRN — 加入温度系数 + NTK-by-parts
    ↓
Dynamic-YaRN — 推理时动态缩放
```

---

## 各方法详解

### 1. Position Interpolation (PI)

**思路**：等比例压缩位置

```math
g(m) = s × m  （位置线性压缩）
h(θ) = θ      （频率不变）
```

**问题**：
- 高频信息丢失（所有维度同等压缩）
- 扩展因子 s > 8 时性能急剧下降

---

### 2. NTK-aware Interpolation

**思路**：改变 RoPE 的 base，保留高频信息

> [!note] 理论依据
> 来自 Neural Tangent Kernel (NTK) 理论：神经网络难以学习低维输入的高频信息。

**解决方案**：
- 高频维度（小 θ）：少压缩
- 低频维度（大 θ）：多压缩

**问题**：最优 base 需要经验调参

---

### 3. NTK-by-parts Interpolation

**思路**：显式分维度处理

**定义**：

| 条件 | 处理方式 |
|------|---------|
| r < α（波长远大于 L） | 线性插值（避免外推） |
| r > β（波长远小于 L） | 不插值（保留高频） |
| α ≤ r ≤ β | 介于两者之间 |

其中 `r = L / λ`（波长比）

**公式**：

```math
g(m) = m
h(θ_d) = (1 - γ(r)) × θ_d/s + γ(r) × θ_d

γ(r) = ramp function:
  0,      if r < α
  1,      if r > β
  (r-α)/(β-α), otherwise
```

**推荐参数**（LLaMA 家族）：
- α = 1
- β = 32

---

### 4. YaRN（完整方法）

**核心创新**：加入温度系数 t

```math
Attention = softmax(q^T k / (t × |D|))
```

> [!important] 
> 温度系数可以"零开销"实现：直接缩放 RoPE embedding

**温度推荐公式**：

```math
t = 0.1 × ln(s) + 1
```

**完整 YaRN 定义**：
- NTK-by-parts interpolation
- Attention temperature scaling

---

### 5. Dynamic-YaRN（推理时）

**思路**：推理时动态调整缩放因子

```math
s = max(1, l' / L)  （当前序列长度 / 训练长度）
```

**优势**：
- 无需微调，直接在原模型上使用
- 序列长度逐渐增长时平滑过渡

---

## 实验结果

### 训练效率

> [!success] 关键结果
> YaRN 收敛更快，损失更低

```
LLaMA 7B 扩展到 32k：
- YaRN: 400 步收敛
- PI: 1000+ 步仍有较高损失
```

### 长序列语言建模（Proof-pile）

| 模型 | 方法 | 8k | 16k | 32k | 64k | 128k |
|------|------|----|----|-----|-----|------|
| Llama2 7B | YaRN (s=16) | 3.51 | 2.99 | 2.65 | 2.42 | >100 |
| Llama2 7B | YaRN (s=32) | 3.56 | 3.04 | 2.70 | 2.45 | **2.37** |
| Llama2 13B | YaRN (s=32) | 3.29 | 2.83 | 2.53 | 2.31 | **2.24** |

> [!success] 外推成功
> s=32 模型用 64k 数据训练，能外推到 128k（困惑度继续下降）

---

## 实际应用

### 已采用 YaRN 的项目

| 项目 | 使用方法 |
|------|---------|
| Code Llama | NTK-aware（base=1M） |
| Qwen 7B | Dynamic NTK |
| LLaMA 长上下文版本 | YaRN |

---

## 代码实现要点

### YaRN 的 RoPE 计算

```python
# 计算新的频率
def compute_yarn_freqs(original_freqs, scale, alpha=1, beta=32):
    # 计算波长比 r
    r = L / (2 * pi * original_freqs)
    
    # ramp 函数
    gamma = torch.where(r < alpha, 0,
                torch.where(r > beta, 1,
                    (r - alpha) / (beta - alpha)))
    
    # 新频率
    new_freqs = (1 - gamma) * original_freqs / scale + gamma * original_freqs
    return new_freqs

# 温度缩放
def yarn_rope(q, k, freqs, scale):
    t = 0.1 * log(scale) + 1
    # 应用 RoPE 并缩放
    q_rope = apply_rope(q, freqs) / sqrt(t)
    k_rope = apply_rope(k, freqs) / sqrt(t)
    return q_rope, k_rope
```

---

## 与其他方法的对比

| 方法 | 训练开销 | 外推能力 | 无需微调 | Flash Attention |
|------|---------|---------|---------|----------------|
| PI | 高 | 8x | ✗ | ✓ |
| NTK-aware | 中 | 16x | ✗ | ✓ |
| ReRoPE | 无 | 无限 | ✓ | ✗ |
| LM-Infinite | 无 | 无限 | ✓ | ✗ |
| **YaRN** | **低** | **32x+** | ✗ | **✓** |
| **Dynamic-YaRN** | **无** | **2x+** | **✓** | **✓** |

---

## 我的理解

### YaRN 的核心洞察

> [!note] 个人分析
> 1. **分维度处理**：不同 RoPE 维度编码不同位置信息，不能一刀切
> 2. **高频保护**：高频信息对局部语义至关重要，不能过度压缩
> 3. **温度调节**：长距离注意力分布变"尖锐"，需要温度软化
> 4. **零开销实现**：通过缩放 embedding 实现温度，不修改 attention 代码

### 与 RoPE 的关系

```
RoPE 是位置编码的基础
YaRN 是 RoPE 的长度扩展方法
两者配合使用，而不是替代
```

---

## 相关概念

- [[RoPE 旋转位置编码研究笔记]] ← 基础
- [[长上下文技术]] ← YaRN 是关键方法之一
- [[15-位置编码]]（minimind 笔记）

---

## 参考文献

- 原论文：[arXiv:2309.00071](https://arxiv.org/abs/2309.00071)
- 代码：[github.com/jquesnelle/yarn](https://github.com/jquesnelle/yarn)
- 相关：Position Interpolation ([Chen et al., 2023])

---

*创建时间：2026-04-15*  
*论文下载：`YaRN-Context-Extension.pdf`（同目录）*