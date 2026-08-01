"""
===============================================================================
UDUAK_QUANT_SYSTEM_PROJECT
-------------------------------------------------------------------------------
File: config/trading.py

Description:
    Central trading policy configuration for the entire trading system.

Responsibilities:
    - Position management rules.
    - Trade execution configuration.
    - Trading session configuration.
    - Default order configuration.
    - Global trading filters.

This module NEVER:
    - Connects to MetaTrader 5.
    - Executes trades.
    - Contains trading logic.
    - Calculates risk.
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


# =============================================================================
# ENUMERATIONS
# =============================================================================

class OrderFilling(Enum):
    """
    Supported MT5 order filling policies.

    AUTO allows the execution engine to detect the correct filling mode
    supported by the connected broker and trading symbol.
    """

    AUTO = "AUTO"

    FOK = "FOK"

    IOC = "IOC"

    RETURN = "RETURN"


class OrderType(Enum):
    """
    Supported order execution types.
    """

    MARKET = "MARKET"

    PENDING = "PENDING"


# =============================================================================
# POSITION CONFIGURATION
# =============================================================================

@dataclass(frozen=True)
class PositionConfig:
    """
    Portfolio position management rules.
    """

    # Maximum total positions allowed.
    max_open_positions: int = 2

    # Maximum positions allowed for one symbol.
    max_positions_per_symbol: int = 1

    # Allow multiple positions on the same instrument.
    allow_multiple_positions: bool = False

    # Allow opposite-direction positions.
    allow_hedging: bool =False


# =============================================================================
# EXECUTION CONFIGURATION
# =============================================================================

@dataclass(frozen=True)
class ExecutionConfig:
    """
    Trade execution settings.
    """

    # Maximum acceptable slippage (points).
    slippage: int = 5

    # AUTO = detect broker-supported filling mode.
    filling_policy: OrderFilling = OrderFilling.AUTO

    # Retry failed trade requests.
    retry_attempts: int = 3

    # Delay between retries (seconds).
    retry_delay_seconds: int = 2

    # Maximum execution timeout (seconds).
    execution_timeout: int = 30


# =============================================================================
# SESSION CONFIGURATION
# =============================================================================

@dataclass(frozen=True)
class SessionConfig:
    """
    Trading schedule.
    """

    trade_monday: bool = True

    trade_tuesday: bool = True

    trade_wednesday: bool = True

    trade_thursday: bool = True

    trade_friday: bool = True

    trade_saturday: bool = False

    trade_sunday: bool = False

    allow_weekend_trading: bool = False

    # Stop opening new trades after this hour
    # (broker/server time).
    friday_cutoff_hour: int = 21


# =============================================================================
# ORDER CONFIGURATION
# =============================================================================

@dataclass(frozen=True)
class OrderConfig:
    """
    Default order parameters.
    """

    magic_number: int = 10001

    comment: str = "UDUAK_QUANT_SYSTEM"

    order_type: OrderType = OrderType.MARKET

    deviation: int = 5


# =============================================================================
# FILTER CONFIGURATION
# =============================================================================

@dataclass(frozen=True)
class FilterConfig:
    """
    Global trading filters.
    """

    # High-impact economic news.
    news_filter: bool = True

    # Trading session filter.
    session_filter: bool = True

    # Maximum spread filter.
    spread_filter: bool = True

    # High volatility filter.
    volatility_filter: bool = True

    # Market regime filter.
    regime_filter: bool = True


# =============================================================================
# MASTER CONFIGURATION
# =============================================================================

@dataclass(frozen=True)
class TradingConfig:
    """
    Root trading configuration.
    """

    position: PositionConfig

    execution: ExecutionConfig

    session: SessionConfig

    order: OrderConfig

    filters: FilterConfig


# =============================================================================
# DEFAULT CONFIGURATION
# =============================================================================

trading = TradingConfig(

    position=PositionConfig(),

    execution=ExecutionConfig(),

    session=SessionConfig(),

    order=OrderConfig(),

    filters=FilterConfig(),

)