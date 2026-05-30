PandaAI工作流-数据API说明
  PandaAI官方  2025年07月23日  1604  1
量化策略因子大赛历史数据数据API
接口文档

一、通用K线数据

1. 获取股票的详细信息

1.1. 方法名：get_stock_detail

1.2. 入参

字段	类型	描述	是否必填
symbol	Optional[Union[str, List[str]]]	股票代码	非必填
fields	Optional[List[str]]	返回字段	非必填
market	Optional[str]	市场，支持cn,hk,us，默认cn	非必填
status	Optional[int]	是否在市，1 -在市，0 -退市，-1 -未知	非必填
1.3. 响应参数

字段	类型	描述
symbol	str	股票代码
industry_code	str	行业代码
market_tplus	int	交易制度
name	str	股票名称
special_type	str	特别处理状态
exchange	str	交易所
status	int	股票状态
type	str	产品类型
de_listed_date	str	退市日期
listed_date	str	上市日期
sector_code_name	str	以当地语言为标准的板块代码名
abbrev_symbol	str	股票的名称缩写
sector_code	str	板块缩写代码
min_order_amount	double	一手对应多少股
trading_hours	str	产品最新交易时间
board_type	str	板块类别
industry_name	str	国民经济行业分类名称
issue_price	double	该证券发行价
trading_code	str	交易代码
office_address	str	公司地址
province	str	省份
purchasedate	str	申购日期
1.4. 使用示例

1.4.1. fields字段为空且status字段为空

import panda_data
result = panda_data.get_stock_detail(
    symbol=["000001.SZ","000002.SZ","000003.SZ"],
    market="cn",
    fields=[""],
    status=None
)
print(result)
symbol abbrev_symbol ... trading_code trading_hours
0 000001.SZ PAYH ... 000001 09:31-11:30,13:01-15:00
1 000002.SZ WKA ... 000002 09:31-11:30,13:01-15:00
2 000003.SZ PTJTA ... 000003 09:31-11:30,13:01-15:00
1.4.2. 指定fields且指定status字段

import panda_data
result = panda_data.get_stock_detail(
    symbol=["000001.SZ","000002.SZ","000003.SZ"],
    fields=["symbol", "name", "province", "office_address", "trading_code"],
    market="cn",
    status=1
)
print(result)
symbol name ... status trading_code
0 000001.SZ 平安银行 ... 1 000001
1 000002.SZ 万科A ... 1 000002
1.4.3. 港股

import panda_data
result = panda_data.get_stock_detail(
    symbol=["0001.HK","0002.HK","0003.HK"],
    market="hk",
    fields=[""],
    status=None
)
print(result)
symbol abbrev_symbol ... status trading_code
0 0001.HK CKHUH ... 1 0001
1 0002.HK CLPHL ... 1 0002
2 0003.HK HKCNG ... 1 0003|864603
1.4.4. 美股

import panda_data
result = panda_data.get_stock_detail(
    symbol=["A.N","AA.N","AABA.O"],
    market="us",
    fields=[""],
    status=None
)
print(result)
symbol abbrev_symbol ... status trading_code
0 A.N Agilent Technologies ... 1 A
1 AA.N Alcoa ... 1 AA
2 AABA.O Altaba ... 0 AABA
1.4.5. 获取全部A股股票代码

import panda_data
result = panda_data.get_stock_detail(
    symbol="",
    fields=["symbol"],
    market="cn",
    status=None
)
print(result)
symbol
0 000001.SZ
1 000002.SZ
2 000003.SZ
3 000004.SZ
4 000005.SZ
... ...
5512 688809.SH
5513 688819.SH
5514 688981.SH
5515 689009.SH
5516 990018.SH
1.4.6. 获取全部港股股票代码

import panda_data
result = panda_data.get_stock_detail(
    symbol="",
    fields=["symbol"],
    market="hk",
    status=None
)
print(result)
symbol
0 000002.SZ
1 000039.SZ
2 000063.SZ
3 0001.HK
4 000157.SZ
... ...
2916 XMUS.DE
2917 XNIF.DE
2918 YACHT.MI
2919 YAL.AX
2920 YUMC.K
1.4.7. 获取全部美股股票代码

import panda_data
result = panda_data.get_stock_detail(
    symbol="",
    fields=["symbol"],
    market="us",
    status=None
)
print(result)
symbol
0 A.N
1 AA.N
2 AAAP.O
3 AABA.O
4 AAC.N
... ...
11683 ZYBT.O
11684 ZYME.O
11685 ZYNE.O
11686 ZYXI.O
11687 ZZ.N
2. 获取日线数据

2.1. 方法名：get_market_data

2.2. 入参

字段	类型	描述	是否必填
start_date	str	开始日期,eg:“20250702”	必填
end_date	str	结束日期,eg:“20250702”	必填
symbol	Optional[Union[str, List[str]]]	股票/指数/期货代码	非必填
fields	Optional[Union[str, List[str]]]	返回字段	非必填
type	Optional[str]	产品类型，包含：“stock” ,“future”,“index”	非必填
indicator	Optional[str]	用作筛选指数成分股的指数代码，默认为"000985"可选值000300，000905，000852。仅在type为stock时有效	非必填
st	Optional[bool]	是否包含ST股，默认True表示包含。仅在type为stock时有效	非必填
2.3. 响应参数

股票:

字段	类型	描述
date	str	日期
symbol	str	股票代码
name	str	股票名称
open	double	当日开盘价
close	double	当日收盘价
high	double	当日最高价
low	double	当日最低价
volume	double	当日成交量
pre_close	double	昨收价
limit_up	double	当日涨停价
limit_down	double	当日跌停价
index_component	str	股票池
trade_status	int	当日是否停牌（0表示当日不停牌）
指数:

字段	类型	描述
symbol	str	指数代码
date	str	日期
open	double	开盘价
close	double	收盘价
high	double	最高价
low	double	最低价
volume	double	成交量
pre_close	double	昨日结算价
amount	double	成交额
期货:

字段	类型	描述
date	str	日期
symbol	str	期货代码
dominant_id	str	主力合约代码
exchange	str	交易所
trading_code	str	交易代码
underlying_symbol	str	期货品种
open	double	当日开盘价
close	double	当日收盘价
high	double	当日最高价
low	double	当日最低价
volume	double	当日成交量
day_session_open	double	日盘开盘价
limit_up	double	当日涨停价
limit_down	double	当日跌停价
amount	double	当日成交额
open_interest	double	累计持仓量
settlement	double	结算价
pre_settlement	double	昨日结算价
2.4. 使用示例

2.4.1. 获取单支股票的日线

import panda_data
result = panda_data.get_market_data(
    symbol=["000001.SZ"],
    start_date="20250101",
    end_date="20250131",
    type="stock",
    fields=[],
    indicator="000300",
    st=True
)
print(result)
date symbol close ... pre_close trade_status volume
0 20250127 000001.SZ 11.47 ... 11.34 0 115193471.0
1 20250124 000001.SZ 11.34 ... 11.32 0 94494421.0
2 20250123 000001.SZ 11.32 ... 11.09 0 151492027.0
3 20250122 000001.SZ 11.09 ... 11.33 0 134712922.0
4 20250121 000001.SZ 11.33 ... 11.42 0 90206894.0
5 20250120 000001.SZ 11.42 ... 11.45 0 83202913.0
6 20250117 000001.SZ 11.45 ... 11.57 0 68976486.0
7 20250116 000001.SZ 11.57 ... 11.48 0 87296399.0
8 20250115 000001.SZ 11.48 ... 11.38 0 103163082.0
9 20250114 000001.SZ 11.38 ... 11.20 0 82462895.0
10 20250113 000001.SZ 11.20 ... 11.30 0 93496618.0
11 20250110 000001.SZ 11.30 ... 11.40 0 79813351.0
12 20250109 000001.SZ 11.40 ... 11.50 0 75148330.0
13 20250108 000001.SZ 11.50 ... 11.51 0 106238601.0
14 20250107 000001.SZ 11.51 ... 11.44 0 74786288.0
15 20250106 000001.SZ 11.44 ... 11.38 0 108553630.0
16 20250103 000001.SZ 11.38 ... 11.43 0 115468044.0
17 20250102 000001.SZ 11.43 ... 11.70 0 181959699.0
2.4.2. 获取多支股票的日线并使用fields

import panda_data
result = panda_data.get_market_data(
    symbol=["000001.SZ","000002.SZ"],
    start_date="20250101",
    end_date="20250110",
    type="stock",
    fields=['high','low','open'],
    indicator="000300",
    st=True
)
print(result)
date symbol high low open
0 20250110 000001.SZ 11.46 11.28 11.40
1 20250109 000001.SZ 11.50 11.35 11.50
2 20250108 000001.SZ 11.63 11.40 11.50
3 20250107 000001.SZ 11.53 11.37 11.42
4 20250106 000001.SZ 11.48 11.22 11.38
5 20250103 000001.SZ 11.54 11.36 11.44
6 20250102 000001.SZ 11.77 11.39 11.73
7 20250110 000002.SZ 7.03 6.69 6.96
8 20250109 000002.SZ 7.01 6.91 6.93
9 20250108 000002.SZ 7.03 6.83 7.02
10 20250107 000002.SZ 7.05 6.92 6.96
11 20250106 000002.SZ 7.01 6.89 6.99
12 20250103 000002.SZ 7.18 6.96 7.17
13 20250102 000002.SZ 7.36 7.07 7.25
2.4.3. 获取单个指数的日线

import panda_data
result = panda_data.get_market_data(
    symbol=["000001.SH"],
    start_date="20250101",
    end_date="20250131",
    type="index",
    fields=[],
    indicator="",
    st=None
)
print(result)
symbol date amount ... open pre_close volume
0 000001.SH 20250127 4.502315e+11 ... 3256.6136 3252.6264 3.874676e+10
1 000001.SH 20250124 4.806851e+11 ... 3222.8774 3230.1637 3.986530e+10
2 000001.SH 20250123 5.398006e+11 ... 3237.5988 3213.6237 4.582468e+10
3 000001.SH 20250122 4.523129e+11 ... 3235.4925 3242.6226 3.648175e+10
4 000001.SH 20250121 4.682634e+11 ... 3256.8325 3244.3776 3.845837e+10
5 000001.SH 20250120 4.697410e+11 ... 3256.1492 3241.8212 4.033379e+10
6 000001.SH 20250117 4.565531e+11 ... 3226.7616 3236.0320 3.835993e+10
7 000001.SH 20250116 4.990554e+11 ... 3239.0261 3227.1167 4.306555e+10
8 000001.SH 20250115 4.662162e+11 ... 3234.7152 3240.9400 4.047232e+10
9 000001.SH 20250114 5.389838e+11 ... 3165.1613 3160.7550 4.692127e+10
10 000001.SH 20250113 4.117740e+11 ... 3148.8259 3168.5238 3.727420e+10
11 000001.SH 20250110 4.659394e+11 ... 3211.7068 3211.3933 4.036633e+10
12 000001.SH 20250109 4.344455e+11 ... 3220.7205 3230.1679 3.829436e+10
13 000001.SH 20250108 5.081484e+11 ... 3218.8577 3229.6439 4.728644e+10
14 000001.SH 20250107 4.363884e+11 ... 3203.3068 3206.9228 4.096605e+10
15 000001.SH 20250106 4.441882e+11 ... 3209.7832 3211.4299 4.309784e+10
16 000001.SH 20250103 5.231598e+11 ... 3267.0766 3262.5607 5.175920e+10
17 000001.SH 20250102 6.033405e+11 ... 3347.9392 3351.7630 5.613752e+10
2.4.4. 获取多个指数的日线并使用fields

import panda_data
result = panda_data.get_market_data(
    symbol=["000001.SH","000002.SH"],
    start_date="20250101",
    end_date="20250110",
    type="index",
    fields=['open','high','low'],
    indicator="",
    st=None
)
print(result)
symbol date high low open
0 000001.SH 20250110 3220.1073 3168.5238 3211.7068
1 000001.SH 20250109 3228.9725 3205.9103 3220.7205
2 000001.SH 20250108 3246.2908 3175.7247 3218.8577
3 000001.SH 20250107 3230.8529 3190.4612 3203.3068
4 000001.SH 20250106 3219.4877 3185.4631 3209.7832
5 000001.SH 20250103 3273.5656 3205.7755 3267.0766
6 000001.SH 20250102 3351.7220 3242.0865 3347.9392
7 000002.SH 20250110 3375.1182 3321.0967 3366.2697
8 000002.SH 20250109 3384.3807 3360.1717 3375.6940
9 000002.SH 20250108 3402.5174 3328.5154 3373.6754
10 000002.SH 20250107 3386.2698 3343.8844 3357.4853
11 000002.SH 20250106 3374.4387 3338.7331 3364.3413
12 000002.SH 20250103 3431.3073 3360.1531 3424.5050
13 000002.SH 20250102 3513.3453 3398.2847 3509.3685
2.4.5. 获取单个期货的日线

import panda_data
result = panda_data.get_market_data(
    symbol=["A_DOMINANT.DCE"],
    start_date="20250101",
    end_date="20250131",
    type="future",
    fields=[],
    indicator="",
    st=None
)
print(result)
symbol date close ... underlying_symbol volume amount
0 A_DOMINANT.DCE 20250127 4026.0 ... A 77051.0 3.101001e+09
1 A_DOMINANT.DCE 20250124 4032.0 ... A 82709.0 3.328289e+09
2 A_DOMINANT.DCE 20250123 4013.0 ... A 137752.0 5.560589e+09
3 A_DOMINANT.DCE 20250122 4060.0 ... A 120244.0 4.858647e+09
4 A_DOMINANT.DCE 20250121 4032.0 ... A 121350.0 4.880503e+09
5 A_DOMINANT.DCE 20250120 4019.0 ... A 156975.0 6.288453e+09
6 A_DOMINANT.DCE 20250117 4028.0 ... A 132882.0 5.316338e+09
7 A_DOMINANT.DCE 20250116 4000.0 ... A 154543.0 6.171644e+09
8 A_DOMINANT.DCE 20250115 3987.0 ... A 135333.0 5.376645e+09
9 A_DOMINANT.DCE 20250114 3962.0 ... A 167882.0 6.639720e+09
10 A_DOMINANT.DCE 20250113 3937.0 ... A 130101.0 5.089278e+09
11 A_DOMINANT.DCE 20250110 3893.0 ... A 183552.0 7.127665e+09
12 A_DOMINANT.DCE 20250109 3840.0 ... A 85396.0 3.278591e+09
13 A_DOMINANT.DCE 20250108 3837.0 ... A 89960.0 3.453663e+09
14 A_DOMINANT.DCE 20250107 3848.0 ... A 153748.0 5.936845e+09
15 A_DOMINANT.DCE 20250106 3892.0 ... A 152269.0 5.931398e+09
16 A_DOMINANT.DCE 20250103 3917.0 ... A 104354.0 4.099407e+09
17 A_DOMINANT.DCE 20250102 3931.0 ... A 86643.0 3.412603e+09
2.4.6. 获取多个期货的日线并使用fields

import panda_data
result = panda_data.get_market_data(
    symbol=["A2501.DCE", "ZN_DOMINANT.SHF"],
    start_date="20250101",
    end_date="20250105",
    type="future",
    fields=['open', 'high', 'low'],
    indicator="",
    st=None
)
print(result)
symbol date high low open
0 A2501.DCE 20250103 3834.000000 3834.000000 3834.000000
1 A2501.DCE 20250102 3860.000000 3819.000000 3820.000000
2 ZN99.SHF 20250103 24998.448587 24498.174088 24905.751147
3 ZN99.SHF 20250102 25278.907173 25078.248769 25216.137054
3. 获取分钟级数据

3.1. 方法名：get_market_min_data

3.2. 入参

字段	类型	描述	是否必填
start_date	str	开始日期,eg:“20250702”	必填
end_date	str	结束日期,eg:“20250702”	必填
symbol	Optional[Union[str, List[str]]]	股票代码	非必填
fields	Optional[Union[str, List[str]]]	返回字段	非必填
symbol_type	Optional[str]	产品类型，包含：“stock” ,“future” ,“index”	非必填
time_zone	Optional[tuple]	时间段过滤,格式为(“HH:MM”, “HH:MM”)，例如(“10:00”, “23:00”)	非必填
frequency	Optional[str]	频率, 支持 “1m”, “5m”, “15m”, “60m”,默认为"1m"（指数仅支持1m）	非必填
3.3. 响应参数

股票:

字段	类型	描述
date	str	日期
minute	str	时间（精确至分钟）
symbol	str	股票代码
name	str	股票名称
open	double	当日开盘价
close	double	当日收盘价
high	double	当日最高价
low	double	当日最低价
volume	double	当日成交量
amount	double	当日成交额
num_trades	double	成交笔数
指数:

字段	类型	描述
symbol	str	指数代码
date	str	日期
minute	str	时间（精确至分钟）
open	double	开盘价
close	double	收盘价
high	double	最高价
low	double	最低价
volume	double	成交量
amount	double	成交额
trading_date	str	交易日期
期货:

字段	类型	描述
date	str	日期
minute	str	时间（精确至分钟）
symbol	str	期货代码
dominant_id	str	主力合约代码
exchange	str	交易所
trading_code	str	交易代码
underlying_symbol	str	期货品种
trading_date	str	交易日期
open	double	当日开盘价
close	double	当日收盘价
high	double	当日最高价
low	double	当日最低价
volume	double	当日成交量
3.4. 使用示例

3.4.1. 获取单支股票的1分钟线数据并使用fields

import panda_data
result = panda_data.get_market_min_data(
    symbol="000001.SZ",
    start_date="20250101",
    end_date="20250131",
    symbol_type="stock",
    fields=["symbol", "date", "num_trades", "amount", "volume"],
    frequency="1m",
    time_zone=("10:00", "11:00")
)
print(result)
symbol num_trades volume amount date minute
0 000001.SZ 95.0 193500.0 2221669.0 20250127 110000
1 000001.SZ 194.0 140400.0 1613212.0 20250127 105900
2 000001.SZ 364.0 338200.0 3886710.0 20250127 105800
3 000001.SZ 160.0 172658.0 1984536.0 20250127 105700
4 000001.SZ 400.0 285300.0 3278079.0 20250127 105600
... ... ... ... ... ... ...
1093 000001.SZ 464.0 927900.0 10830718.0 20250102 100400
1094 000001.SZ 242.0 500200.0 5841058.0 20250102 100300
1095 000001.SZ 729.0 1581800.0 18469542.0 20250102 100200
1096 000001.SZ 296.0 363902.0 4252891.0 20250102 100100
1097 000001.SZ 190.0 232100.0 2714037.0 20250102 100000
3.4.2. 获取多支股票的15分钟线数据

import panda_data
result = panda_data.get_market_min_data(
    symbol=["000001.SZ","000002.SZ"],
    start_date="20250101",
    end_date="20250131",
    symbol_type="stock",
    fields=[],
    frequency="15m",
    time_zone=("10:00", "11:00")
)
print(result)
symbol close high low ... volume amount date minute
0 000001.SZ 11.49 11.50 11.48 ... 3156758.0 36284095.0 20250127 110000
1 000001.SZ 11.50 11.51 11.48 ... 3728400.0 42863418.0 20250127 104500
2 000001.SZ 11.48 11.51 11.48 ... 5857200.0 67340712.0 20250127 103000
3 000001.SZ 11.51 11.52 11.49 ... 5972082.0 68728285.0 20250127 101500
4 000001.SZ 11.50 11.52 11.48 ... 9531000.0 109656164.0 20250127 100000
.. ... ... ... ... ... ... ... ... ...
175 000002.SZ 7.27 7.28 7.25 ... 4502120.0 32724361.0 20250102 110000
176 000002.SZ 7.26 7.31 7.25 ... 8070200.0 58747814.0 20250102 104500
177 000002.SZ 7.31 7.32 7.30 ... 4246800.0 31031117.0 20250102 103000
178 000002.SZ 7.31 7.33 7.29 ... 6696700.0 48973297.0 20250102 101500
179 000002.SZ 7.29 7.36 7.29 ... 11701900.0 85782493.0 20250102 100000
3.4.3. 获取单个指数的1分钟线数据并使用fields

import panda_data
result = panda_data.get_market_min_data(
    symbol="000001.SH",
    start_date="20250101",
    end_date="20250131",
    symbol_type="index",
    fields=["symbol", "date", "amount", "volume"],
    frequency="1m",
    time_zone=("10:00", "11:00")
)
print(result)
symbol amount volume date minute
0 000001.SH 9.364504e+08 78038400.0 20250127 110000
1 000001.SH 1.002671e+09 85079600.0 20250127 105900
2 000001.SH 1.084810e+09 95052300.0 20250127 105800
3 000001.SH 1.383025e+09 109437300.0 20250127 105700
4 000001.SH 1.576401e+09 162083900.0 20250127 105600
... ... ... ... ... ...
1093 000001.SH 4.029659e+09 364572800.0 20250102 100400
1094 000001.SH 3.241950e+09 273959000.0 20250102 100300
1095 000001.SH 3.287943e+09 266980600.0 20250102 100200
1096 000001.SH 3.650173e+09 341037500.0 20250102 100100
1097 000001.SH 3.121190e+09 285190800.0 20250102 100000
3.4.4. 获取多个指数的1分钟线数据

import panda_data
result = panda_data.get_market_min_data(
    symbol=["000001.SH","000002.SH"],
    start_date="20250101",
    end_date="20250110",
    symbol_type="index",
    fields=[],
    frequency="1m",
    time_zone=("10:00", "11:00")
)
print(result)
symbol amount close ... volume date minute
0 000001.SH 1.246789e+09 3202.1239 ... 90331600.0 20250110 110000
1 000001.SH 1.591083e+09 3201.5813 ... 133511900.0 20250110 105900
2 000001.SH 1.201811e+09 3203.3221 ... 89499400.0 20250110 105800
3 000001.SH 1.246054e+09 3203.0991 ... 100101400.0 20250110 105700
4 000001.SH 1.566827e+09 3204.4015 ... 133112700.0 20250110 105600
.. ... ... ... ... ... ... ...
849 000002.SH 4.027991e+09 3483.7672 ... 364440700.0 20250102 100400
850 000002.SH 3.240003e+09 3487.5959 ... 273823500.0 20250102 100300
851 000002.SH 3.286036e+09 3490.9403 ... 266886000.0 20250102 100200
852 000002.SH 3.643868e+09 3491.3390 ... 340761000.0 20250102 100100
853 000002.SH 3.115685e+09 3492.2591 ... 284954000.0 20250102 100000
3.4.5. 获取单个期货的1分钟线数据并使用fields

import panda_data
result = panda_data.get_market_min_data(
    symbol="A2501.DCE",
    start_date="20250101",
    end_date="20250131",
    symbol_type="future",
    fields=["symbol", "date", "num_trades", "amount", "volume"],
    frequency="1m",
    time_zone=("10:00", "11:00")
)
print(result)
symbol volume amount date minute
0 A2501.DCE 0.0 0.0 20250115 110000
1 A2501.DCE 0.0 0.0 20250115 105900
2 A2501.DCE 0.0 0.0 20250115 105800
3 A2501.DCE 0.0 0.0 20250115 105700
4 A2501.DCE 0.0 0.0 20250115 105600
.. ... ... ... ... ...
455 A2501.DCE 10.0 383000.0 20250102 100400
456 A2501.DCE 0.0 0.0 20250102 100300
457 A2501.DCE 5.0 191500.0 20250102 100200
458 A2501.DCE 0.0 0.0 20250102 100100
459 A2501.DCE 10.0 383000.0 20250102 100000
3.4.6. 获取多个期货的15分钟线数据

import panda_data
result = panda_data.get_market_min_data(
    symbol=["A2501.DCE", "ZN_DOMINANT.SHF"],
    start_date="20250101",
    end_date="20250130",
    symbol_type="future",
    fields=[],
    frequency="15m",
    time_zone=("10:00", "11:00")
)
print(result)
symbol close dominant_id ... volume date minute
0 A2501.DCE 3880.0 A2501 ... 0.0 20250115 110000
1 A2501.DCE 3880.0 A2501 ... 0.0 20250115 104500
2 A2501.DCE 3880.0 A2501 ... 0.0 20250115 101500
3 A2501.DCE 3880.0 A2501 ... 0.0 20250115 100000
4 A2501.DCE 3821.0 A2501 ... 0.0 20250114 110000
.. ... ... ... ... ... ... ...
107 ZN_DOMINANT.SHF 24605.0 ZN2502 ... 6483.0 20250103 100000
108 ZN_DOMINANT.SHF 25265.0 ZN2502 ... 3201.0 20250102 110000
109 ZN_DOMINANT.SHF 25215.0 ZN2502 ... 5810.0 20250102 104500
110 ZN_DOMINANT.SHF 25205.0 ZN2502 ... 7043.0 20250102 101500
111 ZN_DOMINANT.SHF 25145.0 ZN2502 ... 11750.0 20250102 100000
4. 获取回测因子

4.1. 方法名：get_factor

4.2. 入参

字段	类型	描述	是否必填
start_date	str	开始日期,eg:“20250702”	必填
end_date	str	结束日期,eg:“20250702”	必填
symbol	Union[str, List[str]]	股票代码	必填
factors	List[str]	因子列表	必填
type	Optional[str]	产品类型，支持"stock" ,“future”，默认为"stock"	非必填
index_component	Optional[str]	指数成分股过滤条件,可选项有沪深300:“100”,中证500:“010”,中证1000:“001”	非必填
4.3. 响应参数

基础因子类:

股票:

字段	类型	描述
date	str	日期
symbol	str	股票代码
name	str	股票名称
open	double	开盘价
close	double	收盘价
high	double	最高价
low	double	最低价
volume	double	成交量
amount	double	成交额
index_component	str	股票池
market_cap	double	市值
turnover	double	换手率
期货:

字段	类型	描述
date	str	日期
symbol	str	期货代码
dominant_id	str	主力合约代码
exchange	str	交易所
trading_code	str	交易代码
underlying_symbol	str	期货品种
open	double	当日开盘价
close	double	收盘价
high	double	最高价
low	double	最低价
volume	double	成交量
day_session_open	double	日盘开盘价
limit_up	double	涨停价
limit_down	double	跌停价
amount	double	成交额
open_interest	double	累计持仓量
settlement	double	结算价
pre_settlement	double	昨日结算价
财务因子类（仅stock可选）:

字段	类型	描述
cash_received_from_sales_of_goods	double	销售商品、提供劳务收到的现金： 公司销售商品、提供劳务实际收到的现金 :investopedia
refunds_of_taxes	double	收到的税费返还： 公司按规定收到的增值税、所得税等税费返还额 :mba
net_deposit_increase	double	客户存款和同业存放款项净增加额
net_increase_from_central_bank	double	向中央银行借款净增加额
net_increase_from_other_financial_institutions	double	向其他金融机构拆入资金净增加额
draw_back_canceled_loans	double	收回已核销贷款
cash_received_from_interests_and_commissions	double	收取利息、手续费及佣金的现金
net_increase_from_disposing_financial_assets	double	处置交易性金融资产净增加额
net_increase_from_repurchasing_business	double	回购业务资金净增加额
cash_received_from_original_insurance	double	收到原保险合同保费取得的现金
cash_received_from_reinsurance	double	收到再保业务现金净额
net_increase_from_insurer_deposit_investment	double	保户储金及投资款净增加额
net_increase_from_financial_institutions	double	拆入资金净增加额
cash_received_from_proxy_security	double	代理买卖证券收到的现金净额
cash_received_from_sub_issue_security	double	代理承销证券收到的现金净额
cash_from_other_operating_activities	double	收到其它与经营活动有关的现金：公司除了上述各项目外，收到的其他与经营活动有关的现金，如捐赠现金收入、罚款收入、流动资产损失中由个人赔偿的现金收入等 :mba
cash_from_operating_activities	double	经营活动现金流入小计
cash_paid_for_goods_and_services	double	购买商品、接受劳务支付的现金： 公司购买商品、接受劳务实际支付的现金 :investopedia
assets_depreciation_reserves	double	资产减值准备
exchange_rate_change_effect	double	汇率变动对现金及现金等价物的影响
other_effecting_cash_equivalent_items	double	影响现金及现金等价物的其他科目
cash_equivalent_increase	double	现金及现金等价物净增加额（来源现金流量表主表）
begin_period_cash_equivalent	double	加:期初现金及现金等价物余额
end_period_cash_equivalent	double	期末现金及现金等价物余额
cash_paid_for_employee	double	支付给职工以及为职工支付的现金： 公司实际支付给职工，以及为职工支付的现金，包括本期实际支付给职工的工资、奖金、各种津贴和补贴等 :mba
cash_paid_for_taxes	double	支付的各项税费： 反映企业按规定支付的各种税费，包括本期发生并支付的税费，以及本期支付以前各期发生的税费和预交的税金等 :mba
net_increase_from_loans_and_advances	double	客户贷款及垫款净增加额
net_increase_from_central_bank_and_banks	double	存放中央银行和同业款项净增加额
net_increase_from_lending_capital	double	拆出资金净增加额
cash_paid_for_comissions	double	支付手续费及佣金的现金
cash_paid_for_orignal_insurance	double	支付原保险合同赔付款项的现金
cash_paid_for_reinsurance	double	支付再保业务现金净额
cash_paid_for_policy_dividends	double	支付保单红利的现金
net_increase_from_trading_financial_assets	double	为交易目的而持有的金融资产净增加额
net_increase_from_operating_buy_back	double	返售业务资金净增加额(经营)
cash_paid_for_other_operation_activities	double	支付其他与经营活动有关的现金： 反映企业支付的其他与经营活动有关的现金支出，如罚款支出、支付的差旅费、业务招待费的现金支出、支付的保险费等 :mba
cash_paid_for_operation_activities	double	经营活动现金流出小计
cash_flow_from_operating_activities	double	经营活动产生的现金流量净额： 指企业投资活动和筹资活动以外的所有交易活动和事项的现金流入和流出量 :mba
cash_received_from_disposal_of_investment	double	收回投资收到的现金
cash_received_from_investment	double	取得投资收益收到的现金
cash_received_from_disposal_of_asset	double	处置固定资产、无形资产和其他长期资产收回的现金净额： 公司处置固定资产、无形资产和其他长期资产收回的现金 :investopedia
cash_received_from_other_investment_activities	double	收到其他与投资活动有关的现金： 公司除了上述各项以外，收到的其他与投资活动有关的现金 :mba
cash_received_from_investment_activities	double	投资活动现金流入小计
cash_paid_for_asset	double	购建固定资产、无形资产和其他长期资产所支付的现金 :wikipedia
cash_paid_to_acquire_investment	double	投资支付的现金： 反映企业进行权益性投资和债权性投资支付的现金，包括企业取得的除现金等价物以外的股票投资和债券投资等支付的现金等 :mba
cash_paid_for_other_investment_activities	double	支付其他与投资活动有关的现金： 反映企业除了上述各项以外，支付的其他与投资活动有关的现金流出 :mba
cash_paid_for_investment_activities	double	投资活动产生的现金流出小计
cash_flow_from_investing_activities	double	投资活动产生的现金流量净额：指企业长期资产的购建和对外投资活动（不包括现金等价物范围的投资）的现金流入和流出量 :mba
cash_received_from_investors	double	吸收投资收到的现金：反映企业收到的投资者投入现金，包括以发行股票、债券等方式筹集的资金实际收到的净额 :mba
cash_received_from_minority_invest_subsidiaries	double	其中:子公司吸收少数股东投资收到的现金
cash_received_from_issuing_security	double	发行债券收到的现金
cash_received_from_financial_institution_borrows	double	取得借款收到的现金： 公司向银行或其他金融机构等借入的资金 :mba
cash_received_from_issuing_equity_instruments	double	发行其他权益工具收到的现金
net_increase_from__financing_buy_back	double	回购业务资金净增加额(筹资)
cash_received_from_other_financing_activities	double	收到其他与筹资活动有关的现金：反映企业收到的其他与筹资活动有关的现金流入，如接受现金捐赠等 :mba
cash_received_from_financing_activities	double	筹资活动现金流入小计
cash_paid_for_debt	double	偿还债务支付的现金：公司以现金偿还债务的本金，包括偿还银行或其他金融机构等的借款本金、偿还债券本金等 :mba
cash_paid_for_dividend_and_interest	double	分配股利、利润或偿付利息支付的现金：反映企业实际支付给投资人的利润以及支付的借款利息、债券利息等 :mba
dividends_paid_to_minority_by_subsidiaries	double	其中:子公司支付给少数股东的股利、利润或偿付的利息
cash_paid_for_other_financing_activities	double	支付其他与筹资活动有关的现金：反映企业支付的其他与筹资活动有关的现金流出 :mba
cash_paid_to_financing_activities	double	筹资活动现金流出小计
cash_flow_from_financing_activities	double	筹资活动产生的现金流量净额：指企业接受投资和借入资金导致的现金流入和流出量 :mba
net_cash_deal_from_sub	double	处置子公司及其他营业单位收到的现金净额
net_cash_payment_from_sub	double	取得子公司及其他营业单位支付的现金净额
net_increase_in_pledge_loans	double	质押贷款净增加额
net_increase_from_investing_buy_back	double	返售业务资金净增加额(投资)
net_inc_cash_and_equivalents	double	现金及现金等价物净增加额（来源为财务附注）
fixed_asset_depreciation	double	固定资产折旧
deferred_expense_amortization	double	长期待摊费用摊销
intangible_asset_amortization	double	无形资产摊销
depreciation_per_share_lf	double	每股折旧和摊销lf
cash_ratio_lyr	double	现金比率lyr
cash_ratio_ttm	double	现金比率ttm
cash_ratio_lf	double	现金比率lf
cash_equivalent_per_share_lyr	double	每股货币资金lyr
cash_equivalent_per_share_ttm	double	每股货币资金ttm
cash_equivalent_per_share_lf	double	每股货币资金lf
dividend_amount_ly0	double	最近年度分红总额
dividend_amount_ly1	double	最近年度分红总额
dividend_amount_ly2	double	最近年度分红总额
dividend_amount_ttm0	double	最近四个季度分红总额
dividend_amount_ttm1	double	最近四个季度分红总额
dividend_amount_ttm2	double	最近四个季度分红总额
financial_asset_held_for_trading	double	企业为了近期内出售而持有的金融资产。通常情况下，以赚取差价为目的从二级市场购入的股票、债券和基金会分类为交易性金融资产 :mba :wikipedia
cash_equivalent	double	货币资金
client_deposits	double	其中:客户资金存款
bill_receivable	double	应收票据：指企业持有的还没有到期、尚未兑现的票据:mba
dividend_receivable	double	应收股利： 指企业因股权投资而应收取的现金股利以及应收其他单位的利润，不包括应收的股票股利 :mba
bill_accts_receivable	double	应收票据及应收账款
interest_receivable	double	应收利息：短期债券投资实际支付的价款中包含的已到付息期但尚未领取的债券利息 :mba
bad_debt_reserve	double	坏账准备：指对应收账款预提的，对不能收回或回收可能性极低的应收账款用来抵销，是应收账款的备抵账户 :mba
net_accts_receivable	double	应收账款净额
contract_assets	double	合同资产
prepayment	double	预付账款：企业因购货和接受劳务，按照合同规定预付给供应单位的款项 :mba
financial_receivable	double	应收款项融资
financial_lease_receivable	double	应收融资租赁款
other_equity_investment	double	其他权益工具投资
other_illiquidy_financial_assets	double	其他非流动金融资产
non_current_asset_due_one_year	double	一年内到期的非流动资产
other_receivables_interest_dividend	double	其他应收款(含利息和股利)
inventory	double	存货: 指企业在日常活动中持有的以备出售的产成品或商品、处在生产过程中的在产品、在生产过程或提供劳务过程中耗用的材料和物料等 :mba
consumable_biological_assets	double	消耗性生物资产
deferred_expense	double	待摊费用： 指支出先发生，费用归属后发生的事项，按照时间长短分为短期待摊费用和长期待摊费用 :mba
assets_hold_for_sale	double	划分为持有待售的资产
contract_work	double	工程施工： 工程施工是指按照设计图纸和相关文件的要求，在建设场地上将设计意图付诸实现的测量、作业、检验，形成工程实体建成最终产品的活动 :mba
other_current_assets	double	其他流动资产： 指除货币资金、短期投资、应收票据、应收账款、其他应收款、存货等流动资产以外的流动资产 :mba
current_assets	double	流动资产合计： 指企业可以在一年内或者超过一年的一个营业周期内变现或者耗用的资产 :mba
financial_asset_available_for_sale	double	可供出售金融资产： 指初始确认时即被指定为可供出售的非衍生金融资产，以及贷款和应收款项、持有至到期投资、交易性金融资产之外的非衍生金融资产 :mba
non_current_liability_due_one_year	double	一年内到期的非流动负债
debt_investment	double	债权投资
other_debt_investment	double	其他债权投资
financial_asset_hold_to_maturity	double	持有至到期投资： 指企业有明确意图并有能力持有至到期，到期日固定、回收金额固定或可确定的非衍生金融资产 :mba
real_estate_investment	double	投资性房地产： 指为赚取租金或资本增值，或两者兼有而持有的房地产 :mba
long_term_receivables	double	长期应收款： 长期应收款是根据长期应收款的账户余额减去未确认融资收益还有一年内到期的长期应收款 :mba
net_long_term_equity_investment	double	长期股权投资净额
accumulated_depreciation	double	累计折旧： "累计折旧"账户属于资产类的备抵调整账户，其结构与一般资产账户的结构刚好相反，贷方登记增加，借方登记减少，余额在贷方 :mba
depreciation_reserve	double	固定资产减值准备： 指由于固定资产市价持续下跌，或技术陈旧、损坏、长期闲置等原因导致其可收回金额低于账面价值的，应当将可收回金额低于其账面价值的差额作为固定资产减值准备 :mba
net_fixed_assets	double	固定资产净额： 固定资产原值减累计折旧再减减值准备后的差额 :mba
total_fixed_assets	double	固定资产合计
engineer_material	double	工程物资： 指用于固定资产建造的建筑材料，如钢材、水泥、玻璃等。在资产负债表中并入在建工程项目 :mba
construction_in_progress	double	在建工程： 指企业固定资产的新建、改建、扩建，或技术改造、设备更新和大修理工程等尚未完工的工程支出 :mba
total_construction_in_progress	double	在建工程合计
fixed_asset_to_be_disposed	double	固定资产清理： 指企业因出售、报废和毁损等原因转入清理的固定资产价值及其在清理过程中所发生的清理费用和清理收入等 :mba
capitalized_biological_assets	double	生产性生物资产： 指为产出农产品、提供劳务或出租等目的而持有的生物资产，包括经济林、薪炭林、产畜和役畜等 :mba
oil_and_gas_assets	double	油气资产： 指油气开采企业所拥有或控制的井及相关设施和矿区权益。油气资产属于递耗资产 :mba
intangible_assets	double	无形资产： 指企业拥有或者控制的没有实物形态的可辨认非货币性资产 :mba
seat_costs	double	交易席位费
impairment_intangible_assets	double	开发支出： 反映企业开发无形资产过程中能够资本化形成无形资产成本的支出部分 :mba
use_right_assets	double	使用权资产
goodwill	double	商誉： 指能在未来期间为企业经营带来超额利润的潜在经济价值，或一家企业预期的获利能力超过可辨认资产正常获利能力（如社会平均投资回报率）的资本化价值 :mba
long_term_deferred_expenses	double	长期待摊费用： 指企业已经支出，但摊销期限在 1 年以上(不含 1 年)的各项费用 :mba
deferred_income_tax_assets	double	递延所得税资产： 指对于可抵扣暂时性差异，以未来期间很可能取得用来抵扣可抵扣暂时性差异的应纳税所得额为限确认的一项资产 :mba
other_non_current_assets	double	其他非流动资产： 指除资产负债表上所列非流动资产项目以外的其他周转期超过 1 年的长期资产 :mba
non_current_assets	double	非流动资产合计
loan_account_receivables	double	投资-贷款及应收款项(应收款项类投资)
fund_providing	double	融出资金
reinsurance_reserve_receivable	double	应收分保合同准备金
settlement_provision	double	结算备付金
client_provision	double	客户备付金
interbank_deposits	double	存放同业款项
precious_metals	double	贵金属
lend_capital	double	拆出资金
derivative_financial_assets	double	衍生金融资产
resale_financial_assets	double	买入返售金融资产
loans_advances_to_customers	double	发放贷款和垫款
insurance_receivable	double	应收保费
subrogation_fee_receivable	double	应收代位追偿款
reinsurance_receivable	double	应收分保账款
unearned_reserve_receivable	double	应收分保未到期责任准备金
unclaimed_reserve_receivable	double	应收分保未决赔款准备金
life_reserve_receivable	double	应收分保寿险责任准备金
health_reserve_receivable	double	应收分保长期健康险责任准备金
insurer_mortgage_loan	double	保户质押贷款
fixed_deposits	double	定期存款
refundable_deposits	double	存出保证金
refundable_capital_deposits	double	存出资本保证金
independent_account_assets	double	独立账户资产
other_assets	double	其他资产
other_accts_receivable	double	其他应收款(原值)：是企业除应收票据、应收账款和预付账款以外的各种应收暂付款项
total_assets	double	总资产： 指企业拥有或可控制的能以货币计量的经济资源，包括各种财产、债权和其他权利 :mba
mortgaged_loan	double	质押借款
short_term_loans	double	短期借款： 还款期一年以下，企业用来维持正常的生产经营所需的资金或为抵偿某项债务而向银行或其他金融机构等外单位借入的资金 :mba
financial_liabilities	double	交易性金融负债： 交易性金融负债，指企业采用短期获利模式进行融资所形成的负债，比如应付短期债券 :others
notes_payable	double	应付票据： 应付票据是指企业购买材料、商品和接受劳务供应等而开出、承兑的商业汇票，包括商业承兑汇票和银行承兑汇票。在我国应收票据、应付票据仅指"商业汇票"，包括"银行承兑汇票"和"商业承兑汇票"两种，属于远期票据，付款期一般在 1 个月以上，6 个月以内 :mba
accts_payable	double	应付账款： 应付帐款是指企业因购买材料、物资和接受劳务供应等而付给供货单位的帐款 :mba
bill_accts_payable	double	应付票据及应付账款
contract_liabilities	double	合同负债
advance_from_customers	double	预收账款： 预收账款指买卖双方协议商定，由购货方预先支付一部分货款给供应方而发生的一项负债 :mba
payroll_payable	double	应付职工薪酬： 应付职工薪酬是指企业为获得职工提供的服务而给予各种形式的报酬以及其他相关支出 :mba
dividend_payable	double	应付股利： 应付股利是指企业根据年度利润分配方案，确定分配的股利 :mba
tax_payable	double	应交税费： 应交税费是指企业根据在一定时期内取得的营业收入、实现的利润等，按照现行税法规定，采用一定的计税方法计提的应交纳的各种税费 :mba
interest_payable	double	应付利息： 应付利息，是指金融企业根据存款或债券金额及其存续期限和规定的利率，按期计提应支付给单位和个人的利息 :investopedia
other_fees_payable	double	其他应交款： 指企业需要向国家缴纳的各项款项中除了税金以外的各种应交款项，主要包括教育附加费、车辆购置附加费等。 :others
other_payable	double	其他应付款： 该科目只核算企业应付其他单位或个人的零星款项，如应付经营租入固定资产和包装物的租金、存入保证金等 :mba
other_payable_interest_dividend	double	其他应付款（含利息和股利）
short_term_debt	double	应付短期债券： 应付短期债券是企业筹资发行一年以下期限的债券，属于流动负债 :others
accrued_expense	double	预提费用： 预提费用是指企业按规定预先提取但尚未实际支付的各项费用。 就是企业还没支付，但应该要支付的，要记入负债 :others
liabilities_hold_for_sale	double	划分为持有待售的负债
estimated_liabilities	double	预计负债： 预计负债是因或有事项可能产生的负债 :mba
deferred_income	double	递延收益： 递延收益是指尚待确认的收入或收益，也可以说是暂时未确认的收益，它是权责发生制在收益确认上的运用 :mba
long_term_liabilities_due_one_year	double	一年内到期的长期负债： 一年内到期的长期负债是指反映企业长期负债中自编表日起一年内到期的长期负债 :others【该数据来自旧会计准则】
other_current_liabilities	double	其他流动负债： 指不能归属于短期借款，应付短期债券券，应付票据，应付帐款，应付所得税，其他应付款，预收账款这七款项目的流动负债。但以上各款流动负债，其金额未超过流动负债合计金额百分之五者，得并入其他流动负债内 :others
current_liabilities	double	流动负债合计： 流动负债合计是指企业在一年内或超过一年的一个营业周期内需要偿还的债务 :mba
long_term_loans	double	长期借款： 长期借款是指企业从银行或其他金融机构借入的期限在一年以上(不含一年)的借款 :mba
bond_payable	double	应付债券： 公司为筹集长期资金而实际发行的债券及应付的利息 :mba
preference_shares	double	优先股
perpetual_bond	double	永续债（应付债券）
long_term_payable	double	长期应付款： 指企业除了长期借款和应付债券以外的长期负债，包括应付引进设备款、应付融资租入固定资产的租赁费等 :mba
accrued_staff_costs	double	长期应付职工薪酬
grants_received	double	专项应付款： 企业接受国家作为企业所有者拨入的具有专门用途的款项所形成的不需要以资产或增加其他负债偿还的负债 :others
housing_revolving_funds	double	住房周转金： 房周转金是指企业从各种规定来源取得的、用于职工住房各方面开支的，除公益金、住房折旧和住房公积金以外的住房基金 :mba
deferred_income_tax_liabilities	double	递延所得税负债： 指根据应纳税暂时性差异计算的未来期间应付所得税的金额 :mba
lease_liabilities	double	租赁负债
financial_lease_payable	double	应付融资租赁款
other_non_current_liabilities	double	其他非流动负债： 反映企业除长期借款、应付债券等项目以外的其他非流动负债 :mba
non_current_liabilities	double	非流动负债合计： 指偿还期在一年或者超过一年的一个营业周期以上的债务。非流动负债的主要项目有长期借款和应付债券 :mba
borrowings_from_central_banks	double	向中央银行借款
deposits_of_interbank	double	同业及其他金融机构存放款项
borrowings_capital	double	拆入资金
derivative_financial_liabilities	double	衍生金融负债
buy_back_security_proceeds	double	卖出回购金融资产款
deposits	double	吸收存款
proxy_security_proceeds	double	代理买卖证券款
sub_issue_security_proceeds	double	代理承销证券款
security_deposits_received	double	存入保证金
advance_insurance	double	预收保费
comission_payable	double	应付手续费及佣金
reinsurance_payable	double	应付分保账款
compensation_payable	double	应付赔付款
policy_dividend_payable	double	应付保单红利
deposits_from_interbank	double	吸收存款及同业存款
insurance_contract_reserve	double	保险合同准备金
insurer_deposit_investment	double	保户储金及投资款
uncertained_premium_reserve	double	未到期责任准备金
unclaimed_indemnity_reserve	double	未决赔款准备金
life_insurance_reserve	double	寿险责任准备金
health_insurance_reserve	double	长期健康险责任准备金
independent_account_liabilities	double	独立账户负债
other_liabilities	double	其他负债
deferred_revenue	double	递延收益(长期负债)： 递延收益是指尚待确认的收入或收益，也可以说是暂时未确认的收益，它是权责发生制在收益确认上的运用 :mba
total_liabilities	double	负债合计： 指企业所承担的能以货币计量，将以资产或劳务偿还的债务 :mba
paid_in_capital	double	实收资本(或股本)： 指企业的投资者按照企业章程或合同、协议的约定，实际投入企业的资本 :mba
other_equity_instruments	double	其他权益工具
equity_preferred_stock	double	权益部分的优先股
perpetual_equity_debt	double	永续债（其他权益工具）
capital_reserve	double	资本公积金： 企业收到的投资者的超出其在企业注册资本所占份额，以及直接计入所有者权益的利得和损失等 :mba【该数据来自旧会计准则】
surplus_reserve	double	盈余公积： 指企业从税后利润中提取形成的、存留于企业内部、具有特定用途的收益积累 :others
undistributed_profit	double	未分配利润： 未分配利润是企业未作分配的利润。它在以后年度可继续进行分配，在未进行分配之前，属于所有者权益的组成部分 :others
treasury_stock	double	减:库存股
equity_parent_company	double	归属于母公司所有者权益合计： 母公司股东权益反映的是母公司所持股份部分的所有者权益数 :others
total_equity	double	股东权益合计： 所有者权益合计是指企业投资人对企业净资产的所有权 :others
general_reserve	double	一般风险准备
trade_risk_allowances	double	交易风险准备
foreign_currency_converted_difference	double	外币报表折算差额
uncertained_impairment_losses	double	未确认投资损失
other_reserves	double	其他储备(公允价值变动储备)
specific_reserve	double	专项储备
minority_interest	double	少数股东权益： 少数股东损益是一个流量概念，是指公司合并报表的子公司其它非控股股东享有的损益 :mba
total_equity_and_liabilities	double	负债和股东权益总计
revenue	double	营业总收入：公司经营所取得的收入总额 金融类公司不公布营业总收入，因此 revenue 指标只能使用类似的一个指标-operating_revenue 来参考 :mba
operating_revenue	double	营业收入：公司经营主要业务所取得的收入总额 :mba
net_interest_income	double	利息净收入
net_commission_income	double	手续费及佣金净收入
commission_income	double	其中:手续费及佣金收入
commission_expense	double	其中:手续费及佣金支出
net_proxy_security_income	double	其中:代理买卖证券业务净收入
sub_issue_security_income	double	其中:证券承销业务净收入
net_trust_income	double	其中:受托客户资产管理业务净收入
earned_premiums	double	已赚保费
premiums_income	double	保险业务收入
reinsurance_income	double	其中:分保费收入
reinsurance	double	减:分出保费
unearned_premium_reserve	double	提取未到期责任准备金
total_expense	double	营业总成本
operating_expense	double	营业支出(金融类企业披露)
refunded_premiums	double	退保金
compensation_expense	double	赔付支出
amortization_expense	double	减:摊回赔付支出
premium_reserve	double	提取保险责任准备金
amortization_premium_reserve	double	减:摊回保险责任准备金
policy_dividend_payout	double	保单红利支出
reinsurance_cost	double	分保费用
other_operating_revenue	double	其他经营收入
other_operating_cost	double	其他经营成本
r_n_d	double	研发费用
other_net_income	double	非经营性净收益
net_open_hedge_income	double	净敞口套期收益
other_revenue	double	其他收益
credit_asset_impairment	double	信用资产减值损失
o_n_a_expense	double	业务及管理费用
amortization_reinsurance_cost	double	减:摊回分保费用
insurance_commission_expense	double	保险手续费及佣金支出
disposal_income_on_asset	double	资产处置收益
cost_of_goods_sold	double	营业成本(非金融类企业披露)：公司经营主要业务产生的实际成本 :mba
sales_tax	double	营业税 :mba
gross_profit	double	主营业务利润 :investopedia
selling_expense	double	销售费用：指企业在销售产品、自制半成品和工业性劳务等过程中发生的各项费用 :mba
ga_expense	double	管理费用：指企业的行政管理部门为管理和组织经营而发生的各项费用 :mba
financing_expense	double	财务费用： 指企业为筹集生产经营所需资金等而发生的费用，包括利息支出（减利息收入）、汇兑损失（减汇兑收益）以及相关的手续费等 :mba
financing_interest_income	double	利息收入（财务费用），财务费用科目下进一步细分的子会计科目
financing_interest_expense	double	利息支出（财务费用），财务费用科目下进一步细分的子会计科目
exchange_gains_or_losses	double	兑汇损益：发生外币交易后期末账户因此调整时，由于采用不同货币，或同一货币不同比价的汇率核算时产生的、按记账本位币折算的差额 :mba
profit_from_operation	double	营业利润： 企业在其全部销售业务中实现的利润，又称营业利润、经营利润，它包含主营业务利润 :mba
invest_income_associates	double	对联营合营企业的投资收益
fair_value_change_income	double	公允价值变动净收益
investment_income	double	投资收益：指企业进行投资所获得的经济利益 :mba
asset_impairment	double	资产减值损失
interest_income	double	利息收入
interest_expense	double	利息支出
non_operating_revenue	double	营业外收入：指企业发生的与其生产经营无直接关系的各项收入，包括固定资产盘盈、非货币性交易收益、出售无形资产收益等 :mba
non_operating_expense	double	营业外支出：企业发生的与其生产经营无直接关系的各项支出，如固定资产盘亏、债务重组损失、罚款支出、捐赠支出、非常损失等 :mba
disposal_loss_on_asset	double	非流动资产处置净损失：包括固定资产处置损失和无形资产出售损失 :mba
other_effecting_total_profits_items	double	影响利润总额的其他科目
profit_before_tax	double	利润总额： 指税前利润，也就是企业在所得税前一定时期内经营活动的总成果 :mba
income_tax	double	所得税：以纳税人的所得额为课税对象的各种税收的统称 :mba
unrealised_investment_loss	double	未确认的投资损失： 因母公司和子公司确认子公司损益方式不同而在合并报表中使用的一个调节性科目
other_effecting_net_profits_items	double	影响净利润的其他科目
net_profit	double	净利润（收益）是指在利润总额中按规定交纳了所得税以后公司的利润留存，一般也称为税后利润或净收入 :mba
non_recurring_pnl	double	非经常性损益
net_profit_deduct_non_recurring_pnl	double	扣除非经常性损益后的净利润
classified_by_continuity_operation	double	(一)按经营持续性分类
continuous_operation_net_profit	double	持续经营净利润
discontinued_operation_net_profit	double	终止经营净利润
classified_by_ownership	double	(二)按所有权归属分类
net_profit_parent_company	double	归属母公司净利润： 反映在企业合并净利润中，归属于母公司股东（所有者）所有的那部分净利润 :others
minority_profit	double	少数股东损益
other_income	double	其他综合收益：指企业根据企业会计准则规定未在损益中确认的各项利得和损失扣除所得税影响后的净额 :mba
other_income_unclassified_income_statement	double	(一)以后不能重分类进损益表的其他综合收益
remearsured_other_income	double	1.1 重新计量设定收益计划净负债或净资产的变动
other_income_equity_unclassified_income_statement	double	1.2 权益法下在被投资单位不能重分类进损益表的其他综合收益中享有的份额
other_equity_instruments_change	double	1.3 其他权益工具投资公允价值变动
corporate_credit_risk_change	double	1.4 企业自身信用风险公允价值变动
other_income_classified_income_statement	double	(二)以后能重分类进损益表的其他综合收益
other_income_equity_classified_income_statement	double	2.1 权益法下在被投资单位能重分类进损益表的其他综合收益中享有的份额
financial_asset_available_for_sale_change	double	2.2 可供出售金融资产公允价值变动损益
financial_asset_hold_to_maturity_change	double	2.3 持有至到期投资重分类为可供出售金融资产损益
cash_flow_hedging_effective_portion	double	2.4 现金流量套期损益的有效部分
foreign_currency_statement_converted_difference	double	2.5 外币财务报表分析折算差额
others	double	2.6 其他
other_debt_investment_change	double	2.7 其他债权投资公允价值变动
assets_reclassified_other_income	double	2.8 金融资产重分类计入其他综合收益的金额
other_debt_investment_reserve	double	2.9 其他债权投资信用减值准备
other_income_minority	double	归属于少数股东的其他综合收益总额
total_income	double	综合收益总额：反映企业净利润与其他综合收益的合计金额 :mba
total_income_parent_company	double	归属于母公司所有者的综合收益总额
total_income_minority	double	归属于少数股东的综合收益总额
basic_earnings_per_share	double	基本每股收益：本每股收益是指企业应当按照属于普通股股东的当期净利润，除以发行在外普通股的加权平均数从而计算出的每股收益 :mba
fully_diluted_earnings_per_share	double	稀释每股收益
adjust_asset_impairment	double	资产减值损失：根据财政部发布的《关于修订印发 2019 年度一般企业财务报表格式的通知》格式，“资产减值损失”不隶属于营业总成本部分。因企业披露不一致性，经研究，从 2020.07.08 披露的 2020 年半年报开始，字段数值按照原文披露展示，历史报告期维持原有规则。
adjust_credit_asset_impairment	double	信用减值损失：根据财政部发布的《关于修订印发 2019 年度一般企业财务报表格式的通知》格式，“信用减值损失”不隶属于营业总成本部分。因企业披露不一致性，经研究，从 2020.07.08 披露的 2020 年半年报开始，字段数值按照原文披露展示，历史报告期维持原有规则。
4.4. 使用示例

4.4.1. 获取单支股票的部分回测因子

import panda_data
result = panda_data.get_factor(
    symbol="000001.SZ",
    start_date="20250101",
    end_date="20250131",
    factors=['open', 'close'],
    index_component="100",
    type="stock"
)
print(result)
date symbol open close index_component
0 20250127 000001.SZ 1923.3110 1938.5218 100
1 20250124 000001.SZ 1913.1706 1916.5507 100
2 20250123 000001.SZ 1887.8194 1913.1706 100
3 20250122 000001.SZ 1913.1706 1874.2987 100
4 20250121 000001.SZ 1935.1416 1914.8606 100
5 20250120 000001.SZ 1943.5920 1930.0714 100
6 20250117 000001.SZ 1948.6622 1935.1416 100
7 20250116 000001.SZ 1952.0424 1955.4226 100
8 20250115 000001.SZ 1923.3110 1940.2118 100
9 20250114 000001.SZ 1892.8896 1923.3110 100
10 20250113 000001.SZ 1901.3400 1892.8896 100
11 20250110 000001.SZ 1926.6912 1909.7904 100
12 20250109 000001.SZ 1943.5920 1926.6912 100
13 20250108 000001.SZ 1943.5920 1943.5920 100
14 20250107 000001.SZ 1930.0714 1945.2821 100
15 20250106 000001.SZ 1923.3110 1933.4515 100
16 20250103 000001.SZ 1933.4515 1923.3110 100
17 20250102 000001.SZ 1982.4638 1931.7614 100
4.4.2. 获取多个期货的部分回测因子

import panda_data
result = panda_data.get_factor(
    symbol=["A_dominant.DCE", "ZN99.SHF"],
    start_date="20250101",
    end_date="20250131",
    factors=['open', 'close'],
    index_component="100",
    type="future"
)
print(result)
date symbol open close
0 20250127 A_dominant.DCE 4026.000000 4026.000000
1 20250124 A_dominant.DCE 4019.000000 4032.000000
2 20250123 A_dominant.DCE 4057.000000 4013.000000
3 20250122 A_dominant.DCE 4041.000000 4060.000000
4 20250121 A_dominant.DCE 4025.000000 4032.000000
5 20250120 A_dominant.DCE 4029.000000 4019.000000
6 20250117 A_dominant.DCE 3998.000000 4028.000000
7 20250116 A_dominant.DCE 3984.000000 4000.000000
8 20250115 A_dominant.DCE 3950.000000 3987.000000
9 20250114 A_dominant.DCE 3938.000000 3962.000000
10 20250113 A_dominant.DCE 3878.000000 3937.000000
11 20250109 A_dominant.DCE 3837.000000 3840.000000
12 20250108 A_dominant.DCE 3847.000000 3837.000000
13 20250107 A_dominant.DCE 3901.000000 3848.000000
14 20250106 A_dominant.DCE 3910.000000 3892.000000
15 20250103 A_dominant.DCE 3942.000000 3917.000000
16 20250102 A_dominant.DCE 3929.000000 3931.000000
17 20250127 ZN99.SHF 23868.645567 23649.747135
18 20250124 ZN99.SHF 23733.936502 23866.787628
19 20250123 ZN99.SHF 24057.276361 23699.230120
20 20250122 ZN99.SHF 24103.643674 24103.442670
21 20250121 ZN99.SHF 24202.884628 24182.237740
22 20250120 ZN99.SHF 24252.715221 24198.003126
23 20250117 ZN99.SHF 23756.282806 24204.240241
24 20250116 ZN99.SHF 23572.938956 23753.526911
25 20250115 ZN99.SHF 24103.828805 23541.263305
26 20250114 ZN99.SHF 24278.029376 24010.551340
27 20250113 ZN99.SHF 24267.122137 24248.561402
28 20250109 ZN99.SHF 24025.194931 24089.120930
29 20250108 ZN99.SHF 24335.637688 24189.688127
30 20250107 ZN99.SHF 24664.223102 24374.164898
31 20250106 ZN99.SHF 24487.481834 24464.454350
32 20250103 ZN99.SHF 24905.751147 24652.227822
33 20250102 ZN99.SHF 25216.137054 25229.964391
二、交易日历数据

1. 获取交易日历

1.1. 方法名：get_trading_calendar

1.2. 入参

字段	类型	描述	是否必填
start_date	Optional[str]	开始日期，格式为 YYYYMMDD	非必填
end_date	Optional[str]	结束日期，格式为 YYYYMMDD	非必填
exchange	Optional[str]	交易所代码，默认为 “SH”，目前支持"SH"和"HK"	非必填
is_trading_day	Optional[int]	是否为交易日，1=交易日，0=非交易日，None=全部	非必填
fields	Optional[Union[str, List[str]]]	需要返回的字段列表	非必填
1.3. 响应参数

字段	类型	描述
nature_date	int	日期，格式为YYYYMMDD
exchange	str	交易所代码
is_trade	int	是否为交易日，1表示交易日，0表示非交易日
pretrade_date	str	当前日期前一个交易日
next_trade_date	str	当前日期后一个交易日
1.4. 使用示例

1.4.1. 获取一段时间内上交所交易日历

import panda_data
result = panda_data.get_trading_calendar(
    start_date="20250101",
    end_date="20250115",
    exchange="SH",
    is_trading_day=None,
    fields=[]
)
print(result)
exchange is_trade nature_date pretrade_date next_trade_date
0 SH 0 20250101 20241231 20250102
1 SH 1 20250102 20241231 20250103
2 SH 1 20250103 20250102 20250106
3 SH 0 20250104 20250103 20250106
4 SH 0 20250105 20250103 20250106
5 SH 1 20250106 20250103 20250107
6 SH 1 20250107 20250106 20250108
7 SH 1 20250108 20250107 20250109
8 SH 1 20250109 20250108 20250110
9 SH 1 20250110 20250109 20250113
10 SH 0 20250111 20250110 20250113
11 SH 0 20250112 20250110 20250113
12 SH 1 20250113 20250110 20250114
13 SH 1 20250114 20250113 20250115
14 SH 1 20250115 20250114 20250116
1.4.2. 获取一段时间内港交所非交易日且使用fields

import panda_data
result = panda_data.get_trading_calendar(
    start_date="20241215",
    end_date="20250110",
    exchange="HK",
    is_trading_day=1,
    fields=["nature_date", "is_trade", "next_trade_date", "pretrade_date"]
)
print(result)
nature_date is_trade next_trade_date pretrade_date
0 20241216 1 20241217 20241213
1 20241217 1 20241218 20241216
2 20241218 1 20241219 20241217
3 20241219 1 20241220 20241218
4 20241220 1 20241223 20241219
5 20241223 1 20241224 20241220
6 20241224 1 20241227 20241223
7 20241227 1 20241230 20241224
8 20241230 1 20241231 20241227
9 20241231 1 20250102 20241230
10 20250102 1 20250103 20241231
11 20250103 1 20250106 20250102
12 20250106 1 20250107 20250103
13 20250107 1 20250108 20250106
14 20250108 1 20250109 20250107
15 20250109 1 20250110 20250108
16 20250110 1 20250113 20250109
1.4.3. 获取一段时间内上交所交易日

import panda_data
result = panda_data.get_trading_calendar(
    start_date="20250101",
    end_date="20250120",
    exchange="SH",
    is_trading_day=1,
    fields=[]
)
print(result)
exchange is_trade nature_date pretrade_date next_trade_date
0 SH 1 20250102 20241231 20250103
1 SH 1 20250103 20250102 20250106
2 SH 1 20250106 20250103 20250107
3 SH 1 20250107 20250106 20250108
4 SH 1 20250108 20250107 20250109
5 SH 1 20250109 20250108 20250110
6 SH 1 20250110 20250109 20250113
7 SH 1 20250113 20250110 20250114
8 SH 1 20250114 20250113 20250115
9 SH 1 20250115 20250114 20250116
10 SH 1 20250116 20250115 20250117
11 SH 1 20250117 20250116 20250120
12 SH 1 20250120 20250117 20250121
2. 获取某一日期前第n个交易日

2.1. 方法名：get_previous_trading_date

2.2. 入参

字段	类型	描述	是否必填
date	str	基准日期，格式为 “YYYYMMDD”	必填
exchange	Optional[str]	交易所代码，默认为 “SH”，目前支持"SH"和"HK"	非必填
n	int	前第n个交易日，默认为1	非必填
2.3. 响应参数

字段	类型	描述
date	str	第前n个交易日，格式 “YYYYMMDD”，如果没有则返回None
2.4. 使用示例

2.4.1. 获取上交所某一日期的前第5个交易日

import panda_data
result = panda_data.get_previous_trading_date(
    date="20250102",
    exchange="SH",
    n=5
)
print(result)
20241225
2.4.2. 获取港交所某一日期的前第5个交易日

import panda_data
result = panda_data.get_previous_trading_date(
    date="20250102",
    exchange="HK",
    n=5
)
print(result)
20241223
3. 获取最新交易日

3.1. 方法名：get_latest_trading_date

3.2. 入参

字段	类型	描述	是否必填
exchange	Optional[str]	交易所代码，默认为 “SH”，目前支持"SH"和"HK"	非必填
3.3. 响应参数

字段	类型	描述
date	str	最新交易日，格式 “YYYYMMDD”，如果没有则返回None
3.4. 使用示例

3.4.1. 获取上交所最新交易日

import panda_data
result = panda_data.get_latest_trading_date(
    exchange="SH"
)
print(result)
20251223
3.4.2. 获取港交所最新交易日

import panda_data
result = panda_data.get_latest_trading_date(
    exchange="HK"
)
print(result)
20251223
三、龙虎榜数据

1. 获取股票龙虎榜数据

1.1. 方法名：get_abnormal

1.2. 入参

字段	类型	描述	是否必填
symbol	Optional[Union[str, List[str]]]	股票代码，如 “000001.SZ”	非必填
type	Optional[Union[str, List[str]]]	龙虎榜类型	非必填
start_date	Optional[str]	开始日期，格式 “YYYYMMDD”	非必填
end_date	Optional[str]	结束日期，格式 “YYYYMMDD”	非必填
fields	Optional[Union[str, List[str]]]	需要返回的字段列表	非必填
1.3. 响应参数

字段	类型	描述
symbol	str	股票代码
date	str	龙虎榜日期
type	str	龙虎榜类型(见下表)
reason	str	龙虎榜原因
amount	double	龙虎榜金额
volume	double	龙虎榜数量
amplitude	double	龙虎榜振幅
change_rate	double	龙虎榜涨跌幅
deviation	double	龙虎榜涨跌幅偏离值
turnover	double	龙虎榜换手率
start_date	double	异动开始日期
end_date	str	异动结束日期
龙虎榜类型:

类型代码	描述
AP015	日价格振幅达15%
AP030	日价格振幅达30%
AP040	日价格振幅达40%
CL000	无价格涨跌幅限制
CP000	日涨跌幅达到20%
CS000	当日无价格涨跌幅限制的A股，出现异常波动停牌的
C0000	涨跌幅
CBB30	连续2个交易日触及涨跌幅限制,同营业部净买入占当日总成交量30%以上,且未公告
CMB30	连续2个交易日触及涨跌幅限制,同营业部净卖出占当日总成交量30%以上,且未公告
CTC00	连续三日触及价格涨跌幅限制
CAC00	连续三日达到价格涨跌幅限制
CCCC0	最近3个有成交的交易日以内收盘价涨跌幅累计达到+120%(-60%)
CCC2X	最近3个有成交的交易日以内收盘价涨跌幅累计达到+200%(-70%)
DCC40	最近3个有成交的交易日以内收盘价涨跌幅偏离值累计达到+40%(-40%)
D0000	涨跌幅偏离值
D0C00	三日涨跌幅偏离值
DSC00	三日涨跌幅偏离值(ST)
F0000	新股首日交易信息
Q0000	退市整理
S0000	实施特别停牌
VB050	当日融资买入数量达到当日该证券总交易量的50％以上
VM050	当日融券卖数量达到当日该证券总交易量的50％以上
N0J03	连续10个交易日内3次出现负向异常波动情形的证券
N0A03	严重异常期间3次出现负向异常波动情形的证券
N0J04	连续10个交易日内4次出现负向异常波动情形的证券
P0J03	连续10个交易日内3次出现正向异常波动情形的证券
P0A03	严重异常期间3次出现正向异常波动情形的证券
P0J04	连续10个交易日内4次出现正向异常波动情形的证券
O0000	其它异常波动的证券
R0000	风险警示期交易
T0020	日换手率达20%
T0C20	连续三个交易日内的日均换手率与前五个交易日日均换手率的比值到达30倍,并且该股票封闭式基金连续三个交易日内累计换手率达到20%
T0030	日换手率达30%
T0010	日换手率达10%
TR030	风险警示股票盘中换手率达到或超过30%
G0007	日涨幅偏离值达7%
GC015	日收盘价涨幅达15%
GCC12	连续三个交易日内，收盘价涨幅偏离值累计达到12%的ST证券、*ST证券
G0C20	连续三个交易日内，涨幅偏离值累计达20%
GCC30	连续3个交易日内日收盘价格涨幅偏离值累计达30%
G0C15	连续三个交易日内，涨幅偏离值累计达到15%（沪）或12%（深）的ST证券、*ST证券和未完成股改证券
GCJ1X	连续10个交易日内收盘价格涨幅偏离值累计达到100%的证券
GCZ2X	连续30个交易日内收盘价格涨幅偏离值累计达到200%的证券
GCA1X	严重异常期间日收盘价格涨幅偏离值累计达到100%的证券
GCA2X	严重异常期间日收盘价格涨幅偏离值累计达到200%的证券
L0007	日跌幅偏离值达7%
LC015	日收盘价跌幅达15%
LCA50	严重异常期间日收盘价格跌幅偏离值累计达到50%的证券
LCA70	严重异常期间日收盘价格跌幅偏离值累计达到70%的证券
LCC12	连续三个交易日内，收盘价跌幅偏离值累计达到12%的ST证券、*ST证券
L0C20	连续三个交易日内，跌幅偏离值累计达20%
LCC30	连续3个交易日内日收盘价格跌幅偏离值累计达30%
L0C15	连续三个交易日内，跌幅偏离值累计达到15%（沪）或12%（深）的ST证券、*ST证券和未完成股改证券
LCJ50	连续10个交易日内收盘价格跌幅偏离值累计达到-50%的证券
LCZ70	连续30个交易日内收盘价格跌幅偏离值累计达到-70%的证券
1.4. 使用示例

1.4.1. 获取一定日期内某一类型所有股票龙虎榜数据

import panda_data
result = panda_data.get_abnormal(
    start_date="20250101",
    end_date="20250131",
    type="G0007",
    symbol="",
    fields=[]
)
print(result)
date symbol type ... start_date turnover volume
0 20250116 000016.SZ G0007 ... 20250116 None 390440000.0
1 20250109 000063.SZ G0007 ... 20250109 None 391500000.0
2 20250103 000533.SZ G0007 ... 20250103 None 240090000.0
3 20250110 000573.SZ G0007 ... 20250110 None 265010000.0
4 20250122 000627.SZ G0007 ... 20250122 None 284190000.0
.. ... ... ... ... ... ... ...
170 20250123 605277.SH G0007 ... 20250123 None 3568019.0
171 20250122 605389.SH G0007 ... 20250122 None 4272238.0
172 20250127 605398.SH G0007 ... 20250127 None 1348103.0
173 20250123 605398.SH G0007 ... 20250123 None 18684754.0
174 20250122 605398.SH G0007 ... 20250122 None 10629766.0
1.4.2. 获取一定日期内某一股票所有龙虎榜数据且使用fields

import panda_data
result = panda_data.get_abnormal(
    symbol="001314.SZ",
    start_date="20250101",
    end_date="20250131",
    fields=["type", "deviation","start_date"],
    type=""
)
print(result)
symbol date type deviation start_date
0 001314.SZ 20250107 T0020 NaN 20250107
1 001314.SZ 20250103 T0020 NaN 20250103
2 001314.SZ 20250102 T0020 NaN 20250102
3 001314.SZ 20250102 G0007 0.1258 20250102
2. 获取股票龙虎榜明细数据

2.1. 方法名：get_abnormal_detail

2.2. 入参

字段	类型	描述	是否必填
symbol	Optional[Union[str, List[str]]] = None	股票代码，如 “000001.SZ”	非必填
type	Optional[Union[str, List[str]]]	龙虎榜类型	非必填
start_date	Optional[str]	开始日期，格式 “YYYYMMDD”	非必填
end_date	Optional[str]	结束日期，格式 “YYYYMMDD”	非必填
side	Optional[str]	买卖方向，可选值为 “buy” 或 “sell”	非必填
fields	Optional[Union[str, List[str]]]	需要返回的字段列表	非必填
2.3. 响应参数

字段	类型	描述
symbol	str	股票代码
date	str	龙虎榜日期
type	str	龙虎榜类型(同前)
side	str	买卖方向
rank	int	龙虎榜排名
agency	str	营业部名称
b_value	double	买入金额
s_value	double	卖出金额
reason	str	龙虎榜原因
2.4. 使用示例

2.4.1. 获取某只股票卖方向龙虎榜明细

import panda_data
result = panda_data.get_abnormal_detail(
    symbol="001314.SZ",
    start_date="20250101",
    end_date="20250131",
    type="T0020",
    side="sell",
    fields=[]
)
print(result)
date rank side symbol ... b_value reason s_value type
0 20250107 1 sell 001314.SZ ... 9264.0 日换手率达20% 65335573.0 T0020
1 20250107 2 sell 001314.SZ ... 87986.0 日换手率达20% 40823242.0 T0020
2 20250107 3 sell 001314.SZ ... 33731705.0 日换手率达20% 12017622.0 T0020
3 20250107 4 sell 001314.SZ ... 883470.0 日换手率达20% 11191385.0 T0020
4 20250107 5 sell 001314.SZ ... 283895.0 日换手率达20% 9456590.0 T0020
5 20250103 1 sell 001314.SZ ... 11702.0 日换手率达20% 61308405.7 T0020
6 20250103 2 sell 001314.SZ ... 13133584.0 日换手率达20% 39695456.0 T0020
7 20250103 3 sell 001314.SZ ... 7232734.0 日换手率达20% 37405572.0 T0020
8 20250103 4 sell 001314.SZ ... 4726659.0 日换手率达20% 34687595.4 T0020
9 20250103 5 sell 001314.SZ ... 546472.0 日换手率达20% 25320659.0 T0020
2.4.2. 获取某只股票买方向龙虎榜明细并使用fields

import panda_data
result = panda_data.get_abnormal_detail(
    symbol="001314.SZ",
    start_date="20250101",
    end_date="20250131",
    type="T0020",
    side="buy",
    fields=["symbol", "date", "type", "s_value", "reason"]
)
print(result)
date symbol reason s_value type
0 20250107 001314.SZ 日换手率达20% 2645439.12 T0020
1 20250107 001314.SZ 日换手率达20% 1135792.00 T0020
2 20250107 001314.SZ 日换手率达20% 0.00 T0020
3 20250107 001314.SZ 日换手率达20% 12017622.00 T0020
4 20250107 001314.SZ 日换手率达20% 0.00 T0020
5 20250103 001314.SZ 日换手率达20% 3272065.00 T0020
6 20250103 001314.SZ 日换手率达20% 6594875.00 T0020
7 20250103 001314.SZ 日换手率达20% 63272.00 T0020
8 20250103 001314.SZ 日换手率达20% 31370.00 T0020
9 20250103 001314.SZ 日换手率达20% 1564684.00 T0020
四、回购数据

1. 获取回购数据

1.1. 方法名：get_buy_back

1.2. 入参

字段	类型	描述	是否必填
symbol	Optional[Union[str, List[str]]]	股票代码	非必填
start_date	Optional[str]	日期，格式 “YYYYMMDD”	非必填
end_date	Optional[str]	日期，格式 “YYYYMMDD”	非必填
fields	Optional[Union[str, List[str]]]	需要返回的字段列表	非必填
1.3. 响应参数

字段	类型	描述
symbol	str	股票代码
date	str	日期，格式 “YYYYMMDD”
seller	str	股份被回购方
procedure	str	事件进程
share_type	str	股份类别
announcement_dt	datetime	公告发布当天的日期时间戳，格式 “YYYY-MM-DD HH:MM:SS.sss”
buy_back_start_date	str	回购期限起始日，格式 “YYYYMMDD”
buy_back_end_date	str	回购期限结束日，格式 “YYYYMMDD”
write_off_date	str	回购注销公告日，格式 “YYYYMMDD”
maturity_desc	str	股份回购期限说明
buy_back_volume	double	回购股数(股)(份)
volume_ceiling	double	回购数量上限(股)(份)
volume_floor	double	回购数量下限(股)(份)
buy_back_value	double	回购总金额(元)
buy_back_price	double	回购价格(元/股)(元/份)
price_ceiling	double	回购价格上限(元)
price_floor	double	回购价格下限(元)
currency	double	货币单位
purpose	str	回购目的
buy_back_percent	double	占总股本比例
value_floor	double	拟回购资金总额下限(元)
value_ceiling	double	拟回购资金总额上限(元)
buy_back_mode	str	股份回购方式
1.4. 使用示例

1.4.1. 获取一定日期内某只股票的回购数据

import panda_data
result = panda_data.get_buy_back(
    symbol="002011.SZ",
    start_date="20250101",
    end_date="20251231",
    fields=[]
)
print(result)
date symbol seller ... value_floor value_ceiling buy_back_mode
0 20251127 002011.SZ 8名激励对象 ... 1350000.0 1350000.0 协议回购
1.4.2. 获取一定日期内某只股票的回购数据且使用fields

import panda_data
result = panda_data.get_buy_back(
    symbol="002011.SZ",
    start_date="20250101",
    end_date="20251231",
    fields=["symbol", "seller", "date", "procedure"]
)
print(result)
date symbol seller procedure
0 20251127 002011.SZ 8名激励对象 预案
五、概念数据

1. 获取概念列表

1.1. 方法名：get_concept_list

1.2. 入参

字段	类型	描述	是否必填
concept	Optional[Union[str, List[str]]]	概念名称	非必填
start_date	Optional[str]	开始时间	非必填
end_date	Optional[str]	结束时间	非必填
1.3. 响应参数

字段	类型	描述
name	str	概念名称
date	str	概念纳入日期
1.4. 使用示例

1.4.1. 获取一定日期内某个概念的列表

import panda_data
result = panda_data.get_concept_list(
    start_date="20250101",
    end_date="20250131",
    concept="英伟达概念"
)
print(result)
name date
0 英伟达概念 20250117
2. 获取概念成分股

2.1. 方法名：get_concept_stock

2.2. 入参

字段	类型	描述	是否必填
concept	Optional[Union[str, List[str]]]	概念名称	非必填
concept_stock	Optional[Union[str, List[str]]]	股票代码	非必填
start_date	Optional[str]	开始时间	非必填
end_date	Optional[str]	结束时间	非必填
fields	Optional[Union[str, List[str]]]	返回字段	非必填
2.3. 响应参数

字段	类型	描述
concept	str	概念名称
concept_stock	str	概念成分股
date	str	股票纳入概念日期
2.4. 使用示例

2.4.1. 获取一定日期内某个概念成分股

import panda_data
result = panda_data.get_concept_stock(
    start_date="20250101",
    end_date="20250131",
    concept="英伟达概念",
    concept_stock="001339.SZ",
    fields=["concept", "concept_stock", "date"]
)
print(result)
concept_stock date concept
0 001339.SZ 20250117 英伟达概念
六、财务数据

1. 获取财务预测数据

1.1. 方法名：get_financial_forecast

1.2. 入参

字段	类型	描述	是否必填
symbol	Optional[Union[str, List[str]]]	股票代码，可以是单个字符串或字符串列表	非必填
fields	Optional[Union[str, List[str]]]	需要返回的字段列表	非必填
info_date	Optional[str]	信息发布日期，格式为 “YYYYMMDD”	非必填
end_quarter	Optional[str]	报告季度，格式为 “YYYYqN”	非必填
1.3. 响应参数

字段	类型	描述
symbol	str	股票代码
info_date	str	信息发布日期
end_date	str	报告日期
forecast_type	str	整体业绩预期
forecast_description	str	业绩预期时间段描述
forecast_growth_rate_floor	double	最小预期增长幅度
forecast_growth_rate_ceiling	double	最大预期增长幅度
forecast_earning_floor	double	最小预期收入
forecast_earning_ceiling	double	最大预期收入
forecast_np_floor	double	最小预期净利润
forecast_np_ceiling	double	最大预期净利润
forecast_eps_floor	double	最小预期每股
forecast_eps_ceiling	double	最大预期每股收益
net_profit_yoy_const_forecast	double	一致预期净利润增幅
1.4. 使用示例

1.4.1. 获取一定日期后某只股票的财务预测数据

import panda_data
result = panda_data.get_financial_forecast(
    symbol="688795.SH",
    info_date="20251128",
    end_quarter="2025q4",
    fields=[]
)
print(result)
symbol info_date ... forecast_type net_profit_yoy_const_forecast
0 688795.SH 20251128 ... 减亏 None
1.4.2. 获取一定日期后某只股票的财务预测数据且使用fields

import panda_data
result = panda_data.get_financial_forecast(
    symbol="688795.SH",
    info_date="20251128",
    end_quarter="2025q4",
    fields=["symbol", "info_date", "end_date", "report_type",
        "forecast_description", "forecast_growth_rate_ceiling", "forecast_type"]
    )
    print(result)
symbol info_date ... forecast_growth_rate_ceiling forecast_type
0 688795.SH 20251128 ... 54.89 减亏
2. 获取财务表现数据

2.1. 方法名：get_financial_performance

2.2. 入参

字段	类型	描述	是否必填
symbol	Optional[Union[str, List[str]]]	股票代码，可以是单个字符串或字符串列表	非必填
fields	Optional[List[str]]	需要返回的字段列表	非必填
info_date	Optional[str]	信息发布日期，格式为 “YYYYMMDD”	非必填
end_quarter	Optional[str]	报告季度，格式为 “YYYYqN”	非必填
2.3. 响应参数

字段	类型	描述
symbol	str	股票代码
info_date	str	信息发布日期
end_date	str	报告日期
operating_revenue	double	营业收入或主营业务收入(元)
gross_profit	double	主营业务利润(元)
operating_profit	double	营业利润(元)
total_profit	double	利润总额(元)
np_parent_owners	double	归属母公司净利润(元)
net_profit_cut	double	扣除非经常性损益后净利润(元)
net_operate_cashflow	double	经营活动现金流量净额(元)
total_assets	double	总资产(元)
se_without_minority	double	归属母公司普通股东权益(元)
se_parent_owners	double	归属母公司股东权益(元)
total_shares	double	总股本(股)
basic_eps	double	基本每股收益
eps_weighted	double	每股收益(加权)(元)
eps_cut_epscut	double	每股收益(扣除)(元)
eps_cut_weighted	double	每股收益(扣除加权)(元)
roe	double	净资产收益率(摊薄)(%)
roe_weighted	double	净资产收益率(加权)(%)
roe_cut	double	净资产收益率(扣除摊薄)(%)
roe_cut_weighted	double	净资产收益率(扣除加权)(%)
net_operate_cashflow_per_share	double	每股经营活动现金流量净额(元)
equity_per_share	double	每股净资产(元)
operating_revenue_yoy	double	主营业务收入同比(%)
gross_profit_yoy	double	主营业务利润同比(%)
operating_profit_yoy	double	营业利润同比(%)
total_profit_yoy	double	利润总额同比(%)
np_parent_minority_pany_yoy	double	归属母公司净利润同比(%)
ne_t_minority_ty_yoy	double	扣除非经常性损益后净利润同比(%)
net_operate_cash_flow_yoy	double	经营活动现金流量净额同比(%)
total_assets_to_opening	double	总资产较期初比(%)
se_without_minority_to_opening	double	归属母公司股东权益较期初比(%)
basic_eps_yoy	double	每股收益(摊薄) 同比(%)
eps_weighted_yoy	double	每股收益(加权) 同比(%)
eps_cut_yoy	double	每股收益(扣除) 同比(%)
eps_cut_weighted_yoy	double	每股收益(扣除加权) 同比(%)
roe_yoy	double	净资产收益率(摊薄) 同比(%)
roe_weighted_yoy	double	净资产收益率(加权) 同比(%)
roe_cut_yoy	double	净资产收益率(扣除摊薄) 同比(%)
roe_cut_weighted_yoy	double	净资产收益率(扣除加权) 同比(%)
net_operate_cash_flow_per_share_yoy	double	每股经营活动现金流量净额同比(%)
net_asset_psto_opening	double	每股净资产较期初比(%)
2.4. 使用示例

2.4.1. 获取一定日期内某只股票的财务表现数据

import panda_data
result = panda_data.get_financial_performance(
    info_date="20251107",
    symbol="688235.SH",
    end_quarter="2025q4"
)
print(result)
info_date symbol basic_eps ... total_profit total_profit_yoy total_shares
0 20251107 688235.SH 0.81 ... 1.543219e+09 145.23766 None
2.4.2. 获取一定日期内某只股票的财务表现数据且使用fields

import panda_data
result = panda_data.get_financial_performance(
    info_date="20251107",
    symbol="688235.SH",
    end_quarter="2025q4",
    fields=["symbol", "info_date", "end_date", "basic_eps", "eps_cut_epscut",
        "ne_t_minority_ty_yoy", "np_parent_owners"]
    )
    print(result)
info_date symbol ... ne_t_minority_ty_yoy np_parent_owners
0 20251107 688235.SH ... 124.295951 1.138596e+09
3. 获取财务季度报告

3.1. 方法名：get_financial_ex

3.2. 入参

字段	类型	描述	是否必填
symbol	Optional[Union[str, list]]	股票名称	非必填
start_quarter	Optional[str]	起始季度，格式为 “YYYYqN”	非必填
end_quarter	Optional[str]	结束季度，格式为 “YYYYqN”	非必填
date	Optional[str]	公告日期(默认返回当日及之前的数据)	非必填
is_latest	bool	True：返回最新披露数据，False：返回全部。默认为True	非必填
fields	Optional[Union[str, list]]	返回字段	非必填
3.3. 响应参数

3.3.1. 响应参数

字段	类型	描述
symbol	str	股票代码
fields	double	需要返回的财务字段(见数据库设计)
quarter	str	季度
if_adjusted	int	是否为当期财报数据，0为当期，1为非当期
3.3.2. fields里的财务字段

字段名	中文名称	详细描述	来源
revenue	营业总收入	公司经营所取得的收入总额 金融类公司不公布营业总收入，因此 revenue 指标只能使用类似的一个指标-operating_revenue 来参考	mba
operating_revenue	营业收入	公司经营主要业务所取得的收入总额	mba
net_interest_income	利息净收入	-	-
net_commission_income	手续费及佣金净收入	-	-
commission_income	手续费及佣金收入	其中:手续费及佣金收入	-
commission_expense	手续费及佣金支出	其中:手续费及佣金支出	-
net_proxy_security_income	代理买卖证券业务净收入	其中:代理买卖证券业务净收入	-
sub_issue_security_income	证券承销业务净收入	其中:证券承销业务净收入	-
net_trust_income	受托客户资产管理业务净收入	其中:受托客户资产管理业务净收入	-
earned_premiums	已赚保费	-	-
premiums_income	保险业务收入	-	-
reinsurance_income	分保费收入	其中:分保费收入	-
reinsurance	分出保费	减:分出保费	-
unearned_premium_reserve	未到期责任准备金	提取未到期责任准备金	-
total_expense	营业总成本	-	-
refunded_premiums	退保金	-	-
compensation_expense	赔付支出	-	-
amortization_expense	摊回赔付支出	减:摊回赔付支出	-
premium_reserve	保险责任准备金	提取保险责任准备金	-
amortization_premium_reserve	摊回保险责任准备金	减:摊回保险责任准备金	-
policy_dividend_payout	保单红利支出	-	-
reinsurance_cost	分保费用	-	-
other_operating_revenue	其他经营收入	-	-
other_operating_cost	其他经营成本	-	-
r_n_d	研发费用	-	-
other_net_income	非经营性净收益	-	-
net_open_hedge_income	净敞口套期收益	-	-
other_revenue	其他收益	-	-
credit_asset_impairment	信用资产减值损失	-	-
o_n_a_expense	业务及管理费用	-	-
amortization_reinsurance_cost	摊回分保费用	减:摊回分保费用	-
insurance_commission_expense	保险手续费及佣金支出	-	-
disposal_income_on_asset	资产处置收益	-	-
cost_of_goods_sold	营业成本	公司经营主要业务产生的实际成本(非金融类企业披露)	mba
sales_tax	营业税	-	mba
gross_profit	主营业务利润	-	investopedia
selling_expense	销售费用	指企业在销售产品、自制半成品和工业性劳务等过程中发生的各项费用	mba
ga_expense	管理费用	指企业的行政管理部门为管理和组织经营而发生的各项费用	mba
financing_expense	财务费用	指企业为筹集生产经营所需资金等而发生的费用，包括利息支出（减利息收入）、汇兑损失（减汇兑收益）以及相关的手续费等	mba
financing_interest_income	利息收入(财务费用)	财务费用科目下进一步细分的子会计科目	-
financing_interest_expense	利息支出(财务费用)	财务费用科目下进一步细分的子会计科目	-
exchange_gains_or_losses	兑汇损益	发生外币交易后期末账户因此调整时，由于采用不同货币，或同一货币不同比价的汇率核算时产生的、按记账本位币折算的差额	mba
profit_from_operation	营业利润	企业在其全部销售业务中实现的利润，又称营业利润、经营利润，它包含主营业务利润	mba
invest_income_associates	对联营合营企业的投资收益	-	-
fair_value_change_income	公允价值变动净收益	-	-
investment_income	投资收益	指企业进行投资所获得的经济利益	mba
asset_impairment	资产减值损失	-	-
interest_income	利息收入	-	-
interest_expense	利息支出	-	-
non_operating_revenue	营业外收入	指企业发生的与其生产经营无直接关系的各项收入，包括固定资产盘盈、非货币性交易收益、出售无形资产收益等	mba
non_operating_expense	营业外支出	企业发生的与其生产经营无直接关系的各项支出，如固定资产盘亏、债务重组损失、罚款支出、捐赠支出、非常损失等	mba
disposal_loss_on_asset	非流动资产处置净损失	包括固定资产处置损失和无形资产出售损失	mba
other_effecting_total_profits_items	影响利润总额的其他科目	-	-
profit_before_tax	利润总额	指税前利润，也就是企业在所得税前一定时期内经营活动的总成果	mba
income_tax	所得税	以纳税人的所得额为课税对象的各种税收的统称	mba
other_effecting_net_profits_items	影响净利润的其他科目	-	-
net_profit	净利润	指在利润总额中按规定交纳了所得税以后公司的利润留存，一般也称为税后利润或净收入	mba
non_recurring_pnl	非经常性损益	-	-
net_profit_deduct_non_recurring_pnl	扣除非经常性损益后的净利润	-	-
classified_by_continuity_operation	按经营持续性分类	(一)按经营持续性分类	-
continuous_operation_net_profit	持续经营净利润	-	-
discontinued_operation_net_profit	终止经营净利润	-	-
classified_by_ownership	按所有权归属分类	(二)按所有权归属分类	-
net_profit_parent_company	归属母公司净利润	反映在企业合并净利润中，归属于母公司股东（所有者）所有的那部分净利润	others
minority_profit	少数股东损益	-	-
other_income	其他综合收益	指企业根据企业会计准则规定未在损益中确认的各项利得和损失扣除所得税影响后的净额	mba
other_income_unclassified_income_statement	以后不能重分类进损益表的其他综合收益	(一)以后不能重分类进损益表的其他综合收益	-
remearsured_other_income	重新计量设定收益计划净负债或净资产的变动	1.1 重新计量设定收益计划净负债或净资产的变动	-
other_income_equity_unclassified_income_statement	权益法下在被投资单位不能重分类进损益表的其他综合收益中享有的份额	1.2 权益法下在被投资单位不能重分类进损益表的其他综合收益中享有的份额	-
other_equity_instruments_change	其他权益工具投资公允价值变动	1.3 其他权益工具投资公允价值变动	-
corporate_credit_risk_change	企业自身信用风险公允价值变动	1.4 企业自身信用风险公允价值变动	-
other_income_classified_income_statement	以后能重分类进损益表的其他综合收益	(二)以后能重分类进损益表的其他综合收益	-
other_income_equity_classified_income_statement	权益法下在被投资单位能重分类进损益表的其他综合收益中享有的份额	2.1 权益法下在被投资单位能重分类进损益表的其他综合收益中享有的份额	-
financial_asset_available_for_sale_change	可供出售金融资产公允价值变动损益	2.2 可供出售金融资产公允价值变动损益	-
financial_asset_hold_to_maturity_change	持有至到期投资重分类为可供出售金融资产损益	2.3 持有至到期投资重分类为可供出售金融资产损益	-
cash_flow_hedging_effective_portion	现金流量套期损益的有效部分	2.4 现金流量套期损益的有效部分	-
foreign_currency_statement_converted_difference	外币财务报表分析折算差额	2.5 外币财务报表分析折算差额	-
others	其他	2.6 其他	-
other_debt_investment_change	其他债权投资公允价值变动	2.7 其他债权投资公允价值变动	-
assets_reclassified_other_income	金融资产重分类计入其他综合收益的金额	2.8 金融资产重分类计入其他综合收益的金额	-
other_debt_investment_reserve	其他债权投资信用减值准备	2.9 其他债权投资信用减值准备	-
other_income_minority	归属于少数股东的其他综合收益总额	-	-
total_income	综合收益总额	反映企业净利润与其他综合收益的合计金额	mba
total_income_parent_company	归属于母公司所有者的综合收益总额	-	-
total_income_minority	归属于少数股东的综合收益总额	-	-
basic_earnings_per_share	基本每股收益	本每股收益是指企业应当按照属于普通股股东的当期净利润，除以发行在外普通股的加权平均数从而计算出的每股收益	mba
fully_diluted_earnings_per_share	稀释每股收益	-	-
adjust_asset_impairment	资产减值损失	根据财政部发布的《关于修订印发 2019 年度一般企业财务报表格式的通知》格式，“资产减值损失”不隶属于营业总成本部分。因企业披露不一致性，经研究，从 2020.07.08 披露的 2020 年半年报开始，字段数值按照原文披露展示，历史报告期维持原有规则。	-
adjust_credit_asset_impairment	信用减值损失	根据财政部发布的《关于修订印发 2019 年度一般企业财务报表格式的通知》格式，“信用减值损失”不隶属于营业总成本部分。因企业披露不一致性，经研究，从 2020.07.08 披露的 2020 年半年报开始，字段数值按照原文披露展示，历史报告期维持原有规则。	-
cash_received_from_sales_of_goods	销售商品、提供劳务收到的现金	公司销售商品、提供劳务实际收到的现金	investopedia
refunds_of_taxes	收到的税费返还	公司按规定收到的增值税、所得税等税费返还额	mba
net_deposit_increase	客户存款和同业存放款项净增加额	-	-
net_increase_from_central_bank	向中央银行借款净增加额	-	-
net_increase_from_other_financial_institutions	向其他金融机构拆入资金净增加额	-	-
draw_back_canceled_loans	收回已核销贷款	-	-
cash_received_from_interests_and_commissions	收取利息、手续费及佣金的现金	-	-
net_increase_from_disposing_financial_assets	处置交易性金融资产净增加额	-	-
net_increase_from_repurchasing_business	回购业务资金净增加额	-	-
cash_received_from_original_insurance	收到原保险合同保费取得的现金	-	-
cash_received_from_reinsurance	收到再保业务现金净额	-	-
net_increase_from_insurer_deposit_investment	保户储金及投资款净增加额	-	-
net_increase_from_financial_institutions	拆入资金净增加额	-	-
cash_received_from_proxy_security	代理买卖证券收到的现金净额	-	-
cash_received_from_sub_issue_security	代理承销证券收到的现金净额	-	-
cash_from_other_operating_activities	收到其它与经营活动有关的现金	公司除了上述各项目外，收到的其他与经营活动有关的现金，如捐赠现金收入、罚款收入、流动资产损失中由个人赔偿的现金收入等	mba
cash_from_operating_activities	经营活动现金流入小计	-	-
cash_paid_for_goods_and_services	购买商品、接受劳务支付的现金	公司购买商品、接受劳务实际支付的现金	investopedia
assets_depreciation_reserves	资产减值准备	-	-
exchange_rate_change_effect	汇率变动对现金及现金等价物的影响	-	-
other_effecting_cash_equivalent_items	影响现金及现金等价物的其他科目	-	-
cash_equivalent_increase	现金及现金等价物净增加额	来源现金流量表主表	-
begin_period_cash_equivalent	期初现金及现金等价物余额	加:期初现金及现金等价物余额	-
end_period_cash_equivalent	期末现金及现金等价物余额	-	-
cash_paid_for_employee	支付给职工以及为职工支付的现金	公司实际支付给职工，以及为职工支付的现金，包括本期实际支付给职工的工资、奖金、各种津贴和补贴等	mba
cash_paid_for_taxes	支付的各项税费	反映企业按规定支付的各种税费，包括本期发生并支付的税费，以及本期支付以前各期发生的税费和预交的税金等	mba
net_increase_from_loans_and_advances	客户贷款及垫款净增加额	-	-
net_increase_from_central_bank_and_banks	存放中央银行和同业款项净增加额	-	-
net_increase_from_lending_capital	拆出资金净增加额	-	-
cash_paid_for_comissions	支付手续费及佣金的现金	-	-
cash_paid_for_orignal_insurance	支付原保险合同赔付款项的现金	-	-
cash_paid_for_reinsurance	支付再保业务现金净额	-	-
cash_paid_for_policy_dividends	支付保单红利的现金	-	-
net_increase_from_trading_financial_assets	为交易目的而持有的金融资产净增加额	-	-
net_increase_from_operating_buy_back	返售业务资金净增加额(经营)	-	-
cash_paid_for_other_operation_activities	支付其他与经营活动有关的现金	反映企业支付的其他与经营活动有关的现金支出，如罚款支出、支付的差旅费、业务招待费的现金支出、支付的保险费等	mba
cash_paid_for_operation_activities	经营活动现金流出小计	-	-
cash_flow_from_operating_activities	经营活动产生的现金流量净额	指企业投资活动和筹资活动以外的所有交易活动和事项的现金流入和流出量	mba
cash_received_from_investment	取得投资收益收到的现金	-	-
cash_received_from_disposal_of_asset	处置固定资产、无形资产和其他长期资产收回的现金净额	公司处置固定资产、无形资产和其他长期资产收回的现金	investopedia
cash_received_from_other_investment_activities	收到其他与投资活动有关的现金	公司除了上述各项以外，收到的其他与投资活动有关的现金	mba
cash_received_from_investment_activities	投资活动现金流入小计	-	-
cash_paid_for_asset	购建固定资产、无形资产和其他长期资产所支付的现金	-	wikipedia
cash_paid_to_acquire_investment	投资支付的现金	反映企业进行权益性投资和债权性投资支付的现金，包括企业取得的除现金等价物以外的股票投资和债券投资等支付的现金等	mba
cash_paid_for_other_investment_activities	支付其他与投资活动有关的现金	反映企业除了上述各项以外，支付的其他与投资活动有关的现金流出	mba
cash_paid_for_investment_activities	投资活动现金流出小计	-	-
cash_flow_from_investing_activities	投资活动产生的现金流量净额	指企业长期资产的购建和对外投资活动（不包括现金等价物范围的投资）的现金流入和流出量	mba
cash_received_from_investors	吸收投资收到的现金	反映企业收到的投资者投入现金，包括以发行股票、债券等方式筹集的资金实际收到的净额	mba
cash_received_from_minority_invest_subsidiaries	子公司吸收少数股东投资收到的现金	其中:子公司吸收少数股东投资收到的现金	-
cash_received_from_issuing_security	发行债券收到的现金	-	-
cash_received_from_financial_institution_borrows	取得借款收到的现金	公司向银行或其他金融机构等借入的资金	mba
cash_received_from_issuing_equity_instruments	发行其他权益工具收到的现金	-	-
net_increase_from__financing_buy_back	回购业务资金净增加额(筹资)	-	-
cash_received_from_other_financing_activities	收到其他与筹资活动有关的现金	反映企业收到的其他与筹资活动有关的现金流入，如接受现金捐赠等	mba
cash_received_from_financing_activities	筹资活动现金流入小计	-	-
cash_paid_for_debt	偿还债务支付的现金	公司以现金偿还债务的本金，包括偿还银行或其他金融机构等的借款本金、偿还债券本金等	mba
cash_paid_for_dividend_and_interest	分配股利、利润或偿付利息支付的现金	反映企业实际支付给投资人的利润以及支付的借款利息、债券利息等	mba
dividends_paid_to_minority_by_subsidiaries	子公司支付给少数股东的股利、利润或偿付的利息	其中:子公司支付给少数股东的股利、利润或偿付的利息	-
cash_paid_for_other_financing_activities	支付其他与筹资活动有关的现金	反映企业支付的其他与筹资活动有关的现金流出	mba
cash_paid_to_financing_activities	筹资活动现金流出小计	-	-
cash_flow_from_financing_activities	筹资活动产生的现金流量净额	指企业接受投资和借入资金导致的现金流入和流出量	mba
net_cash_deal_from_sub	处置子公司及其他营业单位收到的现金净额	-	-
net_cash_payment_from_sub	取得子公司及其他营业单位支付的现金净额	-	-
net_increase_in_pledge_loans	质押贷款净增加额	-	-
net_increase_from_investing_buy_back	返售业务资金净增加额(投资)	-	-
net_inc_cash_and_equivalents	现金及现金等价物净增加额	来源为财务附注	-
fixed_asset_depreciation	固定资产折旧	-	-
deferred_expense_amortization	长期待摊费用摊销	-	-
intangible_asset_amortization	无形资产摊销	-	-
financial_asset_held_for_trading	交易性金融资产	企业为了近期内出售而持有的金融资产。通常情况下，以赚取差价为目的从二级市场购入的股票、债券和基金会分类为交易性金融资产	mba, wikipedia
cash_equivalent	货币资金	-	-
client_deposits	客户资金存款	其中:客户资金存款	-
bill_receivable	应收票据	指企业持有的还没有到期、尚未兑现的票据	mba
dividend_receivable	应收股利	指企业因股权投资而应收取的现金股利以及应收其他单位的利润，不包括应收的股票股利	mba
bill_accts_receivable	应收票据及应收账款	-	-
interest_receivable	应收利息	短期债券投资实际支付的价款中包含的已到付息期但尚未领取的债券利息	mba
bad_debt_reserve	坏账准备	指对应收账款预提的，对不能收回或回收可能性极低的应收账款用来抵销，是应收账款的备抵账户	mba
net_accts_receivable	应收账款净额	-	-
contract_assets	合同资产	-	-
prepayment	预付账款	企业因购货和接受劳务，按照合同规定预付给供应单位的款项	mba
financial_receivable	应收款项融资	-	-
financial_lease_receivable	应收融资租赁款	-	-
other_equity_investment	其他权益工具投资	-	-
other_illiquidy_financial_assets	其他非流动金融资产	-	-
non_current_asset_due_one_year	一年内到期的非流动资产	-	-
other_receivables_interest_dividend	其他应收款(含利息和股利)	-	-
inventory	存货	指企业在日常活动中持有的以备出售的产成品或商品、处在生产过程中的在产品、在生产过程或提供劳务过程中耗用的材料和物料等	mba
consumable_biological_assets	消耗性生物资产	-	-
deferred_expense	待摊费用	指支出先发生，费用归属后发生的事项，按照时间长短分为短期待摊费用和长期待摊费用	mba
assets_hold_for_sale	划分为持有待售的资产	-	-
contract_work	工程施工	工程施工是指按照设计图纸和相关文件的要求，在建设场地上将设计意图付诸实现的测量、作业、检验，形成工程实体建成最终产品的活动	mba
other_current_assets	其他流动资产	指除货币资金、短期投资、应收票据、应收账款、其他应收款、存货等流动资产以外的流动资产	mba
current_assets	流动资产合计	指企业可以在一年内或者超过一年的一个营业周期内变现或者耗用的资产	mba
financial_asset_available_for_sale	可供出售金融资产	指初始确认时即被指定为可供出售的非衍生金融资产，以及贷款和应收款项、持有至到期投资、交易性金融资产之外的非衍生金融资产	mba
non_current_liability_due_one_year	一年内到期的非流动负债	-	-
debt_investment	债权投资	-	-
other_debt_investment	其他债权投资	-	-
financial_asset_hold_to_maturity	持有至到期投资	指企业有明确意图并有能力持有至到期，到期日固定、回收金额固定或可确定的非衍生金融资产	mba
real_estate_investment	投资性房地产	指为赚取租金或资本增值，或两者兼有而持有的房地产	mba
long_term_receivables	长期应收款	长期应收款是根据长期应收款的账户余额减去未确认融资收益还有一年内到期的长期应收款	mba
net_long_term_equity_investment	长期股权投资净额	-	-
accumulated_depreciation	累计折旧	"累计折旧"账户属于资产类的备抵调整账户，其结构与一般资产账户的结构刚好相反，贷方登记增加，借方登记减少，余额在贷方	mba
depreciation_reserve	固定资产减值准备	指由于固定资产市价持续下跌，或技术陈旧、损坏、长期闲置等原因导致其可收回金额低于账面价值的，应当将可收回金额低于其账面价值的差额作为固定资产减值准备	mba
net_fixed_assets	固定资产净额	固定资产原值减累计折旧再减减值准备后的差额	mba
total_fixed_assets	固定资产合计	-	-
engineer_material	工程物资	指用于固定资产建造的建筑材料，如钢材、水泥、玻璃等。在资产负债表中并入在建工程项目	mba
construction_in_progress	在建工程	指企业固定资产的新建、改建、扩建，或技术改造、设备更新和大修理工程等尚未完工的工程支出	mba
total_construction_in_progress	在建工程合计	-	-
fixed_asset_to_be_disposed	固定资产清理	指企业因出售、报废和毁损等原因转入清理的固定资产价值及其在清理过程中所发生的清理费用和清理收入等	mba
capitalized_biological_assets	生产性生物资产	指为产出农产品、提供劳务或出租等目的而持有的生物资产，包括经济林、薪炭林、产畜和役畜等	mba
oil_and_gas_assets	油气资产	指油气开采企业所拥有或控制的井及相关设施和矿区权益。油气资产属于递耗资产	mba
intangible_assets	无形资产	指企业拥有或者控制的没有实物形态的可辨认非货币性资产	mba
seat_costs	交易席位费	-	-
impairment_intangible_assets	开发支出	反映企业开发无形资产过程中能够资本化形成无形资产成本的支出部分	mba
use_right_assets	使用权资产	-	-
goodwill	商誉	指能在未来期间为企业经营带来超额利润的潜在经济价值，或一家企业预期的获利能力超过可辨认资产正常获利能力（如社会平均投资回报率）的资本化价值	mba
long_term_deferred_expenses	长期待摊费用	指企业已经支出，但摊销期限在 1 年以上(不含 1 年)的各项费用	mba
deferred_income_tax_assets	递延所得税资产	指对于可抵扣暂时性差异，以未来期间很可能取得用来抵扣可抵扣暂时性差异的应纳税所得额为限确认的一项资产	mba
other_non_current_assets	其他非流动资产	指除资产负债表上所列非流动资产项目以外的其他周转期超过 1 年的长期资产	mba
non_current_assets	非流动资产合计	-	-
loan_account_receivables	投资-贷款及应收款项	应收款项类投资	-
fund_providing	融出资金	-	-
reinsurance_reserve_receivable	应收分保合同准备金	-	-
settlement_provision	结算备付金	-	-
client_provision	客户备付金	-	-
interbank_deposits	存放同业款项	-	-
precious_metals	贵金属	-	-
lend_capital	拆出资金	-	-
derivative_financial_assets	衍生金融资产	-	-
resale_financial_assets	买入返售金融资产	-	-
loans_advances_to_customers	发放贷款和垫款	-	-
insurance_receivable	应收保费	-	-
subrogation_fee_receivable	应收代位追偿款	-	-
reinsurance_receivable	应收分保账款	-	-
unearned_reserve_receivable	应收分保未到期责任准备金	-	-
unclaimed_reserve_receivable	应收分保未决赔款准备金	-	-
life_reserve_receivable	应收分保寿险责任准备金	-	-
health_reserve_receivable	应收分保长期健康险责任准备金	-	-
insurer_mortgage_loan	保户质押贷款	-	-
fixed_deposits	定期存款	-	-
refundable_deposits	存出保证金	-	-
refundable_capital_deposits	存出资本保证金	-	-
independent_account_assets	独立账户资产	-	-
other_assets	其他资产	-	-
other_accts_receivable	其他应收款(原值)	是企业除应收票据、应收账款和预付账款以外的各种应收暂付款项	-
total_assets	总资产	指企业拥有或可控制的能以货币计量的经济资源，包括各种财产、债权和其他权利	mba
mortgaged_loan	质押借款	-	-
short_term_loans	短期借款	还款期一年以下，企业用来维持正常的生产经营所需的资金或为抵偿某项债务而向银行或其他金融机构等外单位借入的资金	mba
financial_liabilities	交易性金融负债	交易性金融负债，指企业采用短期获利模式进行融资所形成的负债，比如应付短期债券	others
notes_payable	应付票据	应付票据是指企业购买材料、商品和接受劳务供应等而开出、承兑的商业汇票，包括商业承兑汇票和银行承兑汇票。在我国应收票据、应付票据仅指"商业汇票"，包括"银行承兑汇票"和"商业承兑汇票"两种，属于远期票据，付款期一般在 1 个月以上，6 个月以内	mba
accts_payable	应付账款	应付帐款是指企业因购买材料、物资和接受劳务供应等而付给供货单位的帐款	mba
bill_accts_payable	应付票据及应付账款	-	-
contract_liabilities	合同负债	-	-
advance_from_customers	预收账款	预收账款指买卖双方协议商定，由购货方预先支付一部分货款给供应方而发生的一项负债	mba
payroll_payable	应付职工薪酬	应付职工薪酬是指企业为获得职工提供的服务而给予各种形式的报酬以及其他相关支出	mba
dividend_payable	应付股利	应付股利是指企业根据年度利润分配方案，确定分配的股利	mba
tax_payable	应交税费	应交税费是指企业根据在一定时期内取得的营业收入、实现的利润等，按照现行税法规定，采用一定的计税方法计提的应交纳的各种税费	mba
interest_payable	应付利息	应付利息，是指金融企业根据存款或债券金额及其存续期限和规定的利率，按期计提应支付给单位和个人的利息	investopedia
other_fees_payable	其他应交款	指企业需要向国家缴纳的各项款项中除了税金以外的各种应交款项，主要包括教育附加费、车辆购置附加费等	others
other_payable	其他应付款	该科目只核算企业应付其他单位或个人的零星款项，如应付经营租入固定资产和包装物的租金、存入保证金等	mba
other_payable_interest_dividend	其他应付款(含利息和股利)	-	-
short_term_debt	应付短期债券	应付短期债券是企业筹资发行一年以下期限的债券，属于流动负债	others
accrued_expense	预提费用	预提费用是指企业按规定预先提取但尚未实际支付的各项费用。就是企业还没支付，但应该要支付的，要记入负债	others
liabilities_hold_for_sale	划分为持有待售的负债	-	-
estimated_liabilities	预计负债	预计负债是因或有事项可能产生的负债	mba
deferred_income	递延收益	递延收益是指尚待确认的收入或收益，也可以说是暂时未确认的收益，它是权责发生制在收益确认上的运用	mba
long_term_liabilities_due_one_year	一年内到期的长期负债	一年内到期的长期负债是指反映企业长期负债中自编表日起一年内到期的长期负债 (该数据来自旧会计准则)	others
other_current_liabilities	其他流动负债	指不能归属于短期借款，应付短期债券券，应付票据，应付帐款，应付所得税，其他应付款，预收账款这七款项目的流动负债。但以上各款流动负债，其金额未超过流动负债合计金额百分之五者，得并入其他流动负债内	others
current_liabilities	流动负债合计	流动负债合计是指企业在一年内或超过一年的一个营业周期内需要偿还的债务	mba
long_term_loans	长期借款	长期借款是指企业从银行或其他金融机构借入的期限在一年以上(不含一年)的借款	mba
bond_payable	应付债券	公司为筹集长期资金而实际发行的债券及应付的利息	mba
preference_shares	优先股	-	-
perpetual_bond	永续债(应付债券)	-	-
long_term_payable	长期应付款	指企业除了长期借款和应付债券以外的长期负债，包括应付引进设备款、应付融资租入固定资产的租赁费等	mba
accrued_staff_costs	长期应付职工薪酬	-	-
grants_received	专项应付款	企业接受国家作为企业所有者拨入的具有专门用途的款项所形成的不需要以资产或增加其他负债偿还的负债	others
housing_revolving_funds	住房周转金	房周转金是指企业从各种规定来源取得的、用于职工住房各方面开支的，除公益金、住房折旧和住房公积金以外的住房基金	mba
deferred_income_tax_liabilities	递延所得税负债	指根据应纳税暂时性差异计算的未来期间应付所得税的金额	mba
lease_liabilities	租赁负债	-	-
financial_lease_payable	应付融资租赁款	-	-
other_non_current_liabilities	其他非流动负债	反映企业除长期借款、应付债券等项目以外的其他非流动负债	mba
non_current_liabilities	非流动负债合计	指偿还期在一年或者超过一年的一个营业周期以上的债务。非流动负债的主要项目有长期借款和应付债券	mba
borrowings_from_central_banks	向中央银行借款	-	-
deposits_of_interbank	同业及其他金融机构存放款项	-	-
borrowings_capital	拆入资金	-	-
derivative_financial_liabilities	衍生金融负债	-	-
buy_back_security_proceeds	卖出回购金融资产款	-	-
deposits	吸收存款	-	-
proxy_security_proceeds	代理买卖证券款	-	-
sub_issue_security_proceeds	代理承销证券款	-	-
security_deposits_received	存入保证金	-	-
advance_insurance	预收保费	-	-
comission_payable	应付手续费及佣金	-	-
reinsurance_payable	应付分保账款	-	-
compensation_payable	应付赔付款	-	-
policy_dividend_payable	应付保单红利	-	-
deposits_from_interbank	吸收存款及同业存款	-	-
insurance_contract_reserve	保险合同准备金	-	-
insurer_deposit_investment	保户储金及投资款	-	-
uncertained_premium_reserve	未到期责任准备金	-	-
unclaimed_indemnity_reserve	未决赔款准备金	-	-
life_insurance_reserve	寿险责任准备金	-	-
health_insurance_reserve	长期健康险责任准备金	-	-
independent_account_liabilities	独立账户负债	-	-
other_liabilities	其他负债	-	-
deferred_revenue	递延收益(长期负债)	递延收益是指尚待确认的收入或收益，也可以说是暂时未确认的收益，它是权责发生制在收益确认上的运用	mba
total_liabilities	负债合计	指企业所承担的能以货币计量，将以资产或劳务偿还的债务	mba
paid_in_capital	实收资本(或股本)	指企业的投资者按照企业章程或合同、协议的约定，实际投入企业的资本	mba
other_equity_instruments	其他权益工具	-	-
equity_preferred_stock	权益部分的优先股	-	-
perpetual_equity_debt	永续债(其他权益工具)	-	-
capital_reserve	资本公积金	企业收到的投资者的超出其在企业注册资本所占份额，以及直接计入所有者权益的利得和损失等 (该数据来自旧会计准则)	mba
surplus_reserve	盈余公积	指企业从税后利润中提取形成的、存留于企业内部、具有特定用途的收益积累	others
undistributed_profit	未分配利润	未分配利润是企业未作分配的利润。它在以后年度可继续进行分配，在未进行分配之前，属于所有者权益的组成部分	others
treasury_stock	库存股	减:库存股	-
equity_parent_company	归属于母公司所有者权益合计	母公司股东权益反映的是母公司所持股份部分的所有者权益数	others
total_equity	股东权益合计	所有者权益合计是指企业投资人对企业净资产的所有权	others
general_reserve	一般风险准备	-	-
trade_risk_allowances	交易风险准备	-	-
foreign_currency_converted_difference	外币报表折算差额	-	-
uncertained_impairment_losses	未确认投资损失	-	-
other_reserves	其他储备	公允价值变动储备	-
specific_reserve	专项储备	-	-
minority_interest	少数股东权益	少数股东损益是一个流量概念，是指公司合并报表的子公司其它非控股股东享有的损益	mba
total_equity_and_liabilities	负债和股东权益总计	-	-
3.4. 使用示例

3.4.1. 获取一定季度内某只股票的财务季度报告

import panda_data
result = panda_data.get_financial_ex(
    symbol="688795.SH",
    date="20251114",
    start_quarter="2024q1",
    end_quarter="2026q1",
    is_latest=True,
    fields=[]
)
print(result)
date quarter ... unearned_reserve_receivable use_right_assets
0 20251114 2025q3 ... None 19234252.47
1 20250905 2025q2 ... None 19931500.00
2 20250919 2025q2 ... None 19931513.58
3 20250926 2025q2 ... None 19931513.58
4 20251030 2025q2 ... None 19931513.58
5 20251114 2025q2 ... None 19931513.58
6 20250630 2024q4 ... None 17260038.22
7 20250905 2024q4 ... None 17260000.00
8 20250919 2024q4 ... None 17260038.22
9 20250926 2024q4 ... None 17260038.22
10 20251030 2024q4 ... None 17260038.22
11 20251114 2024q4 ... None 17260038.22
12 20251114 2024q3 ... None NaN
13 20251114 2024q2 ... None NaN
14 20250630 2023q4 ... None 23230058.22
15 20250905 2023q4 ... None 23230100.00
16 20250919 2023q4 ... None 23230058.22
17 20250926 2023q4 ... None 23230058.22
18 20251030 2023q4 ... None 23230058.22
19 20251114 2023q4 ... None 23230058.22
20 20250630 2022q4 ... None 29251682.47
21 20250905 2022q4 ... None 29251700.00
22 20250919 2022q4 ... None 29251682.47
23 20250926 2022q4 ... None 29251682.47
24 20251030 2022q4 ... None 29251682.47
25 20251114 2022q4 ... None 29251682.47
1.4.2. 获取一定季度内某只股票的财务季度报告且使用fields

import panda_data
result = panda_data.get_financial_ex(
    symbol="688795.SH",
    date="20251114",
    start_quarter="2024q1",
    end_quarter="2026q1",
    is_latest=True,
    fields=["symbol", "date", "quarter", "adjust_credit_asset_impairment", "accts_payable",
        "cash_from_operating_activities", "cash_from_other_operating_activities"]
    )
    print(result)
date ... cash_from_other_operating_activities
0 20251114 ... 2.777510e+08
1 20250905 ... 2.242624e+08
2 20250919 ... 2.242624e+08
3 20250926 ... 2.242624e+08
4 20251030 ... 2.242624e+08
5 20251114 ... 2.242624e+08
6 20250630 ... 9.349225e+07
7 20250905 ... 9.349220e+07
8 20250919 ... 9.349225e+07
9 20250926 ... 9.349225e+07
10 20251030 ... 9.349225e+07
11 20251114 ... 9.349225e+07
12 20251114 ... 8.178976e+07
13 20251114 ... NaN
14 20250630 ... 2.189290e+08
15 20250905 ... 2.189290e+08
16 20250919 ... 2.189290e+08
17 20250926 ... 2.189290e+08
18 20251030 ... 2.189290e+08
19 20251114 ... 2.189290e+08
20 20250630 ... 9.503041e+06
21 20250905 ... 9.503000e+06
22 20250919 ... 9.503041e+06
23 20250926 ... 9.503041e+06
24 20251030 ... 9.503041e+06
25 20251114 ... 9.503041e+06
七、基金数据

1. 获取所有基金数据

1.1. 方法名：get_all_funds

1.2. 入参

字段	类型	描述	是否必填
symbol	Optional[Union[str, List[str]]]	基金代码	非必填
fields	Optional[Union[str, List[str]]]	返回字段	非必填
1.3. 响应参数

字段	类型	描述
symbol	str	基金代码
name	str	基金名称
list_date	str	上市日期
delist_date	str	退市日期
due_date	str	到期日期
found_date	str	成立日期
issue_date	str	发行日期
purc_startdate	str	日常申购起始日
redm_startdate	str	日常赎回起始日
duration_year	double	存续期
exp_return	double	预期收益率
management	str	管理人
custodian	str	托管人
fund_type	str	投资类型
issue_amount	double	发行份额（亿）
min_amount	double	起点金额（万元）
m_fee	double	管理费
c_fee	double	托管费
p_value	double	面值
benchmark	str	业绩比较基准
status	str	存续状态：D摘牌 I发行 L已上市
invest_type	str	投资风格
type	str	基金类型
market	str	E场内O场外
1.4. 使用示例

1.4.1. 获取某只基金的所有数据

import panda_data
result = panda_data.get_all_funds(
    symbol="025321.OF",
    fields=[]
)
print(result)
symbol benchmark ... trustee type
0 025321.OF 中债综合全价(总值)指数收益率*88%+中证红利低波动指数收益率*10%+中证港股通高股息投... ... None 契约型开放式
1.4.2. 获取某只基金的所有数据且使用fields

import panda_data
result = panda_data.get_all_funds(
    symbol="025321.OF",
    fields=["symbol", "benchmark", "c_fee", "custodian", "issue_date"]
)
print(result)
symbol ... issue_date
0 025321.OF ... 20251117
2. 获取基金持仓数据

2.1. 方法名：get_fund_pro

2.2. 入参

字段	类型	描述	是否必填
symbol	Optional[Union[str, List[str]]]	基金代码	非必填
start_date	Optional[str]	开始日期,eg:“20250702”	非必填
end_date	Optional[str]	结束日期,eg:“20250702”	非必填
fields	Optional[Union[str, List[str]]]	返回字段	非必填
2.3. 响应参数

字段	类型	描述
symbol	str	基金代码
ann_date	str	公布日期
end_date	str	截止日期
stock_symbol	str	股票代码
mkv	double	持有股票市值(元)
amount	double	持有股票数量（股）
stk_mkv_ratio	double	占股票市值比
stk_float_ratio	double	占流通股本比例
2.4. 使用示例

2.4.1. 获取一定日期某只基金的持仓数据

import panda_data
result = panda_data.get_fund_pro(
    symbol="016267.OF",
    start_date="20250101",
    end_date="20250131",
    fields=[]
)
print(result)
end_date symbol stock_symbol ... mkv stk_float_ratio stk_mkv_ratio
0 20241231 016267.OF 603086.SH ... 527296.0 0.03 0.47
1 20241231 016267.OF 300907.SZ ... 582808.0 0.03 0.52
2 20241231 016267.OF 688252.SH ... 603061.0 0.01 0.54
3 20241231 016267.OF 601777.SH ... 703035.0 0.00 0.62
4 20241231 016267.OF 000088.SZ ... 1218474.0 0.01 1.08
5 20241231 016267.OF 600968.SH ... 1564955.0 0.00 1.39
6 20241231 016267.OF 600959.SH ... 1583210.0 0.01 1.41
7 20241231 016267.OF 002500.SZ ... 1625892.0 0.01 1.45
8 20241231 016267.OF 000401.SZ ... 1632283.0 0.02 1.45
9 20241231 016267.OF 600418.SH ... 1736250.0 0.00 1.54
10 20241231 016267.OF 002625.SZ ... 1835520.0 0.00 1.63
11 20241231 016267.OF 600704.SH ... 1850948.0 0.01 1.65
12 20241231 016267.OF 300529.SZ ... 1989252.0 0.01 1.77
13 20241231 016267.OF 000728.SZ ... 2388452.0 0.01 2.12
14 20241231 016267.OF 600352.SH ... 2497383.0 0.01 2.22
2.4.2. 获取一定日期某只基金的持仓数据且使用fields

import panda_data
result = panda_data.get_fund_pro(
    symbol="016267.OF",
    start_date="20250101",
    end_date="20250131",
    fields=["symbol", "ann_date", "amount", "stock_symbol"]
)
print(result)
symbol stock_symbol ann_date amount
0 016267.OF 603086.SH 20250121 123200.0
1 016267.OF 300907.SZ 20250121 27700.0
2 016267.OF 688252.SH 20250121 25180.0
3 016267.OF 601777.SH 20250121 91900.0
4 016267.OF 000088.SZ 20250121 250200.0
5 016267.OF 600968.SH 20250121 366500.0
6 016267.OF 600959.SH 20250121 472600.0
7 016267.OF 002500.SZ 20250121 258900.0
8 016267.OF 000401.SZ 20250121 312100.0
9 016267.OF 600418.SH 20250121 46300.0
10 016267.OF 002625.SZ 20250121 38400.0
11 016267.OF 600704.SH 20250121 365800.0
12 016267.OF 300529.SZ 20250121 67800.0
13 016267.OF 000728.SZ 20250121 285700.0
14 016267.OF 600352.SH 20250121 242700.0
3. 获取基金净值日线数据

3.1. 方法名：get_fund_nav

3.2. 入参

字段	类型	描述	是否必填
symbol	Optional[Union[str, List[str]]]	基金代码	非必填
start_date	Optional[str]	开始日期,eg:“20250702”	非必填
end_date	Optional[str]	结束日期,eg:“20250702”	非必填
fields	Optional[Union[str, List[str]]]	返回字段	非必填
3.3. 响应参数

字段	类型	描述
symbol	str	基金代码
ann_date	str	公布日期
nav_date	str	净值日期
unit_nav	double	单位净值
accum_nav	double	累计净值
accum_div	double	累计分红
net_asset	double	资产净值
total_netasset	double	合计资产净值
adj_nav	double	复权单位净值
3.4. 使用示例

3.4.1. 获取一定日期某只基金的净值日线数据

import panda_data
result = panda_data.get_fund_nav(
    symbol="016267.OF",
    start_date="20250101",
    end_date="20250131",
    fields=[]
)
print(result)
nav_date ann_date symbol ... total_netasset unit_nav update_flag
0 20250127 20250128 016267.OF ... NaN 0.9946 0
1 20250124 20250125 016267.OF ... NaN 1.0015 0
2 20250123 20250124 016267.OF ... NaN 0.9917 0
3 20250122 20250123 016267.OF ... NaN 0.9955 0
4 20250121 20250122 016267.OF ... NaN 1.0004 0
5 20250120 20250121 016267.OF ... NaN 0.9999 0
6 20250117 20250118 016267.OF ... NaN 0.9960 0
7 20250116 20250117 016267.OF ... NaN 0.9865 0
8 20250115 20250116 016267.OF ... NaN 0.9832 0
9 20250114 20250115 016267.OF ... NaN 0.9892 0
10 20250113 20250114 016267.OF ... NaN 0.9579 0
11 20250110 20250111 016267.OF ... NaN 0.9566 0
12 20250109 20250110 016267.OF ... NaN 0.9675 0
13 20250108 20250109 016267.OF ... NaN 0.9691 0
14 20250107 20250108 016267.OF ... NaN 0.9716 0
15 20250106 20250107 016267.OF ... NaN 0.9611 0
16 20250103 20250104 016267.OF ... NaN 0.9618 0
17 20250102 20250103 016267.OF ... NaN 0.9824 0
18 20241231 20250101 016267.OF ... NaN 1.0106 0
19 20241231 20250121 016267.OF ... 1.263648e+08 1.0106 1
3.4.2. 获取一定日期某只基金的净值日线数据且使用fields

import panda_data
result = panda_data.get_fund_nav(
    symbol="016267.OF",
    start_date="20250101",
    end_date="20250131",
    fields=["symbol", "nav_date", "ann_date", "accum_nav"]
)
print(result)
nav_date ann_date symbol accum_nav
0 20250127 20250128 016267.OF 0.9946
1 20250124 20250125 016267.OF 1.0015
2 20250123 20250124 016267.OF 0.9917
3 20250122 20250123 016267.OF 0.9955
4 20250121 20250122 016267.OF 1.0004
5 20250120 20250121 016267.OF 0.9999
6 20250117 20250118 016267.OF 0.9960
7 20250116 20250117 016267.OF 0.9865
8 20250115 20250116 016267.OF 0.9832
9 20250114 20250115 016267.OF 0.9892
10 20250113 20250114 016267.OF 0.9579
11 20250110 20250111 016267.OF 0.9566
12 20250109 20250110 016267.OF 0.9675
13 20250108 20250109 016267.OF 0.9691
14 20250107 20250108 016267.OF 0.9716
15 20250106 20250107 016267.OF 0.9611
16 20250103 20250104 016267.OF 0.9618
17 20250102 20250103 016267.OF 0.9824
18 20241231 20250101 016267.OF 1.0106
19 20241231 20250121 016267.OF 1.0106
八、期货数据

1. 获取期货基本信息

1.1. 方法名：get_future_list

1.2. 入参

字段	类型	描述	是否必填
symbol	Optional[Union[str, List[str]]]	期货代码	非必填
fields	Optional[Union[str, List[str]]]	返回字段列表	非必填
is_trading	Optional[int]	是否可交易	非必填
1.3. 响应参数

字段	类型	描述
symbol	str	期货代码
listed_date	str	上市日期
de_listed_date	str	退市日期
maturity_date	str	到期日期
start_delivery_date	str	开始交割日期
end_delivery_date	str	结束交割日期
contract_multiplier	double	合约乘数
exchange	str	交易所
industry_name	str	行业分类名称
margin_rate	double	最低保证金率
market_tplus	double	交易制度，0表示T+0，以此类推
name	str	合约简称
product	str	合约种类，Commodity对应商品期货，Index对应股指期货，Government对应国债期货
round_lot	double	合约单位，均为1.0
trading_code	str	交易代码
trading_hours	str	交易时间
type	str	合约类型,均为Future
underlying_symbol	str	合约标的名称
is_trading	int	是否可交易，1表示可交易，0表示不可交易
1.4. 使用示例

1.4.1. 获取某些期货的基本信息

import panda_data
result = panda_data.get_future_list(
    symbol=["A0303", "ZN_DOMINANT"],
    fields=[],
    is_trading=None
)
print(result)
symbol contract_multiplier ... underlying_symbol is_trading
0 A0303.DCE 10.0 ... A 0
1 ZN_DOMINANT.SHF 5.0 ... ZN 1
1.4.2. 获取某些在交易的期货的基本信息且使用fields

import panda_data
result = panda_data.get_future_list(
    symbol=["A0303","ZN888"],
    fields=["symbol", "listed_date", "contract_multiplier","product"],
    is_trading= 1
)
print(result)
symbol contract_multiplier listed_date product is_trading
0 ZN888.SHF 5.0 0000-00-00 Commodity 1
2. 获取期货后复权数据

2.1. 方法名：get_future_market_post

2.2. 入参

字段	类型	描述	是否必填
symbol	Optional[Union[str, List[str]]]	期货代码	非必填
start_date	Optional[str]	开始日期,eg:“20250702” （查询上市日期）	非必填
end_date	Optional[str]	结束日期,eg:“20250702” （查询上市日期）	非必填
fields	Optional[Union[str, List[str]]]	返回字段列表	非必填
2.3. 响应参数

字段	类型	描述
symbol	str	期货代码
date	str	日期
amount	double	成交额
close	double	收盘价
day_session_open	double	日盘开盘价
dominant_id	str	主力合约代码
exchange	str	交易所
high	double	最高价
limit_down	double	跌停价
limit_up	double	涨停价
low	double	最低价
open	double	开盘价
open_interest	double	累计持仓量
pre_settlement	double	昨日结算价
settlement	double	结算价
trading_code	str	交易代码
underlying_symbol	str	合约标的代码
volume	double	成交量
2.4. 使用示例

2.4.1. 获取一定日期内某些期货的后复权数据

import panda_data
result = panda_data.get_future_market_post(
    symbol=["A2511", "P2607","A_DOMINANT"],
    start_date="20251101",
    end_date="20251105",
    fields=[]
)
print(result)
date symbol close ... volume pre_settlement amount
0 20251105 A2511.DCE 4048.0 ... 12.0 4053.0 4.861100e+05
1 20251104 A2511.DCE 4044.0 ... 351.0 4090.0 1.422784e+07
2 20251103 A2511.DCE 4076.0 ... 75.0 4082.0 3.067820e+06
3 20251105 A_DOMINANT.DCE 4123.0 ... 217199.0 4076.0 8.857064e+09
4 20251104 A_DOMINANT.DCE 4055.0 ... 135914.0 4092.0 5.539860e+09
5 20251103 A_DOMINANT.DCE 4076.0 ... 155379.0 4095.0 6.358720e+09
6 20251105 P2607.DCE 8650.0 ... 36.0 8686.0 3.120200e+06
7 20251104 P2607.DCE 8644.0 ... 41.0 8670.0 3.561680e+06
8 20251103 P2607.DCE 8658.0 ... 32.0 8738.0 2.774500e+06
2.4.2. 获取一定日期内某些期货的后复权数据且使用fields

import panda_data
result = panda_data.get_future_market_post(
    symbol=["A2511","P2607"],
    start_date="20251101",
    end_date="20251105",
    fields=["symbol", "amount", "close","high"],
)
print(result)
date symbol close high amount
0 20251105 A2511.DCE 4048.0 4052.0 486110.0
1 20251104 A2511.DCE 4044.0 4084.0 14227840.0
2 20251103 A2511.DCE 4076.0 4098.0 3067820.0
3 20251105 P2607.DCE 8650.0 8692.0 3120200.0
4 20251104 P2607.DCE 8644.0 8732.0 3561680.0
5 20251103 P2607.DCE 8658.0 8712.0 2774500.0
九、指数数据

1. 获取指数基本信息

1.1. 方法名：get_index_symbol

1.2. 入参

字段	类型	描述	是否必填
symbol	Optional[Union[str, List[str]]]	指数代码	非必填
fields	Optional[Union[str, List[str]]]	返回字段列表	非必填
status	Optional[str]	指数状态(1：正常交易，0：已退市，-1：暂无信息)	非必填
1.3.响应参数

字段名	类型	描述
symbol	str	指数代码
abbrev_symbol	str	指数简称
de_listed_date	str	退市日期
listed_date	str	上市日期
market_tplus	double	交易制度
min_order_amount	double	最小交易单位
name	str	指数名称
status	int	指数状态
trading_hours	str	交易时间
1.4. 使用示例

1.4.1. 获取所有指数基本信息

import panda_data
result = panda_data.get_index_symbol(
    symbol="",
    status=None,
    fields=[]
)
print(result)
symbol abbrev_symbol ... status trading_hours
0 000001.SH SZZS ... 1 09:31-11:30,13:01-15:00
1 000002.SH AGZS ... 1 09:31-11:30,13:01-15:00
2 000003.SH BGZS ... 1 09:31-11:30,13:01-15:00
3 000004.SH GYZS ... 1 09:31-11:30,13:01-15:00
4 000005.SH SYZS ... 1 09:31-11:30,13:01-15:00
... ... ... ... ... ...
1375 H50065.SH SHBK2 ... 1 09:31-11:30,13:01-15:00
1376 H50066.SH HGAHYJ ... 1 09:31-11:30,13:01-15:00
1377 H50067.SH 180ERC ... 1 09:31-11:30,13:01-15:00
1378 H50068.SH 380ERC ... 1 09:31-11:30,13:01-15:00
1379 H50069.SH GGT ... 1 09:31-11:30,13:01-15:00
1.4.2. 获取单个指数基本信息并使用fields

import panda_data
result = panda_data.get_index_symbol(
    symbol="000001.SH",
    status=1,
    fields=["symbol", "abbrev_symbol", "name", "trading_hours"]
)
print(result)
symbol abbrev_symbol name status trading_hours
0 000001.SH SZZS 上证指数 1 09:31-11:30,13:01-15:00
2. 获取指数估值指标

2.1. 方法名：get_index_indicator

2.2. 入参

字段	类型	描述	是否必填
symbol	Optional[Union[str, List[str]]]	指数代码	非必填
start_date	Optional[str]	开始日期,eg:“20250702”	非必填
end_date	Optional[str]	结束日期,eg:“20250702”	非必填
fields	Optional[Union[str, List[str]]]	返回字段列表	非必填
2.3. 响应参数

字段名	类型	描述
date	str	日期
symbol	str	指数代码
pb_lf	double	市净率(LF)
pb_lyr	double	市净率(LYR)
pb_ttm	double	市净率(TTM)
pe_lyr	double	市盈率(LYR)
pe_ttm	double	市盈率(TTM)
2.4. 使用示例

2.4.1. 获取所有指数一段时间内的估值指标

import panda_data
result = panda_data.get_index_indicator(
    symbol="",
    start_date="20250101",
    end_date="20250131",
    fields=[]
)
print(result)
date symbol pb_lf pb_lyr pb_ttm pe_lyr pe_ttm
0 20250127 000001.SH 1.212212 1.266905 1.235656 14.403007 14.201434
1 20250124 000001.SH 1.210876 1.265509 1.234295 14.387140 14.185789
2 20250123 000001.SH 1.204265 1.258580 1.227551 14.308799 14.108210
3 20250122 000001.SH 1.196207 1.250158 1.219337 14.213050 14.013804
4 20250121 000001.SH 1.206637 1.261058 1.229969 14.336975 14.135992
... ... ... ... ... ... ... ...
2173 20250108 H30318.SH 4.288753 4.423812 4.350295 65.563513 52.513664
2174 20250107 H30318.SH 4.310324 4.446062 4.372176 65.893282 52.777795
2175 20250106 H30318.SH 4.136498 4.266762 4.195856 63.235948 50.649381
2176 20250103 H30318.SH 4.161322 4.292368 4.221036 63.615437 50.953336
2177 20250102 H30318.SH 4.256468 4.390510 4.317547 65.069969 52.118355
2.4.2. 获取单个指数一段时间内的估值指标并使用fields

import panda_data
result = panda_data.get_index_indicator(
    symbol="000001.SH",
    start_date="20250101",
    end_date="20250131",
    fields=["symbol", "date", "pb_lf", "pb_lyr"]
)
print(result)
date symbol pb_lf pb_lyr
0 20250127 000001.SH 1.212212 1.266905
1 20250124 000001.SH 1.210876 1.265509
2 20250123 000001.SH 1.204265 1.258580
3 20250122 000001.SH 1.196207 1.250158
4 20250121 000001.SH 1.206637 1.261058
5 20250120 000001.SH 1.208519 1.263025
6 20250117 000001.SH 1.209137 1.263617
7 20250116 000001.SH 1.207780 1.262187
8 20250115 000001.SH 1.203056 1.257250
9 20250114 000001.SH 1.207666 1.262068
10 20250113 000001.SH 1.180195 1.233359
11 20250110 000001.SH 1.183430 1.236716
12 20250109 000001.SH 1.199218 1.253187
13 20250108 000001.SH 1.207044 1.261365
14 20250107 000001.SH 1.205343 1.259588
15 20250106 000001.SH 1.196401 1.250243
16 20250103 000001.SH 1.199433 1.253411
17 20250102 000001.SH 1.216579 1.271330
3. 获取指数权重信息

3.1. 方法名：get_index_weights

3.2. 入参

字段	类型	描述	是否必填
index_symbol	Optional[Union[str, List[str]]]	指数代码	非必填
stock_symbol	Optional[Union[str, List[str]]]	成分股代码	非必填
start_date	Optional[str]	开始日期,eg:“20250702”	非必填
end_date	Optional[str]	结束日期,eg:“20250702”	非必填
fields	Optional[Union[str, List[str]]]	返回字段列表	非必填
3.3. 响应参数

字段名	类型	描述
index_symbol	str	指数代码
date	str	日期
stock_symbol	str	股票代码
weight	double	权重
3.4. 使用示例

3.4.1. 获取某一指数的成分股在一定日期范围的权重

import panda_data
result = panda_data.get_index_weights(
    index_symbol="000006.SH",
    stock_symbol="",
    start_date="20250101",
    end_date="20250131",
    fields=["index_symbol", "stock_symbol", "date"]
)
print(result)
index_symbol date stock_symbol
0 000006.SH 20250127 600048.SH
1 000006.SH 20250124 600048.SH
2 000006.SH 20250123 600048.SH
3 000006.SH 20250122 600048.SH
4 000006.SH 20250121 600048.SH
.. ... ... ...
355 000006.SH 20250108 603506.SH
356 000006.SH 20250107 603506.SH
357 000006.SH 20250106 603506.SH
358 000006.SH 20250103 603506.SH
359 000006.SH 20250102 603506.SH
3.4.2. 获取某一指数的单个成分股在一定日期范围的权重

import panda_data
result = panda_data.get_index_weights(
    index_symbol="000006.SH",
    stock_symbol="600048.SH",
    start_date="20250101",
    end_date="20250131",
    fields=["index_symbol", "stock_symbol", "date"]
)
print(result)
index_symbol date stock_symbol
0 000006.SH 20250127 600048.SH
1 000006.SH 20250124 600048.SH
2 000006.SH 20250123 600048.SH
3 000006.SH 20250122 600048.SH
4 000006.SH 20250121 600048.SH
5 000006.SH 20250120 600048.SH
6 000006.SH 20250117 600048.SH
7 000006.SH 20250116 600048.SH
8 000006.SH 20250115 600048.SH
9 000006.SH 20250114 600048.SH
10 000006.SH 20250113 600048.SH
11 000006.SH 20250110 600048.SH
12 000006.SH 20250109 600048.SH
13 000006.SH 20250108 600048.SH
14 000006.SH 20250107 600048.SH
15 000006.SH 20250106 600048.SH
16 000006.SH 20250103 600048.SH
17 000006.SH 20250102 600048.SH
十、行业数据

1. 获取行业基本信息数据

1.1. 方法名：get_industry_list

1.2. 入参

字段	类型	描述	是否必填
fields	Optional[Union[str, List[str]]]	返回字段列表	非必填
level	Optional[Union[str, List[str]]]	行业级别，可选值：“L1”(一级)、“L2”(二级)、“L3”(三级)	非必填
1.3. 响应参数

字段名	类型	描述
symbol	str	指数代码
industry_code	str	行业代码
industry_name	str	行业名称
level	str	行业级别
parent_code	str	上级行业代码
1.4. 使用示例

1.4.1. 获取所有行业基本信息（一级）

import panda_data
result = panda_data.get_industry_list(
    level="L1",
    fields=[]
)
print(result)
industry_code industry_name
0 801010 农林牧渔
1 801030 基础化工
2 801040 钢铁
3 801050 有色金属
4 801080 电子
5 801110 家用电器
6 801120 食品饮料
7 801130 纺织服饰
8 801140 轻工制造
9 801150 医药生物
10 801160 公用事业
11 801170 交通运输
12 801180 房地产
13 801200 商贸零售
14 801210 社会服务
15 801230 综合
16 801710 建筑材料
17 801720 建筑装饰
18 801730 电力设备
19 801740 国防军工
20 801750 计算机
21 801760 传媒
22 801770 通信
23 801780 银行
24 801790 非银金融
25 801880 汽车
26 801890 机械设备
27 801950 煤炭
28 801960 石油石化
29 801970 环保
30 801980 美容护理
1.4.2. 获取所有行业基本信息且使用fields （一级）

import panda_data
result = panda_data.get_industry_list(
    level="L1",
    fields=["industry_name"]
)
print(result)
industry_name
0 农林牧渔
1 基础化工
2 钢铁
3 有色金属
4 电子
5 家用电器
6 食品饮料
7 纺织服饰
8 轻工制造
9 医药生物
10 公用事业
11 交通运输
12 房地产
13 商贸零售
14 社会服务
15 综合
16 建筑材料
17 建筑装饰
18 电力设备
19 国防军工
20 计算机
21 传媒
22 通信
23 银行
24 非银金融
25 汽车
26 机械设备
27 煤炭
28 石油石化
29 环保
30 美容护理
2. 获取行业成分股数据

2.1. 方法名：get_industry_stock

2.2. 入参

字段	类型	描述	是否必填
industry_code	Optional[Union[str, List[str]]]	行业代码，如"801010"	非必填
stock_symbol	Optional[Union[str, List[str]]]	股票代码，如"000001.SZ"	非必填
level	Optional[str]	行业级别，可选值：“L1”(一级)、“L2”(二级)、“L3”(三级)	非必填
fields	Optional[Union[str, List[str]]]	返回字段列表	非必填
2.3. 响应参数

字段名	类型	描述
stock_symbol	str	股票代码
l1_code	str	一级行业代码
l2_code	str	二级行业代码
l3_code	str	三级行业代码
in_date	str	纳入时间
l1_name	str	一级行业名称
l2_name	str	二级行业名称
l3_name	str	三级行业名称
out_date	str	剔除时间
stock_name	str	股票名称
2.4. 使用示例

2.4.1. 获取某个行业的成分股数据

import panda_data
result = panda_data.get_industry_stock(
    industry_code="801780",
    stock_symbol="000001.SZ",
    level="L1",
    fields=[]
)
print(result)
l1_code l2_code stock_symbol l3_code ... l2_name l3_name out_date stock_name
0 801780 801783 000001.SZ 857831 ... 股份制银行Ⅱ 股份制银行Ⅲ None 平安银行
2.4.2. 获取某个行业的成分股数据且使用fields

import panda_data
result = panda_data.get_industry_stock(
    industry_code="801780",
    stock_symbol="000001.SZ",
    level="L1",
    fields=["stock_symbol", "industry_code", "l1_code", "stock_name"]
)
print(result)
l1_code stock_symbol stock_name
0 801780 000001.SZ 平安银行
3. 获取指定股票所属的行业信息

3.1. 方法名：get_stock_industry

3.2. 入参

字段	类型	描述	是否必填
stock_symbol	str	股票代码，如"000001.SZ"	必填
level	Optional[str]	行业级别，可选值：“L1”(一级)、“L2”(二级)、“L3”(三级)	非必填
3.3. 响应参数

字段	类型	描述
stock_symbol	str	股票代码
industry_code	str	行业代码
industry_name	str	行业名称
parent_code	str	上级行业代码
parent_name	str	上级行业名称
parent_l1_code	str	一级行业名称
parent_l1_name	str	一级行业名称
parent_l2_code	str	二级行业名称
parent_l2_name	str	二级行业名称
3.4. 使用示例

3.4.1. 获取指定股票所属的行业信息

import panda_data
result = panda_data.get_stock_industry(
    stock_symbol="000001.SZ",
    level="L1"
)
print(result)
stock_symbol industry_code industry_name
0 000001.SZ 801780 银行
十一、融资融券数据

1. 获取融资融券信息

1.1. 方法名：get_securities_margin

1.2. 入参

字段	类型	描述	是否必填
symbol	Optional[Union[str, List[str]]]	股票代码	非必填
start_date	Optional[str]	开始日期,eg:“20250702”	非必填
end_date	Optional[str]	结束日期,eg:“20250702”	非必填
fields	Optional[Union[str, List[str]]]	返回字段列表	非必填
margin_type	Optional[str]	买卖方向，‘stock’ 代表融券卖出，‘cash’ 代表融资买入	非必填
1.3. 响应参数

字段名	类型	描述
short_sell_quantity	double	融券卖出量
buy_on_margin_value	double	融资买入额
date	str	日期
margin_repayment	double	融券偿还额
short_balance	double	融券余额
margin_balance	double	融资余额
symbol	str	股票代码
short_balance_quantity	double	融券余量
short_repayment_quantity	double	融券偿还量
margin_type	str	买卖方向，‘stock’ 代表融券卖出，‘cash’ 代表融资买入
total_balance	double	总余额
1.4. 使用示例

1.4.1. 获取一定日期内某只股票的融资融券信息

import panda_data
result = panda_data.get_securities_margin(
    symbol="000001.SZ",
    start_date="20250101",
    end_date="20250131",
    margin_type="stock",
    fields=[]
)
print(result)
margin_repayment margin_type ... short_sell_quantity margin_balance
0 251279339.0 stock ... 9600.0 4.548699e+09
1 139809406.0 stock ... 27400.0 4.691464e+09
2 319125971.0 stock ... 73000.0 4.711227e+09
3 123876772.0 stock ... 51700.0 4.874748e+09
4 130980727.0 stock ... 30200.0 4.727470e+09
5 98068988.0 stock ... 18400.0 4.652860e+09
6 73332874.0 stock ... 138700.0 4.631203e+09
7 147096301.0 stock ... 115500.0 4.564706e+09
8 147931835.0 stock ... 60100.0 4.623174e+09
9 133426049.0 stock ... 106100.0 4.707604e+09
10 106573656.0 stock ... 30500.0 4.754935e+09
11 124881490.0 stock ... 8100.0 4.701712e+09
12 92421500.0 stock ... 80000.0 4.710915e+09
13 144223648.0 stock ... 104800.0 4.656706e+09
14 105752927.0 stock ... 118400.0 4.625191e+09
15 155997660.0 stock ... 120200.0 4.669212e+09
16 159456379.0 stock ... 23200.0 4.669653e+09
17 280885137.0 stock ... 21000.0 4.659470e+09
1.4.2. 获取一定日期内某只股票的融资融券信息且使用fields

import panda_data
result = panda_data.get_securities_margin(
    symbol="000001.SZ",
    start_date="20250101",
    end_date="20250131",
    margin_type="stock",
    fields=["symbol", "date", "margin_type", "margin_repayment", "margin_balance"]
)
print(result)
margin_repayment margin_type symbol date margin_balance
0 251279339.0 stock 000001.SZ 20250127 4.548699e+09
1 139809406.0 stock 000001.SZ 20250124 4.691464e+09
2 319125971.0 stock 000001.SZ 20250123 4.711227e+09
3 123876772.0 stock 000001.SZ 20250122 4.874748e+09
4 130980727.0 stock 000001.SZ 20250121 4.727470e+09
5 98068988.0 stock 000001.SZ 20250120 4.652860e+09
6 73332874.0 stock 000001.SZ 20250117 4.631203e+09
7 147096301.0 stock 000001.SZ 20250116 4.564706e+09
8 147931835.0 stock 000001.SZ 20250115 4.623174e+09
9 133426049.0 stock 000001.SZ 20250114 4.707604e+09
10 106573656.0 stock 000001.SZ 20250113 4.754935e+09
11 124881490.0 stock 000001.SZ 20250110 4.701712e+09
12 92421500.0 stock 000001.SZ 20250109 4.710915e+09
13 144223648.0 stock 000001.SZ 20250108 4.656706e+09
14 105752927.0 stock 000001.SZ 20250107 4.625191e+09
15 155997660.0 stock 000001.SZ 20250106 4.669212e+09
16 159456379.0 stock 000001.SZ 20250103 4.669653e+09
17 280885137.0 stock 000001.SZ 20250102 4.659470e+09
十二、沪深股通数据

1. 获取沪深股通持股信息

1.1. 方法名：get_stock_connect

1.2. 入参

字段	类型	描述	是否必填
symbol	Optional[Union[str, List[str]]]	股票代码	非必填
start_date	Optional[str]	开始日期,eg:“20250702”	非必填
end_date	Optional[str]	结束日期,eg:“20250702”	非必填
fields	Optional[Union[str, List[str]]]	返回字段列表	非必填
1.3. 响应参数

字段名	类型	描述
date	str	日期
shares_num	double	持股数量
symbol	str	股票代码
adjusted_holding_ratio	double	调整后持股比例
holding_ratio	double	持股比例
1.4. 使用示例

1.4.1. 获取一定日期内某只股票的沪深股通持股信息

import panda_data
result = panda_data.get_stock_connect(
    symbol="000001.SZ",
    start_date="20250601",
    end_date="20250630",
    fields=[]
)
print(result)
adjusted_holding_ratio symbol date holding_ratio shares_num
0 4.2726 000001.SZ 20250630 4.27 829114531.0
1.4.2. 获取一定日期内所有股票的沪深股通持股信息并使用fields

import panda_data
result = panda_data.get_stock_connect(
    symbol="",
    start_date="20250601",
    end_date="20250630",
    fields=["symbol", "date", "shares_num"]
)
print(result)
symbol date b_value b_volume s_value s_volume
0 000001.SZ 20250102 858957231.0 74357447.0 1.243966e+09 107602252.0
1 000001.SZ 20250103 618660413.0 54068235.0 7.018606e+08 61399809.0
2 000001.SZ 20250106 614016296.0 53935269.0 6.202895e+08 54618361.0
3 000001.SZ 20250107 469239789.0 40881504.0 3.890893e+08 33904784.0
4 000001.SZ 20250108 641508573.0 55661966.0 5.820904e+08 50576635.0
5 000001.SZ 20250109 395933847.0 34675524.0 4.619022e+08 40472806.0
6 000001.SZ 20250110 445757841.0 39306512.0 4.592472e+08 40506839.0
7 000001.SZ 20250113 480142237.0 42953409.0 5.647622e+08 50543209.0
8 000001.SZ 20250114 553184905.0 48816902.0 3.812829e+08 33645993.0
9 000001.SZ 20250115 687935047.0 59858384.0 4.974686e+08 43304698.0
10 000001.SZ 20250116 579731465.0 50209533.0 4.279578e+08 37086866.0
11 000001.SZ 20250117 317031580.0 27632456.0 4.741988e+08 41344030.0
12 000001.SZ 20250120 405285150.0 35366053.0 5.478070e+08 47836860.0
13 000001.SZ 20250121 415581086.0 36565077.0 6.092981e+08 53641817.0
14 000001.SZ 20250122 627154596.0 56140803.0 8.776640e+08 78572119.0
15 000001.SZ 20250123 999888511.0 88310470.0 7.152840e+08 63181557.0
16 000001.SZ 20250124 542104766.0 47866911.0 5.277943e+08 46627510.0
17 000001.SZ 20250127 733032970.0 63769269.0 5.912376e+08 51424202.0
1.4.2. 获取一定日期内某只股票的资金流入流出数据且使用fields

import panda_data
result = panda_data.get_stock_flow(
    symbol="000001.SZ",
    start_date="20250101",
    end_date="20250131",
    fields=["symbol", "date", "b_value", "b_volume"]
)
print(result)
symbol date b_value b_volume
0 000001.SZ 20250102 858957231.0 74357447.0
1 000001.SZ 20250103 618660413.0 54068235.0
2 000001.SZ 20250106 614016296.0 53935269.0
3 000001.SZ 20250107 469239789.0 40881504.0
4 000001.SZ 20250108 641508573.0 55661966.0
5 000001.SZ 20250109 395933847.0 34675524.0
6 000001.SZ 20250110 445757841.0 39306512.0
7 000001.SZ 20250113 480142237.0 42953409.0
8 000001.SZ 20250114 553184905.0 48816902.0
9 000001.SZ 20250115 687935047.0 59858384.0
10 000001.SZ 20250116 579731465.0 50209533.0
11 000001.SZ 20250117 317031580.0 27632456.0
12 000001.SZ 20250120 405285150.0 35366053.0
13 000001.SZ 20250121 415581086.0 36565077.0
14 000001.SZ 20250122 627154596.0 56140803.0
15 000001.SZ 20250123 999888511.0 88310470.0
16 000001.SZ 20250124 542104766.0 47866911.0
17 000001.SZ 20250127 733032970.0 63769269.0
2. 获取股票资金流分钟级数据

2.1. 方法名：get_stock_flow_1m

2.2. 入参

字段	类型	描述	是否必填
symbol	Optional[Union[str, List[str]]]	股票代码	非必填
start_date	Optional[str]	开始日期,eg:“20250702”	非必填
end_date	Optional[str]	结束日期,eg:“20250702”	非必填
fields	Optional[Union[str, List[str]]]	返回字段列表	非必填
time_zone	Optional[tuple]	时间段过滤,格式为(“HH:MM”, “HH:MM”)，例如(“10:00”, “23:00”)	非必填
2.3. 响应参数

字段名	类型	描述
symbol	str	股票代码
date	str	日期
minute	str	时间（精确至分钟）
b_value	double	主动买入额
b_volume	double	主动买入量
s_value	double	主动卖出额
s_volume	double	主动卖出量
2.4. 使用示例

2.4.1. 获取一定日期和时间内某只股票的资金流分钟级数据

import panda_data
result = panda_data.get_stock_flow_1m(
    symbol="000001.SZ",
    start_date="20250101",
    end_date="20250831",
    time_zone=("08:00", "12:00"),
    fields=[]
)
print(result)
symbol b_value b_volume s_value s_volume date minute
0 000001.SZ 25921715.0 2147100.0 4702957.0 389300.0 20250701 093100
1 000001.SZ 11888337.0 983700.0 8667288.0 717000.0 20250701 093200
2 000001.SZ 8675749.0 717100.0 7652739.0 632600.0 20250701 093300
3 000001.SZ 3444662.0 284962.0 3844452.0 318100.0 20250701 093400
4 000001.SZ 7979858.0 659600.0 4758157.0 393300.0 20250701 093500
... ... ... ... ... ... ... ...
1915 000001.SZ 619456.0 51500.0 1723926.0 143400.0 20250822 112600
1916 000001.SZ 547586.0 45529.0 1449679.0 120600.0 20250822 112700
1917 000001.SZ 689303.0 57300.0 6975870.0 579900.0 20250822 112800
1918 000001.SZ 722882.0 60100.0 2417218.0 201000.0 20250822 112900
1919 000001.SZ 2485118.0 206700.0 244158.0 20300.0 20250822 113000
2.4.2. 获取一定日期内某些股票的资金流分钟级数据且使用fields

import panda_data
result = panda_data.get_stock_flow_1m(
    symbol="000001.SZ",
    start_date="20250101",
    end_date="20250831",
    time_zone=("08:00", "12:00"),
    fields=["symbol", "date", "s_value", "s_volume"]
)
print(result)
symbol s_value s_volume date minute
0 000001.SZ 4702957.0 389300.0 20250701 093100
1 000001.SZ 8667288.0 717000.0 20250701 093200
2 000001.SZ 7652739.0 632600.0 20250701 093300
3 000001.SZ 3844452.0 318100.0 20250701 093400
4 000001.SZ 4758157.0 393300.0 20250701 093500
... ... ... ... ... ...
1915 000001.SZ 1723926.0 143400.0 20250822 112600
1916 000001.SZ 1449679.0 120600.0 20250822 112700
1917 000001.SZ 6975870.0 579900.0 20250822 112800
1918 000001.SZ 2417218.0 201000.0 20250822 112900
1919 000001.SZ 244158.0 20300.0 20250822 113000
3. 获取财务报告审计意见数据

3.1. 方法名：get_audit_opinion

3.2. 入参

字段	类型	描述	是否必填
symbol	Optional[Union[str, List[str]]]	股票代码	非必填
start_quarter	Optional[str]	开始季度,eg:“2025q1”	非必填
end_quarter	Optional[str]	结束季度,eg:“2025q3”	非必填
fields	Optional[Union[str, List[str]]]	返回字段列表	非必填
market	Optional[str]	市场,默认’cn’为中国内地市场	非必填
3.3. 响应参数

字段	类型	描述
date	str	公告发布日
symbol	str	股票代码
quarter	str	报告季度
audit_type	str	审计报告类型
agency	str	会计师事务所
opinion	str	审计意见（见下表）
审计意见类型表:

opinion	描述
unqualified_opinion	无保留意见
unqualified_opinion_with_emphasis-of-matter_paragraph	无保留意见并带解释性说明
qualified_opinion	保留意见
qualified_opinion_with_basis_for_qualification_paragraph	保留意见并带解释性说明
disclaimer_of_opinion	拒绝/无法表示意见
adverse_opinion	否定意见
no_audit_performed	未经审计
uncertain_opinion	不确定意见
unqualified_opinion_with_material_uncertainty	无保留意见但存在不确定性
3.4. 使用示例

3.4.1. 获取一定报告期内某只股票的财务报告审计意见数据

import panda_data
result = panda_data.get_audit_opinion(
    symbol="000001.SZ",
    start_quarter="2024q1",
    end_quarter="2025q3",
    market="cn",
    fields=[]
)
print(result)
date symbol ... opinion quarter
0 20240420 000001.SZ ... no_audit_performed 2024q1
1 20240816 000001.SZ ... no_audit_performed 2024q2
2 20241019 000001.SZ ... no_audit_performed 2024q3
3 20250315 000001.SZ ... unqualified_opinion 2024q4
4 20250315 000001.SZ ... unqualified_opinion 2024q4
5 20250419 000001.SZ ... no_audit_performed 2025q1
3.4.2. 获取一定报告期内全部股票的财务报告审计意见数据并使用fields

import panda_data
result = panda_data.get_audit_opinion(
    symbol="",
    start_quarter="2025q1",
    end_quarter="2025q2",
    market="cn",
    fields=["symbol", "date", "audit_type", "opinion"]
)
print(result)
date symbol audit_type opinion quarter
0 20250422 000020.SZ financial_statements no_audit_performed 2025q1
1 20250428 000012.SZ financial_statements no_audit_performed 2025q1
2 20250429 000004.SZ financial_statements no_audit_performed 2025q1
3 20250429 000061.SZ financial_statements no_audit_performed 2025q1
4 20250422 000055.SZ financial_statements no_audit_performed 2025q1
... ... ... ... ... ...
4581 20250919 601026.SH financial_statements unqualified_opinion 2025q2
4582 20250828 603027.SH financial_statements unqualified_opinion 2025q2
4583 20250828 603052.SH financial_statements unqualified_opinion 2025q2
4584 20250826 605319.SH financial_statements unqualified_opinion 2025q2
4585 20250818 300943.SZ financial_statements unqualified_opinion 2025q1
4. 获取A股合约投资者关系活动

4.1. 方法名：get_investor_activities

4.2. 入参

字段	类型	描述	是否必填
symbol	Optional[Union[str, List[str]]]	股票代码	非必填
start_date	Optional[str]	开始日期,eg:“20250702”	非必填
end_date	Optional[str]	结束日期,eg:“20250702”	非必填
fields	Optional[Union[str, List[str]]]	返回字段列表	非必填
4.3. 响应参数

字段	类型	描述
date	str	公告发布日
symbol	str	股票代码
participant	str	参与人员
investor_or_analyst_detail	str	与会人员详情
institute	str	参与机构
4.4. 使用示例

4.4.1. 获取一定日期内某只股票合约投资者关系活动数据

import panda_data
result = panda_data.get_investor_activities(
    symbol="000001.SZ",
    start_date="20250101",
    end_date="20250131",
    fields=[]
)
print(result)
participant institute investor_or_analyst_detail symbol date
0 None None 境内投资者 000001.SZ 20250117
4.4.2. 获取一定日期内某只股票合约投资者关系活动数据且使用fields

import panda_data
result = panda_data.get_investor_activities(
    symbol="000001.SZ",
    start_date="20250101",
    end_date="20250131",
    fields=["symbol", "date", "participant", "investor_or_analyst_detail"]
)
print(result)
participant investor_or_analyst_detail symbol date
0 None 境内投资者 000001.SZ 20250117
5. 获取股票限售解禁明细数据

5.1. 方法名：get_restricted_details

5.2. 入参

字段	类型	描述	是否必填
symbol	Optional[Union[str, List[str]]]	股票代码	非必填
start_date	Optional[str]	开始日期,eg:“20250702”	非必填
end_date	Optional[str]	结束日期,eg:“20250702”	非必填
fields	Optional[Union[str, List[str]]]	返回字段列表	非必填
market	Optional[str]	市场,默认’cn’为中国内地市场	非必填
5.3. 响应参数

字段	类型	描述
symbol	str	合约代码
date	str	限售解禁信息发布日期
relieve_date	str	解禁日期
shareholder	str	股东名
shareholder_type	str	股东类型
relieve_shares	double	解除限售股份数量(股)
actual_relieve_shares	double	实际上市流通数量(股)
relieve_reason	str	解禁原因
5.4. 使用示例

5.4.1. 获取一定日期内某只股票的股票限售解禁明细数据

import panda_data
result = panda_data.get_restricted_details(
    symbol="001256.SZ",
    start_date="20251201",
    end_date="20251231",
    fields=[]
)
print(result)
date relieve_date ... relieve_reason shareholder_type
0 20251211 20251212 ... 发行前股份限售流通 企业
1 20251211 20251212 ... 发行前股份限售流通 自然人
2 20251211 20251212 ... 发行前股份限售流通 自然人
3 20251211 20251212 ... 发行前股份限售流通 企业
4 20251211 20251212 ... 发行前股份限售流通 自然人
5.4.2. 获取一定日期内某只股票的股票限售解禁明细数据且使用fields

import panda_data
result = panda_data.get_restricted_details(
    symbol="001256.SZ",
    start_date="20251201",
    end_date="20251231",
    fields=["symbol", "date", "shareholder", "relieve_shares"]
)
print(result)
date relieve_shares symbol shareholder
0 20251211 45758500.0 001256.SZ 浙江承炜股权投资有限公司
1 20251211 37280000.0 001256.SZ 周炳松
2 20251211 10320000.0 001256.SZ 李玉荷
3 20251211 3017825.0 001256.SZ 平阳炜仕股权投资合伙企业(有限合伙)
4 20251211 4000000.0 001256.SZ 於金华
6. 获取股东数量

6.1. 方法名：get_holder_number

6.2. 入参

字段	类型	描述	是否必填
symbol	Optional[Union[str, List[str]]]	股票代码	非必填
start_date	Optional[str]	开始日期,eg:“20250702”	非必填
end_date	Optional[str]	结束日期,eg:“20250702”	非必填
fields	Optional[Union[str, List[str]]]	返回字段列表	非必填
6.3. 响应参数

字段	类型	描述
symbol	str	股票代码
date	str	公告日期
end_date	str	截止日期
a_holders	str	A股股东户数
avg_a_holders	str	A股股东户均持股数
avg_circulation_holders	double	无限售A股股东户均持股数
avg_holders	double	户均持股数
holders	str	股东户数
6.4. 使用示例

6.4.1. 获取一定日期内某只股票的股东数量

import panda_data
result = panda_data.get_holder_number(
    symbol="000001.SZ",
    start_date="20250101",
    end_date="20250531",
    fields=[]
)
print(result)
end_date symbol ... avg_holders holders
0 20241231 000001.SZ ... 39908.69 486258.0
1 20250228 000001.SZ ... 40431.61 479969.0
2 20250331 000001.SZ ... 38483.42 504267.0
6.4.2. 获取一定日期内全部股票的股东数量并使用fields

import panda_data
result = panda_data.get_holder_number(
    symbol="",
    start_date="20250101",
    end_date="20250131",
    fields=["symbol", "date", "holders", "avg_holders"]
)
print(result)
date symbol avg_holders holders
0 20250103 000004.SZ 3021.42 43814.0
1 20250114 000004.SZ 3309.18 40004.0
2 20250122 000004.SZ 3295.5 40170.0
3 20250115 000008.SZ 19666.51 138122.0
4 20250106 000008.SZ 19181.02 141618.0
... ... ... ... ...
2259 20250103 688687.SH 19046.73 8975.0
2260 20250123 688687.SH 19902.72 8589.0
2261 20250107 688689.SH 17274.61 7462.0
2262 20250114 688689.SH 17721.08 7274.0
2263 20250109 688758.SH 14351.43 29019.0
7. 获取A股股东信息

7.1. 方法名：get_main_shareholder

7.2. 入参

字段	类型	描述	是否必填
symbol	Optional[Union[str, List[str]]]	股票代码	非必填
start_date	Optional[str]	开始日期,eg:“20250702”	非必填
end_date	Optional[str]	结束日期,eg:“20250702”	非必填
fields	Optional[Union[str, List[str]]]	返回字段列表	非必填
market	Optional[str]	市场,默认’cn’为中国内地市场	非必填
start_rank	Optional[int]	排名开始值	非必填
end_rank	Optional[int]	排名结束值	非必填
stock_type	Optional[str]	股票种类, flow基于持有A股流通股;total基于所有发行出的A股	非必填
7.3. 响应参数

字段	类型	描述
date	str	信息发布日期
stock_type	str	股票类型
rank	int	排名
symbol	str	股票代码
end_date	str	截止日期
freeze	double	股权冻结涉及股数（股）
hold_percent_float	double	占流通A股比例（%）
hold_percent_total	double	占股比例(%)
holder_attr	str	股东属性
holder_kind	str	股东性质
holder_name	str	股东名称
holder_type	double	股东类别
pledge	double	股权质押涉及股数
7.4. 使用示例

7.4.1. 获取一定日期内某只股票的股东信息

import panda_data
result = panda_data.get_main_shareholder(
    symbol="000001.SZ",
    start_date="20250101",
    end_date="20250531",
    start_rank=1,
    end_rank=5,
    stock_type="flow",
    market="cn",
    fields=[]
)
print(result)
holder_type date holder_kind ... hold_percent_total holder_attr pledge
0 NaN 20250315 金融机构—保险公司 ... 49.564984 企业 NaN
1 NaN 20250315 金融机构—保险公司 ... 6.112055 企业 NaN
2 NaN 20250315 一般企业 ... 3.848732 企业 NaN
3 NaN 20250315 保险投资组合 ... 2.269816 证券品种 NaN
4 NaN 20250315 金融机构—证券公司 ... 2.211865 企业 NaN
5 NaN 20250419 金融机构—保险公司 ... 49.564984 企业 NaN
6 NaN 20250419 金融机构—保险公司 ... 6.112055 企业 NaN
7 NaN 20250419 一般企业 ... 3.391309 企业 NaN
8 NaN 20250419 保险投资组合 ... 2.269816 证券品种 NaN
9 NaN 20250419 金融机构—证券公司 ... 2.211865 企业 NaN
7.4.2. 获取一定日期内某只股票的股东信息据且使用fields

import panda_data
result = panda_data.get_main_shareholder(
    symbol="000001.SZ",
    start_date="20250101",
    end_date="20250531",
    start_rank=1,
    end_rank=5,
    stock_type="flow",
    market="cn",
    fields=["symbol", "date", "holder_kind", "holder_name"]
)
print(result)
date holder_kind rank symbol holder_name stock_type
0 20250315 金融机构—保险公司 1 000001.SZ 中国平安保险(集团)股份有限公司-集团本级-自有资金 flow
1 20250315 金融机构—保险公司 2 000001.SZ 中国平安人寿保险股份有限公司-自有资金 flow
2 20250315 一般企业 3 000001.SZ 香港中央结算有限公司 flow
3 20250315 保险投资组合 4 000001.SZ 中国平安人寿保险股份有限公司-传统-普通保险产品 flow
4 20250315 金融机构—证券公司 5 000001.SZ 中国证券金融股份有限公司 flow
5 20250419 金融机构—保险公司 1 000001.SZ 中国平安保险(集团)股份有限公司-集团本级-自有资金 flow
6 20250419 金融机构—保险公司 2 000001.SZ 中国平安人寿保险股份有限公司-自有资金 flow
7 20250419 一般企业 3 000001.SZ 香港中央结算有限公司 flow
8 20250419 保险投资组合 4 000001.SZ 中国平安人寿保险股份有限公司-传统-普通保险产品 flow
9 20250419 金融机构—证券公司 5 000001.SZ 中国证券金融股份有限公司 flow
8. 获取合约特殊处理数据

8.1. 方法名：get_stock_special_treatment

8.2. 入参

字段	类型	描述	是否必填
symbol	Optional[Union[str, List[str]]]	股票代码	非必填
start_date	Optional[str]	开始日期,eg:“20250702”	非必填
end_date	Optional[str]	结束日期,eg:“20250702”	非必填
fields	Optional[Union[str, List[str]]]	返回字段列表	非必填
8.3. 响应参数

字段	类型	描述
symbol	str	股票代码
date	str	信息发布日期
change_date	str	特别处理（或撤销）实施日期
description	str	特别处理（或撤销）事项描述
name	str	股票名称
type	str	特别处理（或撤销）类别
8.4. 使用示例

8.4.1. 获取一定日期内某只股票合约特殊处理数据

import panda_data
result = panda_data.get_stock_special_treatment(
    symbol="002217.SZ",
    start_date="20250101",
    end_date="20250131",
    fields=[]
)
print(result)
date change_date symbol ... name type info_date
0 20250107 20250106 002217.SZ ... *ST合泰 撤销叠加*ST 20250107
8.4.2. 获取一定日期内全部股票合约特殊处理数据并使用fields

import panda_data
result = panda_data.get_stock_special_treatment(
    symbol="",
    start_date="20250101",
    end_date="20250131",
    fields=["symbol", "date", "change_date", "name", "type"]
)
print(result)
date change_date symbol name type
0 20250107 20250106 002217.SZ *ST合泰 撤销叠加*ST
1 20250109 20250109 002309.SZ *ST中利 撤销叠加*ST
2 20250103 20250102 002310.SZ *ST东园 撤销叠加*ST
3 20250111 20250114 002656.SZ *ST摩登 从ST变为*ST
4 20250110 20250110 300209.SZ *ST有树 撤销叠加*ST
5 20250110 20250113 300301.SZ *ST长方 叠加ST
6 20250105 20250107 300630.SZ *ST普利 *ST
7 20250123 20250207 600225.SH 退市卓朗 退市整理期
8 20250111 20250114 600289.SH *ST信通 叠加*ST
9 20250125 20250127 600360.SH ST华微 叠加ST
10 20250108 20250107 600375.SH *ST汉马 撤销叠加*ST
11 20250107 20250106 600715.SH *ST文投 撤销叠加*ST
12 20250113 20250114 603007.SH ST花王 撤消*ST并实行ST
13 20250109 20250108 603363.SH *ST傲农 撤销叠加*ST
14 20250109 20250108 603559.SH *ST通脉 撤销叠加*ST
9. 获取A股大宗交易信息

9.1. 方法名：get_block_trade

9.2. 入参

字段	类型	描述	是否必填
symbol	Optional[Union[str, List[str]]]	股票代码	非必填
start_date	Optional[str]	开始日期,eg:“20250702”	非必填
end_date	Optional[str]	结束日期,eg:“20250702”	非必填
fields	Optional[Union[str, List[str]]]	返回字段列表	非必填
9.3. 响应参数

字段	类型	描述
symbol	str	股票代码
date	str	交易日期
price	double	成交价
volume	double	成交量
amount	double	成交额
buyer	str	买方营业部
seller	str	卖方营业部
sequence_id	int	序列号
9.4. 使用示例

9.4.1. 获取一定日期内某只股票的大宗交易信息

import panda_data
result = panda_data.get_block_trade(
    symbol="000001.SZ",
    start_date="20250101",
    end_date="20250831",
    fields=[]
)
print(result)
sequence_id date amount ... seller symbol volume
0 1 20250217 2014400.0 ... 中信证券股份有限公司上海分公司 000001.SZ 171000.0
1 1 20250711 12151800.0 ... 中信证券股份有限公司江苏分公司 000001.SZ 1024600.0
9.4.2. 获取一定日期内某只股票的大宗交易信息且使用fields

import panda_data
result = panda_data.get_block_trade(
    symbol="000001.SZ",
    start_date="20250101",
    end_date="20250831",
    fields=["symbol", "date", "buyer", "amount", "price"]
)
print(result)
date amount buyer price symbol
0 20250217 2014400.0 机构专用 11.78 000001.SZ
1 20250711 12151800.0 中信证券股份有限公司江苏分公司 11.86 000001.SZ
10. 获取股票股本数据

10.1. 方法名：get_stock_shares

10.2. 入参

字段	类型	描述	是否必填
symbol	Optional[Union[str, List[str]]]	股票代码	非必填
start_date	Optional[str]	开始日期,eg:“20250702”	非必填
end_date	Optional[str]	结束日期,eg:“20250702”	非必填
fields	Optional[Union[str, List[str]]]	返回字段列表	非必填
10.3. 响应参数

字段	类型	描述
symbol	str	股票代码
date	str	信息发布日期
circulation_a	str	流通A股
free_circulation	str	自由流通股本
non_circulation_a	str	非流通A股
preferred_shares	str	优先股
total	str	总股本
total_a	str	A股总股本
10.4. 使用示例

10.4.1. 获取一定日期内某只股票的股本数据

import panda_data
result = panda_data.get_stock_shares(
    symbol="000001.SZ",
    start_date="20250101",
    end_date="20250831",
    fields=[]
)
print(result)
symbol date ... total total_a
0 000001.SZ 20250102 ... 1.940592e+10 1.940592e+10
1 000001.SZ 20250103 ... 1.940592e+10 1.940592e+10
2 000001.SZ 20250106 ... 1.940592e+10 1.940592e+10
3 000001.SZ 20250107 ... 1.940592e+10 1.940592e+10
4 000001.SZ 20250108 ... 1.940592e+10 1.940592e+10
.. ... ... ... ... ...
150 000001.SZ 20250825 ... 1.940592e+10 1.940592e+10
151 000001.SZ 20250826 ... 1.940592e+10 1.940592e+10
152 000001.SZ 20250827 ... 1.940592e+10 1.940592e+10
153 000001.SZ 20250828 ... 1.940592e+10 1.940592e+10
154 000001.SZ 20250829 ... 1.940592e+10 1.940592e+10
10.4.2. 获取一定日期内某只股票的股本数据且使用fields

import panda_data
result = panda_data.get_stock_shares(
    symbol="000001.SZ",
    start_date="20250101",
    end_date="20250831",
    fields=["symbol", "date", "circulation_a", "free_circulation"]
)
print(result)
symbol date circulation_a free_circulation
0 000001.SZ 20250102 1.940562e+10 8.160498e+09
1 000001.SZ 20250103 1.940562e+10 8.160498e+09
2 000001.SZ 20250106 1.940562e+10 8.160498e+09
3 000001.SZ 20250107 1.940562e+10 8.160498e+09
4 000001.SZ 20250108 1.940562e+10 8.160498e+09
.. ... ... ... ...
150 000001.SZ 20250825 1.940560e+10 8.160481e+09
151 000001.SZ 20250826 1.940560e+10 8.160481e+09
152 000001.SZ 20250827 1.940560e+10 8.160481e+09
153 000001.SZ 20250828 1.940560e+10 8.160481e+09
154 000001.SZ 20250829 1.940560e+10 8.160481e+09
11. 获取复权因子

11.1. 方法名：get_factor_restored

11.2. 入参

字段	类型	描述	是否必填
symbol	Optional[Union[str, List[str]]]	股票代码	非必填
start_date	Optional[str]	开始日期,eg:“20250702”	非必填
end_date	Optional[str]	结束日期,eg:“20250702”	非必填
fields	Optional[Union[str, List[str]]]	返回字段列表	非必填
11.3. 响应参数

字段	类型	描述
symbol	str	股票代码
ex_date	str	除权除息日期
ex_cum_factor	double	前复权因子
ex_factor	double	后复权因子
ex_end_date	str	除权结束日期
announcement_date	str	公告日期
11.4. 使用示例

11.4.1. 获取一定日期内某只股票的复权因子

import panda_data
result = panda_data.get_factor_restored(
    symbol="000001.SZ",
    start_date="20250101",
    end_date="20250831",
    fields=[]
)
print(result)
symbol ex_date announcement_date ex_cum_factor ex_end_date ex_factor
0 000001.SZ 20250612 20250611 174.334 NaN 1.031513
11.4.2. 获取一定日期内全部股票的复权因子并使用fields

import panda_data
result = panda_data.get_factor_restored(
    symbol="",
    start_date="20250101",
    end_date="20250831",
    fields=["symbol", "ex_date", "announcement_date", "ex_cum_factor"]
)
print(result)
symbol ex_date announcement_date ex_cum_factor
0 000001.SZ 20250612 20250611 174.334000
1 000009.SZ 20250827 20250826 12.017100
2 000019.SZ 20250617 20250616 5.634970
3 000021.SZ 20250611 20250610 14.227600
4 000025.SZ 20250528 20250527 2.768860
... ... ... ... ...
3553 688798.SH 20250520 20250519 1.413086
3554 688799.SH 20250529 20250528 1.513119
3555 688800.SH 20250530 20250529 1.855447
3556 688819.SH 20250613 20250612 1.093522
3557 689009.SH 20250613 20250612 1.026022
12. 获取指定日期的在售股票列表

12.1. 方法名：get_trading_stock_list

12.2. 入参

字段	类型	描述	是否必填
date	Optional[Union[str, List[str]]]	日期,eg:“20250702”	必填
12.3. 响应参数

字段	类型	描述
symbol	str	股票代码
date	str	日期
12.4. 使用示例

12.4.1. 获取指定日期的在售股票列表

import panda_data
result = panda_data.get_trading_stock_list(
    date="20251211"
)
print(result)
date symbol
0 20251211 000001.SZ
1 20251211 000002.SZ
2 20251211 000004.SZ
3 20251211 000006.SZ
4 20251211 000007.SZ
... ... ...
5151 20251211 688799.SH
5152 20251211 688800.SH
5153 20251211 688819.SH
5154 20251211 688981.SH
5155 20251211 689009.SH