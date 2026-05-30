'''HOME PAGE FOR THE WEBSITE'''
'''CALLED ASS APP'''

import streamlit as st

st.set_page_config(
    page_title="PriceIntel",
    page_icon="📈",
    layout="wide"
)

st.title("📈 PriceIntel")
st.subheader("Ecommerce Marketplace Intelligence Platform")

st.markdown("""
Welcome to PriceIntel.

Use the navigation menu on the left to access:

- Product Intelligence Dashboard
- Category Intelligence Dashboard
""")
