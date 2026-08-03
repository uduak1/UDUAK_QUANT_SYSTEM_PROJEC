"""
Tests for data/mt5_connection.py
"""

from unittest.mock import patch

from data.mt5_connection import MT5Connection


# =============================================================================
# INITIAL STATE
# =============================================================================

def test_initial_state():

    connection = MT5Connection()

    assert connection.connected is False


# =============================================================================
# SUCCESSFUL CONNECTION
# =============================================================================

@patch("data.mt5_connection.mt5.initialize")
def test_connect_success(mock_initialize):

    mock_initialize.return_value = True

    connection = MT5Connection()

    assert connection.connect() is True

    assert connection.connected is True


# =============================================================================
# FAILED CONNECTION
# =============================================================================

@patch("data.mt5_connection.mt5.last_error")
@patch("data.mt5_connection.mt5.initialize")
def test_connect_failure(
    mock_initialize,
    mock_last_error,
):

    mock_initialize.return_value = False

    mock_last_error.return_value = (
        -1,
        "Initialization Failed",
    )

    connection = MT5Connection()

    assert connection.connect() is False

    assert connection.connected is False


# =============================================================================
# DISCONNECT
# =============================================================================

@patch("data.mt5_connection.mt5.shutdown")
@patch("data.mt5_connection.mt5.initialize")
def test_disconnect(
    mock_initialize,
    mock_shutdown,
):

    mock_initialize.return_value = True

    connection = MT5Connection()

    connection.connect()

    connection.disconnect()

    mock_shutdown.assert_called_once()

    assert connection.connected is False


# =============================================================================
# DOUBLE CONNECT
# =============================================================================

@patch("data.mt5_connection.mt5.initialize")
def test_double_connect(mock_initialize):

    mock_initialize.return_value = True

    connection = MT5Connection()

    assert connection.connect() is True

    assert connection.connect() is True

    # initialize() should only be called once
    mock_initialize.assert_called_once()


# =============================================================================
# LAST ERROR PROPERTY
# =============================================================================

@patch("data.mt5_connection.mt5.last_error")
def test_last_error(mock_last_error):

    mock_last_error.return_value = (
        10001,
        "Sample Error",
    )

    connection = MT5Connection()

    assert connection.last_error == (
        10001,
        "Sample Error",
    )


# =============================================================================
# CONNECT WITH OPTIONAL CONFIGURATION
# =============================================================================

@patch("data.mt5_connection.mt5.initialize")
@patch("data.mt5_connection.mt5_config")
def test_connect_with_optional_configuration(
    mock_mt5_config,
    mock_initialize,
):

    mock_initialize.return_value = True

    mock_mt5_config.timeout = 60000
    mock_mt5_config.portable = False
    mock_mt5_config.terminal_path = "C:/Program Files/MetaTrader5/terminal64.exe"
    mock_mt5_config.login = 12345678
    mock_mt5_config.password = "password"
    mock_mt5_config.server = "Broker-Demo"

    connection = MT5Connection()

    assert connection.connect() is True

    mock_initialize.assert_called_once_with(
        timeout=60000,
        portable=False,
        path="C:/Program Files/MetaTrader5/terminal64.exe",
        login=12345678,
        password="password",
        server="Broker-Demo",
    )


# =============================================================================
# DISCONNECT WHEN ALREADY DISCONNECTED
# =============================================================================

@patch("data.mt5_connection.mt5.shutdown")
def test_disconnect_when_already_disconnected(mock_shutdown):

    connection = MT5Connection()

    connection.disconnect()

    mock_shutdown.assert_not_called()

    assert connection.connected is False