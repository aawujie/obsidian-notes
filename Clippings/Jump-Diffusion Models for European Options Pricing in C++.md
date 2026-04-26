---
title: "Jump-Diffusion Models for European Options Pricing in C++"
source: "https://www.quantstart.com/articles/Jump-Diffusion-Models-for-European-Options-Pricing-in-C/"
author:
published:
created: 2026-04-26
description: "Jump-Diffusion Models for European Options Pricing in C++"
tags:
  - "clippings"
---
与之前关于 [Heston 随机波动率模型](http://quantstart.com/articles/Heston-Stochastic-Volatility-Model-with-Euler-Discretisation-in-C) 的文章一样，本文将探讨布莱克-斯科尔斯模型的另一个假设，并阐述如何对其进行改进。在布莱克-斯科尔斯模型中，股票价格以 [几何布朗运动](http://quantstart.com/articles/Geometric-Brownian-Motion) 的形式演变。关键的是，这一模型支持连续的德尔塔对冲，从而能为股票的任何期权确定固定的无套利价格。

如果我们放宽几何布朗运动（GBM）的假设，引入股票价格不连续跳跃的概念，那么就无法实现完美对冲，进而导致 *市场不完全* 。这意味着期权价格仅受 *约束* ，而非固定不变。本文将探讨此类跳跃发生时期权价格所受的影响，并基于默顿（Merton）推导出的解析公式，用C++实现半闭式定价模型 [^2] 。

## 跳扩散过程建模

*本节紧密参考了 Joshi 所著书中关于跳跃扩散的 [^1] 章节，其中提供了更多理论细节。*

为了对这类股票“跳变”进行建模，我们需要满足特定条件。首先，跳变应以瞬时形式发生，忽略对冲Delta的可能性。其次，我们要求在特定时间区间内发生任何跳变的概率应大致与该时间区间的长度成正比。泊松过程 [^1] 提供了对这种情况进行建模的统计方法。

A Poisson process states the probability of an event occuring in a given time interval $\Delta t$ is given by $\lambda \Delta t + \epsilon$, where $\lambda$ is the *intensity* of the process and $\epsilon$ is an error term. The integer-valued number of events that have occured at time $t$ is given by $N \left(\right. t \left.\right)$. A necessary property is that the probability of a jump occuring is independent of the number of jumps already occured, i.e. all future jumps should have no "memory" of past jumps. The probability of $j$ jumps occuring by time $t$ is given by:泊松过程表明，在给定时间间隔 $\Delta t$ 内发生某一事件的概率由 $\lambda \Delta t + \epsilon$ 给出，其中 $\lambda$ 是过程的 *强度* ， $\epsilon$ 是误差项。在时间 $t$ 时发生的事件的整数值数量由 $N \left(\right. t \left.\right)$ 给出。一个必要的性质是，发生一次跳跃的概率与已发生的跳跃次数无关，即未来所有的跳跃都应“无记忆”过去的跳跃。到时间 $t$ 时发生 $j$ 次跳跃的概率由下式给出：

$$
\mathbb{P} \left(\right. N \left(\right. t \left.\right) = j \left.\right) = \frac{\left(\right. \lambda t \left.\right)^{j}}{j !} e^{- \lambda t}
$$

Thus, we simply need to modify our underlying GBM model for the stock via the addition of jumps. This is achieved by allowing the stock price to be multiplied by a random factor $J$:因此，我们只需通过添加跳跃项来修改股票的基础几何布朗运动（GBM）模型。这一过程通过允许股票价格乘以一个随机因子 $J$ 来实现：

$$
d S_{t} = \mu S_{t} d t + \sigma S_{t} d W_{t} + \left(\right. J - 1 \left.\right) S_{t} d N \left(\right. t \left.\right)
$$

Where dN(t) is Poisson distributed with factor $\lambda d t$.其中 dN(t) 服从参数为 $\lambda d t$ 的泊松分布。

## 跳扩散模型下的欧式期权定价

After an appropriate application of risk neutrality [^1] we have that $log ⁡ S_{T}$, the log of the final price of the stock at option expiry, is given by:在适当应用风险中性假设 [^1] 后，我们得出期权到期时股票最终价格的对数 $log ⁡ S_{T}$ 的表达式为：

$$
log ⁡ \left(\right. S_{T} \left.\right) = log ⁡ \left(\right. S_{0} \left.\right) + \left(\right. \mu + \frac{1}{2} \sigma^{2} \left.\right) T + \sigma \sqrt{T} N \left(\right. 0 , 1 \left.\right) + \sum_{j = 1}^{N \left(\right. T \left.\right)} l o g J_{j}
$$

This is all we need to price European options under a Monte Carlo framework. To carry this out we simply generate multiple final spot prices by drawing from a normal distribution and a Poisson distribution, and then selecting the $J_{j}$ values to form the jumps. However, this is somewhat unsatisfactory as we are specifically choosing the $J_{j}$ values for the jumps. Shouldn't they themselves also be random variables distributed in some manner?这就是我们在蒙特卡洛框架下为欧式期权定价所需的全部内容。要完成这一步，我们只需通过正态分布和泊松分布生成多个最终现货价格，然后选取 $J_{j}$ 值来构成跳跃项。但这种做法并不尽如人意，因为我们是\*\*特意选取\*\*了跳跃项的Jj值。这些值本身难道不也应该是服从某种分布的随机变量吗？

In 1976, Robert Merton [^2] was able to derive a semi-closed form solution for the price of European options where the jump values are themselves normally distributed. If the price of an option priced under Black-Scholes is given by $B S \left(\right. S_{0} , \sigma , r , T , K \left.\right)$ with $S_{0}$ initial spot, $\sigma$ constant volatility, $r$ constant risk-free rate, $T$ time to maturity and $K$ strike price, then in the jump-diffusion framework the price is given by [^1]:1976年，罗伯特·默顿 [^2] 推导出了欧式期权价格的半闭式解，其中跳跃值本身服从正态分布。若布莱克-斯科尔斯模型下的期权价格由 $B S \left(\right. S_{0} , \sigma , r , T , K \left.\right)$ 给出，其中 $S_{0}$ 为初始即期价格、 $\sigma$ 为恒定波动率、 $r$ 为恒定无风险利率、 $T$ 为到期时间、 $K$ 为执行价格，那么在跳跃扩散模型框架下，其价格由 [^1] 给出：

$$
\sum_{n = 0}^{\infty} \frac{e^{- \lambda^{'} T} \left(\right. \lambda^{'} T \left.\right)^{n}}{n !} B S \left(\right. S_{0} , \sigma_{n} , r_{n} , T , K \left.\right)
$$

其中

$$
\sigma_{n} & = & \sqrt{\sigma^{2} + n \nu^{2} / T} \\ r_{n} & = & r - \lambda \left(\right. m - 1 \left.\right) + n log ⁡ m / T \\ \lambda^{'} & = & \lambda m
$$

The extra parameters $\nu$ and $m$ represent the standard deviation of the lognormal jump process and the scale factor for jump intensity, respectively.额外参数 $\nu$ 和 $m$ 分别代表对数正态跳跃过程的标准差和跳跃强度的比例系数。

## C++ 实现

我们将为该模型避免采用完整的面向对象方法，因为它只是对 [欧式看涨期权的解析定价](http://quantstart.com/articles/European-vanilla-option-pricing-with-C-and-analytic-formulae) 进行了相当直接的拓展。以下是完整的代码。主要的修改包括求和循环内阶乘的计算，以及布莱克-斯科尔斯期权价格的加权求和：

```cpp
#define _USE_MATH_DEFINES

#include <iostream>
#include <cmath>

// Standard normal probability density function
double norm_pdf(const double x) {
    return (1.0/(pow(2*M_PI,0.5)))*exp(-0.5*x*x);
}

// An approximation to the cumulative distribution function
// for the standard normal distribution
// Note: This is a recursive function
double norm_cdf(const double x) {
    double k = 1.0/(1.0 + 0.2316419*x);
    double k_sum = k*(0.319381530 + k*(-0.356563782 + k*(1.781477937 + k*(-1.821255978 + 1.330274429*k))));

    if (x >= 0.0) {
        return (1.0 - (1.0/(pow(2*M_PI,0.5)))*exp(-0.5*x*x) * k_sum);
    } else {
        return 1.0 - norm_cdf(-x);
    }
}

// This calculates d_j, for j in {1,2}. This term appears in the closed
// form solution for the European call or put price
double d_j(const int j, const double S, const double K, const double r, const double v, const double T) {
    return (log(S/K) + (r + (pow(-1,j-1))*0.5*v*v)*T)/(v*(pow(T,0.5)));
}

// Calculate the European vanilla call price based on
// underlying S, strike K, risk-free rate r, volatility of
// underlying sigma and time to maturity T
double bs_call_price(const double S, const double K, const double r, 
    const double sigma, const double T) {
    return S * norm_cdf(d_j(1, S, K, r, sigma, T))-K*exp(-r*T) * 
        norm_cdf(d_j(2, S, K, r, sigma, T));
}

// Calculate the Merton jump-diffusion price based on 
// a finite sum approximation to the infinite series
// solution, making use of the BS call price.
double bs_jd_call_price(const double S, const double K, const double r, 
    const double sigma, const double T, const int N, const double m, 
    const double lambda, const double nu) {
  double price = 0.0;  // Stores the final call price
  double factorial = 1.0;

  // Pre-calculate as much as possible
  double lambda_p = lambda * m;
  double lambda_p_T = lambda_p * T;

  // Calculate the finite sum over N terms
  for (int n=0; n<N; n++) {
    double sigma_n = sqrt(sigma*sigma + n*nu*nu/T);
    double r_n = r - lambda*(m - 1) + n*log(m)/T;

    // Calculate n!
    if (n == 0) {
      factorial *= 1;
    } else {
      factorial *= n;
    }
    
    // Refine the jump price over the loop
    price += ((exp(-lambda_p_T) * pow(lambda_p_T,n))/factorial) * 
      bs_call_price(S, K, r_n, sigma_n, T);  
  }

  return price;
}

int main(int argc, char **argv) {
    // First we create the parameter list
    double S = 100.0;     // Option price
    double K = 100.0;     // Strike price
    double r = 0.05;      // Risk-free rate (5%)
    double v = 0.2;       // Volatility of the underlying (20%)
    double T = 1.0;       // One year until expiry
    int N = 50;           // Terms in the finite sum approximation
    double m = 1.083287;  // Scale factor for J
    double lambda = 1.0;  // Intensity of jumps
    double nu = 0.4;      // Stdev of lognormal jump process
 
    // Then we calculate the call jump-diffusion value
    double call_jd = bs_jd_call_price(S, K, r, v, T, N, m, lambda, nu);
    std::cout << "Call Price under JD:      " << call_jd << std::endl;

    return 0;
}
```

代码的输出结果为：

```
Call Price under JD:      18.7336
```

We can clearly see that in comparison to the Black-Scholes price of $10.4506$ given in [this article](http://quantstart.com/articles/European-vanilla-option-pricing-with-C-and-analytic-formulae), the value of the call under the jump diffusion process is much higher. This is to be expected since the jumps introduce extra volatility into the model.我们可以清楚地看到，与本文中给出的布莱克-斯科尔斯价格 $10.4506$ 相比，跳跃扩散过程下的看涨期权价值要高得多。这是意料之中的，因为跳跃给模型带来了额外的波动性。

在下一篇文章中，我们将探讨在完全面向对象的环境中，利用跳跃扩散模型对奇异期权进行定价的方法。

[^1]: \[1\] - 乔希，M. S.， *《金融数学的概念与实践》* ，剑桥大学出版社，2003年

[^2]: \[2\] - 默顿，R.， *基础股票收益不连续时的期权定价* ，《金融经济学杂志》，第3卷，1976年，第125-144页