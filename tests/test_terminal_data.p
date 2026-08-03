from unittest.mock import patch

from data.terminal_data import TerminalData


@patch.object(TerminalData, "get_terminal_info")
def test_auto_trading_none(mock_info):
    mock_info.return_value = None

    terminal = TerminalData()

    assert terminal.is_auto_trading_enabled() is False