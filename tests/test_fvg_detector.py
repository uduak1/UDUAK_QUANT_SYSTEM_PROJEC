"""
UDUAK_QUANT_SYSTEM_PROJECT

File: tests/test_fvg_detector.py

Tests:
    - Empty candles
    - Insufficient candles
    - Invalid candle data
    - Bullish FVG detection
    - Bearish FVG detection
    - No FVG detection
    - Midpoint calculation
    - Gap size calculation
    - Returned fields
    - OHLC validation
"""

from analysis.fvg_detector import FVGDetector


# ==========================================================
# Helpers
# ==========================================================

def bullish_fvg_candles():
    return [
        {
            "open": 100,
            "close": 101,
            "high": 102,
            "low": 99,
            "time": "2026-01-01T00:00:00",
        },
        {
            "open": 103,
            "close": 108,
            "high": 109,
            "low": 103,
            "time": "2026-01-01T01:00:00",
        },
        {
            "open": 106,
            "close": 107,
            "high": 108,
            "low": 105,
            "time": "2026-01-01T02:00:00",
        },
    ]


def bearish_fvg_candles():
    return [
        {
            "open": 110,
            "close": 109,
            "high": 111,
            "low": 108,
            "time": "2026-01-01T00:00:00",
        },
        {
            "open": 107,
            "close": 102,
            "high": 108,
            "low": 101,
            "time": "2026-01-01T01:00:00",
        },
        {
            "open": 104,
            "close": 103,
            "high": 105,
            "low": 102,
            "time": "2026-01-01T02:00:00",
        },
    ]


# ==========================================================
# Empty candles
# ==========================================================

def test_empty_candles():

    detector = FVGDetector()

    result = detector.detect([])

    assert result.success is False
    assert result.error == "EMPTY_CANDLES"


# ==========================================================
# Insufficient candles
# ==========================================================

def test_insufficient_candles():

    detector = FVGDetector()

    candles = [
        {
            "open": 1,
            "close": 1,
            "high": 1,
            "low": 1,
        }
    ]

    result = detector.detect(candles)

    assert result.success is False
    assert result.error == "INSUFFICIENT_CANDLES"


# ==========================================================
# Invalid candle
# ==========================================================

def test_invalid_candle_data():

    detector = FVGDetector()

    candles = [
        {},
        {},
        {},
    ]

    result = detector.detect(candles)

    assert result.success is False
    assert result.error == "INVALID_CANDLE_DATA"


# ==========================================================
# Bullish FVG
# ==========================================================

def test_bullish_fvg():

    detector = FVGDetector()

    result = detector.detect(
        bullish_fvg_candles()
    )

    assert result.success

    assert result.data["fvg_found"] is True

    assert result.data["bullish_count"] == 1

    assert result.data["bearish_count"] == 0


# ==========================================================
# Bearish FVG
# ==========================================================

def test_bearish_fvg():

    detector = FVGDetector()

    result = detector.detect(
        bearish_fvg_candles()
    )

    assert result.success

    assert result.data["fvg_found"] is True

    assert result.data["bullish_count"] == 0

    assert result.data["bearish_count"] == 1


# ==========================================================
# No FVG
# ==========================================================

def test_no_fvg():

    detector = FVGDetector()

    candles = [
        {
            "open":100,
            "close":101,
            "high":102,
            "low":99,
        },
        {
            "open":101,
            "close":102,
            "high":103,
            "low":100,
        },
        {
            "open":102,
            "close":103,
            "high":104,
            "low":101,
        },
    ]

    result = detector.detect(candles)

    assert result.success

    assert result.data["fvg_found"] is False

    assert result.data["bullish_count"] == 0

    assert result.data["bearish_count"] == 0


# ==========================================================
# Midpoint
# ==========================================================

def test_midpoint():

    detector = FVGDetector()

    result = detector.detect(
        bullish_fvg_candles()
    )

    fvg = result.data["bullish_fvg"][0]

    assert fvg["midpoint"] == (
        fvg["top"] + fvg["bottom"]
    ) / 2

    assert (
        fvg["consequent_encroachment"]
        == fvg["midpoint"]
    )


# ==========================================================
# Gap size
# ==========================================================

def test_gap_size():

    detector = FVGDetector()

    result = detector.detect(
        bullish_fvg_candles()
    )

    fvg = result.data["bullish_fvg"][0]

    assert fvg["gap_size"] == (
        fvg["top"] - fvg["bottom"]
    )


# ==========================================================
# Returned fields
# ==========================================================

def test_returned_fields():

    detector = FVGDetector()

    result = detector.detect(
        bullish_fvg_candles()
    )

    fvg = result.data["bullish_fvg"][0]

    expected = {
        "id",
        "index",
        "created_index",
        "type",
        "direction",
        "top",
        "bottom",
        "midpoint",
        "consequent_encroachment",
        "gap_size",
        "impulse_open",
        "impulse_close",
        "impulse_high",
        "impulse_low",
        "time",
    }

    assert expected.issubset(
        set(fvg.keys())
    )


# ==========================================================
# Invalid OHLC
# ==========================================================

def test_invalid_ohlc():

    detector = FVGDetector()

    candles = [
        {
            "open":100,
            "close":101,
            "high":99,
            "low":98,
        },
        {
            "open":100,
            "close":101,
            "high":99,
            "low":98,
        },
        {
            "open":100,
            "close":101,
            "high":99,
            "low":98,
        },
    ]

    result = detector.detect(candles)

    assert result.success is False

    assert result.error == "INVALID_CANDLE_DATA"