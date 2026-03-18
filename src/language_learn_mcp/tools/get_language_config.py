from ..config.languages import get_language_config as _get_lang
from ..utils.cefr import is_level_gte, compare_levels


def get_language_config(language: str, level: str) -> dict:
    """
    Return language-specific configuration resolved for the given CEFR level.

    For Arabic at A1-B1: arabic_variety is forced to "MSA" and arabic_msa_required=True.
    For Arabic at B2+: dialects may be introduced but MSA remains the default.
    """
    config = _get_lang(language)
    normalized_level = level.upper().strip()

    # Resolve formality for this level
    formality = config.formality_by_level.get(normalized_level, config.formality_default)  # type: ignore

    # Arabic-specific logic
    arabic_variety = None
    arabic_msa_required = False
    arabic_tashkeel_required = False
    language_specific_rules: list[str] = []

    if config.arabic_config is not None:
        ac = config.arabic_config
        arabic_variety = "MSA"
        # MSA required below dialect_introduction_level (B2)
        arabic_msa_required = not is_level_gte(normalized_level, ac.dialect_introduction_level)
        if arabic_msa_required:
            language_specific_rules.append(ac.beginner_msa_note)
        else:
            language_specific_rules.append(
                "Arabic B2+: MSA is still the default. You may introduce a dialect only if the "
                "learner specifically requests regional/conversational practice."
            )
        # Tashkeel required at A1-A2
        arabic_tashkeel_required = not is_level_gte(normalized_level, ac.tashkeel_required_until) \
            or normalized_level == ac.tashkeel_required_until.upper()
        if arabic_tashkeel_required:
            language_specific_rules.append(
                "Include tashkeel (diacritics/harakat) on Arabic words to help with pronunciation."
            )

    # Formality rules for T-V distinction languages
    if config.formality_distinction:
        if formality == "formal":
            language_specific_rules.append(
                f"Use formal register (e.g., 'vous' in French, 'Sie' in German, 'usted' in Spanish) — "
                f"appropriate for {normalized_level} learners building standard vocabulary."
            )
        elif formality == "informal":
            language_specific_rules.append(
                f"Use informal register (e.g., 'tu' in French, 'du' in German, 'tú' in Spanish) — "
                f"conversational and approachable for {normalized_level} learners."
            )

    # Honorifics
    if config.honorifics:
        language_specific_rules.append(
            "Use polite/formal speech forms appropriate to the level. "
            "Explain honorific distinctions when introducing them."
        )

    # Script note
    if config.script_note:
        language_specific_rules.append(config.script_note)

    return {
        "language": config.language,
        "iso_code": config.iso_code,
        "script_direction": config.script_direction,
        "formality_for_level": formality,
        "formality_distinction": config.formality_distinction,
        "honorifics": config.honorifics,
        "script_note": config.script_note,
        "arabic_variety": arabic_variety,
        "arabic_msa_required": arabic_msa_required,
        "arabic_tashkeel_required": arabic_tashkeel_required,
        "rtl": config.arabic_config.rtl if config.arabic_config else False,
        "whatsapp_note": config.whatsapp_note,
        "language_specific_rules": language_specific_rules,
    }
