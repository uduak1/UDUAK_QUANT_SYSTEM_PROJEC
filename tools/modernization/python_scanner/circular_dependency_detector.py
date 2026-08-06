"""
tools/modernization/python_scanner/circular_dependency_detector.py

UDUAK QUANT SYSTEM
Modernization Toolkit

Part 2.14

Circular Dependency Detector

Detects circular module dependencies
using depth-first search (DFS).
"""

from __future__ import annotations

from typing import Dict
from typing import List
from typing import Set

from tools.modernization.python_scanner.dependency_graph import (
    DependencyGraphBuilder,
)


class CircularDependencyDetector:
    """
    Detects dependency cycles.
    """

    def __init__(self) -> None:

        self.graph: Dict[str, Set[str]] = {}

        self.cycles: List[List[str]] = []

        self._visited: Set[str] = set()

        self._stack: Set[str] = set()

    # ======================================================
    # PUBLIC
    # ======================================================

    def detect(
        self,
        builder: DependencyGraphBuilder,
    ) -> List[List[str]]:

        self.graph = builder.graph

        self.cycles.clear()

        self._visited.clear()

        self._stack.clear()

        for module in self.graph:

            if module not in self._visited:

                self._dfs(
                    module,
                    [],
                )

        return self.cycles

            # ======================================================
    # DFS
    # ======================================================

    def _dfs(
        self,
        node: str,
        path: List[str],
    ) -> None:

        self._visited.add(
            node,
        )

        self._stack.add(
            node,
        )

        path.append(
            node,
        )

        for dependency in self.graph.get(
            node,
            set(),
        ):

            if dependency not in self.graph:

                continue

            if dependency not in self._visited:

                self._dfs(
                    dependency,
                    path.copy(),
                )

            elif dependency in self._stack:

                index = path.index(
                    dependency,
                )

                cycle = (
                    path[index:]
                    + [dependency]
                )

                if cycle not in self.cycles:

                    self.cycles.append(
                        cycle,
                    )

        self._stack.remove(
            node,
        )

            # ======================================================
    # REPORT
    # ======================================================

    def summary(
        self,
    ) -> dict:

        return {
            "cycles": len(
                self.cycles,
            ),
            "has_cycles": bool(
                self.cycles,
            ),
        }

    # ------------------------------------------------------

    def report(
        self,
    ) -> dict:

        return {
            "summary": self.summary(),
            "cycles": self.cycles,
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

    detector = CircularDependencyDetector()

    detector.detect(
        builder,
    )

    print("=" * 60)
    print("CIRCULAR DEPENDENCY DETECTOR")
    print("=" * 60)

    print(
        detector.summary(),
    )

    for cycle in detector.cycles:

        print(
            " -> ".join(cycle)
        )