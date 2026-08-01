"""

UDUAK_QUANT_SYSTEM_PROJECT

File: analysis/liquidity_detector.py

Description:
    Detects institutional liquidity zones.

Responsibilities:
    - Detect Buy-Side Liquidity (BSL)
    - Detect Sell-Side Liquidity (SSL)
    - Detect Equal Highs
    - Detect Equal Lows
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

class LiquidityDetector:
    """
    Detect institutional liquidity.

    Input:
        Swing highs/lows or market structure.

    Output:
        Standard Response object.
    """

    DEFAULT_TOLERANCE = 0.00010

    # =====================================================================
    # PUBLIC METHODS
    # =====================================================================

    def detect(
        self,
        swings: List[dict],
    ) -> Response:
        """
        Detect liquidity pools.

        Parameters

        swings : List[dict]

        Returns

        Response
        """

        # -------------------------------------------------------------
        # Validation
        # -------------------------------------------------------------

        if not swings:
            logger.error("No swing data supplied.")
            return Response(
                success=False,
                message="No swing data supplied.",
                error="EMPTY_SWINGS",
                data=None,
            )

        if len(swings) < 2:
            logger.error("At least two swing points are required.")
            return Response(
                success=False,
                message="At least two swing points are required.",
                error="INSUFFICIENT_SWINGS",
                data=None,
            )

        buy_side = []
        sell_side = []
        equal_highs = []
        equal_lows = []

        # Use class constant - easier to make symbol-aware later
        tolerance = self.DEFAULT_TOLERANCE

        # -------------------------------------------------------------
        # Detect liquidity pools
        # -------------------------------------------------------------

        for index in range(len(swings) - 1):
            current = swings[index]
            nxt = swings[index + 1]

            current_type = current.get("type")
            next_type = nxt.get("type")

            current_price = current.get("price")
            next_price = nxt.get("price")

            if current_price is None or next_price is None:
                continue

            # ---------------------------------------------------------
            # Equal Highs (Buy-Side Liquidity)
            # ---------------------------------------------------------
            if (
                current_type == "SWING_HIGH"
                and next_type == "SWING_HIGH"
            ):
                if abs(current_price - next_price) <= tolerance:
                    level = round(
                        (current_price + next_price) / 2,
                        10,
                    )
                    equal_highs.append(level)
                    buy_side.append(level)

            # ---------------------------------------------------------
            # Equal Lows (Sell-Side Liquidity)
            # ---------------------------------------------------------
            elif (
                current_type == "SWING_LOW"
                and next_type == "SWING_LOW"
            ):
                if abs(current_price - next_price) <= tolerance:
                    level = round(
                        (current_price + next_price) / 2,
                        10,
                    )
                    equal_lows.append(level)
                    sell_side.append(level)

        # -------------------------------------------------------------
        # Remove duplicate levels
        # -------------------------------------------------------------
        # Fixes: 1.1050, 1.1050, 1.1050 -> [1.1050] instead of [1.1050, 1.1050]

        buy_side = sorted(set(buy_side))
        sell_side = sorted(set(sell_side))
        equal_highs = sorted(set(equal_highs))
        equal_lows = sorted(set(equal_lows))

        # -------------------------------------------------------------
        # Liquidity summary
        # -------------------------------------------------------------

        liquidity_found = len(buy_side) > 0 or len(sell_side) > 0

        logger.info(
            "Liquidity Detection | "
            "BSL=%d SSL=%d EQH=%d EQL=%d",
            len(buy_side),
            len(sell_side),
            len(equal_highs),
            len(equal_lows),
        )

        return Response(
            success=True,
            message=(
                "Liquidity detected." if liquidity_found else "No liquidity detected."
            ),
            error=None,
            data={
                "liquidity_found": liquidity_found,
                "buy_side_liquidity": buy_side,
                "sell_side_liquidity": sell_side,
                "equal_highs": equal_highs,
                "equal_lows": equal_lows,
                "buy_side_count": len(buy_side),
                "sell_side_count": len(sell_side),
            },
        )