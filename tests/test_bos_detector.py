"""
===============================================================================
UDUAK_QUANT_SYSTEM_PROJECT
-------------------------------------------------------------------------------
File: tests/test_bos_detector.py
===============================================================================
"""

from analysis.bos_detector import BOSDetector


# ============================================================================
# EMPTY STRUCTURE
# ============================================================================

def test_empty_structure():

    detector = BOSDetector()

    result = detector.detect([])

    assert result.success is False

    assert result.error == "EMPTY_STRUCTURE"


# ============================================================================
# INSUFFICIENT STRUCTURE
# ============================================================================

def test_insufficient_structure():

    detector = BOSDetector()

    structure = [

        {
            "structure": "HIGHER_HIGH",
            "price": 1.1000,
        },

        {
            "structure": "HIGHER_LOW",
            "price": 1.0950,
        },

    ]

    result = detector.detect(structure)

    assert result.success is False

    assert result.error == "INSUFFICIENT_STRUCTURE"


# ============================================================================
# BULLISH BOS
# ============================================================================

def test_bullish_bos():

    detector = BOSDetector()

    structure = [

        {
            "structure": "INITIAL_HIGH",
            "price": 1.1000,
        },

        {
            "structure": "INITIAL_LOW",
            "price": 1.0900,
        },

        {
            "structure": "HIGHER_HIGH",
            "price": 1.1100,
        },

        {
            "structure": "HIGHER_LOW",
            "price": 1.1000,
        },

    ]

    result = detector.detect(structure)

    assert result.success

    assert result.data["bos"] is True

    assert result.data["direction"] == "BULLISH"

    assert result.data["bullish_bos"] is True

    assert result.data["bearish_bos"] is False

    assert result.data["broken_level"] == 1.1100


# ============================================================================
# BEARISH BOS
# ============================================================================

def test_bearish_bos():

    detector = BOSDetector()

    structure = [

        {
            "structure": "INITIAL_HIGH",
            "price": 1.1200,
        },

        {
            "structure": "INITIAL_LOW",
            "price": 1.1100,
        },

        {
            "structure": "LOWER_HIGH",
            "price": 1.1150,
        },

        {
            "structure": "LOWER_LOW",
            "price": 1.1000,
        },

    ]

    result = detector.detect(structure)

    assert result.success

    assert result.data["bos"] is True

    assert result.data["direction"] == "BEARISH"

    assert result.data["bullish_bos"] is False

    assert result.data["bearish_bos"] is True

    assert result.data["broken_level"] == 1.1000


# ============================================================================
# NO BOS
# ============================================================================

def test_no_bos():

    detector = BOSDetector()

    structure = [

        {
            "structure": "INITIAL_HIGH",
            "price": 1.1000,
        },

        {
            "structure": "INITIAL_LOW",
            "price": 1.0900,
        },

        {
            "structure": "EQUAL_HIGH",
            "price": 1.1000,
        },

        {
            "structure": "EQUAL_LOW",
            "price": 1.0900,
        },

    ]

    result = detector.detect(structure)

    assert result.success

    assert result.data["bos"] is False

    assert result.data["direction"] == "NONE"

    assert result.data["broken_level"] is None


# ============================================================================
# RESPONSE KEYS
# ============================================================================

def test_response_keys():

    detector = BOSDetector()

    structure = [

        {
            "structure": "HIGHER_HIGH",
            "price": 1.1000,
        },

        {
            "structure": "HIGHER_LOW",
            "price": 1.0950,
        },

        {
            "structure": "HIGHER_HIGH",
            "price": 1.1050,
        },

        {
            "structure": "HIGHER_LOW",
            "price": 1.1000,
        },

    ]

    result = detector.detect(structure)

    assert "bos" in result.data

    assert "direction" in result.data

    assert "broken_level" in result.data

    assert "bullish_bos" in result.data

    assert "bearish_bos" in result.data