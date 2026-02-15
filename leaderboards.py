import streamlit as st
import pandas as pd
import plotly.express as px

# 1. PAGE CONFIG
st.set_page_config(page_title="🦉 CASadya 2026 Leaderboards", layout="wide")

# 2. DATA LOAD
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ1k4Liz4HvtBM6s8OaPex9E_8zmGTb_DLtlyShFifZ1XLSQ2e06XI3XQLefwH1xSIu0b-NWBaH3pcf/pub?output=csv"
df = pd.read_csv(url)

# 3. CSS INJECTION
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lexend:wght@700&display=swap');

.stMainBlockContainer {
    padding-top: 1rem !important;
    padding-bottom: 1rem !important;
}

.stApp {
    background-image: url("https://raw.githubusercontent.com/jjpatz/college-fest-leaderboard/main/Background.png");
    background-size: cover;
    background-position: center;
    background-attachment: scroll;
}

html, body, [class*="css"] {
    font-family: 'Cinzel', sans-serif;
    color: white;
}

[data-testid="stVerticalBlock"] > div:has(div[data-testid="stPlotlyChart"]) {
    background: rgba(0, 0, 0, 0.4);
    backdrop-filter: blur(15px);
    border-radius: 20px;
    padding: 20px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.logo-container {
    display: flex;
    justify-content: center;
    padding-top: 0px;
    margin-bottom: -10px;
}

h1 { 
    color: white !important; 
    text-shadow: 2px 2px 8px #000000; 
    text-align: center;
    margin-top: 0px !important;
    padding-top: -10px !important;
}
</style>
""", unsafe_allow_html=True)

# LOGO
logo_url = "https://raw.githubusercontent.com/jjpatz/college-fest-leaderboard/main/logo.png"
st.markdown(f'<div class="logo-container"><img src="{logo_url}" width="600"></div>', unsafe_allow_html=True)

# 4. PLOTLY CHART
# We create the figure with the scores as the primary text
fig = px.bar(
    df, x="ORGANIZATION", y=df.columns[1], 
    color=df.columns[1], color_continuous_scale="Greens",
    text=df.columns[1] # Scores on top
)

# ADDING NAMES INSIDE THE BARS
custom_greens = ["#D1FAE5", "#10B981", "#065F46"] 

fig = px.bar(
    df, x="ORGANIZATION", y=df.columns[1], 
    color=df.columns[1], 
    color_continuous_scale=custom_greens, # Applies gradient based on score
    text=df.columns[1]
)

fig.update_traces(
    # Format for the score (outside)
    texttemplate='<b>%{text}</b>', 
    textposition="outside",
    
    # Rounded corners
    marker=dict(line=dict(width=0), cornerradius=15),
    
    # Hover info
    hovertemplate="<b>%Organization {x}</b><br>Points: <b>%{y}</b><extra></extra>",
    
    # This adds the Organization Name INSIDE the bar at the base
    insidetextanchor="start", 
    insidetextfont=dict(size=20, color="white")
)

# Customizing the layout to hide X-axis and place names inside
for i, row in df.iterrows():
    fig.add_annotation(
        x=row["ORGANIZATION"],
        y=0, # Base of the bar
        text=f"<b>{row['ORGANIZATION']}</b>",
        showarrow=False,
        ay=0,
        yshift=20, # Move it slightly up from the bottom
        font=dict(color="white", size=20),
        textangle=0 # Vertically placed for better fit in narrow bars
    )

fig.update_layout(
    xaxis={'categoryorder':'total descending', 'visible': False}, # Hide the messy bottom labels
    coloraxis_showscale=False,
    yaxis_visible=False,
    paper_bgcolor='rgba(0,0,0,0)', 
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family="Lexend", color="white"),
    margin=dict(t=50, b=20, l=25, r=25),
    bargap=0.05 
)

with st.container():
    st.plotly_chart(fig, use_container_width=True)