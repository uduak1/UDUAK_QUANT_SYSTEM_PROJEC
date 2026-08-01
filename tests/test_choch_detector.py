"""
===============================================================================
UDUAK_QUANT_SYSTEM_PROJECT
-------------------------------------------------------------------------------
File: tests/test_choch_detector.py
===============================================================================
"""

from analysis.choch_detector import CHOCHDetector


# ============================================================================
# EMPTY STRUCTURE
# ============================================================================

def test_empty_structure():

    detector = CHOCHDetector()

    result = detector.detect([])

    assert result.success is False
    assert result.error == "EMPTY_STRUCTURE"


# ============================================================================
# INSUFFICIENT STRUCTURE
# ============================================================================

def test_insufficient_structure():

    detector = CHOCHDetector()

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
# BULLISH CHOCH
# ============================================================================

def test_bullish_choch():

    detector = CHOCHDetector()

    structure = [
        {
            "structure": "LOWER_HIGH",
            "price": 1.1200,
        },
        {
            "structure": "LOWER_LOW",
            "price": 1.1100,
        },
        {
            "structure": "HIGHER_LOW",
            "price": 1.1150,
        },
        {
            "structure": "HIGHER_HIGH",
            "price": 1.1250,
        },
    ]

    result = detector.detect(structure)

    assert result.success
    assert result.data["choch"] is True
    assert result.data["direction"] == "BULLISH"
    assert result.data["bullish_choch"] is True
    assert result.data["bearish_choch"] is False
    assert result.data["broken_level"] == 1.1250


# ============================================================================
# BEARISH CHOCH
# ============================================================================

def test_bearish_choch():

    detector = CHOCHDetector()

    structure = [
        {
            "structure": "HIGHER_LOW",
            "price": 1.1000,
        },
        {
            "structure": "HIGHER_HIGH",
            "price": 1.1100,
        },
        {
            "structure": "LOWER_HIGH",
            "price": 1.1050,
        },
        {
            "structure": "LOWER_LOW",
            "price": 1.0950,
        },
    ]

    result = detector.detect(structure)

    assert result.success
    assert result.data["choch"] is True
    assert result.data["direction"] == "BEARISH"
    assert result.data["bullish_choch"] is False
    assert result.data["bearish_choch"] is True
    assert result.data["broken_level"] == 1.0950


# ============================================================================
# NO CHOCH
# ============================================================================

def test_no_choch():

    detector = CHOCHDetector()

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

    assert result.success
    assert result.data["choch"] is False
    assert result.data["direction"] == "NONE"
    assert result.data["broken_level"] is None


# ============================================================================
# RESPONSE KEYS
# ============================================================================

def test_response_keys():

    detector = CHOCHDetector()

    structure = [
        {
            "structure": "LOWER_HIGH",
            "price": 1.1200,
        },
        {
            "structure": "LOWER_LOW",
            "price": 1.1100,
        },
        {
            "structure": "HIGHER_LOW",
            "price": 1.1150,
        },
        {
            "structure": "HIGHER_HIGH",
            "price": 1.1250,
        },
    ]

    result = detector.detect(structure)

    assert "choch" in result.data
    assert "direction" in result.data
    assert "broken_level" in result.data
    assert "bullish_choch" in result.data
    assert "bearish_choch" in result.data