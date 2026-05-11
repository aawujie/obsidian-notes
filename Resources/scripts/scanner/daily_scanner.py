#!/usr/bin/env python3
# 数据源: 读取 DailyData 中的 JSON 日报
# 运行:   cd obsidian-notes && source .venv/bin/activate && python Resources/scripts/scanner/daily_scanner.py
"""
每日异常扫描脚本
读完五个 monitor 最新一天的 JSON，输出一份"今日关注"清单 → 5.Finance/DailyData/today-focus.md
"""

import json
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
VAULT_ROOT = SCRIPT_DIR.parent.parent.parent
DATA_ROOT = VAULT_ROOT / "5.Finance" / "DailyData"
OUTPUT = DATA_ROOT / "today-focus.md"

MONITORS = ["us-stock", "gold", "a-stock", "hk-stock", "metals"]


def latest_json(subdir):
    """找最新一份 JSON 文件"""
    files = sorted((DATA_ROOT / subdir).glob("*.json"), reverse=True)
    return files[0] if files else None


def load_data(subdir):
    """加载最新一天的结构化数据"""
    f = latest_json(subdir)
    if not f:
        return [], f.stem if f else "unknown"
    records = json.loads(f.read_text()).get("data", [])
    return records, f.stem


def is_trend_up(r):
    """日/周/月三列全正 → 趋势向上确认"""
    d = r.get("change_daily")
    w = r.get("change_weekly")
    m = r.get("change_monthly")
    if d is None or w is None or m is None:
        return False
    return d > 0 and w > 0 and m > 0


def is_volume_spike(r):
    """成交量 > 2 倍均值"""
    return r.get("vol_ratio", 0) > 2


def flag_stocks(records, label):
    """从一批记录中筛选值得关注的"""
    alerts = []
    for r in records:
        d = r.get("change_daily") or 0
        w = r.get("change_weekly")
        m = r.get("change_monthly")
        name = r.get("name", r.get("ticker", "?"))
        ticker = r.get("ticker", "?")
        vol = r.get("vol_ratio", 0)
        new_high = r.get("is_new_high", False)

        reasons = []
        if d >= 5:
            reasons.append(f"单日涨 {d:+.1f}%")
        elif d <= -5:
            reasons.append(f"单日跌 {d:+.1f}%")

        if is_trend_up(r):
            reasons.append("日/周/月全绿(趋势确认)")

        if is_volume_spike(r):
            reasons.append(f"异常放量 {vol:.1f}x")

        if new_high:
            reasons.append("创52周新高")

        if reasons:
            alerts.append({
                "ticker": ticker,
                "name": name,
                "source": label,
                "change_daily": d,
                "change_weekly": w,
                "change_monthly": m,
                "vol_ratio": vol,
                "is_new_high": new_high,
                "reasons": reasons,
            })

    return alerts


def build_report(all_alerts, dates):
    """生成 Markdown 报告"""
    lines = [
        "---",
        "title: 今日关注",
        "type: summary",
        f"created: {datetime.now().strftime('%Y-%m-%d')}",
        "tags: [扫描, 异常, 今日关注]",
        "---",
        "",
        "# 今日关注",
        "",
        f"> 自动扫描于 {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"> 数据日期: {', '.join(set(dates))}",
        "",
    ]

    if not all_alerts:
        lines += ["**今日无异常信号** — 所有品种在正常波动范围内。"]
        return "\n".join(lines)

    # 按日涨跌幅绝对值排序
    all_alerts.sort(key=lambda x: abs(x["change_daily"]), reverse=True)

    lines += [
        f"共发现 **{len(all_alerts)}** 个异常信号：",
        "",
        "| 来源 | 代码 | 名称 | 日 | 周 | 月 | 量 | 触发原因 |",
        "|------|------|------|:---:|:---:|:---:|:---:|------|",
    ]

    for a in all_alerts:
        w = f"{a['change_weekly']:+.1f}%" if a['change_weekly'] is not None else "—"
        m = f"{a['change_monthly']:+.1f}%" if a['change_monthly'] is not None else "—"
        lines.append(
            f"| {a['source']} | **{a['ticker']}** | {a['name']} | "
            f"**{a['change_daily']:+.1f}%** | {w} | {m} | "
            f"{a['vol_ratio']:.1f}x | {', '.join(a['reasons'])} |"
        )

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 下一步")
    lines.append("")
    lines.append("对上述标的逐一查催化剂：")
    lines.append("```")
    lines.append("# 在 Claude Code 中逐个问：")
    lines.append("# XX 今天涨/跌 X%，日/周/月全绿/全红，查下原因")
    lines.append("```")

    return "\n".join(lines)


def main():
    print("扫描最新 DailyData ...")

    all_alerts = []
    dates = []
    for m in MONITORS:
        records, ds = load_data(m)
        if not records:
            print(f"  {m}: 无数据, 跳过")
            continue
        dates.append(ds)
        alerts = flag_stocks(records, m)
        print(f"  {m}: {len(records)} 条 → {len(alerts)} 个异常 ({ds})")
        all_alerts.extend(alerts)

    md = build_report(all_alerts, dates)
    OUTPUT.write_text(md, encoding="utf-8")
    print(f"\n→ {OUTPUT}")
    print(f"  共 {len(all_alerts)} 个标的需要关注")


if __name__ == "__main__":
    main()