#!/usr/bin/env python3
"""
龙虎榜 V4 评分模型 + V3/V4 回测对比
=====================================
V3 模型: 机构(30) + 北向(25) + 连续上榜(20) + 涨停(15) + 外资(10) = 100
V4 模型: V3 + 改进A(反转检测) + 改进B(内外资一致性) + 改进C(连续上榜场景化) + 改进D(时间衰减)

数据源: akshare (东方财富龙虎榜)
数据窗口: 6天滚动

运行: source .venv/bin/activate && python Resources/scripts/lhb_v4_scoring.py
"""

import json
import os
import sys
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import akshare as ak
import pandas as pd
import numpy as np

# --- 配置 ---
VAULT = Path("/home/dr/Documents/obsidian-notes")
OUTPUT_DIR = VAULT / "5.Finance/投研日记"
DATA_DIR = VAULT / "5.Finance/DailyData/lhb-detail"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# 数据窗口天数
WINDOW_DAYS = 6

# 外资投行名称关键词
FOREIGN_BROKER_KEYWORDS = [
    "摩根士丹利", "摩根大通", "J.P. Morgan", "Morgan Stanley",
    "高盛", "Goldman Sachs", "瑞银", "UBS", "花旗", "Citigroup",
    "汇丰", "HSBC", "美林", "Merrill Lynch", "野村", "Nomura",
    "瑞信", "Credit Suisse", "巴克莱", "Barclays",
    "德意志", "Deutsche Bank", "法国巴黎", "BNP Paribas",
    "渣打", "Standard Chartered", "麦格理", "Macquarie",
    "里昂", "CLSA",
]

# 代理设置
PROXY = "http://127.0.0.1:7890"


def setup_proxy():
    os.environ["https_proxy"] = PROXY
    os.environ["http_proxy"] = PROXY


# --- 数据模型 ---
@dataclass
class SeatData:
    """单个席位的交易数据"""
    name: str
    buy_amount: float  # 亿
    sell_amount: float  # 亿
    net_amount: float  # 亿
    seat_type: str  # institution / north_bound / foreign_broker / other


@dataclass
class StockDayData:
    """单只股票单日龙虎榜数据"""
    code: str
    name: str
    date: str
    close_price: float
    change_pct: float
    total_net_buy: float  # 龙虎榜总净买额(亿)
    total_buy: float
    total_sell: float
    turnover_rate: float  # 换手率(%)
    market_cap: float  # 流通市值(亿)
    reason: str  # 上榜原因
    seats: list[SeatData] = field(default_factory=list)

    # 聚合值（按席位类型累加）
    inst_net: float = 0.0  # 机构净买入
    north_net: float = 0.0  # 北向净买入
    foreign_net: float = 0.0  # 外资投行净买入
    limit_up_net: float = 0.0  # 涨停相关净买入（含"涨幅"原因的条目）

    @property
    def is_sell_signal(self) -> bool:
        """当日是否净卖出"""
        return self.total_net_buy < 0


@dataclass
class StockAgg:
    """股票在窗口期内的聚合数据"""
    code: str
    name: str
    days: list[StockDayData] = field(default_factory=list)
    first_date: str = ""
    last_date: str = ""

    @property
    def consecutive_days(self) -> int:
        return len(self.days)

    # 累计值（简单累加）
    @property
    def inst_net_total(self) -> float:
        return sum(d.inst_net for d in self.days)

    @property
    def north_net_total(self) -> float:
        return sum(d.north_net for d in self.days)

    @property
    def foreign_net_total(self) -> float:
        return sum(d.foreign_net for d in self.days)

    @property
    def limit_up_net_total(self) -> float:
        return sum(d.limit_up_net for d in self.days)

    @property
    def latest_day(self) -> Optional[StockDayData]:
        return self.days[-1] if self.days else None

    @property
    def latest_turnover(self) -> float:
        d = self.latest_day
        return d.turnover_rate if d else 0.0

    @property
    def latest_net_sell(self) -> float:
        """最新日净卖出金额（正数=卖出）"""
        d = self.latest_day
        return -d.total_net_buy if d and d.total_net_buy < 0 else 0.0

    def time_weighted_inst_net(self) -> float:
        """改进D: 时间衰减加权机构净买入"""
        n = len(self.days)
        if n == 0:
            return 0.0
        weights = []
        for i in range(n):
            if i == n - 1:  # 最新日
                weights.append(1.0)
            elif i == n - 2:  # 前一日
                weights.append(0.7)
            else:
                weights.append(0.5)
        return sum(d.inst_net * w for d, w in zip(self.days, weights))

    def time_weighted_north_net(self) -> float:
        """改进D: 时间衰减加权北向净买入"""
        n = len(self.days)
        if n == 0:
            return 0.0
        weights = []
        for i in range(n):
            if i == n - 1:
                weights.append(1.0)
            elif i == n - 2:
                weights.append(0.7)
            else:
                weights.append(0.5)
        return sum(d.north_net * w for d, w in zip(self.days, weights))


# --- 数据获取 ---
def classify_seat(name: str) -> str:
    """根据席位名称分类"""
    if "机构专用" in name:
        return "institution"
    if "深股通" in name or "沪股通" in name:
        return "north_bound"
    for kw in FOREIGN_BROKER_KEYWORDS:
        if kw in name:
            return "foreign_broker"
    return "other"


def is_limit_up_reason(reason: str) -> bool:
    """判断上榜原因是否与涨停/涨幅相关"""
    keywords = ["涨幅", "涨停", "涨幅偏离值", "连续三个交易日内"]
    return any(kw in reason for kw in keywords)


def _merge_stock_day(existing: StockDayData, new: StockDayData) -> StockDayData:
    """合并同一股票同一日的多条记录（不同上榜原因导致多行）"""
    # 合并席位数据（去重）
    all_seats = {s.name: s for s in existing.seats}
    for s in new.seats:
        if s.name not in all_seats:
            all_seats[s.name] = s
        else:
            # 同名席位累加金额
            old = all_seats[s.name]
            all_seats[s.name] = SeatData(
                name=s.name,
                buy_amount=old.buy_amount + s.buy_amount,
                sell_amount=old.sell_amount + s.sell_amount,
                net_amount=old.net_amount + s.net_amount,
                seat_type=old.seat_type,
            )

    merged_seats = list(all_seats.values())
    inst_net = sum(s.net_amount for s in merged_seats if s.seat_type == "institution")
    north_net = sum(s.net_amount for s in merged_seats if s.seat_type == "north_bound")
    foreign_net = sum(s.net_amount for s in merged_seats if s.seat_type == "foreign_broker")

    # 涨停净买入：合并原因
    combined_reason = f"{existing.reason}; {new.reason}"
    is_limit = is_limit_up_reason(existing.reason) or is_limit_up_reason(new.reason)
    limit_up_net = (existing.limit_up_net + new.limit_up_net) if is_limit else 0.0

    return StockDayData(
        code=existing.code,
        name=existing.name,
        date=existing.date,
        close_price=new.close_price,  # 用最新的
        change_pct=new.change_pct,
        total_net_buy=existing.total_net_buy + new.total_net_buy,
        total_buy=existing.total_buy + new.total_buy,
        total_sell=existing.total_sell + new.total_sell,
        turnover_rate=max(existing.turnover_rate, new.turnover_rate),
        market_cap=new.market_cap,
        reason=combined_reason,
        seats=merged_seats,
        inst_net=inst_net,
        north_net=north_net,
        foreign_net=foreign_net,
        limit_up_net=limit_up_net,
    )


def fetch_daily_detail(date_str: str) -> dict[str, StockDayData]:
    """获取某日的龙虎榜详情（含席位级数据），返回 {code: StockDayData} 已去重"""
    cache_file = DATA_DIR / f"{date_str}.json"
    if cache_file.exists():
        with open(cache_file) as f:
            data = json.load(f)
        result = {}
        for d in data:
            sd = _dict_to_stock_day(d)
            if sd.code in result:
                result[sd.code] = _merge_stock_day(result[sd.code], sd)
            else:
                result[sd.code] = sd
        return result

    print(f"  获取 {date_str} 龙虎榜概览...")
    try:
        overview = ak.stock_lhb_detail_em(start_date=date_str, end_date=date_str)
    except Exception as e:
        print(f"  ⚠ 获取概览失败: {e}")
        return {}

    if overview is None or overview.empty:
        print(f"  {date_str} 无龙虎榜数据（非交易日或数据未发布）")
        return {}

    results: dict[str, StockDayData] = {}
    total = len(overview)
    for i, row in overview.iterrows():
        code = str(row["代码"]).zfill(6)
        name = row["名称"]

        # 跳过ST和退市股
        if "ST" in name or "退市" in name:
            continue

        if (i + 1) % 20 == 0:
            print(f"    进度: {i+1}/{total}")

        # 获取席位级详情
        seats = []
        try:
            buy_detail = ak.stock_lhb_stock_detail_em(symbol=code, date=date_str, flag="买入")
            time.sleep(0.08)
            sell_detail = ak.stock_lhb_stock_detail_em(symbol=code, date=date_str, flag="卖出")
            time.sleep(0.08)

            # 合并买卖席位（去重）
            seen_names = set()
            for detail_df in [buy_detail, sell_detail]:
                if detail_df is None or detail_df.empty:
                    continue
                for _, srow in detail_df.iterrows():
                    sname = str(srow.get("交易营业部名称", ""))
                    if not sname or sname == "nan":
                        continue
                    if sname in seen_names:
                        continue
                    seen_names.add(sname)
                    buy_amt = float(srow.get("买入金额", 0) or 0) / 1e8
                    sell_amt = float(srow.get("卖出金额", 0) or 0) / 1e8
                    net_amt = float(srow.get("净额", 0) or 0) / 1e8
                    seats.append(SeatData(
                        name=sname, buy_amount=buy_amt,
                        sell_amount=sell_amt, net_amount=net_amt,
                        seat_type=classify_seat(sname),
                    ))
        except Exception:
            pass

        # 聚合席位数据
        inst_net = sum(s.net_amount for s in seats if s.seat_type == "institution")
        north_net = sum(s.net_amount for s in seats if s.seat_type == "north_bound")
        foreign_net = sum(s.net_amount for s in seats if s.seat_type == "foreign_broker")

        # 涨停净买入
        reason = str(row.get("上榜原因", ""))
        limit_up_net = sum(s.net_amount for s in seats) if is_limit_up_reason(reason) else 0.0

        sd = StockDayData(
            code=code,
            name=name,
            date=date_str,
            close_price=float(row.get("收盘价", 0) or 0),
            change_pct=float(row.get("涨跌幅", 0) or 0),
            total_net_buy=float(row.get("龙虎榜净买额", 0) or 0) / 1e8,
            total_buy=float(row.get("龙虎榜买入额", 0) or 0) / 1e8,
            total_sell=float(row.get("龙虎榜卖出额", 0) or 0) / 1e8,
            turnover_rate=float(row.get("换手率", 0) or 0),
            market_cap=float(row.get("流通市值", 0) or 0) / 1e8,
            reason=reason,
            seats=seats,
            inst_net=inst_net,
            north_net=north_net,
            foreign_net=foreign_net,
            limit_up_net=limit_up_net,
        )

        if code in results:
            results[code] = _merge_stock_day(results[code], sd)
        else:
            results[code] = sd

    # 缓存
    cache_data = [_stock_day_to_dict(sd) for sd in results.values()]
    with open(cache_file, "w") as f:
        json.dump(cache_data, f, ensure_ascii=False, indent=2)

    print(f"  {date_str}: {len(results)} 只股票")
    return results


def _stock_day_to_dict(sd: StockDayData) -> dict:
    return {
        "code": sd.code, "name": sd.name, "date": sd.date,
        "close_price": sd.close_price, "change_pct": sd.change_pct,
        "total_net_buy": sd.total_net_buy, "total_buy": sd.total_buy,
        "total_sell": sd.total_sell, "turnover_rate": sd.turnover_rate,
        "market_cap": sd.market_cap, "reason": sd.reason,
        "inst_net": sd.inst_net, "north_net": sd.north_net,
        "foreign_net": sd.foreign_net, "limit_up_net": sd.limit_up_net,
    }


def _dict_to_stock_day(d: dict) -> StockDayData:
    return StockDayData(
        code=d["code"], name=d["name"], date=d["date"],
        close_price=d["close_price"], change_pct=d["change_pct"],
        total_net_buy=d["total_net_buy"], total_buy=d["total_buy"],
        total_sell=d["total_sell"], turnover_rate=d["turnover_rate"],
        market_cap=d["market_cap"], reason=d["reason"],
        inst_net=d["inst_net"], north_net=d["north_net"],
        foreign_net=d["foreign_net"], limit_up_net=d["limit_up_net"],
    )


def fetch_window_data(end_date: str, window_days: int = WINDOW_DAYS) -> dict[str, StockAgg]:
    """获取窗口期内所有股票的聚合数据"""
    end_dt = datetime.strptime(end_date, "%Y%m%d")
    dates = [(end_dt - timedelta(days=i)).strftime("%Y%m%d") for i in range(window_days - 1, -1, -1)]

    print(f"数据窗口: {dates[0]} ~ {dates[-1]} ({len(dates)} 天)")

    all_data: dict[str, StockAgg] = {}
    for date_str in dates:
        daily = fetch_daily_detail(date_str)
        for code, sd in daily.items():
            if code not in all_data:
                all_data[code] = StockAgg(code=sd.code, name=sd.name)
            agg = all_data[code]
            agg.days.append(sd)
            if not agg.first_date:
                agg.first_date = sd.date
            agg.last_date = sd.date
        # 按日期排序
        for agg in all_data.values():
            agg.days.sort(key=lambda d: d.date)

    print(f"共 {len(all_data)} 只股票上榜")
    return all_data


# --- V3 评分 ---
def score_v3(agg: StockAgg) -> dict:
    """V3 评分逻辑"""
    inst = agg.inst_net_total
    north = agg.north_net_total
    days = agg.consecutive_days
    limit_up = agg.limit_up_net_total
    foreign = agg.foreign_net_total

    # 机构净买入力度 (30)
    if inst > 5:
        s_inst = 30
    elif inst > 2:
        s_inst = 20
    elif inst > 0:
        s_inst = 10
    else:
        s_inst = 0

    # 北向资金净买入 (25)
    if north > 10:
        s_north = 25
    elif north > 3:
        s_north = 18
    elif north > 1:
        s_north = 12
    elif north > 0:
        s_north = 6
    else:
        s_north = 0

    # 连续上榜天数 (20)
    if days >= 5:
        s_days = 20
    elif days >= 4:
        s_days = 15
    elif days >= 3:
        s_days = 10
    elif days >= 2:
        s_days = 6
    else:
        s_days = 2

    # 涨停持续性 (15)
    if limit_up > 5:
        s_limit = 15
    elif limit_up > 2:
        s_limit = 10
    elif limit_up > 0:
        s_limit = 5
    else:
        s_limit = 0

    # 外资投行席位 (10)
    if foreign > 2:
        s_foreign = 10
    elif foreign > 0:
        s_foreign = 5
    else:
        s_foreign = 0

    total = s_inst + s_north + s_days + s_limit + s_foreign
    return {
        "total": total,
        "inst": s_inst, "north": s_north, "days": s_days,
        "limit": s_limit, "foreign": s_foreign,
        "inst_raw": inst, "north_raw": north, "days_raw": days,
        "limit_raw": limit_up, "foreign_raw": foreign,
    }


# --- V4 评分 ---
def check_reversal_filter(agg: StockAgg) -> tuple[str, bool]:
    """
    改进A: 当日反转检测过滤层
    返回 (档位, 是否排除)
    档位: "strong"/"mid"/"weak"/"excluded"
    """
    latest = agg.latest_day
    if latest is None:
        return "weak", False

    latest_net_sell = -latest.total_net_buy if latest.total_net_buy < 0 else 0
    turnover = latest.turnover_rate
    days = agg.consecutive_days

    # 最新日净卖出 > 3亿 → 直接排除
    if latest_net_sell > 3:
        return "excluded", True

    # 换手 > 30% + 连续 ≥ 3天 + 最新日净卖出 → 直接排除（晋控电力模式）
    if turnover > 30 and days >= 3 and latest.total_net_buy < 0:
        return "excluded", True

    # 换手 > 25% + 最新日净卖出 > 1亿 → 降一档
    if turnover > 25 and latest_net_sell > 1:
        return "downgrade", False

    return "normal", False


def score_consistency(agg: StockAgg) -> int:
    """
    改进B: 内外资一致性维度（满分10分）
    使用时间衰减加权的值
    """
    inst = agg.time_weighted_inst_net()
    north = agg.time_weighted_north_net()

    if inst > 3 and north > 0:
        return 10  # 同向看多
    elif inst > 0 and north > 0:
        return 5
    elif inst > 3 and north < 0:
        return -15  # 新集能源模式
    elif inst > 0 and north < 0:
        return -8
    elif inst < 0 and north > 3:
        return -10  # 北向拉机构跑
    else:
        return 0


def score_consecutive_days_v4(agg: StockAgg) -> int:
    """
    改进C: 连续上榜分场景赋分（满分20分）
    """
    days = agg.consecutive_days
    latest = agg.latest_day
    if latest is None:
        return 2 if days >= 1 else 0

    latest_net = latest.total_net_buy
    turnover = latest.turnover_rate

    if days >= 3:
        if latest_net > 0 and turnover < 20:
            return 15  # 真建仓
        elif latest_net > 0 and turnover >= 20:
            return 5
        elif latest_net < 0:
            return -5  # 出货型连榜
        else:
            return 5
    elif days == 2:
        if latest_net > 0:
            return 6
        elif latest_net < 0:
            return 0
        else:
            return 6
    elif days == 1:
        return 2
    return 0


def score_v4(agg: StockAgg) -> dict:
    """V4 评分逻辑（含改进A-D）"""
    # 改进A: 反转检测
    filter_result, excluded = check_reversal_filter(agg)
    if excluded:
        return {
            "total": -999, "inst": 0, "north": 0, "days": 0,
            "limit": 0, "foreign": 0, "consistency": 0,
            "inst_raw": agg.inst_net_total, "north_raw": agg.north_net_total,
            "days_raw": agg.consecutive_days, "limit_raw": agg.limit_up_net_total,
            "foreign_raw": agg.foreign_net_total,
            "consistency_raw": score_consistency(agg),
            "excluded": True, "exclude_reason": filter_result,
            "downgrade": False,
        }

    # 改进D: 时间衰减加权
    inst = agg.time_weighted_inst_net()
    north = agg.time_weighted_north_net()
    foreign = agg.foreign_net_total  # 外资暂不加权（金额小）
    limit_up = agg.limit_up_net_total
    days = agg.consecutive_days

    # 机构净买入力度 (30) — 使用加权值
    if inst > 5:
        s_inst = 30
    elif inst > 2:
        s_inst = 20
    elif inst > 0:
        s_inst = 10
    else:
        s_inst = 0

    # 北向资金净买入 (25) — 使用加权值
    if north > 10:
        s_north = 25
    elif north > 3:
        s_north = 18
    elif north > 1:
        s_north = 12
    elif north > 0:
        s_north = 6
    else:
        s_north = 0

    # 改进C: 连续上榜分场景赋分 (20)
    s_days = score_consecutive_days_v4(agg)

    # 涨停持续性 (10) — V4 降为10分
    if limit_up > 5:
        s_limit = 10
    elif limit_up > 2:
        s_limit = 7
    elif limit_up > 0:
        s_limit = 3
    else:
        s_limit = 0

    # 外资投行席位 (5) — V4 降为5分
    if foreign > 2:
        s_foreign = 5
    elif foreign > 0:
        s_foreign = 3
    else:
        s_foreign = 0

    # 改进B: 内外资一致性 (10)
    s_consistency = score_consistency(agg)

    # 改进A: 降档
    downgrade = (filter_result == "downgrade")
    downgrade_penalty = -10 if downgrade else 0

    total = s_inst + s_north + s_days + s_limit + s_foreign + s_consistency + downgrade_penalty
    total = max(0, total)  # 不低于0

    return {
        "total": total,
        "inst": s_inst, "north": s_north, "days": s_days,
        "limit": s_limit, "foreign": s_foreign, "consistency": s_consistency,
        "inst_raw": inst, "north_raw": north, "days_raw": days,
        "limit_raw": limit_up, "foreign_raw": foreign,
        "consistency_raw": s_consistency,
        "excluded": False, "exclude_reason": "",
        "downgrade": downgrade,
    }


def signal_label(score: int) -> str:
    if score >= 80:
        return "🔥极强"
    elif score >= 60:
        return "⭐强"
    elif score >= 40:
        return "📊中"
    elif score >= 20:
        return "💡弱"
    else:
        return "⏸️观望"


# --- 报告生成 ---
def generate_report(
    all_agg: dict[str, StockAgg],
    end_date: str,
    v3_scores: dict[str, dict],
    v4_scores: dict[str, dict],
):
    """生成 V3/V4 对比 Markdown 报告"""
    # 按 V4 总分排序
    ranked = sorted(
        [(code, v3_scores[code], v4_scores[code], all_agg[code])
         for code in all_agg if code in v3_scores and code in v4_scores],
        key=lambda x: (x[2]["total"] if x[2]["total"] != -999 else -1),
        reverse=True,
    )

    # 统计
    v3_strong = sum(1 for _, v3, _, _ in ranked if v3["total"] >= 40)
    v4_strong = sum(1 for _, _, v4, _ in ranked if v4["total"] >= 40 and v4["total"] != -999)
    v4_excluded = sum(1 for _, _, v4, _ in ranked if v4.get("excluded"))

    date_display = f"{end_date[:4]}-{end_date[4:6]}-{end_date[6:]}"
    next_date = (datetime.strptime(end_date, "%Y%m%d") + timedelta(days=1)).strftime("%Y-%m-%d")

    lines = []
    lines.append("---")
    lines.append(f"date: {date_display}")
    lines.append("tags: [龙虎榜, 预测, 量化, V4, V3对比]")
    lines.append("category: 投研日记")
    lines.append("---")
    lines.append("")
    lines.append(f"# 龙虎榜 V4 vs V3 对比 ({date_display} → T+1={next_date})")
    lines.append("")
    lines.append(f"> 数据窗口: {date_display} 前 6 天")
    lines.append(f"> 上榜股票: {len(all_agg)}只 | V3中+信号: {v3_strong}只 | V4中+信号: {v4_strong}只 | V4排除: {v4_excluded}只")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## V4 改进说明")
    lines.append("")
    lines.append("| 改进 | 说明 |")
    lines.append("|:---|:---|")
    lines.append("| A: 反转检测 | 最新日净卖出>3亿排除; 换手>30%+连榜≥3天+净卖出排除; 换手>25%+净卖出>1亿降档 |")
    lines.append("| B: 一致性 | 机构+北向同向加分，反向减分（新集能源模式-15） |")
    lines.append("| C: 连续上榜 | 分场景: 真建仓+15, 高换手+5, 出货型-5 |")
    lines.append("| D: 时间衰减 | 最新日×1.0, 前一日×0.7, 3-6天前×0.5 |")
    lines.append("")
    lines.append(f"**V4 总分 = 机构(30) + 北向(25) + 连续上榜(20) + 涨停(10) + 外资(5) + 一致性(10) = 100**")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## V3 vs V4 推荐对比（V4中信号及以上）")
    lines.append("")
    lines.append("| # | 代码 | 名称 | V3分 | V4分 | 变化 | V4信号 | 要点 |")
    lines.append("|:---|:---|:---|:---|:---|:---|:---|:---|")

    count = 0
    for code, v3, v4, agg in ranked:
        v4_total = v4["total"]
        if v4_total == -999:
            signal = "🚫排除"
        elif v4_total >= 60:
            signal = "⭐强"
        elif v4_total >= 40:
            signal = "📊中"
        else:
            continue

        count += 1
        v3_total = v3["total"]
        if v4_total == -999:
            change = f"排除(原{v3_total})"
        else:
            diff = v4_total - v3_total
            change = f"{diff:+d}" if diff != 0 else "0"

        # 要点
        parts = []
        if v4.get("excluded"):
            parts.append(f"排除:{v4.get('exclude_reason','')}")
        elif v4.get("downgrade"):
            parts.append("⚠降档")
        if v4.get("consistency", 0) < 0:
            parts.append(f"内外资打架({v4['consistency']:+d})")
        if v4.get("days", 0) < 0:
            parts.append("出货型连榜")
        parts.append(f"机构{agg.inst_net_total:.1f}亿")
        parts.append(f"北向{agg.north_net_total:.1f}亿")

        lines.append(f"| {count} | {code} | {agg.name} | {v3_total} | {v4_total if v4_total != -999 else '排除'} | {change} | {signal} | {'; '.join(parts[:3])} |")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 重点标的 V3→V4 变化详解")
    lines.append("")

    # 重点标的: 晋控电力(000767) 和 新集能源(601918)
    focus_codes = ["000767", "601918"]
    for code in focus_codes:
        if code not in all_agg:
            continue
        agg = all_agg[code]
        v3 = v3_scores.get(code, {})
        v4 = v4_scores.get(code, {})

        lines.append(f"### {code} {agg.name}")
        lines.append("")
        lines.append("| 维度 | V3得分 | V4得分 | 说明 |")
        lines.append("|:---|:---|:---|:---|")

        dims = [
            ("机构(30)", "inst", "inst_raw"),
            ("北向(25)", "north", "north_raw"),
            ("连续上榜(20)/(V4:20)", "days", "days_raw"),
            ("涨停(15)/(V4:10)", "limit", "limit_raw"),
            ("外资(10)/(V4:5)", "foreign", "foreign_raw"),
            ("一致性(V4新增,10)", "consistency", "consistency_raw"),
        ]
        for label, key, raw_key in dims:
            v3_val = v3.get(key, 0)
            v4_val = v4.get(key, 0)
            raw_val = v3.get(raw_key, 0)
            raw_str = f"{raw_val:.1f}" if isinstance(raw_val, float) else str(raw_val)
            if key == "consistency":
                note = "V4新增" if v4_val != 0 else "V4新增(0)"
            else:
                note = f"原始值: {raw_str}"
            lines.append(f"| {label} | {v3_val} | {v4_val} | {note} |")

        lines.append(f"| **总分** | **{v3.get('total', 0)}** | **{v4.get('total', -999)}** | {'排除' if v4.get('excluded') else '降档' if v4.get('downgrade') else '-'} |")
        lines.append("")

        # 每日明细
        lines.append("**每日数据明细:**")
        lines.append("")
        lines.append("| 日期 | 总净买(亿) | 换手率 | 机构净买(亿) | 北向净买(亿) |")
        lines.append("|:---|:---|:---|:---|:---|")
        for d in agg.days:
            lines.append(f"| {d.date} | {d.total_net_buy:+.2f} | {d.turnover_rate:.1f}% | {d.inst_net:+.2f} | {d.north_net:+.2f} |")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## 完整排名（V4 前50）")
    lines.append("")
    lines.append("| # | 代码 | 名称 | V3 | V4 | Δ | 机构(亿) | 北向(亿) | 上榜天 | 涨停(亿) | 外资(亿) | 一致性 |")
    lines.append("|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|")

    count = 0
    for code, v3, v4, agg in ranked:
        if count >= 50:
            break
        count += 1
        v4_total = v4["total"]
        v4_str = "排除" if v4_total == -999 else str(v4_total)
        diff = (v4_total if v4_total != -999 else 0) - v3["total"]
        diff_str = f"{diff:+d}" if v4_total != -999 else "—"

        lines.append(
            f"| {count} | {code} | {agg.name} | {v3['total']} | {v4_str} | {diff_str} | "
            f"{agg.inst_net_total:.1f} | {agg.north_net_total:.1f} | {agg.consecutive_days} | "
            f"{agg.limit_up_net_total:.1f} | {agg.foreign_net_total:.1f} | "
            f"{v4.get('consistency', 0):+d} |"
        )

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 风险提示")
    lines.append("")
    lines.append("- V4 模型为实验性改进，尚未经过实盘验证")
    lines.append("- 反转检测过滤层依赖最新日数据，T+1延迟可能导致漏判")
    lines.append("- 内外资一致性维度在极端行情下可能过度惩罚")
    lines.append("- 本报告仅作参考，不构成投资建议")
    lines.append("")

    output_file = OUTPUT_DIR / f"龙虎榜预测-{date_display}.md"
    with open(output_file, "w") as f:
        f.write("\n".join(lines))
    print(f"\n✅ 报告已保存: {output_file}")
    return output_file


# --- 控制台对比输出 ---
def print_console_comparison(ranked, all_agg):
    """打印 V3/V4 对比到控制台"""
    print("\n" + "=" * 100)
    print("V3 vs V4 核心推荐对比")
    print("=" * 100)
    print(f"{'代码':<10} {'名称':<10} {'V3分':>5} {'V4分':>6} {'变化':>5} {'V4信号':<8} {'关键变化':<50}")
    print("-" * 100)

    for code, v3, v4, agg in ranked[:20]:
        v4_total = v4["total"]
        v4_str = f"{v4_total}" if v4_total != -999 else "排除"
        diff = (v4_total if v4_total != -999 else 0) - v3["total"]
        diff_str = f"{diff:+d}" if v4_total != -999 else "—"

        if v4_total == -999:
            signal = "🚫排除"
        elif v4_total >= 60:
            signal = "⭐强"
        elif v4_total >= 40:
            signal = "📊中"
        elif v4_total >= 20:
            signal = "💡弱"
        else:
            signal = "⏸️观望"

        changes = []
        if v4.get("excluded"):
            changes.append(f"排除原因:{v4.get('exclude_reason','')}")
        elif v4.get("downgrade"):
            changes.append("降档")
        c_score = v4.get("consistency", 0)
        if c_score < 0:
            changes.append(f"一致性{c_score:+d}")
        d_score = v4.get("days", 0)
        if d_score < 0:
            changes.append(f"出货型连榜")
        change_str = "; ".join(changes) if changes else "-"

        print(f"{code:<10} {agg.name:<10} {v3['total']:>5} {v4_str:>6} {diff_str:>5} {signal:<8} {change_str:<50}")

    print("-" * 100)
    print()


# --- 主流程 ---
def main():
    setup_proxy()

    # 数据窗口: 截至最新交易日的 6 天
    end_date = "20260602"
    print(f"龙虎榜 V4 评分模型")
    print(f"数据窗口: 6天 (截至 {end_date})")
    print()

    # 1. 获取数据
    print("=" * 60)
    print("Step 1: 获取数据")
    print("=" * 60)
    all_agg = fetch_window_data(end_date)
    print(f"共 {len(all_agg)} 只股票\n")

    # 2. 计算 V3 和 V4 评分
    print("=" * 60)
    print("Step 2: 计算 V3 和 V4 评分")
    print("=" * 60)
    v3_scores = {}
    v4_scores = {}
    for code, agg in all_agg.items():
        v3_scores[code] = score_v3(agg)
        v4_scores[code] = score_v4(agg)

    # 统计
    v3_excluded = 0
    v4_excluded = sum(1 for v in v4_scores.values() if v.get("excluded"))
    v3_downgraded = 0
    v4_downgraded = sum(1 for v in v4_scores.values() if v.get("downgrade"))
    v4_neg_consistency = sum(1 for v in v4_scores.values() if v.get("consistency", 0) < 0)
    v4_neg_days = sum(1 for v in v4_scores.values() if v.get("days", 0) < 0)

    print(f"V3 中信号及以上(≥40): {sum(1 for v in v3_scores.values() if v['total'] >= 40)}")
    print(f"V4 中信号及以上(≥40): {sum(1 for v in v4_scores.values() if v['total'] >= 40 and v['total'] != -999)}")
    print(f"V4 排除: {v4_excluded}")
    print(f"V4 降档: {v4_downgraded}")
    print(f"V4 负一致性: {v4_neg_consistency}")
    print(f"V4 出货型连榜: {v4_neg_days}")
    print()

    # 3. 排序
    ranked = sorted(
        [(code, v3_scores[code], v4_scores[code], all_agg[code])
         for code in all_agg],
        key=lambda x: (x[2]["total"] if x[2]["total"] != -999 else -1),
        reverse=True,
    )

    # 4. 控制台对比
    print_console_comparison(ranked, all_agg)

    # 5. 打印重点标的详情
    for code in ["000767", "601918"]:
        if code not in all_agg:
            continue
        agg = all_agg[code]
        v3 = v3_scores[code]
        v4 = v4_scores[code]
        print(f"\n{'='*60}")
        print(f"重点标的: {code} {agg.name}")
        print(f"{'='*60}")
        print(f"V3: {v3['total']}分 | V4: {v4['total']}分")
        if v4.get("excluded"):
            print(f"  ⚠ V4 排除: {v4.get('exclude_reason')}")
        elif v4.get("downgrade"):
            print(f"  ⚠ V4 降档")
        print(f"  每日数据:")
        for d in agg.days:
            print(f"    {d.date}: 总净买{d.total_net_buy:+.2f}亿, 换手{d.turnover_rate:.1f}%, "
                  f"机构{d.inst_net:+.2f}亿, 北向{d.north_net:+.2f}亿")
        print(f"  V3维度: 机构{v3['inst']}/30 北向{v3['north']}/25 连续{v3['days']}/20 涨停{v3['limit']}/15 外资{v3['foreign']}/10")
        print(f"  V4维度: 机构{v4['inst']}/30 北向{v4['north']}/25 连续{v4['days']}/20 涨停{v4['limit']}/10 外资{v4['foreign']}/5 一致性{v4['consistency']}/10")

    # 6. 生成报告
    print("\n" + "=" * 60)
    print("Step 3: 生成报告")
    print("=" * 60)
    report_path = generate_report(all_agg, end_date, v3_scores, v4_scores)

    print("\n✅ V4 模型完成")
    print(f"报告: {report_path}")


if __name__ == "__main__":
    main()