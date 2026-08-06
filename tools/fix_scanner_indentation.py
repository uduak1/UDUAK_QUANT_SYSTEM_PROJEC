"""
tools/fix_json_path_serialization.py

Fixes Path serialization in
tools/modernization/python_scanner/models.py

Usage:
python tools/fix_json_path_serialization.py
"""

from pathlib import Path
import shutil

TARGET = Path(
    "tools/modernization/python_scanner/models.py"
)


def main():

    print("=" * 60)
    print("JSON PATH SERIALIZATION FIX")
    print("=" * 60)

    backup = TARGET.with_suffix(".py.bak")

    shutil.copy2(TARGET, backup)

    text = TARGET.read_text(encoding="utf-8")

    old = "return asdict(self)"

    new = """data = asdict(self)

        data["path"] = str(self.path)

        return data"""

    if old not in text:

        print("Target code not found.")

        return

    text = text.replace(old, new, 1)

    TARGET.write_text(text, encoding="utf-8")

    print("[OK] Backup created")
    print("[OK] Path serialization fixed")
    print("[OK] Done")


if __name__ == "__main__":
    main()