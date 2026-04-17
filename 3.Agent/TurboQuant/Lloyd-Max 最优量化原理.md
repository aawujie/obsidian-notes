# Lloyd-Max 最优量化原理

> **目的：** 理解 TurboQuant 如何选择最优的量化质心（codebook）
> **前置知识：** 基础概率论（均值、方差、正态分布）
> **创建日期：** 2026-04-02

---

## 1. 量化是什么？

量化 = **用有限的几个代表值来近似连续数据。**

最简单的例子：把考试成绩（0-100）转成等级（A/B/C/D/F）。

```
原始：97, 85, 73, 42, 15
量化：A,  B,  C,  D,  F
还原：95, 85, 75, 55, 25  ← 不精确，但只需要存 5 个值而不是 100 个

这里 [95, 85, 75, 55, 25] 就是"质心"（centroids / reconstruction levels）
```

---

## 2. 标量量化 vs 向量量化

| 类型 | 描述 | TurboQuant 用哪个？ |
|------|------|---------------------|
| **标量量化** | 每个数独立量化 | ✅ 用这个 |
| **向量量化** | 整个向量一起量化 | ❌ 计算量太大 |

TurboQuant 的巧妙之处：**通过 WHT 旋转，让向量的每个坐标变成独立同分布，从而用简单的标量量化达到接近向量量化的效果。**

---

## 3. 均匀量化 vs 最优量化

### 3.1 均匀量化（Uniform Quantization）

等间距划分。例如 4-bit（16 个值）量化 [-1, 1]：

```
质心: -0.9375, -0.8125, -0.6875, ..., 0.9375
间距: 均匀的 0.125
```

**问题：** 如果数据集中在中间（高斯分布），边缘的质心浪费了。

### 3.2 Lloyd-Max 最优量化

**核心思想：** 让质心的位置匹配数据的实际分布。数据密集的区域放更多质心，稀疏区域放更少。

```
均匀量化（高斯数据）：
  |  *  |  *  |  **  |****|****|  **  |  *  |  *  |
  ← 边缘质心利用率低 →     ← 中间拥挤 →

Lloyd-Max 量化（高斯数据）：
  |    *    |  **  |****|****|  **  |    *    |
  ← 边缘区间大 →   ← 中间区间密 →
  MSE 更低！
```

---

## 4. Lloyd-Max 算法

这是一个迭代算法，交替优化两个步骤：

### Step 1: 固定质心，更新分区边界

每个数据点归属到最近的质心：

$$b_k = \frac{c_k + c_{k+1}}{2}$$

（边界是相邻质心的中点）

### Step 2: 固定分区，更新质心

每个质心移到其分区内数据的**条件均值**：

$$c_k = \frac{\int_{b_{k-1}}^{b_k} x \cdot f(x) \, dx}{\int_{b_{k-1}}^{b_k} f(x) \, dx}$$

（$f(x)$ 是数据的概率密度函数）

### 迭代直到收敛

```
初始化：均匀放置 2^b 个质心
重复：
  1. 计算边界（相邻质心中点）
  2. 更新质心（每个区间的条件均值）
  直到质心不再变化
```

**对高斯分布，收敛后的质心位置有已知的最优解。**

---

## 5. TurboQuant 的码本

经过 WHT 旋转后，KV 向量的每个坐标 $\sim N(0, 1/\sqrt{d})$。

TurboQuant 预计算针对这个分布的最优质心：

### 各 bit-width 的质心（高维近似）

**1-bit（2 个质心）— turbo2 的基础：**

$$c = \pm\sqrt{\frac{2}{\pi d}}$$

**2-bit（4 个质心）：**

$$c = \frac{1}{\sqrt{d}} \times \{-1.51, -0.453, +0.453, +1.51\}$$

**3-bit（8 个质心）和 4-bit（16 个质心）：**
用 Lloyd-Max 算法迭代计算，没有简洁的闭合形式。

### 代码实现

```python
# codebook.py（简化）
class Codebook:
    def __init__(self, bit_width, d):
        n_centroids = 2 ** bit_width

        if bit_width == 1:
            # 闭合形式
            c = np.sqrt(2 / (np.pi * d))
            self.centroids = np.array([-c, c])
        elif bit_width == 2:
            # 闭合形式
            self.centroids = np.array([-1.51, -0.453, 0.453, 1.51]) / np.sqrt(d)
        else:
            # Lloyd-Max 迭代
            self.centroids = lloyd_max_iteration(
                pdf=gaussian(0, 1/np.sqrt(d)),
                n_centroids=n_centroids
            )

    def quantize(self, values):
        """每个值找最近的质心，返回索引"""
        distances = np.abs(values[:, None] - self.centroids[None, :])
        return np.argmin(distances, axis=1)

    def dequantize(self, indices):
        """索引查表还原"""
        return self.centroids[indices]
```

---

## 6. 为什么 Lloyd-Max 对 TurboQuant 重要？

### 量化误差对比

假设数据 $\sim N(0, \sigma^2)$，4 个质心（2-bit）：

| 方法 | MSE | 与理论最优的差距 |
|------|-----|-----------------|
| 均匀量化 | 0.148 | 基线 |
| Lloyd-Max | **0.117** | **降低 21%** |

在 3-bit 和 4-bit 上差距更大。这个改进直接反映在 PPL 质量上。

### 失真率理论（Rate-Distortion）

信息论给出了量化的**理论下界**：

$$D(R) = \sigma^2 \cdot 2^{-2R}$$

其中 $R$ 是每个值的 bits，$D$ 是 MSE。

| Bits | 理论最低 MSE | Lloyd-Max MSE | 效率 |
|------|-------------|--------------|------|
| 2 | 0.063 | 0.117 | 54% |
| 3 | 0.016 | 0.030 | 53% |
| 4 | 0.004 | 0.009 | 44% |

Lloyd-Max 接近理论最优（50%+ 效率），而均匀量化效率更低。

---

## 7. 量化全流程串联

把 WHT 和 Lloyd-Max 串联起来理解整个过程：

```
原始 KV 向量 x ∈ R^128
  ↓
坐标分布不规则（kurtosis 900）
  ↓ WHT 随机旋转
坐标分布变成 N(0, 1/√128)（kurtosis 3.0）
  ↓ Lloyd-Max 量化
每个坐标用 3-bit 索引表示（8 个最优质心）
  ↓
MSE 仅 0.03（占原始能量的 3%）

128 维 × fp16 = 256 bytes → 128 × 3 bits = 48 bytes + 2 bytes Norm = 50 bytes
压缩比 ≈ 5.1x
```

---

## 关键要点总结

1. Lloyd-Max 量化根据数据分布放置质心，比均匀量化 MSE 低 20%+
2. 对高斯分布有已知的最优解（低 bit-width 有闭合形式）
3. TurboQuant 先用 WHT 把分布变成高斯，再用 Lloyd-Max 量化——两步配合才有效
4. 质心只依赖维度 $d$ 和 bit-width，可以预计算一次反复使用

---

## 相关笔记

- [[Walsh-Hadamard 变换（WHT）入门]] — 前一步：把分布变成高斯
- [[TurboQuant 实际实现详解]] — 完整管线
- [[Perplexity 与模型质量评估]] — 量化质量的衡量

---

*Lloyd-Max 的本质：把有限的"墨水"涂在最需要精度的地方。*
