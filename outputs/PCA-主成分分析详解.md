---
title: PCA-主成分分析详解
type: concept
created: 2026-06-05
updated: 2026-06-05
sources: [Latent Space Visualisation: PCA, t-SNE, UMAP 系列课程第3集]
tags: [PCA, 降维, 机器学习, 线性代数, 特征值分解, SVD, 数据可视化]
---

# PCA 主成分分析详解

## 概述

- **全称**: Principal Component Analysis（主成分分析）
- **提出者**: Karl Pearson（卡尔·皮尔逊），1901 年
- **本质**: 一种**线性降维**技术，通过寻找数据中方差最大的方向（主成分），将高维数据投影到低维空间
- **核心思想**: 保留数据中尽可能多的方差（信息）

## 核心概念

### 直觉理解

假设数据集有两个特征：城市规模（$X_1$）和生活成本（$X_2$）。这两个特征高度相关——城市越大，生活成本通常越高。因此数据存在冗余，可以压缩到一维。

**问题**: 如何选择最优的投影轴？

- 可以只用 $X_1$ 轴（城市规模）
- 可以只用 $X_2$ 轴（生活成本）
- 也可以选择某个倾斜的轴

**答案**: 选择**方差最大**的轴——即数据点沿该轴散布最广的方向。

> 方差越大 → 数据点区分度越高 → 保留的信息越多

### 方差作为信息度量

单个特征的方差公式：

$$\text{Var}(X) = \frac{1}{n} \sum_{i=1}^{n} (x_i - \bar{x})^2$$

- 数据点远离中心 → 方差大 → 信息量大
- 数据点聚集在中心 → 方差小 → 信息量小
- 极端情况：方差为 0，所有点在同一位置，无法区分

### 主成分（Principal Components）

- 主成分是原始特征的**线性组合**
- 这些组合捕获的信息比单个特征更多
- 主成分之间**彼此正交**（不相关），形成正交基
- 对 $N$ 维数据集，最多有 $N$ 个主成分
- 通常只保留前 $k$ 个（$k < N$）方差最大的主成分

### 碎石图（Scree Plot）

碎石图展示每个主成分的解释方差：

- 第一个主成分解释最多方差
- 后续主成分的解释方差递减
- 通过"肘部"位置选择保留的主成分数量
- 在 2D 示例中，仅保留 PC1 即可保留 90% 的信息

### 本质：基变换（Basis Transformation）

PCA 将数据从原始坐标系变换到以主成分为轴的新坐标系，涉及平移、旋转和缩放。

### 特征脸（Eigenfaces）示例

在人脸图像数据集上应用 PCA：
- 主成分称为**特征脸**（eigenfaces），对应像素空间中的特征向量
- 可以捕获人脸之间的主要变化（鼻子形状、眼睛位置等）
- 任何人脸都可以用特征脸的线性组合重建
- 如果主成分数 < 原始特征数，重建存在信息损失

## 数学原理

### 协方差矩阵（Covariance Matrix）

寻找主成分的闭式解从协方差矩阵开始。

协方差矩阵：
- **对角线**: 各变量的方差
- **非对角线**: 变量之间的协方差

两个变量之间的协方差：

$$\text{Cov}(X, Y) = \frac{1}{n} \sum_{i=1}^{n} (x_i - \bar{x})(y_i - \bar{y})$$

协方差告诉我们特征之间的关系：
- 正值 → 两个变量同向变动
- 负值 → 两个变量反向变动
- 接近零 → 变量之间关系弱

> 协方差 vs 相关性：相关性测量关系的**强度和方向**，协方差仅测量**方向**。相关性 = 归一化的协方差。

### 协方差矩阵的性质

- 协方差矩阵是**对称矩阵**（沿对角线对称）
- 根据**谱定理**（Spectral Theorem），对称矩阵总是具有实特征向量和实特征值
- 矩阵所有特征值的集合称为**矩阵谱**（spectrum）
- 每个协方差矩阵都可以**对角化**

### PCA 的核心结论

> **协方差矩阵的特征向量 = 主成分（方差最大的方向）**
> **特征值 = 该主成分的解释方差**

这是 PCA 最令人惊讶的事实。它源自优化问题（最大化投影方差或最小化投影距离），通过拉格朗日乘数法可以严格证明。

### 最大化方差 ≡ 最小化投影距离

根据毕达哥拉斯定理（勾股定理），最大化投影点的方差（蓝色）等价于最小化数据点到投影轴的距离（红色）——两者同时达到。

### 特征向量与特征值（Eigenvectors & Eigenvalues）

**特征向量**: 在线性变换下方向不变的向量。

**特征值**: 特征向量在变换中被拉伸的强度。

**特征向量方程**:

$$A \mathbf{v} = \lambda \mathbf{v}$$

将矩阵 $A$ 与特征向量 $\mathbf{v}$ 相乘，等价于将 $\mathbf{v}$ 乘以标量特征值 $\lambda$。

**直观例子**: 手臂指向空中旋转一圈——手臂是旋转变换的特征向量，因为它不改变方向。

**矩阵对角化**:

$$A = V \Lambda V^{-1}$$

其中 $V$ 是特征向量矩阵，$\Lambda$ 是特征值的对角矩阵。

### 特征值分解 vs 奇异值分解（SVD）

**特征值分解（Eigendecomposition）**:
- 复杂度: $O(n^3)$（立方级）
- 仅适用于方阵
- 核 PCA 必须使用此方法

**奇异值分解（SVD）**:
- 复杂度更低，取决于数据矩阵形状
- 适用于任意矩形矩阵
- 可直接应用于数据矩阵，无需先计算协方差矩阵
- **sklearn 等库的默认实现**（更快）

两种方法的结果相同。SVD 计算奇异值和奇异向量，对应特征值和特征向量。

## 算法步骤

### 标准 PCA 流程

**Step 1: 数据中心化（Center the Data）**

$$\mathbf{X}_{\text{centered}} = \mathbf{X} - \bar{\mathbf{X}}$$

- 减去每个特征的均值，使数据中心位于原点
- 可选：缩放到单位方差（标准化），使每个变量贡献相同
- 标准化在特征量纲不一致时**非常重要**，否则大方差特征会主导主成分

**Step 2: 计算协方差矩阵**

$$\mathbf{C} = \frac{1}{n-1} \mathbf{X}_{\text{centered}}^T \mathbf{X}_{\text{centered}}$$

协方差矩阵描述了变量间的方差和协方差关系。

**Step 3: 特征值分解**

对协方差矩阵进行特征分解：

$$\mathbf{C} = \mathbf{V} \mathbf{\Lambda} \mathbf{V}^T$$

- $\mathbf{V}$: 特征向量矩阵（列 = 主成分方向）
- $\mathbf{\Lambda}$: 特征值对角矩阵（值 = 各主成分的解释方差）

（实际实现中通常使用 SVD 代替）

**Step 4: 投影到新空间**

$$\mathbf{X}_{\text{new}} = \mathbf{X}_{\text{centered}} \mathbf{W}_k$$

- $\mathbf{W}_k$: 选择前 $k$ 个最大特征值对应的特征向量
- 结果 $\mathbf{X}_{\text{new}}$ 是 $n \times k$ 的降维数据

### 为什么主成分彼此正交

协方差矩阵是对称矩阵，对称矩阵的特征向量总是正交的，因此主成分互相垂直且不相关。PCA 将数据投影到**不相关**的基中。

## 代码实现

### sklearn 实现（推荐）

```python
from sklearn.decomposition import PCA
from sklearn.datasets import load_wine
import time

# 加载数据
wine = load_wine()
X = wine.data  # (178, 13)

# 创建 PCA 对象
pca = PCA(n_components=2)  # 降至 2 维

# 计时
start = time.time()
X_pca = pca.fit_transform(X)  # 内部使用 SVD
elapsed = time.time() - start

# 查看结果
print(f"Shape: {X_pca.shape}")  # (178, 2)
print(f"Time: {elapsed:.4f}s")

# 解释方差比
print(f"Explained variance ratio: {pca.explained_variance_ratio_}")
# 例如: [0.36, 0.19] → PC1 解释 36%，PC2 解释 19%

# 特征值
print(f"Eigenvalues: {pca.explained_variance_}")

# 主成分（特征向量）
print(f"Components: {pca.components_.shape}")  # (2, 13)
```

### NumPy 手动实现

```python
import numpy as np

# 1. 数据中心化
X_centered = X - np.mean(X, axis=0)

# 2. 计算协方差矩阵
cov_matrix = np.cov(X_centered.T)

# 3. 特征值分解
eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)

# 4. 按特征值降序排序
idx = np.argsort(eigenvalues)[::-1]
eigenvalues = eigenvalues[idx]
eigenvectors = eigenvectors[:, idx]

# 5. 选择前 k 个主成分投影
k = 2
W = eigenvectors[:, :k]
X_pca_manual = X_centered @ W
```

## 可视化方法

### 2D 散点图

```python
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(8, 6))
sns.scatterplot(x=X_pca[:, 0], y=X_pca[:, 1], hue=wine.target, palette='Set2')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.title('PCA Projection (2D)')
plt.show()
```

### 3D 可视化（ipyvolume）

```python
import ipyvolume as ipv

pca_3d = PCA(n_components=3)
X_pca_3d = pca_3d.fit_transform(X)

ipv.figure()
ipv.scatter(X_pca_3d[:, 0], X_pca_3d[:, 1], X_pca_3d[:, 2],
            color=wine.target, marker='sphere')
ipv.show()
```

### 碎石图

```python
pca_full = PCA().fit(X)
plt.plot(range(1, len(pca_full.explained_variance_ratio_) + 1),
         np.cumsum(pca_full.explained_variance_ratio_), 'o-')
plt.xlabel('Number of Components')
plt.ylabel('Cumulative Explained Variance')
plt.axhline(y=0.9, color='r', linestyle='--')
plt.show()
```

## 与其他降维技术对比

| 维度 | PCA | t-SNE | UMAP | MDS |
|------|-----|-------|------|-----|
| **类型** | 全局 | 局部 | 局部 | 全局 |
| **线性/非线性** | 线性（可扩展为核PCA） | 非线性 | 非线性 | 取决于距离度量 |
| **方法类别** | 基于投影 | 基于概率 | 基于拓扑 | 基于距离保持 |
| **主要用途** | 数据分析、可视化、去噪 | 可视化 | 可视化、聚类 | 距离可视化 |
| **确定性** | 确定性（每次结果相同） | 随机（不同运行结果不同） | 随机（不同运行结果不同） | 确定性 |
| **计算复杂度** | $O(n^3)$（特征分解）或更低（SVD） | $O(n^2)$ | 近似 $O(n \log n)$ | $O(n^2)$ |
| **超参数** | 主成分数量 | 困惑度（perplexity） | n_neighbors, min_dist | 距离度量 |
| **其他应用** | 压缩、相关分析、去噪 | 高维可视化 | 拓扑数据分析 | 心理测量学 |

### PCA 特点总结

- **全局性**: 同时考虑所有数据
- **线性**: 投影到线性主成分（核 PCA 可处理非线性）
- **确定性**: 每次运行结果相同
- **超参数**: 仅需选择主成分数量（可通过碎石图确定）
- **其他应用**: 数据压缩、去噪、相关分析

### PCA 的局限性

- 只能画直线（线性），无法处理弯曲的流形结构
- 核 PCA（Kernel PCA）是处理非线性数据的扩展，使用核函数映射数据，但它必须使用特征值分解（SVD 不能自然扩展到非线性映射）

## 参考来源

- Peter Bloem 的 PCA 博客文章
- "The Art of PCA for Data Science"
- Alex Williams 的方差-距离可视化
- scikit-learn 官方文档

## 相关笔记

- [[t-SNE 详解]] — 下一篇：t-SNE 非线性降维
- [[UMAP 详解]] — 基于拓扑的降维方法
- [[特征值分解与SVD]] — 线性代数基础
- [[协方差与相关性]] — 统计基础