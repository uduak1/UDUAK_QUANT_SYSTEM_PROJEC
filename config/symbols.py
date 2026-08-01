"""
===============================================================================
UDUAK_QUANT_SYSTEM_PROJECT

File: config/symbols.py

Purpose:
    Central configuration of every financial instrument supported by
    the trading system.

Responsibilities
----------------
- Define supported symbols.
- Group symbols into asset classes.
- Provide one source of truth.

This module NEVER:

- Connects to MT5
- Downloads data
- Executes trades
- Contains strategy logic
===============================================================================
"""

from dataclasses import dataclass
from typing import Final


# =============================================================================
# FOREX
# =============================================================================

FOREX: Final[tuple[str, ...]] = (

    "EURUSD",
    "GBPUSD",
    "USDJPY",
    "USDCHF",
    "USDCAD",

    "AUDUSD",
    "NZDUSD",

    "EURJPY",
    "GBPJPY",
    "EURGBP",
)


# =============================================================================
# PRECIOUS METALS
# =============================================================================

METALS: Final[tuple[str, ...]] = (

    "XAUUSD",

    "XAGUSD",
)


# =============================================================================
# ENERGY
# =============================================================================

ENERGY: Final[tuple[str, ...]] = (

    "USOIL",

    "UKOIL",
)


# =============================================================================
# INDICES
# =============================================================================

INDICES: Final[tuple[str, ...]] = (

    "US30",

    "US100",

    "SPX500",

    "GER40",

    "UK100",
)


# =============================================================================
# RESERVED
# =============================================================================

FUTURES: Final[tuple[str, ...]] = ()

OPTIONS: Final[tuple[str, ...]] = ()

BONDS: Final[tuple[str, ...]] = ()


@dataclass(frozen=True)
class SymbolConfig:
    """
    Immutable container holding all supported trading symbols.
    """

    forex: tuple[str, ...]

    metals: tuple[str, ...]

    energy: tuple[str, ...]

    indices: tuple[str, ...]

    futures: tuple[str, ...]

    options: tuple[str, ...]

    bonds: tuple[str, ...]

    @property
    def all_symbols(self) -> tuple[str, ...]:
        """
        Return every supported symbol.
        """

        return (

            self.forex +

            self.metals +

            self.energy +

            self.indices +

            self.futures +

            self.options +

            self.bonds
        )


symbols = SymbolConfig(

    forex=FOREX,

    metals=METALS,

    energy=ENERGY,

    indices=INDICES,

    futures=FUTURES,

    options=OPTIONS,

    bonds=BONDS,
)