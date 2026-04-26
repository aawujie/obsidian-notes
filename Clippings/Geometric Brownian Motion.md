---
title: "Geometric Brownian Motion"
source: "https://www.quantstart.com/articles/Geometric-Brownian-Motion/"
author:
published:
created: 2026-04-26
description: "Geometric Brownian Motion"
tags:
  - "clippings"
---
The usual model for the time-evolution of an asset price $S \left(\right. t \left.\right)$ is given by the geometric Brownian motion, represented by the following [stochastic differential equation](https://www.quantstart.com/articles/Stochastic-Differential-Equations):资产价格 $S \left(\right. t \left.\right)$ 时间演化的常用模型由几何布朗运动给出，其表达式为下述 [随机微分方程](https://www.quantstart.com/articles/Stochastic-Differential-Equations) ：

$$
d S \left(\right. t \left.\right) = \mu S \left(\right. t \left.\right) d t + \sigma S \left(\right. t \left.\right) d B \left(\right. t \left.\right)
$$

Note that the coefficients $\mu$ and $\sigma$, representing the *drift* and *volatility* of the asset, respectively, are both constant in this model. In more sophisticated models they can be made to be functions of $t$, $S \left(\right. t \left.\right)$ and other stochastic processes.请注意，代表资产 $\mu$ 和 *波动率* 的系数μ与 $\sigma$ 在本模型中均为常数。在更复杂的模型中，可将它们设定为 $t$ 、 $S \left(\right. t \left.\right)$ 及其他随机过程的函数。

The solution $S \left(\right. t \left.\right)$ can be found by the application of [Ito's Lemma](https://www.quantstart.com/articles/Itos-Lemma) to the stochastic differential equation.通过将 [伊藤引理](https://www.quantstart.com/articles/Itos-Lemma) 应用于随机微分方程，可以求得解 $S \left(\right. t \left.\right)$ 。

Dividing through by $S \left(\right. t \left.\right)$ in the above equation leads to:将上述方程两边同时除以 $S \left(\right. t \left.\right)$ 可得：

$$
\frac{d S \left(\right. t \left.\right)}{S \left(\right. t \left.\right)} = \mu d t + \sigma d B \left(\right. t \left.\right)
$$

Notice that the left hand side of this equation looks similar to the derivative of $log ⁡ S \left(\right. t \left.\right)$. Applying Ito's Lemma to $log ⁡ S \left(\right. t \left.\right)$ gives:请注意，该方程的左侧看起来类似于 $log ⁡ S \left(\right. t \left.\right)$ 的导数。对 $log ⁡ S \left(\right. t \left.\right)$ 应用伊藤引理可得：

$$
d \left(\right. l o g S \left(\right. t \left.\right) \left.\right) = \left(\right. l o g S \left(\right. t \left.\right) \left.\right)^{'} \mu S \left(\right. t \left.\right) d t + \left(\right. l o g S \left(\right. t \left.\right) \left.\right)^{'} \sigma S \left(\right. t \left.\right) d B \left(\right. t \left.\right) + \frac{1}{2} \left(\right. l o g S \left(\right. t \left.\right) \left.\right)^{''} \sigma^{2} S \left(\right. t \left.\right)^{2} d t
$$

由此可得：

$$
d \left(\right. l o g S \left(\right. t \left.\right) \left.\right) = \mu d t + \sigma d B \left(\right. t \left.\right) - \frac{1}{2} \sigma^{2} d t = \left(\right. \mu - \frac{1}{2} \sigma^{2} \left.\right) d t + \sigma d B \left(\right. t \left.\right)
$$

这是一个伊藤漂移扩散过程。它是带有漂移项的标准布朗运动。由于上述公式只是积分公式的简写形式，我们可以将其写为：

$$
l o g \left(\right. S \left(\right. t \left.\right) \left.\right) - l o g \left(\right. S \left(\right. 0 \left.\right) \left.\right) = \left(\right. \mu - \frac{1}{2} \sigma^{2} \left.\right) t + \sigma B \left(\right. t \left.\right)
$$

最后，对该方程取指数可得：

$$
S \left(\right. t \left.\right) = S \left(\right. 0 \left.\right) exp ⁡ \left(\right. \left(\right. \mu - \frac{1}{2} \sigma^{2} \left.\right) t + \sigma B \left(\right. t \left.\right) \left.\right)
$$

这是随机微分方程的解。事实上，它是从随机微分方程中能够得到的仅有的解析解之一。