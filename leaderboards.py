import streamlit as st
import pandas as pd

url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ1k4Liz4HvtBM6s8OaPex9E_8zmGTb_DLtlyShFifZ1XLSQ2e06XI3XQLefwH1xSIu0b-NWBaH3pcf/pub?output=csv"

df = pd.read_csv(url)

st.title("Fest Tally Dashboard")
st.bar_chart(df.set_index("ORGANIZATION"))
