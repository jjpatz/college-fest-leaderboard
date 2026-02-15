import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import pytz

# 1. PAGE CONFIG
st.set_page_config(page_title="🦉 CASadya 2026 Leaderboards", layout="wide")

# 2. DATA LOAD & TIMESTAMP
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ1k4Liz4HvtBM6s8OaPex9E_8zmGTb_DLtlyShFifZ1XLSQ2e06XI3XQLefwH1xSIu0b-NWBaH3pcf/pub?output=csv"
df = pd.read_csv(url)
df = df.sort_values(by=df.columns[1], ascending=False)

# Get current time
now = datetime.now(pytz.timezone('Asia/Manila'))
last_updated = now.strftime("%B %d, %Y | %I:%M %p")

# 3. CSS INJECTION
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Lexend:wght@700&display=swap');

.stMainBlockContainer {
    padding-top: 1rem !important;
}

.stApp {
    background-image: url("https://raw.githubusercontent.com/jjpatz/college-fest-leaderboard/main/Background.png");
    background-size: cover;
    background-position: center;
    background-attachment: scroll;
}

html, body, [class*="css"] {
    font-family: 'Lexend', sans-serif;
    color: white;
}

[data-testid="stVerticalBlock"] > div:has(div[data-testid="stPlotlyChart"]) {
    background: rgba(0, 0, 0, 0.4);
    backdrop-filter: blur(15px);
    border-radius: 20px;
    padding: 20px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.header-container {
    text-align: center;
    margin-bottom: 20px;
}

.footer-update {
    position: fixed;
    bottom: 20px;
    right: 20px;
    font-family: 'Montserrat', sans-serif;
    font-size: 12px;
    color: white;
    text-shadow: 1px 1px 3px #000000;
    z-index: 999;
    background: rgba(0, 0, 0, 0.3);
    padding: 5px 10px;
    border-radius: 5px;
}

h1 { 
    color: white !important; 
    text-shadow: 2px 2px 8px #000000; 
    text-align: center;
    margin-top: 5px !important;
}
</style>
""", unsafe_allow_html=True)

# 4. LOGO DISPLAY
logo_url = "https://raw.githubusercontent.com/jjpatz/college-fest-leaderboard/main/logo.png"

st.markdown(f"""
    <div class="header-container">
        <img src="{logo_url}" width="600">
    </div>
    <div class="footer-update">Updated as of {last_updated}</div>
    """, unsafe_allow_html=True)

# 5. PLOTLY CHART
fig = px.bar(
    df, 
    x="ORGANIZATION", 
    y=df.columns[1], 
    text=df.columns[1],
    color=df.columns[1], 
    color_continuous_scale=["#31D07E", "#10B981", "#065F46"] 
)

fig.update_traces(
    texttemplate='<b>%{text}</b>', 
    textposition="outside",
    marker_line_width=0,
    marker_cornerradius=15,
    hovertemplate="<b>Organization %{x}</b><br>Points: <b>%{y}</b><extra></extra>",
    textfont=dict(size=15, color="white")
)

# Organization labels inside bars
for i, (index, row) in enumerate(df.iterrows()):
    fig.add_annotation(
        x=row["ORGANIZATION"],
        y=0, 
        text=f"<b>{row['ORGANIZATION']}</b>",
        showarrow=False,
        yshift=30, 
        font=dict(color="white", size=25, family="Lexend"),
        textangle=0 
    )

# 6. LAYOUT (FIXED SYNTAX)
fig.update_layout(
    xaxis={
        'visible': True,
        'showticklabels': False,
        'title': {
            'text': "<b>Participating Organizations</b>",
            'font': {'family': "Lexend", 'size': 20, 'color': "white"},
            'standoff': 40
        },
        'fixedrange': True
    },
    yaxis={
        'visible': True,
        'showticklabels': False,
        'title': {
            'text': "<b>Total Points</b>",
            'font': {'family': "Lexend", 'size': 20, 'color': "white"},
            'standoff': 20
        },
        'fixedrange': True
    },
    coloraxis_showscale=False,
    paper_bgcolor='rgba(0,0,0,0)', 
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family="Lexend", color="white"),
    margin=dict(t=50, b=100, l=80, r=25), # Increased left (l) and bottom (b) for titles
    bargap=0.05
)

with st.container():
    st.plotly_chart(fig, use_container_width=True)