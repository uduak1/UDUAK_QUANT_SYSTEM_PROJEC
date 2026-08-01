"""
Tests for data/market_data.py
"""

from types import SimpleNamespace
from unittest.mock import patch

import pytest

from data.market_data import MarketData
from models.response import Response


# =============================================================================
# MARKET DATA SUCCESS
# =============================================================================

@patch("data.market_data.mt5.symbol_info_tick")
def test_get_market_data_success(mock_symbol_info_tick):

    tick = SimpleNamespace(
        bid=1.10000,
        ask=1.10020,
        last=1.10015,
        time=1712345678,
        volume=100,
        flags=6,
    )

    mock_symbol_info_tick.return_value = tick

    market_data = MarketData()

    result = market_data.get_market_data("EURUSD")

    assert isinstance(result, Response)

    assert result.success is True

    assert result.message == "Market data retrieved for 'EURUSD'."

    assert result.error is None

    assert result.data["symbol"] == "EURUSD"

    assert result.data["bid"] == pytest.approx(1.10000)

    assert result.data["ask"] == pytest.approx(1.10020)

    assert result.data["last"] == pytest.approx(1.10015)

    assert result.data["spread"] == pytest.approx(0.00020)

    assert result.data["time"] == 1712345678

    assert result.data["volume"] == 100

    assert result.data["flags"] == 6


# =============================================================================
# MARKET DATA FAILURE
# =============================================================================

@patch("data.market_data.mt5.last_error")
@patch("data.market_data.mt5.symbol_info_tick")
def test_get_market_data_failure(
    mock_symbol_info_tick,
    mock_last_error,
):

    mock_symbol_info_tick.return_value = None

    mock_last_error.return_value = (
        -1,
        "Market data unavailable",
    )

    market_data = MarketData()

    result = market_data.get_market_data("EURUSD")

    assert isinstance(result, Response)

    assert result.success is False

    assert result.message == "Unable to retrieve market data for 'EURUSD'."

    assert result.error == (
        -1,
        "Market data unavailable",
    )

    assert result.data is None


# =============================================================================
# MARKET AVAILABLE
# =============================================================================

@patch("data.market_data.mt5.symbol_info_tick")
def test_market_available(mock_symbol_info_tick):

    mock_symbol_info_tick.return_value = SimpleNamespace(
        bid=1.10000,
        ask=1.10020,
        last=1.10015,
        time=1712345678,
        volume=100,
        flags=6,
    )

    market_data = MarketData()

    result = market_data.is_available("EURUSD")

    assert result.success is True

    assert result.message == "Market data for 'EURUSD' is available."

    assert result.error is None

    assert result.data is True


# =============================================================================
# MARKET NOT AVAILABLE
# =============================================================================

@patch("data.market_data.mt5.last_error")
@patch("data.market_data.mt5.symbol_info_tick")
def test_market_not_available(
    mock_symbol_info_tick,
    mock_last_error,
):

    mock_symbol_info_tick.return_value = None

    mock_last_error.return_value = (
        -1,
        "Market data unavailable",
    )

    market_data = MarketData()

    result = market_data.is_available("EURUSD")

    assert result.success is False

    assert result.message == "Market data for 'EURUSD' is not available."

    assert result.error == (
        -1,
        "Market data unavailable",
    )

    assert result.data is False