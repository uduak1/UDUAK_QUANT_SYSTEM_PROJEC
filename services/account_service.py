"""
===============================================================================
UDUAK_QUANT_SYSTEM_PROJECT
-------------------------------------------------------------------------------
File: services/account_service.py

Description:
    Business logic responsible for account management.

Responsibilities:
    - Validate account availability.
    - Retrieve account information.
    - Extract account metrics.
    - Produce account dashboard summary.

This module contains BUSINESS LOGIC ONLY.

It must NEVER:
    - Call MetaTrader5 directly.
    - Execute trades.
    - Execute SQL.
===============================================================================
"""

from __future__ import annotations

from data.account_data import AccountData
from models.response import Response
from monitoring.logger import get_logger

logger = get_logger(__name__)


class AccountService:
    """
    Business logic for trading account management.
    """

    def __init__(self) -> None:
        """
        Initialize service.
        """

        self._account_data = AccountData()

    # =========================================================================
    # ACCOUNT STATUS
    # =========================================================================

    def is_available(self) -> Response:
        """
        Determine whether the trading account is available.
        """

        return self._account_data.is_available()

    # =========================================================================
    # ACCOUNT INFORMATION
    # =========================================================================

    def account_information(self) -> Response:
        """
        Retrieve complete account information.
        """

        return self._account_data.get_account_info()

    # =========================================================================
    # ACCOUNT METRICS
    # =========================================================================

    def balance(self) -> Response:
        """
        Return account balance.
        """

        result = self.account_information()

        if not result.success:
            return result

        return Response(
            success=True,
            message="Account balance retrieved successfully.",
            error=None,
            data=result.data.balance,
        )

    def equity(self) -> Response:
        """
        Return account equity.
        """

        result = self.account_information()

        if not result.success:
            return result

        return Response(
            success=True,
            message="Account equity retrieved successfully.",
            error=None,
            data=result.data.equity,
        )

    def margin(self) -> Response:
        """
        Return used margin.
        """

        result = self.account_information()

        if not result.success:
            return result

        return Response(
            success=True,
            message="Account margin retrieved successfully.",
            error=None,
            data=result.data.margin,
        )

    def free_margin(self) -> Response:
        """
        Return free margin.
        """

        result = self.account_information()

        if not result.success:
            return result

        return Response(
            success=True,
            message="Free margin retrieved successfully.",
            error=None,
            data=result.data.margin_free,
        )

    def margin_level(self) -> Response:
        """
        Return margin level.
        """

        result = self.account_information()

        if not result.success:
            return result

        return Response(
            success=True,
            message="Margin level retrieved successfully.",
            error=None,
            data=result.data.margin_level,
        )

    def leverage(self) -> Response:
        """
        Return account leverage.
        """

        result = self.account_information()

        if not result.success:
            return result

        return Response(
            success=True,
            message="Account leverage retrieved successfully.",
            error=None,
            data=result.data.leverage,
        )

    # =========================================================================
    # DASHBOARD
    # =========================================================================

    def summary(self) -> Response:
        """
        Return account dashboard summary.
        """

        result = self.account_information()

        if not result.success:
            return result

        summary = {
            "login": result.data.login,
            "server": result.data.server,
            "company": result.data.company,
            "name": result.data.name,
            "balance": result.data.balance,
            "equity": result.data.equity,
            "profit": result.data.profit,
            "margin": result.data.margin,
            "free_margin": result.data.margin_free,
            "margin_level": result.data.margin_level,
            "leverage": result.data.leverage,
            "currency": result.data.currency,
        }

        logger.info(
            "Account summary generated."
        )

        return Response(
            success=True,
            message="Account summary generated successfully.",
            error=None,
            data=summary,
        )