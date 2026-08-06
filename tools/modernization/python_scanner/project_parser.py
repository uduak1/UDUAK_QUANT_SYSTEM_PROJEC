"""
tools/modernization/python_scanner/project_parser.py

UDUAK QUANT SYSTEM
Modernization Toolkit

Part 2.7

Project Parser

Parses an entire Python project into a
ProjectAnalysis object.
"""

from __future__ import annotations

from pathlib import Path

from tools.modernization.python_scanner.module_parser import (
    ModuleParser,
)

from tools.modernization.python_scanner.models import (
    ModuleInfo,
    ProjectAnalysis,
)


class ProjectParser:
    """
    Parses an entire project.
    """

    def __init__(self) -> None:

        self.module_parser = ModuleParser()

    # ======================================================
    # PUBLIC
    # ======================================================

    def parse(
        self,
        project_root: Path,
    ) -> ProjectAnalysis:

        project_root = Path(project_root)

        analysis = ProjectAnalysis()

        for file_path in sorted(
            project_root.rglob("*.py")
        ):

            analysis.modules.append(
                self.module_parser.parse(
                    file_path
                )
            )

        analysis.update_statistics()

                # --------------------------------------------------
        # Project Metadata
        # --------------------------------------------------

        analysis.metadata.update(
            {
                "project_root": str(
                    project_root.resolve()
                ),
                "python_files": len(
                    analysis.modules
                ),
                "parsed_modules": sum(
                    1
                    for module in analysis.modules
                    if module.scanned
                ),
                "failed_modules": sum(
                    1
                    for module in analysis.modules
                    if module.has_error
                ),
            }
        )

        return analysis

    # ======================================================
    # FILTERS
    # ======================================================

    @staticmethod
    def modules_with_errors(
        analysis: ProjectAnalysis,
    ) -> list[ModuleInfo]:

        return [
            module
            for module in analysis.modules
            if module.has_error
        ]

    # ------------------------------------------------------

    @staticmethod
    def successfully_parsed(
        analysis: ProjectAnalysis,
    ) -> list[ModuleInfo]:

        return [
            module
            for module in analysis.modules
            if module.scanned
        ]

            # ======================================================
    # SUMMARY
    # ======================================================

    @staticmethod
    def summary(
        analysis: ProjectAnalysis,
    ) -> dict:

        return {
            "modules": analysis.total_modules,
            "classes": analysis.total_classes,
            "functions": analysis.total_functions,
            "imports": analysis.total_imports,
            "syntax_errors": analysis.syntax_errors,
        }


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    parser = ProjectParser()

    analysis = parser.parse(
        Path(".")
    )

    print("=" * 60)
    print("PROJECT PARSER")
    print("=" * 60)

    print(analysis)

    print()

    print(parser.summary(analysis))