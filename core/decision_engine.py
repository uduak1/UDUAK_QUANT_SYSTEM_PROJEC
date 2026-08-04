"""
core/decision_engine.py

==========================================================
UDUAK QUANT SYSTEM
Institutional Decision Engine
==========================================================

This module is responsible for making the final trading
decision.

The Decision Engine combines:

    • Strategy selection
    • Market analyzer outputs
    • Dynamic scoring
    • Required component validation
    • Risk : Reward validation
    • Final approval logic

The Decision Engine NEVER analyzes candles directly.

It only consumes the outputs produced by the analyzers.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from config.scoring import (
    MINIMUM_SCORE,
    MIN_RISK_REWARD_RATIO,
)

from core.scoring_models import (
    DynamicScoringEngine,
    StrategyScore,
)


# ==========================================================
# DECISION RESULT
# ==========================================================

@dataclass(slots=True)
class DecisionResult:
    """
    Final output returned by the Decision Engine.
    """

    strategy_name: str

    decision: str

    approved: bool

    total_score: float

    minimum_required: float

    risk_reward: float

    score: StrategyScore

    missing_components: List[str] = field(default_factory=list)

    rejection_reason: Optional[str] = None

    metadata: Dict = field(default_factory=dict)

    # ==========================================================
# DECISION ENGINE
# ==========================================================

class DecisionEngine:
    """
    Institutional Decision Engine.

    Responsibilities
    ----------------
    1. Validate strategy inputs.
    2. Validate Risk : Reward.
    3. Call the Dynamic Scoring Engine.
    4. Produce the final trading decision.
    """

    def __init__(self) -> None:

        self.scoring_engine = DynamicScoringEngine()

        self.minimum_score = MINIMUM_SCORE

        self.minimum_rr = MIN_RISK_REWARD_RATIO