# Feed-Forward Network (FFN) - 前馈神经网络

## 一句话总结

**FFN = 多层全连接层 + 激活函数**

信号**单向流动**（输入→隐藏层→输出），没有回路、没有循环。

---

## 核心特点

| 特点 | 说明 |
|------|------|
| **前馈** | 信号只向前传，不回头 |
| **全连接** | 每层神经元和下一层所有神经元相连 |
| **无环** | 没有循环/反馈连接 |
| **静态映射** | 同样输入永远产生同样输出 |
| **参数独立** | 每个位置的权重独立（不共享） |

---

## 基本结构

```
输入层 → 隐藏层 1 → 隐藏层 2 → ... → 输出层
   ↓         ↓           ↓            ↓
   x       h1=σ(W1x+b1)  h2=σ(W2h1+b2)  y=W_out*h_last+b_out
```

### 数学公式

**单层 FFN**：
$$h = \sigma(W_1 x + b_1)$$
$$y = W_2 h + b_2$$

**合并**：
$$\text{FFN}(x) = W_2 \cdot \sigma(W_1 x + b_1) + b_2$$

其中：
- $x$：输入向量
- $W_1, W_2$：权重矩阵
- $b_1, b_2$：偏置向量
- $\sigma$：激活函数（ReLU、GELU、Tanh 等）

### 代码实现（单层）
```python
import torch
import torch.nn as nn

class SimpleFFN(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super().__init__()
        self.linear1 = nn.Linear(input_dim, hidden_dim)
        self.activation = nn.ReLU()
        self.linear2 = nn.Linear(hidden_dim, output_dim)
    
    def forward(self, x):
        x = self.linear1(x)
        x = self.activation(x)
        x = self.linear2(x)
        return x

# 使用
ffn = SimpleFFN(128, 256, 10)
x = torch.randn(32, 128)  # (batch, input_dim)
output = ffn(x)           # (batch, output_dim)
```

---

## 在 Transformer 中的 FFN

Transformer 里的 FFN 是**每个注意力层之后**的标准组件。

### 结构

```python
class TransformerFFN(nn.Module):
    def __init__(self, d_model, d_ff, dropout=0.1):
        super().__init__()
        self.linear1 = nn.Linear(d_model, d_ff)   # 升维 (4x)
        self.linear2 = nn.Linear(d_ff, d_model)   # 降维 (回原维度)
        self.activation = nn.GELU()
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, x):
        x = self.linear1(x)
        x = self.activation(x)
        x = self.dropout(x)
        x = self.linear2(x)
        return x
```

### 典型配置

| 模型 | d_model | d_ff | 倍数 |
|------|---------|------|------|
| Transformer-Base | 512 | 2048 | 4x |
| Transformer-Big | 1024 | 4096 | 4x |
| BERT-Base | 768 | 3072 | 4x |
| BERT-Large | 1024 | 4096 | 4x |
| LLaMA-7B | 4096 | 11008 | 2.7x (SwiGLU) |

### 完整 Transformer Block

```python
class TransformerBlock(nn.Module):
    def __init__(self, d_model, n_heads, d_ff, dropout=0.1):
        super().__init__()
        self.attention = nn.MultiheadAttention(d_model, n_heads, dropout=dropout)
        self.ffn = TransformerFFN(d_model, d_ff, dropout)
        self.ln1 = nn.LayerNorm(d_model)
        self.ln2 = nn.LayerNorm(d_model)
    
    def forward(self, x):
        # Attention 子层 + 残差 + LayerNorm
        attn_output, _ = self.attention(x, x, x)
        x = self.ln1(x + attn_output)
        
        # FFN 子层 + 残差 + LayerNorm
        ffn_output = self.ffn(x)
        x = self.ln2(x + ffn_output)
        
        return x
```

### 在 Transformer 中的位置

```
输入 → Embedding → [LayerNorm → Attention → LayerNorm → FFN] × N → 输出
                                              ↑              ↑
                                           交流信息        独立思考
```

---

## 为什么 Transformer 需要 FFN？

### Attention 和 FFN 的分工

| 组件 | 作用 | 信息流动 | 类比 |
|------|------|---------|------|
| **Self-Attention** | 让 token 之间**互相交流** | 跨位置整合信息 | 开会讨论 |
| **FFN** | 让每个 token **独立处理** | 每个位置独立变换 | 各自消化 |

### 形象理解

假设处理句子 "The cat sat on the mat"：

**Attention 阶段**：
- "cat" 关注 "sat"（动作）
- "sat" 关注 "cat"（主语）和 "mat"（地点）
- token 之间交换信息

**FFN 阶段**：
- 每个 token 独立处理自己收到的信息
- "cat" → 提取"动物、主语"特征
- "sat" → 提取"动作、过去式"特征
- 互不干扰

### 为什么需要两步？

```
只有 Attention：
- token 之间能交流，但没有深度特征变换
- 模型表达能力受限

只有 FFN：
- 每个位置独立处理，无法理解上下文
- "bank" 无法区分是"银行"还是"河岸"

Attention + FFN：
- 先交流（理解上下文）
- 再处理（提取深层特征）
- 最佳组合！
```

---

## 🔑 为什么 FFN 要升维（d_ff > d_model）？

### 现象
Transformer 中 `d_ff` 通常是 `d_model` 的 **4 倍**：
- d_model = 512 → d_ff = 2048
- d_model = 768 → d_ff = 3072

### 原因

#### 1. 高维空间更容易线性可分
```
低维空间 (2D)：          高维空间 (3D+)：
  ● ○                    ●
 ○ ●  ← 无法直线分开       ○  ← 可以找个平面分开
  ● ○                    ● ○
```

#### 2. 容纳更多特征
```python
# d_model=512：每个 token 用 512 维表示
# d_ff=2048：中间可以提取 2048 种不同特征

# 类比：
# 512 维 = 512 个"概念"
# 2048 维 = 2048 个"概念"（更细粒度）
```

#### 3. 信息瓶颈
```
输入 (512) → 升维 (2048) → 降维 (512)
              ↓
        高维空间做复杂变换
        然后压缩回原维度
```

**类比**：
- 把问题"展开"到更高维度（更容易处理）
- 处理完再"压缩"回来（保持接口一致）

### 代码验证
```python
import torch
import torch.nn as nn

d_model, d_ff = 512, 2048
ffn = nn.Sequential(
    nn.Linear(d_model, d_ff),
    nn.GELU(),
    nn.Linear(d_ff, d_model)
)

x = torch.randn(32, 10, d_model)  # (batch, seq, d_model)
print(f"输入形状：{x.shape}")      # torch.Size([32, 10, 512])

# 中间层
hidden = ffn[0](x)
print(f"升维后：{hidden.shape}")   # torch.Size([32, 10, 2048])

# 输出
output = ffn(x)
print(f"降维后：{output.shape}")   # torch.Size([32, 10, 512])
```

---

## FFN 的变体

### 1. 标准 FFN（Transformer 原版）
```python
FFN(x) = W_2 · ReLU(W_1 x + b_1) + b_2
```
- 激活函数：ReLU
- 升维倍数：4x

### 2. GELU 版本（BERT、GPT）
```python
FFN(x) = W_2 · GELU(W_1 x + b_1) + b_2
```
- 激活函数：GELU（更平滑）
- 升维倍数：4x

### 3. SwiGLU（LLaMA、PaLM、更现代）
```python
FFN(x) = (Swish(xW) ⊗ (xV)) · W2
```
- 两个线性投影 W 和 V
- Swish 激活（x · sigmoid(x)）
- ⊗ 是逐元素相乘（门控机制）
- 升维倍数：~2.7x（参数效率更高）

**代码**：
```python
class SwiGLUFFN(nn.Module):
    def __init__(self, d_model, d_ff):
        super().__init__()
        self.W = nn.Linear(d_model, d_ff)
        self.V = nn.Linear(d_model, d_ff)
        self.W2 = nn.Linear(d_ff, d_model)
    
    def forward(self, x):
        return self.W2(F.silu(self.W(x)) * self.V(x))
```

### 4. MoE（Mixture of Experts，超大模型）
```python
# 多个 FFN 并行，用门控选择激活哪些
output = Σ(gate_i(x) × FFN_i(x))
```
- 多个"专家"FFN（如 8 个、64 个）
- 每个 token 只激活其中几个（如 top-2）
- 总参数多，但计算量可控
- 用于：GShard、Switch Transformer、Mixtral

**代码**：
```python
class MoEFFN(nn.Module):
    def __init__(self, d_model, d_ff, num_experts=8, top_k=2):
        super().__init__()
        self.experts = nn.ModuleList([
            TransformerFFN(d_model, d_ff) for _ in range(num_experts)
        ])
        self.gate = nn.Linear(d_model, num_experts)
        self.top_k = top_k
    
    def forward(self, x):
        # 计算门控权重
        gate_logits = self.gate(x)  # (batch, seq, num_experts)
        top_k_logits, top_k_indices = gate_logits.topk(self.top_k, dim=-1)
        gate_weights = F.softmax(top_k_logits, dim=-1)
        
        # 加权组合专家输出
        output = 0
        for i, expert in enumerate(self.experts):
            mask = (top_k_indices == i).unsqueeze(-1)
            output += expert(x) * gate_weights[..., self.top_k_indices == i]
        
        return output
```

---

## FFN vs 其他网络结构

| 类型 | 连接方式 | 权重共享 | 适用场景 |
|------|---------|---------|---------|
| **FFN** | 全连接 | 不共享 | 表格数据、分类头、Transformer 内部 |
| **CNN** | 局部连接（卷积核） | 空间共享 | 图像、空间数据 |
| **RNN** | 循环连接 | 时间共享 | 序列、时间序列 |
| **Attention** | 全局连接 | 不共享（但 QKV 共享） | 序列、长距离依赖 |

### 参数量对比

假设输入维度 = 输出维度 = 512，隐藏层 = 2048：

| 类型 | 参数量 | 计算特点 |
|------|--------|---------|
| **FFN** | 512×2048 + 2048×512 ≈ 2M | 独立处理每个位置 |
| **CNN** (3×3 卷积) | 512×512×3×3 ≈ 2.4M | 局部感受野 |
| **Attention** | 512×512×3 (QKV) ≈ 0.8M | 全局依赖，O(n²) 复杂度 |

---

## 常见误区

### ❌ "FFN 就是全连接层"
**不完全对**：
- 全连接层（Linear）是单层
- FFN 通常指**多层**全连接 + 激活函数
- FFN = Linear → Activation → Linear

### ❌ "FFN 在 Transformer 中不重要"
**错**：
- 消融实验证明：去掉 FFN 性能大幅下降
- FFN 贡献了 Transformer 大部分参数（约 2/3）
- Attention 负责"交流"，FFN 负责"思考"

### ❌ "升维倍数越大越好"
**不一定**：
- 4x 是经验值，平衡效果和计算量
- 太大：过拟合、计算慢
- 太小：表达能力不足
- SwiGLU 用 2.7x 达到类似效果（更高效）

### ❌ "FFN 可以跨位置共享信息"
**错**：
- FFN 对每个位置**独立**处理
- 位置间信息交流只靠 Attention
- FFN(x[:, i]) 只依赖 x[:, i]，不依赖 x[:, j]

---

## 实际应用示例

### 1. 分类任务的 FFN 头
```python
class Classifier(nn.Module):
    def __init__(self, input_dim, num_classes):
        super().__init__()
        self.ffn = nn.Sequential(
            nn.Linear(input_dim, input_dim * 2),
            nn.GELU(),
            nn.Dropout(0.1),
            nn.Linear(input_dim * 2, num_classes)
        )
    
    def forward(self, x):
        return self.ffn(x)
```

### 2. 残差连接的 FFN
```python
class ResidualFFN(nn.Module):
    def __init__(self, d_model, d_ff):
        super().__init__()
        self.ffn = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.GELU(),
            nn.Linear(d_ff, d_model)
        )
        self.ln = nn.LayerNorm(d_model)
    
    def forward(self, x):
        return self.ln(x + self.ffn(x))  # 残差连接
```

### 3. 级联 FFN（更深）
```python
class DeepFFN(nn.Module):
    def __init__(self, input_dim, hidden_dims, output_dim):
        super().__init__()
        layers = []
        prev_dim = input_dim
        for h_dim in hidden_dims:
            layers.extend([
                nn.Linear(prev_dim, h_dim),
                nn.GELU(),
                nn.Dropout(0.1)
            ])
            prev_dim = h_dim
        layers.append(nn.Linear(prev_dim, output_dim))
        self.net = nn.Sequential(*layers)
    
    def forward(self, x):
        return self.net(x)

# 使用：3 层隐藏层
deep_ffn = DeepFFN(128, [256, 512, 256], 10)
```

---

## 总结

| 问题 | 答案 |
|------|------|
| FFN 是什么？ | 多层全连接层 + 激活函数 |
| 信号怎么流动？ | 单向，从输入到输出，不回头 |
| Transformer 中作用？ | 独立处理每个 token 的特征变换 |
| 为什么要升维？ | 高维空间做更复杂的特征变换 |
| 有循环/反馈吗？ | 没有，纯前馈 |
| 常见激活函数？ | ReLU、GELU、SwiGLU |
| 升维倍数？ | 通常 4x（SwiGLU 约 2.7x） |
| 参数量占比？ | Transformer 中约 2/3 |

### 核心要点

1. **FFN = Linear → Activation → Linear**
2. **Transformer 中：Attention 交流信息，FFN 独立思考**
3. **升维（4x）是为了高维空间做更复杂变换**
4. **每个位置独立处理，不跨位置共享**
5. **现代变体：SwiGLU（更高效）、MoE（更大规模）**

**记住**：FFN 是神经网络的"基本功"，所有复杂架构（CNN、RNN、Transformer）都包含 FFN 作为基础组件。在 Transformer 中，它和 Attention 配合，一个负责"交流"，一个负责"消化"。

---

**标签**: #深度学习 #神经网络 #FFN #前馈网络 #Transformer #模型架构

**创建日期**: 2026-03-23
**相关**: [[LayerNorm vs Softmax - 本质区别]] [[Transformer 架构详解]] [[激活函数对比]] [[PyTorch 参数管理 - Parameter vs Buffer]]
