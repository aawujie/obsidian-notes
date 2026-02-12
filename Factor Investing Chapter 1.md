---
share_link: https://share.note.sx/lh2idrne#Gn8dKFZsusRn2Oq3uS7D6/IqpqZibJdNrF3RN9FPHTE
share_updated: 2026-02-12T16:09:29+08:00
---
  
  
  

《因子投资：方法与实践》第一章的核心是建立一个理解因子投资的统一视角。全章虽然涉及的公式不多，但逻辑非常严密，从最基础的CAPM模型逐步推导到了多因子矩阵以及方差模型。

  

以下是第一章中所有数学公式的详细学习笔记：

  

## 1. 资本资产定价模型 (CAPM)

**公式 (1.1)**

$$E[R_i] - R_f = \beta_i(E[R_M] - R_f)$$

  

* **符号解释：**

* $E[\cdot]$：期望符号。

* $R_i$：资产 $i$ 的收益率。

* $R_f$：无风险收益率。

* $R_M$：市场组合的预期收益率。

* $\beta_i$：资产 $i$ 对市场风险的暴露程度（或敏感程度），计算公式为 $\beta_i = cov(R_i, R_M) / var(R_M)$。

* **经济学含义：**

这是最简单的线性单因子模型。它指出，资产的预期超额收益率是由“市场组合的预期超额收益率（即市场因子）”和“资产对市场风险的暴露大小（$\beta_i$）”共同决定的。

  

---

  

## 2. 线性多因子定价模型 (由套利定价理论 APT 延伸)

**公式 (1.2)**

$$E[R_i^e] = \boldsymbol{\beta}_i' \boldsymbol{\lambda}$$

  

* **符号解释：**

* $E[R_i^e]$：资产 $i$ 的预期超额收益率。这里舍弃了 $(E[R_i] - R_f)$ 的写法，是为了更具一般性（因为对于多空对冲构建的资金中性组合，其多空预期收益之差本就无需减去无风险收益率）。

* $\boldsymbol{\beta}_i$：资产 $i$ 的因子暴露（factor exposure）或称因子载荷（factor loading）向量。

* $\boldsymbol{\lambda}$：因子预期收益（factor expected return）向量，也常被称为因子溢价（factor risk premium）。

* **经济学含义：**

该公式假设资产的预期超额收益是由多个因子的预期收益率以及资产在这些因子上的暴露程度决定的。它探讨的是**横截面（cross-sectional）差异**，即解释不同资产预期收益率的高低是由什么决定的。

  

---

  

## 3. 包含定价误差的多因子模型

**公式 (1.3)**

$$E[R_i^e] = \alpha_i + \boldsymbol{\beta}_i' \boldsymbol{\lambda}$$

  

* **符号解释：**

* $\alpha_i$：定价误差（pricing error），即资产 $i$ 的实际预期收益率和多因子模型隐含的预期收益率之间的差值。

* **经济学含义：**

在实际金融市场中，多因子模型无法完美解释所有收益，左侧和右侧往往不相等。

* 如果 $\alpha_i$ 显著偏离零，代表该资产存在可以通过套利获得超额收益的机会，也就是书中常说的**异象（anomaly）**。

* 本书就是围绕这个公式，将因子投资分为了三个部分：异象（$\alpha_i$）、因子载荷（$\boldsymbol{\beta}_i$）以及因子溢价（$\boldsymbol{\lambda}$）。

  

---

  

## 4. 时序角度下的多元线性回归模型 (单资产)

**公式 (1.4)**

$$R_{it}^e = \alpha_i + \boldsymbol{\beta}_i' \boldsymbol{\lambda}_t + \varepsilon_{it}$$

  

* **符号解释：**

* $R_{it}^e$：$t$ 时刻资产 $i$ 的超额收益。

* $\boldsymbol{\lambda}_t$：$t$ 时刻因子收益率。

* $\varepsilon_{it}$：$t$ 时刻的随机扰动项。

* **经济学含义：**

将公式(1.3)沿时间轴展开，从关注截面差异（均值模型）切换到了**时间序列（时序）角度**。它反映了每个资产的收益率随时间波动的情况，主要由因子收益率随时间的波动以及随机扰动驱动。

  

---

  

## 5. 时序角度下的多元线性回归模型 (N维矩阵化)

**公式 (1.5)**

$$\boldsymbol{R}_t^e = \boldsymbol{\alpha} + \boldsymbol{\beta} \boldsymbol{\lambda}_t + \boldsymbol{\varepsilon}_t$$

  

* **符号解释：**

* $\boldsymbol{R}_t^e = [R_{1t}^e, R_{2t}^e, \cdots, R_{Nt}^e]'$：$N$ 维超额收益向量（包含 $N$ 个资产）。

* $\boldsymbol{\alpha} = [\alpha_1, \alpha_2, \cdots, \alpha_N]'$：$N$ 维定价误差向量。

* $\boldsymbol{\beta} = [\boldsymbol{\beta}_1, \boldsymbol{\beta}_2, \cdots, \boldsymbol{\beta}_N]'$：$N \times K$ 的因子暴露矩阵（假设有 $K$ 个因子）。

* $\boldsymbol{\varepsilon}_t = [\varepsilon_{1t}, \varepsilon_{2t}, \cdots, \varepsilon_{Nt}]'$：$N$ 维随机扰动向量，满足 $E[\boldsymbol{\varepsilon}_t]=0$ 以及 $cov(\boldsymbol{\lambda}_t, \boldsymbol{\varepsilon}_t)=0$。

* **经济学含义：**

这是公式(1.4)的全局向量化表达，把市场中 $N$ 个资产放在一起考察。它是求解下一公式（方差模型）的基础。

  

---

  

## 6. 方差模型 (协方差矩阵的降维)

**公式 (1.6)**

$$\boldsymbol{\Sigma} = \boldsymbol{\beta} \boldsymbol{\Sigma}_\lambda \boldsymbol{\beta}' + \boldsymbol{\Sigma}_\varepsilon$$

  

* **推导过程：** 对公式(1.5)等号两侧求协方差矩阵，并利用 $cov(\boldsymbol{\lambda}_t, \boldsymbol{\varepsilon}_t)=0$ 得出。

* **符号解释：**

* $\boldsymbol{\Sigma}$：$N$ 个资产的协方差矩阵（$N \times N$ 阶矩阵）。

* $\boldsymbol{\Sigma}_\lambda$：$K$ 个因子的协方差矩阵（$K \times K$ 阶矩阵）。

* $\boldsymbol{\Sigma}_\varepsilon$：$N$ 个随机扰动的协方差矩阵（$N \times N$ 阶矩阵）。因为假设个股扰动相互独立，所以它是一个对角阵。

* **经济学含义（业界实务的核心）：**

* **学术界视角：** 该公式说明因子必须和资产的协方差矩阵有关。好的多因子模型的 $\boldsymbol{\beta} \boldsymbol{\Sigma}_\lambda \boldsymbol{\beta}'$ 应该尽可能接近真实资产协方差矩阵 $\boldsymbol{\Sigma}$ 的非对角线元素（即资产间的联动性）。

* **业界视角（风险控制）：** 如果直接用历史数据算 $N$ 个资产的协方差矩阵 $\boldsymbol{\Sigma}$，需要海量的数据（期数 $T \ge N$），否则矩阵不可逆，这在现实中（如A股3000多只股票）是不可能做到的。通过该公式，把求解 $N \times N$ 阶的协方差矩阵，巧妙地**降维**转化成了求解 $K \times K$ 阶的因子协方差矩阵（因子个数 $K$ 远小于资产个数 $N$），这极大简化了风险控制和投资组合优化的计算。Barra 多因子风险模型就是建立在这个公式之上的。

  
  

---

  

## 详解 $E[R_i^e] = \boldsymbol{\beta}_i' \boldsymbol{\lambda}$

  

这个公式之所以看起来像“单因子”，是因为它使用了**向量（Vector）**和**矩阵代数**的缩写形式。

  

数学上的“多因子”体现在符号的**加粗**和右上角的**转置符号 $'$** 上。

  

让我们把它“拆开”来看，你马上就会明白“多”在哪里：

  

### 1. 符号的展开

在公式 $E[R_i^e] = \boldsymbol{\beta}_i' \boldsymbol{\lambda}$ 中：

  

* **$\boldsymbol{\beta}_i$ 是一个向量（一列数）**：它不是一个单一的 $\beta$ 值，而是包含了资产 $i$ 对 $K$ 个不同因子的敏感度。

$$

\boldsymbol{\beta}_i = \begin{bmatrix}

\beta_{i,1} \\

\beta_{i,2} \\

\vdots \\

\beta_{i,K}

\end{bmatrix}

$$

*(例如：$\beta_{i,1}$是市场贝塔，$\beta_{i,2}$是规模贝塔，$\beta_{i,3}$是价值贝塔...)*

  

* **$\boldsymbol{\lambda}$ 也是一个向量（一列数）**：它代表了这 $K$ 个因子各自的预期收益率（因子溢价）。

$$

\boldsymbol{\lambda} = \begin{bmatrix}

\lambda_1 \\

\lambda_2 \\

\vdots \\

\lambda_K

\end{bmatrix}

$$

  

### 2. 运算的展开

公式中的 $\boldsymbol{\beta}_i' \boldsymbol{\lambda}$ 表示向量的**点积（Dot Product）**。

  

* $\boldsymbol{\beta}_i'$ 表示将 $\boldsymbol{\beta}_i$ 转置（变成横排）。

* 将横排的 $\boldsymbol{\beta}$ 乘以竖排的 $\boldsymbol{\lambda}$，在数学上等于：

  

$$

E[R_i^e] = [\beta_{i,1}, \beta_{i,2}, \cdots, \beta_{i,K}] \times \begin{bmatrix}

\lambda_1 \\

\lambda_2 \\

\vdots \\

\lambda_K

\end{bmatrix}

$$

  

**最终展开的代数形式为：**

  

$$

E[R_i^e] = \underbrace{\beta_{i,1}\lambda_1}_{\text{因子1贡献}} + \underbrace{\beta_{i,2}\lambda_2}_{\text{因子2贡献}} + \cdots + \underbrace{\beta_{i,K}\lambda_K}_{\text{因子K贡献}}

$$

  

### 3. 举个具体的例子（Fama-French 三因子模型）

如果这是一个三因子模型（市场、规模、价值），那么这个简短的公式实际上代表的是：

  

$$

E[R_i^e] = \beta_{i,Mkt} \cdot \lambda_{Mkt} + \beta_{i,SMB} \cdot \lambda_{SMB} + \beta_{i,HML} \cdot \lambda_{HML}

$$

  

**总结：**

数学家为了书写简洁，把后面这一长串加法公式，压缩成了 $\boldsymbol{\beta}_i' \boldsymbol{\lambda}$ 这两个字母的乘积。所以，“多因子”就隐藏在那个代表向量的**加粗字体**里。

  

---

  

## 详解 $\boldsymbol{\Sigma} = \boldsymbol{\beta} \boldsymbol{\Sigma}_\lambda \boldsymbol{\beta}' + \boldsymbol{\Sigma}_\varepsilon$

  

这个公式 **$\boldsymbol{\Sigma} = \boldsymbol{\beta} \boldsymbol{\Sigma}_\lambda \boldsymbol{\beta}' + \boldsymbol{\Sigma}_\varepsilon$** 是量化投资（特别是风险管理）中**最重要**、**最昂贵**（因为Barra等商业模型卖得很贵）的公式之一。

  

简单来说，它的核心作用是：**把一个极其复杂、几乎无法计算的数学难题，变成了一个简单可控的计算题。**

  

下面我从**推导逻辑**、**结构拆解**和**为什么需要它（核心价值）**三个方面为你细讲。

  

---

  

### 1. 为什么会有这个公式？（推导逻辑）

  

这个公式是基于第1.4节提到的**时序回归模型**推导出来的。

  

假设 $N$ 个资产在某一时刻的收益率向量 $\boldsymbol{R}$ 由两部分组成：

1. **因子驱动的部分**：$\boldsymbol{\beta} \boldsymbol{\lambda}$ （因子暴露 $\times$ 因子收益）

2. **特质（残差）部分**：$\boldsymbol{\varepsilon}$ （个股独有的波动）

  

即：

$$ \boldsymbol{R} = \boldsymbol{\beta} \boldsymbol{\lambda} + \boldsymbol{\varepsilon} $$

  

根据方差的数学性质（$Var(A+B) = Var(A) + Var(B) + 2Cov(A,B)$），我们对等式两边求**协方差矩阵（Covariance Matrix）**：

  

1. 假设因子收益 $\boldsymbol{\lambda}$ 和特质收益 $\boldsymbol{\varepsilon}$ 不相关（即 Cov项为0）。

2. $\boldsymbol{\beta}$ 被视为常数矩阵。

  

于是就得到了方差模型公式：

$$ \underbrace{\boldsymbol{\Sigma}}_{\text{资产的总风险}} = \underbrace{\boldsymbol{\beta} \boldsymbol{\Sigma}_\lambda \boldsymbol{\beta}'}_{\text{系统性风险 (因子风险)}} + \underbrace{\boldsymbol{\Sigma}_\varepsilon}_{\text{特质性风险 (残差风险)}} $$

  

---

  

### 2. 结构拆解：每一项代表什么？

  

我们假设有 **$N=3000$** 只股票（A股数量），模型选用了 **$K=10$** 个因子（如行业、市值、动量等）。

  

#### ① 左边：$\boldsymbol{\Sigma}$ (Sigma)

* **含义**：**资产协方差矩阵**。

* **形状**：$3000 \times 3000$ 的巨大矩阵。

* **作用**：它描述了这3000只股票里，任意两只股票之间是怎么一起涨跌的。这是计算投资组合风险（波动率）必须用到的数据。

  

#### ② 右边第一部分：$\boldsymbol{\beta} \boldsymbol{\Sigma}_\lambda \boldsymbol{\beta}'$ (系统性风险)

这是由**共同因子**导致的股价联动。

* **$\boldsymbol{\beta}$ ($3000 \times 10$)**：因子暴露矩阵。比如某只股票是“高波动、大市值、银行股”，这些特征就是 $\beta$。

* **$\boldsymbol{\Sigma}_\lambda$ ($10 \times 10$)**：**因子协方差矩阵**。它描述了这10个因子之间是如何互动的（例如：大盘涨的时候，小市值因子是否会跌？）。

* *注意：这里只需要计算 $10 \times 10 = 100$ 个数据，非常简单稳定。*

  

#### ③ 右边第二部分：$\boldsymbol{\Sigma}_\varepsilon$ (特质性风险)

这是剔除因子影响后，股票**自己的乱动**。

* **关键假设**：多因子模型假设，剔除共同因子后，**股票A的特质波动和股票B的特质波动互不相关**。

* **形状**：虽然它也是 $3000 \times 3000$，但因为互不相关，**只有对角线上有数字，其他全是0**（对角阵）。

* **含义**：它大大简化了计算。

  

---

  

### 3. 核心价值：为什么要用这个公式？（降维打击）

  

你可能会问：*“为什么要搞这么复杂？直接用历史数据算3000只股票的协方差矩阵不行吗？”*

  

**答案是：不行。这就是“维度灾难”。**

  

#### 直接计算的困境：

要计算 $3000 \times 3000$ 的矩阵，你需要估计 **$3000 \times 3001 / 2 \approx 450$ 万** 个不同的参数（两两之间的协方差）。

* **数据不够**：要准确估计450万个参数，你需要长达几百年的日线数据，这不可能。

* **矩阵不可逆**：如果样本天数 $T$ 小于股票数 $N$（肯定小于），算出来的矩阵数学上是“奇异”的，无法求逆，也就**无法做投资组合优化**（无法解方程算出最优权重）。

  

#### 方差模型（Barra模型）的魔法：

通过公式 $\boldsymbol{\Sigma} = \boldsymbol{\beta} \boldsymbol{\Sigma}_\lambda \boldsymbol{\beta}' + \boldsymbol{\Sigma}_\varepsilon$，我们需要估计的参数数量变成了：

1. **$\boldsymbol{\beta}$**：$3000 \times 10 = 30,000$ 个（已知或易求）。

2. **$\boldsymbol{\Sigma}_\lambda$**：$10 \times 10$ 约等于 **55** 个参数（非常容易估计）。

3. **$\boldsymbol{\Sigma}_\varepsilon$**：因为是对角阵，只需要算 **3000** 个方差。

  

**总计参数量：约 3.3 万个。**

  

**结论：**

这个公式把需要估计的参数从 **450万个** 压缩到了 **3.3万个**。

这使得我们利用有限的几年历史数据，就能算出一个**非常稳定、数学上可逆、能用于实战**的风险矩阵。

  

### 4. 直观比喻

  

想象股票是一群**木偶**。

* **直接计算 $\boldsymbol{\Sigma}$**：你试图通过观察每一对木偶（木偶A和木偶B，木偶A和木偶C...）的动作来总结它们的运动规律。这太难了，乱成一团。

* **方差模型**：你发现木偶上方有几根**提线（因子）**，还有一只**看不见的手（因子收益率矩阵 $\boldsymbol{\Sigma}_\lambda$）**在操纵提线。

* 你只需要研究这只手的动作（因子波动）；

* 以及每根线绑在木偶的哪个部位（因子暴露 $\boldsymbol{\beta}$）；

* 最后加上木偶自己随风的轻微抖动（特质风险 $\boldsymbol{\Sigma}_\varepsilon$）。

  

这样，你就能完美预测这群木偶整体的运动幅度（组合风险）了。