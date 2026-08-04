"""
===============================================================================
UDUAK_QUANT_SYSTEM_PROJECT
-------------------------------------------------------------------------------
File: database/repositories/performance_repository.py

Description:
    Repository responsible for performance statistics.

Responsibilities:
    - Read performance metrics
    - Aggregate completed trade statistics
    - Produce dashboard statistics

This repository NEVER executes trading logic.
===============================================================================
"""

from __future__ import annotations

from typing import Any

from database.database import Database
from monitoring.logger import get_logger

logger = get_logger(__name__)


class PerformanceRepository:
    """
    Repository for trading performance statistics.
    """

    def __init__(self) -> None:
        """
        Initialize repository.
        """

        self._database = Database()

    # =====================================================================
    # BASIC COUNTS
    # =====================================================================

    def total_trades(self) -> int:
        """
        Return total completed trades.
        """

        cursor = self._database.execute(
            """
            SELECT COUNT(*)
            FROM trades
            """
        )

        return int(cursor.fetchone()[0])

    def winning_trades(self) -> int:
        """
        Return winning trades.
        """

        cursor = self._database.execute(
            """
            SELECT COUNT(*)
            FROM trades
            WHERE profit > 0
            """
        )

        return int(cursor.fetchone()[0])

    def losing_trades(self) -> int:
        """
        Return losing trades.
        """

        cursor = self._database.execute(
            """
            SELECT COUNT(*)
            FROM trades
            WHERE profit < 0
            """
        )

        return int(cursor.fetchone()[0])

    def breakeven_trades(self) -> int:
        """
        Return breakeven trades.
        """

        cursor = self._database.execute(
            """
            SELECT COUNT(*)
            FROM trades
            WHERE profit = 0
            """
        )

        return int(cursor.fetchone()[0])

    # =====================================================================
    # PROFIT
    # =====================================================================

    def gross_profit(self) -> float:
        """
        Sum of winning trades.
        """

        cursor = self._database.execute(
            """
            SELECT COALESCE(SUM(profit),0)
            FROM trades
            WHERE profit > 0
            """
        )

        return float(cursor.fetchone()[0])

    def gross_loss(self) -> float:
        """
        Sum of losing trades.
        """

        cursor = self._database.execute(
            """
            SELECT COALESCE(ABS(SUM(profit)),0)
            FROM trades
            WHERE profit < 0
            """
        )

        return float(cursor.fetchone()[0])

    def net_profit(self) -> float:
        """
        Total account profit.
        """

        cursor = self._database.execute(
            """
            SELECT COALESCE(SUM(profit),0)
            FROM trades
            """
        )

        return float(cursor.fetchone()[0])

    # =====================================================================
    # AVERAGES
    # =====================================================================

    def average_profit(self) -> float:
        """
        Average trade profit.
        """

        cursor = self._database.execute(
            """
            SELECT COALESCE(AVG(profit),0)
            FROM trades
            """
        )

        return float(cursor.fetchone()[0])

    def average_win(self) -> float:
        """
        Average winning trade.
        """

        cursor = self._database.execute(
            """
            SELECT COALESCE(AVG(profit),0)
            FROM trades
            WHERE profit > 0
            """
        )

        return float(cursor.fetchone()[0])

    def average_loss(self) -> float:
        """
        Average losing trade.
        """

        cursor = self._database.execute(
            """
            SELECT COALESCE(AVG(profit),0)
            FROM trades
            WHERE profit < 0
            """
        )

        return float(cursor.fetchone()[0])

    # =====================================================================
    # PERFORMANCE RATIOS
    # =====================================================================

    def win_rate(self) -> float:
        """
        Win percentage.
        """

        total = self.total_trades()

        if total == 0:
            return 0.0

        return (self.winning_trades() / total) * 100.0

    def loss_rate(self) -> float:
        """
        Loss percentage.
        """

        total = self.total_trades()

        if total == 0:
            return 0.0

        return (self.losing_trades() / total) * 100.0

    def profit_factor(self) -> float:
        """
        Gross Profit / Gross Loss.
        """

        gross_profit = self.gross_profit()
        gross_loss = self.gross_loss()

        if gross_loss == 0:
            return 0.0

        return gross_profit / gross_loss

    def expectancy(self) -> float:
        """
        Average expected profit per trade.
        """

        return self.average_profit()

    # =====================================================================
    # BEST / WORST
    # =====================================================================

    def best_trade(self) -> float:
        """
        Largest winning trade.
        """

        cursor = self._database.execute(
            """
            SELECT COALESCE(MAX(profit),0)
            FROM trades
            """
        )

        return float(cursor.fetchone()[0])

    def worst_trade(self) -> float:
        """
        Largest losing trade.
        """

        cursor = self._database.execute(
            """
            SELECT COALESCE(MIN(profit),0)
            FROM trades
            """
        )

        return float(cursor.fetchone()[0])

    # =====================================================================
    # DASHBOARD SUMMARY
    # =====================================================================

    def summary(self) -> dict[str, Any]:
        """
        Return complete dashboard statistics.
        """

        return {
            "total_trades": self.total_trades(),
            "wins": self.winning_trades(),
            "losses": self.losing_trades(),
            "breakeven": self.breakeven_trades(),
            "win_rate": self.win_rate(),
            "loss_rate": self.loss_rate(),
            "gross_profit": self.gross_profit(),
            "gross_loss": self.gross_loss(),
            "net_profit": self.net_profit(),
            "average_profit": self.average_profit(),
            "average_win": self.average_win(),
            "average_loss": self.average_loss(),
            "profit_factor": self.profit_factor(),
            "expectancy": self.expectancy(),
            "best_trade": self.best_trade(),
            "worst_trade": self.worst_trade(),
        }