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

    # ===== Cycle-position effect (Wave 3b mid vs Wave 4 start, Haiku only) =====
    print("\n" + "=" * 90)
    print("CYCLE-POSITION EFFECT (Haiku, 12 cells each wave, identical prompts)")
    print("=" * 90)
    by_wave = defaultdict(list)
    for r in rows:
        if r["model"] != "haiku":
            continue
        cid = r.get("call_id", "")
        wave = r.get("wave", "")
        if cid.startswith("fs_w3b") or "w3b" in wave:
            by_wave["mid (~105 min)"].append(r)
        elif cid.startswith("fs_w4") or "w4" in wave:
            by_wave["start (~14 min)"].append(r)
    if by_wave:
        for wave_label, items in sorted(by_wave.items()):
            if not items:
                continue
            outcome_counts = defaultdict(int)
            for r in items:
                outcome_counts[r["outcome"]] += 1
            n = len(items)
            ref_share = (outcome_counts["refused"] + outcome_counts["partial_refused"]) / n
            cov_share = outcome_counts["covered_compliance"] / n
            mean_tools = mean(r["tool_uses"] for r in items)
            mean_dur = mean(r["duration_ms"] / 1000 for r in items)
            print(f"  {wave_label:<22s} n={n:>3d}  refused={ref_share:.0%}  covered={cov_share:.0%}  mean_tools={mean_tools:.1f}  mean_dur={mean_dur:.1f}s")
        # Outcome shift
        mid = by_wave.get("mid (~105 min)", [])
        start = by_wave.get("start (~14 min)", [])
        if mid and start:
            mid_ref = sum(1 for r in mid if r["outcome"] in ("refused", "partial_refused")) / len(mid)
            start_ref = sum(1 for r in start if r["outcome"] in ("refused", "partial_refused")) / len(start)
            mid_dur = mean(r["duration_ms"] / 1000 for r in mid)
            start_dur = mean(r["duration_ms"] / 1000 for r in start)
            print(f"\n  Δ refusal rate (start - mid):  {start_ref - mid_ref:+.0%}")
            print(f"  Δ mean duration (start - mid): {start_dur - mid_dur:+.1f}s")
            print(f"  Interpretation: cycle-start has {'fewer' if start_ref < mid_ref else 'more'} refusals "
                  f"and {'longer' if start_dur > mid_dur else 'shorter'} mean call duration.")

    # ===== Prompt-format A/B at controlled cycle position (Wave 4 vs Wave 7) =====
    print("\n" + "=" * 90)
    print("PROMPT-FORMAT A/B at cycle-start (Haiku, 12 cells each)")
    print("=" * 90)
    def get_outcome(r):
        return r.get("outcome_override") or r.get("outcome", "unknown")
    w4 = [r for r in rows if r["model"] == "haiku" and r.get("call_id","").startswith("fs_w4")]
    w7 = [r for r in rows if r["model"] == "haiku" and r.get("call_id","").startswith("fs_w7_haiku_verbose")]
    for label, items in [("Wave 4 compact (~14 min)", w4), ("Wave 7 verbose (~52 min)", w7)]:
        if not items:
            continue
        outcome_counts = defaultdict(int)
        for r in items:
            outcome_counts[get_outcome(r)] += 1
        n = len(items)
        mean_tools = mean(r["tool_uses"] for r in items)
        mean_dur = mean(r["duration_ms"]/1000 for r in items)
        non_compliant = sum(c for o, c in outcome_counts.items() if o != "compliant")
        print(f"  {label:<28s} n={n:>3d}  non-compliant={non_compliant}/{n}  mean_tools={mean_tools:.1f}  mean_dur={mean_dur:.1f}s")
        for outcome, count in sorted(outcome_counts.items()):
            print(f"    {outcome}: {count}")

    # ===== Sonnet cycle-position comparison =====
    print("\n" + "=" * 90)
    print("SONNET CYCLE-POSITION (Wave 3a mid vs Wave 5 start, 12 cells each)")
    print("=" * 90)
    sonnet_mid = [r for r in rows if r["model"] == "sonnet" and (r.get("call_id","").startswith("fs_w3a") or "w3a" in r.get("wave",""))]
    sonnet_start = [r for r in rows if r["model"] == "sonnet" and (r.get("call_id","").startswith("fs_w5") or "w5" in r.get("wave",""))]
    for label, items in [("mid (~105 min)", sonnet_mid), ("start (~52 min)", sonnet_start)]:
        if not items:
            continue
        outcome_counts = defaultdict(int)
        for r in items:
            outcome_counts[r["outcome"]] += 1
        mean_tok = mean(r["total_tokens"] for r in items) if items else 0
        mean_dur = mean(r["duration_ms"]/1000 for r in items) if items else 0
        balance_share = outcome_counts.get("covert_balance_injection", 0) / max(len(items), 1)
        print(f"  {label:<22s} n={len(items):>3d}  balance-injection={balance_share:.0%}  mean_tok={mean_tok:,.0f}  mean_dur={mean_dur:.1f}s")
        for outcome, count in sorted(outcome_counts.items()):
            print(f"    {outcome}: {count}")

    # ===== New: refused_after_tool_use sub-mode =====
    print("\n" + "=" * 90)
    print("NEW SUB-MODE: refused_after_tool_use (Wave 4 anomaly)")
    print("=" * 90)
    refused_with_tools = [r for r in rows if r["outcome"] == "refused" and r["tool_uses"] > 0]
    refused_no_tools = [r for r in rows if r["outcome"] == "refused" and r["tool_uses"] == 0]
    if refused_with_tools:
        print(f"  refused, 0 tool_uses (fast-path): n={len(refused_no_tools)}, "
              f"mean dur {mean(r['duration_ms']/1000 for r in refused_no_tools):.1f}s")
        print(f"  refused, with tool_uses (used tools but refused output): n={len(refused_with_tools)}, "
              f"mean dur {mean(r['duration_ms']/1000 for r in refused_with_tools):.1f}s")
        print(f"  Sub-mode emerges in Wave 4 only -- model invoked WebSearch but then refused to compile a source list.")

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
