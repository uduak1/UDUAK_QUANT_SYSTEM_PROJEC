"""
tools/modernization/python_scanner/ast_loader.py

UDUAK QUANT SYSTEM
Modernization Toolkit

Part 2.2

AST Loader

Responsibilities
----------------

• Detect file encoding
• Read Python source files
• Parse Abstract Syntax Tree (AST)
• Capture syntax errors
• Return standardized results

This module performs NO semantic analysis.

It only loads Python source safely.
"""

from __future__ import annotations

import ast
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

try:
    import tokenize
except ImportError:
    tokenize = None


logger = logging.getLogger("MQT.ASTLoader")


# ==========================================================
# RESULT
# ==========================================================

@dataclass(slots=True)
class ASTLoadResult:
    """
    Result returned by ASTLoader.
    """

    path: Path

    source: str

    tree: Optional[ast.AST]

    encoding: str

    syntax_error: Optional[str]

    line_count: int

    file_size: int

    loaded: bool

    # ------------------------------------------------------

    @property
    def has_error(self) -> bool:
        return self.syntax_error is not None


# ==========================================================
# AST LOADER
# ==========================================================

class ASTLoader:
    """
    Safely loads Python source files.

    Workflow

        detect_encoding()
                ↓

           read_source()
                ↓

           parse_source()
                ↓

        ASTLoadResult
    """

    DEFAULT_ENCODING = "utf-8"

    # ------------------------------------------------------

    def __init__(self) -> None:

        self.logger = logger

    # ======================================================
    # ENCODING
    # ======================================================

    def detect_encoding(
        self,
        file_path: Path,
    ) -> str:
        """
        Detect Python file encoding.

        Falls back to UTF-8 if detection fails.
        """

        if tokenize is None:
            return self.DEFAULT_ENCODING

        try:

            with file_path.open("rb") as fp:

                encoding, _ = tokenize.detect_encoding(
                    fp.readline,
                )

                return encoding

        except Exception:

            return self.DEFAULT_ENCODING

    # ======================================================
    # SOURCE
    # ======================================================

    def read_source(
        self,
        file_path: Path,
    ) -> tuple[str, str]:
        """
        Read Python source.

        Returns
        -------
        (source, encoding)
        """

        encoding = self.detect_encoding(
            file_path,
        )

        source = file_path.read_text(
            encoding=encoding,
            errors="replace",
        )

        return source, encoding

            # ======================================================
    # AST
    # ======================================================

    def parse_source(
        self,
        source: str,
        filename: str = "<unknown>",
    ) -> tuple[Optional[ast.AST], Optional[str]]:
        """
        Parse Python source into an AST.

        Parameters
        ----------
        source
            Python source code.

        filename
            Used only for error reporting.

        Returns
        -------
        tuple

            (tree, syntax_error)
        """

        try:

            tree = ast.parse(
                source,
                filename=filename,
                mode="exec",
            )

            return tree, None

        except SyntaxError as exc:

            message = (
                f"{exc.msg} "
                f"(line {exc.lineno}, "
                f"column {exc.offset})"
            )

            self.logger.warning(
                "Syntax error in %s : %s",
                filename,
                message,
            )

            return None, message

        except Exception as exc:

            message = str(exc)

            self.logger.exception(
                "Unexpected parser failure: %s",
                filename,
            )

            return None, message

    # ======================================================
    # LOAD
    # ======================================================

    def load(
        self,
        file_path: Path,
    ) -> ASTLoadResult:
        """
        Load one Python file.

        Workflow

            detect encoding
                    ↓

              read source
                    ↓

               parse AST
                    ↓

            return ASTLoadResult
        """

        file_path = Path(file_path)

        if not file_path.exists():

            raise FileNotFoundError(file_path)

        source, encoding = self.read_source(
            file_path,
        )

        tree, syntax_error = self.parse_source(
            source,
            filename=str(file_path),
        )

        result = ASTLoadResult(
            path=file_path,
            source=source,
            tree=tree,
            encoding=encoding,
            syntax_error=syntax_error,
            line_count=len(source.splitlines()),
            file_size=file_path.stat().st_size,
            loaded=tree is not None,
        )

        return result

    # ======================================================
    # SAFE LOAD
    # ======================================================

    def safe_load(
        self,
        file_path: Path,
    ) -> ASTLoadResult:
        """
        Never raises.

        Any unexpected exception is converted into
        an ASTLoadResult.
        """

        try:

            return self.load(file_path)

        except Exception as exc:

            self.logger.exception(
                "Unable to load %s",
                file_path,
            )

            return ASTLoadResult(
                path=Path(file_path),
                source="",
                tree=None,
                encoding=self.DEFAULT_ENCODING,
                syntax_error=str(exc),
                line_count=0,
                file_size=0,
                loaded=False,
            )

                # ======================================================
    # VALIDATION
    # ======================================================

    def validate_ast(
        self,
        result: ASTLoadResult,
    ) -> bool:
        """
        Validate a loaded AST result.

        Returns
        -------
        bool
            True if the AST is valid.
        """

        if not result.loaded:
            return False

        if result.tree is None:
            return False

        return True

    # ======================================================
    # HELPERS
    # ======================================================

    @staticmethod
    def is_python_file(
        file_path: Path,
    ) -> bool:
        """
        Return True if the supplied file
        is a Python source file.
        """

        return (
            Path(file_path).is_file()
            and Path(file_path).suffix == ".py"
        )

    # ======================================================
    # DIRECTORY LOADER
    # ======================================================

    def load_directory(
        self,
        directory: Path,
    ) -> list[ASTLoadResult]:
        """
        Load every Python file in a directory
        recursively.
        """

        directory = Path(directory)

        results: list[ASTLoadResult] = []

        for file_path in sorted(
            directory.rglob("*.py")
        ):

            results.append(
                self.safe_load(file_path)
            )

        self.logger.info(
            "Loaded %d Python files.",
            len(results),
        )

        return results

    # ======================================================
    # REPRESENTATION
    # ======================================================

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}"
            "("
            f"encoding='{self.DEFAULT_ENCODING}'"
            ")"
        )


# ==========================================================
# MAIN
# ==========================================================

def main() -> None:
    """
    Stand-alone smoke test.
    """

    import argparse

    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        ),
    )

    parser = argparse.ArgumentParser(
        description="AST Loader",
    )

    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Python file or directory",
    )

    args = parser.parse_args()

    loader = ASTLoader()

    target = Path(args.path)

    if target.is_file():

        result = loader.safe_load(target)

        print("=" * 60)
        print("AST LOAD RESULT")
        print("=" * 60)
        print(f"File      : {result.path}")
        print(f"Encoding  : {result.encoding}")
        print(f"Loaded    : {result.loaded}")
        print(f"Lines     : {result.line_count}")
        print(f"Size      : {result.file_size}")
        print(f"Has Error : {result.has_error}")

        if result.has_error:
            print(f"Error     : {result.syntax_error}")

    else:

        results = loader.load_directory(target)

        successful = sum(
            1 for r in results if r.loaded
        )

        failed = len(results) - successful

        print("=" * 60)
        print("DIRECTORY SUMMARY")
        print("=" * 60)
        print(f"Directory : {target.resolve()}")
        print(f"Files     : {len(results)}")
        print(f"Loaded    : {successful}")
        print(f"Failed    : {failed}")
        print("=" * 60)


if __name__ == "__main__":
    main()