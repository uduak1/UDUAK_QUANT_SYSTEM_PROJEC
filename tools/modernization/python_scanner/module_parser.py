"""
tools/modernization/python_scanner/module_parser.py

UDUAK QUANT SYSTEM
Modernization Toolkit

Part 2.6

Module Parser

Combines the AST Loader, Import Parser,
Function Parser and Class Parser into one
ModuleInfo object.
"""

from __future__ import annotations

from pathlib import Path

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

from tools.modernization.python_scanner.models import (
    ModuleInfo,
)


class ModuleParser:
    """
    Parses one Python module.
    """

    def __init__(self) -> None:

        self.loader = ASTLoader()

        self.import_parser = ImportParser()

        self.function_parser = FunctionParser()

        self.class_parser = ClassParser()

    # ======================================================
    # PUBLIC
    # ======================================================

    def parse(
        self,
        file_path: Path,
    ) -> ModuleInfo:

        result = self.loader.safe_load(file_path)

        module = ModuleInfo(
            path=result.path,
            module_name=self._module_name(
                result.path,
            ),
            file_size=result.file_size,
            line_count=result.line_count,
            syntax_error=result.syntax_error,
            encoding=result.encoding,
            scanned=result.loaded,
        )

        if not result.loaded:

            return module

        module.docstring = self._module_docstring(
            result.tree,
        )

                # --------------------------------------------------
        # Imports
        # --------------------------------------------------

        module.imports = self.import_parser.unique(
            self.import_parser.parse(
                result.tree,
            )
        )

        # --------------------------------------------------
        # Classes
        # --------------------------------------------------

        module.classes = self.class_parser.parse(
            result.tree,
        )

        # --------------------------------------------------
        # Functions
        # --------------------------------------------------

        all_functions = self.function_parser.parse(
            result.tree,
        )

        module.functions = self.function_parser.functions_only(
            all_functions,
        )

        module.metadata.update(
            {
                "method_count": sum(
                    len(cls.methods)
                    for cls in module.classes
                ),
                "class_count": len(
                    module.classes
                ),
                "function_count": len(
                    module.functions
                ),
                "import_count": len(
                    module.imports
                ),
            }
        )

        return module

            # ======================================================
    # HELPERS
    # ======================================================

    @staticmethod
    def _module_name(
        path: Path,
    ) -> str:

        return (
            str(path)
            .replace("\\", ".")
            .replace("/", ".")
            .removesuffix(".py")
        )

    # ------------------------------------------------------

    @staticmethod
    def _module_docstring(
        tree,
    ):

        import ast

        return ast.get_docstring(tree)

    # ------------------------------------------------------

    @staticmethod
    def summary(
        module: ModuleInfo,
    ) -> dict:

        return {
            "module": module.module_name,
            "classes": module.total_classes,
            "functions": module.total_functions,
            "imports": module.total_imports,
            "has_error": module.has_error,
        }


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    from pathlib import Path

    parser = ModuleParser()

    module = parser.parse(
        Path("core/base_analyzer.py")
    )

    print("=" * 60)
    print("MODULE PARSER")
    print("=" * 60)

    print(module)

    print()

    print(parser.summary(module))