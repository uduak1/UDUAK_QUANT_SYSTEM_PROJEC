"""

UDUAK_QUANT_SYSTEM_PROJECT

File: analysis/candle_patterns.py

Description:
    Detect candlestick patterns from analyzed candle data.

Responsibilities:
    - Detect single-candle patterns.
    - Detect multi-candle patterns.
    - Return standardized Response objects.

This module NEVER:
    - Connects to MetaTrader 5.
    - Reads market data.
    - Executes trades.
    - Calculates indicators.
    - Performs risk management.

"""

from __future__ import annotations

from models.response import Response
from monitoring.logger import get_logger

logger = get_logger(__name__)

class CandlePatterns:
    """
    Detect candlestick patterns.

    This class receives one or more analyzed candles and
    identifies well-known candlestick patterns.

    It does NOT decide whether to buy or sell.
    """

    # =========================================================================
    # PUBLIC METHODS
    # =========================================================================

    def detect(
        self,
        candles: list[dict],
    ) -> Response:
        """
        Detect candlestick patterns.

        Parameters

        candles : list[dict]
            One or more analyzed candles.

        Returns

        Response
            Standard project response.
        """

        if not candles:

            logger.error("No candles supplied.")

            return Response(
                success=False,
                message="No candles supplied.",
                error=None,
                data=None,
            )

        if not isinstance(candles, list):

            logger.error("Candles must be provided as a list.")

            return Response(
                success=False,
                message="Candles must be a list.",
                error=None,
                data=None,
            )

        patterns = []

        current = candles[-1]

        if self._is_doji(current):
            patterns.append("DOJI")

        if self._is_marubozu(current):
            patterns.append("MARUBOZU")

        if self._is_spinning_top(current):
            patterns.append("SPINNING_TOP")

        if self._is_hammer(current):
            patterns.append("HAMMER")

        if self._is_hanging_man(current):
            patterns.append("HANGING_MAN")

        if self._is_inverted_hammer(current):
            patterns.append("INVERTED_HAMMER")

        if self._is_shooting_star(current):
            patterns.append("SHOOTING_STAR")

        # ==============================================================
        # Two-Candle Patterns
        # ==============================================================

        if len(candles) >= 2:

            previous = candles[-2]

            if self._is_bullish_engulfing(previous, current):
                patterns.append("BULLISH_ENGULFING")

            if self._is_bearish_engulfing(previous, current):
                patterns.append("BEARISH_ENGULFING")

            if self._is_bullish_harami(previous, current):
                patterns.append("BULLISH_HARAMI")

            if self._is_bearish_harami(previous, current):
                patterns.append("BEARISH_HARAMI")

            if self._is_tweezer_top(previous, current):
                patterns.append("TWEEZER_TOP")

            if self._is_tweezer_bottom(previous, current):
                patterns.append("TWEEZER_BOTTOM")

        # ==============================================================
        # Three-Candle Patterns
        # ==============================================================

        if len(candles) >= 3:

            first = candles[-3]
            second = candles[-2]
            third = candles[-1]

            if self._is_morning_star(first, second, third):
                patterns.append("MORNING_STAR")

            if self._is_evening_star(first, second, third):
                patterns.append("EVENING_STAR")

            if self._is_three_white_soldiers(first, second, third):
                patterns.append("THREE_WHITE_SOLDIERS")

            if self._is_three_black_crows(first, second, third):
                patterns.append("THREE_BLACK_CROWS")

        logger.info(
            "Analyzing %d candle(s) for candlestick patterns.",
            len(candles),
        )

        return Response(
            success=True,
            message="Pattern detection completed.",
            error=None,
            data=patterns,
        )

    # =========================================================================
    # PRIVATE METHODS
    # =========================================================================

    def _is_doji(
        self,
        candle: dict,
    ) -> bool:
        """
        Detect a Doji candle.
        """

        return candle["body_percent"] <= 10.0

    def _is_marubozu(
        self,
        candle: dict,
    ) -> bool:
        """
        Detect a Marubozu candle.
        """

        return (
            candle["body_percent"] >= 90.0
            and candle["upper_wick_percent"] <= 5.0
            and candle["lower_wick_percent"] <= 5.0
        )

    def _is_spinning_top(
        self,
        candle: dict,
    ) -> bool:
        """
        Detect a Spinning Top candle.
        """

        return (
            candle["body_percent"] < 40.0
            and candle["upper_wick_percent"] > 20.0
            and candle["lower_wick_percent"] > 20.0
        )

    def _is_hammer(
        self,
        candle: dict,
    ) -> bool:
        """
        Detect a Hammer candle.
        """

        return (
            candle["body_percent"] <= 40.0
            and candle["lower_wick_percent"] >= 50.0
            and candle["upper_wick_percent"] <= 15.0
            and candle["bullish"]
        )

    def _is_hanging_man(
        self,
        candle: dict,
    ) -> bool:
        """
        Detect a Hanging Man candle.
        """

        return (
            candle["body_percent"] <= 40.0
            and candle["lower_wick_percent"] >= 50.0
            and candle["upper_wick_percent"] <= 15.0
            and candle["bearish"]
        )

    def _is_inverted_hammer(
        self,
        candle: dict,
    ) -> bool:
        """
        Detect an Inverted Hammer candle.
        """

        return (
            candle["body_percent"] <= 40.0
            and candle["upper_wick_percent"] >= 50.0
            and candle["lower_wick_percent"] <= 15.0
            and candle["bullish"]
        )

    def _is_shooting_star(
        self,
        candle: dict,
    ) -> bool:
        """
        Detect a Shooting Star candle.
        """

        return (
            candle["body_percent"] <= 40.0
            and candle["upper_wick_percent"] >= 50.0
            and candle["lower_wick_percent"] <= 15.0
            and candle["bearish"]
        )

    def _is_bullish_engulfing(
        self,
        previous: dict,
        current: dict,
    ) -> bool:
        """
        Detect Bullish Engulfing.
        """

        return (
            previous["bearish"]
            and current["bullish"]
            and current["open"] < previous["close"]
            and current["close"] > previous["open"]
        )

    def _is_bearish_engulfing(
        self,
        previous: dict,
        current: dict,
    ) -> bool:
        """
        Detect Bearish Engulfing.
        """

        return (
            previous["bullish"]
            and current["bearish"]
            and current["open"] > previous["close"]
            and current["close"] < previous["open"]
        )

    def _is_bullish_harami(
        self,
        previous: dict,
        current: dict,
    ) -> bool:
        """
        Detect Bullish Harami.
        """

        return (
            previous["bearish"]
            and current["bullish"]
            and current["open"] > previous["close"]
            and current["close"] < previous["open"]
        )

    def _is_bearish_harami(
        self,
        previous: dict,
        current: dict,
    ) -> bool:
        """
        Detect Bearish Harami.
        """

        return (
            previous["bullish"]
            and current["bearish"]
            and current["open"] < previous["close"]
            and current["close"] > previous["open"]
        )

    def _is_tweezer_top(
        self,
        previous: dict,
        current: dict,
    ) -> bool:
        """
        Detect Tweezer Top.
        """

        return (
            abs(previous["high"] - current["high"]) <= 0.00001
        )

    def _is_tweezer_bottom(
        self,
        previous: dict,
        current: dict,
    ) -> bool:
        """
        Detect Tweezer Bottom.
        """

        return (
            abs(previous["low"] - current["low"]) <= 0.00001
        )

    def _is_morning_star(
        self,
        first: dict,
        second: dict,
        third: dict,
    ) -> bool:
        """
        Detect Morning Star.
        """

        return (
            first["bearish"]
            and second["body_percent"] <= 20.0
            and third["bullish"]
        )

    def _is_evening_star(
        self,
        first: dict,
        second: dict,
        third: dict,
    ) -> bool:
        """
        Detect Evening Star.
        """

        return (
            first["bullish"]
            and second["body_percent"] <= 20.0
            and third["bearish"]
        )

    def _is_three_white_soldiers(
        self,
        first: dict,
        second: dict,
        third: dict,
    ) -> bool:
        """
        Detect Three White Soldiers.
        """

        return (
            first["bullish"]
            and second["bullish"]
            and third["bullish"]
            and first["strong_body"]
            and second["strong_body"]
            and third["strong_body"]
        )

    def _is_three_black_crows(
        self,
        first: dict,
        second: dict,
        third: dict,
    ) -> bool:
        """
        Detect Three Black Crows.
        """

        return (
            first["bearish"]
            and second["bearish"]
            and third["bearish"]
            and first["strong_body"]
            and second["strong_body"]
            and third["strong_body"]
        )