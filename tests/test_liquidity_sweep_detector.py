"""
UDUAK_QUANT_SYSTEM_PROJECT
Tests for LiquiditySweepDetector
"""

from analysis.liquidity_sweep_detector import LiquiditySweepDetector

def test_empty_candles():
    detector = LiquiditySweepDetector()
    result = detector.detect([], {})
    assert result.success is False
    assert result.error == "EMPTY_CANDLES"

def test_insufficient_candles():
    detector = LiquiditySweepDetector()
    candles = [{"high": 1.1050, "low": 1.1000, "close": 1.1030,}]
    result = detector.detect(candles, {})
    assert result.success is False
    assert result.error == "INSUFFICIENT_CANDLES"

def test_empty_liquidity():
    detector = LiquiditySweepDetector()
    candles = [
        {"high": 1.1050, "low": 1.1000, "close": 1.1030,},
        {"high": 1.1060, "low": 1.1010, "close": 1.1040,},
    ]
    result = detector.detect(candles, {})
    assert result.success is False
    assert result.error == "EMPTY_LIQUIDITY"

def test_buy_side_sweep():
    detector = LiquiditySweepDetector()
    candles = [
        {"high": 1.1058, "low": 1.1030, "close": 1.1045,},
        {"high": 1.1040, "low": 1.1020, "close": 1.1035,},
    ]
    liquidity = {"buy_side_liquidity": [1.1050], "sell_side_liquidity": [],}
    result = detector.detect(candles, liquidity)
    assert result.success
    assert result.data["sweep_found"] is True
    assert result.data["buy_sweep_count"] == 1
    assert result.data["sell_sweep_count"] == 0
    sweep = result.data["buy_side_sweeps"][0]
    assert sweep["index"] == 0
    assert sweep["level"] == 1.1050
    assert sweep["direction"] == "BUY_SIDE"

def test_sell_side_sweep():
    detector = LiquiditySweepDetector()
    candles = [
        {"high": 1.1020, "low": 1.0990, "close": 1.1006,},
        {"high": 1.1030, "low": 1.1005, "close": 1.1020,},
    ]
    liquidity = {"buy_side_liquidity": [], "sell_side_liquidity": [1.1000],}
    result = detector.detect(candles, liquidity)
    assert result.success
    assert result.data["sweep_found"] is True
    assert result.data["buy_sweep_count"] == 0
    assert result.data["sell_sweep_count"] == 1
    sweep = result.data["sell_side_sweeps"][0]
    assert sweep["index"] == 0
    assert sweep["level"] == 1.1000
    assert sweep["direction"] == "SELL_SIDE"

def test_no_sweep():
    detector = LiquiditySweepDetector()
    candles = [
        {"high": 1.1040, "low": 1.1020, "close": 1.1035,},
        {"high": 1.1042, "low": 1.1025, "close": 1.1038,},
    ]
    liquidity = {"buy_side_liquidity": [1.1050], "sell_side_liquidity": [1.1000],}
    result = detector.detect(candles, liquidity)
    assert result.success
    assert result.data["sweep_found"] is False
    assert result.data["buy_side_sweeps"] == []
    assert result.data["sell_side_sweeps"] == []
    assert result.data["buy_sweep_count"] == 0
    assert result.data["sell_sweep_count"] == 0

def test_response_structure():
    detector = LiquiditySweepDetector()
    candles = [
        {"high": 1.1058, "low": 1.1030, "close": 1.1045,},
        {"high": 1.1040, "low": 1.1020, "close": 1.1035,},
    ]
    liquidity = {"buy_side_liquidity": [1.1050], "sell_side_liquidity": [],}
    result = detector.detect(candles, liquidity)
    assert result.success
    expected_keys = {"sweep_found","buy_side_sweeps","sell_side_sweeps","buy_sweep_count","sell_sweep_count",}
    assert expected_keys.issubset(result.data.keys())

def test_skip_candle_with_missing_close():
    from analysis.liquidity_sweep_detector import LiquiditySweepDetector
    detector = LiquiditySweepDetector()
    candles = [
        {"high": 1.1010, "low": 1.0990, "close": None,},
        {"high": 1.1020, "low": 1.1000, "close": 1.1010,},
    ]
    liquidity = {
        "buy_side_liquidity": [],
        "sell_side_liquidity": [],
    }
    result = detector.detect(candles, liquidity)
    assert result.success is True
    assert result.data["buy_side_sweeps"] == []
    assert result.data["sell_side_sweeps"] == []
