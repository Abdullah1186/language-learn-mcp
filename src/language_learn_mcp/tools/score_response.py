from ..config.cefr import get_cefr_config
from ..config.languages import get_language_config
from ..config.pedagogy import LEVEL_UP_THRESHOLD, LEVEL_DOWN_THRESHOLD


_CEFR_RUBRICS = {
    "A1": {
        "criteria": [
            "Can use familiar everyday expressions and very basic phrases",
            "Can introduce themselves and others",
            "Can use memorised single words and short phrases correctly",
            "Errors do not impede basic communication",
        ],
        "focus_areas": [
            "basic word order",
            "gender agreement (if applicable)",
            "present tense verb forms",
            "basic pronouns",
        ],
    },
    "A2": {
        "criteria": [
            "Can communicate in simple and routine tasks",
            "Can use short, simple sentences about familiar topics",
            "Can describe immediate surroundings and daily routines",
            "Errors are frequent but meaning is generally clear",
        ],
        "focus_areas": [
            "simple past tense",
            "preposition usage",
            "plural forms",
            "basic adjective agreement",
        ],
    },
    "B1": {
        "criteria": [
            "Can deal with most situations likely to arise while travelling",
            "Can produce simple connected text on familiar topics",
            "Can describe experiences, events, dreams, and ambitions",
            "Errors do not obscure meaning but may distract",
        ],
        "focus_areas": [
            "tense consistency across sentences",
            "subordinate clauses",
            "preposition accuracy",
            "vocabulary range and appropriateness",
        ],
    },
    "B2": {
        "criteria": [
            "Can interact with a degree of fluency and spontaneity",
            "Can produce clear, detailed text on a wide range of subjects",
            "Can explain a viewpoint on a topical issue giving the advantages and disadvantages",
            "Relatively few errors; self-correction evident",
        ],
        "focus_areas": [
            "subjunctive/conditional mood (if applicable)",
            "idiomatic expression accuracy",
            "discourse coherence",
            "register appropriateness",
        ],
    },
    "C1": {
        "criteria": [
            "Can express ideas fluently and spontaneously without much searching for expressions",
            "Can use language flexibly and effectively for social, academic, and professional purposes",
            "Can produce well-structured, detailed text on complex subjects",
            "Errors are rare and non-systematic",
        ],
        "focus_areas": [
            "idiomatic and nuanced vocabulary",
            "stylistic variety",
            "complex syntactic structures",
            "pragmatic appropriateness",
        ],
    },
    "C2": {
        "criteria": [
            "Can understand with ease virtually everything heard or read",
            "Can express themselves spontaneously, very fluently, and precisely",
            "Can differentiate finer shades of meaning even in complex situations",
            "Near-native accuracy",
        ],
        "focus_areas": [
            "subtle lexical distinctions",
            "native-like idiomatic usage",
            "stylistic range",
            "cultural and pragmatic nuance",
        ],
    },
}


def score_response(
    language: str,
    level: str,
    user_input: str,
    exercise_prompt: str | None = None,
    target_words: list[str] | None = None,
) -> dict:
    """
    Build a CEFR rubric for evaluating a learner's response.

    Returns the rubric text for an LLM to evaluate against, plus level-change signals
    based on how the response aligns with CEFR descriptors.
    """
    normalized_level = level.upper().strip()
    cefr_cfg = get_cefr_config(normalized_level)
    lang_cfg = get_language_config(language)
    lang_name = lang_cfg.language

    rubric_data = _CEFR_RUBRICS[normalized_level]

    # Build rubric prompt for the calling LLM
    rubric_lines = [
        f"Evaluate the following {lang_name} learner response at {normalized_level} CEFR level.",
        "",
        f"LEARNER RESPONSE: {user_input}",
    ]

    if exercise_prompt:
        rubric_lines.insert(0, f"EXERCISE: {exercise_prompt}\n")

    rubric_lines += [
        "",
        f"CEFR {normalized_level} CRITERIA — check if the response demonstrates:",
    ]
    for criterion in rubric_data["criteria"]:
        rubric_lines.append(f"  \u2713 {criterion}")

    rubric_lines += [
        "",
        "FOCUS AREAS — look specifically for errors in:",
    ]
    for area in rubric_data["focus_areas"]:
        rubric_lines.append(f"  \u2022 {area}")

    if target_words:
        rubric_lines += [
            "",
            f"TARGET VOCABULARY — check if these words are used correctly: {', '.join(target_words)}",
        ]

    rubric_lines += [
        "",
        "Score from 0.0 to 1.0 where:",
        "  1.0 = fully meets all CEFR criteria with minimal errors",
        "  0.7 = meets most criteria, errors present but comprehensible",
        "  0.4 = partially meets criteria, errors impede communication",
        "  0.0 = does not meet criteria",
        "",
        f"Correction style to use: {cefr_cfg.correction_style}",
    ]

    score_rubric = "\n".join(rubric_lines)

    # Heuristic signals (the calling code tracks actual score; these are thresholds)
    encouragement_note = (
        f"Acknowledge effort and progress. Remind the learner they are at {normalized_level} level "
        f"and improving their {lang_name}."
    )

    return {
        "cefr_estimate": normalized_level,
        "score_rubric": score_rubric,
        "suggest_level_up": False,   # caller should set True if actual score > LEVEL_UP_THRESHOLD over multiple turns
        "suggest_level_down": False,  # caller should set True if actual score < LEVEL_DOWN_THRESHOLD
        "correctness_focus_areas": rubric_data["focus_areas"],
        "encouragement_note": encouragement_note,
    }
