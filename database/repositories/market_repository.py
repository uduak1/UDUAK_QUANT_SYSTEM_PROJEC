"""
===============================================================================
UDUAK_QUANT_SYSTEM_PROJECT
-------------------------------------------------------------------------------
File: database/repositories/market_repository.py

Description:
    Repository responsible for storing and retrieving market data.

Responsibilities:
    - Store historical candles
    - Retrieve historical candles
    - Delete old candles
    - Query market statistics

This repository contains NO trading logic.
===============================================================================
"""

from __future__ import annotations

from typing import Any

from database.database import Database
from monitoring.logger import get_logger

logger = get_logger(__name__)


class MarketRepository:
    """
    Repository for historical market data.
    """

    def __init__(self) -> None:
        """
        Initialize repository.
        """

        self._database = Database()

    # =====================================================================
    # CREATE
    # =====================================================================

    def insert_candle(
        self,
        *,
        symbol: str,
        timeframe: str,
        candle_time: str,
        open_price: float,
        high_price: float,
        low_price: float,
        close_price: float,
        tick_volume: int,
        spread: int = 0,
        real_volume: int = 0,
    ) -> int:
        """
        Store a single historical candle.
        """

        cursor = self._database.execute(
            """
            INSERT INTO market_data (

                symbol,
                timeframe,
                candle_time,
                open_price,
                high_price,
                low_price,
                close_price,
                tick_volume,
                spread,
                real_volume

            )
            VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
            """,
            (
                symbol,
                timeframe,
                candle_time,
                open_price,
                high_price,
                low_price,
                close_price,
                tick_volume,
                spread,
                real_volume,
            ),
        )

        self._database.commit()

        return cursor.lastrowid

    # =====================================================================
    # READ
    # =====================================================================

    def get_candle(
        self,
        *,
        symbol: str,
        timeframe: str,
        candle_time: str,
    ) -> dict[str, Any] | None:
        """
        Retrieve a single candle.
        """

        cursor = self._database.execute(
            """
            SELECT *
            FROM market_data
            WHERE symbol=?
            AND timeframe=?
            AND candle_time=?
            """,
            (
                symbol,
                timeframe,
                candle_time,
            ),
        )

        row = cursor.fetchone()

        return dict(row) if row else None

    def get_recent_candles(
        self,
        *,
        symbol: str,
        timeframe: str,
        limit: int = 500,
    ) -> list[dict[str, Any]]:
        """
        Return the newest candles.
        """

        cursor = self._database.execute(
            """
            SELECT *
            FROM market_data
            WHERE symbol=?
            AND timeframe=?
            ORDER BY candle_time DESC
            LIMIT ?
            """,
            (
                symbol,
                timeframe,
                limit,
            ),
        )

        return [dict(row) for row in cursor.fetchall()]

    def get_candles_between(
        self,
        *,
        symbol: str,
        timeframe: str,
        start_time: str,
        end_time: str,
    ) -> list[dict[str, Any]]:
        """
        Return candles inside a time range.
        """

        cursor = self._database.execute(
            """
            SELECT *
            FROM market_data
            WHERE symbol=?
            AND timeframe=?
            AND candle_time BETWEEN ? AND ?
            ORDER BY candle_time ASC
            """,
            (
                symbol,
                timeframe,
                start_time,
                end_time,
            ),
        )

        return [dict(row) for row in cursor.fetchall()]

    # =====================================================================
    # DELETE
    # =====================================================================

    def delete_symbol(
        self,
        symbol: str,
    ) -> bool:
        """
        Delete every candle for one symbol.
        """

        cursor = self._database.execute(
            """
            DELETE
            FROM market_data
            WHERE symbol=?
            """,
            (symbol,),
        )

        self._database.commit()

        deleted = cursor.rowcount > 0

        if deleted:
            logger.info(
                "Deleted market history for %s",
                symbol,
            )

        return deleted

    def delete_before(
        self,
        *,
        symbol: str,
        timeframe: str,
        before_time: str,
    ) -> bool:
        """
        Delete old candles.
        """

        cursor = self._database.execute(
            """
            DELETE
            FROM market_data
            WHERE symbol=?
            AND timeframe=?
            AND candle_time < ?
            """,
            (
                symbol,
                timeframe,
                before_time,
            ),
        )

        self._database.commit()

        return cursor.rowcount > 0

    # =====================================================================
    # STATISTICS
    # =====================================================================

    def total_candles(self) -> int:
        """
        Return total candles stored.
        """

        cursor = self._database.execute(
            """
            SELECT COUNT(*)
            FROM market_data
            """
        )

        return int(cursor.fetchone()[0])

    def candle_count(
        self,
        *,
        symbol: str,
        timeframe: str,
    ) -> int:
        """
        Return candles for one symbol/timeframe.
        """

        cursor = self._database.execute(
            """
            SELECT COUNT(*)
            FROM market_data
            WHERE symbol=?
            AND timeframe=?
            """,
            (
                symbol,
                timeframe,
            ),
        )

        return int(cursor.fetchone()[0])

    def oldest_candle(
        self,
        *,
        symbol: str,
        timeframe: str,
    ) -> str | None:
        """
        Return oldest candle timestamp.
        """

        cursor = self._database.execute(
            """
            SELECT MIN(candle_time)
            FROM market_data
            WHERE symbol=?
            AND timeframe=?
            """,
            (
                symbol,
                timeframe,
            ),
        )

        return cursor.fetchone()[0]

    def newest_candle(
        self,
        *,
        symbol: str,
        timeframe: str,
    ) -> str | None:
        """
        Return newest candle timestamp.
        """

        cursor = self._database.execute(
            """
            SELECT MAX(candle_time)
            FROM market_data
            WHERE symbol=?
            AND timeframe=?
            """,
            (
                symbol,
                timeframe,
            ),
        )

        return cursor.fetchone()[0]

    # =====================================================================
    # DASHBOARD SUMMARY
    # =====================================================================

    def summary(
        self,
        *,
        symbol: str,
        timeframe: str,
    ) -> dict[str, Any]:
        """
        Return market storage summary.
        """

        return {
            "symbol": symbol,
            "timeframe": timeframe,
            "candles": self.candle_count(
                symbol=symbol,
                timeframe=timeframe,
            ),
            "oldest": self.oldest_candle(
                symbol=symbol,
                timeframe=timeframe,
            ),
            "newest": self.newest_candle(
                symbol=symbol,
                timeframe=timeframe,
            ),
        }