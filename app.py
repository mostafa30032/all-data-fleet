import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from io import BytesIO


# ==========================
# PAGE CONFIG
# ==========================

st.set_page_config(
    page_title="Fleet License Dashboard",
    page_icon="🚚",
    layout="wide"
)


# ==========================
# TITLE
# ==========================

st.title("🚚 Fleet License & Vehicle Dashboard")
st.markdown(
    "Automatic analysis for vehicle licenses, expiry dates and renewals"
)


# ==========================
# GOOGLE SHEET LINK
# ==========================

sheet_url = st.text_input(
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ41VbxaO4yjj852WgbOJZNQYBMaYOXVniixapXiZOEK9gGl3a4RVGX8pRDhatDZ5XT7baMj3bIwF-1/pub?gid=0&single=true&output=csv"
)


if sheet_url:


    try:

        sheet_id = sheet_url.split("/d/")[1].split("/")[0]

        csv_url = (
            f"https://docs.google.com/spreadsheets/d/"
            f"{sheet_id}/export?format=csv"
        )


        df = pd.read_csv(csv_url)


    except Exception as e:

        st.error(
            "Cannot read sheet. Check link permission."
        )

        st.stop()



    # ==========================
    # CLEAN COLUMNS
    # ==========================

    df.columns = (
        df.columns
        .str.strip()
    )


    # Convert date

    df["licence Expiry Date"] = pd.to_datetime(
        df["licence Expiry Date"],
        errors="coerce"
    )


    today = pd.Timestamp.today()



    # ==========================
    # LICENSE ANALYSIS
    # ==========================

    df["Days Remaining"] = (
        df["licence Expiry Date"] - today
    ).dt.days



    def license_status(x):

        if pd.isna(x):
            return "No Date"

        elif x < 0:
            return "Expired"

        elif x <= 30:
            return "Renew This Month"

        elif x <= 60:
            return "Next Month"

        else:
            return "Active"



    df["License Analysis"] = (
        df["Days Remaining"]
        .apply(license_status)
    )



    # ==========================
    # KPI
    # ==========================

    total = len(df)

    expired = len(
        df[
            df["License Analysis"]
            =="Expired"
        ]
    )


    renew = len(
        df[
            df["License Analysis"]
            =="Renew This Month"
        ]
    )


    active = len(
        df[
            df["License Analysis"]
            =="Active"
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
        renew
    )


    c4.metric(
        "Active License",
        active
    )



    st.divider()



    # ==========================
    # FILTERS
    # ==========================


    col1,col2,col3 = st.columns(3)


    with col1:

        area = st.multiselect(
            "Area",
            df["Area"]
            .dropna()
            .unique()
        )


    with col2:

        vehicle = st.multiselect(
            "Vehicle Type",
            df["Vehicle Type"]
            .dropna()
            .unique()
        )


    with col3:

        branch = st.multiselect(
            "Branch",
            df["Branch"]
            .dropna()
            .unique()
        )



    filtered = df.copy()



    if area:
        filtered = filtered[
            filtered["Area"]
            .isin(area)
        ]


    if vehicle:
        filtered = filtered[
            filtered["Vehicle Type"]
            .isin(vehicle)
        ]


    if branch:
        filtered = filtered[
            filtered["Branch"]
            .isin(branch)
        ]



    # ==========================
    # CHART STATUS
    # ==========================

    st.subheader(
        "License Status"
    )


    status = (
        filtered[
            "License Analysis"
        ]
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
        hole=.4
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )



    # ==========================
    # AREA ANALYSIS
    # ==========================

    st.subheader(
        "Vehicles By Area"
    )


    area_data = (
        filtered
        .groupby("Area")
        ["Vehicle ID"]
        .count()
        .reset_index()
    )


    area_data.columns=[
        "Area",
        "Vehicles"
    ]



    fig2 = px.bar(
        area_data,
        x="Area",
        y="Vehicles"
    )


    st.plotly_chart(
        fig2,
        use_container_width=True
    )



    # ==========================
    # VEHICLE TYPE
    # ==========================


    st.subheader(
        "Vehicle Type Analysis"
    )


    type_data = (
        filtered
        .groupby(
            [
                "Vehicle Type",
                "License Analysis"
            ]
        )
        ["Vehicle ID"]
        .count()
        .reset_index()
    )


    fig3 = px.bar(
        type_data,
        x="Vehicle Type",
        y="Vehicle ID",
        color="License Analysis",
        barmode="group"
    )


    st.plotly_chart(
        fig3,
        use_container_width=True
    )



    # ==========================
    # ALERT TABLE
    # ==========================


    st.subheader(
        "⚠️ License Renewal Alerts"
    )


    alerts = filtered[
        filtered["License Analysis"]
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
                "licence Expiry Date",
                "Days Remaining",
                "License Analysis"
            ]
        ],
        use_container_width=True
    )



    # ==========================
    # DOWNLOAD EXCEL
    # ==========================


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
        "Download Renewal Report",
        output.getvalue(),
        "License_Report.xlsx"
    )
