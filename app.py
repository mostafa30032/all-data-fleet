import pandas as pd
import streamlit as st


# إعداد الصفحة
st.set_page_config(
    page_title="Fleet Dashboard",
    page_icon="🚚",
    layout="wide"
)


# عنوان الداشبورد
st.title("🚚 Fleet Management Dashboard")


# اسم ملف Excel الموجود مع app.py
file_path = "جدول بيانات بدون عنوان.xlsx"


# قراءة ملف Excel
try:
    df = pd.read_excel(file_path)

except FileNotFoundError:
    st.error("❌ ملف Excel غير موجود. ارفع الملف بجانب app.py في GitHub")
    st.stop()


# تنظيف أسماء الأعمدة
df.columns = (
    df.columns
    .astype(str)
    .str.strip()
)


# حذف الصفوف الفارغة
df = df.dropna(how="all")


# إحصائيات بسيطة
total_records = len(df)
total_columns = len(df.columns)


col1, col2 = st.columns(2)

with col1:
    st.metric(
        "إجمالي السجلات",
        total_records
    )

with col2:
    st.metric(
        "عدد الأعمدة",
        total_columns
    )


# عرض البيانات
st.subheader("📊 بيانات الأسطول")

st.dataframe(
    df,
    use_container_width=True
)
