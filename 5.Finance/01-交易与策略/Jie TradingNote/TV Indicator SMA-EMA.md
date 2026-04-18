---
notion-id: 28178d23-e296-8013-9821-f2edad373d89
Last edited time: 2025-10-03T21:32:00
Tags: []
Verification: unverified
Owner:
  - 杰 吴
---
## **EMA 概念**

> **Exponential Moving Average**

- **计算方法**：EMA 给近期价格分配**更高的权重**，而给较远期的价格分配**较低的权重**。它的计算是递归的，涉及到前一天的 EMA 值和今天的收盘价。
- **特点**：由于对近期价格更重视，EMA 对价格变动的**反应更快、更灵敏**，能更快地捕捉到趋势的变化。**它能更平滑地跟随价格，减少 SMA 可能出现的跳动。**
- **短期 EMA** (如 5 EMA, 10 EMA, 12 EMA)：对价格变化最敏感，常用于短线交易和捕捉快速趋势。
- **中期 EMA** (如 20 EMA, 50 EMA, 26 EMA)：提供较为平衡的信号，适合中短线交易和判断中期趋势。
- **长期 EMA** (如 100 EMA, 200 EMA)：平滑度最高，滞后性也最大，主要用于识别长期趋势和宏观市场方向。

## Indicator

TradingView 指标名称：3ema

1. **Kristjan **设置为：**10、20、50**
2. 油管币哥设置为：**20、60、120**

![[imgs/image 192.png]]

## **Kristjan 的**均线交易规则

> 适合在强势标的中突破追高

![[imgs/image 193.png]]

![[imgs/image 194.png]]

3. 筛选 1-3 个月涨幅 30%-100% 的强势标的，且 EMA10/20/50 多头排列
4. 日线级别上出现 **2 周到 2 个月的盘整区间**。
5. 等待价格**突破盘整并以关键 K 线的收盘价入场（看4 小时或日线）**。
6. **止损在关键 K 线下方**；仓位初始可以按策略分配。
7. 若突破后行情爆发，约第 5 天可**先止盈 1/3 并将止损移至入场价**；其后**跌破 EMA10 止盈 1/3**，**跌破 EMA20 止盈剩余仓位**。

**回报：**这类小市值的埋伏若成功，波动幅度通常更大，回报潜力较高；

**风险**：假突破次数多、消息面风险、以及流动性不足都可能导致大损失。因此**关键点是用更长的横盘作为筛选条件并用量能作为突破有效性的确认**，以降低假突破概率。


视频课笔记：[[Kristjan三均线突破交易系统实战规则拆解]]  

## 币哥双均线规则

### 开仓

![[imgs/image 195.png]]

![[imgs/image 196.png]]

![[imgs/image 197.png]]

8. **TF 推荐 1h/4h/1d/1w，时间级别越小机会越多，但准确性也会下降。**
9. **均线密集开仓法与回踩20均线不破开仓法**
10. **均线密集后续不一定涨，为控制分险可等到回踩20均线不破再开仓**。

### 止盈

![[imgs/image 198.png]]

11. **在开仓同TF级别找历史的阻力区，作为止盈点，分批止盈。**1

视频课笔记：[[币哥双均线交易系统]] [[币哥双均线高赔率交易系统]] 

## 代码

可手动复制代码创建指标

```javascript
//@version=5
indicator(title="均线系统", shorttitle="均", overlay=true)

sma20 = ta.sma(close, 20)
sma60 = ta.sma(close, 60)
sma120 = ta.sma(close, 120)

ema20 = ta.ema(close, 20)
ema60 = ta.ema(close, 60)
ema120 = ta.ema(close, 120)

plot(sma20, color=color.rgb(255, 221, 0), title="SMA20")
plot(ema20, color=color.new(#a3b800, 50), title="EMA20")

plot(sma60, color=color.blue, title="SMA60")
plot(ema60, color=color.new(#417096, 16), title="EMA60")

plot(sma120, color=color.purple, title="SMA120")
plot(ema120, color=color.new(#a350b1, 50), title="EMA120")

cond = barstate.islast
bl = low
moveBar = input(0, title="Move Bar")
x20 = input(20, title="X20 Offset") + moveBar
x60 = input(60, title="X60 Offset") + moveBar
x120 = input(120, title="X120 Offset") + moveBar

plot(cond ? bl[20] : na, color=#FFC40C, linewidth=5, offset=-x20, style=plot.style_circles, transp=0)
plot(cond ? bl[60] : na, color=#FFC40C, linewidth=5, offset=-x60, style=plot.style_circles, transp=0)
plot(cond ? bl[120] : na, color=#FFC40C, linewidth=5, offset=-x120, style=plot.style_circles, transp=0)

```