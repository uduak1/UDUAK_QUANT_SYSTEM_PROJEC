"""
===============================================================================
UDUAK_QUANT_SYSTEM_PROJECT
-------------------------------------------------------------------------------
File: services/signal_service.py

Description:
    Business logic for signal management.

Responsibilities:
    - Validate trading signals
    - Store new signals
    - Prevent duplicate active signals
    - Execute signals
    - Expire signals
    - Retrieve signals
    - Produce signal statistics

This module contains business logic only.
It must NEVER contain SQL.
===============================================================================
"""

from __future__ import annotations

from typing import Any

from database.repositories.signal_repository import SignalRepository
from monitoring.logger import get_logger

logger = get_logger(__name__)


class SignalService:
    """
    Business logic for trading signals.
    """

    def __init__(self) -> None:
        """
        Initialize signal service.
        """

        self._repository = SignalRepository()

    # =========================================================================
    # CREATE
    # =========================================================================

    def create_signal(
        self,
        *,
        symbol: str,
        direction: str,
        strategy: str,
        confidence: float,
        timeframe: str,
        entry_price: float,
        stop_loss: float,
        take_profit: float,
    ) -> int:
        """
        Validate and store a new signal.
        """

        if not symbol.strip():
            raise ValueError("Symbol cannot be empty.")

        direction = direction.upper()

        if direction not in ("BUY", "SELL"):
            raise ValueError("Direction must be BUY or SELL.")

        if confidence < 0 or confidence > 100:
            raise ValueError("Confidence must be between 0 and 100.")

        if entry_price <= 0:
            raise ValueError("Entry price must be positive.")

        if stop_loss <= 0:
            raise ValueError("Stop loss must be positive.")

        if take_profit <= 0:
            raise ValueError("Take profit must be positive.")

        existing = self._repository.find_active_signal(
            symbol=symbol,
            direction=direction,
            timeframe=timeframe,
        )

        if existing is not None:
            raise ValueError(
                "Active signal already exists."
            )

        logger.info(
            "Creating %s signal for %s",
            direction,
            symbol,
        )

        return self._repository.insert_signal(
            symbol=symbol,
            direction=direction,
            strategy=strategy,
            confidence=confidence,
            timeframe=timeframe,
            entry_price=entry_price,
            stop_loss=stop_loss,
            take_profit=take_profit,
        )

    # =========================================================================
    # READ
    # =========================================================================

    def get_signal(
        self,
        signal_id: int,
    ) -> dict[str, Any] | None:
        """
        Retrieve one signal.
        """

        return self._repository.get_signal(signal_id)

    def get_all_signals(
        self,
    ) -> list[dict[str, Any]]:
        """
        Retrieve all signals.
        """

        return self._repository.get_all_signals()

    def get_active_signals(
        self,
    ) -> list[dict[str, Any]]:
        """
        Retrieve active signals.
        """

        return self._repository.get_active_signals()

    def get_executed_signals(
        self,
    ) -> list[dict[str, Any]]:
        """
        Retrieve executed signals.
        """

        return self._repository.get_executed_signals()

    def get_expired_signals(
        self,
    ) -> list[dict[str, Any]]:
        """
        Retrieve expired signals.
        """

        return self._repository.get_expired_signals()

    # =========================================================================
    # EXECUTION
    # =========================================================================

    def execute_signal(
        self,
        signal_id: int,
    ) -> bool:
        """
        Mark a signal as executed.
        """

        signal = self._repository.get_signal(signal_id)

        if signal is None:
            raise ValueError("Signal not found.")

        if signal["status"] != "ACTIVE":
            raise ValueError(
                "Only active signals can be executed."
            )

        logger.info(
            "Executing signal %s",
            signal_id,
        )

        return self._repository.mark_executed(
            signal_id,
        )

    # =========================================================================
    # EXPIRATION
    # =========================================================================

    def expire_signal(
        self,
        signal_id: int,
    ) -> bool:
        """
        Mark a signal as expired.
        """

        signal = self._repository.get_signal(signal_id)

        if signal is None:
            raise ValueError("Signal not found.")

        if signal["status"] != "ACTIVE":
            raise ValueError(
                "Only active signals can expire."
            )

        logger.info(
            "Expiring signal %s",
            signal_id,
        )

        return self._repository.mark_expired(
            signal_id,
        )

    # =========================================================================
    # DELETE
    # =========================================================================

    def delete_signal(
        self,
        signal_id: int,
    ) -> bool:
        """
        Delete a signal.
        """

        logger.warning(
            "Deleting signal %s",
            signal_id,
        )

        return self._repository.delete_signal(
            signal_id,
        )

    # =========================================================================
    # STATISTICS
    # =========================================================================

    def total_signals(self) -> int:
        """
        Total signals.
        """

        return self._repository.total_signals()

    def active_signals(self) -> int:
        """
        Active signals.
        """

        return self._repository.active_signal_count()

    def executed_signals(self) -> int:
        """
        Executed signals.
        """

        return self._repository.executed_signal_count()

    def expired_signals(self) -> int:
        """
        Expired signals.
        """

        return self._repository.expired_signal_count()

    def execution_rate(self) -> float:
        """
        Percentage of executed signals.
        """

        total = self.total_signals()

        if total == 0:
            return 0.0

        return (
            self.executed_signals() / total
        ) * 100.0