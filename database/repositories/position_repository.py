"""
===============================================================================
UDUAK_QUANT_SYSTEM_PROJECT
-------------------------------------------------------------------------------
File: database/repositories/position_repository.py

Description:
    Repository responsible for database operations related to
    currently open trading positions.
===============================================================================
"""

from __future__ import annotations

from typing import Any

from database.database import Database
from monitoring.logger import get_logger

logger = get_logger(__name__)


class PositionRepository:
    """
    Repository for open positions.
    """

    def __init__(self) -> None:
        self._database = Database()

    # =====================================================================
    # CREATE
    # =====================================================================

    def insert_position(
        self,
        *,
        ticket: int,
        symbol: str,
        direction: str,
        volume: float,
        entry_price: float,
        stop_loss: float | None = None,
        take_profit: float | None = None,
        strategy: str | None = None,
    ) -> int:
        """
        Store an open position.
        """

        cursor = self._database.execute(
            """
            INSERT INTO positions (

                ticket,
                symbol,
                direction,
                volume,
                entry_price,
                stop_loss,
                take_profit,
                strategy,
                opened_at

            )
            VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?,
                CURRENT_TIMESTAMP
            )
            """,
            (
                ticket,
                symbol,
                direction,
                volume,
                entry_price,
                stop_loss,
                take_profit,
                strategy,
            ),
        )

        self._database.commit()

        logger.info(
            "Inserted position %s",
            ticket,
        )

        return cursor.lastrowid

    # =====================================================================
    # READ
    # =====================================================================

    def get_position(
        self,
        ticket: int,
    ) -> dict[str, Any] | None:
        """
        Get a position by ticket.
        """

        cursor = self._database.execute(
            """
            SELECT *
            FROM positions
            WHERE ticket=?
            """,
            (ticket,),
        )

        row = cursor.fetchone()

        return dict(row) if row else None

    def get_all_positions(self) -> list[dict[str, Any]]:
        """
        Return every open position.
        """

        cursor = self._database.execute(
            """
            SELECT *
            FROM positions
            ORDER BY opened_at DESC
            """
        )

        return [dict(row) for row in cursor.fetchall()]

    def get_positions_by_symbol(
        self,
        symbol: str,
    ) -> list[dict[str, Any]]:
        """
        Return positions for one symbol.
        """

        cursor = self._database.execute(
            """
            SELECT *
            FROM positions
            WHERE symbol=?
            ORDER BY opened_at DESC
            """,
            (symbol,),
        )

        return [dict(row) for row in cursor.fetchall()]

    # =====================================================================
    # UPDATE
    # =====================================================================

    def update_stop_loss(
        self,
        *,
        ticket: int,
        stop_loss: float,
    ) -> bool:
        """
        Update stop loss.
        """

        cursor = self._database.execute(
            """
            UPDATE positions
            SET stop_loss=?
            WHERE ticket=?
            """,
            (
                stop_loss,
                ticket,
            ),
        )

        self._database.commit()

        return cursor.rowcount > 0

    def update_take_profit(
        self,
        *,
        ticket: int,
        take_profit: float,
    ) -> bool:
        """
        Update take profit.
        """

        cursor = self._database.execute(
            """
            UPDATE positions
            SET take_profit=?
            WHERE ticket=?
            """,
            (
                take_profit,
                ticket,
            ),
        )

        self._database.commit()

        return cursor.rowcount > 0

    def update_volume(
        self,
        *,
        ticket: int,
        volume: float,
    ) -> bool:
        """
        Update remaining position volume.
        """

        cursor = self._database.execute(
            """
            UPDATE positions
            SET volume=?
            WHERE ticket=?
            """,
            (
                volume,
                ticket,
            ),
        )

        self._database.commit()

        return cursor.rowcount > 0

    # =====================================================================
    # DELETE
    # =====================================================================

    def remove_position(
        self,
        ticket: int,
    ) -> bool:
        """
        Remove a closed position.
        """

        cursor = self._database.execute(
            """
            DELETE
            FROM positions
            WHERE ticket=?
            """,
            (ticket,),
        )

        self._database.commit()

        deleted = cursor.rowcount > 0

        if deleted:
            logger.info(
                "Removed position %s",
                ticket,
            )

        return deleted

    # =====================================================================
    # STATISTICS
    # =====================================================================

    def total_positions(self) -> int:
        """
        Return number of open positions.
        """

        cursor = self._database.execute(
            """
            SELECT COUNT(*)
            FROM positions
            """
        )

        return int(cursor.fetchone()[0])

    def total_volume(self) -> float:
        """
        Return total open volume.
        """

        cursor = self._database.execute(
            """
            SELECT COALESCE(SUM(volume),0)
            FROM positions
            """
        )

        return float(cursor.fetchone()[0])