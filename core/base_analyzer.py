"""
core/base_analyzer.py

==========================================================
UDUAK QUANT SYSTEM

Institutional Base Analyzer

Every analyzer in the system inherits from this class.

Responsibilities

    • Standard interface
    • Standard metadata
    • Standard result object
    • Future logging hooks
    • Future timing hooks
==========================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

from core.analyzer_result import AnalyzerResult


# ==========================================================
# BASE ANALYZER
# ==========================================================

class BaseAnalyzer(ABC):
    """
    Abstract base class for all analyzers.
    """

    def __init__(self, analyzer_name: str):

        self.analyzer_name = analyzer_name

    # ------------------------------------------------------

    @abstractmethod
    def analyze(
        self,
        market_data: Any,
    ) -> AnalyzerResult:
        """
        Execute analyzer logic.

        Every analyzer MUST return an AnalyzerResult.
        """
        raise NotImplementedError

    # ------------------------------------------------------

    def empty_result(self) -> AnalyzerResult:
        """
        Standard empty result.
        """

        return AnalyzerResult.empty(
            self.analyzer_name,
        )

    # ------------------------------------------------------

    def create_result(
        self,
        *,
        score: float,
        confidence: float,
        direction: str | None = None,
        valid: bool = True,
        metadata: dict[str, Any] | None = None,
    ) -> AnalyzerResult:
        """
        Helper for creating analyzer results.
        """

        return AnalyzerResult(
            analyzer_name=self.analyzer_name,
            score=score,
            confidence=confidence,
            direction=direction,
            valid=valid,
            metadata=metadata or {},
            timestamp=datetime.utcnow(),
        )

    # ------------------------------------------------------

    def __repr__(self) -> str:

        return f"{self.__class__.__name__}('{self.analyzer_name}')"