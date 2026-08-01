"""
===============================================================================
UDUAK_QUANT_SYSTEM_PROJECT
-------------------------------------------------------------------------------
File: data/candle_data.py

Description:
    Reads historical candle data from MetaTrader 5.

Responsibilities:
    - Retrieve OHLC candle data.
    - Convert MT5 candle data into Python dictionaries.
    - Calculate basic candle properties.
    - Return standardized Response objects.

This module NEVER:
    - Connects to MT5.
    - Executes trades.
    - Detects candle patterns.
    - Detects chart patterns.
    - Calculates indicators.
    - Performs risk management.
===============================================================================
"""

from __future__ import annotations

from typing import List

import MetaTrader5 as mt5

from models.response import Response
from monitoring.logger import get_logger

logger = get_logger(__name__)


class CandleData:
    """
    Read-only access to historical candle data.

    This class retrieves OHLC candles from MetaTrader 5 and
    enriches each candle with basic calculated properties that
    are useful throughout the trading system.
    """

    # =========================================================================
    # PUBLIC METHODS
    # =========================================================================

    def get_candles(
        self,
        symbol: str,
        timeframe: int,
        count: int,
    ) -> Response:
        """
        Retrieve historical candles.

        Parameters
        ----------
        symbol : str
            Trading symbol.

        timeframe : int
            MetaTrader 5 timeframe.

        count : int
            Number of candles to retrieve.

        Returns
        -------
        Response
            Standard project response.
        """

        rates = mt5.copy_rates_from_pos(
            symbol,
            timeframe,
            0,
            count,
        )

        if rates is None:

            error = mt5.last_error()

            logger.error(
                "Unable to retrieve candle data for '%s': %s",
                symbol,
                error,
            )

            return Response(
                success=False,
                message=f"Unable to retrieve candle data for '{symbol}'.",
                error=error,
                data=None,
            )

        candles: List[dict] = []

        for candle in rates:

            open_price = float(candle["open"])

            high_price = float(candle["high"])

            low_price = float(candle["low"])

            close_price = float(candle["close"])

            body = round(
                abs(close_price - open_price),
                10,
            )

            candle_range = round(
                high_price - low_price,
                10,
            )

            upper_wick = round(
                high_price - max(
                    open_price,
                    close_price,
                ),
                10,
            )

            lower_wick = round(
                min(
                    open_price,
                    close_price,
                ) - low_price,
                10,
            )

            bullish = close_price > open_price

            bearish = close_price < open_price
            candle_data = {
                "time": candle["time"],
                "open": open_price,
                "high": high_price,
                "low": low_price,
                "close": close_price,
                "tick_volume": candle["tick_volume"],
                "spread": candle["spread"],
                "real_volume": candle["real_volume"],

                # -------------------------------------------------------------
                # Derived candle properties
                # -------------------------------------------------------------

                "body": body,
                "candle_range": candle_range,
                "upper_wick": upper_wick,
                "lower_wick": lower_wick,
                "bullish": bullish,
                "bearish": bearish,
            }

            candles.append(candle_data)

        logger.info(
            "Retrieved %d candles for '%s'.",
            len(candles),
            symbol,
        )

        return Response(
            success=True,
            message=(
                f"Retrieved {len(candles)} candles "
                f"for '{symbol}'."
            ),
            error=None,
            data=candles,
        )

    # =========================================================================
    # AVAILABILITY
    # =========================================================================

    def is_available(
        self,
        symbol: str,
        timeframe: int,
    ) -> Response:
        """
        Check whether candle data is available.

        Parameters
        ----------
        symbol : str
            Trading symbol.

        timeframe : int
            MetaTrader 5 timeframe.

        Returns
        -------
        Response
            Standard project response.
        """

        result = self.get_candles(
            symbol=symbol,
            timeframe=timeframe,
            count=1,
        )

        if result.success:

            return Response(
                success=True,
                message=(
                    f"Candle data for '{symbol}' "
                    "is available."
                ),
                error=None,
                data=True,
            )

        return Response(
            success=False,
            message=(
                f"Candle data for '{symbol}' "
                "is not available."
            ),
            error=result.error,
            data=False,
        )
