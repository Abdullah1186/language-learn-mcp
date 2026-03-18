from ..config.cefr import get_cefr_config
from ..config.languages import get_language_config
from ..config.pedagogy import ANTI_DRIFT_INJECTION_INTERVAL
from ..utils.cefr import is_level_gte


def get_reinforcement_note(
    language: str,
    level: str,
    turn_number: int,
    last_drift_result: dict | None = None,
    arabic_variety: str | None = None,
) -> dict:
    """
    Determine whether to inject an anti-drift reinforcement note before the next LLM call.

    Injects when:
    - Scheduled: every ANTI_DRIFT_INJECTION_INTERVAL turns (default 6)
    - Drift-corrective: last drift result had severity 'significant'
    - Dialect: last drift result had drift_type 'dialect'

    Returns should_inject=False when none of the above apply.
    """
    normalized_level = level.upper().strip()
    cefr_cfg = get_cefr_config(normalized_level)
    lang_cfg = get_language_config(language)
    lang_name = lang_cfg.language
    tl_pct = cefr_cfg.ratio.target_language_percent

    # Determine injection triggers
    scheduled = (turn_number > 0) and (turn_number % ANTI_DRIFT_INJECTION_INTERVAL == 0)

    drift_significant = (
        last_drift_result is not None
        and last_drift_result.get("severity") == "significant"
    )
    dialect_detected = (
        last_drift_result is not None
        and last_drift_result.get("drift_type") == "dialect"
    )

    should_inject = scheduled or drift_significant or dialect_detected

    if not should_inject:
        return {
            "should_inject": False,
            "note": "",
            "injection_reason": "none",
        }

    # Determine injection reason (priority: dialect > drift > scheduled)
    if dialect_detected:
        injection_reason = "dialect"
        note = (
            f"ARABIC REMINDER: Use ONLY Modern Standard Arabic (MSA/Fusha) at {normalized_level} level. "
            f"Do NOT use any dialect. MSA is mandatory until B2."
        )
    elif drift_significant:
        injection_reason = "drift-corrective"
        correction = last_drift_result.get("correction_instruction", "")
        note = f"DRIFT CORRECTION: {correction}" if correction else (
            f"REMINDER: Maintain {tl_pct}% {lang_name} usage in every reply at {normalized_level} level."
        )
    else:
        injection_reason = "scheduled"
        note = (
            f"LEVEL REMINDER ({normalized_level}): Use {tl_pct}% {lang_name} / "
            f"{cefr_cfg.ratio.native_language_percent}% English in every reply. "
        )
        if lang_cfg.arabic_config is not None:
            if not is_level_gte(normalized_level, lang_cfg.arabic_config.dialect_introduction_level):
                note += "Use only MSA — no dialects."

    return {
        "should_inject": True,
        "note": note,
        "injection_reason": injection_reason,
    }
