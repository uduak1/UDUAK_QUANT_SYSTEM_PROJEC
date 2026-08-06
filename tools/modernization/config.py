"""
tools/modernization/config.py

==========================================================
UDUAK QUANT SYSTEM
Modernization Toolkit (MQT)

Global Configuration

This module centralizes every configuration used by the
Modernization Toolkit.

Responsibilities
----------------
• Detect project root
• Define directory structure
• Configure logging
• Configure scanner
• Configure repair engine
• Configure report generation
==========================================================
"""

from __future__ import annotations

from pathlib import Path
from dataclasses import dataclass, field
from typing import Set
import logging


# ==========================================================
# PROJECT PATHS
# ==========================================================

THIS_FILE = Path(__file__).resolve()

MODERNIZATION_ROOT = THIS_FILE.parent

TOOLS_ROOT = MODERNIZATION_ROOT.parent

PROJECT_ROOT = TOOLS_ROOT.parent


# ==========================================================
# DIRECTORIES
# ==========================================================

REPORTS_DIR = MODERNIZATION_ROOT / "reports"

BACKUP_DIR = MODERNIZATION_ROOT / "backups"

LOG_DIR = MODERNIZATION_ROOT / "logs"

TEMP_DIR = MODERNIZATION_ROOT / "temp"

CACHE_DIR = MODERNIZATION_ROOT / "cache"


# ==========================================================
# CREATE DIRECTORIES
# ==========================================================

for directory in (
    REPORTS_DIR,
    BACKUP_DIR,
    LOG_DIR,
    TEMP_DIR,
    CACHE_DIR,
):
    directory.mkdir(parents=True, exist_ok=True)


# ==========================================================
# LOGGER
# ==========================================================

LOG_FILE = LOG_DIR / "modernization.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

LOGGER = logging.getLogger("MQT")


# ==========================================================
# FILE FILTERS
# ==========================================================

SUPPORTED_EXTENSIONS: Set[str] = {
    ".py",
}

IGNORED_DIRECTORIES: Set[str] = {
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".git",
    ".idea",
    ".vscode",
    "venv",
    ".venv",
    "env",
    "build",
    "dist",
    "htmlcov",
}


# ==========================================================
# REPORT FILES
# ==========================================================

PROJECT_INVENTORY = REPORTS_DIR / "project_inventory.json"

DEPENDENCY_GRAPH = REPORTS_DIR / "dependency_graph.json"

CLASS_MAP = REPORTS_DIR / "class_map.json"

FUNCTION_MAP = REPORTS_DIR / "function_map.json"

IMPORT_REPORT = REPORTS_DIR / "imports.json"

ARCHITECTURE_REPORT = REPORTS_DIR / "architecture_report.json"

DUPLICATE_CODE_REPORT = REPORTS_DIR / "duplicate_code.json"

DEAD_CODE_REPORT = REPORTS_DIR / "dead_code.json"

MISSING_TESTS_REPORT = REPORTS_DIR / "missing_tests.json"


# ==========================================================
# CONFIGURATION
# ==========================================================

@dataclass(slots=True)
class ScannerConfig:
    """
    Configuration used by the project scanners.
    """

    project_root: Path = PROJECT_ROOT

    reports_directory: Path = REPORTS_DIR

    backup_directory: Path = BACKUP_DIR

    temp_directory: Path = TEMP_DIR

    cache_directory: Path = CACHE_DIR

    supported_extensions: Set[str] = field(
        default_factory=lambda: SUPPORTED_EXTENSIONS.copy()
    )

    ignored_directories: Set[str] = field(
        default_factory=lambda: IGNORED_DIRECTORIES.copy()
    )

    recursive: bool = True

    follow_symlinks: bool = False

    verbose: bool = True


# ==========================================================
# GLOBAL INSTANCE
# ==========================================================

CONFIG = ScannerConfig()


# ==========================================================
# HELPERS
# ==========================================================

def print_banner() -> None:
    """
    Display toolkit banner.
    """

    print("=" * 70)
    print("UDUAK QUANT SYSTEM")
    print("Modernization Toolkit (MQT)")
    print("=" * 70)
    print(f"Project Root : {PROJECT_ROOT}")
    print(f"Reports      : {REPORTS_DIR}")
    print(f"Backups      : {BACKUP_DIR}")
    print("=" * 70)


def get_logger(name: str) -> logging.Logger:
    """
    Return child logger.
    """
    return logging.getLogger(f"MQT.{name}")