# TurboQuant 实际实现详解

> **目的：** 纠正科普视频中的简化理解，基于 turboquant_plus 源码解析真实实现
> **前置知识：** [[Turbo Quant 详解]]（科普版）、[[KV Cache 详解 - 李宏毅]]
> **创建日期：** 2026-04-02

---

## 0. 科普 vs 实际：关键纠正

| 科普视频的说法 | 实际情况 | 影响 |
|---------------|---------|------|
| "零精度损失" | turbo4: +0.23% PPL, turbo3: +1.06%, turbo2: +6.48% | 有损失，只是很小 |
| "极坐标量化" | Norm 提取 + **WHT 随机旋转** + 标量量化 | 不是几何极坐标 |
| "QJL 消除误差" | **QJL 已被废弃**，反而增加方差伤害质量 | 纯 PolarQuant 更好 |
| "8x 速度提升" | Decode 速度 0.78-0.93x（比 q8_0 慢），Prefill ≈ 1.0x | 速度换空间 |
| "6x 内存减少" | 实际压缩比 3.8x-6.4x（取决于 bit-width） | 基本准确 |

**核心修正：TurboQuant 是一个有损压缩算法，但损失极小（1-6% PPL），换取 3.8-6.4x 的内存压缩。**

---

## 1. 实际压缩管线

```
输入：KV cache 向量 x ∈ R^d（一个 attention head 的 K 或 V 向量）

Step 1: 提取 Norm（幅度）
    γ = ||x||₂          ← 存储为元数据
    x̂ = x / γ           ← 归一化到单位球面

Step 2: 随机旋转（WHT + 随机符号翻转）
    y = WHT(sign_flip(x̂))
    旋转后：每个坐标 ≈ N(0, 1/d)  ← 近似独立同分布高斯！

Step 3: 标量量化（PolarQuant）
    对 y 的每个坐标独立量化：
    turbo4: 16 个质心（4-bit），idx = argmin |y[j] - centroid[k]|
    turbo3: 8 个质心（3-bit）
    turbo2: 4 个质心（2-bit）

输出：量化索引 + Norm → 紧凑存储
```

### 为什么这个管线有效？

**关键 insight：高维向量经过随机旋转后，坐标分布变成近似高斯。**

```
原始 KV 向量：
  - 坐标分布不规则，有离群值
  - kurtosis（峰度）≈ 900  ← 分布非常尖

旋转后：
  - 坐标近似 N(0, 1/√d)
  - kurtosis ≈ 2.9  ← 接近高斯的 3.0
  - 每个坐标近似独立
```

一旦分布变成高斯，就可以用 **Lloyd-Max 最优量化器**（针对高斯分布的最优标量量化）来高效压缩。这比直接量化原始向量的效果好得多。

---

## 2. 解压缩管线

```
输入：量化索引 idx + Norm γ

Step 1: 查表还原
    ŷ[j] = centroid[idx[j]]    ← 每个坐标查码本

Step 2: 逆旋转
    x̂_hat = WHT_inverse(sign_flip_inverse(ŷ))

Step 3: 恢复缩放
    x_hat = γ × x̂_hat

输出：近似还原的 KV 向量 x_hat
```

旋转的一个重要性质：**WHT 是自逆的**（H^T = H），所以旋转和逆旋转用同一个操作。

---

## 3. 为什么 QJL 被废弃？

论文原始设计：PolarQuant (b-1 bits) + QJL (1 bit) = TurboQuant (b bits)

QJL 的作用是用 1-bit 符号量化来校正 PolarQuant 的残差。

**实际发现（5 个独立团队确认）：**
- QJL 增加了方差
- Softmax 会放大这个方差（指数函数的性质）
- 结果：attention 质量反而下降
- **更好的方案：直接给 PolarQuant 多一个 bit（多一倍质心数量）**

```
论文方案：  turbo4 = PolarQuant 3-bit + QJL 1-bit → 效果差
实际方案：  turbo4 = PolarQuant 4-bit（16 个质心） → 效果好

代码证据：qjl.py 仍保留在 repo 中但标注为 "kept for reference, not used in production"
```

---

## 4. 三种压缩格式

| 格式 | Bits/值 | 质心数 | 压缩比 | PPL 劣化 | 适用场景 |
|------|---------|--------|--------|----------|---------|
| turbo4 | 4.25 | 16 | 3.8x | +0.23% | 最佳质量，通用 |
| turbo3 | 3.5 | 8 | 4.6x | +1.06% | 最大压缩 |
| turbo2 | 2.5 | 4 | 6.4x | +6.48% | 极端内存压力 |

### 为什么不是整数 bits？

实际存储包含元数据开销：
- 每个 block（32 个值）需要存储一个 Norm（float16 = 16 bits）
- 平均到每个值：16/32 = 0.5 extra bits
- turbo4：4 bits (索引) + 0.25 bits (Norm 均摊) = 4.25 bits/值

---

## 5. 三个关键发现（独立验证）

### 5.1 V 压缩"免费"

压缩 Value cache（即使到 2-bit）对 attention 质量几乎零影响，因为 V 不参与 softmax routing。

```
K = q8_0, V = turbo4 → PPL 变化极小
K = q8_0, V = turbo2 → PPL 仍然可控
```

### 5.2 质量退化全部来自 K 压缩

Key 决定了 softmax 的 attention routing（哪些 token 获得多少权重）。K 精度降低会导致 routing 错误。

```
对于 Q4_K_M 低精度权重模型：
K = turbo3, V = turbo3 → PPL 3556（灾难性）
K = q8_0,  V = turbo3 → PPL 6.71（+2.0%，可接受）
```

**因此推荐非对称配置：K 保持高精度，V 激进压缩。**

### 5.3 边界层特别敏感

Transformer 的第 1-2 层和最后 1-2 层对量化最敏感。只保护这 4 层用 q8_0-V，其余用 turbo2-V，就能恢复 37-91% 的质量差距。

---

## 6. 与其他 KV Cache 优化方法的关系

```
                     改变模型？   需要训练？   压缩类型
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GQA/MQA              是          是         结构压缩（减少 K/V 组数）
MLA (DeepSeek)       是          是         维度压缩（Bottleneck）
KV Cache Pruning     是          否         丢弃不重要的 token
Sliding Window       是          可选       限制 attention 范围
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TurboQuant           否          否         数值压缩（量化每个值的精度）
q8_0/q4_0            否          否         数值压缩（简单量化）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**TurboQuant 的独特优势：**
- 不改变模型架构
- 不需要重新训练
- 与 GQA 等方法正交（可以叠加使用）
- 比 q4_0 质量好（同 4-bit 下，turbo4 的 PPL +0.23% vs q4_0 的 +0.52%）

---

## 7. 代码结构与实际对应

```python
# polar_quant.py — Step 1-3 的实现
class PolarQuant:
    def quantize(self, x):
        norm = np.linalg.norm(x)          # Step 1: 提取 Norm
        x_normalized = x / norm
        rotated = self.rotation @ x_normalized  # Step 2: 旋转
        indices = self.codebook.quantize(rotated) # Step 3: 量化
        return indices, norm

    def dequantize(self, indices, norm):
        values = self.codebook.dequantize(indices)  # 查表
        unrotated = self.rotation.T @ values          # 逆旋转
        return norm * unrotated                       # 恢复缩放

# codebook.py — Lloyd-Max 最优质心
class Codebook:
    def __init__(self, bit_width, d):
        # 针对 N(0, 1/√d) 分布计算最优质心
        self.centroids = lloyd_max(n_centroids=2**bit_width, ...)

# rotation.py — WHT 随机旋转
def hadamard_rotation(x, signs):
    return hadamard_transform(x * signs)  # 符号翻转 + Hadamard
```

---

## 相关笔记

- [[Turbo Quant 详解]] — 科普版（注意已纠正的误解）
- [[Walsh-Hadamard 变换（WHT）入门]] — 核心旋转操作
- [[Lloyd-Max 最优量化原理]] — 码本构建
- [[Perplexity 与模型质量评估]] — 质量指标
- [[GPU 内存带宽与推理加速原理]] — 为什么压缩能加速

---

*基于 turboquant_plus 源码（https://github.com/TheTom/turboquant_plus）分析，非科普级别理解。*
