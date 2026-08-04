"""
core/scoring_models.py

UDUAK QUANT SYSTEM
Institutional Dynamic Scoring Engine

Converts analyzer strengths into a dynamic institutional score.

Analyzer strength:
    0.0 -> Component absent
    1.0 -> Perfect component

Final Score:
    Sum(component_weight × strength × strategy_multiplier)

The Decision Engine uses this score to determine whether
a setup is tradable.
"""

from dataclasses import dataclass
from typing import Dict

from config.scoring import (
    COMPONENT_WEIGHTS,
    STRATEGY_REQUIRED_COMPONENTS,
    STRATEGY_WEIGHT_MULTIPLIERS,
    STRATEGY_MINIMUM_SCORE,
    MIN_COMPONENT_STRENGTH,
    MAX_COMPONENT_STRENGTH,
    MINIMUM_SCORE,
    ScoreBreakdown,
)


# ==========================================================
# STRATEGY SCORE
# ==========================================================

@dataclass(slots=True)
class StrategyScore:
    """
    Final institutional score returned by the scoring engine.
    """

    strategy_name: str

    total_score: float

    approved: bool

    minimum_required: float

    breakdown: ScoreBreakdown

    missing_components: list[str]


# ==========================================================
# DYNAMIC SCORING ENGINE
# ==========================================================

class DynamicScoringEngine:
    """
    Dynamic institutional scoring engine.

    Each analyzer produces a normalized strength:

        0.0 -----------> 1.0

    Example

        Liquidity Sweep

            strength = 0.82

            score =

                weight
                × strength
                × strategy multiplier
    """

    def __init__(self):

        self.weights = COMPONENT_WEIGHTS

    # ------------------------------------------------------

    @staticmethod
    def clamp_strength(strength: float) -> float:
        """
        Clamp analyzer strength between 0 and 1.
        """

        return max(
            MIN_COMPONENT_STRENGTH,
            min(MAX_COMPONENT_STRENGTH, strength),
        )

    # ------------------------------------------------------

    def validate_required_components(
        self,
        strategy_name: str,
        strengths: Dict[str, float],
    ) -> tuple[bool, list[str]]:
        """
        Ensure every required component exists.

        Required component is missing if

            strength <= 0
        """

        required = STRATEGY_REQUIRED_COMPONENTS.get(
            strategy_name,
            set(),
        )

        missing = []

        for component in required:

            if strengths.get(component, 0.0) <= 0.0:

                missing.append(component)

        return len(missing) == 0, missing

    # ------------------------------------------------------

    def score_component(
        self,
        component: str,
        strength: float,
        multiplier: float,
    ) -> float:
        """
        Calculate one component score.
        """

        strength = self.clamp_strength(strength)

        weight = self.weights.get(component, 0.0)

        score = weight * strength * multiplier

        return min(score, weight)

    # ------------------------------------------------------

    def calculate(
        self,
        strategy_name: str,
        strengths: Dict[str, float],
    ) -> StrategyScore:
        """
        Calculate the complete institutional score.
        """

        breakdown = ScoreBreakdown()

        valid, missing = self.validate_required_components(
            strategy_name,
            strengths,
        )

        if not valid:

            return StrategyScore(
                strategy_name=strategy_name,
                total_score=0.0,
                approved=False,
                minimum_required=STRATEGY_MINIMUM_SCORE.get(
                    strategy_name,
                    MINIMUM_SCORE,
                ),
                breakdown=breakdown,
                missing_components=missing,
            )

        multipliers = STRATEGY_WEIGHT_MULTIPLIERS.get(
            strategy_name,
            {},
        )

        total_score = 0.0

        for component, max_weight in self.weights.items():

            strength = strengths.get(component, 0.0)

            multiplier = multipliers.get(component, 1.0)

            component_score = self.score_component(
                component,
                strength,
                multiplier,
            )

            setattr(
                breakdown,
                component,
                round(component_score, 2),
            )

            total_score += component_score

        total_score = round(total_score, 2)

        minimum_required = STRATEGY_MINIMUM_SCORE.get(
            strategy_name,
            MINIMUM_SCORE,
        )

        approved = total_score >= minimum_required

        return StrategyScore(
            strategy_name=strategy_name,
            total_score=total_score,
            approved=approved,
            minimum_required=minimum_required,
            breakdown=breakdown,
            missing_components=[],
        )