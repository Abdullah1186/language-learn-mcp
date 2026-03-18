from ..config.cefr import get_cefr_config
from ..config.languages import get_language_config
from ..utils.cefr import get_i_plus_one_level, is_level_gte
from ..utils.arabic import is_tashkeel_required
from ..config.pedagogy import I_PLUS_ONE_STRETCH_RATIO


def build_vocab_input(
    language: str,
    level: str,
    count: int = 1,
    topic: str | None = None,
    weak_words: list[str] | None = None,
    arabic_variety: str | None = None,
) -> dict:
    """
    Return a structured vocabulary template following Krashen's comprehensible input principle.

    Blend: 70% current-level vocabulary + 30% i+1-level vocabulary.
    Arabic A1-A2: tashkeel (diacritics) field required.
    B1+: includes comprehensible_input_passage instruction.
    """
    if not 1 <= count <= 10:
        raise ValueError(f"count must be between 1 and 10, got {count}")

    normalized_level = level.upper().strip()
    cefr_cfg = get_cefr_config(normalized_level)
    lang_cfg = get_language_config(language)
    lang_name = lang_cfg.language

    i_plus_one = get_i_plus_one_level(normalized_level)
    stretch_count = max(1, round(count * I_PLUS_ONE_STRETCH_RATIO)) if i_plus_one and count > 1 else 0
    current_count = count - stretch_count

    # Determine Arabic config
    effective_arabic_variety = None
    tashkeel_required = False
    if lang_cfg.arabic_config is not None:
        effective_arabic_variety = "MSA"
        tashkeel_required = is_tashkeel_required(normalized_level)

    topic_str = topic or "everyday conversation"

    # Build template items
    items: list[dict] = []

    for i in range(count):
        is_stretch = i >= current_count and stretch_count > 0
        item_level = i_plus_one if (is_stretch and i_plus_one) else normalized_level
        include_translation = cefr_cfg.ratio.always_translate or cefr_cfg.ratio.translate_new_vocab

        item: dict = {
            "word": f"[Generate a {item_level}-level {lang_name} word related to: {topic_str}]",
            "part_of_speech": "[noun/verb/adjective/adverb/etc.]",
            "definition": "[English definition]",
            "example_sentence": (
                f"[{item_level}-appropriate example sentence in {lang_name}"
                + (" (MSA only)" if effective_arabic_variety == "MSA" else "")
                + "]"
            ),
            "example_translation": "[English translation]" if include_translation else None,
            "cefr_level": item_level,
            "pronunciation_note": f"[IPA or phonetic hint for {lang_name}]" if normalized_level in ("A1", "A2") else None,
            "arabic_diacritics": (
                "[Word with full tashkeel/harakat]" if tashkeel_required else None
            ),
        }

        if weak_words and i < len(weak_words):
            item["word"] = weak_words[i]
            item["example_sentence"] = (
                f"[Example sentence using '{weak_words[i]}' at {normalized_level} level]"
            )

        items.append(item)

    # Comprehensible input passage (B1+ and count >= 3)
    comprehensible_input_passage = None
    if is_level_gte(normalized_level, "B1") and count >= 3:
        comprehensible_input_passage = (
            f"[Write a short {lang_name} paragraph (4-6 sentences) on the topic '{topic_str}' "
            f"that naturally uses all {count} vocabulary words above. "
            f"Use {normalized_level}-appropriate structures throughout."
            + (" Use only MSA." if effective_arabic_variety == "MSA" else "")
            + "]"
        )

    level_note = (
        f"{current_count} word(s) at {normalized_level} level"
        + (f", {stretch_count} at {i_plus_one} level (Krashen i+1 stretch)" if stretch_count > 0 else "")
        + ("" if not tashkeel_required else ". Tashkeel (diacritics) required for all Arabic words.")
    )

    return {
        "items": items,
        "comprehensible_input_passage": comprehensible_input_passage,
        "level_note": level_note,
        "arabic_variety_used": effective_arabic_variety,
    }
