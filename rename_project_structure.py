"""
===============================================================================
UDUAK_QUANT_SYSTEM_PROJECT

Project Structure Migration Tool

Purpose:
    Automatically migrate the project to the standard directory layout.

Operations:
    - Rename 'test' to 'tests'
    - Ensure required package folders exist
    - Create missing __init__.py files
    - Create logs directory
    - Create pytest.ini if missing

Safe to run multiple times.
===============================================================================
"""

from pathlib import Path
import shutil

PROJECT_ROOT = Path(__file__).resolve().parent


def rename_test_folder() -> None:
    old = PROJECT_ROOT / "test"
    new = PROJECT_ROOT / "tests"

    if old.exists():
        if new.exists():
            print("[INFO] 'tests' already exists.")

            for item in old.iterdir():
                destination = new / item.name

                if destination.exists():
                    print(f"[SKIP] {destination.name} already exists.")
                else:
                    shutil.move(str(item), str(destination))

            shutil.rmtree(old)
            print("[DONE] Removed old 'test' folder.")

        else:
            old.rename(new)
            print("[DONE] Renamed 'test' -> 'tests'.")

    else:
        print("[INFO] 'test' folder not found.")


def ensure_package(folder: str) -> None:
    package = PROJECT_ROOT / folder

    package.mkdir(parents=True, exist_ok=True)

    init_file = package / "__init__.py"

    if not init_file.exists():
        init_file.touch()
        print(f"[DONE] Created {init_file.relative_to(PROJECT_ROOT)}")
    else:
        print(f"[OK] {init_file.relative_to(PROJECT_ROOT)}")


def ensure_logs() -> None:
    logs = PROJECT_ROOT / "logs"
    logs.mkdir(exist_ok=True)
    print("[OK] logs/")


def ensure_pytest_ini() -> None:
    pytest_file = PROJECT_ROOT / "pytest.ini"

    if pytest_file.exists():
        print("[OK] pytest.ini")
        return

    pytest_file.write_text(
        "[pytest]\n"
        "pythonpath = .\n"
        "testpaths = tests\n"
        "python_files = test_*.py\n",
        encoding="utf-8",
    )

    print("[DONE] Created pytest.ini")


def main() -> None:
    print("=" * 70)
    print("UDUAK QUANT SYSTEM PROJECT")
    print("Project Structure Migration")
    print("=" * 70)

    rename_test_folder()

    packages = [
        "core",
        "monitoring",
        "tests",
        "utils",
    ]

    for package in packages:
        ensure_package(package)

    ensure_logs()
    ensure_pytest_ini()

    print("=" * 70)
    print("Migration completed successfully.")
    print("=" * 70)


if __name__ == "__main__":
    main()