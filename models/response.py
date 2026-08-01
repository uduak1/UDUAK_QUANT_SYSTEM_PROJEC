"""
===============================================================================
UDUAK_QUANT_SYSTEM_PROJECT
-------------------------------------------------------------------------------
File: models/response.py

Standard response object used across the project.
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Response:
    """
    Standard response returned by project modules.
    """

    success: bool

    message: str

    error: Any | None

    data: Any | None