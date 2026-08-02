"""
Tests for analysis/order_block_detector.py
"""

import pytest

from analysis.order_block_detector import OrderBlockDetector


@pytest.fixture
def detector():
    return OrderBlockDetector()


def test_empty_candles(detector):
    result = detector.detect([], {"bos": True, "direction": "BULLISH"})

    assert result.success is False
    assert result.error == "EMPTY_CANDLES"


def test_insufficient_candles(detector):
    candles = [
        {
            "open": 1.1000,
            "close": 1.1010,
            "high": 1.1020,
            "low": 1.0990,
        }
        for _ in range(5)
    ]

    result = detector.detect(
        candles,
        {
            "bos": True,
            "direction": "BULLISH",
        },
    )

    assert result.success is False
    assert result.error == "INSUFFICIENT_CANDLES"


def test_empty_bos(detector):
    candles = [
        {
            "open": 1.1000,
            "close": 1.1010,
            "high": 1.1020,
            "low": 1.0990,
        }
        for _ in range(10)
    ]

    result = detector.detect(candles, {})

    assert result.success is False
    assert result.error == "EMPTY_BOS"


def test_invalid_bos_direction(detector):
    candles = [
        {
            "open": 1.1000,
            "close": 1.1010,
            "high": 1.1020,
            "low": 1.0990,
        }
        for _ in range(10)
    ]

    result = detector.detect(
        candles,
        {
            "bos": True,
            "direction": "UP",
        },
    )

    assert result.success is False
    assert result.error == "INVALID_BOS_DIRECTION"


def test_no_bos(detector):
    candles = [
        {
            "open": 1.1000,
            "close": 1.1010,
            "high": 1.1020,
            "low": 1.0990,
        }
        for _ in range(10)
    ]

    result = detector.detect(
        candles,
        {
            "bos": False,
        },
    )

    assert result.success is True
    assert result.data["order_block_found"] is False


def test_detect_bullish_order_block(detector):
    candles = [
        {
            "open": 1.1000,
            "close": 1.1010,
            "high": 1.1020,
            "low": 1.0990,
            "time": 1,
        }
        for _ in range(9)
    ]

    candles.append(
        {
            "open": 1.1050,
            "close": 1.1030,
            "high": 1.1060,
            "low": 1.1020,
            "time": 10,
        }
    )

    result = detector.detect(
        candles,
        {
            "bos": True,
            "direction": "BULLISH",
        },
    )

    assert result.success is True
    assert result.data["order_block_found"] is True
    assert result.data["bullish_count"] == 1

    block = result.data["bullish_order_blocks"][0]

    assert block["type"] == "BULLISH_ORDER_BLOCK"
    assert block["body_size"] == pytest.approx(0.0020)
    assert block["mitigated"] is False


def test_detect_bearish_order_block(detector):
    candles = [
        {
            "open": 1.1000,
            "close": 1.0990,
            "high": 1.1010,
            "low": 1.0980,
            "time": 1,
        }
        for _ in range(9)
    ]

    candles.append(
        {
            "open": 1.1000,
            "close": 1.1030,
            "high": 1.1040,
            "low": 1.0990,
            "time": 10,
        }
    )

    result = detector.detect(
        candles,
        {
            "bos": True,
            "direction": "BEARISH",
        },
    )

    assert result.success is True
    assert result.data["order_block_found"] is True
    assert result.data["bearish_count"] == 1

    block = result.data["bearish_order_blocks"][0]

    assert block["type"] == "BEARISH_ORDER_BLOCK"
    assert block["body_size"] == pytest.approx(0.0030)
    assert block["mitigated"] is False


def test_invalid_candle_data(detector):
    candles = [
        {
            "open": None,
            "close": None,
            "high": None,
            "low": None,
        }
        for _ in range(10)
    ]

    result = detector.detect(
        candles,
        {
            "bos": True,
            "direction": "BULLISH",
        },
    )

    assert result.success is False
    assert result.error == "INVALID_CANDLE_DATA"