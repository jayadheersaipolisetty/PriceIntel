import pandas as pd
import mysql.connector
import os

# =====================================================
# DATABASE CONNECTION HELPER
# =====================================================
def get_db_connection():
    """
    Establishes a connection to the MySQL database.
    Using environment variables is a GitHub best practice.
    Fallback placeholders are provided for local development.
    """
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "your_database_user"),
        password=os.getenv("DB_PASSWORD", "your_database_password"),
        database=os.getenv("DB_NAME", "ecommerce_prices")
    )

# =====================================================
# PRODUCT PRICE TABLE
# =====================================================
def load_data():
    conn = get_db_connection()

    query = """
    SELECT *
    FROM product_prices
    """

    df = pd.read_sql(
        query,
        conn
    )

    conn.close()
    return df

# =====================================================
# DOMINANCE VIEW
# =====================================================
def load_dominance_data():
    conn = get_db_connection()

    query = """
    SELECT *
    FROM dominance_insights
    """

    df = pd.read_sql(
        query,
        conn
    )

    conn.close()
    return df

# =====================================================
# STOCK TRANSITION DATA
# =====================================================
def load_stock_transition_data():
    conn = get_db_connection()

    query = """
    SELECT *
    FROM stock_transition_insights
    """

    df = pd.read_sql(
        query,
        conn
    )

    conn.close()
    return df
