"""
Tests for models/signal.py
"""

import pytest

from models.signal import (
    Signal,
    SignalDirection,
)


# =============================================================================
# SIGNAL CREATION
# =============================================================================

def test_signal_creation():

    signal = Signal(
        symbol="EURUSD",
        direction=SignalDirection.BUY,
        entry_price=1.1000,
        stop_loss=1.0980,
        take_profit=1.1060,
        strategy_name="Breakout",
    )

    assert signal.symbol == "EURUSD"

    assert signal.direction == SignalDirection.BUY

    assert signal.entry_price == 1.1000

    assert signal.stop_loss == 1.0980

    assert signal.take_profit == 1.1060

    assert signal.strategy_name == "Breakout"


# =============================================================================
# RISK CALCULATION
# =============================================================================

def test_risk_calculation():

    signal = Signal(
        symbol="EURUSD",
        direction=SignalDirection.BUY,
        entry_price=1.1000,
        stop_loss=1.0980,
        take_profit=1.1060,
        strategy_name="Breakout",
    )

    assert signal.risk == pytest.approx(0.0020)


# =============================================================================
# REWARD CALCULATION
# =============================================================================

def test_reward_calculation():

    signal = Signal(
        symbol="EURUSD",
        direction=SignalDirection.BUY,
        entry_price=1.1000,
        stop_loss=1.0980,
        take_profit=1.1060,
        strategy_name="Breakout",
    )

    assert signal.reward == pytest.approx(0.0060)


# =============================================================================
# RISK : REWARD RATIO
# =============================================================================

def test_risk_reward_ratio():

    signal = Signal(
        symbol="EURUSD",
        direction=SignalDirection.BUY,
        entry_price=1.1000,
        stop_loss=1.0980,
        take_profit=1.1060,
        strategy_name="Breakout",
    )

    assert signal.risk_reward_ratio == pytest.approx(3.0)


# =============================================================================
# ZERO RISK
# =============================================================================

def test_zero_risk():

    signal = Signal(
        symbol="EURUSD",
        direction=SignalDirection.BUY,
        entry_price=1.1000,
        stop_loss=1.1000,
        take_profit=1.1060,
        strategy_name="Breakout",
    )

    assert signal.risk == pytest.approx(0.0)

    assert signal.reward == pytest.approx(0.0060)

    assert signal.risk_reward_ratio == pytest.approx(0.0)


# =============================================================================
# SELL SIGNAL
# =============================================================================

def test_sell_signal():

    signal = Signal(
        symbol="GBPUSD",
        direction=SignalDirection.SELL,
        entry_price=1.3000,
        stop_loss=1.3020,
        take_profit=1.2940,
        strategy_name="CHOCH",
    )

    assert signal.direction == SignalDirection.SELL

    assert signal.risk == pytest.approx(0.0020)

    assert signal.reward == pytest.approx(0.0060)

    assert signal.risk_reward_ratio == pytest.approx(3.0)