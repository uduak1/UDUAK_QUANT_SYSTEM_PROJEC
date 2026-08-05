"""
core/signal_models.py

==========================================================
UDUAK QUANT SYSTEM

Institutional Signal Models

Shared signal models used by

    • Signal Engine
    • Decision Engine
    • Dashboard
    • Execution
    • Backtesting
==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

from core.analyzer_result import AnalyzerResult


# ==========================================================
# SIGNAL DIRECTION
# ==========================================================

class SignalDirection(str, Enum):

    BUY = "BUY"

    SELL = "SELL"

    WAIT = "WAIT"


# ==========================================================
# SIGNAL QUALITY
# ==========================================================

class SignalQuality(str, Enum):

    PREMIUM = "PREMIUM"

    HIGH = "HIGH"

    MEDIUM = "MEDIUM"

    LOW = "LOW"

    REJECTED = "REJECTED"


# ==========================================================
# CONFIDENCE
# ==========================================================

@dataclass(slots=True)
class SignalConfidence:

    score: float

    quality: SignalQuality

    analyzer_count: int

    agreement_ratio: float

    passed: bool


# ==========================================================
# SIGNAL
# ==========================================================

@dataclass(slots=True)
class Signal:

    symbol: str

    timeframe: str

    direction: SignalDirection

    confidence: SignalConfidence

    analyzer_results: dict[str, AnalyzerResult]

    timestamp: datetime = field(default_factory=datetime.utcnow)

    metadata: dict[str, Any] = field(default_factory=dict)

    warnings: list[str] = field(default_factory=list)

    # ------------------------------------------------------

    @property
    def approved(self) -> bool:

        return self.confidence.passed

    # ------------------------------------------------------

    @property
    def score(self) -> float:

        return self.confidence.score

    # ------------------------------------------------------

    def add_warning(
        self,
        warning: str,
    ) -> None:

        self.warnings.append(warning)

    # ------------------------------------------------------

    def add_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:

        self.metadata[key] = value

    # ------------------------------------------------------

    def analyzer(
        self,
        name: str,
    ) -> AnalyzerResult | None:

        return self.analyzer_results.get(name)

    # ------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:

        return {

            "symbol": self.symbol,

            "timeframe": self.timeframe,

            "direction": self.direction.value,

            "score": self.score,

            "approved": self.approved,

            "quality": self.confidence.quality.value,

            "agreement_ratio": self.confidence.agreement_ratio,

            "timestamp": self.timestamp.isoformat(),

            "metadata": self.metadata,

            "warnings": self.warnings,
        }