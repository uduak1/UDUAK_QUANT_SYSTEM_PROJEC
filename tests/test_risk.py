"""
Tests for config/risk.py
"""

from config.risk import (
    risk,
    RiskConfig,
    PositionSizingConfig,
    DrawdownConfig,
    ExposureConfig,
    PositionManagementConfig,
    EmergencyProtectionConfig,
)


# =============================================================================
# ROOT CONFIGURATION
# =============================================================================

def test_root_configuration():

    assert isinstance(risk, RiskConfig)


# =============================================================================
# POSITION SIZING
# =============================================================================

def test_position_sizing():

    assert isinstance(
        risk.position_sizing,
        PositionSizingConfig,
    )

    assert risk.position_sizing.risk_per_trade_percent == 1.0

    assert (
        risk.position_sizing.maximum_risk_per_trade_percent
        == 2.0
    )

    assert (
        risk.position_sizing.auto_detect_volume_limits
        is True
    )

    assert (
        risk.position_sizing.normalize_volume
        is True
    )

    assert (
        risk.position_sizing.require_stop_loss
        is True
    )

    assert (
        risk.position_sizing.require_positive_rr
        is True
    )


# =============================================================================
# DRAWDOWN
# =============================================================================

def test_drawdown():

    assert isinstance(
        risk.drawdown,
        DrawdownConfig,
    )

    assert (
        risk.drawdown.maximum_daily_loss_percent
        == 3.0
    )

    assert (
        risk.drawdown.maximum_weekly_loss_percent
        == 6.0
    )

    assert (
        risk.drawdown.maximum_monthly_loss_percent
        == 10.0
    )

    assert (
        risk.drawdown.maximum_account_drawdown_percent
        == 15.0
    )

    assert (
        risk.drawdown.maximum_consecutive_losses
        == 3
    )


# =============================================================================
# EXPOSURE
# =============================================================================

def test_exposure():

    assert isinstance(
        risk.exposure,
        ExposureConfig,
    )

    assert (
        risk.exposure.maximum_portfolio_exposure_percent
        == 5.0
    )

    assert (
        risk.exposure.maximum_symbol_exposure_percent
        == 2.0
    )

    assert (
        risk.exposure.maximum_open_positions
        == 2
    )

    assert (
        risk.exposure.maximum_positions_per_symbol
        == 1
    )

    assert (
        risk.exposure.allow_correlated_positions
        is False
    )


# =============================================================================
# POSITION MANAGEMENT
# =============================================================================

def test_position_management():

    assert isinstance(
        risk.position_management,
        PositionManagementConfig,
    )

    assert (
        risk.position_management.minimum_risk_reward_ratio
        == 3.0
    )

    assert (
        risk.position_management.enable_break_even
        is True
    )

    assert (
        risk.position_management.enable_trailing_stop
        is True
    )

    assert (
        risk.position_management.enable_partial_close
        is True
    )

    assert (
        risk.position_management.partial_close_percentage
        == 50.0
    )


# =============================================================================
# EMERGENCY
# =============================================================================

def test_emergency():

    assert isinstance(
        risk.emergency,
        EmergencyProtectionConfig,
    )

    assert (
        risk.emergency.stop_after_daily_loss
        is True
    )

    assert (
        risk.emergency.stop_after_drawdown
        is True
    )

    assert (
        risk.emergency.stop_after_consecutive_losses
        is True
    )

    assert (
        risk.emergency.require_manual_restart
        is True
    )