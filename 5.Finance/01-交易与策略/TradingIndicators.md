---
title: "TradingIndicators"
type: concept
created: 2025-10-03
updated: 2025-11-29
tags: [notion-import]
---

## 概念

TradingView 指标名称：**Market Structure Break & Order Block by EmreKb**

1. **市场结构突破 M****SB：****价格突破前期高点后创出新低，或者突破前期低点后创出新高时，就会出现市场结构突破（msb）**。
1. **订单块 OB：**出现在市场结构突破（msb）之后。
如果市场结构突破（msb）是**看跌**的，那么订单块（ob）就是**高点之前的最后一根看涨蜡烛线**

如果市场结构突破（msb）是**看涨**的，那么订单块（ob）就是**低点之前的最后一根看跌蜡烛线**

![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/c9678d23-e296-817b-849e-0003ceb9774c/dfc8f4d9-c45b-41b4-9cc4-78c54e16f03d/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4666IRC4E2J%2F20260418%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260418T032644Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBoaCXVzLXdlc3QtMiJIMEYCIQCTXQCxwlYgZJLSi1iChi1z9%2Ft9cBSjQOWObrZzHnb25QIhAKmli9KtHNh1tk8Fg0atnevaeXlXBlwQ0%2FkP%2B5ITE%2FSRKogECOP%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNjM3NDIzMTgzODA1IgzPeEiRFC7Jj%2B3i%2Fm0q3AMMVpoGFo1iVHh3OAkmtDLGkLJRutSZvBWbO%2B4vv%2FxC1Dg%2FcD1nqF1jyibiiKxq4pb3a4orkCf4I%2FlS9YcK275VVdjt2yF05SPC75ulnsAFKz6NreC%2BfVRWa699Nsp6Qtgle2rNpOjPAofvfaRjbqFCCnjylHe9JOeXx9KhfWk6AyrahsB8o7ZA%2FAZbMg5PTMTdK0gRsTl%2FgVatUZba6illEn8F2EiVQv%2FkjUkTH8nBmwQMzOQPv1dZk6MQuJP7ItdPVERkYPsr1tr6YAViMgC3gy%2FJ64Cd6ZeqTBrUIDPAjuEBWGu%2FpzVv508FlYHmzKacBsourFKJ0jd8JtAeciKH9uvsOnT9yZOwEnCF0uXzQKXPjUBhLwSjz0kQXwXmUnLu34DVw%2BEGiWSeYzXbLiE8XMz2WoC4AsxHao7IR%2F37jNG0Rj3lPqmyfT4iNuTE6aC0g%2FhSUsJCdL%2BUgPWsJ2QCPJFcYmWei0VG5uswjlq6fpbyPscM2cO7rEHDaNNnCMCiATL4EbvXmAyTH%2FahctqMeyY5ESmgwY835O5B14HbKClt1ys%2Fb1RJ3fFBhDSeuaPPvQgpLYJsYZeVG0bWZ7OzsLfgf62wlQT6kKefoQwva7l2pFeZJTP0gG2RtzDsxovPBjqkASSspVM3UCIOZbFqBvaplQgNrvovRqXeYGmrCiLam4d88KzhHG3HMspU4EDi7qTxsOZvM2IQi44ydwfy2pwZ9QMjFQB%2Fuv6q6vXtIt6h8dJ6e1a65rJEE2jc6YCF4mo%2BvkNvX7TVJpjbIwDPVX4p%2Fp%2BDoAYe77Z9wIA0wP51O8d3Jd%2FdlDV5Mq%2FS5Pk4LYmmZaGwOB7Du1JWvatjrljc71aklDVt&X-Amz-Signature=1541db14631c9c85eaea7abd97dc7e063174eb39f840465379ed19fad30cdd7f&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

1. **缓解块 MB：****MSB 失败后，原来的OB转变成反方向的MB。**
![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/c9678d23-e296-817b-849e-0003ceb9774c/3a6c15ea-0931-40fe-9260-38e589f3be01/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4666IRC4E2J%2F20260418%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260418T032644Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBoaCXVzLXdlc3QtMiJIMEYCIQCTXQCxwlYgZJLSi1iChi1z9%2Ft9cBSjQOWObrZzHnb25QIhAKmli9KtHNh1tk8Fg0atnevaeXlXBlwQ0%2FkP%2B5ITE%2FSRKogECOP%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNjM3NDIzMTgzODA1IgzPeEiRFC7Jj%2B3i%2Fm0q3AMMVpoGFo1iVHh3OAkmtDLGkLJRutSZvBWbO%2B4vv%2FxC1Dg%2FcD1nqF1jyibiiKxq4pb3a4orkCf4I%2FlS9YcK275VVdjt2yF05SPC75ulnsAFKz6NreC%2BfVRWa699Nsp6Qtgle2rNpOjPAofvfaRjbqFCCnjylHe9JOeXx9KhfWk6AyrahsB8o7ZA%2FAZbMg5PTMTdK0gRsTl%2FgVatUZba6illEn8F2EiVQv%2FkjUkTH8nBmwQMzOQPv1dZk6MQuJP7ItdPVERkYPsr1tr6YAViMgC3gy%2FJ64Cd6ZeqTBrUIDPAjuEBWGu%2FpzVv508FlYHmzKacBsourFKJ0jd8JtAeciKH9uvsOnT9yZOwEnCF0uXzQKXPjUBhLwSjz0kQXwXmUnLu34DVw%2BEGiWSeYzXbLiE8XMz2WoC4AsxHao7IR%2F37jNG0Rj3lPqmyfT4iNuTE6aC0g%2FhSUsJCdL%2BUgPWsJ2QCPJFcYmWei0VG5uswjlq6fpbyPscM2cO7rEHDaNNnCMCiATL4EbvXmAyTH%2FahctqMeyY5ESmgwY835O5B14HbKClt1ys%2Fb1RJ3fFBhDSeuaPPvQgpLYJsYZeVG0bWZ7OzsLfgf62wlQT6kKefoQwva7l2pFeZJTP0gG2RtzDsxovPBjqkASSspVM3UCIOZbFqBvaplQgNrvovRqXeYGmrCiLam4d88KzhHG3HMspU4EDi7qTxsOZvM2IQi44ydwfy2pwZ9QMjFQB%2Fuv6q6vXtIt6h8dJ6e1a65rJEE2jc6YCF4mo%2BvkNvX7TVJpjbIwDPVX4p%2Fp%2BDoAYe77Z9wIA0wP51O8d3Jd%2FdlDV5Mq%2FS5Pk4LYmmZaGwOB7Du1JWvatjrljc71aklDVt&X-Amz-Signature=5f90fa02bf03d10983119557eb0cd96a42d5ba9ce0e17ff3b7215ac150ffeaa8&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

1. **突破块 BB：****之前的下降趋势中的摆动低点被突破（反之），价格又回到该水平进行测试时，就会出现**。
![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/c9678d23-e296-817b-849e-0003ceb9774c/ad04e1f3-ba66-4f13-a662-ec6b496d52d0/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4666IRC4E2J%2F20260418%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260418T032644Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBoaCXVzLXdlc3QtMiJIMEYCIQCTXQCxwlYgZJLSi1iChi1z9%2Ft9cBSjQOWObrZzHnb25QIhAKmli9KtHNh1tk8Fg0atnevaeXlXBlwQ0%2FkP%2B5ITE%2FSRKogECOP%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNjM3NDIzMTgzODA1IgzPeEiRFC7Jj%2B3i%2Fm0q3AMMVpoGFo1iVHh3OAkmtDLGkLJRutSZvBWbO%2B4vv%2FxC1Dg%2FcD1nqF1jyibiiKxq4pb3a4orkCf4I%2FlS9YcK275VVdjt2yF05SPC75ulnsAFKz6NreC%2BfVRWa699Nsp6Qtgle2rNpOjPAofvfaRjbqFCCnjylHe9JOeXx9KhfWk6AyrahsB8o7ZA%2FAZbMg5PTMTdK0gRsTl%2FgVatUZba6illEn8F2EiVQv%2FkjUkTH8nBmwQMzOQPv1dZk6MQuJP7ItdPVERkYPsr1tr6YAViMgC3gy%2FJ64Cd6ZeqTBrUIDPAjuEBWGu%2FpzVv508FlYHmzKacBsourFKJ0jd8JtAeciKH9uvsOnT9yZOwEnCF0uXzQKXPjUBhLwSjz0kQXwXmUnLu34DVw%2BEGiWSeYzXbLiE8XMz2WoC4AsxHao7IR%2F37jNG0Rj3lPqmyfT4iNuTE6aC0g%2FhSUsJCdL%2BUgPWsJ2QCPJFcYmWei0VG5uswjlq6fpbyPscM2cO7rEHDaNNnCMCiATL4EbvXmAyTH%2FahctqMeyY5ESmgwY835O5B14HbKClt1ys%2Fb1RJ3fFBhDSeuaPPvQgpLYJsYZeVG0bWZ7OzsLfgf62wlQT6kKefoQwva7l2pFeZJTP0gG2RtzDsxovPBjqkASSspVM3UCIOZbFqBvaplQgNrvovRqXeYGmrCiLam4d88KzhHG3HMspU4EDi7qTxsOZvM2IQi44ydwfy2pwZ9QMjFQB%2Fuv6q6vXtIt6h8dJ6e1a65rJEE2jc6YCF4mo%2BvkNvX7TVJpjbIwDPVX4p%2Fp%2BDoAYe77Z9wIA0wP51O8d3Jd%2FdlDV5Mq%2FS5Pk4LYmmZaGwOB7Du1JWvatjrljc71aklDVt&X-Amz-Signature=72a4a3fa74d8d533925cd82f64bb891c59b76864d1e189256a561f9eb560a130&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

## 案例

### 2025.10.10_bitcoin插针

![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/c9678d23-e296-817b-849e-0003ceb9774c/119a45e5-8d8d-48f7-8818-aac858a36b13/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4666IRC4E2J%2F20260418%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260418T032644Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBoaCXVzLXdlc3QtMiJIMEYCIQCTXQCxwlYgZJLSi1iChi1z9%2Ft9cBSjQOWObrZzHnb25QIhAKmli9KtHNh1tk8Fg0atnevaeXlXBlwQ0%2FkP%2B5ITE%2FSRKogECOP%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNjM3NDIzMTgzODA1IgzPeEiRFC7Jj%2B3i%2Fm0q3AMMVpoGFo1iVHh3OAkmtDLGkLJRutSZvBWbO%2B4vv%2FxC1Dg%2FcD1nqF1jyibiiKxq4pb3a4orkCf4I%2FlS9YcK275VVdjt2yF05SPC75ulnsAFKz6NreC%2BfVRWa699Nsp6Qtgle2rNpOjPAofvfaRjbqFCCnjylHe9JOeXx9KhfWk6AyrahsB8o7ZA%2FAZbMg5PTMTdK0gRsTl%2FgVatUZba6illEn8F2EiVQv%2FkjUkTH8nBmwQMzOQPv1dZk6MQuJP7ItdPVERkYPsr1tr6YAViMgC3gy%2FJ64Cd6ZeqTBrUIDPAjuEBWGu%2FpzVv508FlYHmzKacBsourFKJ0jd8JtAeciKH9uvsOnT9yZOwEnCF0uXzQKXPjUBhLwSjz0kQXwXmUnLu34DVw%2BEGiWSeYzXbLiE8XMz2WoC4AsxHao7IR%2F37jNG0Rj3lPqmyfT4iNuTE6aC0g%2FhSUsJCdL%2BUgPWsJ2QCPJFcYmWei0VG5uswjlq6fpbyPscM2cO7rEHDaNNnCMCiATL4EbvXmAyTH%2FahctqMeyY5ESmgwY835O5B14HbKClt1ys%2Fb1RJ3fFBhDSeuaPPvQgpLYJsYZeVG0bWZ7OzsLfgf62wlQT6kKefoQwva7l2pFeZJTP0gG2RtzDsxovPBjqkASSspVM3UCIOZbFqBvaplQgNrvovRqXeYGmrCiLam4d88KzhHG3HMspU4EDi7qTxsOZvM2IQi44ydwfy2pwZ9QMjFQB%2Fuv6q6vXtIt6h8dJ6e1a65rJEE2jc6YCF4mo%2BvkNvX7TVJpjbIwDPVX4p%2Fp%2BDoAYe77Z9wIA0wP51O8d3Jd%2FdlDV5Mq%2FS5Pk4LYmmZaGwOB7Du1JWvatjrljc71aklDVt&X-Amz-Signature=2c8d0314b9e756c302da529753139dadea24831f0115e436a3aed77f2cf31c9f&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/c9678d23-e296-817b-849e-0003ceb9774c/fc40b161-36c7-4006-b588-a7682374eb32/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4666IRC4E2J%2F20260418%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260418T032644Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBoaCXVzLXdlc3QtMiJIMEYCIQCTXQCxwlYgZJLSi1iChi1z9%2Ft9cBSjQOWObrZzHnb25QIhAKmli9KtHNh1tk8Fg0atnevaeXlXBlwQ0%2FkP%2B5ITE%2FSRKogECOP%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNjM3NDIzMTgzODA1IgzPeEiRFC7Jj%2B3i%2Fm0q3AMMVpoGFo1iVHh3OAkmtDLGkLJRutSZvBWbO%2B4vv%2FxC1Dg%2FcD1nqF1jyibiiKxq4pb3a4orkCf4I%2FlS9YcK275VVdjt2yF05SPC75ulnsAFKz6NreC%2BfVRWa699Nsp6Qtgle2rNpOjPAofvfaRjbqFCCnjylHe9JOeXx9KhfWk6AyrahsB8o7ZA%2FAZbMg5PTMTdK0gRsTl%2FgVatUZba6illEn8F2EiVQv%2FkjUkTH8nBmwQMzOQPv1dZk6MQuJP7ItdPVERkYPsr1tr6YAViMgC3gy%2FJ64Cd6ZeqTBrUIDPAjuEBWGu%2FpzVv508FlYHmzKacBsourFKJ0jd8JtAeciKH9uvsOnT9yZOwEnCF0uXzQKXPjUBhLwSjz0kQXwXmUnLu34DVw%2BEGiWSeYzXbLiE8XMz2WoC4AsxHao7IR%2F37jNG0Rj3lPqmyfT4iNuTE6aC0g%2FhSUsJCdL%2BUgPWsJ2QCPJFcYmWei0VG5uswjlq6fpbyPscM2cO7rEHDaNNnCMCiATL4EbvXmAyTH%2FahctqMeyY5ESmgwY835O5B14HbKClt1ys%2Fb1RJ3fFBhDSeuaPPvQgpLYJsYZeVG0bWZ7OzsLfgf62wlQT6kKefoQwva7l2pFeZJTP0gG2RtzDsxovPBjqkASSspVM3UCIOZbFqBvaplQgNrvovRqXeYGmrCiLam4d88KzhHG3HMspU4EDi7qTxsOZvM2IQi44ydwfy2pwZ9QMjFQB%2Fuv6q6vXtIt6h8dJ6e1a65rJEE2jc6YCF4mo%2BvkNvX7TVJpjbIwDPVX4p%2Fp%2BDoAYe77Z9wIA0wP51O8d3Jd%2FdlDV5Mq%2FS5Pk4LYmmZaGwOB7Du1JWvatjrljc71aklDVt&X-Amz-Signature=e566d721d74d8574d6a21f0f26bd1a5703c1e6d59bbeb0f11157699ed41b535d&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

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

1. **突破块 (Breaker Block BB)**: 当之前的摆动高点（在上升趋势中）或摆动低点（在下降趋势中）**被突破后，价格又回到该水平进行测试时，就会出现**。导致突破的 K 线组成了“突破块”。
1. **缓解块 (Mitigation Block MB)**: **当市场未能创建更高的高点（在看涨情况下）或更低的低点（在看跌情况下），并且价格回撤到最后一个订单流区域时，就会形成。本质上，当一个订单块被价格突破但未能引发预期的延续时，它就可能转变为缓解块。**
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

[ICT 笔记](https://www.notion.so/28078d23e2968020bf9de1733d2b3802) 

## Volume Profile 概念

> 按 **价格水平** 来统计成交量，而不是按时间

1. **POC (Point of Control)**
- **成交量最大的价格水平**（“最活跃的战场”）。
- 市场通常会**在这个价格附近停留很久，反复博弈**。
1. **VAH / VAL (Value Area High / Low)**
- 包含 **70% 成交量** 的区域范围。
- 就像“**成交量密集区**”，很多人把它看成**支撑/阻力区域**。
- **Low Volume Node (LVN)**
- **成交量稀少的价格区域**。
- 价格往往会**“快速通过”这些区域，不会停留太久**。
## Indicator 1

TradingView 指标名称：**Market sessions and Volume profile - By Leviathan**

1. **查看不同时间段的成交量分布**，每天/周/月/季度/年。
![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/c9678d23-e296-817b-849e-0003ceb9774c/157a4e9e-c371-4221-8534-fa81ec01c624/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4662PQ4MXKX%2F20260418%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260418T032652Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBkaCXVzLXdlc3QtMiJGMEQCIHbpMgSjoInLRhucENTW8Uu352WHQqlpIsIFfgAs%2FfYwAiA%2Bhet9TTK30HfhMz4877QdUb8hu2LPbyVh0qdx4jQmdyqIBAji%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDYzNzQyMzE4MzgwNSIMnFjpulqmyGlW1dd8KtwDYqAR0LwsAm%2BWkqZNP4jd%2B0aEYnzcJqECnF5O7%2BGf6b19qWHVKLfWMYNsxHGo7rYhpkYfbTuz9NFPk%2FzF9YlQgn521tOLmlXXTM%2FQW85ANbdVjNjoedgjVn2vRNEEIPnOk1Wf36lYZghBoOwZusHlQoleU2IKIlHlZqvvLfz96HA2o9y8Y9S1XjloGrQ31FzuP%2FXe4qFuAFeZojpEIwfoswHBxt20FyZH1TFrbH7sPyT8kd6bdzqbCmvveXJvB0dQ1orsX4uxCdOsGpg9mjtsLmgOWwINmZ1LT3liY3GVXn7QGgQYinh%2BxHv6AlKSaJKFn52fG%2B8KrT3kyaWkHldxZgcwmzKB11QyyHhiGhP3v65%2FomPOmpntcyPgPGZlV1MAtgJN0G2Uo6c%2BgbZWBY41TIFUpL%2B68Spr%2F%2F0%2BAu3M3WDsUChWZGXRknUKumsmLHdhkf1zmq9VE29zrukib4Pg91Ve7sdqBNFf7XgMwT9wRYjB3HxadCpImKNxQXdm9XX0v3wjhneb%2FmMSa45dRy9bXzazorBqDHCtY4JfkmZ2AZPUBAKuEVGQKbQriN8PALwpZGFGOJ0owe1ODtEx6vjngrv4XDbQBEjLTA9c%2B6t5tP5ixz0jX85NVDkWDrUw%2B66LzwY6pgHYWBzw8g%2FEfyayzQddrplrArwqrAYM0f4naOBsbxBKjGZC7FtU3fRBLrqPmHY7tmUHGeX%2FpiJLhUxfsr42ltbpNfEogk36zPdj3ieBwFvrT5JhYBsjItDiTLWXV0kd%2BJPU2RDqdJNeHRKnSP15SLXUXI%2BVMS8%2BqDde89Q62QIgfF%2BpbyxfcpYN8y99ZMax7STr2aIBSOrv%2BS1D%2BGOclydsto7Rr2Fe&X-Amz-Signature=96f6b26638c6a2fa934e608b1b0eed4750d78bd2a2ed03c5379afd762a34d7dd&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/c9678d23-e296-817b-849e-0003ceb9774c/9ee5ccab-febc-4e86-a4c6-85d9dcd54381/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4662PQ4MXKX%2F20260418%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260418T032652Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBkaCXVzLXdlc3QtMiJGMEQCIHbpMgSjoInLRhucENTW8Uu352WHQqlpIsIFfgAs%2FfYwAiA%2Bhet9TTK30HfhMz4877QdUb8hu2LPbyVh0qdx4jQmdyqIBAji%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDYzNzQyMzE4MzgwNSIMnFjpulqmyGlW1dd8KtwDYqAR0LwsAm%2BWkqZNP4jd%2B0aEYnzcJqECnF5O7%2BGf6b19qWHVKLfWMYNsxHGo7rYhpkYfbTuz9NFPk%2FzF9YlQgn521tOLmlXXTM%2FQW85ANbdVjNjoedgjVn2vRNEEIPnOk1Wf36lYZghBoOwZusHlQoleU2IKIlHlZqvvLfz96HA2o9y8Y9S1XjloGrQ31FzuP%2FXe4qFuAFeZojpEIwfoswHBxt20FyZH1TFrbH7sPyT8kd6bdzqbCmvveXJvB0dQ1orsX4uxCdOsGpg9mjtsLmgOWwINmZ1LT3liY3GVXn7QGgQYinh%2BxHv6AlKSaJKFn52fG%2B8KrT3kyaWkHldxZgcwmzKB11QyyHhiGhP3v65%2FomPOmpntcyPgPGZlV1MAtgJN0G2Uo6c%2BgbZWBY41TIFUpL%2B68Spr%2F%2F0%2BAu3M3WDsUChWZGXRknUKumsmLHdhkf1zmq9VE29zrukib4Pg91Ve7sdqBNFf7XgMwT9wRYjB3HxadCpImKNxQXdm9XX0v3wjhneb%2FmMSa45dRy9bXzazorBqDHCtY4JfkmZ2AZPUBAKuEVGQKbQriN8PALwpZGFGOJ0owe1ODtEx6vjngrv4XDbQBEjLTA9c%2B6t5tP5ixz0jX85NVDkWDrUw%2B66LzwY6pgHYWBzw8g%2FEfyayzQddrplrArwqrAYM0f4naOBsbxBKjGZC7FtU3fRBLrqPmHY7tmUHGeX%2FpiJLhUxfsr42ltbpNfEogk36zPdj3ieBwFvrT5JhYBsjItDiTLWXV0kd%2BJPU2RDqdJNeHRKnSP15SLXUXI%2BVMS8%2BqDde89Q62QIgfF%2BpbyxfcpYN8y99ZMax7STr2aIBSOrv%2BS1D%2BGOclydsto7Rr2Fe&X-Amz-Signature=f52202809dcef5c9b6f8730b45381f2f39d22d1733c4a72fbf6ba2dcd96429a2&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

## Indicator 2

TradingView 指标名称：**VPVRVolume Profile Visible Range For All Accounts**

1. **在当前屏幕可见的K线范围上，自动更新成交量分布图**
![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/c9678d23-e296-817b-849e-0003ceb9774c/948c54c8-ad02-4853-bdd0-318beef035c7/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4662PQ4MXKX%2F20260418%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260418T032652Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBkaCXVzLXdlc3QtMiJGMEQCIHbpMgSjoInLRhucENTW8Uu352WHQqlpIsIFfgAs%2FfYwAiA%2Bhet9TTK30HfhMz4877QdUb8hu2LPbyVh0qdx4jQmdyqIBAji%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDYzNzQyMzE4MzgwNSIMnFjpulqmyGlW1dd8KtwDYqAR0LwsAm%2BWkqZNP4jd%2B0aEYnzcJqECnF5O7%2BGf6b19qWHVKLfWMYNsxHGo7rYhpkYfbTuz9NFPk%2FzF9YlQgn521tOLmlXXTM%2FQW85ANbdVjNjoedgjVn2vRNEEIPnOk1Wf36lYZghBoOwZusHlQoleU2IKIlHlZqvvLfz96HA2o9y8Y9S1XjloGrQ31FzuP%2FXe4qFuAFeZojpEIwfoswHBxt20FyZH1TFrbH7sPyT8kd6bdzqbCmvveXJvB0dQ1orsX4uxCdOsGpg9mjtsLmgOWwINmZ1LT3liY3GVXn7QGgQYinh%2BxHv6AlKSaJKFn52fG%2B8KrT3kyaWkHldxZgcwmzKB11QyyHhiGhP3v65%2FomPOmpntcyPgPGZlV1MAtgJN0G2Uo6c%2BgbZWBY41TIFUpL%2B68Spr%2F%2F0%2BAu3M3WDsUChWZGXRknUKumsmLHdhkf1zmq9VE29zrukib4Pg91Ve7sdqBNFf7XgMwT9wRYjB3HxadCpImKNxQXdm9XX0v3wjhneb%2FmMSa45dRy9bXzazorBqDHCtY4JfkmZ2AZPUBAKuEVGQKbQriN8PALwpZGFGOJ0owe1ODtEx6vjngrv4XDbQBEjLTA9c%2B6t5tP5ixz0jX85NVDkWDrUw%2B66LzwY6pgHYWBzw8g%2FEfyayzQddrplrArwqrAYM0f4naOBsbxBKjGZC7FtU3fRBLrqPmHY7tmUHGeX%2FpiJLhUxfsr42ltbpNfEogk36zPdj3ieBwFvrT5JhYBsjItDiTLWXV0kd%2BJPU2RDqdJNeHRKnSP15SLXUXI%2BVMS8%2BqDde89Q62QIgfF%2BpbyxfcpYN8y99ZMax7STr2aIBSOrv%2BS1D%2BGOclydsto7Rr2Fe&X-Amz-Signature=309688ef760b2090563959c16ff6d9396b644ece49a3c2dd5b8e6b89c16e59a5&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

coinglass

![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/c9678d23-e296-817b-849e-0003ceb9774c/aaf28be1-031f-466e-a286-7cd8ce879aa4/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4662PQ4MXKX%2F20260418%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260418T032652Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBkaCXVzLXdlc3QtMiJGMEQCIHbpMgSjoInLRhucENTW8Uu352WHQqlpIsIFfgAs%2FfYwAiA%2Bhet9TTK30HfhMz4877QdUb8hu2LPbyVh0qdx4jQmdyqIBAji%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDYzNzQyMzE4MzgwNSIMnFjpulqmyGlW1dd8KtwDYqAR0LwsAm%2BWkqZNP4jd%2B0aEYnzcJqECnF5O7%2BGf6b19qWHVKLfWMYNsxHGo7rYhpkYfbTuz9NFPk%2FzF9YlQgn521tOLmlXXTM%2FQW85ANbdVjNjoedgjVn2vRNEEIPnOk1Wf36lYZghBoOwZusHlQoleU2IKIlHlZqvvLfz96HA2o9y8Y9S1XjloGrQ31FzuP%2FXe4qFuAFeZojpEIwfoswHBxt20FyZH1TFrbH7sPyT8kd6bdzqbCmvveXJvB0dQ1orsX4uxCdOsGpg9mjtsLmgOWwINmZ1LT3liY3GVXn7QGgQYinh%2BxHv6AlKSaJKFn52fG%2B8KrT3kyaWkHldxZgcwmzKB11QyyHhiGhP3v65%2FomPOmpntcyPgPGZlV1MAtgJN0G2Uo6c%2BgbZWBY41TIFUpL%2B68Spr%2F%2F0%2BAu3M3WDsUChWZGXRknUKumsmLHdhkf1zmq9VE29zrukib4Pg91Ve7sdqBNFf7XgMwT9wRYjB3HxadCpImKNxQXdm9XX0v3wjhneb%2FmMSa45dRy9bXzazorBqDHCtY4JfkmZ2AZPUBAKuEVGQKbQriN8PALwpZGFGOJ0owe1ODtEx6vjngrv4XDbQBEjLTA9c%2B6t5tP5ixz0jX85NVDkWDrUw%2B66LzwY6pgHYWBzw8g%2FEfyayzQddrplrArwqrAYM0f4naOBsbxBKjGZC7FtU3fRBLrqPmHY7tmUHGeX%2FpiJLhUxfsr42ltbpNfEogk36zPdj3ieBwFvrT5JhYBsjItDiTLWXV0kd%2BJPU2RDqdJNeHRKnSP15SLXUXI%2BVMS8%2BqDde89Q62QIgfF%2BpbyxfcpYN8y99ZMax7STr2aIBSOrv%2BS1D%2BGOclydsto7Rr2Fe&X-Amz-Signature=088290d599c2ab2911a37b2e0e04b7512345549f51882b695d315eac4f177b52&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

## 概念

TradingView 指标名称：**Sessions [LuxAlgo]**

1. **外汇/股市主要交易时段显示指标**：纽约、伦敦、东京、悉尼四大交易时段。
![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/c9678d23-e296-817b-849e-0003ceb9774c/84132794-3d11-43e5-9c70-3882f259d801/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466ROMRTTM3%2F20260418%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260418T032656Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBkaCXVzLXdlc3QtMiJIMEYCIQCD0UqaW8Nwgxsj5yybiia6jNB%2BEBeOO%2Bu7STMUY6O%2BegIhAK09sdjRcvIbDblYy1%2BOmPGskWzrDsOYNKSf7%2BIX6DevKogECOL%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNjM3NDIzMTgzODA1IgwZil5KKbpwUr81FaUq3AOgaOjtSzBi6wBhCoklMVuGdbz0rOUTW6mmh83L9UOScNmZfgLQykZ1tM6yedk6mZ0KvaYzK%2BC62SM%2BNgOjdoOPAY6RCjnBdf6Pqs1N3fVCXC%2Fn3jhFJ4Bbd9qlU5EuBgo%2FFq8TuF8HWxkn7uCVKnvPEkUZtLkTr4rmVAY26bnxcKGz3ID0zJIqjQtNoTG0%2FgWQvfVyROHiQ5sCEj2sBOKWl3crPJqRwqZrO8nOEUcEwuGpYR79CrtYJMdJJZD%2F7KYIt9N%2Bjo5%2BPsE4DZvXvzLTUzhqTPj3E%2BSjp6KDF2IyN6xjRkerxQGIfr1iqZ%2BcXBjq39Rwk3upWxMUrGK%2BqDxs1IcNmUy8eprSNdrduflAOvNzA7Eussu0m8yVT9szs5CMxxFRmMPtVEsY1x%2FbpqRXw4Vqcp%2FaPGKJqsIC24rxrXr61jmvBTh8Au4if7HIkEOH9wfn%2BdaOn0SEJlZ2mrT4F8zvd79CSGWZaf3CyFmPTdTRwegmERYNqG9lDMN1UbLv1PwyEBwZHrfNHoQ2Ma6TC0pz6b37ryowOt3ccZX3ptMSscxvj3gDnhdcL8C0keYZRmz9LV7NrPmKMeWNCD2clBz%2FTd1SXC19aiO7iA4TDSbPMX6Aog9GYNpDXzD4rIvPBjqkAfVfWHhAtU%2BYJVU29EDot704eiMKU0bZ5YCWtv3hYRUffpW%2BWWNIbUI0F8%2FKF32htGqp3DZQMoBFy8Pg7i0YImjG9Zqa4rBgN2BIn6XbfUinDRahUQnFuU0kzYavPxl3qjHNyppGXzbNY3zkH4X5b9rmqiVSOfj2Q90wCgAgZidPqsv%2FCDJtxvncxkJAmahIGtsOPPTFbC8Ogu1UInLH1QC8lhpJ&X-Amz-Signature=37c0a70e36ff5fb1f9a4b53dbdca690151a04939245d4ba1b0fcfdcd6a93aae3&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

1. 可以修改所在国家的时区
![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/c9678d23-e296-817b-849e-0003ceb9774c/2d8dd0fa-6f98-4c0d-ad56-b30300056ed0/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466ROMRTTM3%2F20260418%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260418T032656Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBkaCXVzLXdlc3QtMiJIMEYCIQCD0UqaW8Nwgxsj5yybiia6jNB%2BEBeOO%2Bu7STMUY6O%2BegIhAK09sdjRcvIbDblYy1%2BOmPGskWzrDsOYNKSf7%2BIX6DevKogECOL%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNjM3NDIzMTgzODA1IgwZil5KKbpwUr81FaUq3AOgaOjtSzBi6wBhCoklMVuGdbz0rOUTW6mmh83L9UOScNmZfgLQykZ1tM6yedk6mZ0KvaYzK%2BC62SM%2BNgOjdoOPAY6RCjnBdf6Pqs1N3fVCXC%2Fn3jhFJ4Bbd9qlU5EuBgo%2FFq8TuF8HWxkn7uCVKnvPEkUZtLkTr4rmVAY26bnxcKGz3ID0zJIqjQtNoTG0%2FgWQvfVyROHiQ5sCEj2sBOKWl3crPJqRwqZrO8nOEUcEwuGpYR79CrtYJMdJJZD%2F7KYIt9N%2Bjo5%2BPsE4DZvXvzLTUzhqTPj3E%2BSjp6KDF2IyN6xjRkerxQGIfr1iqZ%2BcXBjq39Rwk3upWxMUrGK%2BqDxs1IcNmUy8eprSNdrduflAOvNzA7Eussu0m8yVT9szs5CMxxFRmMPtVEsY1x%2FbpqRXw4Vqcp%2FaPGKJqsIC24rxrXr61jmvBTh8Au4if7HIkEOH9wfn%2BdaOn0SEJlZ2mrT4F8zvd79CSGWZaf3CyFmPTdTRwegmERYNqG9lDMN1UbLv1PwyEBwZHrfNHoQ2Ma6TC0pz6b37ryowOt3ccZX3ptMSscxvj3gDnhdcL8C0keYZRmz9LV7NrPmKMeWNCD2clBz%2FTd1SXC19aiO7iA4TDSbPMX6Aog9GYNpDXzD4rIvPBjqkAfVfWHhAtU%2BYJVU29EDot704eiMKU0bZ5YCWtv3hYRUffpW%2BWWNIbUI0F8%2FKF32htGqp3DZQMoBFy8Pg7i0YImjG9Zqa4rBgN2BIn6XbfUinDRahUQnFuU0kzYavPxl3qjHNyppGXzbNY3zkH4X5b9rmqiVSOfj2Q90wCgAgZidPqsv%2FCDJtxvncxkJAmahIGtsOPPTFbC8Ogu1UInLH1QC8lhpJ&X-Amz-Signature=befd188cccb86561ded114b138982f6c1796c57694085baa6176ceb6ed404226&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

## 概念

TradingView 指标名称：**ICT Killzones + Pivots [TFO]**

1. **热战区**：基于你本地时间（排除夜间），显示机构经常活动的战区。
![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/c9678d23-e296-817b-849e-0003ceb9774c/0a29a037-954e-404e-b463-a02df03ff330/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466TYTZAJ25%2F20260418%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260418T032656Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBkaCXVzLXdlc3QtMiJHMEUCIQD5HEVzPpKKQJhV%2B32eTVZsC%2BEvx3J2djY4eUhfBstqqQIgHeie6S8KWgeVHyhIQGz%2FwgicVgg4%2BBjb7NM86LQg%2BigqiAQI4v%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDGd2RTVJme%2FGZzb42yrcA5f1m00L2VUXTgVnpg3%2BM%2Fxuq9V%2FicZ2w1V3pWkLK9GxFXmWDz8jDil3xh17QNNlGYZiPq0PZBtqUDRI3nSz7iEAM3Cr%2BohNbeaOT2Qsfrorq%2FUrGO8BP4deXQAmdWNKW0zc%2FLMdY31Ya71iq1pXqUIoUiHoTSWzTPCxZeDtl3GAXEoeCjBB9jPwInBPZfbEXGL%2BB5HiRbI2fH%2Fw5vMvUIZq9Odfnm6uHax5jh2giX8oRiHy%2F31mTkLynfAE%2BhZoVyVxwv4iekbIDPk%2BYaI26LD84JVVa14erIQ5NE0bnHe0vvunRP6KCaOPvUhLjYITnO8fqPeBOl6y%2FBNVyFzunXPOWAPAVXp40cFX%2Fbrc%2B4Fo%2F2hyYygrTSp5va5varDGpkj773Mge%2FBfmTw0pwpLQD140efsPG9CN55S2%2BxJk%2Fj1SiR%2FOMXfkiJgyLq85VMvytOoplt1m9SUHqFmYITjz79NLYQOAgG3jjKyb0U%2B8ErgCTV398cKqQyQOYUhKi77zxmNjd6mHIbnLbgjmQHQEKCrYdOIOVWZ0CyR82Ab%2BzZJeobaOmSkyGM%2FEDFB%2BLG5gkTbR9nnnPctFMGtwPjR5WH9USXeq2SXxZxSb0Txe4W%2FWd6nKSLOi2LHy%2BkCMNuti88GOqUB5cA0HJzt%2BwRBtTfsfzDIdNCxvyCCfPHycmUKfs7FiQyy8fYW%2FGOeEAtxTGhFekqecNiHDT3V10yqf%2BT9theWQtfuety50vL1XaMskiqSn481jdkLeYCcQO1wEp2utqK%2F%2FF4Da1VUcbJT0Qu6xdZZXLe1C%2F0eh4lXmPiATAlDAamp5t6A7qPr329FdcFYDNvGMFI%2B7F7tEa4BzfBehSk0ID3J0VXD&X-Amz-Signature=3a77084275c6ad1d3e7fbdcdf3fdce843401c9d0072a572debe90e83caaddc82&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

1. **设置**：右键可以设置自己偏好的作战区间
![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/c9678d23-e296-817b-849e-0003ceb9774c/bff06f9a-cb98-4e0f-b0cd-b63862d6a6e8/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466TYTZAJ25%2F20260418%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260418T032656Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBkaCXVzLXdlc3QtMiJHMEUCIQD5HEVzPpKKQJhV%2B32eTVZsC%2BEvx3J2djY4eUhfBstqqQIgHeie6S8KWgeVHyhIQGz%2FwgicVgg4%2BBjb7NM86LQg%2BigqiAQI4v%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDGd2RTVJme%2FGZzb42yrcA5f1m00L2VUXTgVnpg3%2BM%2Fxuq9V%2FicZ2w1V3pWkLK9GxFXmWDz8jDil3xh17QNNlGYZiPq0PZBtqUDRI3nSz7iEAM3Cr%2BohNbeaOT2Qsfrorq%2FUrGO8BP4deXQAmdWNKW0zc%2FLMdY31Ya71iq1pXqUIoUiHoTSWzTPCxZeDtl3GAXEoeCjBB9jPwInBPZfbEXGL%2BB5HiRbI2fH%2Fw5vMvUIZq9Odfnm6uHax5jh2giX8oRiHy%2F31mTkLynfAE%2BhZoVyVxwv4iekbIDPk%2BYaI26LD84JVVa14erIQ5NE0bnHe0vvunRP6KCaOPvUhLjYITnO8fqPeBOl6y%2FBNVyFzunXPOWAPAVXp40cFX%2Fbrc%2B4Fo%2F2hyYygrTSp5va5varDGpkj773Mge%2FBfmTw0pwpLQD140efsPG9CN55S2%2BxJk%2Fj1SiR%2FOMXfkiJgyLq85VMvytOoplt1m9SUHqFmYITjz79NLYQOAgG3jjKyb0U%2B8ErgCTV398cKqQyQOYUhKi77zxmNjd6mHIbnLbgjmQHQEKCrYdOIOVWZ0CyR82Ab%2BzZJeobaOmSkyGM%2FEDFB%2BLG5gkTbR9nnnPctFMGtwPjR5WH9USXeq2SXxZxSb0Txe4W%2FWd6nKSLOi2LHy%2BkCMNuti88GOqUB5cA0HJzt%2BwRBtTfsfzDIdNCxvyCCfPHycmUKfs7FiQyy8fYW%2FGOeEAtxTGhFekqecNiHDT3V10yqf%2BT9theWQtfuety50vL1XaMskiqSn481jdkLeYCcQO1wEp2utqK%2F%2FF4Da1VUcbJT0Qu6xdZZXLe1C%2F0eh4lXmPiATAlDAamp5t6A7qPr329FdcFYDNvGMFI%2B7F7tEa4BzfBehSk0ID3J0VXD&X-Amz-Signature=9a90f9fbcc8d9f5f4c1e788576026d15180054348de24ab96614193b07f74cb1&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

## 概念

TradingView 指标名称：**Key Levels | Flux Charts**

1. **显示历史关键价位：**昨天、上周、上月、去年的最高最低值。
1. 可以根据偏好设置想显示的关键价位
![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/c9678d23-e296-817b-849e-0003ceb9774c/1fc3b52f-ef9c-4d4d-aa2b-b0152e893f54/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466Q3FUA74K%2F20260418%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260418T032657Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBkaCXVzLXdlc3QtMiJHMEUCICHKvyyY3MKN6kOfdtGt4QCkbdUSYdKKGZE8wDN4AW9GAiEAwDXmz8YaKXx3cy8AkI%2FVnOvfcLSv5FgEYwumuTyhDV4qiAQI4v%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDIeAs60dT5MWPF1kXircA3vLXNJavf7w5NOy3zME1yESFcfvmiWnjiNk%2F72fKmi%2FtXTNO%2B2rd0Xz7q%2BWaTSuk96pI1Gu%2F8ljTquOSrCxKhJsXBipxeazitgv5RA7EtwKlpqOA9hqQEDtp%2Bvz2JOrFvTIbPxMXxMv4AxTGHhZNjFvSvlYB9dYzpyKTQ3fiPcetz2CSV7sK481MRdeihr035GCtl2ztwWRfcYBEGbPg70PV%2B0eQDadLJcAXo4PdArUDzlHsh06WAZ92%2FFmZv28pVlE%2ByveP2nhQBVes0yrBbmWNDojciQ77hjcnpc62FHobb%2F9E1uKMhQ%2FEC4dz9XOW1P2xrN48Xck%2F4%2BWVLkZiNiuF13hdefZcLYUTFuZaA1l85MQQ1nwrTmWQB2cekhAZtM9tlC5LH1O31GClifupiJteB68m0Rwv5IOqGapcYn6U0sBIE5ARyXM0rKnBxcujq7ZKPKU1aIha7F%2FZC4IZR4yCmStAvnfavPkvHQ8gRzvzB%2B2CvlYYDWX1qcOMCv9yc9LcWAO1rIPOq%2FbPjkJxkM%2BLtmEVhti9sIRPiH8M7w9SG1GB6GcogJyGOPzqx6ZqgRa3AilK%2BewM0p5PLJyktrDxDcfrxgOMrsjhJjvZjFMzEIHAw6MuWOenjg3MJWvi88GOqUBng9vbIWzX7yfvbHeD3%2BZxR56hk0MU%2BchMROAew%2F5fxMS%2FMOoUv%2FAC9NvRx46%2FBs69wxtM3Ms3FmnLoOkwJyFniuvOMsIGCcl19zxJPgSbJDh5dUNvLzw2UxnfNytZJ5RfzT91Rp7e23Oih6LB9TagYcY%2B9ZIn856Dh3KA5eP32DY2%2BbnY2V%2BzjgfxfbfuDAvFTjV9EDUIgeW3juZ%2B9AVlv6Aj9vo&X-Amz-Signature=8d1df76bc3d1536d013da4636aa6baa10c8344befa6e3c320d007e6e9bd7497a&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

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
1. 油管币哥设置为：**20、60、120**
![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/c9678d23-e296-817b-849e-0003ceb9774c/dae7d048-56c3-4d90-9f75-efadb4d832af/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4663LQPQOHA%2F20260418%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260418T032657Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBkaCXVzLXdlc3QtMiJGMEQCID8e1ezKWr3RP%2FjXWq6UwkULHZrjDvt1OlHS%2Bv%2B9iEj1AiB6IokZf%2B3dmVmoZijYtSbiwYY9yx8yvDJl%2FqCt%2BWpQEiqIBAji%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDYzNzQyMzE4MzgwNSIMay%2FkHBYzSI37scLgKtwDyAh6qDFT5GznaX4sSr7B2C4BuuT23IxHkf3B8bNyLtcfKoGIzSxj%2BNaov9O6Oncthra6ahn6UQaeyHEQbUtuBzIY7oxat5ZfWftz1Yhb5flKgZ7Z7m3v9Zxnrq3xmhM7jRoEDDVJ5rV%2F44orwlFWcFk%2FEnGsGsd8OkRsjpwatQhL9ECFpYbmIy8zFF%2B6wy%2BYRDie7RMYScVdcO2Tuj%2BGVi5TRsLdK0Ulxsg0eiHDHxRAk7ul0DTiJ7GPiz9qQ%2B9zivSMChQpkAKjjWZef8nltSx4ZNtatj04O5yxetbNknPR8I5XSAG%2Fkn46JlIYQirM5J%2FruQ7YyQGmzte7gz4AHpouaaMaH2tuPvIFHmNUS51MktuScWg0zlekMbMDjcKCK0hvwSMZGtEt04242IPxdzVTtpmcb7ekQJD71CTYf2%2BGSjS9pa404Dfc3ft9wNLj3WgTq%2Ba8MMz8%2B3PiacKHM8WXJ5qi3NXgy1jOtedIc0SHxEglNLHAX87UB2QtZvxQj6LVOd6DV2K9GIP7YcQ5rlODBjU3OOnwQSrE%2FiEbC2tMfUuK3WIpG8GhAP4%2Fmm9PrQVpPQQmhh%2FftnmQRAvFJsRKJPr9%2ByHZ%2FFTTb54urvKcKnzAQq14OiqGAz8wjq6LzwY6pgF9zuBln6L9tT2PzN%2FFobKsjzC%2BdEGEcOCSEBznL3Q60%2FElUDXddCys5bAQH7bPjEZ9N4kTvTiuI9SwTDAXdi6mRZ%2FlVbKvHB6wUcqik1KZvjiNGv3Ph%2BnjyZXRUx4DMA6DmIB4In%2B8zvsCd38VhWKosUQ42c%2FHEsYWNzd0v8To%2BXE5TmNke7DUMDXVE%2FjoXPnpJHko8pkoAr48zsnTzhDH1lDxdicU&X-Amz-Signature=929d69a71b58cd69173deca1c528517cba0952aeeff87018f8562d06c52166cd&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

## **Kristjan 的**均线交易规则

> 适合在强势标的中突破追高

![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/c9678d23-e296-817b-849e-0003ceb9774c/52878c41-817a-46c0-a04d-c2e84650128e/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4663LQPQOHA%2F20260418%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260418T032657Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBkaCXVzLXdlc3QtMiJGMEQCID8e1ezKWr3RP%2FjXWq6UwkULHZrjDvt1OlHS%2Bv%2B9iEj1AiB6IokZf%2B3dmVmoZijYtSbiwYY9yx8yvDJl%2FqCt%2BWpQEiqIBAji%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDYzNzQyMzE4MzgwNSIMay%2FkHBYzSI37scLgKtwDyAh6qDFT5GznaX4sSr7B2C4BuuT23IxHkf3B8bNyLtcfKoGIzSxj%2BNaov9O6Oncthra6ahn6UQaeyHEQbUtuBzIY7oxat5ZfWftz1Yhb5flKgZ7Z7m3v9Zxnrq3xmhM7jRoEDDVJ5rV%2F44orwlFWcFk%2FEnGsGsd8OkRsjpwatQhL9ECFpYbmIy8zFF%2B6wy%2BYRDie7RMYScVdcO2Tuj%2BGVi5TRsLdK0Ulxsg0eiHDHxRAk7ul0DTiJ7GPiz9qQ%2B9zivSMChQpkAKjjWZef8nltSx4ZNtatj04O5yxetbNknPR8I5XSAG%2Fkn46JlIYQirM5J%2FruQ7YyQGmzte7gz4AHpouaaMaH2tuPvIFHmNUS51MktuScWg0zlekMbMDjcKCK0hvwSMZGtEt04242IPxdzVTtpmcb7ekQJD71CTYf2%2BGSjS9pa404Dfc3ft9wNLj3WgTq%2Ba8MMz8%2B3PiacKHM8WXJ5qi3NXgy1jOtedIc0SHxEglNLHAX87UB2QtZvxQj6LVOd6DV2K9GIP7YcQ5rlODBjU3OOnwQSrE%2FiEbC2tMfUuK3WIpG8GhAP4%2Fmm9PrQVpPQQmhh%2FftnmQRAvFJsRKJPr9%2ByHZ%2FFTTb54urvKcKnzAQq14OiqGAz8wjq6LzwY6pgF9zuBln6L9tT2PzN%2FFobKsjzC%2BdEGEcOCSEBznL3Q60%2FElUDXddCys5bAQH7bPjEZ9N4kTvTiuI9SwTDAXdi6mRZ%2FlVbKvHB6wUcqik1KZvjiNGv3Ph%2BnjyZXRUx4DMA6DmIB4In%2B8zvsCd38VhWKosUQ42c%2FHEsYWNzd0v8To%2BXE5TmNke7DUMDXVE%2FjoXPnpJHko8pkoAr48zsnTzhDH1lDxdicU&X-Amz-Signature=5ad8cf8173b2d6bf2c67165e7aa49890c99e4599b98101aff7f978d01f46fd5f&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/c9678d23-e296-817b-849e-0003ceb9774c/572c7bed-c57d-4183-b9f7-71ee21fd92d9/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4663LQPQOHA%2F20260418%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260418T032657Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBkaCXVzLXdlc3QtMiJGMEQCID8e1ezKWr3RP%2FjXWq6UwkULHZrjDvt1OlHS%2Bv%2B9iEj1AiB6IokZf%2B3dmVmoZijYtSbiwYY9yx8yvDJl%2FqCt%2BWpQEiqIBAji%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDYzNzQyMzE4MzgwNSIMay%2FkHBYzSI37scLgKtwDyAh6qDFT5GznaX4sSr7B2C4BuuT23IxHkf3B8bNyLtcfKoGIzSxj%2BNaov9O6Oncthra6ahn6UQaeyHEQbUtuBzIY7oxat5ZfWftz1Yhb5flKgZ7Z7m3v9Zxnrq3xmhM7jRoEDDVJ5rV%2F44orwlFWcFk%2FEnGsGsd8OkRsjpwatQhL9ECFpYbmIy8zFF%2B6wy%2BYRDie7RMYScVdcO2Tuj%2BGVi5TRsLdK0Ulxsg0eiHDHxRAk7ul0DTiJ7GPiz9qQ%2B9zivSMChQpkAKjjWZef8nltSx4ZNtatj04O5yxetbNknPR8I5XSAG%2Fkn46JlIYQirM5J%2FruQ7YyQGmzte7gz4AHpouaaMaH2tuPvIFHmNUS51MktuScWg0zlekMbMDjcKCK0hvwSMZGtEt04242IPxdzVTtpmcb7ekQJD71CTYf2%2BGSjS9pa404Dfc3ft9wNLj3WgTq%2Ba8MMz8%2B3PiacKHM8WXJ5qi3NXgy1jOtedIc0SHxEglNLHAX87UB2QtZvxQj6LVOd6DV2K9GIP7YcQ5rlODBjU3OOnwQSrE%2FiEbC2tMfUuK3WIpG8GhAP4%2Fmm9PrQVpPQQmhh%2FftnmQRAvFJsRKJPr9%2ByHZ%2FFTTb54urvKcKnzAQq14OiqGAz8wjq6LzwY6pgF9zuBln6L9tT2PzN%2FFobKsjzC%2BdEGEcOCSEBznL3Q60%2FElUDXddCys5bAQH7bPjEZ9N4kTvTiuI9SwTDAXdi6mRZ%2FlVbKvHB6wUcqik1KZvjiNGv3Ph%2BnjyZXRUx4DMA6DmIB4In%2B8zvsCd38VhWKosUQ42c%2FHEsYWNzd0v8To%2BXE5TmNke7DUMDXVE%2FjoXPnpJHko8pkoAr48zsnTzhDH1lDxdicU&X-Amz-Signature=5fa3d77ed8e20b95c5d4485c2976ba0eabef3f3cf1868109b43d03714e7b0965&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

1. 筛选 1-3 个月涨幅 30%-100% 的强势标的，且 EMA10/20/50 多头排列
1. 日线级别上出现 **2 周到 2 个月的盘整区间**。
1. 等待价格**突破盘整并以关键 K 线的收盘价入场（看4 小时或日线）**。
1. **止损在关键 K 线下方**；仓位初始可以按策略分配。
1. 若突破后行情爆发，约第 5 天可**先止盈 1/3 并将止损移至入场价**；其后**跌破 EMA10 止盈 1/3**，**跌破 EMA20 止盈剩余仓位**。
**回报：**这类小市值的埋伏若成功，波动幅度通常更大，回报潜力较高；

**风险**：假突破次数多、消息面风险、以及流动性不足都可能导致大损失。因此**关键点是用更长的横盘作为筛选条件并用量能作为突破有效性的确认**，以降低假突破概率。


视频课笔记：[Kristjan三均线突破交易系统实战规则拆解](https://www.notion.so/28178d23e296810d95b6ec404fdc77ea)  

## 币哥双均线规则

### 开仓

![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/c9678d23-e296-817b-849e-0003ceb9774c/90d2100d-76ac-4d06-bc97-ae060325560c/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4663LQPQOHA%2F20260418%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260418T032658Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBkaCXVzLXdlc3QtMiJGMEQCID8e1ezKWr3RP%2FjXWq6UwkULHZrjDvt1OlHS%2Bv%2B9iEj1AiB6IokZf%2B3dmVmoZijYtSbiwYY9yx8yvDJl%2FqCt%2BWpQEiqIBAji%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDYzNzQyMzE4MzgwNSIMay%2FkHBYzSI37scLgKtwDyAh6qDFT5GznaX4sSr7B2C4BuuT23IxHkf3B8bNyLtcfKoGIzSxj%2BNaov9O6Oncthra6ahn6UQaeyHEQbUtuBzIY7oxat5ZfWftz1Yhb5flKgZ7Z7m3v9Zxnrq3xmhM7jRoEDDVJ5rV%2F44orwlFWcFk%2FEnGsGsd8OkRsjpwatQhL9ECFpYbmIy8zFF%2B6wy%2BYRDie7RMYScVdcO2Tuj%2BGVi5TRsLdK0Ulxsg0eiHDHxRAk7ul0DTiJ7GPiz9qQ%2B9zivSMChQpkAKjjWZef8nltSx4ZNtatj04O5yxetbNknPR8I5XSAG%2Fkn46JlIYQirM5J%2FruQ7YyQGmzte7gz4AHpouaaMaH2tuPvIFHmNUS51MktuScWg0zlekMbMDjcKCK0hvwSMZGtEt04242IPxdzVTtpmcb7ekQJD71CTYf2%2BGSjS9pa404Dfc3ft9wNLj3WgTq%2Ba8MMz8%2B3PiacKHM8WXJ5qi3NXgy1jOtedIc0SHxEglNLHAX87UB2QtZvxQj6LVOd6DV2K9GIP7YcQ5rlODBjU3OOnwQSrE%2FiEbC2tMfUuK3WIpG8GhAP4%2Fmm9PrQVpPQQmhh%2FftnmQRAvFJsRKJPr9%2ByHZ%2FFTTb54urvKcKnzAQq14OiqGAz8wjq6LzwY6pgF9zuBln6L9tT2PzN%2FFobKsjzC%2BdEGEcOCSEBznL3Q60%2FElUDXddCys5bAQH7bPjEZ9N4kTvTiuI9SwTDAXdi6mRZ%2FlVbKvHB6wUcqik1KZvjiNGv3Ph%2BnjyZXRUx4DMA6DmIB4In%2B8zvsCd38VhWKosUQ42c%2FHEsYWNzd0v8To%2BXE5TmNke7DUMDXVE%2FjoXPnpJHko8pkoAr48zsnTzhDH1lDxdicU&X-Amz-Signature=63bc03ea5372a9cabc3d87cc516f015a75451e94e994e5ab250a38a343df257a&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/c9678d23-e296-817b-849e-0003ceb9774c/c5749cad-a851-4d1a-95f0-aebdb3ef2617/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4663LQPQOHA%2F20260418%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260418T032658Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBkaCXVzLXdlc3QtMiJGMEQCID8e1ezKWr3RP%2FjXWq6UwkULHZrjDvt1OlHS%2Bv%2B9iEj1AiB6IokZf%2B3dmVmoZijYtSbiwYY9yx8yvDJl%2FqCt%2BWpQEiqIBAji%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDYzNzQyMzE4MzgwNSIMay%2FkHBYzSI37scLgKtwDyAh6qDFT5GznaX4sSr7B2C4BuuT23IxHkf3B8bNyLtcfKoGIzSxj%2BNaov9O6Oncthra6ahn6UQaeyHEQbUtuBzIY7oxat5ZfWftz1Yhb5flKgZ7Z7m3v9Zxnrq3xmhM7jRoEDDVJ5rV%2F44orwlFWcFk%2FEnGsGsd8OkRsjpwatQhL9ECFpYbmIy8zFF%2B6wy%2BYRDie7RMYScVdcO2Tuj%2BGVi5TRsLdK0Ulxsg0eiHDHxRAk7ul0DTiJ7GPiz9qQ%2B9zivSMChQpkAKjjWZef8nltSx4ZNtatj04O5yxetbNknPR8I5XSAG%2Fkn46JlIYQirM5J%2FruQ7YyQGmzte7gz4AHpouaaMaH2tuPvIFHmNUS51MktuScWg0zlekMbMDjcKCK0hvwSMZGtEt04242IPxdzVTtpmcb7ekQJD71CTYf2%2BGSjS9pa404Dfc3ft9wNLj3WgTq%2Ba8MMz8%2B3PiacKHM8WXJ5qi3NXgy1jOtedIc0SHxEglNLHAX87UB2QtZvxQj6LVOd6DV2K9GIP7YcQ5rlODBjU3OOnwQSrE%2FiEbC2tMfUuK3WIpG8GhAP4%2Fmm9PrQVpPQQmhh%2FftnmQRAvFJsRKJPr9%2ByHZ%2FFTTb54urvKcKnzAQq14OiqGAz8wjq6LzwY6pgF9zuBln6L9tT2PzN%2FFobKsjzC%2BdEGEcOCSEBznL3Q60%2FElUDXddCys5bAQH7bPjEZ9N4kTvTiuI9SwTDAXdi6mRZ%2FlVbKvHB6wUcqik1KZvjiNGv3Ph%2BnjyZXRUx4DMA6DmIB4In%2B8zvsCd38VhWKosUQ42c%2FHEsYWNzd0v8To%2BXE5TmNke7DUMDXVE%2FjoXPnpJHko8pkoAr48zsnTzhDH1lDxdicU&X-Amz-Signature=9e9c74e2da1bbb99e38fdbb981bad887cc2bd5dd9e7a40ae7389bed09ec74ada&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/c9678d23-e296-817b-849e-0003ceb9774c/70e7c824-ac54-4ccf-9b24-852926edc086/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4663LQPQOHA%2F20260418%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260418T032658Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBkaCXVzLXdlc3QtMiJGMEQCID8e1ezKWr3RP%2FjXWq6UwkULHZrjDvt1OlHS%2Bv%2B9iEj1AiB6IokZf%2B3dmVmoZijYtSbiwYY9yx8yvDJl%2FqCt%2BWpQEiqIBAji%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDYzNzQyMzE4MzgwNSIMay%2FkHBYzSI37scLgKtwDyAh6qDFT5GznaX4sSr7B2C4BuuT23IxHkf3B8bNyLtcfKoGIzSxj%2BNaov9O6Oncthra6ahn6UQaeyHEQbUtuBzIY7oxat5ZfWftz1Yhb5flKgZ7Z7m3v9Zxnrq3xmhM7jRoEDDVJ5rV%2F44orwlFWcFk%2FEnGsGsd8OkRsjpwatQhL9ECFpYbmIy8zFF%2B6wy%2BYRDie7RMYScVdcO2Tuj%2BGVi5TRsLdK0Ulxsg0eiHDHxRAk7ul0DTiJ7GPiz9qQ%2B9zivSMChQpkAKjjWZef8nltSx4ZNtatj04O5yxetbNknPR8I5XSAG%2Fkn46JlIYQirM5J%2FruQ7YyQGmzte7gz4AHpouaaMaH2tuPvIFHmNUS51MktuScWg0zlekMbMDjcKCK0hvwSMZGtEt04242IPxdzVTtpmcb7ekQJD71CTYf2%2BGSjS9pa404Dfc3ft9wNLj3WgTq%2Ba8MMz8%2B3PiacKHM8WXJ5qi3NXgy1jOtedIc0SHxEglNLHAX87UB2QtZvxQj6LVOd6DV2K9GIP7YcQ5rlODBjU3OOnwQSrE%2FiEbC2tMfUuK3WIpG8GhAP4%2Fmm9PrQVpPQQmhh%2FftnmQRAvFJsRKJPr9%2ByHZ%2FFTTb54urvKcKnzAQq14OiqGAz8wjq6LzwY6pgF9zuBln6L9tT2PzN%2FFobKsjzC%2BdEGEcOCSEBznL3Q60%2FElUDXddCys5bAQH7bPjEZ9N4kTvTiuI9SwTDAXdi6mRZ%2FlVbKvHB6wUcqik1KZvjiNGv3Ph%2BnjyZXRUx4DMA6DmIB4In%2B8zvsCd38VhWKosUQ42c%2FHEsYWNzd0v8To%2BXE5TmNke7DUMDXVE%2FjoXPnpJHko8pkoAr48zsnTzhDH1lDxdicU&X-Amz-Signature=87e73d16a1281aa70543bb99e8073877b77cbee5252c7f4e46033d50551441e1&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

1. **TF 推荐 1h/4h/1d/1w，时间级别越小机会越多，但准确性也会下降。**
1. **均线密集开仓法与回踩20均线不破开仓法**
1. **均线密集后续不一定涨，为控制分险可等到回踩20均线不破再开仓**。
### 止盈

![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/c9678d23-e296-817b-849e-0003ceb9774c/c265cdf3-85b7-4ac5-9a41-1b8d5e086302/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4663LQPQOHA%2F20260418%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260418T032658Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBkaCXVzLXdlc3QtMiJGMEQCID8e1ezKWr3RP%2FjXWq6UwkULHZrjDvt1OlHS%2Bv%2B9iEj1AiB6IokZf%2B3dmVmoZijYtSbiwYY9yx8yvDJl%2FqCt%2BWpQEiqIBAji%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDYzNzQyMzE4MzgwNSIMay%2FkHBYzSI37scLgKtwDyAh6qDFT5GznaX4sSr7B2C4BuuT23IxHkf3B8bNyLtcfKoGIzSxj%2BNaov9O6Oncthra6ahn6UQaeyHEQbUtuBzIY7oxat5ZfWftz1Yhb5flKgZ7Z7m3v9Zxnrq3xmhM7jRoEDDVJ5rV%2F44orwlFWcFk%2FEnGsGsd8OkRsjpwatQhL9ECFpYbmIy8zFF%2B6wy%2BYRDie7RMYScVdcO2Tuj%2BGVi5TRsLdK0Ulxsg0eiHDHxRAk7ul0DTiJ7GPiz9qQ%2B9zivSMChQpkAKjjWZef8nltSx4ZNtatj04O5yxetbNknPR8I5XSAG%2Fkn46JlIYQirM5J%2FruQ7YyQGmzte7gz4AHpouaaMaH2tuPvIFHmNUS51MktuScWg0zlekMbMDjcKCK0hvwSMZGtEt04242IPxdzVTtpmcb7ekQJD71CTYf2%2BGSjS9pa404Dfc3ft9wNLj3WgTq%2Ba8MMz8%2B3PiacKHM8WXJ5qi3NXgy1jOtedIc0SHxEglNLHAX87UB2QtZvxQj6LVOd6DV2K9GIP7YcQ5rlODBjU3OOnwQSrE%2FiEbC2tMfUuK3WIpG8GhAP4%2Fmm9PrQVpPQQmhh%2FftnmQRAvFJsRKJPr9%2ByHZ%2FFTTb54urvKcKnzAQq14OiqGAz8wjq6LzwY6pgF9zuBln6L9tT2PzN%2FFobKsjzC%2BdEGEcOCSEBznL3Q60%2FElUDXddCys5bAQH7bPjEZ9N4kTvTiuI9SwTDAXdi6mRZ%2FlVbKvHB6wUcqik1KZvjiNGv3Ph%2BnjyZXRUx4DMA6DmIB4In%2B8zvsCd38VhWKosUQ42c%2FHEsYWNzd0v8To%2BXE5TmNke7DUMDXVE%2FjoXPnpJHko8pkoAr48zsnTzhDH1lDxdicU&X-Amz-Signature=5509a8234d4bc4937c8287281c7002ab9d055ea4e3433bd1082282a7174f173f&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

1. **在开仓同TF级别找历史的阻力区，作为止盈点，分批止盈。**1
视频课笔记：[币哥双均线交易系统](https://www.notion.so/25878d23e29681298e6ce54bbaf8eb81) [币哥双均线高赔率交易系统](https://www.notion.so/25a78d23e296819d90d9d7a7357df67a) 

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

## 概念

TradingView 指标名称：**Turtle Trade Channels Indicator TUTCI（海龟交易/唐奇安通道）**

![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/c9678d23-e296-817b-849e-0003ceb9774c/58ad1896-d633-4dd7-b1ee-55aed2be18e1/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466U262XPW2%2F20260418%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260418T032658Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBkaCXVzLXdlc3QtMiJIMEYCIQCdgFTkS3XleQaLEU8R%2B59KPx%2BSunC9x%2BlVTjc24zB9CgIhANdcGGKRkSP%2F%2BImvdxZhRCztbbogPgSX8jIb7L%2Bq07gCKogECOL%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNjM3NDIzMTgzODA1Igyc8e5UyYI%2BcBauh3Yq3AMgEYTf4593MgJjJnLLAkKsCmudfYDj3rUuvTv1kPGJ%2B1Gb6KNqPXdbWPi9pkmdHavLVNDjJU4tTjnZEncC4SQuu2RSU8%2BOBylSZTv9Omz6hcu1IuDHWJ%2FyEIJRGQyt1cKN%2BErpmFzKfll8KXYZRsjFZ0RY%2FgMz6JJin%2FPDPhUMq77P3NPJcQS%2Fd2e7NjFl3qmRhs5DwyFs%2FJA6enqn4FVRfLjD8T8APaKC6NcSYLz%2F2oQED2CKBzx4Sj06xHomRjrvdUs2GVYG5OY3xaY4kq%2FcfyRi5X%2FUA1M4IzsKmcUyQL5qLPlTKwW3jEDZErPiwM%2FcePouHjUlG9wjZ1QHl6fHmiyIZPBD96ghs5eSkoD9l%2FSxTPHUkFESsazoBM0yl6WLM6tAtui8fClY6FQlbfBMBAjRZhUPhhevXFwXoG5W314YZ6jrv19a4hCvSGSs4ttcCHr7ix9uTtfs%2B69pplQezhifBseVGXuk04%2BKsedXod7IM0dvJAdIJRkNhN9KBO3YxDfYHTdtGmSHt1Bxu1mwmK71%2FjkWrlLFImqPSEfFRYYBvW%2FCMYyspFmT6QHHV7uZItl49xDUqKySHumiEaFlxLgB8bjeASJl1qYduCvrjc6ArP%2Bdzp0QKG3hxzCdrIvPBjqkAf75KcR%2BzCojrlwXn3M5HGyVDcVrj%2BQMcpGOFfRioLp3Mc7YUOq3arhtkoiOBPGYRDlxhz2pYdR3Nw%2BPe6IVEofRLMs9muIQaXtEUDVJjuqvxwm5%2FHP9A69m9afXRXJCRK7gu055EbFa2tIJWkQv9iAc2YIO%2FPZDYSmADhbfLQ6l7n87c25v6Dr5pNavYnrSYAWDl1xnanIJis4LtxrWp5s7TUsq&X-Amz-Signature=f0b2770baa4e9d59efdae998fe0ac717a41ba0be0e18103d28da1b8c901b3ac9&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

1. 主要规则：**在20日突破时交易**，并**在价格突破10日高点或低点时获利了结。**
- 在20日向上突破时买入，当价格触及10日低点时平仓。
- 在20日向下突破时做空，当价格触及10日高点时平仓。
1. 在这个指标中
- **红线是交易线，指示趋势方向**
- 价格**K线在趋势线上方表示上涨趋势**。
- 价格**K线在趋势线下方表示下跌趋势**。
- **蓝色虚线**是退出线
1. 默认参数：20, 10 和 55, 20
- 当价格高点等于或高于过去20天的最高价时做多。
- 当价格低点等于或低于过去20天的最低价时做空。
- 当价格触及退出线时，平仓多头头寸。
- 当价格触及退出线时，平仓空头头寸。
- 推荐的初始止损是开仓价的ATR（平均真实波幅）* 2。
### **海龟法则**

要像海龟一样精确交易，你需要设置两个指标，分别代表**主系统（短期）和备用系统（长期）**。

1. 设置主系统 S1，**入场周期（EntryPeriod）= 20**，**退出周期（ExitPeriod）= 10**。
1. 设置备用系统 S2，**入场周期（EntryPeriod）= 55**，**退出周期（ExitPeriod）= 20**，使用不同的颜色。
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

视频课笔记：[海龟交易实验：交易能力可后天培养的实证](https://www.notion.so/27f78d23e29681eeab50c2164546efdf) 

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

**Liquidity Grab Zones **

## 概念

TradingView 指标名称：Price Action Toolkit (PAT) 

> [https://cn.tradingview.com/script/w0dsFfR5-PAT-Screener-Flux-Charts/](https://cn.tradingview.com/script/w0dsFfR5-PAT-Screener-Flux-Charts/)

![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/c9678d23-e296-817b-849e-0003ceb9774c/bd85cbf8-2524-4323-8236-8809462a66cc/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466TJPVKTZC%2F20260418%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260418T032706Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBkaCXVzLXdlc3QtMiJHMEUCIDs8TvyNNmb9KOVsxQkQz8yoMZ2lQzZG8jIRNBYYCiaeAiEApRNyqP5U1ZwiX7sR8E40aJMPSyR1InjsIL%2BrS9N8ibYqiAQI4v%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDO2r0SwMuHfW9lxHpSrcA4Olm%2BVMPNmObvgtpClVh8xx%2FzBGgdHnGVkSuMyH3GctgTnxPHPtT1U9a6fcMZbwNMdW2O%2FpNmbXZHZN%2FDm3oDjU7W03GiEBmEw1H2ktmt3fZNB51ZKRmkpsVjJxpw0Sly8iluhhEhCVCg8Ttz6Es0P3y1awmYyF5GZH22h4sk%2Fc4Xe9hv72tkCbFT2td7cjisoLVlwNaJIroaDmddg1TCkaAq5udp1vfSpyEy3078oDbw5df62uIbvtwvWkYWmpOzFKjmlnyK0jUHNJm4dZoTXTn28PzUFJ9nw1kNeFisfSXaoBdZ08%2BFELTRn8WcEO8C6EuhyQYomVwGrMu1MfSRLDoicfouJTycF%2BtTd69ZKFO2iln6OqOxaNQ58q7uF2RU7JKeUZMDJDMXJHDGabR8fPljDSGsTDzjZDxSVXWAfDjziipEWglTNjLL%2BY1gslbwxsAcu6%2FSu1S75Qa050X8f5FTyZJe0B0QBu2L7xxUtxGY5%2FJuLjtimsjUIENcmqzJ%2B7O6g4ZRNMtDUYMcFxhF2i9cBu9QI%2BYkizZSZny2ExcsHR4jIds%2BlI5Xw7Lis5A%2BdDR%2FCPLMJo9d63zTnVQYkQB9EtnmuZ3c5BJ%2Bii%2B833%2BTia9d4gl6yhSUknMIGsi88GOqUBzgpD3nPTbzbiYae5jPUZH1gAzi6ri%2Fvg4cax%2ByM1fCAow5CrF6Zyul%2FqqUV%2F05kmxSO4COBAQmsSm%2F%2FSphcCYL6TN1K2BrU09D4i7RKh7R8fqgBkESLoKqA8g%2FHrkGyZmOuvzHSZO9tabIBQBnekCapBTElBZU2FSO%2FAXt9HhO0sgkPtJSRY12WI3sD3hEa9qT1M8BdSuhZmQbLtQY1MbRQKpsYK&X-Amz-Signature=16126fb12dd7f80625d987d0ab6a5f468ef6c79f7ff76e473bd3d41c03cc26ff&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

价格行为学主要特征：

1. Finds Latest Across 8 Tickers
1. Order Blocks
1. Breaker Blocks
1. Fair Value Gaps (FVG)
1. Inversion FVGs
1. Market Structures (BOS, CHoCH, CHoCH+)
1. Liquidity Zones
1. Liquidity Grabs
1. Premium / Discount Zones
显示额外附加信息：

1. Strength
1. Retests
1. (Bullish & Bearish) Volume
1. Consumption
![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/c9678d23-e296-817b-849e-0003ceb9774c/1201000c-b10c-4cc1-bd05-ea724e7c5db8/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4664AI7FBBG%2F20260418%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260418T032707Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBkaCXVzLXdlc3QtMiJGMEQCIDV18LA5%2BQ6r5g2K0NaZZRGjSrBni3TMXv96ZpTZinl8AiArA38xUTyR80WowYoyKkShs4CqSRLOGt6UVd2x56ISlCqIBAji%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDYzNzQyMzE4MzgwNSIMnQZW%2BpArA4zEo3YjKtwDJO4XCEKbjHQwYDjuQKb%2FFbFuLOfTxSWbBsfDzUlRIblvRC10xRwY0A%2F7ergLRtxk3JBoir2lLrAX2yPiDu8OratL%2B6CXC3513a186Dqc6OANDQWrYJGdKofeWfAzuYRyDsqrD7%2FKeUtIfakTBjCpd3mDLpA5khizluxaGkwR%2FynZnnow5VNWFRFc87ArzTddOT1ctJ4pUVbIFFU9siNZUkbghptPvZ5tENLPugvSZMl31Iy1zdNVCrtmt43T2QRuupM8Gt83R6vnli6A1lvmtdx6KxItgJvhV6nh2w9%2FD6pzg%2BbnzHLlWbKblUOwNkmGh7MryEd6rGCxuu8xSz%2FQ7ncFfLC4kcMkRHjpUNj8XWhfSQzz6eabI13fL1xqxj8K1QTGbdjJHouvsKTRLRi5y3rVfxUzlO5ffBIZUY692KEbEiWrsYiEI1FCOe7sygQ%2FJjY6q5l69I1xEDGu2S7FIYMzfQdxp%2BGlwOfiHyU3y555o%2FYj8iZJ%2FRbkWFJpZ%2FHKOt1FoHzcZya0iD4gcG0GRioVyrrUZIk9e9NH8rFcSpvDd1LFfpAe%2FMtU6PEYJBOzEd9HW%2BE7I8OLr7nG6Qgd%2BFG7yBnKcS8wnNEO0gvG8fw%2BXAgE49gm%2Bb9sz1Qwx62LzwY6pgG4S8J8tsOMIwiQhk8pjWtKkiyESa%2ButQ5Vh4pzHEYZoys7ijFcktD1%2BYNx13%2Fat%2BlLLpueXTzjehRIfE7Q8%2FLYpFGDoT9d4HKjuAHslKi3SEadGObovK9lttDjZ9HELoiR0nEJ5TZ7iU6y2wGvdnFuTRPpuO0QLzxIi6FPFzCeZr1oLYPurdCwR%2BkhAfjjiy9J5MkUW1HprNYLUINW9kVjOcvIE0Fh&X-Amz-Signature=773119e7c7ad178a001f8370f5fceed98e9cf8f83aa4932c99868506edc456c7&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

Ref

[枢轴点与布林带结合的稳定盈利交易策略](https://www.notion.so/28478d23e296814991c0fd6a6548a368) 

## 概念

> TradingView 指标名称：Supply and Demand (MTF) | Flux Charts

- **供应区**是过去价格快速下跌、卖方力量显著的区域，当价格再次回到这里时，预计会遇到阻力，是**潜在的卖出（或看跌）机会**。
- **需求区**是过去价格快速上涨、买方力量显著的区域，当价格再次回到这里时，预计会遇到支撑，是**潜在的买入（或看涨）机会**。
![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/c9678d23-e296-817b-849e-0003ceb9774c/f9b3ff30-0cb8-4d58-a1bb-76a031a69326/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4666BA272UM%2F20260418%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260418T032708Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBkaCXVzLXdlc3QtMiJGMEQCIHECAXdEkQUAy0KUkWIdIlwfZbvXzPOSYE8K8gbVKELgAiA2t6aFUZiFjvlOeSS4mde09R19z54WW7yyOjyDT8VpoCqIBAji%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDYzNzQyMzE4MzgwNSIMeUk3IaF1kK1uaeqQKtwDbgiRTZoatwulgx2EqfJC%2FsFlDt327RR8Q5uCK%2FVOG1P54KMruwkhRz6R5FyPprFP8yD%2FYPFDGjsUmmLZLAp2JBSoi0w55Yxsi6hUCb6bOKh4CHz4wexdR4iSy7e01NG1vhm6OQuLrMVSHHuvF73ExlP5FsTABrCChj8BjXpyR4gXsI0x9aWD0KxCQPzxABY5xhv9mhiFfj4de7%2BZZj3zv0D8I1i%2F61Tqk4g%2BlQLuIuNFJdleYjdVvKSeCjmomSNB4dPHinsKLITMnAkOQLOEnsxW0z01w44wVoO0ZMBX1NFOTsqWDHFwhRTOYu40KHf9%2BQPPlSCXK3E5KNSGVPM0uxZUXc9L48HpHX7Jw6FjUYCZ5aTIs9KvKhLJPmPdTsnm6MKoeLjv9%2FkiatrhgF%2B6F%2F0%2BFqC6jDjz5kwhnV3S5%2Bofz53mgQ%2BsR6uBGWZ9GbmcwdwWz2SNpKfzcuMCjJgEXlMimfV6sC5t2CEbrxCF8wESRms4gutjqgz0BzcyYeGMa%2B0yoVstai%2B356VWAsK3GRAI7tlx1rs6OuDRcNEqEw1cf9YeZ5XP3GBhGVluUsGPay3kO3gXk%2BPTnLlNH6mKvz02cBPzkcjvly3bWeWWrQXLkyi3O0X%2B9UqKBgwwlK%2BLzwY6pgHqOB5nYyYPyCbquWMKj4NPtJA5x54fwY9g9KOdgI6eDEJj7XNpl5C9R7OcScSqoUBpDX2a%2BSqCWsfHV6rFmEIl89DA5L7jiIQQcdJgxTzqUZWu2xjkITi6s2KVbPUQSOhi%2B8aLLF82%2FDig%2FH%2FVSOWYlTXbvakE2yU5PcXpBt3mEwOhl8UeyWZ9pUUbJ16LrZFki6eF9ELF61jDfwH4G5rykoKbwPYR&X-Amz-Signature=9676b8557e4fb6e60909429e9379265144b39068813c7d85b94a6c940e6bd961&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/c9678d23-e296-817b-849e-0003ceb9774c/adfcdd74-a4a7-4111-8b8e-18f2e527ce1a/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4666BA272UM%2F20260418%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260418T032708Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBkaCXVzLXdlc3QtMiJGMEQCIHECAXdEkQUAy0KUkWIdIlwfZbvXzPOSYE8K8gbVKELgAiA2t6aFUZiFjvlOeSS4mde09R19z54WW7yyOjyDT8VpoCqIBAji%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDYzNzQyMzE4MzgwNSIMeUk3IaF1kK1uaeqQKtwDbgiRTZoatwulgx2EqfJC%2FsFlDt327RR8Q5uCK%2FVOG1P54KMruwkhRz6R5FyPprFP8yD%2FYPFDGjsUmmLZLAp2JBSoi0w55Yxsi6hUCb6bOKh4CHz4wexdR4iSy7e01NG1vhm6OQuLrMVSHHuvF73ExlP5FsTABrCChj8BjXpyR4gXsI0x9aWD0KxCQPzxABY5xhv9mhiFfj4de7%2BZZj3zv0D8I1i%2F61Tqk4g%2BlQLuIuNFJdleYjdVvKSeCjmomSNB4dPHinsKLITMnAkOQLOEnsxW0z01w44wVoO0ZMBX1NFOTsqWDHFwhRTOYu40KHf9%2BQPPlSCXK3E5KNSGVPM0uxZUXc9L48HpHX7Jw6FjUYCZ5aTIs9KvKhLJPmPdTsnm6MKoeLjv9%2FkiatrhgF%2B6F%2F0%2BFqC6jDjz5kwhnV3S5%2Bofz53mgQ%2BsR6uBGWZ9GbmcwdwWz2SNpKfzcuMCjJgEXlMimfV6sC5t2CEbrxCF8wESRms4gutjqgz0BzcyYeGMa%2B0yoVstai%2B356VWAsK3GRAI7tlx1rs6OuDRcNEqEw1cf9YeZ5XP3GBhGVluUsGPay3kO3gXk%2BPTnLlNH6mKvz02cBPzkcjvly3bWeWWrQXLkyi3O0X%2B9UqKBgwwlK%2BLzwY6pgHqOB5nYyYPyCbquWMKj4NPtJA5x54fwY9g9KOdgI6eDEJj7XNpl5C9R7OcScSqoUBpDX2a%2BSqCWsfHV6rFmEIl89DA5L7jiIQQcdJgxTzqUZWu2xjkITi6s2KVbPUQSOhi%2B8aLLF82%2FDig%2FH%2FVSOWYlTXbvakE2yU5PcXpBt3mEwOhl8UeyWZ9pUUbJ16LrZFki6eF9ELF61jDfwH4G5rykoKbwPYR&X-Amz-Signature=a3e04eb4156f3c22477506a6a141559cf9d83bee3eb2b74e682102b11694c148&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

1. **供应区 (Supply Zones) ****- 通常是****红色或熊市颜色框**
- **识别方式**: **当价格在短时间内出现多根强劲的看跌K线（****实体大小大于平均水平****）**（由变量 momentumSpan 和 momentumCount 定义），**这表明有大量卖家在某一价格区间入场**。指标会根据这些K线之前的某个高点和低点来定义供应区。
- **代表意义**: **供应区代表了市场中存在大量潜在的卖盘**。**当价格再次回到这个区域时，预计会遇到卖家的抛售压力，从而可能导致价格下跌**。这通常被视为潜在的**做空机会**或**现有多头头寸的平仓点**。
1. **需求区 (Demand Zones)**** - 通常是****绿色或牛市颜色框**
- **识别方式**: **与供应区相反，当价格在短时间内出现多根强劲的看涨K线，表明有大量买家在某一价格区间入场**。指标会根据这些K线之前的某个高点和低点来定义需求区。
- **代表意义**: 需求区代表了市场中**存在大量潜在的买盘**。**当价格再次回到这个区域时，预计会遇到买家的买入支撑，从而可能导致价格上涨**。这通常被视为潜在的**做多机会**或**现有空头头寸的平仓点**。
1. **区域失效 (Zone Invalidation)**
- **代表意义**: **当价格完全穿透一个供应区或需求区时，意味着该区域的买卖失衡已经被消耗殆尽，**或者说**买卖双方的力量已经逆转**。该区域就不再有效。
- **视觉呈现**: 默认情况下，**失效的区域仍然会显示，但其颜色可能会稍微透明化**。区域的方框会从其起始时间延伸到breakTime（突破时间），而不是延伸到当前K线。
1. **合并区域 (Combined Zones)**
- **代表意义**: 如果**多个供应区（或需求区）在时间和价格上相互重叠，指标会尝试将它们合并成一个更大的、更强的区域**。这表明**在更广的价格范围内，存在持续的买盘或卖盘压力**。
- **视觉呈现**: 合并后的区域通常会以稍微不同的颜色透明度显示，并且其文本标签可能会显示合并的多个时间周期（**例如“1 Hour & 30 Min Supply”**），表示这个区域是**多时间周期共振形成的**。
1. **重新测试标签 (Retest Labels - "R")**
- **识别方式**: **当价格回撤到未失效的供应区或需求区边缘附近，但并未完全穿透它时，就会标记一个重新测试。**
- **代表意义**: **重新测试表明市场正在再次确认这个区域的有效性**。**在需求区重新测试并反弹，可以看作是买家再次入场的信号；在供应区重新测试并下跌，可以看作是卖家再次入场的信号**。这通常被视为**高概率的交易入场点**。
- **视觉呈现**: 在发生重新测试的K线处，会绘制一个带有“R”字母的标签。需求区重新测试通常是向上的绿色标签，供应区重新测试是向下的红色标签。
1. **突破标签 (Break Labels - "B")**
- **识别方式**: **当价格有效穿透一个供应区或需求区，导致该区域失效时，就会标记一个突破**。
- **代表意义**: **突破意味着市场力量的转换**。**突破需求区可能预示着下跌趋势的开始或延续；突破供应区可能预示着上涨趋势的开始或延续**。这可以被视为**趋势改变**或**趋势延续的信号**。
- **视觉呈现**: 在发生突破的K线处，会绘制一个带有“B”字母的标签，通常是蓝色。向上突破供应区是向上的蓝色标签，向下突破需求区是向下的蓝色标签。
1. **多时间周期 (Multi-Timeframe, MTF)**
- **代表意义**: 指标能够同时显示不同时间周期（例如15分钟、30分钟、1小时）的供应和需求区域。
- **重要性**: **更高时间周期的区域通常比低时间周期的区域更具影响力**。**当低时间周期的价格行为与高时间周期的区域重合时，信号的强度和可靠性会大大增加**。例如，在一个15分钟图上看到价格进入一个1小时的需求区，这通常比仅仅在一个15分钟的需求区内更具说服力。
## **典型的交易策略应用**

1. **在需求区买入，在供应区卖出（****反转策略****）**:
- 当价格进入一个**需求区**并显示出拒绝下跌的K线形态（例如，锤子线、吞噬形态等），交易者可能会考虑**做多**，止损设在需求区下方，目标是下一个供应区或结构高点。
- 当价格进入一个**供应区**并显示出拒绝上涨的K线形态（例如，射击之星、看跌吞噬等），交易者可能会考虑**做空**，止损设在供应区上方，目标是下一个需求区或结构低点。
- **“R” 标签（重新测试）**在这里是**关键的入场信号，它确认了区域的有效性**。
1. **交易区域突破（****趋势延续或趋势反转策略****）**:
- 当价格**突破并收盘在供应区之上**时，这可能预示着**上涨趋势的延续或熊市结构的转变，交易者可能会考虑追多。**
- 当价格**突破并收盘在需求区之下**时，这可能预示着**下跌趋势的延续或牛市结构的转变，交易者可能会考虑追空。**
- **“B”标签（突破）**在这里提供了突破的确认。
1. **结合多时间周期分析**:
- 交易者会寻找**高时间周期**（例如日线、4小时）和**低时间周期**（例如15分钟、1小时）区域的**共振**。例如，如果15分钟图上的价格进入了一个1小时和4小时图上的共同需求区域，这会大大增加该需求区域的可靠性，提供更强的买入信号。
- **多时间周期区域的结合（通过合并区域功能显示）更能反映市场深层次的供需平衡。**
## 代码

```javascript
// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © fluxchart

//@version=5
const bool DEBUG = false
const int maxBoxesCount = 500
const float overlapThresholdPercentage = 0.0
int maxDistanceToLastBar = 1250 // Affects Running Time
const int maxSDZones = 30
const int minZoneSize = 10
const int RETEST_COOLDOWN   = 5
const int minDistanceBetweenZones = 5
const float maxZoneSizeATR = 1.5

indicator(title = 'Supply & Demand (MTF) | Flux Charts', shorttitle = "Supply and Demand (MTF) | Flux Charts", overlay = true, max_boxes_count = maxBoxesCount, max_labels_count = maxBoxesCount, max_lines_count = maxBoxesCount, max_bars_back = 2000, dynamic_requests = true)

maxDistanceString   = input.string("Normal", "Max Distance To Last Bar", options = ["High", "Normal", "Low"],  group = "General Configuration", display = display.none)
sdEndMethod = input.string("Close", "Zone Invalidation", options = ["Wick", "Close"],  group = "General Configuration", display = display.none)
combineSDs = DEBUG ? input.bool(true, "Combine Zones", group = "General Configuration", display = display.none) : true
momentumBodyMult = DEBUG ? input.float(0.5, "Momentum Body Mult", step = 0.1, group = "General Configuration") : 0.5
momentumCount = DEBUG ? input.int(4,"Momentum Count", group = "General Configuration") : 4
momentumSpan = DEBUG ? input.int(4, "Momentum Span", group = "General Configuration") : 4
//zoneCount = input.string("High", 'Zone Count', options = ["High", "Medium", "Low", "One"], tooltip = "Number of S&D Zones to be rendered. Higher options will result in older S&Ds shown.",  group = "General Configuration", display = display.none)
zoneCount = "High"
retestsEnabled  = input.bool(true, "Retests", inline = "rb", group = "General Configuration", display = display.none)
breaksEnabled   = input.bool(false, "Breaks", inline = "rb", group = "General Configuration", display = display.none)
showInvalidated = input.bool(true, "Show Historic Zones", group = "General Configuration", display = display.none)
bullSDZoneColor = input(#08998180, 'Demand', inline = 'sdColor', group = 'General Configuration', display = display.none)
bearSDZoneColor = input(#f2364680, 'Supply', inline = 'sdColor', group = 'General Configuration', display = display.none)

demandZones = zoneCount == "One" ? 1 : zoneCount == "Low" ? 3 : zoneCount == "Medium" ? 5 : 30
supplyZones = zoneCount == "One" ? 1 : zoneCount == "Low" ? 3 : zoneCount == "Medium" ? 5 : 30

timeframe1Enabled = input.bool(true, title = "", group = "Timeframes", inline = "timeframe1", display = display.none)
timeframe1 = input.timeframe("", title = "", group = "Timeframes", inline = "timeframe1", display = display.none)
timeframe2Enabled = input.bool(false, title = "", group = "Timeframes", inline = "timeframe2", display = display.none)
timeframe2 = input.timeframe("15", title = "", group = "Timeframes", inline = "timeframe2", display = display.none)
timeframe3Enabled = input.bool(false, title = "", group = "Timeframes", inline = "timeframe3", display = display.none)
timeframe3 = input.timeframe("30", title = "", group = "Timeframes", inline = "timeframe3", display = display.none)

textColor = input.color(#ffffffcc, "Text Color", group = "Style")
labelsAtSameLevel   = DEBUG ? input.bool(true, "[DBG] Place Labels At Same Level", group = "Style") : true
labelsAtSameLevelBreak = false

atr = ta.atr(20)
averageBodySize = ta.sma(math.abs(close - open), 20)

maxDistanceToLastBar := maxDistanceString == "Low" ? 150 : maxDistanceString == "Normal" ? 500 : 1250

type sdZoneInfo
    float top
    float bottom
    string sdType
    int startTime
    int breakTime
    int guid
    string timeframeStr
    bool disabled = false
    string combinedTimeframesStr = na
    bool combined = false

type sdZone
    sdZoneInfo info
    bool isRendered = false

    box sdBox = na

    line sdBoxLineTop = na
    line sdBoxLineMiddle = na
    line sdBoxLineBottom = na
    //
    box sdBoxText = na

type retestLabelContainer
    int guid
    array<label> labels

createSDZone (sdZoneInfo sdZoneInfoF) =>
    sdZone newSDZone = sdZone.new(sdZoneInfoF)
    newSDZone

safeDeleteSDZone (sdZone sdZoneF) =>
    sdZoneF.isRendered := false

    box.delete(sdZoneF.sdBox)
    box.delete(sdZoneF.sdBoxText)

    line.delete(sdZoneF.sdBoxLineTop)
    line.delete(sdZoneF.sdBoxLineMiddle)
    line.delete(sdZoneF.sdBoxLineBottom)

type timeframeInfo
    int index = na
    string timeframeStr = na
    bool isEnabled = false

    sdZoneInfo[] demandZonesList = na
    sdZoneInfo[] supplyZonesList = na

newTimeframeInfo (index, timeframeStr, isEnabled) =>
    newTFInfo = timeframeInfo.new()
    newTFInfo.index := index
    newTFInfo.isEnabled := isEnabled
    newTFInfo.timeframeStr := timeframeStr

    newTFInfo

// ____ TYPES END ____

var timeframeInfo[] timeframeInfos = array.from(newTimeframeInfo(1, timeframe1, timeframe1Enabled), newTimeframeInfo(2, timeframe2, timeframe2Enabled), newTimeframeInfo(3, timeframe3, timeframe3Enabled))
var demandZonesList = array.new<sdZoneInfo>(0)
var supplyZonesList = array.new<sdZoneInfo>(0)
var breakLabels = map.new<int, label>()
var retestLabels = map.new<int, retestLabelContainer>()

var int oldestBarTime = na
if bar_index == last_bar_index - maxDistanceToLastBar
    oldestBarTime := time

var allSDZonesList = array.new<sdZone>(0)

moveLine(_line, _x, _y, _x2) =>
    line.set_xy1(_line, _x,  _y)
    line.set_xy2(_line, _x2, _y)

moveBox (_box, _topLeftX, _topLeftY, _bottomRightX, _bottomRightY) =>
    box.set_lefttop(_box, _topLeftX, _topLeftY)
    box.set_rightbottom(_box, _bottomRightX, _bottomRightY)

isTimeframeLower (timeframe1F, timeframe2F) =>
    timeframe.in_seconds(timeframe1F) < timeframe.in_seconds(timeframe2F)

getMinTimeframe (timeframe1F, timeframe2F) =>
    if isTimeframeLower(timeframe1F, timeframe2F)
        timeframe1F
    else
        timeframe2F

getMaxTimeframe (timeframe1F, timeframe2F) =>
    if isTimeframeLower(timeframe1F, timeframe2F)
        timeframe2F
    else
        timeframe1F

formatTimeframeString (formatTimeframe) =>
    timeframeF = formatTimeframe == "" ? timeframe.period : formatTimeframe
    
    if str.contains(timeframeF, "D") or str.contains(timeframeF, "W") or str.contains(timeframeF, "S") or str.contains(timeframeF, "M")
        timeframeF
    else
        seconds = timeframe.in_seconds(timeframeF)
        if seconds >= 3600
            hourCount = int(seconds / 3600)
            str.tostring(hourCount) + " Hour" + (hourCount > 1 ? "s" : "")
        else
            timeframeF + " Min"

colorWithTransparency (colorF, transparencyX) =>
    color.new(colorF, color.t(colorF) * transparencyX)

createSDBox (boxColor, transparencyX = 1.0, xlocType = xloc.bar_time) =>
    box.new(na, na, na, na, xloc = xlocType, extend = extend.none, bgcolor = colorWithTransparency(boxColor, transparencyX), text_color = textColor, text_halign = text.align_right, text_valign = text.align_bottom, text_size = size.small, border_color = boxColor)

renderSDZone (sdZone sd) =>
    sdZoneInfo info = sd.info
    
    sd.isRendered := true
    
    sdColor = sd.info.sdType == "Demand" ? bullSDZoneColor : bearSDZoneColor

    int zoneSize = na
    if na(info.breakTime)
        zoneSize := (time + 1) - info.startTime
    else
        zoneSize := (info.breakTime - info.startTime)

    render = true
    if zoneSize < timeframe.in_seconds(info.timeframeStr) * minZoneSize * 1000
        render := false
    if info.startTime < nz(oldestBarTime, time)
        render := false


    if render and (showInvalidated or (na(sd.info.breakTime)))
        sd.sdBox := createSDBox(sdColor, 1.5)
        if sd.info.combined
            sd.sdBox.set_bgcolor(colorWithTransparency(sdColor, 1.1))

        startX = info.startTime
        maxEndX = info.startTime + zoneSize / 2

        float middlePoint = (info.top + info.bottom) / 2
        moveBox(sd.sdBox, info.startTime, info.top, info.startTime + zoneSize, info.bottom)
        
        sd.sdBoxLineMiddle := line.new(info.startTime, middlePoint, info.startTime + zoneSize, middlePoint, xloc = xloc.bar_time, color = textColor, style = line.style_dashed)

        sd.sdBoxText := createSDBox(color.new(color.white, 100))
        moveBox(sd.sdBoxText, maxEndX, middlePoint, info.startTime + zoneSize, info.bottom)
        SDText = (na(sd.info.combinedTimeframesStr) ? formatTimeframeString(sd.info.timeframeStr) : sd.info.combinedTimeframesStr) + " " + sd.info.sdType
        //box.set_text(sd.sdBoxText, SDText)
        boxText = na(sd.info.combinedTimeframesStr) ? formatTimeframeString(sd.info.timeframeStr) : sd.info.combinedTimeframesStr
        if DEBUG
            boxText += " | " + str.tostring(sd.info.guid)
        box.set_text(sd.sdBoxText, boxText)
        

areaOfSD (sdZoneInfo SDInfoF) =>
    float XA1 = SDInfoF.startTime
    float XA2 = na(SDInfoF.breakTime) ? time + 1 : SDInfoF.breakTime
    float YA1 = SDInfoF.top
    float YA2 = SDInfoF.bottom
    float edge1 = math.sqrt((XA2 - XA1) * (XA2 - XA1) + (YA2 - YA2) * (YA2 - YA2))
    float edge2 = math.sqrt((XA2 - XA2) * (XA2 - XA2) + (YA2 - YA1) * (YA2 - YA1))
    float totalArea = edge1 * edge2
    totalArea

doSDsTouch (sdZoneInfo SDInfo1, sdZoneInfo SDInfo2) =>
    float XA1 = SDInfo1.startTime
    float XA2 = na(SDInfo1.breakTime) ? (time + 1) : SDInfo1.breakTime
    float YA1 = SDInfo1.top + atr / 100
    float YA2 = SDInfo1.bottom - atr / 100

    float XB1 = SDInfo2.startTime
    float XB2 = na(SDInfo2.breakTime) ? (time + 1) : SDInfo2.breakTime
    float YB1 = SDInfo2.top + atr / 100
    float YB2 = SDInfo2.bottom - atr / 100
    float intersectionArea = math.max(0, math.min(XA2, XB2) - math.max(XA1, XB1)) * math.max(0, math.min(YA1, YB1) - math.max(YA2, YB2))
    float unionArea = areaOfSD(SDInfo1) + areaOfSD(SDInfo2) - intersectionArea
    
    float overlapPercentage = (intersectionArea / unionArea) * 100.0

    if overlapPercentage > overlapThresholdPercentage
        true
    else
        false

isSDValid (sdZoneInfo SDInfo) =>
    valid = true
    if SDInfo.disabled
        valid := false
    valid

clampSDZone (sdZoneInfo sdZoneF) =>
    sdZoneSize = sdZoneF.top - sdZoneF.bottom
    if sdZoneSize > atr * maxZoneSizeATR
        diff = sdZoneSize - (atr * maxZoneSizeATR)
        sdZoneF.top -= diff / 2
        sdZoneF.bottom += diff / 2

combineSDsFunc () =>
    if allSDZonesList.size() > 0
        lastCombinations = 999
        while lastCombinations > 0
            lastCombinations := 0
            for i = 0 to allSDZonesList.size() - 1
                curSD1 = allSDZonesList.get(i)
                for j = 0 to allSDZonesList.size() - 1
                    curSD2 = allSDZonesList.get(j)
                    if i == j
                        continue
                    if not isSDValid(curSD1.info) or not isSDValid(curSD2.info)
                        continue
                    if curSD1.info.sdType != curSD2.info.sdType
                        continue
                    if doSDsTouch(curSD1.info, curSD2.info)
                        curSD1.info.disabled := true
                        curSD2.info.disabled := true

                        sdZone newSD = createSDZone(sdZoneInfo.new(math.max(curSD1.info.top, curSD2.info.top), math.min(curSD1.info.bottom, curSD2.info.bottom), curSD1.info.sdType))
                        newSD.info.startTime := math.min(curSD1.info.startTime, curSD2.info.startTime)
                        newSD.info.breakTime := math.max(nz(curSD1.info.breakTime), nz(curSD2.info.breakTime))
                        newSD.info.breakTime := newSD.info.breakTime == 0 ? na : newSD.info.breakTime
                        newSD.info.guid := newSD.info.startTime
                        newSD.info.timeframeStr := curSD1.info.timeframeStr
                        clampSDZone(newSD.info)
                        
                        newSD.info.combined := true
                        if timeframe.in_seconds(curSD1.info.timeframeStr) != timeframe.in_seconds(curSD2.info.timeframeStr)
                            newSD.info.combinedTimeframesStr := (na(curSD1.info.combinedTimeframesStr) ? formatTimeframeString(curSD1.info.timeframeStr) : curSD1.info.combinedTimeframesStr) + " & " + (na(curSD2.info.combinedTimeframesStr) ? formatTimeframeString(curSD2.info.timeframeStr) : curSD2.info.combinedTimeframesStr)
                        allSDZonesList.unshift(newSD)
                        lastCombinations += 1


reqSeq (timeframeStr) =>
    if timeframe.in_seconds(timeframeStr) == timeframe.in_seconds()
        [demandZonesList, supplyZonesList]
    else
        [demandZonesListF, supplyZonesListF] = request.security(syminfo.tickerid, timeframeStr, [demandZonesList, supplyZonesList])
        [demandZonesListF, supplyZonesListF]

getTFData (timeframeInfo timeframeInfoF, timeframeStr) =>
    if timeframeInfoF.isEnabled
        [demandZonesListF, supplyZonesListF] = reqSeq(timeframeStr)
        [demandZonesListF, supplyZonesListF]
    else
        [na, na]

handleTimeframeInfo (timeframeInfo timeframeInfoF, demandZonesListF, supplyZonesListF) =>
    if timeframeInfoF.isEnabled
        timeframeInfoF.demandZonesList := demandZonesListF
        timeframeInfoF.supplyZonesList := supplyZonesListF

handleSDZonesFinal () =>
    if DEBUG
        log.info("Demand Count " + str.tostring(demandZonesList.size()))
        log.info("Supply Count " + str.tostring(supplyZonesList.size()))
        log.info("All " + str.tostring(allSDZonesList.size()))
        log.info("Max " + str.tostring(demandZones))

    if allSDZonesList.size() > 0
        for i = 0 to allSDZonesList.size() - 1
            safeDeleteSDZone(allSDZonesList.get(i))
    allSDZonesList.clear()    

    for i = 0 to timeframeInfos.size() - 1
        curTimeframe = timeframeInfos.get(i)
        if not curTimeframe.isEnabled
            continue
        if curTimeframe.demandZonesList.size() > 0
            for j = 0 to math.min(curTimeframe.demandZonesList.size() - 1, demandZones - 1)
                sdZoneInfoF = curTimeframe.demandZonesList.get(j)
                sdZoneInfoF.timeframeStr := curTimeframe.timeframeStr
                allSDZonesList.unshift(createSDZone(sdZoneInfo.copy(sdZoneInfoF)))

        if curTimeframe.supplyZonesList.size() > 0
            for j = 0 to math.min(curTimeframe.supplyZonesList.size() - 1, supplyZones - 1)
                sdZoneInfoF = curTimeframe.supplyZonesList.get(j)
                sdZoneInfoF.timeframeStr := curTimeframe.timeframeStr
                allSDZonesList.unshift(createSDZone(sdZoneInfo.copy(sdZoneInfoF)))

    if combineSDs
        combineSDsFunc()

    if allSDZonesList.size() > 0
        for i = 0 to allSDZonesList.size() - 1
            curSD = allSDZonesList.get(i)
            if isSDValid(curSD.info)
                renderSDZone(curSD)

bodySize = math.abs(close - open)
getMomentumCandleCount (lastBars, reqMult) =>
    bearishCnt = 0
    bullishCnt = 0
    for i = 0 to lastBars - 1
        if bodySize[i] >= averageBodySize * reqMult
            if close[i] > open[i]
                bullishCnt += 1
            else
                bearishCnt += 1
    [bullishCnt, bearishCnt]

[bullishMomentum, bearishMomentum] = getMomentumCandleCount(momentumSpan, momentumBodyMult)

var int lastDemandZone = 0
var int lastSupplyZone = 0
// Find Supply & Demand
if bar_index > last_bar_index - maxDistanceToLastBar
    if bullishMomentum >= momentumCount and bar_index - lastDemandZone > minDistanceBetweenZones
        lastDemandZone := bar_index
        newSDZone = sdZoneInfo.new(high[momentumSpan + 1], low[momentumSpan + 1], "Demand", time[momentumSpan + 1], na, time[momentumSpan + 1])
        clampSDZone(newSDZone)
        demandZonesList.unshift(newSDZone)
        if demandZonesList.size() > maxSDZones
            demandZonesList.pop()
    if bearishMomentum >= momentumCount and bar_index - lastSupplyZone > minDistanceBetweenZones
        lastSupplyZone := bar_index
        newSDZone = sdZoneInfo.new(high[momentumSpan + 1], low[momentumSpan + 1], "Supply", time[momentumSpan + 1], na, time[momentumSpan + 1])
        clampSDZone(newSDZone)
        supplyZonesList.unshift(newSDZone)
        if supplyZonesList.size() > maxSDZones
            supplyZonesList.pop()

    // Invalidation
    if demandZonesList.size() > 0
        for i = demandZonesList.size() - 1 to 0
            currentSD = demandZonesList.get(i)
        
            if na(currentSD.breakTime) 
                if (sdEndMethod == "Wick" ? low : math.min(open, close)) < currentSD.bottom
                    currentSD.breakTime := time

    if supplyZonesList.size() > 0
        for i = supplyZonesList.size() - 1 to 0
            currentSD = supplyZonesList.get(i)

            if na(currentSD.breakTime) 
                if (sdEndMethod == "Wick" ? high : math.max(open, close)) > currentSD.top
                    currentSD.breakTime := time

[demandZonesListTimeframe1, supplyZonesListTimeframe1] = getTFData(timeframeInfos.get(0), timeframe1)
[demandZonesListTimeframe2, supplyZonesListTimeframe2] = getTFData(timeframeInfos.get(1), timeframe2)
[demandZonesListTimeframe3, supplyZonesListTimeframe3] = getTFData(timeframeInfos.get(2), timeframe3)

var lastRetestIndexSupply = 0
var lastRetestIndexDemand = 0

float renderRetestLabelBuyside = na
int renderRetestLabelBuysideGUID = na

float renderRetestLabelSellside = na
int renderRetestLabelSellsideGUID = na

float renderBreakLabelBuyside = na
int renderBreakLabelBuysideGUID = na

float renderBreakLabelSellside = na
int renderBreakLabelSellsideGUID = na

var disabledDuplicateTF = false
// Disable Duplicate Timeframes
if not disabledDuplicateTF
    disabledDuplicateTF := true
    for i = 0 to timeframeInfos.size() - 1
        for j = 0 to timeframeInfos.size() - 1
            if i == j
                continue
            timeframeInfo1 = timeframeInfos.get(i)
            timeframeInfo2 = timeframeInfos.get(j)
            if timeframeInfo1.isEnabled and timeframeInfo2.isEnabled and timeframe.in_seconds(timeframeInfo1.timeframeStr) == timeframe.in_seconds(timeframeInfo2.timeframeStr)
                timeframeInfo1.isEnabled := false

if barstate.isconfirmed and bar_index > last_bar_index - maxDistanceToLastBar
    handleTimeframeInfo(timeframeInfos.get(0), demandZonesListTimeframe1, supplyZonesListTimeframe1)
    handleTimeframeInfo(timeframeInfos.get(1), demandZonesListTimeframe2, supplyZonesListTimeframe2)
    handleTimeframeInfo(timeframeInfos.get(2), demandZonesListTimeframe3, supplyZonesListTimeframe3)
    handleSDZonesFinal()

    // Breaks    

    if allSDZonesList.size() > 0
        for i = 0 to allSDZonesList.size() - 1
            curZone = allSDZonesList.get(i)
            if curZone.info.disabled
                continue
            if not showInvalidated and not na(curZone.info.breakTime)
                continue
            if na(curZone.info.breakTime)
                continue
            if time - curZone.info.startTime < minZoneSize * timeframe.in_seconds(curZone.info.timeframeStr) * 1000
                continue
            if curZone.info.startTime < nz(oldestBarTime, time)
                continue
            
            if time == curZone.info.breakTime
                if curZone.info.sdType == "Supply"
                    if curZone.info.breakTime - curZone.info.startTime > minZoneSize * timeframe.in_seconds() * 1000
                        renderBreakLabelBuyside := curZone.info.bottom
                        renderBreakLabelBuysideGUID := curZone.info.guid
                else
                    if curZone.info.breakTime - curZone.info.startTime > minZoneSize * timeframe.in_seconds() * 1000
                        renderBreakLabelSellside := curZone.info.top
                        renderBreakLabelSellsideGUID := curZone.info.guid
    
    // Retests
    if allSDZonesList.size() > 0
        for i = 0 to allSDZonesList.size() - 1
            curZone = allSDZonesList.get(i)
            
            if curZone.info.disabled
                continue
            if not showInvalidated and not na(curZone.info.breakTime)
                continue
            if not na(curZone.info.breakTime)
                continue
            if time - curZone.info.startTime < minZoneSize * timeframe.in_seconds(curZone.info.timeframeStr) * 1000
                continue
            if curZone.info.startTime < nz(oldestBarTime, time)
                continue
            
            middleLine = (curZone.info.bottom + curZone.info.top) / 2.0
            if curZone.info.sdType == "Supply" and bar_index - lastRetestIndexSupply > RETEST_COOLDOWN
                if high > curZone.info.bottom
                    renderRetestLabelBuyside := curZone.info.top
                    renderRetestLabelBuysideGUID := curZone.info.guid
                    lastRetestIndexSupply := bar_index
            else if curZone.info.sdType == "Demand" and bar_index - lastRetestIndexDemand > RETEST_COOLDOWN
                if low < curZone.info.top
                    renderRetestLabelSellside := curZone.info.bottom
                    renderRetestLabelSellsideGUID := curZone.info.guid
                    lastRetestIndexDemand := bar_index

//plotshape(not na(renderRetestLabelBuyside) and retestsEnabled ? renderRetestLabelBuyside : na, "", shape.labeldown, color = bearSDZoneColor, text = "R", location = labelsAtSameLevel ? location.absolute : location.abovebar, textcolor = color.white, size = size.small)
//plotshape(not na(renderRetestLabelSellside) and retestsEnabled ? renderRetestLabelSellside : na, "", shape.labelup, color = bullSDZoneColor, text = "R", location = labelsAtSameLevel ? location.absolute : location.belowbar, textcolor = color.white, size = size.small)

// Retests

if not na(renderRetestLabelBuyside) and retestsEnabled
    newLabel = label.new(bar_index, renderRetestLabelBuyside, style = label.style_label_down, color = bearSDZoneColor, text = "R", textcolor = color.white, size = size.small)
    //label.new(bar_index, renderRetestLabelSellside, style = label.style_label_up, color = bullSDZoneColor, text = "R", textcolor = color.white, size = size.small)
    if na(retestLabels.get(renderRetestLabelBuysideGUID))
        newContainer = retestLabelContainer.new(renderRetestLabelBuysideGUID)
        newContainer.labels := array.new<label>()
        newContainer.labels.push(newLabel)
        retestLabels.put(renderRetestLabelBuysideGUID, newContainer)
    else
        retestLabels.get(renderRetestLabelBuysideGUID).labels.push(newLabel)

if not na(renderRetestLabelSellside) and retestsEnabled
    newLabel = label.new(bar_index, renderRetestLabelSellside, style = label.style_label_up, color = bullSDZoneColor, text = "R", textcolor = color.white, size = size.small)
    if na(retestLabels.get(renderRetestLabelSellsideGUID))
        newContainer = retestLabelContainer.new(renderRetestLabelSellsideGUID)
        newContainer.labels := array.new<label>()
        newContainer.labels.push(newLabel)
        retestLabels.put(renderRetestLabelSellsideGUID, newContainer)
    else
        retestLabels.get(renderRetestLabelSellsideGUID).labels.push(newLabel)


if retestLabels.keys().size() > 0
    for i = 0 to retestLabels.keys().size() - 1
        curKey = retestLabels.keys().get(i)
        foundKey = false
        if allSDZonesList.size() > 0
            for j = 0 to allSDZonesList.size() - 1
                if allSDZonesList.get(j).info.guid == curKey
                    if allSDZonesList.get(j).info.disabled
                        continue
                    if not showInvalidated and not na(allSDZonesList.get(j).info.breakTime)
                        continue
                    if time - allSDZonesList.get(j).info.startTime < minZoneSize * timeframe.in_seconds(allSDZonesList.get(j).info.timeframeStr) * 1000
                        continue
                    if allSDZonesList.get(j).info.startTime < nz(oldestBarTime, time)
                        continue
                    foundKey := true
                    break
        if not foundKey
            for j = 0 to retestLabels.get(curKey).labels.size() - 1
                label.delete(retestLabels.get(curKey).labels.get(j))

// Breaks
if not na(renderBreakLabelBuyside) and breaksEnabled
    breakLabels.put(renderBreakLabelBuysideGUID, label.new(bar_index, renderBreakLabelBuyside, style = label.style_label_up, color = color.blue, text = "B", textcolor = color.white, size = size.small))

if not na(renderBreakLabelSellside) and breaksEnabled
    breakLabels.put(renderBreakLabelSellsideGUID, label.new(bar_index, renderBreakLabelSellside, style = label.style_label_down, color = color.blue, text = "B", textcolor = color.white, size = size.small))

if breakLabels.keys().size() > 0
    for i = 0 to breakLabels.keys().size() - 1
        curKey = breakLabels.keys().get(i)
        foundKey = false
        if allSDZonesList.size() > 0
            for j = 0 to allSDZonesList.size() - 1
                if allSDZonesList.get(j).info.guid == curKey
                    if allSDZonesList.get(j).info.disabled
                        continue
                    foundKey := true
                    break
        if not foundKey
            label.delete(breakLabels.get(curKey))

alertcondition(not na(renderRetestLabelBuyside) and barstate.isconfirmed, "Supply Zone Retest @ {{ticker}}", "Supply Zone Retest @ {{ticker}}")
alertcondition(not na(renderRetestLabelSellside) and barstate.isconfirmed, "Demand Zone Retest @ {{ticker}}", "Demand Zone Retest @ {{ticker}}")

alertcondition(not na(renderBreakLabelBuyside) and barstate.isconfirmed, "Supply Zone Break @ {{ticker}}", "Supply Zone Break @ {{ticker}}")
alertcondition(not na(renderBreakLabelSellside) and barstate.isconfirmed, "Demand Zone Break @ {{ticker}}", "Demand Zone Break @ {{ticker}}")
```

![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/c9678d23-e296-817b-849e-0003ceb9774c/44e2814b-6933-43ca-baea-e82a9daad933/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466RY4RXZH3%2F20260418%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260418T032716Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBkaCXVzLXdlc3QtMiJGMEQCIGeAZduaza7temIEL1pigsAAIN0%2BTMo0LNzV2ZwFmbrzAiApWe9QLpmvGg0yTvZkaEG6%2FPYkU8Y3EbUy1UAjzSo%2BniqIBAji%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDYzNzQyMzE4MzgwNSIM3WeOg2aqGJ1uxT18KtwDQ0Rgys6OmPWJyDsE%2FSbvHOUrQAlr8g4L3zKKGH8YeDfFOvl%2Bz6ZYi68IlVVngugwUFhEPL%2B%2FoZT6MGKk7%2Far0o61pBW3dxTNBCeH12RHBg9dCYqkGetrYyRl8MsMmEP258ry3rBDfDF14glQyTi13nQ6BakL1u0AO8%2BFWM%2BN9xaaj7g4FjIyJRF8Gc6CivaD5eAHcCwHTSqOTAwopUiRjC6UDWzc7rXdMlHHjfH2ydNmf7p9fZF0oCOk0qxGo%2FNY8MNlcs43RWxGBGCyiD13C1j1yMa5WU%2B967pCFej12HusAcvRC7sIYlqib4Azz9rCkZAF2UIF%2FjHMyCHUFRfqlQ3nVX9zWBtk%2BwkMwgHzGYnSi8h2Ifi66jcpFJgPdOXS1kpV0Ubrz8BiJLK9evxbCFgel7%2FZSOEH5vel0f%2F6%2BwY8D7n2H45FAANdYREAEoNbQrglsIGVdRKRNodv4DeLzSLCYf1jnRUQJ6CP4%2BfYDTN4HH4ma%2FMZNmIrtAVH3HDJm%2B7F%2FW3EFDWTWdc%2BIinZvDGIk2NbRv8SOr3PyKE6oVq2p1aR5JvqMnAmMfaqZaHyUBFIdimTTiF9i%2BhowdJRPq6mu9lmJ%2BuAjIk7%2FbqM4R1J5tXT7uAaW9Rbt7gwqKyLzwY6pgE69bnU7pU8U6uWldUkVA1XPHs%2BSOaRWdcH0r4CqQeUy7XCW3sx9KNPmuh0KX2Vas6S50gtzJLl5aBt9dSMDgtFjoc3kC%2BMUuBAv5%2FsBFDruKRxa5yDoomwCPgBOwcvz6bT8rgRS3nPd6JLm%2FEoYTpif61Y4J1M4j8011H%2FQex%2FYtl1a264kApZpuaqzbUPt9PkJJGU9DPQ8K2dPaA2F2OG2W1eaoFH&X-Amz-Signature=f63c645b1171775e9bfe767c61470de595239ed091f69b19439d72c8bd5a463b&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

ChatGPT：直接看图的话，**庄家更可能去“爆空单”（squeeze shorts）**。理由和要点如下——我把关键点挑出来，短而清晰：

1. 读图关键（图例）
- 绿色曲线/填充 = **累计空单清算强度（short liquidation）**。
- 红色曲线/填充 = **累计多单清算强度（long liquidation）**。
- 柱状为不同杠杆的清算量（浅蓝 10x、深蓝 25x、黄 50x、橙 100x 等）。
1. 为什么是压空（爆空）？
- 当前价（图中虚线）左边红色填充很低、曲线已接近零，说明**靠下方可爆的多单（long）已经很少**或已经被清算得差不多了。
- 右侧绿色填充/曲线很高，且在当前价上方不远处有一簇很高的橙色/黄色柱（高杠杆空单集中区），这表示**上方存在大量高杠杆的空单，一旦往上推就能触发大量爆仓**。
- 因此，从“能造成最大连锁爆仓”的角度看，往上顶爆空单能产生更大的连锁效应——这是庄家常用的诱多手法（squeeze）。
1. 具体位置（图上看得出来的）
- 115k 左右那一带有明显的高杠杆空单柱（橙/黄），是短期内最危险、最容易被挤爆的区域。
1. 风险提示与应对建议（务实）
- 这是基于可见清算分布的概率判断，不是确定性结论；庄家也会做反向止损诱导、盘口挂单掩护、突发消息等操作。
- 如果你是持仓者：**减杠杆、把止损设在高密集清算区外**；不要对着明显的爆仓簇重仓逆向持有。
- 如果想做跟随性交易：谨慎等待突破并观察成交放量与回测（突破是否真实），避免被“假突破”洗掉。
总结一句话：图上显示**上方的空单（short）仓位密集且杠杆高**，庄家更可能尝试往上抬价去挤爆空单（squeeze shorts）。不过市场有不确定性，操作请控制杠杆并管理好止损。

CVD 在加密货币交易和技术分析中是指 **Cumulative Volume Delta（累计成交量差值）**。它是一个基于成交量的指标，旨在直观地展现市场中的买卖压力。与传统的成交量指标只显示总交易量不同，CVD 深入分析了买方和卖方之间的交易量差异，并将其累积起来，从而揭示市场情绪和资金流向的真正动力。[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQEyxIpmmAFIirCT8jmfQxefdH8qrqkhNA0DrkCV9O64JyAIQvZSscyZboZMtqyMbnUB51VzRl6_qDNWOn-dtKcnCk88qucHkjzCxhMpuQrMWn9nW1z89ej-xYN9QdPJjalIrv_1Eld2n3uN4V2L4gveql89jXq4BayRnoGXSQ%3D%3D)][[2](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQGzIeiS9YRLfTQoqVZY2sGTjRwZ-mLxqTAthBSoY3VmT0gcNm7DrBH1yrKqK3F5XpYH7b8FP6QqgdEhDs1nPs_4FNmLodyl3nLYxf64Jn7UvlpDkn9lXziPd4p1D4IrL6RV53hRcaHNqG4ac6tk-B5kZPps01Y67mvseuIpUiU7VaGxWNfcOXupUGZe6BA7)][[3](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQGWUdeusis2Olekjl9HN_mua9A_sSwcGU-x6abQZZ-liwDuq1vVq2kwL_yk_4j9hGYFiq0FTo3yeeMESZXsALcHC5RPf6nTQXL52wS4DHuNPnnI1c5QuDrADZbHM5OX_TRSRNIe4psh6YNcgYk7HKKMjcgPJ3fKGL6OuCYHpp7vVRvY85ImXdwy0TRPGM_EMqxIygP0XeBQf9q6rvLD09JgtWZjK80PZW1L05y9fASFjA%3D%3D)][[4](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQHC1qhTSxg8_57-fZGkHy7dBDujnUv4VgQhDEYP7VkgG0S231jP9tgYTNgbveN3v26ozC9RO1MYGWTDAYbdERM62A_2hUbgb-1dbplshcyYjEVgTOcIExQ2QArTMLiHulAx_ZffdFHxGvfj)]

**CVD 的工作原理：**

1. **成交量差值 (Volume Delta)**：首先，CVD 的基础是“成交量差值（Volume Delta）”。它计算的是在特定时间周期内，激进买入量与激进卖出量之间的净差。通常，在买价（Bid Price）上执行的交易被视为卖出，而在卖价（Ask Price）上执行的交易被视为买入。如果买入量大于卖出量，则 Delta 为正；反之，如果卖出量大于买入量，则 Delta 为负。[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQEyxIpmmAFIirCT8jmfQxefdH8qrqkhNA0DrkCV9O64JyAIQvZSscyZboZMtqyMbnUB51VzRl6_qDNWOn-dtKcnCk88qucHkjzCxhMpuQrMWn9nW1z89ej-xYN9QdPJjalIrv_1Eld2n3uN4V2L4gveql89jXq4BayRnoGXSQ%3D%3D)][[2](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQGzIeiS9YRLfTQoqVZY2sGTjRwZ-mLxqTAthBSoY3VmT0gcNm7DrBH1yrKqK3F5XpYH7b8FP6QqgdEhDs1nPs_4FNmLodyl3nLYxf64Jn7UvlpDkn9lXziPd4p1D4IrL6RV53hRcaHNqG4ac6tk-B5kZPps01Y67mvseuIpUiU7VaGxWNfcOXupUGZe6BA7)][[3](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQGWUdeusis2Olekjl9HN_mua9A_sSwcGU-x6abQZZ-liwDuq1vVq2kwL_yk_4j9hGYFiq0FTo3yeeMESZXsALcHC5RPf6nTQXL52wS4DHuNPnnI1c5QuDrADZbHM5OX_TRSRNIe4psh6YNcgYk7HKKMjcgPJ3fKGL6OuCYHpp7vVRvY85ImXdwy0TRPGM_EMqxIygP0XeBQf9q6rvLD09JgtWZjK80PZW1L05y9fASFjA%3D%3D)][[5](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFzBIlpmkwGfx0AykXEgi3iOcSFedyUleqOW4cdtPagwycDPs5MvkDHbAO_OVCnWVQ0qPpQaG5M-MtEHy2z8-XVO--qlmPR9w78MJhPKKmLTr5PT8U6H1NbcZ4XDx3WcuIpdhvwLlgT8lGsWoxhv9gsT7lfyMA-VYqIWhSZwQBH7aN2)][[6](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQEqd24FlA-ZXqQYWsC9tF2X5MkupkT1_PH1XhfQG2oF8LSF6EXl35vRvgqPFiPLgohOfnjAOZJ58HbpZGkgXT0uXbIxbmNLyrL4QokuIIoepUf9GKqMrWdi23__qMxO1LdV1XL22FoKi_URg7M%3D)]
1. **累积计算 (Cumulative Calculation)**：CVD 的“累计”部分意味着它会将每个时间周期（例如每根 K 线）的成交量差值累加起来，形成一个连续的曲线。这个累积值可以从零开始，并随着时间的推移而增加或减少，反映了持续的市场压力。[[5](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFzBIlpmkwGfx0AykXEgi3iOcSFedyUleqOW4cdtPagwycDPs5MvkDHbAO_OVCnWVQ0qPpQaG5M-MtEHy2z8-XVO--qlmPR9w78MJhPKKmLTr5PT8U6H1NbcZ4XDx3WcuIpdhvwLlgT8lGsWoxhv9gsT7lfyMA-VYqIWhSZwQBH7aN2)][[6](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQEqd24FlA-ZXqQYWsC9tF2X5MkupkT1_PH1XhfQG2oF8LSF6EXl35vRvgqPFiPLgohOfnjAOZJ58HbpZGkgXT0uXbIxbmNLyrL4QokuIIoepUf9GKqMrWdi23__qMxO1LdV1XL22FoKi_URg7M%3D)][[7](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQE7rR8O9UIqmN11AIMZiyMbVegOT0Ic7YaHNL6t2RrhkepsXLN7e54bHmidXGWp811Rn3AJqDd3oMObwp2CCm8OhfY1QJr5TiV7Ai1xnkPswE7Twv8TtyKsu3mXisL4r6y1Yq7q9Kkn2raNm07IYCObi9Y71--BE9wK)]
**CVD 揭示了什么？**

- **买卖压力平衡**：CVD 曲线上升表示买方压力占据主导，市场情绪偏向看涨；CVD 曲线下降则表示卖方压力更强，市场情绪偏向看跌。[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQEyxIpmmAFIirCT8jmfQxefdH8qrqkhNA0DrkCV9O64JyAIQvZSscyZboZMtqyMbnUB51VzRl6_qDNWOn-dtKcnCk88qucHkjzCxhMpuQrMWn9nW1z89ej-xYN9QdPJjalIrv_1Eld2n3uN4V2L4gveql89jXq4BayRnoGXSQ%3D%3D)][[3](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQGWUdeusis2Olekjl9HN_mua9A_sSwcGU-x6abQZZ-liwDuq1vVq2kwL_yk_4j9hGYFiq0FTo3yeeMESZXsALcHC5RPf6nTQXL52wS4DHuNPnnI1c5QuDrADZbHM5OX_TRSRNIe4psh6YNcgYk7HKKMjcgPJ3fKGL6OuCYHpp7vVRvY85ImXdwy0TRPGM_EMqxIygP0XeBQf9q6rvLD09JgtWZjK80PZW1L05y9fASFjA%3D%3D)][[7](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQE7rR8O9UIqmN11AIMZiyMbVegOT0Ic7YaHNL6t2RrhkepsXLN7e54bHmidXGWp811Rn3AJqDd3oMObwp2CCm8OhfY1QJr5TiV7Ai1xnkPswE7Twv8TtyKsu3mXisL4r6y1Yq7q9Kkn2raNm07IYCObi9Y71--BE9wK)][[8](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQGK3Q3uReg6ZUtmHEO0_-fuOSSk843-7EsdEnGiOOR5P_llAlybusoipIqq5ThFBGhdiWd-b1HDRinfMuKU6Cb_WIwjV86NqN9QSqtLPkTCBPDGM_3Hq5wpYXvOSdB8383b4JTDOx-4HHywN1Ratg%3D%3D)]
- **市场趋势确认**：当价格上涨时，如果 CVD 也同步上涨，则表明上涨趋势有真实的买盘支撑，趋势较为健康。反之，如果价格上涨而 CVD 下跌，则可能预示着上涨缺乏实质性买盘，趋势可能出现反转。[[7](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQE7rR8O9UIqmN11AIMZiyMbVegOT0Ic7YaHNL6t2RrhkepsXLN7e54bHmidXGWp811Rn3AJqDd3oMObwp2CCm8OhfY1QJr5TiV7Ai1xnkPswE7Twv8TtyKsu3mXisL4r6y1Yq7q9Kkn2raNm07IYCObi9Y71--BE9wK)][[9](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFzj7Npqtofzrp5Ziwfovm_E123hif4xSFH8BDM1ZYnAPnbdQX5PsMmTHImpqHpsZBZte8R9lJpMviVRVauG4gWbZgLBXwO7B7S9ljXneknxQU8hKsg-rDkt0Jhh8rmd8ECf5xlG51zCyG6JtmiMrwC9c3O_vjFs49Xqhw0s9e0EpMeuTpFJF_AmozliRZjYW8rcEiOUw%3D%3D)]
- **趋势反转信号（背离）**：CVD 最重要的应用之一是识别背离。当价格创出新高，但 CVD 未能创出新高（或反而下降）时，这被称为看跌背离，可能预示着上涨动能减弱，价格即将反转下跌。反之，当价格创出新低，而 CVD 未能创出新低（或反而上升）时，这被称为看涨背离，可能预示着下跌动能减弱，价格可能反转上涨。[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQEyxIpmmAFIirCT8jmfQxefdH8qrqkhNA0DrkCV9O64JyAIQvZSscyZboZMtqyMbnUB51VzRl6_qDNWOn-dtKcnCk88qucHkjzCxhMpuQrMWn9nW1z89ej-xYN9QdPJjalIrv_1Eld2n3uN4V2L4gveql89jXq4BayRnoGXSQ%3D%3D)][[10](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQH4QKA7mwdtrgndOvUn_SCaYmaCZHmAjD1aB6NifKlFek4ltAJb49EDXTYGZpw2U4oa-bN0NH8JumUB95mBXw-GFzAXuTc6n8iQTgGTl8clNW4ZGS4dMxBbDBWnkDRKhH6nB2ysffvzh8aASE-kOGFhwN0IXSTuhcsMiBHHBA%3D%3D)][[11](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFmoW2qXz89aXzrE0fCTu98vwfK43WLpz0M-d5mlNoO-ogewl0MUQKWgwnqT5PxzOdIS8KwVF51iPFT0qONvbzYsjhOEF04ZlTgY3rD5otzuk2G2-U0MipFbB8qUR2v2XPSt_m5JMGaSWtIW5XCPJqpwFPmbeGUTuEs9V8zv8OQJypY-SUfszM%3D)]
- **机构活动洞察**：通过 CVD，交易者可以更好地洞察市场中机构或大户的买卖行为，因为这些大额交易往往会在成交量差值上留下明显的痕迹。[[7](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQE7rR8O9UIqmN11AIMZiyMbVegOT0Ic7YaHNL6t2RrhkepsXLN7e54bHmidXGWp811Rn3AJqDd3oMObwp2CCm8OhfY1QJr5TiV7Ai1xnkPswE7Twv8TtyKsu3mXisL4r6y1Yq7q9Kkn2raNm07IYCObi9Y71--BE9wK)]
**如何使用 CVD？**

- **确认趋势**：在上升趋势中，观察 CVD 是否持续走高；在下降趋势中，观察 CVD 是否持续走低。[[9](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFzj7Npqtofzrp5Ziwfovm_E123hif4xSFH8BDM1ZYnAPnbdQX5PsMmTHImpqHpsZBZte8R9lJpMviVRVauG4gWbZgLBXwO7B7S9ljXneknxQU8hKsg-rDkt0Jhh8rmd8ECf5xlG51zCyG6JtmiMrwC9c3O_vjFs49Xqhw0s9e0EpMeuTpFJF_AmozliRZjYW8rcEiOUw%3D%3D)]
- **寻找反转**：关注价格与 CVD 之间的背离，将其作为潜在趋势反转的早期信号。[[1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQEyxIpmmAFIirCT8jmfQxefdH8qrqkhNA0DrkCV9O64JyAIQvZSscyZboZMtqyMbnUB51VzRl6_qDNWOn-dtKcnCk88qucHkjzCxhMpuQrMWn9nW1z89ej-xYN9QdPJjalIrv_1Eld2n3uN4V2L4gveql89jXq4BayRnoGXSQ%3D%3D)][[10](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQH4QKA7mwdtrgndOvUn_SCaYmaCZHmAjD1aB6NifKlFek4ltAJb49EDXTYGZpw2U4oa-bN0NH8JumUB95mBXw-GFzAXuTc6n8iQTgGTl8clNW4ZGS4dMxBbDBWnkDRKhH6nB2ysffvzh8aASE-kOGFhwN0IXSTuhcsMiBHHBA%3D%3D)]
- **结合其他指标**：CVD 通常与其他技术分析工具结合使用，例如价格行为、支撑阻力位、开仓量（Open Interest）等，以提高交易信号的可靠性。[[5](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFzBIlpmkwGfx0AykXEgi3iOcSFedyUleqOW4cdtPagwycDPs5MvkDHbAO_OVCnWVQ0qPpQaG5M-MtEHy2z8-XVO--qlmPR9w78MJhPKKmLTr5PT8U6H1NbcZ4XDx3WcuIpdhvwLlgT8lGsWoxhv9gsT7lfyMA-VYqIWhSZwQBH7aN2)][[7](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQE7rR8O9UIqmN11AIMZiyMbVegOT0Ic7YaHNL6t2RrhkepsXLN7e54bHmidXGWp811Rn3AJqDd3oMObwp2CCm8OhfY1QJr5TiV7Ai1xnkPswE7Twv8TtyKsu3mXisL4r6y1Yq7q9Kkn2raNm07IYCObi9Y71--BE9wK)][[9](https://www.google.com/url?sa=E&q=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fgrounding-api-redirect%2FAUZIYQFzj7Npqtofzrp5Ziwfovm_E123hif4xSFH8BDM1ZYnAPnbdQX5PsMmTHImpqHpsZBZte8R9lJpMviVRVauG4gWbZgLBXwO7B7S9ljXneknxQU8hKsg-rDkt0Jhh8rmd8ECf5xlG51zCyG6JtmiMrwC9c3O_vjFs49Xqhw0s9e0EpMeuTpFJF_AmozliRZjYW8rcEiOUw%3D%3D)]
# 📘 CoinGlass 清算热力图笔记

---

## 1. 清算热力图的基本定义

- **横轴**：时间。
- **纵轴**：价格。
- **颜色**：从紫到黄，表示清算强度逐渐增加。黄色亮区 = 清算集中度高。
👉 本质：显示在某个价格区间，存在多少杠杆仓位可能触发清算。

---

## 2. 上下方的“买单/卖单”逻辑

- **参照点**：始终是“当时的市场价格”。
- **价格上方亮区**：说明在这个价格以上，有大量做空仓位的清算点（价格继续上涨会触发这些空单的爆仓）。
- **价格下方亮区**：说明在这个价格以下，有大量做多仓位的清算点（价格继续下跌会触发这些多单的爆仓）。
---

## 3. 历史 K 线上的清算热力图

- 历史热力图依然会显示清算密集区。
- 但是，它并不会“随现在的价格改变含义”，而是固定在当时的市场背景下。
- 因此，想要解读历史清算区，一定要结合当时的实时价格来判断其是多单还是空单清算点。
---

## 4. 亮区横向长度的含义

- 横向延伸表示：某一价格区间在一段时间内持续存在大量潜在清算点。
- 短周期图（如 1 分钟、5 分钟）：能看到很多短期的小亮区，细节更丰富。
- 长周期图（如 1 小时、1 天）：会把数据做时间聚合，小规模亮区可能被“稀释”，因此消失不见。
👉 所以，有些亮区短周期能看到，长周期看不到，是因为聚合尺度不同。

---

## 5. 模型 1 / 2 / 3 的区别

CoinGlass 提供三种不同的计算模型，满足不同需求：

- **模型 1**：只统计高杠杆仓位（如 10X、25X、50X、100X），突出显示高杠杆交易者的清算点。
- 用途：捕捉短期风险，适合短线交易者。
- **模型 2**：统计所有杠杆水平的仓位（低杠杆 + 高杠杆）。
- 用途：全局视角，适合中长期趋势分析。
- **模型 3**：在模型 2 的基础上增加交互功能，可以通过调节“流动性阈值”筛选高风险区。
- 用途：让用户聚焦自己关心的“强磁区”，灵活定制。
---

## 6. 总结

- 清算热力图是“价格—时间—清算强度”的三维可视化。
- 判断亮区是多单还是空单清算，要结合**当时价格**。
- 横向长度 = 清算风险的持续时间。
- 不同周期会改变亮区的显著程度。
- 模型 1 聚焦高杠杆，模型 2 全面覆盖，模型 3 提供阈值筛选。
👉 使用场景：

- **短线交易**：重点看模型 1 + 短周期，捕捉爆仓点。
- **中长线研究**：用模型 2 + 长周期，观察市场潜在的清算分布。
- **精细化操作**：用模型 3 自定义风险过滤，找出“价格磁区”。
---

要不要我帮你把这份笔记再整理成一份 **图解版（结构图/思维导图）**，方便快速复盘？

![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/c9678d23-e296-817b-849e-0003ceb9774c/7cf213c9-f3a1-4d15-87d8-a1b45df347da/img_v3_02qh_fd90a7a0-653a-4f06-86ff-6d3842f9eefg.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466R6BTHORE%2F20260418%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260418T032724Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBkaCXVzLXdlc3QtMiJHMEUCIQC7oOZYCjhT6vcwX9BMOahbYju8A4AlR0zswTryKYK5QAIgPOPfp4qszcW9UMoBAKJxxeGR%2Fal8aw%2Bky%2F8RpjX1F0MqiAQI4v%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDGbYY%2FNhBX8tut%2FuuyrcA0Cc0O%2BKi1uZIQzvB%2B095oadzRQaNcx1yaUkbuFSWdEZqf17y7%2Bxm76Ly5EmWhwByRlvSeSAIrQISH%2Bv8C7mIvisMDcnfENmOgX2OFQLhqWPDG%2FKYMOchIzBVLpLjh%2BvPXdGwgU9sw%2FcZ%2FkXy%2Fb4jYmJWli9jbIAmIJH%2BaBWdeyfU5BlJ%2FAwyPTkWHTFNCG3j9aqpU5j6dc2d5pkKsMi%2FsCtMcGuS5kH16MGUCLaJJizXdxMIaYE7Nk1pr5G%2BYkaTZXzc4L0spn668tUOzvCbKX6n5lQ6iyOIJymRKHJACuolpQmW97DdL0ByzEjZHY69TF1PWewfFrVF4IJvX5n1UA6z5lkOHOVmdvnQclfvRA58nqg6f0SVrG1mChmMsH8ORJhjCS6f5maizd09XBU8%2FLHPqxJTHa85rxVYkuhPf8fErly%2BDTA56ohknfYExf8nnckMWy0a2ReFmJVPq2DLQmfTZr88ZQv%2B7cHNSrF4MwScyl%2FEVOjg0eEpJCJteWu8RaaQVZjKqkxHsj74KGq8qthlXZPl61iU5oCOrebbgGHRy%2Bt1w6wq2VAauInN8lQhxzDHFvJ9rIWl2JX672BhJA33Wp39KkCG0uNPBVFcXM%2Fu%2BZcJhLd2R7Ciw3NMP2ri88GOqUBN8v60E9nb6czzgCkKZb0%2Bf8gJPlBJhWh9GEFSkh6pkYwozaFGZ4TcIrGNSskHOesdBIw8j%2Bprm%2BxGiqb4Yxcr3WA08R65yjs%2Bm%2BNZz4IqpyF2ZgLCy0ZB11dv8NzXIQMznsioUuvIGGGr0Gf%2FK2Du6%2BzMT9XT%2Fc%2BOSJ6RFMBAzcJV8vZXNALGenKTnJatqtSeFzIfz37jxeUGdFJ74iWf2u8Dbh4&X-Amz-Signature=b180ba63d86455c0d43000ee7da9011f648552ff1d281401e3bbe0e6f75e2ae7&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

# 1. 流动性热力图是什么？

- 显示的是 **订单簿中的未成交挂单分布**。
- 图上用颜色来表示流动性强度：
- **亮色（黄色/橙色）= 该价位挂单多，流动性强**。
- **暗色（紫色/深色）= 该价位挂单少，流动性弱**。
- 这些横线会固定在某个价格档位，不会随K线移动。
---

## 2. 颜色代表买单还是卖单？

- **颜色本身不区分买单/卖单**，它只表示“订单量的多少”。
- 要判断是买墙还是卖墙，必须结合 **当时的市场价格**：
- **价格上方的亮区 → 卖单墙（阻力）**
- **价格下方的亮区 → 买单墙（支撑）**
---

## 3. 历史K线与热力图的关系

- 热力图不仅展示当前订单簿，还会保存 **历史时刻的订单簿快照**。
- 所以你看到历史K线时，旁边的亮区就是当时真实存在的挂单分布。
- 历史的含义是固定的，不会因为“现在价格”不同而改变：
- 当时价格上方的亮区 = 当时的卖单墙。
- 当时价格下方的亮区 = 当时的买单墙。
---

## 4. 关键结论

1. **亮区 = 高流动性，但方向要靠价格位置来判断。**
1. **实时盘面**：跟着当前价格解释上/下方。
1. **历史盘面**：解释基于当时价格，含义已经锁定。
1. 热力图的亮区往往就是潜在的 **支撑/阻力位**。
---

## 5. 官方文档的说法

- 官方说明：
- **暖色（黄色）= 活跃度高**，冷色（紫色）= 活跃度低【Coinglass Learning Center】。
- 这些高流动性区域通常会成为支撑或阻力。
- 鼠标悬停在亮区上，可以看到当时的具体挂单量。
---

✅ 一句话总结：

**Coinglass 流动性热力图显示的是某个价位的挂单密集程度。
颜色本身不分买卖，要结合价格位置来判断支撑/阻力。
历史部分的含义是固定的，实时部分则随当前价格而定。**

---

要不要我把这个笔记再整理成一个 **图文对照版（带流程图/标注图）**，方便你以后看图时直接套用？

## 显示差值

![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/c9678d23-e296-817b-849e-0003ceb9774c/2b7a537f-767b-4da5-b3d6-350f1c7476b7/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466UCFZ6QVU%2F20260418%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260418T032726Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBkaCXVzLXdlc3QtMiJHMEUCIQDUrbKRbTbhDI3dYu4UXc%2FQqCSGVaTGZvN%2BZDmR5ZNKuQIgW9iqw2jwan%2F1XX%2BfHWXYciivXWM%2FklduZKcSqrZuriwqiAQI4v%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDIYJykF5TFujNiaDpyrcA0ttEnE8Rjaw21NlJclj4Y%2BguUJMEqBMbYkeAQYniULDHv13ksOMqH0g7ubteRPRE4XOze5kqdKZt2yWq7eQSIGxNHHcotxml4890eN8jNNSWe00NveYnIAo6XGmKx2LmO%2BzFDQTWqEJKtj9q7F9539NNPgZBM6hs%2B7W%2FzUZs3Ksw%2Fdcc8gfK8lrgHKz2M5%2BK%2B24KeDFWAW46GQYSFvD7wbx%2BJsRw3xHXqcxtb5aJNXrvG0X8j97C3VMdc%2B7%2B7UYuK4W5Zsy%2FBAEYqQXI7Kgm8irSE7TM0Gq%2BKOIHJq4az2q%2FczbAyd5jUfvo8mUmBHOep9GU3zHW5lEO7fvvqQKOmlYMYeu%2BgfP0OXQou5TYmzjwwPxKm59v%2F4I0li2l5G1QRHaLwJY%2FE8kO0rfyXKfFB58n%2Bt259CcB8RaEeDY9Kl0NoMrPpoW2eAkazcVn8Kp1YDB8dj5nD%2FfZHLBHBIfdE6D1zHQO1F4VCJlkF7F2oU02rpf1wio4N91kwh6VZu0SAMLBrPdGbj%2BuV7scoPH84FaC30qu791TW267ZWxzHyvMEJDAZP6qBWMZq03eooaAhSPIual%2FchDUoRCY%2FzyEBuixMWeiHQBo%2Bs3IAXjpEXhhZpbVsXHv%2F8EuAcGMI6ui88GOqUBmmo%2FFwYrJQpMFI93XSCir7g3neObcUUR8nt2nvmOFJ5MI1hzZCqx304EjxXuYKRxzco%2BvWnn0kqQ1dHQ3IcquRKfKzhaOR0j%2BUQUUHIAVEpvtKwCo0ARk3bj6Sc9WbKRgZMTG3XlDzDYlI8bLuXAGDv8QiNpORxnlFZjucHB2qYZAIRgX4KE%2BOYO3ZqoHHGsxro0qPNYPcOehnRPFe5jCAYq3AE5&X-Amz-Signature=5affb6c366695391f0278c1aa8f7925ebe38fb395f756c46fc42f972a8290ff1&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

## 不显示差值

![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/c9678d23-e296-817b-849e-0003ceb9774c/a2cefe68-378e-48b7-835a-9c75e5f0ed4c/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466UCFZ6QVU%2F20260418%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260418T032726Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBkaCXVzLXdlc3QtMiJHMEUCIQDUrbKRbTbhDI3dYu4UXc%2FQqCSGVaTGZvN%2BZDmR5ZNKuQIgW9iqw2jwan%2F1XX%2BfHWXYciivXWM%2FklduZKcSqrZuriwqiAQI4v%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDIYJykF5TFujNiaDpyrcA0ttEnE8Rjaw21NlJclj4Y%2BguUJMEqBMbYkeAQYniULDHv13ksOMqH0g7ubteRPRE4XOze5kqdKZt2yWq7eQSIGxNHHcotxml4890eN8jNNSWe00NveYnIAo6XGmKx2LmO%2BzFDQTWqEJKtj9q7F9539NNPgZBM6hs%2B7W%2FzUZs3Ksw%2Fdcc8gfK8lrgHKz2M5%2BK%2B24KeDFWAW46GQYSFvD7wbx%2BJsRw3xHXqcxtb5aJNXrvG0X8j97C3VMdc%2B7%2B7UYuK4W5Zsy%2FBAEYqQXI7Kgm8irSE7TM0Gq%2BKOIHJq4az2q%2FczbAyd5jUfvo8mUmBHOep9GU3zHW5lEO7fvvqQKOmlYMYeu%2BgfP0OXQou5TYmzjwwPxKm59v%2F4I0li2l5G1QRHaLwJY%2FE8kO0rfyXKfFB58n%2Bt259CcB8RaEeDY9Kl0NoMrPpoW2eAkazcVn8Kp1YDB8dj5nD%2FfZHLBHBIfdE6D1zHQO1F4VCJlkF7F2oU02rpf1wio4N91kwh6VZu0SAMLBrPdGbj%2BuV7scoPH84FaC30qu791TW267ZWxzHyvMEJDAZP6qBWMZq03eooaAhSPIual%2FchDUoRCY%2FzyEBuixMWeiHQBo%2Bs3IAXjpEXhhZpbVsXHv%2F8EuAcGMI6ui88GOqUBmmo%2FFwYrJQpMFI93XSCir7g3neObcUUR8nt2nvmOFJ5MI1hzZCqx304EjxXuYKRxzco%2BvWnn0kqQ1dHQ3IcquRKfKzhaOR0j%2BUQUUHIAVEpvtKwCo0ARk3bj6Sc9WbKRgZMTG3XlDzDYlI8bLuXAGDv8QiNpORxnlFZjucHB2qYZAIRgX4KE%2BOYO3ZqoHHGsxro0qPNYPcOehnRPFe5jCAYq3AE5&X-Amz-Signature=65d632ef2dc20c4a24f62eab6d810732557e4c1292585fe5e9f480dab7c44dee&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

## **Market Value to Realized Value ****市值/已实现价值比**

> 衡量比特币市场情绪与估值的利器

MVRV-Z Score是一个经典且强大的链上估值指标，它通过对比比特币的**流通市值**与**已实现市值**，并运用统计学上的**标准差**进行标准化，以判断比特币当前价格相对于其链上“实际价值”是处于高估还是低估状态。

---

### 一、标准差（Standard Deviation）：衡量离散程度的基石

在深入了解 MVRV-Z Score之前，我们必须先理解其公式中的核心统计概念——**标准差（Standard Deviation）**。

**标准差**是统计学中衡量一组数据（例如：比特币流通市值与已实现市值的差值）离散程度（即数据波动性）的指标。

- **其意义在于：** 告诉我们数据点平均偏离其均值（平均值）的程度。
- **在金融中的作用：** 它常被用来衡量资产回报的波动性（风险）。
- **在 MVRV-Z 中的作用：** 它是用于将原始的市值差值进行**标准化**，从而将原始数据转化为一个可跨周期、跨量级进行比较的统计量——**Z 分数**。
### 二、MVRV-Z Score 的构成要素

MVRV-Z Score基于两个关键的链上指标：

### 1. 流通市值 (Market Value/Circulating Market Cap)

- **定义：** **当前比特币价格乘以所有流通中的比特币数量**。
- **特性：** 这是市场普遍认可的、最容易观察到的比特币总价值，它波动性高，受市场情绪影响大。
### 2. 已实现市值 (Realized Value/Realized Cap)

- **定义：** **基于链上交易的价值**。它通过**计算链上所有比特币的「最后移动价值」**（即 UTXO「Unspent Transaction Output」被花费时的价格）**的加总而得**。
- **特性：** 它代表了整个比特币供应的**聚合成本基础**。**它会随着新资金的流入（以更高的价格买入并移动）而增加，但不会像流通市值那样随每日价格波动剧烈变化**，因此被视为比特币的“**内在价值**”或“**实际价值**”代理指标。
### 三、MVRV-Z Score 的公式与 Z 标准化

MVRV-ZScore 的核心在于计算流通市值与已实现市值之间的**差异**，并利用标准差来**标准化**这个差异，从而得到一个相对的、具有统计意义的指标。

其公式如下：

![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/c9678d23-e296-817b-849e-0003ceb9774c/69008f93-551d-4797-87d4-46358cfe16a4/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466Q57ORLSZ%2F20260418%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260418T032727Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBkaCXVzLXdlc3QtMiJHMEUCIQCT6q5Y8KxUQuEa7O7wx%2BpnM7bzCjMA8VvIpdIfq1RUCwIgIehUtifqt6WMsWW8Iw%2BEOCRrjHt0yBT9tqylPDAIhFoqiAQI4v%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDMbR1P3O%2FvPZ72PkvyrcA%2B2IYLLD4XnxivwOZiHRmUsT9%2F3ONg6qPEWXSEeBd1bWPh6mjEN1aUeavdbon9%2BVHS8ga2m3QtKX57GiFaxqZVVnbsalLFAXZG9%2BJDHAV5goMcScKgQnJMZ%2FJLon14b4hkjecLWWNogm%2BuX1k2ffk%2FZ9o2nr19x22eY5%2F4ucP%2BwZeuVobhhOvNTr1gM%2B%2BMWKaE2gAMgK6ekC61I11NomqeD1fokpf0L73Xi6MGR53HkDMUONjHs3Dt1IEpAGxbS13Z3TcXANPuIcJHmjQImzOpOoW%2FaZ%2F9g5gZjZjeYtIOzahHma85L8BSd%2B5ENTrrq8tO%2BKG7Yu9pVHcL4SGvWTTonrmhiNaocuEgUKu%2FiH3dVjIKNpdE9%2FpAA0Ov%2Bgl0TCEildNGN1YRkS4hRAZFW4tY02K68toGGEWMh0IFOTJAgHwWFxYdEgqT1Qsj5ker84RyhRyudhY%2BSSBvDIleUt4HugBMfFuVVM6raxnVca2ruzn5g6wP6CI%2FhT1fUmdDnM8Dd60fhgFmxaR7S1uUdOSwXLeTpddbrWbJI4hFdy%2FEw%2BpWqi84cLaPDE73L0ybzgXAxF3tOaaTYC2TVjA9kenzj66BT15EWmtSj26yib66cgofBSv7fAwIgGJfUpMNqti88GOqUBPLtyrJEiYwgEaj8RYnn0qQTz6T%2B5FnIJKJgqCv27LuttHie21Y5HRi23b9cOavYgd0RlYCbEzDetAkIZZSHzmMfqBEOoX%2B6sbARNFUz%2FcKQUmlEHGx6FBTyVceISUGWXZZ%2BM1iK6f0oS%2BLRygxe2Ii%2FjsDH3VLGISmCOFWyw58E0h7QYYICa4KBQ4jpAjV6Dy2WY1ag6AHp91Cq1ewFkRxBnp85s&X-Amz-Signature=fa9a10e0357218dfcea9da1d68b58419e29731e22c2528c6df7c366b39d098eb&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

*（注：根据更严谨的统计定义，分母通常是「流通市值」减去「已实现市值」这个差值的历史标准差，以完成 Z-Score 的标准化步骤。）*

### Z 标准化 (Z-Standardization) 的意义：

通过除以历史标准差，MVRV-Z Score将原始差值转化为了**标准差的倍数**。

- **结果：** 这一分数表明当前流通市值相对于已实现市值的偏离程度，已经达到了历史上的第多少个标准差之外。**这使得我们可以将不同牛市周期的高点（例如，2013年和2021年）放在同一统计框架下进行比较。**
### 四、MVRV-Z Score的解读与应用

根据历史数据，MVRV-Z Score能有效划分比特币市场的“高风险”和“低风险”区域。

[table - see children]

| MVRV-Z Score值 | 市场状态 | 解读 | 投资提示 |
| **极高**（如 > 7 或处于历史红色区域） | **严重高估** | 流通市值远高于已实现市值，市场狂热，投资者集体处于高额浮盈状态。 | **高风险区**：历史经验表明，价格下行趋势的机率增加，须**留意追高的风险**，适合考虑减仓。 |
| **中性**（如在 0 到 3 之间） | **合理估值** | **市场处于正常波动范围，估值相对合理。** | **观察期**：可结合其他指标判断趋势。 |
| **低位**（如 < 0 或处于历史绿色区域） | **低估或熊市底部** | **流通市值接近或跌破已实现市值，市场情绪悲观，大部分投资者处于浮亏状态。** | **低风险区**：历史经验表明，市场处于积累期或底部区域，适合**长期投资者关注**。 |
### **核心逻辑：**

1. 当 MVRV-Z Score**过高**（进入红色区域），表明比特币市值相对于实际价值呈现**高估**。这通常是市场泡沫或牛市顶部的信号。
1. 当 MVRV-Z Score**过低**（进入绿色区域），表明比特币市值相对于实际价值呈现**低估**。这通常是熊市底部或绝佳买入区域的信号。
**总结：** MVRV-Z Score是一个强大的周期性指标，它将链上价值（已实现市值）作为锚点，并利用统计学的工具（标准差）来判断市场情绪（流通市值）的过度偏差程度，为投资者提供了衡量市场风险和机遇的独特视角。

---

## Z 标准化的核心概念

> Z 标准化可以告诉你：**一个特定的数据点，偏离其所在数据集的平均值（均值），相隔了多少个标准差的距离。**

### Z 分数的意义

Z 分数是一个**无量纲**（不带单位）的指标，它消除了原始数据的量纲和单位影响，使得不同类型、不同规模的数据集可以进行公平地比较。

- **如果 Z 分数 = 1：** 表示该数据点位于**平均值之上**，距离平均值正好 1 个标准差。
- **如果 Z 分数 = -2：** 表示该数据点位于**平均值之下**，距离平均值正好 2 个标准差。
- **如果 Z 分数 = 0：** **表示该数据点正好等于平均值**。
### Z 标准化的公式

任何一个数据点 **X** 的 Z 分数计算公式如下：

![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/c9678d23-e296-817b-849e-0003ceb9774c/2ec39bf3-0079-42c4-b10d-8c73c809ed45/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466Q57ORLSZ%2F20260418%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260418T032727Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBkaCXVzLXdlc3QtMiJHMEUCIQCT6q5Y8KxUQuEa7O7wx%2BpnM7bzCjMA8VvIpdIfq1RUCwIgIehUtifqt6WMsWW8Iw%2BEOCRrjHt0yBT9tqylPDAIhFoqiAQI4v%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDMbR1P3O%2FvPZ72PkvyrcA%2B2IYLLD4XnxivwOZiHRmUsT9%2F3ONg6qPEWXSEeBd1bWPh6mjEN1aUeavdbon9%2BVHS8ga2m3QtKX57GiFaxqZVVnbsalLFAXZG9%2BJDHAV5goMcScKgQnJMZ%2FJLon14b4hkjecLWWNogm%2BuX1k2ffk%2FZ9o2nr19x22eY5%2F4ucP%2BwZeuVobhhOvNTr1gM%2B%2BMWKaE2gAMgK6ekC61I11NomqeD1fokpf0L73Xi6MGR53HkDMUONjHs3Dt1IEpAGxbS13Z3TcXANPuIcJHmjQImzOpOoW%2FaZ%2F9g5gZjZjeYtIOzahHma85L8BSd%2B5ENTrrq8tO%2BKG7Yu9pVHcL4SGvWTTonrmhiNaocuEgUKu%2FiH3dVjIKNpdE9%2FpAA0Ov%2Bgl0TCEildNGN1YRkS4hRAZFW4tY02K68toGGEWMh0IFOTJAgHwWFxYdEgqT1Qsj5ker84RyhRyudhY%2BSSBvDIleUt4HugBMfFuVVM6raxnVca2ruzn5g6wP6CI%2FhT1fUmdDnM8Dd60fhgFmxaR7S1uUdOSwXLeTpddbrWbJI4hFdy%2FEw%2BpWqi84cLaPDE73L0ybzgXAxF3tOaaTYC2TVjA9kenzj66BT15EWmtSj26yib66cgofBSv7fAwIgGJfUpMNqti88GOqUBPLtyrJEiYwgEaj8RYnn0qQTz6T%2B5FnIJKJgqCv27LuttHie21Y5HRi23b9cOavYgd0RlYCbEzDetAkIZZSHzmMfqBEOoX%2B6sbARNFUz%2FcKQUmlEHGx6FBTyVceISUGWXZZ%2BM1iK6f0oS%2BLRygxe2Ii%2FjsDH3VLGISmCOFWyw58E0h7QYYICa4KBQ4jpAjV6Dy2WY1ag6AHp91Cq1ewFkRxBnp85s&X-Amz-Signature=0ee571cb35b3b034b54588947526997c001416b4d602cfa32ea190ee384a8975&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

- **X：****原始数据点**（你想要标准化的那个值）。
- `***μ***`**(Mu)：** 原始数据集的**平均值（Mean/均值）**。
- ***σ***** (Sigma)：** 原始数据集的**标准差（Standard Deviation）**。
## Z 标准化的目的与重要性

### 实现数据的可比性 (Comparability)

这是 Z 标准化最核心的作用。

- 例如，比特币流通市值与已实现市值的**差值**，其原始数值可能高达数百亿美元。这个数值本身太大，无法直接与其他时间点的差值进行“感觉”上的比较。
- 但经过 Z 标准化后，不论原始差值是 100 亿美元还是 5000 亿美元，我们都将其转化为了“**标准差的倍数**”。一个 Z 分数 = 5 的数据点，在任何历史时期都代表着一个极度罕见、偏离历史平均水平 5 个标准差的“异常值”。
### 识别异常值 (Outlier Detection)

Z 分数能清晰地界定“正常”和“异常”的范围。

- **在正态分布（Normal Distribution）中**，大**约 68% 的数据点落在 Z 分数 -1 到 +1 之间**，**95% 的数据点落在 -2 到 +2 之间**，**99.7% 的数据点落在 -3 到 +3 之间**。
- 因此，**一个 Z 分数超过 ±3 的值**，通常被视为统计学上的**极端异常值**。
## 图解

![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/c9678d23-e296-817b-849e-0003ceb9774c/0370a42f-fa31-4c32-8d3c-2cb434ebb72a/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466Q57ORLSZ%2F20260418%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260418T032727Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBkaCXVzLXdlc3QtMiJHMEUCIQCT6q5Y8KxUQuEa7O7wx%2BpnM7bzCjMA8VvIpdIfq1RUCwIgIehUtifqt6WMsWW8Iw%2BEOCRrjHt0yBT9tqylPDAIhFoqiAQI4v%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDMbR1P3O%2FvPZ72PkvyrcA%2B2IYLLD4XnxivwOZiHRmUsT9%2F3ONg6qPEWXSEeBd1bWPh6mjEN1aUeavdbon9%2BVHS8ga2m3QtKX57GiFaxqZVVnbsalLFAXZG9%2BJDHAV5goMcScKgQnJMZ%2FJLon14b4hkjecLWWNogm%2BuX1k2ffk%2FZ9o2nr19x22eY5%2F4ucP%2BwZeuVobhhOvNTr1gM%2B%2BMWKaE2gAMgK6ekC61I11NomqeD1fokpf0L73Xi6MGR53HkDMUONjHs3Dt1IEpAGxbS13Z3TcXANPuIcJHmjQImzOpOoW%2FaZ%2F9g5gZjZjeYtIOzahHma85L8BSd%2B5ENTrrq8tO%2BKG7Yu9pVHcL4SGvWTTonrmhiNaocuEgUKu%2FiH3dVjIKNpdE9%2FpAA0Ov%2Bgl0TCEildNGN1YRkS4hRAZFW4tY02K68toGGEWMh0IFOTJAgHwWFxYdEgqT1Qsj5ker84RyhRyudhY%2BSSBvDIleUt4HugBMfFuVVM6raxnVca2ruzn5g6wP6CI%2FhT1fUmdDnM8Dd60fhgFmxaR7S1uUdOSwXLeTpddbrWbJI4hFdy%2FEw%2BpWqi84cLaPDE73L0ybzgXAxF3tOaaTYC2TVjA9kenzj66BT15EWmtSj26yib66cgofBSv7fAwIgGJfUpMNqti88GOqUBPLtyrJEiYwgEaj8RYnn0qQTz6T%2B5FnIJKJgqCv27LuttHie21Y5HRi23b9cOavYgd0RlYCbEzDetAkIZZSHzmMfqBEOoX%2B6sbARNFUz%2FcKQUmlEHGx6FBTyVceISUGWXZZ%2BM1iK6f0oS%2BLRygxe2Ii%2FjsDH3VLGISmCOFWyw58E0h7QYYICa4KBQ4jpAjV6Dy2WY1ag6AHp91Cq1ewFkRxBnp85s&X-Amz-Signature=1c282e52c057f33c8badcf703163934fdef0a18dd33f5b44b553e12f5da4b06b&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/c9678d23-e296-817b-849e-0003ceb9774c/1f587484-b928-4a2c-b042-80ef3c325b01/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466Q57ORLSZ%2F20260418%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260418T032727Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBkaCXVzLXdlc3QtMiJHMEUCIQCT6q5Y8KxUQuEa7O7wx%2BpnM7bzCjMA8VvIpdIfq1RUCwIgIehUtifqt6WMsWW8Iw%2BEOCRrjHt0yBT9tqylPDAIhFoqiAQI4v%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDMbR1P3O%2FvPZ72PkvyrcA%2B2IYLLD4XnxivwOZiHRmUsT9%2F3ONg6qPEWXSEeBd1bWPh6mjEN1aUeavdbon9%2BVHS8ga2m3QtKX57GiFaxqZVVnbsalLFAXZG9%2BJDHAV5goMcScKgQnJMZ%2FJLon14b4hkjecLWWNogm%2BuX1k2ffk%2FZ9o2nr19x22eY5%2F4ucP%2BwZeuVobhhOvNTr1gM%2B%2BMWKaE2gAMgK6ekC61I11NomqeD1fokpf0L73Xi6MGR53HkDMUONjHs3Dt1IEpAGxbS13Z3TcXANPuIcJHmjQImzOpOoW%2FaZ%2F9g5gZjZjeYtIOzahHma85L8BSd%2B5ENTrrq8tO%2BKG7Yu9pVHcL4SGvWTTonrmhiNaocuEgUKu%2FiH3dVjIKNpdE9%2FpAA0Ov%2Bgl0TCEildNGN1YRkS4hRAZFW4tY02K68toGGEWMh0IFOTJAgHwWFxYdEgqT1Qsj5ker84RyhRyudhY%2BSSBvDIleUt4HugBMfFuVVM6raxnVca2ruzn5g6wP6CI%2FhT1fUmdDnM8Dd60fhgFmxaR7S1uUdOSwXLeTpddbrWbJI4hFdy%2FEw%2BpWqi84cLaPDE73L0ybzgXAxF3tOaaTYC2TVjA9kenzj66BT15EWmtSj26yib66cgofBSv7fAwIgGJfUpMNqti88GOqUBPLtyrJEiYwgEaj8RYnn0qQTz6T%2B5FnIJKJgqCv27LuttHie21Y5HRi23b9cOavYgd0RlYCbEzDetAkIZZSHzmMfqBEOoX%2B6sbARNFUz%2FcKQUmlEHGx6FBTyVceISUGWXZZ%2BM1iK6f0oS%2BLRygxe2Ii%2FjsDH3VLGISmCOFWyw58E0h7QYYICa4KBQ4jpAjV6Dy2WY1ag6AHp91Cq1ewFkRxBnp85s&X-Amz-Signature=f68c17f880b4f050f132e682c329c96d026c054a649168d93f9118cd9de6236a&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/c9678d23-e296-817b-849e-0003ceb9774c/cb02fb7d-9e59-4a71-99bf-0db0556ffe7a/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466Q57ORLSZ%2F20260418%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260418T032727Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBkaCXVzLXdlc3QtMiJHMEUCIQCT6q5Y8KxUQuEa7O7wx%2BpnM7bzCjMA8VvIpdIfq1RUCwIgIehUtifqt6WMsWW8Iw%2BEOCRrjHt0yBT9tqylPDAIhFoqiAQI4v%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDMbR1P3O%2FvPZ72PkvyrcA%2B2IYLLD4XnxivwOZiHRmUsT9%2F3ONg6qPEWXSEeBd1bWPh6mjEN1aUeavdbon9%2BVHS8ga2m3QtKX57GiFaxqZVVnbsalLFAXZG9%2BJDHAV5goMcScKgQnJMZ%2FJLon14b4hkjecLWWNogm%2BuX1k2ffk%2FZ9o2nr19x22eY5%2F4ucP%2BwZeuVobhhOvNTr1gM%2B%2BMWKaE2gAMgK6ekC61I11NomqeD1fokpf0L73Xi6MGR53HkDMUONjHs3Dt1IEpAGxbS13Z3TcXANPuIcJHmjQImzOpOoW%2FaZ%2F9g5gZjZjeYtIOzahHma85L8BSd%2B5ENTrrq8tO%2BKG7Yu9pVHcL4SGvWTTonrmhiNaocuEgUKu%2FiH3dVjIKNpdE9%2FpAA0Ov%2Bgl0TCEildNGN1YRkS4hRAZFW4tY02K68toGGEWMh0IFOTJAgHwWFxYdEgqT1Qsj5ker84RyhRyudhY%2BSSBvDIleUt4HugBMfFuVVM6raxnVca2ruzn5g6wP6CI%2FhT1fUmdDnM8Dd60fhgFmxaR7S1uUdOSwXLeTpddbrWbJI4hFdy%2FEw%2BpWqi84cLaPDE73L0ybzgXAxF3tOaaTYC2TVjA9kenzj66BT15EWmtSj26yib66cgofBSv7fAwIgGJfUpMNqti88GOqUBPLtyrJEiYwgEaj8RYnn0qQTz6T%2B5FnIJKJgqCv27LuttHie21Y5HRi23b9cOavYgd0RlYCbEzDetAkIZZSHzmMfqBEOoX%2B6sbARNFUz%2FcKQUmlEHGx6FBTyVceISUGWXZZ%2BM1iK6f0oS%2BLRygxe2Ii%2FjsDH3VLGISmCOFWyw58E0h7QYYICa4KBQ4jpAjV6Dy2WY1ag6AHp91Cq1ewFkRxBnp85s&X-Amz-Signature=c2021ef18d7dc33bd1cf70a1f999c90bcd94785e90ccf77d5a59b0e278f9193f&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/c9678d23-e296-817b-849e-0003ceb9774c/22089e51-4b50-40bf-9a4c-79daef94d2b1/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4662URBUBOB%2F20260418%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260418T032733Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBkaCXVzLXdlc3QtMiJHMEUCIQC7RTdt7ro37zD4qtvCnHcw6AiU8XC5HFaxbjjSy8YctgIgWDb8WvE5c5diTbS9VFnro6R9saK8U2hFgxCRNvLWYUAqiAQI4v%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDM9CeCEGSIL9dOc4GyrcA4tWI5LEqL0g48IIkT9RzyAQB7VXAEy88uenTTc8SvxmCi9ogLMnO5bipwf4EQ6zaLn2HAgCymLoYmr3Z7vuY26Ji4atdhbHZopeq9nF9ljTB7XJdnuDE%2FQLXGhU9JBeJrRbheG79SyKv5vlHCmRPW1nv%2BsDzGQHoheBPw%2BeMNnGrBCIu6K1M18UdW6M96cNseURYoV1pBEn92UbiGxrAQ5eJtq4gjRTn0FJ30UIK46f5%2FF%2Bec6CZr01WCTGUxqZKgdzFHsxHeM4B6vnMFUEPMyomQNn9Gv2%2FRdLiWyI4WhgmWQ8D4XH51VgPuvoLBkzPyXN0HfMjZwmunknzqMkCV1M4Q5Yz62aHYlMAH4sATC4wG5dwAH0pqgxN9IXoJUrwqs%2FYVo8lIduVE0eVIstN4KrGtxz%2FHh3fOEl2H6uxHoZOooNZNNVjgunruBY%2ByRcAMTjUwG6%2BnG3inTI9LqAhwP%2BCo%2F1ECkDa8RAmeY9sPge11hRnb0axZd5j6bEXYQ2B4PMkpPefJ6lnrMAeC6mm20kfbmio74cyOMveBBQeTyK%2F4WmT7BepweIwETQby3JiTPRLSQ%2B3kFSZYJfofRzdfrhZvAVJKZ8JOOA71sacWvGuZ524ZQWStKbvLaKMMati88GOqUBrZOCcCanxUxTnuaoAz%2BKgIJcv6B2MNFV9hlqvN9VcfxW8h60P7%2BvbQeXAQjn3xugbPT6bnqwiTy8LpKn6DP7VtkqRlwo4Xscw6KrinO%2F8NQLVY%2F9%2B8F0J5jL4%2BRF%2B7WhLso8o7wybj5aUhCW65wT%2FcTdikE082i5BmTeilpRnUAOpDFsBfejhZ8%2BvDh7LABt45kB%2Ba4Nt%2FjzVgH1ngxavkJpubHA&X-Amz-Signature=f5c827a876728e78699e8950c13bd87d89dd773227563bedbd984dfc2cd35e73&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

历史上：

当价格跌至**2年均线（绿线）以下时，是一个抄底买入信号**，购买比特币会产生超额收益。

当价格超过**2年均线x5（红线）上时，是一个逃顶卖出信号**，出售比特币会获得较大收益。

![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/c9678d23-e296-817b-849e-0003ceb9774c/b09fccce-d26a-4d7a-9e10-eae461d1f76c/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466ZNLPSRJY%2F20260418%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260418T032733Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBkaCXVzLXdlc3QtMiJHMEUCIQCaH9rFDTfq4ry79ZvyV2KrRU5mXuVPFzZMBm13NoxWrgIgQJOAyoiH4hGtFfNTVUU9NCizLvsjjWwR4LS%2F1J41%2FK8qiAQI4v%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDIEjrPqNUdHM1qlcpircA0x1MhVTkYgiVNyIJgTJ3iZNhBKi%2BY9raaoCa8r6AfTDKVCctniqUCmM6liNSgJBI%2F1AXrLW6OylQHvq41dZygkqQqG1ltNM4aFo9mAIAZ9dgZs3bwkolyEB2VvStVyV%2F8XupgHs8fCnxPbz2itko9Xa4ZHqEAqT0BOeq%2FcMQ82zAFr4F4r4EzKf1r3WZxs6tnobhQjLL8%2BdIomptWYH1aZN1mfJOxhwsHWTJ%2FHwQbpKYAv%2BOFiS%2B5XjF%2FdHYcMoa%2BZNwXidMeEaiY44HA6w1DQ49WHnRxw9PAlpf9EQ%2BwlIMLgzkR3Q4YI8O47XkkofudJ%2Bdp3JZeDOwCMuL41n6OHrp3OlipXG8OjxIv%2Beer5Z0rHwnyekoAiRiBeYWh%2FxFuZxrYyzlamcoM63QdNrtqLdruPp0PO5R8PmC2P4NzwiruBWB7VG4%2BEB4BMpqfDnq%2BAmaNkyaC8iN0nCYISXXNCf87T%2F0et%2BBgSVM%2Fdl0Gi53qmeCNT%2FQixumPaoxXpwT9Zlg%2FMetjqHXylAHmBd%2BC6SEsP27w%2BPATaDGpjAAXwjzOoFlk3fnG%2FKpaLnts9C3mmE5QZixdziOWjdT8UZqeixtzcPt7WIsxR7qR6T1IW%2BRYsypQ%2FG9jTc0dMNMKCti88GOqUBq53ovZnbHw%2FCpSceY%2FITjj3dK%2BUW%2BAy5r5jD7B0jiOYNEiKhEvZNhQj%2Fg0lcZQwDQ7myxA%2F%2FR4bbbv6AeZe7Yq3lUcB6xXfFMbgxIhtmWuk%2Fm3PpmxRJk7TTa15LuAux0jSLUkF%2FJIcz7RISPHPiQOeiOJnKHM%2BMVBf%2F1lStb1HBRtE5sPROYlFjo%2BJLBS6wzdI1OGi4vb%2F6W5SrO4YQOaDOX59O&X-Amz-Signature=ac53c63da7257f7039ad4d0e06380a842fa5a55ff42401fef6a23961c6877198&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

- 彩虹图是比特币的**长期估值工具**。它使用**对数增长曲线**来预测比特币潜在的未来价格方向。
- 它在对数增长曲线通道的顶部覆盖彩虹色带，试图在价格通过它时突出每个彩虹色阶段的市场情绪。因此突出潜在的买卖机会。
- 迄今为止，**比特币价格继续保持在对数增长通道的彩虹色带内**。
**如何解读彩虹图**

- 由于比特币仍然是一种相对年轻的资产类别，其价格走势波动很大。尽管在宏观时间线上比特币正在被采用，我们可以从总体价格上涨中看到，但它确实经历了市场周期。在这些市场周期中，比特币的价格**可以抛物线式上涨，也可以迅速下跌**。它还具有非常高的每日波动率，投资者需要注意。
- BTC 彩虹图突出显示了 BTC 价格在这些周期中的位置，并提供了有关投资者策略的观点。如本文前面所述，此图表及其图例标签仅供娱乐，不构成投资建议。
- 彩虹图上方较暖的颜色显示市场何时可能过热。历史证明，这些时期是战略投资者开始获利的好时机。
- 当今天的价格下跌至较冷的颜色时，整体市场情绪通常会低迷，许多投资者对比特币不感兴趣。彩虹图强调，这些时期通常是战略投资者增持更多比特币的绝佳时机。
![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/c9678d23-e296-817b-849e-0003ceb9774c/f0214f0a-6db1-41fb-bffd-88cde4689e05/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466YO4DK2N6%2F20260418%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260418T032734Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBkaCXVzLXdlc3QtMiJIMEYCIQDGpGhotpMlylV3hTridnhuC4uRJj27YGz0VLWH%2FCwgbQIhAJWM8rkpwsdq%2FfVRUEvilP%2FfRUGb%2FF3EQkMsrANiL3H3KogECOL%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNjM3NDIzMTgzODA1Igwgjk9mdLAi0GtuPfgq3ANjuI7cFXkVSJbVvq61A4S27L25uEfKqOA4JuARIM%2BEeQSfKssODRRAX6q2itVSwDJlh8Lk9XFQW2LXCzK%2BiQ1k9Yrtkt95rA9JrWL%2BJqFgXLp7x9BC6NVFlJvvnstXDYm2yVmAuVzWrrOCmeoeMvPAFCA301WpIyNGmKOdIEeGs1Xw2Hr3qMilInYF1nAybvMR0ouZxTAW3tAZpXwNeOk%2Fy%2Bu2RntTjOeB9r6mB7YbewvFsTQ%2Flz47qZxSB5rcti4WBdjUGUWzu%2Fl3fIUakAn6q4kwCLwulGuZTJXpZ9ty5HkViZQHr1PP8cf4fKJK6qVTD1PyLIr9Yv%2BMxlhvjkSLKyMHQOrgG3oDOiTUosAtiMBaRXE5b11HPwx22DR7QhHiaLFt9ecul7rZvQNwchCyo6cpTtLNVfJzOqE1565XuBlW1P9QZ2hMaGb8nR6wG5qFXgsct%2B1XVqJoDIk8trqG56glh0ZZD11jblXlCMKfbHV2FA9fQjJyCcZ2SOPWjsrkZPRqXkard3Nu%2BBMVx7Xmt1A5Jszvwo20Sr0B0oP5vhePT5B%2Bqp8IfhV%2B6AehoNE%2FaqfXQeOjcquVA%2BPNcUAGqtp932%2FMf4d7LbzhTJNtsmE4JY565YrNZjMJYTDhrYvPBjqkAYVN%2BplAyx5W5nK485kRKA8sjFRNYyd7rCba7kaMBvdjasW2YSKNvevWIQVlTHKCCsgMJR0%2BjD05uHk7vv8PTK9qCN6J1WL5kwi1An2nniiLWSGyKpxRyC0gW03k4t%2B%2BJoXtaIqx6MmNYNUm4MJ0NUu%2FoylGi3vTsJb9kn7KAzq6EtWwVWpYJIjC%2FdDO9fFc3fCrcqcanmjn0kkK0b9Fp45I8%2BbZ&X-Amz-Signature=b2485c16c1804232da391ac3eaefb151d69f20ba31ceb69837da0cc0148140b6&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

- 净未实现利润/亏损 (NUPL)，也称为**相对未实现利润/亏损**，是一个基于两个关键指标的比特币指标：
- **市场价值**：比特币**当前价格 × 流通供应量**——类似于股票市值（股价 × 流通股数）。
- **已实现价值**：每个比特币在**最后一次钱包到钱包转账时的平均价格**，**乘以流通中的总币数**。
- **从市场价值中减去已实现价值，得到未实现利润/亏损**，它**显示了比特币持有者的账面收益或损失**。**将其除以市场价值，你就得到了 NUPL **—— 一个衡量投资者情绪的顶级指标。
![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/c9678d23-e296-817b-849e-0003ceb9774c/710e4144-30b0-4cc0-a7df-48b50d5b9f4f/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466YO4DK2N6%2F20260418%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260418T032734Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBkaCXVzLXdlc3QtMiJIMEYCIQDGpGhotpMlylV3hTridnhuC4uRJj27YGz0VLWH%2FCwgbQIhAJWM8rkpwsdq%2FfVRUEvilP%2FfRUGb%2FF3EQkMsrANiL3H3KogECOL%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNjM3NDIzMTgzODA1Igwgjk9mdLAi0GtuPfgq3ANjuI7cFXkVSJbVvq61A4S27L25uEfKqOA4JuARIM%2BEeQSfKssODRRAX6q2itVSwDJlh8Lk9XFQW2LXCzK%2BiQ1k9Yrtkt95rA9JrWL%2BJqFgXLp7x9BC6NVFlJvvnstXDYm2yVmAuVzWrrOCmeoeMvPAFCA301WpIyNGmKOdIEeGs1Xw2Hr3qMilInYF1nAybvMR0ouZxTAW3tAZpXwNeOk%2Fy%2Bu2RntTjOeB9r6mB7YbewvFsTQ%2Flz47qZxSB5rcti4WBdjUGUWzu%2Fl3fIUakAn6q4kwCLwulGuZTJXpZ9ty5HkViZQHr1PP8cf4fKJK6qVTD1PyLIr9Yv%2BMxlhvjkSLKyMHQOrgG3oDOiTUosAtiMBaRXE5b11HPwx22DR7QhHiaLFt9ecul7rZvQNwchCyo6cpTtLNVfJzOqE1565XuBlW1P9QZ2hMaGb8nR6wG5qFXgsct%2B1XVqJoDIk8trqG56glh0ZZD11jblXlCMKfbHV2FA9fQjJyCcZ2SOPWjsrkZPRqXkard3Nu%2BBMVx7Xmt1A5Jszvwo20Sr0B0oP5vhePT5B%2Bqp8IfhV%2B6AehoNE%2FaqfXQeOjcquVA%2BPNcUAGqtp932%2FMf4d7LbzhTJNtsmE4JY565YrNZjMJYTDhrYvPBjqkAYVN%2BplAyx5W5nK485kRKA8sjFRNYyd7rCba7kaMBvdjasW2YSKNvevWIQVlTHKCCsgMJR0%2BjD05uHk7vv8PTK9qCN6J1WL5kwi1An2nniiLWSGyKpxRyC0gW03k4t%2B%2BJoXtaIqx6MmNYNUm4MJ0NUu%2FoylGi3vTsJb9kn7KAzq6EtWwVWpYJIjC%2FdDO9fFc3fCrcqcanmjn0kkK0b9Fp45I8%2BbZ&X-Amz-Signature=e028a98cd361b4d2351e384192820b2fb62d5334d87c8902ece2bfec7b8320a1&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

**为什么 NUPL 是一个游戏规则改变者**

- **NUPL 跟踪市值增长与获利回吐之间的平衡**。当市值超过利润（红带）时，它标志着市场过热——通常由贪婪推动——使其成为战略投资者抛售的主要窗口。与此同时，**较低的 NUPL 水平可能表示恐惧或低估，暗示买入机会**。
**如何使用 NUPL 图表**

- 高 NUPL（**>50%**）：**贪婪驱动的峰值**；**获利回吐的理想选择**。
- 低 NUPL（**<0%**）：**恐惧或投降**；**潜在的底部**。
- 这些见解使长期投资者能够精确地安排交易时间。
**使用 NUPL 预测比特币价格**

- NUPL 使用链上数据捕捉市场情绪以预测比特币的高点和低点。**高 NUPL 通常先于顶部，而低 NUPL 标志着底部**——为预测价格趋势提供了可靠的优势。
- 使用 NUPL 的数据驱动方法掌握比特币投资以把握市场时机。
![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/c9678d23-e296-817b-849e-0003ceb9774c/563873c4-b056-4874-aa33-54ef70141ea2/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466TC63EMIN%2F20260418%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260418T032738Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBkaCXVzLXdlc3QtMiJHMEUCIQDKLpfRrDWfwIwS6v0pJPS6z4j%2BDdFxg00idnrET03EMwIgWIJdCThUfqOpH%2F%2BGbhatsXvzsxrN85%2FIjSJ%2B7tEfWXMqiAQI4v%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDHIjOyPRec3s%2B%2BNfzyrcA0%2BdRDOG0Vj%2Bv1q3WzneEqSILwwtiLpqrC5pNnMhOqIdO4756k%2BRSAX9KAjk2xrIBHr3bn2zU02kyAqE0Y5jg0FAI7cbo0mQvSox21TROjRiURD1NkRhYNacey5hE0tvaHMZ6IseiBaFwtyjl%2BEnzQeJxilZclw60AfZmW%2B4GXktO1bMUhjJaPvpzHKv4ZKczdEOyrZRb5iMk8S4TkW72ZOfOaR8q9jfp7J6oJX8epWu5NTOQmkxct6Lb%2BnagmqzhED5yqxIUbvDLjTqJ5VuEO7VfAylV5H8fHjAvIcLmd%2B6jSOBqB32lhQFk9zNhozcb641CHkD2EUq9AI5l%2FgY08I2Lu3TzEIdazwrJ85WJiH4VFyu2Rl9dZFv%2F8KZiuiQB6oSF1MwGrklSzHxklTDoTbvIRJN7pjXZVNilOU8sdNeySC9Cy5P4Aff%2BpvptxS8cn6DeAiJHKvc2NYuNPpEGDjkkr%2BmDmQOvdw5XabD2dJPwrgMHEO5i8d3IiGolvq9dbDtk80wW5pwGg%2B0vmlNnJg3LPTnytRFrfj1RguVJDSHipCeysRj4iIs%2BhrK0HxBWJTxgPndYpVT9IsfxAJI3K4Du3c88wRwr%2BGaIiN9on7e0hTyFuUVdE%2F2IAwuMKeui88GOqUBSheiTY%2BcyK3G4riaQFVDQduuNRrgX%2B6WH7xLbBufDJ2vWs7rmkKN0QP0s%2B2HeB3o616sJSX9u1%2BL%2FxfHb6ijwuNvANQ3njIm07d1PAjtrqyfWPU%2Ba20wzvJY7hE7BAYR11EBjFq1F%2B1T0JTL%2F%2BBjvKAMArdJO4azR0GEvqgmlu%2FaVCeQA%2Btr9HgjUsKKdxU%2Fj5AzaZ3X28oevCs1H6h7v3pg5XIV&X-Amz-Signature=9ce8ffdf90777443296e3e998fee02f7946b0462dae45ae1581d5da2eab6fdd1&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/c9678d23-e296-817b-849e-0003ceb9774c/1e81fe39-8b3f-4657-a239-71cb794c86a0/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466TC63EMIN%2F20260418%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260418T032738Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBkaCXVzLXdlc3QtMiJHMEUCIQDKLpfRrDWfwIwS6v0pJPS6z4j%2BDdFxg00idnrET03EMwIgWIJdCThUfqOpH%2F%2BGbhatsXvzsxrN85%2FIjSJ%2B7tEfWXMqiAQI4v%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDHIjOyPRec3s%2B%2BNfzyrcA0%2BdRDOG0Vj%2Bv1q3WzneEqSILwwtiLpqrC5pNnMhOqIdO4756k%2BRSAX9KAjk2xrIBHr3bn2zU02kyAqE0Y5jg0FAI7cbo0mQvSox21TROjRiURD1NkRhYNacey5hE0tvaHMZ6IseiBaFwtyjl%2BEnzQeJxilZclw60AfZmW%2B4GXktO1bMUhjJaPvpzHKv4ZKczdEOyrZRb5iMk8S4TkW72ZOfOaR8q9jfp7J6oJX8epWu5NTOQmkxct6Lb%2BnagmqzhED5yqxIUbvDLjTqJ5VuEO7VfAylV5H8fHjAvIcLmd%2B6jSOBqB32lhQFk9zNhozcb641CHkD2EUq9AI5l%2FgY08I2Lu3TzEIdazwrJ85WJiH4VFyu2Rl9dZFv%2F8KZiuiQB6oSF1MwGrklSzHxklTDoTbvIRJN7pjXZVNilOU8sdNeySC9Cy5P4Aff%2BpvptxS8cn6DeAiJHKvc2NYuNPpEGDjkkr%2BmDmQOvdw5XabD2dJPwrgMHEO5i8d3IiGolvq9dbDtk80wW5pwGg%2B0vmlNnJg3LPTnytRFrfj1RguVJDSHipCeysRj4iIs%2BhrK0HxBWJTxgPndYpVT9IsfxAJI3K4Du3c88wRwr%2BGaIiN9on7e0hTyFuUVdE%2F2IAwuMKeui88GOqUBSheiTY%2BcyK3G4riaQFVDQduuNRrgX%2B6WH7xLbBufDJ2vWs7rmkKN0QP0s%2B2HeB3o616sJSX9u1%2BL%2FxfHb6ijwuNvANQ3njIm07d1PAjtrqyfWPU%2Ba20wzvJY7hE7BAYR11EBjFq1F%2B1T0JTL%2F%2BBjvKAMArdJO4azR0GEvqgmlu%2FaVCeQA%2Btr9HgjUsKKdxU%2Fj5AzaZ3X28oevCs1H6h7v3pg5XIV&X-Amz-Signature=cb6717fabc8e853cdba95d37954bb11554db230fc85d4444057de7a49973624e&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

## **比特币长期持有者平均持仓成本**

![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/c9678d23-e296-817b-849e-0003ceb9774c/1576faf9-9c24-4538-86fc-153a25c7cbe8/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB46674QTXFPI%2F20260418%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260418T032738Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBkaCXVzLXdlc3QtMiJGMEQCIBzmMV%2FeKWWeoLrf9KdzFgFF3eFPU2kRXjO0UOWd6SPPAiB0ICennBDm%2FFwk9gKt2EQYSbnDXH7nL%2Bjj%2BrX6yB0q5yqIBAji%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDYzNzQyMzE4MzgwNSIMR%2FB8qonDnWQivjulKtwDNgaGY3rN3U0qRjE4hIph2T8PgU4IMyeZYaq2OTKy62OXx2MCd9atBeE2bScPI2Nb4OmWLPT%2BhSRUpNau7AvY6CTK%2BDIfZLYyME71djgP4kXhrEe0ZZ0HmLy%2BYs%2BqQ1%2FAFc9yDqzmSN1I%2BKn4D7v0sY8Is8aL%2FLM1TrXCJkIF%2B8pQ9A6%2BAjCRUEdQHv9%2FbLRmbKG%2BYYzGk63rdyoUfrtv4iwCDcwmPFMcX7KviZ2arczSToKIhK5S9aLJhlNXkULZZu099uISd7TDEOzTY6FofpTdjZt4%2FiCb5oq60gMqDEYyoPaktUw%2FlxjvzI7NBF0fkSKQY05r%2Bz79v8Xt8W3gVwcxivv6CEi%2F4XjW8diQSRoePzFkTqlFOX9Y9w5JFGb9l0mwWK%2FRJNbZcLbN48zMd74eOkCD1Pab7ARHjedGwNRpFKSviz1WZGFwPxntFYi3p7cYbG%2FoLFFTDwEPghtF5PEnywJdzV2IquFgvTLvo7FoVLgP1H%2BLzo8i%2FtD4e2IWcWSlSZRs0C23BWrUIPckGToR5lurSmunLy5%2FZhHxnI7J29Z0yOMugSXmf8ivfaWNRr2I82CWEawfDWo8dUvQxxEXdy%2BUAQ3LS2xEnN8u2LmApe%2F1WEUEAurM9Xcw%2F66LzwY6pgHDVjdinZVlnu%2BpldD3kuk6DqvK8yJZxlexHJYCxXsBEw65PC7YtbghnGpIRLVUAZxDdrjUSVgzmZxIR5efJMen65WxIEIobvzcLDeNAhzYYKH5lhREuhBAr3XFOVEGuEIXxJWi0CY3vi2rDGl34bbsKKCrO%2Bd3qmWTyXyWJkc1fSODXjfVUJQCzFUA6bCVX4nN0x%2FIIbAWHOsXbOu%2BJkCXAoHpFAor&X-Amz-Signature=6d85218ec54251a8aac125454a615b25eeb46b7234e6dfd86601fb56c0631154&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

## **比特币短期持有者平均持仓成本**

![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/c9678d23-e296-817b-849e-0003ceb9774c/c2875019-345d-4658-bb65-dbd370c16f8e/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB46674QTXFPI%2F20260418%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260418T032738Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBkaCXVzLXdlc3QtMiJGMEQCIBzmMV%2FeKWWeoLrf9KdzFgFF3eFPU2kRXjO0UOWd6SPPAiB0ICennBDm%2FFwk9gKt2EQYSbnDXH7nL%2Bjj%2BrX6yB0q5yqIBAji%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDYzNzQyMzE4MzgwNSIMR%2FB8qonDnWQivjulKtwDNgaGY3rN3U0qRjE4hIph2T8PgU4IMyeZYaq2OTKy62OXx2MCd9atBeE2bScPI2Nb4OmWLPT%2BhSRUpNau7AvY6CTK%2BDIfZLYyME71djgP4kXhrEe0ZZ0HmLy%2BYs%2BqQ1%2FAFc9yDqzmSN1I%2BKn4D7v0sY8Is8aL%2FLM1TrXCJkIF%2B8pQ9A6%2BAjCRUEdQHv9%2FbLRmbKG%2BYYzGk63rdyoUfrtv4iwCDcwmPFMcX7KviZ2arczSToKIhK5S9aLJhlNXkULZZu099uISd7TDEOzTY6FofpTdjZt4%2FiCb5oq60gMqDEYyoPaktUw%2FlxjvzI7NBF0fkSKQY05r%2Bz79v8Xt8W3gVwcxivv6CEi%2F4XjW8diQSRoePzFkTqlFOX9Y9w5JFGb9l0mwWK%2FRJNbZcLbN48zMd74eOkCD1Pab7ARHjedGwNRpFKSviz1WZGFwPxntFYi3p7cYbG%2FoLFFTDwEPghtF5PEnywJdzV2IquFgvTLvo7FoVLgP1H%2BLzo8i%2FtD4e2IWcWSlSZRs0C23BWrUIPckGToR5lurSmunLy5%2FZhHxnI7J29Z0yOMugSXmf8ivfaWNRr2I82CWEawfDWo8dUvQxxEXdy%2BUAQ3LS2xEnN8u2LmApe%2F1WEUEAurM9Xcw%2F66LzwY6pgHDVjdinZVlnu%2BpldD3kuk6DqvK8yJZxlexHJYCxXsBEw65PC7YtbghnGpIRLVUAZxDdrjUSVgzmZxIR5efJMen65WxIEIobvzcLDeNAhzYYKH5lhREuhBAr3XFOVEGuEIXxJWi0CY3vi2rDGl34bbsKKCrO%2Bd3qmWTyXyWJkc1fSODXjfVUJQCzFUA6bCVX4nN0x%2FIIbAWHOsXbOu%2BJkCXAoHpFAor&X-Amz-Signature=1eb85e5ad9894179bcb53f1b1d776696106717c64814cae4fe17d657c697d389&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

## **比特币长期持有者持币变化量**

![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/c9678d23-e296-817b-849e-0003ceb9774c/622bda08-40d6-4826-84c8-4180aefc9832/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB46674QTXFPI%2F20260418%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260418T032738Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBkaCXVzLXdlc3QtMiJGMEQCIBzmMV%2FeKWWeoLrf9KdzFgFF3eFPU2kRXjO0UOWd6SPPAiB0ICennBDm%2FFwk9gKt2EQYSbnDXH7nL%2Bjj%2BrX6yB0q5yqIBAji%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDYzNzQyMzE4MzgwNSIMR%2FB8qonDnWQivjulKtwDNgaGY3rN3U0qRjE4hIph2T8PgU4IMyeZYaq2OTKy62OXx2MCd9atBeE2bScPI2Nb4OmWLPT%2BhSRUpNau7AvY6CTK%2BDIfZLYyME71djgP4kXhrEe0ZZ0HmLy%2BYs%2BqQ1%2FAFc9yDqzmSN1I%2BKn4D7v0sY8Is8aL%2FLM1TrXCJkIF%2B8pQ9A6%2BAjCRUEdQHv9%2FbLRmbKG%2BYYzGk63rdyoUfrtv4iwCDcwmPFMcX7KviZ2arczSToKIhK5S9aLJhlNXkULZZu099uISd7TDEOzTY6FofpTdjZt4%2FiCb5oq60gMqDEYyoPaktUw%2FlxjvzI7NBF0fkSKQY05r%2Bz79v8Xt8W3gVwcxivv6CEi%2F4XjW8diQSRoePzFkTqlFOX9Y9w5JFGb9l0mwWK%2FRJNbZcLbN48zMd74eOkCD1Pab7ARHjedGwNRpFKSviz1WZGFwPxntFYi3p7cYbG%2FoLFFTDwEPghtF5PEnywJdzV2IquFgvTLvo7FoVLgP1H%2BLzo8i%2FtD4e2IWcWSlSZRs0C23BWrUIPckGToR5lurSmunLy5%2FZhHxnI7J29Z0yOMugSXmf8ivfaWNRr2I82CWEawfDWo8dUvQxxEXdy%2BUAQ3LS2xEnN8u2LmApe%2F1WEUEAurM9Xcw%2F66LzwY6pgHDVjdinZVlnu%2BpldD3kuk6DqvK8yJZxlexHJYCxXsBEw65PC7YtbghnGpIRLVUAZxDdrjUSVgzmZxIR5efJMen65WxIEIobvzcLDeNAhzYYKH5lhREuhBAr3XFOVEGuEIXxJWi0CY3vi2rDGl34bbsKKCrO%2Bd3qmWTyXyWJkc1fSODXjfVUJQCzFUA6bCVX4nN0x%2FIIbAWHOsXbOu%2BJkCXAoHpFAor&X-Amz-Signature=094f3fdd16f99cb8842e69dcff92f366ae9bab4a94455edf7b9fdc49056edbe7&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

## **比特币短期持有者持币变化量**

![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/c9678d23-e296-817b-849e-0003ceb9774c/76687faa-bab2-438e-9847-7ed38858500c/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB46674QTXFPI%2F20260418%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260418T032738Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBkaCXVzLXdlc3QtMiJGMEQCIBzmMV%2FeKWWeoLrf9KdzFgFF3eFPU2kRXjO0UOWd6SPPAiB0ICennBDm%2FFwk9gKt2EQYSbnDXH7nL%2Bjj%2BrX6yB0q5yqIBAji%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDYzNzQyMzE4MzgwNSIMR%2FB8qonDnWQivjulKtwDNgaGY3rN3U0qRjE4hIph2T8PgU4IMyeZYaq2OTKy62OXx2MCd9atBeE2bScPI2Nb4OmWLPT%2BhSRUpNau7AvY6CTK%2BDIfZLYyME71djgP4kXhrEe0ZZ0HmLy%2BYs%2BqQ1%2FAFc9yDqzmSN1I%2BKn4D7v0sY8Is8aL%2FLM1TrXCJkIF%2B8pQ9A6%2BAjCRUEdQHv9%2FbLRmbKG%2BYYzGk63rdyoUfrtv4iwCDcwmPFMcX7KviZ2arczSToKIhK5S9aLJhlNXkULZZu099uISd7TDEOzTY6FofpTdjZt4%2FiCb5oq60gMqDEYyoPaktUw%2FlxjvzI7NBF0fkSKQY05r%2Bz79v8Xt8W3gVwcxivv6CEi%2F4XjW8diQSRoePzFkTqlFOX9Y9w5JFGb9l0mwWK%2FRJNbZcLbN48zMd74eOkCD1Pab7ARHjedGwNRpFKSviz1WZGFwPxntFYi3p7cYbG%2FoLFFTDwEPghtF5PEnywJdzV2IquFgvTLvo7FoVLgP1H%2BLzo8i%2FtD4e2IWcWSlSZRs0C23BWrUIPckGToR5lurSmunLy5%2FZhHxnI7J29Z0yOMugSXmf8ivfaWNRr2I82CWEawfDWo8dUvQxxEXdy%2BUAQ3LS2xEnN8u2LmApe%2F1WEUEAurM9Xcw%2F66LzwY6pgHDVjdinZVlnu%2BpldD3kuk6DqvK8yJZxlexHJYCxXsBEw65PC7YtbghnGpIRLVUAZxDdrjUSVgzmZxIR5efJMen65WxIEIobvzcLDeNAhzYYKH5lhREuhBAr3XFOVEGuEIXxJWi0CY3vi2rDGl34bbsKKCrO%2Bd3qmWTyXyWJkc1fSODXjfVUJQCzFUA6bCVX4nN0x%2FIIbAWHOsXbOu%2BJkCXAoHpFAor&X-Amz-Signature=3d1c7e211949112c57aad994d07afc57d384062d87d447b0df012160cbf23f0f&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

> 长时间处于低波动率情况时，很可能要酝酿一个大的。

![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/c9678d23-e296-817b-849e-0003ceb9774c/d8d1547b-97b1-4611-a425-63c5e6b10906/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4666MW5WN6M%2F20260418%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260418T032739Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBkaCXVzLXdlc3QtMiJIMEYCIQDsBbZOodlekZ3V%2FeOuivU%2BeiQ3h4ynTvk%2FkoaX15%2Bn2gIhAJAwdPtm2%2Fqyn6Hd%2BXcTntqz1AZUNJg5yOMQmFgftiMQKogECOL%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNjM3NDIzMTgzODA1IgyjR2zrJLTDgBJpxS4q3APsx7EExipX5TST7qsWXCHeENH0b608AQplze2WN6ToloAz3%2BJoYLuON%2FNaYwUuPzbzCsphoTlKVqbKS97oinqnrR8GmAByPRauelsapPhJNFpYaSiAjBDB6ZPsLUKlGN4mYwqcAeVYhSBofETzM09uWk0ovBsH61R5A6K8E1sCdXTxyX0R0MKYxZtM99WGrToo6nYVZI0chVezkTi4zZe2rDlZ7OCtDoAdPmjO6AMvVsQlSvgJ0PQ%2FfLQnWwAP3SIO37g8KRhzV%2FZklKtNW1B45Xgz5wAshWqxBpX1%2F4%2F79QAukc%2FiIsOUxeNf52XDjQzNJRKpZVEZB9qaw8WxVZdRHAgWgHm4pSqQiEcUezd7jxo0NJNCtMnS6ExeYP4sY9TvrgHmROaxvqfMBQU0gWa7ePePeKkxnja4Olf9UJB9FCE21o4Sk6rVBg%2FuAm%2FpivKGNDsxAhcZ16u35g8LOVixk5AX5S2Lulit6saDlMdEORUXA9bjy8tu3IfaQqfdz%2BO7eXwe8d0DdBh4MzpFZbT19vWvw2jyl16BL8ZcAdmwEHYwMD0fg4JmYD0ZeTgtI2UGZ8ZrVrL41F8GwB5KY2CIhpoPmmzqcDkQxTVojkkMHaH7FfwZDk%2BKX3UWrjDhrYvPBjqkAZ5UK6hSEQhQirPeIw%2FiqZvSitSVfZZSBP4QdhzyYAUtqJzLEbhfAUxtmMawgs85889N9d6vsrj6Rf1x16LXgX2FrW1EUa2D1oUvvDVxOllekDii1b3zfa%2BPE1WW3Bdye7a7oieXljY%2B%2Fmcyk74fWWekOZLpFKZ6WpjdV6Vtm9Ws7FrdWkX%2BQtmVubLDxAJodEAKuoHiiigTjeUnZURyGG2GU1Rx&X-Amz-Signature=9dc5423b83100dff03697e5d906d85ab5f0383ba756831cf9b78a120f9924b18&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

[https://www.deribit.com/statistics/BTC/volatility-index](https://www.deribit.com/statistics/BTC/volatility-index)

## 1. 定义（一句话记死）

IV = **市场用当前期权价格反推出来的**「对未来波动的预期年化百分比」

它是期权真正的「定价之王」。

## 2. 核心数值区间（BTC，2025年实时标准）

[table - see children]

| 级别 | IV 值 | 市场含义 | 操作建议 |
| 极低 | < 40% | 超级无聊 | 买波动率（Straddle） |
| 正常 | 45%~70% | 日常 | 中性 |
| 偏高 | 70%~90% | 有事件预期 | 谨慎买入 |
| 极高 | 90%~120% | 紧张 | 卖波动率首选 |
| 核爆 | >120% | 恐慌/黑天鹅 | 果断卖IV |
## 3. IV 对期权价格的致命影响（四象限）

[table - see children]

|  | IV 上升 | IV 下降 |
| 买方（长Vega） | 大赚 | 大亏（Vega杀） |
| 卖方（短Vega） | 大亏 | 大赚 |
## 4. 三大散户死法（全与IV有关）

1. 高IV追买 Call/Put → 事件结束IV崩盘 → 方向对了也巨亏
1. 低 IV 买 Straddle → 行情没来，Theta+IV继续掉 → 慢慢磨死
1. 只看行权价和到期日，从不看IV → 永远买在最贵的时候
## 5. IV vs 波动率指数（VIX类）终极对比

[table - see children]

| 项目 | 隐含波动率 IV | 波动率指数（DVOL/BVOL/VIX） |
| 数量 | 每张期权一个IV（几千个） | 全市场只有一个数字 |
| 是否可直接交易 | 不可 | 可直接买卖期货/永续 |
| 代表含义 | 单张期权的预期波动 | 整个市场30天预期波动 |
| 2025代表产品 | Deribit每张期权右上角的% | Deribit DVOL指数 |
| 极端值 | 单张可超300% | 指数最高189（2022.11） |
| 用途 | 判断单张期权贵不贵 | 直接赌波动率涨跌、对冲Vega |
## 6. 专业玩家三句口诀

- IV Rank < 20% → 全仓买波动率
- IV Rank > 80% → 全仓卖波动率
- 大事件后24小时 → IV必崩，提前埋伏卖方
## 7. 2025.11.29 实时参考（Deribit）

- 近月平值IV：68~74%
- 12月26日期权IV：71~76%
- DVOL指数（30天）：71.8
记住：

在期权世界里，**现货价格是表象，IV 才是真正的价格**。

看不懂 IV，就等于裸奔。

[https://cryptoquant.com/analytics/query/667c35e65cf1f8126228dfd4?v=667c4798a3f5b8210d4df5db](https://cryptoquant.com/analytics/query/667c35e65cf1f8126228dfd4?v=667c4798a3f5b8210d4df5db)

按持币数量分层后，不同层用户的持币变化。

![image](https://prod-files-secure.s3.us-west-2.amazonaws.com/c9678d23-e296-817b-849e-0003ceb9774c/04d0216b-4d6b-48fb-a52b-89362d859422/image.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4665GVO4E7M%2F20260418%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20260418T032743Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBkaCXVzLXdlc3QtMiJHMEUCIQCOt7m39dQ6C94a2ypgZuJQBcFlAKW%2B5giIRlUc5mFV0QIgPVcqIjybKnVrPari4ZDjp2O8ODHGpKmyvyxT5aBaPTYqiAQI4v%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDFjAqFABezM1gjEZNircAw9j9aCc%2BLuPRojS19G7uNEc8lEvKc4UZCPtrspJuHWliWukPEaSF5fAblRpX%2FWw%2BaLt0ZAhGYGf1p742mgrwlTCz3oCiTvWqLHuMJqYMX2I%2FWRPZLi2fDeaA9I0HZSPqEdjOP11ffLEe7u8%2FA%2BU9DseK2dtvMwTjdBn4bN2bLBQBzsV%2BidQNOAONU7iTamsSINXOK4pTQkXgyGD7%2FEtWRHU6tvygKaVYtgKmTOEpURt7uRvT4ib7u8HS1IGr0HxdEjQuRWNTHa4ImayGVjQZ3CaAvLwtqukmgkwL5bhLBKA9No7EWQA4aB4Mca1EODAJ7CuMvd%2Bfqv54QM0Ij5IvDj9WAvNpE6lNrTYXmX4P9kPVDuYuvTTw2JbUQm5zPUa56PPrui2zzTB5%2BB3zmxp3qnn4f9972tWQeF7kYtDiHSoH52SqnmqJFdB9bS5iEEn%2F4ZP6F8FJsGAs5AL%2BH2SF4FIgaP7KXXTziHiFhP6TPVngPWRQSgrMtRrwM0NlAb5D8D8%2Fu0PaQPy3zN2wCPBDokaopFnPk6aHs7z9Ikqc5%2FPS4%2Bbi54bWABvm3BDWI04y7Bji3wt66BdBqtm6QadvrQAALuSQswkfu9RdEnubgieIO6uzFq6f3dAnU3XMLOti88GOqUB6P3vBkCrpv%2B1FU37uSWoOwAbw6OikxnRCToZfHbazfuXFeeoAOe8aJG%2FQ%2ByW3vkDKgbA8DmK2%2FLdUl1tFb7xrmzya24xZmH6aaDpKMEzsGtbsMHuVmXDezIxE8QcQRnS2YIIQIgS8cId1lAJrad28Qjv2LYy3m0L8HeXedi8%2B%2B3iGR9cYUej9GBwF5Q7pO9wmaKEmCaT1B3RotsA3gMp5HIB%2FiOV&X-Amz-Signature=5dd5d3959ebd20e992f46e3e1309ae319fddec42fccaf0d48039e8d132e40fbf&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

