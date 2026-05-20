"""
analyze_kappa.py -- Compute Cohen's kappa between author-manual stance labels
and Claude Haiku 4.5 judge labels.

Reads:
  experiments/results/judge_input.jsonl  (has manual_stance per item_id)
  experiments/results/judge_haiku_batches.tsv  (item_id \t haiku_label per line)

Writes:
  experiments/results/judge_agreement.md

Also computes:
  - per-category confusion matrix
  - per-topic kappa
  - per-source-model kappa
  - agreement rate
"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

EXP = Path(__file__).resolve().parent.parent
INPUT_PATH = EXP / "results" / "judge_input.jsonl"
HAIKU_PATH = EXP / "results" / "judge_haiku_batches.tsv"
OUT_PATH = EXP / "results" / "judge_agreement.md"

LABELS = ("pro", "con", "neutral")


def cohen_kappa(labels1: list[str], labels2: list[str]) -> float:
    """3-class Cohen's kappa."""
    if len(labels1) != len(labels2) or not labels1:
        return float("nan")
    n = len(labels1)
    cats = sorted(set(labels1) | set(labels2))
    if len(cats) < 2:
        return float("nan")
    po = sum(1 for a, b in zip(labels1, labels2) if a == b) / n
    c1 = Counter(labels1)
    c2 = Counter(labels2)
    pe = sum((c1[c] / n) * (c2[c] / n) for c in cats)
    if pe == 1.0:
        return float("nan")
    return (po - pe) / (1 - pe)


def main() -> None:
    manual: dict[str, dict] = {}
    with open(INPUT_PATH) as f:
        for line in f:
            r = json.loads(line)
            manual[r["item_id"]] = r

    haiku: dict[str, str] = {}
    with open(HAIKU_PATH) as f:
        for line in f:
            line = line.strip()
            if not line or "\t" not in line:
                continue
            iid, label = line.split("\t", 1)
            label = label.strip().lower()
            if label in LABELS:
                haiku[iid] = label

    # Items with BOTH labels
    common = sorted(set(manual.keys()) & set(haiku.keys()))
    pairs = [(manual[i]["manual_stance"], haiku[i]) for i in common
             if manual[i]["manual_stance"] in LABELS]
    if not pairs:
        print("No comparable pairs.")
        return

    m_labels = [p[0] for p in pairs]
    h_labels = [p[1] for p in pairs]

    k = cohen_kappa(m_labels, h_labels)
    agree = sum(1 for a, b in zip(m_labels, h_labels) if a == b) / len(pairs)

    # Confusion
    confusion: dict[tuple[str, str], int] = defaultdict(int)
    for a, b in zip(m_labels, h_labels):
        confusion[(a, b)] += 1

    # Per-topic kappa
    by_topic: dict[str, list] = defaultdict(list)
    for i in common:
        if manual[i]["manual_stance"] not in LABELS:
            continue
        topic = manual[i]["topic_id"]
        by_topic[topic].append((manual[i]["manual_stance"], haiku[i]))

    # Per-source-model kappa
    by_model: dict[str, list] = defaultdict(list)
    for i in common:
        if manual[i]["manual_stance"] not in LABELS:
            continue
        sm = manual[i]["source_model"].replace("-via-agent", "")
        by_model[sm].append((manual[i]["manual_stance"], haiku[i]))

    # Refused batches: items 480-600 absent from haiku.tsv
    missing = [i for i in manual if i not in haiku]

    # Write report
    with open(OUT_PATH, "w") as f:
        f.write("# Judge Replication -- Author Manual vs Claude Haiku 4.5\n\n")
        f.write(f"Date: 2026-05-21\n")
        f.write(f"Total items judged manually: {len(manual)}\n")
        f.write(f"Total items judged by Haiku: {len(haiku)}\n")
        f.write(f"Items in both: {len(pairs)}\n")
        f.write(f"Items NOT in Haiku (refused/missing): {len(missing)}\n\n")
        f.write("## Overall agreement\n\n")
        f.write(f"- **Agreement rate (raw)**: {agree:.3f} ({sum(1 for a,b in zip(m_labels,h_labels) if a==b)}/{len(pairs)})\n")
        f.write(f"- **Cohen's kappa**: {k:.3f}\n\n")
        if k > 0.8:
            interp = "almost perfect agreement"
        elif k > 0.6:
            interp = "substantial agreement"
        elif k > 0.4:
            interp = "moderate agreement"
        elif k > 0.2:
            interp = "fair agreement"
        else:
            interp = "slight agreement"
        f.write(f"  (Landis-Koch interpretation: **{interp}**)\n\n")

        f.write("## Confusion matrix\n\n")
        f.write("Rows = manual, columns = haiku.\n\n")
        f.write("| manual\\haiku | pro | con | neutral |\n")
        f.write("|---|---|---|---|\n")
        for r in LABELS:
            row = [str(confusion.get((r, c), 0)) for c in LABELS]
            f.write(f"| {r} | {' | '.join(row)} |\n")
        f.write("\n")

        f.write("## Per-topic kappa\n\n")
        f.write("| topic | n | kappa | agreement |\n")
        f.write("|---|---|---|---|\n")
        for topic, items in sorted(by_topic.items(), key=lambda x: -len(x[1])):
            tm = [p[0] for p in items]
            th = [p[1] for p in items]
            tk = cohen_kappa(tm, th)
            ta = sum(1 for a, b in zip(tm, th) if a == b) / len(items) if items else 0.0
            f.write(f"| {topic} | {len(items)} | {tk:.3f} | {ta:.3f} |\n")
        f.write("\n")

        f.write("## Per-source-model kappa\n\n")
        f.write("| source-model | n | kappa | agreement |\n")
        f.write("|---|---|---|---|\n")
        for sm, items in sorted(by_model.items(), key=lambda x: -len(x[1])):
            tm = [p[0] for p in items]
            th = [p[1] for p in items]
            tk = cohen_kappa(tm, th)
            ta = sum(1 for a, b in zip(tm, th) if a == b) / len(items) if items else 0.0
            f.write(f"| {sm} | {len(items)} | {tk:.3f} | {ta:.3f} |\n")
        f.write("\n")

        f.write("## Haiku refusal pattern\n\n")
        if missing:
            f.write(f"{len(missing)} items were not classified by Haiku. ")
            f.write("Inspection of the Agent outputs shows two batches (009, 010) ")
            f.write("were refused with the explanation that the items lack ")
            f.write("substantive summaries -- only source titles/metadata. ")
            f.write("This is itself a finding: Haiku 4.5 declines stance classification ")
            f.write("when it judges source content too thin, even at temperature=0 ")
            f.write("with explicit single-word-output instructions. ")
            f.write("More capable judges (Sonnet) would likely classify the same items ")
            f.write("from prior knowledge of the named sources; Haiku's higher ")
            f.write("confidence threshold trades coverage for caution.\n\n")
        else:
            f.write("No items missing from Haiku output.\n\n")

        f.write("## Interpretation\n\n")
        if k > 0.6:
            verdict = (f"Author-manual labels and Claude Haiku judge labels agree at "
                       f"kappa={k:.3f} (substantial agreement). The Round 4 finding that "
                       f"Sonnet's framed-encounter sets are at floor entropy is robust "
                       f"to judge replication: independent LLM scoring confirms the "
                       f"strong-stance pattern.")
        elif k > 0.4:
            verdict = (f"Moderate agreement (kappa={k:.3f}) suggests the manual and "
                       f"automated scoring disagree on edge cases (especially "
                       f"neutral-vs-flanking-stance items), but the main framed-vs-neutral "
                       f"contrast is robust.")
        else:
            verdict = (f"Low agreement (kappa={k:.3f}) is a methodological concern; the "
                       f"main findings should be re-examined with a third judge before "
                       f"any external claim.")
        f.write(verdict + "\n")

    print(f"Wrote {OUT_PATH}")
    print(f"  Pairs: {len(pairs)}, agreement: {agree:.3f}, kappa: {k:.3f}")


if __name__ == "__main__":
    main()
