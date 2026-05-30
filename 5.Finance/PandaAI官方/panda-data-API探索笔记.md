---
tags:
  - quant
  - data
  - api
  - panda-data
created: 2026-05-30
updated: 2026-05-30
---

# panda-data SDK 深度探索 (v0.0.7)

## 概述

- **SDK**: `panda-data` v0.0.7
- **后端**: `http://pandadata.pandaaiquant.com`
- **账户**: `86` (基础免费套餐)
- **测试时间**: 2026-05-30
- **测试方法**: 实际调用每个 API 函数，记录返回结果和错误码

---

## 账户权限总览

| 类别 | 总数 | 可访问 | 空数据 | 无权限 |
|---|---|---|---|---|
| 行情数据 | 5 | 2 | 1 | 2 |
| 市场参考 | 27 | 8 | 3 | 16 |
| 财务因子 | 8 | 4 | 0 | 4 |
| 期货 | 35 | 1 | 1 | 33 |
| 交易工具 | 5 | 0 | 0 | 5 |
| **合计** | **80** | **15** | **5** | **60** |

> **结论**: 当前账户为基础免费账户，仅能访问 A 股日线级别的基础行情、龙虎榜、融资融券、股东户数、业绩快报、季度财报、因子数据和期货品种列表。分钟行情、港股、美股、概念/行业、大部分期货数据、交易工具等均无权限（错误码 `200103`）。

---

## 可访问 API ✅

### 行情数据

#### `get_market_data(type="stock")` — A股日线行情
```python
panda_data.get_market_data(
    symbol="000001.SZ",
    start_date="20260430", end_date="20260529",
    type="stock"
)
```
- 返回: 19行 × 13列
- 字段: `symbol, date, close, open, high, low, pre_close, change, pct_change, trade_status, volume, amount, turnover_rate`

#### `get_market_data(type="index")` — 指数日线行情
```python
panda_data.get_market_data(
    symbol="000300.SH",
    start_date="20260430", end_date="20260529",
    type="index"
)
```
- 返回: 19行 × 9列
- 字段: `symbol, date, close, open, high, low, pre_close, change, pct_change, volume`

### 市场参考

#### `get_stock_detail(market="cn")` — A股股票基本信息
```python
panda_data.get_stock_detail(symbol="000001.SZ", market="cn")
```
- 返回: 1行 × 18列
- 字段含: symbol, name, industry, area, list_date, total_shares, float_shares 等

#### `get_index_detail()` — 指数基本信息
```python
panda_data.get_index_detail(symbol="000300.SH")
```
- 返回: 1行 × 9列

#### `get_index_indicator()` — 指数日频指标
```python
panda_data.get_index_indicator(
    symbol="000300.SH",
    start_date="20260430", end_date="20260529"
)
```
- 返回: 19行 × 7列
- 字段: `symbol, date, pe_ttm, pb, volume, market_cap, total_market_cap`

#### `get_index_weights()` — 指数成分权重
```python
panda_data.get_index_weights(
    index_symbol="000300.SH",
    start_date="20260430", end_date="20260529"
)
```
- 返回: 5700行 × 4列
- 字段: `index_symbol, stock_symbol, date, weight`

#### `get_lhb_list()` — 龙虎榜列表
```python
panda_data.get_lhb_list(
    start_date="20260430", end_date="20260529"
)
```
- 返回: 1706行 × 12列

#### `get_lhb_detail()` — 龙虎榜明细
```python
panda_data.get_lhb_detail(
    start_date="20260430", end_date="20260529"
)
```
- 返回: 16847行 × 9列

#### `get_margin()` — 融资融券数据
```python
panda_data.get_margin(
    symbol="000001.SZ",
    start_date="20260430", end_date="end_date_str"
)
```
- 返回: 32行 × 11列

#### `get_holder_count()` — 股东户数
```python
panda_data.get_holder_count(symbol="000001.SZ")
```
- 返回: 120行 × 9列

#### `get_block_trade()` — 大宗交易
```python
panda_data.get_block_trade(symbol="000001.SZ")
```
- 返回: 265行 × 7列

### 财务与因子

#### `get_fina_performance()` — 业绩快报
```python
panda_data.get_fina_performance(symbol="000001.SZ")
```
- 返回: 1行 × 44列

#### `get_fina_reports()` — 季度财务报表
```python
panda_data.get_fina_reports(
    symbol="000001.SZ",
    start_quarter="2024q1", end_quarter="2026q2"
)
```
- 返回: 1行 × 320列
- 限制: start_quarter 和 end_quarter 间隔不能超过5年(20个季度)

#### `get_factor()` — 因子数据
```python
panda_data.get_factor(
    symbol="000001.SZ",
    start_date="20260430", end_date="20260529",
    type="stock", factors=["market_cap", "pe_ttm"]
)
```
- 返回: 19行 × 3列
- 限制: type 可选 `stock` 或 `future`，日期间隔不超过5年

#### `get_adj_factor()` — 复权因子
```python
panda_data.get_adj_factor(symbol="000001.SZ")
```
- 返回: 30行 × 6列
- 字段含: `symbol, ex_date, adj_factor` 等

### 期货

#### `get_future_detail()` — 期货品种列表
```python
panda_data.get_future_detail()
```
- 返回: 10657行 × 19列
- 所有上市期货合约列表

---

## 可访问但返回空数据 ⚠️

这些 API 不返回权限错误，但测试参数没有匹配到数据：

| API | 测试参数 | 说明 |
|---|---|---|
| `get_stock_detail(market="hk")` | 00700.HK | 可能需要不同的 symbol 格式 |
| `get_stock_detail(market="us")` | AAPL.US | 可能需要不同的 symbol 格式 |
| `get_hsgt_hold()` | 600519.SH | 可能查询区间无数据 |
| `get_top_holders()` | 000001.SZ, cn | 可能需要 start_date/end_date |
| `get_market_data(type="future")` | RB2501 | 该合约可能已到期 |

---

## 无权限 API ❌ (错误码 200103)

所有以下 API 返回 `[错误码 200103 ：API访问权限不足]`：

### 行情
- `get_market_min_data()` — A股分钟行情（1m/5m/15m/30m/60m/120m）
- `get_hk_daily()` — 港股日线
- `get_us_daily()` — 美股日线

### 概念/行业
- `get_concept_list()` — 概念列表
- `get_concept_constituents()` — 概念成分股
- `get_industry_detail()` — 行业列表
- `get_industry_constituents()` — 行业成分股
- `get_stock_industry()` — 股票所属行业

### 资金/股东/分红/事件
- `get_investor_activity()` — 投资者活动
- `get_share_float()` — 流通股本
- `get_repurchase()` — 回购
- `get_restricted_list()` — 限售解禁
- `get_stock_cash_dividend()` — 现金分红
- `get_stock_dividend_info()` — 分红信息
- `get_stock_split_info()` — 拆股信息
- `get_stock_dividend_amount()` — 分红金额
- `get_stock_private_placement()` — 定向增发
- `get_stock_allotment()` — 配股

### 财务
- `get_fina_forecast()` — 业绩预告
- `get_financial_statement()` — 港美股财务报表
- `get_audit_opinion()` — 审计意见

### 期货（全部除品种列表外）
- `get_future_dominant()` — 主力合约
- `get_future_symbol_posi()` — 合约持仓排名
- `get_future_variety_posi()` — 品种持仓排名
- `get_future_contract_indicators()` — 合约日度指标
- `get_broker_variety_profit()` — 经纪商品种盈亏
- `get_future_net_flow()` — 资金净流向
- `get_future_daily_post()` — 成交持仓排名
- `get_future_netposi_rank()` — 净持仓排名
- `get_broker_grade()` — 经纪商评级
- `get_broker_netmarg()` — 经纪商净保证金
- `get_broker_totlmarg()` — 经纪商总保证金
- `get_broker_netmarg_change()` — 保证金变动
- `get_future_basis()` — 基差
- `get_future_warehouse_receipt()` — 仓单
- `get_future_ls_ratio()` — 多空比
- `get_future_netcap_change()` — 净资本变动
- `get_future_contract_rank()` — 合约排名
- `get_future_term_structure()` — 期限结构
- `get_future_inventory()` — 库存
- `get_broker_oi_value()` — 持仓市值
- `get_future_contract_pool()` — 合约池
- `get_broker_profit()` — 经纪商盈亏
- `get_broker_flow_daily()` — 经纪商资金流向
- `get_broker_ls_ratio()` — 经纪商多空比
- `get_future_nonbroker_net()` — 非经纪商净持仓
- `get_future_calendar_arbitrage()` — 跨期套利
- `get_future_free_spread()` — 自由价差
- `get_future_free_ratio()` — 自由价比
- `get_future_dominant_corr()` — 主力合约相关性
- `get_broker_profit_rank()` — 席位盈利排名
- `get_broker_loss_rank()` — 席位亏损排名
- `get_future_trader_quote()` — 现货报价
- `get_future_spot_profit()` — 现货盈亏
- `get_future_virtual_ratio()` — 虚实比
- `get_future_seat_matching()` — 席位配对
- `get_future_variety_mcap()` — 品种市值
- `get_broker_build_process()` — 建仓过程

### 交易工具
- `get_trade_cal()` — 交易日历
- `get_prev_trade_date()` — 前N交易日
- `get_last_trade_date()` — 最新交易日
- `get_stock_status_change()` — ST/PT状态变更
- `get_trade_list()` — 可交易股票列表

---

## 错误码速查表

| 错误码 | 含义 |
|---|---|
| `100000` | 请求参数错误 |
| `100001` | 请求参数不能为空 |
| `100002` | 请求参数值格式错误 |
| `100003` | 请求参数类型错误 |
| `100004` | 请求参数值超出范围 |
| `100005` | 请求参数值中存在重复 |
| `100006` | 请求参数值无效 |
| `100007` | 日期格式错误 |
| `100008` | 日期范围/季度间隔无效 |
| `200001` | 认证失败 |
| `200002` | 未登录或登录已过期 |
| `200005` | 用户名或密码错误 |
| `200103` | **API 访问权限不足** (最常见) |
| `200104` | 数据访问权限受限 |
| `500001` | 请求频率超限 |
| `500006` | 并发请求数超限 |
| `600001` | 数据查询失败 |
| `900001` | 系统异常 |

---

## 参数要点记录

### Symbol 格式
- **A股**: `000001.SZ`, `600519.SH`
- **指数**: `000300.SH`, `000905.SH`
- **期货合约**: `RB2501`, `AG2201`, `A_DOMINANT`
- **期货品种**: `RB`, `CU`, `A` (纯大写字母)
- **港股**: `00700.HK`
- **美股**: `AAPL.US`

### 关键限制
- 日线数据日期间隔 ≤ 5年
- 季度财报间隔 ≤ 5年(20个季度)
- `get_market_data` type: `stock` / `future` / `index`
- `get_fina_reports` quarter 格式: `YYYYqN` (如 `2024q1`)
- `get_factor` type: `stock` / `future`, factors 必填
- `get_index_indicator` index_component: 新格式 `000300`, 旧格式 `100` 会自动转换

### 注意
- 分钟行情、港美股行情、期货数据等大部分功能需要更高级别的账户套餐
- 认证采用 `username` + `password`(MD5) 方式，Token 缓存在项目根目录的 `user.json`

---

## SDK 模块结构

```
panda_data/
├── __init__.py          # 公开接口导出 (107个函数)
├── client.py            # HTTP 客户端管理
├── exceptions.py        # 异常和错误码枚举
├── config/__init__.py   # 配置加载(环境变量 + yaml)
├── core/service.py      # fetch_dataframe / request_service
├── readers/
│   ├── init_token.py            # 登录认证
│   ├── market_reader.py         # 行情(4函数)
│   ├── market_reference_reader.py # 市场参考(17函数)
│   ├── financial_and_factors_reader.py # 财务因子(8函数)
│   ├── future_reader.py         # 期货(35函数)
│   └── trading_tools_reader.py  # 交易工具(5函数)
├── transport/http.py    # HTTP 传输层
└── utils/
    ├── common_utils.py        # 工具函数
    └── param_check_utils.py   # 参数验证(70KB)
```