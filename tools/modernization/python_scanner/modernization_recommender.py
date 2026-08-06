"""
tools/modernization/python_scanner/modernization_recommender.py

UDUAK QUANT SYSTEM
Modernization Toolkit

Part 2.16

Modernization Recommendation Engine

Generates modernization recommendations
from project analysis and architecture.
"""

from __future__ import annotations

from typing import List

from tools.modernization.python_scanner.models import (
    ProjectAnalysis,
)

from tools.modernization.python_scanner.architecture_analyzer import (
    ArchitectureAnalyzer,
)


class ModernizationRecommender:
    """
    Generates modernization recommendations.
    """

    def __init__(self) -> None:

        self.recommendations: List[str] = []

    # ======================================================
    # PUBLIC
    # ======================================================

    def analyze(
        self,
        analysis: ProjectAnalysis,
        architecture: ArchitectureAnalyzer,
    ) -> List[str]:

        self.recommendations.clear()

        self._project_statistics(
            analysis,
        )

        self._architecture_statistics(
            architecture,
        )

        return self.recommendations

            # ======================================================
    # PROJECT ANALYSIS
    # ======================================================

    def _project_statistics(
        self,
        analysis: ProjectAnalysis,
    ) -> None:

        if analysis.syntax_errors > 0:

            self.recommendations.append(
                f"Fix {analysis.syntax_errors} syntax errors."
            )

        if analysis.total_modules > 200:

            self.recommendations.append(
                "Project is large. Consider splitting into packages."
            )

        if analysis.total_functions > 1000:

            self.recommendations.append(
                "High function count. Review for consolidation."
            )

        if analysis.total_imports > 1000:

            self.recommendations.append(
                "Review excessive module dependencies."
            )

                # ======================================================
    # ARCHITECTURE
    # ======================================================

    def _architecture_statistics(
        self,
        architecture: ArchitectureAnalyzer,
    ) -> None:

        summary = architecture.summary()

        if summary["highly_connected_modules"] > 0:

            self.recommendations.append(
                "Reduce coupling in highly connected modules."
            )

        if summary["independent_modules"] > 20:

            self.recommendations.append(
                "Review isolated modules for dead code."
            )

        if not self.recommendations:

            self.recommendations.append(
                "No major modernization issues detected."
            )

    # ------------------------------------------------------

    def summary(
        self,
    ) -> dict:

        return {
            "recommendations": len(
                self.recommendations,
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

    from tools.modernization.python_scanner.dependency_graph import (
        DependencyGraphBuilder,
    )

    parser = ProjectParser()

    analysis = parser.parse(
        Path("."),
    )

    graph = DependencyGraphBuilder()

    graph.build(
        analysis,
    )

    architecture = ArchitectureAnalyzer()

    architecture.analyze(
        graph,
    )

    recommender = ModernizationRecommender()

    recommendations = recommender.analyze(
        analysis,
        architecture,
    )

    print("=" * 60)
    print("MODERNIZATION RECOMMENDATIONS")
    print("=" * 60)

    for recommendation in recommendations:

        print("-", recommendation)

    print()

    print(
        recommender.summary(),
    )