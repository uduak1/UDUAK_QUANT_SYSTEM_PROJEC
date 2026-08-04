"""
===============================================================================
UDUAK_QUANT_SYSTEM_PROJECT
-------------------------------------------------------------------------------
File: services/storage_service.py

Description:
    Business logic responsible for project storage management.

Responsibilities:
    - Initialize storage directories
    - Validate storage configuration
    - Provide storage locations
    - Produce storage summaries

This module contains BUSINESS LOGIC ONLY.

It must NEVER:
    - Execute SQL.
    - Execute trades.
    - Read market data.
===============================================================================
"""

from __future__ import annotations

from monitoring.logger import get_logger
from storage import initialize_storage, storage

logger = get_logger(__name__)


class StorageService:
    """
    Business logic for project storage.
    """

    def __init__(self) -> None:
        """
        Initialize storage service.
        """

        self._storage = storage

    # =========================================================================
    # INITIALIZATION
    # =========================================================================

    def initialize(self) -> None:
        """
        Initialize all project directories.
        """

        initialize_storage()

        logger.info(
            "Project storage initialized successfully."
        )

    # =========================================================================
    # VALIDATION
    # =========================================================================

    def validate(self) -> bool:
        """
        Verify that all required directories exist.
        """

        directories = [
            self._storage.data_dir,
            self._storage.historical_data_dir,
            self._storage.backtests_dir,
            self._storage.database_dir,
            self._storage.logs_dir,
            self._storage.reports_dir,
            self._storage.exports_dir,
            self._storage.cache_dir,
            self._storage.models_dir,
        ]

        valid = all(directory.exists() for directory in directories)

        if valid:
            logger.info(
                "Storage validation successful."
            )
        else:
            logger.error(
                "Storage validation failed."
            )

        return valid

    # =========================================================================
    # PATH ACCESS
    # =========================================================================

    def project_root(self):
        """
        Return project root directory.
        """

        return self._storage.project_root

    def database_file(self):
        """
        Return database file path.
        """

        return self._storage.database_file

    def logs_directory(self):
        """
        Return logs directory.
        """

        return self._storage.logs_dir

    def reports_directory(self):
        """
        Return reports directory.
        """

        return self._storage.reports_dir

    def exports_directory(self):
        """
        Return exports directory.
        """

        return self._storage.exports_dir

    def historical_directory(self):
        """
        Return historical data directory.
        """

        return self._storage.historical_data_dir

    def models_directory(self):
        """
        Return models directory.
        """

        return self._storage.models_dir

    # =========================================================================
    # SUMMARY
    # =========================================================================

    def summary(self) -> dict:
        """
        Return storage summary.
        """

        summary = {
            "project_root": str(self._storage.project_root),
            "data_dir": str(self._storage.data_dir),
            "database_file": str(self._storage.database_file),
            "logs_dir": str(self._storage.logs_dir),
            "reports_dir": str(self._storage.reports_dir),
            "exports_dir": str(self._storage.exports_dir),
            "cache_dir": str(self._storage.cache_dir),
            "models_dir": str(self._storage.models_dir),
            "storage_valid": self.validate(),
        }

        logger.info(
            "Storage summary generated."
        )

        return summary