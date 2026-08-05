"""
tools/patch_analyzer_registry_phase1.py

UDUAK QUANT SYSTEM

Phase 1 Patch
Analyzer Registry Auto Fix

Safely patches:

    core/analyzer_registry.py

Fixes
------

✔ Creates backup
✔ Adds traceback import
✔ analyzer.analyzer_name -> analyzer.name
✔ Removes duplicate execution statistic dictionaries
✔ Renames _execution_times -> last_execution_times
✔ Renames _failed_analyzers -> last_failures
✔ Cleans duplicate declarations
✔ Prints verification report

Usage
-----

python tools/patch_analyzer_registry_phase1.py
"""

from pathlib import Path
import shutil
import re

PROJECT_ROOT = Path(__file__).resolve().parents[1]

TARGET = PROJECT_ROOT / "core" / "analyzer_registry.py"

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

    text = TARGET.read_text(encoding="utf-8")

    changes = []

    # ------------------------------------------------------
    # traceback import
    # ------------------------------------------------------

    if "import traceback" not in text:

        text = text.replace(
            "import time",
            "import time\nimport traceback",
        )

        changes.append("Added traceback import")

    # ------------------------------------------------------
    # analyzer.analyzer_name
    # ------------------------------------------------------

    if "analyzer.analyzer_name" in text:

        count = text.count("analyzer.analyzer_name")

        text = text.replace(
            "analyzer.analyzer_name",
            "analyzer.name",
        )

        changes.append(
            f"Fixed analyzer.name ({count})"
        )

    # ------------------------------------------------------
    # Remove duplicate dictionaries
    # ------------------------------------------------------

    pattern_execution = re.compile(
        r"\n\s*self\._execution_times: Dict\[str,\s*float\]\s*=\s*\{\}\s*",
        re.MULTILINE,
    )

    matches = pattern_execution.findall(text)

    if matches:

        text = pattern_execution.sub(
            "",
            text,
        )

        changes.append(
            f"Removed duplicate _execution_times ({len(matches)})"
        )

    pattern_failed = re.compile(
        r"\n\s*self\._failed_analyzers: Dict\[str,\s*str\]\s*=\s*\{\}\s*",
        re.MULTILINE,
    )

    matches = pattern_failed.findall(text)

    if matches:

        text = pattern_failed.sub(
            "",
            text,
        )

        changes.append(
            f"Removed duplicate _failed_analyzers ({len(matches)})"
        )

    # ------------------------------------------------------
    # Replace remaining references
    # ------------------------------------------------------

    if "_execution_times" in text:

        count = text.count("_execution_times")

        text = text.replace(
            "_execution_times",
            "last_execution_times",
        )

        changes.append(
            f"Unified execution timing ({count})"
        )

    if "_failed_analyzers" in text:

        count = text.count("_failed_analyzers")

        text = text.replace(
            "_failed_analyzers",
            "last_failures",
        )

        changes.append(
            f"Unified failure storage ({count})"
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

    text = TARGET.read_text(encoding="utf-8")

    errors = []

    if "analyzer.analyzer_name" in text:

        errors.append(
            "Old analyzer_name property still exists"
        )

    if "_execution_times" in text:

        errors.append(
            "_execution_times still exists"
        )

    if "_failed_analyzers" in text:

        errors.append(
            "_failed_analyzers still exists"
        )

    if "import traceback" not in text:

        errors.append(
            "traceback import missing"
        )

    return errors


# ==========================================================
# MAIN
# ==========================================================

def main():

    print("=" * 60)
    print("PATCHING ANALYZER REGISTRY")
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