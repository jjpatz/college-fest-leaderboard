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
    padding: 10px; /* Reduced for mobile */
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.footer-update {
    position: fixed;
    bottom: 10px;
    right: 10px;
    font-family: 'Montserrat', sans-serif;
    font-size: 10px; /* Smaller for mobile */
    color: white;
    z-index: 999;
    background: rgba(0, 0, 0, 0.5);
    padding: 4px 8px;
    border-radius: 5px;
}

/* Ensure the logo shrinks on small screens */
.header-container img {
    max-width: 100%;
    height: auto;
}
</style>
""", unsafe_allow_html=True)

# 4. LOGO
logo_url = "https://raw.githubusercontent.com/jjpatz/college-fest-leaderboard/main/logo.png"
st.markdown(f"""
    <div class="header-container" style="text-align:center;">
        <img src="{logo_url}" width="600">
    </div>
    <div class="footer-update">Updated as of {last_updated}</div>
    """, unsafe_allow_html=True)

# 5. PLOTLY CHART
fig = px.bar(
    df, x="ORGANIZATION", y=df.columns[1], text=df.columns[1],
    color=df.columns[1], color_continuous_scale=["#31D07E", "#10B981", "#065F46"] 
)

# Text on TOP of bars (Responsive size)
fig.update_traces(
    texttemplate='<b>%{text}</b>', 
    textposition="outside",
    marker_line_width=0,
    marker_cornerradius=10,
    textfont=dict(size=15) # Plotly will try to scale this
)

# Organization labels INSIDE bars (Responsive adjustment)
for i, (index, row) in enumerate(df.iterrows()):
    fig.add_annotation(
        x=row["ORGANIZATION"],
        y=0, 
        text=f"<b>{row['ORGANIZATION']}</b>",
        showarrow=False,
        yshift=20, 
        font=dict(color="white", size=20), # Smaller default size works better for both
        textangle=-90 if len(df) > 5 else 0 # Auto-rotate if many orgs exist
    )

# 6. LAYOUT (Responsive tweaks)
fig.update_layout(
    xaxis={
        'visible': True,
        'showticklabels': False,
        'title': {'text': "<b>Organizations</b>", 'font': {'size': 14}, 'standoff': 20}
    },
    yaxis={
        'visible': True,
        'showticklabels': False,
        'title': {'text': "<b>Points</b>", 'font': {'size': 14}, 'standoff': 10}
    },
    coloraxis_showscale=False,
    paper_bgcolor='rgba(0,0,0,0)', 
    plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(t=40, b=40, l=40, r=10), # Tighter margins for mobile
    bargap=0.05,
    autosize=True # Crucial for mobile scaling
)

st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})