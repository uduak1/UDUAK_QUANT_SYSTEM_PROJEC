"""
===============================================================================
UDUAK_QUANT_SYSTEM_PROJECT
-------------------------------------------------------------------------------
File: core/service_locator.py

Description:
    Central registry for application services.

Responsibilities:
    - Create service instances.
    - Store service instances.
    - Provide shared access to services.

This module contains NO business logic.
This module contains NO trading logic.
===============================================================================
"""

from __future__ import annotations

from services.account_service import AccountService
from services.configuration_service import ConfigurationService
from services.database_service import DatabaseService
from services.maintenance_service import MaintenanceService
from services.market_service import MarketService
from services.performance_service import PerformanceService
from services.signal_service import SignalService
from services.storage_service import StorageService
from services.trade_service import TradeService


class ServiceLocator:
    """
    Central registry for application services.

    Each service is created only once and shared
    throughout the application.
    """

    def __init__(self) -> None:
        """
        Create all application services.
        """

        self._configuration_service = ConfigurationService()

        self._storage_service = StorageService()

        self._database_service = DatabaseService()

        self._maintenance_service = MaintenanceService()

        self._account_service = AccountService()

        self._market_service = MarketService()

        self._trade_service = TradeService()

        self._signal_service = SignalService()

        self._performance_service = PerformanceService()

    # =====================================================================
    # CONFIGURATION
    # =====================================================================

    @property
    def configuration(self) -> ConfigurationService:
        """
        Return ConfigurationService.
        """

        return self._configuration_service

    # =====================================================================
    # STORAGE
    # =====================================================================

    @property
    def storage(self) -> StorageService:
        """
        Return StorageService.
        """

        return self._storage_service

    # =====================================================================
    # DATABASE
    # =====================================================================

    @property
    def database(self) -> DatabaseService:
        """
        Return DatabaseService.
        """

        return self._database_service

    # =====================================================================
    # MAINTENANCE
    # =====================================================================

    @property
    def maintenance(self) -> MaintenanceService:
        """
        Return MaintenanceService.
        """

        return self._maintenance_service

    # =====================================================================
    # ACCOUNT
    # =====================================================================

    @property
    def account(self) -> AccountService:
        """
        Return AccountService.
        """

        return self._account_service

    # =====================================================================
    # MARKET
    # =====================================================================

    @property
    def market(self) -> MarketService:
        """
        Return MarketService.
        """

        return self._market_service

    # =====================================================================
    # TRADE
    # =====================================================================

    @property
    def trade(self) -> TradeService:
        """
        Return TradeService.
        """

        return self._trade_service

    # =====================================================================
    # SIGNAL
    # =====================================================================

    @property
    def signal(self) -> SignalService:
        """
        Return SignalService.
        """

        return self._signal_service

    # =====================================================================
    # PERFORMANCE
    # =====================================================================

    @property
    def performance(self) -> PerformanceService:
        """
        Return PerformanceService.
        """

        return self._performance_service