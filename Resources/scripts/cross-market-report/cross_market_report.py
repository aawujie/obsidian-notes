"""跨市场综合日报生成器.

聚合所有市场监控模块的数据，生成一份"一页纸"全景视图，
涵盖宏观、权益、商品、地缘政治、经济日历。
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

VAULT = Path("/home/dr/Documents/obsidian-notes")
DAILY_DIR = VAULT / "5.Finance" / "DailyData"
DATE = datetime.now().strftime("%Y-%m-%d")

CN = {
    "^TNX": "10Y美债", "^TYX": "30Y美债", "^IRX": "3M美债", "^FVX": "5Y美债",
    "DX-Y.NYB": "美元指数", "^VIX": "VIX恐慌指数",
    "CL=F": "WTI原油", "BZ=F": "布伦特原油", "NG=F": "天然气",
    "BTC-USD": "比特币", "ETH-USD": "以太坊", "SOL-USD": "Solana",
    "EURUSD=X": "EUR/USD", "CNY=X": "USD/CNY", "JPY=X": "USD/JPY",
    "GC=F": "黄金期货", "SI=F": "白银期货", "HG=F": "铜期货",
    "000001.SS": "上证指数", "399001.SZ": "深证成指", "399006.SZ": "创业板指",
    "000300.SS": "沪深300",
    "^HSI": "恒生指数", "^HSTECH": "恒生科技",
    "TLT": "20+年美债ETF", "HYG": "高收益债ETF", "LQD": "投资级债ETF",
    "GLD": "SPDR黄金ETF", "GDX": "金矿ETF",
    "XLE": "能源ETF", "USO": "原油ETF",
}


def load_json(market: str) -> dict | None:
    """加载指定市场今日的 JSON 数据."""
    path = DAILY_DIR / market / f"{DATE}.json"
    if not path.exists():
        return None
    try:
        with open(path) as f:
            return json.load(f)
    except Exception as e:
        print(f"  [WARN] 加载 {market} 数据失败: {e}", file=sys.stderr)
        return None


def cn(ticker: str) -> str:
    return CN.get(ticker, ticker)


def pct(v: float | None) -> str:
    if v is None:
        return "—"
    return f"{v:+.2f}%"


def pr(v: float | None, decimals: int = 2) -> str:
    if v is None:
        return "—"
    return f"{v:.{decimals}f}"


def find_ticker(data: list[dict], ticker: str) -> dict | None:
    for d in data:
        if d.get("ticker") == ticker:
            return d
    return None


def risk_emoji(change: float | None) -> str:
    """根据涨跌幅返回情绪指示."""
    if change is None:
        return "⚪"
    if change >= 2:
        return "🟢"
    if change >= 0.5:
        return "🟩"
    if change >= -0.5:
        return "⚪"
    if change >= -2:
        return "🟧"
    return "🔴"


def section_macro(macro_data: dict | None) -> list[str]:
    """生成宏观板块: 利率、美元、VIX、能源、加密."""
    lines = ["## 📊 宏观全景", ""]
    if not macro_data:
        lines.append("> ⚠️ 今日宏观数据缺失")
        return lines

    data = macro_data.get("data", [])
    if not data:
        lines.append("> ⚠️ 今日宏观数据为空")
        return lines

    by_ticker = {d["ticker"]: d for d in data}

    groups = [
        ("利率", ["^IRX", "^FVX", "^TNX", "^TYX"]),
        ("美元 & 汇率", ["DX-Y.NYB", "EURUSD=X", "CNY=X", "JPY=X"]),
        ("风险情绪", ["^VIX"]),
        ("能源", ["CL=F", "BZ=F", "NG=F"]),
        ("加密货币", ["BTC-USD", "ETH-USD", "SOL-USD"]),
        ("信用", ["TLT", "HYG", "LQD"]),
    ]

    lines.append("| 板块 | 指标 | 收盘 | 日涨跌 | 周涨跌 |")
    lines.append("|:---|:---|:---:|:---:|:---:|")

    for group_name, tickers in groups:
        first = True
        for t in tickers:
            d = by_ticker.get(t)
            if not d:
                continue
            label = group_name if first else ""
            first = False
            emoji = risk_emoji(d.get("change_daily"))
            lines.append(
                f"| {label} | {emoji} {cn(t)} | {pr(d['close'])} "
                f"| {pct(d.get('change_daily'))} | {pct(d.get('change_weekly'))} |"
            )

    # VIX 风险提示
    vix = by_ticker.get("^VIX")
    if vix and vix.get("close"):
        vix_val = vix["close"]
        if vix_val > 30:
            lines.extend(["", "🚨 **VIX > 30 — 极度恐慌**"])
        elif vix_val > 25:
            lines.extend(["", "⚠️ **VIX > 25 — 高波动警告**"])
        elif vix_val > 20:
            lines.extend(["", "📌 VIX > 20 — 波动偏高"])

    # 利差分析
    tnx = by_ticker.get("^TNX")
    fvx = by_ticker.get("^FVX")
    if tnx and fvx and tnx.get("close") and fvx.get("close"):
        spread = tnx["close"] - fvx["close"]
        lines.extend([
            "",
            f"📐 **5Y-10Y 利差**: {spread:+.2f}% "
            f"{'（倒挂 ⚠️ 衰退信号）' if spread < 0 else '（正常）'}",
        ])

    lines.append("")
    return lines


def section_equities(
    us_data: dict | None,
    a_data: dict | None,
    hk_data: dict | None,
) -> list[str]:
    """生成权益市场板块: 三大市场主要指数 + TOP 异动."""
    lines = ["## 📈 权益市场", ""]

    lines.append("### 主要指数")
    lines.append("")
    lines.append("| 市场 | 指数 | 收盘 | 日涨跌 | 周涨跌 | 月涨跌 |")
    lines.append("|:---|:---|:---:|:---:|:---:|:---:|")

    # A 股
    if a_data and a_data.get("data"):
        a_list = a_data["data"]
        for t in ["000001.SS", "399001.SZ", "399006.SZ", "000300.SS"]:
            d = find_ticker(a_list, t)
            if d:
                emoji = risk_emoji(d.get("change_daily"))
                lines.append(
                    f"| 🇨🇳 A股 | {emoji} {cn(t)} | {pr(d['close'])} "
                    f"| {pct(d.get('change_daily'))} | {pct(d.get('change_weekly'))} "
                    f"| {pct(d.get('change_monthly'))} |"
                )

    # 港股
    if hk_data and hk_data.get("data"):
        hk_list = hk_data["data"]
        for t in ["^HSI", "^HSTECH"]:
            d = find_ticker(hk_list, t)
            if d:
                emoji = risk_emoji(d.get("change_daily"))
                lines.append(
                    f"| 🇭🇰 港股 | {emoji} {cn(t)} | {pr(d['close'])} "
                    f"| {pct(d.get('change_daily'))} | {pct(d.get('change_weekly'))} "
                    f"| {pct(d.get('change_monthly'))} |"
                )

    # 美股 — 从 data 中找指数级别的 ETF 代替
    if us_data and us_data.get("data"):
        us_list = us_data["data"]
        us_top = sorted(us_list, key=lambda x: x.get("market_cap") or 0, reverse=True)
        mag7 = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA"]
        for t in mag7:
            d = find_ticker(us_list, t)
            if d:
                emoji = risk_emoji(d.get("change_daily"))
                name = d.get("name", t)
                if len(name) > 10:
                    name = name[:10]
                lines.append(
                    f"| 🇺🇸 美股 | {emoji} {name} | {pr(d['close'])} "
                    f"| {pct(d.get('change_daily'))} | {pct(d.get('change_weekly'))} "
                    f"| {pct(d.get('change_monthly'))} |"
                )

    lines.append("")

    # 三大市场异动 TOP 3
    all_movers = []
    for label, mkt_data in [("🇨🇳", a_data), ("🇭🇰", hk_data), ("🇺🇸", us_data)]:
        if not mkt_data or not mkt_data.get("data"):
            continue
        for d in mkt_data["data"]:
            chg = d.get("change_daily")
            if chg is not None and d["ticker"] not in (
                "000001.SS", "399001.SZ", "399006.SZ", "000300.SS",
                "000688.SS", "^HSI", "^HSTECH", "^HSCE", "^HSCCI",
            ):
                all_movers.append({**d, "_flag": label})

    if all_movers:
        lines.append("### 🔥 全球异动 TOP 5")
        lines.append("")
        lines.append("| 市场 | 股票 | 收盘价 | 涨幅 |")
        lines.append("|:---:|:---|:---:|:---:|")

        up = sorted(all_movers, key=lambda x: x["change_daily"], reverse=True)[:5]
        for d in up:
            name = cn(d["ticker"])
            if name == d["ticker"]:
                name = d.get("name", d["ticker"])
            lines.append(
                f"| {d['_flag']} | 🟢 {name} | {pr(d['close'])} "
                f"| {pct(d['change_daily'])} |"
            )

        lines.append("")
        lines.append("| 市场 | 股票 | 收盘价 | 跌幅 |")
        lines.append("|:---:|:---|:---:|:---:|")

        down = sorted(all_movers, key=lambda x: x["change_daily"])[:5]
        for d in down:
            name = cn(d["ticker"])
            if name == d["ticker"]:
                name = d.get("name", d["ticker"])
            lines.append(
                f"| {d['_flag']} | 🔴 {name} | {pr(d['close'])} "
                f"| {pct(d['change_daily'])} |"
            )

        lines.append("")

    # 52 周新高
    new_highs = []
    for label, mkt_data in [("🇨🇳", a_data), ("🇭🇰", hk_data), ("🇺🇸", us_data)]:
        if not mkt_data or not mkt_data.get("data"):
            continue
        for d in mkt_data["data"]:
            if d.get("is_new_high"):
                name = cn(d["ticker"])
                if name == d["ticker"]:
                    name = d.get("name", d["ticker"])
                new_highs.append(f"{label}{name}")

    if new_highs:
        lines.append(f"### 🏆 52 周新高 ({len(new_highs)} 只)")
        lines.append("")
        lines.append(", ".join(new_highs[:20]))
        if len(new_highs) > 20:
            lines.append(f"…及另外 {len(new_highs) - 20} 只")
        lines.append("")

    return lines


def section_commodities(
    gold_data: dict | None,
    metals_data: dict | None,
) -> list[str]:
    """生成商品板块: 贵金属 + 工业金属."""
    lines = ["## ⛏️ 商品市场", ""]

    all_items = []
    for mkt_data in [gold_data, metals_data]:
        if mkt_data and mkt_data.get("data"):
            all_items.extend(mkt_data["data"])

    if not all_items:
        lines.append("> ⚠️ 今日商品数据缺失")
        return lines

    key_tickers = ["GC=F", "SI=F", "HG=F", "GLD", "GDX"]

    lines.append("| 品种 | 收盘 | 日涨跌 | 周涨跌 | 月涨跌 |")
    lines.append("|:---|:---:|:---:|:---:|:---:|")

    by_ticker = {d["ticker"]: d for d in all_items}
    for t in key_tickers:
        d = by_ticker.get(t)
        if d:
            emoji = risk_emoji(d.get("change_daily"))
            lines.append(
                f"| {emoji} {cn(t)} | {pr(d['close'])} "
                f"| {pct(d.get('change_daily'))} | {pct(d.get('change_weekly'))} "
                f"| {pct(d.get('change_monthly'))} |"
            )

    # 金属异动 TOP 3
    movers = sorted(all_items, key=lambda x: abs(x.get("change_daily") or 0), reverse=True)
    top_movers = [d for d in movers if abs(d.get("change_daily") or 0) >= 2][:3]
    if top_movers:
        lines.append("")
        lines.append("**异动**: " + " | ".join(
            f"{cn(d['ticker'])} {pct(d['change_daily'])}" for d in top_movers
        ))

    lines.append("")
    return lines


def section_funds(funds_data: dict | None) -> list[str]:
    """生成基金板块: 各类别冠军."""
    lines = ["## 💰 基金动态", ""]

    if not funds_data or not funds_data.get("rankings"):
        lines.append("> ⚠️ 今日基金数据缺失")
        return lines

    rankings = funds_data["rankings"]
    lines.append("| 类别 | 冠军基金 | 日涨幅 |")
    lines.append("|:---|:---|:---:|")

    for cat, items in rankings.items():
        if not items:
            continue
        top = items[0]
        name = top.get("name", "?")
        if len(name) > 20:
            name = name[:20] + "…"
        chg = top.get("change_daily")
        chg_str = f"{chg:+.2f}%" if chg is not None else "—"
        lines.append(f"| {cat} | {name} | {chg_str} |")

    lines.append("")
    return lines


def section_geopolitics(geo_data: dict | None) -> list[str]:
    """生成地缘政治板块."""
    lines = ["## 🌍 地缘政治", ""]

    if not geo_data:
        lines.append("> ⚠️ 今日地缘政治数据缺失")
        return lines

    events = geo_data.get("events", [])
    sev = geo_data.get("severity_distribution", {})
    total = geo_data.get("total_events", len(events))

    critical = sev.get("critical", 0)
    high = sev.get("high", 0)

    status_parts = [f"共 {total} 条"]
    if critical > 0:
        status_parts.append(f"🔴 {critical}")
    if high > 0:
        status_parts.append(f"🟠 {high}")
    lines.append(" | ".join(status_parts))
    lines.append("")

    top = [e for e in events if e.get("severity") in ("critical", "high")][:3]
    if not top:
        top = events[:3]

    for e in top:
        sev_icon = {
            "critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"
        }.get(e.get("severity", ""), "")
        title = e.get("title", "")[:60]
        regions = ", ".join(e.get("classified_regions", []))
        tickers = ", ".join(e.get("affected_tickers", [])[:5])
        lines.append(f"- {sev_icon} **{title}**")
        if regions:
            lines.append(f"  - 区域: {regions}")
        if tickers:
            lines.append(f"  - 关注: {tickers}")

    lines.append("")
    return lines


def section_calendar(cal_data: dict | None) -> list[str]:
    """生成经济日历板块."""
    lines = ["## 📅 经济日历", ""]

    if not cal_data:
        lines.append("> ⚠️ 今日经济日历数据缺失")
        return lines

    upcoming = cal_data.get("upcoming_events", [])
    emoji_map = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}

    if not upcoming:
        lines.append("> 未来 14 天无重大已知事件")
        return lines

    lines.append("| 日期 | 事件 | 重要性 | 倒计时 |")
    lines.append("|:---|:---|:---:|:---:|")

    for e in upcoming[:7]:
        em = emoji_map.get(e.get("importance", ""), "")
        dt = e.get("days_until", "?")
        when = "今天" if dt == 0 else ("明天" if dt == 1 else f"{dt}天后")
        lines.append(f"| {e['date']} | {em} {e['event']} | {e.get('importance', '')} | {when} |")

    lines.append("")
    return lines


def section_heatmap(
    us_data: dict | None,
    a_data: dict | None,
    hk_data: dict | None,
    macro_data: dict | None,
    gold_data: dict | None,
) -> list[str]:
    """生成顶部市场温度计 — 一行看全局."""
    lines = ["## 🌡️ 市场温度", ""]

    items = []

    # 各主要指数
    checks = [
        (a_data, "000001.SS", "上证"),
        (hk_data, "^HSI", "恒指"),
        (macro_data, "^VIX", "VIX"),
        (macro_data, "DX-Y.NYB", "美元"),
        (macro_data, "^TNX", "10Y美债"),
        (gold_data, "GC=F", "黄金"),
        (macro_data, "CL=F", "原油"),
        (macro_data, "BTC-USD", "BTC"),
    ]

    for mkt_data, ticker, label in checks:
        if not mkt_data or not mkt_data.get("data"):
            items.append(f"⚪ {label} —")
            continue
        d = find_ticker(mkt_data["data"], ticker)
        if not d:
            items.append(f"⚪ {label} —")
            continue
        chg = d.get("change_daily")
        emoji = risk_emoji(chg)
        items.append(f"{emoji} {label} {pct(chg)}")

    # 美股用 Mag7 平均
    if us_data and us_data.get("data"):
        mag7 = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA"]
        mag7_chgs = []
        for t in mag7:
            d = find_ticker(us_data["data"], t)
            if d and d.get("change_daily") is not None:
                mag7_chgs.append(d["change_daily"])
        if mag7_chgs:
            avg = sum(mag7_chgs) / len(mag7_chgs)
            emoji = risk_emoji(avg)
            items.append(f"{emoji} Mag7 {avg:+.2f}%")
        else:
            items.append("⚪ Mag7 —")

    lines.append(" | ".join(items))
    lines.append("")
    return lines


def generate_report() -> tuple[str, dict]:
    """生成完整的跨市场综合日报，返回 (md_content, json_data)."""
    # 加载所有数据源
    macro = load_json("macro")
    us = load_json("us-stock")
    a_stock = load_json("a-stock")
    hk = load_json("hk-stock")
    gold = load_json("gold")
    metals = load_json("metals")
    funds = load_json("funds")
    geo = load_json("geopolitics")
    cal = load_json("macro-calendar")

    available = sum(1 for x in [macro, us, a_stock, hk, gold, metals, funds, geo, cal] if x)

    lines = [
        "---",
        f"date: {DATE}",
        "type: cross-market-report",
        f"sources: {available}/9 modules",
        "tags: [日报, 跨市场, 综合]",
        "---",
        "",
        f"# 📋 跨市场综合日报 — {DATE}",
        "",
    ]

    lines.extend(section_heatmap(us, a_stock, hk, macro, gold))
    lines.extend(section_macro(macro))
    lines.extend(section_equities(us, a_stock, hk))
    lines.extend(section_commodities(gold, metals))
    lines.extend(section_funds(funds))
    lines.extend(section_geopolitics(geo))
    lines.extend(section_calendar(cal))

    # 数据源状态
    lines.append("---")
    lines.append("")
    lines.append("## 📂 数据源")
    lines.append("")
    sources = [
        ("宏观", "macro", macro), ("美股", "us-stock", us),
        ("A股", "a-stock", a_stock), ("港股", "hk-stock", hk),
        ("黄金", "gold", gold), ("金属", "metals", metals),
        ("基金", "funds", funds), ("地缘政治", "geopolitics", geo),
        ("经济日历", "macro-calendar", cal),
    ]
    for label, slug, data in sources:
        status = "✅" if data else "❌"
        count = ""
        if data and data.get("data"):
            count = f" ({len(data['data'])} 条)"
        elif data and data.get("events"):
            count = f" ({len(data['events'])} 条)"
        elif data and data.get("rankings"):
            count = f" ({len(data['rankings'])} 类)"
        elif data and data.get("upcoming_events"):
            count = f" ({len(data['upcoming_events'])} 条)"
        lines.append(f"- {status} [[{DATE}|{label}]]{count} → `DailyData/{slug}/{DATE}.md`")

    md = "\n".join(lines) + "\n"

    summary_json = {
        "date": DATE,
        "generated_at": datetime.now().isoformat(),
        "modules_available": available,
        "modules_total": 9,
    }

    return md, summary_json


def main():
    md, summary_json = generate_report()

    out_dir = DAILY_DIR / "cross-market"
    out_dir.mkdir(parents=True, exist_ok=True)

    md_path = out_dir / f"{DATE}.md"
    json_path = out_dir / f"{DATE}.json"

    with open(md_path, "w") as f:
        f.write(md)

    with open(json_path, "w") as f:
        json.dump(summary_json, f, ensure_ascii=False, indent=2)

    print(f"[OK] 跨市场综合日报已生成: {md_path}")
    print(f"[OK] 摘要 JSON: {json_path}")


if __name__ == "__main__":
    main()
