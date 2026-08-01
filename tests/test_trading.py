"""
===============================================================================
UDUAK_QUANT_SYSTEM_PROJECT

File: tests/test_trading.py

Description:
    Unit tests for config/trading.py
===============================================================================
"""

from config.trading import (
    OrderFilling,
    OrderType,
    trading,
)


# =============================================================================
# Position Configuration
# =============================================================================

def test_max_open_positions():
    assert trading.position.max_open_positions == 2


def test_max_positions_per_symbol():
    assert trading.position.max_positions_per_symbol == 1


def test_multiple_positions():
    assert trading.position.allow_multiple_positions is False


def test_allow_hedging():
    assert trading.position.allow_hedging is False


# =============================================================================
# Execution Configuration
# =============================================================================

def test_slippage():
    assert trading.execution.slippage == 5


def test_filling_policy():
    assert trading.execution.filling_policy == OrderFilling.AUTO


def test_retry_attempts():
    assert trading.execution.retry_attempts == 3


def test_retry_delay():
    assert trading.execution.retry_delay_seconds == 2


def test_execution_timeout():
    assert trading.execution.execution_timeout == 30


# =============================================================================
# Session Configuration
# =============================================================================

def test_trading_days():

    assert trading.session.trade_monday is True
    assert trading.session.trade_tuesday is True
    assert trading.session.trade_wednesday is True
    assert trading.session.trade_thursday is True
    assert trading.session.trade_friday is True

    assert trading.session.trade_saturday is False
    assert trading.session.trade_sunday is False


def test_weekend_trading():
    assert trading.session.allow_weekend_trading is False


def test_friday_cutoff():
    assert trading.session.friday_cutoff_hour == 21


# =============================================================================
# Order Configuration
# =============================================================================

def test_magic_number():
    assert trading.order.magic_number == 10001


def test_order_comment():
    assert trading.order.comment == "UDUAK_QUANT_SYSTEM"


def test_order_type():
    assert trading.order.order_type == OrderType.MARKET


def test_order_deviation():
    assert trading.order.deviation == 5


# =============================================================================
# Filter Configuration
# =============================================================================

def test_news_filter():
    assert trading.filters.news_filter is True


def test_session_filter():
    assert trading.filters.session_filter is True


def test_spread_filter():
    assert trading.filters.spread_filter is True


def test_volatility_filter():
    assert trading.filters.volatility_filter is True


def test_regime_filter():
    assert trading.filters.regime_filter is True


# =============================================================================
# Root Configuration
# =============================================================================

def test_trading_configuration_exists():
    assert trading is not None


def test_configuration_types():

    assert isinstance(trading.execution.filling_policy, OrderFilling)

    assert isinstance(trading.order.order_type, OrderType)