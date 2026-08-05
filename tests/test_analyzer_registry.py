"""
tests/test_analyzer_registry.py
"""

import pytest

from core.analyzer_registry import AnalyzerRegistry
from core.base_analyzer import BaseAnalyzer
from core.analyzer_result import AnalyzerResult


class GoodAnalyzer(BaseAnalyzer):
    def __init__(self, name="good"):
        super().__init__(name=name)

    def validate(self, market_snapshot):
        return True

    def analyze(self, market_snapshot):
        return AnalyzerResult.success_result(
            analyzer=self.name,
            confidence=90.0,
            data={"value": 1},
        )


class BadAnalyzer(BaseAnalyzer):
    def __init__(self, name="bad"):
        super().__init__(name=name)

    def validate(self, market_snapshot):
        return True

    def analyze(self, market_snapshot):
        raise RuntimeError("boom")


class WrongReturnAnalyzer(BaseAnalyzer):
    def __init__(self, name="wrong"):
        super().__init__(name=name)

    def validate(self, market_snapshot):
        return True

    def analyze(self, market_snapshot):
        return {"not": "AnalyzerResult"}


class Dummy:
    pass


def test_registry_creation():
    registry = AnalyzerRegistry()

    assert len(registry) == 0
    assert registry.list_all() == []
    assert registry.list_enabled() == []
    assert registry.execution_times() == {}
    assert registry.failed_analyzers() == {}


def test_register():
    registry = AnalyzerRegistry()

    analyzer = GoodAnalyzer()

    registry.register(analyzer)

    assert len(registry) == 1
    assert "good" in registry
    assert registry.get("good") is analyzer


def test_duplicate_registration():
    registry = AnalyzerRegistry()

    registry.register(GoodAnalyzer())

    with pytest.raises(ValueError):
        registry.register(GoodAnalyzer())


def test_register_invalid_type():
    registry = AnalyzerRegistry()

    with pytest.raises(TypeError):
        registry.register(Dummy())


def test_remove():
    registry = AnalyzerRegistry()

    registry.register(GoodAnalyzer())

    registry.remove("good")

    assert len(registry) == 0
    assert "good" not in registry


def test_enable_disable():
    registry = AnalyzerRegistry()

    registry.register(GoodAnalyzer())

    assert registry.is_enabled("good") is True

    registry.disable("good")

    assert registry.is_enabled("good") is False

    registry.enable("good")

    assert registry.is_enabled("good") is True


def test_enable_missing():
    registry = AnalyzerRegistry()

    with pytest.raises(KeyError):
        registry.enable("missing")


def test_disable_missing():
    registry = AnalyzerRegistry()

    with pytest.raises(KeyError):
        registry.disable("missing")


def test_get_missing():
    registry = AnalyzerRegistry()

    with pytest.raises(KeyError):
        registry.get("missing")


def test_list_enabled():
    registry = AnalyzerRegistry()

    registry.register(GoodAnalyzer("a"))
    registry.register(GoodAnalyzer("b"))

    registry.disable("b")

    assert registry.list_enabled() == ["a"]


def test_execute_success():
    registry = AnalyzerRegistry()

    registry.register(GoodAnalyzer())

    results = registry.execute({})

    assert "good" in results
    assert isinstance(results["good"], AnalyzerResult)

    assert registry.execution_time("good") >= 0

    assert registry.failed_analyzers() == {}

    assert registry.last_results["good"].success is True


def test_execute_failure():
    registry = AnalyzerRegistry()

    registry.register(BadAnalyzer())

    results = registry.execute({})

    assert results == {}

    failures = registry.failed_analyzers()

    assert "bad" in failures

    assert "RuntimeError" in failures["bad"]

    assert registry.execution_time("bad") >= 0


def test_execute_invalid_return():
    registry = AnalyzerRegistry()

    registry.register(WrongReturnAnalyzer())

    results = registry.execute({})

    assert results == {}

    failures = registry.failed_analyzers()

    assert "wrong" in failures

    assert "AnalyzerResult" in failures["wrong"]


def test_execute_disabled():
    registry = AnalyzerRegistry()

    registry.register(GoodAnalyzer())

    registry.disable("good")

    results = registry.execute({})

    assert results == {}

    assert registry.execution_times() == {}
    assert registry.failed_analyzers() == {}


def test_execution_time_unknown():
    registry = AnalyzerRegistry()

    assert registry.execution_time("missing") == 0.0


def test_clear():
    registry = AnalyzerRegistry()

    registry.register(GoodAnalyzer())

    registry.execute({})

    registry.clear()

    assert len(registry) == 0
    assert registry.list_all() == []
    assert registry.list_enabled() == []
    assert registry.execution_times() == {}
    assert registry.failed_analyzers() == {}


def test_contains():
    registry = AnalyzerRegistry()

    registry.register(GoodAnalyzer())

    assert "good" in registry
    assert "missing" not in registry


def test_remove_missing():
    registry = AnalyzerRegistry()

    registry.remove("missing")

    assert len(registry) == 0


def test_execution_times_copy():
    registry = AnalyzerRegistry()

    registry.register(GoodAnalyzer())

    registry.execute({})

    times = registry.execution_times()

    times["good"] = -1

    assert registry.execution_time("good") >= 0


def test_failed_analyzers_copy():
    registry = AnalyzerRegistry()

    registry.register(BadAnalyzer())

    registry.execute({})

    failures = registry.failed_analyzers()

    failures.clear()

    assert "bad" in registry.failed_analyzers()