#!/bin/bash
# 每日市场数据拉取 + 微信通知
# 用法: ./daily_run.sh {a-stock|hk-stock|gold|metals|us-stock|all-overnight}
#
# Crontab:
#   30 15 * * 1-5  → a-stock
#   30 16 * * 1-5  → hk-stock
#    0  0 * * 1-5  → fund
#    0  6 * * 1-5  → all-overnight  (gold, metals, us-stock, macro)
#    0  8 * * *    → geopolitics

set -euo pipefail

MARKET="$1"
VAULT="/home/dr/Documents/obsidian-notes"
VENV="$VAULT/.venv"
SCRIPTS="$VAULT/Resources/scripts"
LOGDIR="$SCRIPTS/logs"
mkdir -p "$LOGDIR"

DATE=$(date +%Y-%m-%d)
LOG="$LOGDIR/${MARKET}-${DATE}.log"

export https_proxy=http://127.0.0.1:7890
export http_proxy=http://127.0.0.1:7890
export all_proxy=socks5://127.0.0.1:7890

WX_CHANNEL="openclaw-weixin"
WX_TARGET="o9cq803b6DrCh5LqQr85vojqnbJI@im.wechat"
WX_ACCOUNT="268e571b45b7-im-bot"

log() { echo "[$(date '+%H:%M:%S')] $*" | tee -a "$LOG"; }

send_wx() {
    openclaw message send \
        --channel "$WX_CHANNEL" \
        --account "$WX_ACCOUNT" \
        -t "$WX_TARGET" \
        -m "$1" >> "$LOG" 2>&1 || log "[WARN] 微信发送失败"
}

run_monitor() {
    local MARKET_NAME="$1"
    local SCRIPT="$2"
    log "开始拉取 $MARKET_NAME 数据..."
    cd "$VAULT"
    source "$VENV/bin/activate"
    if python "$SCRIPT" >> "$LOG" 2>&1; then
        log "$MARKET_NAME ✓ 完成"
    else
        log "$MARKET_NAME ✗ 失败"
        return 1
    fi
}

# ─── 微信摘要生成 (Python 渲染表格 + 中文名) ───────────────
generate_summary() {
    local MARKET_NAME="$1"
    local JSON="$2"
    local EMOJI="$3"

    if [ ! -f "$JSON" ]; then
        echo "${EMOJI} ${MARKET_NAME}日报 ${DATE}

⚠️ 今日无数据"
        return
    fi

    python3 << PYEOF
import json, sys

json_path = "$JSON"
mkt = "$MARKET_NAME"
date_str = "$DATE"
emoji = "$EMOJI"

with open(json_path) as f:
    wrapped = json.load(f)
    data = wrapped.get("data", wrapped if isinstance(wrapped, list) else [])

if not data:
    print(f"{emoji} {mkt}日报 {date_str}\\n\\n⚠️ 今日无数据")
    sys.exit(0)

# ═══════════════════════════════════════════════════════════
#  中文名称总表 (来自各 monitor 脚本的 CHINESE_NAMES)
# ═══════════════════════════════════════════════════════════
CN = {
    # ── 黄金 ──
    "GLD": "SPDR黄金ETF", "IAU": "iShares黄金ETF", "SGOL": "abrdn黄金ETF",
    "NEM": "纽蒙特矿业", "GOLD": "巴里克黄金", "AU": "盎格鲁黄金",
    "GFI": "金田公司", "KGC": "金罗斯黄金", "AEM": "Agnico Eagle",
    "FNV": "Franco-Nevada", "WPM": "惠顿贵金属", "RGLD": "皇家黄金",
    "AGI": "阿拉莫斯黄金", "GDX": "金矿ETF", "GDXJ": "小盘金矿ETF",
    "GC=F": "黄金期货", "SLV": "白银ETF",
    # ── 金属 ──
    "HG=F": "铜期货", "ALI=F": "铝期货",
    "SI=F": "白银期货", "PL=F": "铂金期货", "PA=F": "钯金期货",
    "XME": "矿业ETF-SPDR", "PICK": "全球矿业ETF", "COPX": "铜矿ETF",
    "REMX": "稀土ETF", "LIT": "锂矿ETF", "SIL": "白银矿业ETF",
    "BHP": "必和必拓", "RIO": "力拓", "VALE": "淡水河谷",
    "FCX": "自由港麦克莫兰", "SCCO": "南方铜业", "TECK": "泰克资源",
    "AA": "美国铝业", "CENX": "世纪铝业",
    "MP": "MP稀土", "SGML": "西格玛锂业", "ALB": "雅保锂业", "SQM": "智利矿业化工",
    # ── A股 ──
    "000001.SS": "上证指数", "399001.SZ": "深证成指", "399006.SZ": "创业板指",
    "000688.SS": "科创50", "000300.SS": "沪深300",
    "FXI": "富时中国50", "ASHR": "沪深300ETF", "KWEB": "中国互联网ETF",
    "MCHI": "MSCI中国ETF", "CQQQ": "中国科技ETF", "YINN": "中国3倍做多",
    "0700.HK": "腾讯", "9988.HK": "阿里巴巴", "3690.HK": "美团",
    "9618.HK": "京东", "1810.HK": "小米", "9999.HK": "网易",
    "9888.HK": "百度", "2015.HK": "理想汽车", "9868.HK": "小鹏汽车",
    "9961.HK": "携程", "1024.HK": "快手", "9626.HK": "B站",
    # ── 港股 ──
    "^HSI": "恒生指数", "^HSCE": "国企指数", "^HSCCI": "红筹指数", "^HSTECH": "恒生科技",
    "2800.HK": "盈富基金", "2828.HK": "恒生国企ETF", "3067.HK": "恒生科技ETF",
    "3033.HK": "南方科创板50", "0005.HK": "汇丰控股", "0011.HK": "恒生银行",
    "0388.HK": "港交所", "0941.HK": "中国移动", "1299.HK": "友邦保险",
    "1398.HK": "工商银行", "2318.HK": "中国平安", "2388.HK": "中银香港",
    "2628.HK": "中国人寿", "3968.HK": "招商银行", "3988.HK": "中国银行",
    "2269.HK": "药明生物", "0883.HK": "中海油", "0857.HK": "中石油",
    "1088.HK": "中国神华", "1177.HK": "中国生物制药",
    "1929.HK": "周大福", "2007.HK": "碧桂园", "2057.HK": "中通快递",
    "2382.HK": "舜宇光学", "6618.HK": "京东健康",
    "1755.HK": "碧桂园服务", "1833.HK": "平安好医生", "2013.HK": "微盟集团", "2018.HK": "瑞声科技",
    # ── 美股 ──
    "AAPL": "苹果", "MSFT": "微软", "GOOGL": "谷歌", "AMZN": "亚马逊", "NVDA": "英伟达",
    "META": "Meta", "TSLA": "特斯拉", "AVGO": "博通", "AMD": "AMD", "NFLX": "奈飞",
    "ADBE": "Adobe", "CRM": "Salesforce", "INTC": "英特尔", "QCOM": "高通",
    "TXN": "德州仪器", "AMAT": "应用材料", "ASML": "阿斯麦", "MU": "美光",
    "JPM": "摩根大通", "BAC": "美国银行", "WFC": "富国银行", "C": "花旗",
    "GS": "高盛", "MS": "摩根士丹利", "V": "Visa", "MA": "万事达",
    "JNJ": "强生", "UNH": "联合健康", "PFE": "辉瑞", "ABBV": "艾伯维",
    "MRK": "默克", "LLY": "礼来", "TMO": "赛默飞", "ABT": "雅培",
    "XOM": "埃克森美孚", "CVX": "雪佛龙", "COP": "康菲石油", "SLB": "斯伦贝谢",
    "WMT": "沃尔玛", "COST": "好市多", "HD": "家得宝", "MCD": "麦当劳",
    "NKE": "耐克", "SBUX": "星巴克", "DIS": "迪士尼", "TMUS": "T-Mobile",
    "BA": "波音", "CAT": "卡特彼勒", "GE": "通用电气", "RTX": "雷神",
    "PLTR": "Palantir", "UBER": "优步", "ABNB": "爱彼迎", "SNAP": "Snapchat",
    "DASH": "DoorDash", "RBLX": "Roblox", "COIN": "Coinbase", "SQ": "Block",
    "ARM": "Arm安谋", "CEG": "Constellation能源", "VST": "Vistra能源",
    "GEV": "GE Vernova", "KKR": "KKR", "APO": "阿波罗全球",
    # ── 宏观 ──
    "^IRX": "3月期美债", "^FVX": "5年期美债",
    "^TNX": "10年期美债", "^TYX": "30年期美债",
    "TLT": "20+年美债ETF", "SHY": "短债ETF", "IEF": "中期美债ETF",
    "HYG": "高收益债ETF", "LQD": "投资级企业债ETF",
    "DX-Y.NYB": "美元指数", "EURUSD=X": "欧元/美元",
    "CNY=X": "美元/人民币", "JPY=X": "美元/日元", "GBPUSD=X": "英镑/美元",
    "^VIX": "VIX恐慌指数",
    "CL=F": "WTI原油", "BZ=F": "布伦特原油", "NG=F": "天然气",
    "USO": "原油ETF", "UNG": "天然气ETF",
    "BTC-USD": "比特币", "ETH-USD": "以太坊", "SOL-USD": "Solana",
}

def cn(ticker):
    return CN.get(ticker, "")

def pct(v):
    if v is None: return "—"
    return f"{v:+.2f}%"

def pr(v):
    if v is None: return "—"
    return f"{v:.2f}"

# 排序
up = sorted(data, key=lambda x: x.get("change_daily") or -999, reverse=True)
down = sorted(data, key=lambda x: x.get("change_daily") or 999)

# 关键指数/期货 (前 6)
futs = [d for d in data if "=F" in d["ticker"] or d["ticker"].startswith("^") or ".SS" in d["ticker"] or ".SZ" in d["ticker"]]

lines = [f"{emoji} {mkt}日报 {date_str}"]

if futs:
    lines.append("")
    lines.append("**核心指标**")
    lines.append("")
    lines.append("| 名称 | 收盘价 | 涨跌幅 |")
    lines.append("|:---|:---:|:---:|")
    for d in futs[:6]:
        name = cn(d["ticker"]) or d["ticker"]
        lines.append(f"| {name} | {pr(d['close'])} | {pct(d['change_daily'])} |")
    lines.append("")

# 涨幅 TOP 5
top5 = up[:5]
if top5:
    lines.append("**涨幅 TOP 5**")
    lines.append("")
    lines.append("| 名称 | 价格 | 涨幅 | 周涨幅 |")
    lines.append("|:---|:---:|:---:|:---:|")
    for d in top5:
        name = cn(d["ticker"]) or d["ticker"]
        lines.append(f"| {name} | {pr(d['close'])} | {pct(d['change_daily'])} | {pct(d.get('change_weekly'))} |")
    lines.append("")

# 跌幅 TOP 5
# 对于 HK/US 成分股太多的市场，跌的更有参考价值
bot5 = down[:5]
if bot5:
    lines.append("**跌幅 TOP 5**")
    lines.append("")
    lines.append("| 名称 | 价格 | 跌幅 | 周跌幅 |")
    lines.append("|:---|:---:|:---:|:---:|")
    for d in bot5:
        name = cn(d["ticker"]) or d["ticker"]
        lines.append(f"| {name} | {pr(d['close'])} | {pct(d['change_daily'])} | {pct(d.get('change_weekly'))} |")
    lines.append("")

# 52周新高
new_highs = [d for d in data if d.get("is_new_high")]
if new_highs:
    names = [cn(d["ticker"]) or d["ticker"] for d in new_highs[:10]]
    lines.append(f"**52周新高**: {', '.join(names)}")
    lines.append("")

lines.append(f"📁 完整报告 DailyData/{mkt.lower()}/{date_str}.md")

print("\n".join(lines))
PYEOF
}

# ─── 主逻辑 ────────────────────────────────────────────────
log "=== daily_run.sh $MARKET ==="

case "$MARKET" in
a-stock)
    run_monitor "A股" "$SCRIPTS/a-stock-monitor/a_stock_monitor.py" || true
    SUMMARY=$(generate_summary "A股" "$VAULT/5.Finance/DailyData/a-stock/${DATE}.json" "🇨🇳")
    send_wx "$SUMMARY"
    ;;
hk-stock)
    run_monitor "港股" "$SCRIPTS/hk-stock-monitor/hk_stock_monitor.py" || true
    SUMMARY=$(generate_summary "港股" "$VAULT/5.Finance/DailyData/hk-stock/${DATE}.json" "🇭🇰")
    send_wx "$SUMMARY"
    ;;
fund)
    run_monitor "基金" "$SCRIPTS/fund-monitor/fund_monitor.py" || true
    JSON="$VAULT/5.Finance/DailyData/funds/${DATE}.json"
    if [ -f "$JSON" ]; then
        SUMMARY=$(python3 -c "
import json
with open('$JSON') as f:
    d = json.load(f)
lines = ['💰 基金日报 ' + d['date'], '']
for cat, top in d.get('rankings', {}).items():
    if top:
        f0 = top[0]
        v = f0.get('change_daily')
        lines.append(f'{cat}: {f0.get(\"name\",\"?\")[:18]} {v:+.2f}%' if v is not None else f'{cat}: {f0.get(\"name\",\"?\")[:18]} —')
lines.append('')
lines.append('📁 DailyData/funds/' + d['date'] + '.md')
print('\n'.join(lines))
")
        send_wx "$SUMMARY"
    fi
    ;;
gold)
    run_monitor "黄金" "$SCRIPTS/gold-monitor/gold_monitor.py" || true
    SUMMARY=$(generate_summary "黄金" "$VAULT/5.Finance/DailyData/gold/${DATE}.json" "🥇")
    send_wx "$SUMMARY"
    ;;
metals)
    run_monitor "金属" "$SCRIPTS/metals-monitor/metals_monitor.py" || true
    SUMMARY=$(generate_summary "金属" "$VAULT/5.Finance/DailyData/metals/${DATE}.json" "⛏️")
    send_wx "$SUMMARY"
    ;;
us-stock)
    run_monitor "美股" "$SCRIPTS/us-stock-monitor/us_stock_monitor.py" || true
    SUMMARY=$(generate_summary "美股" "$VAULT/5.Finance/DailyData/us-stock/${DATE}.json" "🇺🇸")
    send_wx "$SUMMARY"
    ;;
geopolitics)
	    run_monitor "地缘政治" "$SCRIPTS/geopolitics-monitor/geopolitics_monitor.py" || true
	    # Custom summary for geopolitics (event-based, not price data)
	    JSON="$VAULT/5.Finance/DailyData/geopolitics/${DATE}.json"
	    SUMMARY=$(python3 << PYEOF
import json
with open("$JSON") as f:
    data = json.load(f)
events = data.get("events", [])
sev = data.get("severity_distribution", {})
critical = sev.get("critical", 0)
high = sev.get("high", 0)
print(f"🌍 地缘政治日报 $DATE")
print(f"")
print(f"共 {len(events)} 条事件")
if critical > 0:
    print(f"🔴 CRITICAL: {critical}")
if high > 0:
    print(f"🟠 HIGH: {high}")
print(f"🟡 MEDIUM: {sev.get('medium', 0)}")
print(f"🟢 LOW: {sev.get('low', 0)}")
print(f"")
top = [e for e in events if e['severity'] in ('critical', 'high')][:5]
if not top:
    top = events[:5]
for e in top:
    sev_icon = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}.get(e['severity'], "")
    regions = ", ".join(e.get('classified_regions', []))
    types = ", ".join(e.get('event_types', []))
    tickers = ", ".join(e.get('affected_tickers', [])[:5])
    print(f"  {sev_icon} {e['title'][:60]}")
    print(f"    → 区域: {regions} | 类型: {types}")
    if tickers:
        print(f"    → 关注: {tickers}")
    print(f"")
print(f"📁 完整报告 DailyData/geopolitics/$DATE.md")
PYEOF
)
	    send_wx "$SUMMARY"
	    ;;
macro)
    run_monitor "宏观" "$SCRIPTS/macro-monitor/macro_monitor.py" || true
    JSON="$VAULT/5.Finance/DailyData/macro/${DATE}.json"
    SUMMARY=$(python3 << PYEOF
import json, sys
json_path = "$JSON"
date_str = "$DATE"
try:
    with open(json_path) as f:
        wrapped = json.load(f)
    data = wrapped.get("data", [])
except Exception:
    print(f"📊 宏观指标日报 {date_str}\n\n⚠️ 今日无数据")
    sys.exit(0)
if not data:
    print(f"📊 宏观指标日报 {date_str}\n\n⚠️ 今日无数据")
    sys.exit(0)
CN = {
    "^TNX": "10Y美债", "^TYX": "30Y美债", "^IRX": "3M美债",
    "DX-Y.NYB": "美元指数", "^VIX": "VIX",
    "CL=F": "WTI原油", "BZ=F": "布油", "NG=F": "天然气",
    "BTC-USD": "BTC", "ETH-USD": "ETH", "SOL-USD": "SOL",
    "EURUSD=X": "EUR/USD", "CNY=X": "USD/CNY", "JPY=X": "USD/JPY",
}
def pct(v):
    if v is None: return "—"
    return f"{v:+.2f}%"
def pr(v):
    if v is None: return "—"
    return f"{v:.2f}"
key_order = ["^TNX", "DX-Y.NYB", "^VIX", "CL=F", "BTC-USD"]
lines = [f"📊 宏观指标日报 {date_str}", ""]
by_ticker = {d["ticker"]: d for d in data}
for t in key_order:
    d = by_ticker.get(t)
    if d:
        lines.append(f"  {CN.get(t, t)}: {pr(d['close'])} ({pct(d['change_daily'])})")
lines.append("")
lines.append(f"📁 完整报告 DailyData/macro/{date_str}.md")
print("\n".join(lines))
PYEOF
)
    send_wx "$SUMMARY"
    ;;
all-overnight)
    for mkt in gold metals us-stock macro; do
        bash "$0" "$mkt"
    done
    ;;
*)  echo "用法: $0 {a-stock|hk-stock|gold|metals|us-stock|macro|all-overnight}"; exit 1 ;;
esac

log "=== 完成 ==="