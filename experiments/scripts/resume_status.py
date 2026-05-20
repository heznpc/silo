"""
resume_status.py -- Show next pending task and token-cycle window info.

Usage: python experiments/scripts/resume_status.py [--next | --json | --summary]

  --summary (default): human-readable status
  --next: print the next pending task ID only (for shell scripts)
  --json: dump full progress.json
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

PROGRESS_PATH = Path(__file__).resolve().parent.parent / "checkpoints" / "progress.json"

# 5-hour cycle anchored at 2026-05-21 03:10 KST
KST = timezone(timedelta(hours=9))
ANCHOR = datetime(2026, 5, 21, 3, 10, 0, tzinfo=KST)
CYCLE = timedelta(hours=5)


def compute_window(now_utc: datetime) -> tuple[datetime, datetime, timedelta]:
    """Return (current_window_start_kst, next_reset_kst, time_until_reset)."""
    now_kst = now_utc.astimezone(KST)
    elapsed = now_kst - ANCHOR
    n_cycles = int(elapsed.total_seconds() // CYCLE.total_seconds())
    start = ANCHOR + n_cycles * CYCLE
    next_reset = start + CYCLE
    until = next_reset - now_kst
    return start, next_reset, until


def main() -> None:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--next", action="store_true")
    g.add_argument("--json", action="store_true")
    args = ap.parse_args()

    with open(PROGRESS_PATH) as f:
        prog = json.load(f)

    if args.json:
        json.dump(prog, sys.stdout, indent=2)
        return

    now = datetime.now(tz=timezone.utc)
    win_start, win_end, until = compute_window(now)

    by_status: dict[str, list] = {"done": [], "in_progress": [], "pending": [], "failed": []}
    for t in prog["tasks"]:
        by_status.setdefault(t["status"], []).append(t)

    next_pending = next((t for t in prog["tasks"] if t["status"] in ("pending", "in_progress")), None)

    if args.next:
        if next_pending:
            print(next_pending["id"])
        else:
            print("ALL_DONE")
        return

    # Summary
    print("=" * 70)
    print("Silo MVE -- Resumable Runner Status")
    print("=" * 70)
    print(f"Now (KST):        {now.astimezone(KST).strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Window started:   {win_start.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"Next reset:       {win_end.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"Time until reset: {until}")
    print()
    print(f"Tasks: {len(by_status['done'])} done, {len(by_status['in_progress'])} in_progress, "
          f"{len(by_status['pending'])} pending, {len(by_status['failed'])} failed")
    print()

    if next_pending:
        print(f"NEXT: {next_pending['id']} ({next_pending['type']})")
        if "description" in next_pending:
            print(f"      {next_pending['description']}")
        if "topic_id" in next_pending:
            print(f"      topic={next_pending['topic_id']} framing={next_pending.get('framing')}")
        if "items_range" in next_pending:
            print(f"      items {next_pending['items_range'][0]}..{next_pending['items_range'][1]}")
        print(f"      agent_calls_needed: {next_pending.get('agent_calls_needed', 0)}")
    else:
        print("ALL TASKS DONE.")

    print()
    print("Task list (by status):")
    for status in ("in_progress", "pending", "done", "failed"):
        for t in by_status[status]:
            marker = {"done": "  +", "in_progress": " ->", "pending": "  .", "failed": "  X"}[status]
            print(f"  {marker} [{status:<11s}] {t['id']:<35s} {t['type']}")


if __name__ == "__main__":
    main()
