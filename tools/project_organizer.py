from pathlib import Path
import shutil

PROJECT_ROOT = Path(__file__).resolve().parent
TOOLS_DIR = PROJECT_ROOT / "tools"

# Create tools directory
TOOLS_DIR.mkdir(exist_ok=True)

# Create __init__.py
(TOOLS_DIR / "__init__.py").touch(exist_ok=True)

# Move this script into tools if it is still in the project root
CURRENT_FILE = Path(__file__).resolve()

if CURRENT_FILE.parent == PROJECT_ROOT:
    destination = TOOLS_DIR / CURRENT_FILE.name

    if not destination.exists():
        shutil.move(str(CURRENT_FILE), str(destination))
        print(f"Moved {CURRENT_FILE.name} -> tools/")
    else:
        print("project_organizer.py already exists in tools/")
else:
    print("Already running from tools/")