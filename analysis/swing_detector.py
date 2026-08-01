"""

UDUAK_QUANT_SYSTEM_PROJECT

File: analysis/swing_detector.py

Description:
    Detects market swing highs and swing lows from analyzed candles.

Responsibilities:
    - Validate candle data.
    - Detect swing highs.
    - Detect swing lows.
    - Return standardized Response objects.

This module NEVER:
    - Connects to MT5.
    - Retrieve market data.
    - Execute trades.
    - Detect chart patterns.
    - Perform risk management.

"""

from __future__ import annotations

from typing import List

from models.response import Response
from monitoring.logger import get_logger

logger = get_logger(__name__)

class SwingDetector:
    """
    Detect market swing highs and swing lows.

    A swing high is a candle whose HIGH is greater than
    neighboring candles.

    A swing low is a candle whose LOW is lower than
    neighboring candles.
    """

    def detect(
        self,
        candles: List[dict],
        lookback: int = 2,
    ) -> Response:
        """
        Detect swing highs and lows.

        Parameters

        candles : List[dict]
            Candle data.

        lookback : int
            Number of candles to compare on each side.

        Returns

        Response
            Standard project response.
        """

        # ---------------------------------------------------------
        # Validation
        # ---------------------------------------------------------

        if not candles:

            logger.warning("No candles supplied.")

            return Response(
                success=False,
                message="No candle data supplied.",
                error=None,
                data=None,
            )

        minimum_required = (lookback * 2) + 1

        if len(candles) < minimum_required:

            logger.warning(
                "Not enough candles to detect swings."
            )

            return Response(
                success=False,
                message=(
                    f"At least {minimum_required} candles "
                    "are required."
                ),
                error=None,
                data=None,
            )

        swings = []

        # ---------------------------------------------------------
        # Detect Swing Highs
        # ---------------------------------------------------------

        for index in range(
            lookback,
            len(candles) - lookback,
        ):

            current = candles[index]

            current_high = current["high"]

            is_swing_high = True

            for offset in range(
                1,
                lookback + 1,
            ):

                left = candles[index - offset]

                right = candles[index + offset]

                if (
                    current_high <= left["high"]
                    or
                    current_high <= right["high"]
                ):

                    is_swing_high = False

                    break

            if is_swing_high:

                swings.append(
                    {
                        "type": "SWING_HIGH",
                        "index": index,
                        "time": current["time"],
                        "price": current_high,
                    }
                )

        # ---------------------------------------------------------
        # Detect Swing Lows
        # ---------------------------------------------------------

        for index in range(
            lookback,
            len(candles) - lookback,
        ):

            current = candles[index]

            current_low = current["low"]

            is_swing_low = True

            for offset in range(
                1,
                lookback + 1,
            ):

                left = candles[index - offset]

                right = candles[index + offset]

                if (
                    current_low >= left["low"]
                    or
                    current_low >= right["low"]
                ):

                    is_swing_low = False

                    break

            if is_swing_low:

                swings.append(
                    {
                        "type": "SWING_LOW",
                        "index": index,
                        "time": current["time"],
                        "price": current_low,
                    }
                )

        # ---------------------------------------------------------
        # Sort swings by candle position
        # ---------------------------------------------------------

        swings.sort(
            key=lambda swing: swing["index"]
        )

        # ---------------------------------------------------------
        # Classify swings
        # ---------------------------------------------------------

        previous_high = None

        previous_low = None

        for swing in swings:

            # ---------------------------------------------
            # Swing High
            # ---------------------------------------------

            if swing["type"] == "SWING_HIGH":

                if previous_high is None:

                    swing["structure"] = "INITIAL_HIGH"

                elif swing["price"] > previous_high:

                    swing["structure"] = "HIGHER_HIGH"

                elif swing["price"] < previous_high:

                    swing["structure"] = "LOWER_HIGH"

                else:

                    swing["structure"] = "EQUAL_HIGH"

                previous_high = swing["price"]

            # ---------------------------------------------
            # Swing Low
            # ---------------------------------------------

            else:

                if previous_low is None:

                    swing["structure"] = "INITIAL_LOW"

                elif swing["price"] > previous_low:

                    swing["structure"] = "HIGHER_LOW"

                elif swing["price"] < previous_low:

                    swing["structure"] = "LOWER_LOW"

                else:

                    swing["structure"] = "EQUAL_LOW"

                previous_low = swing["price"]

        logger.info(
            "Swing detection completed."
        )

        return Response(
            success=True,
            message="Swing detection completed.",
            error=None,
            data=swings,
        )