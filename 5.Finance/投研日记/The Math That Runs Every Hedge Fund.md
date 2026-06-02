---
title: "The Math That Runs Every Hedge Fund You've Never Heard Of"
type: article
created: 2026-06-02
updated: 2026-06-02
sources:
  - "https://x.com/ruujss/status/2061503353008669181"
tags:
  - quant
  - hedge-fund
  - risk-management
  - math
  - framework
---

# The Math That Runs Every Hedge Fund You've Never Heard Of

**作者:** Ruuj (@RuujSs)
**发布时间:** 2026-06-01T17:41:14.000Z
**互动:** 48 likes | 4 RT | 89 bookmarks

---

It isn't what they trade. It's how they think about risk. Here is the complete framework, built from the ground up.

You have probably heard of two-and-twenty.

The classic hedge fund fee structure. 2% of assets under management every year, no matter what. 20% of any profits generated. It sounds like a good deal for the fund manager.

For most hedge funds, it is. Because most hedge funds quietly underperform. They collect the 2%, occasionally collect the 20%, and return something roughly comparable to an index fund after fees. The industry's dirty secret is that the average hedge fund is not worth the fee. You would have done better in a passive ETF.

And yet.

A small number of funds Renaissance, Two Sigma, DE Shaw, Citadel have generated returns that no passive strategy comes close to. Not occasionally. Consistently. For decades. With risk profiles that are genuinely different from the market.

The difference is not that they have better predictions.

The difference is that they have a different relationship with uncertainty itself. They have built systematic frameworks that translate raw uncertainty into structured, sized, and precisely managed positions. They do not try to eliminate risk. They price it, measure it, and get paid for taking exactly the right amount of it.

Most people think trading is about being right.

You study a company. You form a view. You buy. Either the price goes up and you make money, or it does not and you do not. The game is prediction. The edge is accuracy.

This model is not just incomplete. It is wrong in a way that actively prevents people from building durable edge.

Here is the right model.

A casino running a roulette wheel does not have a view on where the ball will land. It has no idea. It makes no prediction. What it has is a mathematical structure that guarantees a 2.7% edge on every spin, and it runs that spin thousands of times per day. The prediction is irrelevant. The edge is structural. The mathematics does the work.

Every serious systematic trading firm on earth is running a version of this structure. They are not in the business of being right about the next price move. They are in the business of finding situations where the mathematical expected value is in their favor, sizing those situations correctly, and running them as many times as possible.

The single formula that captures this is deceptively simple:

Where:

A positive EV means that if you repeat this trade a large number of times, you will make money on average. Not on every trade. On average. Over enough repetitions.

This is not just a formula. It is a philosophical shift in how you think about the job.

The job is not to be right. The job is to find positive expected value, size it correctly, and repeat it enough times that the mathematics accumulates in your favor. Being wrong on any individual trade is fine. Being systematically wrong about the EV calculation is the only real failure mode.

Every chapter in this article builds from this foundation. Understanding the rest requires believing this first.

Here is the question most traders cannot answer precisely:

Most people arrived at it by feeling confident. Or slightly more confident than uncertain. 60% just felt right.

Professional quant systems do not work this way. They build probability estimates from historical base rates, conditional on measurable features of the current situation, updated as new information arrives. Every number is traceable to a data source and a calculation.

The mathematical framework for this is Bayesian inference. It is the single most important concept in quantitative finance, and it is more intuitive than it sounds.

Bayes' theorem:

Read this as: the probability of A given that B has occurred equals the probability of B given A, times the prior probability of A, divided by the overall probability of B.

The language sounds abstract. The idea is completely natural.

You start with a prior belief. Something has happened historically with a certain frequency that is your prior. You observe new evidence. You ask how likely that evidence would be if your hypothesis were true versus false. You update your prior accordingly. The result is a posterior your revised, evidence-adjusted estimate.

A concrete example from prediction markets.

A contract is trading at 45 cents, implying the market believes there is a 45% probability a certain policy decision goes a specific way. You observe that in 20 historically similar situations, the outcome occurred 13 times a base rate of 65%. You also observe that the contract typically trades 10 points below the true base rate due to a known behavioral bias in how market participants process political information.

You are not just agreeing with the market's 45%. You are computing your own posterior:

Prior: 65% (historical base rate)
Evidence: market pricing 45%, historically biased 10% low
Posterior: update toward ~58 - 62%

Your estimate differs from the market's by 13-17 percentage points. On a contract that pays $1.00, that is a 13-17 cent edge per contract. Over a large sample of similar contracts, that edge accumulates into meaningful returns.

The point is not the specific calculation. The point is that professional probability estimation is a disciplined, traceable, evidence-based process. Not a feeling dressed in numerical clothing.

Here is a result that breaks people's intuition the first time they see it clearly.

You can be right more than half the time, on every single trade, with a genuine mathematical edge, and still lose everything. Not because of a black swan. Not because of bad luck. Because of a property of multiplication that almost nobody thinks about until it has already cost them.

Start with something concrete.

A strategy wins 60% of the time. When it wins, it returns 50%. When it loses, it loses 40%. Run the expected value:

Positive 14% per trade. Real edge. So you put everything on each trade.

One win and one loss, in any order:

You lost 10% of your capital. On a strategy with positive expected value on every single trade.

This is not a trick. It is the geometry of compounding.

Percentage losses are not symmetric with percentage gains. Lose 40%, and you need a 67% gain just to return to where you started. Gains and losses do not cancel they multiply. And that multiplication structure means that sizing too large destroys capital even when the arithmetic edge is genuine and positive.

The formal statement of this: what a trader should actually maximize is not expected arithmetic return. It is expected log wealth the geometric growth rate of capital across a sequence of trades:

Where f is the fraction of capital deployed and R is the return on each trade. Approximate this for moderate bet sizes:

The first term grows with bet size good. The second term grows with the square of bet size this is the drag. Double your position, quadruple the variance drag. At some level of f, the drag overwhelms the return and geometric growth goes negative. You are expected to lose money over time despite having a positive edge coin.

The optimal bet size where geometric growth is maximized comes from setting the derivative of G to zero:

Edge divided by variance. Not edge alone. The variance of the strategy is in the denominator because every unit of variance you carry costs you compounding power.

The deeper number, the one that should sit in every trader's mind before entering any position, is the probability of ruin at a given drawdown depth D:

As f grows, the exponent shrinks toward zero and ruin probability approaches certainty. At large enough bet fractions, ruin is not a risk to be managed. It is a mathematical destination.

Two questions that must have numerical answers before any position is entered:

First: What is the maximum loss on this trade as a percentage of total capital? Not approximately. Exactly. If the answer is a feeling rather than a number, the position is not sized it is guessed.

Second: What does a realistic bad run look like, and does the account survive it with enough capital left to keep operating? A 60% win rate strategy will produce six or seven consecutive losses regularly across hundreds of trades. That sequence is not a disaster to survive it is a scheduled event to plan for.

The traders who compound over long periods are not the ones who sized most aggressively when their edge was strongest. They are the ones who understood that surviving to the next trade is itself a form of edge. Compounding requires presence. The mathematics only works if you are still in the game long enough for them to work.

Options were invented because having a view on direction is only one way to think about an asset. Sometimes the more interesting and more tradeable question is not which way a stock will move, but how much it will move, how fast, and over what time frame.

This is where the Black-Scholes framework and its derivatives the Greeks enter quantitative thinking. They appear in the toolkit of every serious systematic trading operation because they provide a precise language for decomposing risk into components that can be managed independently.

The Black-Scholes formula prices a European call option the right to buy an asset at a fixed price on a specific future date:

Where:

The equation itself is useful. The deeper insight is that it completely separates uncertainty about direction from uncertainty about magnitude. The expected return of the asset does not appear in the formula at all. What matters is not where the price goes it is how much it moves. Option pricing is a problem about the geometry of uncertainty, not its direction.

The Greeks are the derivatives of this price with respect to each input. Each one measures a different dimension of risk.

Delta (Δ) - Directional exposure:

How much does the option price change per $1 move in the underlying? A delta of 0.55 means the option gains 55 cents for every dollar the stock rises. This is your directional exposure. Delta hedging owning a quantity of shares equal to delta times your option exposure neutralizes directional risk, leaving you exposed only to the other dimensions.

Gamma (Γ) - Rate of change of delta:

How fast does your directional exposure change as the stock moves? High gamma positions require constant rebalancing because your delta changes rapidly with each price movement. Options near expiration and near the strike price carry very high gamma this is where risk concentrates and where most sizing errors happen.

Vega (ν) - Volatility exposure:

How much does the option price change per 1% change in implied volatility? High vega means your position gains or loses significant value when market uncertainty expands or contracts even if the underlying price does not move at all. Being long vega is being long uncertainty itself.

Theta (Θ) - Time decay:

How much value does the option lose each day purely from the passage of time? Every option is a decaying asset. Option sellers collect theta daily. Option buyers pay it. The majority of retail traders who buy options and lose money are not wrong about direction they are losing to theta before the move they anticipated ever arrives.

The power of this framework is not any single Greek. It is that they decompose risk into independently manageable components. A position can have zero delta (no directional exposure), positive gamma (benefits from large moves in either direction), and negative theta (costs money each day) simultaneously. These are distinct, separable bets on distinct, separable questions. Managing them independently is what professional options desks do that retail participants almost never do.

The implied volatility surface the three-dimensional map of implied volatility across all strikes and all maturities is where this framework becomes genuinely powerful for edge extraction. In a theoretically perfect world, every option on the same underlying would imply the same volatility when you solve the Black-Scholes formula backward from the market price. In reality, they never do. Finding where the surface is mispriced relative to realized volatility, and trading the gap systematically, is the foundational operation of volatility arbitrage.

A hedge fund running 500 simultaneous positions across global equities has a problem that the Kelly Criterion and the Greeks cannot fully solve on their own.

The problem is correlation.

You might think you have 500 independent bets. In reality, those 500 positions might share 7 or 8 underlying sources of risk broad market direction, interest rate sensitivity, credit risk appetite, momentum, size, value. When one of those underlying factors moves, many of your 500 positions move together. Your apparent diversification is partially illusory.

Factor models are the framework for seeing through this illusion.

The foundational model in academic finance is the Fama-French Three-Factor Model, published in 1992, which decomposed equity returns into three components:

Where:

The coefficients β₁, β₂, β₃ tell you exactly how much of the stock's historical return came from broad market exposure, size exposure, and value exposure versus how much was genuinely stock-specific.

The crucial insight: most of what looks like manager skill in equity returns is just undisclosed factor exposure. A fund that returned 15% in a year where small-cap value stocks returned 18% did not add value it took on small-cap value risk and got paid the going rate for that risk. Alpha the α term is what remains after all factor exposures are accounted for. It is extraordinarily rare.

Modern quant funds run on extended versions of this model. Fama and French themselves extended it to five factors. Research has identified dozens of additional factors: momentum, quality, low volatility, profitability, investment patterns. The practical toolkit for a serious systematic equity strategy might include 15-20 factors, each with its own beta, each with its own risk budget.

Portfolio construction with factor models:

The mathematical tool for step 2 is the covariance matrix of factor returns a structure that captures not just how volatile each factor is, but how all factors move relative to each other. Optimization against this matrix produces positions that achieve the intended factor exposures without inadvertent concentration in hidden correlated risks.

This is why large quant funds can hold hundreds of positions without becoming implicitly concentrated. The positions look diverse at the instrument level. The factor model confirms they are genuinely diverse at the risk level. These are not the same thing, and confusing them is one of the most common and costly errors in portfolio construction.

Here is a truth that makes quantitative trading harder than most people initially expect.

Every edge you find is being found by other people simultaneously. The moment an anomaly is large enough to be clearly visible in data, it is being traded by multiple systematic strategies. And trading activity that exploits an anomaly partially corrects that anomaly. The anomaly gets smaller. The edge compresses.

This is the mechanism of market efficiency, and understanding it precisely changes how you think about signal research.

Discovery phase: A researcher identifies a statistical pattern in historical data. The pattern has strong predictive power. Backtested returns are excellent.

Early deployment phase: The researcher or fund deploys capital against the signal. Returns are strong. The signal is not yet widely known.

Proliferation phase: Results leak or are independently discovered. Multiple firms begin trading similar signals. Increasing capital chasing the same anomaly begins correcting it.

Decay phase: The signal's predictive power declines. Not to zero, genuine structural anomalies persist at a lower amplitude but sharply from its peak.

Equilibrium phase: The remaining edge in the signal approximately equals the cost of exploiting it for marginal capital. Only the most efficient operators continue to find it worth trading.

The empirical reality: the half-life of most discovered quantitative signals in equity markets is measured in years, sometimes months. Academic publication of a factor is followed by measurable compression of that factor's returns in the years after publication. The market learns.

First: Signal diversity is not optional. A strategy with one primary signal is one decay event away from failure. Robust systematic strategies maintain portfolios of signals with different underlying mechanisms, different decay rates, and low mutual correlation. When one signal compresses, others continue operating.

Second: Evaluate marginal information, not standalone performance. The correct test for a new signal is not does this signal predict returns? but does this signal predict returns given everything my model already knows? A signal that is correlated with your existing signals adds almost no genuine predictive power regardless of its standalone performance. The marginal contribution the information this signal contains that your model does not already have is the only relevant number.

This is formally captured by conditional mutual information:

I(X; Y | Z) = the information X provides about Y, given that Z is already known

A signal with high unconditional mutual information I(X;Y) but low conditional mutual information I(X;Y|Z) is redundant. It is telling the model something it already knows from a different angle. Adding it increases apparent model complexity while adding minimal genuine predictive power the worst possible combination.

Third: Invest continuously in new signal discovery. The pipeline must constantly produce new, genuinely orthogonal signals to replace those in decay. This is why the best systematic funds spend more on research infrastructure than on trading infrastructure. The intellectual capital is the asset. The trading system is just the execution layer.

Renaissance's Medallion Fund sustained edge for thirty years not because they found one extraordinary signal in 1988 and exploited it forever. They built a machine that continuously found new orthogonal signals and replaced decaying ones. The machine's output was returns. Its actual product was the continuous discovery of genuinely additive information about market structure.

Everything in the previous six chapters is a component. Here is what the assembled system looks like.

A properly structured systematic trading framework has five layers. Each layer builds on the previous one. Removing any layer does not just weaken the system it breaks the logical chain that makes the whole thing work.

Layer 1: Signal generation

The foundation. Raw predictive signals derived from observable data. Price-based signals. Volume signals. Fundamental factor signals. Cross-asset relationship signals. Each signal is evaluated not on its historical performance in isolation but on its conditional mutual information what does this tell us that the model does not already know?

Every signal in the library must pass three tests before deployment:

Statistical significance: the pattern strong enough in historical data that it is unlikely to be noise? Necessary but not sufficient.

Mechanistic explanation: there an identifiable reason this pattern should persist? A signal grounded in structural human behavior, institutional constraint, or information processing friction has a basis for persistence. A signal that looks good in data with no plausible mechanism is almost certainly a false positive.

Out-of-sample stability: Does it generalize? Does performance hold on data the model was never trained on, across time periods with different characteristics, across markets the model was not calibrated on?

A signal that passes all three is in the library. Anything that fails any of the three stays out, regardless of how good the in-sample performance looks.

Layer 2: Regime detection

Markets behave differently across time. A signal that is highly predictive in trending markets may be actively misleading in mean-reverting markets. Trading without awareness of the current regime is like driving with a map that does not update for roadworks.

Regime models whether Hidden Markov Models, threshold models, or more sophisticated variants maintain a probability distribution over the current market state and condition signal weights accordingly. When the regime estimate shifts, signal weights shift with it. The system does not fail when the market changes character. It adapts to the change automatically and explicitly.

Layer 3: Portfolio construction

Individual signal outputs become a portfolio through a construction process that explicitly accounts for factor exposures and correlations. The objective is not to maximize expected return. It is to maximize the ratio of expected alpha to active risk the Sharpe ratio of the unexplained component.

This requires estimating the covariance structure of positions, controlling unintended factor loadings, and ensuring that apparent diversification is genuine diversification at the risk level. A portfolio of 200 positions with implicit concentration in three underlying factors is not a 200-position portfolio. It is a three-factor bet dressed in 200 instruments.

Layer 4: Position sizing

Kelly-adjusted sizing, calibrated to the confidence level of each signal, the correlation structure of the portfolio, and the tail risk of worst-case simultaneous adverse moves. Half-Kelly as the practical baseline. Explicit worst-case scenario modeling before every position is entered.

The discipline here is not about being conservative. It is about recognizing that the edge only compounds if you are present for enough repetitions. A single catastrophic drawdown that requires years of recovery to overcome destroys the geometric compounding that makes the entire system valuable.

Layer 5: Continuous evaluation and adaptation

Live monitoring of signal performance against expectations. Tracking whether Sharpe ratios, hit rates, and decay rates are consistent with historical calibration. Regime monitoring that detects when market structure has shifted in ways that invalidate current signal assumptions.

When signals deteriorate beyond expected decay, size them down. When new signals clear all three validation tests, bring them into the library. When regime indicators suggest the current environment is outside the range of conditions the model was calibrated on, reduce overall exposure until the environment normalizes.

The system is not static. It is a machine for continuously processing new information about both markets and its own performance.

Let me tell you what I think is the actual insight, the one that sits underneath all the mathematics.

Most market participants are trying to answer the question: what will happen next?

It is the natural question. It is the one finance news, analyst reports, and every dinner party conversation about markets is structured around. And it is almost entirely the wrong question for building durable trading edge.

The right question is: given deep uncertainty about what will happen next, what is the correct decision right now?

That reframing changes everything. It shifts the problem from prediction which is hard, noisy, and humbling to decision-making under uncertainty which is precise, mathematical, and tractable.

Expected value tells you whether a bet is worth taking. Kelly tells you how much to bet. The Greeks tell you what dimensions of risk you are holding. Factor models tell you whether your apparent diversification is genuine. Signal evaluation frameworks tell you whether new information is real or noise. Regime models tell you whether your current assumptions about market behavior are still valid.

Every single tool in quantitative finance is a tool for making better decisions under uncertainty. Not for eliminating uncertainty. Not for predicting the future. For pricing uncertainty correctly, holding it in the right amounts, and getting paid fairly for the risk you have deliberately chosen to carry.

The funds that have sustained extraordinary returns across decades through crashes, crises, regime changes, and every manner of market stress are not the ones with the best crystal balls. They are the ones with the most disciplined and precise relationship with uncertainty itself.

They do not know what will happen next. They know exactly how to think about not knowing.

All of the mathematics in this article is just the language that discipline is written in. And like any language, knowing it does not guarantee you say the right thing it guarantees you stop saying things you cannot defend.

That is the edge. All the mathematics in this article is just the language that edge is written in.

