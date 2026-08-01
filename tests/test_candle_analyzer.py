"""

UDUAK_QUANT_SYSTEM_PROJECT

File: tests/test_candle_analyzer.py

Unit tests for analysis/candle_analyzer.py

"""

from analysis.candle_analyzer import CandleAnalyzer
from models.response import Response

def test_analyze_success():

    candle = {
        "open": 1.1000,
        "high": 1.1020,
        "low": 1.0990,
        "close": 1.1015,

        "body": 0.0015,
        "candle_range": 0.0030,
        "upper_wick": 0.0005,
        "lower_wick": 0.0010,

        "bullish": True,
        "bearish": False,
    }

    analyzer = CandleAnalyzer()

    result = analyzer.analyze(candle)

    assert isinstance(result, Response)

    assert result.success is True

    assert result.error is None

    analysis = result.data

    assert analysis["body_percent"] == 50.0

    assert analysis["upper_wick_percent"] == 16.67

    assert analysis["lower_wick_percent"] == 33.33

    assert analysis["dominant_part"] == "BODY"

    assert analysis["strong_body"] is False

    assert analysis["long_upper_wick"] is False

    assert analysis["long_lower_wick"] is False

    assert analysis["bullish"] is True

    assert analysis["bearish"] is False

def test_empty_candle():

    analyzer = CandleAnalyzer()

    result = analyzer.analyze({})

    assert result.success is False

    assert result.data is None

    assert result.message == "No candle supplied."

def test_invalid_candle_range():

    analyzer = CandleAnalyzer()

    candle = {
        "body": 0.0,
        "candle_range": 0.0,
        "upper_wick": 0.0,
        "lower_wick": 0.0,
        "bullish": False,
        "bearish": False,
    }

    result = analyzer.analyze(candle)

    assert result.success is False

    assert result.data is None

    assert result.message == "Invalid candle range."

def test_strong_body():

    analyzer = CandleAnalyzer()

    candle = {
        "body": 0.007,
        "candle_range": 0.010,
        "upper_wick": 0.0015,
        "lower_wick": 0.0015,
        "bullish": True,
        "bearish": False,
    }

    result = analyzer.analyze(candle)

    analysis = result.data

    assert result.success is True

    assert result.data["strong_body"] is True

    assert result.data["dominant_part"] == "BODY"

    assert result.message == "Candle analyzed successfully."