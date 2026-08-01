"""
===============================================================================
UDUAK_QUANT_SYSTEM_PROJECT
-------------------------------------------------------------------------------
File: data/account_data.py

Description:
    Reads trading account information from MetaTrader 5.

Responsibilities:
    - Read account information.
    - Verify account availability.
    - Return standardized Response objects.

This module NEVER:
    - Connects to MT5.
    - Executes trades.
    - Calculates lot sizes.
    - Performs risk management.
    - Reads market prices.
===============================================================================
"""

from __future__ import annotations

import MetaTrader5 as mt5

from models.response import Response
from monitoring.logger import get_logger

logger = get_logger(__name__)


class AccountData:
    """
    Read-only access to MetaTrader 5 account information.
    """

    # =====================================================================
    # ACCOUNT INFORMATION
    # =====================================================================

    def get_account_info(self) -> Response:
        """
        Retrieve the current trading account information.

        Returns
        -------
        Response
            Standard project response containing the MT5 account
            information when successful.
        """

        info = mt5.account_info()

        if info is None:

            error = mt5.last_error()

            logger.error(
                "Unable to retrieve account information: %s",
                error,
            )

            return Response(
                success=False,
                message="Unable to retrieve account information.",
                error=error,
                data=None,
            )

        logger.info(
            "Account information retrieved successfully."
        )

        return Response(
            success=True,
            message="Account information retrieved successfully.",
            error=None,
            data=info,
        )

    # =====================================================================
    # ACCOUNT STATUS
    # =====================================================================

    def is_available(self) -> Response:
        """
        Check whether account information is available.

        Returns
        -------
        Response
            Standard project response.
        """

        result = self.get_account_info()

        if result.success:

            return Response(
                success=True,
                message="Trading account is available.",
                error=None,
                data=True,
            )

        return Response(
            success=False,
            message="Trading account is not available.",
            error=result.error,
            data=False,
        )