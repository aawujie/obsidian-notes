#!/bin/bash
# 每日市场数据拉取 + 微信通知
# 用法: ./daily_run.sh {a-stock|hk-stock|gold|metals|us-stock|all-overnight}
#
# Crontab:
#   30 15 * * 1-5  .../daily_run.sh a-stock
#   30 16 * * 1-5  .../daily_run.sh hk-stock
#    0  6 * * 1-5  .../daily_run.sh all-overnight

set -euo pipefail

MARKET="$1"
VAULT="/home/dr/Documents/obsidian-notes"
VENV="$VAULT/.venv"
SCRIPTS="$VAULT/Resources/scripts"
LOGDIR="$SCRIPTS/logs"
mkdir -p "$LOGDIR"

DATE=$(date +%Y-%m-%d)
LOG="$LOGDIR/${MARKET}-${DATE}.log"

# 微信通知参数
WX_CHANNEL="openclaw-weixin"
WX_TO="o9cq803b6DrCh5LqQr85vojqnbJI@im.wechat"
WX_ACCOUNT="268e571b45b7-im-bot"

log() { echo "[$(date '+%H:%M:%S')] $*" | tee -a "$LOG"; }

send_wx() {
    local MSG="$1"
    # 微信表格前后必须空行 (MEMORY.md 强制规范)
    openclaw message send \
        --channel "$WX_CHANNEL" \
        --account "$WX_ACCOUNT" \
        --to "$WX_TO" \
        --message "$MSG" >> "$LOG" 2>&1 || log "[WARN] 微信发送失败"
}

run_monitor() {
    local MARKET_NAME="$1"
    local SCRIPT="$2"
    local REPORT="$3"

    log "开始拉取 $MARKET_NAME 数据..."
    cd "$VAULT"
    source "$VENV/bin/activate"
    if python "$SCRIPT" >> "$LOG" 2>&1; then
        log "$MARKET_NAME ✓ 数据已保存"
        if [ -f "$REPORT" ]; then
            log "报告: $REPORT"
        fi
    else
        log "$MARKET_NAME ✗ 失败，详情见日志"
    fi
}

# ─── 微信摘要生成 ──────────────────────────────────────────
generate_summary() {
    local MARKET_NAME="$1"
    local JSON="$2"
    local DATE_STR="$3"

    if [ ! -f "$JSON" ]; then
        echo "📊 ${MARKET_NAME}日报 ${DATE_STR}\n⚠️ 今日无数据"
        return
    fi

    python3 - "$JSON" "$MARKET_NAME" "$DATE_STR" << 'PYEOF'
import json, sys

json_path, mkt_name, date_str = sys.argv[1], sys.argv[2], sys.argv[3]

with open(json_path) as f:
    data = json.load(f)["data"]

if not data:
    print(f"📊 {mkt_name}日报 {date_str}\n\n⚠️ 今日无数据")
    sys.exit(0)

# 排序取涨跌
sorted_data = sorted(data, key=lambda x: x.get("change_daily") or -999, reverse=True)
top3 = sorted_data[:3]
bottom3 = sorted_data[-3:]

# 按 ticker 分类 (期货 vs 股票)
futures = [d for d in data if "=F" in d["ticker"]]
stocks = [d for d in data if "=F" not in d["ticker"]]
new_highs = [d for d in data if d.get("is_new_high")]

def pct(v):
    if v is None: return "—"
    return f"{v:+.2f}%"

def price(v):
    if v is None: return "—"
    return f"{v:.2f}"

def cn_name(d):
    cn = d.get("cn_name", "")
    name = d.get("name", d["ticker"])[:20]
    return f"{name}" + (f"({cn})" if cn else "")

lines = [f"📊 {mkt_name}日报 {date_str}", ""]

# 关键指数/期货
if futures:
    lines.append("**期货/指数**")
    lines.append("")
    for f in futures:
        lines.append(f"• {f['ticker']}: ${price(f['close'])} {pct(f['change_daily'])}")
    lines.append("")

# 涨幅前三
if top3:
    lines.append("**涨幅前三**")
    lines.append("")
    for d in top3:
        lines.append(f"• {d['ticker']}: {pct(d['change_daily'])}")
    lines.append("")

# 跌幅前三
if bottom3:
    lines.append("**跌幅前三**")
    lines.append("")
    for d in bottom3:
        lines.append(f"• {d['ticker']}: {pct(d['change_daily'])}")
    lines.append("")

# 52周新高
if new_highs:
    lines.append(f"**52周新高 ({len(new_highs)}只)**")
    lines.append("")
    for d in new_highs[:10]:
        lines.append(f"• {d['ticker']}: ${price(d['close'])}")

print("\n".join(lines))
PYEOF
}

# ─── 主逻辑 ────────────────────────────────────────────────

log "=== daily_run.sh $MARKET ==="

case "$MARKET" in
a-stock)
    run_monitor "A股" \
        "$SCRIPTS/a-stock-monitor/a_stock_monitor.py" \
        "$VAULT/5.Finance/DailyData/a-stock/${DATE}.md"
    SUMMARY=$(generate_summary "A股" "$VAULT/5.Finance/DailyData/a-stock/${DATE}.json" "$DATE")
    send_wx "$SUMMARY"
    ;;

hk-stock)
    run_monitor "港股" \
        "$SCRIPTS/hk-stock-monitor/hk_stock_monitor.py" \
        "$VAULT/5.Finance/DailyData/hk-stock/${DATE}.md"
    SUMMARY=$(generate_summary "港股" "$VAULT/5.Finance/DailyData/hk-stock/${DATE}.json" "$DATE")
    send_wx "$SUMMARY"
    ;;

gold)
    run_monitor "黄金" \
        "$SCRIPTS/gold-monitor/gold_monitor.py" \
        "$VAULT/5.Finance/DailyData/gold/${DATE}.md"
    SUMMARY=$(generate_summary "黄金" "$VAULT/5.Finance/DailyData/gold/${DATE}.json" "$DATE")
    send_wx "$SUMMARY"
    ;;

metals)
    run_monitor "金属" \
        "$SCRIPTS/metals-monitor/metals_monitor.py" \
        "$VAULT/5.Finance/DailyData/metals/${DATE}.md"
    SUMMARY=$(generate_summary "金属" "$VAULT/5.Finance/DailyData/metals/${DATE}.json" "$DATE")
    send_wx "$SUMMARY"
    ;;

us-stock)
    run_monitor "美股" \
        "$SCRIPTS/us-stock-monitor/us_stock_monitor.py" \
        "$VAULT/5.Finance/DailyData/us-stock/${DATE}.md"
    SUMMARY=$(generate_summary "美股" "$VAULT/5.Finance/DailyData/us-stock/${DATE}.json" "$DATE")
    send_wx "$SUMMARY"
    ;;

all-overnight)
    # 早上 6:00 跑：黄金 + 金属 + 美股
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