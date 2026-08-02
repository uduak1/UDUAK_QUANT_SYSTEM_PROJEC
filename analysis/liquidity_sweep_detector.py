"""

UDUAK_QUANT_SYSTEM_PROJECT

File: analysis/liquidity_sweep_detector.py

Description:
    Detects institutional liquidity sweeps.

Responsibilities:
    - Detect Buy-Side Liquidity Sweep
    - Detect Sell-Side Liquidity Sweep
    - Validate sweep conditions
    - Return standardized Response objects

This module NEVER:
    - Reads MT5 data
    - Retrieves candles
    - Executes trades
    - Performs risk management
    - Detects BOS
    - Detects CHOCH

"""

from __future__ import annotations

from typing import List

from models.response import Response
from monitoring.logger import get_logger

logger = get_logger(__name__)

class LiquiditySweepDetector:
    """
    Detect institutional liquidity sweeps.

    Input:
        Candle data together with liquidity levels.

    Output:
        Standard Response object.
    """

    DEFAULT_TOLERANCE = 0.00010

    # =====================================================================
    # PUBLIC METHODS
    # =====================================================================

    def detect(
        self,
        candles: List[dict],
        liquidity: dict,
    ) -> Response:
        """
        Detect liquidity sweeps.

        Parameters

        candles : List[dict]
            Candle data.

        liquidity : dict
            Output from LiquidityDetector.

        Returns

        Response
        """

        # -------------------------------------------------------------
        # Validate candle input
        # -------------------------------------------------------------

        if not candles:
            logger.error("No candle data supplied.")

            return Response(
                success=False,
                message="No candle data supplied.",
                error="EMPTY_CANDLES",
                data=None,
            )

        if len(candles) < 2:
            logger.error(
                "At least two candles are required."
            )

            return Response(
                success=False,
                message="At least two candles are required.",
                error="INSUFFICIENT_CANDLES",
                data=None,
            )

        # -------------------------------------------------------------
        # Validate liquidity input
        # -------------------------------------------------------------

        if not liquidity:
            logger.error("No liquidity data supplied.")

            return Response(
                success=False,
                message="No liquidity data supplied.",
                error="EMPTY_LIQUIDITY",
                data=None,
            )

        buy_levels = liquidity.get(
            "buy_side_liquidity",
            [],
        )

        sell_levels = liquidity.get(
            "sell_side_liquidity",
            [],
        )

        tolerance = self.DEFAULT_TOLERANCE

        buy_side_sweeps: List[dict] = []

        sell_side_sweeps: List[dict] = []

        # -------------------------------------------------------------
        # Detect Liquidity Sweeps (Single-Pass)
        # -------------------------------------------------------------

        for candle_index, candle in enumerate(candles):

            high = candle.get("high")
            low = candle.get("low")
            close = candle.get("close")

            if close is None:
                continue

            # ---------------------------
            # Buy-Side Liquidity Sweeps
            # ---------------------------
            if high is not None:
                for level in buy_levels:
                    # Price traded above liquidity
                    if high > level + tolerance:
                        # But failed to hold above it
                        if close < level:
                            buy_side_sweeps.append(
                                {
                                    "index": candle_index,
                                    "level": level,
                                    "high": high,
                                    "close": close,
                                    "direction": "BUY_SIDE",
                                }
                            )

            # ----------------------------
            # Sell-Side Liquidity Sweeps
            # ----------------------------
            if low is not None:
                for level in sell_levels:
                    # Price traded below liquidity
                    if low < level - tolerance:
                        # But failed to remain below it
                        if close > level:
                            sell_side_sweeps.append(
                                {
                                    "index": candle_index,
                                    "level": level,
                                    "low": low,
                                    "close": close,
                                    "direction": "SELL_SIDE",
                                }
                            )

        # -------------------------------------------------------------
        # Sweep summary
        # -------------------------------------------------------------

        sweep_found = (
            len(buy_side_sweeps) > 0
            or len(sell_side_sweeps) > 0
        )

        logger.info(
            "Liquidity Sweep Detection | "
            "Buy Sweeps=%d Sell Sweeps=%d",
            len(buy_side_sweeps),
            len(sell_side_sweeps),
        )

        return Response(
            success=True,
            message=(
                "Liquidity sweep detected."
                if sweep_found
                else "No liquidity sweep detected."
            ),
            error=None,
            data={
                "sweep_found": sweep_found,
                "buy_side_sweeps": buy_side_sweeps,
                "sell_side_sweeps": sell_side_sweeps,
                "buy_sweep_count": len(buy_side_sweeps),
                "sell_sweep_count": len(sell_side_sweeps),
            },
        )