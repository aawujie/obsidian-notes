---
title: "第24讲：随机微积分"
type: lecture-note
created: 2026-05-19
updated: 2026-05-19
source: "MIT 18.642 数学在金融中的应用 (Fall 2024)"
source_url: "https://www.youtube.com/watch?v=5cruqmIF6l0"
bilibili: "BV15KoXBEE9E"
author: "MIT OpenCourseWare"
tags:
  - stochastic-calculus
  - ito-integral
  - brownian-motion
  - quantitative-finance
  - MIT-OCW
---

# 第24讲：随机微积分

> MIT 18.642《数学在金融中的应用》(Fall 2024) — 中文配音版

---

## 1. 引言与动机

随机微积分的核心问题：**如何对依赖于随机过程（尤其是布朗运动）的函数进行积分？**

在定量金融中，股票价格、衍生品合约价值的动态变化都可以表示为带有随机性的函数积分形式。普通的实数微积分（基于实变量的 Riemann 积分）无法直接处理这种随机性，因此需要发展随机微积分理论。

---

## 2. 回顾：带漂移的布朗运动

### 定义

带漂移的布朗运动 $X_t$ 由两个参数刻画：

- **漂移系数** $\mu$ — 确定性的趋势方向
- **波动率（扩散系数）** $\sigma$ — 随机波动的大小

标准布朗运动 $\mu=0,\ \sigma=1$ 时，增量独立且服从正态分布。

### 增量的分布

对于任意时间增量 $\Delta t$，布朗运动增量 $\Delta X$ 满足：

$$\Delta X \sim \mathcal{N}(\mu\Delta t,\ \sigma^2\Delta t)$$

- **均值**：$\mathbb{E}[\Delta X] = \mu\Delta t$
- **方差**：$\text{Var}(\Delta X) = \sigma^2\Delta t$

### 增量平方的极限性质

当 $\Delta t \to 0$ 时：

$$\mathbb{E}[(\Delta X)^2] = \sigma^2\Delta t + o(\Delta t)$$

这意味着 $(\Delta X)^2 \approx dt$，这是随机微积分区别于普通微积分的**关键性质**——布朗运动增量的平方在无穷小量级上与 $dt$ 同阶。

> **推论**：泰勒展开中关于 $X$ 的二阶项不能像普通微积分那样忽略，必须保留。高阶项（$\geq 3$）为 $o(dt)$，可以忽略。

---

## 3. 随机微分方程 (SDE) 符号

带漂移的布朗运动可以表示为随机微分方程：

$$dX_t = \mu\, dt + \sigma\, dB_t$$

其中 $B_t$ 为标准布朗运动。

### 积分形式

$$X_t = X_0 + \int_0^t \mu\, ds + \int_0^t \sigma\, dB_s$$

这个解的形式在直觉上很自然：
- 第一项是初始值
- 第二项是漂移的累积（普通积分）
- 第三项是随机波动的累积（**伊藤积分**）

### 推广到非恒定参数

更一般的随机微分方程为：

$$dX_t = \mu(t, X_t)\, dt + \sigma(t, X_t)\, dB_t$$

其中漂移和波动率都可以依赖于时间 $t$ 和过程当前值 $X_t$。这在金融建模中极为重要——例如期权价值同时取决于到期时间和标的价格。

---

## 4. 伊藤积分 (Itô Integral) 的构建

积分目标：计算 $\int_0^T f(s, B_s)\, dB_s$

### 4.1 概率基础

- **概率空间**：$(\Omega, \mathcal{F}, P)$
  - $\Omega$：所有可能的样本路径
  - $\mathcal{F}$：$\sigma$-代数（可测事件集合）
  - $P$：概率测度
- **滤子 (Filtration)** $\mathcal{F}_t$：到时间 $t$ 为止已知的所有信息
  - $t$ 之前：路径是确定的、可预测的
  - $t$ 之后：路径是随机的
- **适应性 (Adaptedness)**：函数 $f$ 在 $\mathcal{F}_t$ 下可测 → 只能用过去的已知信息

### 4.2 四种递进情形

#### 情形 1：$f(x) = 1$

$$\int_0^T dB_s = B_T - B_0 = B_T$$

- $\mathbb{E}[\int_0^T dB_s] = 0$
- $\text{Var}(\int_0^T dB_s) = T$
- 这等同于布朗运动本身的总变化量。

> **金融含义**：如果持有 1 单位资产且价格遵循布朗运动，盈亏就是布朗运动的增量。

#### 情形 2：$f$ 为确定性阶梯函数

$f(t)$ 仅依赖于时间，在各时间区间上分段常数：

$$\int_0^T f(s)\, dB_s = \sum_i f(t_i) \cdot (B_{t_{i+1}} - B_{t_i})$$

- 均值仍为 0
- 方差 = $\sum_i f(t_i)^2 (t_{i+1} - t_i)$

> **金融含义**：在不同时间段持有不同确定数量的资产，收益为各段收益之和。

#### 情形 3：$f$ 为适应随机阶梯函数

$A_i = f(\omega)$ 是随机变量，但须满足 $A_i$ 在 $\mathcal{F}_{t_i}$ 下可测（**非预期性** — non-anticipating）：

$$\int_0^T f(s, B_s)\, dB_s = \sum_i A_i \cdot (B_{t_{i+1}} - B_{t_i})$$

- $\mathbb{E}[\int f\, dB] = 0$（因为 $A_i$ 与未来的 $(B_{t_{i+1}}-B_{t_i})$ 独立，后者期望为 0）
- $\text{Var} = \sum_i \mathbb{E}[A_i^2] (t_{i+1} - t_i)$

> **关键直觉**：期望为 0 是因为每一步只用过去的已知信息乘以未来的独立增量，通过条件期望分解可证明。

#### 情形 4：一般适应过程的极限定义

将时间区间 $[0, T]$ 等分为 $n$ 段，令阶梯函数近似 $f$，取 $n \to \infty$ 的极限：

$$\int_0^T f(s, B_s)\, dB_s = \lim_{n\to\infty} \sum_{i=0}^{n-1} f(t_i, B_{t_i}) \cdot (B_{t_{i+1}} - B_{t_i})$$

这个极限在**概率意义**下收敛（均方收敛）。

### 4.3 重要例子：$\int_0^T B_s\, dB_s$

这是随机微积分中最经典的计算。**不是 $\frac{1}{2}B_T^2$！**

**证明（巧妙的代数技巧）**：

注意到恒等式：

$$B_{t_i}(B_{t_{i+1}}-B_{t_i}) = \frac{1}{2}(B_{t_{i+1}}^2 - B_{t_i}^2) - \frac{1}{2}(B_{t_{i+1}}-B_{t_i})^2$$

对 $i=0$ 到 $n-1$ 求和：

$$\sum B_{t_i}\Delta B_i = \frac{1}{2}(B_T^2 - B_0^2) - \frac{1}{2}\sum (\Delta B_i)^2$$

第一项是 Telescoping sum（中间项相消），结果为 $\frac{1}{2}B_T^2$。

第二项的极限：$\sum (\Delta B_i)^2 \to T$（这是布朗运动二次变差的性质）

取极限得：

$$\boxed{\int_0^T B_s\, dB_s = \frac{1}{2}B_T^2 - \frac{1}{2}T}$$

> ⚠️ **关键区别**：普通微积分中 $\int x\,dx = x^2/2$，但随机微积分多了 $-\frac{1}{2}T$ 这一项。这是因为布朗运动的二次变差不为零。

### 4.4 伊藤过程的重要性质

伊藤积分 $X_t = \int_0^t f\, dB_s$ 是一个**鞅 (Martingale)**：

$$\mathbb{E}[X_{t+k} \mid \mathcal{F}_t] = X_t$$

条件方差：

$$\text{Var}(X_{t+k} \mid \mathcal{F}_t) = \mathbb{E}\left[\int_t^{t+k} f^2(s, B_s)\, ds \mid \mathcal{F}_t\right]$$

此外 $X_t$ 是一个**均值为零的高斯过程**，协方差为：

$$\text{Cov}(X_s, X_t) = \int_0^{\min(s,t)} \mathbb{E}[f^2(u, B_u)]\, du$$

### 4.5 L² 等距性 (Itô Isometry)

伊藤积分的关键数学性质：

$$\mathbb{E}\left[\left(\int_0^T f\, dB\right)^2\right] = \mathbb{E}\left[\int_0^T f^2(s, B_s)\, ds\right]$$

即：**伊藤积分的二阶矩 = 被积函数 $f$ 的 $L^2$ 范数**。

这一定理为证明伊藤积分的存在性和唯一收敛极限提供了数学基础，同时也保证了我们可以讨论伊藤过程所在空间的收敛性质。

---

## 5. 伊藤公式 (Itô's Formula)

### 5.1 单变量情形

设 $f: \mathbb{R} \to \mathbb{R}$ 具有连续二阶导数，则：

$$f(B_T) = f(B_0) + \int_0^T f'(B_s)\, dB_s + \frac{1}{2}\int_0^T f''(B_s)\, ds$$

微分形式：

$$\boxed{df(B_t) = f'(B_t)\, dB_t + \frac{1}{2}f''(B_t)\, dt}$$

#### 推导思路

对 $f(B_{t+\Delta t}) - f(B_t)$ 做泰勒展开到二阶：

$$f(B_t + \Delta B) - f(B_t) = f'(B_t)\Delta B + \frac{1}{2}f''(B_t)(\Delta B)^2 + \text{高阶项}$$

因为 $(\Delta B)^2 \approx dt$，二阶项不能忽略。取极限即得伊藤公式。

> 泰勒展开告诉我们：$df = f_x\,dx + \frac{1}{2}f_{xx}\,dx\,dx$，而 $dx\,dx = dt$。

### 5.2 利用伊藤公式反求积分

伊藤公式可以用来**"反向"计算随机积分**（类似于普通微积分中用原函数法计算定积分）。

若存在 $F$ 使得 $F' = f$，且 $F(0) = 0$，则：

$$F(B_T) - F(B_0) = \int_0^T f(B_s)\, dB_s + \frac{1}{2}\int_0^T f'(B_s)\, ds$$

因此：

$$\int_0^T f(B_s)\, dB_s = F(B_T) - F(0) - \frac{1}{2}\int_0^T f'(B_s)\, ds$$

#### 验证：$f(x) = x$

- $F(x) = \frac{1}{2}x^2$，$F'(x) = x = f(x)$，$F''(x) = 1$
- $f'(x) = 1$
- $\int_0^T B_s\, dB_s = \frac{1}{2}B_T^2 - 0 - \frac{1}{2}\int_0^T 1\, ds = \frac{1}{2}B_T^2 - \frac{1}{2}T$ ✅

与之前离散化极限的结果一致。

### 5.3 多变量（双变量）情形

设 $f(t, x): \mathbb{R}_+ \times \mathbb{R} \to \mathbb{R}$ 满足 $f \in C^{1,2}$（对 $t$ 一阶连续可导，对 $x$ 二阶连续可导）：

$$f(T, B_T) = f(0, B_0) + \int_0^T \frac{\partial f}{\partial t}(s, B_s)\, ds + \int_0^T \frac{\partial f}{\partial x}(s, B_s)\, dB_s + \frac{1}{2}\int_0^T \frac{\partial^2 f}{\partial x^2}(s, B_s)\, ds$$

微分形式：

$$\boxed{df(t, B_t) = \frac{\partial f}{\partial t}\, dt + \frac{\partial f}{\partial x}\, dB_t + \frac{1}{2}\frac{\partial^2 f}{\partial x^2}\, dt}$$

**为什么只有 $\partial^2/\partial x^2$ 项保留？**
- $\partial^2/\partial t^2$、$\partial^2/\partial t\partial x$ 等项阶数为 $dt^2$ 或 $dt\,dB_t$，都是 $o(dt)$，可忽略
- 只有 $(\Delta B)^2 \sim dt$，所以只有 $\partial^2/\partial x^2 \cdot (dB)^2$ 贡献到 $dt$ 级别

---

## 6. 鞅理论与偏微分方程的联系

### 6.1 伊藤过程的鞅条件

对于一般过程 $f(t, X_t)$，其中 $X_t$ 为伊藤过程：

$$f(t, X_t) \text{ 是鞅} \iff \frac{\partial f}{\partial t} + \frac{1}{2}\frac{\partial^2 f}{\partial x^2} = 0$$

这就是**热方程**（反向）。

如果时间积分项 $\neq 0$，则过程不是鞅（存在漂移趋势）。

### 6.2 示例：指数鞅

考虑 $f(t, x) = \exp(\sigma x - \frac{1}{2}\sigma^2 t)$：

验证：
- $\frac{\partial f}{\partial t} = -\frac{1}{2}\sigma^2 f$
- $\frac{\partial f}{\partial x} = \sigma f$
- $\frac{\partial^2 f}{\partial x^2} = \sigma^2 f$

代入伊藤公式：

$$df = -\frac{1}{2}\sigma^2 f\, dt + \sigma f\, dB_t + \frac{1}{2}\sigma^2 f\, dt = \sigma f\, dB_t$$

时间积分项消去！因此 $f(t, B_t)$ 是一个**鞅**。

可以验证：对于任意 $t$，$\mathbb{E}[f(t, B_t)] = f(0, 0) = 1$。

> 此时 $f(t, B_t) = \exp(\sigma B_t - \frac{1}{2}\sigma^2 t)$ 是一个经过缩放的对数正态随机变量。

---

## 7. 应用：击中概率 (Hitting Probability)

### 问题设置

假设 $X_t$ 为带漂移的布朗运动：
$$dX_t = \mu\, dt + \sigma\, dB_t$$

从 $X_0 = 0$ 出发，$a > 0$ 为目标上界，$-b < 0$ 为下界。定义停时：
$$\tau = \inf\{t \geq 0 : X_t = a \text{ 或 } X_t = -b\}$$

**问题**：$X_t$ 先到达 $a$ 的概率 $h(x) = P(X_\tau = a \mid X_0 = x)$？

### 用鞅方法求解

定义 $M_t = h(X_t)$，其中 $h$ 应满足边界条件：
- $h(a) = 1$（到达 $a$ 则成功概率为 1）
- $h(-b) = 0$（到达 $-b$ 则成功概率为 0）

由**可选停时定理 (Optional Stopping Theorem)**：

$$h(0) = \mathbb{E}[h(X_\tau)] = 1 \cdot P(\text{到达 }a) + 0 \cdot P(\text{到达 }-b) = P(\text{到达 }a)$$

为使 $M_t$ 成为鞅，$h$ 需满足鞅的 PDE 条件：

$$\mu\, h'(x) + \frac{1}{2}\sigma^2\, h''(x) = 0$$

即：
$$\frac{h''(x)}{h'(x)} = -\frac{2\mu}{\sigma^2}$$

积分得 $\ln h'(x) = -\frac{2\mu}{\sigma^2}x + C$，故 $h'(x) \propto \exp(-2\mu x/\sigma^2)$。

再次积分并代入边界条件，得到指数型线性解。

> 这个论证展示了**鞅理论**在量化金融中的优雅应用：将概率计算转化为微分方程求解。

---

## 8. 下一讲预告

- 随机微分方程 (SDE) 的深入讨论
- 标准伊藤过程中漂移函数 $a(t, X_t)$ 和扩散函数 $b(t, X_t)$ 需满足的条件：
  - $\int |a|\, dt < \infty$（绝对可积）
  - $\int b^2\, dt < \infty$（平方可积，保证方差有限）
- 如果以上条件不满足，积分将发散（"爆炸"）

---

## 关键公式速查

| 公式 | 表达式 |
|:---|:---|
| 布朗运动 SDE | $dX_t = \mu\,dt + \sigma\,dB_t$ |
| 伊藤积分（$f=1$） | $\int_0^T dB_s = B_T$ |
| $\int B_s dB_s$ | $\frac{1}{2}B_T^2 - \frac{1}{2}T$ |
| 伊藤公式（单变量） | $df(B_t) = f'dB_t + \frac{1}{2}f''dt$ |
| 伊藤公式（双变量） | $df = f_t dt + f_x dB_t + \frac{1}{2}f_{xx}dt$ |
| L² 等距性 | $\mathbb{E}[(\int f dB)^2] = \mathbb{E}[\int f^2 dt]$ |
| 鞅条件 (PDE) | $f_t + \frac{1}{2}f_{xx} = 0$ |
| 指数鞅 | $f = \exp(\sigma B_t - \frac{1}{2}\sigma^2 t)$ |

---

*笔记整理自 MIT OpenCourseWare 18.642 Lecture 24 中文配音版，转录工具：OpenAI Whisper (small)*