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

> 待补充：迹在 PCA / 协方差矩阵中的几何意义（等有特征值的背景后再加图）

## 相关概念

- [[特征值与特征向量]]
- [[行列式 det(A)]]
