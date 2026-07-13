import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Fleet Dashboard",
    page_icon="🚗",
    layout="wide"
)

URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ41VbxaO4yjj852WgbOJZNQYBMaYOXVniixapXiZOEK9gGl3a4RVGX8pRDhatDZ5XT7baMj3bIwF-1/pub?gid=0&single=true&output=csv"

@st.cache_data
def load_data():

    df = pd.read_csv(
        URL,
        engine="python",
        encoding="utf-8"
    )

    df.columns = df.columns.str.strip()

    return df


df = load_data()

st.title("🚗 Fleet Management Dashboard")

st.success("Google Sheet Connected Successfully")

st.dataframe(df, use_container_width=True)
