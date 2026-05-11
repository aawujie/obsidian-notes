#!/usr/bin/env python3
# 数据源: akshare (封装东方财富+天天基金 API)
# 运行:   cd obsidian-notes && source .venv/bin/activate && python Resources/scripts/fund-monitor/fund_monitor.py
"""
中国公募基金每日监控脚本
盘后拉取各类型基金涨幅排行 + 热门板块基金表现 + 基金经理/持仓信息

数据维度:
- 6 类基金 (股票/混合/指数/QDII/债券/FOF) × 日涨幅 TOP 10
- 10 个时间维度 (日/周/月/季/半年/1年/2年/3年/今年来/成立来)
- 7 大热门板块基金实时估值
- 涨幅第一基金经理信息 + 重仓股
- 五星基金经理榜单
- 跌幅 TOP 5

输出: 5.Finance/DailyData/funds/ → YYYY-MM-DD.md + YYYY-MM-DD.json
"""

import json
import re
import time
from datetime import datetime
from pathlib import Path

import akshare as ak
import pandas as pd
import requests

SCRIPT_DIR = Path(__file__).resolve().parent
VAULT_ROOT = SCRIPT_DIR.parent.parent.parent
DATA_DIR = VAULT_ROOT / "5.Finance" / "DailyData" / "funds"
DATA_DIR.mkdir(parents=True, exist_ok=True)

PROXIES = {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://fund.eastmoney.com/",
}

FUND_TYPES = ["股票型", "混合型", "指数型", "QDII", "债券型", "FOF"]

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


# --- 格式化工具 ---
def pct(v):
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return "—"
    try:
        return f"{float(v):+.2f}%"
    except (TypeError, ValueError):
        return "—"


def price(v):
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return "—"
    try:
        return f"{float(v):.4f}"
    except (TypeError, ValueError):
        return "—"


def _to_float(val) -> float | None:
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return None
    try:
        return float(val)
    except (TypeError, ValueError):
        return None


# --- 数据拉取 ---

def fetch_rankings(fund_type: str, top_n: int = 10) -> list[dict]:
    """拉取基金排行, 按日涨幅降序, 返回标准化 list[dict]"""
    try:
        df = ak.fund_open_fund_rank_em(symbol=fund_type)
    except Exception as e:
        print(f"  [WARN] {fund_type} 排行请求失败: {e}")
        return []

    if df is None or df.empty:
        return []

    # 按日增长率降序重排 (默认按"自定义"综合排序, 不是日涨幅)
    df = df.sort_values("日增长率", ascending=False, na_position="last")
    df = df.head(top_n)
    funds = []
    for _, row in df.iterrows():
        funds.append({
            "code": str(row.get("基金代码", "")),
            "name": str(row.get("基金简称", "")),
            "nav_date": str(row.get("日期", "")),
            "nav": _to_float(row.get("单位净值")),
            "change_daily": _to_float(row.get("日增长率")),
            "change_weekly": _to_float(row.get("近1周")),
            "change_monthly": _to_float(row.get("近1月")),
            "change_3month": _to_float(row.get("近3月")),
            "change_6month": _to_float(row.get("近6月")),
            "change_1year": _to_float(row.get("近1年")),
            "change_2year": _to_float(row.get("近2年")),
            "change_3year": _to_float(row.get("近3年")),
            "change_ytd": _to_float(row.get("今年来")),
            "change_inception": _to_float(row.get("成立来")),
            "fee": str(row.get("手续费", "")),
        })
    return funds


def fetch_valuation(fund_code: str) -> dict | None:
    """从天天基金拉取单只基金实时估值"""
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


def fetch_sector_data() -> dict[str, list[dict]]:
    """拉取所有热门板块基金的实时估值"""
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


def fetch_fund_manager_info(fund_codes: list[str]) -> dict[str, dict]:
    """通过雪球 API 获取基金详情 (基金经理/规模/类型/公司)"""
    result = {}
    for code in fund_codes:
        try:
            df = ak.fund_individual_basic_info_xq(symbol=code)
            if df is not None and not df.empty:
                info = dict(zip(df["item"], df["value"]))
                result[code] = {
                    "name": info.get("基金名称", ""),
                    "manager": info.get("基金经理", ""),
                    "company": info.get("基金公司", ""),
                    "scale": info.get("最新规模", ""),
                    "type": info.get("基金类型", ""),
                    "inception": info.get("成立时间", ""),
                }
        except Exception:
            pass
        time.sleep(0.4)
    return result


def fetch_top_fund_holdings(fund_codes: list[str]) -> dict[str, list[dict]]:
    """获取基金前5大重仓股 (最新季度)"""
    result = {}
    for code in fund_codes:
        try:
            df = ak.fund_portfolio_hold_em(symbol=code, date="2025")
            if df is not None and not df.empty:
                latest_q = df["季度"].iloc[0]
                qdf = df[df["季度"] == latest_q].head(5)
                holdings = []
                for _, row in qdf.iterrows():
                    holdings.append({
                        "stock_code": str(row.get("股票代码", "")),
                        "stock_name": str(row.get("股票名称", "")),
                        "weight": str(row.get("占净值比例", "")),
                    })
                result[code] = holdings
        except Exception:
            pass
        time.sleep(0.3)
    return result


def fetch_star_managers(top_n: int = 5) -> list[dict]:
    """拉取五星基金经理榜单 (从业时间长+回报高)"""
    try:
        df = ak.fund_manager_em()
        if df is None or df.empty:
            return []
        df = df.drop_duplicates(subset=["姓名"])
        df = df[df["现任基金最佳回报"].apply(lambda x: _to_float(x) or 0) > 50]
        df = df.sort_values("现任基金最佳回报", ascending=False)
        managers = []
        for _, row in df.head(top_n).iterrows():
            managers.append({
                "name": str(row.get("姓名", "")),
                "company": str(row.get("所属公司", "")),
                "experience_days": int(row.get("累计从业时间", 0)),
                "best_return": _to_float(row.get("现任基金最佳回报")),
            })
        return managers
    except Exception:
        return []


# --- 报告生成 ---

def build_report(date_str: str, rankings: dict, sector_data: dict,
                  top_losers: list[dict], manager_info: dict,
                  holdings: dict, star_managers: list[dict]) -> str:
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
        f"> 自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M')} · 数据源: akshare/东方财富",
        "",
    ]

    # --- 各类型涨幅 TOP 10 ---
    for type_name, funds in rankings.items():
        if not funds:
            continue
        lines += [
            f"## {type_name}基金 涨幅 TOP 10",
            "",
            "| 代码 | 名称 | 净值 | 日涨幅 | 近1周 | 近1月 | 近3月 | 近6月 | 近1年 | 今年来 | 手续费 |",
            "|------|------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|",
        ]
        for f in funds:
            lines.append(
                f"| {f['code']} | {f['name']} | {price(f['nav'])} | "
                f"{pct(f['change_daily'])} | {pct(f['change_weekly'])} | "
                f"{pct(f['change_monthly'])} | {pct(f['change_3month'])} | "
                f"{pct(f['change_6month'])} | {pct(f['change_1year'])} | "
                f"{pct(f['change_ytd'])} | {f.get('fee', '—')} |"
            )
        lines.append("")

    # --- 热门板块基金 ---
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

    # --- 涨幅第一基金经理信息 ---
    if manager_info:
        lines += ["## 涨幅第一基金经理信息", ""]
        lines += ["| 基金代码 | 基金名称 | 基金经理 | 基金公司 | 最新规模 | 成立时间 |"]
        lines += ["|------|------|------|------|------|------|"]
        for code, info in manager_info.items():
            lines.append(
                f"| {code} | {info.get('name', '—')} | {info.get('manager', '—')} | "
                f"{info.get('company', '—')} | {info.get('scale', '—')} | "
                f"{info.get('inception', '—')} |"
            )
        lines.append("")

    # --- 涨幅第一重仓股 ---
    if holdings:
        lines += ["## 涨幅第一基金前5大重仓股", ""]
        for code, stocks in holdings.items():
            fund_name = manager_info.get(code, {}).get("name", code)
            lines += [f"### {code} {fund_name}", ""]
            lines += ["| 股票代码 | 股票名称 | 占净值比例 |"]
            lines += ["|------|------|------|"]
            for s in stocks:
                lines.append(f"| {s['stock_code']} | {s['stock_name']} | {s['weight']} |")
            lines.append("")

    # --- 五星基金经理 ---
    if star_managers:
        lines += ["## 五星基金经理 TOP 5", ""]
        lines += ["| 姓名 | 所属公司 | 从业天数 | 最佳回报 |"]
        lines += ["|------|------|------|------|"]
        for m in star_managers:
            lines.append(
                f"| {m['name']} | {m['company']} | {m['experience_days']}天 | "
                f"{pct(m['best_return'])} |"
            )
        lines.append("")

    # --- 跌幅 TOP 5 ---
    lines += [
        "## 跌幅 TOP 5 (股票型+混合型)",
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
    start = time.time()
    date_str = datetime.now().strftime("%Y-%m-%d")
    print(f"公募基金监控 · {date_str}")

    # 1. 排名数据 + 收集中涨幅第一代码
    rankings = {}
    top_codes = []
    for type_name in FUND_TYPES:
        print(f"  拉取{type_name}基金排行...")
        funds = fetch_rankings(type_name, top_n=10)
        rankings[type_name] = funds
        if funds:
            print(f"    → {len(funds)} 条 (涨幅第1: {funds[0]['name']} {pct(funds[0]['change_daily'])})")
            top_codes.append(funds[0]["code"])

    # 2. 热门板块估值
    sector_data = fetch_sector_data()

    # 3. 跌幅 TOP 5
    losers_gp = fetch_rankings("股票型", top_n=50)
    losers_hh = fetch_rankings("混合型", top_n=50)
    all_losers = losers_gp + losers_hh
    all_losers.sort(key=lambda x: x.get("change_daily") or -999)
    top_losers = all_losers[:5]

    # 4. 基金经理信息 (各类型涨幅第1)
    uniq_top = list(dict.fromkeys(top_codes))[:6]  # 去重, 最多6只
    print(f"\n  拉取 {len(uniq_top)} 只涨幅第一基金的经理信息...")
    manager_info = fetch_fund_manager_info(uniq_top)

    # 5. 重仓股 (前3只涨幅第一基金)
    top3 = uniq_top[:3]
    print(f"  拉取前3只基金的持仓...")
    holdings = fetch_top_fund_holdings(top3)

    # 6. 五星基金经理
    print("  拉取五星基金经理...")
    star_managers = fetch_star_managers()

    # 7. 生成报告
    md = build_report(date_str, rankings, sector_data, top_losers,
                      manager_info, holdings, star_managers)
    md_path = DATA_DIR / f"{date_str}.md"
    md_path.write_text(md, encoding="utf-8")
    print(f"\n  → {md_path}")

    json_path = DATA_DIR / f"{date_str}.json"
    json_path.write_text(
        json.dumps({
            "date": date_str,
            "generated_at": datetime.now().isoformat(),
            "source": "akshare",
            "rankings": rankings,
            "sectors": {
                k: [{sk: sv for sk, sv in f.items()} for f in v]
                for k, v in sector_data.items()
            },
            "top_losers": top_losers,
            "manager_info": manager_info,
            "holdings": {k: v for k, v in holdings.items()},
            "star_managers": star_managers,
        }, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"  → {json_path}")

    elapsed = time.time() - start
    print(f"\n各类型涨幅第一:")
    for type_name, funds in rankings.items():
        if funds:
            f = funds[0]
            print(f"  {type_name:5s}  {f['code']}  {f['name'][:20]:20s}  {pct(f['change_daily'])}")
    print(f"\n总耗时: {elapsed:.1f}s")


if __name__ == "__main__":
    main()