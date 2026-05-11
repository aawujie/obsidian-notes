#!/usr/bin/env python3
# 数据源: yfinance (Yahoo Finance, 免费, 无 API Key)
# 运行:   cd obsidian-notes && source .venv/bin/activate && python Resources/scripts/macro-monitor/macro_monitor.py
"""
宏观指标监控脚本.

覆盖每日投研决策最核心的跨资产指标：
- 美债收益率（10Y/30Y/5Y/2Y/3M）
- 美元指数 + 主要汇率（EUR/CNY/JPY/GBP）
- VIX 恐慌指数
- 原油/天然气
- 加密货币（BTC/ETH/SOL）

输出: 5.Finance/DailyData/macro/ → YYYY-MM-DD.md + .json
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
DATA_DIR = VAULT_ROOT / "5.Finance" / "DailyData" / "macro"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# --- 监控标的 ---
TREASURY_YIELDS = [
    "^IRX",    # 3 月期国债收益率
    "^FVX",    # 5 年期国债收益率
    "^TNX",    # 10 年期国债收益率
    "^TYX",    # 30 年期国债收益率
]

BOND_ETF = [
    "TLT",     # 20+年国债 ETF（长期利率方向标）
    "SHY",     # 1-3年短期国债 ETF
    "IEF",     # 7-10年中期国债 ETF
    "HYG",     # 高收益债 ETF（信用利差风向标）
    "LQD",     # 投资级企业债 ETF
]

DOLLAR_FX = [
    "DX-Y.NYB",  # 美元指数
    "EURUSD=X",  # 欧元/美元
    "CNY=X",     # 美元/人民币
    "JPY=X",     # 美元/日元
    "GBPUSD=X",  # 英镑/美元
]

VOLATILITY = [
    "^VIX",    # VIX 恐慌指数
]

ENERGY = [
    "CL=F",    # WTI 原油期货
    "BZ=F",    # 布伦特原油期货
    "NG=F",    # 天然气期货
]

ENERGY_ETF = [
    "USO",     # 原油 ETF
    "XLE",     # 能源板块 ETF
    "UNG",     # 天然气 ETF
]

CRYPTO = [
    "BTC-USD",  # 比特币
    "ETH-USD",  # 以太坊
    "SOL-USD",  # Solana
]

ALL_TICKERS = (
    TREASURY_YIELDS + BOND_ETF + DOLLAR_FX
    + VOLATILITY + ENERGY + ENERGY_ETF + CRYPTO
)

CHINESE_NAMES = {
    "^IRX": "3月期美债收益率", "^FVX": "5年期美债收益率",
    "^TNX": "10年期美债收益率", "^TYX": "30年期美债收益率",
    "TLT": "20+年美债ETF", "SHY": "1-3年短债ETF",
    "IEF": "7-10年中期美债ETF", "HYG": "高收益债ETF",
    "LQD": "投资级企业债ETF",
    "DX-Y.NYB": "美元指数DXY", "EURUSD=X": "欧元/美元",
    "CNY=X": "美元/人民币", "JPY=X": "美元/日元",
    "GBPUSD=X": "英镑/美元",
    "^VIX": "VIX恐慌指数",
    "CL=F": "WTI原油期货", "BZ=F": "布伦特原油期货",
    "NG=F": "天然气期货",
    "USO": "原油ETF-USO", "XLE": "能源板块ETF",
    "UNG": "天然气ETF",
    "BTC-USD": "比特币", "ETH-USD": "以太坊", "SOL-USD": "Solana",
}


def get_cn(ticker: str) -> str:
    """返回中文名称."""
    return CHINESE_NAMES.get(ticker, "")


def safe_pct(val) -> str:
    """格式化百分比，None/NaN 返回 '—'."""
    if val is None:
        return "—"
    try:
        if np.isnan(float(val)):
            return "—"
    except (TypeError, ValueError):
        pass
    return f"{float(val):+.2f}%"


def safe_price(val, decimals: int = 2) -> str:
    """格式化价格."""
    if val is None:
        return "—"
    try:
        if np.isnan(float(val)):
            return "—"
    except (TypeError, ValueError):
        pass
    return f"{float(val):.{decimals}f}"


def full_name(row: dict) -> str:
    """英文名 + 中文名."""
    en = row.get("name", row.get("ticker", ""))
    cn = get_cn(row["ticker"])
    return f"{en} / {cn}" if cn else en


def fetch_data(tickers: list[str]) -> pd.DataFrame:
    """批量拉取行情数据."""
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

                    closes_raw = hist["Close"]
                    if pd.isna(closes_raw.iloc[-1]):
                        if len(closes_raw) >= 2 and not pd.isna(closes_raw.iloc[-2]):
                            hist = hist.iloc[:-1]
                        else:
                            continue

                    closes = hist["Close"]
                    today_close = closes.iloc[-1]
                    prev_close = closes.iloc[-2]
                    change_daily = ((today_close - prev_close) / prev_close) * 100

                    if len(closes) >= 6:
                        change_weekly = (
                            (today_close - closes.iloc[-6]) / closes.iloc[-6]
                        ) * 100
                    else:
                        change_weekly = None

                    if len(closes) >= 22:
                        change_monthly = (
                            (today_close - closes.iloc[-22]) / closes.iloc[-22]
                        ) * 100
                    elif len(closes) >= 15:
                        change_monthly = (
                            (today_close - closes.iloc[-15]) / closes.iloc[-15]
                        ) * 100
                    else:
                        change_monthly = None

                    all_data.append({
                        "ticker": t,
                        "name": info.get("shortName", info.get("longName", t)),
                        "close": today_close,
                        "prev_close": prev_close,
                        "change_daily": round(change_daily, 2),
                        "change_weekly": (
                            round(change_weekly, 2) if change_weekly is not None
                            else None
                        ),
                        "change_monthly": (
                            round(change_monthly, 2) if change_monthly is not None
                            else None
                        ),
                    })
                except Exception as e:
                    print(f"  [WARN] {t} 数据拉取失败: {e}")
                    continue
        except Exception as e:
            print(f"  [WARN] 批次失败: {e}")
    return pd.DataFrame(all_data)


def _render_table(df: pd.DataFrame, tickers: list[str],
                  price_prefix: str = "") -> list[str]:
    """渲染通用表格行."""
    lines = [
        "| 标的 | 名称 | 价格 | 日涨幅 | 周涨幅 | 月涨幅 |",
        "|------|------|:---:|:---:|:---:|:---:|",
    ]
    subset = df[df["ticker"].isin(tickers)]
    for _, row in subset.iterrows():
        w = safe_pct(row["change_weekly"])
        m = safe_pct(row["change_monthly"])
        p = f"{price_prefix}{safe_price(row['close'])}"
        lines.append(
            f"| **{row['ticker']}** | {full_name(row)} | {p} | "
            f"{safe_pct(row['change_daily'])} | {w} | {m} |"
        )
    return lines


def generate_report(df: pd.DataFrame, date_str: str) -> str:
    """生成 Markdown 日报."""
    if df.empty:
        return f"# 宏观指标日报 {date_str}\n\n> 当日无数据\n"

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        "---",
        f"title: 宏观指标日报 {date_str}",
        "type: summary",
        f"created: {date_str}",
        "tags: [宏观, 利率, 汇率, VIX, 原油, 加密, 市场监控, 日报]",
        "---",
        "",
        f"# 宏观指标日报 {date_str}",
        "",
        f"> 自动生成于 {now} · 数据源 Yahoo Finance",
        "",
    ]

    # --- 速览面板 ---
    key_tickers = {
        "^TNX": "10Y美债", "DX-Y.NYB": "美元", "^VIX": "VIX",
        "CL=F": "WTI", "BTC-USD": "BTC",
    }
    key_data = df[df["ticker"].isin(key_tickers.keys())]
    if not key_data.empty:
        lines += ["## 核心指标速览", ""]
        parts = []
        for _, row in key_data.iterrows():
            label = key_tickers.get(row["ticker"], row["ticker"])
            parts.append(
                f"**{label}** {safe_price(row['close'])} "
                f"({safe_pct(row['change_daily'])})"
            )
        lines.append(" · ".join(parts))
        lines.append("")

    # --- VIX 风险提示 ---
    vix_row = df[df["ticker"] == "^VIX"]
    if not vix_row.empty:
        vix_val = vix_row.iloc[0]["close"]
        vix_chg = vix_row.iloc[0]["change_daily"]
        if vix_val >= 30:
            lines.append(
                f"> **VIX 警报** {safe_price(vix_val)} "
                f"({safe_pct(vix_chg)}) — 市场恐慌，考虑降低风险敞口"
            )
        elif vix_val >= 20:
            lines.append(
                f"> **VIX 警惕** {safe_price(vix_val)} "
                f"({safe_pct(vix_chg)}) — 风险偏好下降，注意仓位控制"
            )
        else:
            lines.append(
                f"> VIX {safe_price(vix_val)} "
                f"({safe_pct(vix_chg)}) — 市场情绪稳定"
            )
        lines.append("")

    # --- 利率曲线 ---
    yield_data = df[df["ticker"].isin(TREASURY_YIELDS)]
    if not yield_data.empty:
        lines += [
            "## 美债收益率",
            "",
        ]
        lines += _render_table(df, TREASURY_YIELDS)

        y2 = df[df["ticker"] == "^FVX"]
        y10 = df[df["ticker"] == "^TNX"]
        if not y2.empty and not y10.empty:
            spread_5_10 = y10.iloc[0]["close"] - y2.iloc[0]["close"]
            if spread_5_10 < 0:
                lines.append(
                    f"\n> ⚠️ 5Y-10Y 利差倒挂 "
                    f"({safe_price(spread_5_10)}%)，衰退信号"
                )
            else:
                lines.append(
                    f"\n> 5Y-10Y 利差 {safe_price(spread_5_10)}%"
                )
        lines.append("")

    # --- 债券 ETF ---
    bond_data = df[df["ticker"].isin(BOND_ETF)]
    if not bond_data.empty:
        lines += ["## 债券 ETF", ""]
        lines += _render_table(df, BOND_ETF, price_prefix="$")
        lines.append("")

    # --- 汇率 ---
    fx_data = df[df["ticker"].isin(DOLLAR_FX)]
    if not fx_data.empty:
        lines += ["## 美元与汇率", ""]
        lines += _render_table(df, DOLLAR_FX)
        lines.append("")

    # --- 能源 ---
    energy_data = df[df["ticker"].isin(ENERGY + ENERGY_ETF)]
    if not energy_data.empty:
        lines += ["## 能源", ""]
        lines += _render_table(df, ENERGY + ENERGY_ETF, price_prefix="$")
        lines.append("")

    # --- 加密货币 ---
    crypto_data = df[df["ticker"].isin(CRYPTO)]
    if not crypto_data.empty:
        lines += ["## 加密货币", ""]
        lines += _render_table(df, CRYPTO, price_prefix="$")
        lines.append("")

    return "\n".join(lines)


def main():
    date_str = datetime.now().strftime("%Y-%m-%d")
    print(f"宏观指标监控 · {date_str}")
    print(f"  拉取 {len(ALL_TICKERS)} 个标的...")
    df = fetch_data(ALL_TICKERS)
    if df.empty:
        print("[ERROR] 无数据")
        sys.exit(1)
    print(f"  成功拉取 {len(df)} 个")

    md = generate_report(df, date_str)
    md_path = DATA_DIR / f"{date_str}.md"
    md_path.write_text(md, encoding="utf-8")
    print(f"  → {md_path}")

    records = []
    for _, row in df.iterrows():
        r = row.to_dict()
        for k, v in r.items():
            if isinstance(v, pd.Timestamp):
                r[k] = str(v)
            elif isinstance(v, float) and np.isnan(v):
                r[k] = None
        records.append(r)

    json_path = DATA_DIR / f"{date_str}.json"
    json_path.write_text(
        json.dumps(
            {"date": date_str, "data": records},
            ensure_ascii=False, indent=2,
        ),
        encoding="utf-8",
    )
    print(f"  → {json_path}")

    # 速览
    for label, ticker in [
        ("10Y美债", "^TNX"), ("美元指数", "DX-Y.NYB"),
        ("VIX", "^VIX"), ("WTI原油", "CL=F"), ("BTC", "BTC-USD"),
    ]:
        row = df[df["ticker"] == ticker]
        if not row.empty:
            r = row.iloc[0]
            print(f"  {label:8s} {safe_price(r['close'])}  {safe_pct(r['change_daily'])}")


if __name__ == "__main__":
    main()
