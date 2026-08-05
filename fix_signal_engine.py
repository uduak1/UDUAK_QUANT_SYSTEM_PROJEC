from pathlib import Path
import shutil

FILE = Path("core/signal_engine.py")

if not FILE.exists():
    raise FileNotFoundError(f"Cannot find {FILE}")

# --------------------------------------------------
# Backup
# --------------------------------------------------

BACKUP = FILE.with_suffix(".py.before_collect_fix")
shutil.copy2(FILE, BACKUP)

print(f"Backup created: {BACKUP}")


text = FILE.read_text(encoding="utf-8")


# --------------------------------------------------
# Add market_data parameter
# --------------------------------------------------

text = text.replace(
    """def generate_signal(
        self,
        request: SignalRequest,
    ) -> SignalResult:""",
    """def generate_signal(
        self,
        request: SignalRequest,
        market_data=None,
    ) -> SignalResult:"""
)


# --------------------------------------------------
# Replace collect_strengths call
# --------------------------------------------------

text = text.replace(
    "strengths = self.collect_strengths()",
    "strengths = self.collect_strengths(market_data)"
)


# --------------------------------------------------
# Add collect_strengths method if missing
# --------------------------------------------------

if "def collect_strengths(" not in text:

    insert = """

    # --------------------------------------------------
    # Collect analyzer confidence strengths
    # --------------------------------------------------

    def collect_strengths(
        self,
        market_data,
    ) -> Dict[str, float]:
        \"\"\"
        Execute registered analyzers and convert
        AnalyzerResult confidence values into
        normalized strengths.
        \"\"\"

        if market_data is None:
            return {}

        results = self.analyzer_registry.execute(
            market_data
        )

        strengths = {}

        for name, result in results.items():

            if result.success:

                strengths[name] = float(
                    result.confidence
                )

        return strengths
"""

    text += insert


FILE.write_text(
    text,
    encoding="utf-8"
)

print("SignalEngine collect_strengths fix completed.")