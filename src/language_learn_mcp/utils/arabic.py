"""
Arabic-specific utilities: dialect detection and Unicode helpers.
Used by detect_drift tool.
"""

from ..config.languages import get_language_config
from ..config.pedagogy import ARABIC_UNICODE_START, ARABIC_UNICODE_END


def count_arabic_chars(text: str) -> int:
    """Count characters in the Arabic Unicode block (U+0600–U+06FF)."""
    return sum(
        1 for ch in text
        if ARABIC_UNICODE_START <= ord(ch) <= ARABIC_UNICODE_END
    )


def detect_arabic_dialect(text: str) -> str | None:
    """
    Scan text for dialect marker words.
    Returns the dialect code (e.g. 'egy', 'lev') or None if only MSA detected.
    """
    lang_config = get_language_config("arabic")
    if lang_config.arabic_config is None:
        return None

    text_lower = text.lower()
    for dialect in lang_config.arabic_config.dialects:
        for marker in dialect.marker_words:
            if marker in text_lower or marker in text:
                return dialect.code
    return None


def is_tashkeel_required(level: str) -> bool:
    """Return True if diacritics (tashkeel) should be required at this level."""
    from ..utils.cefr import is_level_gte
    from ..config.languages import get_language_config

    lang_config = get_language_config("arabic")
    if lang_config.arabic_config is None:
        return False

    cutoff = lang_config.arabic_config.tashkeel_required_until
    # Required if level <= cutoff (e.g., A1, A2)
    return not is_level_gte(level, cutoff) or level.upper() == cutoff.upper()
