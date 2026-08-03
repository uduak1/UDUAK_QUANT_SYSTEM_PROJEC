"""

UDUAK_QUANT_SYSTEM_PROJECT

File: tests/test_liquidity_detector.py

Tests for LiquidityDetector

"""

from analysis.liquidity_detector import LiquidityDetector

# ============================================================================
# EMPTY INPUT
# ============================================================================

def test_empty_swings():

    detector = LiquidityDetector()

    result = detector.detect([])

    assert result.success is False
    assert result.error == "EMPTY_SWINGS"

# ============================================================================
# INSUFFICIENT INPUT
# ============================================================================

def test_insufficient_swings():

    detector = LiquidityDetector()

    swings = [
        {
            "type": "SWING_HIGH",
            "price": 1.1050,
        }
    ]

    result = detector.detect(swings)

    assert result.success is False
    assert result.error == "INSUFFICIENT_SWINGS"

# ============================================================================
# BUY SIDE LIQUIDITY
# ============================================================================

def test_buy_side_liquidity():

    detector = LiquidityDetector()

    swings = [
        {
            "type": "SWING_HIGH",
            "price": 1.10500,
        },
        {
            "type": "SWING_HIGH",
            "price": 1.10505,
        },
    ]

    result = detector.detect(swings)

    assert result.success

    assert result.data["liquidity_found"] is True

    assert len(result.data["buy_side_liquidity"]) == 1

    assert len(result.data["equal_highs"]) == 1

    assert result.data["sell_side_count"] == 0

# ============================================================================
# SELL SIDE LIQUIDITY
# ============================================================================

def test_sell_side_liquidity():

    detector = LiquidityDetector()

    swings = [
        {
            "type": "SWING_LOW",
            "price": 1.10000,
        },
        {
            "type": "SWING_LOW",
            "price": 1.10007,
        },
    ]

    result = detector.detect(swings)

    assert result.success

    assert result.data["liquidity_found"] is True

    assert len(result.data["sell_side_liquidity"]) == 1

    assert len(result.data["equal_lows"]) == 1

    assert result.data["buy_side_count"] == 0

# ============================================================================
# NO LIQUIDITY
# ============================================================================

def test_no_liquidity():

    detector = LiquidityDetector()

    swings = [
        {
            "type": "SWING_HIGH",
            "price": 1.1100,
        },
        {
            "type": "SWING_LOW",
            "price": 1.0900,
        },
    ]

    result = detector.detect(swings)

    assert result.success

    assert result.data["liquidity_found"] is False

    assert result.data["buy_side_liquidity"] == []

    assert result.data["sell_side_liquidity"] == []

# ============================================================================
# DUPLICATE LEVELS REMOVED
# ============================================================================

def test_duplicate_liquidity_removed():

    detector = LiquidityDetector()

    swings = [
        {
            "type": "SWING_HIGH",
            "price": 1.10500,
        },
        {
            "type": "SWING_HIGH",
            "price": 1.10505,
        },
        {
            "type": "SWING_HIGH",
            "price": 1.10500,
        },
    ]

    result = detector.detect(swings)

    assert result.success

    assert len(result.data["buy_side_liquidity"]) == 1

    assert len(result.data["equal_highs"]) == 1

# ============================================================================
# RESPONSE KEYS
# ============================================================================

def test_response_keys():

    detector = LiquidityDetector()

    swings = [
        {
            "type": "SWING_HIGH",
            "price": 1.10500,
        },
        {
            "type": "SWING_HIGH",
            "price": 1.10505,
        },
    ]

    result = detector.detect(swings)

    assert "liquidity_found" in result.data

    assert "buy_side_liquidity" in result.data

    assert "sell_side_liquidity" in result.data

    assert "equal_highs" in result.data

    assert "equal_lows" in result.data

    assert "buy_side_count" in result.data

    assert "sell_side_count" in result.data

def test_skip_swing_with_missing_price():
    from analysis.liquidity_detector import LiquidityDetector

    detector = LiquidityDetector()

    swings = [
        {
            "type": "SWING_HIGH",
            "price": None,
        },
        {
            "type": "SWING_HIGH",
            "price": 1.1050,
        },
        {
            "type": "SWING_LOW",
            "price": 1.0950,
        },
    ]

    result = detector.detect(swings)

    assert result.success is True