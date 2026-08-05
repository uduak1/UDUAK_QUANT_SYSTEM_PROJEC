#!/usr/bin/env python3
"""
UDUAK QUANT SYSTEM

Patch AnalyzerRegistry
Option 1 Automation

Adds:

- execution timing
- failure tracking
- _execute_analyzer()

without duplicating patches.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TARGET = ROOT / "core" / "analyzer_registry.py"

text = TARGET.read_text(encoding="utf-8")

# ------------------------------------------------------
# imports
# ------------------------------------------------------

if "import time" not in text:

    text = text.replace(

        "from typing import Dict, List, Type",

        "from typing import Dict, List, Type\n"
        "import time\n"
        "import traceback"

    )

# ------------------------------------------------------
# runtime attributes
# ------------------------------------------------------

runtime_block = """

        self.last_execution_times: Dict[str, float] = {}

        self.last_failures: Dict[str, str] = {}

        self.last_results: Dict[str, AnalyzerResult] = {}
"""

if "self.last_execution_times" not in text:

    marker = """        self._enabled: Dict[str, bool] = {}
"""

    text = text.replace(
        marker,
        marker + runtime_block
    )

# ------------------------------------------------------
# helper
# ------------------------------------------------------

helper = '''

    # ------------------------------------------------------

    def _execute_analyzer(
        self,
        analyzer_name: str,
        analyzer: BaseAnalyzer,
        market_data,
    ) -> AnalyzerResult | None:
        """
        Execute one analyzer with timing and
        failure isolation.
        """

        start = time.perf_counter()

        try:

            result = analyzer.analyze(
                market_data,
            )

            elapsed = (
                time.perf_counter() - start
            ) * 1000.0

            self.last_execution_times[
                analyzer_name
            ] = elapsed

            if not isinstance(
                result,
                AnalyzerResult,
            ):
                raise TypeError(
                    f"{analyzer_name} did not return AnalyzerResult."
                )

            self.last_results[
                analyzer_name
            ] = result

            return result

        except Exception:

            elapsed = (
                time.perf_counter() - start
            ) * 1000.0

            self.last_execution_times[
                analyzer_name
            ] = elapsed

            self.last_failures[
                analyzer_name
            ] = traceback.format_exc()

            return None
'''

if "_execute_analyzer" not in text:

    marker = """

    # ------------------------------------------------------

    def execute(
"""

    text = text.replace(
        marker,
        helper + marker
    )

TARGET.write_text(
    text,
    encoding="utf-8",
)

print("=" * 60)
print("AnalyzerRegistry Option 1 patch applied.")
print(TARGET)
print("=" * 60)