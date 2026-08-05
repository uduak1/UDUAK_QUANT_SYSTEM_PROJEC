"""
core/strategy_registry.py

==========================================================
UDUAK QUANT SYSTEM
Institutional Strategy Registry
==========================================================
"""

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass(slots=True)
class StrategyDefinition:
    """
    Metadata describing one strategy.
    """

    name: str
    description: str
    enabled: bool = True
    category: str = "Price Action"
    version: str = "1.0"


class StrategyRegistry:
    """
    Central registry for institutional strategies.
    """

    def __init__(
        self,
        load_defaults: bool = True,
    ):

        self._strategies: Dict[str, StrategyDefinition] = {}

        if load_defaults:
            self._register_defaults()



    # --------------------------------------------------

    def _register_defaults(self):

        defaults = [

            StrategyDefinition(
                "LiquiditySweep",
                "Institutional Liquidity Sweep",
                category="Liquidity",
            ),

            StrategyDefinition(
                "BOSContinuation",
                "Break of Structure Continuation",
                category="Structure",
            ),

            StrategyDefinition(
                "CHOCHReversal",
                "Change of Character Reversal",
                category="Structure",
            ),

            StrategyDefinition(
                "OrderBlock",
                "Institutional Order Block",
                category="Order Flow",
            ),

            StrategyDefinition(
                "FairValueGap",
                "Institutional Fair Value Gap",
                category="Imbalance",
            ),

        ]

        for strategy in defaults:
            self.register(strategy)

    # --------------------------------------------------

    def register(
        self,
        strategy: StrategyDefinition,
    ) -> None:

        if strategy.name in self._strategies:
            return

        self._strategies[strategy.name] = strategy

    # --------------------------------------------------

    def exists(
        self,
        strategy_name: str,
    ) -> bool:

        return strategy_name in self._strategies

    # --------------------------------------------------

    def get(
        self,
        strategy_name: str,
    ) -> Optional[StrategyDefinition]:

        return self._strategies.get(strategy_name)

    # --------------------------------------------------

    def list_all(
        self,
    ) -> List[StrategyDefinition]:

        return list(self._strategies.values())

    # --------------------------------------------------

    def list_enabled(
        self,
    ) -> List[StrategyDefinition]:

        return [
            strategy
            for strategy in self._strategies.values()
            if strategy.enabled
        ]

    # --------------------------------------------------

    def enable(
        self,
        strategy_name: str,
    ) -> bool:

        strategy = self.get(strategy_name)

        if strategy is None:
            return False

        strategy.enabled = True
        return True

    # --------------------------------------------------

    def disable(
        self,
        strategy_name: str,
    ) -> bool:

        strategy = self.get(strategy_name)

        if strategy is None:
            return False

        strategy.enabled = False
        return True

    # --------------------------------------------------

    def remove(
        self,
        strategy_name: str,
    ) -> bool:

        if strategy_name not in self._strategies:
            return False

        del self._strategies[strategy_name]

        return True
