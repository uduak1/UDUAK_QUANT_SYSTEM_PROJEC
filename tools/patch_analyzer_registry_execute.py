#!/usr/bin/env python3
"""
UDUAK QUANT SYSTEM

Patch AnalyzerRegistry.execute()

Rewrites execute() to use the automated
execution helper.

Idempotent:
Running multiple times produces the same result.
"""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

TARGET = ROOT / "core" / "analyzer_registry.py"

text = TARGET.read_text(encoding="utf-8")

new_execute = '''
    def execute(
        self,
        market_data,
    ) -> Dict[str, AnalyzerResult]:
        """
        Execute every enabled analyzer.

        Returns
        -------
        Dictionary containing successful analyzer results.
        """

        self.last_execution_times.clear()
        self.last_failures.clear()
        self.last_results.clear()

        results: Dict[str, AnalyzerResult] = {}

        for name in self.list_enabled():

            analyzer = self._analyzers[name]

            result = self._execute_analyzer(
                analyzer_name=name,
                analyzer=analyzer,
                market_data=market_data,
            )

            if result is None:
                continue

            results[name] = result

        return results
'''

pattern = (
    r"def execute\(\s*"
    r"self,\s*"
    r"market_data,\s*"
    r"\)\s*->\s*Dict\[str,\s*AnalyzerResult\]:"
    r".*?"
    r"(?=\n\s*# ------------------------------------------------------|\n\s*def |\Z)"
)

replacement = new_execute.rstrip()

updated, count = re.subn(
    pattern,
    replacement,
    text,
    flags=re.DOTALL,
)

if count == 0:
    print("=" * 60)
    print("ERROR")
    print("Could not locate execute() method.")
    print("No changes made.")
    print("=" * 60)
    raise SystemExit(1)

TARGET.write_text(
    updated,
    encoding="utf-8",
)

print("=" * 60)
print("AnalyzerRegistry.execute() patched successfully.")
print(TARGET)
print("=" * 60)