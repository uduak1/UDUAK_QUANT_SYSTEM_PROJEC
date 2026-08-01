"""
===============================================================================
UDUAK_QUANT_SYSTEM_PROJECT

File: config/mt5.py

Purpose:
    Central MetaTrader 5 configuration.

Responsibilities:
    - Store MT5 connection settings.
    - Configure auto-detection behavior.
    - No connection logic.
    - No file searching.
    - No MT5 API calls.

Author: Uduak Hezekiah Japhet
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class MT5Config:
    """
    Global MT5 configuration.

    This class contains configuration values only.
    The actual terminal detection and connection are handled elsewhere.
    """

    # ------------------------------------------------------------------
    # Terminal Detection
    # ------------------------------------------------------------------

    auto_detect_terminal: bool

    terminal_path: Optional[Path]

    # ------------------------------------------------------------------
    # Connection
    # ------------------------------------------------------------------

    login: Optional[int]

    password: Optional[str]

    server: Optional[str]

    timeout: int

    portable: bool

    # ------------------------------------------------------------------
    # Reliability
    # ------------------------------------------------------------------

    auto_reconnect: bool

    max_retries: int

    retry_delay_seconds: int


mt5_config = MT5Config(

    # Automatically detect installed MT5 terminals.
    auto_detect_terminal=True,

    # Leave as None to enable auto detection.
    # Can be manually overridden if required.
    terminal_path=None,

    # If None, the connector will use the account
    # currently logged into the running MT5 terminal.
    login=None,

    password=None,

    server=None,

    # Connection timeout (milliseconds)
    timeout=60000,

    # Standard desktop installation
    portable=False,

    # Retry settings
    auto_reconnect=True,

    max_retries=5,

    retry_delay_seconds=5,
)