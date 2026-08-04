"""

UDUAK_QUANT_SYSTEM_PROJECT

File: services/performance_service.py

Description:
    Business logic responsible for performance analytics.

Responsibilities:
    - Calculate trading statistics
    - Calculate profitability metrics
    - Calculate risk metrics
    - Build equity statistics
    - Produce strategy summaries

This module contains BUSINESS LOGIC ONLY.
It must NEVER contain SQL or Repository access.

"""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from typing import Any

from monitoring.logger import get_logger

logger = get_logger(__name__)

Trade = dict[str, Any] # expected keys: profit, strategy, closed_at, rr

class PerformanceService:
    """
    Business logic for performance analysis.
    Stateless - all methods operate on passed trades.
    """

    def __init__(self) -> None:
        pass

    # =========================================================================
    # BASIC COUNTS
    # =========================================================================

    def total_trades(self, trades: list[Trade]) -> int:
        return len(trades)

    def winning_trades(self, trades: list[Trade]) -> int:
        return sum(1 for t in trades if t.get("profit", 0) > 0)

    def losing_trades(self, trades: list[Trade]) -> int:
        return sum(1 for t in trades if t.get("profit", 0) < 0)

    # =========================================================================
    # PROFIT
    # =========================================================================

    def total_profit(self, trades: list[Trade]) -> float:
        return sum(float(t.get("profit", 0)) for t in trades)

    def gross_profit(self, trades: list[Trade]) -> float:
        return sum(float(t["profit"]) for t in trades if float(t.get("profit", 0)) > 0)

    def gross_loss(self, trades: list[Trade]) -> float:
        return abs(sum(float(t["profit"]) for t in trades if float(t.get("profit", 0)) < 0))

    def net_profit(self, trades: list[Trade]) -> float:
        return self.gross_profit(trades) - self.gross_loss(trades)

    # =========================================================================
    # WIN RATE
    # =========================================================================

    def win_rate(self, trades: list[Trade]) -> float:
        total = self.total_trades(trades)
        if total == 0:
            return 0.0
        return (self.winning_trades(trades) / total) * 100.0

    def loss_rate(self, trades: list[Trade]) -> float:
        total = self.total_trades(trades)
        if total == 0:
            return 0.0
        return (self.losing_trades(trades) / total) * 100.0

    # =========================================================================
    # AVERAGES
    # =========================================================================

    def average_win(self, trades: list[Trade]) -> float:
        wins = [float(t["profit"]) for t in trades if float(t.get("profit", 0)) > 0]
        if not wins:
            return 0.0
        return sum(wins) / len(wins)

    def average_loss(self, trades: list[Trade]) -> float:
        losses = [float(t["profit"]) for t in trades if float(t.get("profit", 0)) < 0]
        if not losses:
            return 0.0
        return abs(sum(losses) / len(losses))

    # =========================================================================
    # PAYOFF / PROFIT FACTOR / EXPECTANCY
    # =========================================================================

    def payoff_ratio(self, trades: list[Trade]) -> float:
        avg_loss = self.average_loss(trades)
        if avg_loss == 0:
            return 0.0
        return self.average_win(trades) / avg_loss

    def profit_factor(self, trades: list[Trade]) -> float:
        gross_loss = self.gross_loss(trades)
        if gross_loss == 0:
            return 0.0
        return self.gross_profit(trades) / gross_loss

    def expectancy(self, trades: list[Trade]) -> float:
        win_prob = self.win_rate(trades) / 100.0
        loss_prob = self.loss_rate(trades) / 100.0
        return win_prob * self.average_win(trades) - loss_prob * self.average_loss(trades)

    # =========================================================================
    # RISK
    # =========================================================================

    def equity_curve(self, trades: list[Trade]) -> list[dict]:
        """Return cumulative equity history sorted by closed_at."""
        sorted_trades = sorted(trades, key=lambda t: t.get("closed_at") or "")
        equity = 0.0
        curve = []
        for t in sorted_trades:
            equity += float(t.get("profit", 0))
            curve.append(
                {
                    "closed_at": t.get("closed_at"),
                    "profit": float(t.get("profit", 0)),
                    "equity": equity,
                }
            )
        return curve

    def max_drawdown(self, trades: list[Trade]) -> float:
        curve = self.equity_curve(trades)
        if not curve:
            return 0.0

        peak = curve[0]["equity"]
        max_dd = 0.0

        for point in curve:
            if point["equity"] > peak:
                peak = point["equity"]
            dd = peak - point["equity"]
            if dd > max_dd:
                max_dd = dd

        return max_dd

    def recovery_factor(self, trades: list[Trade]) -> float:
        dd = self.max_drawdown(trades)
        if dd == 0:
            return 0.0
        return self.net_profit(trades) / dd

    # =========================================================================
    # RISK / REWARD
    # =========================================================================

    def average_rr(self, trades: list[Trade]) -> float:
        rrs = [float(t["rr"]) for t in trades if t.get("rr") is not None]
        if not rrs:
            return 0.0
        return sum(rrs) / len(rrs)

    # =========================================================================
    # STREAKS
    # =========================================================================

    def consecutive_wins(self, trades: list[Trade]) -> int:
        sorted_trades = sorted(trades, key=lambda t: t.get("closed_at") or "")
        max_streak = curr = 0
        for t in sorted_trades:
            if float(t.get("profit", 0)) > 0:
                curr += 1
                max_streak = max(max_streak, curr)
            else:
                curr = 0
        return max_streak

    def consecutive_losses(self, trades: list[Trade]) -> int:
        sorted_trades = sorted(trades, key=lambda t: t.get("closed_at") or "")
        max_streak = curr = 0
        for t in sorted_trades:
            if float(t.get("profit", 0)) < 0:
                curr += 1
                max_streak = max(max_streak, curr)
            else:
                curr = 0
        return max_streak

    # =========================================================================
    # STRATEGY / MONTHLY
    # =========================================================================

    def strategy_summary(self, trades: list[Trade], strategy: str) -> dict:
        filtered = [t for t in trades if t.get("strategy") == strategy]
        return self.overall_statistics(filtered)

    def monthly_summary(self, trades: list[Trade]) -> list[dict]:
        grouped: dict[str, list[Trade]] = defaultdict(list)

        for t in trades:
            closed_at = t.get("closed_at")
            if isinstance(closed_at, str):
                try:
                    dt = datetime.fromisoformat(closed_at)
                    key = dt.strftime("%Y-%m")
                except ValueError:
                    key = str(closed_at)[:7]
            elif isinstance(closed_at, datetime):
                key = closed_at.strftime("%Y-%m")
            else:
                key = "unknown"
            grouped[key].append(t)

        result = []
        for month in sorted(grouped.keys()):
            month_trades = grouped[month]
            result.append(
                {
                    "month": month,
                    "total_trades": self.total_trades(month_trades),
                    "net_profit": round(self.net_profit(month_trades), 2),
                    "win_rate": round(self.win_rate(month_trades), 2),
                }
            )
        return result

    # =========================================================================
    # DASHBOARD
    # =========================================================================

    def overall_statistics(self, trades: list[Trade]) -> dict:
        stats = {
            "total_trades": self.total_trades(trades),
            "winning_trades": self.winning_trades(trades),
            "losing_trades": self.losing_trades(trades),
            "win_rate": round(self.win_rate(trades), 2),
            "loss_rate": round(self.loss_rate(trades), 2),
            "gross_profit": round(self.gross_profit(trades), 2),
            "gross_loss": round(self.gross_loss(trades), 2),
            "net_profit": round(self.net_profit(trades), 2),
            "profit_factor": round(self.profit_factor(trades), 2),
            "expectancy": round(self.expectancy(trades), 2),
            "payoff_ratio": round(self.payoff_ratio(trades), 2),
            "average_rr": round(self.average_rr(trades), 2),
            "max_drawdown": round(self.max_drawdown(trades), 2),
            "recovery_factor": round(self.recovery_factor(trades), 2),
            "longest_win_streak": self.consecutive_wins(trades),
            "longest_loss_streak": self.consecutive_losses(trades),
        }

        logger.info("Performance statistics generated.")
        return stats