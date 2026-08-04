"""
===============================================================================
UDUAK_QUANT_SYSTEM_PROJECT
-------------------------------------------------------------------------------
File: services/trade_service.py

Description:
    Business logic for trade management.

Responsibilities:
    - Validate trade requests
    - Open new trades
    - Close trades
    - Update risk parameters
    - Retrieve trades
    - Calculate trade profit
    - Expose trade statistics

This module must NEVER contain SQL.
===============================================================================
"""

from __future__ import annotations

from typing import Any

from database.repositories.trade_repository import TradeRepository
from monitoring.logger import get_logger

logger = get_logger(__name__)


class TradeService:
    """
    Business logic for trade operations.
    """

    def __init__(self) -> None:
        self._repository = TradeRepository()

    # =========================================================================
    # CREATE
    # =========================================================================

    def open_trade(
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
    ) -> int:
        """
        Validate and store a new trade.
        """

        if ticket <= 0:
            raise ValueError("Ticket must be positive.")

        if not symbol.strip():
            raise ValueError("Symbol cannot be empty.")

        direction = direction.upper()

        if direction not in ("BUY", "SELL"):
            raise ValueError("Direction must be BUY or SELL.")

        if volume <= 0:
            raise ValueError("Volume must be greater than zero.")

        if entry_price <= 0:
            raise ValueError("Entry price must be greater than zero.")

        logger.info(
            "Opening %s trade on %s",
            direction,
            symbol,
        )

        return self._repository.insert_trade(
            ticket=ticket,
            symbol=symbol,
            direction=direction,
            strategy=strategy,
            volume=volume,
            entry_price=entry_price,
            stop_loss=stop_loss,
            take_profit=take_profit,
        )

    # =========================================================================
    # READ
    # =========================================================================

    def get_trade(
        self,
        ticket: int,
    ) -> dict[str, Any] | None:
        """
        Return one trade.
        """

        return self._repository.get_trade_by_ticket(ticket)

    def get_open_trades(self) -> list[dict[str, Any]]:
        """
        Return all open trades.
        """

        return self._repository.get_open_trades()

    def get_closed_trades(self) -> list[dict[str, Any]]:
        """
        Return all closed trades.
        """

        return self._repository.get_closed_trades()

    def get_all_trades(self) -> list[dict[str, Any]]:
        """
        Return every trade.
        """

        return self._repository.get_all_trades()

    # =========================================================================
    # CLOSE TRADE
    # =========================================================================

    def close_trade(
        self,
        *,
        ticket: int,
        exit_price: float,
    ) -> bool:
        """
        Close an existing trade.

        Profit is calculated automatically.
        """

        trade = self._repository.get_trade_by_ticket(ticket)

        if trade is None:
            raise ValueError("Trade not found.")

        if trade["status"] != "OPEN":
            raise ValueError("Trade already closed.")

        entry = float(trade["entry_price"])

        volume = float(trade["volume"])

        direction = trade["direction"]

        if direction == "BUY":
            profit = (exit_price - entry) * volume

        else:
            profit = (entry - exit_price) * volume

        logger.info(
            "Closing trade %s profit=%0.2f",
            ticket,
            profit,
        )

        return self._repository.close_trade(
            ticket=ticket,
            exit_price=exit_price,
            profit=profit,
        )

    # =========================================================================
    # RISK MANAGEMENT
    # =========================================================================

    def update_stop_loss(
        self,
        *,
        ticket: int,
        stop_loss: float,
    ) -> bool:
        """
        Update stop loss.
        """

        if stop_loss <= 0:
            raise ValueError("Stop loss must be positive.")

        return self._repository.update_stop_loss(
            ticket=ticket,
            stop_loss=stop_loss,
        )

    def update_take_profit(
        self,
        *,
        ticket: int,
        take_profit: float,
    ) -> bool:
        """
        Update take profit.
        """

        if take_profit <= 0:
            raise ValueError("Take profit must be positive.")

        return self._repository.update_take_profit(
            ticket=ticket,
            take_profit=take_profit,
        )

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

        logger.warning(
            "Deleting trade %s",
            ticket,
        )

        return self._repository.delete_trade(ticket)

    # =========================================================================
    # STATISTICS
    # =========================================================================

    def total_trades(self) -> int:
        return self._repository.total_trades()

    def total_profit(self) -> float:
        return self._repository.total_profit()

    def win_count(self) -> int:
        return self._repository.win_count()

    def loss_count(self) -> int:
        return self._repository.loss_count()

    def win_rate(self) -> float:
        return self._repository.win_rate()