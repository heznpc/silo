"""
entropy_demo.py -- Computational simulation of Silo Study 2.

Generates synthetic data for 240 participants (2x3 design), computes all
hoard-diversity metrics from hoard_diversity.py, produces publication-quality
figures, and runs the planned statistical tests.

Outputs (saved to the same directory):
  figure_entropy_by_condition.png
  figure_source_diversity.png
  figure_metacognitive_gap.png
  figure_temporal_trajectory.png
  figure_inter_vs_intra.png
  entropy_demo_results.md
"""

from __future__ import annotations

import os
import warnings
from itertools import combinations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

import hoard_diversity as hd

# Reproducibility
RNG = np.random.default_rng(42)

_SRC_DIR = os.path.dirname(os.path.abspath(__file__))
_EXP_DIR = os.path.dirname(_SRC_DIR)
OUT_DIR = os.path.join(_EXP_DIR, "results")
os.makedirs(OUT_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# 1.  Design parameters
# ---------------------------------------------------------------------------

CONDITIONS = ["LLM", "Algorithm", "Unmediated"]
TOPICS = ["Controversial", "Neutral"]
N_PER_CELL = 40
STANCES = ["pro", "con", "neutral"]
TIME_WINDOWS = 6  # every 5 min in a 30-min session

# Base stance proportions (pro, neutral, con) -- from the task spec
BASE_PROPS: dict[tuple[str, str], tuple[float, float, float]] = {
    ("LLM", "Controversial"):       (0.70, 0.20, 0.10),
    ("Algorithm", "Controversial"):  (0.55, 0.25, 0.20),
    ("Unmediated", "Controversial"): (0.40, 0.30, 0.30),
    ("LLM", "Neutral"):             (0.45, 0.35, 0.20),
    ("Algorithm", "Neutral"):        (0.40, 0.35, 0.25),
    ("Unmediated", "Neutral"):       (0.35, 0.35, 0.30),
}

# Source parameters by condition
SOURCE_COUNTS = {"LLM": (3, 5), "Algorithm": (4, 7), "Unmediated": (5, 8)}
# Source concentration (Dirichlet alpha): lower = more concentrated
SOURCE_ALPHA = {"LLM": 0.3, "Algorithm": 0.7, "Unmediated": 1.5}

# Metacognitive bias
META_BIAS = {
    "LLM":        (0.15, 0.05),
    "Algorithm":   (0.10, 0.05),
    "Unmediated": (0.05, 0.05),
}

# Temporal trajectory modifiers (per-window multiplier on pro proportion)
# LLM: entropy declines (pro proportion increases over time)
# Algorithm: slight decline
# Unmediated: flat
TEMPORAL_PRO_DRIFT = {
    "LLM":        np.array([0.00, 0.03, 0.06, 0.09, 0.12, 0.15]),
    "Algorithm":   np.array([0.00, 0.01, 0.02, 0.03, 0.03, 0.04]),
    "Unmediated": np.array([0.00, 0.00, 0.00, 0.00, 0.00, 0.00]),
}

# Synthetic source-name pools
SOURCE_POOLS = {
    "Controversial": [
        "nytimes.com", "foxnews.com", "bbc.co.uk", "reuters.com",
        "theguardian.com", "wsj.com", "cnn.com", "apnews.com",
        "politico.com", "theatlantic.com", "jacobin.com", "reason.com",
    ],
    "Neutral": [
        "tripadvisor.com", "lonelyplanet.com", "booking.com", "expedia.com",
        "fodors.com", "nomadicmatt.com", "travelandleisure.com",
        "ricksteves.com", "atlasobscura.com", "cntraveler.com",
    ],
}


# ---------------------------------------------------------------------------
# 2.  Synthetic data generation
# ---------------------------------------------------------------------------

def _noisy_proportions(base: tuple[float, ...], noise_sd: float = 0.08) -> np.ndarray:
    """Add Gaussian noise to base proportions and renormalise."""
    noisy = np.array(base) + RNG.normal(0, noise_sd, size=len(base))
    noisy = np.clip(noisy, 0.01, None)  # avoid zero / negative
    return noisy / noisy.sum()


def _sample_stances(proportions: np.ndarray, n: int) -> list[str]:
    """Sample n stance labels from a multinomial distribution."""
    counts = RNG.multinomial(n, proportions)
    labels: list[str] = []
    for stance, count in zip(STANCES, counts):
        labels.extend([stance] * count)
    RNG.shuffle(labels)
    return list(labels)


def _sample_sources(
    condition: str, topic: str, n_items: int
) -> list[str]:
    """Sample source names for n_items saves."""
    lo, hi = SOURCE_COUNTS[condition]
    n_sources = RNG.integers(lo, hi + 1)
    pool = SOURCE_POOLS[topic]
    chosen = list(RNG.choice(pool, size=min(n_sources, len(pool)), replace=False))
    alpha = np.full(len(chosen), SOURCE_ALPHA[condition])
    weights = RNG.dirichlet(alpha)
    return list(RNG.choice(chosen, size=n_items, p=weights))


def _temporal_items(
    base_props: tuple[float, float, float],
    condition: str,
    n_items: int,
) -> list[list[str]]:
    """Generate items split into TIME_WINDOWS with temporal drift."""
    # Distribute items roughly evenly across windows
    items_per_window = np.full(TIME_WINDOWS, n_items // TIME_WINDOWS)
    remainder = n_items % TIME_WINDOWS
    for i in range(remainder):
        items_per_window[i] += 1

    drift = TEMPORAL_PRO_DRIFT[condition]
    windows: list[list[str]] = []
    for t in range(TIME_WINDOWS):
        props = np.array(base_props, dtype=float)
        props[0] += drift[t]          # pro increases
        props[2] -= drift[t] * 0.6    # con decreases more
        props[1] -= drift[t] * 0.4    # neutral decreases less
        props = np.clip(props, 0.01, None)
        props /= props.sum()
        window_items = _sample_stances(props, int(items_per_window[t]))
        windows.append(window_items)
    return windows


def generate_dataset() -> pd.DataFrame:
    """Generate full synthetic dataset for 240 participants."""
    rows: list[dict] = []
    pid = 0
    for condition in CONDITIONS:
        for topic in TOPICS:
            base = BASE_PROPS[(condition, topic)]
            for _ in range(N_PER_CELL):
                n_items = RNG.integers(10, 31)
                props = _noisy_proportions(base)
                items = _sample_stances(props, n_items)
                sources = _sample_sources(condition, topic, n_items)
                temporal = _temporal_items(base, condition, n_items)

                actual_ent = hd.stance_entropy(items)
                bias_mu, bias_sd = META_BIAS[condition]
                # Logit-space bias to avoid ceiling/floor effects
                eps = 1e-6
                clamped = np.clip(actual_ent, eps, 1 - eps)
                logit_ent = np.log(clamped / (1 - clamped))
                logit_biased = logit_ent + RNG.normal(bias_mu, bias_sd)
                perceived = 1 / (1 + np.exp(-logit_biased))
                trajectory = hd.temporal_entropy_trajectory(temporal)
                sdi = hd.source_diversity_index(sources)

                rows.append({
                    "pid": pid,
                    "condition": condition,
                    "topic": topic,
                    "n_items": n_items,
                    "items": items,
                    "sources": sources,
                    "stance_entropy": actual_ent,
                    "source_entropy": sdi["entropy"],
                    "source_raw_count": sdi["raw_count"],
                    "source_dominance": sdi["dominance"],
                    "perceived_diversity": float(perceived),
                    "metacognitive_gap": hd.metacognitive_gap(
                        float(perceived), actual_ent
                    ),
                    "trajectory": trajectory,
                    "temporal_items": temporal,
                })
                pid += 1
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# 3.  Figures
# ---------------------------------------------------------------------------

# Consistent colour palette
COND_COLORS = {"LLM": "#d62728", "Algorithm": "#ff7f0e", "Unmediated": "#2ca02c"}
TOPIC_HATCHES = {"Controversial": "", "Neutral": "//"}


def _style_ax(ax: plt.Axes, xlabel: str, ylabel: str, title: str) -> None:
    ax.set_xlabel(xlabel, fontsize=13)
    ax.set_ylabel(ylabel, fontsize=13)
    ax.set_title(title, fontsize=14, weight="bold")
    ax.tick_params(labelsize=12)


def fig_entropy_by_condition(df: pd.DataFrame) -> None:
    """Box plot: stance entropy by condition x topic (main result figure)."""
    fig, ax = plt.subplots(figsize=(9, 5.5))

    positions = []
    labels = []
    data = []
    colors = []
    pos = 0
    for topic in TOPICS:
        for cond in CONDITIONS:
            subset = df[(df["condition"] == cond) & (df["topic"] == topic)]
            data.append(subset["stance_entropy"].values)
            positions.append(pos)
            labels.append(f"{cond}\n{topic}")
            colors.append(COND_COLORS[cond])
            pos += 1
        pos += 0.5  # gap between topics

    bp = ax.boxplot(
        data,
        positions=positions,
        widths=0.6,
        patch_artist=True,
        showmeans=True,
        meanprops=dict(marker="D", markerfacecolor="black", markersize=5),
    )
    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.65)

    ax.set_xticks(positions)
    ax.set_xticklabels(labels, fontsize=11)
    _style_ax(
        ax,
        "",
        "Normalised Stance Entropy",
        "Stance Entropy by Information Source and Topic",
    )
    ax.set_ylim(-0.05, 1.15)
    ax.axhline(1.0, ls="--", lw=0.8, color="grey", alpha=0.5)
    ax.text(positions[-1] + 0.3, 1.01, "max diversity", fontsize=9, color="grey")

    # Legend
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=COND_COLORS[c], alpha=0.65, label=c) for c in CONDITIONS]
    ax.legend(handles=legend_elements, fontsize=11, loc="upper left")

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "figure_entropy_by_condition.png"), dpi=200)
    plt.close(fig)


def fig_source_diversity(df: pd.DataFrame) -> None:
    """Box plot: source entropy by condition."""
    fig, ax = plt.subplots(figsize=(8, 5))

    positions = []
    labels = []
    data = []
    colors = []
    pos = 0
    for topic in TOPICS:
        for cond in CONDITIONS:
            subset = df[(df["condition"] == cond) & (df["topic"] == topic)]
            data.append(subset["source_entropy"].values)
            positions.append(pos)
            labels.append(f"{cond}\n{topic}")
            colors.append(COND_COLORS[cond])
            pos += 1
        pos += 0.5

    bp = ax.boxplot(
        data, positions=positions, widths=0.6, patch_artist=True,
        showmeans=True,
        meanprops=dict(marker="D", markerfacecolor="black", markersize=5),
    )
    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.65)

    ax.set_xticks(positions)
    ax.set_xticklabels(labels, fontsize=11)
    _style_ax(ax, "", "Normalised Source Entropy", "Source Diversity by Condition and Topic")
    ax.set_ylim(-0.05, 1.15)
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=COND_COLORS[c], alpha=0.65, label=c) for c in CONDITIONS]
    ax.legend(handles=legend_elements, fontsize=11, loc="upper left")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "figure_source_diversity.png"), dpi=200)
    plt.close(fig)


def fig_metacognitive_gap(df: pd.DataFrame) -> None:
    """Scatter: actual entropy vs perceived diversity, coloured by condition."""
    fig, ax = plt.subplots(figsize=(7, 6))

    for cond in CONDITIONS:
        subset = df[df["condition"] == cond]
        ax.scatter(
            subset["stance_entropy"],
            subset["perceived_diversity"],
            c=COND_COLORS[cond],
            label=cond,
            alpha=0.55,
            s=30,
            edgecolors="white",
            linewidths=0.3,
        )

    # Diagonal = perfect calibration
    ax.plot([0, 1], [0, 1], "k--", lw=1, alpha=0.5, label="Perfect calibration")
    _style_ax(
        ax,
        "Actual Stance Entropy",
        "Perceived Diversity (self-report)",
        "Metacognitive Gap: Perceived vs. Actual Diversity",
    )
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.05, 1.15)
    ax.legend(fontsize=11)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "figure_metacognitive_gap.png"), dpi=200)
    plt.close(fig)


def fig_temporal_trajectory(df: pd.DataFrame) -> None:
    """Line plot: mean entropy trajectory (controversial topic only)."""
    fig, ax = plt.subplots(figsize=(7, 5))

    subset = df[df["topic"] == "Controversial"]
    x = np.arange(1, TIME_WINDOWS + 1) * 5  # minutes

    for cond in CONDITIONS:
        cond_df = subset[subset["condition"] == cond]
        trajs = np.array(cond_df["trajectory"].tolist())
        mean_traj = trajs.mean(axis=0)
        se_traj = trajs.std(axis=0) / np.sqrt(len(trajs))
        ax.plot(x, mean_traj, "o-", color=COND_COLORS[cond], label=cond, lw=2)
        ax.fill_between(
            x,
            mean_traj - 1.96 * se_traj,
            mean_traj + 1.96 * se_traj,
            color=COND_COLORS[cond],
            alpha=0.15,
        )

    _style_ax(
        ax,
        "Session Time (minutes)",
        "Cumulative Stance Entropy",
        "Temporal Entropy Trajectory (Controversial Topic)",
    )
    ax.legend(fontsize=12)
    ax.set_xticks(x)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "figure_temporal_trajectory.png"), dpi=200)
    plt.close(fig)


def fig_inter_vs_intra(df: pd.DataFrame) -> None:
    """Bar plot: mean intra-user vs inter-user entropy by condition."""
    fig, ax = plt.subplots(figsize=(8, 5))

    x = np.arange(len(CONDITIONS))
    width = 0.35
    intra_means = []
    intra_ses = []
    inter_vals = []

    for cond in CONDITIONS:
        cond_df = df[df["condition"] == cond]
        intra = cond_df["stance_entropy"].values
        intra_means.append(intra.mean())
        intra_ses.append(intra.std() / np.sqrt(len(intra)))
        # Inter-user diversity: average pairwise JSD
        all_items = cond_df["items"].tolist()
        inter_vals.append(hd.inter_user_diversity(all_items))

    bars1 = ax.bar(
        x - width / 2, intra_means, width,
        yerr=np.array(intra_ses) * 1.96,
        label="Intra-user (mean stance entropy)",
        color=[COND_COLORS[c] for c in CONDITIONS],
        alpha=0.7,
        capsize=4,
    )
    bars2 = ax.bar(
        x + width / 2, inter_vals, width,
        label="Inter-user (mean pairwise JSD)",
        color=[COND_COLORS[c] for c in CONDITIONS],
        alpha=0.35,
        edgecolor=[COND_COLORS[c] for c in CONDITIONS],
        linewidth=1.5,
        hatch="//",
    )

    ax.set_xticks(x)
    ax.set_xticklabels(CONDITIONS, fontsize=12)
    _style_ax(
        ax,
        "Condition",
        "Diversity Metric",
        "Intra-User vs. Inter-User Diversity",
    )
    ax.legend(fontsize=11)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "figure_inter_vs_intra.png"), dpi=200)
    plt.close(fig)


# ---------------------------------------------------------------------------
# 4.  Statistical tests
# ---------------------------------------------------------------------------

def _cohens_d(a: np.ndarray, b: np.ndarray) -> float:
    """Cohen's d for two independent samples."""
    n1, n2 = len(a), len(b)
    var1, var2 = a.var(ddof=1), b.var(ddof=1)
    pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    if pooled_std == 0:
        return 0.0
    return float((a.mean() - b.mean()) / pooled_std)


def run_statistical_tests(df: pd.DataFrame) -> str:
    """Run all planned tests and return a Markdown report."""
    lines: list[str] = []
    lines.append("# Silo Study 2 -- Simulation Results\n")
    lines.append("## Dataset summary\n")
    lines.append(f"- Total participants: {len(df)}")
    lines.append(f"- Cells: {df.groupby(['condition','topic']).size().to_dict()}")
    lines.append(f"- Mean items saved per participant: {df['n_items'].mean():.1f} "
                 f"(SD = {df['n_items'].std():.1f})\n")

    # --- Descriptive statistics ---
    lines.append("## Descriptive statistics: Stance entropy by cell\n")
    lines.append("| Condition | Topic | Mean | SD | Median |")
    lines.append("|-----------|-------|------|----|--------|")
    for cond in CONDITIONS:
        for topic in TOPICS:
            s = df[(df["condition"] == cond) & (df["topic"] == topic)]["stance_entropy"]
            lines.append(
                f"| {cond} | {topic} | {s.mean():.3f} | {s.std():.3f} | {s.median():.3f} |"
            )
    lines.append("")

    # --- Normality check ---
    lines.append("## Normality check (Shapiro-Wilk on stance entropy per cell)\n")
    all_normal = True
    for cond in CONDITIONS:
        for topic in TOPICS:
            s = df[(df["condition"] == cond) & (df["topic"] == topic)]["stance_entropy"]
            stat, p = stats.shapiro(s)
            normal_flag = "normal" if p > 0.05 else "NON-NORMAL"
            if p <= 0.05:
                all_normal = False
            lines.append(f"- {cond} x {topic}: W = {stat:.4f}, p = {p:.4f} ({normal_flag})")
    lines.append("")

    # --- 2x3 ANOVA (or Kruskal-Wallis) ---
    lines.append("## Omnibus test: 2x3 ANOVA on stance entropy\n")
    # Two-way ANOVA via OLS (lightweight, no statsmodels dependency required)
    # We'll use scipy for one-way tests within each factor and interaction proxy
    # Full factorial with scipy only: use Kruskal-Wallis across all 6 groups
    groups = []
    group_labels = []
    for cond in CONDITIONS:
        for topic in TOPICS:
            s = df[(df["condition"] == cond) & (df["topic"] == topic)]["stance_entropy"].values
            groups.append(s)
            group_labels.append(f"{cond}x{topic}")

    kw_stat, kw_p = stats.kruskal(*groups)
    lines.append(f"Kruskal-Wallis across all 6 cells: H = {kw_stat:.3f}, p = {kw_p:.6f}\n")

    # Main effect of condition (collapsing across topic)
    cond_groups = [df[df["condition"] == c]["stance_entropy"].values for c in CONDITIONS]
    f_cond, p_cond = stats.f_oneway(*cond_groups)
    lines.append(f"One-way ANOVA, main effect of condition: F = {f_cond:.3f}, p = {p_cond:.6f}")

    # Main effect of topic
    topic_groups = [df[df["topic"] == t]["stance_entropy"].values for t in TOPICS]
    f_topic, p_topic = stats.f_oneway(*topic_groups)
    lines.append(f"One-way ANOVA, main effect of topic: F = {f_topic:.3f}, p = {p_topic:.6f}\n")

    # --- Post-hoc pairwise comparisons ---
    pairwise = list(combinations(CONDITIONS, 2))
    n_comparisons = len(pairwise)
    lines.append(f"## Post-hoc pairwise comparisons (Mann-Whitney U + Cohen's d, Bonferroni k={n_comparisons})\n")
    lines.append("| Comparison | U | p | p (corrected) | Cohen's d | Interpretation |")
    lines.append("|------------|---|---|---------------|-----------|----------------|")
    for c1, c2 in pairwise:
        a = df[df["condition"] == c1]["stance_entropy"].values
        b = df[df["condition"] == c2]["stance_entropy"].values
        u_stat, u_p = stats.mannwhitneyu(a, b, alternative="two-sided")
        p_corrected = min(u_p * n_comparisons, 1.0)
        d = _cohens_d(a, b)
        size = "large" if abs(d) >= 0.8 else "medium" if abs(d) >= 0.5 else "small"
        sig = "*" if p_corrected < 0.05 else "ns"
        lines.append(
            f"| {c1} vs {c2} | {u_stat:.1f} | {u_p:.6f} | {p_corrected:.6f} {sig} | {d:+.3f} | {size} |"
        )
    lines.append("")

    # --- Correlation: stance entropy <-> source entropy ---
    lines.append("## Correlation: Stance entropy and source diversity\n")
    r, p_r = stats.pearsonr(df["stance_entropy"], df["source_entropy"])
    rho, p_rho = stats.spearmanr(df["stance_entropy"], df["source_entropy"])
    lines.append(f"- Pearson r = {r:.3f}, p = {p_r:.6f}")
    lines.append(f"- Spearman rho = {rho:.3f}, p = {p_rho:.6f}\n")

    # --- Metacognitive gap: LLM vs Unmediated ---
    lines.append("## Metacognitive gap: LLM vs Unmediated (t-test)\n")
    gap_llm = df[df["condition"] == "LLM"]["metacognitive_gap"].values
    gap_unmed = df[df["condition"] == "Unmediated"]["metacognitive_gap"].values
    t_stat, t_p = stats.ttest_ind(gap_llm, gap_unmed)
    d_gap = _cohens_d(gap_llm, gap_unmed)
    lines.append(f"- LLM gap: M = {gap_llm.mean():.3f}, SD = {gap_llm.std():.3f}")
    lines.append(f"- Unmediated gap: M = {gap_unmed.mean():.3f}, SD = {gap_unmed.std():.3f}")
    lines.append(f"- t = {t_stat:.3f}, p = {t_p:.6f}, Cohen's d = {d_gap:+.3f}\n")

    # --- Inter vs Intra summary ---
    lines.append("## Inter-user vs intra-user diversity\n")
    lines.append("| Condition | Mean intra (stance H) | Inter (mean pairwise JSD) |")
    lines.append("|-----------|----------------------|---------------------------|")
    for cond in CONDITIONS:
        cond_df = df[df["condition"] == cond]
        intra = cond_df["stance_entropy"].mean()
        inter = hd.inter_user_diversity(cond_df["items"].tolist())
        lines.append(f"| {cond} | {intra:.3f} | {inter:.3f} |")
    lines.append("")

    # --- Temporal trajectory summary ---
    lines.append("## Temporal trajectory summary (Controversial topic)\n")
    lines.append("Mean cumulative entropy at each 5-min window:\n")
    lines.append("| Window | LLM | Algorithm | Unmediated |")
    lines.append("|--------|-----|-----------|------------|")
    sub = df[df["topic"] == "Controversial"]
    for t in range(TIME_WINDOWS):
        vals = []
        for cond in CONDITIONS:
            trajs = np.array(sub[sub["condition"] == cond]["trajectory"].tolist())
            vals.append(f"{trajs[:, t].mean():.3f}")
        lines.append(f"| {(t+1)*5} min | {' | '.join(vals)} |")
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 5.  Main
# ---------------------------------------------------------------------------

def main() -> None:
    print("Generating synthetic dataset (n=240) ...")
    df = generate_dataset()
    print(f"  {len(df)} participants generated.\n")

    print("Generating figures ...")
    fig_entropy_by_condition(df)
    print("  [1/5] figure_entropy_by_condition.png")
    fig_source_diversity(df)
    print("  [2/5] figure_source_diversity.png")
    fig_metacognitive_gap(df)
    print("  [3/5] figure_metacognitive_gap.png")
    fig_temporal_trajectory(df)
    print("  [4/5] figure_temporal_trajectory.png")
    fig_inter_vs_intra(df)
    print("  [5/5] figure_inter_vs_intra.png")

    print("\nRunning statistical tests ...")
    report = run_statistical_tests(df)
    report_path = os.path.join(OUT_DIR, "entropy_demo_results.md")
    with open(report_path, "w") as f:
        f.write(report)
    print(f"  Results written to {report_path}")

    # Print report to stdout as well
    print("\n" + "=" * 70)
    print(report)
    print("=" * 70)
    print("\nDone. All outputs saved to:", OUT_DIR)


if __name__ == "__main__":
    main()
