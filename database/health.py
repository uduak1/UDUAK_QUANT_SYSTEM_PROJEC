"""
===============================================================================
UDUAK_QUANT_SYSTEM_PROJECT
-------------------------------------------------------------------------------
File: database/health.py

Description:
    Database health monitoring.

Responsibilities:
    - Verify connectivity
    - Verify integrity
    - Monitor database size
    - Monitor table growth
    - Report overall database health

Contains NO trading logic.
===============================================================================
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from database.database import Database
from database.maintenance import DatabaseMaintenance
from monitoring.logger import get_logger

logger = get_logger(__name__)


class DatabaseHealth:
    """
    Database health monitoring.
    """

    def __init__(self) -> None:
        """
        Initialize health monitor.
        """

        self._database = Database()

        self._maintenance = DatabaseMaintenance()

    # =====================================================================
    # CONNECTION
    # =====================================================================

    def connection_ok(self) -> bool:
        """
        Verify database connection.
        """

        try:

            cursor = self._database.execute(
                """
                SELECT 1;
                """
            )

            return cursor.fetchone()[0] == 1

        except Exception as error:

            logger.exception(error)

            return False

    # =====================================================================
    # INTEGRITY
    # =====================================================================

    def integrity_ok(self) -> bool:
        """
        Verify database integrity.
        """

        return self._maintenance.integrity_check()

    # =====================================================================
    # QUICK CHECK
    # =====================================================================

    def quick_check(self) -> bool:
        """
        Execute SQLite quick check.
        """

        return self._maintenance.quick_check()

    # =====================================================================
    # DATABASE SIZE
    # =====================================================================

    def database_size(self) -> int:
        """
        Return database size.
        """

        return self._maintenance.database_size()

    # =====================================================================
    # TABLE COUNTS
    # =====================================================================

    def table_counts(self) -> dict[str, int]:
        """
        Return table statistics.
        """

        return self._maintenance.table_counts()

    # =====================================================================
    # HEALTH SCORE
    # =====================================================================

    def health_score(self) -> int:
        """
        Calculate health score.

        Score:
            100 = Excellent
             75 = Warning
             50 = Poor
              0 = Critical
        """

        score = 100

        if not self.connection_ok():
            score -= 50

        if not self.quick_check():
            score -= 25

        if not self.integrity_ok():
            score -= 25

        return max(score, 0)

    # =====================================================================
    # STATUS
    # =====================================================================

    def status(self) -> str:
        """
        Return readable health status.
        """

        score = self.health_score()

        if score == 100:
            return "HEALTHY"

        if score >= 75:
            return "WARNING"

        if score >= 50:
            return "POOR"

        return "CRITICAL"

    # =====================================================================
    # FULL REPORT
    # =====================================================================

    def report(self) -> dict[str, Any]:
        """
        Return complete health report.
        """

        return {
            "generated_at": datetime.utcnow().isoformat(),
            "status": self.status(),
            "health_score": self.health_score(),
            "connection": self.connection_ok(),
            "integrity": self.integrity_ok(),
            "quick_check": self.quick_check(),
            "database_size_bytes": self.database_size(),
            "tables": self.table_counts(),
        }

    # =====================================================================
    # PRINT REPORT
    # =====================================================================

    def print_report(self) -> None:
        """
        Print health report.
        """

        report = self.report()

        logger.info(
            "================================================"
        )

        logger.info(
            "DATABASE HEALTH REPORT"
        )

        logger.info(
            "================================================"
        )

        for key, value in report.items():

            logger.info(
                "%s : %s",
                key,
                value,
            )

        logger.info(
            "================================================"
        )