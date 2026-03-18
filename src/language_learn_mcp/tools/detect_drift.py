from ..config.cefr import get_cefr_config
from ..config.languages import get_language_config
from ..utils.arabic import count_arabic_chars, detect_arabic_dialect
from ..config.pedagogy import (
    DRIFT_DETECTION_WINDOW,
    RATIO_TOLERANCE,
    MIN_MESSAGES_FOR_DRIFT,
    ARABIC_UNICODE_START, ARABIC_UNICODE_END,
    HIRAGANA_START, HIRAGANA_END,
    KATAKANA_START, KATAKANA_END,
    CJK_START, CJK_END,
    HEBREW_START, HEBREW_END,
    CYRILLIC_START, CYRILLIC_END,
    DEVANAGARI_START, DEVANAGARI_END,
)


# High-frequency diacritic characters for Latin-script TL detection
_LATIN_TL_DIACRITICS = set("àáâãäåæçèéêëìíîïðñòóôõöùúûüýþÿœšžÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖÙÚÛÜÝÞŸŒŠŽ")


def _count_target_language_chars(text: str, iso_code: str) -> tuple[int, int]:
    """
    Return (target_lang_chars, total_alpha_chars) for the given text and language.
    Uses Unicode block ranges for non-Latin scripts; diacritic heuristics for Latin.
    """
    total_alpha = sum(1 for ch in text if ch.isalpha())
    if total_alpha == 0:
        return 0, 0

    if iso_code == "ar":
        tl_chars = count_arabic_chars(text)
    elif iso_code == "ja":
        tl_chars = sum(
            1 for ch in text
            if (HIRAGANA_START <= ord(ch) <= HIRAGANA_END
                or KATAKANA_START <= ord(ch) <= KATAKANA_END
                or CJK_START <= ord(ch) <= CJK_END)
        )
    elif iso_code == "zh":
        tl_chars = sum(1 for ch in text if CJK_START <= ord(ch) <= CJK_END)
    elif iso_code == "he":
        tl_chars = sum(1 for ch in text if HEBREW_START <= ord(ch) <= HEBREW_END)
    elif iso_code == "ru":
        tl_chars = sum(1 for ch in text if CYRILLIC_START <= ord(ch) <= CYRILLIC_END)
    elif iso_code == "hi":
        tl_chars = sum(1 for ch in text if DEVANAGARI_START <= ord(ch) <= DEVANAGARI_END)
    else:
        # Latin-script language: count diacritics + estimate from word ratio
        diacritic_chars = sum(1 for ch in text if ch in _LATIN_TL_DIACRITICS)
        # Rough heuristic: if >10% of alpha chars have diacritics, count those words
        tl_chars = min(diacritic_chars * 4, total_alpha)  # rough word estimate

    return tl_chars, total_alpha


def detect_drift(
    language: str,
    level: str,
    recent_messages: list[dict],
    window_size: int | None = None,
) -> dict:
    """
    Analyse recent message history and detect language mixing drift.

    Pure Python computation — no LLM calls, sub-millisecond execution.
    Uses Unicode block ranges for script-based languages.
    For Arabic: also scans for dialect marker words.
    """
    normalized_level = level.upper().strip()
    window = window_size or DRIFT_DETECTION_WINDOW

    cefr_cfg = get_cefr_config(normalized_level)
    lang_cfg = get_language_config(language)

    target_tl_percent = cefr_cfg.ratio.target_language_percent

    # Filter to assistant messages only within window
    assistant_msgs = [
        m for m in recent_messages
        if isinstance(m, dict) and m.get("role") == "assistant"
    ][-window:]

    # Arabic dialect check runs on ANY number of messages — even one dialect word is a violation
    if lang_cfg.arabic_config is not None:
        all_assistant_text = " ".join(m.get("content", "") for m in assistant_msgs)
        dialect_code = detect_arabic_dialect(all_assistant_text)
        if dialect_code:
            from ..utils.cefr import is_level_gte
            dialect_allowed = is_level_gte(
                normalized_level,
                lang_cfg.arabic_config.dialect_introduction_level
            )
            if not dialect_allowed:
                dialect_name = next(
                    (d.name for d in lang_cfg.arabic_config.dialects if d.code == dialect_code),
                    dialect_code
                )
                return {
                    "drift_detected": True,
                    "drift_type": "dialect",
                    "estimated_target_percent": float(target_tl_percent),
                    "target_percent": target_tl_percent,
                    "severity": "significant",
                    "correction_instruction": (
                        f"DIALECT DETECTED ({dialect_name}): You are using Arabic dialect at {normalized_level} level. "
                        f"Switch IMMEDIATELY to Modern Standard Arabic (MSA/Fusha). "
                        f"Dialect is not introduced until {lang_cfg.arabic_config.dialect_introduction_level}."
                    ),
                }

    # Not enough messages for reliable ratio measurement
    if len(assistant_msgs) < MIN_MESSAGES_FOR_DRIFT:
        return {
            "drift_detected": False,
            "drift_type": "none",
            "estimated_target_percent": float(target_tl_percent),
            "target_percent": target_tl_percent,
            "severity": "none",
            "correction_instruction": "",
        }

    # Measure target language ratio
    total_tl = 0
    total_alpha = 0
    for msg in assistant_msgs:
        content = msg.get("content", "")
        tl_chars, alpha_chars = _count_target_language_chars(content, lang_cfg.iso_code)
        total_tl += tl_chars
        total_alpha += alpha_chars

    if total_alpha == 0:
        estimated_pct = 0.0
    else:
        estimated_pct = round((total_tl / total_alpha) * 100, 1)

    # Determine drift severity
    diff = estimated_pct - target_tl_percent
    abs_diff = abs(diff)
    tolerance_pct = RATIO_TOLERANCE * 100

    if abs_diff <= tolerance_pct:
        severity = "none"
        drift_detected = False
        drift_type = "none"
        correction = ""
    elif abs_diff <= tolerance_pct * 2:
        severity = "mild"
        drift_detected = True
        drift_type = "language-mix"
        direction = "low" if diff < 0 else "high"
        correction = (
            f"Language mix drift ({severity}): currently ~{estimated_pct:.0f}% {lang_cfg.language}, "
            f"target is {target_tl_percent}% (running {direction}). "
            f"Adjust your next reply to use more "
            + (lang_cfg.language if diff < 0 else "English")
            + "."
        )
    else:
        severity = "significant"
        drift_detected = True
        drift_type = "language-mix"
        correction = (
            f"SIGNIFICANT language mix drift: currently ~{estimated_pct:.0f}% {lang_cfg.language}, "
            f"target is {target_tl_percent}% for {normalized_level}. "
            f"IMMEDIATELY adjust to {'increase' if diff < 0 else 'reduce'} {lang_cfg.language} usage."
        )

    return {
        "drift_detected": drift_detected,
        "drift_type": drift_type,
        "estimated_target_percent": estimated_pct,
        "target_percent": target_tl_percent,
        "severity": severity,
        "correction_instruction": correction,
    }
