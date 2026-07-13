import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="Fleet Management System",
    page_icon="🚗",
    layout="wide"
)

# Sidebar
with st.sidebar:
    selected = option_menu(
        "Fleet Management",
        [
            "Dashboard",
            "Vehicles",
            "GPS",
            "Fuel",
            "Licence",
            "Insurance",
            "Reports",
            "Settings"
        ],
        icons=[
            "speedometer2",
            "truck",
            "geo-alt",
            "fuel-pump",
            "file-earmark-text",
            "shield-check",
            "bar-chart",
            "gear"
        ],
        menu_icon="list",
        default_index=0,
    )

# Main Page
st.title("🚗 Fleet Management System")

st.markdown("---")

if selected == "Dashboard":
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Vehicles", "365")
    col2.metric("Active", "320")
    col3.metric("Expired Licence", "12")
    col4.metric("Insurance Expired", "5")

    st.write("")
    st.subheader("Dashboard")

    st.info("Fleet Dashboard will be here.")
