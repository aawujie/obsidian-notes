# Walsh-Hadamard 变换（WHT）入门

> **目的：** 理解 TurboQuant 核心旋转操作的数学基础
> **前置知识：** 矩阵乘法、正交矩阵概念
> **创建日期：** 2026-04-02

---

## 1. WHT 是什么？

Walsh-Hadamard Transform（WHT）是一种**正交变换**，作用类似于 FFT（快速傅里叶变换），但更简单：

| 对比 | FFT | WHT |
|------|-----|-----|
| 基函数 | 正弦/余弦（连续） | ±1（离散） |
| 矩阵元素 | 复数 | 只有 +1 和 -1 |
| 计算复杂度 | O(d log d) | O(d log d) |
| 硬件友好 | 需要浮点乘法 | **只需加减法** |

---

## 2. Hadamard 矩阵

最小的 Hadamard 矩阵：

$$H_1 = \begin{bmatrix} 1 \end{bmatrix}$$

递归构造（Sylvester 构造）：

$$H_2 = \frac{1}{\sqrt{2}} \begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix}$$

$$H_4 = \frac{1}{2} \begin{bmatrix} 1 & 1 & 1 & 1 \\ 1 & -1 & 1 & -1 \\ 1 & 1 & -1 & -1 \\ 1 & -1 & -1 & 1 \end{bmatrix}$$

**规律：** 每次把矩阵"分成四块"，右下角取负。

$$H_{2n} = \frac{1}{\sqrt{2}} \begin{bmatrix} H_n & H_n \\ H_n & -H_n \end{bmatrix}$$

### 关键性质

1. **正交性：** $H^T H = I$（矩阵与其转置的乘积是单位矩阵）
2. **自逆性：** $H = H^{-1} = H^T$（Hadamard 变换的逆就是自身！）
3. **保范性：** $\|Hx\| = \|x\|$（变换不改变向量长度）
4. **尺寸限制：** 只能是 2 的幂次（2, 4, 8, 16, 32, 64, 128...）

---

## 3. 直觉理解

### 3.1 信号处理角度

把 WHT 想象成"频率分析"：

```
原始信号 x = [3, 1, 4, 2]

WHT 后 y = H₄ · x = [10, 2, 0, -4] / 2 = [5, 1, 0, -2]

y[0] = 均值（整体水平）
y[1] = 奇偶差异
y[2] = 前后差异
y[3] = 交替差异
```

它把信号分解成不同"频率"的成分，类似傅里叶变换但用方波代替正弦波。

### 3.2 在 TurboQuant 中的作用

**问题：** KV cache 向量的坐标分布不均匀，有些坐标值很大（离群值），直接量化效果差。

**解法：** 用 WHT + 随机符号翻转做"搅拌"（mixing），让所有坐标的分布变均匀。

```
旋转前：x = [0.01, 0.02, 0.5, -0.8, 0.01, ...]
         ↑ 大部分很小，个别很大（kurtosis ≈ 900）

WHT + 随机符号翻转

旋转后：y = [0.08, -0.09, 0.07, 0.10, -0.08, ...]
         ↑ 分布均匀，近似高斯（kurtosis ≈ 3.0）
```

**类比：** 想象一杯分层的鸡尾酒（颜色不均匀），WHT 就像搅拌器，把所有颜色混合均匀。

---

## 4. 随机符号翻转（Random Sign Flips）

仅用 WHT 不够随机（因为 Hadamard 矩阵是确定的）。加上**随机符号翻转**增强随机性：

$$y = H \cdot (\sigma \odot x)$$

其中 $\sigma \in \{+1, -1\}^d$ 是随机符号向量，$\odot$ 是逐元素乘法。

```python
# rotation.py 中的实现（简化）
def rotate(x, hadamard_matrix, signs):
    x_flipped = x * signs          # 随机翻转每个坐标的符号
    y = hadamard_matrix @ x_flipped  # Hadamard 变换
    return y
```

**为什么需要随机符号？**
- Hadamard 矩阵是固定的，某些特殊输入可能旋转后仍不均匀
- 随机符号确保对**任何输入**都能均匀化
- 符号向量由 seed 确定，解压时用同一个 seed 恢复

---

## 5. 蝶形运算（Butterfly）—— 为什么 O(d log d)

朴素矩阵乘法 $y = Hx$ 需要 $O(d^2)$。但 Hadamard 矩阵的递归结构允许用蝶形算法加速：

```
d = 8 的蝶形计算示例：

第 1 轮（相邻配对）：
  y[0] = x[0] + x[1]    y[1] = x[0] - x[1]
  y[2] = x[2] + x[3]    y[3] = x[2] - x[3]
  y[4] = x[4] + x[5]    y[5] = x[4] - x[5]
  y[6] = x[6] + x[7]    y[7] = x[6] - x[7]

第 2 轮（间隔 2 配对）：
  z[0] = y[0] + y[2]    z[2] = y[0] - y[2]
  z[1] = y[1] + y[3]    z[3] = y[1] - y[3]
  ...

第 3 轮（间隔 4 配对）：
  ...

总共 log₂(8) = 3 轮，每轮 d/2 = 4 次加法
总运算量 = d/2 × log₂d = O(d log d)
```

**没有任何乘法！** 只有加法和减法。这就是 WHT 在 GPU 上极快的原因。

---

## 6. WHT vs 密集随机旋转

| | WHT + 符号翻转 | 密集随机旋转矩阵 |
|---|---|---|
| 生成方式 | Hadamard 递归 + 随机符号 | Haar 分布 QR 分解 |
| 存储 | O(d) 只存符号向量 | O(d²) 存整个矩阵 |
| 计算 | O(d log d) 蝶形 | O(d²) 矩阵乘 |
| 随机性 | 足够好（实验验证） | 理论最优 |

TurboQuant 的优化旅程：
1. 最初用密集矩阵：739 tok/s（0.27x q8_0）
2. 换成 WHT：性能飙升到 2747 tok/s（1.02x q8_0）

**WHT 让 TurboQuant 从"理论可行但太慢"变成"实际可用"。**

---

## 7. 高维高斯化定理（为什么有效）

**数学保证：** 对于单位球面上的向量 $x$，经过随机正交变换后，当维度 $d$ 足够大时（$d \geq 128$ 在实践中就够了），每个坐标近似服从：

$$x_i \sim N(0, 1/d)$$

且坐标之间近似独立。

这就是为什么 TurboQuant 在 head_dim = 128（主流 LLM）上效果很好。

**实际验证（来自 repo）：**
```
真实 Qwen3-1.7B KV 张量：
  原始 kurtosis:    900.4
  旋转后 kurtosis:  2.9  （高斯分布的 kurtosis = 3.0）
  旋转后标准差:     0.088388
  理论值 1/√d:      0.088388
  比值:             1.000（精确匹配）
```

---

## 8. 代码中的 WHT

```python
# turboquant/rotation.py 关键函数（简化）

def fast_hadamard_transform(x):
    """O(d log d) 蝶形运算实现"""
    d = len(x)
    h = 1
    while h < d:
        for i in range(0, d, h * 2):
            for j in range(i, i + h):
                a = x[j]
                b = x[j + h]
                x[j] = a + b      # 蝶形加
                x[j + h] = a - b  # 蝶形减
        h *= 2
    return x / np.sqrt(d)  # 归一化

def random_rotation(x, seed):
    """WHT + 随机符号翻转"""
    rng = np.random.default_rng(seed)
    signs = rng.choice([-1, 1], size=len(x))
    return fast_hadamard_transform(x * signs)
```

---

## 关键要点总结

1. WHT 是一种只用加减法的正交变换，计算量 O(d log d)
2. Hadamard 矩阵是自逆的：变换和逆变换用同一个操作
3. WHT + 随机符号翻转 = 高效的随机旋转，把任意分布"搅拌"成高斯
4. 这是 TurboQuant 的性能关键：让压缩从 0.27x 加速到 1.02x q8_0

---

## 相关笔记

- [[TurboQuant 实际实现详解]] — WHT 在完整管线中的位置
- [[Lloyd-Max 最优量化原理]] — 旋转后的量化步骤
- [[注意力机制详解]] — 理解 KV cache 的上下文

---

*WHT 本质上是最简单的正交变换——只做加减法就能实现"信息搅拌"。*
