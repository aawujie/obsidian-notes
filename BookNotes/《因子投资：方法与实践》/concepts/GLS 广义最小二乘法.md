---
share_link: https://share.note.sx/jw3bhgg1#HKrWPKnev3ysJ1wxZF2ymKRS8DGTvtEBwoj723vWQkk
share_updated: 2026-02-15T13:56:13+08:00
---
在《因子投资：方法与实践》第二章第二节中，**广义最小二乘法（Generalized Least Squares, GLS）** 是作为 **截面回归（Cross-sectional Regression）** 的高级估计手段出现的。

如果说 **OLS（普通最小二乘法）** 是 “**<span style="color:rgb(255, 77, 77)">一视同仁</span>**” 地对待所有资产，那么 **GLS** 就是一个 “**<span style="color:rgb(255, 77, 77)">带有偏好的</span>**智者”，<span style="color:rgb(255, 77, 77)">它会根据资产之间的相关性和波动大小来调整自己的判断权重</span>。

以下是为您整理的 GLS 深度学习笔记：

---

## 1. 核心动机：为什么要替代 OLS？

在多因子模型的截面回归中，我们用<span style="color:rgb(195, 117, 255)">资产收益率</span>对<span style="color:rgb(195, 117, 255)">因子的风险暴露（$\beta$）</span>做回归。

*   **OLS 的缺陷**：OLS 假设不同资产的定价误差（残差 $\alpha_i$）是<span style="color:rgb(195, 117, 255)">**相互独立</span>**且**<span style="color:rgb(195, 117, 255)">方差相等**的</span>。
*   **现实情况**：股票之间存在复<span style="color:rgb(255, 77, 77)">杂的**截面相关性</span>**（例如：属于同一行业的股票往往一起涨跌）。
*   **后果**：如果忽略这种相关性直接用 OLS，算出来的参数估计值虽是无偏的，但<span style="color:rgb(255, 77, 77)"><b>标准误（Standard Error）会存在巨大误差</b></span>（通常会被低估），导致你得出的 $t$ 统计量虚高，误以为因子很显著。

---

## 2. 数学表达与逻辑 (公式 2.26)

GLS 的核心是引入了**<span style="color:rgb(255, 77, 77)">资产残差的协方差矩阵 $\Sigma$** </span>来作为**<span style="color:rgb(195, 117, 255)">“权重”**</span>。

**GLS 估计量公式：**
$$\hat{\lambda}_{GLS} = (\boldsymbol{\beta}' \boldsymbol{\Sigma}^{-1} \boldsymbol{\beta})^{-1} \boldsymbol{\beta}' \boldsymbol{\Sigma}^{-1} E_T[\boldsymbol{R}^e]$$

*   **符号解释：**
    *   $\boldsymbol{\beta}$：因子暴露矩阵。
    *   $\boldsymbol{\Sigma}^{-1}$：**关键点！** 资产残差协方差矩阵的逆。
    *   $E_T[\boldsymbol{R}^e]$：资产的平均超额收益。

*   **逻辑拆解：**
    *   公式中夹杂着 $\boldsymbol{\Sigma}^{-1}$，本质上是进行了一次 **<span style="color:rgb(195, 117, 255)">“去相关” 和 “降噪”</span>** 的处理。
    *   **权重分配**：**<span style="color:rgb(195, 117, 255)">波动大（噪声多）或者与其他资产高度相关的资产，在计算中所占的权重会被调低</span>**；反之，**<span style="color:rgb(195, 117, 255)">独立、稳定的资产权重更高</span>**。

---

## 3. 定价误差与显著性检验

使用 GLS 后，我们可以得到更严谨的定价误差估计：

*   **定价误差 (公式 2.27)**：$\hat{\alpha}_{GLS} = E_T[\boldsymbol{R}^e] - \boldsymbol{\beta} \hat{\lambda}_{GLS}$
*   **联合检验 (公式 2.31)**：通过构建 $\chi^2$（卡方）统计量，联合检验所有资产的 $\alpha$ 是否为 0。

**注意（Shanken 修正）**：

书中特别提到（公式 2.29），由于 $\beta$ 是第一步回出来的估计值而非真实值，在计算 GLS 的标准误时，必须包含 $(1 + \boldsymbol{\lambda}' \boldsymbol{\Sigma}_f^{-1} \boldsymbol{\lambda})$ 这一项进行修正。

---

## 4. 形象比喻：老师批改作文

假设<span style="color:rgb(195, 117, 255)">老师（回归模型）</span>要通过<span style="color:rgb(195, 117, 255)">几篇作文（资产收益）</span>来评估<span style="color:rgb(195, 117, 255)">学生的真实水平（因子溢价 $\lambda$）</span>：

*   **OLS 批改法**：老师认为每篇作文都是独立的，平均打个分。但如果学生有两篇作文是<span style="color:rgb(0, 176, 240)">抄袭同一个模板的（截面相关）</span>，<span style="color:rgb(0, 176, 240)">老师还按两篇算，就会给高分（显著性虚高）</span>。
*   **GLS 批改法**：老师<span style="color:rgb(0, 176, 240)">先研究了作文之间的关系（计算 $\boldsymbol{\Sigma}$）</span>。他发现<span style="color:rgb(0, 176, 240)">有几篇内容高度雷同</span>，于是<span style="color:rgb(0, 176, 240)">降低了这几篇的权重</span>；他发现<span style="color:rgb(0, 176, 240)">某篇作文写得特别乱（波动大），也降低了权重。</span>
*   **结果**：GLS 老师给出的评分（$\hat{\lambda}$）更接近真实水平。

---

## 5. OLS 与 GLS 的关键选择

书中第 2.2.3 节和 2.2.5 节给出了实战建议：

1.  **什么时候用 GLS？** 当你非常<span style="color:rgb(255, 77, 77)">看重统计推断的**有效性（Efficiency）</span>**，<span style="color:rgb(255, 77, 77)">且能够较好地估计 $\boldsymbol{\Sigma}$ 矩阵时</span>。
2.  **现实挑战**：如果资产数量 $N$ 很大，准确估计 $N \times N$ 阶的 $\boldsymbol{\Sigma}$ 矩阵非常困难。<span style="color:rgb(255, 77, 77)">如果 $\boldsymbol{\Sigma}$ 估得不准，GLS 反而可能弄巧成拙。</span>
3.  **结论**：在很多学术研究中，为了简单稳健，研究者有时仍会<span style="color:rgb(255, 77, 77)">使用 OLS</span>，但会<span style="color:rgb(255, 77, 77)">配合更高级的标准误计算方法（如 Newey-West 调整）来修正相关性问题。</span>

---

## 💡 总结给你的笔记卡片：

*   **OLS** = 简单、直观，但容易在相关性数据面前 “盲目自信”。
*   **GLS** = 严谨、高效，利用残差协方差矩阵 $\boldsymbol{\Sigma}$ <span style="color:rgb(195, 117, 255)">消除截面相关性的干扰</span>。
*   **核心动作**：<span style="color:rgb(195, 117, 255)">通过 $\boldsymbol{\Sigma}^{-1}$ 对数据进行“加权”</span>，让噪声小、独立性强的资产说更大的话。