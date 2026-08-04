from pathlib import Path

FILE = Path("core/decision_engine.py")

text = FILE.read_text(encoding="utf-8")

old = """            return DecisionResult(
    strategy_name=strategy_name,
    decision=decision,
    approved=score.approved,
    total_score=score.total_score,
    minimum_required=score.minimum_required,
    risk_reward=risk_reward,
    score=score,
    missing_components=score.missing_components,
    rejection_reason=rejection_reason,
    metadata={
        "component_count": len(strengths),
        "approved_by_score": score.approved,
        "risk_reward_passed": risk_reward >= self.minimum_rr,
    },
)"""

new = """        return DecisionResult(
            strategy_name=strategy_name,
            decision=decision,
            approved=score.approved,
            total_score=score.total_score,
            minimum_required=score.minimum_required,
            risk_reward=risk_reward,
            score=score,
            missing_components=score.missing_components,
            rejection_reason=rejection_reason,
            metadata={
                "component_count": len(strengths),
                "approved_by_score": score.approved,
                "risk_reward_passed": risk_reward >= self.minimum_rr,
            },
        )"""

if old not in text:
    print("ERROR")
    print("Return block not found.")
    raise SystemExit(1)

text = text.replace(old, new, 1)

FILE.write_text(text, encoding="utf-8")

print("SUCCESS")
print("DecisionEngine return block fixed.")