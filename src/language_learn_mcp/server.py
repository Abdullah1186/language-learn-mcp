"""
language-learn-mcp MCP Server

Provides 8 tools for language learning pedagogy:
- get_mixing_config: Research-grounded CEFR language mixing ratios
- get_language_config: Language-specific rules (formality, MSA, scripts)
- build_system_prompt: Complete system prompt with anti-drift mechanisms
- generate_exercise: CEFR-appropriate exercises using Krashen i+1
- build_vocab_input: Structured vocabulary with comprehensible input
- score_response: CEFR rubric and level-change signals
- detect_drift: Pure-Python language mixing drift detection
- get_reinforcement_note: Scheduled anti-drift injection logic
"""

from mcp.server.fastmcp import FastMCP

from .tools.get_mixing_config import get_mixing_config
from .tools.get_language_config import get_language_config
from .tools.build_system_prompt import build_system_prompt
from .tools.generate_exercise import generate_exercise
from .tools.build_vocab_input import build_vocab_input
from .tools.score_response import score_response
from .tools.detect_drift import detect_drift
from .tools.get_reinforcement_note import get_reinforcement_note

import os as _os
mcp = FastMCP("language-learn-mcp", host="0.0.0.0", port=int(_os.environ.get("PORT", 8000)))


@mcp.tool()
def tool_get_mixing_config(level: str, language: str) -> dict:
    """
    Return the research-grounded language mixing configuration for a CEFR level.

    Corrects common mistakes in language apps (wrong mixing ratios).
    Research basis: CLIL 75/25 rule, Krashen i+1, CEFR descriptors.
    """
    return get_mixing_config(level=level, language=language)


@mcp.tool()
def tool_get_language_config(language: str, level: str) -> dict:
    """
    Return language-specific rules resolved for the given CEFR level.

    For Arabic A1-B1: forces MSA (Modern Standard Arabic), rejects dialects.
    Includes formality rules, script direction, and WhatsApp formatting tips.
    """
    return get_language_config(language=language, level=level)


@mcp.tool()
def tool_build_system_prompt(
    language: str,
    level: str,
    persona: str = "pen-pal",
    app_context: str = "",
    reinforcement_note: str = "",
    arabic_variety: str = "",
) -> dict:
    """
    Build a complete, research-backed system prompt for an LLM language tutor.

    Uses numbered mixing rules (more drift-resistant than prose instructions).
    Injects mandatory MSA enforcement for Arabic A1-B1.
    Returns system_prompt, anti_drift_reminder, and language_specific_rules.
    """
    return build_system_prompt(
        language=language,
        level=level,
        persona=persona or "pen-pal",
        app_context=app_context or None,
        reinforcement_note=reinforcement_note or None,
        arabic_variety=arabic_variety or None,
    )


@mcp.tool()
def tool_generate_exercise(
    language: str,
    level: str,
    type: str,
    topic: str = "",
    weak_words: list[str] | None = None,
    arabic_variety: str = "",
) -> dict:
    """
    Return a structured exercise instruction using Krashen's i+1 principle.

    Types: translation, fill_in_blank, multiple_choice, sentence_construction,
           listening_comprehension_prompt, error_correction.
    If weak_words provided -> accessible. Otherwise -> stretch (i+1 level vocab).
    """
    return generate_exercise(
        language=language,
        level=level,
        type=type,
        topic=topic or None,
        weak_words=weak_words or None,
        arabic_variety=arabic_variety or None,
    )


@mcp.tool()
def tool_build_vocab_input(
    language: str,
    level: str,
    count: int = 1,
    topic: str = "",
    weak_words: list[str] | None = None,
    arabic_variety: str = "",
) -> dict:
    """
    Return structured vocabulary following Krashen's comprehensible input principle.

    Blend: 70% current-level + 30% i+1-level vocabulary.
    Arabic A1-A2: includes tashkeel (diacritics) field.
    B1+: includes comprehensible_input_passage instruction.
    """
    return build_vocab_input(
        language=language,
        level=level,
        count=count,
        topic=topic or None,
        weak_words=weak_words or None,
        arabic_variety=arabic_variety or None,
    )


@mcp.tool()
def tool_score_response(
    language: str,
    level: str,
    user_input: str,
    exercise_prompt: str = "",
    target_words: list[str] | None = None,
) -> dict:
    """
    Build a CEFR rubric for evaluating a learner's response.

    Returns the rubric text for the calling LLM to evaluate against,
    plus correctness focus areas for the given CEFR level.
    """
    return score_response(
        language=language,
        level=level,
        user_input=user_input,
        exercise_prompt=exercise_prompt or None,
        target_words=target_words or None,
    )


@mcp.tool()
def tool_detect_drift(
    language: str,
    level: str,
    recent_messages: list[dict],
    window_size: int = 6,
) -> dict:
    """
    Detect language mixing drift in recent message history.

    Pure Python computation — no LLM calls, sub-millisecond execution.
    Uses Unicode block ranges for script detection.
    For Arabic: also detects dialect marker words and flags them.
    """
    return detect_drift(
        language=language,
        level=level,
        recent_messages=recent_messages,
        window_size=window_size,
    )


@mcp.tool()
def tool_get_reinforcement_note(
    language: str,
    level: str,
    turn_number: int,
    last_drift_result: dict | None = None,
    arabic_variety: str = "",
) -> dict:
    """
    Determine whether to inject an anti-drift reinforcement note.

    Injects when: every 6 turns (scheduled), significant drift detected, or dialect use detected.
    Returns should_inject, note text, and injection_reason.
    Prepend the note to the system prompt when should_inject is True.
    """
    return get_reinforcement_note(
        language=language,
        level=level,
        turn_number=turn_number,
        last_drift_result=last_drift_result,
        arabic_variety=arabic_variety or None,
    )


def main():
    mcp.run(transport="sse")


if __name__ == "__main__":
    main()
