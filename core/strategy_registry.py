"""
core/strategy_registry.py

==========================================================
UDUAK QUANT SYSTEM
Institutional Strategy Registry
==========================================================

The Strategy Registry is responsible for maintaining the
list of institutional trading strategies available inside
the system.

It does NOT execute strategies.

It does NOT analyze market data.

It simply stores metadata describing every strategy so
other modules (Signal Engine, Decision Engine, Dashboard,
Backtester) can discover available strategies without
hard-coding them.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional


# ==========================================================
# STRATEGY DEFINITION
# ==========================================================

@dataclass(slots=True)
class StrategyDefinition:
    """
    Describes one institutional trading strategy.
    """

    name: str

    description: str

    enabled: bool = True

    category: str = "Price Action"

    version: str = "1.0"
    # ==========================================================
# STRATEGY REGISTRY
# ==========================================================

class StrategyRegistry:
    """
    Central registry for all institutional strategies.

    The registry is responsible for:

        • Registering strategies
        • Looking up strategies
        • Listing enabled strategies
        • Preventing duplicate registrations

    No trading logic belongs here.
    """

    def __init__(self):

        self._strategies: Dict[str, StrategyDefinition] = {}

    # ------------------------------------------------------

    def register(
        self,
        strategy: StrategyDefinition,
    ) -> None:
        """
        Register one strategy.

        Raises
        ------
        ValueError
            If another strategy already has the same name.
        """

        if strategy.name in self._strategies:
            raise ValueError(
                f"Strategy '{strategy.name}' already exists."
            )

        self._strategies[strategy.name] = strategy

    # ------------------------------------------------------

    def exists(
        self,
        strategy_name: str,
    ) -> bool:
        """
        Check whether a strategy exists.
        """

        return strategy_name in self._strategies

    # ------------------------------------------------------

    def get(
        self,
        strategy_name: str,
    ) -> Optional[StrategyDefinition]:
        """
        Retrieve one registered strategy.

        Returns None if not found.
        """

        return self._strategies.get(strategy_name)

            # ------------------------------------------------------

    def list_all(
        self,
    ) -> List[StrategyDefinition]:
        """
        Return every registered strategy.
        """

        return list(self._strategies.values())

    # ------------------------------------------------------

    def list_enabled(
        self,
    ) -> List[StrategyDefinition]:
        """
        Return only enabled strategies.
        """

        return [
            strategy
            for strategy in self._strategies.values()
            if strategy.enabled
        ]

    # ------------------------------------------------------

    def enable(
        self,
        strategy_name: str,
    ) -> bool:
        """
        Enable a registered strategy.

        Returns
        -------
        bool
            True if the strategy exists.
        """

        strategy = self.get(strategy_name)

        if strategy is None:
            return False

        strategy.enabled = True

        return True

    # ------------------------------------------------------

    def disable(
        self,
        strategy_name: str,
    ) -> bool:
        """
        Disable a registered strategy.

        Returns
        -------
        bool
            True if the strategy exists.
        """

        strategy = self.get(strategy_name)

        if strategy is None:
            return False

        strategy.enabled = False

        return True

    # ------------------------------------------------------

    def remove(
        self,
        strategy_name: str,
    ) -> bool:
        """
        Remove a strategy from the registry.

        Returns
        -------
        bool
            True if the strategy existed.
        """

        if strategy_name not in self._strategies:
            return False

        del self._strategies[strategy_name]

        return True