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
    ScoreBreakdown,
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
            # ==========================================================
    # MAIN EVALUATION
    # ==========================================================

    def evaluate(
        self,
        strategy_name: str,
        strengths: Dict[str, float],
        risk_reward: float,
    ) -> DecisionResult:
        """
        Evaluate a strategy and produce the final decision.

        Parameters
        ----------
        strategy_name
            Name of the strategy being evaluated.

        strengths
            Dictionary containing normalized analyzer strengths
            (0.0 - 1.0).

        risk_reward
            Calculated Risk : Reward ratio.

        Returns
        -------
        DecisionResult
            Final institutional decision.
        """

                # --------------------------------------------------
        # Validate Risk : Reward
        # --------------------------------------------------

        if risk_reward < self.minimum_rr:

            return DecisionResult(
                strategy_name=strategy_name,
                decision="REJECTED",
                approved=False,
                total_score=0.0,
                minimum_required=self.minimum_score,
                risk_reward=risk_reward,
                score=StrategyScore(
                    strategy_name=strategy_name,
                    total_score=0.0,
                    approved=False,
                    minimum_required=self.minimum_score,
                    breakdown=ScoreBreakdown(),
                    missing_components=[],
                ),
                rejection_reason=(
                    f"Risk:Reward below minimum "
                    f"({risk_reward:.2f} < {self.minimum_rr:.2f})"
                ),
            )

        # --------------------------------------------------
        # Run Dynamic Scoring Engine
        # --------------------------------------------------

        score = self.scoring_engine.calculate(
            strategy_name,
            strengths,
        )

                # --------------------------------------------------
        # Final Decision
        # --------------------------------------------------

        if score.approved:

            decision = "APPROVED"
            rejection_reason = None

        else:

            decision = "REJECTED"
            rejection_reason = (
                f"Score below minimum "
                f"({score.total_score:.2f} < "
                f"{score.minimum_required:.2f})"
            )

        return DecisionResult(
            strategy_name=strategy_name,
            decision=decision,
            approved=score.approved,
            total_score=score.total_score,
            minimum_required=score.minimum_required,
            risk_reward=risk_reward,
            score=score,
            missing_components=score.missing_components,
            rejection_reason=rejection_reason,
            metadata={
                "component_count": len(strengths),
                "approved_by_score": score.approved,
                "risk_reward_passed": risk_reward >= self.minimum_rr,
            },
        )