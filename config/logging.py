"""
===============================================================================
UDUAK_QUANT_SYSTEM_PROJECT

File: logging.py

Purpose:
    Central logging configuration.

Responsibilities:
    - Logging level
    - Log file location
    - Log formatting
    - Rotation settings

Author: Uduak Hezekiah Japhet
===============================================================================
"""

from dataclasses import dataclass
from pathlib import Path

from config.storage import storage


@dataclass(frozen=True)
class LoggingConfig:
    """
    Global logging configuration.
    """

    level: str

    log_directory: Path

    log_file: Path

    log_format: str

    date_format: str

    max_file_size: int

    backup_count: int


logging_config = LoggingConfig(

    level="DEBUG",

    log_directory=storage.logs_dir,

    log_file=storage.logs_dir / "application.log",

    log_format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",

    date_format="%Y-%m-%d %H:%M:%S",

    max_file_size=10 * 1024 * 1024,      # 10 MB

    backup_count=10,

)