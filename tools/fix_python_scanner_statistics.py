"""
tools/fix_python_scanner_statistics.py

Repairs scanner.py so statistics are refreshed
before logging and report generation.

Usage
-----
python tools/fix_python_scanner_statistics.py
"""

from pathlib import Path
import shutil

TARGET = Path(
    "tools/modernization/python_scanner/scanner.py"
)


def backup():

    bak = TARGET.with_suffix(".py.bak")

    shutil.copy2(TARGET, bak)

    print(f"[OK] Backup -> {bak.name}")


def patch(text: str):

    marker = """analysis = (
            self.project_parser.parse(
                self.project_root
            )
        )"""

    replacement = marker + """

        # ------------------------------------------
        # Refresh project statistics
        # ------------------------------------------

        if hasattr(
            analysis,
            "update_statistics",
        ):
            analysis.update_statistics()
"""

    if "update_statistics()" in text:

        print("[OK] Statistics refresh already exists.")

        return text, False

    if marker not in text:

        raise RuntimeError(
            "Unable to locate parse() block."
        )

    return text.replace(
        marker,
        replacement,
        1,
    ), True


def verify(text):

    return "analysis.update_statistics()" in text


def main():

    print("=" * 60)
    print("PYTHON SCANNER STATISTICS FIX")
    print("=" * 60)

    if not TARGET.exists():

        print("scanner.py not found.")

        return

    backup()

    text = TARGET.read_text(
        encoding="utf-8"
    )

    text, changed = patch(text)

    TARGET.write_text(
        text,
        encoding="utf-8",
    )

    if verify(text):

        print("[OK] Statistics refresh inserted.")

    else:

        print("[FAILED] Patch verification failed.")

    if changed:

        print("[OK] Patch applied.")

    else:

        print("[OK] No changes required.")

    print()
    print("Done.")


if __name__ == "__main__":

    main()