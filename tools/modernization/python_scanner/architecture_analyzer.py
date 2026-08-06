"""
tools/modernization/python_scanner/architecture_analyzer.py

UDUAK QUANT SYSTEM
Modernization Toolkit

Part 2.15

Project Architecture Analyzer

Analyzes project architecture using
the dependency graph.
"""

from __future__ import annotations

from collections import Counter
from typing import Dict

from tools.modernization.python_scanner.dependency_graph import (
    DependencyGraphBuilder,
)


class ArchitectureAnalyzer:
    """
    Analyzes overall project architecture.
    """

    def __init__(self) -> None:

        self.graph: Dict[str, set[str]] = {}

    # ======================================================
    # PUBLIC
    # ======================================================

    def analyze(
        self,
        builder: DependencyGraphBuilder,
    ) -> dict:

        self.graph = builder.graph

        return {
            "modules": len(
                self.graph,
            ),
            "dependency_statistics":
                self._dependency_statistics(),
            "top_dependencies":
                self._top_dependencies(),
        }

            # ======================================================
    # STATISTICS
    # ======================================================

    def _dependency_statistics(
        self,
    ) -> dict:

        counts = [
            len(dependencies)
            for dependencies
            in self.graph.values()
        ]

        if not counts:

            return {
                "minimum": 0,
                "maximum": 0,
                "average": 0.0,
            }

        return {
            "minimum": min(
                counts,
            ),
            "maximum": max(
                counts,
            ),
            "average": round(
                sum(counts)
                / len(counts),
                2,
            ),
        }

    # ------------------------------------------------------

    def _top_dependencies(
        self,
    ) -> dict:

        counter = Counter()

        for dependencies in self.graph.values():

            counter.update(
                dependencies,
            )

        return dict(
            counter.most_common(20)
        )

            # ======================================================
    # HELPERS
    # ======================================================

    def independent_modules(
        self,
    ) -> list[str]:

        return sorted(
            module
            for module, dependencies
            in self.graph.items()
            if not dependencies
        )

    # ------------------------------------------------------

    def highly_connected_modules(
        self,
        minimum: int = 10,
    ) -> list[str]:

        return sorted(
            module
            for module, dependencies
            in self.graph.items()
            if len(dependencies)
            >= minimum
        )

    # ------------------------------------------------------

    def summary(
        self,
    ) -> dict:

        return {
            "modules": len(
                self.graph,
            ),
            "independent_modules": len(
                self.independent_modules()
            ),
            "highly_connected_modules": len(
                self.highly_connected_modules()
            ),
        }

        # ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    from pathlib import Path

    from tools.modernization.python_scanner.project_parser import (
        ProjectParser,
    )

    parser = ProjectParser()

    analysis = parser.parse(
        Path("."),
    )

    builder = DependencyGraphBuilder()

    builder.build(
        analysis,
    )

    architecture = ArchitectureAnalyzer()

    report = architecture.analyze(
        builder,
    )

    print("=" * 60)
    print("PROJECT ARCHITECTURE")
    print("=" * 60)

    for key, value in report.items():

        print(f"{key}:")
        print(value)
        print()

    print("Summary")
    print(
        architecture.summary(),
    )