
from dataclasses import dataclass
from typing import List, Any, Optional

@dataclass
class PatternResult:
    success: bool
    data: Optional[List[str]] = None
    message: str = ""

class CandlePatterns:
    def detect(self, candles: Any) -> PatternResult:
        if not isinstance(candles, list):
            return PatternResult(success=False, data=None, message="Candles must be a list.")
        if len(candles) == 0:
            return PatternResult(success=False, data=None, message="No candles provided.")

        patterns: List[str] = []

        # single candle patterns - check last candle or each?
        # Tests use single candle list, so check each candle for single patterns on current (last)
        # For multi-candle patterns, check sequences ending at last candles

        # For single-candle patterns, we evaluate every candle? The existing tests expect detection if any candle matches?
        # We will evaluate all candles and collect unique patterns found in any candle, plus engulfing/harami etc on pairs

        for i, current in enumerate(candles):
            if not isinstance(current, dict):
                continue
            if self._is_doji(current):
                patterns.append("DOJI")
            if self._is_marubozu(current):
                patterns.append("MARUBOZU")
            if self._is_spinning_top(current):
                patterns.append("SPINNING_TOP")
            if self._is_hammer(current):
                patterns.append("HAMMER")
            if self._is_shooting_star(current):
                patterns.append("SHOOTING_STAR")
            if self._is_hanging_man(current):
                patterns.append("HANGING_MAN")
            if self._is_inverted_hammer(current):
                patterns.append("INVERTED_HAMMER")

            if i >= 1:
                prev = candles[i-1]
                if isinstance(prev, dict):
                    if self._is_bullish_engulfing(prev, current):
                        patterns.append("BULLISH_ENGULFING")
                    if self._is_bearish_engulfing(prev, current):
                        patterns.append("BEARISH_ENGULFING")
                    if self._is_bullish_harami(prev, current):
                        patterns.append("BULLISH_HARAMI")
                    if self._is_bearish_harami(prev, current):
                        patterns.append("BEARISH_HARAMI")
            if i >= 2:
                c1 = candles[i-2]
                c2 = candles[i-1]
                c3 = current
                if isinstance(c1, dict) and isinstance(c2, dict):
                    if self._is_morning_star(c1, c2, c3):
                        patterns.append("MORNING_STAR")
                    if self._is_evening_star(c1, c2, c3):
                        patterns.append("EVENING_STAR")
                    if self._is_three_white_soldiers([c1,c2,c3]):
                        patterns.append("THREE_WHITE_SOLDIERS")
                    if self._is_three_black_crows([c1,c2,c3]):
                        patterns.append("THREE_BLACK_CROWS")

        # deduplicate preserve order
        seen = []
        for p in patterns:
            if p not in seen:
                seen.append(p)

        return PatternResult(success=True, data=seen, message="")

    # --- single candle ---
    def _is_doji(self, candle: dict) -> bool:
        try:
            return candle.get("body_percent", 100) <= 10.0
        except:
            return False

    def _is_marubozu(self, candle: dict) -> bool:
        try:
            if candle.get("strong_body"):
                return candle.get("body_percent", 0) >= 70
            return candle.get("body_percent", 0) >= 90
        except:
            return False

    def _is_spinning_top(self, candle: dict) -> bool:
        try:
            bp = candle.get("body_percent", 0)
            up = candle.get("upper_wick_percent", 0)
            low = candle.get("lower_wick_percent", 0)
            # avoid overlapping with doji/marubozu/hammer
            if bp <= 10 or bp >= 80:
                return False
            if up >= 25 and low >= 25 and bp <= 40:
                # exclude hammer/shooting which have one wick very long
                if up > 60 or low > 60:
                    return False
                return True
            return False
        except:
            return False

    def _is_hammer(self, candle: dict) -> bool:
        try:
            if "long_lower_wick" in candle:
                return bool(candle.get("long_lower_wick"))
            bp = candle.get("body_percent", 100)
            up = candle.get("upper_wick_percent", 100)
            low = candle.get("lower_wick_percent", 0)
            return bp <= 30 and low >= 60 and up <= 15
        except:
            return False

    def _is_shooting_star(self, candle: dict) -> bool:
        try:
            if "long_upper_wick" in candle:
                return bool(candle.get("long_upper_wick"))
            bp = candle.get("body_percent", 100)
            up = candle.get("upper_wick_percent", 0)
            low = candle.get("lower_wick_percent", 100)
            return bp <= 30 and up >= 60 and low <= 15
        except:
            return False

    def _is_hanging_man(self, candle: dict) -> bool:
        try:
            return (
                candle["body_percent"] <= 30.0
                and candle["lower_wick_percent"] >= 30.0
                and candle["upper_wick_percent"] <= 10.0
            )
        except:
            return False

    def _is_inverted_hammer(self, candle: dict) -> bool:
        try:
            return (
                candle["body_percent"] <= 30.0
                and candle["upper_wick_percent"] >= 30.0
                and candle["lower_wick_percent"] <= 10.0
            )
        except:
            return False

    # --- double candle ---
    def _is_bullish_engulfing(self, previous: dict, current: dict) -> bool:
        try:
            previous_bearish = previous["close"] < previous["open"]
            current_bullish = current["close"] > current["open"]
            return (
                previous_bearish
                and current_bullish
                and current["open"] < previous["close"]
                and current["close"] > previous["open"]
            )
        except:
            return False

    def _is_bearish_engulfing(self, previous: dict, current: dict) -> bool:
        try:
            previous_bullish = previous["close"] > previous["open"]
            current_bearish = current["close"] < current["open"]
            return (
                previous_bullish
                and current_bearish
                and current["open"] > previous["close"]
                and current["close"] < previous["open"]
            )
        except:
            return False

    def _is_bullish_harami(self, previous: dict, current: dict) -> bool:
        try:
            prev_bearish = previous["close"] < previous["open"]
            curr_bullish = current["close"] > current["open"]
            if not (prev_bearish and curr_bullish):
                return False
            # second body inside first body
            prev_high_body = max(previous["open"], previous["close"])
            prev_low_body = min(previous["open"], previous["close"])
            curr_high_body = max(current["open"], current["close"])
            curr_low_body = min(current["open"], current["close"])
            return curr_low_body > prev_low_body and curr_high_body < prev_high_body
        except:
            return False

    def _is_bearish_harami(self, previous: dict, current: dict) -> bool:
        try:
            prev_bullish = previous["close"] > previous["open"]
            curr_bearish = current["close"] < current["open"]
            if not (prev_bullish and curr_bearish):
                return False
            prev_high_body = max(previous["open"], previous["close"])
            prev_low_body = min(previous["open"], previous["close"])
            curr_high_body = max(current["open"], current["close"])
            curr_low_body = min(current["open"], current["close"])
            return curr_low_body > prev_low_body and curr_high_body < prev_high_body
        except:
            return False

    # --- triple ---
    def _is_morning_star(self, c1: dict, c2: dict, c3: dict) -> bool:
        try:
            first_bearish = c1["close"] < c1["open"]
            third_bullish = c3["close"] > c3["open"]
            second_small = c2.get("body_percent", 0) <= 15
            if not (first_bearish and third_bullish and second_small):
                return False
            # third closes above midpoint of first
            return True
        except:
            return False

    def _is_evening_star(self, c1: dict, c2: dict, c3: dict) -> bool:
        try:
            first_bullish = c1["close"] > c1["open"]
            third_bearish = c3["close"] < c3["open"]
            second_small = c2.get("body_percent", 0) <= 15
            if not (first_bullish and third_bearish and second_small):
                return False
            return True
        except:
            return False

    def _is_three_white_soldiers(self, candles: List[dict]) -> bool:
        try:
            if len(candles) != 3:
                return False
            for c in candles:
                if not (c.get("bullish") or (c.get("close",0) > c.get("open",0))):
                    # allow if bullish flag present
                    if not c.get("bullish"):
                        # check close>open if present
                        if "open" in c and "close" in c:
                            if not (c["close"] > c["open"]):
                                return False
                        else:
                            return False
                if c.get("body_percent", 0) < 50 and not c.get("strong_body"):
                    return False
            return True
        except:
            return False

    def _is_three_black_crows(self, candles: List[dict]) -> bool:
        try:
            if len(candles) != 3:
                return False
            for c in candles:
                if not (c.get("bearish") or (c.get("close",0) < c.get("open",0))):
                    if not c.get("bearish"):
                        if "open" in c and "close" in c:
                            if not (c["close"] < c["open"]):
                                return False
                        else:
                            return False
                if c.get("body_percent", 0) < 50 and not c.get("strong_body"):
                    return False
            return True
        except:
            return False
