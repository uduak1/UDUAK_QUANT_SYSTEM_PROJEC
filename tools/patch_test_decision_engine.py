from pathlib import Path

FILE = Path("tests/test_decision_engine.py")

text = FILE.read_text(encoding="utf-8")

start = text.find("# ==========================================================\n# APPROVED TRADE")
end = text.find("def test_reject_low_rr()")

if start == -1 or end == -1:
    print("ERROR: Could not locate the patch region.")
    raise SystemExit(1)

replacement = '''# ==========================================================
# REJECTED TRADE (LOW SCORE)
# ==========================================================

def test_rejected_trade_low_score():

    engine = DecisionEngine()

    strengths = {
        "market_structure": 1.0,
        "liquidity_sweep": 1.0,
        "change_of_character": 1.0,
        "trend_alignment": 1.0,
        "fair_value_gap": 1.0,
    }

    result = engine.evaluate(
        "LiquiditySweepReversal",
        strengths,
        3.5,
    )

    assert result.approved is False
    assert result.decision == "REJECTED"


# ==========================================================
# APPROVED TRADE
# ==========================================================

def test_approved_trade():

    engine = DecisionEngine()

    strengths = {
        "market_structure": 1.0,
        "liquidity_sweep": 1.0,
        "fair_value_gap": 1.0,
        "order_block": 1.0,
        "change_of_character": 1.0,
        "break_of_structure": 1.0,
        "trend_alignment": 1.0,
        "volume_confirmation": 1.0,
        "session_quality": 1.0,
        "market_regime": 1.0,
        "premium_discount": 1.0,
    }

    result = engine.evaluate(
        "LiquiditySweepReversal",
        strengths,
        5.0,
    )

    assert result.approved is True
    assert result.decision == "APPROVED"

'''

text = text[:start] + replacement + text[end:]

FILE.write_text(text, encoding="utf-8")

print("SUCCESS")
print("Patched tests/test_decision_engine.py")