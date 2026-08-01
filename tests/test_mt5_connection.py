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