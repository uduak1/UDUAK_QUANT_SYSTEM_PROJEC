"""
tests/test_decision_engine.py

Unit tests for:

core/decision_engine.py
"""

import pytest

from core.decision_engine import DecisionEngine


# ==========================================================
# ENGINE CREATION
# ==========================================================

def test_engine_creation():

    engine = DecisionEngine()

    assert engine is not None


# ==========================================================
# REJECTED TRADE (LOW SCORE)
# ==========================================================

def test_rejected_trade_low_score():

    engine = DecisionEngine()

    strengths = {
        "market_structure": 1.0,
        "liquidity_sweep": 1.0,
        "change_of_character": 1.0,
        "trend_alignment": 1.0,
        "fair_value_gap": 1.0,
    }

    result = engine.evaluate(
        "LiquiditySweepReversal",
        strengths,
        3.5,
    )

    assert result.approved is False
    assert result.decision == "REJECTED"


# ==========================================================
# APPROVED TRADE
# ==========================================================

def test_approved_trade():

    engine = DecisionEngine()

    strengths = {
        "market_structure": 1.0,
        "liquidity_sweep": 1.0,
        "fair_value_gap": 1.0,
        "order_block": 1.0,
        "change_of_character": 1.0,
        "break_of_structure": 1.0,
        "trend_alignment": 1.0,
        "volume_confirmation": 1.0,
        "session_quality": 1.0,
        "market_regime": 1.0,
        "premium_discount": 1.0,
    }

    result = engine.evaluate(
        "LiquiditySweepReversal",
        strengths,
        5.0,
    )

    assert result.approved is True
    assert result.decision == "APPROVED"

def test_reject_low_rr():

    engine = DecisionEngine()

    strengths = {
        "market_structure": 1.0,
        "liquidity_sweep": 1.0,
        "change_of_character": 1.0,
    }

    result = engine.evaluate(
        "LiquiditySweepReversal",
        strengths,
        2.0,
    )

    assert result.approved is False
    assert result.decision == "REJECTED"
    assert result.rejection_reason is not None


# ==========================================================
# REJECT MISSING REQUIRED COMPONENT
# ==========================================================

def test_missing_required_component():

    engine = DecisionEngine()

    strengths = {
        "market_structure": 1.0,
    }

    result = engine.evaluate(
        "LiquiditySweepReversal",
        strengths,
        4.0,
    )

    assert result.approved is False
    assert len(result.missing_components) > 0


# ==========================================================
# SCORE EXISTS
# ==========================================================

def test_score_object_exists():

    engine = DecisionEngine()

    strengths = {
        "market_structure": 1.0,
        "trend_alignment": 1.0,
    }

    result = engine.evaluate(
        "TrendContinuation",
        strengths,
        4.0,
    )

    assert result.score is not None


# ==========================================================
# SCORE VALUE
# ==========================================================

def test_score_value_positive():

    engine = DecisionEngine()

    strengths = {
        "market_structure": 1.0,
        "trend_alignment": 1.0,
    }

    result = engine.evaluate(
        "TrendContinuation",
        strengths,
        4.0,
    )

    assert result.total_score >= 0


# ==========================================================
# METADATA EXISTS
# ==========================================================

def test_metadata_created():

    engine = DecisionEngine()

    strengths = {
        "market_structure": 1.0,
        "trend_alignment": 1.0,
    }

    result = engine.evaluate(
        "TrendContinuation",
        strengths,
        4.0,
    )

    assert isinstance(result.metadata, dict)


# ==========================================================
# COMPONENT COUNT
# ==========================================================

def test_metadata_component_count():

    engine = DecisionEngine()

    strengths = {
        "market_structure": 1.0,
        "trend_alignment": 1.0,
        "fair_value_gap": 0.5,
    }

    result = engine.evaluate(
        "TrendContinuation",
        strengths,
        4.0,
    )

    assert result.metadata["component_count"] == len(strengths)


# ==========================================================
# RR FLAG
# ==========================================================

def test_metadata_rr_flag():

    engine = DecisionEngine()

    strengths = {
        "market_structure": 1.0,
        "trend_alignment": 1.0,
    }

    result = engine.evaluate(
        "TrendContinuation",
        strengths,
        4.0,
    )

    assert result.metadata["risk_reward_passed"] is True


# ==========================================================
# SCORE FLAG
# ==========================================================

def test_metadata_score_flag():

    engine = DecisionEngine()

    strengths = {
        "market_structure": 1.0,
        "trend_alignment": 1.0,
    }

    result = engine.evaluate(
        "TrendContinuation",
        strengths,
        4.0,
    )

    assert result.metadata["approved_by_score"] == result.score.approved