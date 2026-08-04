"""
tests/test_scoring_models.py

Unit tests for the institutional dynamic scoring engine.
"""

import pytest

from core.scoring_models import (
    DynamicScoringEngine,
    StrategyScore,
)

from config.scoring import (
    COMPONENT_WEIGHTS,
    STRATEGY_REQUIRED_COMPONENTS,
    STRATEGY_MINIMUM_SCORE,
)


# ==========================================================
# FIXTURE
# ==========================================================

@pytest.fixture
def engine():
    return DynamicScoringEngine()


# ==========================================================
# ENGINE CREATION
# ==========================================================

def test_engine_creation(engine):

    assert engine is not None

    assert engine.weights == COMPONENT_WEIGHTS


# ==========================================================
# CLAMP STRENGTH
# ==========================================================

def test_clamp_strength_lower(engine):

    assert engine.clamp_strength(-1.0) == 0.0


def test_clamp_strength_upper(engine):

    assert engine.clamp_strength(5.0) == 1.0


def test_clamp_strength_normal(engine):

    assert engine.clamp_strength(0.75) == 0.75


# ==========================================================
# REQUIRED COMPONENT VALIDATION
# ==========================================================

def test_required_components_valid(engine):

    strengths = {
        "market_structure": 1.0,
        "liquidity_sweep": 1.0,
        "change_of_character": 1.0,
    }

    valid, missing = engine.validate_required_components(
        "LiquiditySweepReversal",
        strengths,
    )

    assert valid

    assert missing == []


def test_required_components_missing(engine):

    strengths = {
        "market_structure": 1.0,
    }

    valid, missing = engine.validate_required_components(
        "LiquiditySweepReversal",
        strengths,
    )

    assert not valid

    assert "liquidity_sweep" in missing

    assert "change_of_character" in missing


# ==========================================================
# COMPONENT SCORE
# ==========================================================

def test_component_score_zero(engine):

    score = engine.score_component(
        "market_structure",
        0.0,
        1.0,
    )

    assert score == 0.0


def test_component_score_max(engine):

    score = engine.score_component(
        "market_structure",
        1.0,
        1.0,
    )

    assert score == COMPONENT_WEIGHTS["market_structure"]


def test_component_score_multiplier(engine):

    score = engine.score_component(
        "market_structure",
        1.0,
        1.20,
    )

    assert score == COMPONENT_WEIGHTS["market_structure"]


# ==========================================================
# COMPLETE STRATEGY SCORE
# ==========================================================

def test_strategy_score_success(engine):

    strengths = {
        component: 1.0
        for component in COMPONENT_WEIGHTS
    }

    result = engine.calculate(
        "TrendContinuation",
        strengths,
    )

    assert isinstance(result, StrategyScore)

    assert result.approved

    assert result.total_score >= result.minimum_required


def test_strategy_score_missing_required(engine):

    strengths = {
        "trend_alignment": 1.0,
    }

    result = engine.calculate(
        "TrendContinuation",
        strengths,
    )

    assert not result.approved

    assert result.total_score == 0.0

    assert "market_structure" in result.missing_components


# ==========================================================
# BREAKDOWN
# ==========================================================

def test_breakdown_total(engine):

    strengths = {
        component: 1.0
        for component in COMPONENT_WEIGHTS
    }

    result = engine.calculate(
        "TrendContinuation",
        strengths,
    )

    assert result.breakdown.total == pytest.approx(
        result.total_score,
        abs=0.01,
    )


# ==========================================================
# STRATEGY MINIMUM SCORE
# ==========================================================

def test_strategy_minimum_scores_exist():

    for strategy in STRATEGY_REQUIRED_COMPONENTS:

        assert strategy in STRATEGY_MINIMUM_SCORE