"""
tools/fix_analyzer_registry_phase8.py

Phase 8
Automatic AnalyzerRegistry Repair

Repairs:
1. lastlastlastlast_execution_times
2. lastlastlast_execution_times

Both become

    last_execution_times

Author:
UDUAK Quant System
"""

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent

FILE = ROOT / "core" / "analyzer_registry.py"


def main():

    if not FILE.exists():
        print("ERROR: core/analyzer_registry.py not found.")
        return

    text = FILE.read_text(encoding="utf-8")

    replacements = {
        "lastlastlastlast_execution_times": "last_execution_times",
        "lastlastlast_execution_times": "last_execution_times",
    }

    changed = False

    for old, new in replacements.items():

        if old in text:
            text = text.replace(old, new)
            changed = True

    if changed:
        FILE.write_text(text, encoding="utf-8")
        print("✓ AnalyzerRegistry repaired successfully.")
    else:
        print("✓ AnalyzerRegistry already clean.")


if __name__ == "__main__":
    main()