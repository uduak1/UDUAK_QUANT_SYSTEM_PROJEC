"""
===============================================================================
UDUAK_QUANT_SYSTEM_PROJECT
-------------------------------------------------------------------------------
File: data/market_data.py

Description:
    Reads live market prices from MetaTrader 5.

Responsibilities:
    - Retrieve current market prices.
    - Calculate the current spread.
    - Return standardized Response objects.

This module NEVER:
    - Connects to MT5.
    - Executes trades.
    - Reads candle history.
    - Calculates indicators.
    - Performs risk management.
===============================================================================
"""

from __future__ import annotations

import MetaTrader5 as mt5

from models.response import Response
from monitoring.logger import get_logger

logger = get_logger(__name__)


class MarketData:
    """
    Read-only access to live market prices.
    """

    # =====================================================================
    # MARKET DATA
    # =====================================================================

    def get_market_data(self, symbol: str) -> Response:
        """
        Retrieve the latest market prices for a symbol.

        Parameters
        ----------
        symbol : str
            Trading symbol.

        Returns
        -------
        Response
            Standard project response.
        """

        tick = mt5.symbol_info_tick(symbol)

        if tick is None:

            error = mt5.last_error()

            logger.error(
                "Unable to retrieve market data for '%s': %s",
                symbol,
                error,
            )

            return Response(
                success=False,
                message=f"Unable to retrieve market data for '{symbol}'.",
                error=error,
                data=None,
            )

        spread = tick.ask - tick.bid

        market = {
            "symbol": symbol,
            "bid": tick.bid,
            "ask": tick.ask,
            "last": tick.last,
            "spread": spread,
            "time": tick.time,
            "volume": tick.volume,
            "flags": tick.flags,
        }

        logger.info(
            "Retrieved market data for '%s'.",
            symbol,
        )

        return Response(
            success=True,
            message=f"Market data retrieved for '{symbol}'.",
            error=None,
            data=market,
        )

    # =====================================================================
    # MARKET AVAILABILITY
    # =====================================================================

    def is_available(self, symbol: str) -> Response:
        """
        Check whether live market data is available.

        Parameters
        ----------
        symbol : str
            Trading symbol.

        Returns
        -------
        Response
            Standard project response.
        """

        result = self.get_market_data(symbol)

        if result.success:

            return Response(
                success=True,
                message=f"Market data for '{symbol}' is available.",
                error=None,
                data=True,
            )

        return Response(
            success=False,
            message=f"Market data for '{symbol}' is not available.",
            error=result.error,
            data=False,
        )