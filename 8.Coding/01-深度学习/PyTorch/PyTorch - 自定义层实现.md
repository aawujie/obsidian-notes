# PyTorch - 自定义层实现

> 视频学习笔记：PyTorch 中自定义层的构建方法，包括无参数和带参数自定义层

---

## 📌 核心概念

### 自定义层与自定义网络的本质关联

- **本质相同**：自定义层和自定义神经网络无本质区别
- **继承关系**：均是 `nn.Module` 的子类
- **实现语言**：建议使用 Python 3 进行实现

```python
import torch
import torch.nn as nn

class CustomLayer(nn.Module):
    def __init__(self):
        super().__init__()
        # 初始化逻辑
    
    def forward(self, x):
        # 前向传播逻辑
        return x
```

---

## 🔷 无参数自定义层的实现

### 示例：Center Layer（中心化层）

以 `center layer` 为例，实现输入减去自身均值的逻辑：

```python
class CenteredLayer(nn.Module):
    def __init__(self):
        super().__init__()
        # 无需在 __init__ 函数做额外操作
    
    def forward(self, x):
        # 实现输入减去自身均值的逻辑
        return x - x.mean()
```

### 使用与验证

```python
# 实例化
layer = CenteredLayer()

# 传入 tensor
x = torch.tensor([1.0, 2.0, 3.0, 4.0, 5.0])
output = layer(x)

# 验证：输出均值趋近于 0（存在浮点计算误差）
print(output.mean())  # tensor(0.)
```

**特点**：
- ✅ 无需在 `__init__` 函数做额外操作
- ✅ 仅需定义 `forward` 函数实现逻辑
- ✅ 实例化后传入 tensor 可使输入均值趋近于 0
- ✅ 存在浮点计算误差（正常现象）
- ✅ 该层可融入复杂网络

---

## 🔶 带参数自定义层的实现核心

### nn.Parameter 类的作用

带参数的自定义层需将参数封装为 `nn.Parameter` 类的实例：

```python
class CustomLayerWithParams(nn.Module):
    def __init__(self):
        super().__init__()
        # 将参数封装为 nn.Parameter
        self.weight = nn.Parameter(torch.randn(10, 10))
```

### nn.Parameter 的特性

| 特性 | 说明 |
|------|------|
| 自动添加梯度 | 参数会自动注册到模型的梯度计算图中 |
| 合适名称 | 自动设置参数名称（如 `weight`, `bias`） |
| requires_grad | 默认设为 `true`，支持参数更新 |

```python
# 验证
param = nn.Parameter(torch.randn(5, 5))
print(param.requires_grad)  # True
```

---

## 📐 自定义线性层的实现步骤

### 完整实现示例

```python
class MyLinear(nn.Module):
    def __init__(self, in_features, out_features):
        super().__init__()
        # 初始化输入、输出维度
        self.in_features = in_features
        self.out_features = out_features
        
        # 构建权重（输入×输出维度矩阵）
        # 正一负一均匀分布初始化
        self.weight = nn.Parameter(torch.Tensor(in_features, out_features))
        nn.init.uniform_(self.weight, -1, 1)
        
        # 构建偏置（可随机或置零）
        self.bias = nn.Parameter(torch.Tensor(out_features))
        nn.init.zeros_(self.bias)  # 或随机初始化
    
    def forward(self, x):
        # 通过 .data 访问参数
        # 完成矩阵乘法、加偏置操作
        output = torch.matmul(x, self.weight.data) + self.bias.data
        
        # 还可直接加入 ReLU 激活函数
        output = torch.relu(output)
        
        return output
```

### 关键点

1. **`__init__` 中**：
   - 初始化输入、输出维度
   - 构建权重矩阵（输入×输出维度）
   - 使用正一负一均匀分布初始化
   - 构建偏置（可随机或置零）
   - 用 `nn.Parameter` 包裹参数

2. **`forward` 中**：
   - 通过 `.data` 访问参数
   - 完成矩阵乘法操作
   - 加上偏置
   - 可选择性加入激活函数（如 ReLU）

---

## 🔗 自定义层的通用使用方式

### 方式一：单独使用

```python
# 自定义层单独实例化
layer = MyLinear(128, 64)

# 传入数据得到结果
x = torch.randn(32, 128)
output = layer(x)
print(output.shape)  # torch.Size([32, 64])
```

### 方式二：融入 Sequential

```python
# 将自定义层实例放入 Sequential
model = nn.Sequential(
    MyLinear(128, 64),
    nn.ReLU(),
    MyLinear(64, 32),
    nn.Softmax(dim=1)
)

# 参与复杂网络的构造
output = model(x)
```

### 方式三：嵌套在其他模块中

```python
class ComplexNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.custom_layer1 = MyLinear(128, 64)
        self.custom_layer2 = MyLinear(64, 32)
        self.fc = nn.Linear(32, 10)
    
    def forward(self, x):
        x = self.custom_layer1(x)
        x = self.custom_layer2(x)
        return self.fc(x)
```

**特点**：
- ✅ 自定义层可单独实例化传入数据得到结果
- ✅ 可放入 Sequential 中参与复杂网络构造
- ✅ 使用方式与 PyTorch 内置层无差异

---

## 📝 核心实现总结

### 自定义层的关键要点

| 要点 | 说明 |
|------|------|
| 继承 | 必须继承 `nn.Module` |
| 无参数层 | 仅需实现 `forward` 逻辑 |
| 带参数层 | 需将初始化的参数用 `nn.Parameter` 包裹 |
| 参数初始化 | 在 `__init__` 中完成 |
| 前向传播 | 在 `forward` 中定义计算逻辑 |

### 实现模板

```python
# 无参数自定义层模板
class NoParamLayer(nn.Module):
    def __init__(self):
        super().__init__()
    
    def forward(self, x):
        # 实现变换逻辑
        return x

# 带参数自定义层模板
class WithParamLayer(nn.Module):
    def __init__(self, in_features, out_features):
        super().__init__()
        self.weight = nn.Parameter(torch.Tensor(in_features, out_features))
        self.bias = nn.Parameter(torch.Tensor(out_features))
        # 初始化参数
        self._init_weights()
    
    def _init_weights(self):
        nn.init.xavier_uniform_(self.weight)
        nn.init.zeros_(self.bias)
    
    def forward(self, x):
        return torch.matmul(x, self.weight) + self.bias
```

---

## 🔖 标签

#PyTorch #深度学习 #自定义层 #神经网络 #nn.Module
