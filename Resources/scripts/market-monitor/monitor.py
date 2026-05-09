#!/usr/bin/env python3
"""
美股市场监控脚本
用途：盘后扫描 S&P 500 + 纳斯达克100，输出涨幅排名、异常放量、52周新高
运行：python Resources/scripts/market-monitor/monitor.py
数据源：yfinance (Yahoo Finance, 免费, 无 API Key)

输出到 5.Finance/DailyData/：
  - YYYY-MM-DD.md     Markdown 日报（可在 Obsidian 中查看）
  - YYYY-MM-DD.json    结构化数据（供后续分析）
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf

# --- 路径配置：相对于 obsidian-notes 根目录 ---
SCRIPT_DIR = Path(__file__).resolve().parent
VAULT_ROOT = SCRIPT_DIR.parent.parent.parent  # Resources/scripts/market-monitor → 根
DATA_DIR = VAULT_ROOT / "5.Finance" / "DailyData"
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


def fetch_stock_data(tickers, period="5d"):
    """
    批量拉取股票数据
    返回 DataFrame: 每行一只股票，含价格、涨跌幅、成交量等
    """
    # 分批拉，避免单次请求过大
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

                    # 当天数据（最新一个交易日）
                    today = hist.iloc[-1]
                    prev = hist.iloc[-2]
                    # 5日均量
                    avg_vol_5d = hist["Volume"].tail(5).mean() if len(hist) >= 5 else hist["Volume"].mean()

                    close = today["Close"]
                    prev_close = prev["Close"]
                    change_pct = ((close - prev_close) / prev_close) * 100
                    volume = today["Volume"]
                    vol_ratio = volume / avg_vol_5d if avg_vol_5d > 0 else 1.0

                    # 52 周高低
                    high52 = info.get("fiftyTwoWeekHigh", None)
                    low52 = info.get("fiftyTwoWeekLow", None)

                    # 距 52 周高点的距离
                    dist_from_high = ((close - high52) / high52 * 100) if high52 and high52 > 0 else None

                    # 判断是否接近 52 周新高 (< 1% = 创了)
                    is_new_high = dist_from_high is not None and dist_from_high >= -0.5

                    all_data.append({
                        "ticker": t,
                        "name": info.get("shortName") or info.get("longName", t),
                        "sector": info.get("sector", ""),
                        "industry": info.get("industry", ""),
                        "market_cap": info.get("marketCap"),
                        "close": close,
                        "prev_close": prev_close,
                        "change_pct": round(change_pct, 2),
                        "volume": volume,
                        "avg_vol_5d": round(avg_vol_5d, 0),
                        "vol_ratio": round(vol_ratio, 2),
                        "high52": high52,
                        "low52": low52,
                        "dist_from_high": round(dist_from_high, 2) if dist_from_high else None,
                        "is_new_high": is_new_high,
                    })
                except Exception:
                    continue  # 单只失败不中断整批
        except Exception as e:
            print(f"  [ERROR] 批次拉取失败: {e}")
            continue

    return pd.DataFrame(all_data)


def generate_report(df, date_str):
    """生成 Markdown 日报"""
    if df.empty:
        return f"# 美股市场日报 {date_str}\n\n> 当日无数据（可能为非交易日或数据拉取失败）\n"

    lines = [
        f"---",
        f"title: 美股市场日报 {date_str}",
        f"type: summary",
        f"created: {date_str}",
        f"tags: [美股, 市场监控, 日报]",
        f"---",
        f"",
        f"# 美股市场日报 {date_str}",
        f"",
        f"> 自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M')} · 覆盖 S&P 500 + Nasdaq 100 · 数据源 Yahoo Finance",
        f"",
    ]

    # --- 概览 ---
    total = len(df)
    up = len(df[df["change_pct"] > 0])
    down = len(df[df["change_pct"] < 0])
    flat = total - up - down
    avg_change = df["change_pct"].mean()
    new_highs = df["is_new_high"].sum()

    lines += [
        f"## 市场概览",
        f"",
        f"| 指标 | 数值 |",
        f"|------|------|",
        f"| 覆盖股票数 | {total} |",
        f"| 上涨 | {up} ({up/total*100:.0f}%) |",
        f"| 下跌 | {down} ({down/total*100:.0f}%) |",
        f"| 持平 | {flat} |",
        f"| 平均涨跌幅 | {avg_change:+.2f}% |",
        f"| 创 52 周新高 | {new_highs} 只 |",
        f"",
    ]

    # --- 涨幅 TOP 15 ---
    gainers = df.nlargest(15, "change_pct")
    lines += [
        f"## 涨幅 TOP 15",
        f"",
        f"| 排名 | 代码 | 名称 | 涨幅 | 收盘价 | 成交量/均值 | 52周新高 |",
        f"|:---:|------|------|:---:|:---:|:---:|:---:|",
    ]
    for rank, (_, row) in enumerate(gainers.iterrows(), 1):
        high_flag = "⭐" if row["is_new_high"] else ""
        lines.append(
            f"| {rank} | **{row['ticker']}** | {row['name']} | "
            f"**{row['change_pct']:+.2f}%** | "
            f"${row['close']:.2f} | "
            f"{row['vol_ratio']:.1f}x"
            f"{' 🔥' if row['vol_ratio'] > 2 else ''} | "
            f"{high_flag} |"
        )
    lines.append("")

    # --- 跌幅 TOP 10 ---
    losers = df.nsmallest(10, "change_pct")
    lines += [
        f"## 跌幅 TOP 10",
        f"",
        f"| 排名 | 代码 | 名称 | 跌幅 | 收盘价 | 成交量/均值 |",
        f"|:---:|------|------|:---:|:---:|:---:|",
    ]
    for rank, (_, row) in enumerate(losers.iterrows(), 1):
        lines.append(
            f"| {rank} | **{row['ticker']}** | {row['name']} | "
            f"**{row['change_pct']:+.2f}%** | "
            f"${row['close']:.2f} | "
            f"{row['vol_ratio']:.1f}x |"
        )
    lines.append("")

    # --- 异常放量 (>3x 平均) ---
    unusual_vol = df[df["vol_ratio"] > 3].nlargest(10, "vol_ratio")
    if not unusual_vol.empty:
        lines += [
            f"## 异常放量（成交量 > 3 倍均值）",
            f"",
            f"| 代码 | 名称 | 涨幅 | 成交量/均值 |",
            f"|------|------|:---:|:---:|",
        ]
        for _, row in unusual_vol.iterrows():
            lines.append(
                f"| **{row['ticker']}** | {row['name']} | "
                f"{row['change_pct']:+.2f}% | "
                f"**{row['vol_ratio']:.1f}x** |"
            )
        lines.append("")

    # --- 52 周新高 ---
    new_high_stocks = df[df["is_new_high"]].nlargest(15, "change_pct")
    if not new_high_stocks.empty:
        lines += [
            f"## 创 52 周新高 ({len(df[df['is_new_high']])} 只)",
            f"",
            f"| 代码 | 名称 | 涨幅 | 收盘价 |",
            f"|------|------|:---:|:---:|",
        ]
        for _, row in new_high_stocks.iterrows():
            lines.append(
                f"| **{row['ticker']}** | {row['name']} | "
                f"{row['change_pct']:+.2f}% | "
                f"${row['close']:.2f} |"
            )
        lines.append("")

    # --- 板块表现 ---
    if df["sector"].notna().any() and (df["sector"] != "").any():
        sector_stats = df.groupby("sector").agg(
            平均涨幅=("change_pct", "mean"),
            股票数=("ticker", "count"),
            新高数=("is_new_high", "sum"),
        ).round(2).sort_values("平均涨幅", ascending=False)

        lines += [
            f"## 板块表现",
            f"",
            f"| 板块 | 平均涨幅 | 股票数 | 新高数 |",
            f"|------|:---:|:---:|:---:|",
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
    top3 = df.nlargest(3, "change_pct")
    print("当日涨幅前三：")
    for _, row in top3.iterrows():
        print(f"  {row['ticker']:6s} {row['change_pct']:+.2f}%  {row['name']}")
    new_high_count = df["is_new_high"].sum()
    unusual_count = len(df[df["vol_ratio"] > 3])
    print(f"创 52 周新高: {new_high_count} 只  |  异常放量: {unusual_count} 只")
    print("=" * 60)


if __name__ == "__main__":
    main()