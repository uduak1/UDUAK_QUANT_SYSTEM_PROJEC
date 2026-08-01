"""
===============================================================================
UDUAK_QUANT_SYSTEM_PROJECT
-------------------------------------------------------------------------------
File: core/application.py

Description:
    Controls the application lifecycle.

Responsibilities:
    - Initialize the system.
    - Start the application.
    - Stop the application.
    - Shutdown gracefully.
    - Report application state.

This module must never contain trading logic.
===============================================================================
"""

from __future__ import annotations


class Application:
    """
    Coordinates the lifecycle of the trading system.
    """

    def __init__(self) -> None:
        """
        Create a new Application instance.

        The constructor only prepares the object.
        It does not start the system.
        """

        self._running = False

    def initialize(self) -> None:
        """
        Initialize application resources.

        Future responsibilities:

        - Load configuration
        - Initialize logger
        - Check environment
        - Prepare database
        """

        print("Initializing application...")

    def start(self) -> None:
        """
        Start the application.
        """

        if self._running:
            print("Application already running.")
            return

        self.initialize()

        self._running = True

        print("UDUAK Quant System started successfully.")

    def stop(self) -> None:
        """
        Stop the application.
        """

        if not self._running:
            print("Application already stopped.")
            return

        self._running = False

        print("Application stopped.")

    def shutdown(self) -> None:
        """
        Shutdown the application safely.
        """

        if self._running:
            self.stop()

        print("Shutdown complete.")

    def status(self) -> str:
        """
        Return current application status.
        """

        return "RUNNING" if self._running else "STOPPED"