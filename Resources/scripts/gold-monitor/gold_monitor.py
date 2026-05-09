#!/usr/bin/env python3
# 数据源: yfinance (Yahoo Finance, 免费, 无 API Key)
# 运行:   cd obsidian-notes && source .venv/bin/activate && python Resources/scripts/gold-monitor/gold_monitor.py
"""
黄金市场监控脚本
盘后扫描金价ETF、金矿股、黄金期货、白银ETF

输出: 5.Finance/DailyData/gold/ → YYYY-MM-DD.md + .json
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
DATA_DIR = VAULT_ROOT / "5.Finance" / "DailyData" / "gold"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# --- 监控标的 ---
GOLD_ETF = ["GLD", "IAU", "SGOL"]           # 黄金ETF
GOLD_MINERS = ["NEM", "GOLD", "AU", "GFI", "KGC", "AEM", "FNV", "WPM", "RGLD", "AGI"]  # 金矿股
GOLD_JUNIORS = ["GDX", "GDXJ"]              # 金矿ETF
GOLD_FUTURES = ["GC=F"]                     # 黄金期货
SILVER = ["SLV"]                              # 白银ETF (AG=F 符号在 yfinance 已失效)

ALL_TICKERS = GOLD_ETF + GOLD_MINERS + GOLD_JUNIORS + GOLD_FUTURES + SILVER

CHINESE_NAMES = {
    "GLD": "SPDR黄金ETF", "IAU": "iShares黄金ETF", "SGOL": "abrdn黄金ETF",
    "NEM": "纽蒙特矿业", "GOLD": "巴里克黄金", "AU": "盎格鲁黄金",
    "GFI": "金田公司", "KGC": "金罗斯黄金", "AEM": "Agnico Eagle矿业",
    "FNV": "Franco-Nevada权利金", "WPM": "惠顿贵金属", "RGLD": "皇家黄金",
    "AGI": "阿拉莫斯黄金", "GDX": "金矿ETF-VanEck", "GDXJ": "小盘金矿ETF",
    "GC=F": "黄金期货", "SLV": "iShares白银ETF", "AG=F": "白银期货",
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
    """拉取行情数据"""
    all_data = []
    try:
        stocks = yf.Tickers(" ".join(tickers))
        for t in tickers:
            try:
                info = stocks.tickers[t].info
                hist = stocks.tickers[t].history(period="1mo")
                if hist.empty or len(hist) < 2:
                    continue

                # 兜底：如果最新 Close 是 NaN，用前一天数据
                closes_raw = hist["Close"]
                if pd.isna(closes_raw.iloc[-1]):
                    if len(closes_raw) >= 2 and not pd.isna(closes_raw.iloc[-2]):
                        hist = hist.iloc[:-1]
                    else:
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
                if len(closes) >= 15:
                    change_monthly = ((today_close - closes.iloc[-15]) / closes.iloc[-15]) * 100
                else:
                    change_monthly = None

                today = hist.iloc[-1]
                avg_vol = hist["Volume"].tail(5).mean() if len(hist) >= 5 else hist["Volume"].mean()
                close = today_close
                volume = today["Volume"]
                vol_ratio = volume / avg_vol if avg_vol > 0 else 1.0
                high52 = info.get("fiftyTwoWeekHigh")
                is_new_high = high52 and close >= high52 * 0.995
                all_data.append({
                    "ticker": t, "name": info.get("shortName", info.get("longName", t)),
                    "close": close,
                    "change_daily": round(change_daily, 2),
                    "change_weekly": round(change_weekly, 2) if change_weekly is not None else None,
                    "change_monthly": round(change_monthly, 2) if change_monthly is not None else None,
                    "volume": volume, "vol_ratio": round(vol_ratio, 2),
                    "high52": high52, "is_new_high": is_new_high,
                })
            except Exception:
                continue
    except Exception as e:
        print(f"  [ERROR] {e}")
    return pd.DataFrame(all_data)


def generate_report(df, date_str):
    if df.empty:
        return f"# 黄金市场日报 {date_str}\n\n> 当日无数据\n"

    lines = [
        "---", f"title: 黄金市场日报 {date_str}", "type: summary",
        f"created: {date_str}", "tags: [黄金, 贵金属, 市场监控, 日报]", "---",
        "", f"# 黄金市场日报 {date_str}",
        "", f"> 自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M')} · 数据源 Yahoo Finance",
        "",
        "## 金价与期货",
        "",
        "| 标的 | 名称 | 价格 | 日涨幅 | 周涨幅 | 月涨幅 | 52周新高 |",
        "|------|------|:---:|:---:|:---:|:---:|:---:|",
    ]
    for _, row in df[df["ticker"].isin(GOLD_ETF + GOLD_FUTURES + SILVER)].iterrows():
        high = "⭐" if row["is_new_high"] else ""
        w = safe_pct(row["change_weekly"])
        m = safe_pct(row["change_monthly"])
        lines.append(
            f"| **{row['ticker']}** | {full_name(row)} | ${safe_price(row['close'])} | "
            f"{safe_pct(row['change_daily'])} | {w} | {m} | {high} |"
        )

    gold_n = df[df["ticker"].isin(GOLD_MINERS)].nlargest(10, "change_daily")
    lines += [
        "", "## 金矿股 TOP 10", "",
        "| 代码 | 名称 | 日涨幅 | 周涨幅 | 月涨幅 | 收盘价 | 成交量/均值 |",
        "|------|------|:---:|:---:|:---:|:---:|:---:|",
    ]
    for _, row in gold_n.iterrows():
        w = safe_pct(row["change_weekly"])
        m = safe_pct(row["change_monthly"])
        lines.append(
            f"| **{row['ticker']}** | {full_name(row)} | "
            f"{safe_pct(row['change_daily'])} | {w} | {m} | ${safe_price(row['close'])} | {row['vol_ratio']:.1f}x |"
        )

    new_highs = df[df["is_new_high"]]
    if not new_highs.empty:
        lines += ["", "## 创 52 周新高", "", "| 代码 | 名称 | 日涨幅 | 周涨幅 | 月涨幅 |",
                  "|------|------|:---:|:---:|:---:|"]
        for _, row in new_highs.iterrows():
            w = safe_pct(row["change_weekly"])
            m = safe_pct(row["change_monthly"])
            lines.append(
                f"| **{row['ticker']}** | {full_name(row)} | "
                f"{safe_pct(row['change_daily'])} | {w} | {m} |"
            )

    return "\n".join(lines)


def main():
    date_str = datetime.now().strftime("%Y-%m-%d")
    print(f"黄金市场监控 · {date_str}")
    print(f"  拉取 {len(ALL_TICKERS)} 个标的...")
    df = fetch_data(ALL_TICKERS)
    if df.empty:
        print("[ERROR] 无数据"), sys.exit(1)
    print(f"  成功拉取 {len(df)} 个")

    md = generate_report(df, date_str)
    (DATA_DIR / f"{date_str}.md").write_text(md, encoding="utf-8")
    print(f"  → {DATA_DIR / f'{date_str}.md'}")

    # JSON
    records = []
    for _, row in df.iterrows():
        r = row.to_dict()
        for k, v in r.items():
            if isinstance(v, (pd.Timestamp,)): r[k] = str(v)
            elif isinstance(v, float) and np.isnan(v): r[k] = None
        records.append(r)
    json_path = DATA_DIR / f"{date_str}.json"
    json_path.write_text(json.dumps({"date": date_str, "data": records}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  → {json_path}")

    top3 = df.nlargest(3, "change_daily")
    print("\n涨幅前三：")
    for _, row in top3.iterrows():
        print(f"  {row['ticker']:6s} {safe_pct(row['change_daily'])}  {full_name(row)}")


if __name__ == "__main__":
    main()