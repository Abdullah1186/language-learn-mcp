from ..config.cefr import get_cefr_config
from ..config.languages import get_language_config
from ..utils.cefr import get_i_plus_one_level, is_level_gte
from ..config.pedagogy import I_PLUS_ONE_STRETCH_RATIO


_EXERCISE_TEMPLATES = {
    "translation": (
        "Present the learner with {count} {source_lang} sentences or words and ask them to translate "
        "into {target_lang}. Use vocabulary from the {level} CEFR range. "
        "Format as a numbered list. After each response, confirm or gently correct."
    ),
    "fill_in_blank": (
        "Create {count} fill-in-the-blank sentences in {target_lang} at {level} level. "
        "Each sentence should have one blank marked with ___. "
        "Provide a word bank of options below the sentences (including distractors). "
        "Format as a numbered list."
    ),
    "multiple_choice": (
        "Create {count} multiple-choice questions testing {target_lang} vocabulary or grammar at {level} level. "
        "Each question has 4 options (A-D). Only one is correct. "
        "Present one question at a time and wait for the learner's answer."
    ),
    "sentence_construction": (
        "Give the learner {count} sets of {target_lang} words in scrambled order. "
        "Ask them to arrange the words into a correct sentence. "
        "Use {level}-appropriate grammar structures. Format as a numbered list."
    ),
    "listening_comprehension_prompt": (
        "Write a short {target_lang} passage ({word_count} words) on the topic: {topic}. "
        "Use {level} vocabulary and sentence structures. "
        "Then ask {count} comprehension questions about the passage. "
        "Present the passage first, then ask: 'Please read the passage and answer these questions.'"
    ),
    "error_correction": (
        "Write {count} {target_lang} sentences that each contain exactly one error appropriate for a "
        "{level} learner to find (e.g., wrong verb conjugation, incorrect gender agreement, wrong preposition). "
        "Ask the learner to identify and correct the error in each sentence. Format as a numbered list."
    ),
}

_LEVEL_WORD_COUNTS = {
    "A1": 30, "A2": 50, "B1": 80, "B2": 120, "C1": 160, "C2": 200
}


def generate_exercise(
    language: str,
    level: str,
    type: str,
    topic: str | None = None,
    weak_words: list[str] | None = None,
    arabic_variety: str | None = None,
) -> dict:
    """
    Return a structured exercise instruction template using Krashen's i+1 principle.

    If weak_words provided -> accessible difficulty (targeting known weak spots).
    If no weak_words -> stretch difficulty (i+1, one level above).
    """
    normalized_level = level.upper().strip()
    exercise_type = type.lower().strip()

    valid_types = list(_EXERCISE_TEMPLATES.keys())
    if exercise_type not in valid_types:
        raise ValueError(f"Invalid exercise type: {type!r}. Must be one of: {valid_types}")

    cefr_cfg = get_cefr_config(normalized_level)
    lang_cfg = get_language_config(language)
    lang_name = lang_cfg.language

    # i+1 logic: determine difficulty
    i_plus_one = get_i_plus_one_level(normalized_level)
    if weak_words:
        expected_difficulty = "accessible"
        vocab_level = normalized_level
        level_justification = (
            f"Targeting weak words {weak_words[:3]}{'...' if len(weak_words) > 3 else ''} "
            f"at {normalized_level} level — accessible difficulty to reinforce known gaps."
        )
    elif i_plus_one:
        expected_difficulty = "stretch"
        vocab_level = i_plus_one
        level_justification = (
            f"Using i+1 vocabulary ({i_plus_one} level, ~{int(I_PLUS_ONE_STRETCH_RATIO*100)}% stretch) "
            f"to push the learner just beyond their current {normalized_level} comfort zone per Krashen's hypothesis."
        )
    else:
        expected_difficulty = "on-level"
        vocab_level = normalized_level
        level_justification = f"At C2 level — on-level exercise using mastery-range vocabulary."

    # Determine effective Arabic variety
    effective_arabic_variety = None
    if lang_cfg.arabic_config is not None:
        if not is_level_gte(normalized_level, lang_cfg.arabic_config.dialect_introduction_level):
            effective_arabic_variety = "MSA"
        else:
            effective_arabic_variety = arabic_variety or "MSA"

    # Build the exercise prompt
    topic_str = topic or "everyday life"
    word_count = _LEVEL_WORD_COUNTS.get(normalized_level, 80)
    count = 3 if normalized_level in ("A1", "A2") else 5

    template = _EXERCISE_TEMPLATES[exercise_type]
    prompt = template.format(
        count=count,
        target_lang=lang_name + (" (MSA)" if effective_arabic_variety == "MSA" else ""),
        source_lang="English",
        level=vocab_level,
        topic=topic_str,
        word_count=word_count,
    )

    # Add weak word targeting
    if weak_words:
        prompt += f"\n\nFocus on these specific words/phrases: {', '.join(weak_words[:5])}"

    # Add Arabic MSA reminder
    if effective_arabic_variety == "MSA":
        prompt += "\n\nIMPORTANT: Use only Modern Standard Arabic (MSA/Fusha) in this exercise."

    # Scaffolding notes (hints if learner is stuck)
    scaffolding_notes = _get_scaffolding_notes(exercise_type, normalized_level, lang_name)

    return {
        "prompt": prompt,
        "exercise_type": exercise_type,
        "target_vocabulary": weak_words or [],
        "level_justification": level_justification,
        "scaffolding_notes": scaffolding_notes,
        "expected_difficulty": expected_difficulty,
        "arabic_variety_used": effective_arabic_variety,
    }


def _get_scaffolding_notes(exercise_type: str, level: str, language: str) -> str:
    notes = {
        "translation": (
            f"If the learner is stuck, offer the first letter of the answer as a hint. "
            f"For A1-A2 learners, accept approximate translations."
        ),
        "fill_in_blank": (
            "If the learner cannot answer after two attempts, reveal the answer and explain why it is correct."
        ),
        "multiple_choice": (
            "If the learner chooses incorrectly, explain why the correct answer is right "
            "without revealing other questions' answers."
        ),
        "sentence_construction": (
            "If stuck, offer to reveal one correctly-placed word as a starting hint."
        ),
        "listening_comprehension_prompt": (
            "If the learner struggles, offer to re-read the key sentence containing the answer "
            "and ask them to focus on that section."
        ),
        "error_correction": (
            "If the learner cannot find the error, narrow it down: tell them which part of speech "
            "contains the error (verb, noun, preposition, etc.)."
        ),
    }
    return notes.get(exercise_type, "Offer a hint if the learner cannot answer after two attempts.")
