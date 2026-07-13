import gspread
from google.oauth2.service_account import Credentials
import pandas as pd


# رابط الشيت ثابت
sheet_url = "https://docs.google.com/spreadsheets/d/1o3_NF6_BRJ-UpD7GBH9eqs6Uf0JivV7P78xEZNyiPwo/edit?gid=0#gid=0"


# Google API
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]


import streamlit as st

creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope
)
)


client = gspread.authorize(creds)


sheet = client.open_by_url(sheet_url)

worksheet = sheet.sheet1


data = worksheet.get_all_records()


df = pd.DataFrame(data)


# تنظيف أسماء الأعمدة
df.columns = (
    df.columns
    .astype(str)
    .str.strip()
)
