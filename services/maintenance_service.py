"""
===============================================================================
UDUAK_QUANT_SYSTEM_PROJECT
-------------------------------------------------------------------------------
File: services/maintenance_service.py

Description:
    Business logic responsible for database maintenance operations.

Responsibilities:
    - Execute database maintenance
    - Validate database integrity
    - Optimize database
    - Remove obsolete records
    - Produce maintenance reports

This module contains BUSINESS LOGIC ONLY.

It must NEVER:
    - Execute SQL directly.
    - Contain repository logic.
    - Contain trading logic.
===============================================================================
"""

from __future__ import annotations

from typing import Any

from database.maintenance import DatabaseMaintenance
from monitoring.logger import get_logger

logger = get_logger(__name__)


class MaintenanceService:
    """
    Business logic for database maintenance.
    """

    def __init__(self) -> None:
        """
        Initialize maintenance service.
        """

        self._maintenance = DatabaseMaintenance()

    # =========================================================================
    # DATABASE OPTIMIZATION
    # =========================================================================

    def vacuum(self) -> None:
        """
        Optimize the database.
        """

        self._maintenance.vacuum()

        logger.info(
            "Database vacuum completed."
        )

    def analyze(self) -> None:
        """
        Refresh SQLite statistics.
        """

        self._maintenance.analyze()

        logger.info(
            "Database analysis completed."
        )

    # =========================================================================
    # DATABASE HEALTH
    # =========================================================================

    def integrity_check(self) -> bool:
        """
        Verify database integrity.
        """

        return self._maintenance.integrity_check()

    def quick_check(self) -> bool:
        """
        Perform a quick database integrity check.
        """

        return self._maintenance.quick_check()

    # =========================================================================
    # CLEANUP
    # =========================================================================

    def purge_old_signals(
        self,
        before_timestamp: str,
    ) -> int:
        """
        Remove old trading signals.
        """

        deleted = self._maintenance.purge_old_signals(
            before_timestamp
        )

        logger.info(
            "Purged %s old signals.",
            deleted,
        )

        return deleted

    def purge_old_market_data(
        self,
        before_timestamp: str,
    ) -> int:
        """
        Remove historical market data.
        """

        deleted = self._maintenance.purge_old_market_data(
            before_timestamp
        )

        logger.info(
            "Purged %s historical candles.",
            deleted,
        )

        return deleted

    # =========================================================================
    # DATABASE INFORMATION
    # =========================================================================

    def database_size(self) -> int:
        """
        Return database size in bytes.
        """

        return self._maintenance.database_size()

    def table_counts(self) -> dict[str, int]:
        """
        Return table record counts.
        """

        return self._maintenance.table_counts()

    # =========================================================================
    # REPORTING
    # =========================================================================

    def report(self) -> dict[str, Any]:
        """
        Return maintenance report.
        """

        report = self._maintenance.report()

        logger.info(
            "Maintenance report generated."
        )

        return report

    # =========================================================================
    # COMPLETE MAINTENANCE
    # =========================================================================

    def run(self) -> dict[str, Any]:
        """
        Execute the complete maintenance routine.
        """

        logger.info(
            "Running maintenance service."
        )

        report = self._maintenance.run()

        logger.info(
            "Maintenance service completed."
        )

        return report