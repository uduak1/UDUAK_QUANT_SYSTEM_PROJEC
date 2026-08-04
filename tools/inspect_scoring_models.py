"""
Inspect core/scoring_models.py

Prints:

1. All @dataclass classes
2. DynamicScoringEngine
3. All methods inside DynamicScoringEngine
"""

import ast
from pathlib import Path

FILE = Path("core/scoring_models.py")


def is_dataclass(node):
    for dec in node.decorator_list:
        if isinstance(dec, ast.Name):
            if dec.id == "dataclass":
                return True

        if isinstance(dec, ast.Call):
            if isinstance(dec.func, ast.Name):
                if dec.func.id == "dataclass":
                    return True

    return False


def main():

    tree = ast.parse(FILE.read_text(encoding="utf-8"))

    print("=" * 70)
    print("DATACLASSES")
    print("=" * 70)

    for node in tree.body:

        if isinstance(node, ast.ClassDef):

            if is_dataclass(node):
                print(node.name)

    print()
    print("=" * 70)
    print("DynamicScoringEngine")
    print("=" * 70)

    for node in tree.body:

        if isinstance(node, ast.ClassDef):

            if node.name == "DynamicScoringEngine":

                print(node.name)

                print()

                print("Methods")

                print("-" * 40)

                for item in node.body:

                    if isinstance(item, ast.FunctionDef):
                        print(item.name)

                return

    print("DynamicScoringEngine NOT FOUND")


if __name__ == "__main__":
    main()