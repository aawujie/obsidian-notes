#!/usr/bin/env python3
# 数据源: yfinance (Yahoo Finance, 免费, 无 API Key)
# 运行:   cd obsidian-notes && source .venv/bin/activate && python Resources/scripts/metals-monitor/metals_monitor.py
"""
金属市场监控脚本
盘后扫描工业金属(铜铝) + 贵金属(金银铂钯) + 锂稀土 + 矿业股/ETF

输出: 5.Finance/DailyData/metals/ → YYYY-MM-DD.md + .json
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
DATA_DIR = VAULT_ROOT / "5.Finance" / "DailyData" / "metals"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# --- 监控标的 ---
BASE_METALS = [  # 工业金属期货
    "HG=F",   # 铜
    "ALI=F",  # 铝
    "ZNC=F",  # 锌 (可能不可用，用镍代替)
    "ALI=F",  # 铝
]

PRECIOUS_METALS = [  # 贵金属
    "GC=F",   # 黄金
    "SI=F",   # 白银
    "PL=F",   # 铂金
    "PA=F",   # 钯金
]

# 矿业ETF + 大矿企
MINING_ETF = ["XME", "PICK", "COPX", "REMX", "LIT", "SIL"]  # 金属矿业/铜/稀土/锂/白银ETF
MAJOR_MINERS = [
    "BHP", "RIO", "VALE", "FCX", "SCCO", "TECK",  # 综合矿业/铜
    "AA", "CENX",                                    # 铝
    "MP", "SGML", "ALB", "SQM",                      # 稀土/锂
]

ALL_TICKERS = list(dict.fromkeys(
    BASE_METALS + PRECIOUS_METALS + MINING_ETF + MAJOR_MINERS
))

CHINESE_NAMES = {
    "HG=F": "铜期货", "ALI=F": "铝期货",
    "GC=F": "黄金期货", "SI=F": "白银期货",
    "PL=F": "铂金期货", "PA=F": "钯金期货",
    "XME": "金属矿业ETF-SPDR", "PICK": "全球矿业ETF-iShares",
    "COPX": "铜矿ETF", "REMX": "稀土ETF",
    "LIT": "锂矿ETF", "SIL": "白银矿业ETF",
    "BHP": "必和必拓BHP", "RIO": "力拓Rio Tinto",
    "VALE": "淡水河谷", "FCX": "自由港麦克莫兰(铜)",
    "SCCO": "南方铜业", "TECK": "泰克资源",
    "AA": "美国铝业", "CENX": "世纪铝业",
    "MP": "MP Materials(稀土)", "SGML": "西格玛锂业",
    "ALB": "雅保锂业", "SQM": "智利矿业化工(锂)",
}


def get_cn(ticker):
    return CHINESE_NAMES.get(ticker, "")


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

                    today = hist.iloc[-1]
                    close = today_close
                    high52 = info.get("fiftyTwoWeekHigh")
                    all_data.append({
                        "ticker": t,
                        "name": info.get("shortName", info.get("longName", t)),
                        "close": close, "change_daily": round(change_daily, 2), "change_weekly": round(change_weekly, 2) if change_weekly is not None else None, "change_monthly": round(change_monthly, 2) if change_monthly is not None else None,
                        "high52": high52,
                        "is_new_high": high52 and close >= high52 * 0.995,
                    })
                except Exception:
                    continue
        except Exception as e:
            print(f"  [WARN] 批次失败: {e}")
    return pd.DataFrame(all_data)


def generate_report(df, date_str):
    if df.empty:
        return f"# 金属市场日报 {date_str}\n\n> 当日无数据\n"

    lines = [
        "---", f"title: 金属市场日报 {date_str}", "type: summary",
        f"created: {date_str}", "tags: [金属, 大宗商品, 铜, 锂, 稀土, 市场监控, 日报]", "---",
        "", f"# 金属市场日报 {date_str}",
        "", f"> 自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M')} · 数据源 Yahoo Finance",
    ]

    # 贵金属
    lines += [
        "", "## 贵金属期货", "",
        "| 品种 | 名称 | 价格 | 日涨幅 | 周涨幅 | 月涨幅 |",
        "|------|------|:---:|:---:|:---:|:---:|",
    ]
    for _, row in df[df["ticker"].isin(PRECIOUS_METALS)].iterrows():
        w = f"{row['change_weekly']:+.2f}%" if row["change_weekly"] is not None else "—"
        m = f"{row['change_monthly']:+.2f}%" if row["change_monthly"] is not None else "—"
        lines.append(
            f"| **{row['ticker']}** | {full_name(row)} | ${row['close']:.2f} | "
            f"{row['change_daily']:+.2f}% | {w} | {m} |"
        )

    # 工业金属
    base = df[df["ticker"].isin(BASE_METALS)]
    if not base.empty:
        lines += [
            "", "## 工业金属期货", "",
            "| 品种 | 名称 | 价格 | 日涨幅 | 周涨幅 | 月涨幅 |",
            "|------|------|:---:|:---:|:---:|:---:|",
        ]
        for _, row in base.iterrows():
            w = f"{row['change_weekly']:+.2f}%" if row["change_weekly"] is not None else "—"
            m = f"{row['change_monthly']:+.2f}%" if row["change_monthly"] is not None else "—"
            lines.append(
                f"| **{row['ticker']}** | {full_name(row)} | ${row['close']:.2f} | "
                f"{row['change_daily']:+.2f}% | {w} | {m} |"
            )

    # ETF
    lines += [
        "", "## 矿业 ETF", "",
        "| 代码 | 名称 | 价格 | 日涨幅 | 周涨幅 | 月涨幅 | 52周新高 |",
        "|------|------|:---:|:---:|:---:|:---:|:---:|",
    ]
    for _, row in df[df["ticker"].isin(MINING_ETF)].iterrows():
        high = "⭐" if row["is_new_high"] else ""
        w = f"{row['change_weekly']:+.2f}%" if row["change_weekly"] is not None else "—"
        m = f"{row['change_monthly']:+.2f}%" if row["change_monthly"] is not None else "—"
        lines.append(
            f"| **{row['ticker']}** | {full_name(row)} | ${row['close']:.2f} | "
            f"{row['change_daily']:+.2f}% | {w} | {m} | {high} |"
        )

    # 大矿企
    miners = df[df["ticker"].isin(MAJOR_MINERS)].nlargest(14, "change_daily")
    lines += [
        "", "## 大型矿企", "",
        "| 代码 | 名称 | 涨幅 | 收盘价 | 52周新高 |",
        "|------|------|:---:|:---:|:---:|",
    ]
    for _, row in miners.iterrows():
        high = "⭐" if row["is_new_high"] else ""
        lines.append(f"| **{row['ticker']}** | {full_name(row)} | {row['change_daily']:+.2f}% | ${row['close']:.2f} | {high} |")

    return "\n".join(lines)


def main():
    date_str = datetime.now().strftime("%Y-%m-%d")
    print(f"金属市场监控 · {date_str}")
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
        print(f"  {row['ticker']:6s} {row['change_daily']:+.2f}%  {full_name(row)}")


if __name__ == "__main__":
    main()