"""

UDUAK_QUANT_SYSTEM_PROJECT

File: analysis/candle_analyzer.py

Description:
    Analyze a single candle and calculate descriptive metrics.

Responsibilities:
    - Analyze one candle.
    - Calculate body percentage.
    - Calculate upper wick percentage.
    - Calculate lower wick percentage.
    - Identify the dominant candle component.
    - Return standardized Response objects.

This module NEVER:
    - Connects to MetaTrader 5.
    - Reads market data.
    - Executes trades.
    - Detects candle patterns.
    - Detects chart patterns.
    - Calculates indicators.
    - Performs risk management.

"""

from __future__ import annotations

from models.response import Response
from monitoring.logger import get_logger

logger = get_logger(__name__)

class CandleAnalyzer:
    """
    Analyze a single candle.

    This class converts raw candle measurements into
    descriptive statistics that can later be used by
    pattern recognition and trading strategies.
    """

    # =====================================================================
    # PUBLIC METHODS
    # =====================================================================

    def analyze(
        self,
        candle: dict,
    ) -> Response:
        """
        Analyze a single candle.

        Parameters

        candle : dict
            Candle returned from CandleData.

        Returns

        Response
            Standard project response.
        """

        if not candle:

            logger.error("No candle supplied for analysis.")

            return Response(
                success=False,
                message="No candle supplied.",
                error=None,
                data=None,
            )

        candle_range = candle["candle_range"]

        if candle_range <= 0:

            logger.error("Invalid candle range.")

            return Response(
                success=False,
                message="Invalid candle range.",
                error=None,
                data=None,
            )

        # ==============================================================
        # Calculate percentages
        # ==============================================================

        body_percent = round(
            (candle["body"] / candle_range) * 100,
            2,
        )

        upper_wick_percent = round(
            (candle["upper_wick"] / candle_range) * 100,
            2,
        )

        lower_wick_percent = round(
            (candle["lower_wick"] / candle_range) * 100,
            2,
        )

        # ==============================================================
        # Determine dominant candle component
        # ==============================================================

        dominant_part = "BODY"

        largest = max(
            candle["body"],
            candle["upper_wick"],
            candle["lower_wick"],
        )

        if largest == candle["upper_wick"]:

            dominant_part = "UPPER_WICK"

        elif largest == candle["lower_wick"]:

            dominant_part = "LOWER_WICK"

        # ==============================================================
        # Candle strength
        # ==============================================================

        strong_body = body_percent >= 70.0

        long_upper_wick = upper_wick_percent >= 50.0

        long_lower_wick = lower_wick_percent >= 50.0

        # ==============================================================
        # Analysis Result
        # ==============================================================

        analysis = {
            "body_percent": body_percent,
            "upper_wick_percent": upper_wick_percent,
            "lower_wick_percent": lower_wick_percent,
            "dominant_part": dominant_part,
            "strong_body": strong_body,
            "long_upper_wick": long_upper_wick,
            "long_lower_wick": long_lower_wick,
            "bullish": candle["bullish"],
            "bearish": candle["bearish"],
        }

        logger.info("Candle analyzed successfully.")

        return Response(
            success=True,
            message="Candle analyzed successfully.",
            error=None,
            data=analysis,
        )