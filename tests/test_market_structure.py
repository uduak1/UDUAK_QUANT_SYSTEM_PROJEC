"""
===============================================================================
UDUAK_QUANT_SYSTEM_PROJECT
-------------------------------------------------------------------------------
File: tests/test_market_structure.py
===============================================================================
"""

from analysis.market_structure import MarketStructure


# ============================================================================
# EMPTY INPUT
# ============================================================================

def test_empty_swings():

    analyzer = MarketStructure()

    result = analyzer.analyze([])

    assert result.success is False

    assert result.error == "EMPTY_SWINGS"


# ============================================================================
# ONE SWING
# ============================================================================

def test_insufficient_swings():

    analyzer = MarketStructure()

    swings = [

        {
            "type": "SWING_HIGH",
            "price": 1.1000,
            "time": 1,
            "index": 0,
        }

    ]

    result = analyzer.analyze(swings)

    assert result.success is False

    assert result.error == "INSUFFICIENT_SWINGS"


# ============================================================================
# UPTREND
# ============================================================================

def test_uptrend():

    analyzer = MarketStructure()

    swings = [

        {
            "type": "SWING_HIGH",
            "price": 1.1000,
            "time": 1,
            "index": 0,
        },

        {
            "type": "SWING_LOW",
            "price": 1.0900,
            "time": 2,
            "index": 1,
        },

        {
            "type": "SWING_HIGH",
            "price": 1.1100,
            "time": 3,
            "index": 2,
        },

        {
            "type": "SWING_LOW",
            "price": 1.0950,
            "time": 4,
            "index": 3,
        },

        {
            "type": "SWING_HIGH",
            "price": 1.1200,
            "time": 5,
            "index": 4,
        },

        {
            "type": "SWING_LOW",
            "price": 1.1000,
            "time": 6,
            "index": 5,
        },

    ]

    result = analyzer.analyze(swings)

    assert result.success

    assert result.data["trend"] == "UPTREND"


# ============================================================================
# DOWNTREND
# ============================================================================

def test_downtrend():

    analyzer = MarketStructure()

    swings = [

        {
            "type": "SWING_HIGH",
            "price": 1.1200,
            "time": 1,
            "index": 0,
        },

        {
            "type": "SWING_LOW",
            "price": 1.1100,
            "time": 2,
            "index": 1,
        },

        {
            "type": "SWING_HIGH",
            "price": 1.1150,
            "time": 3,
            "index": 2,
        },

        {
            "type": "SWING_LOW",
            "price": 1.1000,
            "time": 4,
            "index": 3,
        },

        {
            "type": "SWING_HIGH",
            "price": 1.1100,
            "time": 5,
            "index": 4,
        },

        {
            "type": "SWING_LOW",
            "price": 1.0900,
            "time": 6,
            "index": 5,
        },

    ]

    result = analyzer.analyze(swings)

    assert result.success

    assert result.data["trend"] == "DOWNTREND"


# ============================================================================
# RANGE
# ============================================================================

def test_range():

    analyzer = MarketStructure()

    swings = [

        {
            "type": "SWING_HIGH",
            "price": 1.1000,
            "time": 1,
            "index": 0,
        },

        {
            "type": "SWING_LOW",
            "price": 1.0900,
            "time": 2,
            "index": 1,
        },

        {
            "type": "SWING_HIGH",
            "price": 1.1000,
            "time": 3,
            "index": 2,
        },

        {
            "type": "SWING_LOW",
            "price": 1.0900,
            "time": 4,
            "index": 3,
        },

        {
            "type": "SWING_HIGH",
            "price": 1.1000,
            "time": 5,
            "index": 4,
        },

        {
            "type": "SWING_LOW",
            "price": 1.0900,
            "time": 6,
            "index": 5,
        },

    ]

    result = analyzer.analyze(swings)

    assert result.success

    assert result.data["trend"] == "RANGE"


# ============================================================================
# TRANSITION
# ============================================================================

def test_transition():

    analyzer = MarketStructure()

    swings = [

        {
            "type": "SWING_HIGH",
            "price": 1.1000,
            "time": 1,
            "index": 0,
        },

        {
            "type": "SWING_LOW",
            "price": 1.0900,
            "time": 2,
            "index": 1,
        },

        {
            "type": "SWING_HIGH",
            "price": 1.1100,
            "time": 3,
            "index": 2,
        },

        {
            "type": "SWING_LOW",
            "price": 1.0800,
            "time": 4,
            "index": 3,
        },

    ]

    result = analyzer.analyze(swings)

    assert result.success

    assert result.data["trend"] == "TRANSITION"


# ============================================================================
# STATISTICS
# ============================================================================

def test_statistics():

    analyzer = MarketStructure()

    swings = [

        {
            "type": "SWING_HIGH",
            "price": 1.1000,
            "time": 1,
            "index": 0,
        },

        {
            "type": "SWING_LOW",
            "price": 1.0900,
            "time": 2,
            "index": 1,
        },

        {
            "type": "SWING_HIGH",
            "price": 1.1100,
            "time": 3,
            "index": 2,
        },

        {
            "type": "SWING_LOW",
            "price": 1.0950,
            "time": 4,
            "index": 3,
        },

    ]

    result = analyzer.analyze(swings)

    stats = result.data["statistics"]

    assert stats["higher_highs"] == 1

    assert stats["higher_lows"] == 1

    assert stats["lower_highs"] == 0

    assert stats["lower_lows"] == 0

    assert stats["total_swings"] == 4