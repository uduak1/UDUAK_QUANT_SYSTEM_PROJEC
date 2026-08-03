"""
===============================================================================
UDUAK_QUANT_SYSTEM_PROJECT
SwingDetector - implementation covering all structure classifications
"""

from dataclasses import dataclass, field
from typing import Any, List, Dict, Optional


@dataclass
class SwingResult:
    success: bool = False
    data: Optional[List[Dict[str, Any]]] = None
    error: str = None


class SwingDetector:
    def detect(self, candles) -> SwingResult:
        # No candles
        if not candles:
            return SwingResult(success=False, data=None, error="NO_CANDLES")
        
        # Not enough candles - needs at least 5 for a 5-candle swing pattern
        if len(candles) < 5:
            return SwingResult(success=False, data=None, error="NOT_ENOUGH_CANDLES")

        swings: List[Dict[str, Any]] = []

        # Detect swing highs and lows using 2 left + 2 right confirmation
        for i in range(2, len(candles) - 2):
            c = candles[i]
            high = c.get("high")
            low = c.get("low")
            time = c.get("time", i)

            if high is None or low is None:
                continue

            # Check swing high: high greater than 2 left and 2 right
            left_highs = [candles[i-1].get("high"), candles[i-2].get("high")]
            right_highs = [candles[i+1].get("high"), candles[i+2].get("high")]
            if all(h is not None and high > h for h in left_highs + right_highs):
                swings.append({
                    "type": "SWING_HIGH",
                    "price": high,
                    "index": i,
                    "time": time,
                })

            # Check swing low: low less than 2 left and 2 right
            left_lows = [candles[i-1].get("low"), candles[i-2].get("low")]
            right_lows = [candles[i+1].get("low"), candles[i+2].get("low")]
            if all(l is not None and low < l for l in left_lows + right_lows):
                swings.append({
                    "type": "SWING_LOW",
                    "price": low,
                    "index": i,
                    "time": time,
                })

        # Classify structure
        self._classify_structure(swings)

        return SwingResult(success=True, data=swings)

    def _classify_structure(self, swings: List[Dict[str, Any]]) -> None:
        """
        Classify each swing relative to previous swing of same type.
        Covers: INITIAL_HIGH, HIGHER_HIGH, LOWER_HIGH, EQUAL_HIGH,
                INITIAL_LOW, LOWER_LOW, HIGHER_LOW, EQUAL_LOW
        """
        last_high_price = None
        last_low_price = None

        for swing in swings:
            s_type = swing.get("type")
            price = swing.get("price")

            if price is None:
                continue

            if s_type == "SWING_HIGH":
                if last_high_price is None:
                    swing["structure"] = "INITIAL_HIGH"
                else:
                    if price > last_high_price:
                        swing["structure"] = "HIGHER_HIGH"
                    elif price < last_high_price:
                        swing["structure"] = "LOWER_HIGH"
                    else:
                        swing["structure"] = "EQUAL_HIGH"
                last_high_price = price

            elif s_type == "SWING_LOW":
                if last_low_price is None:
                    swing["structure"] = "INITIAL_LOW"
                else:
                    if price < last_low_price:
                        swing["structure"] = "LOWER_LOW"
                    elif price > last_low_price:
                        swing["structure"] = "HIGHER_LOW"
                    else:
                        swing["structure"] = "EQUAL_LOW"
                last_low_price = price
