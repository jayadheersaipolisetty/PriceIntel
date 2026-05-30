'''FINAL CATEGORY INTELLIGENCE WHITH ROUTE WHICH SHOWS ON WEBSITE'''

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from database import load_dominance_data, load_stock_transition_data
from insights2 import render_insights

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Category Intelligence Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom layout stylings for clean dashboard representation
st.markdown("""
<style>
    div[data-testid="metric-container"] {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    .metric-title {
        font-size: 14px;
        font-weight: 600;
        color: #495057;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

# =====================================================
# DATA INGESTION LAYER
# =====================================================
df = load_dominance_data()
transition_df = load_stock_transition_data()

transition_df["today_date"] = pd.to_datetime(transition_df["today_date"])

if df.empty:
    st.error("No data fetched from database. Please check your connection configuration.")
    st.stop()

# Prepare dates and ensure strict chronological order
df["scrape_day"] = pd.to_datetime(df["scrape_day"])
df = df.sort_values("scrape_day")

# =====================================================
# DATA STANDARDIZATION LAYER
# =====================================================
if "amazon_stock" in df.columns:
    df["amazon_stock"] = df["amazon_stock"].fillna("Out Of Stock").astype(str).str.strip().str.title()
if "flipkart_stock" in df.columns:
    df["flipkart_stock"] = df["flipkart_stock"].fillna("Out Of Stock").astype(str).str.strip().str.title()

# Identify comparative price frames dynamically
amazon_price_cols = [c for c in df.columns if 'amazon' in c.lower() and 'price' in c.lower()]
flipkart_price_cols = [c for c in df.columns if 'flipkart' in c.lower() and 'price' in c.lower()]

# Define strict Price-vs-Price calculation
if amazon_price_cols and flipkart_price_cols:
    a_p_col = amazon_price_cols[0]
    f_p_col = flipkart_price_cols[0]
    
    df[a_p_col] = pd.to_numeric(df[a_p_col], errors='coerce')
    df[f_p_col] = pd.to_numeric(df[f_p_col], errors='coerce')
    
    def calculate_pure_price_winner(row):
        ap = row[a_p_col]
        fp = row[f_p_col]
        
        ap_valid = pd.notna(ap) and ap > 0
        fp_valid = pd.notna(fp) and fp > 0
        
        if ap_valid and fp_valid:
            if ap < fp:
                return "Amazon"
            elif fp < ap:
                return "Flipkart"
            else:
                return "Tie"
        elif ap_valid and not fp_valid:
            return "Amazon"
        elif fp_valid and not ap_valid:
            return "Flipkart"
        else:
            return "Tie"

    df["price_winner"] = df.apply(calculate_pure_price_winner, axis=1)
else:
    df["price_winner"] = df["winner"].fillna("Tie") if "winner" in df.columns else "Tie"

# Define Stock Availability Integrated Winner
if "amazon_stock" in df.columns and "flipkart_stock" in df.columns:
    def calculate_stock_integrated_winner(row):
        pw = row["price_winner"]
        a_stock = str(row["amazon_stock"]).strip().lower()
        f_stock = str(row["flipkart_stock"]).strip().lower()
        
        # Override structural winner rules based on inventory flags
        if "in stock" in a_stock and "out of stock" in f_stock:
            return "Amazon"
        elif "in stock" in f_stock and "out of stock" in a_stock:
            return "Flipkart"
        elif "out of stock" in a_stock and "out of stock" in f_stock:
            return "Tie"
        return pw

    df["integrated_winner"] = df.apply(calculate_stock_integrated_winner, axis=1)
else:
    df["integrated_winner"] = df["price_winner"]

# Map current logic parameters back to target winner column
df["winner"] = df["price_winner"]

# =====================================================
# UI ROUTING FRAMES
# =====================================================
st.title("📊 Category Intelligence Dashboard")
st.markdown("Monitor price competitiveness, catalog overlapping, stock status, and market advantages across major platforms.")

# =====================================================
# TOP FILTERS
# =====================================================
col1, col2 = st.columns(2)

with col1:
    selected_category = st.selectbox(
        "Select Category Target",
        sorted(df["category"].dropna().unique())
    )
    transition_df = transition_df[transition_df["category"] == selected_category].copy()

with col2:
    selected_range = st.selectbox(
        "Analyze Date Range",
        ["today", "Last 7 Days", "Last 30 Days", "overall"]
    )

# =====================================================
# FILTER LOGIC SPLICERS
# =====================================================
filtered_df = df[df["category"] == selected_category].copy()

if filtered_df.empty:
    st.warning("No data found for the selected category.")
    st.stop()

latest_date = filtered_df["scrape_day"].max()

if selected_range == "today":
    filtered_df = filtered_df[filtered_df["scrape_day"] == latest_date]
elif selected_range == "Last 7 Days":
    filtered_df = filtered_df[filtered_df["scrape_day"] >= latest_date - pd.Timedelta(days=6)]
elif selected_range == "Last 30 Days":
    filtered_df = filtered_df[filtered_df["scrape_day"] >= latest_date - pd.Timedelta(days=29)]

total_products = len(filtered_df)

# =====================================================
# METRIC CORE COMPUTATIONS
# =====================================================
amazon_wins = filtered_df["price_winner"].eq("Amazon").sum()
flipkart_wins = filtered_df["price_winner"].eq("Flipkart").sum()
tie_count = filtered_df["price_winner"].eq("Tie").sum()

amazon_instock = filtered_df["amazon_stock"].eq("In Stock").sum()
flipkart_instock = filtered_df["flipkart_stock"].eq("In Stock").sum()

amazon_oos = filtered_df["amazon_stock"].eq("Out Of Stock").sum()
flipkart_oos = filtered_df["flipkart_stock"].eq("Out Of Stock").sum()

amazon_exclusive_oos = len(filtered_df[
    (filtered_df["amazon_stock"].str.lower() == "out of stock") & 
    (filtered_df["flipkart_stock"].str.lower() == "in stock")
])

flipkart_exclusive_oos = len(filtered_df[
    (filtered_df["flipkart_stock"].str.lower() == "out of stock") & 
    (filtered_df["amazon_stock"].str.lower() == "in stock")
])

# =====================================================
# KPI UI RENDERING GRID
# =====================================================
st.divider()
st.subheader("Key Performance Indicators (KPIs)")

kpi_cols = st.columns(6)

with kpi_cols[0]:
    st.markdown('<div class="metric-title">🏷️ Cheaper Price</div>', unsafe_allow_html=True)
    st.write(f"Amazon wins: **{amazon_wins}**")
    st.write(f"Flipkart wins: **{flipkart_wins}**")
    st.caption(f"Ties: {tie_count} (Pure Price Only)")

with kpi_cols[1]:
    st.markdown('<div class="metric-title">🟢 In Stock Items</div>', unsafe_allow_html=True)
    st.write(f"Amazon: **{amazon_instock}**")
    st.write(f"Flipkart: **{flipkart_instock}**")
    st.caption(f"Availability tracking")

with kpi_cols[2]:
    st.markdown('<div class="metric-title">🔴 Out Of Stock (OOS)</div>', unsafe_allow_html=True)
    st.write(f"Amazon: **{amazon_oos}**")
    st.write(f"Flipkart: **{flipkart_oos}**")
    st.caption("Lower is better")

with kpi_cols[3]:
    st.markdown('<div class="metric-title">❌ Amazon OOS Deficit</div>', unsafe_allow_html=True)
    st.subheader(amazon_exclusive_oos)
    st.caption("OOS on Amazon, but In Stock on Flipkart")

with kpi_cols[4]:
    st.markdown('<div class="metric-title">❌ Flipkart OOS Deficit</div>', unsafe_allow_html=True)
    st.subheader(flipkart_exclusive_oos)
    st.caption("OOS on Flipkart, but In Stock on Amazon")

with kpi_cols[5]:
    st.markdown('<div class="metric-title">📦 Products Recorded</div>', unsafe_allow_html=True)
    st.subheader(total_products)
    st.caption(f"Cumulative tracking instances")

st.divider()

# =====================================================
# SIDE-BY-SIDE VISUAL LAYOUT
# =====================================================
left_trend_col, right_trend_col = st.columns(2)

# =====================================================
# TREND 1: PRICE DOMINANCE METRICS OVER TIME
# =====================================================
with left_trend_col:
    st.subheader("📈 Price Dominance Trend")
    
    t1_filters_col1, t1_filters_col2 = st.columns(2)
    
    with t1_filters_col1:
        trend1_filter1 = st.selectbox(
            "Stock Logic Integration",
            ["Price Only", "Stock Availability Included"],
            key="t1_logic"
        )
        
    with t1_filters_col2:
        trend1_platform = st.selectbox(
            "Platform Perspective",
            ["Both", "Amazon", "Flipkart"],
            key="t1_platform"
        )
        
    trend_df = filtered_df.copy()
    winner_col = "integrated_winner" if trend1_filter1 == "Stock Availability Included" else "price_winner"
        
    trend_df["scrape_day_str"] = trend_df["scrape_day"].dt.strftime("%Y-%m-%d")
    
    amazon_trend = trend_df.groupby("scrape_day_str")[winner_col].apply(lambda x: (x == "Amazon").sum()).reset_index(name="Amazon")
    flipkart_trend = trend_df.groupby("scrape_day_str")[winner_col].apply(lambda x: (x == "Flipkart").sum()).reset_index(name="Flipkart")
    tie_trend = trend_df.groupby("scrape_day_str")[winner_col].apply(lambda x: (x == "Tie").sum()).reset_index(name="Tie")
    
    trend_data = amazon_trend.merge(flipkart_trend, on="scrape_day_str", how="outer").merge(tie_trend, on="scrape_day_str", how="outer").fillna(0)
    
    fig1 = go.Figure()
    
    if trend1_platform in ["Both", "Amazon"]:
        fig1.add_trace(go.Scatter(x=trend_data["scrape_day_str"], y=trend_data["Amazon"], mode="lines+markers", name="Amazon", line=dict(color="#FF9900", width=3)))
        
    if trend1_platform in ["Both", "Flipkart"]:
        fig1.add_trace(go.Scatter(x=trend_data["scrape_day_str"], y=trend_data["Flipkart"], mode="lines+markers", name="Flipkart", line=dict(color="#2874F0", width=3)))
        
    if trend1_platform == "Both":
        fig1.add_trace(go.Scatter(x=trend_data["scrape_day_str"], y=trend_data["Tie"], mode="lines+markers", name="Tie", line=dict(color="#FFD700", width=3)))
        
    fig1.update_layout(
        title=f"Who Has the Advantage Over Time? ({trend1_filter1})",
        hovermode="x unified",
        xaxis_title="Date",
        yaxis_title="Winning Products",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(gridcolor="#f1f3f5"),
        xaxis=dict(type="category")
    )
    st.plotly_chart(fig1, use_container_width=True)

# =====================================================
# TREND 2: PLATFORM STOCK STATUS TIMESERIES
# =====================================================
with right_trend_col:
    st.subheader("🔄 Stock Availability Trend")
    
    t2_filters_col1, t2_filters_col2 = st.columns(2)
    
    with t2_filters_col1:
        trend2_platform = st.selectbox(
            "Target Platform Analysis",
            ["Both", "Amazon", "Flipkart"],
            key="t2_platform"
        )
        
    with t2_filters_col2:
        trend2_status = st.selectbox(
            "Stock Filter Metric",
            ["In Stock", "Out Of Stock"]
        )
        
    filtered_df["scrape_day_str"] = filtered_df["scrape_day"].dt.strftime("%Y-%m-%d")
    
    stock_trend = filtered_df.groupby("scrape_day_str").agg(
        Amazon_In_Stock=("amazon_stock", lambda s: s.fillna("").eq("In Stock").sum()),
        Amazon_Out_of_Stock=("amazon_stock", lambda s: s.fillna("").eq("Out Of Stock").sum()),
        Flipkart_In_Stock=("flipkart_stock", lambda s: s.fillna("").eq("In Stock").sum()),
        Flipkart_Out_of_Stock=("flipkart_stock", lambda s: s.fillna("").eq("Out Of Stock").sum())
    ).reset_index()
    
    if not stock_trend.empty:
        fig2 = go.Figure()
        
        if trend2_platform in ["Both", "Amazon"]:
            if trend2_status == "In Stock":
                fig2.add_trace(go.Scatter(x=stock_trend["scrape_day_str"], y=stock_trend["Amazon_In_Stock"], mode='lines+markers', name='Amazon (In Stock)', line=dict(color='#FF9900', width=2)))
            elif trend2_status == "Out Of Stock":
                fig2.add_trace(go.Scatter(x=stock_trend["scrape_day_str"], y=stock_trend["Amazon_Out_of_Stock"], mode='lines+markers', name='Amazon (Out of Stock)', line=dict(color='#E47911', width=1, dash='dash')))
                
        if trend2_platform in ["Both", "Flipkart"]:
            if trend2_status == "In Stock":
                fig2.add_trace(go.Scatter(x=stock_trend["scrape_day_str"], y=stock_trend["Flipkart_In_Stock"], mode='lines+markers', name='Flipkart (In Stock)', line=dict(color='#2874F0', width=2)))
            elif trend2_status == "Out Of Stock":
                fig2.add_trace(go.Scatter(x=stock_trend["scrape_day_str"], y=stock_trend["Flipkart_Out_of_Stock"], mode='lines+markers', name='Flipkart (Out of Stock)', line=dict(color='#1A4A99', width=1, dash='dash')))
                
        fig2.update_layout(
            title=f"Platform Inventory Trends: {trend2_platform} ({trend2_status})",
            xaxis_title="Date",
            yaxis_title="Product Catalog Count",
            hovermode="x unified",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(gridcolor="#f1f3f5"),
            xaxis=dict(type="category", categoryorder="category ascending")
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Insufficient longitudinal data to plot Stock Availability Trends.")

st.divider()

# =====================================================
# ANALYTICS INSIGHT GENERATOR LAYER
# =====================================================
render_insights(tie_count, filtered_df, transition_df)

# =====================================================
# DATA EXPORT GRID (RAW AUDIT PREVIEW)
# =====================================================
with st.expander("🔍 Inspect Processed Matchup Data"):
    st.dataframe(filtered_df, use_container_width=True)
