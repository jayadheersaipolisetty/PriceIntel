'''BACKGORUND WORK FOR INSIGHTS TO BE SHOWN ON THE WEBSITE'''

import streamlit as st
import pandas as pd

# =====================================================
# CATEGORY INSIGHTS RENDERING LAYER
# =====================================================

def render_insights(
    tie_count,
    filtered_df,
    transition_df
):

    # =================================================
    # INSIGHT 1: PRICING PARITY BREAKDOWN
    # =================================================
    insight_1 = (
        f"Amazon and Flipkart had a tie in "
        f"{tie_count} instances."
    )

    # =================================================
    # INSIGHT 2: INVENTORY STOCKOUT TRANSITIONS
    # =================================================
    amazon_oos = transition_df[
        transition_df["fresh_oos_amazon"].notna()
    ].copy()

    flipkart_oos = transition_df[
        transition_df["fresh_oos_flipkart"].notna()
    ].copy()

    amazon_oos_count = len(amazon_oos)
    flipkart_oos_count = len(flipkart_oos)

    insight_2 = (
        f"{amazon_oos_count} products from Amazon, "
        f"{flipkart_oos_count} products from Flipkart "
        f"freshly out of stock recorded today."
    )

    # =================================================
    # INSIGHT 3: INVENTORY RE-STOCK TRANSITIONS
    # =================================================
    amazon_instock = transition_df[
        transition_df["fresh_instock_amazon"].notna()
    ].copy()

    flipkart_instock = transition_df[
        transition_df["fresh_instock_flipkart"].notna()
    ].copy()

    amazon_instock_count = len(amazon_instock)
    flipkart_instock_count = len(flipkart_instock)

    insight_3 = (
        f"{amazon_instock_count} products from Amazon, "
        f"{flipkart_instock_count} products from Flipkart "
        f"freshly in stock recorded today."
    )

    # Placeholders reserved for custom downstream metrics
    insight_4 = ""
    insight_5 = ""

    # =================================================
    # UI DOM RENDERER
    # =================================================
    st.subheader("💡 Insights")

    # Clean styling context injections for expansion metrics
    st.markdown("""
    <style>
    .streamlit-expanderHeader {
        background-color: #dbeafe;
        border-radius: 10px;
        padding: 12px;
        color: #1e3a8a;
        font-size: 17px;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

    # =================================================
    # RENDER INSIGHT 1
    # =================================================
    with st.expander(insight_1, expanded=False):
        tie_products = filtered_df[
            filtered_df["winner"] == "Tie"
        ][["scrape_day", "product_name"]]

        if len(tie_products) > 0:
            st.dataframe(
                tie_products,
                use_container_width=True
            )
        else:
            st.info("No tied products found.")

    # =================================================
    # RENDER INSIGHT 2
    # =================================================
    with st.expander(insight_2, expanded=False):
        amazon_table = amazon_oos[["today_date", "product_name"]].copy()
        amazon_table["platform"] = "Amazon"

        flipkart_table = flipkart_oos[["today_date", "product_name"]].copy()
        flipkart_table["platform"] = "Flipkart"

        details_table = pd.concat(
            [amazon_table, flipkart_table],
            ignore_index=True
        )

        if len(details_table) > 0:
            st.dataframe(
                details_table.sort_values("today_date"),
                use_container_width=True
            )
        else:
            st.info("No freshly out of stock products found.")

    # =================================================
    # RENDER INSIGHT 3
    # =================================================
    with st.expander(insight_3, expanded=False):
        amazon_table = amazon_instock[["today_date", "product_name"]].copy()
        amazon_table["platform"] = "Amazon"

        flipkart_table = flipkart_instock[["today_date", "product_name"]].copy()
        flipkart_table["platform"] = "Flipkart"

        details_table = pd.concat(
            [amazon_table, flipkart_table],
            ignore_index
