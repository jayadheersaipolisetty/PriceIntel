import streamlit as st
from database import load_data
from product_dashboard import render_product_dashboard

# =====================================================
# PLATFORM PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="PriceIntel",
    layout="wide"
)

# =====================================================
# BANNER HEADER
# =====================================================
st.title("📈 PriceIntel")
st.subheader("Ecommerce Marketplace Intelligence Platform")

# =====================================================
# DATA INGESTION ENGINE
# =====================================================
df = load_data()

# =====================================================
# GLOBAL CATEGORY TAXONOMY FILTER
# =====================================================
selected_category = st.selectbox(
    "Select Category",
    sorted(df["category"].dropna().unique())
)

# =====================================================
# TARGET RUNTIME ROUTER
# =====================================================
render_product_dashboard(
    df,
    selected_category
)
