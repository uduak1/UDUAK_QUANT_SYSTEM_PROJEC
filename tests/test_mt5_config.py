from pathlib import Path

from config.mt5 import mt5_config


def test_auto_detect_enabled():
    """Auto detection should be enabled by default."""
    assert mt5_config.auto_detect_terminal is True


def test_terminal_path():
    """
    When auto detection is enabled,
    terminal_path should be None.
    """
    assert mt5_config.terminal_path is None


def test_timeout():
    assert mt5_config.timeout == 60000


def test_auto_reconnect():
    assert mt5_config.auto_reconnect is True


def test_max_retries():
    assert mt5_config.max_retries == 5


def test_retry_delay():
    assert mt5_config.retry_delay_seconds == 5


def test_portable_flag():
    assert mt5_config.portable is False


def test_login_type():
    assert (
        mt5_config.login is None
        or isinstance(mt5_config.login, int)
    )


def test_password_type():
    assert (
        mt5_config.password is None
        or isinstance(mt5_config.password, str)
    )


def test_server_type():
    assert (
        mt5_config.server is None
        or isinstance(mt5_config.server, str)
    )