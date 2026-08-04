"""
===============================================================================
UDUAK_QUANT_SYSTEM_PROJECT
-------------------------------------------------------------------------------
File: database/migrations.py

Description:
    Database schema version management.

Responsibilities:
    - Track schema version
    - Apply migrations
    - Upgrade database
    - Prevent duplicate migrations
    - Report migration history

Contains NO trading logic.
===============================================================================
"""

from __future__ import annotations

from collections.abc import Callable

from database.database import Database
from monitoring.logger import get_logger

logger = get_logger(__name__)


Migration = Callable[[Database], None]


class DatabaseMigrations:
    """
    Handles database version upgrades.
    """

    def __init__(self) -> None:
        """
        Initialize migration manager.
        """

        self._database = Database()

        self._create_version_table()

        self._migrations: dict[int, Migration] = {
            1: self._migration_001,
        }

    # =====================================================================
    # VERSION TABLE
    # =====================================================================

    def _create_version_table(self) -> None:
        """
        Create migration table.
        """

        self._database.execute(
            """
            CREATE TABLE IF NOT EXISTS schema_version (

                version INTEGER PRIMARY KEY,

                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

            )
            """
        )

        self._database.commit()

    # =====================================================================
    # CURRENT VERSION
    # =====================================================================

    def current_version(self) -> int:
        """
        Return current schema version.
        """

        cursor = self._database.execute(
            """
            SELECT MAX(version)
            FROM schema_version
            """
        )

        version = cursor.fetchone()[0]

        return version if version is not None else 0

    # =====================================================================
    # LATEST VERSION
    # =====================================================================

    def latest_version(self) -> int:
        """
        Return newest available migration.
        """

        if not self._migrations:
            return 0

        return max(self._migrations.keys())

    # =====================================================================
    # UPGRADE
    # =====================================================================

    def upgrade(self) -> None:
        """
        Upgrade database.
        """

        current = self.current_version()

        latest = self.latest_version()

        if current >= latest:

            logger.info(
                "Database already up-to-date."
            )

            return

        logger.info(
            "Starting database migration..."
        )

        for version in sorted(self._migrations):

            if version <= current:
                continue

            logger.info(
                "Applying migration %s",
                version,
            )

            self._migrations[version](
                self._database
            )

            self._database.execute(
                """
                INSERT INTO schema_version (
                    version
                )
                VALUES (?)
                """,
                (version,),
            )

            self._database.commit()

            logger.info(
                "Migration %s complete.",
                version,
            )

        logger.info(
            "Database upgrade complete."
        )

    # =====================================================================
    # HISTORY
    # =====================================================================

    def history(self) -> list[dict]:
        """
        Return migration history.
        """

        cursor = self._database.execute(
            """
            SELECT
                version,
                applied_at
            FROM schema_version
            ORDER BY version
            """
        )

        rows = cursor.fetchall()

        return [
            {
                "version": row["version"],
                "applied_at": row["applied_at"],
            }
            for row in rows
        ]

    # =====================================================================
    # STATUS
    # =====================================================================

    def status(self) -> dict:
        """
        Return migration status.
        """

        return {
            "current_version": self.current_version(),
            "latest_version": self.latest_version(),
            "up_to_date":
                self.current_version()
                == self.latest_version(),
        }

    # =====================================================================
    # MIGRATIONS
    # =====================================================================

    def _migration_001(
        self,
        database: Database,
    ) -> None:
        """
        Initial migration.

        Future schema changes should be added
        as new migration methods.
        """

        logger.info(
            "Migration 001 executed."
        )