---
title: 泛函与变分法：泛函的导数与Euler-Lagrange方程系统推导
type: concept
created: 2026-06-08
updated: 2026-06-08
tags: [泛函分析, 变分法, Gateaux导数, Fréchet导数, Euler-Lagrange方程]
sources: [Gelfand & Fomin - Calculus of Variations, Zeidler - Applied Functional Analysis, Brezis - Functional Analysis]
---

# 泛函与变分法：泛函的导数与Euler-Lagrange方程系统推导

> 本文是系列第二篇，将普通微积分中"导数"的概念推广到无限维函数空间，系统建立 Gateaux 导数和 Fréchet 导数的理论，并在此基础上推导各种形式的 Euler-Lagrange 方程。

---

## 1. 从有限维到无限维：导数的再思考

### 1.1 有限维情形回顾

在 $\mathbb{R}^n$ 中，函数 $f: \mathbb{R}^n \to \mathbb{R}$ 的导数有两种等价刻画：

- **方向导数**：$\nabla_v f(x) = \lim_{t \to 0} \frac{f(x+tv) - f(x)}{t}$
- **全微分**：$f(x+h) = f(x) + \nabla f(x) \cdot h + o(\|h\|)$

第二个刻画更强：它要求逼近误差 $o(\|h\|)$ 对**所有方向一致**地趋于零。将这两种刻画推广到无穷维函数空间，就得到了 **Gâteaux 导数**和 **Fréchet 导数**。

### 1.2 函数空间：比 $\mathbb{R}^n$ 多了什么？

| 性质 | $\mathbb{R}^n$ | 函数空间（如 $C^1[a,b]$） |
|------|---------------|--------------------------|
| 维度 | 有限 $n$ | 无限维 |
| 范数 | 所有范数等价 | 不同范数不等价 |
| 单位球 | 紧致 (Heine-Borel) | **不紧致**（关键区别） |
| 完备性 | 自动完备 | 依赖于范数选择 |

> **核心洞察**：在无限维空间中，有界序列不一定有收敛子序列——这是所有"困难"的根源，也是为什么需要 Sobolev 空间和弱收敛等概念。

---

## 2. Gateaux 导数：方向导数

### 2.1 定义

设 $J: X \to \mathbb{R}$ 是定义在赋范线性空间 $X$ 上的泛函。$J$ 在 $y \in X$ 处沿方向 $h \in X$ 的 **Gâteaux 导数**（或**一阶变分**）定义为：

$$\boxed{\delta J(y; h) = \lim_{\epsilon \to 0} \frac{J[y + \epsilon h] - J[y]}{\epsilon} = \left.\frac{d}{d\epsilon} J[y + \epsilon h]\right|_{\epsilon=0}}$$

如果该极限对**所有** $h \in X$ 存在，则称 $J$ 在 $y$ 处 **Gâteaux 可微**。

### 2.2 性质

- **齐次性**：$\delta J(y; \alpha h) = \alpha \delta J(y; h)$（对任意 $\alpha \in \mathbb{R}$）
- **不一定线性**：Gâteaux 导数可以是 $h$ 的非线性函数（这是它与 Fréchet 导数的关键区别）
- **不一定连续**：即使对每个 $h$ 存在，映射 $h \mapsto \delta J(y; h)$ 可能不连续

### 2.3 例子

**例1**（二次泛函）：$J[y] = \int_a^b (y'(x))^2\,dx$

$$\begin{aligned}
\delta J(y; h) &= \left.\frac{d}{d\epsilon} \int_a^b (y' + \epsilon h')^2\,dx\right|_{\epsilon=0} \\
&= \int_a^b 2y'(x) h'(x)\,dx
\end{aligned}$$

这是 $h$ 的**线性泛函**。

**例2**（非线性的 Gâteaux 导数）：$J[y] = \|y\|_\infty = \max_{x\in[a,b]}|y(x)|$ 在 $y \equiv 0$ 处

$$\delta J(0; h) = \lim_{\epsilon \to 0} \frac{\|\epsilon h\|_\infty}{\epsilon} = \|h\|_\infty$$

这是 $h$ 的非线性函数。

---

## 3. Fréchet 导数：真正的"全微分"

### 3.1 定义

$J$ 在 $y$ 处 **Fréchet 可微**，如果存在一个**有界线性泛函** $DJ[y] \in X^*$，使得：

$$\boxed{\lim_{\|h\| \to 0} \frac{|J[y+h] - J[y] - DJ[y](h)|}{\|h\|} = 0}$$

等价地写成：

$$J[y+h] = J[y] + DJ[y](h) + o(\|h\|)$$

### 3.2 与 Gâteaux 导数的关系

| 性质 | Gâteaux | Fréchet |
|------|---------|---------|
| 定义 | 逐方向极限 | 一致极限（对所有方向） |
| $h$ 的依赖 | 可以不线性 | 必须线性 |
| 连续性 | 不保证 | 自动连续 |
| 推导关系 | Fréchet ⇒ Gâteaux | Gâteaux ⇏ Fréchet |

**关键定理**：如果 Gâteaux 导数 $\delta J(y; h)$ 在 $y$ 的某个邻域内存在，$h \mapsto \delta J(y; h)$ 是**有界线性泛函**，且 $\delta J(y; h)$ 在 $y$ 处（作为 $y$ 的函数）连续，则 $J$ 是 Fréchet 可微的，且 $DJ[y](h) = \delta J(y; h)$。

### 3.3 实例辨析

**Gâteaux 但非 Fréchet 的例子**（在 $\mathbb{R}^2$ 中）：

$$f(x,y) = \begin{cases} \frac{x^3}{x^2+y^2} & (x,y) \neq (0,0) \\ 0 & (x,y) = (0,0) \end{cases}$$

在 $(0,0)$ 处，沿任何方向的方向导数都存在，但 $f$ 在 $(0,0)$ 不连续，更不 Fréchet 可微。

---

## 4. 变分导数 $\frac{\delta J}{\delta y}$

### 4.1 动机

在物理和工程中，我们经常需要将泛函的导数表示为**积分核**的形式。如果存在函数（或分布）$\frac{\delta J}{\delta y(x)}$ 使得：

$$DJ[y](h) = \int_a^b \frac{\delta J}{\delta y(x)} \, h(x) \, dx$$

则称 $\frac{\delta J}{\delta y(x)}$ 为 **变分导数 (variational derivative)**。

### 4.2 计算规则

对于 $J[y] = \int_a^b F(x, y, y')\,dx$：

$$\frac{\delta J}{\delta y(x)} = \frac{\partial F}{\partial y} - \frac{d}{dx}\!\left(\frac{\partial F}{\partial y'}\right)$$

**关键对应**：

$$\delta J = 0 \;\Longleftrightarrow\; \frac{\delta J}{\delta y} = 0 \;\Longleftrightarrow\; \text{Euler-Lagrange 方程}$$

### 4.3 常用变分导数

| 泛函 $J[y]$ | $\frac{\delta J}{\delta y(x)}$ |
|-------------|-------------------------------|
| $\int \frac{1}{2}(y')^2\,dx$ | $-y''(x)$ |
| $\int \frac{1}{2}y^2\,dx$ | $y(x)$ |
| $\int \frac{1}{2}(y')^2 + V(y)\,dx$ | $-y''(x) + V'(y)$ |
| $\int \sqrt{1+(y')^2}\,dx$ | $-\frac{d}{dx}\!\left(\frac{y'}{\sqrt{1+(y')^2}}\right)$ |
| $y(x_0)$ | $\delta(x - x_0)$（Dirac分布） |

---

## 5. Euler-Lagrange 方程的系统推广

### 5.1 多个函数（向量值函数）

设 $J[y_1, \ldots, y_n] = \int_a^b F(x, y_1, \ldots, y_n, y_1', \ldots, y_n')\,dx$，则对每个 $i$ 有一个 EL 方程：

$$\boxed{\frac{\partial F}{\partial y_i} - \frac{d}{dx}\!\left(\frac{\partial F}{\partial y_i'}\right) = 0, \quad i = 1, 2, \ldots, n}$$

**物理意义**：这正是 Lagrangian 力学的核心——对每个广义坐标 $q_i$ 给出一个运动方程。

**例**：在平面中，$J[\mathbf{r}] = \int \frac{1}{2}m(\dot{x}^2 + \dot{y}^2) - V(x,y)\,dt$，EL 方程给出 $m\ddot{x} = -\partial V/\partial x$，$m\ddot{y} = -\partial V/\partial y$。

### 5.2 高阶导数

设 $J[y] = \int_a^b F(x, y, y', y'', \ldots, y^{(n)})\,dx$，则：

$$\boxed{\sum_{k=0}^n (-1)^k \frac{d^k}{dx^k}\!\left(\frac{\partial F}{\partial y^{(k)}}\right) = 0}$$

**推导**：反复分部积分，每次分部产生一个 $(-1)$ 因子。

**例**：弹性梁的弯曲能 $J[y] = \int \left[\frac{1}{2}EI(y'')^2 - qy\right]dx$，EL 方程给出 $EI\,y^{(4)} = q$（四阶梁方程）。

### 5.3 多元函数（多重积分）

设 $J[u] = \int_\Omega F(x_1, \ldots, x_n, u, u_{x_1}, \ldots, u_{x_n})\,d\mathbf{x}$，则：

$$\boxed{\frac{\partial F}{\partial u} - \sum_{i=1}^n \frac{\partial}{\partial x_i}\!\left(\frac{\partial F}{\partial u_{x_i}}\right) = 0}$$

**推导**：对每个 $\partial/\partial x_i$ 项使用**散度定理**（高维分部积分），边界项因 $\eta|_{\partial\Omega} = 0$ 而消失。

**例**：$F = \frac{1}{2}|\nabla u|^2$ → $\Delta u = 0$（Laplace 方程）；$F = \frac{1}{2}|\nabla u|^2 - fu$ → $-\Delta u = f$（Poisson 方程）。

---

## 6. 变分法基本引理

### 6.1 古典版本

> **引理**：设 $f \in C[a,b]$。若对任意 $\eta \in C^1[a,b]$ 满足 $\eta(a) = \eta(b) = 0$，都有 $\int_a^b f(x)\eta(x)\,dx = 0$，则 $f(x) \equiv 0$ 在 $[a,b]$ 上。

**证明思路**：若存在 $x_0$ 使 $f(x_0) \neq 0$，由连续性可在 $x_0$ 附近构造一个"鼓包函数" $\eta$ 使积分为正，矛盾。

### 6.2 推广版本

- **Du Bois-Reymond 引理**：若 $f \in C[a,b]$ 且 $\int_a^b f(x)\eta'(x)\,dx = 0$ 对所有 $\eta \in C^1$ 且 $\eta(a)=\eta(b)=0$ 成立，则 $f(x) = \text{const}$。
- **$L^p$ 版本**：若 $f \in L^2[a,b]$ 且 $\int_a^b f\phi = 0$ 对所有 $\phi \in C_c^\infty(a,b)$ 成立，则 $f = 0$ a.e.

> 这个引理是将 $\delta J = 0$ 转化为逐点微分方程的逻辑桥梁，没有它，我们无法从积分形式得到 Euler-Lagrange 方程。

---

## 7. 二阶变分与极值判定

### 7.1 二阶变分

类似于普通微积分中的 $f''(x^*)$，我们定义泛函的**二阶变分**：

$$\delta^2 J := \left.\frac{d^2}{d\epsilon^2} J[y + \epsilon \eta]\right|_{\epsilon=0}$$

对于 $J[y] = \int_a^b F(x, y, y')\,dx$：

$$\delta^2 J = \int_a^b \left[F_{yy}\eta^2 + 2F_{yy'}\eta\eta' + F_{y'y'}(\eta')^2\right] dx$$

通过分部积分可化为标准二次型：

$$\delta^2 J = \int_a^b \left[P(x)(\eta')^2 + Q(x)\eta^2\right] dx$$

其中 $P = F_{y'y'}$，$Q = F_{yy} - \frac{d}{dx}F_{yy'}$。

### 7.2 极值的充分条件

| 条件 | 结论 |
|------|------|
| $\delta J = 0$ 且 $\delta^2 J > 0$（对所有 $\eta \neq 0$） | **严格极小值** |
| $\delta J = 0$ 且 $\delta^2 J < 0$（对所有 $\eta \neq 0$） | **严格极大值** |
| $\delta J = 0$ 且 $\delta^2 J \geq 0$ | 极小值的**必要条件** |

### 7.3 Legendre 条件

$\delta^2 J \geq 0$ 对所有 $\eta$ 成立的一个必要条件是：

$$\boxed{F_{y'y'} \geq 0 \quad \text{（Legendre 条件）}}$$

如果 $F_{y'y'} > 0$（严格），则称为**强 Legendre 条件**，这是极小值的较强必要条件。

**物理直觉**：$F_{y'y'} > 0$ 意味着系统对"弯曲"有正刚度——偏离极值曲线会增加能量。

---

## 8. 自由端点与横截条件

### 8.1 端点可变的情形

当端点 $y(a)$ 或 $y(b)$ 不固定时，分部积分产生的边界项不能丢弃：

$$\delta J = \int_a^b \left[F_y - \frac{d}{dx}F_{y'}\right]\eta\,dx + \left[F_{y'}\eta\right]_a^b$$

除了 EL 方程，还需要边界条件：

$$\boxed{F_{y'}\big|_{x=a} = 0 \quad \text{或} \quad F_{y'}\big|_{x=b} = 0}$$

这称为**自然边界条件 (natural boundary condition)**。

### 8.2 横截条件 (Transversality)

当端点可以在给定曲线上滑动时（如 $y(b) = \phi(b)$），需满足：

$$\boxed{F + (\phi' - y')F_{y'} = 0 \quad \text{在端点}}$$

---

## 总结：三个层次的导数

```
方向导数（Gâteaux）
    │  δJ(y; h) = lim_{ε→0} [J(y+εh) - J(y)]/ε
    │  对每个方向 h 单独取极限
    │
    ├── 若 h ↦ δJ(y; h) 是 有界线性泛函 且 连续
    │       │
    │       ▼
    │   全微分（Fréchet）
    │   J(y+h) = J(y) + DJ[y](h) + o(‖h‖)
    │   对所有方向一致逼近
    │
    └── 若 DJ[y](h) = ∫(δJ/δy)·h dx
            │
            ▼
        变分导数 δJ/δy
        极值条件: δJ/δy = 0 ⟺ Euler-Lagrange 方程
```

> 下一篇 [[泛函与变分法-Sobolev空间与直接方法]] 将讨论现代变分法的核心框架：如何在 Sobolev 空间中保证极值解的存在性。

---

## 延伸阅读

- [[泛函与变分法-古典问题到现代框架]] — 历史动机与基础概念
- [[泛函与变分法-Sobolev空间与直接方法]] — 现代变分法理论
- [[泛函与变分法的关系]] — 入门概述
- [[对偶性 duality]] — 对偶空间 $X^*$（Fréchet 导数的落点）