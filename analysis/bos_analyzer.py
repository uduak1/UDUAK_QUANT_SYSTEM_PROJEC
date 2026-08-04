"""
analysis/bos_analyzer.py

==========================================================
UDUAK QUANT SYSTEM

Institutional Break Of Structure Analyzer

Version 1

Responsibilities

    • Bullish BOS
    • Bearish BOS
    • BOS Direction
    • BOS Strength

Uses MarketStructureAnalyzer.

Does NOT calculate swings itself.
==========================================================
"""

from __future__ import annotations

from typing import Any, Dict

import pandas as pd

from core.base_analyzer import BaseAnalyzer
from analysis.market_structure_analyzer import MarketStructureAnalyzer


# ==========================================================
# BOS ANALYZER
# ==========================================================

class BOSAnalyzer(BaseAnalyzer):

    def __init__(
        self,
        swing_window: int = 2,
    ):

        super().__init__("BOSAnalyzer")

        self.structure = MarketStructureAnalyzer(
            swing_window=swing_window,
        )

    # ------------------------------------------------------

    def analyze(
        self,
        market_data: pd.DataFrame,
    ) -> Dict[str, Any]:

        structure = self.structure.analyze(
            market_data,
        )

        if structure["market_structure"] == 0.0:

            return {
                "bos": 0.0,
                "direction": None,
                "confirmed": False,
            }

        last_close = float(
            market_data.iloc[-1]["close"]
        )

        swing_high = structure["last_swing_high"]

        swing_low = structure["last_swing_low"]

        bullish = last_close > swing_high

        bearish = last_close < swing_low

        score = 0.0

        direction = None

        if bullish:

            score = 1.0

            direction = "bullish"

        elif bearish:

            score = 1.0

            direction = "bearish"

        return {

            "bos": score,

            "direction": direction,

            "confirmed": bullish or bearish,

            "broken_level": (
                swing_high
                if bullish
                else swing_low
                if bearish
                else None
            ),

            "last_close": last_close,

            "trend": structure["trend"],
        }