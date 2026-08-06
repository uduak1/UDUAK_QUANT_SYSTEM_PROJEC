"""
tools/modernization/python_scanner/dependency_graph.py

UDUAK QUANT SYSTEM
Modernization Toolkit

Part 2.11

Dependency Graph Builder

Builds a project-wide dependency graph
from parsed ModuleInfo objects.
"""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Dict
from typing import List
from typing import Set

from tools.modernization.python_scanner.models import (
    ModuleInfo,
    ProjectAnalysis,
)


class DependencyGraphBuilder:
    """
    Builds module dependency graph.
    """

    def __init__(self) -> None:

        self.graph: Dict[str, Set[str]] = defaultdict(set)

        self.reverse_graph: Dict[str, Set[str]] = defaultdict(set)

    # ======================================================
    # PUBLIC
    # ======================================================

    def build(
        self,
        analysis: ProjectAnalysis,
    ) -> Dict[str, Set[str]]:

        self.graph.clear()

        self.reverse_graph.clear()

        for module in analysis.modules:

            self._add_module(module)

        return self.graph

            # ======================================================
    # BUILD
    # ======================================================

    def _add_module(
        self,
        module: ModuleInfo,
    ) -> None:

        module_name = module.module_name

        self.graph.setdefault(
            module_name,
            set(),
        )

        self.reverse_graph.setdefault(
            module_name,
            set(),
        )

        for imp in module.imports:

            dependency = imp.module

            if not dependency:

                continue

            self.graph[module_name].add(
                dependency,
            )

            self.reverse_graph[
                dependency
            ].add(
                module_name,
            )

    # ======================================================
    # LOOKUPS
    # ======================================================

    def dependencies_of(
        self,
        module_name: str,
    ) -> Set[str]:

        return self.graph.get(
            module_name,
            set(),
        )

    # ------------------------------------------------------

    def dependents_of(
        self,
        module_name: str,
    ) -> Set[str]:

        return self.reverse_graph.get(
            module_name,
            set(),
        )

            # ======================================================
    # SUMMARY
    # ======================================================

    def summary(self) -> dict:

        edge_count = sum(
            len(edges)
            for edges in self.graph.values()
        )

        return {
            "modules": len(
                self.graph,
            ),
            "dependencies": edge_count,
        }

    # ------------------------------------------------------

    def export(self) -> dict:

        return {
            module: sorted(edges)
            for module, edges in self.graph.items()
        }

    # ------------------------------------------------------

    def export_reverse(self) -> dict:

        return {
            module: sorted(edges)
            for module, edges
            in self.reverse_graph.items()
        }

        # ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    from tools.modernization.python_scanner.project_parser import (
        ProjectParser,
    )

    analysis = ProjectParser().parse(
        Path("."),
    )

    builder = DependencyGraphBuilder()

    builder.build(
        analysis,
    )

    print("=" * 60)
    print("DEPENDENCY GRAPH")
    print("=" * 60)

    print(
        builder.summary(),
    )

    print()

    first = next(
        iter(builder.graph),
    )

    print("Example Module")
    print(first)

    print()

    print(
        builder.dependencies_of(
            first,
        )
    )