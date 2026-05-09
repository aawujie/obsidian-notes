#!/usr/bin/env python3
# 数据源: yfinance (Yahoo Finance, 免费, 无 API Key)
# 运行:   cd obsidian-notes && source .venv/bin/activate && python Resources/scripts/us-stock-monitor/us_stock_monitor.py
"""
美股市场监控脚本
盘后扫描 S&P 500 + 纳斯达克100，输出涨幅排名、异常放量、52周新高

输出: 5.Finance/DailyData/us-stock/ → YYYY-MM-DD.md + .json
"""

import json
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf

# --- 路径配置：相对于 obsidian-notes 根目录 ---
SCRIPT_DIR = Path(__file__).resolve().parent
VAULT_ROOT = SCRIPT_DIR.parent.parent.parent  # Resources/scripts/us-stock-monitor → 根
DATA_DIR = VAULT_ROOT / "5.Finance" / "DailyData" / "us-stock"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def get_sp500_tickers():
    """从 Wikipedia 获取 S&P 500 成分股"""
    try:
        table = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")[0]
        return table["Symbol"].str.replace(".", "-", regex=False).tolist()
    except Exception:
        print("[WARN] 无法获取 S&P 500 成分股列表，使用内置缓存")
        return _fallback_sp500()


def get_nasdaq100_tickers():
    """从 Wikipedia 获取纳斯达克100成分股"""
    try:
        table = pd.read_html("https://en.wikipedia.org/wiki/Nasdaq-100")[4]
        return table["Ticker"].str.replace(".", "-", regex=False).tolist()
    except Exception:
        print("[WARN] 无法获取 Nasdaq 100 成分股列表，使用内置缓存")
        return _fallback_nasdaq100()


def _fallback_sp500():
    """S&P 500 前 100 大权重股 (按市值)"""
    return [
        "AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA", "BRK-B",
        "AVGO", "LLY", "JPM", "V", "UNH", "XOM", "MA", "COST", "WMT", "HD",
        "PG", "NFLX", "JNJ", "ABBV", "BAC", "CRM", "ORCL", "AMD", "MRK",
        "CVX", "KO", "WFC", "PEP", "CSCO", "ACN", "IBM", "TMO", "MCD", "LIN",
        "ABT", "GE", "DIS", "CAT", "PM", "ISRG", "TXN", "QCOM", "VZ", "INTU",
        "NOW", "AXP", "DHR", "AMGN", "GS", "BKNG", "UBER", "SPGI", "PFE",
        "MS", "RTX", "BLK", "UNP", "HON", "LOW", "NEE", "SYK", "TJX", "PGR",
        "CMCSA", "BSX", "ETN", "COP", "LMT", "ANET", "ELV", "ADI", "C",
        "MDT", "FI", "MU", "DE", "PLD", "CB", "ADP", "KLAC", "AMT", "UPS",
        "INTC", "MMC", "LRCX", "BA", "BX", "SO", "SCHW", "GILD", "CI",
    ]


def _fallback_nasdaq100():
    """Nasdaq 100 成分股"""
    return [
        "AAPL", "MSFT", "NVDA", "AMZN", "AVGO", "META", "TSLA", "GOOGL",
        "GOOG", "COST", "NFLX", "AMD", "ADBE", "PEP", "CSCO", "TMUS",
        "QCOM", "TXN", "INTU", "AMGN", "ISRG", "CMCSA", "AMAT", "HON",
        "BKNG", "GILD", "ADI", "SBUX", "VRTX", "LRCX", "ADP", "REGN",
        "MELI", "MDLZ", "PYPL", "INTC", "KLAC", "CTAS", "SNPS", "CDNS",
        "MAR", "CRWD", "ORLY", "ASML", "CEG", "MRVL", "FTNT", "CSX",
        "ADSK", "DASH", "ABNB", "ROP", "PCAR", "WDAY", "MNST", "AEP",
        "NXPI", "KDP", "PAYX", "TTD", "ODFL", "FAST", "CHTR", "KHC",
        "MCHP", "EXC", "ROST", "IDXX", "AZN", "LULU", "CCEP", "BKR",
        "EA", "CTSH", "XEL", "TEAM", "GEHC", "VRSK", "ZS", "DXCM",
        "FANG", "PDD", "ANSS", "BIIB", "TTWO", "CDW", "MDB", "DLTR",
        "WBD", "GFS", "ON", "ARM", "SIRI", "ILMN",
    ]


# --- 中英文名称对照 ---
CHINESE_NAMES = {
    "A": "安捷伦科技", "AAPL": "苹果", "ABBV": "艾伯维", "ABNB": "爱彼迎",
    "ABT": "雅培", "ACN": "埃森哲", "ADBE": "奥多比", "ADI": "亚德诺半导体",
    "ADP": "自动数据处理", "ADSK": "欧特克", "AEP": "美国电力",
    "AMAT": "应用材料", "AMD": "AMD超威半导体", "AMGN": "安进", "AMT": "美国铁塔",
    "AMZN": "亚马逊", "ANET": "Arista网络", "APA": "阿帕奇石油",
    "ARM": "Arm安谋", "ASML": "阿斯麦", "AVGO": "博通", "AXP": "美国运通",
    "AZN": "阿斯利康", "BA": "波音", "BAC": "美国银行", "BIIB": "渤健",
    "BKNG": "缤客Booking", "BKR": "贝克休斯", "BLK": "贝莱德", "BSX": "波士顿科学",
    "BX": "黑石", "C": "花旗银行", "CAT": "卡特彼勒", "CB": "安达保险",
    "CCEP": "可口可乐欧洲", "CDNS": "Cadence", "CDW": "CDW", "CEG": "Constellation能源",
    "CHTR": "特许通讯", "CI": "信诺", "CMCSA": "康卡斯特", "COP": "康菲石油",
    "COST": "好市多", "CRM": "赛富时Salesforce", "CRWD": "CrowdStrike",
    "CSCO": "思科", "CSX": "CSX铁路", "CTAS": "Cintas", "CTSH": "高知特",
    "CVX": "雪佛龙", "DASH": "DoorDash", "DE": "迪尔", "DELL": "戴尔科技",
    "DHR": "丹纳赫", "DIS": "迪士尼", "DLTR": "美元树", "DXCM": "德康医疗",
    "EA": "艺电", "ELV": "Elevance健康", "ETN": "伊顿", "EXC": "艾克斯龙",
    "FANG": "钻石背能源", "FAST": "快扣", "FTNT": "飞塔Fortinet",
    "GD": "通用动力", "GE": "通用电气", "GEHC": "GE医疗", "GFS": "格芯",
    "GILD": "吉利德科学", "GLW": "康宁", "GOOG": "谷歌-C", "GOOGL": "谷歌-A",
    "GS": "高盛", "HD": "家得宝", "HON": "霍尼韦尔", "IBM": "IBM",
    "IDXX": "IDEXX", "ILMN": "Illumina", "INTC": "英特尔",
    "INTU": "财捷Intuit", "ISRG": "直觉外科", "JNJ": "强生",
    "JPM": "摩根大通", "KDP": "Keurig Dr Pepper", "KHC": "卡夫亨氏",
    "KLAC": "科磊KLA", "KO": "可口可乐", "LIN": "林德气体", "LLY": "礼来",
    "LMT": "洛克希德马丁", "LOW": "劳氏", "LRCX": "泛林半导体Lam Research",
    "LULU": "露露乐檬", "MA": "万事达", "MAR": "万豪", "MCD": "麦当劳",
    "MCHP": "微芯科技", "MDLZ": "亿滋", "MDT": "美敦力", "MELI": "美客多",
    "META": "Meta脸书", "MMC": "威达信", "MNST": "怪物饮料Monster",
    "MRK": "默沙东", "MRVL": "迈威尔Marvell", "MS": "摩根士丹利",
    "MSFT": "微软", "MU": "美光科技", "NEE": "新纪元能源NextEra",
    "NFLX": "奈飞Netflix", "NOW": "ServiceNow", "NVDA": "英伟达Nvidia",
    "NXPI": "恩智浦半导体", "ODFL": "Old Dominion", "ON": "安森美半导体",
    "ORCL": "甲骨文", "ORLY": "奥莱利O'Reilly",
    "PAYX": "沛齐Paychex", "PCAR": "帕卡PACCAR", "PDD": "拼多多",
    "PEP": "百事可乐", "PFE": "辉瑞", "PG": "宝洁", "PGR": "前进保险",
    "PLD": "普洛斯", "PM": "菲利普莫里斯",
    "PWR": "广达服务Quanta", "PYPL": "贝宝PayPal", "QCOM": "高通",
    "REGN": "再生元制药", "ROP": "罗珀技术", "ROST": "罗斯百货",
    "RTX": "雷神技术", "SBUX": "星巴克", "SCHW": "嘉信理财",
    "SIRI": "天狼星XM", "SMCI": "超微电脑SMCI", "SNPS": "新思科技Synopsys",
    "SO": "南方电力", "SPGI": "标普全球", "STX": "希捷科技",
    "SYK": "史赛克", "TEAM": "Atlassian", "TJX": "TJX",
    "TMO": "赛默飞", "TMUS": "T-Mobile", "TSLA": "特斯拉",
    "TTD": "The Trade Desk", "TTWO": "Take-Two", "TXN": "德州仪器",
    "UBER": "优步Uber", "UNH": "联合健康", "UNP": "联合太平洋",
    "UPS": "UPS快递", "V": "维萨Visa", "VRSK": "Verisk",
    "VRTX": "福泰制药", "VZ": "威瑞森", "WBD": "华纳兄弟探索",
    "WDAY": "Workday", "WDC": "西部数据", "WFC": "富国银行",
    "WMT": "沃尔玛", "XEL": "Xcel能源", "XOM": "埃克森美孚",
    "ZS": "Zscaler",
}


def get_cn(ticker):
    """返回中文名称，无映射时返回空"""
    return CHINESE_NAMES.get(ticker, "")


def full_name(row):
    """拼装显示名称：英文名 + 中文名"""
    en = row.get("name", row.get("ticker", ""))
    cn = get_cn(row["ticker"])
    if cn:
        return f"{en} / {cn}"
    return en


def fetch_stock_data(tickers, period="1mo"):
    """
    批量拉取股票数据（默认 1 个月历史，用于计算日/周/月涨跌幅）
    返回 DataFrame: 每行一只股票，含价格、涨跌幅、成交量等
    """
    batch_size = 200
    all_data = []

    for i in range(0, len(tickers), batch_size):
        batch = tickers[i:i + batch_size]
        print(f"  拉取 {i+1}-{min(i+batch_size, len(tickers))}/{len(tickers)} ...")

        try:
            stocks = yf.Tickers(" ".join(batch))
            for t in batch:
                try:
                    info = stocks.tickers[t].info
                    hist = stocks.tickers[t].history(period=period)

                    if hist.empty or len(hist) < 2:
                        continue

                    closes = hist["Close"]
                    today_close = closes.iloc[-1]
                    prev_close = closes.iloc[-2]

                    # 日涨跌幅
                    change_daily = ((today_close - prev_close) / prev_close) * 100

                    # 周涨跌幅（约 5 个交易日）
                    if len(closes) >= 6:
                        week_ago = closes.iloc[-6]
                        change_weekly = ((today_close - week_ago) / week_ago) * 100
                    else:
                        change_weekly = None

                    # 月涨跌幅（约 21 个交易日）
                    if len(closes) >= 22:
                        month_ago = closes.iloc[-22]
                        change_monthly = ((today_close - month_ago) / month_ago) * 100
                    else:
                        change_monthly = None

                    # 5日均量
                    avg_vol_5d = hist["Volume"].tail(5).mean() if len(hist) >= 5 else hist["Volume"].mean()
                    volume = today = hist.iloc[-1]["Volume"]
                    vol_ratio = volume / avg_vol_5d if avg_vol_5d > 0 else 1.0

                    # 52 周高低
                    high52 = info.get("fiftyTwoWeekHigh")
                    low52 = info.get("fiftyTwoWeekLow")
                    dist_from_high = ((today_close - high52) / high52 * 100) if high52 and high52 > 0 else None
                    is_new_high = dist_from_high is not None and dist_from_high >= -0.5

                    all_data.append({
                        "ticker": t,
                        "name": info.get("shortName") or info.get("longName", t),
                        "sector": info.get("sector", ""),
                        "industry": info.get("industry", ""),
                        "market_cap": info.get("marketCap"),
                        "close": today_close,
                        "prev_close": prev_close,
                        "change_daily": round(change_daily, 2),
                        "change_weekly": round(change_weekly, 2) if change_weekly is not None else None,
                        "change_monthly": round(change_monthly, 2) if change_monthly is not None else None,
                        "volume": volume,
                        "avg_vol_5d": round(avg_vol_5d, 0),
                        "vol_ratio": round(vol_ratio, 2),
                        "high52": high52,
                        "low52": low52,
                        "dist_from_high": round(dist_from_high, 2) if dist_from_high else None,
                        "is_new_high": is_new_high,
                    })
                except Exception:
                    continue
        except Exception as e:
            print(f"  [ERROR] 批次拉取失败: {e}")
            continue

    return pd.DataFrame(all_data)


def generate_report(df, date_str):
    """生成 Markdown 日报"""
    if df.empty:
        return f"# 美股市场日报 {date_str}\n\n> 当日无数据（可能为非交易日或数据拉取失败）\n"

    lines = [
        "---",
        f"title: 美股市场日报 {date_str}",
        "type: summary",
        f"created: {date_str}",
        "tags: [美股, 市场监控, 日报]",
        "---",
        "",
        f"# 美股市场日报 {date_str}",
        "",
        f"> 自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M')} · 覆盖 S&P 500 + Nasdaq 100 · 数据源 Yahoo Finance",
        "",
    ]

    # --- 概览 ---
    total = len(df)
    up = len(df[df["change_daily"] > 0])
    down = len(df[df["change_daily"] < 0])
    flat = total - up - down
    avg_daily = df["change_daily"].mean()
    avg_weekly = df["change_weekly"].dropna().mean()
    avg_monthly = df["change_monthly"].dropna().mean()
    new_highs = df["is_new_high"].sum()

    lines += [
        "## 市场概览",
        "",
        "| 指标 | 数值 |",
        "|------|------|",
        f"| 覆盖股票数 | {total} |",
        f"| 上涨 | {up} ({up/total*100:.0f}%) |",
        f"| 下跌 | {down} ({down/total*100:.0f}%) |",
        f"| 持平 | {flat} |",
        f"| 平均日涨幅 | {avg_daily:+.2f}% |",
        f"| 平均周涨幅 | {avg_weekly:+.2f}% |",
        f"| 平均月涨幅 | {avg_monthly:+.2f}% |",
        f"| 创 52 周新高 | {new_highs} 只 |",
        "",
    ]

    # --- 涨幅 TOP 15 ---
    gainers = df.nlargest(15, "change_daily")
    lines += [
        "## 涨幅 TOP 15",
        "",
        "| 排名 | 代码 | 名称 | 日涨幅 | 周涨幅 | 月涨幅 | 收盘价 | 成交量/均值 | 52周新高 |",
        "|:---:|------|------|:---:|:---:|:---:|:---:|:---:|:---:|",
    ]
    for rank, (_, row) in enumerate(gainers.iterrows(), 1):
        high_flag = "⭐" if row["is_new_high"] else ""
        w = f"{row['change_weekly']:+.2f}%" if row["change_weekly"] is not None else "—"
        m = f"{row['change_monthly']:+.2f}%" if row["change_monthly"] is not None else "—"
        lines.append(
            f"| {rank} | **{row['ticker']}** | {full_name(row)} | "
            f"**{row['change_daily']:+.2f}%** | "
            f"{w} | {m} | "
            f"${row['close']:.2f} | "
            f"{row['vol_ratio']:.1f}x"
            f"{' 🔥' if row['vol_ratio'] > 2 else ''} | "
            f"{high_flag} |"
        )
    lines.append("")

    # --- 跌幅 TOP 10 ---
    losers = df.nsmallest(10, "change_daily")
    lines += [
        "## 跌幅 TOP 10",
        "",
        "| 排名 | 代码 | 名称 | 跌幅 | 收盘价 | 成交量/均值 |",
        "|:---:|------|------|:---:|:---:|:---:|",
    ]
    for rank, (_, row) in enumerate(losers.iterrows(), 1):
        lines.append(
            f"| {rank} | **{row['ticker']}** | {full_name(row)} | "
            f"**{row['change_daily']:+.2f}%** | "
            f"${row['close']:.2f} | "
            f"{row['vol_ratio']:.1f}x |"
        )
    lines.append("")

    # --- 异常放量 (>3x 平均) ---
    unusual_vol = df[df["vol_ratio"] > 3].nlargest(10, "vol_ratio")
    if not unusual_vol.empty:
        lines += [
            "## 异常放量（成交量 > 3 倍均值）",
            "",
            "| 代码 | 名称 | 涨幅 | 成交量/均值 |",
            "|------|------|:---:|:---:|",
        ]
        for _, row in unusual_vol.iterrows():
            lines.append(
                f"| **{row['ticker']}** | {full_name(row)} | "
                f"{row['change_daily']:+.2f}% | "
                f"**{row['vol_ratio']:.1f}x** |"
            )
        lines.append("")

    # --- 52 周新高 ---
    new_high_stocks = df[df["is_new_high"]].nlargest(15, "change_daily")
    if not new_high_stocks.empty:
        lines += [
            f"## 创 52 周新高 ({len(df[df['is_new_high']])} 只)",
            "",
            "| 代码 | 名称 | 涨幅 | 收盘价 |",
            "|------|------|:---:|:---:|",
        ]
        for _, row in new_high_stocks.iterrows():
            lines.append(
                f"| **{row['ticker']}** | {full_name(row)} | "
                f"{row['change_daily']:+.2f}% | "
                f"${row['close']:.2f} |"
            )
        lines.append("")

    # --- 板块表现 ---
    if df["sector"].notna().any() and (df["sector"] != "").any():
        sector_stats = df.groupby("sector").agg(
            平均涨幅=("change_daily", "mean"),
            股票数=("ticker", "count"),
            新高数=("is_new_high", "sum"),
        ).round(2).sort_values("平均涨幅", ascending=False)

        lines += [
            "## 板块表现",
            "",
            "| 板块 | 平均涨幅 | 股票数 | 新高数 |",
            "|------|:---:|:---:|:---:|",
        ]
        for sector, row in sector_stats.iterrows():
            if sector == "":
                continue
            lines.append(
                f"| {sector} | {row['平均涨幅']:+.2f}% | "
                f"{int(row['股票数'])} | {int(row['新高数'])} |"
            )
        lines.append("")

    return "\n".join(lines)


def save_data(df, date_str):
    """保存结构化 JSON 数据"""
    # 转换 Timestamp 和 numpy 类型，确保 JSON 可序列化
    records = []
    for _, row in df.iterrows():
        r = row.to_dict()
        for k, v in r.items():
            if isinstance(v, (pd.Timestamp,)):
                r[k] = str(v)
            elif isinstance(v, (np.integer,)):
                r[k] = int(v)
            elif isinstance(v, (np.floating,)):
                r[k] = float(v) if not np.isnan(v) else None
            elif isinstance(v, float) and np.isnan(v):
                r[k] = None
        records.append(r)

    json_path = DATA_DIR / f"{date_str}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "date": date_str,
            "generated_at": datetime.now().isoformat(),
            "total_stocks": len(records),
            "data": records,
        }, f, ensure_ascii=False, indent=2)
    print(f"  JSON → {json_path}")


def main():
    today = datetime.now()
    date_str = today.strftime("%Y-%m-%d")

    print("=" * 60)
    print(f"美股市场监控 · {date_str}")
    print("=" * 60)

    # 1. 获取成分股列表
    print("\n[1/4] 获取成分股列表...")
    sp500 = get_sp500_tickers()
    nasdaq100 = get_nasdaq100_tickers()
    all_tickers = sorted(set(sp500 + nasdaq100))
    print(f"  S&P 500: {len(sp500)} 只, Nasdaq 100: {len(nasdaq100)} 只")
    print(f"  去重后合计: {len(all_tickers)} 只")

    # 2. 拉取数据
    print("\n[2/4] 拉取行情数据...")
    df = fetch_stock_data(all_tickers)
    if df.empty:
        print("[ERROR] 未拉取到任何数据，退出")
        sys.exit(1)
    print(f"  成功拉取 {len(df)} 只股票数据")

    # 3. 生成报告
    print("\n[3/4] 生成日报...")
    md_report = generate_report(df, date_str)
    md_path = DATA_DIR / f"{date_str}.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_report)
    print(f"  Markdown → {md_path}")

    # 4. 保存结构化数据
    print("\n[4/4] 保存数据...")
    save_data(df, date_str)

    # 摘要
    print("\n" + "=" * 60)
    top3 = df.nlargest(3, "change_daily")
    print("当日涨幅前三：")
    for _, row in top3.iterrows():
        print(f"  {row['ticker']:6s} {row['change_daily']:+.2f}%  {full_name(row)}")
    new_high_count = df["is_new_high"].sum()
    unusual_count = len(df[df["vol_ratio"] > 3])
    print(f"创 52 周新高: {new_high_count} 只  |  异常放量: {unusual_count} 只")
    print("=" * 60)


if __name__ == "__main__":
    main()