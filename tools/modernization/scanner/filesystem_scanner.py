"""
tools/modernization/scanner/filesystem_scanner.py

==========================================================
UDUAK QUANT SYSTEM
Modernization Toolkit (MQT)

Filesystem Scanner

Responsibilities
----------------
• Scan the entire project directory
• Discover all folders
• Discover all Python files
• Ignore excluded directories
• Build project inventory
• Collect filesystem statistics
• Export inventory for downstream scanners

This scanner is the foundation of the Modernization Toolkit.
Every other scanner depends on its output.
==========================================================
"""

from __future__ import annotations

import json
import logging

from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Dict, List

from tools.modernization.config import (
    CONFIG,
    PROJECT_INVENTORY,
)

logger = logging.getLogger("MQT.FileSystemScanner")


# ==========================================================
# FILE INFORMATION
# ==========================================================

@dataclass(slots=True)
class FileInfo:
    """
    Represents one discovered file.
    """

    name: str

    path: str

    extension: str

    size: int

    parent: str


# ==========================================================
# DIRECTORY INFORMATION
# ==========================================================

@dataclass(slots=True)
class DirectoryInfo:
    """
    Represents one discovered directory.
    """

    name: str

    path: str

    parent: str


# ==========================================================
# PROJECT INVENTORY
# ==========================================================

@dataclass(slots=True)
class ProjectInventory:
    """
    Full filesystem inventory.
    """

    root: str

    directories: List[DirectoryInfo] = field(default_factory=list)

    files: List[FileInfo] = field(default_factory=list)

    statistics: Dict[str, int] = field(default_factory=dict)

    # ------------------------------------------------------

    @property
    def total_files(self) -> int:
        return len(self.files)

    @property
    def total_directories(self) -> int:
        return len(self.directories)

    @property
    def python_files(self) -> int:
        return sum(
            1
            for file in self.files
            if file.extension == ".py"
        )

    # ------------------------------------------------------

    def to_dict(self) -> Dict:
        """
        Serialize inventory.
        """

        return {
            "root": self.root,
            "directories": [
                asdict(directory)
                for directory in self.directories
            ],
            "files": [
                asdict(file)
                for file in self.files
            ],
            "statistics": self.statistics,
        }


# ==========================================================
# FILESYSTEM SCANNER
# ==========================================================

class FileSystemScanner:
    """
    Performs recursive filesystem discovery.
    """

    def __init__(self) -> None:

        self.config = CONFIG

        self.inventory = ProjectInventory(
            root=str(self.config.project_root)
        )

            # ==========================================================
    # PRIVATE HELPERS
    # ==========================================================

    def _is_ignored_directory(
        self,
        directory: Path,
    ) -> bool:
        """
        Determine whether a directory should be ignored.
        """

        return (
            directory.name
            in self.config.ignored_directories
        )

    # ----------------------------------------------------------

    def _discover_directory(
        self,
        directory: Path,
    ) -> None:
        """
        Record a discovered directory.
        """

        info = DirectoryInfo(
            name=directory.name,
            path=str(directory),
            parent=str(directory.parent),
        )

        self.inventory.directories.append(info)

        logger.debug(
            "Directory discovered: %s",
            directory,
        )

    # ----------------------------------------------------------

    def _discover_file(
        self,
        file_path: Path,
    ) -> None:
        """
        Record a discovered file.
        """

        try:

            info = FileInfo(
                name=file_path.name,
                path=str(file_path),
                extension=file_path.suffix,
                size=file_path.stat().st_size,
                parent=str(file_path.parent),
            )

            self.inventory.files.append(info)

            logger.debug(
                "File discovered: %s",
                file_path,
            )

        except OSError as exc:

            logger.warning(
                "Unable to inspect file %s : %s",
                file_path,
                exc,
            )

    # ----------------------------------------------------------

    def _scan_directory(
        self,
        directory: Path,
    ) -> None:
        """
        Recursively scan one directory.
        """

        if self._is_ignored_directory(directory):

            logger.debug(
                "Ignoring directory: %s",
                directory,
            )

            return

        self._discover_directory(directory)

        try:

            entries = sorted(
                directory.iterdir(),
                key=lambda item: item.name.lower(),
            )

        except PermissionError:

            logger.warning(
                "Permission denied: %s",
                directory,
            )

            return

        except OSError as exc:

            logger.warning(
                "Unable to access %s : %s",
                directory,
                exc,
            )

            return

        for entry in entries:

            if entry.is_dir():

                self._scan_directory(entry)

                continue

            if not entry.is_file():

                continue

            if (
                entry.suffix
                not in self.config.supported_extensions
            ):
                continue

            self._discover_file(entry)

                # ==========================================================
    # STATISTICS
    # ==========================================================

    def _build_statistics(self) -> None:
        """
        Build project statistics after scanning.
        """

        total_size = sum(
            file.size
            for file in self.inventory.files
        )

        extension_counts: Dict[str, int] = {}

        for file in self.inventory.files:

            extension_counts[file.extension] = (
                extension_counts.get(
                    file.extension,
                    0,
                )
                + 1
            )

        self.inventory.statistics = {
            "total_directories": self.inventory.total_directories,
            "total_files": self.inventory.total_files,
            "python_files": self.inventory.python_files,
            "total_size_bytes": total_size,
        }

        # Store extension statistics separately
        self.inventory.statistics.update(
            {
                f"ext_{extension}": count
                for extension, count
                in sorted(extension_counts.items())
            }
        )

    # ==========================================================
    # PUBLIC API
    # ==========================================================

    def scan(self) -> ProjectInventory:
        """
        Perform a complete filesystem scan.

        Returns
        -------
        ProjectInventory
            Fully populated project inventory.
        """

        logger.info(
            "Starting filesystem scan..."
        )

        self.inventory.directories.clear()
        self.inventory.files.clear()
        self.inventory.statistics.clear()

        self._scan_directory(
            self.config.project_root
        )

        self._build_statistics()

        logger.info(
            "Filesystem scan complete."
        )

        logger.info(
            "Directories : %d",
            self.inventory.total_directories,
        )

        logger.info(
            "Files : %d",
            self.inventory.total_files,
        )

        logger.info(
            "Python Files : %d",
            self.inventory.python_files,
        )

        return self.inventory

    # ==========================================================
    # SUMMARY
    # ==========================================================

    def summary(self) -> Dict[str, int]:
        """
        Return a lightweight summary of the last scan.
        """

        if not self.inventory.statistics:

            self._build_statistics()

        return dict(
            self.inventory.statistics
        )

    # ==========================================================
    # RESET
    # ==========================================================

    def reset(self) -> None:
        """
        Reset scanner state.
        """

        self.inventory = ProjectInventory(
            root=str(self.config.project_root)
        )

        logger.debug(
            "Filesystem scanner reset."
        )

            # ==========================================================
    # REPORT WRITING
    # ==========================================================

    def export_inventory(
        self,
        output_file: Path | None = None,
    ) -> Path:
        """
        Export the current inventory as JSON.

        Parameters
        ----------
        output_file
            Optional destination path.

        Returns
        -------
        Path
            Path of the generated report.
        """

        if output_file is None:
            output_file = PROJECT_INVENTORY

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with output_file.open(
            "w",
            encoding="utf-8",
        ) as fp:

            json.dump(
                self.inventory.to_dict(),
                fp,
                indent=4,
                ensure_ascii=False,
            )

        logger.info(
            "Inventory exported -> %s",
            output_file,
        )

        return output_file

    # ----------------------------------------------------------

    def save(self) -> Path:
        """
        Convenience wrapper.

        Saves the inventory to the default report.
        """

        return self.export_inventory()

    # ==========================================================
    # VALIDATION
    # ==========================================================

    def validate_inventory(self) -> bool:
        """
        Validate inventory consistency.

        Returns
        -------
        bool
            True if inventory is internally consistent.
        """

        statistics = self.inventory.statistics

        if (
            statistics.get("total_files", 0)
            != self.inventory.total_files
        ):
            logger.error(
                "Inventory validation failed "
                "(file count mismatch)"
            )
            return False

        if (
            statistics.get("total_directories", 0)
            != self.inventory.total_directories
        ):
            logger.error(
                "Inventory validation failed "
                "(directory count mismatch)"
            )
            return False

        if (
            statistics.get("python_files", 0)
            != self.inventory.python_files
        ):
            logger.error(
                "Inventory validation failed "
                "(python file count mismatch)"
            )
            return False

        logger.info(
            "Inventory validation passed."
        )

        return True

    # ==========================================================
    # PRETTY PRINT
    # ==========================================================

    def print_summary(self) -> None:
        """
        Display scan summary.
        """

        summary = self.summary()

        print()

        print("=" * 60)
        print("FILESYSTEM SCAN SUMMARY")
        print("=" * 60)

        print(
            f"Directories : "
            f"{summary['total_directories']}"
        )

        print(
            f"Files       : "
            f"{summary['total_files']}"
        )

        print(
            f"Python Files: "
            f"{summary['python_files']}"
        )

        print(
            f"Total Size  : "
            f"{summary['total_size_bytes']:,} bytes"
        )

        print("=" * 60)
        print()

            # ==========================================================
    # SEARCH UTILITIES
    # ==========================================================

    def find_file(
        self,
        filename: str,
    ) -> FileInfo | None:
        """
        Find the first file with the given filename.

        Parameters
        ----------
        filename
            Filename to search.

        Returns
        -------
        FileInfo | None
        """

        for file in self.inventory.files:

            if file.name == filename:
                return file

        return None

    # ----------------------------------------------------------

    def find_files_by_extension(
        self,
        extension: str,
    ) -> List[FileInfo]:
        """
        Return every file having the given extension.

        Example
        -------
        ".py"
        """

        return [
            file
            for file in self.inventory.files
            if file.extension == extension
        ]

    # ----------------------------------------------------------

    def find_files_containing(
        self,
        text: str,
    ) -> List[FileInfo]:
        """
        Return every file whose filename contains text.
        """

        text = text.lower()

        return [
            file
            for file in self.inventory.files
            if text in file.name.lower()
        ]

    # ----------------------------------------------------------

    def files_in_directory(
        self,
        directory: str,
    ) -> List[FileInfo]:
        """
        Return every file inside one directory.
        """

        directory = str(Path(directory))

        return [
            file
            for file in self.inventory.files
            if file.parent == directory
        ]

    # ----------------------------------------------------------

    def directory_exists(
        self,
        directory: str,
    ) -> bool:
        """
        Check whether a directory exists
        inside the inventory.
        """

        directory = str(Path(directory))

        return any(
            item.path == directory
            for item in self.inventory.directories
        )

    # ----------------------------------------------------------

    def file_exists(
        self,
        filepath: str,
    ) -> bool:
        """
        Check whether a file exists
        inside the inventory.
        """

        filepath = str(Path(filepath))

        return any(
            item.path == filepath
            for item in self.inventory.files
        )

    # ==========================================================
    # FILTERING
    # ==========================================================

    def python_files(
        self,
    ) -> List[FileInfo]:
        """
        Return all Python source files.
        """

        return self.find_files_by_extension(".py")

    # ----------------------------------------------------------

    def non_python_files(
        self,
    ) -> List[FileInfo]:
        """
        Return all non-Python files.
        """

        return [
            file
            for file in self.inventory.files
            if file.extension != ".py"
        ]

    # ----------------------------------------------------------

    def top_largest_files(
        self,
        limit: int = 20,
    ) -> List[FileInfo]:
        """
        Return largest files.
        """

        return sorted(
            self.inventory.files,
            key=lambda file: file.size,
            reverse=True,
        )[:limit]

    # ----------------------------------------------------------

    def empty_files(
        self,
    ) -> List[FileInfo]:
        """
        Return files with zero bytes.
        """

        return [
            file
            for file in self.inventory.files
            if file.size == 0
        ]

            # ==========================================================
    # DIAGNOSTICS
    # ==========================================================

    def diagnostics(self) -> Dict[str, object]:
        """
        Return diagnostic information about the scanner.
        """

        return {
            "project_root": str(self.config.project_root),
            "supported_extensions": sorted(
                self.config.supported_extensions
            ),
            "ignored_directories": sorted(
                self.config.ignored_directories
            ),
            "directories_discovered": (
                self.inventory.total_directories
            ),
            "files_discovered": (
                self.inventory.total_files
            ),
            "python_files": (
                self.inventory.python_files
            ),
            "inventory_valid": (
                self.validate_inventory()
            ),
        }

    # ==========================================================
    # MAGIC METHODS
    # ==========================================================

    def __len__(self) -> int:
        """
        Return total number of discovered files.
        """

        return self.inventory.total_files

    # ----------------------------------------------------------

    def __iter__(self):
        """
        Iterate over discovered files.
        """

        return iter(self.inventory.files)

    # ----------------------------------------------------------

    def __repr__(self) -> str:
        """
        Debug representation.
        """

        return (
            f"{self.__class__.__name__}("
            f"directories={self.inventory.total_directories}, "
            f"files={self.inventory.total_files}, "
            f"python_files={self.inventory.python_files})"
        )


# ==========================================================
# COMMAND LINE ENTRY POINT
# ==========================================================

def main() -> None:
    """
    Execute a standalone filesystem scan.
    """

    logger.info("=" * 60)
    logger.info("MODERNIZATION TOOLKIT")
    logger.info("Filesystem Scanner")
    logger.info("=" * 60)

    scanner = FileSystemScanner()

    scanner.scan()

    scanner.print_summary()

    scanner.save()

    if scanner.validate_inventory():

        logger.info(
            "Filesystem scan completed successfully."
        )

    else:

        logger.error(
            "Filesystem scan completed with validation errors."
        )


# ==========================================================
# SCRIPT ENTRY
# ==========================================================

if __name__ == "__main__":

    main()