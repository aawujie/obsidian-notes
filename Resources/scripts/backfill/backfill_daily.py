#!/usr/bin/env python3
# 数据源: yfinance (Yahoo Finance, 免费, 无 API Key)
# 运行:   cd obsidian-notes && source .venv/bin/activate && python Resources/scripts/backfill/backfill_daily.py [天数]
"""
历史数据回填脚本
回填过去 N 个交易日的 DailyData 日报。

通过动态导入现有 monitor 模块复用其 ALL_TICKERS + generate_report + CHINESE_NAMES，
只重新实现 fetch_date() 来按历史日期拉数据。

输出: 5.Finance/DailyData/*/ → 每个交易日各一份 YYYY-MM-DD.md + .json
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd
import yfinance as yf

SCRIPT_DIR = Path(__file__).resolve().parent
VAULT_ROOT = SCRIPT_DIR.parent.parent.parent
DATA_DIR = VAULT_ROOT / "5.Finance" / "DailyData"

# 监控器路径 → 数据子目录
MONITORS = [
    ("us-stock",  VAULT_ROOT / "Resources/scripts/us-stock-monitor/us_stock_monitor.py",  "us-stock"),
    ("gold",      VAULT_ROOT / "Resources/scripts/gold-monitor/gold_monitor.py",          "gold"),
    ("a-stock",   VAULT_ROOT / "Resources/scripts/a-stock-monitor/a_stock_monitor.py",    "a-stock"),
    ("hk-stock",  VAULT_ROOT / "Resources/scripts/hk-stock-monitor/hk_stock_monitor.py",  "hk-stock"),
    ("metals",    VAULT_ROOT / "Resources/scripts/metals-monitor/metals_monitor.py",      "metals"),
]


def trading_days(n):
    """过去 n 个美股交易日（跳过周末）"""
    days = []
    d = datetime.now().date()
    while len(days) < n:
        if d.weekday() < 5:
            days.append(d)
        d -= timedelta(days=1)
    return sorted(days)


def fetch_date(tickers, date):
    """拉取以 date 为截止日的行情数据"""
    end_str = (date + timedelta(days=1)).strftime("%Y-%m-%d")
    start_str = (date - timedelta(days=65)).strftime("%Y-%m-%d")

    rows = []
    for i in range(0, len(tickers), 80):
        batch = tickers[i:i + 80]
        try:
            stocks = yf.Tickers(" ".join(batch))
            for t in batch:
                try:
                    info = stocks.tickers[t].info
                    hist = stocks.tickers[t].history(start=start_str, end=end_str)

                    # 过滤：只保留 <= date 的数据
                    if hasattr(hist.index, "tz") and hist.index.tz is not None:
                        hist.index = hist.index.tz_localize(None)
                    hist = hist[hist.index.date <= date]

                    if len(hist) < 2:
                        continue

                    closes = hist["Close"]
                    # NaN 兜底
                    if pd.isna(closes.iloc[-1]):
                        if len(closes) >= 2 and not pd.isna(closes.iloc[-2]):
                            closes = closes.iloc[:-1]
                            hist = hist.iloc[:-1]
                        else:
                            continue

                    tc = closes.iloc[-1]
                    pc = closes.iloc[-2]
                    change_daily = (tc - pc) / pc * 100

                    change_weekly = None
                    if len(closes) >= 6:
                        change_weekly = (tc - closes.iloc[-6]) / closes.iloc[-6] * 100

                    change_monthly = None
                    if len(closes) >= 15:
                        change_monthly = (tc - closes.iloc[-15]) / closes.iloc[-15] * 100

                    avg_vol = hist["Volume"].tail(5).mean()
                    vol = hist.iloc[-1]["Volume"]
                    vol_ratio = vol / avg_vol if avg_vol > 0 else 1.0
                    high52 = info.get("fiftyTwoWeekHigh")
                    is_new_high = bool(high52 and tc >= high52 * 0.995)

                    rows.append({
                        "ticker": t,
                        "name": info.get("shortName") or info.get("longName", t),
                        "sector": info.get("sector", ""),
                        "industry": info.get("industry", ""),
                        "market_cap": info.get("marketCap"),
                        "close": tc,
                        "prev_close": pc,
                        "change_daily": round(change_daily, 2),
                        "change_weekly": round(change_weekly, 2) if change_weekly is not None else None,
                        "change_monthly": round(change_monthly, 2) if change_monthly is not None else None,
                        "volume": vol,
                        "avg_vol_5d": round(avg_vol, 0),
                        "vol_ratio": round(vol_ratio, 2),
                        "high52": high52,
                        "low52": info.get("fiftyTwoWeekLow"),
                        "dist_from_high": round((tc - high52) / high52 * 100, 2) if high52 and high52 > 0 else None,
                        "is_new_high": is_new_high,
                    })
                except Exception:
                    continue
        except Exception as e:
            print(f"    batch error: {e}")

    return pd.DataFrame(rows)


def save_report(df, date_str, out_dir, generate_fn):
    """调用 monitor 的 generate_report + 保存 JSON"""
    out_dir.mkdir(parents=True, exist_ok=True)

    # Markdown 报告
    md = generate_fn(df, date_str)
    (out_dir / f"{date_str}.md").write_text(md, encoding="utf-8")

    # JSON 数据
    records = []
    for _, row in df.iterrows():
        r = row.to_dict()
        for k, v in r.items():
            if isinstance(v, (pd.Timestamp,)):
                r[k] = str(v)
            elif isinstance(v, float) and np.isnan(v):
                r[k] = None
        records.append(r)
    (out_dir / f"{date_str}.json").write_text(
        json.dumps({"date": date_str, "data": records}, ensure_ascii=False, indent=2),
        encoding="utf-8")


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    td = trading_days(n)
    print(f"回填 {len(td)} 个交易日 ({td[0]} → {td[-1]})\n")

    for name, script_path, subdir in MONITORS:
        out_dir = DATA_DIR / subdir
        tickers = None
        generate_report = None
        all_tickers_fn = None

        # 尝试用 importlib 动态导入
        import importlib.util
        spec = importlib.util.spec_from_file_location(f"monitor_{name}", script_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        # 获取 ticker 列表
        if hasattr(mod, "ALL_TICKERS"):
            tickers = mod.ALL_TICKERS
        elif hasattr(mod, "all_tickers"):
            tickers = mod.all_tickers
        elif hasattr(mod, "get_sp500_tickers"):
            try:
                sp = mod.get_sp500_tickers()
                nq = mod.get_nasdaq100_tickers()
                tickers = sorted(set(sp + nq))
            except Exception:
                tickers = list(mod._fallback_sp500()) + list(mod._fallback_nasdaq100())

        if not tickers:
            tickers = []
        generate_report = mod.generate_report

        print(f"[{name}] {len(tickers)} tickers, gen={generate_report.__name__ if generate_report else 'N/A'}")
        new = skip = 0

        for day in td:
            ds = day.strftime("%Y-%m-%d")
            if (out_dir / f"{ds}.md").exists():
                skip += 1
                continue

            df = fetch_date(tickers, day)
            if df.empty:
                skip += 1
                continue

            save_report(df, ds, out_dir, generate_report)
            new += 1

        print(f"  新增 {new}, 跳过 {skip}\n")

    print("=" * 50)
    for name, _, subdir in MONITORS:
        cnt = len(list((DATA_DIR / subdir).glob("*.md")))
        print(f"  {name}: {cnt} 份")


if __name__ == "__main__":
    main()