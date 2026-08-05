"""
core/signal_models.py

==========================================================
UDUAK QUANT SYSTEM
Institutional Signal Models
==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

from core.analyzer_result import AnalyzerResult


# ==========================================================
# ENUMS
# ==========================================================

class SignalDirection(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    WAIT = "WAIT"


class SignalQuality(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    PREMIUM = "PREMIUM"


class SignalConfidence(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


# ==========================================================
# SIGNAL REQUEST
# ==========================================================

@dataclass(slots=True)
class SignalRequest:
    """
    Input supplied to the Signal Engine.
    """

    strategy_name: str
    strengths: Dict[str, float]
    risk_reward: float
    symbol: str = ""
    timeframe: str = ""


# ==========================================================
# SIGNAL RESULT
# ==========================================================

@dataclass(slots=True)
class SignalResult:
    """
    Output returned by the Signal Engine.
    """

    symbol: str
    timeframe: str
    strategy_name: str
    approved: bool
    decision: str
    score: float
    risk_reward: float
    decision_result: Optional[Any] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


# ==========================================================
# LEGACY SIGNAL MODEL
# ==========================================================

@dataclass(slots=True)
class Signal:
    """
    Generic signal model retained for backwards compatibility.
    """

    symbol: str
    direction: SignalDirection
    confidence: SignalConfidence
    quality: SignalQuality
    score: float

    timestamp: datetime = field(default_factory=datetime.utcnow)

    analyzer_results: Dict[str, AnalyzerResult] = field(default_factory=dict)

    metadata: Dict[str, Any] = field(default_factory=dict)
