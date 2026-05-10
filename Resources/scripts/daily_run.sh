#!/bin/bash
# 每日市场数据拉取 + 微信通知
# 用法: ./daily_run.sh {a-stock|hk-stock|gold|metals|us-stock|all-overnight}
#
# Crontab 已安装 (crontab -l 查看):
#   30 15 * * 1-5  → a-stock (收盘 15:00)
#   30 16 * * 1-5  → hk-stock (收盘 16:00)
#    0  6 * * 1-5  → all-overnight (黄金+金属+美股)

set -euo pipefail

MARKET="$1"
VAULT="/home/dr/Documents/obsidian-notes"
VENV="$VAULT/.venv"
SCRIPTS="$VAULT/Resources/scripts"
LOGDIR="$SCRIPTS/logs"
mkdir -p "$LOGDIR"

DATE=$(date +%Y-%m-%d)
LOG="$LOGDIR/${MARKET}-${DATE}.log"

# 代理 (Yahoo Finance 需要)
export https_proxy=http://127.0.0.1:7890
export http_proxy=http://127.0.0.1:7890
export all_proxy=socks5://127.0.0.1:7890

# 微信通知参数
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
    local REPORT="$3"

    log "开始拉取 $MARKET_NAME 数据..."
    cd "$VAULT"
    source "$VENV/bin/activate"
    if python "$SCRIPT" >> "$LOG" 2>&1; then
        log "$MARKET_NAME ✓ 数据已保存 → $REPORT"
    else
        log "$MARKET_NAME ✗ 失败，详情见日志"
        return 1
    fi
}

# ─── 微信摘要生成 ──────────────────────────────────────────
generate_summary() {
    local MARKET_NAME="$1"
    local JSON="$2"

    if [ ! -f "$JSON" ]; then
        echo "📊 ${MARKET_NAME}日报 ${DATE}
⚠️ 今日无数据"
        return
    fi

    python3 - "$JSON" "$MARKET_NAME" "$DATE" << 'PYEOF'
import json, sys, os

json_path, mkt_name, date_str = sys.argv[1], sys.argv[2], sys.argv[3]

with open(json_path) as f:
    wrapped = json.load(f)
    data = wrapped.get("data", wrapped if isinstance(wrapped, list) else [])

if not data:
    print(f"📊 {mkt_name}日报 {date_str}\n⚠️ 今日无数据")
    sys.exit(0)

sorted_up = sorted(data, key=lambda x: x.get("change_daily") or -999, reverse=True)
top3 = sorted_up[:3]
bottom3 = sorted_up[-3:]

# 分类
futures = [d for d in data if "=F" in d["ticker"]]
stocks = [d for d in data if "=F" not in d["ticker"]]
new_highs = [d for d in data if d.get("is_new_high")]

def pct(v):
    if v is None: return "—"
    return f"{v:+.2f}%"

def price(v):
    if v is None: return "—"
    return f"{v:.2f}"

# emoji by market
emoji = {"黄金": "🥇", "金属": "⛏️", "A股": "🇨🇳", "港股": "🇭🇰", "美股": "🇺🇸"}.get(mkt_name, "📊")

lines = [f"{emoji} {mkt_name}日报 {date_str}", ""]

# 期货/指数
if futures:
    lines.append("▸ 期货/指数")
    for f in futures[:8]:
        lines.append(f"{f['ticker']}: ${price(f['close'])} {pct(f['change_daily'])}")
    lines.append("")

# 涨幅前三
lines.append("▸ 涨幅前三")
for d in top3:
    nm = d.get("name", d["ticker"])
    if len(nm) > 25:
        nm = nm[:25]
    lines.append(f"{d['ticker']} {pct(d['change_daily'])}  {nm}")
lines.append("")

# 跌幅前三
lines.append("▸ 跌幅前三")
for d in bottom3:
    nm = d.get("name", d["ticker"])
    if len(nm) > 25:
        nm = nm[:25]
    lines.append(f"{d['ticker']} {pct(d['change_daily'])}  {nm}")
lines.append("")

# 52周新高
if new_highs:
    lines.append(f"▸ 52周新高 ({len(new_highs)}只)")
    for d in new_highs[:5]:
        lines.append(f"{d['ticker']}: ${price(d['close'])}  {d.get('name', '')[:20]}")

print("\n".join(lines))
PYEOF
}

# ─── 主逻辑 ────────────────────────────────────────────────

log "=== daily_run.sh $MARKET ==="

case "$MARKET" in
a-stock)
    run_monitor "A股" \
        "$SCRIPTS/a-stock-monitor/a_stock_monitor.py" \
        "$VAULT/5.Finance/DailyData/a-stock/${DATE}.md" || true
    SUMMARY=$(generate_summary "A股" "$VAULT/5.Finance/DailyData/a-stock/${DATE}.json")
    send_wx "$SUMMARY"
    ;;

hk-stock)
    run_monitor "港股" \
        "$SCRIPTS/hk-stock-monitor/hk_stock_monitor.py" \
        "$VAULT/5.Finance/DailyData/hk-stock/${DATE}.md" || true
    SUMMARY=$(generate_summary "港股" "$VAULT/5.Finance/DailyData/hk-stock/${DATE}.json")
    send_wx "$SUMMARY"
    ;;

gold)
    run_monitor "黄金" \
        "$SCRIPTS/gold-monitor/gold_monitor.py" \
        "$VAULT/5.Finance/DailyData/gold/${DATE}.md" || true
    SUMMARY=$(generate_summary "黄金" "$VAULT/5.Finance/DailyData/gold/${DATE}.json")
    send_wx "$SUMMARY"
    ;;

metals)
    run_monitor "金属" \
        "$SCRIPTS/metals-monitor/metals_monitor.py" \
        "$VAULT/5.Finance/DailyData/metals/${DATE}.md" || true
    SUMMARY=$(generate_summary "金属" "$VAULT/5.Finance/DailyData/metals/${DATE}.json")
    send_wx "$SUMMARY"
    ;;

us-stock)
    run_monitor "美股" \
        "$SCRIPTS/us-stock-monitor/us_stock_monitor.py" \
        "$VAULT/5.Finance/DailyData/us-stock/${DATE}.md" || true
    SUMMARY=$(generate_summary "美股" "$VAULT/5.Finance/DailyData/us-stock/${DATE}.json")
    send_wx "$SUMMARY"
    ;;

all-overnight)
    for mkt in gold metals us-stock; do
        bash "$0" "$mkt"
    done
    ;;

*)
    echo "用法: $0 {a-stock|hk-stock|gold|metals|us-stock|all-overnight}"
    exit 1
    ;;
esac

log "=== 完成 ==="