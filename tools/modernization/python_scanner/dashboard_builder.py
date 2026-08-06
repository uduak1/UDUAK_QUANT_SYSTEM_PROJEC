"""
tools/modernization/python_scanner/dashboard_builder.py

UDUAK QUANT SYSTEM
Modernization Toolkit

Part 2.18

Modernization Dashboard Builder

Builds a unified modernization dashboard
from all scanner components.
"""

from __future__ import annotations

from pathlib import Path

from tools.modernization.python_scanner.models import (
    ProjectAnalysis,
)

from tools.modernization.python_scanner.project_health_score import (
    ProjectHealthScore,
)

from tools.modernization.python_scanner.modernization_recommender import (
    ModernizationRecommender,
)

from tools.modernization.python_scanner.circular_dependency_detector import (
    CircularDependencyDetector,
)


class DashboardBuilder:
    """
    Builds modernization dashboard data.
    """

    def __init__(
        self,
        output_directory: Path,
    ) -> None:

        self.output_directory = Path(
            output_directory,
        )

        self.output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    # ======================================================
    # PUBLIC
    # ======================================================

    def build(
        self,
        analysis: ProjectAnalysis,
        health: ProjectHealthScore,
        recommender: ModernizationRecommender,
        cycles: CircularDependencyDetector,
    ) -> dict:

        return {
            "project": self._project_card(
                analysis,
            ),
            "health": self._health_card(
                health,
            ),
            "recommendations": self._recommendation_card(
                recommender,
            ),
            "dependencies": self._dependency_card(
                cycles,
            ),
        }

            # ======================================================
    # DASHBOARD CARDS
    # ======================================================

    @staticmethod
    def _project_card(
        analysis: ProjectAnalysis,
    ) -> dict:

        return {
            "modules": analysis.total_modules,
            "classes": analysis.total_classes,
            "functions": analysis.total_functions,
            "imports": analysis.total_imports,
            "syntax_errors": analysis.syntax_errors,
        }

    # ------------------------------------------------------

    @staticmethod
    def _health_card(
        health: ProjectHealthScore,
    ) -> dict:

        return health.report()

    # ------------------------------------------------------

    @staticmethod
    def _recommendation_card(
        recommender: ModernizationRecommender,
    ) -> dict:

        return {
            "count": len(
                recommender.recommendations,
            ),
            "items": recommender.recommendations,
        }

            # ------------------------------------------------------

    @staticmethod
    def _dependency_card(
        cycles: CircularDependencyDetector,
    ) -> dict:

        return {
            "cycle_count": len(
                cycles.cycles,
            ),
            "cycles": cycles.cycles,
        }

    # ======================================================
    # EXPORT
    # ======================================================

    def save_json(
        self,
        dashboard: dict,
    ) -> Path:

        import json

        output = (
            self.output_directory
            / "modernization_dashboard.json"
        )

        with output.open(
            "w",
            encoding="utf-8",
        ) as fp:

            json.dump(
                dashboard,
                fp,
                indent=4,
            )

        return output

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
    from tools.modernization.python_scanner.architecture_analyzer import (
        ArchitectureAnalyzer,
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

    detector = CircularDependencyDetector()

    detector.detect(
        graph,
    )

    recommender = ModernizationRecommender()

    recommender.analyze(
        analysis,
        architecture,
    )

    health = ProjectHealthScore()

    health.calculate(
        analysis,
        architecture,
        recommender,
    )

    dashboard = DashboardBuilder(
        Path(
            "tools/modernization/reports",
        )
    )

    data = dashboard.build(
        analysis,
        health,
        recommender,
        detector,
    )

    output = dashboard.save_json(
        data,
    )

    print("=" * 60)
    print("MODERNIZATION DASHBOARD")
    print("=" * 60)
    print(output)