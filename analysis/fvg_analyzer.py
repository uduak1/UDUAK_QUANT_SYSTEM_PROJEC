"""
UDUAK_QUANT_SYSTEM_PROJECT

File: analysis/fvg_analyzer.py

Description:
    Performs analysis on previously detected Fair Value Gaps (FVG).

Responsibilities:
    - Calculate gap size
    - Calculate midpoint (Consequent Encroachment)
    - Calculate fill percentage
    - Calculate retest count
    - Calculate age
    - Determine mitigation status
    - Return standardized Response objects

This module NEVER:
    - Detect Fair Value Gaps
    - Read MT5 data
    - Retrieve candles
    - Execute trades
    - Perform risk management
    - Detect BOS
    - Detect CHOCH
    - Detect Liquidity
    - Detect Order Blocks
    - Score trade quality
    - Filter sessions
    - Filter trend
"""

from __future__ import annotations

from typing import List
from typing import Optional
from typing import Tuple

from models.response import Response
from monitoring.logger import get_logger

logger = get_logger(__name__)

class FVGAnalyzer:
    """
    Analyze previously detected Fair Value Gaps.

    IMPORTANT

    This class DOES NOT detect Fair Value Gaps.

    It only receives FVGs that were already detected
    by FVGDetector and enriches them with additional
    analytical information.

    Input

    Historical candles

    Detected FVG list

    Output

    Standard Response object.
    """

    FULL_FILL_PERCENTAGE = 100.0

        # ------------------------------------------------------------------
    # Public wrappers
    # ------------------------------------------------------------------

    def validate_fvg(self, fvg):
        """
        Public wrapper around _validate_fvg().

        Exists so external callers and unit tests can validate a single FVG
        without depending on private implementation details.
        """
        return self._validate_fvg(fvg)

    def is_mitigated(self, fvg):
        """
        Public wrapper that accepts an FVG dictionary.
        """

        if not isinstance(fvg, dict):
            return False

        status = fvg.get("status")

        if status is None:
            return False

        if status == "MITIGATED":
            return True

        return False

    # ==========================================================
    # PRIVATE HELPERS
    # ==========================================================

    def _validate_fvg(
        self,
        fvg: dict,
    ) -> bool:
        if not isinstance(fvg, dict):
            return False

        required_keys = (
            "top",
            "bottom",
            "created_index",
            "direction",
        )

        if not all(key in fvg for key in required_keys):
            return False

        if not isinstance(fvg["top"], (int, float)):
            return False

        if not isinstance(fvg["bottom"], (int, float)):
            return False

        if fvg["top"] <= fvg["bottom"]:
            return False

        if not isinstance(fvg["created_index"], int):
            return False

        if fvg["direction"] not in ("BULLISH", "BEARISH"):
            return False

        return True

    def _extract_candle_fields(
        self,
        candle: dict,
    ) -> Optional[Tuple[float, float]]:
        """
        Extract only the High and Low values.

        The analyzer only needs High and Low because
        it is measuring how price interacted with
        the existing Fair Value Gap.

        Parameters

        candle : dict

        Returns

        Tuple

            (high, low)

        None

            If candle is malformed.
        """

        high = candle.get("high")
        low = candle.get("low")

        if high is None or low is None:
            return None

        if high < low:
            return None

        return (
            high,
            low,
        )

    def _calculate_gap_size(
        self,
        top: float,
        bottom: float,
    ) -> float:
        """
        Calculate total gap size.

        Formula

            gap_size = top - bottom

        Parameters

        top : float

        bottom : float

        Returns

        float
        """

        return top - bottom

    def _calculate_midpoint(
        self,
        top: float,
        bottom: float,
    ) -> float:
        """
        Calculate Consequent Encroachment (CE).

        ICT refers to the midpoint of the Fair Value Gap
        as the Consequent Encroachment.

        Formula

            midpoint = (top + bottom) / 2

        Parameters

        top : float

        bottom : float

        Returns

        float
        """

        return (
            top + bottom
        ) / 2

    def _calculate_age(
        self,
        current_index: int,
        created_index: int,
    ) -> int:
        """
        Calculate the age of the Fair Value Gap.

        Age simply means how many candles have formed
        since the FVG appeared.

        Formula

            age = current_index - created_index

        Parameters

        current_index

        created_index

        Returns

        int
        """

        return current_index - created_index

    def _calculate_fill_percentage(
        self,
        candles: List[dict],
        start_index: int,
        top: float,
        bottom: float,
        bullish: bool,
    ) -> float:
        """
        Calculate how much of the Fair Value Gap
        has been filled by later price action.

        Fill Percentage

            0% = untouched

            100% = fully mitigated

        Parameters

        candles

            Historical candles.

        start_index

            First candle AFTER the FVG.

        top

            Upper gap boundary.

        bottom

            Lower gap boundary.

        bullish

            True for Bullish FVG.

            False for Bearish FVG.

        Returns

        float

            Fill percentage.
        """

        gap_size = top - bottom

        if gap_size <= 0:
            return 0.0

        deepest_fill = 0.0

        for candle in candles[start_index:]:

            fields = self._extract_candle_fields(candle)

            if fields is None:
                continue

            high, low = fields

            # ----------------------------------------------
            # Bullish Gap
            # ----------------------------------------------

            if bullish:

                # Price entered the gap

                if low <= top:

                    penetration = top - max(low, bottom)

                    fill = (
                        penetration / gap_size
                    ) * 100

                    deepest_fill = max(
                        deepest_fill,
                        fill,
                    )

            # ----------------------------------------------
            # Bearish Gap
            # ----------------------------------------------

            else:

                if high >= bottom:

                    penetration = (
                        min(high, top)
                        - bottom
                    )

                    fill = (
                        penetration / gap_size
                    ) * 100

                    deepest_fill = max(
                        deepest_fill,
                        fill,
                    )

        return round(
            min(deepest_fill, self.FULL_FILL_PERCENTAGE),
            2,
        )

    def _calculate_retest_count(
        self,
        candles: List[dict],
        start_index: int,
        top: float,
        bottom: float,
        bullish: bool,
    ) -> int:
        """
        Count how many independent times price
        revisited the Fair Value Gap.

        Multiple consecutive candles inside the gap
        count as ONE retest.

        Returns

        int
        """

        retests = 0

        inside_gap = False

        for candle in candles[start_index:]:

            fields = self._extract_candle_fields(candle)

            if fields is None:
                continue

            high, low = fields

            if bullish:

                touched = low <= top

            else:

                touched = high >= bottom

            if touched and not inside_gap:

                retests += 1

                inside_gap = True

            elif not touched:

                inside_gap = False

        return retests

    def _is_mitigated(
        self,
        fill_percentage: float,
    ) -> bool:
        """
        Determine whether the Fair Value Gap
        has been completely mitigated.

        Returns

        bool
        """

        return fill_percentage >= self.FULL_FILL_PERCENTAGE

    def _status(
        self,
        fill_percentage: float,
    ) -> str:
        """
        Convert fill percentage into
        a standardized status.

        Returns

        str
        """

        if fill_percentage == 0:

            return "OPEN"

        if fill_percentage < self.FULL_FILL_PERCENTAGE:

            return "PARTIALLY_FILLED"

        return "MITIGATED"

    def _analyze_single_fvg(
        self,
        fvg: dict,
        candles: List[dict],
        current_index: int,
    ) -> dict:
        """
        Analyze one previously detected
        Fair Value Gap.

        This method enriches the original
        FVG with additional analytical
        information.

        Parameters

        fvg

            One detected Fair Value Gap.

        candles

            Historical candles.

        current_index

            Index of the most recent candle.

        Returns

        dict
        """

        top = fvg["top"]
        bottom = fvg["bottom"]

        created_index = fvg["created_index"]

        direction = fvg["direction"]

        bullish = direction == "BULLISH"

        start_index = fvg.get(
            "analysis_start_index",
            created_index + 2,
        )

        if start_index >= len(candles):
            start_index = len(candles)

        # --------------------------------------------
        # Core Measurements
        # --------------------------------------------

        gap_size = self._calculate_gap_size(
            top,
            bottom,
        )

        midpoint = self._calculate_midpoint(
            top,
            bottom,
        )

        age = self._calculate_age(
            current_index,
            created_index,
        )

        fill_percentage = self._calculate_fill_percentage(
            candles,
            start_index,
            top,
            bottom,
            bullish,
        )

        retest_count = self._calculate_retest_count(
            candles,
            start_index,
            top,
            bottom,
            bullish,
        )

        mitigated = self._is_mitigated(
            fill_percentage,
        )

        status = self._status(
            fill_percentage,
        )

        # --------------------------------------------
        # Copy original detector output
        # --------------------------------------------

        analyzed = dict(fvg)

        # --------------------------------------------
        # Add analysis
        # --------------------------------------------

        analyzed.update(
            {
                "gap_size": gap_size,

                "midpoint": midpoint,

                "consequent_encroachment": midpoint,

                "fill_percentage": fill_percentage,

                "retest_count": retest_count,

                "age": age,

                "mitigated": mitigated,

                "status": status,
            }
        )

        return analyzed

    # ==========================================================
    # PUBLIC METHODS
    # ==========================================================

    def analyze(
        self,
        candles: List[dict],
        detected_fvg: List[dict],
    ) -> Response:
        """
        Analyze previously detected Fair Value Gaps.

        Parameters

        candles : List[dict]

            Historical candle data.

        detected_fvg : List[dict]

            Output from FVGDetector.

        Returns

        Response
        """

        # ------------------------------------------------------
        # Validate candles
        # ------------------------------------------------------

        if not candles:

            logger.error(
                "No candle data supplied."
            )

            return Response(
                success=False,
                message="No candle data supplied.",
                error="EMPTY_CANDLES",
                data=None,
            )

        # ------------------------------------------------------
        # Validate detected FVG list
        # ------------------------------------------------------

        if detected_fvg is None:

            logger.error(
                "No Fair Value Gap data supplied."
            )

            return Response(
                success=False,
                message="No Fair Value Gap data supplied.",
                error="EMPTY_FVG",
                data=None,
            )

        if len(detected_fvg) == 0:

            logger.info(
                "No Fair Value Gap available for analysis."
            )

            return Response(
                success=True,
                message="No Fair Value Gap available for analysis.",
                error=None,
                data={
                    "analyzed_fvg": [],
                    "count": 0,
                },
            )

        current_index = len(candles) - 1

        analyzed_fvg: List[dict] = []

        # ------------------------------------------------------
        # Analyze each Fair Value Gap
        # ------------------------------------------------------

        for fvg in detected_fvg:

            if not self._validate_fvg(fvg):

                logger.warning(
                    "Skipping malformed Fair Value Gap."
                )

                continue

            analyzed = self._analyze_single_fvg(
                fvg=fvg,
                candles=candles,
                current_index=current_index,
            )

            analyzed_fvg.append(
                analyzed
            )

        # ------------------------------------------------------
        # Logging
        # ------------------------------------------------------

        logger.info(
            "FVG Analysis | Total=%d",
            len(analyzed_fvg),
        )

        # ------------------------------------------------------
        # Response
        # ------------------------------------------------------

        return Response(
            success=True,
            message="Fair Value Gap analysis completed.",
            error=None,
            data={
                "analyzed_fvg": analyzed_fvg,
                "count": len(analyzed_fvg),
            },
        )