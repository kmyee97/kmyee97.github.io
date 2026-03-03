import streamlit as st
import numpy as np
import pandas as pd
from collections import Counter
from datetime import datetime

st.set_page_config(layout="wide")

st.title("🦞 10 Lottery Sets - Auto Refresh")

game = st.selectbox("Game:", ["Powerball", "Mega Millions", "Arizona The Pick"], key="game")
year = st.slider("Year:", 2020, datetime.now().year, datetime.now().year-1, key="year")

if 'last_game' not in st.session_state:
    st.session_state.last_game = game
if 'last_year' not in st.session_state:
    st.session_state.last_year = year

if game != st.session_state.last_game or year != st.session_state.last_year:
    st.session_state.last_game = game
    st.session_state.last_year = year
    st.rerun()

# Config & probs
if game == "Powerball":
    main_range, main_c = range(1,70), 5
    bonus_range = range(1,27)
    hot_main = [61,21,23,32,36,39,59,62,63,69]
elif game == "Mega Millions":
    main_range, main_c = range(1,71), 5
    bonus_range = range(1,26)
    hot_main = [10,3,17,46,14,31,20,8,38,64]
else:  # AZ Pick
    main_range, main_c = range(1,45), 6
    bonus_range = None
    hot_main = [23,19,27,41,34,28,9,38,23,27]

freq_main = Counter(hot_main * (year % 10 + 5))  # fake year bias
probs_main = np.array([freq_main.get(i, 1) for i in main_range], dtype=float)
probs_main /= probs_main.sum()

st.subheader(f"{game} {year} - 10 Sets (Hot Bias)")
preds = []
for i in range(10):
    main = sorted(np.random.choice(list(main_range), main_c, replace=False, p=probs_main))
    if bonus_range:
        bonus = np.random.choice(list(bonus_range))
        preds.append({'Main': '-'.join(f'{n:2}' for n in main), 'Bonus': bonus})
    else:
        preds.append({'Main': '-'.join(f'{n:2}' for n in main)})

st.dataframe(pd.DataFrame(preds), use_container_width=True)

st.caption("Auto-refreshes on game/year. Hot YTD bias. Reroll: change slider.")