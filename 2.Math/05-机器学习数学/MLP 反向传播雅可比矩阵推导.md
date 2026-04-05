# MLP 反向传播雅可比矩阵推导

**标签**: #深度学习 #反向传播 #雅可比矩阵 #梯度消失 #梯度爆炸
**创建日期**: 2026-03-06
**来源**: 《动手学深度学习》/《Deep Learning》(花书)

---

## 公式含义拆解

这两个公式是**多层感知机（MLP）反向传播中，层间隐藏状态的雅可比矩阵计算式**，核心是用链式法则描述"后层状态变化对前层状态的影响"。

### <span style="color:rgb(195, 117, 255)">上层公式：单步层间导数</span>

$$
\frac{\partial \mathbf{h}^t}{\partial \mathbf{h}^{t-1}} = \mathrm{diag}\left(\sigma'\left(\mathbf{W}^t \mathbf{h}^{t-1}\right)\right) \left(\mathbf{W}^t\right)^T
$$

**符号说明**：
- $\mathbf{h}^t$：<span style="color:rgb(195, 117, 255)">第 $t$ 层的隐藏状态向量</span>
- $\mathbf{h}^{t-1}$：<span style="color:rgb(195, 117, 255)">第 $t-1$ 层的隐藏状态向量</span>
- $\sigma'$：<span style="color:rgb(255, 77, 77)">激活函数 $\sigma$ 的导数</span>（比如 ReLU 的导数）
- $\mathbf{W}^t$：<span style="color:rgb(195, 117, 255)">第 $t$ 层的权重矩阵</span>，$\left(\mathbf{W}^t\right)^T$ 是它的转置
- $\mathrm{diag}(\cdot)$：**<span style="color:rgb(195, 117, 255)">对角矩阵构造操作</span>** —— <span style="color:rgb(0, 176, 240)">把输入向量的元素放在矩阵主对角线上，其余位置全为 0<br></span>
**物理意义**：描述 "<span style="color:rgb(195, 117, 255)">第 $t-1$ 层状态变一点，会让第 $t$ 层状态怎么变</span>"，这个变化率由两部分相乘：

1. $\mathrm{diag}\left(\sigma'\left(\mathbf{W}^t \mathbf{h}^{t-1}\right)\right)$：<span style="color:rgb(255, 77, 77)">激活函数的 "门控效应"</span> —— <span style="color:rgb(195, 117, 255)">只有激活后（$\sigma'>0$）的维度才会传递变化</span>
2. $\left(\mathbf{W}^t\right)^T$：权重矩阵的转置，<span style="color:rgb(195, 117, 255)">代表信息沿权重连接反向传播</span>

---

### <span style="color:rgb(255, 77, 77)">下层公式：多步层间导数累积</span>

$$
\prod_{i=t}^{d-1} \frac{\partial \mathbf{h}^{i+1}}{\partial \mathbf{h}^i} = \prod_{i=t}^{d-1} \mathrm{diag}\left(\sigma'\left(\mathbf{W}^i \mathbf{h}^{i-1}\right)\right) \left(\mathbf{W}^i\right)^T
$$

**符号说明**：
- $\prod$：累乘符号，<span style="color:rgb(255, 77, 77)">从第 $t$ 层一直乘到第 $d-1$ 层（$d$ 是网络总层数）</span>
- 本质：<span style="color:rgb(195, 117, 255)">把<b>从第 $t$ 层到输出层前一层</b>的所有单步导数连乘起来</span>

**物理意义**：描述 "<span style="color:rgb(195, 117, 255)">最底层（第 $t$ 层）的状态变化，最终会怎么影响最顶层（输出层前一层）的状态</span>"，是反向传播中梯度跨层传递的核心计算式。

---

## 为什么要用 $\mathrm{diag}$（对角矩阵）？

$\mathrm{diag}$ 在这里是**数学上的简洁写法**，解决两个关键问题：

1. **<span style="color:rgb(195, 117, 255)">逐元素激活的导数特性</span>**：<span style="color:rgb(255, 77, 77)">激活函数 $\sigma$ 是对向量每个元素独立作用的</span>（比如 $\sigma([x_1,x_2])=[\sigma(x_1),\sigma(x_2)]$），<span style="color:rgb(255, 77, 77)">它的导数天然是 "逐元素相乘"</span>，<span style="color:rgb(255, 77, 77)">用对角矩阵就能把逐元素乘法转化为矩阵乘法</span>，<span style="color:rgb(195, 117, 255)">和后面的权重转置矩阵对齐运算<br></span>
2. **<span style="color:rgb(195, 117, 255)">保持矩阵乘法结构</span>**：反向传播的梯度流本质是矩阵连乘，<span style="color:rgb(195, 117, 255)">$\mathrm{diag}$ 让激活导数部分也变成矩阵，完美嵌入链式法则的矩阵乘法框架</span>，不用额外写复杂的逐元素运算

---

## 公式出处

这类推导是**深度学习经典教材**的核心内容，典型出处包括：

- 📘 **《Deep Learning》**（Ian Goodfellow 等著，俗称"花书"）：第 6 章「深度前馈网络」详细推导了反向传播的雅可比矩阵形式
- 📘 **《动手学深度学习》**（李沐 等著）：第 5 章「深度学习计算」讲解了数值稳定性、梯度消失/爆炸时，会用这个公式分析累乘带来的数值问题
- 📘 **《Neural Networks and Deep Learning》**（Michael Nielsen 著）：用更直观的方式推导了反向传播的矩阵形式

---

## 和梯度爆炸/消失的关系

当网络层数很多（$d-t$ 很大）时，这个累乘式会出现数值问题：

| 情况 | 条件 | 结果 |
|------|------|------|
| **梯度爆炸** | 权重矩阵 $\mathbf{W}^i$ 的范数 > 1 | 累乘让梯度值指数级增长 |
| **梯度消失** | 权重矩阵范数 < 1 | 累乘让梯度值指数级衰减 |

这也是为什么深度学习早期训练深层网络困难，后来需要以下技术来缓解的核心原因：

- **残差连接（ResNet）**：通过跳跃连接绕过累乘
- **层归一化（LayerNorm）**：控制每层输出的尺度
- **Xavier/He 初始化**：让初始权重范数接近 1
- **ReLU 及其变体**：缓解梯度消失（导数不为 0）

---

## 相关笔记

- [[反向传播算法]]
- [[梯度消失与梯度爆炸]]
- [[神经网络基础]]
- [[激活函数对比]]

---

*笔记整理自课程讲解，用于理解反向传播的矩阵形式推导。*
