import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Fleet Management System",
    page_icon="🚗",
    layout="wide"
)

# ==========================
# Google Sheet URL
# ==========================

GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ41VbxaO4yjj852WgbOJZNQYBMaYOXVniixapXiZOEK9gGl3a4RVGX8pRDhatDZ5XT7baMj3bIwF-1/pubhtml"

# ==========================
# Load Data
# ==========================

@st.cache_data(ttl=300)
def load_data():

    df = pd.read_csv(GOOGLE_SHEET_URL)

    df.columns = df.columns.str.strip()

    return df


try:
    df = load_data()

except Exception as e:
    st.error("Unable to connect to Google Sheet")
    st.error(e)
    st.stop()

# ==========================
# Dashboard
# ==========================

st.title("🚗 Fleet Management Dashboard")

st.success("Connected Successfully")

st.write(df)

st.write("Total Vehicles :", len(df))
