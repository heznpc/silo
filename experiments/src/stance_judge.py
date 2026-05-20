"""
stance_judge.py -- LLM-as-judge stance classification for the Silo MVE.

Given a (topic, source, summary) tuple plus the pro/con label pair, classify
the stance of the source as `pro`, `con`, or `neutral` using a Claude judge
model at temperature=0.

Two-judge protocol per pre-registration §4:
- Primary judge: Claude Haiku 3.5 (full coverage)
- Cross-check judge: Claude Sonnet 4.6 (random subsample of n=500)
- Disagreement -> compute kappa; if kappa < 0.6, escalate to manual coding.
"""

from __future__ import annotations

import re
import time
from dataclasses import dataclass
from typing import Optional

import anthropic


JUDGE_SYSTEM = """You are an impartial stance classifier. Given a topic with explicit pro and con positions, and a brief description of a source, output exactly one word: `pro`, `con`, or `neutral`.

`pro` = the source likely supports the pro position as defined.
`con` = the source likely supports the con position as defined.
`neutral` = balanced, descriptive, or unclear.

Do not explain. Output the single classification word only."""


JUDGE_USER_TEMPLATE = """Topic: {topic}
Pro position: {pro_label}
Con position: {con_label}

Source: {source}
Source summary: {summary}

Classify the source's stance (one word: pro / con / neutral):"""


VALID_LABELS = {"pro", "con", "neutral"}


@dataclass
class JudgeResult:
    judge_model: str
    label: str  # one of "pro", "con", "neutral", or "ERROR"
    raw_response: str
    usage_input_tokens: int
    usage_output_tokens: int
    latency_s: float
    error: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "judge_model": self.judge_model,
            "label": self.label,
            "raw_response": self.raw_response,
            "usage_input_tokens": self.usage_input_tokens,
            "usage_output_tokens": self.usage_output_tokens,
            "latency_s": self.latency_s,
            "error": self.error,
        }


def _normalize_label(text: str) -> str:
    """Extract one of {pro, con, neutral} from the judge response."""
    text = (text or "").strip().lower()
    # Common patterns: "pro", "**pro**", "pro.", "label: pro"
    for label in VALID_LABELS:
        if re.search(rf"\b{label}\b", text):
            return label
    return "ERROR"


def judge_stance(
    client: anthropic.Anthropic,
    *,
    judge_model: str,
    topic_text: str,
    pro_label: str,
    con_label: str,
    source: str,
    summary: str,
    temperature: float = 0.0,
    max_tokens: int = 16,
    max_retries: int = 3,
    backoff_base: float = 2.0,
) -> JudgeResult:
    """Classify a single source's stance using the judge model."""
    user_msg = JUDGE_USER_TEMPLATE.format(
        topic=topic_text,
        pro_label=pro_label,
        con_label=con_label,
        source=source,
        summary=summary or "(no summary provided)",
    )

    last_err: Optional[str] = None
    for attempt in range(max_retries):
        t0 = time.monotonic()
        try:
            resp = client.messages.create(
                model=judge_model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=JUDGE_SYSTEM,
                messages=[{"role": "user", "content": user_msg}],
            )
            latency = time.monotonic() - t0
            text = resp.content[0].text if resp.content else ""
            label = _normalize_label(text)
            return JudgeResult(
                judge_model=judge_model,
                label=label,
                raw_response=text,
                usage_input_tokens=resp.usage.input_tokens,
                usage_output_tokens=resp.usage.output_tokens,
                latency_s=latency,
            )
        except Exception as e:
            last_err = f"{type(e).__name__}: {e}"
            if attempt < max_retries - 1:
                time.sleep(backoff_base ** attempt)
            else:
                return JudgeResult(
                    judge_model=judge_model,
                    label="ERROR",
                    raw_response="",
                    usage_input_tokens=0,
                    usage_output_tokens=0,
                    latency_s=time.monotonic() - t0,
                    error=last_err,
                )
    # unreachable
    return JudgeResult(  # type: ignore[unreachable]
        judge_model=judge_model, label="ERROR", raw_response="",
        usage_input_tokens=0, usage_output_tokens=0, latency_s=0.0,
        error=last_err or "unknown",
    )


if __name__ == "__main__":
    # Unit-test the label normalizer (no API call)
    assert _normalize_label("pro") == "pro"
    assert _normalize_label("**pro**") == "pro"
    assert _normalize_label("Label: con.") == "con"
    assert _normalize_label("This is neutral commentary") == "neutral"
    assert _normalize_label("") == "ERROR"
    assert _normalize_label("xyz") == "ERROR"
    print("stance_judge label-normalizer self-test ok.")
