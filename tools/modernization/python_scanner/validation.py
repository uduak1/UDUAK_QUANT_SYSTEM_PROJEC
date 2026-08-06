"""
tools/modernization/python_scanner/validation.py

UDUAK QUANT SYSTEM
Modernization Toolkit

Part 2.10 (1/4)

Parser Accuracy & Validation

Validates that the parser is discovering
modules, classes, functions and imports correctly.
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from typing import Dict
from typing import List

from tools.modernization.python_scanner.models import (
    ModuleInfo,
    ProjectAnalysis,
)


# ==========================================================
# VALIDATION ISSUE
# ==========================================================

@dataclass(slots=True)
class ValidationIssue:
    """
    Represents one parser problem.
    """

    module: str

    severity: str

    message: str


# ==========================================================
# VALIDATION REPORT
# ==========================================================

@dataclass(slots=True)
class ValidationReport:
    """
    Overall parser validation report.
    """

    checked_modules: int = 0

    checked_classes: int = 0

    checked_functions: int = 0

    checked_imports: int = 0

    issues: List[ValidationIssue] = field(
        default_factory=list
    )

    metadata: Dict[str, object] = field(
        default_factory=dict
    )

    @property
    def passed(self) -> bool:

        return len(self.issues) == 0


# ==========================================================
# VALIDATOR
# ==========================================================

class ParserValidator:
    """
    Performs structural validation of parser output.
    """

    def validate(
        self,
        analysis: ProjectAnalysis,
    ) -> ValidationReport:

        report = ValidationReport()

        report.checked_modules = (
            analysis.total_modules
        )

        report.checked_classes = (
            analysis.total_classes
        )

        report.checked_functions = (
            analysis.total_functions
        )

        report.checked_imports = (
            analysis.total_imports
        )

        for module in analysis.modules:

            self._validate_module(
                module,
                report,
            )

        return report

    # ======================================================
    # MODULE
    # ======================================================

    def _validate_module(
        self,
        module: ModuleInfo,
        report: ValidationReport,
    ) -> None:

            # ----------------------------------------------
        # Empty module
        # ----------------------------------------------

        if (
            module.total_classes == 0
            and module.total_functions == 0
            and module.total_imports == 0
        ):

            report.issues.append(
                ValidationIssue(
                    module=module.module_name,
                    severity="WARNING",
                    message="Empty module detected.",
                )
            )

        # ----------------------------------------------
        # Syntax error
        # ----------------------------------------------

        if module.has_error:

            report.issues.append(
                ValidationIssue(
                    module=module.module_name,
                    severity="ERROR",
                    message=module.syntax_error
                    or "Unknown syntax error",
                )
            )

        # ----------------------------------------------
        # Suspicious module
        # (imports/functions but zero classes)
        # ----------------------------------------------

        if (
            module.total_classes == 0
            and (
                module.total_functions > 20
                or module.total_imports > 20
            )
        ):

            report.issues.append(
                ValidationIssue(
                    module=module.module_name,
                    severity="INFO",
                    message=(
                        "Large module contains "
                        "no detected classes. "
                        "Verify ClassParser."
                    ),
                )
            )

        # ----------------------------------------------
        # Duplicate imports
        # ----------------------------------------------

        names = [
            (
                imp.module,
                imp.name,
            )
            for imp in module.imports
        ]

        if len(names) != len(set(names)):

            report.issues.append(
                ValidationIssue(
                    module=module.module_name,
                    severity="INFO",
                    message="Duplicate imports detected.",
                )
            )

                    # ----------------------------------------------
        # Validate classes
        # ----------------------------------------------

        for cls in module.classes:

            if not cls.name.strip():

                report.issues.append(
                    ValidationIssue(
                        module=module.module_name,
                        severity="ERROR",
                        message="Class with empty name detected.",
                    )
                )

            if cls.line <= 0:

                report.issues.append(
                    ValidationIssue(
                        module=module.module_name,
                        severity="ERROR",
                        message=f"Invalid line number for class '{cls.name}'.",
                    )
                )

            if cls.end_line < cls.line:

                report.issues.append(
                    ValidationIssue(
                        module=module.module_name,
                        severity="ERROR",
                        message=f"Invalid line range for class '{cls.name}'.",
                    )
                )

            for method in cls.methods:

                if not method.is_method:

                    report.issues.append(
                        ValidationIssue(
                            module=module.module_name,
                            severity="WARNING",
                            message=(
                                f"Method '{method.name}' "
                                f"is not marked as a class method."
                            ),
                        )
                    )

        # ----------------------------------------------
        # Validate standalone functions
        # ----------------------------------------------

        for function in module.functions:

            if not function.name.strip():

                report.issues.append(
                    ValidationIssue(
                        module=module.module_name,
                        severity="ERROR",
                        message="Function with empty name detected.",
                    )
                )

            if function.line <= 0:

                report.issues.append(
                    ValidationIssue(
                        module=module.module_name,
                        severity="ERROR",
                        message=(
                            f"Invalid line number "
                            f"for function '{function.name}'."
                        ),
                    )
                )

            if function.end_line < function.line:

                report.issues.append(
                    ValidationIssue(
                        module=module.module_name,
                        severity="ERROR",
                        message=(
                            f"Invalid line range "
                            f"for function '{function.name}'."
                        ),
                    )
                )

            if function.is_method:

                report.issues.append(
                    ValidationIssue(
                        module=module.module_name,
                        severity="WARNING",
                        message=(
                            f"Standalone function "
                            f"'{function.name}' is marked as a method."
                        ),
                    )
                )

                    # ======================================================
    # SUMMARY
    # ======================================================

    @staticmethod
    def summary(
        report: ValidationReport,
    ) -> dict:

        return {
            "passed": report.passed,
            "checked_modules": report.checked_modules,
            "checked_classes": report.checked_classes,
            "checked_functions": report.checked_functions,
            "checked_imports": report.checked_imports,
            "issue_count": len(report.issues),
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

    validator = ParserValidator()

    report = validator.validate(
        analysis
    )

    print("=" * 60)
    print("PARSER VALIDATION")
    print("=" * 60)

    stats = validator.summary(
        report
    )

    for key, value in stats.items():

        print(f"{key:<20}: {value}")

    if report.issues:

        print()
        print("Validation Issues")
        print("-" * 60)

        for issue in report.issues:

            print(
                f"[{issue.severity}] "
                f"{issue.module} -> "
                f"{issue.message}"
            )

    else:

        print()
        print("No validation issues found.")