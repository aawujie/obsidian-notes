---
notion-id: 28178d23-e296-80e3-99b4-c647e248cc45
Last edited time: 2025-10-03T21:32:00
Tags: []
Verification: unverified
Owner:
  - 杰 吴
---
## 概念

TradingView 指标名称：**Turtle Trade Channels Indicator TUTCI（海龟交易/唐奇安通道）**

![[imgs/image 210.png]]

1. 主要规则：**在20日突破时交易**，并**在价格突破10日高点或低点时获利了结。**
    - 在20日向上突破时买入，当价格触及10日低点时平仓。
    - 在20日向下突破时做空，当价格触及10日高点时平仓。
2. 在这个指标中
    - **红线是交易线，指示趋势方向**
        - 价格**K线在趋势线上方表示上涨趋势**。
        - 价格**K线在趋势线下方表示下跌趋势**。
    - **蓝色虚线**是退出线
3. 默认参数：20, 10 和 55, 20
    - 当价格高点等于或高于过去20天的最高价时做多。
    - 当价格低点等于或低于过去20天的最低价时做空。
    - 当价格触及退出线时，平仓多头头寸。
    - 当价格触及退出线时，平仓空头头寸。
    - 推荐的初始止损是开仓价的ATR（平均真实波幅）* 2。

### **海龟法则**

要像海龟一样精确交易，你需要设置两个指标，分别代表**主系统（短期）和备用系统（长期）**。

4. 设置主系统 S1，**入场周期（EntryPeriod）= 20**，**退出周期（ExitPeriod）= 10**。
5. 设置备用系统 S2，**入场周期（EntryPeriod）= 55**，**退出周期（ExitPeriod）= 20**，使用不同的颜色。
- 使用S1的入场策略：
    - **只有当上次S1信号的交易是亏损时**，才买入20日向上突破。
    - **只有当上次S1信号的交易是亏损时**，才卖出20日向下突破。
    - 如果上次S1信号的交易是盈利的，则不应交易——无论方向如何，也无论你上次是否交易了该信号。
- 使用S2的入场策略：
    - 只有当你忽略了上次S1信号并且市场在你没有参与的情况下上涨时，才买入55日向上突破。
    - 只有当你忽略了上次S1信号并且市场在你没有参与的情况下暴跌时，才卖出55日向下突破。
- 颜色：
    - 背景色为绿色时做多。
    - 背景色为红色时做空。
    - 没有背景色时表示空仓。

**警告：海龟交易的止损或加仓规则不包括在内。**

视频课笔记：[[海龟交易实验：交易能力可后天培养的实证]] 

## 代码

```javascript
//@version=4
//author: @kivancozbilgic

study(title="Turtle Trade Channels Indicator", shorttitle="TuTCI", overlay=true, resolution="")
length = input(20,"Entry Length", minval=1)
len2=input(10, "Exit Length", minval=1)
showsignals = input(title="Show Entry/Exit Signals ?", type=input.bool, defval=true)
highlighting = input(title="Highlighter On/Off ?", type=input.bool, defval=true)


lower = lowest(length)
upper = highest(length)
u = plot(upper, "Upper", color=#0094FF)
l = plot(lower, "Lower", color=#0094FF)

up=highest(high,length)
down=lowest(low,length)
sup=highest(high,len2)
sdown=lowest(low,len2)
K1=barssince(high>=up[1])<=barssince(low<=down[1]) ? down : up
K2=iff(barssince(high>=up[1])<=barssince(low<=down[1]),sdown,sup)
K3=iff(close>K1,down,na)
K4=iff(close<K1,up,na)
plot(K1, title="Trend Line", color=color.red, linewidth=2)
e=plot(K2, title="Exit Line", color=color.blue, linewidth=1, style=6)


buySignal=high==upper[1] or crossover(high,upper[1])
sellSignal = low==lower[1] or crossover(lower[1],low)
buyExit=low==sdown[1] or crossover(sdown[1],low)
sellExit = high==sup[1] or crossover(high,sup[1])

O1= barssince(buySignal)
O2= barssince(sellSignal)
O3= barssince(buyExit)
O4= barssince(sellExit)

E1= barssince(buySignal[1])
E2= barssince(sellSignal[1])
E3= barssince(buyExit[1])
E4= barssince(sellExit[1])

plotshape(buySignal and O3<O1[1] ? down : na, title="Long Entry", location=location.absolute, style=shape.circle, size=size.tiny, color=color.green, transp=0)
plotshape(buySignal and showsignals and O3<O1[1] ? down : na, title="Long", text="Long Entry", location=location.absolute, style=shape.labelup, size=size.tiny, color=color.green, textcolor=color.white, transp=0)

plotshape(sellSignal and O4<O2[1] ? up : na, title="Short Entry", location=location.absolute, style=shape.circle, size=size.tiny, color=color.red, transp=0)
plotshape(sellSignal and showsignals and O4<O2[1]  ? up : na, title="Short", text="Short Entry", location=location.absolute, style=shape.labeldown, size=size.tiny, color=color.red, textcolor=color.white, transp=0)

plotshape(buyExit and O1<O3[1] ? up : na, title="Long Exit", location=location.absolute, style=shape.circle, size=size.tiny, color=color.blue, transp=0)
plotshape(buyExit and showsignals and O1<O3[1] ? up : na, title="Long Exit", text="Exit Long", location=location.absolute, style=shape.labeldown, size=size.tiny, color=color.blue, textcolor=color.white, transp=0)

plotshape(sellExit and O2<O4[1] ? down : na, title="Short Exit", location=location.absolute, style=shape.circle, size=size.tiny, color=color.blue, transp=0)
plotshape(sellExit and showsignals and O2<O4[1] ? down : na, title="Short", text="Exit Short", location=location.absolute, style=shape.labelup, size=size.tiny, color=color.blue, textcolor=color.white, transp=0)

color1= highlighting and min(O1,O2,O3)==O1 ? color.green : na
color2= highlighting and min(O1,O2,O4)==O2 ? color.red : na
fill(u, e, color=color1, transp=88, title="Background")
fill(l, e, color=color2, transp=88, title="Background")


```
