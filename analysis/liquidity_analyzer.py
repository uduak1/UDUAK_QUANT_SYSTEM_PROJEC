"""
Institutional Liquidity Analyzer

Detects:

- Swing Highs
- Swing Lows
- Equal Highs (EQH)
- Equal Lows (EQL)
- Buy-Side Liquidity (BSL)
- Sell-Side Liquidity (SSL)
- Liquidity Sweeps

This analyzer follows the same institutional architecture
as FVGAnalyzer.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

class LiquidityAnalyzer:
    """
    Institutional Liquidity Analyzer.
    """

    BUY_SIDE = "BUY_SIDE"
    SELL_SIDE = "SELL_SIDE"

    ACTIVE = "ACTIVE"
    SWEPT = "SWEPT"

    DEFAULT_EQUAL_TOLERANCE = 0.0001

    def __init__(
        self,
        equal_tolerance: float = DEFAULT_EQUAL_TOLERANCE,
    ):
        self.equal_tolerance = equal_tolerance

    # ==========================================================
    # Public API
    # ==========================================================

    def validate_liquidity(
        self,
        liquidity: Dict,
    ) -> bool:
        """
        Validate a liquidity object.
        """
        return self._validate_liquidity(liquidity)

    def analyze(
        self,
        candles: List[Dict],
    ) -> List[Dict]:
        """
        Analyze candles for institutional liquidity.
        """

        if not candles:
            return []

        results: List[Dict] = []

        buy_side = self._detect_buy_side_liquidity(
            candles,
        )

        sell_side = self._detect_sell_side_liquidity(
            candles,
        )

        for liquidity in buy_side:

            if self._validate_liquidity(liquidity):

                results.append(
                    self._analyze_single_liquidity(
                        liquidity,
                        candles,
                    )
                )

        for liquidity in sell_side:

            if self._validate_liquidity(liquidity):

                results.append(
                    self._analyze_single_liquidity(
                        liquidity,
                        candles,
                    )
                )

        return sorted(
            results,
            key=lambda x: x["created_index"],
        )

    # ==========================================================
    # Validation
    # ==========================================================

    def _validate_liquidity(
        self,
        liquidity: Dict,
    ) -> bool:
        """
        Validate a liquidity object.
        """

        if not isinstance(liquidity, dict):
            return False

        required = (
            "level",
            "type",
            "created_index",
        )

        if not all(key in liquidity for key in required):
            return False

        if not isinstance(liquidity["level"], (int, float)):
            return False

        if not isinstance(liquidity["created_index"], int):
            return False

        if liquidity["type"] not in (
            self.BUY_SIDE,
            self.SELL_SIDE,
        ):
            return False

        return True

    # ==========================================================
    # Candle Helpers
    # ==========================================================

    def _extract_candle_fields(
        self,
        candle: Dict,
    ) -> Optional[Tuple[float, float]]:
        """
        Extract high and low from a candle.
        """

        high = candle.get("high")
        low = candle.get("low")

        if high is None or low is None:
            return None

        if not isinstance(high, (int, float)):
            return None

        if not isinstance(low, (int, float)):
            return None

        if high < low:
            return None

        return (
            float(high),
            float(low),
        )

    # ==========================================================
    # Swing Detection
    # ==========================================================

    def _is_swing_high(
        self,
        candles: List[Dict],
        index: int,
    ) -> bool:
        """
        Determine whether a candle is a swing high.
        """

        if index <= 0:
            return False

        if index >= len(candles) - 1:
            return False

        left = self._extract_candle_fields(
            candles[index - 1]
        )

        middle = self._extract_candle_fields(
            candles[index]
        )

        right = self._extract_candle_fields(
            candles[index + 1]
        )

        if left is None or middle is None or right is None:
            return False

        left_high, _ = left
        middle_high, _ = middle
        right_high, _ = right

        return (
            middle_high > left_high
            and
            middle_high > right_high
        )

    def _is_swing_low(
        self,
        candles: List[Dict],
        index: int,
    ) -> bool:
        """
        Determine whether a candle is a swing low.
        """

        if index <= 0:
            return False

        if index >= len(candles) - 1:
            return False

        left = self._extract_candle_fields(
            candles[index - 1]
        )

        middle = self._extract_candle_fields(
            candles[index]
        )

        right = self._extract_candle_fields(
            candles[index + 1]
        )

        if left is None or middle is None or right is None:
            return False

        _, left_low = left
        _, middle_low = middle
        _, right_low = right

        return (
            middle_low < left_low
            and
            middle_low < right_low
        )

    # ==========================================================
    # Equal High / Equal Low
    # ==========================================================

    def _find_equal_highs(
        self,
        candles: List[Dict],
    ) -> List[Dict]:
        """
        Find Equal Highs (EQH).
        """

        equal_highs: List[Dict] = []

        for i in range(1, len(candles) - 1):

            if not self._is_swing_high(candles, i):
                continue

            left = self._extract_candle_fields(candles[i])

            if left is None:
                continue

            left_high, _ = left

            for j in range(i + 1, len(candles) - 1):

                if not self._is_swing_high(candles, j):
                    continue

                right = self._extract_candle_fields(candles[j])

                if right is None:
                    continue

                right_high, _ = right

                if abs(left_high - right_high) <= self.equal_tolerance:

                    equal_highs.append(
                        {
                            "level": max(left_high, right_high),
                            "type": self.BUY_SIDE,
                            "created_index": j,
                        }
                    )

                    break

        return equal_highs

    def _find_equal_lows(
        self,
        candles: List[Dict],
    ) -> List[Dict]:
        """
        Find Equal Lows (EQL).
        """

        equal_lows: List[Dict] = []

        for i in range(1, len(candles) - 1):

            if not self._is_swing_low(candles, i):
                continue

            left = self._extract_candle_fields(candles[i])

            if left is None:
                continue

            _, left_low = left

            for j in range(i + 1, len(candles) - 1):

                if not self._is_swing_low(candles, j):
                    continue

                right = self._extract_candle_fields(candles[j])

                if right is None:
                    continue

                _, right_low = right

                if abs(left_low - right_low) <= self.equal_tolerance:

                    equal_lows.append(
                        {
                            "level": min(left_low, right_low),
                            "type": self.SELL_SIDE,
                            "created_index": j,
                        }
                    )

                    break

        return equal_lows

    # ==========================================================
    # Liquidity
    # ==========================================================

    def _detect_buy_side_liquidity(
        self,
        candles: List[Dict],
    ) -> List[Dict]:
        """
        Detect Buy-Side Liquidity (BSL).

        Buy-side liquidity forms above Equal Highs.
        """

        liquidity: List[Dict] = []

        equal_highs = self._find_equal_highs(candles)

        for eqh in equal_highs:

            liquidity.append(
                {
                    "level": eqh["level"],
                    "type": self.BUY_SIDE,
                    "created_index": eqh["created_index"],
                    "status": self.ACTIVE,
                }
            )

        return liquidity

    def _detect_sell_side_liquidity(
        self,
        candles: List[Dict],
    ) -> List[Dict]:
        """
        Detect Sell-Side Liquidity (SSL).

        Sell-side liquidity forms below Equal Lows.
        """

        liquidity: List[Dict] = []

        equal_lows = self._find_equal_lows(candles)

        for eql in equal_lows:

            liquidity.append(
                {
                    "level": eql["level"],
                    "type": self.SELL_SIDE,
                    "created_index": eql["created_index"],
                    "status": self.ACTIVE,
                }
            )

        return liquidity

    # ==========================================================
    # Sweep Detection
    # ==========================================================

    def _detect_sweep(
        self,
        liquidity: Dict,
        candles: List[Dict],
    ) -> bool:
        """
        Determine whether liquidity has been swept.
        """

        level = liquidity["level"]
        liquidity_type = liquidity["type"]
        start = liquidity["created_index"] + 1

        for candle in candles[start:]:

            fields = self._extract_candle_fields(candle)

            if fields is None:
                continue

            high, low = fields

            if liquidity_type == self.BUY_SIDE:

                if high > level:
                    return True

            else:

                if low < level:
                    return True

        return False

    def _is_liquidity_swept(self, liquidity, candles):
        return self._detect_sweep(liquidity, candles)

    def _is_swept(self, liquidity, candles):
        return self._detect_sweep(liquidity, candles)

    def _calculate_sweep_strength(
        self,
        liquidity: Dict,
        candles: List[Dict],
    ) -> float:
        """
        Calculate sweep strength.
        """

        level = liquidity["level"]
        liquidity_type = liquidity["type"]
        start = liquidity["created_index"] + 1

        strongest = 0.0

        for candle in candles[start:]:

            fields = self._extract_candle_fields(candle)

            if fields is None:
                continue

            high, low = fields

            if liquidity_type == self.BUY_SIDE:

                penetration = max(0.0, high - level)

            else:

                penetration = max(0.0, level - low)

            strongest = max(strongest, penetration)

        return round(strongest, 5)

    # ==========================================================
    # Utility
    # ==========================================================

    def _calculate_age(
        self,
        created_index: int,
        current_index: int,
    ) -> int:
        """
        Calculate liquidity age.
        """

        return max(
            current_index - created_index,
            0,
        )

    def _status(
        self,
        swept: bool,
    ) -> str:
        """
        Determine liquidity status.
        """

        if swept:
            return self.SWEPT

        return self.ACTIVE

    # ==========================================================
    # Internal Analyzer
    # ==========================================================

    def _analyze_single_liquidity(
        self,
        liquidity: Dict,
        candles: List[Dict],
    ) -> Dict:
        """
        Analyze a single liquidity level.
        """

        result = liquidity.copy()

        swept = self._detect_sweep(
            liquidity,
            candles,
        )

        result["swept"] = swept

        result["status"] = self._status(
            swept,
        )

        result["strength"] = (
            self._calculate_sweep_strength(
                liquidity,
                candles,
            )
        )

        result["age"] = self._calculate_age(
            liquidity["created_index"],
            len(candles) - 1,
        )

        return result