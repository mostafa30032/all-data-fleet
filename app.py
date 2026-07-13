import pandas as pd
import streamlit as st


# عنوان الصفحة
st.set_page_config(
    page_title="Fleet Dashboard",
    page_icon="🚚",
    layout="wide"
)


# قراءة ملف Excel
file_path = "D:/USERS/01041878/Downloads/جدول بيانات بدون عنوان.xlsx"
    df = pd.read_excel(file_path)

except FileNotFoundError:
    st.error("لم يتم العثور على ملف Excel. تأكد أن الملف موجود بجانب app.py")
    st.stop()


# تنظيف أسماء الأعمدة
df.columns = (
    df.columns
    .astype(str)
    .str.strip()
)


# تنظيف البيانات
df = df.dropna(how="all")

# عدد السيارات
total_rows = len(df)


# عرض Dashboard بسيط
st.title("🚚 Fleet Management Dashboard")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "إجمالي السجلات",
        total_rows
    )

with col2:
    st.metric(
        "عدد الأعمدة",
        len(df.columns)
    )


# عرض البيانات
st.subheader("بيانات الأسطول")

st.dataframe(
    df,
    use_container_width=True
)
