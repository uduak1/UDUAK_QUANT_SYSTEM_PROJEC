"""
===============================================================================
UDUAK_QUANT_SYSTEM_PROJECT
-------------------------------------------------------------------------------
File: database/database.py

Description:
    Central SQLite database manager.

Responsibilities:
    - Initialize storage.
    - Create database connection.
    - Execute SQL safely.
    - Manage transactions.
    - Fetch query results.
    - Close connections cleanly.

This module must remain generic.
Business logic belongs inside repository classes.
===============================================================================
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

from config.storage import initialize_storage
from config.storage import storage
from monitoring.logger import get_logger


logger = get_logger(__name__)


class Database:
    """
    SQLite database manager.

    A single Database object owns one SQLite connection.

    Example
    -------
    >>> with Database() as db:
    ...     db.execute("CREATE TABLE test(id INTEGER)")
    """

    def __init__(self) -> None:
        """
        Create database manager.

        The database connection is not opened until connect()
        is called.
        """

        initialize_storage()

        self._database_file: Path = storage.database_file

        self._connection: sqlite3.Connection | None = None

    # =========================================================================
    # CONNECTION
    # =========================================================================

    def connect(self) -> sqlite3.Connection:
        """
        Open SQLite connection.

        Returns
        -------
        sqlite3.Connection
        """

        if self._connection is not None:
            return self._connection

        logger.info("Opening database: %s", self._database_file)

        self._connection = sqlite3.connect(self._database_file)

        self._connection.row_factory = sqlite3.Row

        return self._connection

    # =========================================================================
    # EXECUTE
    # =========================================================================

    def execute(
        self,
        query: str,
        parameters: tuple[Any, ...] = (),
    ) -> sqlite3.Cursor:
        """
        Execute one SQL statement.
        """

        connection = self.connect()

        cursor = connection.cursor()

        cursor.execute(query, parameters)

        return cursor

    # =========================================================================
    # EXECUTEMANY
    # =========================================================================

    def executemany(
        self,
        query: str,
        parameters: list[tuple[Any, ...]],
    ) -> sqlite3.Cursor:
        """
        Execute many SQL statements.
        """

        connection = self.connect()

        cursor = connection.cursor()

        cursor.executemany(query, parameters)

        return cursor

    # =========================================================================
    # FETCH ONE
    # =========================================================================

    def fetch_one(
        self,
        query: str,
        parameters: tuple[Any, ...] = (),
    ) -> sqlite3.Row | None:
        """
        Execute query and return one row.
        """

        return self.execute(
            query,
            parameters,
        ).fetchone()

    # =========================================================================
    # FETCH ALL
    # =========================================================================

    def fetch_all(
        self,
        query: str,
        parameters: tuple[Any, ...] = (),
    ) -> list[sqlite3.Row]:
        """
        Execute query and return all rows.
        """

        return self.execute(
            query,
            parameters,
        ).fetchall()

    # =========================================================================
    # COMMIT
    # =========================================================================

    def commit(self) -> None:
        """
        Commit current transaction.
        """

        if self._connection is not None:
            self._connection.commit()

    # =========================================================================
    # ROLLBACK
    # =========================================================================

    def rollback(self) -> None:
        """
        Roll back current transaction.
        """

        if self._connection is not None:
            self._connection.rollback()

    # =========================================================================
    # CLOSE
    # =========================================================================

    def close(self) -> None:
        """
        Close database connection.
        """

        if self._connection is None:
            return

        logger.info("Closing database.")

        self._connection.close()

        self._connection = None

    # =========================================================================
    # CONTEXT MANAGER
    # =========================================================================

    def __enter__(self) -> "Database":
        """
        Enter context manager.
        """

        self.connect()

        return self

    def __exit__(
        self,
        exc_type,
        exc,
        traceback,
    ) -> None:
        """
        Exit context manager.
        """

        if exc is None:
            self.commit()
        else:
            self.rollback()

        self.close()