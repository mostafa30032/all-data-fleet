import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Fleet Management Dashboard",
    layout="wide"
)


# Google Sheet Link
url = st.text_input(
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ41VbxaO4yjj852WgbOJZNQYBMaYOXVniixapXiZOEK9gGl3a4RVGX8pRDhatDZ5XT7baMj3bIwF-1/pub?gid=0&single=true&output=csv"
)


if url:

    sheet_id = url.split("/d/")[1].split("/")[0]

    csv_url = (
        f"https://docs.google.com/spreadsheets/d/"
        f"{sheet_id}/export?format=csv"
    )


    df = pd.read_csv(csv_url)


    st.success(
        f"Loaded {len(df)} Vehicles"
    )


    # KPIs

    col1,col2,col3,col4 = st.columns(4)


    col1.metric(
        "Total Vehicles",
        len(df)
    )


    col2.metric(
        "Branches",
        df["Branch"].nunique()
    )


    col3.metric(
        "Vehicle Types",
        df["Vehicle Type"].nunique()
    )


    col4.metric(
        "Companies",
        df["Company name"].nunique()
    )



    st.divider()


    # Vehicle by Branch

    st.subheader(
        "Vehicles By Branch"
    )

    branch = (
        df["Branch"]
        .value_counts()
        .reset_index()
    )

    branch.columns=[
        "Branch",
        "Count"
    ]


    fig = px.bar(
        branch,
        x="Branch",
        y="Count"
    )

    st.plotly_chart(fig)



    # Insurance Status

    st.subheader(
        "Insurance Status"
    )


    insurance = (
        df["InsuranceStatus"]
        .value_counts()
        .reset_index()
    )


    insurance.columns=[
        "Status",
        "Count"
    ]


    fig2 = px.pie(
        insurance,
        names="Status",
        values="Count"
    )


    st.plotly_chart(fig2)



    # Expiry Alerts

    st.subheader(
        "Expiry Alerts"
    )


    alerts=df[
        (df["InsuranceStatus"]!="Active")
        |
        (df["licence Status"]!="Active")
    ]


    st.dataframe(
        alerts,
        use_container_width=True
    )
