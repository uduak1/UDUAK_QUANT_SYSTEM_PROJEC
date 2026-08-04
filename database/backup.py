"""
===============================================================================
UDUAK_QUANT_SYSTEM_PROJECT
-------------------------------------------------------------------------------
File: database/backup.py

Description:
    Database backup utilities.

Responsibilities:
    - Create timestamped backups
    - Restore backups
    - List available backups

No trading logic belongs here.
===============================================================================
"""

from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path

from config.storage import storage
from monitoring.logger import get_logger

logger = get_logger(__name__)


class DatabaseBackup:
    """
    Handles database backups.
    """

    def __init__(self) -> None:

        self.database_file = storage.database_file

        self.backup_directory = (
            storage.database_dir / "backups"
        )

        self.backup_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    # =====================================================================
    # CREATE BACKUP
    # =====================================================================

    def create_backup(self) -> Path:
        """
        Create timestamped database backup.
        """

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        backup_file = (
            self.backup_directory
            / f"uduak_quant_{timestamp}.db"
        )

        shutil.copy2(
            self.database_file,
            backup_file,
        )

        logger.info(
            "Database backup created: %s",
            backup_file,
        )

        return backup_file

    # =====================================================================
    # RESTORE
    # =====================================================================

    def restore_backup(
        self,
        backup_file: Path,
    ) -> None:
        """
        Restore selected backup.
        """

        shutil.copy2(
            backup_file,
            self.database_file,
        )

        logger.info(
            "Database restored from %s",
            backup_file,
        )

    # =====================================================================
    # LIST BACKUPS
    # =====================================================================

    def backups(self) -> list[Path]:
        """
        Return available backups.
        """

        return sorted(
            self.backup_directory.glob("*.db"),
            reverse=True,
        )

    # =====================================================================
    # LATEST BACKUP
    # =====================================================================

    def latest_backup(self) -> Path | None:
        """
        Return newest backup.
        """

        backups = self.backups()

        if not backups:
            return None

        return backups[0]

    # =====================================================================
    # DELETE BACKUP
    # =====================================================================

    def delete_backup(
        self,
        backup_file: Path,
    ) -> bool:
        """
        Delete backup file.
        """

        if not backup_file.exists():
            return False

        backup_file.unlink()

        logger.info(
            "Deleted backup %s",
            backup_file,
        )

        return True