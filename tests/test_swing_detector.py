"""
===============================================================================
UDUAK_QUANT_SYSTEM_PROJECT
-------------------------------------------------------------------------------
File: tests/test_swing_detector.py

Unit tests for SwingDetector.
===============================================================================
"""

from analysis.swing_detector import SwingDetector


def make_candle(high, low, time):
    """
    Create a minimal candle for swing testing.
    """
    return {
        "high": high,
        "low": low,
        "time": time,
    }


def test_no_candles():

    detector = SwingDetector()

    result = detector.detect([])

    assert result.success is False
    assert result.data is None


def test_not_enough_candles():

    detector = SwingDetector()

    candles = [
        make_candle(10, 5, 1),
        make_candle(11, 6, 2),
        make_candle(12, 7, 3),
    ]

    result = detector.detect(candles)

    assert result.success is False
    assert result.data is None


def test_detect_single_swing_high():

    detector = SwingDetector()

    candles = [

        make_candle(10, 5, 1),
        make_candle(12, 6, 2),
        make_candle(20, 8, 3),
        make_candle(11, 6, 4),
        make_candle(10, 5, 5),

    ]

    result = detector.detect(candles)

    assert result.success

    highs = [
        s for s in result.data
        if s["type"] == "SWING_HIGH"
    ]

    assert len(highs) == 1
    assert highs[0]["price"] == 20
    assert highs[0]["structure"] == "INITIAL_HIGH"


def test_detect_single_swing_low():

    detector = SwingDetector()

    candles = [

        make_candle(10, 8, 1),
        make_candle(11, 7, 2),
        make_candle(12, 1, 3),
        make_candle(11, 7, 4),
        make_candle(10, 8, 5),

    ]

    result = detector.detect(candles)

    assert result.success

    lows = [
        s for s in result.data
        if s["type"] == "SWING_LOW"
    ]

    assert len(lows) == 1
    assert lows[0]["price"] == 1
    assert lows[0]["structure"] == "INITIAL_LOW"


def test_higher_high_classification():

    detector = SwingDetector()

    candles = [

        make_candle(10, 5, 1),
        make_candle(12, 6, 2),
        make_candle(20, 7, 3),
        make_candle(11, 6, 4),
        make_candle(10, 5, 5),

        make_candle(12, 6, 6),
        make_candle(14, 7, 7),
        make_candle(25, 8, 8),
        make_candle(13, 7, 9),
        make_candle(12, 6, 10),

    ]

    result = detector.detect(candles)

    highs = [
        s for s in result.data
        if s["type"] == "SWING_HIGH"
    ]

    assert highs[0]["structure"] == "INITIAL_HIGH"
    assert highs[1]["structure"] == "HIGHER_HIGH"


def test_lower_low_classification():

    detector = SwingDetector()

    candles = [

        make_candle(10, 8, 1),
        make_candle(11, 7, 2),
        make_candle(12, 5, 3),
        make_candle(11, 7, 4),
        make_candle(10, 8, 5),

        make_candle(10, 8, 6),
        make_candle(11, 7, 7),
        make_candle(12, 2, 8),
        make_candle(11, 7, 9),
        make_candle(10, 8, 10),

    ]

    result = detector.detect(candles)

    lows = [
        s for s in result.data
        if s["type"] == "SWING_LOW"
    ]

    assert lows[0]["structure"] == "INITIAL_LOW"
    assert lows[1]["structure"] == "LOWER_LOW"