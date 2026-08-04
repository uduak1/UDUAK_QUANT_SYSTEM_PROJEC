"""
Phase 5 Auto Patch
core/signal_engine.py

Safe patcher

• Creates backup
• Detects existing code
• Never duplicates
"""

from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]

SIGNAL_FILE = ROOT / "core" / "signal_engine.py"
ANALYZER_FILE = ROOT / "core" / "analyzer_registry.py"

# ==========================================================
# BACKUP
# ==========================================================

for file in (SIGNAL_FILE, ANALYZER_FILE):

    if file.exists():

        shutil.copy2(file, file.with_suffix(".py.bak"))

# ==========================================================
# PATCH ANALYZER REGISTRY
# ==========================================================

text = ANALYZER_FILE.read_text(encoding="utf-8")

if "instance:" not in text:

    marker = 'version: str = "1.0"'

    replacement = (
        marker
        + "\n\n"
        + "    instance: object | None = None"
    )

    text = text.replace(marker, replacement)

    ANALYZER_FILE.write_text(text, encoding="utf-8")

    print("Patched analyzer_registry.py")

else:

    print("Analyzer registry already patched.")

# ==========================================================
# PATCH SIGNAL ENGINE
# ==========================================================

text = SIGNAL_FILE.read_text(encoding="utf-8")

modified = False

# ----------------------------------------------------------
# collect_strengths()
# ----------------------------------------------------------

if "def collect_strengths" not in text:

    insert = '''

    # --------------------------------------------------

    def collect_strengths(self) -> Dict[str, float]:
        """
        Collect strengths from enabled analyzers.
        """

        strengths: Dict[str, float] = {}

        for analyzer in self.available_analyzers():

            instance = getattr(analyzer, "instance", None)

            if instance is None:
                continue

            analyzer_output = instance.analyze()

            strengths.update(analyzer_output)

        return strengths

'''

    pos = text.find("def evaluate(")

    if pos != -1:

        text = text[:pos] + insert + text[pos:]

        modified = True

# ----------------------------------------------------------
# Auto strengths
# ----------------------------------------------------------

if "self.collect_strengths()" not in text:

    marker = "# --------------------------------------------------\n        # Ask the Decision Engine"

    replacement = '''
        # --------------------------------------------------
        # Automatically collect analyzer strengths
        # --------------------------------------------------

        strengths = request.strengths

        if not strengths:

            strengths = self.collect_strengths()

''' + marker

    if marker in text:

        text = text.replace(marker, replacement)

        modified = True

# ----------------------------------------------------------
# DecisionEngine call
# ----------------------------------------------------------

old = """strengths=request.strengths,"""

new = """strengths=strengths,"""

if old in text:

    text = text.replace(old, new)

    modified = True

# ----------------------------------------------------------
# Metadata
# ----------------------------------------------------------

old = "len(request.strengths)"

new = "len(strengths)"

if old in text:

    text = text.replace(old, new)

    modified = True

if modified:

    SIGNAL_FILE.write_text(text, encoding="utf-8")

    print("Patched signal_engine.py")

else:

    print("Signal engine already patched.")

print("\nSUCCESS")
print("Phase 5 complete.")