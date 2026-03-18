from __future__ import annotations
from dataclasses import dataclass, field
from typing import Literal, TypedDict

# ── CEFR Level ────────────────────────────────────────────────────────────────

CEFRLevel = Literal["A1", "A2", "B1", "B2", "C1", "C2"]
CEFR_LEVELS: list[CEFRLevel] = ["A1", "A2", "B1", "B2", "C1", "C2"]

# ── Config Data Structures ────────────────────────────────────────────────────

@dataclass
class MixingRatio:
    target_language_percent: int       # 0–100
    native_language_percent: int       # 0–100
    always_translate: bool             # translate every TL word?
    translate_new_vocab: bool          # translate only new words?
    description: str                   # human-readable label
    research_basis: str                # citation/rationale


@dataclass
class CEFRMixingConfig:
    level: CEFRLevel
    ratio: MixingRatio
    i_plus_one_level: CEFRLevel | None  # next level per Krashen i+1 (None at C2)
    instruction_style: str              # e.g. "pen-pal", "immersive"
    correction_style: str              # how to handle errors at this level
    vocabulary_range: str              # e.g. "~500 words (A1 CEFR)"


@dataclass
class DialectInfo:
    code: str            # e.g. "egy", "lev", "gulf", "mag"
    name: str            # e.g. "Egyptian Arabic"
    region: str
    marker_words: list[str]   # words/tokens that identify this dialect
    when_to_use: str


@dataclass
class ArabicConfig:
    default_variety: str              # always "MSA" for beginners
    dialect_introduction_level: CEFRLevel  # "B2"
    dialects: list[DialectInfo]
    tashkeel_required_until: CEFRLevel     # "A2" — diacritics for beginners
    rtl: bool
    beginner_msa_note: str            # instruction to embed in system prompt


@dataclass
class LanguageConfig:
    language: str                     # display name: "Arabic", "French", etc.
    iso_code: str                     # BCP-47: "ar", "fr", "ja", etc.
    script_direction: Literal["ltr", "rtl", "mixed"]
    formality_distinction: bool       # T-V distinction (tu/vous, tú/usted)?
    formality_default: Literal["formal", "informal", "both"]
    formality_by_level: dict[CEFRLevel, Literal["formal", "informal", "both"]]
    honorifics: bool                  # Japanese keigo, Korean levels, etc.
    script_note: str | None           # hiragana→kanji progression, etc.
    arabic_config: ArabicConfig | None
    whatsapp_note: str                # platform-specific formatting tips


# ── Tool Input TypedDicts ─────────────────────────────────────────────────────

class GetMixingConfigInput(TypedDict):
    level: str   # CEFRLevel — validated at runtime
    language: str


class GetLanguageConfigInput(TypedDict):
    language: str
    level: str   # CEFRLevel


class BuildSystemPromptInput(TypedDict, total=False):
    language: str
    level: str
    persona: str          # "pen-pal" | "tutor" | "conversation-partner"
    app_context: str      # e.g. "WhatsApp, keep replies under 300 chars"
    reinforcement_note: str
    arabic_variety: str   # "MSA" or dialect code


class GenerateExerciseInput(TypedDict, total=False):
    language: str
    level: str
    type: str             # exercise type — see ExerciseType below
    topic: str
    weak_words: list[str]
    arabic_variety: str


class BuildVocabInputInput(TypedDict, total=False):
    language: str
    level: str
    count: int            # 1–10
    topic: str
    weak_words: list[str]
    arabic_variety: str


class ScoreResponseInput(TypedDict, total=False):
    language: str
    level: str
    user_input: str
    exercise_prompt: str
    target_words: list[str]


class DetectDriftInput(TypedDict, total=False):
    language: str
    level: str
    recent_messages: list[dict]   # list of {"role": "user"|"assistant", "content": str}
    window_size: int


class GetReinforcementNoteInput(TypedDict, total=False):
    language: str
    level: str
    turn_number: int
    last_drift_result: dict | None
    arabic_variety: str


# ── Tool Output TypedDicts ────────────────────────────────────────────────────

class MixingConfigOutput(TypedDict):
    level: str
    target_language_percent: int
    native_language_percent: int
    always_translate: bool
    translate_new_vocab: bool
    description: str
    research_basis: str
    i_plus_one_level: str | None
    instruction_style: str
    correction_style: str
    vocabulary_range: str


class LanguageConfigOutput(TypedDict):
    language: str
    iso_code: str
    script_direction: str
    formality_for_level: str
    formality_distinction: bool
    honorifics: bool
    script_note: str | None
    arabic_variety: str | None        # "MSA" if Arabic and level < B2
    arabic_msa_required: bool
    arabic_tashkeel_required: bool
    rtl: bool
    whatsapp_note: str
    language_specific_rules: list[str]


class SystemPromptOutput(TypedDict):
    system_prompt: str
    anti_drift_reminder: str
    mixing_summary: str
    language_specific_rules: list[str]


class ExerciseOutput(TypedDict):
    prompt: str
    exercise_type: str
    target_vocabulary: list[str]
    level_justification: str
    scaffolding_notes: str
    expected_difficulty: str   # "accessible" | "on-level" | "stretch"
    arabic_variety_used: str | None


class VocabItem(TypedDict):
    word: str
    part_of_speech: str
    definition: str           # in English (learner's native language)
    example_sentence: str     # in target language, level-appropriate
    example_translation: str  # provided for A1-B1, optional for B2+
    cefr_level: str
    pronunciation_note: str | None
    arabic_diacritics: str | None  # tashkeel form (Arabic only)


class VocabInputOutput(TypedDict):
    items: list[VocabItem]
    comprehensible_input_passage: str | None  # short passage using all words (B1+)
    level_note: str
    arabic_variety_used: str | None


class ScoreOutput(TypedDict):
    cefr_estimate: str        # CEFRLevel or "below-A1" or "above-C2"
    score_rubric: str         # the rubric text for the LLM to evaluate against
    suggest_level_up: bool
    suggest_level_down: bool
    correctness_focus_areas: list[str]  # what to check at this level
    encouragement_note: str


class DriftOutput(TypedDict):
    drift_detected: bool
    drift_type: str           # "language-mix" | "formality" | "dialect" | "none"
    estimated_target_percent: float   # estimated % of target language in recent msgs
    target_percent: int               # what it should be
    severity: str             # "none" | "mild" | "significant"
    correction_instruction: str       # text to inject back into agent


class ReinforcementOutput(TypedDict):
    should_inject: bool
    note: str
    injection_reason: str     # "scheduled" | "drift-corrective" | "dialect" | "none"


# ── Exercise Types ────────────────────────────────────────────────────────────

ExerciseType = Literal[
    "translation",
    "fill_in_blank",
    "multiple_choice",
    "sentence_construction",
    "listening_comprehension_prompt",
    "error_correction",
]

EXERCISE_TYPES: list[ExerciseType] = [
    "translation",
    "fill_in_blank",
    "multiple_choice",
    "sentence_construction",
    "listening_comprehension_prompt",
    "error_correction",
]
