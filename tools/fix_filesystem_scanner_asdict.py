"""
tools/fix_filesystem_scanner_asdict.py

UDUAK QUANT SYSTEM

Filesystem Scanner Auto Fix

Fixes
------

✔ Creates backup
✔ Adds asdict import
✔ Replaces vars(...) with asdict(...)
✔ Verifies patch
✔ Safe to run multiple times

Usage
-----

python tools/fix_filesystem_scanner_asdict.py
"""

from pathlib import Path
import shutil
import re

PROJECT_ROOT = Path(__file__).resolve().parents[1]

TARGET = (
    PROJECT_ROOT
    / "tools"
    / "modernization"
    / "scanner"
    / "filesystem_scanner.py"
)

BACKUP = TARGET.with_suffix(".py.bak")


# ==========================================================
# BACKUP
# ==========================================================

def backup():

    if BACKUP.exists():

        print("[SKIP] Backup already exists")

    else:

        shutil.copy2(TARGET, BACKUP)

        print(f"[OK] Backup created -> {BACKUP.name}")


# ==========================================================
# PATCH
# ==========================================================

def patch():

    text = TARGET.read_text(
        encoding="utf-8",
    )

    changes = []

    # ------------------------------------------------------
    # Ensure asdict import exists
    # ------------------------------------------------------

    if "asdict" not in text:

        pattern = (
            r"from dataclasses import "
            r"([^\n]+)"
        )

        match = re.search(
            pattern,
            text,
        )

        if match:

            imports = match.group(1)

            if "asdict" not in imports:

                new_import = (
                    "from dataclasses import "
                    + imports.strip()
                    + ", asdict"
                )

                text = text.replace(
                    match.group(0),
                    new_import,
                    1,
                )

                changes.append(
                    "Added asdict import"
                )

    # ------------------------------------------------------
    # Replace vars(...)
    # ------------------------------------------------------

    count = len(
        re.findall(
            r"\bvars\s*\(",
            text,
        )
    )

    if count:

        text = re.sub(
            r"\bvars\s*\(",
            "asdict(",
            text,
        )

        changes.append(
            f"Replaced vars() ({count})"
        )

    TARGET.write_text(
        text,
        encoding="utf-8",
    )

    return changes


# ==========================================================
# VERIFY
# ==========================================================

def verify():

    text = TARGET.read_text(
        encoding="utf-8",
    )

    errors = []

    if "vars(" in text:

        errors.append(
            "vars() still exists"
        )

    if "asdict" not in text:

        errors.append(
            "asdict import missing"
        )

    return errors


# ==========================================================
# MAIN
# ==========================================================

def main():

    print("=" * 60)
    print("FILESYSTEM SCANNER AUTO FIX")
    print("=" * 60)

    backup()

    print()

    changes = patch()

    print("Applied Changes")

    if changes:

        for item in changes:

            print(f"  ✔ {item}")

    else:

        print("  Nothing to patch")

    print()

    errors = verify()

    if errors:

        print("Verification FAILED")

        for err in errors:

            print(f"  ✘ {err}")

    else:

        print("Verification PASSED")

    print()
    print("Patch Complete")


if __name__ == "__main__":
    main()