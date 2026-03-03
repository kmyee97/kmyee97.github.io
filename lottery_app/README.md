# Lottery Predictor 🦞

## Run It
```bash
cd lottery_app
chmod +x run.sh
./run.sh
```
- First run: creates `venv/`, installs deps (~1min).
- Opens http://localhost:8501 automatically.
- Refresh/re-run anytime.

## Customize
- Edit `app.py` for scrapers/charts/generators.
- AZ Pick scraper: Tweak BS4 selector if lotterypost changes (inspect HTML).

## Notes
- Uses NY open data for Powerball/Mega Millions YTD JSON.
- Lotterypost for AZ The Pick (scraped table).
- Predictions: Weighted random from hot numbers (freq-based).
- **Random game—fun stats only! No guarantees.**

Tested on Python 3.14+. Play responsibly.