from config.logging import logging_config
from monitoring.logger import get_logger


def test_logging_configuration():

    logger = get_logger("TEST")

    assert logger.name == "TEST"


def test_log_file_location():

    assert logging_config.log_file.name == "application.log"


def test_log_directory():

    assert logging_config.log_directory.exists()


def test_backup_count():

    assert logging_config.backup_count > 0