"""
mark_task.py -- Update progress.json for one task.

Usage:
  python mark_task.py <task_id> in_progress
  python mark_task.py <task_id> done [--note "..."]
  python mark_task.py <task_id> failed --note "error message"

The script preserves all other fields and only mutates `status` (and optional
`note`, `completed_at_kst`, `failed_at_kst`).
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

PROGRESS_PATH = Path(__file__).resolve().parent.parent / "checkpoints" / "progress.json"
KST = timezone(timedelta(hours=9))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("task_id")
    ap.add_argument("status", choices=["pending", "in_progress", "done", "failed"])
    ap.add_argument("--note", default=None)
    args = ap.parse_args()

    with open(PROGRESS_PATH) as f:
        prog = json.load(f)

    target = None
    for t in prog["tasks"]:
        if t["id"] == args.task_id:
            target = t
            break
    if target is None:
        print(f"ERROR: task '{args.task_id}' not found", file=sys.stderr)
        sys.exit(1)

    now = datetime.now(tz=KST).isoformat()
    target["status"] = args.status
    if args.status == "done":
        target["completed_at_kst"] = now
    elif args.status == "failed":
        target["failed_at_kst"] = now
    elif args.status == "in_progress":
        target.setdefault("started_at_kst", now)
    if args.note:
        target["note"] = args.note

    with open(PROGRESS_PATH, "w") as f:
        json.dump(prog, f, indent=2)
        f.write("\n")

    print(f"OK [{args.task_id}] -> {args.status}")


if __name__ == "__main__":
    main()
