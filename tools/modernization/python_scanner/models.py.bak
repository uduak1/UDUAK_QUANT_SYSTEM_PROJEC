"""
tools/modernization/python_scanner/models.py

UDUAK QUANT SYSTEM
Modernization Toolkit

Part 2.1

Python Source Scanner Models

These models represent every structural object discovered
while parsing Python source code.

The parser in Part 2.2 will populate these models.
"""

from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field

from pathlib import Path

from typing import Dict
from typing import List
from typing import Optional


# ==========================================================
# IMPORT
# ==========================================================

@dataclass(slots=True)
class ImportInfo:
    """
    Represents one import statement.
    """

    module: str

    name: Optional[str] = None

    alias: Optional[str] = None

    line: int = 0

    is_from_import: bool = False


# ==========================================================
# FUNCTION
# ==========================================================

@dataclass(slots=True)
class FunctionInfo:
    """
    Represents one function.
    """

    name: str

    line: int

    end_line: int

    arguments: List[str] = field(default_factory=list)

    decorators: List[str] = field(default_factory=list)

    returns: Optional[str] = None

    docstring: Optional[str] = None

    is_async: bool = False

    is_method: bool = False

    is_staticmethod: bool = False

    is_classmethod: bool = False

    complexity: int = 1


# ==========================================================
# CLASS
# ==========================================================

@dataclass(slots=True)
class ClassInfo:
    """
    Represents one class.
    """

    name: str

    line: int

    end_line: int

    bases: List[str] = field(default_factory=list)

    decorators: List[str] = field(default_factory=list)

    methods: List[FunctionInfo] = field(default_factory=list)

    docstring: Optional[str] = None

    is_dataclass: bool = False

    is_abstract: bool = False


# ==========================================================
# MODULE
# ==========================================================

@dataclass(slots=True)
class ModuleInfo:
    """
    Represents one Python module.
    """

    path: Path

    module_name: str

    file_size: int

    line_count: int

    imports: List[ImportInfo] = field(default_factory=list)

    classes: List[ClassInfo] = field(default_factory=list)

    functions: List[FunctionInfo] = field(default_factory=list)

    syntax_error: Optional[str] = None

    docstring: Optional[str] = None

    encoding: str = "utf-8"

    scanned: bool = False

    metadata: Dict[str, object] = field(default_factory=dict)

    # ------------------------------------------------------

    @property
    def total_classes(self) -> int:

        return len(self.classes)

    # ------------------------------------------------------

    @property
    def total_functions(self) -> int:

        return len(self.functions)

    # ------------------------------------------------------

    @property
    def total_imports(self) -> int:

        return len(self.imports)

    # ------------------------------------------------------

    @property
    def has_error(self) -> bool:

        return self.syntax_error is not None

    # ------------------------------------------------------

    def to_dict(self) -> Dict:

        return asdict(self)


# ==========================================================
# PROJECT
# ==========================================================

@dataclass(slots=True)
class ProjectAnalysis:
    """
    Complete parsed project.
    """

    modules: List[ModuleInfo] = field(default_factory=list)

    total_modules: int = 0

    total_classes: int = 0

    total_functions: int = 0

    total_imports: int = 0

    syntax_errors: int = 0

    metadata: Dict[str, object] = field(default_factory=dict)

    # ------------------------------------------------------

    def update_statistics(self) -> None:

        self.total_modules = len(self.modules)

        self.total_classes = sum(
            m.total_classes
            for m in self.modules
        )

        self.total_functions = sum(
            m.total_functions
            for m in self.modules
        )

        self.total_imports = sum(
            m.total_imports
            for m in self.modules
        )

        self.syntax_errors = sum(
            1
            for m in self.modules
            if m.has_error
        )

    # ------------------------------------------------------

    def to_dict(self) -> Dict:

        return {
            "modules": [
                module.to_dict()
                for module in self.modules
            ],
            "statistics": {
                "total_modules": self.total_modules,
                "total_classes": self.total_classes,
                "total_functions": self.total_functions,
                "total_imports": self.total_imports,
                "syntax_errors": self.syntax_errors,
            },
            "metadata": self.metadata,
        }

    # ------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}("
            f"modules={self.total_modules}, "
            f"classes={self.total_classes}, "
            f"functions={self.total_functions}, "
            f"imports={self.total_imports}, "
            f"errors={self.syntax_errors})"
        )