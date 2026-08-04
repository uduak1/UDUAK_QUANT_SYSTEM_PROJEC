"""
core/analyzer_manager.py

==========================================================
UDUAK QUANT SYSTEM
Institutional Analyzer Manager
==========================================================

The Analyzer Manager is responsible for creating and
registering runtime analyzer instances.

It acts as the bridge between the Analyzer Registry and
the Signal Engine.

It NEVER performs market analysis itself.
"""

from __future__ import annotations

from typing import Dict

from core.analyzer_registry import AnalyzerRegistry
from core.base_analyzer import BaseAnalyzer


# ==========================================================
# ANALYZER MANAGER
# ==========================================================

class AnalyzerManager:
    """
    Creates, stores and registers analyzer instances.
    """

    def __init__(
        self,
        registry: AnalyzerRegistry,
    ):

        self.registry = registry

        self.instances: Dict[str, BaseAnalyzer] = {}

    # ------------------------------------------------------

    def register(
        self,
        analyzer: BaseAnalyzer,
    ) -> bool:
        """
        Register one analyzer instance.
        """

        self.instances[analyzer.name] = analyzer

        return self.registry.register_instance(
            analyzer.name,
            analyzer,
        )

    # ------------------------------------------------------

    def unregister(
        self,
        analyzer_name: str,
    ) -> bool:
        """
        Remove one analyzer instance.
        """

        if analyzer_name not in self.instances:
            return False

        del self.instances[analyzer_name]

        analyzer = self.registry.get(analyzer_name)

        if analyzer is not None:
            analyzer.instance = None

        return True

    # ------------------------------------------------------

    def get(
        self,
        analyzer_name: str,
    ) -> BaseAnalyzer | None:
        """
        Return one analyzer instance.
        """

        return self.instances.get(analyzer_name)

    # ------------------------------------------------------

    def clear(
        self,
    ) -> None:
        """
        Remove every registered analyzer instance.
        """

        self.instances.clear()

        self.registry.clear_instances()

    # ------------------------------------------------------

    def count(
        self,
    ) -> int:
        """
        Number of registered analyzer instances.
        """

        return len(self.instances)

    # ------------------------------------------------------

    def all_instances(
        self,
    ) -> Dict[str, BaseAnalyzer]:
        """
        Return every registered analyzer instance.
        """

        return self.instances.copy()