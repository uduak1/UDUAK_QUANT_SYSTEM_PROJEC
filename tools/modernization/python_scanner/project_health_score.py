"""
tools/modernization/python_scanner/project_health_score.py

UDUAK QUANT SYSTEM
Modernization Toolkit

Part 2.17

Project Health Score Engine

Calculates an overall project
health score from analysis,
architecture and modernization
recommendations.
"""

from __future__ import annotations

from tools.modernization.python_scanner.models import (
    ProjectAnalysis,
)

from tools.modernization.python_scanner.architecture_analyzer import (
    ArchitectureAnalyzer,
)

from tools.modernization.python_scanner.modernization_recommender import (
    ModernizationRecommender,
)


class ProjectHealthScore:
    """
    Calculates overall project health.
    """

    def __init__(self) -> None:

        self.score = 100.0

        self.breakdown = {}

    # ======================================================
    # PUBLIC
    # ======================================================

    def calculate(
        self,
        analysis: ProjectAnalysis,
        architecture: ArchitectureAnalyzer,
        recommender: ModernizationRecommender,
    ) -> float:

        self.score = 100.0

        self.breakdown.clear()

        self._analysis_score(
            analysis,
        )

        self._architecture_score(
            architecture,
        )

        self._recommendation_score(
            recommender,
        )

        self.score = max(
            0.0,
            round(self.score, 2),
        )

        return self.score

            # ======================================================
    # ANALYSIS SCORE
    # ======================================================

    def _analysis_score(
        self,
        analysis: ProjectAnalysis,
    ) -> None:

        deduction = 0.0

        deduction += (
            analysis.syntax_errors * 10
        )

        self.score -= deduction

        self.breakdown[
            "analysis"
        ] = {
            "deduction": deduction,
            "syntax_errors": analysis.syntax_errors,
        }

    # ======================================================
    # ARCHITECTURE SCORE
    # ======================================================

    def _architecture_score(
        self,
        architecture: ArchitectureAnalyzer,
    ) -> None:

        summary = architecture.summary()

        deduction = (
            summary[
                "highly_connected_modules"
            ] * 2
        )

        self.score -= deduction

        self.breakdown[
            "architecture"
        ] = {
            "deduction": deduction,
            **summary,
        }

            # ======================================================
    # RECOMMENDATIONS
    # ======================================================

    def _recommendation_score(
        self,
        recommender: ModernizationRecommender,
    ) -> None:

        deduction = (
            len(
                recommender.recommendations
            ) * 1.5
        )

        self.score -= deduction

        self.breakdown[
            "recommendations"
        ] = {
            "deduction": deduction,
            "count": len(
                recommender.recommendations
            ),
        }

    # ------------------------------------------------------

    def report(
        self,
    ) -> dict:

        return {
            "health_score": self.score,
            "breakdown": self.breakdown,
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

    recommender.analyze(
        analysis,
        architecture,
    )

    scorer = ProjectHealthScore()

    scorer.calculate(
        analysis,
        architecture,
        recommender,
    )

    print("=" * 60)
    print("PROJECT HEALTH SCORE")
    print("=" * 60)

    print(
        scorer.report(),
    )