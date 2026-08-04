#!/usr/bin/env bash

echo "========================================="
echo " FULL PROJECT SCAN"
echo "========================================="

grep -RIn \
-e "DecisionEngine" \
-e "decision_engine" \
-e "score_breakdown" \
-e "signal_score" \
-e "SignalScore" \
-e "ScoreCalculator" \
-e "confidence_score" \
-e "quality_score" \
-e "weighted" \
-e "weights" \
-e "approval" \
-e "approve_trade" \
-e "final_score" \
-e "institutional" \
-e "market_score" \
-e "trade_score" \
-e "component_score" \
-e "score_components" \
--exclude-dir=.git \
--exclude-dir=venv \
--exclude-dir=.venv \
--exclude-dir=__pycache__ \
.