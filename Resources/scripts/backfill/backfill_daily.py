#!/usr/bin/env python3
# 数据源: yfinance (Yahoo Finance, 免费, 无 API Key)
# 运行:   cd obsidian-notes && source .venv/bin/activate && python Resources/scripts/backfill/backfill_daily.py
"""
历史数据回填脚本
回填过去 N 个交易日的 DailyData 日报（需先跑过当日 monitor 确保函数可导入）

输出: 5.Finance/DailyData/*/ → 每个交易日各一份 YYYY-MM-DD.md + .json
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
import importlib.util

import numpy as np
import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
VAULT_ROOT = SCRIPT_DIR.parent.parent.parent
DATA_DIR = VAULT_ROOT / "5.Finance" / "DailyData"

MONITORS = {
    "us-stock": VAULT_ROOT / "Resources/scripts/us-stock-monitor/us_stock_monitor.py",
    "gold":     VAULT_ROOT / "Resources/scripts/gold-monitor/gold_monitor.py",
    "a-stock":  VAULT_ROOT / "Resources/scripts/a-stock-monitor/a_stock_monitor.py",
    "hk-stock": VAULT_ROOT / "Resources/scripts/hk-stock-monitor/hk_stock_monitor.py",
    "metals":   VAULT_ROOT / "Resources/scripts/metals-monitor/metals_monitor.py",
}


def import_monitor(script_path):
    """动态导入 monitor 模块"""
    spec = importlib.util.spec_from_file_location("monitor", script_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def get_trading_days(n):
    """
    获取过去 n 个美股交易日（简单版：剔除周末）
    精确版应使用美股交易日历，简单版对回填足够
    """
    days = []
    d = datetime.now().date()
    while len(days) < n:
        if d.weekday() < 5:  # Mon-Fri
            days.append(d)
        d -= timedelta(days=1)
    return sorted(days)


def backfill_for_date(mod, date, data_subdir, all_tickers, fetch_fn, generate_fn):
    """
    对单个日期拉取数据并生成报告
    date: datetime.date 对象
    """
    date_str = date.strftime("%Y-%m-%d")
    end_date = date + timedelta(days=1)
    end_str = end_date.strftime("%Y-%m-%d")

    out_dir = DATA_DIR / data_subdir
    out_dir.mkdir(parents=True, exist_ok=True)

    # 跳过已有报告
    if (out_dir / f"{date_str}.md").exists():
        return False

    try:
        # 用 yfinance 拉取以 date 为截止日的数据
        import yfinance as yf

        all_data = []
        tickers = all_tickers if isinstance(all_tickers, list) else all_tickers()

        for i in range(0, len(tickers), 50):
            batch = tickers[i:i + 50]
            try:
                stocks = yf.Tickers(" ".join(batch))
                for t in batch:
                    try:
                        info = stocks.tickers[t].info
                        # 拉取 end_date 之前 2 个月的数据
                        hist = stocks.tickers[t].history(start=(date - timedelta(days=60)).strftime("%Y-%m-%d"), end=end_str)
                        # 过滤：只保留 end_date 之前的数据
                        hist = hist[hist.index.date <= date if hasattr(hist.index, 'date') else hist.index]

                        if hist.empty or len(hist) < 2:
                            continue

                        closes = hist["Close"]
                        # NaN 兜底
                        if pd.isna(closes.iloc[-1]):
                            if len(closes) >= 2 and not pd.isna(closes.iloc[-2]):
                                hist = hist.iloc[:-1]
                                closes = hist["Close"]
                            else:
                                continue

                        today_close = closes.iloc[-1]
                        prev_close = closes.iloc[-2]
                        change_daily = ((today_close - prev_close) / prev_close) * 100

                        if len(closes) >= 6:
                            change_weekly = ((today_close - closes.iloc[-6]) / closes.iloc[-6]) * 100
                        else:
                            change_weekly = None

                        if len(closes) >= 15:
                            change_monthly = ((today_close - closes.iloc[-15]) / closes.iloc[-15]) * 100
                        else:
                            change_monthly = None

                        avg_vol = hist["Volume"].tail(5).mean() if len(hist) >= 5 else hist["Volume"].mean()
                        volume = hist.iloc[-1]["Volume"]
                        vol_ratio = volume / avg_vol if avg_vol > 0 else 1.0
                        high52 = info.get("fiftyTwoWeekHigh")
                        is_new_high = high52 and today_close >= high52 * 0.995

                        all_data.append({
                            "ticker": t,
                            "name": info.get("shortName", info.get("longName", t)),
                            "sector": info.get("sector", ""),
                            "industry": info.get("industry", ""),
                            "market_cap": info.get("marketCap"),
                            "close": today_close,
                            "prev_close": prev_close,
                            "change_daily": round(change_daily, 2),
                            "change_weekly": round(change_weekly, 2) if change_weekly is not None else None,
                            "change_monthly": round(change_monthly, 2) if change_monthly is not None else None,
                            "volume": volume,
                            "avg_vol_5d": round(avg_vol, 0),
                            "vol_ratio": round(vol_ratio, 2),
                            "high52": high52,
                            "is_new_high": is_new_high,
                        })
                    except Exception:
                        continue
            except Exception:
                continue

        df = pd.DataFrame(all_data)
        if df.empty:
            return False

        # 生成报告（用 monitor 自身的 generate_report 函数）
        md = generate_fn(df, date_str)
        (out_dir / f"{date_str}.md").write_text(md, encoding="utf-8")

        # JSON
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

        return True
    except Exception as e:
        print(f"    [ERROR] {date_str} {data_subdir}: {e}")
        return False


def backfill_monitor(name, script_path, n_days):
    """对单个 monitor 进行回填"""
    mod = import_monitor(script_path)
    trading_days = get_trading_days(n_days)

    new_count = 0
    skip_count = 0
    for day in trading_days:
        ok = backfill_for_date(
            mod, day, name, mod.ALL_TICKERS,
            mod.fetch_data, mod.generate_report
        )
        if ok:
            new_count += 1
        else:
            skip_count += 1
    return new_count, skip_count


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    print(f"回填过去 {n} 个交易日 DailyData\n")

    for name, script_path in MONITORS.items():
        print(f"[{name}]")
        new, skip = backfill_monitor(name, script_path, n)
        print(f"  新增 {new} 份, 跳过 {skip} 份 (已有)\n")

    # 验证
    print("=" * 50)
    print("验证报告数量:")
    for name in MONITORS:
        count = len(list((DATA_DIR / name).glob("*.md")))
        print(f"  {name}: {count} 份")
    print("=" * 50)


if __name__ == "__main__":
    main()