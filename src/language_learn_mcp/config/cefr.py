"""
CEFR-level mixing configurations grounded in SLA research.

Corrects poly-pal's LEVEL_BALANCE dict which used incorrect ratios.
Research basis: CLIL 75/25 rule, Krashen i+1, CEFR descriptors.
"""

from ..types import CEFRLevel, CEFRMixingConfig, MixingRatio

CEFR_CONFIGS: dict[CEFRLevel, CEFRMixingConfig] = {
    "A1": CEFRMixingConfig(
        level="A1",
        ratio=MixingRatio(
            target_language_percent=15,
            native_language_percent=85,
            always_translate=True,
            translate_new_vocab=True,
            description="Single words and very short phrases only. English explains everything.",
            research_basis="A1 CEFR descriptor: can use familiar everyday expressions and very basic phrases",
        ),
        i_plus_one_level="A2",
        instruction_style="pen-pal",
        correction_style="Warmly rephrase in English first, then repeat the correct target-language word or phrase.",
        vocabulary_range="~500 words (A1 CEFR core vocabulary)",
    ),
    "A2": CEFRMixingConfig(
        level="A2",
        ratio=MixingRatio(
            target_language_percent=30,
            native_language_percent=70,
            always_translate=True,
            translate_new_vocab=True,
            description="Short phrases and simple sentences. Translate all target-language words inline.",
            research_basis="A2 CEFR descriptor: can communicate in simple and routine tasks requiring a simple and direct exchange of information",
        ),
        i_plus_one_level="B1",
        instruction_style="pen-pal",
        correction_style="Gently echo the correct form in target language, then continue in English.",
        vocabulary_range="~1,000 words (A2 CEFR core vocabulary)",
    ),
    "B1": CEFRMixingConfig(
        level="B1",
        ratio=MixingRatio(
            target_language_percent=60,
            native_language_percent=40,
            always_translate=False,
            translate_new_vocab=True,
            description="Mostly target language. Translate only new or complex vocabulary inline.",
            research_basis="CLIL research: 75/25 TL/L1 ratio optimal for intermediate learners; B1 approximated at 60/40",
        ),
        i_plus_one_level="B2",
        instruction_style="conversation-partner",
        correction_style="Note the error naturally in passing — rephrase what they said correctly and continue.",
        vocabulary_range="~2,000 words (B1 CEFR vocabulary)",
    ),
    "B2": CEFRMixingConfig(
        level="B2",
        ratio=MixingRatio(
            target_language_percent=80,
            native_language_percent=20,
            always_translate=False,
            translate_new_vocab=False,
            description="Almost entirely target language. Use English only for complex explanations.",
            research_basis="CLIL 75/25 rule applied at B2; research shows intermediate+ learners benefit from near-immersion",
        ),
        i_plus_one_level="C1",
        instruction_style="conversation-partner",
        correction_style="Briefly correct without interrupting the conversational flow.",
        vocabulary_range="~4,000 words (B2 CEFR vocabulary)",
    ),
    "C1": CEFRMixingConfig(
        level="C1",
        ratio=MixingRatio(
            target_language_percent=90,
            native_language_percent=10,
            always_translate=False,
            translate_new_vocab=False,
            description="Target language throughout. Minimal English only for rare nuance.",
            research_basis="C1 CEFR descriptor: can express ideas fluently and spontaneously without much obvious searching for expressions",
        ),
        i_plus_one_level="C2",
        instruction_style="immersive",
        correction_style="Only correct significant errors that impede understanding or sound unnatural.",
        vocabulary_range="~8,000 words (C1 CEFR vocabulary)",
    ),
    "C2": CEFRMixingConfig(
        level="C2",
        ratio=MixingRatio(
            target_language_percent=100,
            native_language_percent=0,
            always_translate=False,
            translate_new_vocab=False,
            description="100% target language. Native-level interaction.",
            research_basis="C2 CEFR descriptor: can understand with ease virtually everything heard or read",
        ),
        i_plus_one_level=None,
        instruction_style="immersive",
        correction_style="Correct only when necessary, as a native speaker would with another native speaker.",
        vocabulary_range="16,000+ words (C2 CEFR mastery)",
    ),
}


def get_cefr_config(level: str) -> CEFRMixingConfig:
    """Return the CEFR config for a level string, with validation."""
    normalized = level.upper().strip()
    if normalized not in CEFR_CONFIGS:
        raise ValueError(f"Invalid CEFR level: {level!r}. Must be one of A1, A2, B1, B2, C1, C2.")
    return CEFR_CONFIGS[normalized]  # type: ignore[index]
