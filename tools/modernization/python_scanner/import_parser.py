"""
tools/modernization/python_scanner/import_parser.py

UDUAK QUANT SYSTEM
Modernization Toolkit

Part 2.3

Import Parser

Extracts every import statement from an AST.
"""

from __future__ import annotations

import ast

from typing import List

from tools.modernization.python_scanner.models import (
    ImportInfo,
)


class ImportParser:
    """
    Parses import statements from a Python AST.
    """

    def __init__(self) -> None:

        self.imports: List[ImportInfo] = []

    # ======================================================
    # PUBLIC
    # ======================================================

    def parse(
        self,
        tree: ast.AST,
    ) -> List[ImportInfo]:
        """
        Parse every import inside an AST.
        """

        self.imports = []

        for node in ast.walk(tree):

            if isinstance(node, ast.Import):

                self._parse_import(node)

            elif isinstance(node, ast.ImportFrom):

                self._parse_import_from(node)

        return self.imports

    # ======================================================
    # IMPORT
    # ======================================================

    def _parse_import(
        self,
        node: ast.Import,
    ) -> None:

        for alias in node.names:

            self.imports.append(
                ImportInfo(
                    module=alias.name,
                    alias=alias.asname,
                    line=node.lineno,
                    is_from_import=False,
                )
            )

                # ======================================================
    # FROM IMPORT
    # ======================================================

    def _parse_import_from(
        self,
        node: ast.ImportFrom,
    ) -> None:

        module = node.module or ""

        if node.level > 0:

            module = ("." * node.level) + module

        for alias in node.names:

            self.imports.append(
                ImportInfo(
                    module=module,
                    name=alias.name,
                    alias=alias.asname,
                    line=node.lineno,
                    is_from_import=True,
                )
            )

    # ======================================================
    # HELPERS
    # ======================================================

    @staticmethod
    def unique(
        imports: List[ImportInfo],
    ) -> List[ImportInfo]:
        """
        Remove duplicate imports while preserving order.
        """

        seen = set()

        result: List[ImportInfo] = []

        for item in imports:

            key = (
                item.module,
                item.name,
                item.alias,
                item.is_from_import,
            )

            if key in seen:
                continue

            seen.add(key)

            result.append(item)

        return result

            # ======================================================
    # SUMMARY
    # ======================================================

    @staticmethod
    def summary(
        imports: List[ImportInfo],
    ) -> dict:
        """
        Produce summary statistics.
        """

        return {
            "total_imports": len(imports),
            "normal_imports": sum(
                1
                for item in imports
                if not item.is_from_import
            ),
            "from_imports": sum(
                1
                for item in imports
                if item.is_from_import
            ),
            "aliased_imports": sum(
                1
                for item in imports
                if item.alias is not None
            ),
        }


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    from pathlib import Path

    from tools.modernization.python_scanner.ast_loader import (
        ASTLoader,
    )

    loader = ASTLoader()

    parser = ImportParser()

    result = loader.safe_load(
        Path("core/base_analyzer.py")
    )

    if result.loaded:

        imports = parser.parse(result.tree)

        imports = parser.unique(imports)

        print("=" * 60)
        print("IMPORT PARSER")
        print("=" * 60)

        for item in imports:

            print(item)

        print()
        print(parser.summary(imports))

    else:

        print(result.syntax_error)