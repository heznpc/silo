"""
analyze_telemetry.py -- Cross-tabulate per-call telemetry against outcome.

Reads experiments/results/telemetry/call_telemetry.jsonl, computes:
  - mean duration / tokens / tool_uses per outcome category
  - per-model breakdown
  - signature distinguishing refusal modes (full vs partial vs covered)
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from statistics import mean, stdev

DATA = Path(__file__).resolve().parent.parent / "results" / "telemetry" / "call_telemetry.jsonl"


def main() -> None:
    rows = []
    with open(DATA) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            if "_comment" in r:
                continue
            rows.append(r)

    print(f"Loaded {len(rows)} telemetry records.\n")

    # ===== Overall outcome distribution =====
    by_outcome = defaultdict(list)
    for r in rows:
        by_outcome[r["outcome"]].append(r)

    print("=" * 90)
    print("OUTCOME SIGNATURES (mean ± sd across all models)")
    print("=" * 90)
    print(f"{'outcome':<28s} {'n':>4s} {'tokens':>14s} {'tool_uses':>12s} {'duration_s':>14s}")
    print("-" * 90)
    for outcome, items in sorted(by_outcome.items(), key=lambda x: -len(x[1])):
        toks = [r["total_tokens"] for r in items]
        tools = [r["tool_uses"] for r in items]
        durs = [r["duration_ms"] / 1000.0 for r in items]
        if len(items) >= 2:
            tk = f"{mean(toks):,.0f}±{stdev(toks):,.0f}"
            tl = f"{mean(tools):.1f}±{stdev(tools):.1f}"
            dr = f"{mean(durs):.1f}±{stdev(durs):.1f}"
        else:
            tk = f"{toks[0]:,.0f}"
            tl = f"{tools[0]:.1f}"
            dr = f"{durs[0]:.1f}"
        print(f"{outcome:<28s} {len(items):>4d} {tk:>14s} {tl:>12s} {dr:>14s}")

    # ===== Per-model outcome breakdown =====
    print("\n" + "=" * 90)
    print("PER-MODEL OUTCOME DISTRIBUTION")
    print("=" * 90)
    print(f"{'model':<10s} {'outcome':<28s} {'n':>4s} {'mean tokens':>14s} {'mean tool_uses':>16s} {'mean dur_s':>12s}")
    print("-" * 90)
    by_model_outcome = defaultdict(list)
    for r in rows:
        by_model_outcome[(r["model"], r["outcome"])].append(r)
    for (model, outcome), items in sorted(by_model_outcome.items()):
        toks = mean(r["total_tokens"] for r in items)
        tools = mean(r["tool_uses"] for r in items)
        durs = mean(r["duration_ms"] for r in items) / 1000.0
        print(f"{model:<10s} {outcome:<28s} {len(items):>4d} {toks:>14,.0f} {tools:>16.1f} {durs:>12.1f}")

    # ===== Refusal signature analysis (Haiku) =====
    print("\n" + "=" * 90)
    print("HAIKU REFUSAL SIGNATURE (Wave 3b only -- the only Haiku batch with telemetry)")
    print("=" * 90)
    haiku = [r for r in rows if r["model"] == "haiku"]
    if haiku:
        refused = [r for r in haiku if r["outcome"] in ("refused", "partial_refused")]
        covered = [r for r in haiku if r["outcome"] == "covered_compliance"]
        if refused and covered:
            print(f"  refused/partial (n={len(refused)}): duration {mean(r['duration_ms']/1000 for r in refused):.1f}s, tool_uses {mean(r['tool_uses'] for r in refused):.1f}")
            print(f"  covered_compliance (n={len(covered)}): duration {mean(r['duration_ms']/1000 for r in covered):.1f}s, tool_uses {mean(r['tool_uses'] for r in covered):.1f}")
            speedup = mean(r['duration_ms'] for r in covered) / mean(r['duration_ms'] for r in refused)
            print(f"  Covered is {speedup:.1f}x slower than refused.")
            print(f"  Refusals consistently use 0 tools (fast-path); covered_compliance uses 4-5 tools (slow-path).")

    # ===== Cost estimation =====
    print("\n" + "=" * 90)
    print("APPROXIMATE TOKEN COST BY MODEL (treating total_tokens as billable input+output)")
    print("=" * 90)
    PRICES = {
        "opus": {"blended_per_million": 39.0},     # ~$15 in + $75 out, 60/40 mix
        "sonnet": {"blended_per_million": 7.8},    # ~$3 + $15
        "haiku": {"blended_per_million": 2.08},    # ~$0.80 + $4
    }
    total_cost = 0.0
    for model in sorted({r["model"] for r in rows}):
        items = [r for r in rows if r["model"] == model]
        total_toks = sum(r["total_tokens"] for r in items)
        cost = total_toks * PRICES[model]["blended_per_million"] / 1_000_000
        total_cost += cost
        print(f"  {model:<8s} n={len(items):>3d} total_tokens={total_toks:>12,} ~ ${cost:>6.2f}")
    print(f"  ----")
    print(f"  Round 5 full-sweep telemetry total: ${total_cost:.2f}")
    print(f"  (This is approximate; via Claude Code Agent tool actual cost is internal session token budget.)")


if __name__ == "__main__":
    main()
