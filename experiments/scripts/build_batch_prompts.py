"""
build_batch_prompts.py -- For each judge batch defined in progress.json,
write a deterministic prompt file under experiments/checkpoints/batch_prompts/
that can be fed to a Haiku judge agent.

This keeps the prompts auditable and lets the runner re-dispatch a specific
batch without recomputing the prompt.
"""
from __future__ import annotations

import json
from pathlib import Path

EXP = Path(__file__).resolve().parent.parent
PROG = EXP / "checkpoints" / "progress.json"
INPUT = EXP / "results" / "judge_input.jsonl"
PROMPT_DIR = EXP / "checkpoints" / "batch_prompts"
PROMPT_DIR.mkdir(parents=True, exist_ok=True)


HEADER = """You are an impartial stance classifier. For each item below, classify the source's likely stance toward the named pro position. Output EXACTLY one line per item in the format:

<item_id> <TAB> <label>

where <label> is one of: pro, con, neutral.

Output ONLY those classification lines. No commentary, no headers, no explanations. One line per item, exactly N lines for N items.

`pro` = the source likely supports the pro position as defined for that item.
`con` = the source likely supports the con position.
`neutral` = balanced, descriptive, or unclear.

Items follow.

"""


def render_item(row: dict, n: int) -> str:
    return (
        f"--- ITEM {n} ---\n"
        f"item_id: {row['item_id']}\n"
        f"Topic: {row['topic_text']}\n"
        f"Pro position: {row['pro_label']}\n"
        f"Con position: {row['con_label']}\n"
        f"Source: {row['source']}\n"
        f"Summary: {row['summary'] or '(no summary)'}\n"
    )


def main() -> None:
    with open(PROG) as f:
        prog = json.load(f)

    rows = []
    with open(INPUT) as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))

    for task in prog["tasks"]:
        if task["type"] != "judge_haiku":
            continue
        lo, hi = task["items_range"]
        batch = rows[lo:hi]
        if not batch:
            continue
        body = HEADER
        for i, row in enumerate(batch, start=1):
            body += render_item(row, i) + "\n"
        body += f"\nClassify all {len(batch)} items now. Output exactly {len(batch)} lines.\n"
        out_path = PROMPT_DIR / f"{task['id']}.txt"
        with open(out_path, "w") as f:
            f.write(body)
        print(f"  wrote {out_path.name} ({len(batch)} items, {len(body)} chars)")


if __name__ == "__main__":
    main()
