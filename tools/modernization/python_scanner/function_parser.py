"""
tools/modernization/python_scanner/function_parser.py

UDUAK QUANT SYSTEM
Modernization Toolkit

Part 2.4

Function Parser

Extracts functions and methods from a Python AST.
"""

from __future__ import annotations

import ast

from typing import List

from tools.modernization.python_scanner.models import (
    FunctionInfo,
)


class FunctionParser(ast.NodeVisitor):
    """
    Parses Python functions.
    """

    def __init__(self) -> None:

        self.functions: List[FunctionInfo] = []

        self._inside_class = False

    # ======================================================
    # PUBLIC
    # ======================================================

    def parse(
        self,
        tree: ast.AST,
    ) -> List[FunctionInfo]:

        self.functions.clear()

        self.visit(tree)

        return self.functions

    # ======================================================
    # CLASS
    # ======================================================

    def visit_ClassDef(
        self,
        node: ast.ClassDef,
    ) -> None:

        previous = self._inside_class

        self._inside_class = True

        self.generic_visit(node)

        self._inside_class = previous

    # ======================================================
    # FUNCTION
    # ======================================================

    def visit_FunctionDef(
        self,
        node: ast.FunctionDef,
    ) -> None:

        self.functions.append(
            self._build_function(node)
        )

        self.generic_visit(node)

    # ======================================================
    # ASYNC FUNCTION
    # ======================================================

    def visit_AsyncFunctionDef(
        self,
        node: ast.AsyncFunctionDef,
    ) -> None:

        info = self._build_function(node)

        info.is_async = True

        self.functions.append(info)

        self.generic_visit(node)

            # ======================================================
    # BUILD FUNCTION
    # ======================================================

    def _build_function(
        self,
        node: ast.FunctionDef | ast.AsyncFunctionDef,
    ) -> FunctionInfo:

        decorators = [
            ast.unparse(d)
            for d in node.decorator_list
        ]

        arguments = [
            arg.arg
            for arg in node.args.args
        ]

        end_line = getattr(
            node,
            "end_lineno",
            node.lineno,
        )

        returns = None

        if node.returns is not None:

            try:

                returns = ast.unparse(
                    node.returns
                )

            except Exception:

                returns = None

        info = FunctionInfo(
            name=node.name,
            line=node.lineno,
            end_line=end_line,
            arguments=arguments,
            decorators=decorators,
            returns=returns,
            docstring=ast.get_docstring(node),
            is_async=False,
            is_method=self._inside_class,
            is_staticmethod=(
                "staticmethod"
                in decorators
            ),
            is_classmethod=(
                "classmethod"
                in decorators
            ),
            complexity=self._calculate_complexity(
                node
            ),
        )

        return info

    # ======================================================
    # COMPLEXITY
    # ======================================================

    def _calculate_complexity(
        self,
        node: ast.AST,
    ) -> int:

        complexity = 1

        decision_nodes = (
            ast.If,
            ast.For,
            ast.AsyncFor,
            ast.While,
            ast.Try,
            ast.ExceptHandler,
            ast.With,
            ast.AsyncWith,
            ast.Match,
            ast.BoolOp,
        )

        for child in ast.walk(node):

            if isinstance(
                child,
                decision_nodes,
            ):

                complexity += 1

        return complexity