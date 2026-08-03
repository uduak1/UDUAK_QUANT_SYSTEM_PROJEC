import pytest

from analysis.fvg_detector import FVGDetector
from analysis.fvg_analyzer import FVGAnalyzer

@pytest.fixture
def detector():
    return FVGDetector()

@pytest.fixture
def analyzer():
    return FVGAnalyzer()

def test_analyze_bullish_fvg(detector, analyzer):
    candles = [
        {"high": 100, "low": 95, "open": 96, "close": 99},
        {"high": 110, "low": 101, "open": 102, "close": 109},
        {"high": 120, "low": 105, "open": 106, "close": 118},
        {"high": 125, "low": 99, "open": 101, "close": 122},
        {"high": 126, "low": 97, "open": 98, "close": 120},
    ]

    detection = detector.detect(candles)

    fvg_list = (
        detection.data["bullish_fvg"]
        + detection.data["bearish_fvg"]
    )

    result = analyzer.analyze(candles, fvg_list)

    assert result.success is True
    assert result.data["count"] == 1

    fvg = result.data["analyzed_fvg"][0]

    assert fvg["direction"] == "BULLISH"
    assert fvg["gap_size"] == 5
    assert fvg["midpoint"] == 102.5
    assert fvg["age"] == 3
    assert "fill_percentage" in fvg
    assert "status" in fvg

def test_empty_candles(analyzer):
    result = analyzer.analyze([], [])

    assert result.success is False
    assert result.error == "EMPTY_CANDLES"

def test_none_fvg(analyzer):
    candles = [
        {"high": 10, "low": 5}
    ]

    result = analyzer.analyze(candles, None)

    assert result.success is False
    assert result.error == "EMPTY_FVG"

def test_empty_fvg_list(analyzer):
    candles = [
        {"high": 10, "low": 5}
    ]

    result = analyzer.analyze(candles, [])

    assert result.success is True
    assert result.data["count"] == 0

def test_skip_invalid_fvg(analyzer):
    candles = [
        {"high": 10, "low": 5},
        {"high": 11, "low": 6},
        {"high": 12, "low": 7},
    ]

    invalid = [
        {
            "top": 10,
            "bottom": 10,
            "direction": "BULLISH",
        }
    ]

    result = analyzer.analyze(candles, invalid)

    assert result.success is True
    assert result.data["count"] == 0

def test_validate_fvg():
    analyzer = FVGAnalyzer()

    valid = {
        "top": 110.0,
        "bottom": 100.0,
        "created_index": 5,
        "direction": "BULLISH",
    }

    assert analyzer._validate_fvg(valid) is True

def test_validate_bad_direction():
    analyzer = FVGAnalyzer()

    bad = {
        "top": 110,
        "bottom": 100,
        "created_index": 5,
        "direction": "SIDEWAYS",
    }

    assert analyzer._validate_fvg(bad) is False

def test_validate_bad_gap():
    analyzer = FVGAnalyzer()

    bad = {
        "top": 100,
        "bottom": 100,
        "created_index": 5,
        "direction": "BULLISH",
    }

    assert analyzer._validate_fvg(bad) is False

def test_status_values():
    analyzer = FVGAnalyzer()

    assert analyzer._status(0) == "OPEN"
    assert analyzer._status(25) == "PARTIALLY_FILLED"
    assert analyzer._status(100) == "MITIGATED"

def test_is_mitigated():
    analyzer = FVGAnalyzer()

    assert analyzer._is_mitigated(100) is True
    assert analyzer._is_mitigated(99.99) is False

# ==========================================================
# Additional edge-case coverage
# ==========================================================

def test_validate_none():
    analyzer = FVGAnalyzer()
    assert analyzer.validate_fvg(None) is False

def test_validate_missing_direction():
    analyzer = FVGAnalyzer()
    fvg = {"gap_size": 15, "status": "OPEN"}
    assert analyzer.validate_fvg(fvg) is False

def test_validate_missing_status():
    analyzer = FVGAnalyzer()
    fvg = {"direction": "bullish", "gap_size": 15}
    assert analyzer.validate_fvg(fvg) is False

def test_validate_missing_gap():
    analyzer = FVGAnalyzer()
    fvg = {"direction": "bullish", "status": "OPEN"}
    assert analyzer.validate_fvg(fvg) is False

def test_validate_zero_gap():
    analyzer = FVGAnalyzer()
    fvg = {"direction": "bullish", "status": "OPEN", "gap_size": 0}
    assert analyzer.validate_fvg(fvg) is False

def test_validate_negative_gap():
    analyzer = FVGAnalyzer()
    fvg = {"direction": "bearish", "status": "OPEN", "gap_size": -8}
    assert analyzer.validate_fvg(fvg) is False

def test_is_mitigated_none():
    analyzer = FVGAnalyzer()
    assert analyzer.is_mitigated(None) is False

def test_is_mitigated_missing_status():
    analyzer = FVGAnalyzer()
    fvg = {}
    assert analyzer.is_mitigated(fvg) is False

def test_is_mitigated_partial():
    analyzer = FVGAnalyzer()
    fvg = {"status": "PARTIALLY_FILLED"}
    assert analyzer.is_mitigated(fvg) is False

def test_is_mitigated_true():
    analyzer = FVGAnalyzer()
    fvg = {"status": "MITIGATED"}
    assert analyzer.is_mitigated(fvg) is True

def test_validate_case_sensitivity():
    analyzer = FVGAnalyzer()
    fvg = {"direction": "Bullish", "gap_size": 20, "status": "OPEN"}
    assert analyzer.validate_fvg(fvg) is False

def test_validate_unknown_status():
    analyzer = FVGAnalyzer()
    fvg = {"direction": "bullish", "gap_size": 20, "status": "UNKNOWN"}
    assert analyzer.validate_fvg(fvg) is False

def test_validate_unknown_direction():
    analyzer = FVGAnalyzer()
    fvg = {"direction": "sideways", "gap_size": 20, "status": "OPEN"}
    assert analyzer.validate_fvg(fvg) is False

def test_validate_invalid_top_type():
    analyzer = FVGAnalyzer()
    fvg = {
        "direction": "bullish",
        "status": "OPEN",
        "gap_size": 20,
        "top": "100.5",
        "bottom": 99.5
    }
    assert analyzer.validate_fvg(fvg) is False

def test_validate_invalid_top_type_internal():
    analyzer = FVGAnalyzer()
    fvg = {
        "top": "100.0",
        "bottom": 99.0,
        "created_index": 5,
        "direction": "BULLISH",
    }
    assert analyzer.validate_fvg(fvg) is False

def test_validate_invalid_bottom_type():
    analyzer = FVGAnalyzer()
    fvg = {
        "top": 100.0,
        "bottom": "99.0",
        "created_index": 5,
        "direction": "BULLISH",
    }
    assert analyzer.validate_fvg(fvg) is False

def test_validate_invalid_created_index_type():
    analyzer = FVGAnalyzer()
    fvg = {
        "top": 100.0,
        "bottom": 99.0,
        "created_index": "5",
        "direction": "BULLISH",
    }
    assert analyzer.validate_fvg(fvg) is False

# ==========================================================
# Coverage for uncovered branches (lines 168, 171, 313, 322, 353-364, 403, 413, 423, 513)
# ==========================================================

def test_extract_candle_fields_missing_high():
    analyzer = FVGAnalyzer()
    candle = {"low": 1.1000}
    assert analyzer._extract_candle_fields(candle) is None

def test_extract_candle_fields_missing_low():
    analyzer = FVGAnalyzer()
    candle = {"high": 1.1200}
    assert analyzer._extract_candle_fields(candle) is None

def test_extract_candle_fields_invalid_range():
    analyzer = FVGAnalyzer()
    candle = {"high": 1.1000, "low": 1.2000}
    assert analyzer._extract_candle_fields(candle) is None

def test_calculate_fill_percentage_zero_gap():
    analyzer = FVGAnalyzer()
    assert analyzer._calculate_fill_percentage(
        top=100,
        bottom=100,
        candles=[],
        start_index=0,
        bullish=True,
    ) == 0.0

def test_fill_percentage_skips_invalid_candle():
    analyzer = FVGAnalyzer()
    candles = [{"high": None, "low": 100}]
    analyzer._calculate_fill_percentage(
        top=110,
        bottom=100,
        candles=candles,
        start_index=0,
        bullish=True,
    )

def test_calculate_fill_percentage_bearish_gap():
    analyzer = FVGAnalyzer()
    candles = [{"high": 108, "low": 104}]
    result = analyzer._calculate_fill_percentage(
        top=110,
        bottom=100,
        candles=candles,
        start_index=0,
        bullish=False,
    )
    assert result > 0

def test_count_retests_skips_invalid_candle():
    analyzer = FVGAnalyzer()
    fvg = {
        "top": 10,
        "bottom": 5,
        "direction": "BULLISH",
        "created_index": 0
    }
    # line 403: if fields is None: continue
    result = analyzer.analyze(
        [{"high": 10, "low": 5}, {"high": None, "low": 1}, {"high": 12, "low": 11}],
        [fvg]
    )
    assert result.success is True

def test_count_retests_bearish():
    analyzer = FVGAnalyzer()
    # line 413: bearish branch `touched = high >= bottom`
    fvg = {
        "top": 110,
        "bottom": 100,
        "direction": "BEARISH",
        "created_index": 0
    }
    candles = [
        {"high": 10, "low": 5},
        {"high": 11, "low": 6},
        {"high": 12, "low": 7},
        {"high": 105, "low": 95},
    ]
    result = analyzer.analyze(candles, [fvg])
    assert result.success is True

def test_count_retests_leave_gap():
    analyzer = FVGAnalyzer()
    # line 423: `elif not touched: inside_gap = False`
    fvg = {
        "top": 110,
        "bottom": 100,
        "direction": "BULLISH",
        "created_index": 0
    }
    candles = [
        {"high": 10, "low": 5},
        {"high": 11, "low": 6},
        {"high": 12, "low": 7},
        {"high": 105, "low": 95},
        {"high": 90, "low": 80},
        {"high": 105, "low": 95},
    ]
    result = analyzer.analyze(candles, [fvg])
    assert result.success is True

def test_analysis_start_index_beyond_candles():
    analyzer = FVGAnalyzer()
    # line 513: `if start_index >= len(candles): start_index = len(candles)`
    fvg = {
        "top": 110,
        "bottom": 100,
        "direction": "BULLISH",
        "created_index": 100,
    }
    candles = [
        {"high": 10, "low": 5},
        {"high": 11, "low": 6},
        {"high": 12, "low": 7},
    ]
    result = analyzer.analyze(candles, [fvg])
    assert result.success is True