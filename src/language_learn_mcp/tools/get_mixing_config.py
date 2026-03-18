from ..config.cefr import get_cefr_config
from ..config.languages import get_language_config


def get_mixing_config(level: str, language: str) -> dict:
    """
    Return the research-grounded language mixing configuration for a CEFR level.

    Corrects poly-pal's LEVEL_BALANCE which used incorrect ratios.
    Research basis: CLIL 75/25 rule, Krashen i+1, CEFR descriptors.
    """
    config = get_cefr_config(level)  # validates level
    lang_config = get_language_config(language)  # normalizes language name

    return {
        "level": config.level,
        "target_language_percent": config.ratio.target_language_percent,
        "native_language_percent": config.ratio.native_language_percent,
        "always_translate": config.ratio.always_translate,
        "translate_new_vocab": config.ratio.translate_new_vocab,
        "description": config.ratio.description,
        "research_basis": config.ratio.research_basis,
        "i_plus_one_level": config.i_plus_one_level,
        "instruction_style": config.instruction_style,
        "correction_style": config.correction_style,
        "vocabulary_range": config.vocabulary_range,
        "language": lang_config.language,
        "iso_code": lang_config.iso_code,
    }
