"""
===============================================================================
UDUAK_QUANT_SYSTEM_PROJECT
-------------------------------------------------------------------------------
File: analysis/bos_detector.py

Description:
    Detects Break of Structure (BOS) using market structure.

Responsibilities:
    - Validate market structure data.
    - Detect bullish BOS.
    - Detect bearish BOS.
    - Return standardized Response objects.

This module NEVER:
    - Reads MT5 data.
    - Retrieves candles.
    - Detects swing highs/lows.
    - Detects candle patterns.
    - Detects chart patterns.
    - Executes trades.
    - Performs risk management.
===============================================================================
"""

from __future__ import annotations

from typing import List

from models.response import Response
from monitoring.logger import get_logger

logger = get_logger(__name__)


class BOSDetector:
    """
    Detect Break of Structure (BOS).

    This class analyzes the output of MarketStructure and
    determines whether price has produced a valid bullish
    or bearish Break of Structure.

    Future modules:

        • CHOCH
        • Liquidity
        • Order Blocks
        • Signal Engine

    will consume the output of this detector.
    """

    # =====================================================================
    # PUBLIC METHODS
    # =====================================================================

    def detect(
        self,
        structure: List[dict],
    ) -> Response:
        """
        Detect Break of Structure.

        Parameters
        ----------
        structure : List[dict]
            Output from MarketStructure.

        Returns
        -------
        Response
            Standard project response.
        """

        # -------------------------------------------------------------
        # Validation
        # -------------------------------------------------------------

        if not structure:

            logger.error(
                "No market structure supplied."
            )

            return Response(
                success=False,
                message="No market structure supplied.",
                error="EMPTY_STRUCTURE",
                data=None,
            )

        if len(structure) < 3:

            logger.error(
                "At least three structure points are required."
            )

            return Response(
                success=False,
                message=(
                    "At least three structure points are required."
                ),
                error="INSUFFICIENT_STRUCTURE",
                data=None,
            )

        bullish_bos = False

        bearish_bos = False

        broken_level = None

        direction = "NONE"

        # -------------------------------------------------------------
        # Analyze recent market structure
        # -------------------------------------------------------------

        recent = structure[-4:]

        labels = [
            item["structure"]
            for item in recent
        ]

        prices = [
            item["price"]
            for item in recent
        ]

        # -------------------------------------------------------------
        # Bullish BOS
        # -------------------------------------------------------------

        if (
            "HIGHER_HIGH" in labels
            and "HIGHER_LOW" in labels
        ):

            bullish_bos = True

            direction = "BULLISH"

            for item in reversed(recent):

                if (
                    item["structure"]
                    == "HIGHER_HIGH"
                ):

                    broken_level = item["price"]

                    break

        # -------------------------------------------------------------
        # Bearish BOS
        # -------------------------------------------------------------

        elif (
            "LOWER_HIGH" in labels
            and "LOWER_LOW" in labels
        ):

            bearish_bos = True

            direction = "BEARISH"

            for item in reversed(recent):

                if (
                    item["structure"]
                    == "LOWER_LOW"
                ):

                    broken_level = item["price"]

                    break

        # -------------------------------------------------------------
        # No BOS detected
        # -------------------------------------------------------------

        if not bullish_bos and not bearish_bos:

            logger.info(
                "No Break of Structure detected."
            )

            return Response(
                success=True,
                message="No Break of Structure detected.",
                error=None,
                data={
                    "bos": False,
                    "direction": "NONE",
                    "broken_level": None,
                },
            )

        # -------------------------------------------------------------
        # BOS detected
        # -------------------------------------------------------------

        logger.info(
            "Break of Structure detected. "
            "Direction=%s Level=%s",
            direction,
            broken_level,
        )

        return Response(
            success=True,
            message="Break of Structure detected.",
            error=None,
            data={
                "bos": True,
                "direction": direction,
                "broken_level": broken_level,
                "bullish_bos": bullish_bos,
                "bearish_bos": bearish_bos,
            },
        )
