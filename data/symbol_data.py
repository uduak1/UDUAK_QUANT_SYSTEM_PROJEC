"""
===============================================================================
UDUAK_QUANT_SYSTEM_PROJECT
-------------------------------------------------------------------------------
File: data/symbol_data.py

Description:
    Reads symbol information from MetaTrader 5.

Responsibilities:
    - Retrieve symbol information.
    - Verify symbol availability.
    - Return standardized Response objects.

This module NEVER:
    - Connects to MT5.
    - Executes trades.
    - Calculates lot sizes.
    - Performs risk management.
    - Reads candle data.
===============================================================================
"""

from __future__ import annotations

import MetaTrader5 as mt5

from models.response import Response
from monitoring.logger import get_logger

logger = get_logger(__name__)


class SymbolData:
    """
    Read-only access to MetaTrader 5 symbol information.
    """

    # =====================================================================
    # SYMBOL INFORMATION
    # =====================================================================

    def get_symbol_info(self, symbol: str) -> Response:
        """
        Retrieve information for a trading symbol.

        Parameters
        ----------
        symbol : str
            Trading symbol.

        Returns
        -------
        Response
            Standard project response.
        """

        info = mt5.symbol_info(symbol)

        if info is None:

            error = mt5.last_error()

            logger.error(
                "Unable to retrieve information for symbol '%s': %s",
                symbol,
                error,
            )

            return Response(
                success=False,
                message=f"Unable to retrieve information for symbol '{symbol}'.",
                error=error,
                data=None,
            )

        logger.info(
            "Retrieved information for symbol '%s'.",
            symbol,
        )

        return Response(
            success=True,
            message=f"Retrieved information for symbol '{symbol}'.",
            error=None,
            data=info,
        )

    # =====================================================================
    # SYMBOL AVAILABILITY
    # =====================================================================

    def is_available(self, symbol: str) -> Response:
        """
        Check whether a symbol exists.

        Parameters
        ----------
        symbol : str
            Trading symbol.

        Returns
        -------
        Response
            Standard project response.
        """

        result = self.get_symbol_info(symbol)

        if result.success:

            return Response(
                success=True,
                message=f"Symbol '{symbol}' is available.",
                error=None,
                data=True,
            )

        return Response(
            success=False,
            message=f"Symbol '{symbol}' is not available.",
            error=result.error,
            data=False,
        )