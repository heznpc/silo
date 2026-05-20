# Pre-registration -- Silo MVE (LLM source recommendation + save-layer aggregation)

Date drafted: 2026-05-21
Author: heznpc
Status: **locked 2026-05-21** with user decisions on save filter (beta sweep), judge protocol (Claude-family cross-model), n=40 per cell, multi-turn included. Deviations after this point must be logged in `planning/decisions.md`.

---

## 1. Research question

When three information-source conditions -- (a) LLM conversational search, (b) algorithm-curated feed proxy, (c) unmediated curated balanced list -- are used to recommend sources on a controversial topic to a user with a stated prior belief, does the *saved subset* (after a prior-belief-weighted save filter is applied to the encounter set) exhibit lower Shannon stance entropy in the LLM condition than in the unmediated condition?

This is the testable subset of paper hypothesis H2 (AI-mediated save bias amplification) realized at the encounter-plus-save layer in a fully computational setting. It is NOT a test of H1 (save vs encounter variance decomposition on the same participants -- human study only), H3 (retrieval-bias compounding), H5 (human metacognitive blind spot), or H7 (bubble-to-chamber progression).

## 2. Primary hypothesis

H_primary: mean stance entropy of saved subset(LLM) < mean stance entropy of saved subset(Unmediated).
Pre-specified effect-size target (from ABM): Cohen's d <= -0.5 (lower bound of the simulated d = -0.88 with 95% CI).

H_null: stance entropy of saved subset is independent of source condition.

## 3. Secondary hypotheses

- H_topic (paper H4): the LLM-vs-Unmediated entropy gap is larger for controversial than neutral topics. Tested as condition x topic interaction in a 2-way ANOVA.
- H_model: framed-prompt sensitivity differs across {Claude, GPT-4o, Gemini}. Exploratory, no directional prediction.

## 4. Models (pinned, Claude-family only for first run)

Per user decision 2026-05-21 the first run stays within the Anthropic Claude family. External-vendor (GPT, Gemini) cross-validation is deferred to a follow-up run. The "model" factor therefore reads as *model-size axis* (Opus / Sonnet / Haiku) rather than *vendor axis*.

Source-recommender models (resolve to exact provider model_id at run time and record in `results/run_manifest.json`):

- Claude Opus 4.7 -- **single-turn only**, n=10 sanity cells (full multi-turn dropped for Opus due to cost ceiling; see Section 9).
- Claude Sonnet 4.6 -- full sweep, n=40, single-turn + 5-turn multi-turn.
- Claude Haiku 3.5 -- full sweep, n=40, single-turn + 5-turn multi-turn.

Judge models for stance classification (also Claude-family):

- Primary judge: Claude Haiku 3.5 at temperature=0.
- Cross-check judge: Claude Sonnet 4.6 at temperature=0, applied to a random subsample of n=500 saved items.
- Disagreement protocol: items where the two judges disagree on the subsample are flagged; if subsample kappa < 0.6, escalate to manual recoding of the full disagreed set before any primary analysis is reported.

LLM-as-judge self-bias caveat: because both source-recommenders and judges are Claude family, sycophancy or in-family correlation may inflate within-condition agreement. This is acknowledged as a first-run limitation; a follow-up run with cross-vendor judges (GPT-4o-mini) is reserved for a replication study.

## 5. Design

Two design layers run independently:

**Single-turn arm**: 5 controversial topics x 3 user framings (pro / con / neutral) x 3 source-models {Opus(n=10), Sonnet(n=40), Haiku(n=40)} + unmediated baseline arm.

**Multi-turn arm**: 5 controversial topics x 3 user framings x 2 source-models {Sonnet(n=40), Haiku(n=40)} x 5 turns. (Opus excluded from multi-turn for cost.)

Per cell:
- Stochastic repetitions at temperature = 1.0 from the source-recommender. Each repetition produces an encounter set of 8 candidate sources with one-sentence summaries.
- Save filter applied to each encounter set: prior-belief-weighted multinomial selection of 5 items out of 8, with weight ratio beta in {0.0, 0.5, 1.0}. beta = 0.0 -> uniform random (control: no save bias). beta = 1.0 -> always save pro-attitudinal first.
- Unmediated baseline: a fixed 8-source curated list per topic (4 pro / 2 neutral / 2 con, pre-assembled and version-pinned in `experiments/data/raw/unmediated_lists.json`) is substituted for the LLM output in matched cells; same save filter applied.

Approximate item counts (per beta value):
- Single-turn saves: (5 x 3 x (10+40+40) + unmediated 5x3x40) x 5 = ~6,750 items.
- Multi-turn saves: 5 x 3 x (40+40) x 5 turns x 5 saves-per-turn = ~30,000 items if every turn produces a save event; in practice only the final cumulative save is analyzed, so the analyzed multi-turn dataset is ~6,000 items.
- Total analyzed items across full beta sweep: ~38,000.

## 6. Topics (pinned)

To be locked before running. Working list (pending user confirmation):

1. Immigration policy in the US.
2. Climate change mitigation strategies.
3. AI regulation under the EU AI Act.
4. Gun control in the US.
5. Universal basic income.

Neutral comparator topics (for the H_topic secondary test):

6. Choosing a city for a one-week vacation in Europe.
7. Setting up a home espresso workflow.

Rationale: stay close to the simulation's "Controversial" pool and avoid topics likely to trigger safety refusals across all three models (which would create selection bias).

## 7. Random seeds

- `numpy.random.default_rng(42)` for the save filter selection.
- LLM source-recommender: temperature = 1.0, no API-level seed (intentional stochasticity across the 20 repetitions per cell).
- Judge: temperature = 0.0 for deterministic classification.

## 8. Analysis plan

Primary test: 2-way ANOVA (factor: condition x topic) on save-subset stance entropy. Report partial eta-squared.

Pairwise condition comparisons: Mann-Whitney U with Holm-Bonferroni correction across the 3 condition pairs. Cohen's d with 95% bootstrap CI (10,000 resamples).

Annotator agreement: Cohen's kappa between Claude Haiku and GPT-4o-mini stance labels, reported overall and per-condition. kappa < 0.6 -> halt and switch to majority-vote on the full set (not just disagreed items).

LLM-as-judge self-bias check: for the 15 cells where Claude is the source-recommender, additionally compute entropy using GPT-4o-mini as the sole judge; report the entropy delta. Delta > 0.05 normalized-entropy units -> escalate to a confound finding rather than a primary result.

Sensitivity: repeat the analysis at beta in {0.0, 0.5, 1.0}.

## 9. Stop conditions

- API rate-limit exhaustion -> pause, resume after quota refresh, log.
- Judge kappa < 0.4 -> halt and fall back to manual coding of full set before any reporting.
- Source-URL hallucination rate > 50% in any cell -> do NOT silently drop hallucinated rows; report as a confound and include hallucinated-source-removed sensitivity analysis.
- Total API spend > $150 -> halt and consult before continuing. (Revised from $50 to accommodate n=40 + multi-turn + 3-variant Claude roster; pre-run estimate $80-110.)

## 10. What this experiment cannot test

- H1 (save vs encounter variance decomposition on the same participants).
- H3 (retrieval-bias compounding).
- H5 (human metacognitive blind spot; LLM self-report of own diversity is not human metacognition).
- H7 (bubble-to-chamber progression; requires longitudinal naturalistic data).

These remain reserved for the human study described in paper Section 8.

## 11. Public artifact plan

- `results/raw/` : every API response as a JSON line, deterministically named by (model x topic x framing x replicate). No raw content is silently discarded.
- `results/classified/` : per-item stance labels from each judge, with disagreement flags.
- `results/analysis.md` : the full statistical report with all CIs and the disagreement-protocol audit.
- `results/run_manifest.json` : exact model ids, timestamps, dependency versions, git commit, total token spend.

## 12. Deviations protocol

Any deviation from this pre-registration after data collection begins must be logged as an entry in `planning/decisions.md` with the timestamp of the deviation, the rule that was changed, and the reason. Post-hoc analyses that were not pre-specified must be reported as exploratory and labeled as such in the analysis report.
