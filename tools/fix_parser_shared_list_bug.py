"""
tools/fix_parser_shared_list_bug.py

Repairs the shared-list bug in:

- class_parser.py
- function_parser.py
"""

from pathlib import Path
import re

ROOT = Path("tools/modernization/python_scanner")

FILES = [
    ROOT / "class_parser.py",
    ROOT / "function_parser.py",
]


NEW_PARSE = """def parse(
        self,
        tree: ast.AST,
    ) -> List[{}]:

        self.{} = []

        self._inside_class = False if hasattr(self, "_inside_class") else False

        self.visit(tree)

        return list(self.{})
"""


def patch_function_parser(text: str) -> str:

    pattern = (
        r"def parse\([\s\S]*?return self\.functions"
    )

    replacement = NEW_PARSE.format(
        "FunctionInfo",
        "functions",
        "functions",
    )

    return re.sub(
        pattern,
        replacement,
        text,
        count=1,
    )


def patch_class_parser(text: str) -> str:

    pattern = (
        r"def parse\([\s\S]*?return self\.classes"
    )

    replacement = """def parse(
        self,
        tree: ast.AST,
    ) -> List[ClassInfo]:

        self.classes = []

        self.visit(tree)

        return list(self.classes)
"""

    return re.sub(
        pattern,
        replacement,
        text,
        count=1,
    )


print("=" * 60)
print("FIXING PARSER SHARED LIST BUG")
print("=" * 60)

for file in FILES:

    source = file.read_text(
        encoding="utf-8",
    )

    backup = file.with_suffix(
        file.suffix + ".bak"
    )

    backup.write_text(
        source,
        encoding="utf-8",
    )

    if file.name == "function_parser.py":
        patched = patch_function_parser(source)
    else:
        patched = patch_class_parser(source)

    file.write_text(
        patched,
        encoding="utf-8",
    )

    print(f"[OK] {file.name}")

print()
print("Backups created.")
print("Done.")