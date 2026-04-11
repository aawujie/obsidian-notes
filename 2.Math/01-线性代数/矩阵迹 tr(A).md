# 矩阵迹 tr(A)

## 定义

矩阵的**迹（trace）** 是方阵主对角线元素之和：

$$\text{tr}(A) = \sum_{i} A_{ii} = A_{11} + A_{22} + \cdots + A_{nn}$$

## 例子

$$A = \begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix} \Rightarrow \text{tr}(A) = 1 + 4 = 5$$

$$B = \begin{pmatrix} 3 & 0 & 1 \\ 2 & -1 & 4 \\ 0 & 5 & 2 \end{pmatrix} \Rightarrow \text{tr}(B) = 3 + (-1) + 2 = 4$$

## 常用性质

| 性质 | 公式 |
|------|------|
| 线性 | $\text{tr}(A+B) = \text{tr}(A) + \text{tr}(B)$ |
| 数乘 | $\text{tr}(cA) = c\,\text{tr}(A)$ |
| 转置不变 | $\text{tr}(A) = \text{tr}(A^T)$ |
| 乘积交换 | $\text{tr}(AB) = \text{tr}(BA)$（即使 $AB \neq BA$） |
| 特征值之和 | $\text{tr}(A) = \sum_{i} \lambda_i$ |

## 与特征值的关系

迹等于所有特征值之和，行列式等于所有特征值之积：

$$\text{tr}(A) = \lambda_1 + \lambda_2 + \cdots + \lambda_n$$
$$\det(A) = \lambda_1 \cdot \lambda_2 \cdots \lambda_n$$

## 重要性质（补充）

| 性质 | 公式 | 说明 |
|------|------|------|
| 相似不变性 | $\text{tr}(P^{-1}AP) = \text{tr}(A)$ | 相似矩阵有相同的迹 |
| 循环性（一般形式） | $\text{tr}(ABC) = \text{tr}(BCA) = \text{tr}(CAB)$ | 循环置换不变，但 $\text{tr}(ACB) \neq \text{tr}(ABC)$ 一般 |
| 幂的迹 | $\text{tr}(A^k) = \sum_{i} \lambda_i^k$ | 与特征值的幂和相关 |
| 迹与秩 | $\text{tr}(I_n) = n$ | 单位矩阵的迹等于维度 |

## 应用场景

### 机器学习
- **正则化项**：Ridge 回归中 $\text{tr}(X^TX)$ 用于惩罚模型复杂度
- **PCA**：协方差矩阵的迹表示总方差，特征值分解保留最大迹的方向
- **矩阵范数**：Frobenius 范数 $\|A\|_F = \sqrt{\text{tr}(A^TA)}$

### 量子力学
- **密度矩阵**：$\text{tr}(\rho) = 1$（概率归一化）
- **期望值**：可观测量 $A$ 的期望 $\langle A \rangle = \text{tr}(\rho A)$
- **迹运算**：部分迹用于描述子系统

### 图论
- **邻接矩阵**：$\text{tr}(A) = 0$（简单图无自环）
- **环的数量**：$\text{tr}(A^k)$ 等于长度为 $k$ 的闭途径数量

### 微分几何
- **度量张量**：迹用于缩并张量
- **Ricci 曲率**：由 Riemann 曲率张量缩并得到

## 相关概念

- [[特征值与特征向量]]
- [[行列式 det(A)]]
