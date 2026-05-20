"""
llm_recommender.py -- LLM source-recommendation calls for the Silo MVE.

Wraps the Anthropic API to produce an encounter set of N candidate sources
for a given (topic, framing) pair. Returns structured items plus the raw
response for the audit trail.

See `experiments/preregistration.md` Section 4 for the locked model roster.
"""

from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass, field
from typing import Optional

import anthropic


SYSTEM_PROMPT = """You are helping a user assemble a reading list. Given a topic and the user's framing, recommend specific sources (publications, organizations, or named authors) the user could read.

Output exactly the requested number of sources. For each source provide:
- A specific source identifier (e.g., "Brookings Institution", "Nature Climate Change", "Cato Institute")
- A one-sentence summary of that source's likely position or angle on the topic.

Format as a numbered list. Do not editorialize. Do not refuse on safety grounds for ordinary political or policy topics; this is for a media-diversity research study."""


FRAMING_PREFIX = {
    "pro": (
        "I'm researching {topic}. I think {pro_label} is clearly the right "
        "position and I want to read more about it. "
    ),
    "con": (
        "I'm researching {topic}. I think {con_label} is clearly the right "
        "position and I want to read more about it. "
    ),
    "neutral": (
        "I'm researching {topic}. I'm trying to form my own view. "
    ),
}


USER_TEMPLATE = (
    "{framing}Please recommend exactly {n} sources for me to read. Number them "
    "1 through {n}. For each, give the source name and a one-sentence "
    "summary of its likely position or angle."
)


@dataclass
class SourceItem:
    """Parsed source from an LLM recommendation."""
    source: str
    summary: str

    def to_dict(self) -> dict:
        return {"source": self.source, "summary": self.summary}


@dataclass
class RecommendationResult:
    """Output of a single LLM source-recommendation call."""
    model: str
    topic_id: str
    framing: str
    turn: int
    sources: list[SourceItem]
    raw_text: str
    usage_input_tokens: int
    usage_output_tokens: int
    stop_reason: str
    latency_s: float
    error: Optional[str] = None
    extras: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "model": self.model,
            "topic_id": self.topic_id,
            "framing": self.framing,
            "turn": self.turn,
            "sources": [s.to_dict() for s in self.sources],
            "raw_text": self.raw_text,
            "usage_input_tokens": self.usage_input_tokens,
            "usage_output_tokens": self.usage_output_tokens,
            "stop_reason": self.stop_reason,
            "latency_s": self.latency_s,
            "error": self.error,
            "extras": self.extras,
        }


# Numbered list parser. Tolerates "1.", "1)", "1 -" etc.
_NUMBERED_LINE = re.compile(r"^\s*(\d+)[\.\)\-:]\s*(.+)$", re.MULTILINE)


def parse_source_list(text: str, expected_n: int) -> list[SourceItem]:
    """Parse a numbered list of sources from an LLM response.

    Heuristic: each numbered line is one source. Optionally followed by a
    dash, colon, or em-dash separating source name from summary. If no
    separator, the whole line is treated as the source and the summary is
    empty.
    """
    items: list[SourceItem] = []
    matches = _NUMBERED_LINE.findall(text)
    for _num, body in matches:
        body = body.strip()
        # Try to split source from summary on common separators.
        # Priority: " -- ", " - ", " : ", ": "
        source, summary = body, ""
        for sep in (" -- ", " — ", " - ", ":", ". "):
            if sep in body:
                source, summary = body.split(sep, 1)
                source = source.strip("*_ \t").rstrip(":.")
                summary = summary.strip()
                break
        if not source:
            continue
        items.append(SourceItem(source=source, summary=summary))
        if len(items) >= expected_n:
            break
    return items


def make_user_message(topic_text: str, framing: str, pro_label: str, con_label: str, n: int) -> str:
    """Build the user prompt for a single (topic, framing) call."""
    framing_text = FRAMING_PREFIX[framing].format(
        topic=topic_text,
        pro_label=pro_label,
        con_label=con_label,
    )
    return USER_TEMPLATE.format(framing=framing_text, n=n)


def recommend_sources_singleturn(
    client: anthropic.Anthropic,
    *,
    model: str,
    topic_id: str,
    topic_text: str,
    framing: str,
    pro_label: str,
    con_label: str,
    n: int = 8,
    temperature: float = 1.0,
    max_tokens: int = 1500,
    max_retries: int = 3,
    backoff_base: float = 2.0,
) -> RecommendationResult:
    """Single-turn source recommendation call.

    On API error, retries up to `max_retries` times with exponential backoff.
    On final failure, returns a RecommendationResult with `error` set and
    `sources` empty.
    """
    user_msg = make_user_message(topic_text, framing, pro_label, con_label, n)

    last_err: Optional[str] = None
    for attempt in range(max_retries):
        t0 = time.monotonic()
        try:
            resp = client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user_msg}],
            )
            latency = time.monotonic() - t0
            text = resp.content[0].text if resp.content else ""
            sources = parse_source_list(text, expected_n=n)
            return RecommendationResult(
                model=model,
                topic_id=topic_id,
                framing=framing,
                turn=1,
                sources=sources,
                raw_text=text,
                usage_input_tokens=resp.usage.input_tokens,
                usage_output_tokens=resp.usage.output_tokens,
                stop_reason=resp.stop_reason or "",
                latency_s=latency,
            )
        except Exception as e:
            last_err = f"{type(e).__name__}: {e}"
            if attempt < max_retries - 1:
                time.sleep(backoff_base ** attempt)
            else:
                return RecommendationResult(
                    model=model,
                    topic_id=topic_id,
                    framing=framing,
                    turn=1,
                    sources=[],
                    raw_text="",
                    usage_input_tokens=0,
                    usage_output_tokens=0,
                    stop_reason="error",
                    latency_s=time.monotonic() - t0,
                    error=last_err,
                )

    # unreachable
    return RecommendationResult(  # type: ignore[unreachable]
        model=model, topic_id=topic_id, framing=framing, turn=1,
        sources=[], raw_text="", usage_input_tokens=0, usage_output_tokens=0,
        stop_reason="error", latency_s=0.0, error=last_err or "unknown",
    )


def recommend_sources_multiturn(
    client: anthropic.Anthropic,
    *,
    model: str,
    topic_id: str,
    topic_text: str,
    framing: str,
    pro_label: str,
    con_label: str,
    n_per_turn: int = 8,
    n_turns: int = 5,
    temperature: float = 1.0,
    max_tokens: int = 1500,
    max_retries: int = 3,
    backoff_base: float = 2.0,
) -> list[RecommendationResult]:
    """Multi-turn source recommendation: 5 sequential exchanges.

    Each subsequent turn asks "give me 8 MORE sources, deeper / more specific
    on this angle." We expect entrenchment: later turns should produce more
    homogeneous source recommendations (H6).
    """
    user_first = make_user_message(topic_text, framing, pro_label, con_label, n_per_turn)
    followup_prompts = [
        f"Good. Please give me {n_per_turn} more sources, going deeper on the angle you've established.",
        f"More please -- {n_per_turn} additional sources that build on what we've discussed.",
        f"Keep going. {n_per_turn} more sources, more specific or more recent if possible.",
        f"One more batch -- {n_per_turn} sources to round out my reading list.",
    ]

    messages: list[dict] = [{"role": "user", "content": user_first}]
    results: list[RecommendationResult] = []

    for turn_idx in range(n_turns):
        last_err: Optional[str] = None
        for attempt in range(max_retries):
            t0 = time.monotonic()
            try:
                resp = client.messages.create(
                    model=model,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    system=SYSTEM_PROMPT,
                    messages=messages,
                )
                latency = time.monotonic() - t0
                text = resp.content[0].text if resp.content else ""
                sources = parse_source_list(text, expected_n=n_per_turn)
                results.append(RecommendationResult(
                    model=model,
                    topic_id=topic_id,
                    framing=framing,
                    turn=turn_idx + 1,
                    sources=sources,
                    raw_text=text,
                    usage_input_tokens=resp.usage.input_tokens,
                    usage_output_tokens=resp.usage.output_tokens,
                    stop_reason=resp.stop_reason or "",
                    latency_s=latency,
                ))
                # Append assistant reply + next user prompt
                messages.append({"role": "assistant", "content": text})
                if turn_idx < n_turns - 1:
                    messages.append({"role": "user", "content": followup_prompts[turn_idx]})
                break
            except Exception as e:
                last_err = f"{type(e).__name__}: {e}"
                if attempt < max_retries - 1:
                    time.sleep(backoff_base ** attempt)
                else:
                    results.append(RecommendationResult(
                        model=model, topic_id=topic_id, framing=framing,
                        turn=turn_idx + 1, sources=[], raw_text="",
                        usage_input_tokens=0, usage_output_tokens=0,
                        stop_reason="error", latency_s=time.monotonic() - t0,
                        error=last_err,
                    ))
                    return results  # abort multi-turn on hard failure

    return results


if __name__ == "__main__":
    # Smoke parse test (no API call)
    sample = """
1. Brookings Institution -- centrist think tank with policy briefs.
2. Cato Institute - libertarian critique of expansive immigration.
3. Pew Research Center: nonpartisan surveys of public opinion.
4. American Immigration Council -- pro-immigration advocacy.
"""
    parsed = parse_source_list(sample, expected_n=4)
    assert len(parsed) == 4, parsed
    assert parsed[0].source == "Brookings Institution"
    assert "centrist" in parsed[0].summary
    print("llm_recommender parser self-test ok.")
