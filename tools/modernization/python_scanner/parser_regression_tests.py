"""
tools/modernization/python_scanner/parser_regression_tests.py

UDUAK QUANT SYSTEM
Modernization Toolkit

Part 2.11

Parser Regression Tests

Verifies every parser still produces
correct output after future changes.
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from pathlib import Path

from typing import List

from tools.modernization.python_scanner.ast_loader import (
    ASTLoader,
)

from tools.modernization.python_scanner.import_parser import (
    ImportParser,
)

from tools.modernization.python_scanner.function_parser import (
    FunctionParser,
)

from tools.modernization.python_scanner.class_parser import (
    ClassParser,
)

from tools.modernization.python_scanner.module_parser import (
    ModuleParser,
)

from tools.modernization.python_scanner.project_parser import (
    ProjectParser,
)


# ==========================================================
# TEST RESULT
# ==========================================================

@dataclass(slots=True)
class RegressionResult:

    component: str

    passed: bool

    message: str = ""


# ==========================================================
# TEST SUITE
# ==========================================================

@dataclass(slots=True)
class RegressionSuite:

    results: List[RegressionResult] = field(
        default_factory=list
    )

    @property
    def passed(self) -> bool:

        return all(
            result.passed
            for result in self.results
        )

    def add(
        self,
        component: str,
        passed: bool,
        message: str = "",
    ) -> None:

        self.results.append(
            RegressionResult(
                component,
                passed,
                message,
            )
        )


# ==========================================================
# REGRESSION TESTER
# ==========================================================

class ParserRegressionTester:

    def __init__(self):

        self.loader = ASTLoader()

        self.import_parser = ImportParser()

        self.function_parser = FunctionParser()

        self.class_parser = ClassParser()

        self.module_parser = ModuleParser()

        self.project_parser = ProjectParser()

    # ======================================================

    def run(
        self,
        sample_file: Path,
    ) -> RegressionSuite:

        suite = RegressionSuite()

        sample_file = Path(sample_file)

                # --------------------------------------------------
        # AST Loader
        # --------------------------------------------------

        loaded = self.loader.safe_load(
            sample_file
        )

        suite.add(
            "ASTLoader",
            loaded.loaded,
            loaded.syntax_error or "",
        )

        if not loaded.loaded:

            return suite

        tree = loaded.tree

        # --------------------------------------------------
        # Import Parser
        # --------------------------------------------------

        imports = self.import_parser.parse(
            tree,
        )

        suite.add(
            "ImportParser",
            isinstance(imports, list),
            f"{len(imports)} imports found",
        )

        # --------------------------------------------------
        # Function Parser
        # --------------------------------------------------

        functions = self.function_parser.parse(
            tree,
        )

        suite.add(
            "FunctionParser",
            isinstance(functions, list),
            f"{len(functions)} functions found",
        )

        standalone = (
            self.function_parser.functions_only(
                functions
            )
        )

        suite.add(
            "StandaloneFunctions",
            len(standalone) <= len(functions),
            (
                f"{len(standalone)} "
                f"standalone functions"
            ),
        )

                # --------------------------------------------------
        # Class Parser
        # --------------------------------------------------

        classes = self.class_parser.parse(
            tree,
        )

        suite.add(
            "ClassParser",
            isinstance(classes, list),
            f"{len(classes)} classes found",
        )

        # Verify every parsed class has a name
        valid_classes = all(
            cls.name.strip()
            for cls in classes
        )

        suite.add(
            "ClassNames",
            valid_classes,
            "Verified class names",
        )

        # --------------------------------------------------
        # Module Parser
        # --------------------------------------------------

        module = self.module_parser.parse(
            sample_file,
        )

        suite.add(
            "ModuleParser",
            module.scanned,
            module.module_name,
        )

        suite.add(
            "ModuleClassCount",
            module.total_classes == len(classes),
            (
                f"Module={module.total_classes}, "
                f"Parser={len(classes)}"
            ),
        )

        suite.add(
            "ModuleFunctionCount",
            module.total_functions == len(standalone),
            (
                f"Module={module.total_functions}, "
                f"Parser={len(standalone)}"
            ),
        )

        # --------------------------------------------------
        # Project Parser
        # --------------------------------------------------

        project = self.project_parser.parse(
            sample_file.parent.parent.parent
        )

        suite.add(
            "ProjectParser",
            project.total_modules > 0,
            f"{project.total_modules} modules",
        )

        suite.add(
            "ProjectStatistics",
            (
                project.total_functions >=
                module.total_functions
            ),
            "Statistics verified",
        )

        return suite

            # ======================================================
    # SUMMARY
    # ======================================================

    @staticmethod
    def summary(
        suite: RegressionSuite,
    ) -> dict:

        passed = sum(
            1
            for result in suite.results
            if result.passed
        )

        failed = len(
            suite.results
        ) - passed

        return {
            "total_tests": len(
                suite.results
            ),
            "passed": passed,
            "failed": failed,
            "success": suite.passed,
        }


# ==========================================================
# MAIN
# ==========================================================

def main():

    tester = ParserRegressionTester()

    suite = tester.run(
        Path("core/base_analyzer.py")
    )

    print("=" * 60)
    print("PARSER REGRESSION TESTS")
    print("=" * 60)

    for result in suite.results:

        status = (
            "PASS"
            if result.passed
            else "FAIL"
        )

        print(
            f"[{status}] "
            f"{result.component:<25}"
            f"{result.message}"
        )

    print()

    stats = tester.summary(
        suite
    )

    print("=" * 60)

    for key, value in stats.items():

        print(
            f"{key:<15}: {value}"
        )

    print("=" * 60)


if __name__ == "__main__":

    main()