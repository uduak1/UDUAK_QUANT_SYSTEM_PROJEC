"""
tools/fix_strategy_registry_duplicates.py

UDUAK QUANT SYSTEM

Repairs duplicated default strategy registration introduced
during Phase 7 migration.
"""

from pathlib import Path
import re

FILE = Path("core/strategy_registry.py")

text = FILE.read_text(encoding="utf-8")


# ----------------------------------------------------------
# 1. Remove accidental second _register_defaults() call
# ----------------------------------------------------------

text = re.sub(
    r"(self\._register_defaults\(\)\s*\n)\s*self\._register_defaults\(\)",
    r"\1",
    text,
)

# ----------------------------------------------------------
# 2. Make register idempotent for default loading
# ----------------------------------------------------------

old = """
        if strategy.name in self._strategies:
            raise ValueError(
                f"Strategy '{strategy.name}' already exists."
            )

        self._strategies[strategy.name] = strategy
"""

new = """
        if strategy.name in self._strategies:
            return

        self._strategies[strategy.name] = strategy
"""

text = text.replace(old, new)

FILE.write_text(text, encoding="utf-8")

print("✓ Strategy registry duplicate registration repaired.")