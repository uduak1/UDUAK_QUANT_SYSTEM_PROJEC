from config.settings import settings


def test_application_name():

    assert settings.app_name == "UDUAK_QUANT_SYSTEM_PROJECT"


def test_version():

    assert settings.version == "1.0.0"


def test_debug_mode():

    assert settings.debug is True


def test_project_root_exists():

    assert settings.project_root.exists()