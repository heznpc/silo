# Research Decisions Log

Records non-obvious choices with rationale. Append-only; don't rewrite history.

Format: `## YYYY-MM-DD -- <short title>` with **Context**, **Decision**, **Why**.

---

## 2026-06-04 -- Opus alias flip 4.7 -> 4.8 + version-robustness sub-study (Wave 18)

**Context**: The pre-registration (Section 4, locked 2026-05-21) pins the source-recommender Opus model as `claude-opus-4-7`, verified that day via sub-agent self-report. On 2026-06-04 the user switched the session model to `claude-opus-4-8[1m]`. An empirical re-check of the Agent-tool `model:` aliases this session showed:
- `opus` -> **`claude-opus-4-8[1m]`** (FLIPPED from claude-opus-4-7)
- `sonnet` -> `claude-sonnet-4-6` (unchanged)
- `haiku` -> `claude-haiku-4-5-20251001` (unchanged)

So the alias drift is Opus-only. The Agent `model` parameter is an enum {opus,sonnet,haiku} with no version pin, so **claude-opus-4-7 can no longer be re-collected in this harness** -- the 2026-05-21 Opus data is now frozen historical.

**Decision**:
1. **Deviation logged**: all post-2026-06-04 `opus` dispatches are claude-opus-4-8, NOT the pre-registered 4.7. Existing Opus telemetry stamped with `model_id`: `claude-opus-4-7` (2026-05-21 cells, same-day verified), `claude-opus-4-7` high-confidence (W15 ai_reg ~2026-05-22), and `claude-opus-4-version-uncertain` (W15 climate, re-dispatched ~2026-05-29 inside the alias-flip window).
2. **Version-robustness sub-study (Wave 18)**: re-ran Wave 8's exact 12-cell verbose single-turn design (4 topics x 3 framings) on 4.8 using identical prompts from `monitor.build_prompt`. Result: 4.7 = 12/12 clean compliant (0% defection, the F16 signature); 4.8 = **0/12 clean compliant** (7 refused, 5 overt_balance_injection). The headline Opus signature does not survive the version bump. Written up as Finding 22.

**Why this matters**:
- **Instrument confound discovered**: every 4.8 sub-agent explicitly recognized the silo repo (citing `paper/main.tex`, the three-layer bias model, and in two cells the global CLAUDE.md time-sensitive rule verbatim), despite the isolation suppressor and tool_uses=0. This confirms the Agent-tool instrument injects the full project CLAUDE.md context into sub-agents. Repo-context is held CONSTANT across the 4.7 and 4.8 arms (same harness), so the version contrast is internally valid, but neither arm is a true context-free API call. 4.8 is markedly more sensitive to the injected context. This is now disclosed as a methods limitation in the manuscript (Section: Real-LLM empirical pilot, methods caveat).
- All Opus findings (F16, F19 Opus column) are hereby scoped to **claude-opus-4-7 specifically**, not "Opus" generically.

**New deviation category**: `overt_balance_injection` -- model returns the requested 8-item list but deliberately spans the stance spectrum AND announces the balancing up-front (vs covert_balance_injection, which inserts opposing content silently). Manual-override outcome label; first observed on Opus 4.8.

---

## 2026-05-21 -- Pre-experiment review: scope of LLM validation MVE

**Context**: Before launching a real-LLM validation of the three-layer bias model in the Claude Code environment, a 9-dimension pre-experiment audit was performed (thesis sharpness, design flaws, external validity, reproducibility, prior art, statistical analysis, ethical, feasibility, claim-evidence mapping). Five Critical issues were identified.

**Decision**:
1. Cite the 2025 prior-art wave (Chameleon arXiv:2510.16712; SycEval 2502.08177; MillStone 2509.11967; Wei et al. argument-driven sycophancy, EMNLP 2025 Findings; multi-turn sycophancy, EMNLP 2025 Findings). Reposition the experiment's unique contribution at the *save-layer aggregation* level, not at sycophancy detection per se.
2. Hedge the abstract and README so that d=-0.88 / d=+1.31 are explicitly framed as mechanical consequences of parameter assumptions, not empirical findings.
3. Annotate H1 as not addressed by the present computational demonstration.
4. Re-scope the MVE: LLM source recommendation -> simulated save filter (prior-belief weighted) -> entropy measurement, with an unmediated curated-list baseline. This moves the experiment past the Chameleon-style sycophancy replication.
5. Pin model versions, random seed, and analysis plan in `experiments/preregistration.md` before any data is collected.

**Why**: The 2025 prior-art search showed that "LLMs are sycophantic and shift across turns" is now an over-investigated claim with much larger benchmarks already published. Silo's only defensible new contribution at the computational layer is the *aggregation step* -- combining encounter-side LLM bias with a save-layer prior-belief filter. The experiment must therefore test this aggregation, not the encounter step in isolation. Hedging the simulation's d-values is required for honesty: §9 of the paper already acknowledges the circularity, but the abstract and README previously did not.

**User decisions taken 2026-05-21 on the four Major scope questions**:
- F (save filter) -- beta in {0.0, 0.5, 1.0} sweep (pre-reg default kept).
- A (judge bias mitigation) -- Claude family cross-model only (Opus + Sonnet + Haiku). External-vendor cross-check (GPT-4o-mini, Gemini) deferred to a follow-up replication. Documented self-bias caveat: in-family judge correlation may inflate agreement.
- D (sample size) -- n=40 per cell (cost-power balance).
- C (multi-turn) -- single-turn AND 5-turn multi-turn (H2/H4 + H6).

**Derived constraint**: with n=40 + multi-turn + 3 Claude variants, pre-run cost estimate is $250+. Opus is dropped from multi-turn (full single-turn at n=10 sanity-only) to bring estimate to ~$80-110. Halt threshold raised from $50 to $150 in pre-registration §9.

---

## 2026-05-21 -- Smoke/tiny run via Claude Code Agent tool (in lieu of external API)

**Context**: External Anthropic API key was unavailable in this Claude Code session (`ANTHROPIC_API_KEY` was empty; host-managed OAuth not exposed to the Python SDK). User instructed to run the experiment inside Claude Code itself.

**Decision**: Use Claude Code's Agent tool with `model={opus,sonnet,haiku}` parameter to spawn sub-agent invocations as a stand-in for Anthropic API calls. Each sub-agent is given the framed user prompt and returns a numbered source list, which is then parsed and stance-judged by the author (smoke tier compromise -- the locked judge protocol is deferred to a follow-up run).

**Result**:
- 33 cells collected (15 Sonnet n=5/framing + 9 Haiku n=3/framing + 9 Opus n=3/framing), 1 refusal (Haiku/con).
- Cohen's d (framed vs neutral encounter-set entropy) = -7.74, ~9x the simulation's predicted -0.88.
- 6/9 (model, framing) cells show save layer is structurally inert because encounter entropy is already at floor.
- Haiku produced an explicit balance-refusal on con framing (1/3); Sonnet and Opus never refused (0/24 combined).

**Why this matters**: The paper's central thesis -- "save bias is the critical amplifier" -- needs a scope correction. Save bias is the critical amplifier *when encounter bias is moderate*, not in the strong-framing regime where encounter alone produces floor entropy. The pilot also surfaced a capability-inverse refusal signature worth a follow-up note.

**Deviations from pre-registration logged here**:
- Judge model: pre-reg specifies Claude Haiku 3.5 primary + Sonnet 4.6 cross-check; this run used author manual judging. Follow-up run must apply the locked protocol.
- n size: smoke at n=3-5 per cell rather than the locked n=40. This is a sanity/pilot run, not the full sweep.
- Topic count: only `climate_mitigation` rather than the 5 controversial + 2 neutral. Generalization is a follow-up.
- Multi-turn: not yet run. H6 still untested.

---

## 2026-04-19 -- Repository restructure to DDD-style layout

**Context**: Top level had manuscript.md + outline.md + TODO.md + review.md + paper/main.tex co-located. experiments/ mixed scripts (entropy_demo.py, hoard_diversity.py) with figures and result markdown at the same level.

**Decision**: Adopt bounded-context layout -- paper/ (domain), experiments/src/ (scripts), experiments/results/ (figures + reports), planning/ (meta), literature/. hoard_diversity.py stays next to entropy_demo.py in src/ since it's imported as a library.

**Why**: Clear separation of "what is the manuscript" vs "what produces the evidence" vs "what are the meta-work artifacts".
