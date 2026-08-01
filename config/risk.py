"""

UDUAK_QUANT_SYSTEM_PROJECT

File: config/risk.py

Description:
    Central risk management configuration.

Responsibilities:
    - Position sizing policy.
    - Drawdown protection.
    - Portfolio exposure limits.
    - Position management rules.
    - Emergency protection rules.

This module NEVER:
    - Connects to MetaTrader 5.
    - Reads broker information.
    - Calculates lot sizes.
    - Executes trades.
    - Contains trading strategies.

"""

from __future__ import annotations

from dataclasses import dataclass

# =============================================================================
# POSITION SIZING CONFIGURATION
# =============================================================================

@dataclass(frozen=True)
class PositionSizingConfig:
    """
    Position sizing policy.

    The Risk Engine calculates the final trading volume automatically
    using:

        • Account balance/equity
        • Risk percentage
        • Stop-loss distance
        • Symbol contract size
        • Tick/Pip value
        • Broker minimum volume
        • Broker maximum volume
        • Broker volume step

    This configuration only defines the policy.
    """

    # Percentage of account equity to risk per trade.
    risk_per_trade_percent: float = 1.0

    # Absolute maximum allowed risk.
    maximum_risk_per_trade_percent: float = 2.0

    # Automatically detect broker volume limits.
    auto_detect_volume_limits: bool = True

    # Round calculated lot size to the broker's
    # supported volume step.
    normalize_volume: bool = True

    # Never allow zero stop-loss trades.
    require_stop_loss: bool = True

    # Never allow negative Risk:Reward trades.
    require_positive_rr: bool = True

# =============================================================================
# DRAWDOWN CONFIGURATION
# =============================================================================

@dataclass(frozen=True)
class DrawdownConfig:
    """
    Account protection rules.

    These rules prevent the trading system from
    destroying the trading account during losing
    periods.
    """

    # Maximum daily loss.
    maximum_daily_loss_percent: float = 3.0

    # Maximum weekly loss.
    maximum_weekly_loss_percent: float = 6.0

    # Maximum monthly loss.
    maximum_monthly_loss_percent: float = 10.0

    # Maximum account drawdown.
    maximum_account_drawdown_percent: float = 15.0

    # Stop after this many losing trades.
    maximum_consecutive_losses: int = 3

    # Pause trading after hitting the daily limit.
    stop_trading_after_daily_limit: bool = True

    # Resume automatically the next trading day.
    auto_resume_next_day: bool = True

# =============================================================================
# PORTFOLIO EXPOSURE CONFIGURATION
# =============================================================================

@dataclass(frozen=True)
class ExposureConfig:
    """
    Portfolio exposure policy.

    These rules prevent excessive exposure to one
    symbol or highly correlated markets.
    """

    # Maximum portfolio exposure.
    maximum_portfolio_exposure_percent: float = 5.0

    # Maximum exposure for one symbol.
    maximum_symbol_exposure_percent: float = 2.0

    # Allow trades that are highly correlated.
    allow_correlated_positions: bool = False

    # Maximum correlated positions.
    maximum_correlated_positions: int = 1

    # Maximum total open positions.
    maximum_open_positions: int = 2

    # Maximum positions allowed per symbol.
    maximum_positions_per_symbol: int = 1

# =============================================================================
# POSITION MANAGEMENT CONFIGURATION
# =============================================================================

@dataclass(frozen=True)
class PositionManagementConfig:
    """
    Rules used to manage an already open trade.
    """

    # -------------------------------------------------------------------------
    # Risk : Reward
    # -------------------------------------------------------------------------

    # Minimum acceptable Risk : Reward.
    minimum_risk_reward_ratio: float = 3.0

    # -------------------------------------------------------------------------
    # Break Even
    # -------------------------------------------------------------------------

    enable_break_even: bool = True

    # Move Stop Loss to entry after reaching 1R.
    break_even_trigger_rr: float = 1.0

    # Lock a few points after break-even.
    break_even_offset_points: int = 5

    # -------------------------------------------------------------------------
    # Trailing Stop
    # -------------------------------------------------------------------------

    enable_trailing_stop: bool = True

    # Start trailing after reaching 2R.
    trailing_stop_trigger_rr: float = 2.0

    # Update trailing stop only after candle closes.
    trail_on_candle_close: bool = True

    # -------------------------------------------------------------------------
    # Partial Profit
    # -------------------------------------------------------------------------

    enable_partial_close: bool = True

    # Close part of the trade at 3R.
    partial_close_trigger_rr: float = 3.0

    # Percentage to close.
    partial_close_percentage: float = 50.0

    # Let remaining volume continue running.
    let_remaining_position_run: bool = True

# =============================================================================
# EMERGENCY PROTECTION CONFIGURATION
# =============================================================================

@dataclass(frozen=True)
class EmergencyProtectionConfig:
    """
    Emergency account protection.
    """

    # Stop trading after reaching the daily loss limit.
    stop_after_daily_loss: bool = True

    # Stop trading after maximum account drawdown.
    stop_after_drawdown: bool = True

    # Stop trading after consecutive losing trades.
    stop_after_consecutive_losses: bool = True

    # Manual restart required after shutdown.
    require_manual_restart: bool = True

    # Do not force-close existing trades by default.
    close_all_positions_on_shutdown: bool = False

    # Log every emergency event.
    log_emergency_events: bool = True

# =============================================================================
# MASTER RISK CONFIGURATION
# =============================================================================

@dataclass(frozen=True)
class RiskConfig:
    """
    Master Risk Configuration.

    This class combines every risk-related configuration
    into a single object that can be imported throughout
    the application.

    Example

    from config.risk import risk

    print(risk.position_sizing.risk_per_trade_percent)
    """

    position_sizing: PositionSizingConfig

    drawdown: DrawdownConfig

    exposure: ExposureConfig

    position_management: PositionManagementConfig

    emergency: EmergencyProtectionConfig

# =============================================================================
# DEFAULT RISK CONFIGURATION
# =============================================================================

risk = RiskConfig(

    position_sizing=PositionSizingConfig(),

    drawdown=DrawdownConfig(),

    exposure=ExposureConfig(),

    position_management=PositionManagementConfig(),

    emergency=EmergencyProtectionConfig(),

)