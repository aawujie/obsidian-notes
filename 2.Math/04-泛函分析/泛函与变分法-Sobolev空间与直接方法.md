---
title: 泛函与变分法：Sobolev空间、直接方法与现代理论
type: concept
created: 2026-06-08
updated: 2026-06-08
tags: [泛函分析, 变分法, Sobolev空间, 直接方法, 弱收敛, Noether定理, 机器学习]
sources: [Dacorogna - Direct Methods in the Calculus of Variations, Brezis - Functional Analysis, Evans - Partial Differential Equations]
---

# 泛函与变分法：Sobolev空间、直接方法与现代理论

> 本文是系列第三篇，讨论古典变分法的局限性如何催生了现代变分理论，包括 Sobolev 空间、直接方法、约束变分、Noether 定理，以及变分法在机器学习中的应用。

---

## 1. 古典变分法的困境

### 1.1 两个核心问题

回顾前两篇的讨论，古典变分法存在两个根本性缺陷：

**问题一：极值解未必存在**

在 $C^1[a,b]$ 中，极小化序列 $\{y_n\}$ 可能收敛到一个**不可微**的函数。例如，考虑：

$$J[y] = \int_0^1 (y'(x)^2 - 1)^2\,dx, \quad y(0)=y(1)=0$$

这个泛函在 $C^1$ 中**没有极小值**——你可以用越来越密的锯齿形函数（$y' = \pm 1$，a.e.）使 $J \to 0$，但极限函数处处不可微，不属于 $C^1$。

**问题二：$C^1$ 不完备**

$C^1[a,b]$ 在 $C^1$ 范数下不是完备空间——Cauchy 列可能不收敛到 $C^1$ 函数。这使得标准的极限论证失效。

### 1.2 解决方向

> **核心思想**：放弃 $C^1$，换到一个更大的、完备的、并具有紧性的函数空间——**Sobolev 空间**。

---

## 2. Sobolev 空间速览

### 2.1 弱导数

**定义**：$v \in L^1_{\text{loc}}(\Omega)$ 称为 $u$ 的**第 $\alpha$ 阶弱导数**，如果对所有 $\phi \in C_c^\infty(\Omega)$：

$$\int_\Omega u \cdot D^\alpha \phi \,dx = (-1)^{|\alpha|} \int_\Omega v \cdot \phi \,dx$$

**直觉**：分部积分公式就是弱导数的定义。它把导数从函数本身"转移"到了测试函数上。

**例**：$u(x) = |x|$ 在 $x \in (-1,1)$ 上，经典导数在 $x=0$ 不存在，但弱导数为 $u'(x) = \text{sgn}(x)$（属于 $L^2$）。

### 2.2 Sobolev 空间定义

$$W^{k,p}(\Omega) = \{u \in L^p(\Omega) : D^\alpha u \in L^p(\Omega),\; \forall |\alpha| \leq k\}$$

配备范数：

$$\|u\|_{W^{k,p}} = \left(\sum_{|\alpha| \leq k} \|D^\alpha u\|_{L^p}^p\right)^{1/p}$$

**关键性质**：
- $W^{k,p}$ 是 **Banach 空间**（完备）
- $W^{k,2}$（记为 $H^k$）是 **Hilbert 空间**
- $C_c^\infty(\Omega)$ 在 $W^{k,p}(\Omega)$ 中**稠密**

### 2.3 紧嵌入定理 (Rellich-Kondrachov)

$$\boxed{W^{1,p}(\Omega) \Subset L^q(\Omega), \quad 1 \leq q < p^* = \frac{np}{n-p} \;\text{(若 } p < n\text{)}}$$

> **意义**：$W^{1,p}$ 中的有界序列在 $L^q$ 中有**强收敛**子序列。这是直接方法中紧性步骤的核心。

---

## 3. 直接方法：三步证明极小值存在

### 3.1 框架

考虑极小化问题：

$$\min_{u \in X} J[u], \quad J[u] = \int_\Omega F(x, u, \nabla u)\,dx$$

其中 $X$ 是 Sobolev 空间（如 $W^{1,p}(\Omega)$），加上适当的边界条件。

### 3.2 三步走

```
Step 1: 强制性 (Coercivity)
    J[u] → ∞ 当 ‖u‖_X → ∞
    ⇒ 极小化序列 {u_n} 有界
          │
          ▼
Step 2: 弱下半连续性 (Weak Lower Semicontinuity)
    u_n ⇀ u (弱收敛) ⇒ J[u] ≤ liminf J[u_n]
    （整条序列的）
          │
          ▼
Step 3: 紧性 (Compactness)
    由 Rellich-Kondrachov，有界序列有弱收敛子序列
    u_{n_k} ⇀ u^* in X
          │
          ▼
    结合 Step 2: J[u^*] ≤ liminf J[u_{n_k}] = inf J
    ⇒ u^* 是极小值点！
```

### 3.3 Tonelli 定理：弱下半连续性的关键判据

> **Tonelli 定理**：若被积函数 $F(x, s, \xi)$ 满足：
> 1. $F$ 对 $\xi$ **凸**（convex）
> 2. $F$ 满足适当增长条件（如 $|F| \leq C(1+|s|^p+|\xi|^p)$）
>
> 则泛函 $J[u] = \int F(x, u, \nabla u)\,dx$ 在 $W^{1,p}$ 中是**弱下半连续的**。

**直觉**：凸性保证"振荡不会降低能量"。如果 $F$ 对梯度是凸的，弱收敛导致的快速振荡会使能量上升或不变，而不会下降。

### 3.4 一个完整例子

$$J[u] = \int_0^1 \left(\frac{1}{2}|u'|^2 + \frac{1}{4}u^4 - fu\right) dx, \quad u(0)=u(1)=0$$

- **强制性**：$J[u] \geq \frac{1}{2}\|u'\|_{L^2}^2 - \|f\|_{L^2}\|u\|_{L^2}$，由 Poincaré 不等式，$J[u] \to \infty$ 当 $\|u\|_{H^1} \to \infty$。✓
- **弱下半连续性**：$F(\xi) = \frac{1}{2}|\xi|^2$ 对 $\xi$ 严格凸，$u^4$ 项由紧嵌入处理。✓
- **结论**：极小值在 $H_0^1(0,1)$ 中存在。

---

## 4. 约束变分问题

### 4.1 等周问题 (Isoperimetric Problem)

**问题**：在约束 $K[y] = \int_a^b G(x, y, y')\,dx = C$ 下，极小化 $J[y] = \int_a^b F(x, y, y')\,dx$。

**解法**：引入 **Lagrange 乘子** $\lambda$，构造辅助泛函：

$$J_\lambda[y] = J[y] - \lambda K[y] = \int_a^b (F - \lambda G)\,dx$$

其 EL 方程为：

$$\boxed{\frac{\partial}{\partial y}(F - \lambda G) - \frac{d}{dx}\frac{\partial}{\partial y'}(F - \lambda G) = 0}$$

**经典例子**：固定长度的曲线围成最大面积 → 圆（Dido 问题）。

### 4.2 点态约束（非完整约束）

当约束与导数有关：$g(x, y, y') = 0$，乘子变为**函数** $\lambda(x)$：

$$\frac{\partial}{\partial y}(F + \lambda g) - \frac{d}{dx}\frac{\partial}{\partial y'}(F + \lambda g) = 0$$

### 4.3 无限维的 Lagrange 乘子定理

在 Banach 空间框架下，约束 $K[u] = 0$（$K: X \to \mathbb{R}$ 是 $C^1$ 泛函）的极小值点满足：

$$DJ[u^*] = \lambda \cdot DK[u^*]$$

这在 PDE 约束优化和最优控制中至关重要。

---

## 5. Noether 定理：对称性与守恒量

### 5.1 定理陈述

> **Noether 定理 (1918)**：作用量泛函的每一个连续对称性对应一个守恒量。

### 5.2 变分法中的形式

设 $J[y] = \int_a^b F(x, y, y')\,dx$。考虑单参数变换族：

$$x \to \bar{x}(x, y, \epsilon), \quad y \to \bar{y}(x, y, \epsilon)$$

如果 $J$ 在该变换下不变（$\delta J = 0$），则存在守恒量：

$$\boxed{\left(F - y'\frac{\partial F}{\partial y'}\right)\tau + \frac{\partial F}{\partial y'}\xi = \text{const}}$$

其中 $\tau = \left.\frac{\partial \bar{x}}{\partial \epsilon}\right|_{\epsilon=0}$，$\xi = \left.\frac{\partial \bar{y}}{\partial \epsilon}\right|_{\epsilon=0}$。

### 5.3 三个经典对应

| 对称性 | 守恒量 | 物理意义 |
|--------|--------|----------|
| $x$-平移不变（$F$ 不显含 $x$） | $F - y'F_{y'} = C$ | "能量"守恒 |
| $y$-平移不变（$F$ 不显含 $y$） | $F_{y'} = C$ | "动量"守恒 |
| 旋转不变性 | $x F_{y'} - y(F - y'F_{y'}) = C$ | 角动量守恒 |

---

## 6. 哈密顿形式与最优控制

### 6.1 从 Lagrangian 到 Hamiltonian

定义广义动量：

$$p = \frac{\partial F}{\partial y'}$$

通过 Legendre 变换定义 Hamiltonian：

$$\boxed{H(x, y, p) = p \cdot y' - F(x, y, y')}$$

其中 $y'$ 需通过 $p = \partial F/\partial y'$ 反解为 $y'(x, y, p)$。

### 6.2 哈密顿方程

EL 方程等价于**哈密顿正则方程**：

$$\boxed{\frac{dy}{dx} = \frac{\partial H}{\partial p}, \quad \frac{dp}{dx} = -\frac{\partial H}{\partial y}}$$

这是一阶方程组，在数值计算中更稳定。

### 6.3 Pontryagin 极大值原理

在最优控制中，变分法推广为 Pontryagin 极大值原理：

$$\max_{u} H(x, y, p, u) \quad \text{s.t. } \dot{y} = f(x, y, u)$$

这是现代控制论（火箭轨迹、自动驾驶）的数学基础。

---

## 7. 变分法在机器学习中的应用

### 7.1 变分推断 (Variational Inference)

贝叶斯推断中，后验 $p(z|x)$ 难以直接计算。变分推断用一族参数化分布 $q_\phi(z)$ 逼近真实后验，极小化 KL 散度：

$$J[q_\phi] = \text{KL}(q_\phi(z) \| p(z|x)) = \mathbb{E}_{q_\phi}[\log q_\phi(z) - \log p(z,x)] + \text{const}$$

这本质上是**对概率分布（函数）的泛函求极值**。ELBO（Evidence Lower Bound）的推导直接使用了变分原理。

**应用**：Variational Autoencoder (VAE)、Bayesian Neural Networks、Normalizing Flows。

### 7.2 物理信息神经网络 (PINNs)

PINNs 将 PDE 求解转化为**在神经网络参数空间中极小化泛函**：

$$J[u_\theta] = \| \mathcal{N}[u_\theta] - f\|_{L^2(\Omega)}^2 + \lambda\| \mathcal{B}[u_\theta] - g\|_{L^2(\partial\Omega)}^2$$

其中 $\mathcal{N}$ 是微分算子，$\mathcal{B}$ 是边界条件算子。极小化通过梯度下降（自动微分）完成。

> **变分视角**：PINNs 是 Ritz 方法的现代版本——用神经网络代替有限元基函数。

### 7.3 能量基模型 (Energy-Based Models)

$$J[p] = \mathbb{E}_{x\sim p}[E_\theta(x)] + H(p)$$

极小化能量泛函得到 Boltzmann 分布 $p(x) \propto e^{-E_\theta(x)}$。这是生成模型的基础。

### 7.4 最优传输 (Optimal Transport)

Monge-Kantorovich 问题：

$$J[T] = \int \|x - T(x)\|^2\,d\mu(x)$$

约束于 $T_\#\mu = \nu$。这是典型的约束变分问题，在 GAN、domain adaptation 中有广泛应用。

---

## 8. 总结：全景图

```
                    ┌──────────────────────────────────┐
                    │     变  分  法  的  全  景       │
                    └──────────────────────────────────┘
                                      │
        ┌─────────────────────────────┼─────────────────────────────┐
        │                             │                             │
        ▼                             ▼                             ▼
  古典变分法                      现代变分法                      计算方法
  (18-19世纪)                    (20世纪)                      (21世纪)
        │                             │                             │
  • Euler-Lagrange              • Sobolev 空间                • 有限元法 (FEM)
  • 最速降线/测地线              • 直接方法                     • Ritz-Galerkin
  • 最小作用量原理               • 弱收敛/下半连续性             • PINNs
  • Beltrami 恒等式             • Tonelli 定理                 • 自动微分
  • Legendre 条件               • 约束变分                     • 梯度下降
        │                       • Noether 定理                     │
        │                             │                             │
        └─────────────────────────────┼─────────────────────────────┘
                                      │
                                      ▼
                          ┌───────────────────────┐
                          │      应  用  层       │
                          ├───────────────────────┤
                          │ 物理: 经典力学/场论    │
                          │ 几何: 测地线/极小曲面  │
                          │ 工程: 最优控制/结构优化│
                          │ ML:  VAE/PINNs/OT     │
                          │ 金融: 随机最优控制     │
                          └───────────────────────┘
```

### 学习路线建议

```
泛函分析基础 (Banach/Hilbert空间)
    │
    ├── 古典变分法 (EL方程, 经典问题)
    │       │
    │       └── 阅读: Gelfand & Fomin《Calculus of Variations》
    │
    ├── 泛函的导数 (Gâteaux / Fréchet)
    │       │
    │       └── 阅读: Zeidler《Applied Functional Analysis》
    │
    ├── 现代变分法 (Sobolev空间, 直接方法)
    │       │
    │       └── 阅读: Dacorogna《Direct Methods in the Calculus of Variations》
    │
    └── 应用专题 (按兴趣选择)
            │
            ├── PDE: Evans《Partial Differential Equations》
            ├── 最优控制: Liberzon《Calculus of Variations and Optimal Control》
            ├── ML: Bishop《Pattern Recognition》Ch.10, Goodfellow et al. Ch.19
            └── 几何分析: Jost《Riemannian Geometry and Geometric Analysis》
```

---

## 延伸阅读

- [[泛函与变分法-古典问题到现代框架]] — 历史动机与基础概念
- [[泛函与变分法-导数与Euler-Lagrange]] — 泛函导数与 EL 方程的系统推导
- [[泛函与变分法的关系]] — 入门级概述
- [[对偶性 duality]] — 对偶空间与弱收敛