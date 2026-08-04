"""
===============================================================================
UDUAK_QUANT_SYSTEM_PROJECT
-------------------------------------------------------------------------------
File: services/database_service.py

Description:
    Business logic responsible for database lifecycle management.

Responsibilities:
    - Open database connection.
    - Close database connection.
    - Commit transactions.
    - Roll back transactions.
    - Verify database availability.
    - Produce database summary.

This module contains BUSINESS LOGIC ONLY.

It must NEVER:
    - Execute SQL directly.
    - Contain repository logic.
    - Contain trading logic.
===============================================================================
"""

from __future__ import annotations

from database.database import Database
from monitoring.logger import get_logger

logger = get_logger(__name__)


class DatabaseService:
    """
    Business logic for database management.
    """

    def __init__(self) -> None:
        """
        Initialize database service.
        """

        self._database = Database()

    # =====================================================================
    # CONNECTION
    # =====================================================================

    def connect(self) -> None:
        """
        Open the database connection.
        """

        self._database.connect()

        logger.info(
            "Database connection established."
        )

    def close(self) -> None:
        """
        Close the database connection.
        """

        self._database.close()

        logger.info(
            "Database connection closed."
        )

    # =====================================================================
    # TRANSACTIONS
    # =====================================================================

    def commit(self) -> None:
        """
        Commit current transaction.
        """

        self._database.commit()

        logger.info(
            "Database transaction committed."
        )

    def rollback(self) -> None:
        """
        Roll back current transaction.
        """

        self._database.rollback()

        logger.info(
            "Database transaction rolled back."
        )

    # =====================================================================
    # STATUS
    # =====================================================================

    def is_available(self) -> bool:
        """
        Verify that the database can be opened.
        """

        try:
            self._database.connect()
            return True

        except Exception as error:

            logger.error(
                "Database unavailable: %s",
                error,
            )

            return False

    # =====================================================================
    # INFORMATION
    # =====================================================================

    def database_file(self):
        """
        Return the database file path.
        """

        return self._database._database_file

    # =====================================================================
    # SUMMARY
    # =====================================================================

    def summary(self) -> dict:
        """
        Return database summary.
        """

        summary = {
            "database_file": str(
                self.database_file()
            ),
            "available": self.is_available(),
        }

        logger.info(
            "Database summary generated."
        )

        return summary