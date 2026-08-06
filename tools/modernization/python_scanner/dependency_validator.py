"""
tools/modernization/python_scanner/dependency_validator.py

UDUAK QUANT SYSTEM
Modernization Toolkit

Part 2.12

Dependency Graph Validator

Validates the dependency graph and
detects common dependency problems.
"""

from __future__ import annotations

from typing import Dict
from typing import List
from typing import Set

from tools.modernization.python_scanner.dependency_graph import (
    DependencyGraphBuilder,
)


class DependencyValidator:
    """
    Validates dependency graphs.
    """

    def __init__(self) -> None:

        self.graph: Dict[str, Set[str]] = {}

        self.errors: List[str] = []

        self.warnings: List[str] = []

    # ======================================================
    # PUBLIC
    # ======================================================

    def validate(
        self,
        builder: DependencyGraphBuilder,
    ) -> bool:

        self.graph = builder.graph

        self.errors.clear()

        self.warnings.clear()

        self._check_missing_modules()

        self._check_isolated_modules()

        return len(self.errors) == 0

            # ======================================================
    # VALIDATION
    # ======================================================

    def _check_missing_modules(
        self,
    ) -> None:

        known = set(
            self.graph.keys()
        )

        for module, deps in self.graph.items():

            for dep in deps:

                if dep not in known:

                    self.warnings.append(
                        f"{module} -> Missing module: {dep}"
                    )

    # ------------------------------------------------------

    def _check_isolated_modules(
        self,
    ) -> None:

        referenced = set()

        for deps in self.graph.values():

            referenced.update(
                deps
            )

        for module in self.graph:

            if (
                module not in referenced
                and not self.graph[module]
            ):

                self.warnings.append(
                    f"Isolated module: {module}"
                )

                    # ======================================================
    # REPORTS
    # ======================================================

    def summary(
        self,
    ) -> dict:

        return {
            "modules": len(
                self.graph,
            ),
            "errors": len(
                self.errors,
            ),
            "warnings": len(
                self.warnings,
            ),
            "valid": len(
                self.errors,
            ) == 0,
        }

    # ------------------------------------------------------

    def report(
        self,
    ) -> dict:

        return {
            "summary": self.summary(),
            "errors": self.errors,
            "warnings": self.warnings,
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

    validator = DependencyValidator()

    validator.validate(
        builder,
    )

    print("=" * 60)
    print("DEPENDENCY VALIDATOR")
    print("=" * 60)

    print(
        validator.summary(),
    )

    for warning in validator.warnings:

        print("[WARNING]", warning)

    for error in validator.errors:

        print("[ERROR]", error)