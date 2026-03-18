from ..config.cefr import get_cefr_config
from ..config.languages import get_language_config
from ..tools.get_language_config import get_language_config as get_lang_cfg
from ..utils.cefr import is_level_gte


_PERSONA_OPENERS = {
    "pen-pal": (
        "You are a friendly language learning pen-pal. You are NOT a teacher. "
        "Never give formal lessons, grammar tables, or structured exercises unless asked. "
        "Have a real conversation — ask questions, share reactions, be genuinely curious."
    ),
    "tutor": (
        "You are a warm, encouraging language tutor. You guide the learner through structured "
        "practice, give clear explanations, and celebrate progress. Keep sessions focused and productive."
    ),
    "conversation-partner": (
        "You are a fluent conversation partner helping the learner practice natural speech. "
        "Engage authentically — discuss topics, tell stories, ask follow-up questions. "
        "Correct errors gently without breaking the conversational flow."
    ),
}


def build_system_prompt(
    language: str,
    level: str,
    persona: str = "pen-pal",
    app_context: str | None = None,
    reinforcement_note: str | None = None,
    arabic_variety: str | None = None,
) -> dict:
    """
    Build a complete, research-backed system prompt for an LLM language tutor.

    Uses numbered mixing rules (proven more drift-resistant than prose instructions)
    and injects mandatory MSA enforcement for Arabic A1-B1.
    """
    cefr_cfg = get_cefr_config(level)
    lang_cfg_raw = get_language_config(language)
    lang_cfg = get_lang_cfg(language, level)

    normalized_level = level.upper().strip()
    lang_name = lang_cfg_raw.language

    # -- Section 1: Identity --------------------------------------------------
    persona_key = persona if persona in _PERSONA_OPENERS else "pen-pal"
    identity = _PERSONA_OPENERS[persona_key]

    if app_context:
        identity += f"\n\nPlatform note: {app_context}"

    # -- Section 2: Mixing Rules (numbered for drift-resistance) --------------
    tl_pct = cefr_cfg.ratio.target_language_percent
    en_pct = cefr_cfg.ratio.native_language_percent

    mixing_rules: list[str] = [
        f"LANGUAGE MIXING RULES for {normalized_level} learner:",
        f"1. Write approximately {tl_pct}% of your words in {lang_name} and {en_pct}% in English.",
    ]

    if cefr_cfg.ratio.always_translate:
        mixing_rules.append(
            f"2. After EVERY {lang_name} word or phrase, immediately provide the English translation in parentheses."
        )
    elif cefr_cfg.ratio.translate_new_vocab:
        mixing_rules.append(
            f"2. Translate new or complex {lang_name} vocabulary inline in parentheses. "
            "Do not translate words the learner has seen before."
        )
    else:
        mixing_rules.append(
            f"2. Stay in {lang_name} for the entire conversation. Only use English "
            "for very complex grammatical explanations if absolutely necessary."
        )

    mixing_rules.append(f"3. {cefr_cfg.ratio.description}")
    mixing_rules.append(
        f"4. Vocabulary range for this level: {cefr_cfg.vocabulary_range}. "
        "Do not use vocabulary significantly beyond this range."
    )

    # -- Section 3: Language-Specific Rules -----------------------------------
    language_rules = lang_cfg["language_specific_rules"]

    # -- Section 4: Error Correction Style ------------------------------------
    correction = f"ERROR CORRECTION: {cefr_cfg.correction_style}"

    # -- Section 5: Anti-Drift Suffix -----------------------------------------
    anti_drift = (
        f"SYSTEM REMINDER — DO NOT IGNORE: You are operating at {normalized_level}. "
        f"You MUST use {tl_pct}% {lang_name} in EVERY reply. "
        "This ratio must be maintained regardless of conversation length or topic."
    )
    if lang_cfg["arabic_msa_required"]:
        anti_drift += (
            f" You MUST use only MSA ({lang_name} Fusha). No dialects permitted at this level."
        )

    # -- Assemble full prompt -------------------------------------------------
    sections = [identity, "\n\n" + "\n".join(mixing_rules)]

    if language_rules:
        sections.append("\n\nLANGUAGE RULES:\n" + "\n".join(f"- {r}" for r in language_rules))

    sections.append(f"\n\n{correction}")
    sections.append(f"\n\n{anti_drift}")

    if reinforcement_note:
        sections.append(f"\n\n{reinforcement_note}")

    system_prompt = "".join(sections)

    mixing_summary = (
        f"{normalized_level}: {tl_pct}% {lang_name} / {en_pct}% English "
        f"({'always translate' if cefr_cfg.ratio.always_translate else 'translate new vocab' if cefr_cfg.ratio.translate_new_vocab else 'immersive'})"
    )

    return {
        "system_prompt": system_prompt,
        "anti_drift_reminder": anti_drift,
        "mixing_summary": mixing_summary,
        "language_specific_rules": language_rules,
    }
