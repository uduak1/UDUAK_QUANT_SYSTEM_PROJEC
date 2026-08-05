"""
tests/test_signal_engine.py

Signal Engine tests
"""

import pytest

from core.signal_engine import SignalEngine
from core.signal_models import SignalRequest


# ==========================================================
# FIXTURES
# ==========================================================

@pytest.fixture
def engine():
    return SignalEngine()


@pytest.fixture
def signal_request():

    return SignalRequest(
        strategy_name="LiquiditySweep",

        strengths={
            "liquidity": 1.0,
            "market_structure": 1.0,
            "fvg": 1.0,
            "order_block": 1.0,
            "displacement": 1.0,
        },

        risk_reward=3.0,

        symbol="EURUSD",

        timeframe="H1",
    )


# ==========================================================
# TESTS
# ==========================================================

def test_signal_engine_creation(engine):

    assert engine is not None


def test_generate_signal(
    engine,
    signal_request,
):

    signal = engine.generate_signal(
        signal_request
    )

    assert signal.strategy_name == signal_request.strategy_name

    assert signal.symbol == "EURUSD"

    assert signal.timeframe == "H1"

    assert isinstance(signal.score, float)

    assert signal.decision in (
        "APPROVED",
        "REJECTED",
    )


def test_signal_metadata(
    engine,
    signal_request,
):

    signal = engine.generate_signal(
        signal_request
    )

    assert isinstance(
        signal.metadata,
        dict,
    )

    assert "component_count" in signal.metadata

    assert "approved" in signal.metadata

    assert "decision" in signal.metadata


def test_unknown_strategy(
    engine,
    signal_request,
):

    signal_request.strategy_name = "DOES_NOT_EXIST"

    with pytest.raises(ValueError):

        engine.generate_signal(
            signal_request
        )


def test_collect_strengths_none(engine):

    strengths = engine.collect_strengths(
        None
    )

    assert strengths == {}


def test_request_symbol(
    engine,
    signal_request,
):

    signal = engine.generate_signal(
        signal_request
    )

    assert signal.symbol == signal_request.symbol


def test_request_timeframe(
    engine,
    signal_request,
):

    signal = engine.generate_signal(
        signal_request
    )

    assert signal.timeframe == signal_request.timeframe


def test_request_rr(
    engine,
    signal_request,
):

    signal = engine.generate_signal(
        signal_request
    )

    assert signal.risk_reward == signal_request.risk_reward


def test_decision_result_present(
    engine,
    signal_request,
):

    signal = engine.generate_signal(
        signal_request
    )

    assert signal.decision_result is not None


def test_score_type(
    engine,
    signal_request,
):

    signal = engine.generate_signal(
        signal_request
    )

    assert isinstance(
        signal.score,
        float,
    )


def test_signal_result_type(
    engine,
    signal_request,
):

    signal = engine.generate_signal(
        signal_request
    )

    assert signal is not None
