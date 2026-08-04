"""
===============================================================================
UDUAK_QUANT_SYSTEM_PROJECT
-------------------------------------------------------------------------------
File: database/services/database_service.py

Description:
    Central service layer for all database operations.

Responsibilities:
    - Coordinate repositories
    - Provide one interface to the database
    - Keep SQL hidden from business logic

This service contains NO trading logic.
===============================================================================
"""

from __future__ import annotations

from typing import Any

from database.repositories.market_repository import MarketRepository
from database.repositories.performance_repository import (
    PerformanceRepository,
)
from database.repositories.position_repository import (
    PositionRepository,
)
from database.repositories.signal_repository import SignalRepository
from database.repositories.trade_repository import TradeRepository
from monitoring.logger import get_logger

logger = get_logger(__name__)


class DatabaseService:
    """
    Central database service.
    """

    def __init__(self) -> None:
        """
        Initialize repositories.
        """

        self.trade_repository = TradeRepository()

        self.signal_repository = SignalRepository()

        self.position_repository = PositionRepository()

        self.performance_repository = (
            PerformanceRepository()
        )

        self.market_repository = (
            MarketRepository()
        )

    # =====================================================================
    # TRADE OPERATIONS
    # =====================================================================

    def save_trade(
        self,
        **kwargs: Any,
    ) -> int:
        """
        Save completed trade.
        """

        return self.trade_repository.insert_trade(
            **kwargs
        )

    def trade(
        self,
        trade_id: int,
    ) -> dict[str, Any] | None:
        """
        Retrieve one trade.
        """

        return self.trade_repository.get_trade(
            trade_id
        )

    def trades(self) -> list[dict[str, Any]]:
        """
        Retrieve all trades.
        """

        return self.trade_repository.get_all_trades()

    # =====================================================================
    # SIGNAL OPERATIONS
    # =====================================================================

    def save_signal(
        self,
        **kwargs: Any,
    ) -> int:
        """
        Save signal.
        """

        return self.signal_repository.insert_signal(
            **kwargs
        )

    def signal(
        self,
        signal_id: int,
    ) -> dict[str, Any] | None:
        """
        Retrieve signal.
        """

        return self.signal_repository.get_signal(
            signal_id
        )

    def signals(self) -> list[dict[str, Any]]:
        """
        Retrieve all signals.
        """

        return self.signal_repository.get_all_signals()

    # =====================================================================
    # POSITION OPERATIONS
    # =====================================================================

    def save_position(
        self,
        **kwargs: Any,
    ) -> int:
        """
        Save open position.
        """

        return (
            self.position_repository.insert_position(
                **kwargs
            )
        )

    def position(
        self,
        ticket: int,
    ) -> dict[str, Any] | None:
        """
        Retrieve position.
        """

        return self.position_repository.get_position(
            ticket
        )

    def positions(self) -> list[dict[str, Any]]:
        """
        Retrieve all positions.
        """

        return (
            self.position_repository.get_all_positions()
        )

    def remove_position(
        self,
        ticket: int,
    ) -> bool:
        """
        Remove closed position.
        """

        return (
            self.position_repository.remove_position(
                ticket
            )
        )

    # =====================================================================
    # MARKET DATA
    # =====================================================================

    def save_candle(
        self,
        **kwargs: Any,
    ) -> int:
        """
        Save market candle.
        """

        return self.market_repository.insert_candle(
            **kwargs
        )

    def recent_candles(
        self,
        *,
        symbol: str,
        timeframe: str,
        limit: int = 500,
    ) -> list[dict[str, Any]]:
        """
        Retrieve latest candles.
        """

        return (
            self.market_repository.get_recent_candles(
                symbol=symbol,
                timeframe=timeframe,
                limit=limit,
            )
        )

    # =====================================================================
    # PERFORMANCE
    # =====================================================================

    def performance_summary(
        self,
    ) -> dict[str, Any]:
        """
        Return performance metrics.
        """

        return (
            self.performance_repository.summary()
        )

    # =====================================================================
    # DASHBOARD
    # =====================================================================

    def dashboard(self) -> dict[str, Any]:
        """
        Return complete dashboard data.
        """

        return {
            "performance": (
                self.performance_repository.summary()
            ),
            "positions": (
                self.position_repository.get_all_positions()
            ),
            "signals": (
                self.signal_repository.get_all_signals()
            ),
            "trades": (
                self.trade_repository.get_all_trades()
            ),
        }

    # =====================================================================
    # HEALTH
    # =====================================================================

    def health(self) -> dict[str, Any]:
        """
        Return database health.
        """

        return {
            "status": "ONLINE",
            "trades": (
                self.performance_repository.total_trades()
            ),
            "signals": (
                self.signal_repository.total_signals()
            ),
            "positions": (
                self.position_repository.total_positions()
            ),
            "candles": (
                self.market_repository.total_candles()
            ),
        }