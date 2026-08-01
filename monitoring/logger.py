"""
===============================================================================
UDUAK_QUANT_SYSTEM_PROJECT
-------------------------------------------------------------------------------
File: monitoring/logger.py

Central logging system.
===============================================================================
"""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler

from config.logging import logging_config


def _log_level(level_name: str) -> int:
    """
    Convert a string log level into a logging constant.
    """

    return getattr(logging, level_name.upper(), logging.INFO)


def get_logger(name: str) -> logging.Logger:
    """
    Return a configured logger.
    """

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(_log_level(logging_config.level))

    formatter = logging.Formatter(
        fmt=logging_config.log_format,
        datefmt=logging_config.date_format,
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(_log_level(logging_config.level))
    console_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(
        filename=logging_config.log_file,
        maxBytes=logging_config.max_file_size,
        backupCount=logging_config.backup_count,
        encoding="utf-8",
    )

    file_handler.setLevel(_log_level(logging_config.level))
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logger.propagate = False

    return logger