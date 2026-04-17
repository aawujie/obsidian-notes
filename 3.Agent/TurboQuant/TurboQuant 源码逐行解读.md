# TurboQuant 源码逐行解读

> **目的：** 逐文件、逐函数解读 turboquant_plus 核心源码，建立代码级理解
> **源码版本：** turboquant_plus main 分支（2026-04-02）
> **前置知识：** [[TurboQuant 实际实现详解]]、[[Walsh-Hadamard 变换（WHT）入门]]、[[Lloyd-Max 最优量化原理]]
> **创建日期：** 2026-04-02

---

## 0. 整体架构

```
turboquant/
├── __init__.py          ← 公开 API 导出
├── rotation.py          ← 第 1 步：随机旋转（WHT + 密集旋转）
├── codebook.py          ← 第 2 步：Lloyd-Max 码本构建
├── polar_quant.py       ← 第 3 步：PolarQuant 核心（组合旋转+量化）
├── qjl.py              ← [已废弃] QJL 1-bit 残差量化
├── turboquant.py        ← 完整管线（PolarQuant + QJL / MSE-only）
├── kv_cache.py          ← KV Cache 集成层（K 和 V 分别处理）
├── utils.py             ← Bit packing 工具
├── outlier.py           ← 离群通道策略（2.5-bit/3.5-bit）
└── hw_replay.py         ← 硬件诊断（与核心算法无关）
```

**调用关系（从上到下）：**

```
用户代码
  ↓
KVCacheCompressor (kv_cache.py)
  ├── K cache → TurboQuant (turboquant.py)
  │               ├── PolarQuant (polar_quant.py)
  │               │     ├── random_rotation_dense (rotation.py)
  │               │     └── optimal_centroids + nearest_centroid_indices (codebook.py)
  │               └── QJL (qjl.py) [废弃，但代码仍在]
  │
  └── V cache → TurboQuantMSE (turboquant.py)
                  └── PolarQuant (同上)
```

---

## 1. `rotation.py` — 随机旋转

### 1.1 密集随机旋转（精确，O(d²)）

```python
def random_rotation_dense(d, rng):
    G = rng.standard_normal((d, d))     # 生成 d×d 随机高斯矩阵
    Q, R = np.linalg.qr(G)             # QR 分解，Q 是正交矩阵
    signs = np.sign(np.diag(R))        # R 对角线的符号
    signs[signs == 0] = 1.0
    Q = Q * signs[np.newaxis, :]       # 修正 Q 使其 Haar 分布
    sign, _ = np.linalg.slogdet(Q)     # 检查行列式符号
    if sign < 0:
        Q[:, 0] = -Q[:, 0]            # 确保 det(Q) = +1（旋转，不是反射）
    return Q
```

**为什么不直接用 `np.linalg.qr(G)` 的 Q？**

QR 分解的 Q 不是均匀分布在所有正交矩阵上的（Haar 分布）。需要用 R 的对角线符号修正才能得到真正均匀的随机旋转矩阵。这是数值线性代数的经典技巧。

**使用场景：** Python 原型中使用。精确但 O(d²)，对于 d=128 的 head_dim 完全够用。

### 1.2 快速结构化旋转（近似，O(d log d)）

```python
def fast_walsh_hadamard_transform(x):
    n = len(x)
    x = x.copy().astype(np.float64)
    h = 1
    while h < n:                        # log₂(n) 轮
        for i in range(0, n, h * 2):    # 每轮 n/(2h) 组
            for j in range(i, i + h):   # 每组 h 对蝶形
                a, b = x[j], x[j + h]
                x[j] = a + b           # 蝶形加
                x[j + h] = a - b       # 蝶形减
        h *= 2
    return x / np.sqrt(n)              # 归一化
```

**蝶形运算可视化（d=8）：**
```
     轮1(h=1)     轮2(h=2)     轮3(h=4)
x[0] ─+─ = y[0]  ─+─ = z[0]  ─+─ = out[0]
x[1] ─-─ = y[1]  │         │  │         │
                  │         │  │         │
x[2] ─+─ = y[2]  ─-─ = z[2]  │         │
x[3] ─-─ = y[3]              │         │
                              │         │
x[4] ─+─ = y[4]  ─+─ = z[4]  ─-─ = out[4]
x[5] ─-─ = y[5]  │         │
                  │         │
x[6] ─+─ = y[6]  ─-─ = z[6]
x[7] ─-─ = y[7]
```

只有加减法，没有乘法。三轮搞定 8 个元素的变换。

**批量版本（`apply_fast_rotation_batch`）：** 用 reshape 技巧让 NumPy 向量化蝶形运算，避免 Python 循环。这是性能关键代码。

### 1.3 完整旋转流程

```python
def apply_fast_rotation(x, signs1, signs2, padded_d):
    d = len(x)
    padded = np.zeros(padded_d)
    padded[:d] = x              # Step 0: 补零到 2 的幂次
    padded *= signs1            # Step 1: 随机符号翻转
    padded = fwht(padded)       # Step 2: Hadamard 变换
    padded *= signs2            # Step 3: 第二次符号翻转
    return padded[:d]           # Step 4: 截断回原维度
```

**为什么两次符号翻转？** 一次不够随机。D₂ @ H @ D₁ 的组合提供足够的随机性，使旋转后的分布接近 Haar 分布。

---

## 2. `codebook.py` — 最优码本

### 2.1 质心计算

```python
def optimal_centroids(bit_width, d):
    n_centroids = 1 << bit_width    # 2^b 个质心

    if bit_width == 1:
        c = np.sqrt(2.0 / (np.pi * d))
        return np.array([-c, c])    # 闭合形式：±√(2/πd)

    if bit_width == 2:
        return np.array([-1.51, -0.453, 0.453, 1.51]) / np.sqrt(d)
        # 闭合形式：论文给出的最优值

    # 3-bit 及以上：Lloyd 迭代
    return _lloyds_gaussian(n_centroids, sigma=1.0 / np.sqrt(d))
```

**质心的缩放规律：** 所有质心都和 `1/√d` 成比例。这是因为旋转后坐标的标准差是 `1/√d`（高维单位球面的性质）。

### 2.2 Lloyd 迭代

```python
def _lloyds_gaussian(n_centroids, sigma, n_iter=100):
    # 初始化：用高斯分位数均匀放置边界
    boundaries = stats.norm.ppf(
        np.linspace(0, 1, n_centroids + 1)[1:-1], scale=sigma
    )

    for _ in range(n_iter):
        # Step 1: 边界 = 相邻质心的中点
        boundaries = (centroids[:-1] + centroids[1:]) / 2.0

        # Step 2: 质心 = 每个区间内数据的条件期望
        centroids[0] = E[X | X < boundaries[0]]
        centroids[i] = E[X | boundaries[i-1] < X < boundaries[i]]
        centroids[-1] = E[X | X > boundaries[-1]]

    return np.sort(centroids)
```

**条件期望公式（`_gaussian_conditional_expectation`）：**

$$E[X | a < X < b] = \sigma^2 \cdot \frac{\phi(a/\sigma) - \phi(b/\sigma)}{\Phi(b/\sigma) - \Phi(a/\sigma)}$$

- $\phi$: 标准正态 PDF
- $\Phi$: 标准正态 CDF

代码中处理了数值稳定性（极端值时用 `sf()` 代替 `1 - cdf()` 避免精度丢失）。

### 2.3 最近质心查找

```python
def nearest_centroid_indices(values, centroids):
    boundaries = (centroids[:-1] + centroids[1:]) / 2.0
    return np.searchsorted(boundaries, values.ravel()).reshape(values.shape)
```

**巧妙的实现：** 利用质心已排序的特性，用 `searchsorted`（二分查找 O(log k)）代替暴力搜索 O(k)。对每个值，找到它落在哪两个质心的中点之间，就知道最近的质心是哪个。

---

## 3. `polar_quant.py` — PolarQuant 核心

### 3.1 量化

```python
class PolarQuant:
    def __init__(self, d, bit_width, seed=42, norm_correction=True):
        self.rotation = random_rotation_dense(d, rng)  # d×d 旋转矩阵
        self.centroids = optimal_centroids(bit_width, d)  # 2^b 个质心

    def quantize(self, x):
        # 1. 提取 Norm
        norms = np.linalg.norm(x, axis=1)
        x_normalized = x / norms[:, np.newaxis]   # 归一化到单位球

        # 2. 旋转
        y = (self.rotation @ x_normalized.T).T    # 矩阵乘法

        # 3. 量化（最近质心）
        indices = nearest_centroid_indices(y, self.centroids)

        return indices, norms
```

**数据流：**
```
x = [0.5, -0.3, 0.8, ...]   (128 维，任意范数)
  ↓ 提取 norm = 1.2, 归一化
x̂ = [0.42, -0.25, 0.67, ...]  (128 维，单位范数)
  ↓ 旋转 (128×128 矩阵乘法)
y = [0.08, -0.09, 0.07, ...]   (128 维，近似 N(0, 1/√128))
  ↓ 量化 (每个坐标独立)
idx = [5, 2, 4, ...]           (128 个 3-bit 整数)
```

### 3.2 反量化

```python
    def dequantize(self, indices, norms):
        # 1. 查表
        y_hat = self.centroids[indices]     # 用索引查对应的质心值

        # 2. Norm correction（关键！）
        if self.norm_correction:
            y_hat_norms = np.linalg.norm(y_hat, axis=1, keepdims=True)
            y_hat = y_hat / y_hat_norms     # 重新归一化到单位范数

        # 3. 逆旋转
        x_hat_unit = (self.rotation.T @ y_hat.T).T  # rotation.T = rotation⁻¹

        # 4. 恢复原始缩放
        x_hat = x_hat_unit * norms[:, np.newaxis]

        return x_hat
```

**Norm correction 的作用：**
量化后的向量 `y_hat` 的范数不再精确等于 1（因为质心是离散的）。如果不修正，累积误差会让 PPL 变差。

```
没有 norm correction: PPL +2.2% (turbo3)
有 norm correction:   PPL +1.06% (turbo3)  ← 几乎减半！
```

这是从 @spiritbuun 的 CUDA 实现中移植过来的优化。仅仅一行代码的差别。

---

## 4. `turboquant.py` — 完整管线

### 4.1 TurboQuant（PolarQuant + QJL）

```python
class TurboQuant:
    def __init__(self, d, bit_width, seed=42):
        # PolarQuant 用 b-1 bits（留 1 bit 给 QJL）
        self.polar_quant = PolarQuant(d, bit_width=bit_width-1, seed=seed)
        self.qjl = QJL(d, seed=seed + 1000)

    def quantize(self, x):
        # Stage 1: PolarQuant
        indices, norms, residual = self.polar_quant.quantize_and_residual(x)
        # Stage 2: QJL on residual
        qjl_signs, residual_norms = self.qjl.quantize(residual)
        return CompressedVector(indices, norms, qjl_signs, residual_norms, ...)

    def dequantize(self, compressed):
        x_mse = self.polar_quant.dequantize(...)   # PolarQuant 还原
        x_qjl = self.qjl.dequantize(...)           # QJL 残差还原
        return x_mse + x_qjl                       # 两部分相加
```

> ⚠️ **注意：** 虽然代码中 TurboQuant 仍然包含 QJL，但实际 llama.cpp 实现已废弃 QJL，使用的是下面的 TurboQuantMSE。

### 4.2 TurboQuantMSE（纯 PolarQuant，生产版本）

```python
class TurboQuantMSE:
    """MSE-only — 不用 QJL，给 PolarQuant 全部 b bits"""

    def __init__(self, d, bit_width, seed=42):
        # 注意：bit_width 直接给 PolarQuant，不减 1
        self.polar_quant = PolarQuant(d, bit_width=bit_width, seed=seed)

    def quantize(self, x):
        return self.polar_quant.quantize(x)  # 直接返回 (indices, norms)

    def dequantize(self, indices, norms):
        return self.polar_quant.dequantize(indices, norms)
```

**TurboQuant vs TurboQuantMSE 对比：**

| | TurboQuant | TurboQuantMSE |
|---|---|---|
| 结构 | PolarQuant (b-1 bits) + QJL (1 bit) | PolarQuant (b bits) |
| 总 bits | b | b |
| 质心数 | 2^(b-1) | 2^b |
| 存储开销 | 多存 QJL signs + residual norm | 只存 indices + norm |
| 质量 | 较差（QJL 增加方差） | 较好 |
| 用途 | 论文原始设计 | **实际使用** |

---

## 5. `kv_cache.py` — KV Cache 集成

### 5.1 设计决策

```python
class KVCacheCompressor:
    def __init__(self, head_dim, k_bits=3, v_bits=3):
        # K cache: 用 TurboQuant (内积保持)
        self.k_quantizer = TurboQuant(head_dim, bit_width=k_bits)
        # V cache: 用 TurboQuantMSE (MSE 保持)
        self.v_quantizer = TurboQuantMSE(head_dim, bit_width=v_bits)
```

**为什么 K 和 V 用不同的量化器？**

```
Attention 计算：
  scores = softmax(Q @ K^T / √d)   ← K 参与点积，内积保持重要
  output = scores @ V               ← V 参与加权求和，MSE 保持重要

K 误差 → softmax 输入偏移 → 指数放大 → routing 错误 → 灾难
V 误差 → 加权求和的加性噪声 → 线性传播 → 影响小
```

### 5.2 压缩流程

```python
    def compress(self, k_cache, v_cache):
        # k_cache shape: (num_layers, num_heads, seq_len, head_dim)
        for layer in range(num_layers):
            for head in range(num_heads):
                k_vecs = k_cache[layer, head]    # (seq_len, head_dim)
                k_compressed = self.k_quantizer.quantize(k_vecs)  # 批量量化

                v_vecs = v_cache[layer, head]
                v_indices, v_norms = self.v_quantizer.quantize(v_vecs)
```

**注意维度：** 量化沿 `head_dim` 维度进行。每个 attention head 的每个 token 位置独立量化一个 `head_dim` 维向量（通常 128 维）。

### 5.3 内存统计

```python
    def memory_stats(self, seq_len, num_layers, num_heads):
        n_vectors = num_layers * num_heads * seq_len
        original_bytes = n_vectors * self.head_dim * 2   # fp16 = 2 bytes

        k_bits = n_vectors * (self.head_dim * self.k_bits + 32)  # 32 for norm
        v_bits = n_vectors * self.head_dim * self.v_bits

        return {
            "compression_ratio": original_bytes / ((k_bits + v_bits) / 8)
        }
```

---

## 6. `utils.py` — Bit Packing

### 6.1 符号压缩

```python
def pack_bits(signs):
    """把 {+1, -1} 数组打包成 uint8 位域，8 个符号 1 字节"""
    bits = (signs > 0).astype(np.uint8)  # {+1,-1} → {1,0}
    return np.packbits(bits)              # NumPy 内置位打包

def unpack_bits(packed, d):
    bits = np.unpackbits(packed)[:d]      # 位解包
    return bits.astype(np.int8) * 2 - 1   # {1,0} → {+1,-1}
```

### 6.2 索引压缩

```python
def pack_indices(indices, bit_width):
    """把 b-bit 索引紧凑打包"""
    if bit_width <= 4:
        # 3-bit 索引: 每 8 个索引打包成 3 字节（24 bits）
        flat = indices.ravel().astype(np.uint8)
        bits = np.zeros(len(flat) * bit_width, dtype=np.uint8)
        for b in range(bit_width):
            bits[b::bit_width] = (flat >> (bit_width - 1 - b)) & 1
        return np.packbits(bits)
    else:
        return indices.astype(np.uint8)  # 5-8 bit 直接用 uint8
```

**3-bit packing 示例：**
```
索引:  [5, 3, 7, 1]
二进制: [101, 011, 111, 001]
展开:  [1,0,1, 0,1,1, 1,1,1, 0,0,1]
打包:  [0b10101111, 0b10010000]  ← 2 字节存 4 个 3-bit 索引
原始:  4 字节（每个 uint8）
节省:  50%
```

---

## 7. 数据流完整追踪

### 压缩一个 KV 向量（turbo3, d=128）

```
输入: x ∈ R^128, fp16, 256 bytes

Step 1: Norm 提取
  norm = ||x|| = 1.732
  x̂ = x / 1.732                    → 128 个 fp64 值

Step 2: 旋转 (rotation.py)
  y = Q @ x̂                        → 128 × 128 矩阵乘法
  y 的分布: 每个坐标 ≈ N(0, 0.0884) → kurtosis ≈ 3.0

Step 3: 量化 (codebook.py)
  centroids = [-0.189, -0.080, -0.0267, 0.0267, 0.080, 0.189, ...]  (8个)
  对 y 的每个坐标找最近质心
  indices = [3, 5, 4, 2, ...]       → 128 个 3-bit 整数

存储:
  indices: 128 × 3 bits = 384 bits = 48 bytes
  norm: 1 × fp16 = 2 bytes
  总计: 50 bytes

压缩比: 256 / 50 = 5.12x ✅
```

### 解压缩

```
输入: indices (128 × 3-bit) + norm (fp16)

Step 1: 查表
  y_hat[j] = centroids[indices[j]]   → 128 个 fp64 值

Step 2: Norm correction
  y_hat = y_hat / ||y_hat||          → 重新归一化

Step 3: 逆旋转
  x̂_hat = Q^T @ y_hat              → 128 × 128 矩阵乘法

Step 4: 恢复缩放
  x_hat = norm × x̂_hat             → 128 个 fp64 值

输出: x_hat ∈ R^128
  cosine_sim(x, x_hat) ≈ 0.91
  MSE ≈ 0.0018
```

---

## 8. 公开 API（`__init__.py`）

```python
from turboquant.polar_quant import PolarQuant
from turboquant.qjl import QJL
from turboquant.turboquant import TurboQuant, TurboQuantMSE, CompressedVector
from turboquant.kv_cache import KVCacheCompressor
```

**用户最常用的两个类：**

| 类 | 用途 | 示例 |
|---|---|---|
| `KVCacheCompressor` | 压缩整个 KV Cache | `comp.compress(k, v)` |
| `TurboQuantMSE` | 单独压缩向量 | `tq.quantize(x)` → `tq.dequantize(idx, norm)` |

---

## 9. 代码质量观察

### 优点
- 代码简洁，核心压缩逻辑 < 200 行
- 数值稳定性处理到位（零向量保护、slogdet 替代 det、sf() 替代 1-cdf()）
- 批量处理支持良好（单向量和批量共用接口）
- 500+ 测试，CI 要求 ≥95% 覆盖率

### 设计选择
- Python 原型用密集旋转矩阵（O(d²)），C/Metal 实现用 WHT（O(d log d)）
- 码本是静态预计算的（依赖 d 和 bit_width），无需运行时校准
- K 和 V 用不同的量化策略（TurboQuant vs TurboQuantMSE）

### 与 llama.cpp C 实现的差异
- Python 用密集矩阵旋转，C 用 WHT 蝶形运算
- Python 是原型验证，C 有 Metal/CUDA GPU 内核
- Python 没有 Sparse V（C 实现独有的优化）
- Python 没有 Boundary V（C 实现独有的层级策略）

---

## 相关笔记

- [[Turbo Quant 详解]] — 整体概述
- [[TurboQuant 实际实现详解]] — 管线概念解释
- [[Walsh-Hadamard 变换（WHT）入门]] — rotation.py 的数学基础
- [[Lloyd-Max 最优量化原理]] — codebook.py 的数学基础

---

*核心算法不到 500 行 Python，这就是 TurboQuant 的全部。复杂度在数学，不在工程。*
