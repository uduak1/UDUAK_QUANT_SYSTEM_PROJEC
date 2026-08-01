"""
===============================================================================
UDUAK_QUANT_SYSTEM_PROJECT

File: settings.py
Purpose:
    Global application settings used throughout the trading system.

Design Principles:
    - Single Responsibility
    - Immutable configuration
    - No business logic
    - No MT5 credentials
    - No trading parameters

Author: Uduak Hezekiah Japhet
===============================================================================
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Final


# ============================================================================
# Project Information
# ============================================================================

APP_NAME: Final[str] = "UDUAK_QUANT_SYSTEM_PROJECT"
APP_VERSION: Final[str] = "1.0.0"
AUTHOR: Final[str] = "Uduak Hezekiah Japhet"


# ============================================================================
# Environment
# ============================================================================

ENV_DEVELOPMENT: Final[str] = "development"
ENV_TESTING: Final[str] = "testing"
ENV_PRODUCTION: Final[str] = "production"


# ============================================================================
# Global Settings
# ============================================================================

@dataclass(frozen=True)
class Settings:
    """
    Global application configuration.
    """

    app_name: str
    version: str
    author: str

    environment: str

    debug: bool

    timezone: str

    project_root: Path


# ============================================================================
# Build Configuration
# ============================================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent


settings = Settings(
    app_name=APP_NAME,
    version=APP_VERSION,
    author=AUTHOR,
    environment=ENV_DEVELOPMENT,
    debug=True,
    timezone="UTC",
    project_root=PROJECT_ROOT,
)