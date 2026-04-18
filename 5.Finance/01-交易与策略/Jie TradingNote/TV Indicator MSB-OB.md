---
notion-id: 28178d23-e296-80e5-9d95-d13d2ec7a750
Last edited time: 2025-10-12T02:17:00
Tags: []
Verification: unverified
Owner:
  - 杰 吴
---
## 概念

TradingView 指标名称：**Market Structure Break & Order Block by EmreKb**

1. **市场结构突破 M****SB：****价格突破前期高点后创出新低，或者突破前期低点后创出新高时，就会出现市场结构突破（msb）**。
2. **订单块 OB：**出现在市场结构突破（msb）之后。
如果市场结构突破（msb）是**看跌**的，那么订单块（ob）就是**高点之前的最后一根看涨蜡烛线**
如果市场结构突破（msb）是**看涨**的，那么订单块（ob）就是**低点之前的最后一根看跌蜡烛线**

![[imgs/image 211.png]]

3. **缓解块 MB：****MSB 失败后，原来的OB转变成反方向的MB。**

![[imgs/image 212.png]]

4. **突破块 BB：****之前的下降趋势中的摆动低点被突破（反之），价格又回到该水平进行测试时，就会出现**。

![[imgs/image 213.png]]

## 案例

### 2025.10.10_bitcoin插针

![[imgs/image 214.png]]

![[imgs/image 215.png]]

## 源码&注解

```javascript
// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © EmreKb

//@version=5
indicator("Market Structure Break & Order Block", "MSB-OB", overlay=true, max_lines_count=500, max_bars_back=4900, max_boxes_count=500)

settings = "Settings"
zigzag_len = input.int(9, "ZigZag Length", group=settings)
show_zigzag = input.bool(true, "Show Zigzag", group=settings)
fib_factor = input.float(0.33, "Fib Factor for breakout confirmation", 0, 1, 0.01, group=settings)

text_size = input.string(size.tiny, "Text Size", [size.tiny, size.small, size.normal, size.large, size.huge], group=settings)

delete_boxes = input.bool(true, "Delete Old/Broken Boxes", group=settings)

bu_ob_inline_color = "Bu-OB Colors"
be_ob_inline_color = "Be-OB Colors"
bu_bb_inline_color = "Bu-BB Colors"
be_bb_inline_color = "Be-BB Colors"

bu_ob_display_settings = "Bu-OB Display Settings"
bu_ob_color = input.color(color.new(color.green, 70), "Color", group=bu_ob_display_settings, inline=bu_ob_inline_color)
bu_ob_border_color = input.color(color.green, "Border Color", group=bu_ob_display_settings, inline=bu_ob_inline_color)
bu_ob_text_color = input.color(color.green, "Text Color", group=bu_ob_display_settings, inline=bu_ob_inline_color)

be_ob_display_settings = "Be-OB Display Settings"
be_ob_color = input.color(color.new(color.red, 70), "Color", group=be_ob_display_settings, inline=be_ob_inline_color)
be_ob_border_color = input.color(color.red, "Border Color", group=be_ob_display_settings, inline=be_ob_inline_color)
be_ob_text_color = input.color(color.red, "Text Color", group=be_ob_display_settings, inline=be_ob_inline_color)

bu_bb_display_settings = "Bu-BB & Bu-MB Display Settings"
bu_bb_color = input.color(color.new(color.green, 70), "Color", group=bu_bb_display_settings, inline=bu_bb_inline_color)
bu_bb_border_color = input.color(color.green, "Border Color", group=bu_bb_display_settings, inline=bu_bb_inline_color)
bu_bb_text_color = input.color(color.green, "Text Color", group=bu_bb_display_settings, inline=bu_bb_inline_color)

be_bb_display_settings = "Be-BB & Be-MB Display Settings"
be_bb_color = input.color(color.new(color.red, 70), "Color", group=be_bb_display_settings, inline=be_bb_inline_color)
be_bb_border_color = input.color(color.red, "Border Color", group=be_bb_display_settings, inline=be_bb_inline_color)
be_bb_text_color = input.color(color.red, "Text Color", group=be_bb_display_settings, inline=be_bb_inline_color)

var float[] high_points_arr = array.new_float(5)
var int[] high_index_arr = array.new_int(5)
var float[] low_points_arr = array.new_float(5)
var int[] low_index_arr = array.new_int(5)

var box[] bu_ob_boxes = array.new_box(5)
var box[] be_ob_boxes = array.new_box(5)
var box[] bu_bb_boxes = array.new_box(5)
var box[] be_bb_boxes = array.new_box(5)

to_up = high >= ta.highest(zigzag_len)
to_down = low <= ta.lowest(zigzag_len)

trend = 1
trend := nz(trend[1], 1)
trend := trend == 1 and to_down ? -1 : trend == -1 and to_up ? 1 : trend

last_trend_up_since = ta.barssince(to_up[1])
low_val = ta.lowest(nz(last_trend_up_since > 0 ? last_trend_up_since : 1, 1))
low_index = bar_index - ta.barssince(low_val == low)

last_trend_down_since = ta.barssince(to_down[1])
high_val = ta.highest(nz(last_trend_down_since > 0 ? last_trend_down_since : 1, 1))
high_index = bar_index - ta.barssince(high_val == high)

if ta.change(trend) != 0
if trend == 1
array.push(low_points_arr, low_val)
array.push(low_index_arr, low_index)
if trend == -1
array.push(high_points_arr, high_val)
array.push(high_index_arr, high_index)

f_get_high(ind) =>
[array.get(high_points_arr, array.size(high_points_arr) - 1 - ind), array.get(high_index_arr, array.size(high_index_arr) - 1 - ind)]

f_get_low(ind) =>
[array.get(low_points_arr, array.size(low_points_arr) - 1 - ind), array.get(low_index_arr, array.size(low_index_arr) - 1 - ind)]

f_delete_box(box_arr) =>
if delete_boxes
box.delete(array.shift(box_arr))
else
array.shift(box_arr)
0

[h0, h0i] = f_get_high(0)
[h1, h1i] = f_get_high(1)

[l0, l0i] = f_get_low(0)
[l1, l1i] = f_get_low(1)

if ta.change(trend) != 0 and show_zigzag
if trend == 1
line.new(h0i, h0, l0i, l0)
if trend == -1
line.new(l0i, l0, h0i, h0)

market = 1
market := nz(market[1], 1)
// market := market == 1 and close < l0 and low < l0 - math.abs(h0 - l0) * fib_factor ? -1 : market == -1 and close > h0 and high > h0 + math.abs(h0 - l0) * fib_factor ? 1 : market
last_l0 = ta.valuewhen(ta.change(market) != 0, l0, 0)
last_h0 = ta.valuewhen(ta.change(market) != 0, h0, 0)
market := last_l0 == l0 or last_h0 == h0 ? market : market == 1 and l0 < l1 and l0 < l1 - math.abs(h0 - l1) * fib_factor ? -1 : market == -1 and h0 > h1 and h0 > h1 + math.abs(h1 - l0) * fib_factor ? 1 : market

bu_ob_index = bar_index
bu_ob_index := nz(bu_ob_index[1], bar_index)
for i=h1i to l0i[zigzag_len]
index = bar_index - i
if open[index] > close[index]
bu_ob_index := bar_index[index]

bu_ob_since = bar_index - bu_ob_index

be_ob_index = bar_index
be_ob_index := nz(be_ob_index[1], bar_index)
for i=l1i to h0i[zigzag_len]
index = bar_index - i
if open[index] < close[index]
be_ob_index := bar_index[index]

be_ob_since = bar_index - be_ob_index

be_bb_index = bar_index
be_bb_index := nz(be_bb_index[1], bar_index)
for i=h1i - zigzag_len to l1i
index = bar_index - i
if open[index] > close[index]
be_bb_index := bar_index[index]

be_bb_since = bar_index - be_bb_index

bu_bb_index = bar_index
bu_bb_index := nz(bu_bb_index[1], bar_index)
for i=l1i - zigzag_len to h1i
index = bar_index - i
if open[index] < close[index]
bu_bb_index := bar_index[index]

bu_bb_since = bar_index - bu_bb_index

if ta.change(market) != 0
if market == 1
line.new(h1i, h1, h0i, h1, color=color.green, width=2)
label.new(int(math.avg(h1i, l0i)), h1, "MSB", color=color.new(color.black, 100), style=label.style_label_down, textcolor=color.green, size=size.small)
bu_ob = box.new(bu_ob_index, high[bu_ob_since], bar_index + 10, low[bu_ob_since], bgcolor=bu_ob_color, border_color=bu_ob_border_color, text="Bu-OB", text_color=bu_ob_text_color, text_halign=text.align_right, text_size=text_size)
bu_bb = box.new(bu_bb_index, high[bu_bb_since], bar_index + 10, low[bu_bb_since], bgcolor=bu_bb_color, border_color=bu_bb_border_color, text=l0 < l1 ? "Bu-BB" : "Bu-MB", text_color=bu_bb_text_color, text_halign=text.align_right, text_size=text_size)
array.push(bu_ob_boxes, bu_ob)
array.push(bu_bb_boxes, bu_bb)
if market == -1
line.new(l1i, l1, l0i, l1, color=color.red, width=2)
label.new(int(math.avg(l1i, h0i)), l1, "MSB", color=color.new(color.black, 100), style=label.style_label_up, textcolor=color.red, size=size.small)
be_ob = box.new(be_ob_index, high[be_ob_since], bar_index + 10, low[be_ob_since], bgcolor=be_ob_color, border_color=be_ob_border_color, text="Be-OB", text_color=be_ob_text_color, text_halign=text.align_right, text_size=text_size)
be_bb = box.new(be_bb_index, high[be_bb_since], bar_index + 10, low[be_bb_since], bgcolor=be_bb_color, border_color=be_bb_border_color, text=h0 > h1 ? "Be-BB" : "Be-MB", text_color=be_bb_text_color, text_halign=text.align_right, text_size=text_size)
array.push(be_ob_boxes, be_ob)
array.push(be_bb_boxes, be_bb)

for bull_ob in bu_ob_boxes
bottom = box.get_bottom(bull_ob)
top = box.get_top(bull_ob)
if close < bottom
f_delete_box(bu_ob_boxes)
else if close < top
alert("Price in the BU-OB zone")
else
box.set_right(bull_ob, bar_index + 10)

for bear_ob in be_ob_boxes
top = box.get_top(bear_ob)
bottom = box.get_bottom((bear_ob))
if close > top
f_delete_box(be_ob_boxes)
if close > bottom
alert("Price in the BE-OB zone")
else
box.set_right(bear_ob, bar_index + 10)

for bear_bb in be_bb_boxes
top = box.get_top(bear_bb)
bottom = box.get_bottom(bear_bb)
if close > top
f_delete_box(be_bb_boxes)
else if close > bottom
alert("Price in the BE-BB zone")
else
box.set_right(bear_bb, bar_index + 10)

for bull_bb in bu_bb_boxes
bottom = box.get_bottom(bull_bb)
top = box.get_top(bull_bb)
if close < bottom
f_delete_box(bu_bb_boxes)
else if close < top
alert("Price in the BU-BB zone")
else
box.set_right(bull_bb, bar_index + 10)

alertcondition(ta.change(market) != 0, "MSB", "MSB")
```

### 1. 设置 (Settings)

脚本首先定义了各种输入参数，允许用户自定义指标的行为和外观：

- **zigzag_len** (之字形长度): 用于 ta.highest() 和 ta.lowest() 函数的长度，**帮助识别之字形模式中的摆动高点和摆动低点。**
- **show_zigzag** (显示之字形): 一个布尔值，决定是否绘制连接摆动点的之字形线条。
- **fib_factor** (斐波那契因子): 一个浮点值（0到1之间），用作确认市场结构破裂的敏感度因子。它应用于类似斐波那契回撤的水平，以确认突破是否显著。
- **text_size** (文本大小): 控制方框上文本标签的大小。
- **delete_boxes** (删除旧/失效方框): 如果为 true，则旧的或“失效”（被验证无效）的订单块/突破块/缓解块将从图表中删除。如果为 false，它们将保留。
- **颜色设置**: 提供了多种颜色输入，用于自定义看涨（Bu-OB, Bu-BB, Bu-MB）和看跌（Be-OB, Be-BB, Be-MB）方块、其边框和文本的显示颜色。

### 2. 摆动点和趋势 (ZigZag 逻辑 - Swing Points and Trend Logic)

脚本使用自定义的类似之字形（ZigZag）的逻辑来识别重要的摆动高点和低点：

- **to_up**: 如果当前高点在 zigzag_len 周期内是最高点，则为 true，表示潜在的摆动高点。
- **to_down**: 如果当前低点在 zigzag_len 周期内是最低点，则为 true，表示潜在的摆动低点。
- **trend** (趋势): 这个变量跟踪基于 to_up 和 to_down 的短期趋势。
    - trend = 1 表示上升趋势（创造更高的低点）。
    - trend = -1 表示下降趋势（创造更低的低点）。
    - 当检测到新的 to_down（在上升趋势中预示潜在低点）或 to_up（在下降趋势中预示潜在高点）时，趋势会翻转。
- **high_points_arr, low_points_arr**: 数组，用于存储已识别的摆动高点和摆动低点的价格值。
- **high_index_arr, low_index_arr**: 数组，用于存储这些摆动高点和低点发生的 K 线索引。
- **f_get_high(ind) / f_get_low(ind)**: 辅助函数，用于从数组中检索过去的摆动高点/低点值及其索引。h0, h1 分别表示最近和次最近的摆动高点。l0, l1 则表示摆动低点。

if ta.change(trend) != 0 and show_zigzag 代码块会绘制之字形线条，以可视化这些已识别的摆动。

### 3. 市场结构破裂 (Market Structure Break - MSB)

这是智能资金概念（SMC）交易中的一个核心概念。**当价格突破重要的摆动高点（看涨MSB）或摆动低点（看跌MSB）时，就发生了MSB，这预示着市场方向可能发生转变。**

- **market** (市场): 这个变量跟踪整体市场结构趋势。
    - market = 1 表示看涨市场结构。
    - market = -1 表示看跌市场结构。
- 看跌MSB（市场转向-1）的条件是：market == 1 and l0 < l1 and l0 < l1 - math.abs(h0 - l1) * fib_factor。这检查**当前的摆动低点 (l0)**** **是否低于**前一个摆动低点 (l1)**，并且已经突破了**最近高点 (h0) **和**前一个低点 (l1) **之间范围的“斐波那契因子”百分比。这个 fib_factor 提供了突破显著性的确认。
- 看涨MSB（市场转向1）的条件是：market == -1 and h0 > h1 and h0 > h1 + math.abs(h1 - l0) * fib_factor。这检查**当前的摆动高点 (h0) 是否高于前一个摆动高点 (h1)，并且已经突破了前一个高点 (h1) 和最近低点 (l0) 之间范围的“斐波那契因子”百分比**。

当MSB发生时 (ta.change(market) != 0)，脚本会绘制一条水平线指示被突破的水平，并在突破点处显示“MSB”标签。

### 4. 订单块 (Order Block - OB)

订单块代表了一个预期存在机构买卖压力的区域。它通常是导致市场结构破裂的强劲移动之前，最后一个相反方向的 K 线。

- **看涨订单块 (Bullish Order Block - Bu-OB)**:
    - 在看跌市场结构中（或在看涨MSB之前）被识别。
    - bu_ob_index 循环从最后一个摆动高点 (h1i) 向后搜索到最后一个摆动低点 (l0i)，寻找在导致MSB的看涨移动之前的**最后一个看跌 K 线（开盘价 > 收盘价）**。该 K 线的高点和低点定义了订单块。
- **看跌订单块 (Bearish Order Block - Be-OB)**:
    - 在看涨市场结构中（或在看跌MSB之前）被识别。
    - be_ob_index 循环从最后一个摆动低点 (l1i) 向后搜索到最后一个摆动高点 (h0i)，寻找在导致MSB的看跌移动之前的**最后一个看涨 K 线（开盘价 < 收盘价）**。该 K 线的高点和低点定义了订单块。

当MSB发生时，相应的 box.new 函数会在图表上创建这些订单块方框，并将其向右延伸。

### 5. 突破块 (Breaker Block - BB) / 缓解块 (Mitigation Block - MB)

这些是市场结构破裂后形成的特定类型的块。

5. **突破块 (Breaker Block BB)**: 当之前的摆动高点（在上升趋势中）或摆动低点（在下降趋势中）**被突破后，价格又回到该水平进行测试时，就会出现**。导致突破的 K 线组成了“突破块”。
6. **缓解块 (Mitigation Block MB)**: **当市场未能创建更高的高点（在看涨情况下）或更低的低点（在看跌情况下），并且价格回撤到最后一个订单流区域时，就会形成。本质上，当一个订单块被价格突破但未能引发预期的延续时，它就可能转变为缓解块。**

脚本根据MSB的方向识别出 bu_bb_index (看涨) 和 be_bb_index (看跌)。

- **看涨块 (****Bu-BB/Bu-MB****)**:
    - 在看涨MSB发生时创建。
    - 如果 l0 < l1 (当前低点低于前一个低点，表示强烈的看涨结构)，则标记为 "Bu-BB" (突破块)。
    - 否则，标记为 "Bu-MB" (缓解块)。
- **看跌块 (****Be-BB/Be-MB****)**:
    - 在看跌MSB发生时创建。
    - 如果 h0 > h1 (当前高点高于前一个高点，表示强烈的看跌结构)，则标记为 "Be-BB" (突破块)。
    - 否则，标记为 "Be-MB" (缓解块)。

这些方框同样使用 box.new 创建并向右延伸。

### 6. 块的管理 (Box Management)

脚本会持续管理图表上的订单块和突破块/缓解块：

- **更新方框**: 对于所有活动的方框，box.set_right(box, bar_index + 10) 会将其右侧边界更新到当前 K 线之后10根 K 线的位置，确保方框在价格图上持续显示。
- **删除方框 (f_delete_box)**:
    - 如果启用了 delete_boxes 设置，**当一个块被“突破”或“失效”时，它会被删除**。
    - 对于**看涨块** (Bu-OB, Bu-BB, Bu-MB)：如果 close < bottom (收盘价低于块的底部)，则认为该块失效并被删除。
    - 对于**看跌块** (Be-OB, Be-BB, Be-MB)：如果 close > top (收盘价高于块的顶部)，则认为该块失效并被删除。
- **警报**:
    - 当价格进入一个订单块或突破块/缓解块的区域时（例如，对于看涨块，close < top 但不低于 bottom），会触发相应的“Price in the BU-OB zone”等警报信息。

### 7. 警报条件 (Alert Conditions)

- alertcondition(ta.change(market) != 0, "MSB", "MSB"): 当市场结构发生变化（即MSB发生）时，会触发一个名为“MSB”的警报。

## Ref

[[ICT 笔记]] 
