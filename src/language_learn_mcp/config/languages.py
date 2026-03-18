"""
Per-language configuration: formality, script direction, Arabic MSA enforcement,
dialect markers, and WhatsApp formatting notes.
"""

from ..types import CEFRLevel, ArabicConfig, DialectInfo, LanguageConfig

# ── Arabic Configuration ──────────────────────────────────────────────────────

ARABIC_CONFIG = ArabicConfig(
    default_variety="MSA",
    dialect_introduction_level="B2",
    tashkeel_required_until="A2",
    rtl=True,
    beginner_msa_note=(
        "MANDATORY: Use only Modern Standard Arabic (الفصحى / Fusha / MSA). "
        "Do NOT use Egyptian, Levantine, Gulf, or any other dialect. "
        "MSA is the international standard required for beginners and cross-regional communication."
    ),
    dialects=[
        DialectInfo(
            code="egy",
            name="Egyptian Arabic",
            region="Egypt",
            marker_words=["إيه", "عايز", "عايزة", "مش", "بتاع", "فين", "إزيك", "كويس", "أوي", "زي"],
            when_to_use="Only after B2 — most widely understood dialect due to Egyptian media influence.",
        ),
        DialectInfo(
            code="lev",
            name="Levantine Arabic",
            region="Syria, Lebanon, Jordan, Palestine",
            marker_words=["شو", "هيك", "كتير", "منيح", "بدي", "هلق", "يلا", "مبلا", "شي"],
            when_to_use="Only after B2 — relatively accessible grammar and pronunciation for learners.",
        ),
        DialectInfo(
            code="gulf",
            name="Gulf Arabic",
            region="Saudi Arabia, UAE, Kuwait, Qatar, Bahrain",
            marker_words=["وش", "چذي", "ابغى", "زين", "حدي", "يبغى", "هنيه"],
            when_to_use="Only after B2 — recommended for learners based in Gulf region.",
        ),
        DialectInfo(
            code="mag",
            name="Moroccan Arabic (Darija)",
            region="Morocco, Algeria, Tunisia",
            marker_words=["واش", "بزاف", "دابا", "خويا", "كيداير", "مزيان", "غادي"],
            when_to_use="Only after B2 — most distinct from MSA; best learned after solid MSA foundation.",
        ),
    ],
)

# ── Language Configs ──────────────────────────────────────────────────────────

_FORMALITY_INFORMAL_ALWAYS: dict[CEFRLevel, str] = {
    "A1": "informal", "A2": "informal", "B1": "informal",
    "B2": "informal", "C1": "informal", "C2": "informal",
}

_FORMALITY_FORMAL_FROM_B1: dict[CEFRLevel, str] = {
    "A1": "informal", "A2": "informal", "B1": "formal",
    "B2": "formal", "C1": "formal", "C2": "both",
}

LANGUAGE_CONFIGS: dict[str, LanguageConfig] = {
    "ar": LanguageConfig(
        language="Arabic",
        iso_code="ar",
        script_direction="rtl",
        formality_distinction=True,
        formality_default="formal",
        formality_by_level={
            "A1": "formal", "A2": "formal", "B1": "formal",
            "B2": "formal", "C1": "both", "C2": "both",
        },
        honorifics=False,
        script_note="Use Arabic script throughout. Include tashkeel (diacritics) at A1-A2 to aid pronunciation.",
        arabic_config=ARABIC_CONFIG,
        whatsapp_note="Arabic is RTL. WhatsApp renders Arabic script correctly. Use *bold* sparingly.",
    ),
    "fr": LanguageConfig(
        language="French",
        iso_code="fr",
        script_direction="ltr",
        formality_distinction=True,
        formality_default="informal",
        formality_by_level=_FORMALITY_FORMAL_FROM_B1,
        honorifics=False,
        script_note=None,
        arabic_config=None,
        whatsapp_note="Use *bold* for new French vocabulary words to highlight them.",
    ),
    "es": LanguageConfig(
        language="Spanish",
        iso_code="es",
        script_direction="ltr",
        formality_distinction=True,
        formality_default="informal",
        formality_by_level=_FORMALITY_FORMAL_FROM_B1,
        honorifics=False,
        script_note=None,
        arabic_config=None,
        whatsapp_note="Use *bold* for new Spanish vocabulary words to highlight them.",
    ),
    "de": LanguageConfig(
        language="German",
        iso_code="de",
        script_direction="ltr",
        formality_distinction=True,
        formality_default="informal",
        formality_by_level=_FORMALITY_FORMAL_FROM_B1,
        honorifics=False,
        script_note="Capitalize all nouns in German (e.g., das Haus, der Mann).",
        arabic_config=None,
        whatsapp_note="Use *bold* for new German words. Note noun gender with articles.",
    ),
    "ja": LanguageConfig(
        language="Japanese",
        iso_code="ja",
        script_direction="ltr",
        formality_distinction=True,
        formality_default="formal",
        formality_by_level={
            "A1": "formal", "A2": "formal", "B1": "formal",
            "B2": "both", "C1": "both", "C2": "both",
        },
        honorifics=True,
        script_note=(
            "A1-A2: Use hiragana primarily, introduce katakana for loanwords. "
            "B1+: Introduce common kanji with furigana. B2+: Reduce furigana for known kanji."
        ),
        arabic_config=None,
        whatsapp_note="Japanese renders correctly in WhatsApp. Use *bold* for new vocabulary.",
    ),
    "zh": LanguageConfig(
        language="Mandarin Chinese",
        iso_code="zh",
        script_direction="ltr",
        formality_distinction=False,
        formality_default="both",
        formality_by_level=_FORMALITY_INFORMAL_ALWAYS,
        honorifics=False,
        script_note="Use Simplified Chinese characters. Include pinyin romanization at A1-B1.",
        arabic_config=None,
        whatsapp_note="Chinese characters render correctly in WhatsApp. Include pinyin in parentheses for A1-B1.",
    ),
    "pt": LanguageConfig(
        language="Portuguese",
        iso_code="pt",
        script_direction="ltr",
        formality_distinction=True,
        formality_default="informal",
        formality_by_level=_FORMALITY_FORMAL_FROM_B1,
        honorifics=False,
        script_note=None,
        arabic_config=None,
        whatsapp_note="Use *bold* for new Portuguese vocabulary words.",
    ),
    "hi": LanguageConfig(
        language="Hindi",
        iso_code="hi",
        script_direction="ltr",
        formality_distinction=True,
        formality_default="informal",
        formality_by_level=_FORMALITY_FORMAL_FROM_B1,
        honorifics=False,
        script_note="Use Devanagari script. Include romanization at A1-A2.",
        arabic_config=None,
        whatsapp_note="Hindi Devanagari renders in WhatsApp. Include romanization for A1-A2 learners.",
    ),
    "ko": LanguageConfig(
        language="Korean",
        iso_code="ko",
        script_direction="ltr",
        formality_distinction=True,
        formality_default="formal",
        formality_by_level={
            "A1": "formal", "A2": "formal", "B1": "formal",
            "B2": "both", "C1": "both", "C2": "both",
        },
        honorifics=True,
        script_note="Use Hangul throughout. A1-A2: focus on polite formal speech (합쇼체/해요체). B2+: introduce casual (반말).",
        arabic_config=None,
        whatsapp_note="Korean Hangul renders correctly in WhatsApp.",
    ),
    "ru": LanguageConfig(
        language="Russian",
        iso_code="ru",
        script_direction="ltr",
        formality_distinction=True,
        formality_default="informal",
        formality_by_level=_FORMALITY_FORMAL_FROM_B1,
        honorifics=False,
        script_note="Use Cyrillic script. Include romanization at A1 only.",
        arabic_config=None,
        whatsapp_note="Cyrillic renders correctly in WhatsApp.",
    ),
    "it": LanguageConfig(
        language="Italian",
        iso_code="it",
        script_direction="ltr",
        formality_distinction=True,
        formality_default="informal",
        formality_by_level=_FORMALITY_FORMAL_FROM_B1,
        honorifics=False,
        script_note=None,
        arabic_config=None,
        whatsapp_note="Use *bold* for new Italian vocabulary words.",
    ),
    "tr": LanguageConfig(
        language="Turkish",
        iso_code="tr",
        script_direction="ltr",
        formality_distinction=True,
        formality_default="informal",
        formality_by_level=_FORMALITY_FORMAL_FROM_B1,
        honorifics=False,
        script_note="Turkish uses Latin alphabet with special characters: ç, ğ, ı, ö, ş, ü.",
        arabic_config=None,
        whatsapp_note="Use *bold* for new Turkish words. Ensure special characters are preserved.",
    ),
}

# Name aliases for flexible lookup (e.g. "arabic" → "ar", "french" → "fr")
_NAME_TO_ISO: dict[str, str] = {
    config.language.lower(): iso
    for iso, config in LANGUAGE_CONFIGS.items()
}
_NAME_TO_ISO.update({
    "mandarin": "zh",
    "chinese": "zh",
    "mandarin chinese": "zh",
})

# Generic fallback for languages not explicitly configured
_GENERIC_CONFIG_TEMPLATE = dict(
    script_direction="ltr",
    formality_distinction=False,
    formality_default="informal",
    formality_by_level={
        "A1": "informal", "A2": "informal", "B1": "informal",
        "B2": "informal", "C1": "informal", "C2": "informal",
    },
    honorifics=False,
    script_note=None,
    arabic_config=None,
    whatsapp_note="Use *bold* for new vocabulary words to highlight them.",
)


def get_language_config(language: str) -> LanguageConfig:
    """
    Return LanguageConfig for a language name or ISO code.
    Falls back to a generic config for unlisted languages.
    """
    normalized = language.strip().lower()

    # Try ISO code first
    if normalized in LANGUAGE_CONFIGS:
        return LANGUAGE_CONFIGS[normalized]

    # Try display name
    if normalized in _NAME_TO_ISO:
        return LANGUAGE_CONFIGS[_NAME_TO_ISO[normalized]]

    # Fallback: generic config
    return LanguageConfig(
        language=language.strip().title(),
        iso_code=normalized[:2],
        **_GENERIC_CONFIG_TEMPLATE,  # type: ignore[arg-type]
    )
