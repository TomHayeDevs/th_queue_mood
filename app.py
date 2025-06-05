import os
import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv
from streamlit_autorefresh import st_autorefresh

from storage import append_row, get_counts_between, get_latest_notes

load_dotenv()
# ---------------------------------------------------
# --- MAIN APP --------------------------------------
# ---------------------------------------------------

st.set_page_config(
    page_title="Mood of the Queue",
    page_icon="😊",
    layout="centered",
)

st_autorefresh(interval=5000, key="auto_refresh")

st.markdown(
    """
    <h1 style="text-align:center;">✨ Mood of the Queue ✨</h1>
    <p style="text-align:center;">Log and visualize team mood</p>
    """,
    unsafe_allow_html=True,
)
st.write("---")

# --- LOGGING SECTION --------------------------------------
st.subheader("Log Your Mood")

EMOJI_MAP = {"😡": 1, "😠": 2, "🤔": 3, "🙂": 4, "😁": 5}
emoji = st.selectbox("Select mood", options=list(EMOJI_MAP.keys()), index=2)
mood = EMOJI_MAP[emoji]
note = st.text_input("Optional note", placeholder="Any extra context?")

if st.button("Submit"):
    success = append_row(mood, note)
    if success:
        st.success("Logged successfully!")
    else:
        st.error("Failed to log – check credentials or Sheet permissions.")

st.write("---")

# --- VISUALIZATION SECTION --------------------------------------
st.subheader("Mood Distribution")

# date filters
col_start, col_end = st.columns(2)
with col_start:
    start = st.date_input("Start date", value=datetime.now().date())
with col_end:
    end = st.date_input("End date", value=datetime.now().date())

if start > end:
    st.error("Start date cannot be after end date.")
    st.stop()

counts = get_counts_between(start.isoformat(), end.isoformat())
if not counts:
    st.error("Failed to fetch mood data. Check your credentials or Sheet permissions.")
    st.stop()

latest_notes = get_latest_notes()
hover_texts = [latest_notes.get(i, "(no note)") for i in [1, 2, 3, 4, 5]]
if not hover_texts:
    st.error("Failed to fetch latest notes.")
    st.stop()

df = pd.DataFrame({"Mood": list(counts.keys()), "Count": list(counts.values())})

if df["Count"].sum() == 0:
    st.write("No mood logged in this date range.")
else:
    EMOJI_TICKS = {v: k for k, v in EMOJI_MAP.items()}

# bar chart (Plotly, to allow for mouse-over tooltip)
fig = px.bar(
    x=[EMOJI_TICKS[i] for i in [1, 2, 3, 4, 5]],
    y=[counts[i] for i in [1, 2, 3, 4, 5]],
    labels={"y": "Number of entries"},
    hover_data={"Note": hover_texts},
)
fig.update_layout(
    title_text=f"Mood Counts: {start.isoformat()} to {end.isoformat()}",
    xaxis={'categoryorder':'array','categoryarray':[EMOJI_TICKS[i] for i in [1,2,3,4,5]]}
)
st.plotly_chart(fig, use_container_width=True)