#!/usr/bin/env python3
# 数据源: Tavily Search API (主) + Google News RSS (fallback) + web_fetch (详情)
# 运行:   cd obsidian-notes && source .venv/bin/activate && python Resources/scripts/geopolitics-monitor/geopolitics_monitor.py
"""
全球地缘冲突监控脚本
每日自动收集地缘政治冲突动态，分析对金融市场的影响

输出: 5.Finance/DailyData/geopolitics/ → YYYY-MM-DD.md + .json
"""

import html
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
CLAUDE_MODEL = os.environ.get("CLAUDE_MODEL", "claude-3-5-haiku-20241022")

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

# ─── LLM 分类可用的事件类型和区域 ─────────────────────────────
VALID_EVENT_TYPES = [
    "原油供应风险", "军事冲突升级", "避险需求", "航运中断",
    "中美关税", "粮食供应", "汇率波动", "供应链中断", "军工受益",
]
VALID_REGIONS = list(REGION_QUERIES.keys())
VALID_SEVERITIES = ["critical", "high", "medium", "low"]

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

SEVERITY_EMOJI = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}


def clean_html(text: str) -> str:
    """移除 HTML 标签和实体"""
    text = html.unescape(text)
    return re.sub(r"<[^>]+>", "", text)


def classify_articles_batch(articles: list[dict]) -> None:
    """用 LLM 批量分类文章的事件类型、严重程度和区域归属."""
    to_classify = [
        (i, a) for i, a in enumerate(articles)
        if not a.get("_classified")
    ]
    if not to_classify:
        return

    event_types_str = ", ".join(VALID_EVENT_TYPES)
    regions_str = ", ".join(VALID_REGIONS)
    batch_size = 10
    classified = 0

    for start in range(0, len(to_classify), batch_size):
        batch = to_classify[start : start + batch_size]
        items = "\n".join(
            f'{idx}. [{a["title"][:100]}] {a.get("content", "")[:200]}'
            for idx, a in batch
        )
        prompt = (
            "你是地缘政治分析师。对以下新闻逐条分类，返回 JSON 数组。\n\n"
            f"可用事件类型(1-3个): {event_types_str}\n"
            f"可用区域(1-3个): {regions_str}\n"
            "严重程度: critical(战争/核/封锁), high(军事行动/制裁升级), "
            "medium(外交摩擦/威胁), low(谈判/缓和)\n\n"
            "输出格式(只输出 JSON 数组，不要其他文字):\n"
            '[{"id":0,"event_types":["军事冲突升级"],'
            '"severity":"high","regions":["俄乌战争"]}]\n\n'
            f"新闻列表:\n{items}"
        )

        result = _call_llm(prompt)
        if not result:
            for idx, a in batch:
                a["event_types"] = a.get("event_types", ["避险需求"])
                a["severity"] = a.get("severity", "medium")
                a["classified_regions"] = a.get("classified_regions",
                                                 [a.get("search_region", "其他")])
                a["_classified"] = True
            continue

        try:
            json_match = re.search(r"\[.*\]", result, re.DOTALL)
            if not json_match:
                raise ValueError("no JSON array found")
            items_data = json.loads(json_match.group())
            for item in items_data:
                idx = item.get("id")
                if idx is None:
                    continue
                for orig_idx, a in batch:
                    if orig_idx == idx:
                        a["event_types"] = [
                            t for t in item.get("event_types", [])
                            if t in VALID_EVENT_TYPES
                        ] or ["避险需求"]
                        sev = item.get("severity", "medium")
                        a["severity"] = sev if sev in VALID_SEVERITIES else "medium"
                        a["classified_regions"] = [
                            r for r in item.get("regions", [])
                            if r in VALID_REGIONS
                        ] or [a.get("search_region", "其他")]
                        a["_classified"] = True
                        classified += 1
                        break
        except (json.JSONDecodeError, ValueError) as e:
            print(f"    [WARN] LLM 分类解析失败: {e}")
            for idx, a in batch:
                if not a.get("_classified"):
                    a["event_types"] = ["避险需求"]
                    a["severity"] = "medium"
                    a["classified_regions"] = [a.get("search_region", "其他")]
                    a["_classified"] = True

    # 未被 LLM 处理到的条目兜底
    for a in articles:
        if not a.get("_classified"):
            a.setdefault("event_types", ["避险需求"])
            a.setdefault("severity", "medium")
            a.setdefault("classified_regions", [a.get("search_region", "其他")])
            a["_classified"] = True

    print(f"    LLM 分类: {classified}/{len(articles)} 条")


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
    text = html.unescape(text)  # safety net
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


def translate_titles_batch(articles: list[dict]) -> None:
    """批量翻译标题为中文，结果写入 article['title_cn'].

    使用 LLM API 翻译，失败则保留英文原文。
    """
    titles_to_translate = [
        (i, a["title"]) for i, a in enumerate(articles)
        if a.get("title") and not a.get("title_cn")
    ]
    if not titles_to_translate:
        return

    llm_translated = 0

    batch_size = 15
    for start in range(0, len(titles_to_translate), batch_size):
        batch = titles_to_translate[start : start + batch_size]
        numbered = "\n".join(f"{idx}. {title}" for idx, title in batch)
        prompt = (
            "将以下英文新闻标题翻译成简洁的中文，每行一条，保留编号。\n"
            "要求：简洁、专业、保留关键实体（人名/地名用通用译名）。\n"
            "只输出翻译结果，不要解释，不要思考过程。\n\n"
            f"{numbered}"
        )

        result_text = _call_llm(prompt)
        if not result_text:
            continue

        for line in result_text.strip().split("\n"):
            line = line.strip()
            if not line:
                continue
            match = re.match(r"(\d+)\.\s*(.+)", line)
            if match:
                idx = int(match.group(1))
                cn_title = match.group(2).strip()
                for orig_idx, _ in batch:
                    if orig_idx == idx:
                        articles[idx]["title_cn"] = cn_title
                        llm_translated += 1
                        break

    if llm_translated:
        print(f"    标题翻译: LLM {llm_translated} 条")
    untranslated = sum(1 for a in articles if not a.get("title_cn") and a.get("title"))
    if untranslated:
        print(f"    标题翻译: {untranslated} 条保留英文原文")


def _call_llm(prompt: str) -> str | None:
    """调用 LLM API.

    优先级: 内部 AI 平台(ANTHROPIC_AUTH_TOKEN) → ANTHROPIC_API_KEY → OPENAI_API_KEY.
    """
    # 内部平台（Anthropic Messages 协议）
    internal_token = os.environ.get("ANTHROPIC_AUTH_TOKEN", "")
    internal_url = os.environ.get("ANTHROPIC_BASE_URL", "")
    internal_model = os.environ.get("ANTHROPIC_MODEL", CLAUDE_MODEL)
    # 清理模型名中的上下文窗口标记（如 deepseek-v4-pro[1m] → deepseek-v4-pro）
    internal_model = re.sub(r"\[.*?\]", "", internal_model).strip()

    if internal_token and internal_url:
        api_url = f"{internal_url.rstrip('/')}/v1/messages"
        try:
            resp = requests.post(
                api_url,
                json={
                    "model": internal_model,
                    "max_tokens": 2000,
                    "messages": [{"role": "user", "content": prompt}],
                },
                headers={
                    "Authorization": f"Bearer {internal_token}",
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                timeout=120,
            )
            if resp.status_code == 200:
                data = resp.json()
                for block in data.get("content", []):
                    if block.get("type") == "text":
                        return block["text"]
                return data["content"][0].get("text", "")
            else:
                print(f"    [WARN] 内部 AI 平台 {resp.status_code}: {resp.text[:200]}")
        except Exception as e:
            print(f"    [WARN] 内部 AI 平台翻译失败: {e}")

    # Anthropic 官方 API
    if ANTHROPIC_API_KEY:
        try:
            resp = requests.post(
                "https://api.anthropic.com/v1/messages",
                json={
                    "model": CLAUDE_MODEL,
                    "max_tokens": 2000,
                    "messages": [{"role": "user", "content": prompt}],
                },
                headers={
                    "x-api-key": ANTHROPIC_API_KEY,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                timeout=30,
                proxies=PROXIES,
            )
            if resp.status_code == 200:
                data = resp.json()
                return data["content"][0]["text"]
            else:
                print(f"    [WARN] Anthropic API {resp.status_code}: {resp.text[:200]}")
        except Exception as e:
            print(f"    [WARN] Anthropic 翻译失败: {e}")

    # OpenAI 兼容 API
    if OPENAI_API_KEY:
        try:
            resp = requests.post(
                "https://api.openai.com/v1/chat/completions",
                json={
                    "model": LLM_MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 2000,
                    "temperature": 0.3,
                },
                headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
                timeout=30,
                proxies=PROXIES,
            )
            if resp.status_code == 200:
                return resp.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"    [WARN] OpenAI 翻译失败: {e}")

    return None


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
    content_done = 0
    for a in target:
        url = a.get("url", "")
        content = content_map.get(url, "")
        if content:
            a["content_detail"] = content
            content_done += 1
        # Generate summary from available text
        text_for_summary = content or a.get("content", "")
        a["summary"] = generate_summary(text_for_summary, a.get("title", ""))

    print(f"    正文提取: {content_done} 条, 摘要已生成")

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

    # 批量翻译标题为中文
    print(f"    翻译标题...")
    translate_titles_batch(articles)


def fetch_all_articles() -> list[dict]:
    """抓取所有区域新闻"""
    all_articles = []

    for region, query in REGION_QUERIES.items():
        print(f"  搜索: {region}...")

        # 优先 Tavily, 回退 Google News
        results = search_tavily(query)
        if not results:
            results = search_google_news(query)

        for r in results:
            title = r.get("title", "")
            content = r.get("content", "")
            url = r.get("url", "")

            all_articles.append({
                "title": title,
                "url": url,
                "content": content[:500] if content else "",
                "published_date": r.get("published_date", ""),
                "search_region": region,
            })

        print(f"    获取 {len(results)} 条")

    return all_articles


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
        title_cn = a.get("title_cn", "")
        title_en = a["title"][:80]
        title_display = title_cn or title_en
        url = a.get("url", "")
        regions = ", ".join(a["classified_regions"][:2])
        sev = a["severity"]
        sev_emoji = SEVERITY_EMOJI.get(sev, "")
        types_str = ", ".join(a["event_types"][:2])
        assets = get_impact_assets(a["event_types"])
        ticker_str = " ".join(f"`{t['ticker']}`" for t in assets[:4]) if assets else "—"

        title_md = f"[{title_display}]({url})" if url else title_display
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

    # ── 严重事件速报 ──
    critical_articles = [a for a in sorted_articles if a["severity"] in ("critical", "high")][:5]
    if critical_articles:
        lines += [
            "",
            "## ⚠️ 严重事件速报",
            "",
        ]
        for a in critical_articles:
            sev_emoji = SEVERITY_EMOJI.get(a["severity"], "")
            summary = a.get("summary", "")
            headline = a.get("title_cn") or a["title"]
            lines += [f"### {sev_emoji} {headline}", ""]
            if a.get("title_cn"):
                lines.append(f"*{a['title'][:100]}*")
                lines.append("")
            if summary:
                lines.append(f"> **摘要**: {summary}")
                lines.append("")
            if a.get("content_detail"):
                lines.append(f"> {a['content_detail'][:400]}")
            elif a.get("content"):
                lines.append(f"> {a['content'][:400]}")
            lines.append(f"[{a.get('url', '#')}]({a.get('url', '#')})")
            lines.append("")

    # ── 关键新闻详情 ──
    top_with_detail = [a for a in sorted_articles[:15] if a.get("content_detail") or a.get("content")][:10]
    if top_with_detail:
        lines += [
            "",
            "## 关键新闻详情",
            "",
        ]
        for idx, a in enumerate(top_with_detail, 1):
            sev_emoji = SEVERITY_EMOJI.get(a["severity"], "")
            summary = a.get("summary", "")
            regions = ", ".join(a["classified_regions"][:2])
            headline = a.get("title_cn") or a["title"]
            lines += [
                f"### {idx}. {sev_emoji} {headline}",
                "",
            ]
            if a.get("title_cn"):
                lines.append(f"*{a['title'][:100]}*")
                lines.append("")
            lines += [
                f"- **区域**: {regions}",
                f"- **事件类型**: {', '.join(a['event_types'][:3])}",
            ]
            if summary:
                lines.append(f"- **摘要**: {summary}")
            if a.get("content_detail"):
                lines.extend(["", f"> {a['content_detail'][:600]}", ""])
            lines.append(f"[阅读原文]({a.get('url', '#')})")
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
            "title_cn": a.get("title_cn", ""),
            "url": a.get("url", ""),
            "content": a.get("content", "")[:300],
            "content_detail": a.get("content_detail", ""),
            "published_date": a.get("published_date", ""),
            "search_region": a["search_region"],
            "classified_regions": a["classified_regions"],
            "event_types": a["event_types"],
            "severity": a["severity"],
            "summary": a.get("summary", ""),
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

    # 2. LLM 分类（事件类型、严重程度、区域归属）
    print("  LLM 分类...")
    classify_articles_batch(unique)

    # 3. 抓取正文 + 生成摘要 (top 20 或 MEDIUM+)
    print("  抓取正文与摘要...")
    enrich_articles(unique)

    # 4. 生成报告
    md = generate_report(unique, date_str)
    md_path = DATA_DIR / f"{date_str}.md"
    md_path.write_text(md, encoding="utf-8")
    print(f"  → {md_path}")

    # 5. 生成 JSON
    json_data = build_json(unique, date_str)
    json_path = DATA_DIR / f"{date_str}.json"
    json_path.write_text(json.dumps(json_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  → {json_path}")

    # 6. 控制台摘要
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