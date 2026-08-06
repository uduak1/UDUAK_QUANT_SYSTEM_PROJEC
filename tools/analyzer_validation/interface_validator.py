"""
tools/analyzer_validation/interface_validator.py

UDUAK QUANT SYSTEM
Analyzer Validation Toolkit

Part 1/4

Interface Validator

Validates that every discovered analyzer follows the
institutional analyzer interface.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

from tools.analyzer_validation.analyzer_discovery import (
    AnalyzerDiscovery,
    AnalyzerRecord,
)


# ==========================================================
# VALIDATION ISSUE
# ==========================================================

@dataclass(slots=True)
class ValidationIssue:
    """
    Represents one validation problem.
    """

    analyzer: str

    severity: str

    message: str

    rule: str


# ==========================================================
# VALIDATION RESULT
# ==========================================================

@dataclass(slots=True)
class AnalyzerValidationResult:
    """
    Validation result for one analyzer.
    """

    analyzer: AnalyzerRecord

    passed: bool = True

    issues: List[ValidationIssue] = field(default_factory=list)

    metadata: Dict[str, object] = field(default_factory=dict)

    @property
    def warning_count(self) -> int:

        return sum(
            1
            for issue in self.issues
            if issue.severity == "WARNING"
        )

    @property
    def error_count(self) -> int:

        return sum(
            1
            for issue in self.issues
            if issue.severity == "ERROR"
        )


# ==========================================================
# PROJECT VALIDATION
# ==========================================================

@dataclass(slots=True)
class ProjectValidationResult:
    """
    Complete validation result.
    """

    analyzers: List[AnalyzerValidationResult] = field(
        default_factory=list
    )

    metadata: Dict[str, object] = field(default_factory=dict)

    @property
    def total(self) -> int:

        return len(self.analyzers)

    @property
    def passed(self) -> int:

        return sum(
            1
            for analyzer in self.analyzers
            if analyzer.passed
        )

    @property
    def failed(self) -> int:

        return self.total - self.passed


# ==========================================================
# INTERFACE VALIDATOR
# ==========================================================

class InterfaceValidator:
    """
    Validates analyzer interfaces.

    Part 1 implements only the framework.

    Validation rules are added in
    Parts 2, 3 and 4.
    """

    def __init__(
        self,
        project_root: Path,
    ) -> None:

        self.project_root = Path(project_root)

        self.discovery = AnalyzerDiscovery(
            self.project_root
        )

    # ======================================================
    # PUBLIC
    # ======================================================

    def validate(
        self,
    ) -> ProjectValidationResult:

        discovered = self.discovery.discover()

        result = ProjectValidationResult()

        for analyzer in discovered.analyzers:

            result.analyzers.append(
                self.validate_analyzer(
                    analyzer
                )
            )

        result.metadata.update(
            {
                "scanned_packages":
                    discovered.scanned_packages,
                "scanned_modules":
                    discovered.scanned_modules,
                "total_analyzers":
                    discovered.total_analyzers,
            }
        )

        return result

    # ======================================================
    # SINGLE ANALYZER
    # ======================================================

    def validate_analyzer(
        self,
        analyzer: AnalyzerRecord,
    ) -> AnalyzerValidationResult:

        result = AnalyzerValidationResult(
            analyzer=analyzer,
        )

        #
        # Validation rules will be added
        # in Parts 2–4.
        #

        return result

    # ======================================================
    # HELPERS
    # ======================================================

    @staticmethod
    def add_issue(
        result: AnalyzerValidationResult,
        severity: str,
        rule: str,
        message: str,
    ) -> None:

        result.issues.append(
            ValidationIssue(
                analyzer=result.analyzer.name,
                severity=severity,
                rule=rule,
                message=message,
            )
        )

        if severity == "ERROR":

            result.passed = False


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    validator = InterfaceValidator(
        Path(".")
    )

    report = validator.validate()

    print("=" * 60)
    print("INTERFACE VALIDATOR")
    print("=" * 60)

    print("Analyzers :", report.total)
    print("Passed    :", report.passed)
    print("Failed    :", report.failed)