#!/usr/bin/env python3
# 数据源: 东方财富基金排行 + 天天基金实时估值
# 运行:   cd obsidian-notes && source .venv/bin/activate && python Resources/scripts/fund-monitor/fund_monitor.py
"""
中国公募基金每日监控脚本
盘后拉取各类型基金涨幅排行 + 热门板块基金表现

输出: 5.Finance/DailyData/funds/ → YYYY-MM-DD.md + .json
"""

import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path

import requests

SCRIPT_DIR = Path(__file__).resolve().parent
VAULT_ROOT = SCRIPT_DIR.parent.parent.parent
DATA_DIR = VAULT_ROOT / "5.Finance" / "DailyData" / "funds"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# --- Proxy ---
PROXIES = {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}

# --- 基金类型 (东方财富 API ft 参数) ---
FUND_TYPES = {
    "股票型": "gp",
    "混合型": "hh",
    "指数型": "zs",
    "QDII": "qdii",
    "债券型": "zq",
    "FOF": "fof",
}

# --- 热门板块基金 ---
SECTOR_FUNDS = {
    "半导体/芯片": [
        ("320007", "诺安成长混合"),
        ("008281", "国泰CES半导体芯片ETF联接A"),
        ("008282", "国泰CES半导体芯片ETF联接C"),
        ("008887", "华夏国证半导体芯片ETF联接A"),
        ("007301", "国联安中证半导体ETF联接C"),
    ],
    "新能源/光伏": [
        ("001156", "申万菱信新能源汽车"),
        ("161028", "富国中证新能源汽车"),
        ("009067", "国泰中证新能源汽车ETF联接A"),
        ("400015", "东方新能源汽车"),
    ],
    "消费/白酒": [
        ("110022", "易方达消费行业"),
        ("000083", "汇添富消费行业"),
        ("160222", "国泰国证食品饮料"),
        ("519915", "富国消费主题"),
    ],
    "医药/医疗": [
        ("000220", "富国医疗保健"),
        ("161726", "招商国证生物医药"),
        ("000913", "农银医疗保健"),
        ("001344", "华宝医药生物"),
    ],
    "军工/国防": [
        ("002251", "华夏军工安全"),
        ("004224", "南方军工改革"),
        ("005609", "富国军工主题"),
        ("161024", "富国中证军工"),
    ],
    "AI/人工智能": [
        ("001986", "前海开源人工智能"),
        ("008586", "华夏人工智能ETF联接C"),
        ("161631", "融通人工智能"),
        ("002803", "东方红沪港深"),
    ],
    "红利/高股息": [
        ("090010", "大成中证红利"),
        ("501029", "华宝标普中国A股红利机会"),
        ("512890", "华泰柏瑞红利低波ETF"),
        ("161907", "万家中证红利"),
    ],
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://fund.eastmoney.com/",
}


# --- 格式化工具 ---
def pct(v):
    """格式化百分比，空值返回 '—'"""
    if v is None:
        return "—"
    try:
        f = float(v)
        return f"{f:+.2f}%"
    except (TypeError, ValueError):
        return "—"


def price(v):
    """格式化净值，空值返回 '—'"""
    if v is None:
        return "—"
    try:
        return f"{float(v):.4f}"
    except (TypeError, ValueError):
        return "—"


# --- 数据拉取 ---
def fetch_rankings(fund_type_code, top_n=10):
    """
    从东方财富拉取基金涨幅排行。
    返回 list[dict]，字段: code, name, nav_date, nav, change_daily, change_weekly,
    change_monthly, change_3month
    """
    url = "https://fund.eastmoney.com/data/rankhandler.aspx"
    params = {
        "op": "ph", "dt": "kf", "ft": fund_type_code,
        "rs": "", "gs": "0",
        "sc": "zzf", "st": "desc",
        "pi": "1", "pn": str(top_n), "dx": "1",
    }
    try:
        resp = requests.get(url, params=params, headers=HEADERS, proxies=PROXIES, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        print(f"  [WARN] {fund_type_code} 请求失败: {e}")
        return []

    # 解析 JS 对象 → JSON: 东方财富返回的是 JS 对象 (key 不带引号)
    m = re.search(r"\{.*\}", resp.text, re.DOTALL)
    if not m:
        return []

    # 为 unquoted keys 加引号: {key: → {"key":
    js_text = m.group(0)
    json_text = re.sub(r'([\{,])\s*(\w+)\s*:', r'\1"\2":', js_text)
    try:
        data = json.loads(json_text)
    except json.JSONDecodeError:
        return []

    funds = []
    for item in data.get("datas", []):
        parts = item.split(",")
        if len(parts) < 11:
            continue
        funds.append({
            "code": parts[0],
            "name": parts[1],
            "nav_date": parts[3] if len(parts) > 3 else "",
            "nav": float(parts[4]) if parts[4] else None,
            "change_daily": float(parts[6]) if parts[6] else None,
            "change_weekly": float(parts[7]) if parts[7] else None,
            "change_monthly": float(parts[8]) if parts[8] else None,
            "change_3month": float(parts[9]) if parts[9] else None,
        })
    return funds


def fetch_valuation(fund_code):
    """从天天基金拉取单只基金实时估值。返回 dict 或 None。"""
    url = f"https://fundgz.1234567.com.cn/js/{fund_code}.js"
    try:
        resp = requests.get(url, headers=HEADERS, proxies=PROXIES, timeout=10)
        resp.raise_for_status()
    except Exception:
        return None

    m = re.search(r"jsonpgz\((.*?)\);", resp.text, re.DOTALL)
    if not m:
        return None
    try:
        item = json.loads(m.group(1))
    except json.JSONDecodeError:
        return None
    return {
        "code": item["fundcode"],
        "name": item["name"],
        "nav": float(item["dwjz"]) if item.get("dwjz") else None,
        "est_nav": float(item["gsz"]) if item.get("gsz") else None,
        "est_change": float(item["gszzl"]) if item.get("gszzl") else None,
        "nav_date": item.get("jzrq", ""),
        "est_time": item.get("gztime", ""),
    }


def fetch_sector_data():
    """拉取所有热门板块基金的实时估值。返回 dict[sector_name, list[dict]]。"""
    # 收集所有唯一基金代码
    seen = set()
    ordered = []
    for funds in SECTOR_FUNDS.values():
        for code, _name in funds:
            if code not in seen:
                seen.add(code)
                ordered.append(code)

    print(f"  逐个拉取 {len(ordered)} 只板块基金估值...")
    valuations = {}
    for i, code in enumerate(ordered):
        v = fetch_valuation(code)
        if v:
            valuations[code] = v
        if (i + 1) % 10 == 0:
            print(f"    ... {i + 1}/{len(ordered)}")
        time.sleep(0.3)

    sector_data = {}
    for sector_name, funds in SECTOR_FUNDS.items():
        items = []
        for code, fallback_name in funds:
            if code in valuations:
                items.append(valuations[code])
            else:
                items.append({
                    "code": code, "name": fallback_name,
                    "nav": None, "est_nav": None, "est_change": None,
                    "nav_date": "", "est_time": "",
                })
        sector_data[sector_name] = items
    return sector_data


# --- 报告生成 ---
def build_report(date_str, rankings, sector_data, top_losers):
    lines = [
        "---",
        f"title: 公募基金日报 {date_str}",
        "type: summary",
        f"created: {date_str}",
        "tags: [基金, 公募基金, 市场监控, 日报]",
        "---",
        "",
        f"# 公募基金日报 {date_str}",
        "",
        f"> 自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M')} · "
        "数据源: 东方财富/天天基金",
        "",
    ]

    # 各类型涨幅 TOP 10
    for type_name, funds in rankings.items():
        if not funds:
            continue
        lines += [
            f"## {type_name}基金 涨幅 TOP 10",
            "",
            "| 代码 | 名称 | 净值 | 日涨幅 | 近1周 | 近1月 | 近3月 |",
            "|------|------|:---:|:---:|:---:|:---:|:---:|",
        ]
        for f in funds:
            lines.append(
                f"| {f['code']} | {f['name']} | {price(f['nav'])} | "
                f"{pct(f['change_daily'])} | {pct(f['change_weekly'])} | "
                f"{pct(f['change_monthly'])} | {pct(f['change_3month'])} |"
            )
        lines.append("")

    # 热门板块基金
    lines += ["## 热门板块基金表现", ""]
    for sector_name, funds in sector_data.items():
        lines += [
            f"### {sector_name}",
            "",
            "| 代码 | 名称 | 净值 | 估算涨幅 |",
            "|------|------|:---:|:---:|",
        ]
        for f in funds:
            lines.append(
                f"| {f['code']} | {f['name']} | {price(f['nav'])} | "
                f"{pct(f['est_change'])} |"
            )
        lines.append("")

    # 跌幅 TOP 5
    lines += [
        "## 跌幅 TOP 5（股票型+混合型）",
        "",
        "| 代码 | 名称 | 净值 | 日涨幅 |",
        "|------|------|:---:|:---:|",
    ]
    for f in top_losers:
        lines.append(
            f"| {f['code']} | {f['name']} | {price(f['nav'])} | "
            f"{pct(f['change_daily'])} |"
        )
    lines.append("")

    return "\n".join(lines)


# --- 主流程 ---
def main():
    date_str = datetime.now().strftime("%Y-%m-%d")
    print(f"公募基金监控 · {date_str}")

    # 1. 拉取各类型基金涨幅排行
    rankings = {}
    for type_name, type_code in FUND_TYPES.items():
        print(f"  拉取{type_name}基金排行...")
        funds = fetch_rankings(type_code, top_n=10)
        rankings[type_name] = funds
        if funds:
            print(f"    → {len(funds)} 条 (涨幅第1: {funds[0]['name']} {pct(funds[0]['change_daily'])})")

    # 2. 拉取热门板块基金估值
    sector_data = fetch_sector_data()

    # 3. 跌幅 TOP 5 (股票型+混合型各取50条，合并排序)
    losers_gp = fetch_rankings("gp", top_n=50)
    losers_hh = fetch_rankings("hh", top_n=50)
    all_losers = losers_gp + losers_hh
    all_losers.sort(key=lambda x: x.get("change_daily") or -999)
    top_losers = all_losers[:5]

    # 4. 生成报告
    md = build_report(date_str, rankings, sector_data, top_losers)
    md_path = DATA_DIR / f"{date_str}.md"
    md_path.write_text(md, encoding="utf-8")
    print(f"\n  → {md_path}")

    json_path = DATA_DIR / f"{date_str}.json"
    json_path.write_text(
        json.dumps({
            "date": date_str,
            "generated_at": datetime.now().isoformat(),
            "rankings": rankings,
            "sectors": {
                k: [{sk: sv for sk, sv in f.items()} for f in v]
                for k, v in sector_data.items()
            },
            "top_losers": top_losers,
        }, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"  → {json_path}")

    # 摘要
    print("\n各类型涨幅第一:")
    for type_name, funds in rankings.items():
        if funds:
            f = funds[0]
            print(f"  {type_name:5s}  {f['code']}  {f['name'][:20]:20s}  {pct(f['change_daily'])}")


if __name__ == "__main__":
    main()