"""
===============================================================================
UDUAK_QUANT_SYSTEM_PROJECT

File: config/timeframes.py

Purpose:
    Central definition of all supported trading timeframes.

Responsibilities:
    - Define supported chart timeframes.
    - Store timeframe metadata.
    - Provide one source of truth.

This module NEVER:

- Connects to MT5
- Downloads data
- Contains trading logic
===============================================================================
"""

from dataclasses import dataclass
from typing import Final


# =============================================================================
# Timeframe Definition
# =============================================================================

@dataclass(frozen=True)
class TimeFrame:
    """
    Represents a single chart timeframe.
    """

    name: str

    minutes: int

    rank: int

    intraday: bool


# =============================================================================
# Supported Timeframes
# =============================================================================

M1 = TimeFrame(
    name="M1",
    minutes=1,
    rank=1,
    intraday=True,
)

M5 = TimeFrame(
    name="M5",
    minutes=5,
    rank=2,
    intraday=True,
)

M15 = TimeFrame(
    name="M15",
    minutes=15,
    rank=3,
    intraday=True,
)

M30 = TimeFrame(
    name="M30",
    minutes=30,
    rank=4,
    intraday=True,
)

H1 = TimeFrame(
    name="H1",
    minutes=60,
    rank=5,
    intraday=True,
)

H4 = TimeFrame(
    name="H4",
    minutes=240,
    rank=6,
    intraday=True,
)

D1 = TimeFrame(
    name="D1",
    minutes=1440,
    rank=7,
    intraday=False,
)

W1 = TimeFrame(
    name="W1",
    minutes=10080,
    rank=8,
    intraday=False,
)

MN1 = TimeFrame(
    name="MN1",
    minutes=43200,      # Approximate
    rank=9,
    intraday=False,
)


# =============================================================================
# Configuration
# =============================================================================

@dataclass(frozen=True)
class TimeFrameConfig:

    supported: tuple[TimeFrame, ...]

    execution: TimeFrame

    confirmation: TimeFrame

    trend: TimeFrame

    macro: TimeFrame


timeframes = TimeFrameConfig(

    supported=(

        M1,

        M5,

        M15,

        M30,

        H1,

        H4,

        D1,

        W1,

        MN1,
    ),

    execution=M5,

    confirmation=M15,

    trend=H1,

    macro=H4,
)