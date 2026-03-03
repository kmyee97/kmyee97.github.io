# StockClaw v1.1 Setup Summary

## Overview
We've built a micro-budget ($300 max) trading bot for Charles Schwab Trader API, focusing on US equities and Level 2 options. All critical guards are in place for safety.

## Key Features
- **Budget Cap**: $300 total (cash + positions), $1.50 max per-trade risk.
- **Time Windows**: Trades only 9:30-11:30 AM ET or 2-4 PM ET.
- **Human Oversight**: Requires user online confirmation before trades.
- **Level 2 Only**: Long calls/puts, covered calls, protective puts—no spreads/naked.
- **Risk Management**: 2:1 RR min, -0.5% stops, skip VIX>25/earnings.
- **Scanning**: S&P500 + <$20 stocks + cheap options ($0.20-1.00 prem).
- **Signals**: RSI<35 + vol surge>150% + bullish MACD + score>85.
- **Execution**: Limit orders with stops/targets, 10-min cycles.

## Files Created
- `stockclaw_v2.py`: Full Python script with mocked Schwab API functions.
- Replace mocks with real API calls (schwab-python library or direct requests).
- Schwab API docs: https://developer.schwab.com/

## Next Steps (When Account/API Ready)
1. Set up Schwab Developer account and get app_key, tokens, account_hash.
2. Replace mock functions in `stockclaw_v2.py` with real Schwab API calls.
3. Test in paper trading mode first.
4. Update username in online_check().
5. Run the script during market hours.

## Conversation History
- Attempted GitHub CLI setup (needs token input).
- Spawned subagents for StockClaw: scan failed (API permissions), script creation succeeded.
- Created mocked script enforcing all guards.

Ready to activate once Schwab account is live! 🦞