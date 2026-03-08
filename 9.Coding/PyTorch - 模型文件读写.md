# PyTorch - 模型文件读写

> 视频学习笔记：PyTorch 中 tensor 和神经网络模型的文件读写方法

---

## 📌 Tensor 的读写方法

### 单个 Tensor 的读写

```python
import torch

# 创建 tensor
x = torch.tensor([1.0, 2.0, 3.0, 4.0])

# 保存单个 tensor 到指定文件
torch.save(x, 'tensor.pt')

# 读取 tensor
loaded_x = torch.load('tensor.pt')

# 返回的仍是 tensor
print(type(loaded_x))  # <class 'torch.Tensor'>
print(loaded_x)        # tensor([1., 2., 3., 4.])
```

### 多个 Tensor 的批量存取

```python
# 存储包含多个 tensor 的 list
tensor_list = [torch.randn(3, 3), torch.randn(3, 3)]
torch.save(tensor_list, 'tensors_list.pt')

# 读取后还原为 list 结构
loaded_list = torch.load('tensors_list.pt')
print(len(loaded_list))  # 2

# 存储包含多个 tensor 的字典
tensor_dict = {
    'weight': torch.randn(10, 5),
    'bias': torch.randn(5),
    'data': torch.randn(100)
}
torch.save(tensor_dict, 'tensors_dict.pt')

# 读取后还原为字典结构
loaded_dict = torch.load('tensors_dict.pt')
print(loaded_dict.keys())  # dict_keys(['weight', 'bias', 'data'])
```

**特点**：
- ✅ 使用 `torch.save` 可将单个 tensor 存入指定文件
- ✅ 通过 `torch.load` 读取，返回的仍是 tensor
- ✅ 可存储包含多个 tensor 的 list 或字典
- ✅ 读取后会还原为对应的数据结构
- ✅ 能实现多 tensor 的批量存取

---

## 🔍 PyTorch 存储神经网络的特点

### 与 TensorFlow、MXNet 的差异

| 框架 | 存储方式 | 说明 |
|------|----------|------|
| TensorFlow | 整个模型 | 可存储模型定义 + 权重 |
| MXNet | 整个模型 | 可存储模型定义 + 权重 |
| **PyTorch** | **仅权重参数** | 因 imperative 模式，无法直接存储整个网络定义 |

### Imperative 模式的影响

- PyTorch 采用 **imperative（命令式）模式**
- 无法直接存储整个网络的模型定义
- **仅需存储网络的权重参数即可**

### TorchScript（扩展了解）

```python
# TorchScript 可实现模型整体存储（本视频不做详细介绍）
scripted_model = torch.jit.script(model)
scripted_model.save('model_scripted.pt')

# 加载
loaded_model = torch.jit.load('model_scripted.pt')
```

---

## 💾 神经网络权重参数的存储

### 使用 state_dict 保存权重

```python
import torch
import torch.nn as nn

# 定义 MLP 神经网络
class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(128, 64)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 10)
    
    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.relu(x)
        return self.fc3(x)

# 实例化网络
model = MLP()

# 通过 model.state_dict() 获取所有参数的映射字典
# 参数名对应参数值（OrderedDict 类型）
state_dict = model.state_dict()

# 查看参数字典结构
print(state_dict.keys())
# dict_keys(['fc1.weight', 'fc1.bias', 'fc2.weight', 'fc2.bias', ...])

# 使用 torch.save 将该字典存入文件
torch.save(state_dict, 'mlp_weights.pt')
```

**关键点**：
- ✅ `state_dict()` 返回参数字典（参数名 → 参数值）
- ✅ 类型为 `OrderedDict`
- ✅ 只保存权重参数，不保存网络结构定义

---

## 📥 神经网络权重参数的读取与验证

### 读取并加载参数

```python
# 1. 重新定义相同结构的 MLP 网络
new_model = MLP()

# 2. 通过 torch.load 读取存储的参数字典
loaded_state_dict = torch.load('mlp_weights.pt')

# 3. 调用 load_state_dict() 将字典参数覆盖网络随机初始化的参数
new_model.load_state_dict(loaded_state_dict)

# 4. 设置为评估模式（如果需要）
new_model.eval()
```

### 验证参数加载成功

```python
# 创建相同的随机输入
torch.manual_seed(42)
test_input = torch.randn(1, 128)

# 原网络的输出（假设已保存前的状态）
# original_output = model(test_input)

# 加载参数后的新网络输出
with torch.no_grad():
    loaded_output = new_model(test_input)

# 对比输出结果
# 如果结果一致，说明参数读取和加载成功
print(loaded_output)
```

**验证逻辑**：
- ✅ 将相同的随机输入传入原网络和加载参数后的新网络
- ✅ 对比输出结果
- ✅ 结果一致即说明参数读取和加载成功

---

## 🔄 完整的保存与加载流程

### 保存模型

```python
def save_model(model, path):
    """保存模型权重"""
    torch.save(model.state_dict(), path)
    print(f"模型已保存到 {path}")

# 使用
save_model(model, 'checkpoints/mlp_best.pt')
```

### 加载模型

```python
def load_model(model_class, path):
    """加载模型权重"""
    # 1. 实例化相同结构的网络
    model = model_class()
    
    # 2. 加载参数字典
    state_dict = torch.load(path)
    
    # 3. 应用参数
    model.load_state_dict(state_dict)
    
    # 4. 设置为评估模式
    model.eval()
    
    print(f"模型已从 {path} 加载")
    return model

# 使用
loaded_model = load_model(MLP, 'checkpoints/mlp_best.pt')
```

### 训练 checkpoint 的保存与恢复

```python
# 保存训练 checkpoint
checkpoint = {
    'epoch': epoch,
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'loss': loss,
}
torch.save(checkpoint, 'checkpoint.pt')

# 恢复训练
checkpoint = torch.load('checkpoint.pt')
model.load_state_dict(checkpoint['model_state_dict'])
optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
start_epoch = checkpoint['epoch']
```

---

## 📝 核心逻辑总结

### PyTorch 文件读写核心逻辑

| 对象类型 | 保存方法 | 加载方法 |
|----------|----------|----------|
| **单个 Tensor** | `torch.save(tensor, path)` | `tensor = torch.load(path)` |
| **多个 Tensor** | `torch.save([t1, t2], path)` | `list = torch.load(path)` |
| **Tensor 字典** | `torch.save({'w': w, 'b': b}, path)` | `dict = torch.load(path)` |
| **神经网络** | `torch.save(model.state_dict(), path)` | `model.load_state_dict(torch.load(path))` |

### 神经网络存取流程

```
保存流程：
定义网络 → 训练/初始化 → model.state_dict() → torch.save()

加载流程：
重新定义相同网络 → torch.load() → model.load_state_dict() → eval()
```

### 关键要点

- ✅ 通过 `torch.save` 和 `torch.load` 可实现 tensor 的直接读写
- ✅ 针对神经网络，核心是借助 `state_dict` 获取参数、保存参数
- ✅ 读取后再将参数覆盖新网络的初始化参数
- ✅ 完成模型的整体存取
- ⚠️ 必须保证加载时的网络结构与保存时完全一致

---

## 🔖 标签

#PyTorch #深度学习 #模型保存 #state_dict #文件读写
