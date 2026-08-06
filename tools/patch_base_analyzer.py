from pathlib import Path
import textwrap

TARGET = Path("core/base_analyzer.py")

TARGET.write_text(
    textwrap.dedent(
        '''\
        """
        core/base_analyzer.py

        UDUAK QUANT SYSTEM
        Institutional Base Analyzer
        """

        from __future__ import annotations

        from abc import ABC, abstractmethod
        from typing import Any, Dict

        from core.analyzer_result import AnalyzerResult


        class BaseAnalyzer(ABC):
            """
            Base class for every analyzer.
            """

            def __init__(
                self,
                name: str,
                version: str = "1.0.0",
                enabled: bool = True,
            ) -> None:
                self._name = name
                self._version = version
                self._enabled = enabled

            # ==========================================================
            # PROPERTIES
            # ==========================================================

            @property
            def name(self) -> str:
                return self._name

            @property
            def version(self) -> str:
                return self._version

            @property
            def enabled(self) -> bool:
                return self._enabled

            # ==========================================================
            # CONTROL
            # ==========================================================

            def enable(self) -> None:
                self._enabled = True

            def disable(self) -> None:
                self._enabled = False

            # ==========================================================
            # INITIALIZATION
            # ==========================================================

            def initialize(self) -> bool:
                return True

            # ==========================================================
            # HEALTH
            # ==========================================================

            def health_check(self) -> bool:
                return True

            # ==========================================================
            # COMMON VALIDATION HELPERS
            # ==========================================================

            @staticmethod
            def validate_not_none(market_data: Any) -> bool:
                return market_data is not None

            @staticmethod
            def validate_not_empty(market_data: Any) -> bool:
                if market_data is None:
                    return False

                empty = getattr(market_data, "empty", None)

                if empty is not None:
                    return not empty

                try:
                    return len(market_data) > 0
                except TypeError:
                    return True

            # ==========================================================
            # REQUIRED METHODS
            # ==========================================================

            @abstractmethod
            def validate(
                self,
                market_data: Any,
            ) -> bool:
                """
                Validate input before analysis.
                """
                raise NotImplementedError

            @abstractmethod
            def analyze(
                self,
                market_data: Any,
            ) -> AnalyzerResult:
                """
                Execute analyzer logic.
                """
                raise NotImplementedError

            # ==========================================================
            # INFORMATION
            # ==========================================================

            def metadata(self) -> Dict[str, Any]:
                return {
                    "name": self.name,
                    "version": self.version,
                    "enabled": self.enabled,
                }

            # ==========================================================
            # REPRESENTATION
            # ==========================================================

            def __repr__(self) -> str:
                return (
                    f"{self.__class__.__name__}("
                    f"name='{self.name}', "
                    f"version='{self.version}', "
                    f"enabled={self.enabled})"
                )
        '''
    ),
    encoding="utf-8",
)

print("✓ BaseAnalyzer completely rebuilt.")