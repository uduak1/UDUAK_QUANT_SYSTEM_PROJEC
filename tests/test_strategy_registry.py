"""
tests/test_strategy_registry.py

Unit tests for:

core/strategy_registry.py
"""

from core.strategy_registry import (
    StrategyRegistry,
    StrategyDefinition,
)


# ==========================================================
# REGISTRY CREATION
# ==========================================================

def test_registry_creation():

    registry = StrategyRegistry(load_defaults=False)

    assert registry is not None


# ==========================================================
# REGISTER STRATEGY
# ==========================================================

def test_register_strategy():

    registry = StrategyRegistry(load_defaults=False)

    strategy = StrategyDefinition(
        name="LiquiditySweepReversal",
        description="Institutional liquidity reversal",
    )

    registry.register(strategy)

    assert registry.exists("LiquiditySweepReversal")


# ==========================================================
# DUPLICATE REGISTRATION
# ==========================================================

def test_duplicate_registration():

    registry = StrategyRegistry(load_defaults=False)

    strategy = StrategyDefinition(
        name="LiquiditySweepReversal",
        description="Institutional liquidity reversal",
    )

    registry.register(strategy)

    try:

        registry.register(strategy)

        assert False

    except ValueError:

        assert True


# ==========================================================
# GET STRATEGY
# ==========================================================

def test_get_strategy():

    registry = StrategyRegistry(load_defaults=False)

    strategy = StrategyDefinition(
        name="BOSContinuation",
        description="Break of Structure continuation",
    )

    registry.register(strategy)

    result = registry.get("BOSContinuation")

    assert result.name == "BOSContinuation"


# ==========================================================
# ENABLE / DISABLE
# ==========================================================

def test_disable_strategy():

    registry = StrategyRegistry(load_defaults=False)

    strategy = StrategyDefinition(
        name="CHOCHReversal",
        description="CHOCH reversal",
    )

    registry.register(strategy)

    registry.disable("CHOCHReversal")

    assert registry.get("CHOCHReversal").enabled is False


def test_enable_strategy():

    registry = StrategyRegistry(load_defaults=False)

    strategy = StrategyDefinition(
        name="CHOCHReversal",
        description="CHOCH reversal",
        enabled=False,
    )

    registry.register(strategy)

    registry.enable("CHOCHReversal")

    assert registry.get("CHOCHReversal").enabled is True


# ==========================================================
# REMOVE
# ==========================================================

def test_remove_strategy():

    registry = StrategyRegistry(load_defaults=False)

    strategy = StrategyDefinition(
        name="TrendContinuation",
        description="Trend continuation",
    )

    registry.register(strategy)

    registry.remove("TrendContinuation")

    assert registry.exists("TrendContinuation") is False


# ==========================================================
# LIST ALL
# ==========================================================

def test_list_all():

    registry = StrategyRegistry(load_defaults=False)

    registry.register(
        StrategyDefinition(
            "A",
            "A",
        )
    )

    registry.register(
        StrategyDefinition(
            "B",
            "B",
        )
    )

    assert len(registry.list_all()) == 2


# ==========================================================
# LIST ENABLED
# ==========================================================

def test_list_enabled():

    registry = StrategyRegistry(load_defaults=False)

    registry.register(
        StrategyDefinition(
            "Enabled",
            "Enabled",
            enabled=True,
        )
    )

    registry.register(
        StrategyDefinition(
            "Disabled",
            "Disabled",
            enabled=False,
        )
    )

    enabled = registry.list_enabled()

    assert len(enabled) == 1

    assert enabled[0].name == "Enabled"
    # ==========================================================
# NON-EXISTENT STRATEGIES
# ==========================================================

def test_disable_missing_strategy():

    registry = StrategyRegistry(load_defaults=False)

    assert registry.disable("UnknownStrategy") is False


def test_enable_missing_strategy():

    registry = StrategyRegistry(load_defaults=False)

    assert registry.enable("UnknownStrategy") is False


def test_remove_missing_strategy():

    registry = StrategyRegistry(load_defaults=False)

    assert registry.remove("UnknownStrategy") is False