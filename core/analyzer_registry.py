"""
core/analyzer_registry.py

==========================================================
UDUAK QUANT SYSTEM

Institutional Analyzer Registry

Responsibilities

    • Register analyzers
    • Remove analyzers
    • Enable / Disable analyzers
    • Retrieve analyzers
    • Execute analyzers
    • Validate analyzer type
    • Isolate analyzer failures
    • Record execution timing

Every registered analyzer MUST inherit BaseAnalyzer.
==========================================================
"""

from __future__ import annotations

import logging
import time
import traceback

from typing import Dict
from typing import List

from core.base_analyzer import BaseAnalyzer
from core.analyzer_result import AnalyzerResult


logger = logging.getLogger(__name__)


class AnalyzerRegistry:
    """
    Registry for all analyzers.
    """

    def __init__(self):

        self._analyzers: Dict[str, BaseAnalyzer] = {}

        self._enabled: Dict[str, bool] = {}


        self.last_execution_times: Dict[str, float] = {}

        self.last_failures: Dict[str, str] = {}

        self.last_results: Dict[str, AnalyzerResult] = {}

    # ------------------------------------------------------

    def register(
        self,
        analyzer: BaseAnalyzer,
    ) -> None:
        """
        Register an analyzer instance.
        """

        if not isinstance(analyzer, BaseAnalyzer):
            raise TypeError(
                "Analyzer must inherit BaseAnalyzer."
            )

        name = analyzer.name

        if name in self._analyzers:
            raise ValueError(
                f"Analyzer '{name}' already registered."
            )

        self._analyzers[name] = analyzer
        self._enabled[name] = True

    # ------------------------------------------------------

    def remove(
        self,
        analyzer_name: str,
    ) -> None:

        self._analyzers.pop(analyzer_name, None)
        self._enabled.pop(analyzer_name, None)

        self.last_execution_times.pop(analyzer_name, None)
        self.last_failures.pop(analyzer_name, None)

    # ------------------------------------------------------

    def enable(
        self,
        analyzer_name: str,
    ) -> None:

        if analyzer_name not in self._enabled:
            raise KeyError(analyzer_name)

        self._enabled[analyzer_name] = True

    # ------------------------------------------------------

    def disable(
        self,
        analyzer_name: str,
    ) -> None:

        if analyzer_name not in self._enabled:
            raise KeyError(analyzer_name)

        self._enabled[analyzer_name] = False

    # ------------------------------------------------------

    def is_enabled(
        self,
        analyzer_name: str,
    ) -> bool:

        return self._enabled.get(
            analyzer_name,
            False,
        )

    # ------------------------------------------------------

    def get(
        self,
        analyzer_name: str,
    ) -> BaseAnalyzer:

        if analyzer_name not in self._analyzers:
            raise KeyError(analyzer_name)

        return self._analyzers[analyzer_name]

    # ------------------------------------------------------

    def list_all(
        self,
    ) -> List[str]:

        return sorted(self._analyzers.keys())

    # ------------------------------------------------------

    def list_enabled(
        self,
    ) -> List[str]:

        return sorted(
            name
            for name, enabled in self._enabled.items()
            if enabled
        )

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


    # ------------------------------------------------------

    
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

    # ------------------------------------------------------

    def execution_time(
        self,
        analyzer_name: str,
    ) -> float:

        return self.last_execution_times.get(
            analyzer_name,
            0.0,
        )

    # ------------------------------------------------------

    def execution_times(
        self,
    ) -> Dict[str, float]:

        return dict(
            self.last_execution_times,
        )

    # ------------------------------------------------------

    def failed_analyzers(
        self,
    ) -> Dict[str, str]:

        return dict(
            self.last_failures,
        )

    # ------------------------------------------------------

    def clear(
        self,
    ) -> None:

        self._analyzers.clear()
        self._enabled.clear()
        self.last_execution_times.clear()
        self.last_failures.clear()

    # ------------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return len(self._analyzers)

    # ------------------------------------------------------

    def __contains__(
        self,
        analyzer_name: str,
    ) -> bool:

        return analyzer_name in self._analyzers