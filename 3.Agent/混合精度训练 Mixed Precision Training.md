# 混合精度训练 Mixed Precision Training

## 核心思想

同时使用 **FP16**（半精度）和 **FP32**（单精度）进行训练：

| 精度       | 位数  | 数值范围          | 用途                                                            |
| -------- | --- | ------------- | ------------------------------------------------------------- |
| **FP32** | 32位 | ~1e-38 到 1e38 | <span style="color:rgb(255, 77, 77)">权重更新、损失计算（保证精度）</span>   |
| **FP16** | 16位 | ~6e-5 到 65504 | <span style="color:rgb(255, 77, 77)">前向/反向传播（加速计算、省显存）</span> |

---

## 为什么用混合精度？

### 1. 速度更快
- FP16 计算<span style="color:rgb(255, 77, 77)">吞吐量更高</span>（Tensor Core 优化）
- 矩阵运算速度可提升 <span style="color:rgb(255, 77, 77)"><b>2-8 倍</b></span>

### 2. 显存更省
- 模型参数占用减半
- 激活值占用减半
- 同样显存可以训练更大模型或使用更大 batch size

### 3. Batch Size 更大
- 显存节省 → batch size 翻倍 → 训练更稳定

---

## 核心问题：<span style="color:rgb(255, 77, 77)">梯度下溢（Gradient Underflow）</span>

FP16 的数值范围很小（~6e-5 到 65504），反向传播时梯度可能<span style="color:rgb(255, 77, 77)"><b>下溢为 0</b></span>：

```
真实梯度: 1e-20
FP16 最小值: 6e-5
结果: 0 (下溢！)
```

<span style="color:rgb(255, 77, 77)">梯度为 0 → 权重不更新 → 模型停止学习</span>

---

## 解决方案：<span style="color:rgb(255, 77, 77)">梯度缩放（Gradient Scaling）</span>

### 核心思想

<span style="color:rgb(255, 77, 77)"><b>放大损失 → 放大梯度 → 避免下溢 → 更新后恢复</b></span>

1. 前向传播 (FP16)     → 速度快
2. 计算损失 (FP16)     
3. <span style="color:rgb(255, 77, 77)">缩放损失 </span>× 65536    → 防止下溢
4. 反向传播 (FP16)     → <span style="color:rgb(255, 77, 77)">梯度也被放大</span>
5. 更新权重 (FP32)     → 转回 FP32 保证精度
6. <span style="color:rgb(255, 77, 77)">缩放因子自动调整</span> → 动态平衡防止上溢

---

## PyTorch 实现

```python
from torch.cuda.amp import autocast, GradScaler

# 创建梯度缩放器
scaler = GradScaler()

for data, target in dataloader:
    optimizer.zero_grad()
    
    # 自动 FP16 转换上下文
    with autocast():
        output = model(data)
        loss = criterion(output, target)
    
    # 缩放损失并反向传播
    scaler.scale(loss).backward()
    
    # 缩放后的梯度更新权重
    scaler.step(optimizer)
    
    # 更新缩放因子（自动调整）
    scaler.update()
```

---

## 关键组件解析

### 1. `autocast()` 上下文管理器

<span style="color:rgb(255, 77, 77)">自动决定哪些操作使用 FP16，哪些使用 FP32</span>：

```python
with autocast():
    # FP16: 矩阵乘法、卷积（有 Tensor Core 加速）
    output = model(data)
    
    # FP32: Softmax、Loss（需要精度）
    loss = criterion(output, target)
```

### 2. `GradScaler` <span style="color:rgb(255, 77, 77)">梯度缩放器</span>

```python
scaler = GradScaler()

# 缩放损失（乘大数）
scaled_loss = loss * 65536.0

# 反向传播（梯度也被放大）
scaled_loss.backward()

# 更新权重（自动缩放回正常范围）
scaler.step(optimizer)
```

### 3. <span style="color:rgb(255, 77, 77)">自动缩放调整</span>

- 如果<span style="color:rgb(255, 77, 77)">梯度正常</span> → <span style="color:rgb(255, 77, 77)">保持或增大缩放因子</span>
- 如果<span style="color:rgb(255, 77, 77)">梯度溢出（Inf/NaN）</span>→ <span style="color:rgb(255, 77, 77)">跳过更新，减小缩放因子</span>

---

## 工作流程图解

```
┌─────────────────────────────────────────────────┐
│                   训练循环                        │
└─────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────┐
│  1. 前向传播 (FP16)                              │
│     model(data) → output                        │
│     【Tensor Core 加速】                         │
└─────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────┐
│  2. 计算损失 (FP16/FP32)                         │
│     loss = criterion(output, target)            │
└─────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────┐
│  3. 缩放损失                                     │
│     scaled_loss = loss × scale_factor           │
│     【防止梯度下溢】                              │
└─────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────┐
│  4. 反向传播 (FP16)                              │
│     scaled_loss.backward()                      │
│     【梯度也被放大】                              │
└─────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────┐
│  5. 更新权重 (FP32)                              │
│     scaler.step(optimizer)                      │
│     【转回 FP32 保证精度】                        │
└─────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────┐
│  6. 调整缩放因子                                 │
│     scaler.update()                             │
│     【自动适应训练动态】                           │
└─────────────────────────────────────────────────┘
```

---

## 精度对比

| 训练方式     | 显存占用                                             | 速度                                               | 精度损失                                                      |
| -------- | ------------------------------------------------ | ------------------------------------------------ | --------------------------------------------------------- |
| **FP32** | 100%                                             | 1x                                               | <span style="color:rgb(255, 77, 77)">0% (baseline)</span> |
| **FP16** | 50%                                              | <span style="color:rgb(255, 77, 77)">2-8x</span> | 可能较大                                                      |
| **混合精度** | <span style="color:rgb(255, 77, 77)">~60%</span> | <span style="color:rgb(255, 77, 77)">2-6x</span> | <span style="color:rgb(255, 77, 77)"><1%</span>           |

---

## 上溢 vs 下溢

| 类型               | 问题   | 数值范围    | 现象           | 解决方案                                                                  |
| ---------------- | ---- | ------- | ------------ | --------------------------------------------------------------------- |
| **下溢 Underflow** | 数值太小 | < 6e-5  | 梯度变成 0       | **缩放因子存在的原因**（<span style="color:rgb(255, 77, 77)">放大 65536 倍</span>） |
| **上溢 Overflow**  | 数值太大 | > 65504 | 梯度变成 Inf/NaN | **动态调整缩放因子**（减小）                                                      |

### <span style="color:rgb(255, 77, 77)">动态调整机制</span>

GradScaler 自动寻找 "最大安全缩放因子"：

```python
# 初始化
scaler = GradScaler(init_scale=65536.0)

# 每次迭代：
if 梯度正常（无 Inf/NaN）:
    正常更新权重
    尝试增大缩放因子（×2）→ 提高精度
else:
    跳过本次更新（不执行 optimizer.step）
    减小缩放因子（÷2）→ 防止上溢
```

### 为什么正常时还要尝试增大？

**目标**：<span style="color:rgb(255, 77, 77)"><b>找到刚好不溢出的最大因子</b></span>

- <span style="color:rgb(255, 77, 77)"><b>缩放因子越大 → 梯度数值越大 → FP16 精度越高</b></span>
- 但太大 → 上溢为 Inf
- 所以 GradScaler <span style="color:rgb(255, 77, 77)"><b>试探性增大</b></span>，直到临界点

### 溢出后的处理

```python
# 第 N 次迭代：缩放因子 = 65536，梯度上溢为 Inf
scaler.step(optimizer)  # 检测到 Inf，跳过更新
scaler.update()         # 缩放因子减半 = 32768

# 第 N+1 次迭代：缩放因子 = 32768，梯度正常
scaler.step(optimizer)  # 正常更新
scaler.update()         # 尝试恢复 = 65536（或保持）
```

**关键**：<span style="color:rgb(255, 77, 77)"><b>溢出那次权重不更新，但模型不崩</b></span>，下次继续。

---

## 一句话总结

> **下溢是"病"，缩放是"药"，上溢是"药过量"，动态调整是"精准用药"。**

> **FP16 计算 + FP32 更新 + 梯度缩放 = 又快又稳**

---

## 参考资料

- PyTorch AMP Documentation: https://pytorch.org/docs/stable/amp.html
- NVIDIA Mixed Precision Training: https://docs.nvidia.com/deeplearning/performance/mixed-precision-training/
- Paper: Mixed Precision Training (Micikevicius et al., 2018)

---

## 相关笔记

- [[CUDA 优化]]
- [[Transformer 训练技巧]]
- [[显存优化策略]]
