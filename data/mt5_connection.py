"""
===============================================================================
UDUAK_QUANT_SYSTEM_PROJECT
-------------------------------------------------------------------------------
File: data/mt5_connection.py

Description:
    Central MetaTrader 5 connection manager.

Responsibilities:
    - Initialize MetaTrader 5.
    - Shutdown MetaTrader 5.
    - Report connection status.
    - Expose MT5 connection errors.

This module NEVER:
    - Executes trades.
    - Reads market data.
    - Reads account information.
    - Calculates indicators.
    - Performs risk management.
===============================================================================
"""

from __future__ import annotations

import MetaTrader5 as mt5

from monitoring.logger import get_logger

logger = get_logger(__name__)


class MT5Connection:
    """
    Manages the application's connection to MetaTrader 5.

    This class is the only place responsible for starting and
    stopping the MT5 terminal connection.
    """

    def __init__(self) -> None:
        """
        Initialize the connection manager.
        """

        self._connected = False

    # =========================================================================
    # PROPERTIES
    # =========================================================================

    @property
    def connected(self) -> bool:
        """
        Returns
        -------
        bool
            True if the application is connected to MT5.
        """

        return self._connected

    @property
    def last_error(self):
        """
        Returns
        -------
        tuple
            Last MetaTrader 5 error.
        """

        return mt5.last_error()

    # =========================================================================
    # CONNECTION
    # =========================================================================

    def connect(self) -> bool:
        """
        Initialize MetaTrader 5.

        Returns
        -------
        bool
            True if initialization succeeds.
        """

        if self._connected:
            logger.debug("MetaTrader 5 is already connected.")
            return True

        if not mt5.initialize():

            logger.error(
                "MetaTrader 5 initialization failed: %s",
                mt5.last_error(),
            )

            self._connected = False
            return False

        self._connected = True

        logger.info("MetaTrader 5 connected successfully.")

        return True

    # =========================================================================
    # DISCONNECT
    # =========================================================================

    def disconnect(self) -> None:
        """
        Shutdown MetaTrader 5.
        """

        if not self._connected:
            logger.debug("MetaTrader 5 is already disconnected.")
            return

        mt5.shutdown()

        self._connected = False

        logger.info("MetaTrader 5 disconnected.")

    # =========================================================================
    # STATUS
    # =========================================================================

    def is_connected(self) -> bool:
        """
        Check whether MT5 is currently connected.

        Returns
        -------
        bool
            Current connection state.
        """

        return self._connected