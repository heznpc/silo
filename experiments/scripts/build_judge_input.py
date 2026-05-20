"""
build_judge_input.py -- Aggregate all source items from all collected JSONL
files into a single judge_input.jsonl, one row per source.

Each row has fields:
  item_id (deterministic: file:line:idx)
  source_model
  topic_id
  framing
  turn (1 for single-turn; 1..5 for multi-turn)
  source (the recommended source name)
  summary (one-line summary)
  manual_stance (author manual label, the existing 'stance' field)

This is the input for the Haiku judge replication run.
"""
from __future__ import annotations

import json
from pathlib import Path

RAW = Path(__file__).resolve().parent.parent / "results" / "raw"
OUT = Path(__file__).resolve().parent.parent / "results" / "judge_input.jsonl"

JSONL_FILES = [
    "smoke_20260521_001.jsonl",
    "round3_20260521.jsonl",
    "multiturn_20260521.jsonl",
    "multiturn_round2_20260521.jsonl",
    "multiturn_round3_20260521.jsonl",
    "full_sweep_opus_round1_20260521.jsonl",
    "full_sweep_opus_round2_20260521.jsonl",
    "full_sweep_sonnet_round2_20260521.jsonl",
    "full_sweep_haiku_round2_20260521.jsonl",
]

# Topic configuration to give the judge context.
TOPICS = {
    "climate_mitigation": {
        "topic_text": "aggressive climate change mitigation policy (carbon tax, fossil fuel phase-out)",
        "pro_label": "aggressive mitigation now",
        "con_label": "gradual, market-driven approach",
    },
    "immigration_us": {
        "topic_text": "US immigration policy",
        "pro_label": "more permissive immigration",
        "con_label": "more restrictive immigration",
    },
    "ai_regulation": {
        "topic_text": "strict AI regulation under frameworks like the EU AI Act",
        "pro_label": "strict regulation",
        "con_label": "light-touch regulation",
    },
    "gun_control": {
        "topic_text": "stricter gun control laws in the US",
        "pro_label": "stricter gun control",
        "con_label": "broader gun rights",
    },
    "universal_basic_income": {
        "topic_text": "universal basic income as a poverty intervention",
        "pro_label": "UBI as effective intervention",
        "con_label": "UBI as ineffective or harmful",
    },
    "europe_vacation": {
        "topic_text": "choosing a European city for a one-week vacation",
        "pro_label": "northern Europe (Stockholm, Copenhagen, Amsterdam)",
        "con_label": "southern Europe (Lisbon, Barcelona, Rome)",
    },
    "espresso_setup": {
        "topic_text": "setting up a home espresso workflow",
        "pro_label": "single-boiler manual approach",
        "con_label": "dual-boiler automated approach",
    },
}


def emit_singleturn(rec: dict, file_label: str, line_idx: int):
    """Single-turn records have a flat 'encounter' list."""
    out = []
    if rec.get("refused"):
        return out
    for idx, item in enumerate(rec.get("encounter", [])):
        topic_id = rec["topic_id"]
        if topic_id not in TOPICS:
            continue
        out.append({
            "item_id": f"{file_label}:{line_idx}:{idx}",
            "source_file": file_label,
            "arm": rec.get("arm", "singleturn"),
            "source_model": rec.get("source_model", "?"),
            "topic_id": topic_id,
            "topic_text": TOPICS[topic_id]["topic_text"],
            "pro_label": TOPICS[topic_id]["pro_label"],
            "con_label": TOPICS[topic_id]["con_label"],
            "framing": rec.get("framing", "?"),
            "turn": 1,
            "source": item.get("source", ""),
            "summary": item.get("summary", ""),
            "manual_stance": item.get("stance", ""),
        })
    return out


def emit_multiturn(rec: dict, file_label: str, line_idx: int):
    """Multi-turn records have 'turns' list, each with its own 'encounter'."""
    out = []
    if rec.get("refused"):
        return out
    topic_id = rec.get("topic_id", "")
    if topic_id not in TOPICS:
        return out
    for t in rec.get("turns", []):
        for idx, item in enumerate(t.get("encounter", [])):
            out.append({
                "item_id": f"{file_label}:{line_idx}:t{t['turn']}:{idx}",
                "source_file": file_label,
                "arm": rec.get("arm", "multiturn"),
                "source_model": rec.get("source_model", "?"),
                "topic_id": topic_id,
                "topic_text": TOPICS[topic_id]["topic_text"],
                "pro_label": TOPICS[topic_id]["pro_label"],
                "con_label": TOPICS[topic_id]["con_label"],
                "framing": rec.get("framing", "?"),
                "turn": t["turn"],
                "source": item.get("source", ""),
                "summary": item.get("summary", ""),
                "manual_stance": item.get("stance", ""),
            })
    return out


def main():
    all_rows = []
    for fname in JSONL_FILES:
        path = RAW / fname
        if not path.exists():
            print(f"  skip missing: {fname}")
            continue
        with open(path) as f:
            for line_idx, line in enumerate(f):
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)
                if "turns" in rec:
                    rows = emit_multiturn(rec, fname, line_idx)
                else:
                    rows = emit_singleturn(rec, fname, line_idx)
                all_rows.extend(rows)

    with open(OUT, "w") as f:
        for r in all_rows:
            f.write(json.dumps(r) + "\n")
    print(f"Wrote {len(all_rows)} items to {OUT.name}")

    # Distribution summary
    by_arm = {}
    by_topic = {}
    by_model = {}
    by_stance = {}
    for r in all_rows:
        by_arm[r["arm"]] = by_arm.get(r["arm"], 0) + 1
        by_topic[r["topic_id"]] = by_topic.get(r["topic_id"], 0) + 1
        m = r["source_model"].replace("-via-agent", "")
        by_model[m] = by_model.get(m, 0) + 1
        by_stance[r["manual_stance"]] = by_stance.get(r["manual_stance"], 0) + 1
    print(f"\n  By arm: {by_arm}")
    print(f"  By topic: {by_topic}")
    print(f"  By model: {by_model}")
    print(f"  By manual stance: {by_stance}")


if __name__ == "__main__":
    main()
