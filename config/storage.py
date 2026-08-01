"""
===============================================================================
UDUAK_QUANT_SYSTEM_PROJECT

File: storage.py

Purpose:
    Central storage configuration for the entire trading system.
===============================================================================
"""

from dataclasses import dataclass
from pathlib import Path

from config.settings import settings


@dataclass(frozen=True)
class StorageConfig:
    project_root: Path

    data_dir: Path
    historical_data_dir: Path
    backtests_dir: Path

    database_dir: Path
    database_file: Path

    logs_dir: Path
    reports_dir: Path
    exports_dir: Path
    cache_dir: Path
    models_dir: Path


storage = StorageConfig(
    project_root=settings.project_root,

    data_dir=settings.project_root / "data",

    historical_data_dir=settings.project_root / "data" / "historical",

    backtests_dir=settings.project_root / "data" / "backtests",

    database_dir=settings.project_root / "data" / "database",

    database_file=settings.project_root / "data" / "database" / "uduak_quant.db",

    logs_dir=settings.project_root / "logs",

    reports_dir=settings.project_root / "reports",

    exports_dir=settings.project_root / "exports",

    cache_dir=settings.project_root / "cache",

    models_dir=settings.project_root / "models",
)


def initialize_storage() -> None:
    directories = [
        storage.data_dir,
        storage.historical_data_dir,
        storage.backtests_dir,
        storage.database_dir,
        storage.logs_dir,
        storage.reports_dir,
        storage.exports_dir,
        storage.cache_dir,
        storage.models_dir,
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
