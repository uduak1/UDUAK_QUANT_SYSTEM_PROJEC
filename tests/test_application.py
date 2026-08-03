"""
Tests for core/application.py
"""

from core.application import Application


# =============================================================================
# INITIAL STATE
# =============================================================================

def test_initial_state():

    app = Application()

    assert app.status() == "STOPPED"


# =============================================================================
# INITIALIZE
# =============================================================================

def test_initialize(capsys):

    app = Application()

    app.initialize()

    captured = capsys.readouterr()

    assert "Initializing application..." in captured.out


# =============================================================================
# START
# =============================================================================

def test_start(capsys):

    app = Application()

    app.start()

    captured = capsys.readouterr()

    assert app.status() == "RUNNING"

    assert "UDUAK Quant System started successfully." in captured.out


# =============================================================================
# START WHEN ALREADY RUNNING
# =============================================================================

def test_start_when_running(capsys):

    app = Application()

    app.start()

    app.start()

    captured = capsys.readouterr()

    assert "Application already running." in captured.out

    assert app.status() == "RUNNING"


# =============================================================================
# STOP
# =============================================================================

def test_stop(capsys):

    app = Application()

    app.start()

    app.stop()

    captured = capsys.readouterr()

    assert app.status() == "STOPPED"

    assert "Application stopped." in captured.out


# =============================================================================
# STOP WHEN ALREADY STOPPED
# =============================================================================

def test_stop_when_already_stopped(capsys):

    app = Application()

    app.stop()

    captured = capsys.readouterr()

    assert "Application already stopped." in captured.out

    assert app.status() == "STOPPED"


# =============================================================================
# SHUTDOWN WHEN RUNNING
# =============================================================================

def test_shutdown_when_running(capsys):

    app = Application()

    app.start()

    app.shutdown()

    captured = capsys.readouterr()

    assert app.status() == "STOPPED"

    assert "Shutdown complete." in captured.out


# =============================================================================
# SHUTDOWN WHEN ALREADY STOPPED
# =============================================================================

def test_shutdown_when_stopped(capsys):

    app = Application()

    app.shutdown()

    captured = capsys.readouterr()

    assert "Shutdown complete." in captured.out

    assert app.status() == "STOPPED"