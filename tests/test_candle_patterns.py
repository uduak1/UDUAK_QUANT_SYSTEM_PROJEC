"""
===============================================================================
UDUAK_QUANT_SYSTEM_PROJECT
-------------------------------------------------------------------------------
File: tests/test_candle_patterns.py

Unit tests for CandlePatterns.
===============================================================================
"""

from analysis.candle_patterns import CandlePatterns


def analyzed_candle(**kwargs):
    """
    Create a fully analyzed candle.

    Mirrors the output produced by CandleAnalyzer so every pattern detector
    receives all required fields.
    """

    candle = {
        "open": 1.1000,
        "high": 1.1010,
        "low": 1.0990,
        "close": 1.1005,
        "body": 0.0005,
        "candle_range": 0.0020,
        "upper_wick": 0.0005,
        "lower_wick": 0.0010,
        "bullish": True,
        "bearish": False,
        "body_percent": 25.0,
        "upper_wick_percent": 25.0,
        "lower_wick_percent": 50.0,
        "dominant_part": "LOWER_WICK",
        "strong_body": False,
        "long_upper_wick": False,
        "long_lower_wick": False,
    }

    candle.update(kwargs)

    return candle


def test_empty_list():

    detector = CandlePatterns()

    result = detector.detect([])

    assert result.success is False
    assert result.data is None


def test_doji():

    detector = CandlePatterns()

    candles = [
        analyzed_candle(
            body_percent=5.0,
            upper_wick_percent=47.5,
            lower_wick_percent=47.5,
            bullish=False,
            bearish=False,
        )
    ]

    result = detector.detect(candles)

    assert result.success
    assert "DOJI" in result.data


def test_marubozu():

    detector = CandlePatterns()

    candles = [
        analyzed_candle(
            body_percent=95.0,
            upper_wick_percent=2.0,
            lower_wick_percent=3.0,
            bullish=True,
            bearish=False,
            strong_body=True,
        )
    ]

    result = detector.detect(candles)

    assert "MARUBOZU" in result.data


def test_spinning_top():

    detector = CandlePatterns()

    candles = [
        analyzed_candle(
            body_percent=25.0,
            upper_wick_percent=35.0,
            lower_wick_percent=40.0,
        )
    ]

    result = detector.detect(candles)

    assert "SPINNING_TOP" in result.data


def test_hammer():

    detector = CandlePatterns()

    candles = [
        analyzed_candle(
            body_percent=20.0,
            upper_wick_percent=5.0,
            lower_wick_percent=75.0,
            bullish=True,
            bearish=False,
            long_lower_wick=True,
        )
    ]

    result = detector.detect(candles)

    assert "HAMMER" in result.data


def test_shooting_star():

    detector = CandlePatterns()

    candles = [
        analyzed_candle(
            body_percent=20.0,
            upper_wick_percent=75.0,
            lower_wick_percent=5.0,
            bullish=False,
            bearish=True,
            long_upper_wick=True,
        )
    ]

    result = detector.detect(candles)

    assert "SHOOTING_STAR" in result.data


def test_bullish_engulfing():

    detector = CandlePatterns()

    candles = [

        analyzed_candle(
            open=1.1050,
            close=1.1000,
            bullish=False,
            bearish=True,
            strong_body=True,
            body_percent=70.0,
        ),

        analyzed_candle(
            open=1.0990,
            close=1.1060,
            bullish=True,
            bearish=False,
            strong_body=True,
            body_percent=80.0,
        ),

    ]

    result = detector.detect(candles)

    assert result.success
    assert "BULLISH_ENGULFING" in result.data


def test_bearish_engulfing():

    detector = CandlePatterns()

    candles = [

        analyzed_candle(
            open=1.1000,
            close=1.1050,
            bullish=True,
            bearish=False,
            strong_body=True,
            body_percent=70.0,
        ),

        analyzed_candle(
            open=1.1060,
            close=1.0990,
            bullish=False,
            bearish=True,
            strong_body=True,
            body_percent=80.0,
        ),

    ]

    result = detector.detect(candles)

    assert result.success
    assert "BEARISH_ENGULFING" in result.data


def test_three_white_soldiers():

    detector = CandlePatterns()

    candles = [

        analyzed_candle(
            bullish=True,
            bearish=False,
            strong_body=True,
            body_percent=75.0,
        ),

        analyzed_candle(
            bullish=True,
            bearish=False,
            strong_body=True,
            body_percent=75.0,
        ),

        analyzed_candle(
            bullish=True,
            bearish=False,
            strong_body=True,
            body_percent=75.0,
        ),

    ]

    result = detector.detect(candles)

    assert result.success
    assert "THREE_WHITE_SOLDIERS" in result.data


def test_three_black_crows():

    detector = CandlePatterns()

    candles = [

        analyzed_candle(
            bullish=False,
            bearish=True,
            strong_body=True,
            body_percent=75.0,
        ),

        analyzed_candle(
            bullish=False,
            bearish=True,
            strong_body=True,
            body_percent=75.0,
        ),

        analyzed_candle(
            bullish=False,
            bearish=True,
            strong_body=True,
            body_percent=75.0,
        ),

    ]

    result = detector.detect(candles)

    assert result.success
    assert "THREE_BLACK_CROWS" in result.data