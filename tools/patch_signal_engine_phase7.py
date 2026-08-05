"""
tools/patch_signal_engine_phase7.py

UDUAK QUANT SYSTEM
Phase 7 Automatic Repair

Repairs:

1. strategy_registry duplicate registration
2. signal_engine imports
3. signal_engine tests
"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


# ============================================================
# helper
# ============================================================

def replace_once(text: str, old: str, new: str):
    if old not in text:
        return text, False
    return text.replace(old, new, 1), True


# ============================================================
# Strategy Registry
# ============================================================

registry = ROOT / "core" / "strategy_registry.py"

if registry.exists():

    text = registry.read_text(encoding="utf-8")

    #
    # Restore duplicate protection
    #

    old = """        if strategy.name in self._strategies:
            return
"""

    new = """        if strategy.name in self._strategies:
            raise ValueError(
                f"Strategy '{strategy.name}' already exists."
            )
"""

    text, changed1 = replace_once(text, old, new)

    #
    # Make _register_defaults() idempotent
    #

    old = """        for strategy in defaults:
            self.register(strategy)
"""

    new = """        for strategy in defaults:

            if strategy.name not in self._strategies:
                self.register(strategy)
"""

    text, changed2 = replace_once(text, old, new)

    registry.write_text(text, encoding="utf-8")

    if changed1 or changed2:
        print("✓ Strategy registry repaired.")


# ============================================================
# Signal Engine
# ============================================================

engine = ROOT / "core" / "signal_engine.py"

if engine.exists():

    text = engine.read_text(encoding="utf-8")

    text = text.replace(
        "from core.signal_models import Signal",
        "from core.signal_models import Signal, SignalRequest, SignalResult",
    )

    engine.write_text(text, encoding="utf-8")

    print("✓ signal_engine imports updated")


# ============================================================
# Signal tests
# ============================================================

tests = ROOT / "tests" / "test_signal_engine.py"

if tests.exists():

    text = tests.read_text(encoding="utf-8")

    text = text.replace(
        "signal_signal_request",
        "signal_request",
    )

    text = text.replace(
        "signal_signal_result",
        "signal_result",
    )

    tests.write_text(text, encoding="utf-8")

    print("✓ signal_engine tests updated")


print()
print("============================================================")
print("Phase 7 automatic repair complete.")
print("============================================================")