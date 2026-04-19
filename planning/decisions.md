# Research Decisions Log

Records non-obvious choices with rationale. Append-only; don't rewrite history.

Format: `## YYYY-MM-DD -- <short title>` with **Context**, **Decision**, **Why**.

---

## 2026-04-19 -- Repository restructure to DDD-style layout

**Context**: Top level had manuscript.md + outline.md + TODO.md + review.md + paper/main.tex co-located. experiments/ mixed scripts (entropy_demo.py, hoard_diversity.py) with figures and result markdown at the same level.

**Decision**: Adopt bounded-context layout -- paper/ (domain), experiments/src/ (scripts), experiments/results/ (figures + reports), planning/ (meta), literature/. hoard_diversity.py stays next to entropy_demo.py in src/ since it's imported as a library.

**Why**: Clear separation of "what is the manuscript" vs "what produces the evidence" vs "what are the meta-work artifacts".
