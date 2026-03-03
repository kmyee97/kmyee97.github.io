#!/bin/bash
# Bot runner loop - Claw
LOG=bot_run.log
FIX_COUNT=0
MAX_FIX=5

while true; do
  echo &quot;=== Run $((++RUN_COUNT)) at $(date) ===&quot; | tee -a $LOG
  source venv/bin/activate
  if python equities_bot.py >> $LOG 2>&1; then
    echo &quot;SUCCESS! Summary above. Sleeping 30min.&quot; | tee -a $LOG
    sleep 1800
  else
    echo &quot;FAILED - attempt fix $((++FIX_COUNT))&quot; | tee -a $LOG
    # Pseudo fix: pip upgrade
    pip install --upgrade yfinance pandas numpy --force-reinstall >> $LOG 2>&1
    if [ $FIX_COUNT -ge $MAX_FIX ]; then
      echo &quot;Max fixes—stop.&quot; | tee -a $LOG
      break
    fi
    sleep 60
  fi
done