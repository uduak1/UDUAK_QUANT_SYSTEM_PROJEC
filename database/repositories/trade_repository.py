"""
===============================================================================
UDUAK_QUANT_SYSTEM_PROJECT
-------------------------------------------------------------------------------
File: database/repositories/trade_repository.py

Description:
    Repository responsible for all database operations related to trades.

Responsibilities:
    - Insert trades
    - Update trades
    - Delete trades
    - Retrieve trades
    - Query statistics

Business logic must NOT exist here.
===============================================================================
"""

from __future__ import annotations

from typing import Any

from database.database import Database
from monitoring.logger import get_logger

logger = get_logger(__name__)


class TradeRepository:
    """
    Repository for trade database operations.
    """

    def __init__(self) -> None:
        """
        Initialize repository.
        """

        self._database = Database()

    # =========================================================================
    # CREATE
    # =========================================================================

    def insert_trade(
        self,
        *,
        ticket: int,
        symbol: str,
        direction: str,
        strategy: str,
        volume: float,
        entry_price: float,
        stop_loss: float | None = None,
        take_profit: float | None = None,
        status: str = "OPEN",
    ) -> int:
        """
        Insert a new trade.

        Returns
        -------
        int
            Row ID.
        """

        cursor = self._database.execute(
            """
            INSERT INTO trades (

                ticket,
                symbol,
                direction,
                strategy,
                volume,
                entry_price,
                stop_loss,
                take_profit,
                status,
                opened_at

            )
            VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?,
                CURRENT_TIMESTAMP
            )
            """,
            (
                ticket,
                symbol,
                direction,
                strategy,
                volume,
                entry_price,
                stop_loss,
                take_profit,
                status,
            ),
        )

        self._database.commit()

        logger.info(
            "Inserted trade %s (%s)",
            ticket,
            symbol,
        )

        return cursor.lastrowid

    # =========================================================================
    # READ
    # =========================================================================

    def get_trade_by_ticket(
        self,
        ticket: int,
    ) -> dict[str, Any] | None:
        """
        Retrieve a trade using its MT5 ticket.
        """

        cursor = self._database.execute(
            """
            SELECT *
            FROM trades
            WHERE ticket = ?
            """,
            (ticket,),
        )

        row = cursor.fetchone()

        return dict(row) if row else None

    def get_all_trades(self) -> list[dict[str, Any]]:
        """
        Return every trade.
        """

        cursor = self._database.execute(
            """
            SELECT *
            FROM trades
            ORDER BY opened_at DESC
            """
        )

        return [dict(row) for row in cursor.fetchall()]

    def get_open_trades(self) -> list[dict[str, Any]]:
        """
        Return all open trades.
        """

        cursor = self._database.execute(
            """
            SELECT *
            FROM trades
            WHERE status='OPEN'
            ORDER BY opened_at DESC
            """
        )

        return [dict(row) for row in cursor.fetchall()]

    def get_closed_trades(self) -> list[dict[str, Any]]:
        """
        Return all closed trades.
        """

        cursor = self._database.execute(
            """
            SELECT *
            FROM trades
            WHERE status='CLOSED'
            ORDER BY closed_at DESC
            """
        )

        return [dict(row) for row in cursor.fetchall()]

    # =========================================================================
    # UPDATE
    # =========================================================================

    def close_trade(
        self,
        *,
        ticket: int,
        exit_price: float,
        profit: float,
    ) -> bool:
        """
        Mark a trade as closed.
        """

        cursor = self._database.execute(
            """
            UPDATE trades
            SET

                exit_price=?,
                profit=?,
                status='CLOSED',
                closed_at=CURRENT_TIMESTAMP

            WHERE ticket=?
            """,
            (
                exit_price,
                profit,
                ticket,
            ),
        )

        self._database.commit()

        updated = cursor.rowcount > 0

        if updated:
            logger.info(
                "Closed trade %s",
                ticket,
            )

        return updated

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
            UPDATE trades
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
            UPDATE trades
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

    # =========================================================================
    # DELETE
    # =========================================================================

    def delete_trade(
        self,
        ticket: int,
    ) -> bool:
        """
        Delete a trade.
        """

        cursor = self._database.execute(
            """
            DELETE
            FROM trades
            WHERE ticket=?
            """,
            (ticket,),
        )

        self._database.commit()

        deleted = cursor.rowcount > 0

        if deleted:
            logger.warning(
                "Deleted trade %s",
                ticket,
            )

        return deleted

    # =========================================================================
    # STATISTICS
    # =========================================================================

    def total_trades(self) -> int:
        """
        Return total number of trades.
        """

        cursor = self._database.execute(
            """
            SELECT COUNT(*)
            FROM trades
            """
        )

        return int(cursor.fetchone()[0])

    def total_profit(self) -> float:
        """
        Return cumulative profit.
        """

        cursor = self._database.execute(
            """
            SELECT COALESCE(SUM(profit),0)
            FROM trades
            """
        )

        return float(cursor.fetchone()[0])

    def win_count(self) -> int:
        """
        Number of winning trades.
        """

        cursor = self._database.execute(
            """
            SELECT COUNT(*)
            FROM trades
            WHERE profit > 0
            """
        )

        return int(cursor.fetchone()[0])

    def loss_count(self) -> int:
        """
        Number of losing trades.
        """

        cursor = self._database.execute(
            """
            SELECT COUNT(*)
            FROM trades
            WHERE profit < 0
            """
        )

        return int(cursor.fetchone()[0])

    def win_rate(self) -> float:
        """
        Calculate win rate percentage.
        """

        total = self.total_trades()

        if total == 0:
            return 0.0

        return (self.win_count() / total) * 100.0