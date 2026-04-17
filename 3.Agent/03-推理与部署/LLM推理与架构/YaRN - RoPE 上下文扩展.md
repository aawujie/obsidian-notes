# YaRN - RoPE 上下文扩展

## 概述

**YaRN**（Yet another RoPE extension）是一种用于扩展 Transformer 模型上下文窗口的技术，专门针对使用 **RoPE**（Rotary Position Embedding）的模型。

> <span style="color:rgb(255, 77, 77)"><b>RoPE 负责编码位置，YaRN 负责扩展长度，两者结合实现训短用长</b></span>

---

## 核心问题：RoPE 的外推困境

### RoPE 的局限

RoPE 模型（如 LLaMA、Mistral）在训练时有一个<span style="color:rgb(255, 77, 77)"><b>固定的上下文长度</b></span>（如 2048 或 4096）。<span style="color:rgb(255, 77, 77)">直接外推到更长的序列会导致性能急剧下降</span>：

```
训练长度: 4096 tokens
推理长度: 8192 tokens ← 超出训练范围！
结果: 注意力分数分布混乱 → 模型失效
```

### <span style="color:rgb(255, 77, 77)">为什么会失效？</span>

1. <span style="color:rgb(255, 77, 77)"><b>位置编码超出范围</b></span>：RoPE 的旋转角度随位置线性增长，长序列的角度模型从未见过
2. <span style="color:rgb(255, 77, 77)"><b>注意力分布偏移</b></span>：<span style="color:rgb(195, 117, 255)">远距离 token 的注意力权重变得异常</span>
3. <span style="color:rgb(255, 77, 77)"><b>内积爆炸/消失</b></span>：旋转后的向量内积超出稳定范围

---

## YaRN 的解决方案

### 核心思想

通过<span style="color:rgb(255, 77, 77)"><b>修改注意力温度（temperature）</b> </span>来保持<span style="color:rgb(255, 77, 77)">长序列的注意力分布与训练时的短序列相似</span>：

```
Attention(Q, K, V) = softmax(Q·K^T / (temperature × √d_k)) · V
```

### 温度缩放公式

```
temperature = (L_train / L_current)^(1/α)

其中：
- L_train: 训练时的最大长度（如 4096）
- L_current: 当前序列长度
- α: 超参数（通常 1 或 2）
```

### 温度是什么？直观理解

温度控制注意力分布的**"平滑程度"**：

| 温度 | 效果 | 类比 |
|------|------|------|
| **temperature = 1** | 标准 softmax | 正常音量 |
| **temperature > 1** | 分布更平滑 | 音量调小，差异变小 |
| **temperature < 1** | 分布更尖锐 | 音量调大，差异变大 |

#### Code Demo

```python
import torch

scores = torch.tensor([1.0, 2.0, 3.0])

# temperature = 1 (standard)
softmax_1 = torch.softmax(scores / 1, dim=0)
# → [0.09, 0.24, 0.67]  obvious difference

# temperature = 2 (smoother)
softmax_2 = torch.softmax(scores / 2, dim=0)  
# → [0.18, 0.32, 0.50]  smaller difference

# temperature = 0.5 (sharper)
softmax_05 = torch.softmax(scores / 0.5, dim=0)
# → [0.02, 0.12, 0.86]  larger difference
```

![Temperature 对 Softmax 分布的影响](temperature_softmax.png)

*上图直观展示：temperature 越大，概率分布越平滑（差距越小）；temperature 越小，分布越尖锐（差距越大）*

#### 为什么 YaRN 需要增大温度？

**问题：序列变长 → 注意力变"尖锐"**

```
短序列（训练时）：
位置 1 和位置 10 的注意力：[0.1, 0.2] → softmax → [0.45, 0.55]  较平滑

长序列（推理时）：
位置 1 和位置 100 的注意力：[0.01, 0.1] → softmax → [0.02, 0.98]  太尖锐！
```

**尖锐的问题**：模型只关注极少数位置，忽略其他重要信息。

**解决**：增大温度 → 强制平滑

```python
长序列 + temperature=2：
[0.01, 0.1] / 2 = [0.005, 0.05] → softmax → [0.12, 0.88]  更平滑！
```

### 场景对比

| 场景 | 温度调整 | 效果 |
|------|----------|------|
| 序列长度 = 训练长度 | temperature = 1 | 正常注意力 |
| 序列长度 > 训练长度 | temperature > 1 | 软化注意力，防止尖锐分布 |
| 序列长度 < 训练长度 | temperature < 1 | 锐化注意力（较少使用）|

---

## YaRN vs 其他方法

### 位置插值 <span style="color:rgb(255, 77, 77)">PI（Position Interpolation）</span>

```python
# PI: 将位置编码压缩到训练范围内
position = position × (L_train / L_current)
```

- **优点**：简单直接
- **缺点**：需要微调（fine-tuning），否则性能下降

### YaRN

```python
# YaRN: 保持位置编码不变，调整注意力温度
temperature = (L_train / L_current)^(1/α)
```

- **优点**：<span style="color:rgb(255, 77, 77)">免训练直接外推（training-free extrapolation）</span>
- **缺点**：超参数 α 需要调优

### 对比总结

| 方法            | 原理   | 需要微调  | 外推能力  |
| ------------- | ---- | ----- | ----- |
| **直接外推**      | 无    | 否     | ❌ 极差  |
| **PI**        | 压缩位置 | ✅ 需要  | ⚠️ 一般 |
| **YaRN**      | 温度缩放 | ❌ 不需要 | ✅ 优秀  |
| **NTK-aware** | 频率调整 | 部分需要  | ✅ 良好  |

---

## 实际应用

### 现代大模型的选择

| 模型         | 基础位置编码 | 扩展方案                  | 上下文长度    |
| ---------- | ------ | --------------------- | -------- |
| LLaMA-1    | RoPE   | 无                     | 2048     |
| LLaMA-2    | RoPE   | 部分使用 YaRN             | 4096     |
| Mistral-7B | RoPE   | Sliding Window + YaRN | 8192/32K |
| Yi-34B     | RoPE   | YaRN                  | 200K     |
| GPT-4      | 未知     | 类似技术                  | 128K     |

### 代码示例（概念）

```python
import torch
import torch.nn as nn

class YaRNAttention(nn.Module):
    """使用 YaRN 的注意力层"""
    
    def __init__(self, d_model, n_heads, max_train_len=4096, alpha=1.0):
        super().__init__()
        self.d_model = d_model
        self.n_heads = n_heads
        self.max_train_len = max_train_len
        self.alpha = alpha
        
        # 标准 RoPE
        self.rope = RotaryPositionalEmbedding(d_model // n_heads)
        
    def forward(self, q, k, v):
        batch_size, seq_len, _ = q.shape
        
        # 应用 RoPE
        q = self.rope(q)
        k = self.rope(k)
        
        # 计算注意力分数
        scores = torch.matmul(q, k.transpose(-2, -1)) / torch.sqrt(self.d_model)
        
        # YaRN: 动态温度缩放
        if seq_len > self.max_train_len:
            temperature = (self.max_train_len / seq_len) ** (1 / self.alpha)
            scores = scores / temperature
        
        # Softmax 和加权
        attn = torch.softmax(scores, dim=-1)
        output = torch.matmul(attn, v)
        
        return output
```

---

## 数学原理深入

### RoPE 回顾

RoPE 通过旋转矩阵编码位置：

```
R(θ, m) = [[cos(mθ), -sin(mθ)],
           [sin(mθ),  cos(mθ)]]

其中 m 是位置，θ 是频率
```

### YaRN 的温度缩放

关键洞察：<span style="color:rgb(255, 77, 77)"><b>长序列的注意力分布应该与短序列相似</b></span>

```
原始注意力: A_ij = softmax(q_i · k_j / √d)

YaRN 注意力: A_ij = softmax(q_i · k_j / (temperature × √d))

温度缩放: temperature = (L_train / L_current)^(1/α)
```

### 为什么温度缩放有效？

1. **长度增加 → 内积方差增大 → Softmax 更尖锐**
2. **温度 > 1 → 软化 Softmax → 恢复原有分布**
3. **保持相对关系 → 不影响模型学到的模式**

---

## 超参数调优

### α（alpha）参数

```
α = 1: 线性温度缩放
α = 2: 平方根温度缩放（更保守）
```

| α 值 | 适用场景     |
| --- | -------- |
| 1.0 | 2-4 倍外推  |
| 2.0 | 4-8 倍外推  |
| 4.0 | 8-16 倍外推 |

### 实际调优建议

1. **从 α=1 开始**
2. **在验证集上测试困惑度（perplexity）**
3. **如果性能下降，增大 α**
4. **如果注意力过于平滑，减小 α**

---

## 一句话总结

> **温度 = "注意力分散器"**：序列太长 → 注意力太集中 → 增大温度 → 强制分散注意力 → 恢复训练时的分布

> **RoPE 编码位置信息，YaRN 通过温度缩放让模型"感觉"序列没那么长，从而实现免训练的长上下文扩展。**

---

## 相关概念

- [[RoPE - 旋转位置编码]]
- [[注意力机制详解]]
- [[大模型上下文扩展技术]]
- [[NTK-aware 位置编码]]
- [[位置插值 PI]]

---

## 参考资料

1. YaRN Paper: "YaRN: Efficient Context Window Extension of Large Language Models" (Peng et al., 2023)
2. RoPE Paper: "RoFormer: Enhanced Transformer with Rotary Position Embedding" (Su et al., 2021)
3. PI Paper: "Extending Context Window of Large Language Models via Position Interpolation" (Chen et al., 2023)
4. 技术博客: https://blog.eleuther.ai/yarn/
