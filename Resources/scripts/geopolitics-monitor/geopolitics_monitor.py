#!/usr/bin/env python3
# 数据源: Tavily Search API (主) + Google News RSS (fallback) + web_fetch (详情)
# 运行:   cd obsidian-notes && source .venv/bin/activate && python Resources/scripts/geopolitics-monitor/geopolitics_monitor.py
"""
全球地缘冲突监控脚本
每日自动收集地缘政治冲突动态，分析对金融市场的影响

输出: 5.Finance/DailyData/geopolitics/ → YYYY-MM-DD.md + .json
"""

import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from collections import Counter

import requests

SCRIPT_DIR = Path(__file__).resolve().parent
VAULT_ROOT = SCRIPT_DIR.parent.parent.parent
DATA_DIR = VAULT_ROOT / "5.Finance" / "DailyData" / "geopolitics"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# ─── Tavily API Config ───────────────────────────────────────
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY", "")
TAVILY_URL = "https://api.tavily.com/search"
PROXY = os.environ.get("https_proxy", "http://127.0.0.1:7890")
PROXIES = {"http": PROXY, "https": PROXY}

# LLM summarization (optional — falls back to rule-based)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
LLM_MODEL = os.environ.get("LLM_MODEL", "gpt-4o-mini")  # OpenAI-compatible

# Tavily Extract API
TAVILY_EXTRACT_URL = "https://api.tavily.com/extract"
MAX_ENRICH_ARTICLES = 20  # enrich top N articles with full content + summary
CONTENT_MAX_CHARS = 1500
SUMMARY_MAX_CHARS_CN = 50
SUMMARY_MAX_WORDS_EN = 30

# ─── 监控区域 ────────────────────────────────────────────────
REGION_QUERIES = {
    "美伊冲突": "Iran nuclear deal OR US Iran sanctions OR Strait of Hormuz oil OR Israel Iran conflict",
    "俄乌战争": "Russia Ukraine war OR Ukraine counteroffensive OR Russia sanctions energy OR Black Sea grain",
    "中美博弈": "US China tariffs OR US China trade war OR semiconductor export controls OR China entity list sanctions",
    "中东/红海": "Red Sea Houthi shipping attacks OR Gaza ceasefire OR Hezbollah Israel OR Suez Canal disruption",
    "台海/南海/朝鲜": "Taiwan China military drills OR South China Sea dispute OR North Korea missile test OR PLA Taiwan",
    "全球制裁": "G7 sanctions OR SWIFT sanctions OR OFAC sanctions OR EU sanctions OR global trade restrictions",
}

# ─── 事件类型 → 关键词匹配 ──────────────────────────────────
EVENT_TYPE_KEYWORDS = [
    ("原油供应风险", [
        "oil supply", "crude oil", "OPEC", "oil price", "oil production",
        "supply disruption", "refinery", "oil field", "pipeline",
        "Hormuz", "Persian Gulf", "oil tanker", "oil embargo",
        "石油供应", "原油", "油田", "炼厂", "霍尔木兹", "波斯湾",
    ]),
    ("军事冲突升级", [
        "missile strike", "airstrike", "bombing", "invasion", "offensive",
        "ground forces", "drone attack", "fighter jet", "warship",
        "war", "military operation", "troops", "artillery",
        "导弹袭击", "空袭", "地面进攻", "入侵", "坦克", "无人机攻击",
        "军演", "军事行动", "舰队", "战机",
    ]),
    ("避险需求", [
        "safe haven", "flight to safety", "risk aversion", "market panic",
        "sell-off", "capital flight", "gold surge", "yen strengthen",
        "investor fear", "uncertainty spikes",
        "避险", "恐慌", "资本外逃", "黄金上涨", "市场暴跌",
    ]),
    ("航运中断", [
        "Red Sea", "Houthi", "shipping attack", "cargo vessel",
        "container ship", "freight rate surge", "Suez Canal",
        "blockade", "naval route", "Bab el-Mandeb", "reroute",
        "红海", "胡塞", "货船遇袭", "苏伊士", "绕行",
        "运费飙升", "航运中断", "封锁",
    ]),
    ("中美关税", [
        "tariff", "trade war", "US China trade", "export control",
        "chip ban", "entity list", "Section 301", "USTR",
        "semiconductor restriction", "decouple", "de-risk",
        "关税", "贸易战", "芯片禁令", "实体清单", "断链",
        "出口管制", "301条款",
    ]),
    ("粮食供应", [
        "grain", "wheat", "corn", "soybean", "food crisis",
        "Black Sea grain deal", "food export ban", "famine",
        "粮食", "小麦", "玉米", "大豆", "粮食协议", "粮食危机",
    ]),
    ("汇率波动", [
        "exchange rate", "dollar surge", "yen depreciation",
        "yuan devaluation", "forex shock", "currency crisis",
        "central bank intervention",
        "汇率", "美元走强", "日元贬值", "人民币贬值", "卢布",
    ]),
    ("供应链中断", [
        "supply chain", "chip shortage", "semiconductor",
        "TSMC", "NVIDIA", "wafer", "rare earth",
        "供应链", "芯片短缺", "半导体", "稀土", "台积电",
    ]),
    ("军工受益", [
        "defense spending", "military aid", "arms deal", "weapons package",
        "defense budget", "military procurement", "NATO spending",
        "军援", "军费", "武器采购", "国防预算", "军售",
    ]),
]

# ─── 事件 → 市场标的映射 ─────────────────────────────────────
IMPACT_ASSET_MAP = {
    "原油供应风险": {
        "impact": "原油供应中断风险 → 油价上涨, 能源板块受益",
        "tickers": ["CL=F", "BZ=F"],
        "etf": ["USO", "XLE", "BNO"],
        "chinese": "WTI原油(CL=F) / 布油(BZ=F) / 能源ETF(XLE)",
    },
    "军事冲突升级": {
        "impact": "军事冲突升级 → 避险资产上涨, 军工股受益",
        "tickers": ["GC=F", "SI=F", "LMT", "NOC", "RTX", "GD"],
        "etf": ["GLD", "SLV", "ITA", "PPA"],
        "chinese": "黄金(GC=F) / 军工ETF(ITA) / 洛克希德(LMT) / 雷神(RTX)",
    },
    "避险需求": {
        "impact": "市场风险偏好下降 → 资金涌入避险资产",
        "tickers": ["GC=F", "GLD", "SI=F", "^VIX", "DX-Y.NYB"],
        "etf": ["GLD", "IAU", "TLT", "UVXY"],
        "chinese": "黄金(GLD) / VIX(^VIX) / 美债(TLT) / 美元指数(DX-Y.NYB)",
    },
    "航运中断": {
        "impact": "航运成本飙升 → 航运股波动, 供应链成本上升",
        "tickers": ["ZIM", "MATX"],
        "etf": ["BOAT", "SEA"],
        "chinese": "以星航运(ZIM) / 航运ETF(BOAT) / BDI指数",
    },
    "中美关税": {
        "impact": "中美关系紧张 → 中概股承压, 供应链转移受益国受益",
        "tickers": ["FXI", "ASHR", "KWEB", "YINN", "MCHI", "0700.HK", "9988.HK"],
        "etf": ["FXI", "KWEB", "CQQQ"],
        "chinese": "富时中国(FXI) / 沪深300(ASHR) / 中国互联网(KWEB) / 腾讯(0700.HK)",
    },
    "粮食供应": {
        "impact": "粮食供应链中断 → 农产品期货上涨",
        "tickers": ["ZW=F", "ZC=F", "ZS=F"],
        "etf": ["DBA", "WEAT", "CORN"],
        "chinese": "小麦(ZW=F) / 玉米(ZC=F) / 大豆(ZS=F) / 农业ETF(DBA)",
    },
    "汇率波动": {
        "impact": "主要货币汇率剧烈波动 → 外汇和跨国企业受影响",
        "tickers": ["DX-Y.NYB", "FXY", "FXE"],
        "chinese": "美元指数(DX-Y.NYB) / 日元ETF(FXY) / 欧元ETF(FXE)",
    },
    "供应链中断": {
        "impact": "半导体/制造供应链中断 → 芯片股和制造业波动",
        "tickers": ["NVDA", "TSM", "INTC", "AMD", "ASML"],
        "etf": ["SMH", "SOXX"],
        "chinese": "英伟达(NVDA) / 台积电(TSM) / 半导体ETF(SMH)",
    },
    "军工受益": {
        "impact": "国防支出增加 → 军工板块估值提升",
        "tickers": ["LMT", "NOC", "RTX", "GD", "LHX"],
        "etf": ["ITA", "PPA", "XAR"],
        "chinese": "军工ETF(ITA) / 洛克希德(LMT) / 诺斯罗普(NOC)",
    },
}

# ─── 严重程度判定 ───────────────────────────────────────────
SEVERITY_LEVELS = [
    ("critical", [
        "declare war", "nuclear", "full-scale invasion", "regime collapse",
        "strait blockade", "oil embargo", "decapitation strike",
        "宣战", "核", "全面入侵", "政权崩溃", "海峡封锁", "石油禁运",
    ]),
    ("high", [
        "missile launch", "military drill near border", "sanctions escalation",
        "tariff hike", "shot down", "ground offensive", "naval standoff",
        "terrorist attack", "coup attempt",
        "导弹发射", "军演", "制裁升级", "关税大幅上调", "边境冲突", "政变",
    ]),
    ("medium", [
        "talks collapse", "diplomatic expulsion", "sanctions warning",
        "tariff threat", "reconnaissance", "incursion",
        "谈判破裂", "外交驱逐", "制裁警告", "关税威胁",
    ]),
    ("low", [
        "dialogue", "negotiations", "ceasefire", "de-escalation",
        "peace talks", "diplomatic visit", "summit",
        "对话", "谈判", "停火", "缓和", "和平", "外交访问", "峰会",
    ]),
]

SEVERITY_EMOJI = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}


def clean_html(text: str) -> str:
    """移除 HTML 标签"""
    return re.sub(r"<[^>]+>", "", text)


def classify_severity(text: str) -> str:
    """判定事件严重程度"""
    text_lower = text.lower()
    for level, keywords in SEVERITY_LEVELS:
        for kw in keywords:
            if kw.lower() in text_lower:
                return level
    return "medium"


def classify_event_types(text: str) -> list[str]:
    """根据文本内容识别事件类型"""
    matched = []
    text_lower = text.lower()
    for etype, keywords in EVENT_TYPE_KEYWORDS:
        score = sum(1 for kw in keywords if kw.lower() in text_lower)
        if score >= 1:
            matched.append(etype)
    return matched[:3] if matched else ["避险需求"]


def classify_region(text: str) -> list[str]:
    """根据文本匹配区域"""
    matched = []
    text_lower = text.lower()
    for region, keywords in {
        "美伊冲突": ["iran", "israel", "hormuz", "persian gulf", "nuclear deal", "irgc"],
        "俄乌战争": ["ukraine", "russia", "putin", "zelensky", "crimea", "donbas", "nato"],
        "中美博弈": ["tariff", "trade war", "export control", "chip ban", "entity list", "semiconductor", "ustr", "china", "beijing"],
        "中东/红海": ["red sea", "houthi", "gaza", "hezbollah", "suez", "hamas", "yemen", "lebanon"],
        "台海/南海/朝鲜": ["taiwan", "south china sea", "north korea", "pla", "missile", "kim jong", "philippines"],
        "全球制裁": ["sanctions", "swift", "ofac", "g7", "eu sanctions"],
    }.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        if score >= 1:
            matched.append(region)
    return matched if matched else ["其他重大事件"]


def search_tavily(query: str, max_results: int = 8) -> list[dict]:
    """Tavily Search API (topic=news, time_range=day)"""
    if not TAVILY_API_KEY:
        return []

    try:
        resp = requests.post(
            TAVILY_URL,
            json={
                "api_key": TAVILY_API_KEY,
                "query": query,
                "search_depth": "advanced",
                "topic": "news",
                "days": 1,
                "max_results": max_results,
                "include_answer": False,
                "include_raw_content": False,
                "include_images": False,
            },
            timeout=30,
            proxies=PROXIES,
        )
        resp.raise_for_status()
        data = resp.json()
        return data.get("results", [])
    except (requests.RequestException, ValueError, KeyError) as e:
        print(f"    [WARN] Tavily 搜索失败: {e}")
        return []


def search_google_news(query: str, max_results: int = 8) -> list[dict]:
    """Google News RSS fallback (免费, 无需 API Key)"""
    encoded = query.replace(" ", "+")
    url = f"https://news.google.com/rss/search?q={encoded}&hl=en-US&gl=US&ceid=US:en"
    results = []
    try:
        resp = requests.get(url, timeout=15, proxies=PROXIES)
        if resp.status_code != 200:
            return []
        root = ET.fromstring(resp.text)
        items = root.findall(".//item")[:max_results]
        for item in items:
            title = item.findtext("title", "")
            link = item.findtext("link", "")
            pub_date = item.findtext("pubDate", "")
            desc = item.findtext("description", "")
            results.append({
                "title": clean_html(title),
                "url": link,
                "content": clean_html(desc),
                "published_date": pub_date,
            })
    except (requests.RequestException, ET.ParseError) as e:
        print(f"    [WARN] Google News 搜索失败: {e}")

    return results


def extract_urls_batch(urls: list[str]) -> dict[str, str]:
    """Tavily Extract API — batch fetch clean article content. Returns {url: raw_content}."""
    if not TAVILY_API_KEY or not urls:
        return {}

    content_map = {}
    # Tavily extract supports up to 20 URLs per call
    batch_size = 20
    for i in range(0, len(urls), batch_size):
        batch = urls[i : i + batch_size]
        try:
            resp = requests.post(
                TAVILY_EXTRACT_URL,
                json={
                    "api_key": TAVILY_API_KEY,
                    "urls": batch,
                    "include_images": False,
                    "extract_depth": "basic",
                },
                timeout=15,
                proxies=PROXIES,
            )
            resp.raise_for_status()
            data = resp.json()
            for r in data.get("results", []):
                content_map[r["url"]] = r.get("raw_content", "")[:CONTENT_MAX_CHARS]
            # Log failed URLs
            for f in data.get("failed_results", []):
                print(f"    [WARN] Tavily extract failed: {f['url'][:60]} — {f.get('error', 'unknown')}")
        except (requests.RequestException, ValueError, KeyError) as e:
            print(f"    [WARN] Tavily Extract API 失败: {e}")
            # Fallback: try individual URLs with raw requests
            for url in batch:
                raw = _extract_single_fallback(url)
                if raw:
                    content_map[url] = raw
    return content_map


def _extract_single_fallback(url: str) -> str | None:
    """Fallback: raw HTTP fetch + simple regex extraction."""
    try:
        resp = requests.get(
            url, timeout=15, proxies=PROXIES,
            headers={"User-Agent": "Mozilla/5.0 (compatible; GeopoliticsMonitor/2.0)"},
        )
        if resp.status_code != 200:
            return None
        text = re.sub(r"<script[^>]*>.*?</script>", "", resp.text, flags=re.DOTALL)
        text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL)
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text[:CONTENT_MAX_CHARS] if text else None
    except (requests.RequestException, OSError):
        return None


def summarize_with_llm(text: str, title: str) -> str | None:
    """LLM summarization via OpenAI-compatible API. Returns None if unavailable/fails."""
    if not OPENAI_API_KEY:
        return None

    prompt = (
        f"Summarize this news in ONE sentence.\n"
        f"- For Chinese: under {SUMMARY_MAX_CHARS_CN} characters\n"
        f"- For English: under {SUMMARY_MAX_WORDS_EN} words\n"
        f"- Only return the summary, no quotes, no extra text\n\n"
        f"Title: {title}\nContent: {text[:CONTENT_MAX_CHARS]}"
    )
    try:
        resp = requests.post(
            "https://api.openai.com/v1/chat/completions",
            json={
                "model": LLM_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 80,
                "temperature": 0.3,
            },
            headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
            timeout=15,
            proxies=PROXIES,
        )
        if resp.status_code == 200:
            result = resp.json()["choices"][0]["message"]["content"].strip().strip('"')
            return _trim_summary(result)
    except Exception:
        pass
    return None


def _trim_summary(text: str) -> str:
    """Ensure summary stays within length limits."""
    has_cjk = bool(re.search(r'[一-鿿]', text))
    if has_cjk:
        return text[:SUMMARY_MAX_CHARS_CN]
    else:
        words = text.split()
        if len(words) <= SUMMARY_MAX_WORDS_EN:
            return text
        return ' '.join(words[:SUMMARY_MAX_WORDS_EN])


def generate_summary(text: str, title: str) -> str:
    """Generate a one-sentence summary. LLM first, fallback to rule-based."""
    if not text:
        return title[:SUMMARY_MAX_CHARS_CN]

    # Try LLM first
    llm_result = summarize_with_llm(text, title)
    if llm_result:
        return llm_result

    # Rule-based: extract first meaningful sentence
    sentences = re.split(r'(?<=[.!?。！？\n])\s*', text.strip())
    for s in sentences:
        s = s.strip()
        # Skip boilerplate, short fragments, navigation text
        if len(s) < 15:
            continue
        skip_prefixes = (
            "Share", "Cookie", "Subscribe", "©", "Skip to",
            "Please enable", "This website", "We use",
            "Advertisement", "Ad", "Sign in", "Log in",
            "By clicking", "You can also", "Read more",
        )
        if s.startswith(skip_prefixes):
            continue
        return _trim_summary(s)

    return title[:SUMMARY_MAX_CHARS_CN]


def enrich_articles(articles: list[dict], top_n: int = MAX_ENRICH_ARTICLES) -> None:
    """Enrich articles: fetch full content + generate summary for top N or MEDIUM+ articles."""
    # Select articles to enrich: MEDIUM+ first, then by position, capped at top_n
    target = []
    rest = []
    for a in articles:
        if a.get("severity") in ("critical", "high", "medium"):
            target.append(a)
        else:
            rest.append(a)
    # Fill up to top_n with remaining articles
    target.extend(rest[: max(0, top_n - len(target))])
    target = target[:top_n]

    if not target:
        return

    # Collect URLs
    url_list = [a.get("url", "") for a in target if a.get("url")]
    print(f"    提取 {len(url_list)} 条新闻正文 (Tavily Extract)...")

    # Batch extract
    content_map = extract_urls_batch(url_list)

    # Enrich each article
    enriched = 0
    for a in target:
        url = a.get("url", "")
        content = content_map.get(url, "")
        if content:
            a["content_detail"] = content
            enriched += 1
        # Generate summary from available text
        text_for_summary = content or a.get("content", "")
        a["summary"] = generate_summary(text_for_summary, a.get("title", ""))
        if text_for_summary:
            enriched += 1

    print(f"    正文提取: {enriched} 条 / 摘要生成完成")

    # Fetch individual fallback for URLs that Tavily extract missed
    missed = [a for a in target if not a.get("content_detail") and a.get("url")]
    if missed:
        print(f"    回退抓取 {len(missed)} 条缺失正文...")
        for a in missed:
            url = a.get("url", "")
            print(f"      → {a['title'][:60]}...")
            raw = _extract_single_fallback(url)
            if raw:
                a["content_detail"] = raw
                if not a.get("summary") or a["summary"] == a["title"][:SUMMARY_MAX_CHARS_CN]:
                    a["summary"] = generate_summary(raw, a.get("title", ""))


def deduplicate_articles(articles: list[dict]) -> list[dict]:
    """按标题前缀去重"""
    seen = set()
    unique = []
    for a in articles:
        key = a["title"][:70].lower().strip()
        if key not in seen:
            seen.add(key)
            unique.append(a)
    return unique


def get_impact_assets(event_types: list[str]) -> list[dict]:
    """根据事件类型返回受影响标的"""
    assets = []
    seen = set()
    for etype in event_types:
        impact = IMPACT_ASSET_MAP.get(etype)
        if not impact:
            continue
        for t in impact.get("tickers", []):
            if t not in seen:
                seen.add(t)
                assets.append({"ticker": t, "type": etype})
        for t in impact.get("etf", []):
            if t not in seen:
                seen.add(t)
                assets.append({"ticker": t, "type": etype})
    return assets


# ═══════════════════════════════════════════════════════════════
#  报告生成
# ═══════════════════════════════════════════════════════════════

def generate_report(articles: list[dict], date_str: str) -> str:
    """生成 Obsidian markdown 报告"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    sorted_articles = sorted(articles, key=lambda a: severity_order.get(a["severity"], 3))

    # ── 统计数据 ──
    sev_counter = Counter(a["severity"] for a in articles)
    region_counter = Counter()
    for a in articles:
        for r in a["classified_regions"]:
            region_counter[r] += 1

    lines = [
        "---",
        f"title: 全球地缘冲突日报 {date_str}",
        "type: summary",
        f"created: {date_str}",
        "tags: [地缘政治, 冲突监控, 市场影响, 日报]",
        "---",
        "",
        f"# 全球地缘冲突日报 {date_str}",
        "",
        f"> 自动生成于 {now} · 数据源 Tavily Search / Google News",
        "",
    ]

    # ── 概览仪表板 ──
    lines += [
        "## 事件概览",
        "",
        "| 严重程度 | 数量 | 说明 |",
        "|:---|:---:|:---|",
    ]
    for level in ["critical", "high", "medium", "low"]:
        cnt = sev_counter.get(level, 0)
        emoji = SEVERITY_EMOJI.get(level, "")
        desc = {
            "critical": "需立即关注，可能引发市场剧烈波动",
            "high": "密切关注，可能影响市场情绪",
            "medium": "常规跟踪",
            "low": "缓解信号，利空出尽",
        }.get(level, "")
        lines.append(f"| {emoji} {level.upper()} | {cnt} | {desc} |")

    lines += [
        "",
        "| 区域 | 事件数 |",
        "|:---|:---:|",
    ]
    for region, cnt in region_counter.most_common():
        lines.append(f"| {region} | {cnt} |")

    # ── 重点事件详情 ──
    lines += [
        "",
        "## 重点事件与市场影响",
        "",
        "| # | 事件 | 区域 | 严重程度 | 事件类型 | 关键信息 | 关注标的 |",
        "|:---:|:---|:---|:---:|:---|:---|:---|",
    ]

    for i, a in enumerate(sorted_articles[:25], 1):
        title = a["title"][:80]
        url = a.get("url", "")
        regions = ", ".join(a["classified_regions"][:2])
        sev = a["severity"]
        sev_emoji = SEVERITY_EMOJI.get(sev, "")
        types_str = ", ".join(a["event_types"][:2])
        assets = get_impact_assets(a["event_types"])
        ticker_str = " ".join(f"`{t['ticker']}`" for t in assets[:4]) if assets else "—"

        title_md = f"[{title}]({url})" if url else title
        summary = a.get("summary", "") or ""
        lines.append(
            f"| {i} | {title_md} | {regions} | {sev_emoji} {sev} | {types_str} | {summary} | {ticker_str} |"
        )

    # ── 影响标的汇总表 ──
    lines += [
        "",
        "## 市场影响映射",
        "",
        "| 事件类型 | 影响逻辑 | 关注标的 |",
        "|:---|:---|:---|",
    ]

    all_types = set()
    for a in sorted_articles:
        for t in a["event_types"]:
            all_types.add(t)

    for etype in sorted(all_types):
        impact = IMPACT_ASSET_MAP.get(etype)
        if not impact:
            continue
        lines.append(
            f"| {etype} | {impact['impact']} | {impact['chinese']} |"
        )

    # ── 严重事件详情 ──
    critical_articles = [a for a in sorted_articles if a["severity"] in ("critical", "high")][:5]
    if critical_articles:
        lines += [
            "",
            "## ⚠️ 严重事件速报",
            "",
        ]
        for a in critical_articles:
            sev_emoji = SEVERITY_EMOJI.get(a["severity"], "")
            lines += [f"### {sev_emoji} {a['title']}", ""]
            if a.get("content_detail"):
                lines.append(f"> {a['content_detail'][:400]}")
            elif a.get("content"):
                lines.append(f"> {a['content'][:400]}")
            lines.append(f"📎 [{a.get('url', '#')}]({a.get('url', '#')})")
            lines.append("")

    # ── 投资启示 ──
    lines += [
        "## 投资启示",
        "",
    ]

    if sev_counter.get("critical", 0) > 0:
        lines.append("- 🔴 **警报**: 存在重大地缘事件，建议增加避险资产配置(黄金GLD、美债TLT)")
    if sev_counter.get("high", 0) >= 3:
        lines.append("- 🟠 **警惕**: 多重地缘风险叠加，减少新兴市场敞口，增加现金/黄金比例")
    if "中美博弈" in region_counter:
        lines.append("- 💼 **中美博弈**: 关注中概股波动(ASHR/KWEB)，国产替代/半导体自主可控受政策催化")
    if "俄乌战争" in region_counter:
        lines.append("- ⚡ **能源粮食**: 俄乌冲突持续扰动能源和粮食供应链，原油(CL=F)、小麦(ZW=F)保持关注")
    if "中东/红海" in region_counter:
        lines.append("- 🚢 **航运风险**: 红海安全影响亚欧航线，航运成本持续高位(ZIM/BOAT)")
    if "台海/南海/朝鲜" in region_counter:
        lines.append("- 🏝 **亚太紧张**: 台海/南海局势影响亚太市场情绪，关注台积电(TSM)、军工(ITA)")
    if "美伊冲突" in region_counter:
        lines.append("- 🛢 **中东风险**: 美伊关系紧张推升油价预期，能源ETF(XLE/USO)波动加大")

    lines += [
        "",
        "---",
        "",
        f"> 📊 共覆盖 {len(region_counter)} 个区域 · {len(articles)} 条事件",
        f"> 🕐 更新时间: {now}",
        "> 🤖 自动生成 · 不构成投资建议 · 仅供参考",
    ]

    return "\n".join(lines)


def build_json(articles: list[dict], date_str: str) -> dict:
    """构建 JSON 原始数据"""
    events = []
    for a in articles:
        assets = get_impact_assets(a["event_types"])
        events.append({
            "title": a["title"],
            "url": a.get("url", ""),
            "content": a.get("content", "")[:300],
            "content_detail": a.get("content_detail", ""),
            "published_date": a.get("published_date", ""),
            "search_region": a["search_region"],
            "classified_regions": a["classified_regions"],
            "event_types": a["event_types"],
            "severity": a["severity"],
            "affected_tickers": [t["ticker"] for t in assets],
        })

    return {
        "date": date_str,
        "generated_at": datetime.now().isoformat(),
        "total_events": len(events),
        "severity_distribution": dict(Counter(e["severity"] for e in events)),
        "events": events,
    }


# ═══════════════════════════════════════════════════════════════

def main():
    date_str = datetime.now().strftime("%Y-%m-%d")
    print(f"全球地缘冲突监控 · {date_str}")

    if TAVILY_API_KEY:
        print(f"  数据源: Tavily Search API")
    else:
        print(f"  [INFO] TAVILY_API_KEY 未设置，使用 Google News RSS")
        print(f"  获取 Key: https://tavily.com → export TAVILY_API_KEY=tvly-xxx")

    # 1. 抓取新闻
    print(f"  搜索 {len(REGION_QUERIES)} 个区域...")
    articles = fetch_all_articles()

    if not articles:
        print("[ERROR] 未抓取到新闻，请检查网络/代理")
        (DATA_DIR / f"{date_str}.md").write_text(
            f"# 全球地缘冲突日报 {date_str}\n\n> 当日无数据\n\n请检查网络代理或 TAVILY_API_KEY", encoding="utf-8")
        sys.exit(1)

    unique = deduplicate_articles(articles)
    print(f"  去重: {len(articles)} → {len(unique)} 条")

    # 2. 抓取严重事件详情
    critical_count = sum(1 for a in unique if a["severity"] in ("critical", "high"))
    if critical_count > 0:
        print(f"  抓取 {critical_count} 条严重事件详情...")
        fetch_critical_details(unique)

    # 3. 生成报告
    md = generate_report(unique, date_str)
    md_path = DATA_DIR / f"{date_str}.md"
    md_path.write_text(md, encoding="utf-8")
    print(f"  → {md_path}")

    # 4. 生成 JSON
    json_data = build_json(unique, date_str)
    json_path = DATA_DIR / f"{date_str}.json"
    json_path.write_text(json.dumps(json_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  → {json_path}")

    # 5. 控制台摘要
    sev_counter = Counter(a["severity"] for a in unique)
    print("\n  严重程度分布:")
    for level in ["critical", "high", "medium", "low"]:
        cnt = sev_counter.get(level, 0)
        emoji = SEVERITY_EMOJI.get(level, "")
        if cnt > 0:
            print(f"    {emoji} {level.upper()}: {cnt}")

    region_counter = Counter()
    for a in unique:
        for r in a["classified_regions"]:
            region_counter[r] += 1
    print("\n  区域分布:")
    for region, cnt in region_counter.most_common():
        print(f"    {region}: {cnt}")


if __name__ == "__main__":
    main()