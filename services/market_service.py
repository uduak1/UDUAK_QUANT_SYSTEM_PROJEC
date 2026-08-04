"""
===============================================================================
UDUAK_QUANT_SYSTEM_PROJECT
-------------------------------------------------------------------------------
File: services/market_service.py

Description:
    Business logic responsible for market data management.

Responsibilities:
    - Store market candles
    - Retrieve historical candles
    - Validate market data
    - Delete historical data
    - Produce market summaries

This module contains BUSINESS LOGIC ONLY.

It must NEVER contain SQL.
===============================================================================
"""

from __future__ import annotations

from typing import Any

from database.repositories.market_repository import MarketRepository
from monitoring.logger import get_logger

logger = get_logger(__name__)


class MarketService:
    """
    Business logic for historical market data.
    """

    def __init__(self) -> None:
        """
        Initialize service.
        """

        self._repository = MarketRepository()

    # =========================================================================
    # STORE
    # =========================================================================

    def store_candle(
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
        Store one historical candle.
        """

        logger.info(
            "Storing candle %s %s %s",
            symbol,
            timeframe,
            candle_time,
        )

        return self._repository.insert_candle(
            symbol=symbol,
            timeframe=timeframe,
            candle_time=candle_time,
            open_price=open_price,
            high_price=high_price,
            low_price=low_price,
            close_price=close_price,
            tick_volume=tick_volume,
            spread=spread,
            real_volume=real_volume,
        )

    # =========================================================================
    # RETRIEVE
    # =========================================================================

    def get_candle(
        self,
        *,
        symbol: str,
        timeframe: str,
        candle_time: str,
    ) -> dict[str, Any] | None:
        """
        Retrieve one candle.
        """

        return self._repository.get_candle(
            symbol=symbol,
            timeframe=timeframe,
            candle_time=candle_time,
        )

    def recent_candles(
        self,
        *,
        symbol: str,
        timeframe: str,
        limit: int = 500,
    ) -> list[dict[str, Any]]:
        """
        Return newest candles.
        """

        return self._repository.get_recent_candles(
            symbol=symbol,
            timeframe=timeframe,
            limit=limit,
        )

    def candles_between(
        self,
        *,
        symbol: str,
        timeframe: str,
        start_time: str,
        end_time: str,
    ) -> list[dict[str, Any]]:
        """
        Return candles within a time range.
        """

        return self._repository.get_candles_between(
            symbol=symbol,
            timeframe=timeframe,
            start_time=start_time,
            end_time=end_time,
        )

    # =========================================================================
    # VALIDATION
    # =========================================================================

    def has_market_data(
        self,
        *,
        symbol: str,
        timeframe: str,
    ) -> bool:
        """
        Determine whether market history exists.
        """

        return (
            self._repository.candle_count(
                symbol=symbol,
                timeframe=timeframe,
            )
            > 0
        )

    # =========================================================================
    # DELETE
    # =========================================================================

    def delete_symbol(
        self,
        symbol: str,
    ) -> bool:
        """
        Delete all historical candles for a symbol.
        """

        logger.warning(
            "Deleting market history for %s",
            symbol,
        )

        return self._repository.delete_symbol(symbol)

    def delete_before(
        self,
        *,
        symbol: str,
        timeframe: str,
        before_time: str,
    ) -> bool:
        """
        Delete candles before a timestamp.
        """

        return self._repository.delete_before(
            symbol=symbol,
            timeframe=timeframe,
            before_time=before_time,
        )

    # =========================================================================
    # STATISTICS
    # =========================================================================

    def total_candles(self) -> int:
        """
        Return total stored candles.
        """

        return self._repository.total_candles()

    def candle_count(
        self,
        *,
        symbol: str,
        timeframe: str,
    ) -> int:
        """
        Return stored candles for one symbol/timeframe.
        """

        return self._repository.candle_count(
            symbol=symbol,
            timeframe=timeframe,
        )

    def oldest_candle(
        self,
        *,
        symbol: str,
        timeframe: str,
    ) -> str | None:
        """
        Return oldest candle timestamp.
        """

        return self._repository.oldest_candle(
            symbol=symbol,
            timeframe=timeframe,
        )

    def newest_candle(
        self,
        *,
        symbol: str,
        timeframe: str,
    ) -> str | None:
        """
        Return newest candle timestamp.
        """

        return self._repository.newest_candle(
            symbol=symbol,
            timeframe=timeframe,
        )

    # =========================================================================
    # DASHBOARD
    # =========================================================================

    def market_summary(
        self,
        *,
        symbol: str,
        timeframe: str,
    ) -> dict[str, Any]:
        """
        Return market storage summary.
        """

        summary = self._repository.summary(
            symbol=symbol,
            timeframe=timeframe,
        )

        logger.info(
            "Market summary generated for %s %s",
            symbol,
            timeframe,
        )

        return summary