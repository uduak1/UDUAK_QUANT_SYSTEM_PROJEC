"""
tests/test_scoring.py

Unit tests for config/scoring.py

These tests validate the institutional scoring configuration
used throughout the UDUAK Quant System.
"""

import pytest

from config.scoring import (
    MAX_SCORE,
    MINIMUM_SCORE,
    HIGH_CONFIDENCE_SCORE,
    PREMIUM_SCORE,
    MIN_RISK_REWARD_RATIO,
    REQUIRE_MIN_RISK_REWARD,
    COMPONENT_WEIGHTS,
    SCORE_THRESHOLDS,
    MIN_COMPONENT_STRENGTH,
    MAX_COMPONENT_STRENGTH,
    STRATEGY_MINIMUM_SCORE,
    STRATEGY_REQUIRED_COMPONENTS,
    STRATEGY_OPTIONAL_COMPONENTS,
    STRATEGY_WEIGHT_MULTIPLIERS,
    COMPONENT_DESCRIPTION,
    ScoreBreakdown,
)


# ==========================================================
# GLOBAL SETTINGS
# ==========================================================

def test_global_scores():
    assert MAX_SCORE == 100.0
    assert MINIMUM_SCORE == 70.0
    assert HIGH_CONFIDENCE_SCORE == 85.0
    assert PREMIUM_SCORE == 90.0


# ==========================================================
# RISK REWARD
# ==========================================================

def test_risk_reward():
    assert REQUIRE_MIN_RISK_REWARD is True
    assert MIN_RISK_REWARD_RATIO == 3.0


# ==========================================================
# COMPONENT WEIGHTS
# ==========================================================

def test_component_weights_total():
    assert round(sum(COMPONENT_WEIGHTS.values()), 2) == 100.0


def test_component_weights_positive():
    for weight in COMPONENT_WEIGHTS.values():
        assert weight > 0


# ==========================================================
# SCORE THRESHOLDS
# ==========================================================

def test_score_thresholds():
    assert SCORE_THRESHOLDS["WATCH"] == 50
    assert SCORE_THRESHOLDS["MONITOR"] == 60
    assert SCORE_THRESHOLDS["TRADABLE"] == 70
    assert SCORE_THRESHOLDS["HIGH_CONFIDENCE"] == 85
    assert SCORE_THRESHOLDS["INSTITUTIONAL"] == 90


# ==========================================================
# COMPONENT STRENGTH
# ==========================================================

def test_component_strength_limits():
    assert MIN_COMPONENT_STRENGTH == 0.0
    assert MAX_COMPONENT_STRENGTH == 1.0


# ==========================================================
# STRATEGY MINIMUM SCORES
# ==========================================================

def test_strategy_minimum_scores():
    for strategy, score in STRATEGY_MINIMUM_SCORE.items():
        assert 70 <= score <= 100


# ==========================================================
# STRATEGY CONFIGURATION
# ==========================================================

def test_every_strategy_has_required_components():
    for strategy in STRATEGY_MINIMUM_SCORE:
        assert strategy in STRATEGY_REQUIRED_COMPONENTS


def test_every_strategy_has_optional_components():
    for strategy in STRATEGY_MINIMUM_SCORE:
        assert strategy in STRATEGY_OPTIONAL_COMPONENTS


def test_every_strategy_has_weight_multipliers():
    for strategy in STRATEGY_MINIMUM_SCORE:
        assert strategy in STRATEGY_WEIGHT_MULTIPLIERS


# ==========================================================
# REQUIRED COMPONENTS EXIST
# ==========================================================

def test_required_components_exist():
    for components in STRATEGY_REQUIRED_COMPONENTS.values():
        for component in components:
            assert component in COMPONENT_WEIGHTS


# ==========================================================
# OPTIONAL COMPONENTS EXIST
# ==========================================================

def test_optional_components_exist():
    for components in STRATEGY_OPTIONAL_COMPONENTS.values():
        for component in components:
            assert component in COMPONENT_WEIGHTS


# ==========================================================
# WEIGHT MULTIPLIERS
# ==========================================================

def test_weight_multiplier_components_exist():
    for multipliers in STRATEGY_WEIGHT_MULTIPLIERS.values():
        for component in multipliers:
            assert component in COMPONENT_WEIGHTS


def test_weight_multiplier_values():
    for multipliers in STRATEGY_WEIGHT_MULTIPLIERS.values():
        for value in multipliers.values():
            assert value > 0


# ==========================================================
# COMPONENT DESCRIPTIONS
# ==========================================================

def test_every_component_has_description():
    for component in COMPONENT_WEIGHTS:
        assert component in COMPONENT_DESCRIPTION


# ==========================================================
# SCORE BREAKDOWN
# ==========================================================

def test_score_breakdown_defaults():
    score = ScoreBreakdown()

    assert score.total == 0.0


def test_score_breakdown_total():

    score = ScoreBreakdown(
        market_structure=20,
        liquidity_sweep=14,
        fair_value_gap=9,
        order_block=9,
        change_of_character=9,
        break_of_structure=9,
        trend_alignment=10,
        volume_confirmation=4,
        session_quality=4,
        market_regime=4,
        premium_discount=8,
    )

    assert score.total == 100.0