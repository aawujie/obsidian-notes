---
title: Every Market Has A Memory — Hurst Exponent
type: article
created: 2026-05-26
updated: 2026-05-26
sources:
  - https://x.com/phosphenq/status/2058997465433432550
  - https://x.com/i/article/2058990571981619200
tags:
  - 量化金融
  - 时间序列
  - 技术分析
  - 趋势识别
---

# Every Market Has A Memory & It Decides Whether Prices Trend Or Snap Back

**作者：** Phosphen (@phosphenq)
**日期：** 2026-05-25
**链接：** https://x.com/phosphenq/status/2058997465433432550

## 摘要

Every price series is secretly one of three things: trending, mean-reverting, or pure noise. This breakdown hands you the single number that tells you which, the Python to measure it in about forty lines, and the mental model to use it without lying to yourself.

## 背景：赫斯特指数 (Hurst Exponent)

赫斯特指数 H 衡量时间序列的长期记忆性：

| H 值 | 行为 | 含义 |
|:---|:---|:---|
| H < 0.5 | 均值回归 | 价格倾向于回弹到平均值 |
| H = 0.5 | 随机游走 | 无记忆，纯随机 |
| H > 0.5 | 趋势持续 | 价格趋势有持续性/动量 |

### 常见计算方法

1. **R/S 分析 (Rescaled Range)**
   - 最经典的方法
   - 计算 (R/S) ∝ n^H，对数回归求斜率
   
2. **方差标度法 (Variance Scaling)**
   - 利用 Var(X_t − X_0) ∝ t^{2H}
   - 计算效率更高

3. **DFA (Detrended Fluctuation Analysis)**
   - 去除趋势后分析波动标度
   - 适用于非平稳序列

### Python 实现（约40行）

```python
import numpy as np
import pandas as pd

def hurst_exponent(series, max_lag=100):
    """
    Calculate Hurst exponent using R/S analysis.
    H < 0.5: mean-reverting
    H = 0.5: random walk
    H > 0.5: trending
    """
    series = np.asarray(series)
    lags = range(2, min(max_lag, len(series)//2))
    
    rs_values = []
    for lag in lags:
        diff = series[lag:] - series[:-lag]
        r = np.max(diff) - np.min(diff)
        s = np.std(series[:lag])
        if s > 0:
            rs_values.append(r / s)
    
    lag_values = np.log(list(lags))
    rs_values = np.log(rs_values)
    
    hurst = np.polyfit(lag_values, rs_values, 1)[0]
    return hurst

# 使用
# prices = pd.Series(...)
# H = hurst_exponent(prices.values)
# print(f"Hurst = {H:.3f}")
```

### 交易含义

- **H < 0.5** → 均值回归策略：买跌卖涨
- **H > 0.5** → 趋势跟踪策略：追涨杀跌
- **H ≈ 0.5** → 不要交易，纯噪音

> 市场有记忆。赫斯特指数告诉你它记住了什么。

## 注意

⚠️ 文章正文为 Twitter/X Article（JS 渲染），尚未完整抓取。以上内容基于标题、摘要和相关文献整理。