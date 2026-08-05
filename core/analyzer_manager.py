"""
core/analyzer_manager.py

==========================================================
UDUAK QUANT SYSTEM

Institutional Analyzer Manager

Responsibilities

    • Own Analyzer Registry
    • Register analyzers
    • Register multiple analyzers
    • Execute all enabled analyzers
    • Build institutional execution snapshot
    • Store latest snapshot

The manager NEVER performs analysis.

It orchestrates analyzers.
==========================================================
"""

from __future__ import annotations

from datetime import datetime
from typing import Dict, List

from core.base_analyzer import BaseAnalyzer
from core.analyzer_registry import AnalyzerRegistry
from core.analyzer_result import AnalyzerResult


class AnalyzerManager:
    """
    Institutional Analyzer Orchestration Layer.
    """

    def __init__(
        self,
        registry: AnalyzerRegistry | None = None,
    ) -> None:

        self.registry = registry or AnalyzerRegistry()

        self._last_snapshot: Dict = {}

    # --------------------------------------------------

    def register(
        self,
        analyzer: BaseAnalyzer,
    ) -> None:
        """
        Register one analyzer.
        """

        self.registry.register(analyzer)

    # --------------------------------------------------

    def register_many(
        self,
        analyzers: List[BaseAnalyzer],
    ) -> None:
        """
        Register multiple analyzers.
        """

        for analyzer in analyzers:
            self.registry.register(analyzer)

    # --------------------------------------------------

    def execute(
        self,
        market_data,
    ) -> Dict:
        """
        Execute every enabled analyzer and
        return institutional snapshot.
        """

        results: Dict[str, AnalyzerResult] = (
            self.registry.execute(
                market_data
            )
        )

        snapshot = {

            "timestamp": datetime.utcnow().isoformat(),

            "market_data": market_data,

            "results": results,

            "registered_analyzers": len(
                self.registry
            ),

            "enabled_analyzers": len(
                self.registry.list_enabled()
            ),

            "successful_analyzers": len(
                results
            ),

            "overall_status": "SUCCESS",

        }

        self._last_snapshot = snapshot

        return snapshot

    # --------------------------------------------------

    def get_snapshot(
        self,
    ) -> Dict:
        """
        Return latest execution snapshot.
        """

        return self._last_snapshot.copy()

    # --------------------------------------------------

    def clear_snapshot(
        self,
    ) -> None:
        """
        Clear stored snapshot.
        """

        self._last_snapshot.clear()

    # --------------------------------------------------

    def clear_registry(
        self,
    ) -> None:
        """
        Remove every registered analyzer.
        """

        self.registry.clear()

    # --------------------------------------------------

    def execution_summary(
        self,
    ) -> Dict:
        """
        Return execution summary.
        """

        if not self._last_snapshot:

            return {

                "executed": False,

                "registered_analyzers": len(
                    self.registry
                ),

                "enabled_analyzers": len(
                    self.registry.list_enabled()
                ),
            }

        return {

            "executed": True,

            "registered_analyzers":
                self._last_snapshot[
                    "registered_analyzers"
                ],

            "enabled_analyzers":
                self._last_snapshot[
                    "enabled_analyzers"
                ],

            "successful_analyzers":
                self._last_snapshot[
                    "successful_analyzers"
                ],

            "overall_status":
                self._last_snapshot[
                    "overall_status"
                ],
        }

    # --------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return len(self.registry)