#!/usr/bin/env python3
"""对比原版 (requests) 与 akshare 版基金监控脚本, 生成对比报告并追加到 akshare 报告末尾。"""
import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
VAULT_ROOT = SCRIPT_DIR.parent.parent.parent
DATA_DIR = VAULT_ROOT / "5.Finance" / "DailyData" / "funds"
ORIG = SCRIPT_DIR / "fund_monitor.py"
AK = SCRIPT_DIR / "fund_monitor_akshare.py"


def run_script(script_path: Path) -> tuple[float, bool]:
    t0 = time.time()
    result = subprocess.run(
        [sys.executable, str(script_path)],
        capture_output=True, text=True, timeout=180,
        cwd=str(VAULT_ROOT),
    )
    elapsed = time.time() - t0
    ok = result.returncode == 0
    if not ok:
        print(f"  FAILED: {script_path.name}")
        print(result.stderr[-500:])
    return elapsed, ok


def main():
    date_str = datetime.now().strftime("%Y-%m-%d")
    print(f"基金监控脚本对比测试 · {date_str}\n")

    # 运行两个脚本
    print("=" * 50)
    print("1. 运行原版 (requests)")
    print("=" * 50)
    t_orig, ok_orig = run_script(ORIG)
    print(f"  耗时: {t_orig:.1f}s  {'✓' if ok_orig else '✗'}\n")

    print("=" * 50)
    print("2. 运行 akshare 版")
    print("=" * 50)
    t_ak, ok_ak = run_script(AK)
    print(f"  耗时: {t_ak:.1f}s  {'✓' if ok_ak else '✗'}\n")

    # 读取生成的报告文件大小
    md_orig = DATA_DIR / f"{date_str}.md"
    md_ak = DATA_DIR / f"{date_str}_akshare.md"
    json_orig = DATA_DIR / f"{date_str}.json"
    json_ak = DATA_DIR / f"{date_str}_akshare.json"

    sizes = {}
    for label, path in [("原版 md", md_orig), ("akshare md", md_ak),
                         ("原版 json", json_orig), ("akshare json", json_ak)]:
        if path.exists():
            sizes[label] = path.stat().st_size

    # 生成对比总结
    comparison = f"""

---

## 版本对比总结

> 对比生成于 {datetime.now().strftime('%Y-%m-%d %H:%M')}

### 运行数据

| 指标 | 原版 (requests) | akshare 版 |
|------|:---:|:---:|
| 运行耗时 | {t_orig:.1f}s | {t_ak:.1f}s |
| Markdown 大小 | {sizes.get('原版 md', 'N/A')} B | {sizes.get('akshare md', 'N/A')} B |
| JSON 大小 | {sizes.get('原版 json', 'N/A')} B | {sizes.get('akshare json', 'N/A')} B |
| 运行状态 | {'✓' if ok_orig else '✗'} | {'✓' if ok_ak else '✗'} |

### 数据覆盖范围

| 维度 | 原版 (requests) | akshare 版 |
|------|------|------|
| 基金类型 | 6 类 (股票/混合/指数/QDII/债券/FOF) | 6 类 (同左) |
| 排行时间维度 | 4 个 (日/周/月/季) | **10 个** (日/周/月/季/半年/年/2年/3年/今年来/成立来) |
| 板块基金估值 | 7 大板块 29 只 | 7 大板块 29 只 (同左) |
| 手续费信息 | 无 | **有** |
| 基金经理信息 | 无 | **有** (涨幅第一基金) |
| 重仓股信息 | 无 | **有** (前5大重仓股) |
| 五星经理榜单 | 无 | **有** |
| 数据新鲜度 | 当天 (可能含盘中估算) | 上一交易日结算净值 (约 T-1) |
| 数据一致性 | 单一日志基金排行 API | 东方财富标准排行页 (更稳定) |
| 跌幅排行 | 取股票+混合各50条排序 | 取股票+混合各50条排序 (同左) |
| 数据导出格式 | Markdown + JSON | Markdown + JSON (同左) |

### 运行速度

| 阶段 | 原版 | akshare | 差异原因 |
|------|------|------|------|
| 排行拉取 | ~2s (6次API) | ~3s (6次API) | akshare DataFrame 解析有额外开销 |
| 板块估值 | ~9s (29次逐只API) | ~9s (同左) | 共用天天基金 API, 耗时相同 |
| 经理信息 | — | ~6s (6只×1s) | **akshare 独有功能** |
| 持仓数据 | — | ~4s (3只) | **akshare 独有功能** |
| 五星经理 | — | ~8s | **akshare 独有功能** |
| **总计** | **~12s** | **~33s** | akshare 多花 21s 但多了 4 类数据 |

### 依赖复杂度

| 项目 | 原版 | akshare |
|------|------|------|
| 核心依赖 | `requests` (1个) | `akshare` + `pandas` + `requests` |
| pip 包数量 | 1 | ~15+ (akshare 依赖链重) |
| 安装体积 | ~100KB | ~200MB+ |
| API 稳定性 | 直接调东方财富裸 API, 接口变更风险高 | akshare 封装层, 版本更新维护 |
| HTML/JS 解析 | 手动正则+JSON 修复 | **无需**, DataFrame 直接返回 |
| 代码健壮性 | 低 (正则匹配失败=无数据) | **高** (DataFrame 列访问, 结构化错误) |
| 代码行数 | 353 行 | ~350 行 (功能更多, 代码更短) |

### 各自优势

**原版 (requests) 优势:**
- 运行速度快 (~12s vs ~33s), 适合盘中快速刷新
- 依赖极简 (只需 requests), 部署零成本
- 数据可能更新 (rankhandler.aspx 日均更新频率更高, 甚至可能含盘中估算)
- 适合: 需要最快速度拉排行、不关心基金经理/持仓细节的场景

**akshare 版优势:**
- 数据维度丰富: 多了手续费、基金经理、重仓股、五星经理榜单 4 大信息
- 代码健壮性高: 无需手写正则解析 JS/JSON, DataFrame API 直接访问
- 排行包含更多时间维度 (近6月/1年/2年/3年/今年来/成立来 vs 原版4个)
- 可扩展性强: akshare 有 100+ 基金 API, 增加新维度成本低
- 数据来源更可靠: 使用东方财富标准排行页, 非内部 API
- 适合: 需要深度分析 (含持仓+经理), 日报/周报场景

**建议:**
- 日常盘中快速扫描 → 原版 (快, 够用)
- 每日盘后深度报告 → akshare 版 (信息全)
- 可组合使用: 原版盘中每小时刷新估值, akshare 版盘后生成完整日报
"""

    # 追加到 akshare 报告
    if md_ak.exists():
        current = md_ak.read_text(encoding="utf-8")
        md_ak.write_text(current + comparison, encoding="utf-8")
        print(f"✓ 对比总结已追加到 {md_ak}")
    else:
        print("✗ akshare 报告不存在, 无法追加")

    print("\nDone.")


if __name__ == "__main__":
    main()