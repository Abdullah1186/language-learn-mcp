"""Utility functions for CEFR level comparison and progression."""

from ..types import CEFRLevel, CEFR_LEVELS


def get_i_plus_one_level(level: str) -> CEFRLevel | None:
    """Return the next CEFR level (i+1 in Krashen's model), or None at C2."""
    normalized = level.upper().strip()
    if normalized not in CEFR_LEVELS:
        raise ValueError(f"Invalid CEFR level: {level!r}")
    idx = CEFR_LEVELS.index(normalized)  # type: ignore[arg-type]
    return CEFR_LEVELS[idx + 1] if idx < len(CEFR_LEVELS) - 1 else None


def compare_levels(level_a: str, level_b: str) -> int:
    """
    Compare two CEFR levels.
    Returns -1 if a < b, 0 if equal, 1 if a > b.
    """
    a = level_a.upper().strip()
    b = level_b.upper().strip()
    if a not in CEFR_LEVELS or b not in CEFR_LEVELS:
        raise ValueError(f"Invalid level(s): {level_a!r}, {level_b!r}")
    idx_a = CEFR_LEVELS.index(a)  # type: ignore[arg-type]
    idx_b = CEFR_LEVELS.index(b)  # type: ignore[arg-type]
    return 0 if idx_a == idx_b else (1 if idx_a > idx_b else -1)


def is_level_gte(level: str, minimum: str) -> bool:
    """Return True if level >= minimum."""
    return compare_levels(level, minimum) >= 0
