"""
tools/modernization/python_scanner/report_generator.py

UDUAK QUANT SYSTEM
Modernization Toolkit

Part 2.8

Report Generator

Exports ProjectAnalysis into readable reports.
"""

from __future__ import annotations

import json

from pathlib import Path

from typing import Dict

from tools.modernization.python_scanner.models import (
    ProjectAnalysis,
)


class ReportGenerator:
    """
    Generates modernization reports.
    """

    def __init__(
        self,
        output_directory: Path,
    ) -> None:

        self.output_directory = Path(
            output_directory
        )

        self.output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    # ======================================================
    # JSON REPORT
    # ======================================================

    def export_json(
        self,
        analysis: ProjectAnalysis,
        filename: str = "project_analysis.json",
    ) -> Path:

        output_file = (
            self.output_directory / filename
        )

        with output_file.open(
            "w",
            encoding="utf-8",
        ) as fp:

            json.dump(
                analysis.to_dict(),
                fp,
                indent=4,
                ensure_ascii=False,
            )

        return output_file

            # ======================================================
    # MARKDOWN REPORT
    # ======================================================

    def export_markdown(
        self,
        analysis: ProjectAnalysis,
        filename: str = "project_analysis.md",
    ) -> Path:

        output_file = (
            self.output_directory / filename
        )

        lines = []

        lines.append("# UDUAK QUANT SYSTEM")
        lines.append("")
        lines.append("## Project Analysis")
        lines.append("")

        stats = analysis.to_dict()["statistics"]

        for key, value in stats.items():

            lines.append(f"- **{key}** : {value}")

        lines.append("")
        lines.append("## Modules")
        lines.append("")

        for module in analysis.modules:

            lines.append(
                f"### {module.module_name}"
            )

            lines.append(
                f"- Classes : {module.total_classes}"
            )

            lines.append(
                f"- Functions : {module.total_functions}"
            )

            lines.append(
                f"- Imports : {module.total_imports}"
            )

            lines.append(
                f"- Error : {module.has_error}"
            )

            lines.append("")

        output_file.write_text(
            "\n".join(lines),
            encoding="utf-8",
        )

        return output_file

    # ======================================================
    # TEXT SUMMARY
    # ======================================================

    def export_summary(
        self,
        analysis: ProjectAnalysis,
        filename: str = "summary.txt",
    ) -> Path:

        output_file = (
            self.output_directory / filename
        )

        stats = analysis.to_dict()["statistics"]

        report = [
            "PROJECT SUMMARY",
            "=" * 60,
        ]

        for key, value in stats.items():

            report.append(
                f"{key:<20}: {value}"
            )

        output_file.write_text(
            "\n".join(report),
            encoding="utf-8",
        )

        return output_file

            # ======================================================
    # GENERATE ALL REPORTS
    # ======================================================

    def generate_all(
        self,
        analysis: ProjectAnalysis,
    ) -> Dict[str, Path]:

        return {
            "json": self.export_json(
                analysis,
            ),
            "markdown": self.export_markdown(
                analysis,
            ),
            "summary": self.export_summary(
                analysis,
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
        Path(".")
    )

    generator = ReportGenerator(
        Path(
            "tools/modernization/reports"
        )
    )

    reports = generator.generate_all(
        analysis
    )

    print("=" * 60)
    print("REPORT GENERATOR")
    print("=" * 60)

    for name, path in reports.items():

        print(f"{name:<10}: {path}")