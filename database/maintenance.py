"""
===============================================================================
UDUAK_QUANT_SYSTEM_PROJECT
-------------------------------------------------------------------------------
File: database/maintenance.py

Description:
    Database maintenance utilities.

Responsibilities:
    - Optimize the database
    - Verify database integrity
    - Analyze database statistics
    - Clean old data
    - Report maintenance information

This module contains NO trading logic.
===============================================================================
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from database.database import Database
from monitoring.logger import get_logger

logger = get_logger(__name__)


class DatabaseMaintenance:
    """
    Handles routine database maintenance.
    """

    def __init__(self) -> None:
        """
        Initialize maintenance service.
        """

        self._database = Database()

    # =====================================================================
    # VACUUM
    # =====================================================================

    def vacuum(self) -> None:
        """
        Optimize database size and storage.
        """

        logger.info("Running VACUUM...")

        self._database.execute(
            """
            VACUUM
            """
        )

        logger.info("VACUUM completed.")

    # =====================================================================
    # ANALYZE
    # =====================================================================

    def analyze(self) -> None:
        """
        Refresh SQLite query statistics.
        """

        logger.info("Running ANALYZE...")

        self._database.execute(
            """
            ANALYZE
            """
        )

        logger.info("ANALYZE completed.")

    # =====================================================================
    # INTEGRITY CHECK
    # =====================================================================

    def integrity_check(self) -> bool:
        """
        Verify database integrity.
        """

        cursor = self._database.execute(
            """
            PRAGMA integrity_check;
            """
        )

        result = cursor.fetchone()[0]

        healthy = result == "ok"

        if healthy:
            logger.info(
                "Database integrity check passed."
            )
        else:
            logger.error(
                "Database integrity check failed: %s",
                result,
            )

        return healthy

    # =====================================================================
    # QUICK CHECK
    # =====================================================================

    def quick_check(self) -> bool:
        """
        Fast integrity check.
        """

        cursor = self._database.execute(
            """
            PRAGMA quick_check;
            """
        )

        result = cursor.fetchone()[0]

        return result == "ok"

    # =====================================================================
    # DELETE OLD SIGNALS
    # =====================================================================

    def purge_old_signals(
        self,
        before_timestamp: str,
    ) -> int:
        """
        Delete old signals.
        """

        cursor = self._database.execute(
            """
            DELETE
            FROM signals
            WHERE created_at < ?
            """,
            (
                before_timestamp,
            ),
        )

        self._database.commit()

        deleted = cursor.rowcount

        logger.info(
            "Deleted %s old signals.",
            deleted,
        )

        return deleted

    # =====================================================================
    # DELETE OLD MARKET DATA
    # =====================================================================

    def purge_old_market_data(
        self,
        before_timestamp: str,
    ) -> int:
        """
        Delete historical candles.
        """

        cursor = self._database.execute(
            """
            DELETE
            FROM market_data
            WHERE candle_time < ?
            """,
            (
                before_timestamp,
            ),
        )

        self._database.commit()

        deleted = cursor.rowcount

        logger.info(
            "Deleted %s market candles.",
            deleted,
        )

        return deleted

    # =====================================================================
    # DATABASE SIZE
    # =====================================================================

    def page_count(self) -> int:
        """
        Return SQLite page count.
        """

        cursor = self._database.execute(
            """
            PRAGMA page_count;
            """
        )

        return int(cursor.fetchone()[0])

    def page_size(self) -> int:
        """
        Return SQLite page size.
        """

        cursor = self._database.execute(
            """
            PRAGMA page_size;
            """
        )

        return int(cursor.fetchone()[0])

    def database_size(self) -> int:
        """
        Approximate database size in bytes.
        """

        return self.page_count() * self.page_size()

    # =====================================================================
    # TABLE COUNTS
    # =====================================================================

    def table_counts(self) -> dict[str, int]:
        """
        Return record count for every table.
        """

        tables = (
            "signals",
            "trades",
            "positions",
            "market_data",
        )

        counts: dict[str, int] = {}

        for table in tables:

            cursor = self._database.execute(
                f"""
                SELECT COUNT(*)
                FROM {table}
                """
            )

            counts[table] = int(
                cursor.fetchone()[0]
            )

        return counts

    # =====================================================================
    # MAINTENANCE REPORT
    # =====================================================================

    def report(self) -> dict[str, Any]:
        """
        Return maintenance report.
        """

        return {
            "generated_at": datetime.utcnow().isoformat(),
            "integrity_ok": self.integrity_check(),
            "quick_check": self.quick_check(),
            "database_size_bytes": self.database_size(),
            "page_count": self.page_count(),
            "page_size": self.page_size(),
            "tables": self.table_counts(),
        }

    # =====================================================================
    # FULL MAINTENANCE
    # =====================================================================

    def run(self) -> dict[str, Any]:
        """
        Execute complete maintenance routine.
        """

        logger.info(
            "Starting database maintenance..."
        )

        self.analyze()

        self.vacuum()

        report = self.report()

        logger.info(
            "Database maintenance completed."
        )

        return report