"""
tools/modernization/python_scanner/class_parser_repair.py

UDUAK QUANT SYSTEM
Modernization Toolkit

Part 2.11

Class Parser Repair Utility

Verifies that every ClassDef node discovered by Python's AST
is also returned by ClassParser.
"""

from __future__ import annotations

import ast

from pathlib import Path

from tools.modernization.python_scanner.ast_loader import ASTLoader
from tools.modernization.python_scanner.class_parser import ClassParser


class ClassParserRepair:

    def __init__(self):

        self.loader = ASTLoader()

        self.parser = ClassParser()

    # =====================================================

    def repair(self, file_path: Path):

        result = self.loader.safe_load(file_path)

        if not result.loaded:

            print(result.syntax_error)

            return

        tree = result.tree

        parser_classes = self.parser.parse(tree)

        ast_classes = [
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.ClassDef)
        ]

        print("=" * 60)
        print(file_path)
        print("=" * 60)

        print("AST Classes :", len(ast_classes))
        print("Parser Classes :", len(parser_classes))
        print()

        parser_names = {
            cls.name
            for cls in parser_classes
        }

        missing = []

        for cls in ast_classes:

            if cls.name not in parser_names:

                missing.append(cls)

        if not missing:

            print("PASS")

            return

        print("Missing Classes")

        print("-" * 60)

        for cls in missing:

            print(
                f"{cls.name} "
                f"(line {cls.lineno})"
            )


# =========================================================

def main():

    repair = ClassParserRepair()

    repair.repair(
        Path("core/base_analyzer.py")
    )


if __name__ == "__main__":

    main()