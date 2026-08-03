import pytest
from unittest.mock import patch

from analysis.liquidity_analyzer import LiquidityAnalyzer


def test_empty_candles():
    analyzer = LiquidityAnalyzer()
    assert analyzer.analyze([]) == []


def test_validate_none():
    analyzer = LiquidityAnalyzer()
    assert analyzer.validate_liquidity(None) is False


def test_validate_valid():
    analyzer = LiquidityAnalyzer()
    liquidity = {
        "level": 1.2050,
        "type": analyzer.BUY_SIDE,
        "created_index": 10,
    }
    assert analyzer.validate_liquidity(liquidity) is True


def test_validate_missing_level():
    analyzer = LiquidityAnalyzer()
    liquidity = {
        "type": analyzer.BUY_SIDE,
        "created_index": 10,
    }
    assert analyzer.validate_liquidity(liquidity) is False


def test_validate_missing_type():
    analyzer = LiquidityAnalyzer()
    liquidity = {
        "level": 1.2050,
        "created_index": 10,
    }
    assert analyzer.validate_liquidity(liquidity) is False


def test_validate_missing_created_index():
    analyzer = LiquidityAnalyzer()
    liquidity = {
        "level": 1.2050,
        "type": analyzer.BUY_SIDE,
    }
    assert analyzer.validate_liquidity(liquidity) is False


def test_validate_bad_type():
    analyzer = LiquidityAnalyzer()
    liquidity = {
        "level": 1.2050,
        "type": "INVALID",
        "created_index": 10,
    }
    assert analyzer.validate_liquidity(liquidity) is False


def test_validate_bad_level():
    analyzer = LiquidityAnalyzer()
    liquidity = {
        "level": "bad",
        "type": analyzer.BUY_SIDE,
        "created_index": 10,
    }
    assert analyzer.validate_liquidity(liquidity) is False


def test_validate_bad_created_index():
    analyzer = LiquidityAnalyzer()
    liquidity = {
        "level": 1.2050,
        "type": analyzer.BUY_SIDE,
        "created_index": "10",
    }
    assert analyzer.validate_liquidity(liquidity) is False


def test_extract_candle_fields_valid():
    analyzer = LiquidityAnalyzer()
    candle = {
        "high": 10,
        "low": 5,
    }
    assert analyzer._extract_candle_fields(candle) == (10.0, 5.0)


def test_extract_candle_fields_missing_high():
    analyzer = LiquidityAnalyzer()
    candle = {
        "low": 5,
    }
    assert analyzer._extract_candle_fields(candle) is None


def test_extract_candle_fields_missing_low():
    analyzer = LiquidityAnalyzer()
    candle = {
        "high": 10,
    }
    assert analyzer._extract_candle_fields(candle) is None


def test_extract_candle_fields_invalid_range():
    analyzer = LiquidityAnalyzer()
    candle = {
        "high": 5,
        "low": 10,
    }
    assert analyzer._extract_candle_fields(candle) is None


def test_extract_candle_fields_invalid_high_type():
    analyzer = LiquidityAnalyzer()

    candle = {
        "high": "10",   # invalid
        "low": 5,
    }

    assert analyzer._extract_candle_fields(candle) is None


def test_extract_candle_fields_invalid_low_type():
    analyzer = LiquidityAnalyzer()

    candle = {
        "high": 10,
        "low": "5",     # invalid
    }

    assert analyzer._extract_candle_fields(candle) is None


def test_calculate_age():
    analyzer = LiquidityAnalyzer()
    assert analyzer._calculate_age(10, 20) == 10


def test_calculate_age_negative():
    analyzer = LiquidityAnalyzer()
    assert analyzer._calculate_age(20, 10) == 0


def test_status_swept():
    analyzer = LiquidityAnalyzer()
    assert analyzer._status(True) == analyzer.SWEPT


def test_status_active():
    analyzer = LiquidityAnalyzer()
    assert analyzer._status(False) == analyzer.ACTIVE


def test_is_swing_high_true():
    analyzer = LiquidityAnalyzer()

    candles = [
        {"high": 10, "low": 5},
        {"high": 15, "low": 8},
        {"high": 11, "low": 6},
    ]

    assert analyzer._is_swing_high(candles, 1) is True


def test_is_swing_high_false():
    analyzer = LiquidityAnalyzer()

    candles = [
        {"high": 15, "low": 5},
        {"high": 10, "low": 6},
        {"high": 11, "low": 7},
    ]

    assert analyzer._is_swing_high(candles, 1) is False


def test_is_swing_high_first_index():
    analyzer = LiquidityAnalyzer()

    candles = [
        {"high": 10, "low": 5},
        {"high": 15, "low": 8},
        {"high": 11, "low": 6},
    ]

    assert analyzer._is_swing_high(candles, 0) is False


def test_is_swing_high_last_index():
    analyzer = LiquidityAnalyzer()

    candles = [
        {"high": 10, "low": 5},
        {"high": 15, "low": 8},
        {"high": 11, "low": 6},
    ]

    assert analyzer._is_swing_high(candles, 2) is False


def test_is_swing_high_invalid_neighbor():
    analyzer = LiquidityAnalyzer()

    candles = [
        {"high": 10},  # invalid
        {"high": 15, "low": 8},
        {"high": 11, "low": 6},
    ]

    assert analyzer._is_swing_high(candles, 1) is False


def test_is_swing_low_true():
    analyzer = LiquidityAnalyzer()

    candles = [
        {"high": 15, "low": 8},
        {"high": 12, "low": 5},
        {"high": 14, "low": 7},
    ]

    assert analyzer._is_swing_low(candles, 1) is True


def test_is_swing_low_false():
    analyzer = LiquidityAnalyzer()

    candles = [
        {"high": 15, "low": 5},
        {"high": 12, "low": 8},
        {"high": 14, "low": 7},
    ]

    assert analyzer._is_swing_low(candles, 1) is False


def test_is_swing_low_first_index():
    analyzer = LiquidityAnalyzer()

    candles = [
        {"high": 15, "low": 8},
        {"high": 12, "low": 5},
        {"high": 14, "low": 7},
    ]

    assert analyzer._is_swing_low(candles, 0) is False


def test_is_swing_low_last_index():
    analyzer = LiquidityAnalyzer()

    candles = [
        {"high": 15, "low": 8},
        {"high": 12, "low": 5},
        {"high": 14, "low": 7},
    ]

    assert analyzer._is_swing_low(candles, 2) is False


def test_is_swing_low_invalid_neighbor():
    analyzer = LiquidityAnalyzer()

    candles = [
        {"high": 15, "low": 8},
        {"high": 12, "low": 5},
        {"high": 14},  # invalid (missing low)
    ]

    assert analyzer._is_swing_low(candles, 1) is False


def test_find_equal_highs_empty():
    analyzer = LiquidityAnalyzer()

    assert analyzer._find_equal_highs([]) == []


def test_find_equal_highs_no_equal_highs():
    analyzer = LiquidityAnalyzer()

    candles = [
        {"high": 10, "low": 5},
        {"high": 15, "low": 8},   # swing high
        {"high": 11, "low": 6},
        {"high": 18, "low": 9},   # swing high (not equal)
        {"high": 12, "low": 7},
    ]

    assert analyzer._find_equal_highs(candles) == []


def test_find_equal_highs_found():
    analyzer = LiquidityAnalyzer()

    candles = [
        {"high": 10.0, "low": 5},
        {"high": 15.0, "low": 8},      # swing high
        {"high": 11.0, "low": 6},
        {"high": 15.00005, "low": 9},  # equal swing high
        {"high": 10.0, "low": 5},
    ]

    result = analyzer._find_equal_highs(candles)

    assert len(result) == 1
    assert result[0]["type"] == analyzer.BUY_SIDE
    assert result[0]["created_index"] == 3


def test_find_equal_highs_invalid_candle():
    analyzer = LiquidityAnalyzer()

    candles = [
        {"high": 10, "low": 5},
        {"high": 15},               # invalid
        {"high": 11, "low": 6},
        {"high": 15, "low": 8},
        {"high": 10, "low": 5},
    ]

    assert analyzer._find_equal_highs(candles) == []


def test_find_equal_lows_empty():
    analyzer = LiquidityAnalyzer()

    assert analyzer._find_equal_lows([]) == []


def test_find_equal_lows_no_equal_lows():
    analyzer = LiquidityAnalyzer()

    candles = [
        {"high": 15, "low": 10},
        {"high": 14, "low": 5},   # swing low
        {"high": 15, "low": 8},
        {"high": 16, "low": 2},   # swing low (not equal)
        {"high": 17, "low": 9},
    ]

    assert analyzer._find_equal_lows(candles) == []


def test_find_equal_lows_found():
    analyzer = LiquidityAnalyzer()

    candles = [
        {"high": 15, "low": 10},
        {"high": 14, "low": 5.00000},      # swing low
        {"high": 15, "low": 8},
        {"high": 16, "low": 5.00005},      # equal swing low
        {"high": 17, "low": 9},
    ]

    result = analyzer._find_equal_lows(candles)

    assert len(result) == 1
    assert result[0]["type"] == analyzer.SELL_SIDE
    assert result[0]["created_index"] == 3


def test_find_equal_lows_invalid_candle():
    analyzer = LiquidityAnalyzer()

    candles = [
        {"high": 15, "low": 10},
        {"low": 5},               # invalid (missing high)
        {"high": 15, "low": 8},
        {"high": 16, "low": 5},
        {"high": 17, "low": 9},
    ]

    assert analyzer._find_equal_lows(candles) == []


def test_detect_buy_side_liquidity_empty():
    analyzer = LiquidityAnalyzer()

    assert analyzer._detect_buy_side_liquidity([]) == []


def test_detect_buy_side_liquidity_none_found():
    analyzer = LiquidityAnalyzer()

    candles = [
        {"high": 10, "low": 8},
        {"high": 11, "low": 9},
        {"high": 12, "low": 10},
    ]

    assert analyzer._detect_buy_side_liquidity(candles) == []


def test_detect_buy_side_liquidity_found():
    analyzer = LiquidityAnalyzer()

    candles = [
        {"high": 8, "low": 5},
        {"high": 10, "low": 7},
        {"high": 9, "low": 6},
        {"high": 10.00001, "low": 7},
        {"high": 8, "low": 5},
    ]

    result = analyzer._detect_buy_side_liquidity(candles)

    assert len(result) == 1
    assert result[0]["type"] == analyzer.BUY_SIDE
    assert result[0]["status"] == analyzer.ACTIVE
    assert "level" in result[0]
    assert "created_index" in result[0]


def test_detect_sell_side_liquidity_empty():
    analyzer = LiquidityAnalyzer()

    assert analyzer._detect_sell_side_liquidity([]) == []


def test_detect_sell_side_liquidity_none_found():
    analyzer = LiquidityAnalyzer()

    candles = [
        {"high": 10, "low": 8},
        {"high": 9, "low": 7},
        {"high": 8, "low": 6},
        {"high": 7, "low": 5},
        {"high": 6, "low": 4},
    ]

    result = analyzer._detect_sell_side_liquidity(candles)

    assert result == []


def test_detect_sell_side_liquidity_found():
    analyzer = LiquidityAnalyzer()

    candles = [
        {"high": 10, "low": 7},
        {"high": 9, "low": 5},
        {"high": 8, "low": 6},
        {"high": 9, "low": 5.00005},
        {"high": 10, "low": 7},
    ]

    result = analyzer._detect_sell_side_liquidity(candles)

    assert len(result) == 1

    liquidity = result[0]

    assert liquidity["level"] == 5
    assert liquidity["type"] == analyzer.SELL_SIDE
    assert liquidity["status"] == analyzer.ACTIVE
    assert liquidity["created_index"] == 3


def test_detect_sell_side_liquidity_invalid_equal_low():
    analyzer = LiquidityAnalyzer()

    analyzer._find_equal_lows = lambda candles: [
        {
            "level": 5,
            "type": analyzer.SELL_SIDE,
            "created_index": 3,
        }
    ]

    result = analyzer._detect_sell_side_liquidity([])

    assert len(result) == 1


def test_is_liquidity_swept_buy_side_true():
    analyzer = LiquidityAnalyzer()

    liquidity = {
        "level": 10.0,
        "type": analyzer.BUY_SIDE,
        "created_index": 0,
    }

    candles = [
        {"high": 9, "low": 8},
        {"high": 10.2, "low": 9},
    ]

    assert analyzer._is_liquidity_swept(liquidity, candles) is True


def test_is_liquidity_swept_buy_side_false():
    analyzer = LiquidityAnalyzer()

    liquidity = {
        "level": 10.0,
        "type": analyzer.BUY_SIDE,
        "created_index": 0,
    }

    candles = [
        {"high": 9.8, "low": 8},
        {"high": 9.9, "low": 8},
    ]

    assert analyzer._is_liquidity_swept(liquidity, candles) is False


def test_is_liquidity_swept_sell_side_true():
    analyzer = LiquidityAnalyzer()

    liquidity = {
        "level": 5.0,
        "type": analyzer.SELL_SIDE,
        "created_index": 0,
    }

    candles = [
        {"high": 7, "low": 5.5},
        {"high": 6, "low": 4.8},
    ]

    assert analyzer._is_liquidity_swept(liquidity, candles) is True


def test_is_liquidity_swept_invalid_candle():
    analyzer = LiquidityAnalyzer()

    liquidity = {
        "level": 10,
        "type": analyzer.BUY_SIDE,
        "created_index": 0,
    }

    candles = [
        {"low": 5},
        {"high": 10.5, "low": 9},
    ]

    assert analyzer._is_liquidity_swept(liquidity, candles) is True


def test_analyze_single_liquidity():
    analyzer = LiquidityAnalyzer()

    liquidity = {
        "level": 10.0,
        "type": analyzer.BUY_SIDE,
        "created_index": 1,
    }

    candles = [
        {"high": 9.0, "low": 8.0},
        {"high": 10.0, "low": 9.0},
        {"high": 10.5, "low": 9.5},   # sweeps liquidity
    ]

    result = analyzer._analyze_single_liquidity(
        liquidity,
        candles,
    )

    assert result["level"] == 10.0
    assert result["type"] == analyzer.BUY_SIDE
    assert result["created_index"] == 1
    assert result["swept"] is True
    assert result["status"] == analyzer.SWEPT
    assert result["strength"] == 0.5
    assert result["age"] == 1


def test_is_swept_buy_side_true():
    analyzer = LiquidityAnalyzer()

    liquidity = {
        "level": 10,
        "type": analyzer.BUY_SIDE,
        "created_index": 0,
    }

    candles = [
        {"high": 9, "low": 7},
        {"high": 10.2, "low": 8},
    ]

    assert analyzer._is_swept(liquidity, candles) is True


def test_is_swept_buy_side_false():
    analyzer = LiquidityAnalyzer()

    liquidity = {
        "level": 10,
        "type": analyzer.BUY_SIDE,
        "created_index": 0,
    }

    candles = [
        {"high": 9.9, "low": 8},
        {"high": 9.8, "low": 7},
    ]

    assert analyzer._is_swept(liquidity, candles) is False


def test_is_swept_sell_side_true():
    analyzer = LiquidityAnalyzer()

    liquidity = {
        "level": 5,
        "type": analyzer.SELL_SIDE,
        "created_index": 0,
    }

    candles = [
        {"high": 7, "low": 5.2},
        {"high": 6, "low": 4.8},
    ]

    assert analyzer._is_swept(liquidity, candles) is True


def test_is_swept_sell_side_false():
    analyzer = LiquidityAnalyzer()

    liquidity = {
        "level": 5,
        "type": analyzer.SELL_SIDE,
        "created_index": 0,
    }

    candles = [
        {"high": 7, "low": 5.2},
        {"high": 6, "low": 5.1},
    ]

    assert analyzer._is_swept(liquidity, candles) is False


def test_is_swept_invalid_candle():
    analyzer = LiquidityAnalyzer()

    liquidity = {
        "level": 10,
        "type": analyzer.BUY_SIDE,
        "created_index": 0,
    }

    candles = [
        {"low": 5},
        {"high": 11, "low": 8},
    ]

    assert analyzer._is_swept(liquidity, candles) is True


def test_calculate_sweep_strength_buy_side():
    analyzer = LiquidityAnalyzer()

    liquidity = {
        "level": 10,
        "type": analyzer.BUY_SIDE,
        "created_index": 0,
    }

    candles = [
        {"high": 10.1, "low": 8},
        {"high": 10.5, "low": 8},
        {"high": 10.3, "low": 8},
    ]

    assert analyzer._calculate_sweep_strength(liquidity, candles) == 0.5


def test_calculate_sweep_strength_sell_side():
    analyzer = LiquidityAnalyzer()

    liquidity = {
        "level": 5,
        "type": analyzer.SELL_SIDE,
        "created_index": 0,
    }

    candles = [
        {"high": 6, "low": 4.8},
        {"high": 6, "low": 4.4},
        {"high": 6, "low": 4.7},
    ]

    assert analyzer._calculate_sweep_strength(liquidity, candles) == 0.6


def test_calculate_sweep_strength_none():
    analyzer = LiquidityAnalyzer()

    liquidity = {
        "level": 10,
        "type": analyzer.BUY_SIDE,
        "created_index": 0,
    }

    candles = [
        {"high": 9.8, "low": 8},
        {"high": 9.9, "low": 8},
    ]

    assert analyzer._calculate_sweep_strength(liquidity, candles) == 0.0


def test_calculate_sweep_strength_invalid_candle():
    analyzer = LiquidityAnalyzer()

    liquidity = {
        "level": 10,
        "type": analyzer.BUY_SIDE,
        "created_index": 0,
    }

    candles = [
        {"low": 5},
        {"high": 10.4, "low": 8},
    ]

    assert analyzer._calculate_sweep_strength(liquidity, candles) == 0.4


def test_analyze_no_liquidity():
    analyzer = LiquidityAnalyzer()

    candles = [
        {"high": 1, "low": 0},
        {"high": 2, "low": 1},
        {"high": 3, "low": 2},
        {"high": 4, "low": 3},
    ]

    result = analyzer.analyze(candles)

    assert result == []


def test_analyze_buy_side():
    analyzer = LiquidityAnalyzer(equal_tolerance=0.1)

    candles = [
        {"high": 8, "low": 5},
        {"high": 10, "low": 7},
        {"high": 9, "low": 6},
        {"high": 10.05, "low": 7},
        {"high": 8, "low": 5},
        {"high": 10.50, "low": 8},
    ]

    result = analyzer.analyze(candles)

    assert len(result) == 1
    assert result[0]["type"] == analyzer.BUY_SIDE


def test_analyze_sell_side():
    analyzer = LiquidityAnalyzer(equal_tolerance=0.1)

    candles = [
        {"high": 10, "low": 8},
        {"high": 9, "low": 5},
        {"high": 8, "low": 6},
        {"high": 9, "low": 5.05},
        {"high": 10, "low": 8},
        {"high": 9, "low": 4.50},
    ]

    result = analyzer.analyze(candles)

    assert len(result) == 1
    assert result[0]["type"] == analyzer.SELL_SIDE


def test_find_equal_highs_left_invalid_type():
    analyzer = LiquidityAnalyzer()

    candles = [
        {"high": 8, "low": 5},
        {"high": "10", "low": 7},   # invalid swing candle
        {"high": 9, "low": 6},
        {"high": 10, "low": 7},
        {"high": 8, "low": 5},
    ]

    assert analyzer._find_equal_highs(candles) == []


def test_find_equal_highs_right_invalid_type():
    analyzer = LiquidityAnalyzer()

    candles = [
        {"high": 8, "low": 5},
        {"high": 10, "low": 7},
        {"high": 9, "low": 6},
        {"high": "10", "low": 7},   # invalid second swing
        {"high": 8, "low": 5},
    ]

    assert analyzer._find_equal_highs(candles) == []


def test_find_equal_lows_left_invalid_type():
    analyzer = LiquidityAnalyzer()

    candles = [
        {"high": 10, "low": 8},
        {"high": 9, "low": "5"},
        {"high": 10, "low": 7},
        {"high": 9, "low": 5},
        {"high": 10, "low": 8},
    ]

    assert analyzer._find_equal_lows(candles) == []


def test_find_equal_lows_right_invalid_type():
    analyzer = LiquidityAnalyzer()

    candles = [
        {"high": 10, "low": 8},
        {"high": 9, "low": 5},
        {"high": 10, "low": 7},
        {"high": 9, "low": "5"},
        {"high": 10, "low": 8},
    ]

    assert analyzer._find_equal_lows(candles) == []


def test_calculate_sweep_strength_skips_invalid_candle():
    analyzer = LiquidityAnalyzer()

    liquidity = {
        "level": 10,
        "type": analyzer.BUY_SIDE,
        "created_index": 0,
    }

    candles = [
        {"high": 8, "low": 5},
        {"high": "bad", "low": 6},
        {"high": 12, "low": 7},
    ]

    assert analyzer._calculate_sweep_strength(
        liquidity,
        candles,
    ) == 2.0


def test_find_equal_highs_left_none_branch():
    analyzer = LiquidityAnalyzer()

    candles = [{}] * 5

    with patch.object(analyzer, "_is_swing_high", return_value=True):
        with patch.object(
            analyzer,
            "_extract_candle_fields",
            return_value=None,
        ):
            assert analyzer._find_equal_highs(candles) == []


def test_find_equal_highs_right_none_branch():
    analyzer = LiquidityAnalyzer()

    candles = [{}] * 5

    with patch.object(analyzer, "_is_swing_high", return_value=True):
        with patch.object(
            analyzer,
            "_extract_candle_fields",
            side_effect=[(10, 5), None] + [None]*10,
        ):
            assert analyzer._find_equal_highs(candles) == []


def test_find_equal_lows_left_none_branch():
    analyzer = LiquidityAnalyzer()

    candles = [{}] * 5

    with patch.object(analyzer, "_is_swing_low", return_value=True):
        with patch.object(
            analyzer,
            "_extract_candle_fields",
            return_value=None,
        ):
            assert analyzer._find_equal_lows(candles) == []


def test_find_equal_lows_right_none_branch():
    analyzer = LiquidityAnalyzer()

    candles = [{}] * 5

    with patch.object(analyzer, "_is_swing_low", return_value=True):
        with patch.object(
            analyzer,
            "_extract_candle_fields",
            side_effect=[(10, 5), None] + [None]*10,
        ):
            assert analyzer._find_equal_lows(candles) == []


def test_calculate_sweep_strength_fields_none_branch():
    from unittest.mock import patch

    analyzer = LiquidityAnalyzer()

    liquidity = {
        "level": 10,
        "type": analyzer.BUY_SIDE,
        "created_index": 0,
    }

    candles = [
        {"high": 8, "low": 5},
        {"high": 9, "low": 6},
    ]

    with patch.object(
        analyzer,
        "_extract_candle_fields",
        side_effect=[None],
    ):
        assert analyzer._calculate_sweep_strength(
            liquidity,
            candles,
        ) == 0.0


def test_calculate_sweep_strength_continue_on_invalid_fields():
    analyzer = LiquidityAnalyzer()

    liquidity = {
        "level": 10.0,
        "type": analyzer.BUY_SIDE,
        "created_index": 0,
    }

    candles = [
        {"high": 10, "low": 8},      # created candle
        {"high": None, "low": 7},    # invalid -> should hit line 436
        {"high": 11, "low": 9},      # valid
    ]

    assert analyzer._extract_candle_fields(candles[1]) is None

    strength = analyzer._calculate_sweep_strength(
        liquidity,
        candles,
    )

    assert strength == 1.0
