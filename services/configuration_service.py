"""
===============================================================================
UDUAK_QUANT_SYSTEM_PROJECT
-------------------------------------------------------------------------------
File: services/configuration_service.py

Description:
    Business logic responsible for application configuration.

Responsibilities:
    - Access project configuration
    - Validate configuration
    - Provide configuration summaries

This module contains BUSINESS LOGIC ONLY.

It must NEVER:
    - Read SQL
    - Execute trades
    - Read market data
===============================================================================
"""

from __future__ import annotations

from config.settings import settings
from monitoring.logger import get_logger

logger = get_logger(__name__)


class ConfigurationService:
    """
    Business logic for project configuration.
    """

    def __init__(self) -> None:
        """
        Initialize configuration service.
        """

        self._settings = settings

    # =====================================================================
    # PROJECT
    # =====================================================================

    def project_root(self):
        """
        Return project root directory.
        """

        return self._settings.project_root

    # =====================================================================
    # VALIDATION
    # =====================================================================

    def validate(self) -> bool:
        """
        Validate configuration.

        Returns
        -------
        bool
            True when configuration is valid.
        """

        valid = True

        if self._settings.project_root is None:
            logger.error("Project root is not configured.")
            valid = False

        return valid

    # =====================================================================
    # SUMMARY
    # =====================================================================

    def summary(self) -> dict:
        """
        Return configuration summary.
        """

        return {
            "project_root": str(self._settings.project_root),
        }