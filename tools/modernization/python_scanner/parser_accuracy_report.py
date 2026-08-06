"""
tools/modernization/python_scanner/parser_accuracy_report.py

UDUAK QUANT SYSTEM
Modernization Toolkit

Parser Accuracy Report

Generates a human-readable report showing the
accuracy of every parser component.
"""

from __future__ import annotations

import json

from pathlib import Path

from tools.modernization.python_scanner.parser_regression_tests import (
    ParserRegressionTester,
)


class ParserAccuracyReport:

    def __init__(
        self,
        report_directory: Path,
    ):

        self.report_directory = Path(
            report_directory
        )

        self.report_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.tester = (
            ParserRegressionTester()
        )

    # ======================================================

    def generate(
        self,
        sample_file: Path,
    ):

        suite = self.tester.run(
            sample_file
        )

        summary = self.tester.summary(
            suite
        )

        return suite, summary

            # ======================================================
    # JSON REPORT
    # ======================================================

    def export_json(
        self,
        suite,
        summary,
        filename: str = "parser_accuracy.json",
    ) -> Path:

        output = (
            self.report_directory / filename
        )

        data = {
            "summary": summary,
            "results": [
                {
                    "component": r.component,
                    "passed": r.passed,
                    "message": r.message,
                }
                for r in suite.results
            ],
        }

        output.write_text(
            json.dumps(
                data,
                indent=4,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        return output

    # ======================================================
    # MARKDOWN REPORT
    # ======================================================

    def export_markdown(
        self,
        suite,
        summary,
        filename: str = "parser_accuracy.md",
    ) -> Path:

        output = (
            self.report_directory / filename
        )

        lines = [
            "# Parser Accuracy Report",
            "",
            "## Summary",
            "",
        ]

        for key, value in summary.items():

            lines.append(
                f"- **{key}** : {value}"
            )

        lines.extend(
            [
                "",
                "## Components",
                "",
            ]
        )

        for result in suite.results:

            status = (
                "PASS"
                if result.passed
                else "FAIL"
            )

            lines.append(
                f"- **{result.component}** "
                f": {status}"
            )

            if result.message:

                lines.append(
                    f"  - {result.message}"
                )

        output.write_text(
            "\n".join(lines),
            encoding="utf-8",
        )

        return output

            # ======================================================
    # GENERATE ALL REPORTS
    # ======================================================

    def generate_all(
        self,
        sample_file: Path,
    ):

        suite, summary = self.generate(
            sample_file
        )

        return {
            "json": self.export_json(
                suite,
                summary,
            ),
            "markdown": self.export_markdown(
                suite,
                summary,
            ),
        }


# ==========================================================
# MAIN
# ==========================================================

def main():

    report = ParserAccuracyReport(
        Path(
            "tools/modernization/reports"
        )
    )

    reports = report.generate_all(
        Path(
            "core/base_analyzer.py"
        )
    )

    print("=" * 60)
    print("PARSER ACCURACY REPORT")
    print("=" * 60)

    for name, path in reports.items():

        print(
            f"{name:<12}: {path}"
        )


if __name__ == "__main__":

    main()