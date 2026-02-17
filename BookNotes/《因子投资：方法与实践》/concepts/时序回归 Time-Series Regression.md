在《因子投资》这本书中，时序回归是检验多因子模型（尤其是像 Fama-French 这种由**风格因子**构成的模型）最**直观**、最**基础**的方法。

## 1. 核心定位：因子的“试金石”

*   **适用场景**：当你手中的因子是 **“<span style="color:rgb(255, 77, 77)">可交易的投资组合</span>”**（如：SMB、HML、MOM）时。
    *   *注：如果是宏观经济指标（如 GDP 增长率、通胀率），因为它们不能直接买卖，无法使用此时序回归框架（除非先构建模拟组合）。*
*   **核心逻辑**：
    如果一个<span style="color:rgb(255, 77, 77)">模型是完美的</span>，那么资产的超额收益应该**完全**由它对因子的<span style="color:rgb(255, 77, 77)">风险暴露（$\beta$）和因子本身的收益（$\lambda$）来解释</span>。
    **剩下的 “解释不了的截距项（$\alpha$）”，应该在统计上等于 0。**

---

## 2. 数学模型 (公式 2.13)

假设我们有 $N$ 个资产，要检验 $K$ 个因子。

对**每一个**资产 $i$（$i=1, \dots, N$），我们分别做如下的线性回归：

$$ R_{it}^e = \alpha_i + \boldsymbol{\beta}_i' \boldsymbol{\lambda}_t + \varepsilon_{it} $$

### 符号拆解：
*   **$R_{it}^e$ (Y 变量)**：<span style="color:rgb(255, 77, 77)">资产 $i$ 在 $t$ 时刻的超额收益。</span>
*   **$\boldsymbol{\lambda}_t$ (X 变量)**：<span style="color:rgb(195, 117, 255)">因子在 $t$ 时刻的<b>实际收益率</b></span>（Realized Return）。
    *   *关键点：这里的 <span style="color:rgb(195, 117, 255)">$X$ 是已知的</span>、观测到的因子收益序列。*
*   **$\boldsymbol{\beta}_i$ (斜率)**：<span style="color:rgb(195, 117, 255)">资产 $i$ 对因子的风险暴露</span>。
*   **$\alpha_i$ (截距)**：**<span style="color:rgb(255, 77, 77)">定价误差 (Pricing Error)**</span>。这是我们最关心的部分！

---

## 3. 检验的灵魂：$\alpha$ 必须为 0

### (1) 单个资产检验 ($t$ 检验)

对于某一只股票或某一个组合 $i$：
*   **原假设**：$\alpha_i = 0$。
*   **含义**：如果<span style="color:rgb(195, 117, 255)"> $\alpha_i$ 显著不为 0（$t$ 值很大）</span>，说明这个<span style="color:rgb(195, 117, 255)">模型<b>失效</b>了</span>，它没能解释这只股票的收益。这只股票存在“异常收益”。

### (2) 整体模型检验 (GRS 检验)

我们不能只看某一只股票，我们要看用来测试的这 $N$ 个资产**整体**表现如何。

*   **原假设**：<span style="color:rgb(195, 117, 255)">所有资产的 $\alpha$ 同时为 0 ($\alpha<i>1 = \alpha</i>2 = \dots = \alpha_N = 0$)</span>。
*   **工具**：**GRS 统计量**（$F$ 检验）。
    *   如果 <span style="color:rgb(195, 117, 255)">GRS 检验拒绝了原假设</span>，说明<span style="color:rgb(195, 117, 255)">这个因子模型作为一个整体，不能解释这些资产的定价。</span>

---

## 4. 时序回归 vs 截面回归（书中的精彩对比）

这是第二章最容易混淆，也最显功力的地方（见书中图 2.4 和 2.6）。
![[Pasted image 20260217111316.png]]
![[Pasted image 20260217111256.png]]
**时序回归有一个“霸道”的隐含约束：**

它强制认为，**<span style="color:rgb(255, 77, 77)">因子的预期风险溢价（Risk Premium）</span> = <span style="color:rgb(255, 77, 77)">因子在历史上的平均收益率</span>（Time-series Mean）。**

*   **几何直观**：
    在“预期收益率 - Beta”的坐标图上，时序回归拟合出的直线，**<span style="color:rgb(255, 77, 77)">必须强制穿过两个点</span>**：
    1.  **<span style="color:rgb(255, 77, 77)">原点 (0, 0)**</span>：Beta 为 0 时，超额收益必须为 0。
    2.  **<span style="color:rgb(255, 77, 77)">因子点 (1, $\bar{\lambda}$)**</span>：Beta 为 1 时，预期收益必须等于因子的历史均值。

**对比截面回归：**

*   **<span style="color:rgb(255, 77, 77)">截面回归 (OLS)** 是“软”的</span>。它画出的线，<span style="color:rgb(255, 77, 77)">只要求离所有资产的距离最近</span>（最小二乘），**<span style="color:rgb(255, 77, 77)">不强制穿过原点或因子均值点</span>**。
*   **结果**：所以，截面回归算出的因子溢价（$\lambda$）往往不等于因子的历史平均收益率。

---

## 5. 操作步骤总结（实战指南）

如果你要用时序回归检验 Fama-French 三因子模型：

1.  **准备数据**：
    *   $Y$：<span style="color:rgb(255, 77, 77)">找 25 个股票组合</span>（例如按市值和账面市值比分组的组合）的月度超额收益序列。
    *   $X$：<span style="color:rgb(255, 77, 77)">下载 Fama-French 的三个因子</span>（MKT, SMB, HML）的月度收益序列。
2.  **跑回归**：
    *   对这 25 个组合，<span style="color:rgb(255, 77, 77)"><b>分别</b>跑 25 次线性回归</span>。
    *   <span style="color:rgb(255, 77, 77)">得到 25 个 $\alpha$ 和对应的 $t$ 值</span>。
3.  **下结论**：
    *   **个体**：<span style="color:rgb(255, 77, 77)">看哪些组合的 $\alpha$ 显著</span>（$t > 2$），说明模型解释不了这些特定的组合。
    *   **整体**：<span style="color:rgb(255, 77, 77)">把这 25 个 $\alpha$ 和残差矩阵放进 <b>GRS 公式</b> 算一下</span>。如果 P 值 < 0.05，遗憾地宣布：三因子模型被拒绝了（虽然它已经很优秀了，但还是有解释不了的部分）。

---

## 💡 笔记小结

*   **时序回归**是最简单、最严格的模型检验方法。
*   它的核心假设是：**<span style="color:rgb(255, 77, 77)">因子本身就是完美的定价基准</span>**（因子自己的 $\alpha$ 为 0，收益率就是风险溢价）。
*   它的<span style="color:rgb(255, 77, 77)">终极判决由 <b>GRS 检验</b> 给出</span>。