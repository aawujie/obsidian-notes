# SVM 支持向量机详解

> 核心问题：给定两类数据点，找一条线（或超平面）把它们分开——但不止于分开，要分得最"稳"。

---
type: concept
created: 2026-04-29
updated: 2026-04-29
tags: [ML, 分类算法, SVM, 核方法]
---

## 直觉：什么是"最好的"分界线？

下图是同一份数据的三条分界线，哪条最好？

```mermaid
graph TD
    subgraph "A: 贴着红点"
        A1[太近, 泛化差]
    end
    subgraph "B: 居中, 间隔最大"
        B1[最稳 ★]
    end
    subgraph "C: 贴着蓝点"
        C1[太近, 泛化差]
    end
```

**SVM 的答案**：找一条线，让它离最近的样本点**尽可能远**——这个距离叫**间隔（margin）**。

直观类比：你在两张纸之间放一本书 vs 放一根头发丝。书明显更稳，新纸片进来也不容易碰到边界。SVM 就是在找"书"的厚度。

## 核心概念

### 超平面（Hyperplane）

$d$ 维空间中的一个 $d-1$ 维平面：

$$
\mathbf{w}^T\mathbf{x} + b = 0
$$

- $\mathbf{w}$：法向量，决定方向
- $b$：偏置，决定位置
- 分类规则：$\mathbf{w}^T\mathbf{x} + b > 0$ → 正类，否则负类

### 支持向量（Support Vector）

离超平面**最近**的那些训练样本。关键性质：

> **只有支持向量决定了超平面的位置。** 其他所有点删掉都不影响结果。

这是 SVM 和逻辑回归的本质区别——逻辑回归用所有点拟合，SVM 只用边界上的点。

### 间隔（Margin）

支持向量到超平面的距离 × 2：

$$
\text{margin} = \frac{2}{\|\mathbf{w}\|}
$$

SVM 目标：**最大化** $\frac{2}{\|\mathbf{w}\|}$，等价于**最小化** $\|\mathbf{w}\|^2$。

## 数学推导

### 硬间隔 SVM（数据线性可分）

**优化问题（primal form）**：

$$
\begin{aligned}
\min_{\mathbf{w}, b} \quad & \frac{1}{2}\|\mathbf{w}\|^2 \\
\text{s.t.} \quad & y_i(\mathbf{w}^T\mathbf{x}_i + b) \geq 1, \quad \forall i
\end{aligned}
$$

- 目标：最小化 $\|\mathbf{w}\|$ → 最大化间隔
- 约束：每个点都分对，且离超平面至少距离 1

### 为什么约束是 $y_i(\mathbf{w}^T\mathbf{x}_i + b) \geq 1$？

- $y_i \in \{-1, +1\}$
- 正确分类时，$y_i$ 和 $\mathbf{w}^T\mathbf{x}_i + b$ 同号，乘积 > 0
- 加上 ≥ 1 的约束，确保点在 margin 之外

### 对偶问题（Dual Form）

引入拉格朗日乘子 $\alpha_i \geq 0$：

$$
\begin{aligned}
\max_{\alpha} \quad & \sum_{i=1}^n \alpha_i - \frac{1}{2}\sum_{i=1}^n\sum_{j=1}^n \alpha_i\alpha_j y_i y_j (\mathbf{x}_i^T\mathbf{x}_j) \\
\text{s.t.} \quad & \alpha_i \geq 0, \quad \sum_{i=1}^n \alpha_i y_i = 0
\end{aligned}
$$

**为什么用对偶形式？**
1. 解出来 $\alpha_i > 0$ 的点就是**支持向量**（大部分 $\alpha_i = 0$，稀疏解）
2. 只依赖样本间的**内积** $\mathbf{x}_i^T\mathbf{x}_j$——为核函数埋下伏笔

最终分类函数：

$$
f(\mathbf{x}) = \text{sign}\left(\sum_{i \in SV} \alpha_i y_i (\mathbf{x}_i^T\mathbf{x}) + b\right)
$$

只对支持向量（$\alpha_i > 0$）求和。

## 核函数（Kernel Trick）

现实中的数据往往线性不可分：

```mermaid
flowchart LR
    A["2D 环形数据<br/>(线性不可分)"] -->|"φ(x) 映射"| B["3D 空间<br/>(线性可分)"]
```

**核函数**直接算高维空间的内积，不需要显式做映射：

$$
K(\mathbf{x}_i, \mathbf{x}_j) = \phi(\mathbf{x}_i)^T\phi(\mathbf{x}_j)
$$

| 核函数 | 公式 | 适用场景 |
|--------|------|----------|
| 线性 | $K(x_i, x_j) = x_i^T x_j$ | 高维稀疏数据（文本） |
| 多项式 | $K(x_i, x_j) = (x_i^T x_j + c)^d$ | 有多项式关系 |
| **RBF（高斯）** | $K(x_i, x_j) = e^{-\gamma\|x_i-x_j\|^2}$ | **最常用**，无限维映射 |
| Sigmoid | $K(x_i, x_j) = \tanh(\kappa x_i^T x_j + c)$ | 类似神经网络 |

**RBF 核的直觉**：把每个样本变成一个高斯"小山"，所有山叠在一起形成决策边界。$\gamma$ 控制山的宽度——$\gamma$ 大 → 山窄 → 边界曲折（过拟合）；$\gamma$ 小 → 山宽 → 边界平滑（欠拟合）。

## 软间隔（Soft Margin）

真实数据总有噪声，强行完美分开反而过拟合。引入**松弛变量** $\xi_i \geq 0$：

$$
\begin{aligned}
\min_{\mathbf{w}, b, \xi} \quad & \frac{1}{2}\|\mathbf{w}\|^2 + C\sum_{i=1}^n \xi_i \\
\text{s.t.} \quad & y_i(\mathbf{w}^T\mathbf{x}_i + b) \geq 1 - \xi_i, \quad \xi_i \geq 0
\end{aligned}
$$

- $\xi_i$：第 $i$ 个点"犯规"的程度（跑到 margin 里面或分错）
- **$C$**：惩罚系数——**SVM 最重要的超参数**
  - $C$ 大 → 严格要求分对 → margin 窄 → 容易过拟合
  - $C$ 小 → 容忍错误 → margin 宽 → 泛化好

---

## 实战：完整 sklearn 例子

### 问题设定

用 sklearn 生成一个非线性可分的数据集（同心圆），对比线性 SVM vs RBF SVM。

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.datasets import make_circles, make_moons
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler

# ============================================
# 1. 生成数据：同心圆（线性不可分）
# ============================================
X, y = make_circles(n_samples=500, noise=0.1, factor=0.4, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# SVM 对特征尺度敏感，必须先标准化
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# ============================================
# 2. 训练三个模型对比
# ============================================
models = {
    "Linear SVM": SVC(kernel="linear", C=1.0),
    "RBF SVM (C=1, γ=1)": SVC(kernel="rbf", C=1.0, gamma=1.0),
    "RBF SVM (C=10, γ=5)": SVC(kernel="rbf", C=10.0, gamma=5.0),
}

fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))

for ax, (name, model) in zip(axes, models.items()):
    model.fit(X_train, y_train)

    # 画决策边界
    xx, yy = np.meshgrid(
        np.linspace(X_train[:, 0].min() - 0.5, X_train[:, 0].max() + 0.5, 300),
        np.linspace(X_train[:, 1].min() - 0.5, X_train[:, 1].max() + 0.5, 300),
    )
    Z = model.decision_function(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    ax.contourf(xx, yy, Z, levels=[-1, 0, 1], alpha=0.3, colors=["#ff9999", "#9999ff"])
    ax.contour(xx, yy, Z, levels=[0], colors="black", linewidths=1.5)  # 决策边界
    ax.contour(xx, yy, Z, levels=[-1, 1], colors="black", linestyles="dashed", linewidths=0.8)  # margin

    # 标出支持向量
    ax.scatter(model.support_vectors_[:, 0], model.support_vectors_[:, 1],
               s=80, facecolors="none", edgecolors="green", linewidths=1.5, label=f"SV={len(model.support_vectors_)}")

    ax.scatter(X_train[:, 0], X_train[:, 1], c=y_train, cmap="RdBu", alpha=0.6, s=20)
    ax.set_title(f"{name}\nTest Acc: {model.score(X_test, y_test):.3f}")
    ax.legend(fontsize=8)

plt.tight_layout()
plt.savefig("svm_comparison.png", dpi=150, bbox_inches="tight")
plt.show()

# ============================================
# 3. 超参数调优：GridSearchCV
# ============================================
param_grid = {
    "C": [0.1, 1, 10, 100],
    "gamma": [0.01, 0.1, 1, 5, 10],
}
grid = GridSearchCV(SVC(kernel="rbf"), param_grid, cv=5, scoring="accuracy")
grid.fit(X_train, y_train)

print(f"Best params: {grid.best_params_}")
print(f"Best CV score: {grid.best_score_:.3f}")
print(f"Test score: {grid.best_estimator_.score(X_test, y_test):.3f}")

# ============================================
# 4. 最终评估
# ============================================
best_model = grid.best_estimator_
y_pred = best_model.predict(X_test)
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=["Class 0", "Class 1"]))
```

### 运行结果解读

```
Best params: {'C': 10, 'gamma': 1}
Best CV score: 0.888
Test score: 0.890

Classification Report:
              precision    recall  f1-score   support
     Class 0       0.91      0.86      0.88        50
     Class 1       0.87      0.92      0.89        50
```

关键观察：
- **Linear SVM** 在同心圆上几乎等于乱猜（~50%），因为它只能在二维画直线
- **RBF SVM** 把数据映射到高维后轻松分开（~89%+）
- $\gamma=5$ 时边界过度弯曲，支持向量暴增 → 过拟合信号
- GridSearchCV 找到了最优的 C 和 $\gamma$

### 支持向量数目的含义

| 现象 | 诊断 |
|------|------|
| SV 数量 ≈ 训练集大小 | C 太大或 $\gamma$ 太大 → **过拟合** |
| SV 数量很少 | C 太小 → **欠拟合** |
| SV 数量适中 | 泛化好 |

---

## SVM 面试要点

### 必会推导
1. 写出硬间隔 SVM 的 primal 优化问题（目标 + 约束）
2. 解释为什么最小化 $\|\mathbf{w}\|^2$ = 最大化 margin
3. 写出对偶形式，说明为什么引入对偶（核函数 + 稀疏性）
4. 解释软间隔中 $C$ 的含义和影响

### 必会概念
- 支持向量的定义和作用
- RBF 核为什么能处理非线性
- $\gamma$ 和 $C$ 的调参方向
- SVM vs 逻辑回归的区别（决策边界来源不同：所有点 vs 支持向量）

### 常见追问
- "SVM 为什么要做特征标准化？" → 因为 $\|\mathbf{w}\|$ 对尺度敏感，量纲不统一会扭曲 margin
- "SVM 能输出概率吗？" → 原生不能，但可以加 Platt scaling（`SVC(probability=True)`）
- "SVM 适合什么场景？" → 小样本、高维数据（文本分类）；不适合大数据集（$O(n^2)$~$O(n^3)$ 复杂度）
