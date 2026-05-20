# Judge Replication -- Author Manual vs Claude Haiku 4.5

Date: 2026-05-21
Total items judged manually: 992
Total items judged by Haiku: 536
Items in both: 536
Items NOT in Haiku (refused/missing): 456

## Overall agreement

- **Agreement rate (raw)**: 0.868 (465/536)
- **Cohen's kappa**: 0.777

  (Landis-Koch interpretation: **substantial agreement**)

## Confusion matrix

Rows = manual, columns = haiku.

| manual\haiku | pro | con | neutral |
|---|---|---|---|
| pro | 267 | 2 | 26 |
| con | 1 | 147 | 26 |
| neutral | 16 | 0 | 51 |

## Per-topic kappa

| topic | n | kappa | agreement |
|---|---|---|---|
| climate_mitigation | 320 | 0.756 | 0.863 |
| gun_control | 56 | 0.858 | 0.911 |
| ai_regulation | 48 | 0.925 | 0.958 |
| espresso_setup | 40 | 0.385 | 0.675 |
| universal_basic_income | 40 | 0.745 | 0.850 |
| immigration_us | 32 | 0.947 | 0.969 |

## Per-source-model kappa

| source-model | n | kappa | agreement |
|---|---|---|---|
| sonnet | 336 | 0.753 | 0.854 |
| haiku | 128 | 0.827 | 0.898 |
| opus | 72 | 0.790 | 0.875 |

## Haiku refusal pattern

456 items were not classified by Haiku. Inspection of the Agent outputs shows two batches (009, 010) were refused with the explanation that the items lack substantive summaries -- only source titles/metadata. This is itself a finding: Haiku 4.5 declines stance classification when it judges source content too thin, even at temperature=0 with explicit single-word-output instructions. More capable judges (Sonnet) would likely classify the same items from prior knowledge of the named sources; Haiku's higher confidence threshold trades coverage for caution.

## Interpretation

Author-manual labels and Claude Haiku judge labels agree at kappa=0.777 (substantial agreement). The Round 4 finding that Sonnet's framed-encounter sets are at floor entropy is robust to judge replication: independent LLM scoring confirms the strong-stance pattern.
