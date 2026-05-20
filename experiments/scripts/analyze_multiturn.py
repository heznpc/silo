"""
analyze_multiturn.py -- Multi-turn temporal entropy trajectory (H6 test).

For each conversation in multiturn_*.jsonl, compute the *cumulative* stance
entropy after each turn. H6 prediction: framed conditions stay at floor;
neutral condition may decline if conversational entrenchment occurs.
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
import hoard_diversity as hd  # noqa: E402

DATA = Path(__file__).resolve().parent.parent / "results" / "raw" / "multiturn_20260521.jsonl"


def main() -> None:
    print(f"Loading {DATA.name}\n")
    convs = []
    with open(DATA) as f:
        for line in f:
            if line.strip():
                convs.append(json.loads(line))

    print("=" * 90)
    print("MULTI-TURN CUMULATIVE STANCE ENTROPY (H6 test)")
    print("=" * 90)
    print(f"{'conversation':<25s} {'turn':>4s} {'cum_n':>5s} {'p/n/c dist':<14s} {'H_cum':>8s}")
    print("-" * 90)

    for c in convs:
        label = c["conversation_id"]
        cumulative = []
        for t in c["turns"]:
            cumulative.extend(it["stance"] for it in t["encounter"])
            dist = Counter(cumulative)
            dstr = f"{dist.get('pro',0)}p/{dist.get('neutral',0)}n/{dist.get('con',0)}c"
            H = hd.stance_entropy(cumulative)
            print(f"{label:<25s} {t['turn']:>4d} {len(cumulative):>5d} {dstr:<14s} {H:>8.3f}")
        print()

    # Summary: turn 1 vs turn 5 cumulative entropy
    print("=" * 90)
    print("H6 PREDICTION TEST: cumulative entropy change from turn 1 to turn 5")
    print("=" * 90)
    print(f"{'conversation':<25s} {'H_turn1':>9s} {'H_turn5':>9s} {'delta':>8s} {'H6 verdict':>30s}")
    print("-" * 90)
    for c in convs:
        cums = {}
        cumlist = []
        for t in c["turns"]:
            cumlist.extend(it["stance"] for it in t["encounter"])
            cums[t["turn"]] = hd.stance_entropy(cumlist[:])
        H1, H5 = cums[1], cums[5]
        delta = H5 - H1
        if H1 < 0.1 and H5 < 0.1:
            verdict = "floor (already homogeneous)"
        elif delta < -0.05:
            verdict = "H6 SUPPORTED (declines)"
        elif delta > 0.05:
            verdict = "H6 REJECTED (rises)"
        else:
            verdict = "ambiguous (small change)"
        print(f"{c['conversation_id']:<25s} {H1:>9.3f} {H5:>9.3f} {delta:>+8.3f} {verdict:>30s}")


if __name__ == "__main__":
    main()
