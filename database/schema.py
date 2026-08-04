"""
===============================================================================
UDUAK_QUANT_SYSTEM_PROJECT
-------------------------------------------------------------------------------
File: database/schema.py

Description:
    Creates and maintains the SQLite database schema.

Responsibilities:
    - Create all required database tables.
    - Create indexes.
    - Initialize database structure.

Business logic must NOT exist here.
===============================================================================
"""

from __future__ import annotations

from database.database import Database
from monitoring.logger import get_logger

logger = get_logger(__name__)


class DatabaseSchema:
    """
    Creates all database tables required by the trading system.
    """

    def __init__(self) -> None:
        """
        Initialize schema manager.
        """

        self._database = Database()

    # =========================================================================
    # INITIALIZE
    # =========================================================================

    def initialize(self) -> None:
        """
        Create all database objects.
        """

        logger.info("Initializing database schema...")

        self._create_signals_table()

        self._create_trades_table()

        self._create_positions_table()

        self._create_performance_table()

        self._create_market_snapshots_table()

        self._create_indexes()

        self._database.commit()

        logger.info("Database schema initialized successfully.")

    # =========================================================================
    # SIGNALS
    # =========================================================================

    def _create_signals_table(self) -> None:
        """
        Store generated trading signals.
        """

        self._database.execute(
            """
            CREATE TABLE IF NOT EXISTS signals (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                symbol TEXT NOT NULL,

                direction TEXT NOT NULL,

                strategy TEXT NOT NULL,

                timeframe TEXT NOT NULL,

                entry REAL NOT NULL,

                stop_loss REAL NOT NULL,

                take_profit REAL NOT NULL,

                confidence REAL NOT NULL,

                status TEXT NOT NULL,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

    # =========================================================================
    # TRADES
    # =========================================================================

    def _create_trades_table(self) -> None:
        """
        Store completed trades.
        """

        self._database.execute(
            """
            CREATE TABLE IF NOT EXISTS trades (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                ticket INTEGER UNIQUE,

                symbol TEXT NOT NULL,

                direction TEXT NOT NULL,

                strategy TEXT NOT NULL,

                volume REAL NOT NULL,

                entry_price REAL NOT NULL,

                exit_price REAL,

                stop_loss REAL,

                take_profit REAL,

                profit REAL DEFAULT 0,

                status TEXT NOT NULL,

                opened_at TIMESTAMP,

                closed_at TIMESTAMP
            )
            """
        )

    # =========================================================================
    # POSITIONS
    # =========================================================================

    def _create_positions_table(self) -> None:
        """
        Store currently open positions.
        """

        self._database.execute(
            """
            CREATE TABLE IF NOT EXISTS positions (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                ticket INTEGER UNIQUE,

                symbol TEXT NOT NULL,

                direction TEXT NOT NULL,

                volume REAL NOT NULL,

                entry_price REAL NOT NULL,

                stop_loss REAL,

                take_profit REAL,

                current_price REAL,

                floating_profit REAL DEFAULT 0,

                opened_at TIMESTAMP
            )
            """
        )

    # =========================================================================
    # PERFORMANCE
    # =========================================================================

    def _create_performance_table(self) -> None:
        """
        Store trading performance statistics.
        """

        self._database.execute(
            """
            CREATE TABLE IF NOT EXISTS performance (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                date DATE NOT NULL,

                trades INTEGER DEFAULT 0,

                wins INTEGER DEFAULT 0,

                losses INTEGER DEFAULT 0,

                win_rate REAL DEFAULT 0,

                gross_profit REAL DEFAULT 0,

                gross_loss REAL DEFAULT 0,

                net_profit REAL DEFAULT 0
            )
            """
        )

    # =========================================================================
    # MARKET SNAPSHOTS
    # =========================================================================

    def _create_market_snapshots_table(self) -> None:
        """
        Store market state snapshots.
        """

        self._database.execute(
            """
            CREATE TABLE IF NOT EXISTS market_snapshots (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                symbol TEXT NOT NULL,

                timeframe TEXT NOT NULL,

                trend TEXT,

                regime TEXT,

                volatility REAL,

                liquidity TEXT,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

    # =========================================================================
    # INDEXES
    # =========================================================================

    def _create_indexes(self) -> None:
        """
        Create database indexes.
        """

        self._database.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_trade_symbol
            ON trades(symbol)
            """
        )

        self._database.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_trade_status
            ON trades(status)
            """
        )

        self._database.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_signal_symbol
            ON signals(symbol)
            """
        )

        self._database.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_signal_status
            ON signals(status)
            """
        )

        self._database.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_position_symbol
            ON positions(symbol)
            """
        )