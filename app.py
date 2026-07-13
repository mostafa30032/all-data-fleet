import streamlit as st
import pandas as pd
import plotly.express as px
import gspread

from google.oauth2.service_account import Credentials
from io import BytesIO


# ==============================
# PAGE SETTINGS
# ==============================

st.set_page_config(
    page_title="Fleet License Dashboard",
    page_icon="🚚",
    layout="wide"
)


st.title("🚚 Fleet License & Renewal Dashboard")


# ==============================
# GOOGLE SHEET CONNECTION
# ==============================

sheet_url = st.text_input(
    "https://docs.google.com/spreadsheets/d/1o3_NF6_BRJ-UpD7GBH9eqs6Uf0JivV7P78xEZNyiPwo/edit?gid=0#gid=0"
)


if sheet_url:


    try:

        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]


        creds = Credentials.from_service_account_file(
            "credentials.json",
            scopes=scope
        )


        client = gspread.authorize(creds)


        sheet = client.open_by_url(sheet_url)

        worksheet = sheet.sheet1


        data = worksheet.get_all_records()


        df = pd.DataFrame(data)



    except Exception as e:

        st.error(e)
        st.stop()



    # ==============================
    # CLEAN DATA
    # ==============================

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )


    # تحويل التاريخ

    df["licence Expiry Date"] = pd.to_datetime(
        df["licence Expiry Date"],
        errors="coerce"
    )



    today = pd.Timestamp.today()



    df["Days Remaining"] = (
        df["licence Expiry Date"]
        - today
    ).dt.days



    # ==============================
    # LICENSE STATUS ANALYSIS
    # ==============================


    def status(days):

        if pd.isna(days):
            return "No Date"

        elif days < 0:
            return "Expired"

        elif days <= 30:
            return "Renew This Month"

        elif days <= 60:
            return "Next Month"

        else:
            return "Active"



    df["License Status Analysis"] = (
        df["Days Remaining"]
        .apply(status)
    )



    # ==============================
    # KPI
    # ==============================


    total = len(df)


    expired = len(
        df[
            df["License Status Analysis"]
            =="Expired"
        ]
    )


    renew_month = len(
        df[
            df["License Status Analysis"]
            =="Renew This Month"
        ]
    )


    upcoming = len(
        df[
            df["License Status Analysis"]
            =="Next Month"
        ]
    )



    c1,c2,c3,c4 = st.columns(4)


    c1.metric(
        "Total Vehicles",
        total
    )


    c2.metric(
        "Expired License",
        expired
    )


    c3.metric(
        "Renew This Month",
        renew_month
    )


    c4.metric(
        "Upcoming",
        upcoming
    )



    st.divider()



    # ==============================
    # FILTERS
    # ==============================


    col1,col2,col3 = st.columns(3)


    with col1:

        areas = st.multiselect(
            "Area",
            df["Area"].dropna().unique()
        )


    with col2:

        types = st.multiselect(
            "Vehicle Type",
            df["Vehicle Type"].dropna().unique()
        )


    with col3:

        branches = st.multiselect(
            "Branch",
            df["Branch"].dropna().unique()
        )



    result = df.copy()



    if areas:
        result = result[
            result["Area"].isin(areas)
        ]


    if types:
        result = result[
            result["Vehicle Type"].isin(types)
        ]


    if branches:
        result = result[
            result["Branch"].isin(branches)
        ]



    # ==============================
    # STATUS CHART
    # ==============================

    st.subheader(
        "License Status"
    )


    status_chart = (
        result["License Status Analysis"]
        .value_counts()
        .reset_index()
    )


    status_chart.columns=[
        "Status",
        "Count"
    ]


    fig = px.pie(
        status_chart,
        names="Status",
        values="Count",
        hole=0.4
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )



    # ==============================
    # AREA ANALYSIS
    # ==============================


    st.subheader(
        "Vehicles By Area"
    )


    area = (
        result
        .groupby("Area")
        ["Vehicle ID"]
        .count()
        .reset_index()
    )


    area.columns=[
        "Area",
        "Vehicles"
    ]



    fig2 = px.bar(
        area,
        x="Area",
        y="Vehicles"
    )


    st.plotly_chart(
        fig2,
        use_container_width=True
    )



    # ==============================
    # VEHICLE TYPE ANALYSIS
    # ==============================


    st.subheader(
        "Vehicle Type Renewal Analysis"
    )


    vehicle_analysis = (
        result
        .groupby(
            [
                "Vehicle Type",
                "License Status Analysis"
            ]
        )
        ["Vehicle ID"]
        .count()
        .reset_index()
    )


    fig3 = px.bar(
        vehicle_analysis,
        x="Vehicle Type",
        y="Vehicle ID",
        color="License Status Analysis",
        barmode="group"
    )


    st.plotly_chart(
        fig3,
        use_container_width=True
    )



    # ==============================
    # ALERT TABLE
    # ==============================


    st.subheader(
        "⚠️ Renewal Alerts"
    )


    alerts = result[
        result["License Status Analysis"]
        .isin(
            [
                "Expired",
                "Renew This Month",
                "Next Month"
            ]
        )
    ]


    st.dataframe(
        alerts[
            [
                "Vehicle ID",
                "Area",
                "Vehicle Type",
                "Branch",
                "licence Expiry Date",
                "Days Remaining",
                "License Status Analysis"
            ]
        ],
        use_container_width=True
    )



    # ==============================
    # EXPORT REPORT
    # ==============================


    output = BytesIO()


    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        alerts.to_excel(
            writer,
            index=False,
            sheet_name="Renewal Alerts"
        )


    st.download_button(
        "📥 Download Renewal Report",
        output.getvalue(),
        file_name="License_Renewal_Report.xlsx"
    )
