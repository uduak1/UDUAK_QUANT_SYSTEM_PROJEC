from pathlib import Path
import shutil
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def main():
    if len(sys.argv) != 3:
        print("Usage:")
        print("python tools/apply_patch.py <target_file> <template_file>")
        sys.exit(1)

    target = PROJECT_ROOT / sys.argv[1]
    template = PROJECT_ROOT / sys.argv[2]

    if not template.exists():
        print(f"[ERROR] Template not found: {template}")
        sys.exit(1)

    if target.exists():
        backup = target.with_suffix(target.suffix + ".bak")
        shutil.copy2(target, backup)
        print(f"[OK] Backup created: {backup.name}")

    shutil.copy2(template, target)

    print(f"[OK] Updated: {target.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()