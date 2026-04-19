# Silo Study 2 -- Simulation Results

## Dataset summary

- Total participants: 240
- Cells: {('Algorithm', 'Controversial'): 40, ('Algorithm', 'Neutral'): 40, ('LLM', 'Controversial'): 40, ('LLM', 'Neutral'): 40, ('Unmediated', 'Controversial'): 40, ('Unmediated', 'Neutral'): 40}
- Mean items saved per participant: 19.8 (SD = 6.1)

## Descriptive statistics: Stance entropy by cell

| Condition | Topic | Mean | SD | Median |
|-----------|-------|------|----|--------|
| LLM | Controversial | 0.713 | 0.195 | 0.737 |
| LLM | Neutral | 0.897 | 0.086 | 0.912 |
| Algorithm | Controversial | 0.878 | 0.077 | 0.886 |
| Algorithm | Neutral | 0.921 | 0.073 | 0.944 |
| Unmediated | Controversial | 0.925 | 0.069 | 0.946 |
| Unmediated | Neutral | 0.919 | 0.062 | 0.931 |

## Normality check (Shapiro-Wilk on stance entropy per cell)

- LLM x Controversial: W = 0.9057, p = 0.0028 (NON-NORMAL)
- LLM x Neutral: W = 0.9144, p = 0.0051 (NON-NORMAL)
- Algorithm x Controversial: W = 0.9575, p = 0.1379 (normal)
- Algorithm x Neutral: W = 0.8752, p = 0.0004 (NON-NORMAL)
- Unmediated x Controversial: W = 0.8780, p = 0.0005 (NON-NORMAL)
- Unmediated x Neutral: W = 0.8388, p = 0.0000 (NON-NORMAL)

## Omnibus test: 2x3 ANOVA on stance entropy

Kruskal-Wallis across all 6 cells: H = 59.143, p = 0.000000

One-way ANOVA, main effect of condition: F = 22.376, p = 0.000000
One-way ANOVA, main effect of topic: F = 22.066, p = 0.000004

## Post-hoc pairwise comparisons (Mann-Whitney U + Cohen's d)

| Comparison | U | p | Cohen's d | Interpretation |
|------------|---|---|-----------|----------------|
| LLM vs Algorithm | 2115.0 | 0.000215 | -0.694 | medium |
| LLM vs Unmediated | 1763.0 | 0.000001 | -0.881 | large |
| Algorithm vs Unmediated | 2711.0 | 0.095488 | -0.314 | small |

## Correlation: Stance entropy and source diversity

- Pearson r = 0.342, p = 0.000000
- Spearman rho = 0.187, p = 0.003691

## Metacognitive gap: LLM vs Unmediated (t-test)

- LLM gap: M = 0.104, SD = 0.062
- Unmediated gap: M = 0.034, SD = 0.041
- t = 8.266, p = 0.000000, Cohen's d = +1.307

## Inter-user vs intra-user diversity

| Condition | Mean intra (stance H) | Inter (mean pairwise JSD) |
|-----------|----------------------|---------------------------|
| LLM | 0.805 | 0.108 |
| Algorithm | 0.899 | 0.065 |
| Unmediated | 0.922 | 0.070 |

## Temporal trajectory summary (Controversial topic)

Mean cumulative entropy at each 5-min window:

| Window | LLM | Algorithm | Unmediated |
|--------|-----|-----------|------------|
| 5 min | 0.634 | 0.737 | 0.841 |
| 10 min | 0.695 | 0.847 | 0.867 |
| 15 min | 0.705 | 0.845 | 0.901 |
| 20 min | 0.676 | 0.848 | 0.927 |
| 25 min | 0.667 | 0.845 | 0.939 |
| 30 min | 0.645 | 0.850 | 0.947 |
