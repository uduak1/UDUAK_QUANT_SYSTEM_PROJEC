"""
===============================================================================
UDUAK_QUANT_SYSTEM_PROJECT
-------------------------------------------------------------------------------
File: models/signal.py

Description:
    Defines the standard trading signal used throughout the application.

Responsibilities:
    - Represent a trade opportunity.
    - Store entry information.
    - Validate basic signal data.

This module NEVER:
    - Connects to MetaTrader 5.
    - Places trades.
    - Calculates indicators.
    - Makes trading decisions.
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


# =============================================================================
# ENUMERATIONS
# =============================================================================

class SignalDirection(Enum):
    """
    Direction of a trading signal.
    """

    BUY = "BUY"
    SELL = "SELL"


# =============================================================================
# SIGNAL MODEL
# =============================================================================

@dataclass(slots=True)
class Signal:
    """
    Standard trading signal.

    Every strategy in the project must return this object.
    """

    # Trading symbol.
    symbol: str

    # BUY or SELL.
    direction: SignalDirection

    # Planned entry price.
    entry_price: float

    # Protective stop loss.
    stop_loss: float

    # Planned take profit.
    take_profit: float

    # Strategy that generated the signal.
    strategy_name: str

    @property
    def risk(self) -> float:
        """
        Distance between entry and stop loss.
        """
        return abs(self.entry_price - self.stop_loss)

    @property
    def reward(self) -> float:
        """
        Distance between entry and take profit.
        """
        return abs(self.take_profit - self.entry_price)

    @property
    def risk_reward_ratio(self) -> float:
        """
        Calculate Risk : Reward ratio.
        """

        if self.risk == 0:
            return 0.0

        return self.reward / self.risk