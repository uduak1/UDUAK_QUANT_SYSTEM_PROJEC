"""
tools/analyzer_validation/analyzer_discovery.py

UDUAK QUANT SYSTEM
Analyzer Validation Framework

Part 1/4

Analyzer Discovery

Discovers every analyzer implemented inside the project.

Responsibilities
----------------
• Locate Python files
• Load modules safely
• Discover analyzer classes
• Collect metadata
• Build discovery report

This module DOES NOT execute analyzers.
Execution validation is handled separately.
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from pathlib import Path

from typing import Any
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional

import importlib
import inspect
import logging
import pkgutil
import traceback


LOGGER = logging.getLogger("UDUAK.AnalyzerDiscovery")


# ==========================================================
# ANALYZER RECORD
# ==========================================================


@dataclass(slots=True)
class AnalyzerRecord:
    """
    Represents one discovered analyzer.
    """

    name: str

    qualified_name: str

    module: str

    file_path: Path

    class_name: str

    package: str

    base_classes: List[str] = field(default_factory=list)

    methods: List[str] = field(default_factory=list)

    public_methods: List[str] = field(default_factory=list)

    docstring: Optional[str] = None

    is_abstract: bool = False

    successfully_loaded: bool = True

    load_error: Optional[str] = None

    metadata: Dict[str, Any] = field(default_factory=dict)


# ==========================================================
# DISCOVERY RESULT
# ==========================================================


@dataclass(slots=True)
class DiscoveryResult:
    """
    Complete analyzer discovery result.
    """

    analyzers: List[AnalyzerRecord] = field(default_factory=list)

    scanned_modules: int = 0

    scanned_packages: int = 0

    failed_modules: int = 0

    skipped_modules: int = 0

    metadata: Dict[str, Any] = field(default_factory=dict)

    # ------------------------------------------------------

    @property
    def total_analyzers(self) -> int:
        return len(self.analyzers)

    # ------------------------------------------------------

    @property
    def successful_analyzers(self) -> int:
        return sum(
            1
            for analyzer in self.analyzers
            if analyzer.successfully_loaded
        )

    # ------------------------------------------------------

    @property
    def failed_analyzers(self) -> int:
        return sum(
            1
            for analyzer in self.analyzers
            if not analyzer.successfully_loaded
        )


# ==========================================================
# ANALYZER DISCOVERY
# ==========================================================


class AnalyzerDiscovery:
    """
    Discovers analyzer implementations.
    """

    DEFAULT_PACKAGES = (
        "analysis",
        "core",
        "strategies",
    )

    # ------------------------------------------------------

    def __init__(
        self,
        project_root: Path,
        packages: Optional[Iterable[str]] = None,
    ) -> None:

        self.project_root = Path(project_root)

        self.packages = list(
            packages
            if packages is not None
            else self.DEFAULT_PACKAGES
        )

    # ======================================================
    # PUBLIC
    # ======================================================

    def discover(self) -> DiscoveryResult:
        """
        Discover all analyzers.
        """

        LOGGER.info(
            "Starting analyzer discovery..."
        )

        result = DiscoveryResult()

        for package in self.packages:

            self._discover_package(
                package=package,
                result=result,
            )

        LOGGER.info(
            "Discovery complete. %s analyzers found.",
            result.total_analyzers,
        )

        return result

    # ======================================================
    # INTERNAL
    # ======================================================

        # ======================================================
    # PACKAGE DISCOVERY
    # ======================================================

    def _discover_package(
        self,
        package: str,
        result: DiscoveryResult,
    ) -> None:
        """
        Discover every module inside one package.
        """

        LOGGER.info(
            "Scanning package: %s",
            package,
        )

        try:

            imported_package = importlib.import_module(
                package,
            )

        except Exception as exc:

            LOGGER.exception(
                "Unable to import package %s",
                package,
            )

            result.failed_modules += 1

            result.metadata.setdefault(
                "package_errors",
                {},
            )[package] = str(exc)

            return

        result.scanned_packages += 1

        #
        # Package itself
        #

        self._discover_module(
            module_name=package,
            result=result,
        )

        #
        # Child modules
        #

        if not hasattr(
            imported_package,
            "__path__",
        ):

            return

        for module in pkgutil.walk_packages(
            imported_package.__path__,
            prefix=f"{package}.",
        ):

            self._discover_module(
                module_name=module.name,
                result=result,
            )

    # ======================================================
    # MODULE DISCOVERY
    # ======================================================

    def _discover_module(
        self,
        module_name: str,
        result: DiscoveryResult,
    ) -> None:
        """
        Safely inspect one module.
        """

        LOGGER.debug(
            "Loading module %s",
            module_name,
        )

        try:

            module = importlib.import_module(
                module_name,
            )

        except Exception as exc:

            LOGGER.debug(
                "Failed loading %s\n%s",
                module_name,
                traceback.format_exc(),
            )

            result.failed_modules += 1

            result.metadata.setdefault(
                "module_errors",
                {},
            )[module_name] = str(exc)

            return

        result.scanned_modules += 1

        #
        # Inspect every class inside module
        #

        for _, cls in inspect.getmembers(
            module,
            inspect.isclass,
        ):

            #
            # Ignore imported classes
            #

            if cls.__module__ != module_name:

                continue

            #
            # Ignore private classes
            #

            if cls.__name__.startswith("_"):

                continue

            #
            # Analyzer filtering
            #

            if not self._looks_like_analyzer(
                cls,
            ):

                continue

            try:

                record = self._build_record(
                    cls,
                    module_name,
                )

                result.analyzers.append(
                    record,
                )

            except Exception:

                LOGGER.exception(
                    "Unable to build record for %s",
                    cls.__name__,
                )

    # ======================================================
    # FILTERING
    # ======================================================

    @staticmethod
    def _looks_like_analyzer(
        cls: type,
    ) -> bool:
        """
        Decide whether a class should be treated
        as an analyzer.
        """

        name = cls.__name__.lower()

        #
        # Name heuristic
        #

        if name.endswith("analyzer"):

            return True

        #
        # Base-class heuristic
        #

        for base in cls.__mro__[1:]:

            if base.__name__.lower() == "baseanalyzer":

                return True

        #
        # Interface heuristic
        #

        required = (
            "analyze",
            "calculate",
            "run",
        )

        members = set(dir(cls))

        if any(
            method in members
            for method in required
        ):

            return True

        return False

    # ------------------------------------------------------

        # ======================================================
    # RECORD BUILDER
    # ======================================================

    def _build_record(
        self,
        cls: type,
        module_name: str,
    ) -> AnalyzerRecord:
        """
        Build AnalyzerRecord from a class.
        """

        #
        # Module information
        #

        try:

            module = importlib.import_module(
                module_name,
            )

            file_path = Path(
                inspect.getfile(module)
            )

        except Exception:

            file_path = Path("<unknown>")

        #
        # Base classes
        #

        bases = [
            base.__name__
            for base in cls.__bases__
        ]

        #
        # Class methods
        #

        methods = []

        public_methods = []

        for name, member in inspect.getmembers(
            cls,
            predicate=inspect.isfunction,
        ):

            methods.append(name)

            if not name.startswith("_"):

                public_methods.append(name)

        #
        # Abstract
        #

        is_abstract = inspect.isabstract(
            cls,
        )

        #
        # Metadata
        #

        metadata = {
            "method_count": len(
                methods,
            ),
            "public_method_count": len(
                public_methods,
            ),
            "base_count": len(
                bases,
            ),
            "module": module_name,
        }

        #
        # Build record
        #

        return AnalyzerRecord(
            name=cls.__name__,
            qualified_name=f"{module_name}.{cls.__name__}",
            module=module_name,
            file_path=file_path,
            class_name=cls.__name__,
            package=module_name.split(".")[0],
            base_classes=bases,
            methods=sorted(methods),
            public_methods=sorted(public_methods),
            docstring=inspect.getdoc(cls),
            is_abstract=is_abstract,
            successfully_loaded=True,
            metadata=metadata,
        )

    # ======================================================
    # HELPERS
    # ======================================================

    @staticmethod
    def analyzer_names(
        result: DiscoveryResult,
    ) -> list[str]:
        """
        Return analyzer names.
        """

        return sorted(
            analyzer.name
            for analyzer in result.analyzers
        )

    # ------------------------------------------------------

    @staticmethod
    def modules(
        result: DiscoveryResult,
    ) -> list[str]:
        """
        Return modules containing analyzers.
        """

        return sorted(
            {
                analyzer.module
                for analyzer in result.analyzers
            }
        )

    # ------------------------------------------------------

    @staticmethod
    def packages(
        result: DiscoveryResult,
    ) -> list[str]:
        """
        Return packages.
        """

        return sorted(
            {
                analyzer.package
                for analyzer in result.analyzers
            }
        )

    # ------------------------------------------------------

    @staticmethod
    def summary(
        result: DiscoveryResult,
    ) -> dict:
        """
        Discovery summary.
        """

        return {
            "packages": result.scanned_packages,
            "modules": result.scanned_modules,
            "analyzers": result.total_analyzers,
            "successful": result.successful_analyzers,
            "failed": result.failed_analyzers,
        }