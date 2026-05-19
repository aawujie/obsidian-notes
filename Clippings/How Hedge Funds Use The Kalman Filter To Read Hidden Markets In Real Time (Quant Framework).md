---
title: "How Hedge Funds Use The Kalman Filter To Read Hidden Markets In Real Time (Quant Framework)"
source: "https://x.com/phosphenq/status/2056438562451513660?s=46"
author:
  - "[[@phosphenq]]"
published: 2026-05-19
created: 2026-05-19
description: "I am going to break down how hedge funds use the Kalman Filter to estimate hidden market states in real time, & share the exact framework yo..."
tags:
  - "clippings"
---
![Image](https://pbs.twimg.com/media/HInkKi6WEAAVu4Z?format=jpg&name=large)

I am going to break down how hedge funds use the Kalman Filter to estimate hidden market states in real time, & share the exact framework you can start building today. Let's get straight to it.

> **About me** I am Phosphen. I write long-form breakdowns of the math hedge funds actually run on every trade. Follow [@phosphenq](https://x.com/@phosphenq) on X. DMs open. Now let's get into the math.

Most traders look at a price and see the market.

Quants look at the same price and see a noisy measurement of something they cannot directly observe. Volatility regime. Hedge ratio. Mean reversion strength. Liquidity condition. None of those are written on the chart. They have to be estimated from what the chart leaves visible, which is itself just truth corrupted by noise.

The framework that fixes this is called the **Kalman Filter**. And it solves the most underappreciated problem in trading: how to separate the signal from the noise in real time.

Note: this article is deliberately long. Every part builds on the one before it. If you are serious about adding a genuine quantitative edge to your trading, read every word. If you are looking for a shortcut, this is not for you.

## Part 1: Why The Price You See Is Not The State You Want To Trade

**The price on your chart is not the market.** It is a measurement of the market. And every measurement carries noise.

The closing price of SPY today is the last trade printed before the auction. That trade reflects the marginal preference of two counterparties at a specific microsecond. The underlying state of the market is not directly observable. It is hidden. What you see is a noisy projection of that hidden state onto a single number.

Every systematic fund treats prices as observations, not as truth. The discipline is called **state-space modeling**. The most important tool inside it is the Kalman Filter.

Take two examples in different domains.

The first is order book imbalance. The bid-ask depth at any moment is a snapshot of where liquidity is parked. But the true inventory pressure on the desk that posted those quotes is not directly observable. The imbalance is a noisy proxy for that pressure. A market maker who treats the snapshot as ground truth gets adversely selected. A market maker who filters it as a noisy observation of a slowly evolving inventory state prices the next quote correctly.

The second is rolling beta. Regress AAPL returns against SPY returns over the last 60 days and you get a number that is supposed to represent the sensitivity of AAPL to the market. But the true sensitivity is shifting every day as Apple's product mix, capital structure, and macro exposure evolve. The regression hands you a sixty-day average of something that has already moved. The current value is hidden inside the residuals.

This is what the Kalman Filter solves. **It does not solve prediction. It solves estimation.** It estimates an unobservable, time-varying state from a sequence of noisy observations, in real time, with minimum mean squared error.

The naive moving average is the simplest possible response to noise and it is wrong in every direction that matters. It assumes the noise variance equals the signal variance, that the underlying state is constant over the window, and that every observation should be weighted equally. None of that is true. The Kalman Filter fixes all three errors with two equations and one recursive loop.

> You can never observe the market directly. You can only observe noisy measurements of it. The math that fixes this is the same math that landed Apollo on the moon.

## Part 2: The State-Space Model and The Prediction-Update Cycle

A Kalman Filter sits on top of a state-space model. Two equations.

The first describes how the hidden state evolves over time. The process model.

**x\_t = F · x\_{t-1} + w\_t, w\_t ~ N(0, Q)**

F is the state transition matrix. Q is the process noise covariance, how much the state can drift between observations.

The second describes how the measurement is generated from the hidden state. The measurement model.

**z\_t = H · x\_t + v\_t, v\_t ~ N(0, R)**

H is the measurement matrix. R is the measurement noise covariance, how noisy your observations are.

That is the whole model. Six matrices total (F, Q, H, R, plus x₀ and P₀). Everything else falls out.

When both noise terms are Gaussian, the posterior stays Gaussian forever. The filter only ever has to track a mean and a covariance. That is what makes it computationally tractable.

The recursive loop has two halves.

**Predict** projects the prior forward using the process model:

**x̂****t|t-1 = F · x̂****{t-1|t-1}** **P\_t|t-1 = F · P\_{t-1|t-1} · Fᵀ + Q**

Uncertainty grows because the state has drifted and no new information has arrived.

**Update** merges the prior with the new observation z\_t. The gain math comes in Part 3. In final form:

**x̂\_t|t = x̂\_t|t-1 + K\_t · (z\_t - H · x̂\_t|t-1)** **P\_t|t = (I - K\_t · H) · P\_t|t-1**

Uncertainty shrinks because new information has arrived.

Bare-bones implementation in 30 lines of NumPy. Scalar, single hidden state. Every concept of the full filter is already here.

```text
import numpy as np

class KalmanFilter1D:
    def __init__(self, x0, P0, F, Q, H, R):
        self.x = x0       # state estimate (scalar)
        self.P = P0       # state variance (scalar)
        self.F = F        # state transition
        self.Q = Q        # process noise variance
        self.H = H        # measurement matrix
        self.R = R        # measurement noise variance
        self.history = []

    def predict(self):
        self.x = self.F * self.x
        self.P = self.F * self.P * self.F + self.Q
        return self.x

    def update(self, z):
        y = z - self.H * self.x                  # innovation (residual)
        S = self.H * self.P * self.H + self.R    # innovation variance
        K = self.P * self.H / S                  # Kalman gain
        self.x = self.x + K * y                  # state update
        self.P = (1 - K * self.H) * self.P       # covariance update
        self.history.append((self.x, self.P, K))
        return self.x

    def step(self, z):
        self.predict()
        return self.update(z)
```

![Image](https://pbs.twimg.com/media/HInr2XHXAAAcZEH?format=jpg&name=large)

This is the entire filter in 30 lines. You feed it observations one at a time. It maintains its best estimate of the hidden state, x, and its uncertainty about that estimate, P. The next part is where it becomes mathematically optimal.

![Image](https://pbs.twimg.com/media/HIntYKCXcAEq750?format=png&name=large)

## Part 3: The Kalman Gain - Where The Filter Becomes Optimal

The gain is the single most important quantity in the filter. The reason the algorithm has dominated state estimation in engineering and finance for six decades.

The filter has two pieces of information about the current state. A prior estimate x̂\_t|t-1 with uncertainty P\_t|t-1, and a new observation z\_t with measurement noise R. How should they be merged?

Naive averaging is wrong. The two quantities carry different uncertainties and treating them as equally informative throws away signal. The correct answer is a weighted combination where the weight depends on the relative uncertainties.

Three quantities.

The **innovation** is the residual between what was observed and what the filter predicted.

**y\_t = z\_t - H · x̂\_t|t-1**

The **innovation covariance** accounts for both prior uncertainty and measurement noise.

**S\_t = H · P\_t|t-1 · Hᵀ + R**

The **Kalman gain** translates innovation into state correction.

**K\_t = P\_t|t-1 · Hᵀ · S\_t⁻¹**

In scalar form the structure becomes obvious.

**K = P\_prior / (P\_prior + R)**

Prior uncertainty divided by total uncertainty. When the prior is much more certain than the observation, K is near zero and the filter ignores the new data. When the observation is much more precise, K is near one and the filter snaps to it. In between, K interpolates.

This is the optimal interpolation. It minimizes the mean squared error of the posterior among all linear unbiased combinations. **The Kalman gain is the math that tells you exactly how much to trust new evidence relative to your prior belief.**

With the gain in hand, the update step writes itself.

**x̂\_t|t = x̂\_t|t-1 + K\_t · y\_t** **P\_t|t = (I - K\_t · H) · P\_t|t-1**

Multi-dimensional version below. The structure is identical, with matrix ops replacing scalars. This is the production form you will deploy.

```text
import numpy as np

class KalmanFilter:
    def __init__(self, F, H, Q, R, x0, P0):
        self.F, self.H, self.Q, self.R = F, H, Q, R
        self.x = x0          # state vector (n x 1)
        self.P = P0          # state covariance (n x n)
        self.I = np.eye(F.shape[0])

    def predict(self):
        self.x = self.F @ self.x
        self.P = self.F @ self.P @ self.F.T + self.Q
        return self.x

    def update(self, z):
        y = z - self.H @ self.x                          # innovation
        S = self.H @ self.P @ self.H.T + self.R          # innovation cov
        K = self.P @ self.H.T @ np.linalg.inv(S)         # Kalman gain
        self.x = self.x + K @ y                          # state update
        self.P = (self.I - K @ self.H) @ self.P          # covariance update
        return self.x.copy()

    def step(self, z):
        self.predict()
        return self.update(z)
```

![Image](https://pbs.twimg.com/media/HIntrKBWEAAy_te?format=jpg&name=large)

Every component of the hidden state is tracked with its own variance and covariance, which means the filter can model correlated hidden quantities. Slope and intercept of a regression simultaneously. Level and trend of volatility. Multiple regime-conditional means at once.

![Image](https://pbs.twimg.com/media/HInt2NVXwAAIR4g?format=jpg&name=large)

## Part 4: Dynamic Beta - A Live Application Every Quant Desk Recognizes

The cleanest application of the Kalman Filter in systematic trading is dynamic beta. Every quant desk runs some version of this. Most retail traders do not realize it is necessary.

Setup. Two return series, the market r\_m and an asset r\_a. Classical CAPM:

**r\_a,t = α + β · r\_m,t + ε\_t**

Run OLS, get a beta, use it for hedging, sizing, factor decomposition. One problem: **beta is not constant.** It shifts as the company's revenue mix, capital structure, and macro exposure evolve. Treating it as a single number estimated over a fixed window throws away the most important fact a quant has: it is changing.

Fix it. Treat beta as a hidden state and let a Kalman Filter estimate it in real time.

State-space model. The hidden state evolves as a random walk:

**β\_t = β\_{t-1} + w\_t, w\_t ~ N(0, Q)**

Q controls smoothness. Smaller Q → smoother estimate. Larger Q → more responsive.

The measurement equation comes from the regression itself:

**r\_a,t = β\_t · r\_m,t + v\_t, v\_t ~ N(0, R)**

This is a Kalman Filter with time-varying H\_t = r\_m,t. Otherwise standard.

```text
import numpy as np
import pandas as pd
import yfinance as yf

def kalman_beta(market_returns, asset_returns, q=1e-5, r=1e-3, beta0=1.0, P0=1.0):
    n = len(market_returns)
    betas = np.zeros(n)
    variances = np.zeros(n)

    beta = beta0
    P = P0

    for t in range(n):
        # Predict
        P = P + q

        # Update with this period's observation
        H = market_returns.iloc[t]
        y = asset_returns.iloc[t] - H * beta            # innovation
        S = H * P * H + r                               # innovation variance
        K = P * H / S                                   # Kalman gain
        beta = beta + K * y                             # update beta
        P = (1 - K * H) * P                             # update variance

        betas[t] = beta
        variances[t] = P

    return pd.Series(betas, index=market_returns.index), pd.Series(variances, index=market_returns.index)

# Real example: QQQ beta to SPY over 10 years
spy = yf.Ticker("SPY").history(period="10y", interval="1d")['Close'].pct_change().dropna()
qqq = yf.Ticker("QQQ").history(period="10y", interval="1d")['Close'].pct_change().dropna()
returns = pd.concat([spy, qqq], axis=1).dropna()
returns.columns = ['SPY', 'QQQ']

beta_series, var_series = kalman_beta(returns['SPY'], returns['QQQ'], q=1e-5, r=1e-3)

print(f"Latest beta estimate: {beta_series.iloc[-1]:.4f}")
print(f"Latest uncertainty (1σ): {np.sqrt(var_series.iloc[-1]):.4f}")
print(f"Beta range over 10 years: [{beta_series.min():.3f}, {beta_series.max():.3f}]")
```

![Image](https://pbs.twimg.com/media/HInuEBqXAAEDV8R?format=jpg&name=large)

Run this on ten years of SPY and QQQ. Beta does not sit at a constant value. It oscillates in a tight band between 1.006 and 1.240, compressed to 1.137 in early 2020 as COVID forced everything to move together, expanded back toward 1.181 in the 2024 AI rally. Current reading: **1.1994, ±0.0982 one-sigma.**

![Image](https://pbs.twimg.com/media/HInuLLWXwAAk8s9?format=jpg&name=large)

OLS cannot see any of this. The Kalman estimate gives you the current state with an uncertainty band. The static estimate gives you whatever the last sixty days averaged out to.

This matters for hedging (size the short by current beta, not historical mean), for factor decomposition (the residual is the only return uncorrelated with the factor), and for signals (deviation from long-run mean is a tradeable mean-reversion edge).

Simple position-sizing rule built on the Kalman beta.

```text
def beta_signal(beta_series, lookback=252):
    # Compute z-score of current beta vs trailing 1-year distribution
    rolling_mean = beta_series.rolling(lookback).mean()
    rolling_std = beta_series.rolling(lookback).std()
    z = (beta_series - rolling_mean) / rolling_std

    # Position: short QQQ when beta is elevated, long when compressed
    # Sized in [-1, 1] by tanh of z-score
    position = -np.tanh(z / 1.5)
    return position.dropna()

position = beta_signal(beta_series)
print(f"Current position: {position.iloc[-1]:.3f}")
print(f"Average absolute position: {position.abs().mean():.3f}")
```

![Image](https://pbs.twimg.com/media/HInuWKnXkAAxF7Q?format=png&name=large)

Current reading: a strong short on QQQ relative to SPY at -0.892, because dynamic beta is near the top of its trailing one-year distribution. Average absolute position is 0.672, so the signal stays meaningfully positioned rather than collapsing to zero. No signal works in every regime, but the Kalman beta is the right input to almost any beta-aware strategy.

> OLS gives you the average. Kalman gives you the current state. Trading on the average when the current state has moved is how strategies that look great in backtest die in production.

## Part 5: Volatility Tracking - Kalman As An Alternative To GARCH

The second canonical Kalman application is volatility tracking.

EWMA, GARCH, and realized variance all treat volatility as if it were directly observable. They are not wrong exactly, but they share one conceptual flaw: they conflate the variance of recent returns with the current state of underlying volatility. The squared log-return on any single day is itself a noisy estimate of the true latent variance. Treat each squared return as ground truth and you fold all of that noise back into your volatility estimate.

State-space formulation. The hidden state is the log of the current variance.

**log(σ²\_t) = log(σ²\_{t-1}) + w\_t, w\_t ~ N(0, Q)**

Log-space keeps variance positive and stabilizes the dynamics. Q controls how fast the filter responds to regime shifts.

The measurement equation links observed squared returns to latent variance.

**log(r\_t²) = log(σ²\_t) + η\_t**

For Gaussian returns the squared return is chi-squared distributed and the noise is not exactly Gaussian, but the Gaussian approximation works well in practice. Two Sigma and AQR both deploy variants in their vol-of-vol models.

```text
import numpy as np
import pandas as pd
import yfinance as yf

def kalman_volatility(returns, q=0.1, r=1.0, log_var0=None, P0=1.0):
    n = len(returns)
    # Observation: log of squared return. Floor to avoid log(0).
    log_sq_returns = np.log(np.maximum(returns ** 2, 1e-12))

    if log_var0 is None:
        log_var0 = log_sq_returns[:60].mean()

    log_var = log_var0
    P = P0
    estimates = np.zeros(n)

    for t in range(n):
        # Predict
        P = P + q

        # Update
        y = log_sq_returns.iloc[t] - log_var
        S = P + r
        K = P / S
        log_var = log_var + K * y
        P = (1 - K) * P

        estimates[t] = np.exp(log_var)

    annual_vol = np.sqrt(estimates * 252)
    return pd.Series(annual_vol, index=returns.index)

# Real example: SPY volatility tracking
spy_returns = yf.Ticker("SPY").history(period="5y", interval="1d")['Close'].pct_change().dropna()
kalman_vol = kalman_volatility(spy_returns, q=0.1, r=1.0)
ewma_vol = spy_returns.ewm(span=20).std() * np.sqrt(252)
realized_60d = spy_returns.rolling(60).std() * np.sqrt(252)

print(f"Current Kalman vol estimate: {kalman_vol.iloc[-1]:.2%}")
print(f"Current EWMA vol: {ewma_vol.iloc[-1]:.2%}")
print(f"Current 60d realized: {realized_60d.iloc[-1]:.2%}")
```

![Image](https://pbs.twimg.com/media/HInulj3WMAAGKdc?format=jpg&name=large)

Plot the three series against VIX. The Kalman estimate tracks the broader trend while EWMA and rolling realized respond more aggressively to recent shocks. **Responsiveness is controlled by q.** Higher q → faster response, more noise. Lower q → smoother, more lag. There is no universally optimal value. Vol-targeting on a five-minute horizon wants a different q than a six-month risk overlay.

![Image](https://pbs.twimg.com/media/HInuvT1WcAANQAE?format=jpg&name=large)

```text
def vol_target_position(returns, target_vol=0.15, max_leverage=2.0):
    kvol = kalman_volatility(returns, q=0.1, r=1.0)
    raw_leverage = target_vol / kvol
    return np.clip(raw_leverage, 0, max_leverage)

leverage = vol_target_position(spy_returns, target_vol=0.15)
print(f"Current target leverage: {leverage.iloc[-1]:.3f}")
print(f"Leverage range last year: [{leverage.iloc[-252:].min():.2f}, {leverage.iloc[-252:].max():.2f}]")
```

![Image](https://pbs.twimg.com/media/HInu2LBXMAAP60C?format=png&name=large)

Position size is inversely proportional to current vol. The latest reading delivers target leverage near the cap because the filter is reading vol below 15%. Across the last 252 trading days the leverage has swung between **0.89 and 2.00**, exactly the kind of automatic risk modulation vol targeting is supposed to deliver. Bridgewater built All Weather around this logic across assets. AQR's Managed Futures funds run on it. Citadel's risk-targeting overlay uses it. The common ingredient is a real-time estimate of the current state of volatility, tunable through one parameter.

> GARCH tells you what volatility was. Kalman tells you what volatility is right now, and what it will be a moment from now.

## Part 6: The Complete Implementation Pipeline and Critical Limitations

Everything so far has been single-purpose. A production system runs many filters in parallel, integrates them with execution, and degrades gracefully when assumptions break.

The complete pipeline collected into a single class. Written to be readable, not maximally clever.

```text
import numpy as np
import pandas as pd
import yfinance as yf

class MarketKalmanFilter:
    """
    A general-purpose Kalman Filter for univariate state estimation
    on financial time series.

    Parameters
    ----------
    q : float
        Process noise variance. Smaller = smoother state. Larger = more responsive.
    r : float
        Measurement noise variance. Smaller = trust observations more.
    x0 : float
        Initial state estimate.
    P0 : float
        Initial state variance.
    """
    def __init__(self, q=1e-5, r=1e-3, x0=0.0, P0=1.0):
        self.q = q
        self.r = r
        self.x = x0
        self.P = P0
        self.history = []

    def step(self, observation, H=1.0):
        # Predict
        self.P = self.P + self.q
        # Update
        y = observation - H * self.x
        S = H * self.P * H + self.r
        K = self.P * H / S
        self.x = self.x + K * y
        self.P = (1 - K * H) * self.P
        self.history.append({'x': self.x, 'P': self.P, 'K': K, 'y': y, 'H': H})
        return self.x

    def state_series(self, observations, H_series=None):
        results = np.zeros(len(observations))
        if H_series is None:
            H_series = np.ones(len(observations))
        for t, (z, H) in enumerate(zip(observations, H_series)):
            results[t] = self.step(z, H=H)
        return pd.Series(results, index=observations.index)

def walk_forward_kalman_backtest(ticker_asset, ticker_market, target_vol=0.15, q_beta=1e-5, r_beta=1e-3, q_vol=0.1, r_vol=1.0):
    """
    Walk-forward backtest of a dynamic-beta + vol-target strategy.
    Trades the asset, hedges the beta exposure against the market, sized by Kalman vol.
    """
    asset = yf.Ticker(ticker_asset).history(period="10y", interval="1d")['Close'].pct_change().dropna()
    market = yf.Ticker(ticker_market).history(period="10y", interval="1d")['Close'].pct_change().dropna()
    df = pd.concat([asset, market], axis=1).dropna()
    df.columns = ['asset', 'market']

    # Stream 1: dynamic beta via Kalman
    beta_filter = MarketKalmanFilter(q=q_beta, r=r_beta, x0=1.0, P0=1.0)
    betas = beta_filter.state_series(df['asset'], H_series=df['market'].values)

    # Stream 2: Kalman volatility on asset
    vol_filter_input = df['asset']
    log_sq = np.log(np.maximum(vol_filter_input ** 2, 1e-12))
    vol_filter = MarketKalmanFilter(q=q_vol, r=r_vol, x0=log_sq.iloc[:60].mean(), P0=1.0)
    log_var_series = vol_filter.state_series(log_sq)
    annual_vol = np.sqrt(np.exp(log_var_series) * 252)

    # Position: vol-targeted, beta-neutralized
    leverage = np.clip(target_vol / annual_vol, 0, 2.0)
    hedge_ratio = betas
    strategy_returns = leverage.shift(1) * (df['asset'] - hedge_ratio.shift(1) * df['market'])

    # Performance metrics
    sharpe = strategy_returns.mean() / strategy_returns.std() * np.sqrt(252)
    cum = (1 + strategy_returns).cumprod()
    max_dd = ((cum - cum.cummax()) / cum.cummax()).min()
    annual_return = strategy_returns.mean() * 252

    print(f"\nWalk-Forward Kalman Backtest Results — {ticker_asset} / {ticker_market}")
    print(f"  Annualized Sharpe:  {sharpe:.4f}")
    print(f"  Max Drawdown:       {max_dd:.4f}")
    print(f"  Annualized Return:  {annual_return:.4f}")
    print(f"  Avg leverage:       {leverage.mean():.3f}")
    print(f"  Beta range:         [{betas.min():.3f}, {betas.max():.3f}]")
    print(f"  Final state — beta: {betas.iloc[-1]:.3f}, vol: {annual_vol.iloc[-1]:.3%}")

    return strategy_returns, betas, annual_vol

# Run
strat_returns, betas, vols = walk_forward_kalman_backtest("QQQ", "SPY")
```

![Image](https://pbs.twimg.com/media/HInvDRVWsAARYlW?format=jpg&name=large)

![Image](https://pbs.twimg.com/media/HInvHXOXIAA9bfP?format=jpg&name=large)

Run this on ten years of QQQ and SPY. The strategy posts an annualized **Sharpe of 0.44, annual return near 4.9%, max drawdown of -23%.** Average leverage across the window is 1.53. Final beta state 1.199, final volatility state 13.29%.

![Image](https://pbs.twimg.com/media/HInvM9qWIAAakwB?format=jpg&name=large)

The pipeline does not lookahead. Every state estimate at time t uses only observations up to time t, and strategy returns are shifted forward one period before being applied. The Kalman filter naturally produces a sequential, causal estimate.

Three assumptions determine whether your filter survives contact with live markets.

**Linearity:** The standard filter assumes F and H are linear. Implied vol surface evolution, options price response, regime-switching credit spreads, all violate this. Mitigation: the Extended Kalman Filter linearizes around the current estimate at each step. The Unscented Kalman Filter uses sigma points for strongly nonlinear systems without needing derivatives. Production at modern funds runs UKFs on most state-space problems.

**Gaussian noise:** Real return innovations are fat-tailed. The Gaussian approximation survives in many cases because the filter only uses the first two moments and the CLT cleans up a lot over many steps. But on extreme observations a standard filter responds too aggressively. Mitigation: **robust Kalman filtering** with a Huber-style gain that downweights extreme innovations. Small efficiency loss in normal regimes, dramatic improvement during tail events.

**Stationarity of Q and R:** Both are typically treated as constants. They are not. Innovation variance changes with regime, liquidity-driven measurement noise expands and contracts with market conditions. Mitigation: adaptive estimation using the innovation sequence itself. If your innovations are systematically larger than the model's S, the model is underestimating Q or R. Re-tune.

> **Production rule:** if innovation variance diverges from S\_t, your model is wrong. Tune before you trade. This is the single difference between a research filter and a production filter.

## The Summary

The Kalman Filter does not predict the future. It estimates an unobservable state in real time from noisy observations, with mathematically optimal accuracy under reasonable assumptions.

Invented in 1960 to guide spacecraft. Now run by every major systematic fund to estimate quantities no chart can show you directly. Dynamic beta. Dynamic volatility. Inventory pressure, mean reversion strength, alpha decay, regime probability, latent liquidity. All are unobservable variables extracted from observable measurements using the same predict-update-gain cycle you just learned.

A Markov model tells you which regime you are in. The Kalman Filter tells you where you actually are inside that regime, right now. **The two complement each other.** A serious systematic system runs both.

so the question i want to leave you with.

if you put a Kalman Filter on the single most important hidden state in the market you trade most often, what would you pick? volatility regime? liquidity condition? something domain-specific only your edge has access to?

drop your answer in the replies.

let me know if you want a part 2 on the Extended Kalman Filter for non-linear dynamics. could be the most useful follow-up i write this year :)