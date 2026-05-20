"""
analyze_smoke.py -- Analyze the smoke-test JSONL.

Reports:
  - Per-cell encounter distribution and entropy
  - Save-subset entropy at beta in {0.0, 0.5, 1.0}
  - Refusal rates per model x framing
  - Aggregate (model, framing) means with simple SE
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
import hoard_diversity as hd            # noqa: E402
from save_filter import belief_weighted_save  # noqa: E402

BETA_SWEEP = [0.0, 0.5, 1.0]
K_SAVES = 5
SEED = 42

RAW_GLOB = Path(__file__).resolve().parent.parent / "results" / "raw"


def cohen_d(a: list[float], b: list[float]) -> float:
    a, b = np.asarray(a), np.asarray(b)
    if len(a) < 2 or len(b) < 2:
        return float("nan")
    pooled = np.sqrt(((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) /
                     (len(a) + len(b) - 2))
    if pooled == 0:
        # When variance is zero in both, fall back to mean-difference scale
        return float("inf") if a.mean() != b.mean() else 0.0
    return float((a.mean() - b.mean()) / pooled)


def boot_ci(values: list[float], n_boot: int = 10000, ci: float = 0.95,
            rng: np.random.Generator | None = None) -> tuple[float, float]:
    if not values:
        return float("nan"), float("nan")
    rng = rng or np.random.default_rng(SEED)
    arr = np.asarray(values)
    boots = rng.choice(arr, size=(n_boot, len(arr)), replace=True).mean(axis=1)
    lo, hi = np.quantile(boots, [(1 - ci) / 2, 1 - (1 - ci) / 2])
    return float(lo), float(hi)


def main() -> None:
    paths = sorted(RAW_GLOB.glob("smoke_*.jsonl"))
    if not paths:
        print(f"No smoke jsonl found in {RAW_GLOB}")
        sys.exit(1)

    print(f"Loading {len(paths)} file(s):")
    for p in paths:
        print(f"  {p.name}")

    records = []
    for p in paths:
        with open(p) as f:
            for line in f:
                line = line.strip()
                if line:
                    records.append(json.loads(line))

    n_refused = sum(1 for r in records if r.get("refused"))
    print(f"\nLoaded {len(records)} cell records ({n_refused} refusals).\n")

    rng = np.random.default_rng(SEED)

    # ===== Per-cell table =====
    print("=" * 110)
    print("PER-CELL")
    print("=" * 110)
    print(f"{'model':<8s} {'framing':<8s} {'rep':>3s} {'dist':<14s} {'H_enc':>7s} " +
          " ".join(f"H_save(b={b:.1f})" for b in BETA_SWEEP))
    print("-" * 110)

    cell_rows = []
    for r in records:
        model = r["source_model"].replace("-via-agent", "")
        if r.get("refused"):
            print(f"{model:<8s} {r['framing']:<8s} {r['rep']:>3d} {'REFUSED':<14s} {'--':>7s} {'--':>15s} {'--':>15s} {'--':>15s}")
            continue
        encounter = r["encounter"]
        stances = [it["stance"] for it in encounter]
        dist = Counter(stances)
        dist_str = f"{dist.get('pro',0)}p/{dist.get('neutral',0)}n/{dist.get('con',0)}c"
        H_enc = hd.stance_entropy(stances)

        if r["framing"] == "pro":
            prior = "pro"
        elif r["framing"] == "con":
            prior = "con"
        else:
            prior = "pro" if rng.random() < 0.5 else "con"

        H_saves = []
        for beta in BETA_SWEEP:
            saved = belief_weighted_save(encounter, k=K_SAVES, beta=beta, prior=prior, rng=rng)
            H_save = hd.stance_entropy([s["stance"] for s in saved])
            H_saves.append(H_save)

        print(f"{model:<8s} {r['framing']:<8s} {r['rep']:>3d} {dist_str:<14s} {H_enc:>7.3f} " +
              " ".join(f"{h:>15.3f}" for h in H_saves))
        cell_rows.append({
            "model": model, "framing": r["framing"], "rep": r["rep"],
            "dist": dist_str, "H_enc": H_enc,
            **{f"H_save_b{b:.1f}": H_saves[i] for i, b in enumerate(BETA_SWEEP)},
        })

    # ===== Aggregate by (model, framing) =====
    print("\n" + "=" * 110)
    print("AGGREGATE BY (MODEL x FRAMING)")
    print("=" * 110)
    print(f"{'model':<8s} {'framing':<8s} {'n':>3s} {'mean H_enc':>11s} " +
          " ".join(f"H_save(b={b:.1f})" for b in BETA_SWEEP))
    print("-" * 100)

    agg: dict[tuple[str, str], list[dict]] = {}
    for r in cell_rows:
        agg.setdefault((r["model"], r["framing"]), []).append(r)

    for (model, framing), rows in sorted(agg.items()):
        n = len(rows)
        mH = np.mean([r["H_enc"] for r in rows])
        mHs = [np.mean([r[f"H_save_b{b:.1f}"] for r in rows]) for b in BETA_SWEEP]
        print(f"{model:<8s} {framing:<8s} {n:>3d} {mH:>11.3f} " +
              " ".join(f"{h:>14.3f}" for h in mHs))

    # ===== Refusal rates =====
    print("\n" + "=" * 110)
    print("REFUSAL RATES (per model x framing)")
    print("=" * 110)
    by_model_framing: dict[tuple[str, str], dict] = {}
    for r in records:
        model = r["source_model"].replace("-via-agent", "")
        k = (model, r["framing"])
        d = by_model_framing.setdefault(k, {"total": 0, "refused": 0})
        d["total"] += 1
        if r.get("refused"):
            d["refused"] += 1
    print(f"{'model':<8s} {'framing':<8s} {'refused':>8s} / {'total':<5s}")
    print("-" * 40)
    for (model, framing), d in sorted(by_model_framing.items()):
        marker = " <-- !" if d["refused"] > 0 else ""
        print(f"{model:<8s} {framing:<8s} {d['refused']:>8d} / {d['total']:<5d}{marker}")

    # ===== Primary statistical contrast: LLM-pro vs LLM-con encounter entropy =====
    print("\n" + "=" * 110)
    print("PRIMARY CONTRAST: encounter-set entropy LLM-framed (pro+con) vs neutral")
    print("=" * 110)
    framed_H = [r["H_enc"] for r in cell_rows if r["framing"] in ("pro", "con")]
    neutral_H = [r["H_enc"] for r in cell_rows if r["framing"] == "neutral"]
    d = cohen_d(framed_H, neutral_H)
    lo, hi = boot_ci(framed_H)
    nlo, nhi = boot_ci(neutral_H)
    print(f"  Framed (n={len(framed_H)}): mean H_enc = {np.mean(framed_H):.3f}  95%CI [{lo:.3f}, {hi:.3f}]")
    print(f"  Neutral (n={len(neutral_H)}): mean H_enc = {np.mean(neutral_H):.3f}  95%CI [{nlo:.3f}, {nhi:.3f}]")
    print(f"  Cohen's d (framed - neutral): {d:.3f}")

    print("\n" + "=" * 110)
    print("SAVE-LAYER AMPLIFIER TEST (paper §3.3 central claim)")
    print("=" * 110)
    print("If save bias is a non-trivial amplifier, H_save(b=1.0) should be < H_enc")
    print("substantially across all cells. If encounter is already 0-entropy under")
    print("framing, save layer cannot amplify further.")
    print()
    for (model, framing), rows in sorted(agg.items()):
        mH = np.mean([r["H_enc"] for r in rows])
        mH1 = np.mean([r["H_save_b1.0"] for r in rows])
        delta = mH - mH1
        marker = "  <-- save amplifies" if delta > 0.05 else "  <-- save inert"
        print(f"  {model:<6s} {framing:<8s}: H_enc={mH:.3f}  H_save(b=1.0)={mH1:.3f}  delta={delta:+.3f}{marker}")


if __name__ == "__main__":
    main()
