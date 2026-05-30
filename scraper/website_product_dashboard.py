'''ALL THE OTHER INFORMATION OF PRODUCT INTELLIGENCE DASHBOARD WHICH WILL BE SHOWN ON WEBSITE'''

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from insights import generate_insights

def render_product_dashboard(df, selected_category):

    # Category normalization filter
    filtered_df = df[df["category"] == selected_category].copy()
    filtered_df["scrape_date"] = pd.to_datetime(filtered_df["scrape_date"])

    # Product dropdown mapping
    products = sorted(filtered_df["product_name"].dropna().unique())
    selected_product = st.selectbox("Select Product", products)

    # Product slice allocation
    product_df = filtered_df[filtered_df["product_name"] == selected_product].copy()
    product_df = product_df.sort_values("scrape_date")

    if product_df.empty:
        st.warning("No data available for the selected product.")
        return

    latest_date = product_df["scrape_date"].max()

    # Temporal range controls
    selected_range = st.selectbox(
        "Select Range",
        ["Today", "Last 7 Days", "Last 30 Days", "Overall"]
    )

    # Range constraint slicing
    if selected_range == "Today":
        graph_df = product_df[product_df["scrape_date"] == latest_date].copy()
    elif selected_range == "Last 7 Days":
        graph_df = product_df[product_df["scrape_date"] >= latest_date - pd.Timedelta(days=7)].copy()
    elif selected_range == "Last 30 Days":
        graph_df = product_df[product_df["scrape_date"] >= latest_date - pd.Timedelta(days=30)].copy()
    else:
        graph_df = product_df.copy()

    if graph_df.empty:
        st.warning("No data available for the selected date range.")
        return

    # -------------------------
    # MARKETPLACE STRUCTURING
    # -------------------------
    amazon_graph_df = graph_df[graph_df["platform"].str.lower().str.strip() == "amazon"].copy()
    flipkart_graph_df = graph_df[graph_df["platform"].str.lower().str.strip() == "flipkart"].copy()

    # INITIAL BASE PRICING
    amazon_initial = amazon_graph_df["price"].iloc[0] if not amazon_graph_df.empty else 0
    flipkart_initial = flipkart_graph_df["price"].iloc[0] if not flipkart_graph_df.empty else 0

    # DELTA RUNTIME PRICING
    amazon_current = amazon_graph_df["price"].iloc[-1] if not amazon_graph_df.empty else 0
    flipkart_current = flipkart_graph_df["price"].iloc[-1] if not flipkart_graph_df.empty else 0

    # SCALED MOM PERCENTAGE SPREADS
    amazon_change = (((amazon_current - amazon_initial) / amazon_initial) * 100) if amazon_initial > 0 else 0
    flipkart_change = (((flipkart_current - flipkart_initial) / flipkart_initial) * 100) if flipkart_initial > 0 else 0

    # -------------------------
    # RUNTIME COMPETITIVENESS
    # -------------------------
    today_rows = product_df[product_df["scrape_date"] == latest_date]
    
    if not today_rows.empty:
        lowest_today_price = today_rows["price"].min()
        lowest_today_matches = today_rows[today_rows["price"] == lowest_today_price]
        lowest_today_platform = "Both" if len(lowest_today_matches["platform"].unique()) > 1 else lowest_today_matches["platform"].iloc[0]
        lowest_today_date = lowest_today_matches["scrape_date"].iloc[0]
    else:
        lowest_today_price, lowest_today_platform, lowest_today_date = 0, "N/A", latest_date

    # EXT EXTREMUMS ANALYTICS
    lowest_ever_row = graph_df.loc[graph_df["price"].idxmin()] if not graph_df.empty else None
    highest_ever_row = graph_df.loc[graph_df["price"].idxmax()] if not graph_df.empty else None

    # -------------------------
    # STRUCTURAL KPI LAYOUT
    # -------------------------
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        st.markdown('<b style="font-size:15px; color:#495057;">Initial Price</b>', unsafe_allow_html=True)
        st.markdown(f"Amazon: **₹{amazon_initial:,.0f}**<br>Flipkart: **₹{flipkart_initial:,.0f}**", unsafe_allow_html=True)

    with col2:
        st.markdown('<b style="font-size:15px; color:#495057;">Current Price</b>', unsafe_allow_html=True)
        st.markdown(f"Amazon: **₹{amazon_current:,.0f}**<br>Flipkart: **₹{flipkart_current:,.0f}**", unsafe_allow_html=True)

    with col3:
        st.markdown('<b style="font-size:15px; color:#495057;">Price Change %</b>', unsafe_allow_html=True)
        st.markdown(f"Amazon: **{amazon_change:+.2f}%**<br>Flipkart: **{flipkart_change:+.2f}%**", unsafe_allow_html=True)

    with col4:
        st.markdown('<b style="font-size:15px; color:#495057;">Lowest Today</b>', unsafe_allow_html=True)
        st.markdown(f"**₹{lowest_today_price:,.0f}**<br><span style='color:gray; font-size:12px;'>{lowest_today_platform}<br>{lowest_today_date.strftime('%d-%b-%Y')}</span>", unsafe_allow_html=True)

    with col5:
        st.markdown('<b style="font-size:15px; color:#495057;">Lowest Ever</b>', unsafe_allow_html=True)
        if lowest_ever_row is not None:
            st.markdown(f"**₹{lowest_ever_row['price']:,.0f}**<br><span style='color:gray; font-size:12px;'>{lowest_ever_row['platform']}<br>{lowest_ever_row['scrape_date'].strftime('%d-%b-%Y')}</span>", unsafe_allow_html=True)
        else:
            st.markdown("**N/A**")

    with col6:
        st.markdown('<b style="font-size:15px; color:#495057;">Highest Ever</b>', unsafe_allow_html=True)
        if highest_ever_row is not None:
            st.markdown(f"**₹{highest_ever_row['price']:,.0f}**<br><span style='color:gray; font-size:12px;'>{highest_ever_row['platform']}<br>{highest_ever_row['scrape_date'].strftime('%d-%b-%Y')}</span>", unsafe_allow_html=True)
        else:
            st.markdown("**N/A**")

    st.divider()

    # -------------------------
    # TIME SERIES GRAPH BUFFER
    # -------------------------
    chart_prep_df = graph_df.copy()
    chart_prep_df["platform"] = chart_prep_df["platform"].str.lower().str.strip()

    chart_df = chart_prep_df.pivot_table(
        index="scrape_date",
        columns="platform",
        values="price",
        aggfunc="first"
    )

    fig = go.Figure()

    if "amazon" in chart_df.columns:
        fig.add_trace(
            go.Scatter(
                x=chart_df.index,
                y=chart_df["amazon"],
                mode="lines+markers",
                name="Amazon",
                line=dict(color="#FF9900", width=3)
            )
        )

    if "flipkart" in chart_df.columns:
        fig.add_trace(
            go.Scatter(
                x=chart_df.index,
                y=chart_df["flipkart"],
                mode="lines+markers",
                name="Flipkart",
                line=dict(color="#2874F0", width=3)
            )
        )

    fig.update_layout(
        height=450,
        margin=dict(l=40, r=20, t=20, b=40),
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis_title="Date",
        yaxis_title="Price (₹)",
        hovermode="x unified",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    fig.update_xaxes(showgrid=True, gridcolor="#f1f3f5")
    fig.update_yaxes(showgrid=True, gridcolor="#f1f3f5")

    # -------------------------
    # DOWNSTREAM INSIGHT PROCESSING
    # -------------------------
    (
        insight_1,
        insight_2,
        insight_3,
        insight_4,
        threshold_text
    ) = generate_insights(
        graph_df,
        selected_range,
        selected_category
    )

    # -------------------------
    # MATRIX UI ALIGNMENT GRID
    # -------------------------
    graph_col, insight_col = st.columns([3, 1])

    with graph_col:
        st.subheader("Price Trend Analysis")
        st.plotly_chart(fig, use_container_width=True)

    with insight_col:
        st.subheader("Insights")
        if insight_1: st.info(insight_1)
        if insight_2: st.info(insight_2)
        if insight_3: st.info(insight_3)
        if insight_4: st.info(insight_4)
        if threshold_text: st.caption(threshold_text)
