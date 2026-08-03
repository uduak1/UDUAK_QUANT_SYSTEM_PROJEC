"""
Tests for main.py
"""

from unittest.mock import patch

import main


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

@patch("main.Application")
def test_main(mock_application):

    app = mock_application.return_value

    main.main()

    mock_application.assert_called_once()

    app.start.assert_called_once()