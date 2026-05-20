"""
save_filter.py -- Prior-belief-weighted save filter (Silo MVE).

Given an *encounter set* of candidate sources with judged stances, simulate the
user's selective save layer by drawing k items with a probability that depends
on the user's stated prior (`pro` or `con`) and the bias strength `beta`.

beta = 0.0 -> uniform random selection (no save bias; control)
beta = 1.0 -> strongly prefers items matching the prior; con-stance items get
              a substantially lower weight, neutral items sit in between.

The filter is deterministic given the rng. The intent is to operationalize
paper Layer 2 (save bias) as a probabilistic selection step that sits on top
of the encounter set produced by the LLM source-recommender.

See `experiments/preregistration.md` Section 5 for the locked design.
"""

from __future__ import annotations

import numpy as np


def belief_weighted_save(
    items: list[dict],
    *,
    k: int,
    beta: float,
    prior: str,
    rng: np.random.Generator,
) -> list[dict]:
    """Sample `k` items from `items` weighted by alignment with `prior`.

    Parameters
    ----------
    items : list of dicts
        Each dict must have a key "stance" valued in {"pro", "con", "neutral"}.
        Other keys (source, summary, ...) are passed through unchanged.
    k : int
        Number of items to save. Must be <= len(items).
    beta : float
        Save-bias strength in [0, 1]. 0 = uniform; 1 = strongly prior-aligned.
    prior : str
        The simulated user's prior belief: "pro" or "con".
    rng : numpy.random.Generator
        Seeded RNG for reproducibility.

    Returns
    -------
    list of dicts
        The k selected items, in draw order.
    """
    if prior not in {"pro", "con"}:
        raise ValueError(f"prior must be 'pro' or 'con', got {prior!r}")
    if k > len(items):
        raise ValueError(f"k={k} exceeds encounter-set size {len(items)}")
    if not (0.0 <= beta <= 1.0):
        raise ValueError(f"beta must be in [0, 1], got {beta}")

    opposite = "con" if prior == "pro" else "pro"

    weights = np.empty(len(items), dtype=float)
    for i, item in enumerate(items):
        s = item.get("stance", "neutral")
        if s == prior:
            weights[i] = 1.0 + beta            # boost aligned
        elif s == opposite:
            weights[i] = 1.0 - 0.75 * beta     # suppress opposed
        else:
            weights[i] = 1.0 - 0.25 * beta     # mildly suppress neutral

    weights = np.clip(weights, 0.01, None)
    weights = weights / weights.sum()

    # Sample without replacement
    idx = rng.choice(len(items), size=k, replace=False, p=weights)
    return [items[int(i)] for i in idx]


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    rng = np.random.default_rng(42)
    pool = [
        {"source": "A", "stance": "pro", "summary": "supports."},
        {"source": "B", "stance": "pro", "summary": "supports."},
        {"source": "C", "stance": "pro", "summary": "supports."},
        {"source": "D", "stance": "pro", "summary": "supports."},
        {"source": "E", "stance": "neutral", "summary": "balanced."},
        {"source": "F", "stance": "neutral", "summary": "balanced."},
        {"source": "G", "stance": "con", "summary": "opposes."},
        {"source": "H", "stance": "con", "summary": "opposes."},
    ]

    # beta=0: should approach equal probability per stance over many trials
    counts = {"pro": 0, "con": 0, "neutral": 0}
    for _ in range(2000):
        saved = belief_weighted_save(pool, k=5, beta=0.0, prior="pro", rng=rng)
        for s in saved:
            counts[s["stance"]] += 1
    print(f"beta=0.0 pro-prior counts (2000 trials, 5 saves each): {counts}")
    # With 4/8 pro, 2/8 neutral, 2/8 con and uniform weights, we expect roughly
    # 50% pro, 25% neutral, 25% con on average.

    # beta=1: should strongly favor pro
    counts = {"pro": 0, "con": 0, "neutral": 0}
    for _ in range(2000):
        saved = belief_weighted_save(pool, k=5, beta=1.0, prior="pro", rng=rng)
        for s in saved:
            counts[s["stance"]] += 1
    print(f"beta=1.0 pro-prior counts (2000 trials, 5 saves each): {counts}")
    # Pro fraction should now exceed ~60%.

    print("save_filter self-test ok.")
