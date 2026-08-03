"""
UDUAK_QUANT_SYSTEM_PROJECT

File: analysis/fvg_filter.py

Description:
    Filters previously analyzed Fair Value Gaps (FVG)
    to retain only high-quality institutional setups.

Responsibilities:
    - Validate analyzed FVG data
    - Reject mitigated Fair Value Gaps
    - Reject small Fair Value Gaps
    - Reject old Fair Value Gaps
    - Reject heavily retested Fair Value Gaps
    - Return standardized Response objects

This module NEVER:
    - Detect Fair Value Gaps
    - Analyze Fair Value Gaps
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

from models.response import Response
from monitoring.logger import get_logger

logger = get_logger(__name__)

class FVGFilter:
    """
    Filter previously analyzed Fair Value Gaps.

    IMPORTANT

    This class DOES NOT detect Fair Value Gaps.

    This class DOES NOT analyze Fair Value Gaps.

    It only filters analyzed Fair Value Gaps
    according to predefined institutional rules.

    Input

        Analyzed FVG list.

    Output

        Standard Response object.
    """

    # ==========================================================
    # FILTER SETTINGS
    # ==========================================================

    MIN_GAP_SIZE = 0.0005

    MAX_AGE = 30

    MAX_RETESTS = 2

    ALLOW_OPEN = True

    ALLOW_PARTIALLY_FILLED = True

    REJECT_MITIGATED = True

    # ==========================================================
    # PRIVATE HELPERS
    # ==========================================================

    def _validate_fvg(
        self,
        fvg: dict,
    ) -> bool:
        """
        Validate analyzed Fair Value Gap.

        Returns

        bool
        """

        if not isinstance(fvg, dict):
            return False

        required_keys = (
            "gap_size",
            "age",
            "retest_count",
            "status",
            "direction",
        )

        if not all(key in fvg for key in required_keys):
            return False

        if (
            not isinstance(fvg["gap_size"], (int, float))
            or fvg["gap_size"] <= 0
        ):
            return False

        if (
            not isinstance(fvg["age"], int)
            or fvg["age"] < 0
        ):
            return False

        if (
            not isinstance(fvg["retest_count"], int)
            or fvg["retest_count"] < 0
        ):
            return False

        if fvg["direction"] not in (
            "BULLISH",
            "BEARISH",
        ):
            return False

        if fvg["status"] not in (
            "OPEN",
            "PARTIALLY_FILLED",
            "MITIGATED",
        ):
            return False

        return True

    def _passes_gap_size(
        self,
        fvg: dict,
    ) -> bool:
        """
        Check whether the Fair Value Gap
        is large enough.

        Returns

        bool
        """

        return (
            fvg["gap_size"]
            >= self.MIN_GAP_SIZE
        )

    def _passes_age(
        self,
        fvg: dict,
    ) -> bool:
        """
        Check whether the Fair Value Gap
        is still fresh enough.

        Returns

        bool
        """

        return (
            fvg["age"]
            <= self.MAX_AGE
        )

    def _passes_retests(
        self,
        fvg: dict,
    ) -> bool:
        """
        Reject Fair Value Gaps that have
        been revisited too many times.

        Returns

        bool
        """

        return (
            fvg["retest_count"]
            <= self.MAX_RETESTS
        )

    def _passes_status(
        self,
        fvg: dict,
    ) -> bool:
        """
        Determine whether the current
        mitigation status is acceptable.

        Returns

        bool
        """

        status = fvg["status"]

        if (
            self.REJECT_MITIGATED
            and status == "MITIGATED"
        ):
            return False

        if (
            status == "OPEN"
            and self.ALLOW_OPEN
        ):
            return True

        if (
            status == "PARTIALLY_FILLED"
            and self.ALLOW_PARTIALLY_FILLED
        ):
            return True

        return False

    def _passes_filters(
        self,
        fvg: dict,
    ) -> bool:
        """
        Run every institutional filter.

        Returns

        bool
        """

        return (
            self._passes_gap_size(fvg)
            and self._passes_age(fvg)
            and self._passes_retests(fvg)
            and self._passes_status(fvg)
        )

    # ==========================================================
    # PUBLIC METHODS
    # ==========================================================

    def filter(
        self,
        analyzed_fvg: List[dict],
    ) -> Response:
        """
        Filter analyzed Fair Value Gaps.

        Parameters

        analyzed_fvg : List[dict]

            Output from FVGAnalyzer.

        Returns

        Response
        """

        # ------------------------------------------------------
        # Validate input
        # ------------------------------------------------------

        if analyzed_fvg is None:

            logger.error(
                "No Fair Value Gap data supplied."
            )

            return Response(
                success=False,
                message="No Fair Value Gap data supplied.",
                error="EMPTY_FVG",
                data=None,
            )

        if len(analyzed_fvg) == 0:

            logger.info(
                "No Fair Value Gaps available for filtering."
            )

            return Response(
                success=True,
                message="No Fair Value Gaps available for filtering.",
                error=None,
                data={
                    "filtered_fvg": [],
                    "rejected_fvg": [],
                    "filtered_count": 0,
                    "rejected_count": 0,
                },
            )

        filtered_fvg: List[dict] = []

        rejected_fvg: List[dict] = []

        # ------------------------------------------------------
        # Filter each analyzed Fair Value Gap
        # ------------------------------------------------------

        for fvg in analyzed_fvg:

            if not self._validate_fvg(fvg):

                logger.warning(
                    "Skipping malformed Fair Value Gap."
                )

                rejected_fvg.append(fvg)

                continue

            if self._passes_filters(fvg):

                filtered_fvg.append(fvg)

            else:

                rejected_fvg.append(fvg)

        # ------------------------------------------------------
        # Logging
        # ------------------------------------------------------

        logger.info(
            (
                "FVG Filter | "
                "Accepted=%d "
                "Rejected=%d"
            ),
            len(filtered_fvg),
            len(rejected_fvg),
        )

        # ------------------------------------------------------
        # Response
        # ------------------------------------------------------

        return Response(
            success=True,
            message="Fair Value Gap filtering completed.",
            error=None,
            data={
                "filtered_fvg": filtered_fvg,
                "rejected_fvg": rejected_fvg,
                "filtered_count": len(
                    filtered_fvg
                ),
                "rejected_count": len(
                    rejected_fvg
                ),
            },
        )