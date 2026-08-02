"""
UDUAK_QUANT_SYSTEM_PROJECT

File: analysis/fvg_detector.py

Description:
    Detects institutional Fair Value Gaps (FVG).

Responsibilities:
    - Detect Bullish Fair Value Gaps
    - Detect Bearish Fair Value Gaps
    - Validate candle input
    - Validate OHLC values
    - Return standardized Response objects

This module NEVER:
    - Reads MT5 data
    - Retrieves candles
    - Executes trades
    - Performs risk management
    - Detects BOS
    - Detects CHOCH
    - Detects Liquidity
    - Detects Order Blocks
    - Scores trade quality
    - Filters sessions
    - Filters trend
"""

from __future__ import annotations

from typing import List
from typing import Optional
from typing import Tuple

from models.response import Response
from monitoring.logger import get_logger

logger = get_logger(__name__)


class FVGDetector:
    """
    Detect institutional Fair Value Gaps.

    Input
    -----
    Historical candle data.

    Output
    ------
    Standard Response object.
    """

    DEFAULT_MIN_CANDLES = 3

    # ==========================================================
    # PRIVATE HELPERS
    # ==========================================================

    def _extract_candle_fields(
        self,
        candle: dict,
    ) -> Optional[Tuple[float, float, float, float]]:
        """
        Validate and extract OHLC values.

        Parameters
        ----------
        candle : dict

        Returns
        -------
        Tuple
            (open, close, high, low)

        None
            If candle is malformed.
        """

        open_price = candle.get("open")
        close_price = candle.get("close")
        high = candle.get("high")
        low = candle.get("low")

        if (
            open_price is None
            or close_price is None
            or high is None
            or low is None
        ):
            return None

        # Validate OHLC relationships - reject impossible candles
        if (
            high < low
            or high < open_price
            or high < close_price
            or low > open_price
            or low > close_price
        ):
            return None

        return (
            open_price,
            close_price,
            high,
            low,
        )

    def _calculate_midpoint(
        self,
        top: float,
        bottom: float,
    ) -> float:
        """
        Calculate consequent encroachment (midpoint) consistently.

        Parameters
        ----------
        top : float
        bottom : float

        Returns
        -------
        float
            Midpoint of the gap.
        """
        return (top + bottom) / 2

    # ==========================================================
    # PUBLIC METHODS
    # ==========================================================

    def detect(
        self,
        candles: List[dict],
    ) -> Response:
        """
        Detect Fair Value Gaps.

        Parameters
        ----------
        candles : List[dict]

        Returns
        -------
        Response
        """

        # ------------------------------------------------------
        # Validate candle input
        # ------------------------------------------------------

        if not candles:

            logger.error("No candle data supplied.")

            return Response(
                success=False,
                message="No candle data supplied.",
                error="EMPTY_CANDLES",
                data=None,
            )

        if len(candles) < self.DEFAULT_MIN_CANDLES:

            logger.error(
                "At least %d candles are required.",
                self.DEFAULT_MIN_CANDLES,
            )

            return Response(
                success=False,
                message=(
                    f"At least {self.DEFAULT_MIN_CANDLES} candles are required."
                ),
                error="INSUFFICIENT_CANDLES",
                data=None,
            )

        bullish_fvg: List[dict] = []
        bearish_fvg: List[dict] = []

        valid_candle_count = 0

        # ------------------------------------------------------
        # Detection logic
        # ------------------------------------------------------
        for index in range(1, len(candles) - 1):

            previous = candles[index - 1]
            current = candles[index]
            nxt = candles[index + 1]

            previous_fields = self._extract_candle_fields(previous)
            current_fields = self._extract_candle_fields(current)
            next_fields = self._extract_candle_fields(nxt)

            if (
                previous_fields is None
                or current_fields is None
                or next_fields is None
            ):
                continue

            valid_candle_count += 1

            # Only required fields
            _, _, previous_high, previous_low = previous_fields
            current_open, current_close, current_high, current_low = current_fields
            _, _, next_high, next_low = next_fields

            # --------------------------------------------------
            # Bullish Fair Value Gap
            # --------------------------------------------------

            if previous_high < next_low:

                gap_top = next_low
                gap_bottom = previous_high
                gap_size = gap_top - gap_bottom
                midpoint = self._calculate_midpoint(gap_top, gap_bottom)

                bullish_fvg.append(
                    {
                        "id": f"FVG_{index}",
                        "index": index,
                        "created_index": index,
                        "type": "BULLISH_FVG",
                        "direction": "BULLISH",

                        # Gap boundaries
                        "top": gap_top,
                        "bottom": gap_bottom,
                        "midpoint": midpoint,
                        "consequent_encroachment": midpoint,

                        # Measurements
                        "gap_size": gap_size,

                        # Impulse candle
                        "impulse_open": current_open,
                        "impulse_close": current_close,
                        "impulse_high": current_high,
                        "impulse_low": current_low,

                        # Metadata
                        "time": current.get("time"),
                    }
                )

            # --------------------------------------------------
            # Bearish Fair Value Gap
            # --------------------------------------------------

            if previous_low > next_high:

                gap_top = previous_low
                gap_bottom = next_high
                gap_size = gap_top - gap_bottom
                midpoint = self._calculate_midpoint(gap_top, gap_bottom)

                bearish_fvg.append(
                    {
                        "id": f"FVG_{index}",
                        "index": index,
                        "created_index": index,
                        "type": "BEARISH_FVG",
                        "direction": "BEARISH",

                        # Gap boundaries
                        "top": gap_top,
                        "bottom": gap_bottom,
                        "midpoint": midpoint,
                        "consequent_encroachment": midpoint,

                        # Measurements
                        "gap_size": gap_size,

                        # Impulse candle
                        "impulse_open": current_open,
                        "impulse_close": current_close,
                        "impulse_high": current_high,
                        "impulse_low": current_low,

                        # Metadata
                        "time": current.get("time"),
                    }
                )

        # ------------------------------------------------------
        # Validate detected candle data
        # ------------------------------------------------------

        if valid_candle_count == 0:

            logger.error(
                "All candles supplied are malformed."
            )

            return Response(
                success=False,
                message="Invalid candle data.",
                error="INVALID_CANDLE_DATA",
                data=None,
            )

        # ------------------------------------------------------
        # Detection Summary
        # ------------------------------------------------------

        fvg_found = bool(
            bullish_fvg or bearish_fvg
        )

        logger.info(
            (
                "FVG Detection | "
                "Bullish=%d "
                "Bearish=%d"
            ),
            len(bullish_fvg),
            len(bearish_fvg),
        )

        # ------------------------------------------------------
        # Return Response
        # ------------------------------------------------------

        return Response(
            success=True,
            message=(
                "Fair Value Gap detected."
                if fvg_found
                else "No Fair Value Gap detected."
            ),
            error=None,
            data={
                "fvg_found": fvg_found,

                "bullish_fvg": bullish_fvg,
                "bearish_fvg": bearish_fvg,

                "bullish_count": len(
                    bullish_fvg
                ),
                "bearish_count": len(
                    bearish_fvg
                ),
            },
        )
