"""
hoard_diversity.py -- Shannon entropy measurement module for Silo Study 2.

Implements hoard diversity metrics described in outline Section 6:
  6.1  Shannon Entropy of Saved Content (stance entropy)
  6.2  Source Diversity Index
  6.3  Temporal Diversity Trajectory
  6.4  Intra-User vs. Inter-User Diversity (following Anwar & Schoenebeck 2024)

Additional metrics:
  - Metacognitive gap (H5: perceived vs. actual diversity)
  - Simple keyword-based stance classifier for pipeline demo
"""

from __future__ import annotations

import math
from collections import Counter
from itertools import combinations

import numpy as np


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _distribution(items: list[str]) -> dict[str, float]:
    """Return normalised probability distribution over item labels."""
    if not items:
        return {}
    counts = Counter(items)
    total = len(items)
    return {k: v / total for k, v in counts.items()}


def _shannon_entropy(dist: dict[str, float]) -> float:
    """Raw Shannon entropy (base-2) from a probability distribution."""
    return -sum(p * math.log2(p) for p in dist.values() if p > 0)


def _normalised_entropy(items: list[str]) -> float:
    """Shannon entropy normalised to [0, 1] by dividing by log2(num_categories)."""
    if not items:
        return 0.0
    dist = _distribution(items)
    num_categories = len(dist)
    if num_categories <= 1:
        return 0.0
    h = _shannon_entropy(dist)
    h_max = math.log2(num_categories)
    return h / h_max


def _dist_from_labels(labels: list[str], vocab: list[str] | None = None) -> np.ndarray:
    """Return probability vector aligned to *vocab* (sorted unique labels if None)."""
    if vocab is None:
        vocab = sorted(set(labels))
    counts = Counter(labels)
    total = len(labels) if labels else 1
    return np.array([counts.get(v, 0) / total for v in vocab])


# ---------------------------------------------------------------------------
# Core metrics (Section 6)
# ---------------------------------------------------------------------------

def stance_entropy(items: list[str]) -> float:
    """Shannon entropy of stance distribution, normalised to [0, 1].

    Parameters
    ----------
    items : list of stance labels ('pro', 'con', 'neutral')

    Returns
    -------
    float
        H / log2(num_categories).  Range [0, 1].
        0 = all items have the same stance.
        1 = items are uniformly distributed across all observed stances.
    """
    return _normalised_entropy(items)


def source_entropy(sources: list[str]) -> float:
    """Shannon entropy of source distribution, normalised to [0, 1].

    Parameters
    ----------
    sources : list of domain names / source identifiers

    Returns
    -------
    float
        Normalised Shannon entropy of the source distribution.
    """
    return _normalised_entropy(sources)


def source_diversity_index(sources: list[str]) -> dict:
    """Composite source-diversity summary (Section 6.2).

    Returns
    -------
    dict with keys:
        raw_count  -- number of unique sources
        entropy    -- normalised source entropy
        dominance  -- proportion of saves from the single most common source
    """
    if not sources:
        return {"raw_count": 0, "entropy": 0.0, "dominance": 0.0}
    counts = Counter(sources)
    return {
        "raw_count": len(counts),
        "entropy": source_entropy(sources),
        "dominance": max(counts.values()) / len(sources),
    }


def temporal_entropy_trajectory(
    items_by_time: list[list[str]],
) -> list[float]:
    """Cumulative stance entropy over successive time windows (Section 6.3).

    Parameters
    ----------
    items_by_time : list of lists
        Each inner list contains stance labels saved during one time window
        (e.g., every 5 minutes of a 30-min session).

    Returns
    -------
    list[float]
        Normalised stance entropy of the *cumulative* collection at each
        time point.  A declining trajectory indicates progressive silo
        formation.
    """
    trajectory: list[float] = []
    cumulative: list[str] = []
    for window in items_by_time:
        cumulative.extend(window)
        trajectory.append(stance_entropy(cumulative))
    return trajectory


def intra_user_diversity(user_items: list[str]) -> float:
    """Stance entropy for a single user's hoard (Section 6.4)."""
    return stance_entropy(user_items)


def inter_user_diversity(all_users_items: list[list[str]]) -> float:
    """Average pairwise Jensen--Shannon divergence between users' stance distributions.

    Measures how *different* users' hoards are from each other, following
    Anwar & Schoenebeck (2024) distinction between intra- and inter-user
    diversity.

    Parameters
    ----------
    all_users_items : list of lists
        Each inner list is one user's stance labels.

    Returns
    -------
    float
        Mean pairwise JSD (base-2, range [0, 1]).
    """
    if len(all_users_items) < 2:
        return 0.0

    vocab = sorted({label for user in all_users_items for label in user})
    dists = [_dist_from_labels(u, vocab) for u in all_users_items]

    def _jsd(p: np.ndarray, q: np.ndarray) -> float:
        m = 0.5 * (p + q)
        # Use convention 0 * log(0) = 0
        def _kl(a: np.ndarray, b: np.ndarray) -> float:
            with np.errstate(divide="ignore", invalid="ignore"):
                terms = np.where(a > 0, a * np.log2(a / np.where(b > 0, b, 1)), 0)
            return float(np.sum(terms))
        return 0.5 * _kl(p, m) + 0.5 * _kl(q, m)

    jsds = [_jsd(dists[i], dists[j]) for i, j in combinations(range(len(dists)), 2)]
    return float(np.mean(jsds))


def metacognitive_gap(perceived_diversity: float, actual_entropy: float) -> float:
    """Metacognitive gap (H5): perceived minus actual diversity.

    Parameters
    ----------
    perceived_diversity : float
        User self-report of hoard diversity, normalised to [0, 1].
    actual_entropy : float
        Normalised stance entropy of the user's hoard.

    Returns
    -------
    float
        Positive values indicate the user *overestimates* the diversity of
        their hoard.
    """
    return perceived_diversity - actual_entropy


# ---------------------------------------------------------------------------
# Keyword-based stance classifier (simple, for pipeline demo)
# ---------------------------------------------------------------------------

def classify_stance(text: str, topic_keywords: dict[str, list[str]]) -> str:
    """Simple keyword-based stance classification.

    Parameters
    ----------
    text : str
        The text of a saved item.
    topic_keywords : dict
        {'pro': [keyword, ...], 'con': [keyword, ...]}

    Returns
    -------
    str
        'pro', 'con', or 'neutral'.
    """
    text_lower = text.lower()
    pro_hits = sum(1 for kw in topic_keywords.get("pro", []) if kw.lower() in text_lower)
    con_hits = sum(1 for kw in topic_keywords.get("con", []) if kw.lower() in text_lower)
    if pro_hits > con_hits:
        return "pro"
    elif con_hits > pro_hits:
        return "con"
    return "neutral"


# ---------------------------------------------------------------------------
# Quick self-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Sanity checks
    assert stance_entropy(["pro", "pro", "pro"]) == 0.0
    assert abs(stance_entropy(["pro", "con", "neutral"]) - 1.0) < 1e-9

    mixed = ["pro"] * 4 + ["con"] * 3 + ["neutral"] * 3
    h = stance_entropy(mixed)
    assert 0.0 < h < 1.0, f"Expected intermediate entropy, got {h}"

    sdi = source_diversity_index(["nyt", "nyt", "bbc", "fox"])
    assert sdi["raw_count"] == 3
    assert 0.0 < sdi["entropy"] < 1.0
    assert sdi["dominance"] == 0.5

    traj = temporal_entropy_trajectory([["pro"], ["pro", "con"], ["neutral"]])
    assert len(traj) == 3
    assert traj[0] == 0.0  # only one label so far
    assert traj[-1] > traj[0]

    gap = metacognitive_gap(0.8, 0.4)
    assert gap == 0.4

    label = classify_stance(
        "This policy will boost the economy and create jobs",
        {"pro": ["boost", "create jobs"], "con": ["destroy", "harm"]},
    )
    assert label == "pro"

    print("All self-tests passed.")
