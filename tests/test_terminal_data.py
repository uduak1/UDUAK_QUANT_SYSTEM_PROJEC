"""
Tests for data/terminal_data.py
"""

from types import SimpleNamespace
from unittest.mock import patch

from data.terminal_data import TerminalData


# =============================================================================
# TERMINAL INFORMATION
# =============================================================================

@patch("data.terminal_data.mt5.terminal_info")
def test_get_terminal_info(mock_terminal_info):

    info = SimpleNamespace(
        trade_allowed=True,
        build=5120,
        name="MetaTrader 5",
    )

    mock_terminal_info.return_value = info

    terminal = TerminalData()

    result = terminal.get_terminal_info()

    assert result is info


# =============================================================================
# TERMINAL AVAILABLE
# =============================================================================

@patch("data.terminal_data.mt5.terminal_info")
def test_terminal_available(mock_terminal_info):

    mock_terminal_info.return_value = SimpleNamespace(
        trade_allowed=True,
    )

    terminal = TerminalData()

    assert terminal.is_available() is True


# =============================================================================
# TERMINAL NOT AVAILABLE
# =============================================================================

@patch("data.terminal_data.mt5.last_error")
@patch("data.terminal_data.mt5.terminal_info")
def test_terminal_not_available(
    mock_terminal_info,
    mock_last_error,
):

    mock_terminal_info.return_value = None

    mock_last_error.return_value = (
        -1,
        "Terminal not running",
    )

    terminal = TerminalData()

    assert terminal.is_available() is False


# =============================================================================
# AUTOTRADING ENABLED
# =============================================================================

@patch("data.terminal_data.mt5.terminal_info")
def test_auto_trading_enabled(mock_terminal_info):

    mock_terminal_info.return_value = SimpleNamespace(
        trade_allowed=True,
    )

    terminal = TerminalData()

    assert terminal.is_auto_trading_enabled() is True


# =============================================================================
# AUTOTRADING DISABLED
# =============================================================================

@patch("data.terminal_data.mt5.terminal_info")
def test_auto_trading_disabled(mock_terminal_info):

    mock_terminal_info.return_value = SimpleNamespace(
        trade_allowed=False,
    )

    terminal = TerminalData()

    assert terminal.is_auto_trading_enabled() is False


# =============================================================================
# VERSION
# =============================================================================

@patch("data.terminal_data.mt5.version")
def test_version(mock_version):

    mock_version.return_value = (
        500,
        5120,
        "18 Jul 2026",
    )

    terminal = TerminalData()

    assert terminal.version() == (
        500,
        5120,
        "18 Jul 2026",
    )