import pandas as pd

def generate_insights(
    graph_df,
    selected_range,
    selected_category
):
    # Dynamic thresholds based on product categories
    threshold_map = {
        "electronics": 3,
        "fashion": 8,
        "accessories": 10,
        "home appliances": 5,
        "toys": 10
    }

    threshold = threshold_map.get(
        selected_category.lower(),
        5
    )

    threshold_text = (
        f"(only considered when the price change is > "
        f"{threshold}% of initial price)"
    )

    # -------------------------
    # PLATFORM SLICING LAYERS
    # -------------------------
    amazon_df = graph_df[
        graph_df["platform"]
        .str.lower() == "amazon"
    ].copy()

    flipkart_df = graph_df[
        graph_df["platform"]
        .str.lower() == "flipkart"
    ].copy()

    # =========================
    # INSIGHT 1: STOCK STATUS
    # =========================
    def stock_message(df, platform_name):
        if len(df) == 0:
            return f"{platform_name}: No data"

        latest = df.iloc[-1]
        current_stock = str(latest["stock_status"]).upper().strip()

        if current_stock == "IN STOCK":
            return f"{platform_name} is currently in stock."

        # Compute consecutive Out-of-Stock instances
        reversed_df = (
            df.sort_values("scrape_date")
            .iloc[::-1]
        )

        count = 0
        for _, row in reversed_df.iterrows():
            row_stock = str(row["stock_status"]).upper().strip()
            if "NOT IN STOCK" in row_stock or "OUT OF STOCK" in row_stock:
                count += 1
            else:
                break

        return (
            f"{platform_name} has been out of stock "
            f"for {count} consecutive days."
        )

    insight_1 = (
        stock_message(amazon_df, "Amazon")
        + " "
        + stock_message(flipkart_df, "Flipkart")
    )

    # =========================
    # INSIGHT 2: PRICE GAP
    # =========================
    try:
        amazon_price = amazon_df.iloc[-1]["price"]
        flipkart_price = flipkart_df.iloc[-1]["price"]
        gap = abs(amazon_price - flipkart_price)

        if amazon_price < flipkart_price:
            insight_2 = f"Amazon is currently ₹{gap:,.0f} cheaper than Flipkart."
        elif flipkart_price < amazon_price:
            insight_2 = f"Flipkart is currently ₹{gap:,.0f} cheaper than Amazon."
        else:
            insight_2 = "Both platforms are currently priced equally."
    except Exception:
        insight_2 = "Price comparison unavailable."

    # =========================
    # INSIGHT 3: COMPETITIVENESS
    # =========================
    merged = pd.merge(
        amazon_df[["scrape_date", "price"]],
        flipkart_df[["scrape_date", "price"]],
        on="scrape_date",
        suffixes=("_amazon", "_flipkart")
    )

    if len(merged) == 0:
        insight_3 = "No comparable pricing data."
    else:
        amazon_wins = (merged["price_amazon"] < merged["price_flipkart"]).sum()
        flipkart_wins = (merged["price_flipkart"] < merged["price_amazon"]).sum()
        total_days = len(merged)

        if amazon_wins > flipkart_wins:
            pct = (amazon_wins / total_days) * 100
            insight_3 = f"Amazon offered lower prices on {amazon_wins} of {total_days} comparable days ({pct:.0f}%)."
        elif flipkart_wins > amazon_wins:
            pct = (flipkart_wins / total_days) * 100
            insight_3 = f"Flipkart offered lower prices on {flipkart_wins} of {total_days} comparable days ({pct:.0f}%)."
        else:
            insight_3 = "Both platforms were equally competitive."

    # =========================
    # INSIGHT 4: SIGNIFICANT CHANGES
    # =========================
    def price_change_summary(df, platform_name):
        if len(df) <= 1:
            return f"{platform_name}: Not enough data."

        initial_price = df["price"].iloc[0]
        threshold_value = initial_price * threshold / 100

        changes = df["price"].diff().abs() > threshold_value
        change_count = changes.sum()

        if change_count == 0:
            return f"{platform_name} pricing remained stable."

        last_change_date = df.loc[changes, "scrape_date"].max()
        return (
            f"{platform_name} has shown {change_count} significant "
            f"price changes, recent change on {last_change_date.strftime('%d-%b-%Y')}."
        )

    insight_4 = (
        price_change_summary(amazon_df, "Amazon")
        + " "
        + price_change_summary(flipkart_df, "Flipkart")
    )

    return (
        insight_1,
        insight_2,
        insight_3,
        insight_4,
        threshold_text
    )
