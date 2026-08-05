"""
core/analyzer_result.py

UDUAK QUANT SYSTEM
Institutional Analyzer Result Model

Every analyzer MUST return this object.

This standardizes communication between:

    Analyzer
        ↓
Analyzer Manager
        ↓
Signal Engine
        ↓
Decision Engine
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List


@dataclass(slots=True)
class AnalyzerResult:
    """
    Standard output from every analyzer.
    """

    analyzer: str

    success: bool

    confidence: float = 0.0

    data: Dict[str, Any] = field(default_factory=dict)

    warnings: List[str] = field(default_factory=list)

    errors: List[str] = field(default_factory=list)

    metadata: Dict[str, Any] = field(default_factory=dict)

    execution_time_ms: float = 0.0

    timestamp: datetime = field(default_factory=datetime.utcnow)

    # ======================================================
    # VALIDATION
    # ======================================================

    def __post_init__(self) -> None:
        self.confidence = max(0.0, min(100.0, float(self.confidence)))

    # ======================================================
    # STATUS
    # ======================================================

    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0

    @property
    def has_warnings(self) -> bool:
        return len(self.warnings) > 0

    @property
    def is_valid(self) -> bool:
        return self.success and not self.has_errors

    # ======================================================
    # HELPERS
    # ======================================================

    def add_warning(self, message: str) -> None:
        self.warnings.append(str(message))

    def add_error(self, message: str) -> None:
        self.errors.append(str(message))

    def add_metadata(self, key: str, value: Any) -> None:
        self.metadata[key] = value

    # ======================================================
    # SERIALIZATION
    # ======================================================

    def to_dict(self) -> Dict[str, Any]:
        return {
            "analyzer": self.analyzer,
            "success": self.success,
            "confidence": self.confidence,
            "data": self.data,
            "warnings": self.warnings,
            "errors": self.errors,
            "metadata": self.metadata,
            "execution_time_ms": self.execution_time_ms,
            "timestamp": self.timestamp.isoformat(),
        }

    # ======================================================
    # FACTORY METHODS
    # ======================================================

    @classmethod
    def success_result(
        cls,
        analyzer: str,
        confidence: float,
        data: Dict[str, Any],
        execution_time_ms: float = 0.0,
    ) -> "AnalyzerResult":
        return cls(
            analyzer=analyzer,
            success=True,
            confidence=confidence,
            data=data,
            execution_time_ms=execution_time_ms,
        )

    @classmethod
    def failure_result(
        cls,
        analyzer: str,
        error: str,
        execution_time_ms: float = 0.0,
    ) -> "AnalyzerResult":
        result = cls(
            analyzer=analyzer,
            success=False,
            confidence=0.0,
            execution_time_ms=execution_time_ms,
        )
        result.add_error(error)
        return result

    # ======================================================
    # REPRESENTATION
    # ======================================================

    def __repr__(self) -> str:
        return (
            f"AnalyzerResult("
            f"analyzer='{self.analyzer}', "
            f"success={self.success}, "
            f"confidence={self.confidence:.1f}, "
            f"errors={len(self.errors)}, "
            f"warnings={len(self.warnings)})"
        )