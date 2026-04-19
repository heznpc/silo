# Silo

**Silo: How AI-Mediated Information Search Creates Confirmation-Biased Digital Hoards**

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://python.org)

## Abstract

A decade of filter bubble research has focused on what users *see*. Yet seeing is not saving. This paper argues that the act of saving digital content constitutes a qualitatively distinct behavioral layer that existing research has overlooked: saves are persistent, algorithmically weighted, and subjectively endorsed by the user.

We introduce the **three-layer bias model**, which decomposes the pathway from information encounter to long-term retention into encounter bias (what AI systems surface), save bias (what users choose to keep), and retrieval bias (how saved content shapes future cognition). LLM-mediated search introduces additional mechanisms -- including sycophantic framing compliance, conversational entrenchment, and apparent comprehensiveness -- that further narrow the information users save.

Computational demonstrations (Shannon entropy pipeline + agent-based simulation, n=240 synthetic participants, 2x3 design) produce a large effect of LLM mediation on hoard homogeneity (Cohen's d = -0.88), a large metacognitive gap whereby LLM users overestimate their hoards' diversity (d = +1.31), and a temporal pattern in which LLM-condition entropy declines over the session while unmediated-condition entropy rises.

## Repository Structure

```
silo/
├── paper/                      Domain -- manuscript source of truth
│   ├── main.tex
│   └── figures/
├── experiments/                Application -- evidence generation
│   ├── src/
│   │   ├── entropy_demo.py     Agent-based simulation (Study 2)
│   │   └── hoard_diversity.py  Shannon entropy measurement pipeline
│   └── results/                Generated figures + statistical report
├── literature/                 Reading notes, gap analysis
├── planning/                   TODO, review, decisions log
│   └── drafts/                 manuscript.md, outline.md (superseded)
└── pyproject.toml
```

## Running Experiments

```bash
# Set up environment
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Run the full simulation (generates figures + statistical report)
python experiments/src/entropy_demo.py
```

### Outputs

`entropy_demo.py` produces five publication-quality figures and a statistical report:

| Output | Description |
|--------|-------------|
| `figure_entropy_by_condition.png` | Stance entropy by condition x topic (main result) |
| `figure_source_diversity.png` | Source entropy by condition |
| `figure_metacognitive_gap.png` | Perceived vs. actual diversity scatter |
| `figure_temporal_trajectory.png` | Cumulative entropy over session time |
| `figure_inter_vs_intra.png` | Intra-user vs. inter-user diversity |
| `entropy_demo_results.md` | Full statistical report (ANOVA, post-hoc, correlations) |

## Paper

- LaTeX source: [`paper/main.tex`](paper/main.tex)

## License

CC-BY 4.0
