"""
tests/test_analyzer_result.py
"""

from datetime import datetime

from core.analyzer_result import AnalyzerResult


# ==========================================================
# Construction
# ==========================================================

def test_creation():

    result = AnalyzerResult(
        analyzer="FVG",
        success=True,
    )

    assert result.analyzer == "FVG"
    assert result.success is True
    assert result.confidence == 0.0
    assert result.data == {}
    assert result.warnings == []
    assert result.errors == []
    assert result.metadata == {}
    assert result.execution_time_ms == 0.0
    assert isinstance(result.timestamp, datetime)


# ==========================================================
# Confidence clamp
# ==========================================================

def test_confidence_lower_bound():

    result = AnalyzerResult(
        analyzer="A",
        success=True,
        confidence=-25,
    )

    assert result.confidence == 0.0


def test_confidence_upper_bound():

    result = AnalyzerResult(
        analyzer="A",
        success=True,
        confidence=150,
    )

    assert result.confidence == 100.0


def test_confidence_normal():

    result = AnalyzerResult(
        analyzer="A",
        success=True,
        confidence=82.5,
    )

    assert result.confidence == 82.5


# ==========================================================
# Error / warning properties
# ==========================================================

def test_has_errors_false():

    result = AnalyzerResult(
        analyzer="A",
        success=True,
    )

    assert result.has_errors is False


def test_has_errors_true():

    result = AnalyzerResult(
        analyzer="A",
        success=True,
    )

    result.add_error("failure")

    assert result.has_errors is True


def test_has_warnings_false():

    result = AnalyzerResult(
        analyzer="A",
        success=True,
    )

    assert result.has_warnings is False


def test_has_warnings_true():

    result = AnalyzerResult(
        analyzer="A",
        success=True,
    )

    result.add_warning("warning")

    assert result.has_warnings is True


# ==========================================================
# is_valid
# ==========================================================

def test_is_valid_success():

    result = AnalyzerResult(
        analyzer="A",
        success=True,
    )

    assert result.is_valid is True


def test_is_valid_failure():

    result = AnalyzerResult(
        analyzer="A",
        success=False,
    )

    assert result.is_valid is False


def test_is_valid_error_present():

    result = AnalyzerResult(
        analyzer="A",
        success=True,
    )

    result.add_error("boom")

    assert result.is_valid is False


# ==========================================================
# Helpers
# ==========================================================

def test_add_warning():

    result = AnalyzerResult(
        analyzer="A",
        success=True,
    )

    result.add_warning("warning")

    assert result.warnings == ["warning"]


def test_add_error():

    result = AnalyzerResult(
        analyzer="A",
        success=True,
    )

    result.add_error("error")

    assert result.errors == ["error"]


def test_add_metadata():

    result = AnalyzerResult(
        analyzer="A",
        success=True,
    )

    result.add_metadata("tf", "M15")

    assert result.metadata["tf"] == "M15"


# ==========================================================
# Serialization
# ==========================================================

def test_to_dict():

    result = AnalyzerResult(
        analyzer="Liquidity",
        success=True,
        confidence=88,
        data={"level": 1},
        execution_time_ms=2.5,
    )

    result.add_warning("warn")
    result.add_metadata("symbol", "EURUSD")

    d = result.to_dict()

    assert d["analyzer"] == "Liquidity"
    assert d["success"] is True
    assert d["confidence"] == 88
    assert d["data"] == {"level": 1}
    assert d["warnings"] == ["warn"]
    assert d["errors"] == []
    assert d["metadata"]["symbol"] == "EURUSD"
    assert d["execution_time_ms"] == 2.5
    assert isinstance(d["timestamp"], str)


# ==========================================================
# Factory methods
# ==========================================================

def test_success_result():

    result = AnalyzerResult.success_result(
        analyzer="FVG",
        confidence=91,
        data={"gap": 12},
        execution_time_ms=7.5,
    )

    assert result.success is True
    assert result.analyzer == "FVG"
    assert result.confidence == 91
    assert result.data["gap"] == 12
    assert result.execution_time_ms == 7.5
    assert result.errors == []


def test_failure_result():

    result = AnalyzerResult.failure_result(
        analyzer="Liquidity",
        error="Analyzer crashed",
        execution_time_ms=4.2,
    )

    assert result.success is False
    assert result.confidence == 0.0
    assert result.execution_time_ms == 4.2
    assert result.errors == ["Analyzer crashed"]


# ==========================================================
# __repr__
# ==========================================================

def test_repr():

    result = AnalyzerResult(
        analyzer="FVG",
        success=True,
        confidence=81.5,
    )

    text = repr(result)

    assert "AnalyzerResult" in text
    assert "FVG" in text
    assert "81.5" in text


def test_repr_with_error():

    result = AnalyzerResult(
        analyzer="Liquidity",
        success=False,
    )

    result.add_error("bad")

    text = repr(result)

    assert "errors=1" in text