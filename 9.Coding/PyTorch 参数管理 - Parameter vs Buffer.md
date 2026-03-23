# PyTorch 参数管理 - Parameter vs Buffer

## 一句话总结

- **`nn.Parameter`**：模型要**学习**的东西（权重、偏置）
- **`register_buffer`**：模型要**记住**但不学的东西（统计量、掩码）

---

## 核心区别

| 特性 | `nn.Parameter` | `register_buffer` | 直接赋值 `self.xxx` |
|------|---------------|-------------------|---------------------|
| 出现在 `parameters()` | ✅ | ❌ | ❌ |
| 出现在 `buffers()` | ❌ | ✅ | ❌ |
| 出现在 `state_dict()` | ✅ | ✅ | ❌ |
| `requires_grad` | True（自动） | False（默认） | 取决于张量 |
| 优化器会更新 | ✅ | ❌ | - |
| `.cuda()` 自动移动 | ✅ | ✅ | ❌ |
| 保存/加载会保留 | ✅ | ✅ | ❌ |

---

## 代码示例

### 定义模型
```python
import torch
import torch.nn as nn

class _Demo(nn.Module):
    def __init__(self):
        super().__init__()
        
        # 可学习参数
        self.weight = nn.Parameter(torch.randn(3))
        
        # 缓冲常量
        self.register_buffer('constant', torch.tensor([1.0, 2.0, 3.0]))
        
        # ❌ 错误：直接赋值（不推荐）
        self.temp = torch.tensor([9, 9, 9])

_m = _Demo()
```

### 查看参数
```python
print("可学习参数:")
for name, p in _m.named_parameters():
    print(f" {name}: {p.data} (requires_grad={p.requires_grad})")

# 输出:
# weight: tensor([...]) (requires_grad=True)

print("Buffer (常量):")
for name, b in _m.named_buffers():
    print(f" {name}: {b} (requires_grad={b.requires_grad})")

# 输出:
# constant: tensor([1., 2., 3.]) (requires_grad=False)

print("直接赋值的属性:")
print(f" temp: {_m.temp} (不在 parameters 或 buffers 中)")
```

---

## nn.Parameter - 可学习参数

### 是什么
`nn.Parameter` 是 `torch.Tensor` 的子类，自动设置 `requires_grad=True`。

### 特点
- ✅ 会被优化器更新（SGD、Adam 等）
- ✅ 出现在 `model.parameters()` 中
- ✅ 会被 `state_dict()` 保存
- ✅ `.cuda()` 时自动移动到 GPU
- ✅ 保存/加载模型时会保留

### 使用场景
```python
# 1. 线性层权重和偏置
self.weight = nn.Parameter(torch.randn(out_dim, in_dim))
self.bias = nn.Parameter(torch.zeros(out_dim))

# 2. LayerNorm 的缩放和平移
self.gamma = nn.Parameter(torch.ones(dim))   # γ
self.beta = nn.Parameter(torch.zeros(dim))   # β

# 3. Embedding 矩阵
self.embedding = nn.Parameter(torch.randn(vocab_size, embed_dim))

# 4. 注意力机制中的查询、键、值投影
self.W_q = nn.Parameter(torch.randn(d_model, d_k))
self.W_k = nn.Parameter(torch.randn(d_model, d_k))
self.W_v = nn.Parameter(torch.randn(d_model, d_v))
```

### 训练时的行为
```python
model = _Demo()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# 训练循环
for x, y in dataloader:
    optimizer.zero_grad()
    output = model(x)
    loss = criterion(output, y)
    loss.backward()
    optimizer.step()  # ← 只更新 nn.Parameter，不更新 buffer
```

---

## register_buffer - 缓冲常量

### 是什么
`register_buffer()` 注册的张量会成为模型的一部分，但不会被当作可学习参数。

### 特点
- ❌ 不会被优化器更新
- ❌ 不会计算梯度（`requires_grad=False`）
- ✅ 会被 `state_dict()` 保存
- ✅ `.cuda()` 时自动移动到 GPU
- ✅ 保存/加载模型时会保留

### 使用场景

#### 1. BatchNorm 的运行统计量
```python
class BatchNorm(nn.Module):
    def __init__(self, num_features):
        super().__init__()
        # 可学习
        self.weight = nn.Parameter(torch.ones(num_features))
        self.bias = nn.Parameter(torch.zeros(num_features))
        
        # 缓冲（训练时累积，但不通过梯度更新）
        self.register_buffer('running_mean', torch.zeros(num_features))
        self.register_buffer('running_var', torch.ones(num_features))
        self.register_buffer('num_batches_tracked', torch.tensor(0))
```

#### 2. Transformer 位置编码
```python
class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=5000):
        super().__init__()
        
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2) * -(math.log(10000.0) / d_model))
        
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        
        # 注册为 buffer（固定不变）
        self.register_buffer('pe', pe.unsqueeze(0))  # (1, max_len, d_model)
    
    def forward(self, x):
        return x + self.pe[:, :x.size(1), :]
```

#### 3. 注意力掩码
```python
class Transformer(nn.Module):
    def __init__(self, seq_len):
        super().__init__()
        # 下三角掩码（防止看到未来）
        mask = torch.triu(torch.ones(seq_len, seq_len), diagonal=1)
        mask = mask.masked_fill(mask == 1, float('-inf'))
        self.register_buffer('attn_mask', mask)
    
    def forward(self, x):
        # 使用掩码
        attn_scores = self.attn(x) + self.attn_mask
        return F.softmax(attn_scores, dim=-1)
```

#### 4. 固定权重/预计算值
```python
class FixedConv(nn.Module):
    def __init__(self):
        super().__init__()
        # Sobel 算子（边缘检测，固定不变）
        sobel_x = torch.tensor([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=torch.float32)
        self.register_buffer('sobel_kernel', sobel_x.view(1, 1, 3, 3))
    
    def forward(self, x):
        return F.conv2d(x, self.sobel_kernel)
```

---

## ❌ 为什么不能直接赋值？

### 问题 1：不会出现在 state_dict() 中
```python
class BadModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.weight = nn.Parameter(torch.randn(3, 3))  # ✅
        self.mask = torch.ones(3, 3)                   # ❌ 直接赋值

model = BadModel()
state = model.state_dict()

print('weight' in state)  # True
print('mask' in state)    # False ← 保存时会丢失！
```

### 问题 2：设备移动时不会跟着走
```python
model = BadModel()
model.cuda()

print(model.weight.device)  # cuda:0 ✅
print(model.mask.device)    # cpu ❌ 还在 CPU 上！
```

### 问题 3：优化器可能漏掉
```python
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
# 只包含 weight，不包含 mask
```

---

## 完整对比示例

```python
import torch
import torch.nn as nn

class CompleteExample(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super().__init__()
        
        # ========== 可学习参数 (nn.Parameter) ==========
        self.W1 = nn.Parameter(torch.randn(hidden_dim, input_dim))
        self.b1 = nn.Parameter(torch.zeros(hidden_dim))
        self.W2 = nn.Parameter(torch.randn(output_dim, hidden_dim))
        self.b2 = nn.Parameter(torch.zeros(output_dim))
        
        # LayerNorm 参数
        self.gamma = nn.Parameter(torch.ones(hidden_dim))
        self.beta = nn.Parameter(torch.zeros(hidden_dim))
        
        # ========== 缓冲常量 (register_buffer) ==========
        # 位置编码
        self.register_buffer('pos_encoding', self._make_pos_encoding(hidden_dim))
        
        # 注意力掩码
        self.register_buffer('causal_mask', self._make_causal_mask(100))
        
        # 运行统计量
        self.register_buffer('running_mean', torch.zeros(hidden_dim))
        self.register_buffer('running_var', torch.ones(hidden_dim))
        
        # ========== 临时变量（不要存为 self.xxx）==========
        # 这些在 forward 中计算即可，不需要保存
    
    def _make_pos_encoding(self, dim):
        # 简化的位置编码
        return torch.randn(1, 100, dim)
    
    def _make_causal_mask(self, seq_len):
        mask = torch.triu(torch.ones(seq_len, seq_len), diagonal=1)
        return mask.masked_fill(mask == 1, float('-inf'))
    
    def forward(self, x):
        # 使用 buffer
        x = x + self.pos_encoding[:, :x.size(1), :]
        
        # 前向传播
        x = torch.linear(x, self.W1, self.b1)
        x = self.gamma * (x - x.mean()) / x.std() + self.beta  # LayerNorm
        x = torch.linear(x, self.W2, self.b2)
        
        return x

# 测试
model = CompleteExample(128, 256, 10)

print("可学习参数数量:", len(list(model.parameters())))
# 输出：6 (W1, b1, W2, b2, gamma, beta)

print("Buffer 数量:", len(list(model.buffers())))
# 输出：4 (pos_encoding, causal_mask, running_mean, running_var)

print("state_dict 键:", list(model.state_dict().keys()))
# 包含所有 Parameter 和 Buffer
```

---

## 常见误区

### ❌ "Buffer 不会保存，所以不用管"
**错！** Buffer 会被 `state_dict()` 保存，只是不会被优化器更新。

### ❌ "直接赋值更简单，为什么不用？"
**问题：**
- 保存模型时会丢失
- `.cuda()` 时不会跟着移动
- 可能导致设备不一致的错误

### ❌ "Buffer 的 requires_grad 可以改成 True"
**可以但不推荐：**
```python
self.register_buffer('x', tensor, persistent=True)
self.x.requires_grad_(True)  # 可以，但奇怪
```
如果需要梯度，直接用 `nn.Parameter`。

### ❌ "所有固定值都用 Buffer"
**不一定：**
- 如果只在 forward 中临时使用 → 局部变量即可
- 如果需要保存/跨设备 → 用 Buffer
- 如果每个样本不同 → 作为输入传入

---

## 选择指南

```
需要这个张量吗？
│
├─ 不需要保存，只在 forward 中临时用
│  └─→ 局部变量（不要存为 self.xxx）
│
├─ 需要保存
│   │
│   ├─ 需要梯度更新吗？
│   │   │
│   │   ├─ 是 → nn.Parameter
│   │   │       (权重、偏置、γ、β等)
│   │   │
│   │   └─ 否 → register_buffer
│   │           (统计量、掩码、位置编码等)
│   │
│   └─ 不需要保存 → 局部变量
```

---

## 与 LayerNorm 的联系

在 LayerNorm 中：
```python
class LayerNorm(nn.Module):
    def __init__(self, dim):
        super().__init__()
        # 可学习的缩放和平移
        self.gamma = nn.Parameter(torch.ones(dim))   # ← 会被更新
        self.beta = nn.Parameter(torch.zeros(dim))   # ← 会被更新
        
        # 如果用 buffer（错误示范）
        # self.gamma = torch.ones(dim)  # ❌ 不会更新！
    
    def forward(self, x):
        mean = x.mean(dim=-1, keepdim=True)
        var = x.var(dim=-1, keepdim=True)
        x_normed = (x - mean) / torch.sqrt(var + 1e-5)
        return self.gamma * x_normed + self.beta  # γ, β 在这里起作用
```

**如果用直接赋值而不是 nn.Parameter**：
- 优化器不会更新 γ, β
- LayerNorm 失去"反悔权"
- 模型性能下降

---

## 总结

| 问题 | 答案 |
|------|------|
| 什么时候用 `nn.Parameter`？ | 需要训练更新的权重、偏置 |
| 什么时候用 `register_buffer`？ | 需要保存但不更新的常量 |
| 什么时候直接赋值？ | 临时变量，不需要保存 |
| Buffer 会出现在 state_dict 吗？ | ✅ 会 |
| Buffer 会被优化器更新吗？ | ❌ 不会 |
| Buffer 会跟着 `.cuda()` 移动吗？ | ✅ 会 |

**记住**：
- `named_parameters()` → 模型要**学**的东西
- `named_buffers()` → 模型要**记住**但不学的东西
- 直接赋值 → 用完就扔的临时工

---

**标签**: #PyTorch #深度学习 #参数管理 #nn.Parameter #register_buffer #模型训练

**创建日期**: 2026-03-23
**相关**: [[LayerNorm vs Softmax - 本质区别]] [[PyTorch 模型保存与加载]] [[BatchNorm 原理详解]]
