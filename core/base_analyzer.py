"""
core/base_analyzer.py

UDUAK QUANT SYSTEM
Institutional Base Analyzer

Every analyzer in the system MUST inherit from this class.

Responsibilities
----------------
- Standardize analyzer interface
- Validate input
- Execute analysis
- Perform health checks
- Report metadata
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseAnalyzer(ABC):
    """
    Base class for every analyzer.

    Required methods:

        validate()
        analyze()

    Optional methods:

        initialize()
        health_check()
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
        """Analyzer name."""
        return self._name

    @property
    def version(self) -> str:
        """Analyzer version."""
        return self._version

    @property
    def enabled(self) -> bool:
        """Whether analyzer is enabled."""
        return self._enabled

    # ==========================================================
    # CONTROL
    # ==========================================================

    def enable(self) -> None:
        """Enable analyzer."""
        self._enabled = True

    def disable(self) -> None:
        """Disable analyzer."""
        self._enabled = False

    # ==========================================================
    # INITIALIZATION
    # ==========================================================

    def initialize(self) -> bool:
        """
        Optional initialization.

        Override if analyzer requires startup logic.
        """
        return True

    # ==========================================================
    # HEALTH
    # ==========================================================

    def health_check(self) -> bool:
        """
        Analyzer health check.

        Override if analyzer depends on
        external resources.
        """
        return True

    # ==========================================================
    # REQUIRED METHODS
    # ==========================================================

    @abstractmethod
    def validate(
        self,
        market_snapshot: Dict[str, Any],
    ) -> bool:
        """
        Validate input before analysis.
        """
        raise NotImplementedError

    @abstractmethod
    def analyze(
        self,
        market_snapshot: Dict[str, Any],
    ) -> Any:
        """
        Execute analyzer logic.
        """
        raise NotImplementedError

    # ==========================================================
    # INFORMATION
    # ==========================================================

    def metadata(self) -> Dict[str, Any]:
        """
        Analyzer metadata.
        """
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