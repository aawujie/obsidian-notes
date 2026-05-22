#!/usr/bin/env python3
"""Backfill A-stock data for specific dates by running the main script with date override."""
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path
import shutil

VAULT = Path("/home/dr/Documents/obsidian-notes")
SCRIPT = VAULT / "Resources/scripts/a-stock-monitor/a_stock_monitor.py"
OUTDIR = VAULT / "5.Finance/DailyData/a-stock"

# Find missing dates between start and end (weekdays only)
start = date(2026, 5, 10)
end = date(2026, 5, 22)

missing = []
d = start
while d <= end:
    if d.weekday() < 5:  # Mon-Fri
        if not (OUTDIR / f"{d}.json").exists():
            missing.append(d)
    d += timedelta(days=1)

print(f"Missing dates: {missing}")

for dt in missing:
    date_str = dt.isoformat()
    print(f"\nBackfilling {date_str}...")

    env = {
        **__import__('os').environ,
        'BACKFILL_DATE': date_str,
        'https_proxy': 'http://127.0.0.1:7890',
        'http_proxy': 'http://127.0.0.1:7890',
    }

    # Patch: copy the script, replace datetime.now() with the target date
    script_text = SCRIPT.read_text()
    patched = script_text.replace(
        'date_str = datetime.now().strftime("%Y-%m-%d")',
        f'date_str = "{date_str}"'
    )
    patched = patched.replace(
        '> 自动生成于 {datetime.now().strftime(\'%Y-%m-%d %H:%M\')}',
        f'> 自动生成于 {date_str} 23:59'
    )

    tmp = Path("/tmp/backfill_a_stock.py")
    tmp.write_text(patched)

    result = subprocess.run(
        [str(VAULT / ".venv/bin/python3"), str(tmp)],
        env=env,
        capture_output=True, text=True,
        timeout=60,
        cwd=str(VAULT),
    )

    if result.returncode == 0:
        # Move output to correct date if script wrote with today's date
        today_file = OUTDIR / f"{date.today()}.json"
        if today_file.exists() and dt != date.today():
            shutil.move(str(today_file), str(OUTDIR / f"{date_str}.json"))
            shutil.move(str(today_file.with_suffix('.md')), str(OUTDIR / f"{date_str}.md"))
        print(f"  ✅ {date_str}")
        print(result.stdout.split('\n')[-5:])
    else:
        print(f"  ❌ {date_str}: {result.stderr[-300:]}")