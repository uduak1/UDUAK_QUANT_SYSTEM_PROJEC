#!/usr/bin/env python3
"""
tools/patch_scoring_models.py

UDUAK QUANT SYSTEM

Automatically replace core/scoring_models.py with a
clean institutional version.

Usage

python tools/patch_scoring_models.py
"""

from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parent.parent

TARGET = ROOT / "core" / "scoring_models.py"

TEMPLATE = ROOT / "templates" / "scoring_models_clean.py"


def backup_target():
    backup = TARGET.with_suffix(".py.bak")

    shutil.copy2(TARGET, backup)

    print(f"[OK] Backup created:\n{backup}")

    return backup


def patch():

    if not TEMPLATE.exists():

        print(
            "\nERROR\n"
            "Template not found:\n"
            f"{TEMPLATE}"
        )

        sys.exit(1)

    if not TARGET.exists():

        print(
            "\nERROR\n"
            "Target not found:\n"
            f"{TARGET}"
        )

        sys.exit(1)

    backup_target()

    shutil.copy2(TEMPLATE, TARGET)

    print(
        "\nSUCCESS\n"
        "core/scoring_models.py patched successfully."
    )


if __name__ == "__main__":
    patch()