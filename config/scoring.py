"""
config/scoring.py

UDUAK QUANT SYSTEM
Institutional Dynamic Scoring Configuration

TOTAL SCORE = 100
"""

from dataclasses import dataclass
from typing import Dict

# ==========================================================
# GLOBAL SCORING SETTINGS
# ==========================================================

MAX_SCORE = 100.0
MINIMUM_SCORE = 70.0
HIGH_CONFIDENCE_SCORE = 85.0
PREMIUM_SCORE = 90.0

# ==========================================================
# RISK / REWARD VALIDATION
# ==========================================================

MIN_RISK_REWARD_RATIO = 3.0
REQUIRE_MIN_RISK_REWARD = True

# ==========================================================
# COMPONENT WEIGHTS
# ==========================================================

COMPONENT_WEIGHTS: Dict[str, float] = {
    "market_structure": 20.0,
    "liquidity_sweep": 14.0,
    "fair_value_gap": 9.0,
    "order_block": 9.0,
    "change_of_character": 9.0,
    "break_of_structure": 9.0,
    "trend_alignment": 10.0,
    "volume_confirmation": 4.0,
    "session_quality": 4.0,
    "market_regime": 4.0,
    "premium_discount": 8.0,
}

# ==========================================================
# DECISION THRESHOLDS
# ==========================================================

SCORE_THRESHOLDS = {
    "REJECT": 0,
    "WATCH": 50,
    "MONITOR": 60,
    "TRADABLE": 70,
    "HIGH_CONFIDENCE": 85,
    "INSTITUTIONAL": 90,
}

# ==========================================================
# DYNAMIC SCORING PARAMETERS
# ==========================================================

MIN_COMPONENT_STRENGTH = 0.0
MAX_COMPONENT_STRENGTH = 1.0

# ==========================================================
# STRATEGY OVERRIDES
# ==========================================================

STRATEGY_MINIMUM_SCORE = {
    "LiquiditySweepReversal": 82,
    "BreakoutMomentum": 78,
    "TrendContinuation": 75,
    "CHOCHReversal": 80,
    "BOSContinuation": 78,
    "RangeMeanReversion": 72,
    "LiquidityGrabFade": 82,
    "DisplacementMomentum": 84,
    "MultiTimeFrameTrend": 80,
}

# ==========================================================
# STRATEGY REQUIREMENTS
# ==========================================================

STRATEGY_REQUIRED_COMPONENTS = {
    "LiquiditySweepReversal": {
        "market_structure",
        "liquidity_sweep",
        "change_of_character",
    },
    "LiquidityGrabFade": {
        "market_structure",
        "liquidity_sweep",
    },
    "BreakoutMomentum": {
        "market_structure",
        "break_of_structure",
        "trend_alignment",
    },
    "BOSContinuation": {
        "market_structure",
        "break_of_structure",
        "trend_alignment",
    },
    "TrendContinuation": {
        "market_structure",
        "trend_alignment",
    },
    "MultiTimeFrameTrend": {
        "market_structure",
        "trend_alignment",
    },
    "CHOCHReversal": {
        "market_structure",
        "change_of_character",
    },
    "DisplacementMomentum": {
        "market_structure",
        "break_of_structure",
        "fair_value_gap",
    },
    "RangeMeanReversion": {
        "market_structure",
        "premium_discount",
    },
}

# ==========================================================
# STRATEGY OPTIONAL COMPONENTS
# ==========================================================

STRATEGY_OPTIONAL_COMPONENTS = {
    "LiquiditySweepReversal": {
        "fair_value_gap",
        "order_block",
        "trend_alignment",
        "volume_confirmation",
        "session_quality",
        "market_regime",
        "premium_discount",
    },
    "LiquidityGrabFade": {
        "fair_value_gap",
        "order_block",
        "change_of_character",
        "trend_alignment",
        "volume_confirmation",
        "session_quality",
        "market_regime",
        "premium_discount",
    },
    "BreakoutMomentum": {
        "liquidity_sweep",
        "fair_value_gap",
        "order_block",
        "change_of_character",
        "volume_confirmation",
        "session_quality",
        "market_regime",
        "premium_discount",
    },
    "BOSContinuation": {
        "liquidity_sweep",
        "fair_value_gap",
        "order_block",
        "change_of_character",
        "volume_confirmation",
        "session_quality",
        "market_regime",
        "premium_discount",
    },
    "TrendContinuation": {
        "liquidity_sweep",
        "fair_value_gap",
        "order_block",
        "change_of_character",
        "break_of_structure",
        "volume_confirmation",
        "session_quality",
        "market_regime",
        "premium_discount",
    },
    "MultiTimeFrameTrend": {
        "liquidity_sweep",
        "fair_value_gap",
        "order_block",
        "change_of_character",
        "break_of_structure",
        "volume_confirmation",
        "session_quality",
        "market_regime",
        "premium_discount",
    },
    "CHOCHReversal": {
        "liquidity_sweep",
        "fair_value_gap",
        "order_block",
        "trend_alignment",
        "volume_confirmation",
        "session_quality",
        "market_regime",
        "premium_discount",
    },
    "DisplacementMomentum": {
        "liquidity_sweep",
        "order_block",
        "trend_alignment",
        "change_of_character",
        "volume_confirmation",
        "session_quality",
        "market_regime",
        "premium_discount",
    },
    "RangeMeanReversion": {
        "liquidity_sweep",
        "fair_value_gap",
        "order_block",
        "change_of_character",
        "break_of_structure",
        "trend_alignment",
        "volume_confirmation",
        "session_quality",
        "market_regime",
    },
}

# ==========================================================
# STRATEGY WEIGHT MULTIPLIERS
# ==========================================================
#
# Allows each strategy to emphasize certain market
# components without changing the global scoring model.
#
# 1.00 = normal importance
# >1.00 = more important
# <1.00 = less important
#
# Final Component Score =
#
# component_weight
# × analyzer_strength
# × multiplier
#
# ==========================================================

STRATEGY_WEIGHT_MULTIPLIERS = {

    "LiquiditySweepReversal": {
        "liquidity_sweep": 1.30,
        "change_of_character": 1.20,
        "trend_alignment": 0.80,
    },

    "LiquidityGrabFade": {
        "liquidity_sweep": 1.25,
        "premium_discount": 1.15,
    },

    "BreakoutMomentum": {
        "break_of_structure": 1.25,
        "trend_alignment": 1.20,
        "liquidity_sweep": 0.75,
    },

    "BOSContinuation": {
        "break_of_structure": 1.30,
        "trend_alignment": 1.20,
    },

    "TrendContinuation": {
        "trend_alignment": 1.30,
        "break_of_structure": 1.10,
    },

    "MultiTimeFrameTrend": {
        "trend_alignment": 1.35,
        "market_structure": 1.10,
    },

    "CHOCHReversal": {
        "change_of_character": 1.35,
        "order_block": 1.15,
    },

    "DisplacementMomentum": {
        "fair_value_gap": 1.30,
        "break_of_structure": 1.20,
    },

    "RangeMeanReversion": {
        "premium_discount": 1.35,
        "order_block": 1.20,
    },

}

# ==========================================================
# COMPONENT DESCRIPTIONS
# ==========================================================

COMPONENT_DESCRIPTION = {

    "market_structure":
        "Overall market structure quality",

    "liquidity_sweep":
        "Liquidity sweep quality",

    "fair_value_gap":
        "Fair Value Gap quality",

    "order_block":
        "Order Block quality",

    "change_of_character":
        "CHOCH confirmation",

    "break_of_structure":
        "Break of Structure confirmation",

    "trend_alignment":
        "Higher timeframe trend alignment",

    "volume_confirmation":
        "Institutional volume confirmation",

    "session_quality":
        "Trading session quality",

    "market_regime":
        "Current market regime quality",

    "premium_discount":
        "Premium / Discount location",

}

# ==========================================================
# SCORE BREAKDOWN
# ==========================================================

@dataclass(slots=True)
class ScoreBreakdown:
    market_structure: float = 0.0
    liquidity_sweep: float = 0.0
    fair_value_gap: float = 0.0
    order_block: float = 0.0
    change_of_character: float = 0.0
    break_of_structure: float = 0.0
    trend_alignment: float = 0.0
    volume_confirmation: float = 0.0
    session_quality: float = 0.0
    market_regime: float = 0.0
    premium_discount: float = 0.0

    @property
    def total(self) -> float:
        return round(
            self.market_structure
            + self.liquidity_sweep
            + self.fair_value_gap
            + self.order_block
            + self.change_of_character
            + self.break_of_structure
            + self.trend_alignment
            + self.volume_confirmation
            + self.session_quality
            + self.market_regime
            + self.premium_discount,
            2,
        )

# ==========================================================
# VALIDATION
# ==========================================================

assert round(sum(COMPONENT_WEIGHTS.values()), 2) == 100.0, (
    f"Component weights must total 100. "
    f"Current total = {sum(COMPONENT_WEIGHTS.values())}"
)

# ==========================================================
# CONFIG VALIDATION
# ==========================================================

assert (
    STRATEGY_MINIMUM_SCORE.keys()
    == STRATEGY_REQUIRED_COMPONENTS.keys()
    == STRATEGY_OPTIONAL_COMPONENTS.keys()
    == STRATEGY_WEIGHT_MULTIPLIERS.keys()
), "Strategy configuration mismatch."

VALID_COMPONENTS = set(COMPONENT_WEIGHTS.keys())

for strategy, components in STRATEGY_REQUIRED_COMPONENTS.items():
    assert components <= VALID_COMPONENTS, (
        f"{strategy} contains unknown required components."
    )

for strategy, components in STRATEGY_OPTIONAL_COMPONENTS.items():
    assert components <= VALID_COMPONENTS, (
        f"{strategy} contains unknown optional components."
    )