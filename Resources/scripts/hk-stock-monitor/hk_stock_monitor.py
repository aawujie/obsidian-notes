#!/usr/bin/env python3
# 数据源: yfinance (Yahoo Finance, 免费, 无 API Key)
# 运行:   cd obsidian-notes && source .venv/bin/activate && python Resources/scripts/hk-stock-monitor/hk_stock_monitor.py
"""
港股市场监控脚本
盘后扫描恒生指数 + 成分股 + 港股ETF + 热门港股

输出: 5.Finance/DailyData/hk-stock/ → YYYY-MM-DD.md + .json
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
DATA_DIR = VAULT_ROOT / "5.Finance" / "DailyData" / "hk-stock"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# --- 监控标的 ---
HK_INDICES = [
    "^HSI",       # 恒生指数
    "^HSCE",      # 国企指数
    "^HSCCI",     # 红筹指数
    "^HSTECH",    # 恒生科技
]

HK_ETF = [
    "2800.HK",    # 盈富基金(恒生ETF)
    "2828.HK",    # 恒生中国企业
    "3067.HK",    # 恒生科技ETF
    "3033.HK",    # 南方科创板50
]

# 恒生指数主要成分 + 热门港股
HK_BIG_CAP = [
    "0005.HK",    # 汇丰
    "0011.HK",    # 恒生银行
    "0388.HK",    # 港交所
    "0700.HK",    # 腾讯
    "0941.HK",    # 中国移动
    "1299.HK",    # 友邦保险
    "1398.HK",    # 工商银行
    "2318.HK",    # 平安
    "2388.HK",    # 中银香港
    "2628.HK",    # 中国人寿
    "3968.HK",    # 招商银行
    "3988.HK",    # 中国银行
    "2269.HK",    # 药明生物
    "0883.HK",    # 中海油
    "0857.HK",    # 中石油
    "1088.HK",    # 中国神华
    "1177.HK",    # 中国生物制药
    "1755.HK",    # 碧桂园服务
    "1810.HK",    # 小米
    "1833.HK",    # 平安好医生
    "1929.HK",    # 周大福
    "2007.HK",    # 碧桂园
    "2013.HK",    # 微盟
    "2018.HK",    # 瑞声科技
    "2057.HK",    # 中通快递
    "2382.HK",    # 舜宇光学
    "6618.HK",    # 京东健康
    "9626.HK",    # B站
    "9868.HK",    # 小鹏
    "9888.HK",    # 百度
    "9961.HK",    # 携程
    "9988.HK",    # 阿里
    "9999.HK",    # 网易
]

ALL_TICKERS = HK_INDICES + HK_ETF + list(dict.fromkeys(HK_BIG_CAP))  # 去重

CHINESE_NAMES = {
    "^HSI": "恒生指数", "^HSCE": "国企指数", "^HSCCI": "红筹指数", "^HSTECH": "恒生科技",
    "2800.HK": "盈富基金", "2828.HK": "恒生中国企业ETF", "3067.HK": "恒生科技ETF",
    "3033.HK": "南方科创板50", "0005.HK": "汇丰控股", "0011.HK": "恒生银行",
    "0388.HK": "香港交易所", "0700.HK": "腾讯控股", "0941.HK": "中国移动",
    "1299.HK": "友邦保险", "1398.HK": "工商银行", "2318.HK": "中国平安",
    "2388.HK": "中银香港", "2628.HK": "中国人寿", "3968.HK": "招商银行",
    "3988.HK": "中国银行", "2269.HK": "药明生物", "0883.HK": "中海油",
    "0857.HK": "中石油", "1088.HK": "中国神华", "1177.HK": "中国生物制药",
    "1810.HK": "小米集团", "1929.HK": "周大福", "2007.HK": "碧桂园",
    "2057.HK": "中通快递", "2382.HK": "舜宇光学", "6618.HK": "京东健康",
    "9626.HK": "哔哩哔哩", "9868.HK": "小鹏汽车", "9888.HK": "百度",
    "9961.HK": "携程集团", "9988.HK": "阿里巴巴", "9999.HK": "网易",
    "3690.HK": "美团", "9618.HK": "京东", "2015.HK": "理想汽车",
    "1024.HK": "快手", "1755.HK": "碧桂园服务", "1833.HK": "平安好医生",
    "2013.HK": "微盟集团", "2018.HK": "瑞声科技",
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

                    # 兜底：如果最新 Close 是 NaN（如尚未收盘），用前一天数据
                    closes_raw = hist["Close"]
                    if pd.isna(closes_raw.iloc[-1]):
                        if len(closes_raw) >= 2 and not pd.isna(closes_raw.iloc[-2]):
                            hist = hist.iloc[:-1]  # 去掉最后一行 NaN
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
                    close = today_close
                    avg_vol = hist["Volume"].tail(5).mean() if len(hist) >= 5 else hist["Volume"].mean()
                    volume = today["Volume"]
                    vol_ratio = volume / avg_vol if avg_vol > 0 else 1.0
                    high52 = info.get("fiftyTwoWeekHigh")
                    all_data.append({
                        "ticker": t,
                        "name": info.get("shortName", info.get("longName", t)),
                        "close": close, "change_daily": round(change_daily, 2), "change_weekly": round(change_weekly, 2) if change_weekly is not None else None, "change_monthly": round(change_monthly, 2) if change_monthly is not None else None,
                        "volume": volume,
                        "vol_ratio": round(volume / avg_vol, 2) if avg_vol > 0 else 1.0,
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
        return f"# 港股市场日报 {date_str}\n\n> 当日无数据\n"

    lines = [
        "---", f"title: 港股市场日报 {date_str}", "type: summary",
        f"created: {date_str}", "tags: [港股, 恒生, 市场监控, 日报]", "---",
        "", f"# 港股市场日报 {date_str}",
        "", f"> 自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M')} · 数据源 Yahoo Finance",
        "", "## 主要指数",
        "", "| 指数 | 名称 | 点位 | 日涨幅 | 周涨幅 | 月涨幅 |",
        "|------|------|:---:|:---:|:---:|:---:|",
    ]
    for _, row in df[df["ticker"].isin(HK_INDICES)].iterrows():
        w = safe_pct(row["change_weekly"])
        m = safe_pct(row["change_monthly"])
        lines.append(
            f"| **{row['ticker']}** | {full_name(row)} | {safe_price(row['close'])} | "
            f"{safe_pct(row['change_daily'])} | {w} | {m} |"
        )

    lines += ["", "## 港股 ETF", "",
              "| 代码 | 名称 | 价格 | 日涨幅 | 周涨幅 | 月涨幅 |",
              "|------|------|:---:|:---:|:---:|:---:|"]
    for _, row in df[df["ticker"].isin(HK_ETF)].iterrows():
        w = safe_pct(row["change_weekly"])
        m = safe_pct(row["change_monthly"])
        lines.append(
            f"| **{row['ticker']}** | {full_name(row)} | {safe_price(row['close'])} | "
            f"{safe_pct(row['change_daily'])} | {w} | {m} |"
        )

    top_n = df[df["ticker"].isin(HK_BIG_CAP)].nlargest(15, "change_daily")
    lines += ["", "## 成分股涨幅 TOP 15", "",
              "| 代码 | 名称 | 日涨幅 | 周涨幅 | 月涨幅 | 收盘价 | 成交量/均值 | 52周新高 |",
              "|------|------|:---:|:---:|:---:|:---:|:---:|:---:|"]
    for _, row in top_n.iterrows():
        high = "⭐" if row["is_new_high"] else ""
        w = safe_pct(row["change_weekly"])
        m = safe_pct(row["change_monthly"])
        lines.append(
            f"| **{row['ticker']}** | {full_name(row)} | "
            f"{safe_pct(row['change_daily'])} | {w} | {m} | "
            f"{row['close']:.2f} | "
            f"{row['vol_ratio']:.1f}x{' 🔥' if row['vol_ratio'] > 2 else ''} | {high} |"
        )

    return "\n".join(lines)


def main():
    date_str = datetime.now().strftime("%Y-%m-%d")
    print(f"港股监控 · {date_str}")
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