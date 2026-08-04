"""
Phase 6 Auto Patch

Adds runtime analyzer instance support.

Safe:
    - Creates backups
    - Skips existing code
    - Can run multiple times
"""

from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]

ANALYZER = ROOT / "core" / "analyzer_registry.py"
SIGNAL = ROOT / "core" / "signal_engine.py"


def backup(path: Path):
    shutil.copy2(path, path.with_suffix(".py.bak"))


# ==========================================================
# Backup
# ==========================================================

backup(ANALYZER)
backup(SIGNAL)

# ==========================================================
# analyzer_registry.py
# ==========================================================

text = ANALYZER.read_text(encoding="utf-8")
modified = False

# ----------------------------------------------------------
# register_instance()
# ----------------------------------------------------------

if "def register_instance(" not in text:

    insert = '''

    # ------------------------------------------------------

    def register_instance(
        self,
        analyzer_name: str,
        instance: object,
    ) -> bool:
        """
        Attach a runtime analyzer instance.
        """

        analyzer = self.get(analyzer_name)

        if analyzer is None:
            return False

        analyzer.instance = instance

        return True

'''

    pos = text.rfind("def ")

    if pos != -1:

        end = text.find("\n", pos)
        text += insert
        modified = True

# ----------------------------------------------------------
# clear_instances()
# ----------------------------------------------------------

if "def clear_instances(" not in text:

    insert = '''

    # ------------------------------------------------------

    def clear_instances(
        self,
    ) -> None:
        """
        Remove all runtime instances.
        """

        for analyzer in self._analyzers.values():

            analyzer.instance = None

'''

    text += insert
    modified = True

if modified:
    ANALYZER.write_text(text, encoding="utf-8")
    print("Patched analyzer_registry.py")
else:
    print("Analyzer registry already patched.")

# ==========================================================
# signal_engine.py
# ==========================================================

text = SIGNAL.read_text(encoding="utf-8")
modified = False

# ----------------------------------------------------------
# register_analyzer_instance()
# ----------------------------------------------------------

if "def register_analyzer_instance(" not in text:

    insert = '''

    # ------------------------------------------------------

    def register_analyzer_instance(
        self,
        analyzer_name: str,
        instance: object,
    ) -> bool:
        """
        Register a runtime analyzer.
        """

        return self.analyzer_registry.register_instance(
            analyzer_name,
            instance,
        )

'''

    pos = text.find("def evaluate(")

    if pos != -1:

        text = text[:pos] + insert + text[pos:]
        modified = True

# ----------------------------------------------------------
# clear_registered_analyzers()
# ----------------------------------------------------------

if "def clear_registered_analyzers(" not in text:

    insert = '''

    # ------------------------------------------------------

    def clear_registered_analyzers(
        self,
    ):
        """
        Remove all runtime analyzers.
        """

        self.analyzer_registry.clear_instances()

'''

    pos = text.find("def evaluate(")

    if pos != -1:

        text = text[:pos] + insert + text[pos:]
        modified = True

if modified:
    SIGNAL.write_text(text, encoding="utf-8")
    print("Patched signal_engine.py")
else:
    print("Signal engine already patched.")

print()
print("SUCCESS")
print("Phase 6 patch complete.")