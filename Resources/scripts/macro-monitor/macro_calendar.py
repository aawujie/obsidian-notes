#!/usr/bin/env python3
# 数据源: 硬编码 FOMC 日程 + Tavily Search API (经济事件)
# 运行:   cd obsidian-notes && source .venv/bin/activate && python Resources/scripts/macro-monitor/macro_calendar.py
"""
宏观经济日历监控脚本.

追踪对金融市场影响最大的经济事件：
- FOMC 利率决议（硬编码 2026 日程 + 利率预测）
- CPI / PPI / PCE（通胀）
- 非农就业 / 失业率
- GDP / PMI / 零售销售
- 中国 PMI / 贸易数据
- 全球央行议息（ECB / BOJ / PBOC）

输出: 5.Finance/DailyData/macro-calendar/ → YYYY-MM-DD.md + .json
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

import requests

SCRIPT_DIR = Path(__file__).resolve().parent
VAULT_ROOT = SCRIPT_DIR.parent.parent.parent
DATA_DIR = VAULT_ROOT / "5.Finance" / "DailyData" / "macro-calendar"
DATA_DIR.mkdir(parents=True, exist_ok=True)

TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY", "")
PROXY = os.environ.get("https_proxy", "http://127.0.0.1:7890")
PROXIES = {"http": PROXY, "https": PROXY}

# ═══════════════════════════════════════════════════════════════
#  2026 年关键经济事件日程（每年初更新一次）
#
#  来源:
#  - FOMC: https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm
#  - CPI/NFP/GDP: BLS/BEA 官方日历（每年 12 月公布下一年）
#  - ECB/BOJ: 各央行官网
# ═══════════════════════════════════════════════════════════════

FIXED_EVENTS_2026 = [
    # FOMC 利率决议
    {"date": "2026-01-28", "event": "FOMC 利率决议", "importance": "critical",
     "category": "央行", "note": "附新闻发布会"},
    {"date": "2026-03-18", "event": "FOMC 利率决议", "importance": "critical",
     "category": "央行", "note": "附 SEP 经济预测 + 点阵图"},
    {"date": "2026-05-06", "event": "FOMC 利率决议", "importance": "critical",
     "category": "央行", "note": "附新闻发布会"},
    {"date": "2026-06-17", "event": "FOMC 利率决议", "importance": "critical",
     "category": "央行", "note": "附 SEP 经济预测 + 点阵图"},
    {"date": "2026-07-29", "event": "FOMC 利率决议", "importance": "critical",
     "category": "央行", "note": "附新闻发布会"},
    {"date": "2026-09-16", "event": "FOMC 利率决议", "importance": "critical",
     "category": "央行", "note": "附 SEP 经济预测 + 点阵图"},
    {"date": "2026-11-04", "event": "FOMC 利率决议", "importance": "critical",
     "category": "央行", "note": "附新闻发布会"},
    {"date": "2026-12-16", "event": "FOMC 利率决议", "importance": "critical",
     "category": "央行", "note": "附 SEP 经济预测 + 点阵图"},

    # CPI（通常每月第二或第三周二/三发布）
    {"date": "2026-01-14", "event": "美国 CPI (12月)", "importance": "high",
     "category": "通胀"},
    {"date": "2026-02-11", "event": "美国 CPI (1月)", "importance": "high",
     "category": "通胀"},
    {"date": "2026-03-11", "event": "美国 CPI (2月)", "importance": "high",
     "category": "通胀"},
    {"date": "2026-04-14", "event": "美国 CPI (3月)", "importance": "high",
     "category": "通胀"},
    {"date": "2026-05-13", "event": "美国 CPI (4月)", "importance": "high",
     "category": "通胀"},
    {"date": "2026-06-10", "event": "美国 CPI (5月)", "importance": "high",
     "category": "通胀"},
    {"date": "2026-07-15", "event": "美国 CPI (6月)", "importance": "high",
     "category": "通胀"},
    {"date": "2026-08-12", "event": "美国 CPI (7月)", "importance": "high",
     "category": "通胀"},
    {"date": "2026-09-11", "event": "美国 CPI (8月)", "importance": "high",
     "category": "通胀"},
    {"date": "2026-10-13", "event": "美国 CPI (9月)", "importance": "high",
     "category": "通胀"},
    {"date": "2026-11-12", "event": "美国 CPI (10月)", "importance": "high",
     "category": "通胀"},
    {"date": "2026-12-11", "event": "美国 CPI (11月)", "importance": "high",
     "category": "通胀"},

    # 非农就业报告（通常每月第一个周五）
    {"date": "2026-01-09", "event": "非农就业报告 (12月)", "importance": "high",
     "category": "就业"},
    {"date": "2026-02-06", "event": "非农就业报告 (1月)", "importance": "high",
     "category": "就业"},
    {"date": "2026-03-06", "event": "非农就业报告 (2月)", "importance": "high",
     "category": "就业"},
    {"date": "2026-04-03", "event": "非农就业报告 (3月)", "importance": "high",
     "category": "就业"},
    {"date": "2026-05-01", "event": "非农就业报告 (4月)", "importance": "high",
     "category": "就业"},
    {"date": "2026-06-05", "event": "非农就业报告 (5月)", "importance": "high",
     "category": "就业"},
    {"date": "2026-07-02", "event": "非农就业报告 (6月)", "importance": "high",
     "category": "就业"},
    {"date": "2026-08-07", "event": "非农就业报告 (7月)", "importance": "high",
     "category": "就业"},
    {"date": "2026-09-04", "event": "非农就业报告 (8月)", "importance": "high",
     "category": "就业"},
    {"date": "2026-10-02", "event": "非农就业报告 (9月)", "importance": "high",
     "category": "就业"},
    {"date": "2026-11-06", "event": "非农就业报告 (10月)", "importance": "high",
     "category": "就业"},
    {"date": "2026-12-04", "event": "非农就业报告 (11月)", "importance": "high",
     "category": "就业"},
]

IMPORTANCE_EMOJI = {
    "critical": "🔴",
    "high": "🟠",
    "medium": "🟡",
    "low": "🟢",
}


def get_upcoming_fixed_events(date_str: str, days_ahead: int = 14) -> list[dict]:
    """获取未来 N 天内的已知固定事件."""
    today = datetime.strptime(date_str, "%Y-%m-%d")
    end = today + timedelta(days=days_ahead)
    upcoming = []
    for evt in FIXED_EVENTS_2026:
        evt_date = datetime.strptime(evt["date"], "%Y-%m-%d")
        if today <= evt_date <= end:
            days_until = (evt_date - today).days
            upcoming.append({**evt, "days_until": days_until})
    return sorted(upcoming, key=lambda x: x["date"])


def get_recent_fixed_events(date_str: str, days_back: int = 3) -> list[dict]:
    """获取最近 N 天内已发生的事件（可能有市场余波）."""
    today = datetime.strptime(date_str, "%Y-%m-%d")
    start = today - timedelta(days=days_back)
    recent = []
    for evt in FIXED_EVENTS_2026:
        evt_date = datetime.strptime(evt["date"], "%Y-%m-%d")
        if start <= evt_date < today:
            days_ago = (today - evt_date).days
            recent.append({**evt, "days_ago": days_ago})
    return sorted(recent, key=lambda x: x["date"], reverse=True)


def search_economic_events(date_str: str) -> list[dict]:
    """通过 Tavily 搜索本周关键经济数据发布."""
    if not TAVILY_API_KEY:
        return []

    queries = [
        "US economic data release this week CPI GDP jobs",
        "Federal Reserve speech this week monetary policy",
        "China PMI economic data this week",
    ]

    all_events = []
    for query in queries:
        try:
            resp = requests.post(
                "https://api.tavily.com/search",
                json={
                    "api_key": TAVILY_API_KEY,
                    "query": query,
                    "search_depth": "basic",
                    "topic": "news",
                    "days": 3,
                    "max_results": 5,
                    "include_answer": True,
                },
                timeout=15,
                proxies=PROXIES,
            )
            resp.raise_for_status()
            data = resp.json()

            if data.get("answer"):
                all_events.append({
                    "source": "tavily_answer",
                    "query": query,
                    "answer": data["answer"][:500],
                })

            for r in data.get("results", [])[:3]:
                all_events.append({
                    "source": "tavily_result",
                    "title": r.get("title", ""),
                    "url": r.get("url", ""),
                    "content": r.get("content", "")[:300],
                })
        except Exception as e:
            print(f"  [WARN] Tavily 搜索失败: {e}")

    return all_events


def generate_report(
    date_str: str,
    upcoming: list[dict],
    recent: list[dict],
    web_events: list[dict],
) -> str:
    """生成 Markdown 日报."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        "---",
        f"title: 宏观经济日历 {date_str}",
        "type: summary",
        f"created: {date_str}",
        "tags: [宏观, 经济日历, FOMC, CPI, 非农, 市场监控, 日报]",
        "---",
        "",
        f"# 宏观经济日历 {date_str}",
        "",
        f"> 自动生成于 {now}",
        "",
    ]

    # --- 近期已发生事件 ---
    if recent:
        lines += ["## 近期已发生事件", ""]
        lines += [
            "| 日期 | 事件 | 重要性 | 类别 | 说明 | 距今 |",
            "|------|------|:---:|:---:|------|:---:|",
        ]
        for evt in recent:
            emoji = IMPORTANCE_EMOJI.get(evt["importance"], "")
            note = evt.get("note", "")
            lines.append(
                f"| {evt['date']} | {evt['event']} | "
                f"{emoji} {evt['importance']} | {evt['category']} | "
                f"{note} | {evt['days_ago']}天前 |"
            )
        lines.append("")

    # --- 未来 14 天事件 ---
    if upcoming:
        lines += ["## 未来两周关键事件", ""]
        lines += [
            "| 日期 | 事件 | 重要性 | 类别 | 说明 | 倒计时 |",
            "|------|------|:---:|:---:|------|:---:|",
        ]
        for evt in upcoming:
            emoji = IMPORTANCE_EMOJI.get(evt["importance"], "")
            note = evt.get("note", "")
            if evt["days_until"] == 0:
                countdown = "**今天**"
            elif evt["days_until"] == 1:
                countdown = "**明天**"
            else:
                countdown = f"{evt['days_until']}天"
            lines.append(
                f"| {evt['date']} | {evt['event']} | "
                f"{emoji} {evt['importance']} | {evt['category']} | "
                f"{note} | {countdown} |"
            )
        lines.append("")

        # FOMC 特别提醒
        fomc_events = [e for e in upcoming if "FOMC" in e["event"]]
        if fomc_events:
            next_fomc = fomc_events[0]
            lines += [
                "### FOMC 倒计时",
                "",
                f"> 下次 FOMC 利率决议: **{next_fomc['date']}** "
                f"({next_fomc['days_until']}天后)",
            ]
            if next_fomc.get("note"):
                lines.append(f"> {next_fomc['note']}")
            lines.append("")
    else:
        lines += [
            "## 未来两周关键事件",
            "",
            "> 未来 14 天内无重大已知经济事件",
            "",
        ]

    # --- 本周经济要闻（Tavily 搜索） ---
    if web_events:
        lines += ["## 本周经济要闻", ""]
        answers = [e for e in web_events if e["source"] == "tavily_answer"]
        if answers:
            for a in answers:
                lines.append(f"> {a['answer']}")
                lines.append("")
        articles = [e for e in web_events if e["source"] == "tavily_result"]
        if articles:
            lines += [
                "| 标题 | 摘要 |",
                "|------|------|",
            ]
            seen = set()
            for a in articles:
                title = a["title"][:80]
                if title in seen:
                    continue
                seen.add(title)
                url = a.get("url", "")
                content = a.get("content", "")[:100]
                title_md = f"[{title}]({url})" if url else title
                lines.append(f"| {title_md} | {content} |")
            lines.append("")

    # --- 重要性说明 ---
    lines += [
        "## 重要性说明",
        "",
        "| 级别 | 含义 | 典型事件 |",
        "|:---:|:---|:---|",
        "| 🔴 CRITICAL | 大概率引发市场剧烈波动 | "
        "FOMC 利率决议、非农就业（意外值）|",
        "| 🟠 HIGH | 可能显著影响市场情绪 | "
        "CPI、GDP、PMI |",
        "| 🟡 MEDIUM | 值得关注但影响有限 | "
        "零售销售、工业产出、央行讲话 |",
        "| 🟢 LOW | 常规跟踪 | "
        "消费者信心、贸易数据 |",
    ]

    return "\n".join(lines)


def main():
    date_str = datetime.now().strftime("%Y-%m-%d")
    print(f"宏观经济日历 · {date_str}")

    # 1. 固定事件
    upcoming = get_upcoming_fixed_events(date_str)
    recent = get_recent_fixed_events(date_str)
    print(f"  未来 14 天事件: {len(upcoming)} 个")
    print(f"  近期已发生事件: {len(recent)} 个")

    # 2. 搜索本周经济要闻
    print("  搜索本周经济要闻...")
    web_events = search_economic_events(date_str)
    print(f"  获取 {len(web_events)} 条")

    # 3. 生成报告
    md = generate_report(date_str, upcoming, recent, web_events)
    md_path = DATA_DIR / f"{date_str}.md"
    md_path.write_text(md, encoding="utf-8")
    print(f"  → {md_path}")

    # 4. JSON
    json_data = {
        "date": date_str,
        "generated_at": datetime.now().isoformat(),
        "upcoming_events": upcoming,
        "recent_events": recent,
        "web_events": web_events,
    }
    json_path = DATA_DIR / f"{date_str}.json"
    json_path.write_text(
        json.dumps(json_data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"  → {json_path}")

    # 5. 控制台摘要
    if upcoming:
        print("\n  关键事件:")
        for evt in upcoming[:5]:
            emoji = IMPORTANCE_EMOJI.get(evt["importance"], "")
            if evt["days_until"] == 0:
                when = "今天"
            elif evt["days_until"] == 1:
                when = "明天"
            else:
                when = f"{evt['days_until']}天后"
            print(f"    {emoji} {evt['date']}  {evt['event']}  ({when})")
    else:
        print("\n  未来 14 天无重大已知事件")


if __name__ == "__main__":
    main()
