"""

UDUAK_QUANT_SYSTEM_PROJECT

File: analysis/choch_detector.py

Description:
    Detects Change of Character (CHOCH).

Responsibilities:
    - Validate market structure.
    - Detect bullish CHOCH.
    - Detect bearish CHOCH.
    - Return standardized Response objects.

This module NEVER:
    - Reads MT5 data.
    - Retrieves candles.
    - Detects swing highs/lows.
    - Executes trades.
    - Performs risk management.

"""

from __future__ import annotations

from typing import List

from models.response import Response
from monitoring.logger import get_logger

logger = get_logger(__name__)

class CHOCHDetector:
    """
    Detect Change of Character (CHOCH).

    CHOCH identifies the first structural shift that
    suggests the existing market trend may be reversing.

    Input:
        Output from MarketStructure.

    Output:
        Standard Response object.
    """

    # =====================================================================
    # PUBLIC METHODS
    # =====================================================================

    def detect(
        self,
        structure: List[dict],
    ) -> Response:
        """
        Detect Change of Character.

        Parameters

        structure : List[dict]
            Market structure output.

        Returns

        Response
            Standard project response.
        """

        # -------------------------------------------------------------
        # Validation
        # -------------------------------------------------------------

        if not structure:
            logger.error("No market structure supplied.")
            return Response(
                success=False,
                message="No market structure supplied.",
                error="EMPTY_STRUCTURE",
                data=None,
            )

        if len(structure) < 4:
            logger.error("At least four structure points are required.")
            return Response(
                success=False,
                message="At least four structure points are required.",
                error="INSUFFICIENT_STRUCTURE",
                data=None,
            )

        bullish_choch = False
        bearish_choch = False
        direction = "NONE"
        broken_level = None

        # -------------------------------------------------------------
        # Analyze recent market structure
        # -------------------------------------------------------------

        recent = structure[-4:]

        labels = [
            item.get("structure")
            for item in recent
        ]

        recent_labels = labels[-2:]

        # -------------------------------------------------------------
        # Bullish CHOCH
        # Market has started making bullish structure:
        # HIGHER_LOW -> HIGHER_HIGH
        # -------------------------------------------------------------

        if recent_labels == [
            "HIGHER_LOW",
            "HIGHER_HIGH",
        ]:
            bullish_choch = True
            direction = "BULLISH"

            for item in reversed(recent):
                if item.get("structure") == "HIGHER_HIGH":
                    broken_level = item.get("price")
                    break

        # -------------------------------------------------------------
        # Bearish CHOCH
        # Market has started making bearish structure:
        # LOWER_HIGH -> LOWER_LOW
        # -------------------------------------------------------------

        elif recent_labels == [
            "LOWER_HIGH",
            "LOWER_LOW",
        ]:
            bearish_choch = True
            direction = "BEARISH"

            for item in reversed(recent):
                if item.get("structure") == "LOWER_LOW":
                    broken_level = item.get("price")
                    break

        # -------------------------------------------------------------
        # No CHOCH detected
        # -------------------------------------------------------------

        if not bullish_choch and not bearish_choch:
            logger.info("No Change of Character detected.")
            return Response(
                success=True,
                message="No Change of Character detected.",
                error=None,
                data={
                    "choch": False,
                    "direction": "NONE",
                    "broken_level": None,
                    "bullish_choch": False,
                    "bearish_choch": False,
                },
            )

        # -------------------------------------------------------------
        # CHOCH detected
        # -------------------------------------------------------------

        logger.info(
            "Change of Character detected. "
            "Direction=%s Level=%s",
            direction,
            broken_level,
        )

        return Response(
            success=True,
            message="Change of Character detected.",
            error=None,
            data={
                "choch": True,
                "direction": direction,
                "broken_level": broken_level,
                "bullish_choch": bullish_choch,
                "bearish_choch": bearish_choch,
            },
        )