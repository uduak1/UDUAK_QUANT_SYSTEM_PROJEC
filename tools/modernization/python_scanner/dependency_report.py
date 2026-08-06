"""
tools/modernization/python_scanner/dependency_report.py

UDUAK QUANT SYSTEM
Modernization Toolkit

Part 2.13

Dependency Graph Report Generator

Generates JSON and Markdown reports
for the project dependency graph.
"""

from __future__ import annotations

import json

from pathlib import Path

from tools.modernization.python_scanner.dependency_graph import (
    DependencyGraphBuilder,
)

from tools.modernization.python_scanner.dependency_validator import (
    DependencyValidator,
)


class DependencyReportGenerator:
    """
    Generates dependency graph reports.
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
    # PUBLIC
    # ======================================================

    def generate(
        self,
        builder: DependencyGraphBuilder,
        validator: DependencyValidator,
    ) -> dict:

        return {
            "json": self.export_json(
                builder,
                validator,
            ),
            "markdown": self.export_markdown(
                builder,
                validator,
            ),
        }

            # ======================================================
    # JSON
    # ======================================================

    def export_json(
        self,
        builder: DependencyGraphBuilder,
        validator: DependencyValidator,
    ) -> Path:

        output = (
            self.output_directory
            / "dependency_graph.json"
        )

        data = {
            "summary": validator.summary(),
            "graph": builder.export(),
            "reverse_graph": builder.export_reverse(),
            "errors": validator.errors,
            "warnings": validator.warnings,
        }

        with output.open(
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False,
            )

        return output

            # ======================================================
    # MARKDOWN
    # ======================================================

    def export_markdown(
        self,
        builder: DependencyGraphBuilder,
        validator: DependencyValidator,
    ) -> Path:

        output = (
            self.output_directory
            / "dependency_graph.md"
        )

        with output.open(
            "w",
            encoding="utf-8",
        ) as file:

            file.write("# Dependency Graph\n\n")

            summary = validator.summary()

            for key, value in summary.items():

                file.write(
                    f"- **{key}** : {value}\n"
                )

            file.write("\n## Modules\n\n")

            for module, deps in sorted(
                builder.export().items()
            ):

                file.write(
                    f"### {module}\n"
                )

                if deps:

                    for dep in deps:

                        file.write(
                            f"- {dep}\n"
                        )

                else:

                    file.write(
                        "- No dependencies\n"
                    )

                file.write("\n")

        return output

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

    reporter = DependencyReportGenerator(
        Path(
            "tools/modernization/reports"
        )
    )

    reports = reporter.generate(
        builder,
        validator,
    )

    print("=" * 60)
    print("DEPENDENCY REPORTS")
    print("=" * 60)

    for name, path in reports.items():

        print(f"{name:<12}: {path}")