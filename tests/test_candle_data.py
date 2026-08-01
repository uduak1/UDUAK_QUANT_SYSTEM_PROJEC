"""
===============================================================================
UDUAK_QUANT_SYSTEM_PROJECT

File: tests/test_candle_data.py

Unit tests for data/candle_data.py
===============================================================================
"""

from types import SimpleNamespace
from unittest.mock import patch

from data.candle_data import CandleData
from models.response import Response


@patch("data.candle_data.mt5.copy_rates_from_pos")
def test_get_candles_success(mock_copy_rates):

    mock_copy_rates.return_value = [
        {
            "time": 1712345678,
            "open": 1.1000,
            "high": 1.1020,
            "low": 1.0990,
            "close": 1.1015,
            "tick_volume": 100,
            "spread": 20,
            "real_volume": 50,
        }
    ]

    candle_data = CandleData()

    result = candle_data.get_candles(
        symbol="EURUSD",
        timeframe=1,
        count=1,
    )

    assert isinstance(result, Response)

    assert result.success is True

    assert result.error is None

    assert result.message == "Retrieved 1 candles for 'EURUSD'."

    candle = result.data[0]

    assert candle["open"] == 1.1000

    assert candle["high"] == 1.1020

    assert candle["low"] == 1.0990

    assert candle["close"] == 1.1015

    assert candle["body"] == 0.0015

    assert candle["candle_range"] == 0.003

    assert candle["upper_wick"] == 0.0005

    assert candle["lower_wick"] == 0.001

    assert candle["bullish"] is True

    assert candle["bearish"] is False
