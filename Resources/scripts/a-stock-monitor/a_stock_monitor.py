#!/usr/bin/env python3
# 数据源: yfinance (Yahoo Finance, 免费, 无 API Key) — A股个股覆盖不全，升级用 akshare
# 运行:   cd obsidian-notes && source .venv/bin/activate && python Resources/scripts/a-stock-monitor/a_stock_monitor.py
"""
A股 / 中国市场监控脚本
盘后扫描上证、深证、创业板指数 + 美市中国ETF + 港市中概股

输出: 5.Finance/DailyData/a-stock/ → YYYY-MM-DD.md + .json
"""

import json
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf

SCRIPT_DIR = Path(__file__).resolve().parent
VAULT_ROOT = SCRIPT_DIR.parent.parent.parent
DATA_DIR = VAULT_ROOT / "5.Finance" / "DailyData" / "a-stock"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# --- 监控标的 ---
INDICES = [
    "000001.SS",   # 上证指数
    "399001.SZ",   # 深证成指
    "399006.SZ",   # 创业板指
    "000688.SS",   # 科创50
    "000300.SS",   # 沪深300
]

US_CHINA_ETF = [  # 美市中国ETF → 反映外资对中国的态度
    "FXI",    # 富时中国50
    "ASHR",   # 沪深300 ETF
    "KWEB",   # 中国互联网
    "MCHI",   # MSCI中国
    "CQQQ",   # 中国科技
    "YINN",   # 中国三倍做多
]

BIG_CAP = [  # 大蓝筹 (yfinance 可覆盖的)
    "0700.HK",   # 腾讯
    "9988.HK",   # 阿里巴巴
    "3690.HK",   # 美团
    "9618.HK",   # 京东
    "1810.HK",   # 小米
    "9999.HK",   # 网易
    "9888.HK",   # 百度
    "2015.HK",   # 理想汽车
    "9868.HK",   # 小鹏汽车
    "9961.HK",   # 携程
    "1024.HK",   # 快手
    "9626.HK",   # B站
]

ALL_TICKERS = INDICES + US_CHINA_ETF + BIG_CAP

CHINESE_NAMES = {
    "000001.SS": "上证指数", "399001.SZ": "深证成指", "399006.SZ": "创业板指",
    "000688.SS": "科创50", "000300.SS": "沪深300",
    "FXI": "富时中国50 ETF", "ASHR": "沪深300 ETF(Xtrackers)",
    "KWEB": "中国互联网ETF", "MCHI": "MSCI中国ETF", "CQQQ": "中国科技ETF",
    "YINN": "中国3倍做多", "0700.HK": "腾讯控股", "9988.HK": "阿里巴巴",
    "3690.HK": "美团", "9618.HK": "京东", "1810.HK": "小米集团",
    "9999.HK": "网易", "9888.HK": "百度", "2015.HK": "理想汽车",
    "9868.HK": "小鹏汽车", "9961.HK": "携程集团", "1024.HK": "快手",
    "9626.HK": "哔哩哔哩",
}


def get_cn(ticker):
    return CHINESE_NAMES.get(ticker, "")


def safe_pct(val):
    """将 None 或 NaN 转为 '—'，否则格式化为 +x.xx%"""
    if val is None:
        return "—"
    try:
        if np.isnan(float(val)):
            return "—"
    except (TypeError, ValueError):
        pass
    return f"{float(val):+.2f}%"


def safe_price(val):
    """将 None 或 NaN 转为 '—'，否则保留两位小数"""
    if val is None:
        return "—"
    try:
        if np.isnan(float(val)):
            return "—"
    except (TypeError, ValueError):
        pass
    return f"{float(val):.2f}"


def full_name(row):
    en = row.get("name", row.get("ticker", ""))
    cn = get_cn(row["ticker"])
    if cn:
        return f"{en} / {cn}"
    return en


def fetch_data(tickers):
    all_data = []
    for i in range(0, len(tickers), 50):
        batch = tickers[i:i + 50]
        try:
            stocks = yf.Tickers(" ".join(batch))
            for t in batch:
                try:
                    info = stocks.tickers[t].info
                    hist = stocks.tickers[t].history(period="1mo")
                    if hist.empty or len(hist) < 2:
                        continue

                    closes = hist["Close"]
                    today_close = closes.iloc[-1]
                    prev_close = closes.iloc[-2]

                    # 日涨跌幅
                    change_daily = ((today_close - prev_close) / prev_close) * 100

                    # 周涨跌幅（约 5 个交易日）
                    if len(closes) >= 6:
                        change_weekly = ((today_close - closes.iloc[-6]) / closes.iloc[-6]) * 100
                    else:
                        change_weekly = None

                    # 月涨跌幅（约 21 个交易日）
                    if len(closes) >= 22:
                        change_monthly = ((today_close - closes.iloc[-22]) / closes.iloc[-22]) * 100
                    else:
                        change_monthly = None

                    high52 = info.get("fiftyTwoWeekHigh")
                    all_data.append({
                        "ticker": t,
                        "name": info.get("shortName", info.get("longName", t)),
                        "close": today_close,
                        "change_daily": round(change_daily, 2),
                        "change_weekly": round(change_weekly, 2) if change_weekly is not None else None,
                        "change_monthly": round(change_monthly, 2) if change_monthly is not None else None,
                        "high52": high52,
                        "is_new_high": high52 and today_close >= high52 * 0.995,
                    })
                except Exception:
                    continue
        except Exception as e:
            print(f"  [WARN] 批次失败: {e}")
    return pd.DataFrame(all_data)


def generate_report(df, date_str):
    if df.empty:
        return f"# A股市场日报 {date_str}\n\n> 当日无数据\n"

    lines = [
        "---", f"title: A股市场日报 {date_str}", "type: summary",
        f"created: {date_str}", "tags: [A股, 中国市场, 中概股, 市场监控, 日报]", "---",
        "", f"# A股市场日报 {date_str}",
        "", f"> 自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M')} · 数据源 Yahoo Finance",
        "", "## 主要指数",
        "", "| 指数 | 名称 | 点位 | 日涨幅 | 周涨幅 | 月涨幅 |",
        "|------|------|:---:|:---:|:---:|:---:|",
    ]
    for _, row in df[df["ticker"].isin(INDICES)].iterrows():
        w = safe_pct(row["change_weekly"])
        m = safe_pct(row["change_monthly"])
        lines.append(
            f"| **{row['ticker']}** | {full_name(row)} | {safe_price(row['close'])} | "
            f"{safe_pct(row['change_daily'])} | {w} | {m} |"
        )

    lines += ["", "## 美市中国ETF（外资情绪）", "",
              "| 代码 | 名称 | 价格 | 日涨幅 | 周涨幅 | 月涨幅 | 52周新高 |",
              "|------|------|:---:|:---:|:---:|:---:|:---:|"]
    for _, row in df[df["ticker"].isin(US_CHINA_ETF)].iterrows():
        high = "⭐" if row["is_new_high"] else ""
        w = safe_pct(row["change_weekly"])
        m = safe_pct(row["change_monthly"])
        lines.append(
            f"| **{row['ticker']}** | {full_name(row)} | ${safe_price(row['close'])} | "
            f"{safe_pct(row['change_daily'])} | {w} | {m} | {high} |"
        )

    lines += ["", "## 大市值中概 / 港股", "",
              "| 代码 | 名称 | 价格 | 日涨幅 | 周涨幅 | 月涨幅 | 52周新高 |",
              "|------|------|:---:|:---:|:---:|:---:|:---:|"]
    for _, row in df[df["ticker"].isin(BIG_CAP)].iterrows():
        high = "⭐" if row["is_new_high"] else ""
        w = safe_pct(row["change_weekly"])
        m = safe_pct(row["change_monthly"])
        lines.append(
            f"| **{row['ticker']}** | {full_name(row)} | {safe_price(row['close'])} | "
            f"{safe_pct(row['change_daily'])} | {w} | {m} | {high} |"
        )

    return "\n".join(lines)


def main():
    date_str = datetime.now().strftime("%Y-%m-%d")
    print(f"A股/中国监控 · {date_str}")
    print(f"  拉取 {len(ALL_TICKERS)} 个标的...")
    df = fetch_data(ALL_TICKERS)
    if df.empty: print("[ERROR] 无数据"), sys.exit(1)
    print(f"  成功拉取 {len(df)} 个")

    md = generate_report(df, date_str)
    (DATA_DIR / f"{date_str}.md").write_text(md, encoding="utf-8")
    print(f"  → {DATA_DIR / f'{date_str}.md'}")

    records = []
    for _, row in df.iterrows():
        r = row.to_dict()
        for k, v in r.items():
            if isinstance(v, (pd.Timestamp,)): r[k] = str(v)
            elif isinstance(v, float) and np.isnan(v): r[k] = None
        records.append(r)
    (DATA_DIR / f"{date_str}.json").write_text(
        json.dumps({"date": date_str, "data": records}, ensure_ascii=False, indent=2), encoding="utf-8")

    top3 = df.nlargest(3, "change_daily")
    print("\n涨幅前三：")
    for _, row in top3.iterrows():
        print(f"  {row['ticker']:10s} {safe_pct(row['change_daily'])}  {full_name(row)}")


if __name__ == "__main__":
    main()