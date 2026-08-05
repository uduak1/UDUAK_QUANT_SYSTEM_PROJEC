"""
tests/test_base_analyzer.py

Unit tests for core/base_analyzer.py
"""

import pytest

from core.base_analyzer import BaseAnalyzer


class DummyAnalyzer(BaseAnalyzer):
    """Concrete implementation for testing."""

    def __init__(
        self,
        name="Dummy",
        version="1.2.3",
        enabled=True,
    ):
        super().__init__(
            name=name,
            version=version,
            enabled=enabled,
        )

    def validate(self, market_snapshot):
        return True

    def analyze(self, market_snapshot):
        return {"signal": "BUY"}


# ==========================================================
# CONSTRUCTION
# ==========================================================


def test_constructor_defaults():
    analyzer = DummyAnalyzer()

    assert analyzer.name == "Dummy"
    assert analyzer.version == "1.2.3"
    assert analyzer.enabled is True


def test_constructor_custom():
    analyzer = DummyAnalyzer(
        name="Liquidity",
        version="2.0",
        enabled=False,
    )

    assert analyzer.name == "Liquidity"
    assert analyzer.version == "2.0"
    assert analyzer.enabled is False


# ==========================================================
# PROPERTIES
# ==========================================================


def test_name_property():
    analyzer = DummyAnalyzer(name="FVG")

    assert analyzer.name == "FVG"


def test_version_property():
    analyzer = DummyAnalyzer(version="9.1")

    assert analyzer.version == "9.1"


def test_enabled_property():
    analyzer = DummyAnalyzer(enabled=False)

    assert analyzer.enabled is False


# ==========================================================
# ENABLE / DISABLE
# ==========================================================


def test_enable():
    analyzer = DummyAnalyzer(enabled=False)

    analyzer.enable()

    assert analyzer.enabled is True


def test_disable():
    analyzer = DummyAnalyzer(enabled=True)

    analyzer.disable()

    assert analyzer.enabled is False


# ==========================================================
# INITIALIZATION
# ==========================================================


def test_initialize():
    analyzer = DummyAnalyzer()

    assert analyzer.initialize() is True


# ==========================================================
# HEALTH
# ==========================================================


def test_health_check():
    analyzer = DummyAnalyzer()

    assert analyzer.health_check() is True


# ==========================================================
# REQUIRED METHODS
# ==========================================================


def test_validate():
    analyzer = DummyAnalyzer()

    assert analyzer.validate({}) is True


def test_analyze():
    analyzer = DummyAnalyzer()

    result = analyzer.analyze({})

    assert result == {"signal": "BUY"}


# ==========================================================
# METADATA
# ==========================================================


def test_metadata():
    analyzer = DummyAnalyzer(
        name="CHOCH",
        version="5.0",
        enabled=False,
    )

    metadata = analyzer.metadata()

    assert metadata == {
        "name": "CHOCH",
        "version": "5.0",
        "enabled": False,
    }


# ==========================================================
# REPRESENTATION
# ==========================================================


def test_repr():
    analyzer = DummyAnalyzer(
        name="Liquidity",
        version="3.1",
        enabled=True,
    )

    text = repr(analyzer)

    assert "DummyAnalyzer" in text
    assert "Liquidity" in text
    assert "3.1" in text
    assert "enabled=True" in text


# ==========================================================
# ABSTRACT CLASS
# ==========================================================


def test_base_analyzer_cannot_be_instantiated():
    with pytest.raises(TypeError):
        BaseAnalyzer(
            name="Base",
            version="1.0",
        )