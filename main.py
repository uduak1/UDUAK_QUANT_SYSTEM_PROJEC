"""
===============================================================================
UDUAK_QUANT_SYSTEM_PROJECT
-------------------------------------------------------------------------------
File: main.py

Description:
    Main entry point for the UDUAK Quant Trading System.

Responsibilities:
    - Start the application.
    - Initialize the application lifecycle.
    - Handle unexpected startup errors.
    - Exit gracefully.

This file must remain lightweight.
Business logic belongs in other modules.

Author:
    Uduak Hezekiah Japhet

===============================================================================
"""

from core.application import Application


def main() -> None:
    """
    Main application entry point.

    Creates the Application object and starts the system.
    """

    app = Application()
    app.start()


if __name__ == "__main__":
    main()