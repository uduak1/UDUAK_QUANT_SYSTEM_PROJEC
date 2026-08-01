"""
Tests for data/account_data.py
"""

from types import SimpleNamespace
from unittest.mock import patch

from data.account_data import AccountData
from models.response import Response


# =============================================================================
# ACCOUNT INFORMATION SUCCESS
# =============================================================================

@patch("data.account_data.mt5.account_info")
def test_get_account_info_success(mock_account_info):

    account = SimpleNamespace(
        login=123456,
        balance=10000.0,
        equity=10050.0,
        margin=100.0,
        margin_free=9950.0,
        currency="USD",
    )

    mock_account_info.return_value = account

    account_data = AccountData()

    result = account_data.get_account_info()

    assert isinstance(result, Response)

    assert result.success is True

    assert result.message == "Account information retrieved successfully."

    assert result.error is None

    assert result.data is account


# =============================================================================
# ACCOUNT INFORMATION FAILURE
# =============================================================================

@patch("data.account_data.mt5.last_error")
@patch("data.account_data.mt5.account_info")
def test_get_account_info_failure(
    mock_account_info,
    mock_last_error,
):

    mock_account_info.return_value = None

    mock_last_error.return_value = (
        -1,
        "Account unavailable",
    )

    account_data = AccountData()

    result = account_data.get_account_info()

    assert isinstance(result, Response)

    assert result.success is False

    assert result.message == "Unable to retrieve account information."

    assert result.error == (
        -1,
        "Account unavailable",
    )

    assert result.data is None


# =============================================================================
# ACCOUNT AVAILABLE
# =============================================================================

@patch("data.account_data.mt5.account_info")
def test_account_available(mock_account_info):

    mock_account_info.return_value = SimpleNamespace()

    account_data = AccountData()

    result = account_data.is_available()

    assert result.success is True

    assert result.data is True

    assert result.error is None

    assert result.message == "Trading account is available."


# =============================================================================
# ACCOUNT NOT AVAILABLE
# =============================================================================

@patch("data.account_data.mt5.last_error")
@patch("data.account_data.mt5.account_info")
def test_account_not_available(
    mock_account_info,
    mock_last_error,
):

    mock_account_info.return_value = None

    mock_last_error.return_value = (
        -1,
        "Account unavailable",
    )

    account_data = AccountData()

    result = account_data.is_available()

    assert result.success is False

    assert result.data is False

    assert result.error == (
        -1,
        "Account unavailable",
    )

    assert result.message == "Trading account is not available."