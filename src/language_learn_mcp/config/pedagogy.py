"""
Pedagogy constants grounded in SLA research.

Sources:
- Krashen (1982): Comprehensible Input / i+1 hypothesis
- CLIL research: 75% TL / 25% L1 optimal for intermediate+
- Alignment drift study (arXiv 2505.08351): CEFR prompts degrade over long dialogues
"""

# How often to re-inject mixing reminders (every N turns)
ANTI_DRIFT_INJECTION_INTERVAL: int = 6

# How many recent messages to inspect for drift detection
DRIFT_DETECTION_WINDOW: int = 6

# ±tolerance before flagging drift (0.10 = ±10%)
RATIO_TOLERANCE: float = 0.10

# Fraction of next-level (i+1) vocabulary to include in exercises
I_PLUS_ONE_STRETCH_RATIO: float = 0.30

# Score thresholds for level change recommendations
LEVEL_UP_THRESHOLD: float = 0.85    # suggest level up if score > this
LEVEL_DOWN_THRESHOLD: float = 0.40  # suggest level down if score < this

# Minimum messages before drift detection makes sense
MIN_MESSAGES_FOR_DRIFT: int = 2

# Arabic Unicode block range for character counting
ARABIC_UNICODE_START: int = 0x0600
ARABIC_UNICODE_END: int = 0x06FF

# Japanese Unicode ranges for character counting
HIRAGANA_START: int = 0x3040
HIRAGANA_END: int = 0x309F
KATAKANA_START: int = 0x30A0
KATAKANA_END: int = 0x30FF
CJK_START: int = 0x4E00
CJK_END: int = 0x9FFF

# Hebrew Unicode range
HEBREW_START: int = 0x0590
HEBREW_END: int = 0x05FF

# Cyrillic Unicode range
CYRILLIC_START: int = 0x0400
CYRILLIC_END: int = 0x04FF

# Devanagari Unicode range (Hindi)
DEVANAGARI_START: int = 0x0900
DEVANAGARI_END: int = 0x097F
