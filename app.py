import pandas as pd
import streamlit as st
import plotly.express as px


# إعداد الصفحة
st.set_page_config(
    page_title="Fleet Dashboard",
    page_icon="🚚",
    layout="wide"
)


# قراءة ملف Excel
file_path = "جدول بيانات بدون عنوان.xlsx"

df = pd.read_excel(file_path)


# تنظيف الأعمدة
df.columns = (
    df.columns
    .astype(str)
    .str.strip()
)


# تنظيف البيانات
df = df.dropna(how="all")


# عنوان الصفحة
st.title("🚚 Fleet Management Dashboard")
st.markdown("---")


# ======================
# Sidebar Filters
# ======================

st.sidebar.header("🔎 Filters")


# فلتر المنطقة
if "area" in df.columns:

    areas = df["area"].dropna().unique()

    selected_area = st.sidebar.multiselect(
        "Select Area",
        areas,
        default=areas
    )

    df = df[df["area"].isin(selected_area)]


# فلتر نوع السيارة
if "vehicle type" in df.columns:

    types = df["vehicle type"].dropna().unique()

    selected_type = st.sidebar.multiselect(
        "Vehicle Type",
        types,
        default=types
    )

    df = df[df["vehicle type"].isin(selected_type)]



# ======================
# KPI Cards
# ======================

col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "🚗 Total Vehicles",
        df["platenumber"].nunique()
        if "platenumber" in df.columns
        else len(df)
    )


with col2:
    st.metric(
        "🛣 Total KM",
        f"{df['km system'].sum():,.0f}"
        if "km system" in df.columns
        else "N/A"
    )


with col3:
    st.metric(
        "⛽ Total Fuel",
        f"{df['liters'].sum():,.0f} L"
        if "liters" in df.columns
        else "N/A"
    )


with col4:
    st.metric(
        "📊 Average KM/L",
        round(df["km/liter"].mean(),2)
        if "km/liter" in df.columns
        else "N/A"
    )



st.markdown("---")


# ======================
# Charts
# ======================


col1, col2 = st.columns(2)


# Fuel Consumption
if "vehicle type" in df.columns and "liters" in df.columns:

    fuel_chart = (
        df.groupby("vehicle type")["liters"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        fuel_chart,
        x="vehicle type",
        y="liters",
        title="⛽ Fuel Consumption By Vehicle Type"
    )

    col1.plotly_chart(
        fig,
        use_container_width=True
    )



# KM By Area
if "area" in df.columns and "km system" in df.columns:

    km_chart = (
        df.groupby("area")["km system"]
        .sum()
        .reset_index()
    )


    fig2 = px.pie(
        km_chart,
        names="area",
        values="km system",
        title="🗺 KM Distribution By Area"
    )


    col2.plotly_chart(
        fig2,
        use_container_width=True
    )



# ======================
# Top Vehicles
# ======================

st.subheader("🔥 Top 10 Vehicles By Fuel Consumption")


if "platenumber" in df.columns and "liters" in df.columns:

    top_vehicle = (
        df.groupby("platenumber")["liters"]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(10)
        .reset_index()
    )


    fig3 = px.bar(
        top_vehicle,
        x="platenumber",
        y="liters",
        title="Highest Fuel Consuming Vehicles"
    )


    st.plotly_chart(
        fig3,
        use_container_width=True
    )



# ======================
# Data Table
# ======================

st.subheader("📋 Fleet Data")

st.dataframe(
    df,
    use_container_width=True
)
