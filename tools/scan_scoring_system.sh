#!/usr/bin/env bash

echo "==========================================================="
echo "        UDUAK QUANT SYSTEM - SCORING SYSTEM SCAN"
echo "==========================================================="

SEARCH_DIRS="analysis core services config database models"

KEYWORDS=(
"score"
"confidence"
"weight"
"weighted"
"signal_score"
"quality_score"
"rank"
"ranking"
"priority"
"probability"
"threshold"
"min_confidence"
"max_confidence"
"decision"
"approve"
"approved"
"reject"
"rejected"
"buy"
"sell"
"wait"
"hold"
"confirmation"
"confirmations"
"signal_strength"
"strength"
"regime"
"trend_alignment"
"trend"
"bias"
"risk_reward"
"rr"
)

echo
echo "Searching directories:"
echo "$SEARCH_DIRS"
echo

for word in "${KEYWORDS[@]}"
do
    echo "======================================================"
    echo "KEYWORD: $word"
    echo "======================================================"

    grep -RIn \
        --exclude-dir=.git \
        --exclude-dir=__pycache__ \
        --exclude-dir=.pytest_cache \
        --exclude-dir=htmlcov \
        --include="*.py" \
        "$word" \
        $SEARCH_DIRS 2>/dev/null

    echo
done

echo
echo "======================================================"
echo "Possible scoring functions"
echo "======================================================"

grep -RIn \
--include="*.py" \
-E "def .*score|def .*confidence|def .*decision|def .*rank|def .*weight|class .*Decision|class .*Score|class .*Signal" \
$SEARCH_DIRS 2>/dev/null

echo
echo "======================================================"
echo "Possible configuration constants"
echo "======================================================"

grep -RIn \
--include="*.py" \
-E "MIN_|MAX_|THRESHOLD|CONFIDENCE|WEIGHT|SCORE" \
config analysis core services database 2>/dev/null

echo
echo "======================================================"
echo "Decision logic"
echo "======================================================"

grep -RIn \
--include="*.py" \
-E "BUY|SELL|WAIT|APPROVE|REJECT|EXECUTE|NO_TRADE" \
analysis core services 2>/dev/null

echo
echo "======================================================"
echo "SCAN COMPLETE"
echo "======================================================"