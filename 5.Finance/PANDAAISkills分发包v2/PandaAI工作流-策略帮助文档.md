框架基本方法
基础方法说明
该策略为事件驱动性策略，需要实现框架中约定的事件回调方法，实现后回测、仿真、实盘通用。
策略头部需要默认引用内置API，运行代码为：from panda_backtest.api.api import *，后文不再重复赘述。

策略初始化（必选）
函数：initialize
描述：策略初始化，主要用于初始化策略上下文中的变量，只在策略启动时运行一次

代码
def initialize(context):
参数
字段	类型	描述
context	Context对象	策略上下文对象
例子
def initialize(context):
    # 期货账号 回测时写5588 仿真盘会自动替换为真实账号
    context.account = '5588'
    
    # 关注的期货合约
    context.future_contract = 'RB2601.SHF'
    
    # 策略参数
    context.short_window = 5
    context.long_window = 20
    
    # 用于保存历史价格数据
    context.historical_prices = []
    
    # 用于保存订单ID
    context.order_ids = []
    
    SRLogger.info("策略初始化完成")
    SRLogger.info(f"期货账号: {context.account}")
    SRLogger.info(f"关注合约: {context.future_contract}")
策略bar运行（必选）
函数：handle_data
描述：策略bar触发运行函数，日线回测为每日调用一次，分钟则为每个交易分钟时间调用一次

运行时间说明
当有基金交易时，分为普通交易和所有时间交易，分钟运行时间参考下表：

策略类型	运行时间
股票	9:30 ~ 15:00
期货	9:00 ~ 15:00
代码
def handle_data(context, data):
参数
字段	类型	描述
context	Context对象	策略上下文对象
data	Bar对象	bar行情字典对象
例子
def handle_data(context, data):
    # 获取当前交易账户
    account=context.account
    # 获取行情数据
    bar = data['RB2601.SHF']
    close_price = bar.close
    open_price = bar.open
    high_price = bar.high
    low_price = bar.low
    volume = bar.volume
    oi = bar.oi  # 持仓量
    settle = bar.settle  # 结算价
    last = bar.last  # 最新价
    turnover = bar.turnover  # 成交金额
    
    # 获取期货账户信息
    futures_account = context.future_account_dict.get(context.account)
    if futures_account:
        total_value = futures_account.total_value  # 总权益
        cash = futures_account.cash  # 可用资金
        margin = futures_account.margin  # 保证金
        
        # 获取持仓信息
        if 'RB2601.SHF' in futures_account.positions:
            position = futures_account.positions['RB2601.SHF']
            buy_quantity = position.buy_quantity  # 多头持仓
            sell_quantity = position.sell_quantity  # 空头持仓
    
    # 期货账号以市价开仓买入1手
    buy_open(context.account, 'RB2601.SHF', 1, style=MarketOrderStyle)
策略开盘前（可选）
函数：before_trading
描述：策略开盘前运行函数
注意：该函数只在交易日调用，分钟回测调用时间参考下表

运行时间
策略类型	运行时间
股票	8:30
期货	20:30
代码
def before_trading(context):
参数
字段	类型	描述
context	Context对象	策略上下文对象
例子
def before_trading(context):
    SRLogger.info(f"开盘前运行 - 当前日期: {context.now}")
    
    # 获取所有期货账户信息
    if hasattr(context, 'future_account_dict') and context.future_account_dict:
        for account_id, futures_account in context.future_account_dict.items():
            SRLogger.info(f"\n【账户 {account_id} 开盘前信息】")
            SRLogger.info(f"  总权益: {futures_account.total_value}")
            SRLogger.info(f"  可用资金: {futures_account.cash}")
            SRLogger.info(f"  冻结资金: {futures_account.frozen_cash}")
            SRLogger.info(f"  持仓盈亏: {futures_account.holding_pnl}")
            SRLogger.info(f"  平仓盈亏: {futures_account.realized_pnl}")
            SRLogger.info(f"  保证金: {futures_account.margin}")
            SRLogger.info(f"  手续费: {futures_account.transaction_cost}")
            
            # 遍历所有持仓
            positions = futures_account.positions
            if isinstance(positions, dict):
                for symbol, position in positions.items():
                    SRLogger.info(f"\n  持仓合约: {symbol}")
                    SRLogger.info(f"    多头持仓: {position.buy_quantity}")
                    SRLogger.info(f"    空头持仓: {position.sell_quantity}")
                    SRLogger.info(f"    多头盈亏: {position.buy_pnl}")
                    SRLogger.info(f"    空头盈亏: {position.sell_pnl}")
策略收盘后（可选）
函数：after_trading
描述：策略收盘后运行函数
注意：该函数只在交易日调用，调用时间为15:30

代码
def after_trading(context):
参数
字段	类型	描述
context	Context对象	策略上下文对象
例子
def after_trading(context):
    SRLogger.info(f"收盘后运行 - 当前日期: {context.now}")
    
    # 获取期货账户信息
    futures_account = context.future_account_dict.get(context.account)
    if futures_account:
        SRLogger.info(f"\n【收盘后期货账户信息】")
        SRLogger.info(f"  总权益: {futures_account.total_value}")
        SRLogger.info(f"  可用资金: {futures_account.cash}")
        SRLogger.info(f"  持仓盈亏: {futures_account.holding_pnl}")
        SRLogger.info(f"  平仓盈亏: {futures_account.realized_pnl}")
        
        # 打印所有持仓信息
        positions = futures_account.positions
        if isinstance(positions, dict):
            for symbol, position in positions.items():
                SRLogger.info(f"\n  持仓合约: {symbol}")
                SRLogger.info(f"    多头持仓: {position.buy_quantity}")
                SRLogger.info(f"    空头持仓: {position.sell_quantity}")
                SRLogger.info(f"    总盈亏: {position.pnl}")
股票报单回报（可选）
函数：on_stock_trade_rtn
描述：当有报单委托成交后触发

代码
def on_stock_trade_rtn(context, order):
参数
字段	类型	描述
context	Context对象	策略上下文对象
order	Order对象	订单信息
例子
def on_stock_trade_rtn(context, order):
    SRLogger.info("【股票报单回报】")
    SRLogger.info(f"订单ID: {order.order_id}")
    SRLogger.info(f"合约: {order.order_book_id}")
    SRLogger.info(f"买卖方向: {order.side} (1:买, 2:卖)")
    SRLogger.info(f"订单价格: {order.price}")
    SRLogger.info(f"下单数量: {order.quantity}")
    SRLogger.info(f"已成交数量: {order.filled_quantity}")
    SRLogger.info(f"剩余数量: {order.unfilled_quantity}")
    SRLogger.info(f"订单状态: {order.status} (1:未成交, 2:已成交, 3:已撤, -1:拒单)")
    
    # 如果订单已成交，更新持仓信息
    if order.status == 2:
        stock_account = context.stock_account_dict.get(context.account)
        if stock_account and order.order_book_id in stock_account.positions:
            position = stock_account.positions[order.order_book_id]
            SRLogger.info(f"当前持仓数量: {position.quantity}")
            SRLogger.info(f"持仓市值: {position.market_value}")
股票撤单回报（可选）
函数：stock_order_cancel
描述：当有报单委托被撤单后触发

代码
def stock_order_cancel(context, order):
参数
字段	类型	描述
context	Context对象	策略上下文对象
order	Order对象	订单信息
例子
def stock_order_cancel(context, order):
    SRLogger.info("【股票撤单回报】")
    SRLogger.info(f"订单ID: {order.order_id}")
    SRLogger.info(f"合约: {order.order_book_id}")
    SRLogger.info(f"订单状态: {order.status} (3:已撤)")
    
    # 从订单列表中移除
    if hasattr(context, 'order_ids') and order.order_id in context.order_ids:
        context.order_ids.remove(order.order_id)
        SRLogger.info(f"订单 {order.order_id} 已从列表中移除")
期货报单回报（可选）
函数：on_future_trade_rtn
描述：当有报单委托成交后触发

代码
def on_future_trade_rtn(context, order):
参数
字段	类型	描述
context	Context对象	策略上下文对象
order	Order对象	订单信息
例子
def on_future_trade_rtn(context, order):
    SRLogger.info("【期货报单回报】")
    SRLogger.info(f"订单ID: {order.order_id}")
    SRLogger.info(f"合约: {order.order_book_id}")
    SRLogger.info(f"买卖方向: {order.side} (1:买, 2:卖)")
    SRLogger.info(f"开平方向: {order.effect} (0:开, 1:平)")
    SRLogger.info(f"订单价格: {order.price}")
    SRLogger.info(f"下单数量: {order.quantity}")
    SRLogger.info(f"已成交数量: {order.filled_quantity}")
    SRLogger.info(f"剩余数量: {order.unfilled_quantity}")
    SRLogger.info(f"订单状态: {order.status} (1:未成交, 2:已成交, 3:已撤, -1:拒单)")
    SRLogger.info(f"订单信息: {order.message}")
    
    # 如果订单已成交，更新持仓信息
    if order.status == 2:
        futures_account = context.future_account_dict.get(context.account)
        if futures_account and order.order_book_id in futures_account.positions:
            position = futures_account.positions[order.order_book_id]
            SRLogger.info(f"当前多头持仓: {position.buy_quantity}")
            SRLogger.info(f"当前空头持仓: {position.sell_quantity}")
            SRLogger.info(f"多头盈亏: {position.buy_pnl}")
            SRLogger.info(f"空头盈亏: {position.sell_pnl}")
    
    # 从订单ID列表中移除已成交订单
    if hasattr(context, 'order_ids') and order.order_id in context.order_ids:
        context.order_ids.remove(order.order_id)
        SRLogger.info(f"订单 {order.order_id} 已成交，从订单列表中移除")
期货撤单回报（可选）
函数：future_order_cancel
描述：当有报单委托被撤单后触发

代码
def future_order_cancel(context, order):
参数
字段	类型	描述
context	Context对象	策略上下文对象
order	Order对象	订单信息
例子
def future_order_cancel(context, order):
    SRLogger.info("【期货撤单回报】")
    SRLogger.info(f"订单ID: {order.order_id}")
    SRLogger.info(f"合约: {order.order_book_id}")
    SRLogger.info(f"买卖方向: {order.side} (1:买, 2:卖)")
    SRLogger.info(f"开平方向: {order.effect} (0:开, 1:平)")
    SRLogger.info(f"订单状态: {order.status} (3:已撤)")
    
    # 从订单ID列表中移除
    if hasattr(context, 'order_ids') and order.order_id in context.order_ids:
        context.order_ids.remove(order.order_id)
        SRLogger.info(f"订单 {order.order_id} 已撤单，从订单列表中移除")
事件拓展
系统支持自定义事件，详细参考开源代码 src/panda_backtest/backtest_common/system/event/event.py

基础对象说明
context对象
对象：context
描述：全局上下文对象，可在基础函数中传递，同时会内置数据对象

代码
context.变量
内置变量
字段	类型	描述
now	str	当前日期（yyyMMdd）
trade_date	str	交易日期
trade_time	str	交易时间
portfolio_dict	dict	收益信息字典（key为account，value为Portfolio对象）
stock_account_dict	dict	股票账户信息字典（key为account，value为StockAccount对象）
future_account_dict	dict	期货账户信息字典（key为account，value为FutureAccount对象）
sub_future_symbol_list	set	订阅的期货合约列表
sub_stock_symbol_list	set	订阅的股票合约列表
sub_strategy_future_symbol_list	set	策略订阅的期货合约列表
sub_strategy_stock_symbol_list	set	策略订阅的股票合约列表
例子
# 获取当前日期
current_date = context.now

# 获取股票账户
stock_account = context.stock_account_dict['15032863']

# 获取期货账户
future_account = context.future_account_dict['5588']

# 获取订阅的期货合约列表
subscribed_futures = context.sub_future_symbol_list

# 遍历所有期货账户
for account_id, future_account in context.future_account_dict.items():
    SRLogger.info(f"账户 {account_id} 总权益: {future_account.total_value}")
Bar对象
对象：Bar
描述：当前bar行情对象

代码
data[合约]
# 或
bar_dict[合约]
内置变量
字段	类型	描述
symbol	str	合约
open	double	开盘价
high	double	最高价
low	double	最低价
close	double	收盘价
settle	double	结算价（期货）
last	double	最新价
volume	long	成交量
oi	long	持仓量（期货）
turnover	double	成交金额
例子
def handle_data(context, data):
    # 获取平安银行当前bar收盘价
    stock_bar = data['000001.SZ']
    close_price = stock_bar.close
    open_price = stock_bar.open
    high_price = stock_bar.high
    low_price = stock_bar.low
    volume = stock_bar.volume
    
    # 获取黄金2002合约当前bar信息
    future_bar = data['AU2002.SHF']
    close_price = future_bar.close
    settle_price = future_bar.settle  # 结算价
    last_price = future_bar.last  # 最新价
    volume = future_bar.volume  # 成交量
    oi = future_bar.oi  # 持仓量
    turnover = future_bar.turnover  # 成交金额
    
    # 遍历所有订阅的合约
    if hasattr(data, 'future_real_time_bar_map'):
        future_map = data.future_real_time_bar_map
        for symbol in future_map.keys():
            bar = data[symbol]
            SRLogger.info(f"合约 {symbol}: 收盘价={bar.close}, 成交量={bar.volume}")
Order对象
对象：Order
描述：下单返回订单对象

代码
order = order_shares('15032863','000001.SZ', 100)
order = buy_open('5588','AU2002.SHF', 1)
内置变量
字段	类型	描述
order_id	str	订单唯一标识
order_book_id	str	下单合约
side	int	买卖方向（1：买 2：卖）
effect	int	开平方向（0：开，1：平，仅期货）
price	double	订单价格，只有在订单类型为’限价单’的时候才有意义
quantity	int	下单数量
filled_quantity	int	订单已成交数量
unfilled_quantity	int	订单剩余数量
status	int	订单状态（1：未成交，2：已成交，3：已撤，-1：拒单）
message	str	订单信息
例子
def handle_data(context, data):
    # 股票下单
    order = order_shares('15032863','000001.SZ', 100, style=MarketOrderStyle)
    if order:
        SRLogger.info(f"订单ID: {order.order_id}")
        SRLogger.info(f"订单状态: {order.status}")
        # 保存订单ID用于后续撤单
        context.order_ids.append(order.order_id)
    
    # 期货下单
    order = buy_open('5588','AU2002.SHF', 1, style=MarketOrderStyle)
    if order:
        SRLogger.info(f"订单ID: {order.order_id}")
        SRLogger.info(f"买卖方向: {order.side} (1:买, 2:卖)")
        SRLogger.info(f"开平方向: {order.effect} (0:开, 1:平)")
        SRLogger.info(f"已成交数量: {order.filled_quantity}")
        
        # 检查订单是否完全成交
        if order.status == 2 and order.filled_quantity == order.quantity:
            SRLogger.info("订单已完全成交")
StockAccount对象
对象：StockAccount
描述：股票账号信息实体对象

代码
context.stock_account_dict['15032863']
内置变量
字段	类型	描述
total_value	double	总权益
cash	double	可用资金
frozen_cash	double	冻结资金
market_value	double	持仓市值
positions	dict	持仓字典（key为合约，value为StockPositions对象）
例子
def handle_data(context, data):
    # 获取股票账号
    stock_account = context.stock_account_dict.get('15032863')
    if stock_account:
        # 获取账户基本信息
        total_value = stock_account.total_value  # 总权益
        cash = stock_account.cash  # 可用资金
        frozen_cash = stock_account.frozen_cash  # 冻结资金
        market_value = stock_account.market_value  # 持仓市值
        
        SRLogger.info(f"账户总权益: {total_value}")
        SRLogger.info(f"可用资金: {cash}")
        SRLogger.info(f"冻结资金: {frozen_cash}")
        SRLogger.info(f"持仓市值: {market_value}")
        
        # 遍历所有持仓
        positions = stock_account.positions
        if isinstance(positions, dict):
            SRLogger.info(f"持仓数量: {len(positions)}")
            for symbol, position in positions.items():
                SRLogger.info(f"\n持仓合约: {symbol}")
                SRLogger.info(f"  持仓数量: {position.quantity}")
                SRLogger.info(f"  可卖数量: {position.sellable}")
                SRLogger.info(f"  持仓市值: {position.market_value}")
                SRLogger.info(f"  持仓均价: {position.avg_price}")
                SRLogger.info(f"  持仓盈亏: {position.pnl}")
        
        # 检查特定股票的持仓
        if '000001.SZ' in stock_account.positions:
            position = stock_account.positions['000001.SZ']
            if position.quantity > 0:
                SRLogger.info(f"平安银行持仓: {position.quantity} 股")
                SRLogger.info(f"持仓盈亏: {position.pnl}")
StockPosition对象
对象：StockPositions
描述：股票持仓对象

代码
context.stock_account_dict['15032863'].positions['000001.SZ']
内置变量
字段	类型	描述
order_book_id	str	合约
quantity	int	持仓数量
sellable	int	可卖数量
market_value	double	持仓市值
avg_price	double	持仓均价
pnl	double	持仓盈亏
例子
def handle_data(context, data):
    stock_account = context.stock_account_dict.get('15032863')
    if stock_account and '000001.SZ' in stock_account.positions:
        position = stock_account.positions['000001.SZ']
        
        # 获取持仓详细信息
        symbol = position.order_book_id  # 合约代码
        quantity = position.quantity  # 持仓数量
        sellable = position.sellable  # 可卖数量
        market_value = position.market_value  # 持仓市值
        avg_price = position.avg_price  # 持仓均价
        pnl = position.pnl  # 持仓盈亏
        
        SRLogger.info(f"合约: {symbol}")
        SRLogger.info(f"持仓数量: {quantity}")
        SRLogger.info(f"可卖数量: {sellable}")
        SRLogger.info(f"持仓市值: {market_value}")
        SRLogger.info(f"持仓均价: {avg_price}")
        SRLogger.info(f"持仓盈亏: {pnl}")
        
        # 根据持仓情况决定是否卖出
        if quantity > 0 and sellable > 0:
            # 如果盈利超过10%，卖出50%
            if pnl > 0 and (pnl / market_value) > 0.1:
                sell_quantity = int(sellable * 0.5)
                order_shares('15032863', '000001.SZ', -sell_quantity, style=MarketOrderStyle)
FutureAccount对象
对象：FutureAccount
描述：期货账号信息实体对象

代码
context.future_account_dict['5588']
内置变量
字段	类型	描述
total_value	double	总权益
cash	double	可用资金
frozen_cash	double	冻结资金
holding_pnl	double	持仓盈亏
realized_pnl	double	平仓盈亏
margin	double	保证金
transaction_cost	double	手续费
positions	dict	持仓字典（key为合约，value为FuturePositions对象）
例子
def handle_data(context, data):
    # 获取期货账户
    futures_account = context.future_account_dict.get('5588')
    if futures_account:
        # 获取账户基本信息
        total_value = futures_account.total_value  # 总权益
        cash = futures_account.cash  # 可用资金
        frozen_cash = futures_account.frozen_cash  # 冻结资金
        holding_pnl = futures_account.holding_pnl  # 持仓盈亏
        realized_pnl = futures_account.realized_pnl  # 平仓盈亏
        margin = futures_account.margin  # 保证金
        transaction_cost = futures_account.transaction_cost  # 手续费
        
        SRLogger.info(f"账户总权益: {total_value}")
        SRLogger.info(f"可用资金: {cash}")
        SRLogger.info(f"冻结资金: {frozen_cash}")
        SRLogger.info(f"持仓盈亏: {holding_pnl}")
        SRLogger.info(f"平仓盈亏: {realized_pnl}")
        SRLogger.info(f"保证金: {margin}")
        SRLogger.info(f"手续费: {transaction_cost}")
        
        # 计算账户使用率
        if total_value > 0:
            margin_ratio = margin / total_value
            SRLogger.info(f"保证金使用率: {margin_ratio:.2%}")
        
        # 遍历所有持仓
        positions = futures_account.positions
        if isinstance(positions, dict):
            SRLogger.info(f"持仓合约数量: {len(positions)}")
            for symbol, position in positions.items():
                SRLogger.info(f"\n持仓合约: {symbol}")
                SRLogger.info(f"  多头持仓: {position.buy_quantity}")
                SRLogger.info(f"  空头持仓: {position.sell_quantity}")
        
        # 检查特定合约的持仓
        if 'AU2002.SHF' in futures_account.positions:
            position = futures_account.positions['AU2002.SHF']
            if position.buy_quantity > 0:
                SRLogger.info(f"黄金2002多头持仓: {position.buy_quantity} 手")
                SRLogger.info(f"多头盈亏: {position.buy_pnl}")
FuturePosition对象
对象：FuturePositions
描述：期货持仓对象

代码
context.future_account_dict['5588'].positions['AU2601.SHF']
内置变量
字段	类型	描述
order_book_id	str	合约
buy_quantity	int	多头持仓
buy_today_quantity	int	多头今日持仓
closable_buy_quantity	int	多头可平持仓
buy_margin	double	多头保证金
buy_pnl	double	多头累计收益
buy_avg_open_price	double	多头开仓均价
buy_avg_holding_price	double	多头持仓均价
buy_transaction_cost	double	多头手续费
sell_quantity	int	空头持仓
sell_today_quantity	int	空头今日持仓
closable_sell_quantity	int	空头可平持仓
sell_margin	double	空头保证金
sell_pnl	double	空头累计收益
sell_avg_open_price	double	空头开仓均价
sell_avg_holding_price	double	空头持仓均价
sell_transaction_cost	double	空头手续费
pnl	double	总盈亏
daily_pnl	double	当日盈亏
holding_pnl	double	持仓盈亏
realized_pnl	double	已实现盈亏
transaction_cost	double	总手续费
margin	double	总保证金
market_value	double	持仓市值
例子
def handle_data(context, data):
    futures_account = context.future_account_dict.get('5588')
    if futures_account and 'AU2002.SHF' in futures_account.positions:
        position = futures_account.positions['AU2002.SHF']
        
        # 获取合约信息
        symbol = position.order_book_id
        
        # 多头信息
        buy_quantity = position.buy_quantity  # 多头持仓
        buy_today_quantity = position.buy_today_quantity  # 多头今日持仓
        closable_buy_quantity = position.closable_buy_quantity  # 多头可平持仓
        buy_margin = position.buy_margin  # 多头保证金
        buy_pnl = position.buy_pnl  # 多头累计收益
        buy_avg_open_price = position.buy_avg_open_price  # 多头开仓均价
        buy_avg_holding_price = position.buy_avg_holding_price  # 多头持仓均价
        buy_transaction_cost = position.buy_transaction_cost  # 多头手续费
        
        # 空头信息
        sell_quantity = position.sell_quantity  # 空头持仓
        sell_today_quantity = position.sell_today_quantity  # 空头今日持仓
        closable_sell_quantity = position.closable_sell_quantity  # 空头可平持仓
        sell_margin = position.sell_margin  # 空头保证金
        sell_pnl = position.sell_pnl  # 空头累计收益
        sell_avg_open_price = position.sell_avg_open_price  # 空头开仓均价
        sell_avg_holding_price = position.sell_avg_holding_price  # 空头持仓均价
        sell_transaction_cost = position.sell_transaction_cost  # 空头手续费
        
        # 总体信息
        total_pnl = position.pnl  # 总盈亏
        daily_pnl = position.daily_pnl  # 当日盈亏
        holding_pnl = position.holding_pnl  # 持仓盈亏
        realized_pnl = position.realized_pnl  # 已实现盈亏
        total_transaction_cost = position.transaction_cost  # 总手续费
        total_margin = position.margin  # 总保证金
        market_value = position.market_value  # 持仓市值
        
        SRLogger.info(f"合约: {symbol}")
        SRLogger.info(f"\n多头信息:")
        SRLogger.info(f"  多头持仓: {buy_quantity}")
        SRLogger.info(f"  多头可平: {closable_buy_quantity}")
        SRLogger.info(f"  多头盈亏: {buy_pnl}")
        SRLogger.info(f"  多头开仓均价: {buy_avg_open_price}")
        SRLogger.info(f"\n空头信息:")
        SRLogger.info(f"  空头持仓: {sell_quantity}")
        SRLogger.info(f"  空头可平: {closable_sell_quantity}")
        SRLogger.info(f"  空头盈亏: {sell_pnl}")
        SRLogger.info(f"  空头开仓均价: {sell_avg_open_price}")
        SRLogger.info(f"\n总体信息:")
        SRLogger.info(f"  总盈亏: {total_pnl}")
        SRLogger.info(f"  持仓盈亏: {holding_pnl}")
        SRLogger.info(f"  总保证金: {total_margin}")
        
        # 根据持仓情况决定是否平仓
        if buy_quantity > 0 and closable_buy_quantity > 0:
            # 如果多头盈利超过5%，平掉一半
            if buy_pnl > 0 and (buy_pnl / (buy_avg_open_price * buy_quantity)) > 0.05:
                close_quantity = int(closable_buy_quantity * 0.5)
                sell_close('5588', symbol, close_quantity, style=MarketOrderStyle)
        
        if sell_quantity > 0 and closable_sell_quantity > 0:
            # 如果空头亏损超过3%，止损平仓
            if sell_pnl < 0 and abs(sell_pnl / (sell_avg_open_price * sell_quantity)) > 0.03:
                buy_close('5588', symbol, closable_sell_quantity, style=MarketOrderStyle)
交易函数
股票交易
指定股数下单
函数：order_shares
描述：指定股数进行股票交易

代码
def order_shares(account, symbol, amount, style):
参数
字段	类型	描述
account	str	股票账号
symbol	str	股票合约
amount	int	股数（正数代表买入，负数代表卖出）
style	enum	订单类型, MarketOrderStyle=市价单, LimitOrderStyle=限价单
输出参数
字段	类型	描述
order	Order对象	订单对象
例子
def handle_data(context, data):
    # 按照市价最新价买入100股平安银行
    order = order_shares('15032863','000001.SZ', 100, style=MarketOrderStyle)
    if order:
        SRLogger.info(f"买入订单ID: {order.order_id}")
        context.order_ids.append(order.order_id)
    
    # 按照市价最新价卖出100股平安银行
    order = order_shares('15032863','000001.SZ', -100, style=MarketOrderStyle)
    if order:
        SRLogger.info(f"卖出订单ID: {order.order_id}")
    
    # 按照12.89价格买入100股平安银行（限价单）
    order = order_shares('15032863','000001.SZ', 100, style=LimitOrderStyle(12.89))
    if order:
        SRLogger.info(f"限价买入订单ID: {order.order_id}")
        # 限价单可以撤单
        if order.status == 1:  # 未成交
            cancel_order('15032863', order.order_id)
按照目标持仓下单
函数：target_stock_group_order
描述：按照目标持仓下单，在1分钟内，以最小代价，将当前持仓改为目标持仓

代码
def target_stock_group_order(account, symbol_dict):
参数
字段	类型	描述
account	str	股票账号
symbol_dict	dict	股票合约和股数 （{“000001.SZ”:100}）
输出参数
字段	类型	描述
order	Order对象	订单对象
例子
def handle_data(context, data):
    # 平掉当前持仓，买入中国平安100股
    target_dict = {'000001.SZ': 100}
    order = target_stock_group_order('15032863', target_dict)
    if order:
        SRLogger.info(f"目标持仓下单成功，订单ID: {order.order_id}")
    
    # 多只股票目标持仓
    target_dict = {
        '000001.SZ': 1000,  # 平安银行1000股
        '600000.SH': 500,    # 浦发银行500股
        '000002.SZ': 200    # 万科A 200股
    }
    order = target_stock_group_order('15032863', target_dict)
撤单
函数：cancel_order
描述：股票撤单，一般只用于限价单挂单，市价单为即成即撤无法撤单

代码
def cancel_order(account, order_id):
参数
字段	类型	描述
account	str	股票账号
order_id	str	订单id
输出参数
字段	类型	描述
result	bool	是否撤单成功
例子
def handle_data(context, data):
    # 下限价单
    order = order_shares('15032863','000001.SZ', 100, style=LimitOrderStyle(12.50))
    if order:
        context.order_ids.append(order.order_id)
    
    # 对订单进行撤单
    if context.order_ids:
        for order_id in context.order_ids[:]:  # 使用切片复制列表
            result = cancel_order('15032863', order_id)
            if result:
                SRLogger.info(f"撤单成功，订单ID: {order_id}")
                context.order_ids.remove(order_id)
            else:
                SRLogger.info(f"撤单失败，订单ID: {order_id}")
期货交易
买入开仓
函数：buy_open
描述：期货买入开仓

代码
def buy_open(account, symbol, amount, style):
参数
字段	类型	描述
account	str	期货账号
symbol	str	期货合约
amount	int	手数
style	enum	订单类型, MarketOrderStyle=市价单, LimitOrderStyle=限价单
输出参数
字段	类型	描述
order	Order对象	订单对象
例子
def handle_data(context, data):
    # 按照市价最新价开仓买入1手AG2002
    order = buy_open('5588','AG2002.SHF', 1, style=MarketOrderStyle)
    if order:
        SRLogger.info(f"买入开仓订单ID: {order.order_id}")
        SRLogger.info(f"订单状态: {order.status}")
        context.order_ids.append(order.order_id)
    
    # 按照4280价格开仓买入1手AG2002（限价单）
    current_price = data['AG2002.SHF'].close
    limit_price = current_price * 0.99  # 低于当前价1%
    order = buy_open('5588','AG2002.SHF', 1, style=LimitOrderStyle(limit_price))
    if order:
        SRLogger.info(f"限价买入开仓订单ID: {order.order_id}")
        SRLogger.info(f"限价: {limit_price}")
卖出开仓
函数：sell_open
描述：期货卖出开仓

代码
def sell_open(account, symbol, amount, style):
参数
字段	类型	描述
account	str	期货账号
symbol	symbol	期货合约
amount	int	手数
style	enum	订单类型, MarketOrderStyle=市价单, LimitOrderStyle=限价单
输出参数
字段	类型	描述
order	Order对象	订单对象
例子
def handle_data(context, data):
    # 按照市价最新价开仓卖出1手AG2002
    order = sell_open('5588','AG2002.SHF', 1, style=MarketOrderStyle)
    if order:
        SRLogger.info(f"卖出开仓订单ID: {order.order_id}")
        context.order_ids.append(order.order_id)
    
    # 按照4280价格开仓卖出1手AG2002（限价单）
    current_price = data['AG2002.SHF'].close
    limit_price = current_price * 1.01  # 高于当前价1%
    order = sell_open('5588','AG2002.SHF', 1, style=LimitOrderStyle(limit_price))
    if order:
        SRLogger.info(f"限价卖出开仓订单ID: {order.order_id}")
买入平仓
函数：buy_close
描述：期货买入平仓，即平空头仓位

代码
def buy_close(account, symbol, amount, style):
参数
字段	类型	描述
account	str	期货账号
symbol	str	期货合约
amount	int	手数
style	enum	订单类型, MarketOrderStyle=市价单, LimitOrderStyle=限价单
输出参数
字段	类型	描述
order	Order对象	订单对象
例子
def handle_data(context, data):
    # 获取账户和持仓信息
    futures_account = context.future_account_dict.get('5588')
    if futures_account and 'AG2002.SHF' in futures_account.positions:
        position = futures_account.positions['AG2002.SHF']
        
        # 如果有空头持仓，平掉空头
        if position.sell_quantity > 0:
            closable_quantity = position.closable_sell_quantity
            if closable_quantity > 0:
                # 按照市价最新价平仓空头
                order = buy_close('5588','AG2002.SHF', closable_quantity, style=MarketOrderStyle)
                if order:
                    SRLogger.info(f"买入平仓订单ID: {order.order_id}")
                    SRLogger.info(f"平仓数量: {closable_quantity} 手")
    
    # 限价平仓示例
    current_price = data['AG2002.SHF'].close
    limit_price = current_price * 0.99  # 低于当前价1%平仓
    order = buy_close('5588','AG2002.SHF', 1, style=LimitOrderStyle(limit_price))
    if order:
        SRLogger.info(f"限价买入平仓订单ID: {order.order_id}")
卖出平仓
函数：sell_close
描述：期货卖出平仓，即平多头仓位

代码
def sell_close(account, symbol, amount, style):
参数
字段	类型	描述
account	str	期货账号
symbol	str	期货合约
amount	int	手数
style	enum	订单类型, MarketOrderStyle=市价单, LimitOrderStyle=限价单
输出参数
字段	类型	描述
order	Order对象	订单对象
例子
def handle_data(context, data):
    # 获取账户和持仓信息
    futures_account = context.future_account_dict.get('5588')
    if futures_account and 'AG2002.SHF' in futures_account.positions:
        position = futures_account.positions['AG2002.SHF']
        
        # 如果有多头持仓，平掉多头
        if position.buy_quantity > 0:
            closable_quantity = position.closable_buy_quantity
            if closable_quantity > 0:
                # 按照市价最新价平仓多头
                order = sell_close('5588','AG2002.SHF', closable_quantity, style=MarketOrderStyle)
                if order:
                    SRLogger.info(f"卖出平仓订单ID: {order.order_id}")
                    SRLogger.info(f"平仓数量: {closable_quantity} 手")
    
    # 限价平仓示例
    current_price = data['AG2002.SHF'].close
    limit_price = current_price * 1.01  # 高于当前价1%平仓
    order = sell_close('5588','AG2002.SHF', 1, style=LimitOrderStyle(limit_price))
    if order:
        SRLogger.info(f"限价卖出平仓订单ID: {order.order_id}")
按照目标持仓下单
函数：target_future_group_order
描述：按照目标持仓下单，在1分钟内，以最小代价，将当前持仓改为目标持仓

代码
def target_future_group_order(account, long_symbol_dict, short_symbol_dict):
参数
字段	类型	描述
account	str	期货账号
long_symbol_dict	dict	多头期货合约和手数 （{“AG2509.SHF”:1}）
short_symbol_dict	dict	空头期货合约和手数 （{“AG2509.SHF”:1}）
输出参数
字段	类型	描述
order	Order对象	订单对象
例子
def handle_data(context, data):
    # 平掉当前持仓，建立多头AG2505.SHF 1手，空头A2505.DCE 1手
    long_dict = {"AG2505.SHF": 1}
    short_dict = {"A2505.DCE": 1}
    order = target_future_group_order('5588', long_dict, short_dict)
    if order:
        SRLogger.info(f"目标持仓下单成功，订单ID: {order.order_id}")
    
    # 多合约目标持仓
    long_dict = {
        "AG2505.SHF": 2,  # 黄金多头2手
        "AU2506.SHF": 1   # 白银多头1手
    }
    short_dict = {
        "A2505.DCE": 1,   # 豆粕空头1手
        "RB2505.SHF": 1   # 螺纹钢空头1手
    }
    order = target_future_group_order('5588', long_dict, short_dict)
    
    # 只建立多头，平掉所有空头
    long_dict = {"AG2505.SHF": 1}
    short_dict = {}  # 空字典表示平掉所有空头
    order = target_future_group_order('5588', long_dict, short_dict)
    
    # 只建立空头，平掉所有多头
    long_dict = {}  # 空字典表示平掉所有多头
    short_dict = {"A2505.DCE": 1}
    order = target_future_group_order('5588', long_dict, short_dict)
期货撤单
函数：cancel_future_order
描述：期货撤单，一般只用于限价单挂单，市价单为即成即撤无法撤单

代码
def cancel_future_order(account, order_id):
参数
字段	类型	描述
account	str	期货账号
order_id	str	订单id
输出参数
字段	类型	描述
result	bool	是否撤单成功
例子
def handle_data(context, data):
    # 下限价单
    current_price = data['AG2002.SHF'].close
    limit_price = current_price * 0.99
    order = buy_open('5588','AG2002.SHF', 1, style=LimitOrderStyle(limit_price))
    if order:
        context.order_ids.append(order.order_id)
    
    # 对订单进行撤单
    if context.order_ids:
        for order_id in context.order_ids[:]:  # 使用切片复制列表
            result = cancel_future_order('5588', order_id)
            if result:
                SRLogger.info(f"撤单成功，订单ID: {order_id}")
                context.order_ids.remove(order_id)
            else:
                SRLogger.info(f"撤单失败，订单ID: {order_id}")
完整案例
案例1：根据期货因子下单
描述：根据因子数据（DataFrame格式）进行期货交易，因子格式为dataframe，列为symbol、factor_name、value

完整代码
from panda_backtest.api.api import *
from panda_backtest.api.future_api import *
from panda_backtest.backtest_common.type.order_type import MarketOrderStyle, LimitOrderStyle
import pandas as pd
import numpy as np
import datetime

def initialize(context):
    """
    策略初始化
    """
    # 策略参数设置
    context.s_top_n = 5               # 每次买入的前N只标的
    context.s_rb_period = 5            # 调仓周期（单位：天）
    context.account = '5588'          # 期货账号
    
    # 预处理因子数据
    if hasattr(context, 'df_factor') and context.df_factor is not None:
        context.df_factor = context.df_factor.reset_index()
        # 获取因子列名（第三列，索引为2）
        factor_column = context.df_factor.columns[2]
        context.df_factor['factor_value'] = pd.to_numeric(
            context.df_factor
            .groupby('symbol')[factor_column]
            .shift(1),
            errors='coerce'
        )
        SRLogger.info(f"因子数据预处理完成，因子列: {factor_column}")
        SRLogger.info(f"因子数据行数: {len(context.df_factor)}")
    else:
        SRLogger.warning("未找到因子数据 df_factor")
    
    SRLogger.info("策略初始化完成")
    SRLogger.info(f"期货账号: {context.account}")
    SRLogger.info(f"每次买入前 {context.s_top_n} 只标的")
    SRLogger.info(f"调仓周期: {context.s_rb_period} 天")


def handle_data(context, data):
    """
    策略主函数
    """
    # 检查是否为调仓日
    if int(context.now) % context.s_rb_period != 0:
        return  # 非调仓日不执行任何操作
    
    SRLogger.info(f"调仓日：{context.now}")
    today = context.now
    
    # 检查因子数据是否存在
    if not hasattr(context, 'df_factor') or context.df_factor is None:
        SRLogger.warning("因子数据不存在，跳过本次调仓")
        return
    
    # 获取今日因子值并按值排序
    df_today = context.df_factor[context.df_factor["date"] == today]
    if df_today.empty:
        SRLogger.warning(f"日期 {today} 无因子数据，跳过本次调仓")
        return
    
    df_today_sorted = df_today.sort_values('factor_value', ascending=False)
    buy_list = df_today_sorted.head(context.s_top_n)['symbol'].tolist()
    
    SRLogger.info(f"选中的标的: {buy_list}")
    
    # 获取行情数据
    try:
        quotation_df = future_api_quotation(
            symbol_list=buy_list, 
            start_date=today, 
            end_date=today, 
            period="1d"
        )
        if quotation_df.empty:
            SRLogger.warning("行情数据为空，跳过本次调仓")
            return
        
        # 获取主力合约
        quotation_df['symbol'] = quotation_df['dominant_id'] + '.' + quotation_df['exchange']
        per_close = quotation_df.set_index('symbol')['close'].to_dict()
        symbols = list(per_close.keys())
        
        SRLogger.info(f"主力合约映射: {dict(zip(buy_list, symbols))}")
    except Exception as e:
        SRLogger.error(f"获取行情数据失败: {e}")
        return
    
    # 获取合约乘数
    try:
        contract_mul_df = future_api_symbol_contractmul(symbols)
        if contract_mul_df.empty:
            SRLogger.warning("合约乘数数据为空，跳过本次调仓")
            return
        contract_mul = contract_mul_df.set_index('symbol')['contractmul'].to_dict()
    except Exception as e:
        SRLogger.error(f"获取合约乘数失败: {e}")
        return
    
    # 获取账户信息
    futures_account = context.future_account_dict.get(context.account)
    if not futures_account:
        SRLogger.error(f"未找到期货账户: {context.account}")
        return
    
    total_value = futures_account.total_value
    SRLogger.info(f"账户总权益: {total_value}")
    
    # 构建下单指令
    orders = {}
    for symbol in symbols:
        if symbol not in contract_mul or symbol not in per_close:
            SRLogger.warning(f"缺失数据: {symbol}")
            continue
        
        # 计算下单手数：总权益 / (合约乘数 * 价格 * 标的数量)
        hands = total_value / (contract_mul[symbol] * per_close[symbol] * context.s_top_n)
        hands = np.floor(np.abs(hands))
        orders[symbol] = int(hands)
        
        SRLogger.info(f"{symbol}: 合约乘数={contract_mul[symbol]}, 收盘价={per_close[symbol]}, 下单手数={hands}")
    
    if orders:
        SRLogger.info("下单指令:")
        order_df = pd.DataFrame(list(orders.items()), columns=['symbol', 'order_hands'])
        SRLogger.info(order_df)
        
        # 执行目标持仓下单
        try:
            target_future_group_order(context.account, orders, {})
            SRLogger.info("目标持仓下单完成")
        except Exception as e:
            SRLogger.error(f"目标持仓下单失败: {e}")
    else:
        SRLogger.warning("无有效下单指令")


def before_trading(context):
    """
    开盘前运行
    """
    SRLogger.info(f"开盘前运行 - 当前日期: {context.now}")
    
    # 获取账户信息
    futures_account = context.future_account_dict.get(context.account)
    if futures_account:
        SRLogger.info(f"账户总权益: {futures_account.total_value}")
        SRLogger.info(f"可用资金: {futures_account.cash}")
        SRLogger.info(f"保证金: {futures_account.margin}")
        
        # 打印当前持仓
        positions = futures_account.positions
        if isinstance(positions, dict) and positions:
            SRLogger.info(f"当前持仓合约数量: {len(positions)}")
            for symbol, position in positions.items():
                SRLogger.info(f"  {symbol}: 多头={position.buy_quantity}, 空头={position.sell_quantity}")


def after_trading(context):
    """
    收盘后运行
    """
    SRLogger.info(f"收盘后运行 - 当前日期: {context.now}")
    
    # 获取账户信息
    futures_account = context.future_account_dict.get(context.account)
    if futures_account:
        SRLogger.info(f"账户总权益: {futures_account.total_value}")
        SRLogger.info(f"持仓盈亏: {futures_account.holding_pnl}")
        SRLogger.info(f"平仓盈亏: {futures_account.realized_pnl}")
案例2：双均线策略（期货）
描述：基于双均线的期货交易策略，当短期均线上穿长期均线时买入开仓，下穿时卖出平仓

完整代码
from panda_backtest.api.api import *
from panda_backtest.api.future_api import *
from panda_backtest.backtest_common.type.order_type import MarketOrderStyle
import numpy as np

def initialize(context):
    """
    策略初始化
    """
    # 期货账号
    context.account = '5588'
    
    # 关注的期货合约
    context.future_contract = 'RB2601.SHF'
    
    # 短期和长期均线窗口
    context.short_window = 5
    context.long_window = 20
    
    # 用于保存历史价格数据
    context.historical_prices = []
    
    # 用于保存订单ID
    context.order_ids = []
    
    SRLogger.info("策略初始化完成")
    SRLogger.info(f"期货账号: {context.account}")
    SRLogger.info(f"关注合约: {context.future_contract}")
    SRLogger.info(f"短期均线: {context.short_window} 日")
    SRLogger.info(f"长期均线: {context.long_window} 日")


def handle_data(context, data):
    """
    策略主函数
    """
    # 获取行情数据
    try:
        contract_key = str(context.future_contract) if context.future_contract else None
        if not contract_key:
            SRLogger.warning("context.future_contract为空")
            return
        
        bar = data[contract_key]
    except KeyError:
        SRLogger.warning(f"合约 {contract_key} 不在data中")
        return
    except Exception as e:
        SRLogger.error(f"获取行情数据失败: {e}")
        return
    
    close_price = bar.close
    if close_price == 0:
        SRLogger.warning("收盘价为0，跳过本次处理")
        return
    
    # 保存价格到历史数据
    context.historical_prices.append(close_price)
    
    # 如果不足以计算均线，则退出
    if len(context.historical_prices) < context.long_window:
        SRLogger.info(f"历史数据不足，当前: {len(context.historical_prices)}, 需要: {context.long_window}")
        return
    
    # 剪切历史价格，保持长度为长均线窗口
    if len(context.historical_prices) > context.long_window:
        context.historical_prices.pop(0)
    
    # 计算均线
    short_mavg = np.mean(context.historical_prices[-context.short_window:])
    long_mavg = np.mean(context.historical_prices)
    
    SRLogger.info(f"短期均线({context.short_window}日): {short_mavg:.2f}")
    SRLogger.info(f"长期均线({context.long_window}日): {long_mavg:.2f}")
    
    # 获取期货账户信息
    futures_account = context.future_account_dict.get(context.account)
    if not futures_account:
        SRLogger.warning(f"未找到期货账户: {context.account}")
        return
    
    # 检查是否有持仓
    has_position = (context.future_contract in futures_account.positions and
                   (futures_account.positions[context.future_contract].buy_quantity > 0 or
                    futures_account.positions[context.future_contract].sell_quantity > 0))
    
    if not has_position:
        # 无持仓情况下，检查开仓信号（双均线金叉、死叉）
        SRLogger.info("当前无持仓，检查开仓信号...")
        
        if short_mavg > long_mavg:
            # 金叉买入开仓
            hands = int(futures_account.total_value * 0.05 // close_price)
            if hands > 0:
                SRLogger.info(f"【买入开仓】金叉信号，准备买入 {hands} 手")
                order = buy_open(context.account, context.future_contract, hands, style=MarketOrderStyle)
                if order:
                    context.order_ids.append(order.order_id)
                    SRLogger.info(f"✅ 买入开仓成功，订单ID: {order.order_id}")
                else:
                    SRLogger.warning("❌ 买入开仓失败")
        elif short_mavg < long_mavg:
            # 死叉卖出开仓
            hands = int(futures_account.total_value * 0.05 // close_price)
            if hands > 0:
                SRLogger.info(f"【卖出开仓】死叉信号，准备卖出 {hands} 手")
                order = sell_open(context.account, context.future_contract, hands, style=MarketOrderStyle)
                if order:
                    context.order_ids.append(order.order_id)
                    SRLogger.info(f"✅ 卖出开仓成功，订单ID: {order.order_id}")
                else:
                    SRLogger.warning("❌ 卖出开仓失败")
    else:
        # 如果当前持仓，检查平仓信号（双均线死叉、金叉）
        position = futures_account.positions[context.future_contract]
        SRLogger.info("当前有持仓，检查平仓信号...")
        
        if short_mavg < long_mavg and position.buy_quantity > 0:
            # 死叉买入平仓（卖出现有多头）
            closable_hands = position.closable_buy_quantity
            if closable_hands > 0:
                SRLogger.info(f"【卖出平仓】死叉信号，准备平多头 {closable_hands} 手")
                order = sell_close(context.account, context.future_contract, closable_hands, style=MarketOrderStyle)
                if order:
                    context.order_ids.append(order.order_id)
                    SRLogger.info(f"✅ 卖出平仓成功，订单ID: {order.order_id}")
                else:
                    SRLogger.warning("❌ 卖出平仓失败")
        elif short_mavg > long_mavg and position.sell_quantity > 0:
            # 金叉卖出平仓（买入现有空头）
            closable_hands = position.closable_sell_quantity
            if closable_hands > 0:
                SRLogger.info(f"【买入平仓】金叉信号，准备平空头 {closable_hands} 手")
                order = buy_close(context.account, context.future_contract, closable_hands, style=MarketOrderStyle)
                if order:
                    context.order_ids.append(order.order_id)
                    SRLogger.info(f"✅ 买入平仓成功，订单ID: {order.order_id}")
                else:
                    SRLogger.warning("❌ 买入平仓失败")


def on_future_trade_rtn(context, order):
    """
    期货报单回报
    """
    SRLogger.info("【期货报单回报】")
    SRLogger.info(f"订单ID: {order.order_id}")
    SRLogger.info(f"合约: {order.order_book_id}")
    SRLogger.info(f"买卖方向: {order.side} (1:买, 2:卖)")
    SRLogger.info(f"开平方向: {order.effect} (0:开, 1:平)")
    SRLogger.info(f"订单状态: {order.status} (1:未成交, 2:已成交, 3:已撤, -1:拒单)")
    
    # 如果订单已成交，从订单ID列表中移除
    if order.status == 2 and order.order_id in context.order_ids:
        context.order_ids.remove(order.order_id)
        SRLogger.info(f"✅ 订单 {order.order_id} 已成交，从订单列表中移除")
案例3：获取并打印账户和持仓信息
描述：在handle_data中获取并打印所有账户信息、持仓信息和行情信息

完整代码
from panda_backtest.api.api import *

def handle_data(context, data):
    """
    获取并打印所有信息
    """
    # ==================== 1. 收集订阅合约的行情信息 ====================
    subscribed_symbols = []
    quotation_info_list = []
    
    # 从context中获取订阅的合约列表
    try:
        if hasattr(context, 'sub_future_symbol_list') and context.sub_future_symbol_list:
            subscribed_symbols.extend(list(context.sub_future_symbol_list))
    except Exception:
        pass
    
    try:
        if hasattr(context, 'sub_strategy_future_symbol_list') and context.sub_strategy_future_symbol_list:
            for symbol in context.sub_strategy_future_symbol_list:
                if symbol not in subscribed_symbols:
                    subscribed_symbols.append(symbol)
    except Exception:
        pass
    
    # 从data中获取可用的合约
    try:
        if hasattr(data, 'future_real_time_bar_map'):
            future_map = data.future_real_time_bar_map
            if hasattr(future_map, 'keys'):
                for symbol in future_map.keys():
                    if symbol not in subscribed_symbols:
                        subscribed_symbols.append(symbol)
    except Exception:
        pass
    
    # 收集每个合约的行情信息
    for symbol in subscribed_symbols:
        try:
            bar = data[symbol]
            quotation_info = (
                f"{symbol}: "
                f"open={bar.open}, high={bar.high}, low={bar.low}, close={bar.close}, "
                f"last={bar.last}, settle={bar.settle}, volume={bar.volume}, "
                f"oi={bar.oi}, turnover={bar.turnover}"
            )
            quotation_info_list.append(quotation_info)
        except Exception:
            pass
    
    # ==================== 2. 收集账户信息 ====================
    account_info_list = []
    
    try:
        if hasattr(context, 'future_account_dict') and context.future_account_dict:
            for account_id, futures_account in context.future_account_dict.items():
                try:
                    account_info = (
                        f"账户{account_id}: "
                        f"总权益={futures_account.total_value}, "
                        f"可用资金={futures_account.cash}, "
                        f"冻结资金={futures_account.frozen_cash}, "
                        f"持仓盈亏={futures_account.holding_pnl}, "
                        f"平仓盈亏={futures_account.realized_pnl}, "
                        f"保证金={futures_account.margin}, "
                        f"手续费={futures_account.transaction_cost}"
                    )
                    account_info_list.append(account_info)
                except Exception:
                    pass
    except Exception:
        pass
    
    # ==================== 3. 收集持仓信息 ====================
    position_info_list = []
    
    try:
        if hasattr(context, 'future_account_dict') and context.future_account_dict:
            for account_id, futures_account in context.future_account_dict.items():
                try:
                    positions = futures_account.positions
                    positions_keys = []
                    
                    # 处理positions是dict的情况
                    if isinstance(positions, dict):
                        positions_keys = list(positions.keys())
                    # 处理positions是FuturePositions对象的情况
                    elif hasattr(positions, 'keys'):
                        try:
                            positions_keys = list(positions.keys())
                        except Exception:
                            pass
                    
                    # 收集每个持仓的信息
                    for symbol in positions_keys:
                        try:
                            position = positions[symbol]
                            position_info = (
                                f"账户{account_id}-{symbol}: "
                                f"合约={position.order_book_id}, "
                                f"多头持仓={position.buy_quantity}, "
                                f"多头可平={position.closable_buy_quantity}, "
                                f"多头保证金={position.buy_margin}, "
                                f"多头盈亏={position.buy_pnl}, "
                                f"多头开仓均价={position.buy_avg_open_price}, "
                                f"多头持仓均价={position.buy_avg_holding_price}, "
                                f"空头持仓={position.sell_quantity}, "
                                f"空头可平={position.closable_sell_quantity}, "
                                f"空头保证金={position.sell_margin}, "
                                f"空头盈亏={position.sell_pnl}, "
                                f"空头开仓均价={position.sell_avg_open_price}, "
                                f"空头持仓均价={position.sell_avg_holding_price}, "
                                f"总盈亏={position.pnl}, "
                                f"手续费={position.transaction_cost}, "
                                f"保证金={position.margin}"
                            )
                            position_info_list.append(position_info)
                        except Exception:
                            pass
                except Exception:
                    pass
    except Exception:
        pass
    
    # ==================== 整合打印三行日志 ====================
    # 第一行：合约行情信息
    quotation_str = " | ".join(quotation_info_list) if quotation_info_list else "无订阅合约行情"
    SRLogger.info(f"【合约行情信息】{quotation_str}")
    
    # 第二行：账户信息
    account_str = " | ".join(account_info_list) if account_info_list else "无期货账户"
    SRLogger.info(f"【账户信息】{account_str}")
    
    # 第三行：持仓信息
    position_str = " | ".join(position_info_list) if position_info_list else "无持仓"
    SRLogger.info(f"【持仓信息】{position_str}")
注意事项
引用路径：

回测环境：from panda_backtest.api.api import *
仿真/实盘环境：from panda_trading.trading_common.api.api import *
订单类型：

MarketOrderStyle：市价单，立即成交
LimitOrderStyle(price)：限价单，需要指定价格
持仓对象：

positions可能是dict类型或FuturePositions对象
访问时需要先判断类型，使用isinstance(positions, dict)或hasattr(positions, 'keys')
日期格式：

所有日期参数格式为：yyyMMdd（如：20250101）
错误处理：

建议对所有API调用和对象访问进行异常处理
使用try-except捕获可能的异常
常见问题
Q1: 如何获取所有账户的持仓信息？
for account_id, futures_account in context.future_account_dict.items():
    positions = futures_account.positions
    if isinstance(positions, dict):
        for symbol, position in positions.items():
            print(f"账户{account_id} 合约{symbol}: 多头={position.buy_quantity}, 空头={position.sell_quantity}")
Q2: 如何判断是否有持仓？
futures_account = context.future_account_dict.get('5588')
if futures_account and 'RB2601.SHF' in futures_account.positions:
    position = futures_account.positions['RB2601.SHF']
    has_position = position.buy_quantity > 0 or position.sell_quantity > 0
Q3: 如何计算持仓市值？
# 获取合约乘数
contract_mul_df = future_api_symbol_contractmul(symbol_list=['RB2601.SHF'])
mul = contract_mul_df.iloc[0]['contractmul']

# 获取当前价格
bar = data['RB2601.SHF']
current_price = bar.close

# 获取持仓
position = futures_account.positions['RB2601.SHF']
long_value = position.buy_quantity * current_price * mul
short_value = position.sell_quantity * current_price * mul
total_value = long_value + short_value
Q4: 如何获取主力合约？
# 查询主力合约
result = future_api_domain_symbol(symbol="AG88", date=context.now)
if result:
    dominant_contract = result.get('trading_code') + '.' + result.get('exchange')
    print(f"主力合约: {dominant_contract}")
文档版本: v1.0
最后更新: 2025-01-XX

最后一次编辑于 2025年12月29日