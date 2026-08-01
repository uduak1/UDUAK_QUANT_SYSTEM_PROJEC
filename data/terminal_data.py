"""
===============================================================================
UDUAK_QUANT_SYSTEM_PROJECT
-------------------------------------------------------------------------------
File: data/terminal_data.py

Description:
    Reads information about the MetaTrader 5 terminal.

Responsibilities:
    - Retrieve terminal information.
    - Check terminal availability.
    - Check AutoTrading status.

This module NEVER:
    - Connects to MT5.
    - Executes trades.
    - Reads account information.
    - Reads market prices.
===============================================================================
"""

from __future__ import annotations

import MetaTrader5 as mt5

from monitoring.logger import get_logger

logger = get_logger(__name__)


class TerminalData:
    """
    Provides read-only access to MetaTrader 5 terminal information.
    """

    # =====================================================================
    # TERMINAL INFORMATION
    # =====================================================================

    def get_terminal_info(self):
        """
        Return the MetaTrader 5 terminal information.

        Returns
        -------
        mt5.TerminalInfo | None
        """

        info = mt5.terminal_info()

        if info is None:

            logger.error(
                "Unable to retrieve terminal information: %s",
                mt5.last_error(),
            )

        return info

    # =====================================================================
    # TERMINAL STATUS
    # =====================================================================

    def is_available(self) -> bool:
        """
        Returns True if terminal information can be read.
        """

        return self.get_terminal_info() is not None

    # =====================================================================
    # AUTOTRADING
    # =====================================================================

    def is_auto_trading_enabled(self) -> bool:
        """
        Returns
        -------
        bool
            True if AutoTrading is enabled.
        """

        info = self.get_terminal_info()

        if info is None:
            return False

        return bool(info.trade_allowed)

    # =====================================================================
    # VERSION
    # =====================================================================

    def version(self):
        """
        Returns MT5 version information.
        """

        return mt5.version()