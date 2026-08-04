"""
analysis/market_structure_analyzer.py

==========================================================
UDUAK QUANT SYSTEM

Institutional Market Structure Analyzer

Version 1

Detects

    • Swing Highs
    • Swing Lows
    • Higher Highs (HH)
    • Higher Lows (HL)
    • Lower Highs (LH)
    • Lower Lows (LL)
    • Overall Trend
    • Structure Strength

Produces normalized output for the Signal Engine.

Future Versions

Version 2
    • ATR Adaptive Swing Detection

Version 3
    • Multi-Timeframe Structure

Version 4
    • Institutional Structure Engine
==========================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

import pandas as pd

from core.base_analyzer import BaseAnalyzer


# ==========================================================
# DATA MODEL
# ==========================================================

@dataclass
class StructureResult:

    trend: str

    strength: float

    last_swing_high: float | None

    last_swing_low: float | None

    higher_high: bool

    higher_low: bool

    lower_high: bool

    lower_low: bool


# ==========================================================
# ANALYZER
# ==========================================================

class MarketStructureAnalyzer(BaseAnalyzer):

    def __init__(
        self,
        swing_window: int = 2,
    ):

        super().__init__("MarketStructureAnalyzer")

        if swing_window < 1:
            raise ValueError("swing_window must be >= 1")

        self.swing_window = swing_window

    # ------------------------------------------------------

    @staticmethod
    def _find_swings(
        df: pd.DataFrame,
        window: int,
    ):

        swing_highs: List[float] = []

        swing_lows: List[float] = []

        for i in range(window, len(df) - window):

            current_high = df.iloc[i]["high"]
            current_low = df.iloc[i]["low"]

            left_highs = df.iloc[i - window:i]["high"]
            right_highs = df.iloc[i + 1:i + window + 1]["high"]

            if (
                current_high > left_highs.max()
                and current_high > right_highs.max()
            ):
                swing_highs.append(current_high)

            left_lows = df.iloc[i - window:i]["low"]
            right_lows = df.iloc[i + 1:i + window + 1]["low"]

            if (
                current_low < left_lows.min()
                and current_low < right_lows.min()
            ):
                swing_lows.append(current_low)

        return swing_highs, swing_lows

    # ------------------------------------------------------

    def analyze(
        self,
        market_data: pd.DataFrame,
    ) -> Dict[str, Any]:

        required_columns = {
            "high",
            "low",
        }

        if not required_columns.issubset(market_data.columns):
            raise ValueError(
                "market_data must contain 'high' and 'low' columns."
            )

        minimum_rows = (self.swing_window * 2) + 6

        if len(market_data) < minimum_rows:

            return {
                "market_structure": 0.0,
            }

        highs, lows = self._find_swings(
            market_data,
            self.swing_window,
        )

        if len(highs) < 2 or len(lows) < 2:

            return {
                "market_structure": 0.0,
            }

        higher_high = highs[-1] > highs[-2]
        lower_high = highs[-1] < highs[-2]

        higher_low = lows[-1] > lows[-2]
        lower_low = lows[-1] < lows[-2]

        trend = "range"

        score = 0.50

        if higher_high and higher_low:

            trend = "bullish"

            score = 1.00

        elif lower_high and lower_low:

            trend = "bearish"

            score = 1.00

        elif higher_high:

            trend = "potential_bullish"

            score = 0.70

        elif lower_low:

            trend = "potential_bearish"

            score = 0.70

        return {

            "market_structure": score,

            "trend": trend,

            "higher_high": float(higher_high),

            "higher_low": float(higher_low),

            "lower_high": float(lower_high),

            "lower_low": float(lower_low),

            "last_swing_high": highs[-1],

            "last_swing_low": lows[-1],

            "swing_window": self.swing_window,

            "swing_high_count": len(highs),

            "swing_low_count": len(lows),
        }