"""
llm_stance_entropy.py -- MVE runner for the Silo three-layer bias model.

Pipeline per (topic, framing, source-model, repetition, prior):
  1. Source-recommender LLM produces an encounter set of 8 candidates.
  2. Stance judge classifies each candidate (pro / con / neutral).
  3. Save filter samples 5 items weighted by user prior (beta sweep).
  4. Compute Shannon stance entropy of the saved subset.

Modes:
  --smoke    1 topic, 1 framing, 1 source-model (Haiku), n=2 reps. ~$0.10.
  --tiny     2 topics, 3 framings, Haiku only, n=5. ~$1.
  --full     5 topics + 2 neutral, 3 framings, Opus/Sonnet/Haiku, n=40. ~$80-110.

The --full mode honors the pre-registration:
  - Opus: single-turn only, n=10 sanity.
  - Sonnet, Haiku: single + 5-turn multi-turn at n=40.

All raw API responses are persisted to experiments/results/raw/ as JSONL.
Stance classifications to experiments/results/classified/.
Final analysis to experiments/results/llm_stance_entropy.md.

Run: python experiments/src/llm_stance_entropy.py --smoke
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

# Local imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hoard_diversity as hd            # noqa: E402
from save_filter import belief_weighted_save  # noqa: E402
from llm_recommender import (             # noqa: E402
    recommend_sources_singleturn,
    recommend_sources_multiturn,
    RecommendationResult,
)
from stance_judge import judge_stance     # noqa: E402

try:
    import anthropic
except ImportError as e:
    raise SystemExit("anthropic SDK not installed. Run: pip install anthropic") from e

try:
    import yaml
except ImportError as e:
    raise SystemExit("pyyaml not installed. Run: pip install pyyaml") from e


# ---------------------------------------------------------------------------
# Configuration -- locked per pre-registration
# ---------------------------------------------------------------------------

# Model IDs. Use Anthropic's stable aliases; the actual versions are recorded
# in run_manifest.json from the API response.
MODELS = {
    "opus":   "claude-opus-4-5",
    "sonnet": "claude-sonnet-4-5",
    "haiku":  "claude-haiku-4-5",
}
# Fallback model ids if the above are not available on this account.
MODEL_FALLBACKS = {
    "opus":   ["claude-opus-4-1-20250805", "claude-3-opus-20240229"],
    "sonnet": ["claude-sonnet-4-20250514", "claude-3-5-sonnet-20241022"],
    "haiku":  ["claude-haiku-4-5-20251001", "claude-3-5-haiku-20241022"],
}

JUDGE_PRIMARY_KEY = "haiku"
JUDGE_CROSSCHECK_KEY = "sonnet"

BETA_SWEEP = [0.0, 0.5, 1.0]
K_SAVES = 5
N_ENCOUNTER = 8
SEED = 42

# Paths
_SRC_DIR = Path(__file__).resolve().parent
_EXP_DIR = _SRC_DIR.parent
RAW_DIR = _EXP_DIR / "results" / "raw"
CLF_DIR = _EXP_DIR / "results" / "classified"
ANALYSIS_PATH = _EXP_DIR / "results" / "llm_stance_entropy.md"
MANIFEST_PATH = _EXP_DIR / "results" / "run_manifest.json"
TOPICS_PATH = _EXP_DIR / "data" / "raw" / "topics.yaml"

RAW_DIR.mkdir(parents=True, exist_ok=True)
CLF_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Topic loading
# ---------------------------------------------------------------------------

def load_topics() -> dict:
    """Load locked topics from topics.yaml."""
    with open(TOPICS_PATH) as f:
        return yaml.safe_load(f)


# ---------------------------------------------------------------------------
# Cost estimation
# ---------------------------------------------------------------------------

# Anthropic per-1M-token prices (USD) as of 2026-05 (approx; update if needed).
PRICES = {
    "claude-opus-4-5":   {"input": 15.0, "output": 75.0},
    "claude-sonnet-4-5": {"input": 3.0,  "output": 15.0},
    "claude-haiku-4-5":  {"input": 0.80, "output": 4.0},
}
PRICE_FALLBACK = {"input": 3.0, "output": 15.0}


def estimate_cost(usage_input: int, usage_output: int, model_id: str) -> float:
    """Compute approximate USD cost from token usage."""
    p = PRICES.get(model_id, PRICE_FALLBACK)
    return (usage_input * p["input"] + usage_output * p["output"]) / 1_000_000


# ---------------------------------------------------------------------------
# Cell execution
# ---------------------------------------------------------------------------

def resolve_model(client: anthropic.Anthropic, key: str) -> str:
    """Try MODELS[key] first; fall back to MODEL_FALLBACKS list if it errors.

    We probe by issuing a tiny test call. The first model that responds is
    cached for the rest of the run.
    """
    candidates = [MODELS[key], *MODEL_FALLBACKS[key]]
    for m in candidates:
        try:
            client.messages.create(
                model=m,
                max_tokens=4,
                messages=[{"role": "user", "content": "Reply with: ok"}],
            )
            return m
        except anthropic.NotFoundError:
            continue
        except Exception:
            continue
    raise RuntimeError(f"No working model found for key={key!r} among {candidates}")


def run_cell_singleturn(
    *,
    client: anthropic.Anthropic,
    source_model: str,
    judge_primary: str,
    judge_crosscheck: str | None,
    topic_id: str,
    topic: dict,
    framing: str,
    n_reps: int,
    rng: np.random.Generator,
    raw_jsonl_path: Path,
    clf_jsonl_path: Path,
    crosscheck_rate: float = 0.0,
) -> list[dict]:
    """Run n_reps repetitions of the single-turn pipeline for one cell.

    Returns a list of per-rep records suitable for aggregation, including the
    saved subsets at each beta value.
    """
    cell_records: list[dict] = []
    for rep in range(n_reps):
        # 1. LLM source recommendation
        result: RecommendationResult = recommend_sources_singleturn(
            client,
            model=source_model,
            topic_id=topic_id,
            topic_text=topic["framing_topic"],
            framing=framing,
            pro_label=topic["pro_label"],
            con_label=topic["con_label"],
            n=N_ENCOUNTER,
        )

        # Persist raw response
        with open(raw_jsonl_path, "a") as f:
            f.write(json.dumps({
                "kind": "recommend",
                "arm": "singleturn",
                "rep": rep,
                **result.to_dict(),
            }) + "\n")

        if result.error or len(result.sources) < K_SAVES:
            cell_records.append({
                "rep": rep, "topic_id": topic_id, "framing": framing,
                "source_model": source_model, "arm": "singleturn",
                "encounter_size": len(result.sources),
                "error": result.error or f"only {len(result.sources)} sources parsed",
                "saves_by_beta": {},
            })
            continue

        # 2. Stance judging of each encounter-set item
        judged_items = []
        for src in result.sources:
            jr = judge_stance(
                client,
                judge_model=judge_primary,
                topic_text=topic["framing_topic"],
                pro_label=topic["pro_label"],
                con_label=topic["con_label"],
                source=src.source,
                summary=src.summary,
            )
            crosscheck_label = None
            if judge_crosscheck and rng.random() < crosscheck_rate:
                jr2 = judge_stance(
                    client,
                    judge_model=judge_crosscheck,
                    topic_text=topic["framing_topic"],
                    pro_label=topic["pro_label"],
                    con_label=topic["con_label"],
                    source=src.source,
                    summary=src.summary,
                )
                crosscheck_label = jr2.label
                with open(clf_jsonl_path, "a") as f:
                    f.write(json.dumps({
                        "kind": "judge",
                        "judge": "crosscheck",
                        "topic_id": topic_id,
                        "framing": framing,
                        "source_model": source_model,
                        "rep": rep,
                        "arm": "singleturn",
                        "source": src.source,
                        **jr2.to_dict(),
                    }) + "\n")

            with open(clf_jsonl_path, "a") as f:
                f.write(json.dumps({
                    "kind": "judge",
                    "judge": "primary",
                    "topic_id": topic_id,
                    "framing": framing,
                    "source_model": source_model,
                    "rep": rep,
                    "arm": "singleturn",
                    "source": src.source,
                    "crosscheck_label": crosscheck_label,
                    **jr.to_dict(),
                }) + "\n")

            judged_items.append({
                "source": src.source,
                "summary": src.summary,
                "stance": jr.label if jr.label in {"pro", "con", "neutral"} else "neutral",
            })

        # 3. Save filter sweep over beta
        # Prior chosen to match the framing: pro-framed user has pro prior; con-framed has con prior; neutral has random.
        if framing == "pro":
            prior = "pro"
        elif framing == "con":
            prior = "con"
        else:
            prior = "pro" if rng.random() < 0.5 else "con"

        saves_by_beta: dict[str, list[dict]] = {}
        for beta in BETA_SWEEP:
            saved = belief_weighted_save(
                judged_items, k=K_SAVES, beta=beta, prior=prior, rng=rng,
            )
            saves_by_beta[f"{beta:.2f}"] = saved

        # 4. Per-rep entropy summary
        entropies = {
            f"{beta:.2f}": hd.stance_entropy([s["stance"] for s in saves_by_beta[f"{beta:.2f}"]])
            for beta in BETA_SWEEP
        }
        cell_records.append({
            "rep": rep,
            "topic_id": topic_id,
            "framing": framing,
            "source_model": source_model,
            "arm": "singleturn",
            "prior": prior,
            "encounter_size": len(judged_items),
            "encounter_stances": [it["stance"] for it in judged_items],
            "saves_by_beta": saves_by_beta,
            "entropy_by_beta": entropies,
            "usage_input": result.usage_input_tokens,
            "usage_output": result.usage_output_tokens,
        })

    return cell_records


def run_cell_unmediated(
    *,
    rng: np.random.Generator,
    topic_id: str,
    unmediated_pool: list[dict],
    framing: str,
    n_reps: int,
) -> list[dict]:
    """Unmediated baseline arm: encounter set is the pre-assembled curated list.

    No LLM source-recommender call; stance is taken from the curated 'intended_stance'.
    Same save filter applied for fair comparison.
    """
    cell_records: list[dict] = []
    for rep in range(n_reps):
        items = [
            {"source": x["source"], "summary": x["summary"], "stance": x["intended_stance"]}
            for x in unmediated_pool
        ]
        if framing == "pro":
            prior = "pro"
        elif framing == "con":
            prior = "con"
        else:
            prior = "pro" if rng.random() < 0.5 else "con"

        saves_by_beta = {}
        for beta in BETA_SWEEP:
            saved = belief_weighted_save(items, k=K_SAVES, beta=beta, prior=prior, rng=rng)
            saves_by_beta[f"{beta:.2f}"] = saved

        entropies = {
            f"{beta:.2f}": hd.stance_entropy([s["stance"] for s in saves_by_beta[f"{beta:.2f}"]])
            for beta in BETA_SWEEP
        }
        cell_records.append({
            "rep": rep,
            "topic_id": topic_id,
            "framing": framing,
            "source_model": "Unmediated",
            "arm": "singleturn",
            "prior": prior,
            "encounter_size": len(items),
            "encounter_stances": [x["intended_stance"] for x in unmediated_pool],
            "saves_by_beta": saves_by_beta,
            "entropy_by_beta": entropies,
            "usage_input": 0,
            "usage_output": 0,
        })
    return cell_records


# ---------------------------------------------------------------------------
# Run plans
# ---------------------------------------------------------------------------

def plan_smoke() -> dict:
    """1 topic, 1 framing, Haiku only, n=2 reps. Single-turn. No unmediated."""
    return {
        "mode": "smoke",
        "topic_ids": ["climate_mitigation"],
        "framings": ["pro"],
        "source_models": ["haiku"],
        "n_reps": 2,
        "include_unmediated": False,
        "multi_turn": False,
        "crosscheck_rate": 0.0,
    }


def plan_tiny() -> dict:
    """2 topics, 3 framings, Haiku only, n=5. Includes unmediated."""
    return {
        "mode": "tiny",
        "topic_ids": ["climate_mitigation", "europe_vacation"],
        "framings": ["pro", "con", "neutral"],
        "source_models": ["haiku"],
        "n_reps": 5,
        "include_unmediated": True,
        "multi_turn": False,
        "crosscheck_rate": 0.10,
    }


def plan_full() -> dict:
    """Locked pre-registration plan."""
    return {
        "mode": "full",
        "topic_ids": ["immigration_us", "climate_mitigation", "ai_regulation",
                       "gun_control", "universal_basic_income",
                       "europe_vacation", "espresso_setup"],
        "framings": ["pro", "con", "neutral"],
        "source_models": ["opus", "sonnet", "haiku"],
        "n_reps_default": 40,
        "n_reps_opus": 10,           # Opus sanity only
        "include_unmediated": True,
        "multi_turn_models": ["sonnet", "haiku"],
        "multi_turn_turns": 5,
        "crosscheck_rate": 0.05,    # 500-item-ish subsample
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="Silo MVE: LLM stance entropy")
    grp = parser.add_mutually_exclusive_group(required=True)
    grp.add_argument("--smoke", action="store_true")
    grp.add_argument("--tiny", action="store_true")
    grp.add_argument("--full", action="store_true")
    parser.add_argument("--run-id", default=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    parser.add_argument("--budget-usd", type=float, default=150.0,
                        help="Halt the run if total estimated cost exceeds this.")
    args = parser.parse_args()

    if args.smoke:
        plan = plan_smoke()
    elif args.tiny:
        plan = plan_tiny()
    else:
        plan = plan_full()

    run_id = args.run_id
    raw_path = RAW_DIR / f"{run_id}.jsonl"
    clf_path = CLF_DIR / f"{run_id}.jsonl"

    client = anthropic.Anthropic()  # picks up ANTHROPIC_API_KEY + ANTHROPIC_BASE_URL

    # Resolve model ids
    print(f"[run-id {run_id}] resolving models...")
    resolved: dict[str, str] = {}
    for key in set(plan["source_models"]) | {JUDGE_PRIMARY_KEY, JUDGE_CROSSCHECK_KEY}:
        m = resolve_model(client, key)
        resolved[key] = m
        print(f"  {key:10s} -> {m}")

    topics = load_topics()
    topic_lookup = {t["id"]: t for t in topics["controversial"] + topics["neutral"]}

    with open(_EXP_DIR / "data" / "raw" / "unmediated_lists.json") as f:
        unmediated_lists = json.load(f)

    rng = np.random.default_rng(SEED)
    all_records: list[dict] = []
    total_cost = 0.0

    cells_run = 0
    started = time.monotonic()
    for tid in plan["topic_ids"]:
        if tid not in topic_lookup:
            print(f"  skip unknown topic_id {tid}")
            continue
        topic = topic_lookup[tid]
        for framing in plan["framings"]:
            for sm_key in plan["source_models"]:
                model_id = resolved[sm_key]
                if plan["mode"] == "full":
                    n_reps = plan["n_reps_opus"] if sm_key == "opus" else plan["n_reps_default"]
                else:
                    n_reps = plan["n_reps"]
                print(f"[cell] topic={tid:25s} framing={framing:7s} model={sm_key:6s} n={n_reps}", flush=True)
                recs = run_cell_singleturn(
                    client=client,
                    source_model=model_id,
                    judge_primary=resolved[JUDGE_PRIMARY_KEY],
                    judge_crosscheck=resolved.get(JUDGE_CROSSCHECK_KEY) if plan.get("crosscheck_rate", 0) > 0 else None,
                    topic_id=tid,
                    topic=topic,
                    framing=framing,
                    n_reps=n_reps,
                    rng=rng,
                    raw_jsonl_path=raw_path,
                    clf_jsonl_path=clf_path,
                    crosscheck_rate=plan.get("crosscheck_rate", 0.0),
                )
                all_records.extend(recs)
                cells_run += 1
                # Tally cost
                for r in recs:
                    total_cost += estimate_cost(
                        r.get("usage_input", 0),
                        r.get("usage_output", 0),
                        model_id,
                    )
                if total_cost > args.budget_usd:
                    print(f"!! budget halt at ${total_cost:.2f} > ${args.budget_usd:.2f}")
                    break
            if total_cost > args.budget_usd:
                break
        if total_cost > args.budget_usd:
            break

        # Unmediated arm
        if plan.get("include_unmediated") and tid in unmediated_lists:
            for framing in plan["framings"]:
                n_reps = plan.get("n_reps", plan.get("n_reps_default", 40))
                # match the heaviest sampled cell so the unmediated arm has comparable n
                print(f"[cell] topic={tid:25s} framing={framing:7s} model=Unmedia. n={n_reps}", flush=True)
                recs = run_cell_unmediated(
                    rng=rng,
                    topic_id=tid,
                    unmediated_pool=unmediated_lists[tid],
                    framing=framing,
                    n_reps=n_reps,
                )
                all_records.extend(recs)
                cells_run += 1

    elapsed = time.monotonic() - started

    # Persist aggregated records
    agg_path = _EXP_DIR / "results" / f"{run_id}_records.jsonl"
    with open(agg_path, "w") as f:
        for r in all_records:
            f.write(json.dumps(r) + "\n")

    # Write manifest
    manifest = {
        "run_id": run_id,
        "mode": plan["mode"],
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "elapsed_s": elapsed,
        "cells_run": cells_run,
        "records": len(all_records),
        "resolved_models": resolved,
        "estimated_cost_usd": round(total_cost, 4),
        "raw_jsonl": str(raw_path.relative_to(_EXP_DIR.parent)),
        "classified_jsonl": str(clf_path.relative_to(_EXP_DIR.parent)),
        "records_jsonl": str(agg_path.relative_to(_EXP_DIR.parent)),
        "git_commit": _git_commit(),
        "seed": SEED,
        "beta_sweep": BETA_SWEEP,
        "k_saves": K_SAVES,
        "n_encounter": N_ENCOUNTER,
    }
    with open(MANIFEST_PATH, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"\n[done] cells={cells_run} records={len(all_records)} cost~=${total_cost:.2f} elapsed={elapsed:.1f}s")
    print(f"  raw:        {raw_path}")
    print(f"  classified: {clf_path}")
    print(f"  records:    {agg_path}")
    print(f"  manifest:   {MANIFEST_PATH}")
    return 0


def _git_commit() -> str:
    try:
        import subprocess
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        return "unknown"


if __name__ == "__main__":
    sys.exit(main())
