"""
core/analyzer_result.py

==========================================================
UDUAK QUANT SYSTEM

Analyzer Result Model

Every analyzer in the system returns this object.

This creates a unified interface between:

    • Signal Engine
    • Analyzer Registry
    • Decision Engine
    • Dashboard
    • Backtester

==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# ==========================================================
# ANALYZER RESULT
# ==========================================================

@dataclass(slots=True)
class AnalyzerResult:
    """
    Standard output returned by every analyzer.
    """

    analyzer_name: str

    score: float

    confidence: float

    direction: str | None = None

    valid: bool = True

    metadata: dict[str, Any] = field(default_factory=dict)

    warnings: list[str] = field(default_factory=list)

    timestamp: Any | None = None

    # ------------------------------------------------------

    @property
    def approved(self) -> bool:
        """
        Whether this analyzer produced
        a usable institutional signal.
        """
        return self.valid and self.score > 0.0

    # ------------------------------------------------------

    def add_warning(
        self,
        message: str,
    ) -> None:

        self.warnings.append(message)

    # ------------------------------------------------------

    def merge_metadata(
        self,
        values: dict[str, Any],
    ) -> None:

        self.metadata.update(values)

    # ------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:

        return {
            "analyzer_name": self.analyzer_name,
            "score": self.score,
            "confidence": self.confidence,
            "direction": self.direction,
            "valid": self.valid,
            "metadata": self.metadata,
            "warnings": self.warnings,
            "timestamp": self.timestamp,
        }

    # ------------------------------------------------------

    @classmethod
    def empty(
        cls,
        analyzer_name: str,
    ) -> "AnalyzerResult":

        return cls(
            analyzer_name=analyzer_name,
            score=0.0,
            confidence=0.0,
            direction=None,
            valid=False,
        )