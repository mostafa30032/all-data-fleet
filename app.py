import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime


# ======================
# Page Setup
# ======================

st.set_page_config(
    page_title="Fleet Licensing Dashboard",
    page_icon="🚗",
    layout="wide"
)


# ======================
# Read Excel
# ======================

file_path = ""D:\USERS\01041878\Downloads\جدول بيانات بدون عنوان.xlsx""

try:
    df = pd.read_excel(file_path)

except:
    st.error("ملف التراخيص غير موجود بجانب app.py")
    st.stop()



# ======================
# Clean Columns
# ======================

df.columns = (
    df.columns
    .astype(str)
    .str.strip()
    .str.lower()
)



df = df.dropna(how="all")



# ======================
# Convert Dates
# ======================

date_columns = [
    "license expiry",
    "expiry date",
    "end date",
    "expiration"
]


for col in date_columns:
    if col in df.columns:
        df[col] = pd.to_datetime(
            df[col],
            errors="coerce"
        )



# ======================
# Title
# ======================

st.title("🚗 Fleet Licensing Management Dashboard")

st.markdown("---")



# ======================
# Sidebar
# ======================

st.sidebar.header("🔎 Filters")


if "area" in df.columns:

    areas = df["area"].dropna().unique()

    area = st.sidebar.multiselect(
        "Select Area",
        areas,
        default=areas
    )

    df = df[df["area"].isin(area)]



if "vehicle type" in df.columns:

    types = df["vehicle type"].dropna().unique()

    vehicle = st.sidebar.multiselect(
        "Vehicle Type",
        types,
        default=types
    )

    df = df[
        df["vehicle type"].isin(vehicle)
    ]



# ======================
# License Status
# ======================


today = pd.Timestamp.today()


expiry_col = None


for c in date_columns:
    if c in df.columns:
        expiry_col = c
        break



if expiry_col:


    df["License Status"] = df[expiry_col].apply(
        lambda x:
        "Expired"
        if x < today
        else
        "Expire Soon"
        if (x-today).days <= 30
        else
        "Valid"
    )



# ======================
# KPI Cards
# ======================

c1,c2,c3,c4 = st.columns(4)



with c1:

    st.metric(
        "🚗 Total Vehicles",
        df.shape[0]
    )


with c2:

    if expiry_col:

        valid = (
            df["License Status"]
            =="Valid"
        ).sum()

        st.metric(
            "✅ Valid Licenses",
            valid
        )


with c3:

    if expiry_col:

        expired = (
            df["License Status"]
            =="Expired"
        ).sum()

        st.metric(
            "🔴 Expired",
            expired
        )


with c4:

    if expiry_col:

        soon = (
            df["License Status"]
            =="Expire Soon"
        ).sum()

        st.metric(
            "🟡 Expire Soon",
            soon
        )



st.markdown("---")



# ======================
# Charts
# ======================


col1,col2 = st.columns(2)



# Status Chart

if "License Status" in df.columns:


    status = (
        df["License Status"]
        .value_counts()
        .reset_index()
    )


    status.columns=[
        "Status",
        "Count"
    ]


    fig = px.pie(
        status,
        names="Status",
        values="Count",
        title="License Status"
    )


    col1.plotly_chart(
        fig,
        use_container_width=True
    )



# Area Analysis

if "area" in df.columns:


    area_chart = (
        df.groupby("area")
        .size()
        .reset_index(
            name="Vehicles"
        )
    )


    fig2 = px.bar(
        area_chart,
        x="area",
        y="Vehicles",
        title="Vehicles By Area"
    )


    col2.plotly_chart(
        fig2,
        use_container_width=True
    )



# ======================
# Expiring Vehicles Table
# ======================

st.subheader(
    "⚠️ Vehicles Need Action"
)


if "License Status" in df.columns:


    action = df[
        df["License Status"]
        != "Valid"
    ]


    st.dataframe(
        action,
        use_container_width=True
    )



# ======================
# Full Data
# ======================

st.subheader(
    "📋 All Licensing Data"
)


st.dataframe(
    df,
    use_container_width=True
)
