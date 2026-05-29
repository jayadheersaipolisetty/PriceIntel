# PriceIntel

PriceIntel is an automated ecommerce intelligence platform designed to track product prices, stock availability, category dominance, and competitive marketplace behavior across multiple ecommerce platforms.

The platform combines automated web scraping, SQL-based historical storage, analytics generation, and dashboard-driven intelligence to support data-driven decision making.

## Ecommerce Marketplace Intelligence & Product Analytics Platform

---

## Problem Statement

Consumers, sellers, and businesses often lack visibility into historical pricing trends, stock changes, and competitive marketplace dynamics.

PriceIntel automates data collection and transforms raw marketplace data into actionable intelligence through analytics dashboards and automated insights.

---

## Key Features

- Automated product price tracking
- Historical price analysis
- Stock availability monitoring
- Product Intelligence Dashboard
- Category Intelligence Dashboard
- Category dominance analytics
- Competitive intelligence
- Automated insight generation
- Multi-platform marketplace comparison

---

## Architecture

```text
Google Sheets Product Catalog
            ↓
Amazon & Flipkart Scrapers
            ↓
MySQL Database
            ↓
Analytics Engine
            ↓
Product Intelligence Dashboard
            ↓
Category Intelligence Dashboard
```

## Tech Stack

- Python
- Selenium
- MySQL
- Google Sheets
- Excel
- ThreadPoolExecutor (Experimental Parallel Pipeline)

---

## Product Intelligence Dashboard

Tracks:

- Initial Price
- Current Price
- Price Change %
- Lowest Price
- Highest Price
- Product Trend Analysis
- Product-Level Insights (Today, Last 7 Days, Last 30 Days, Overall)
- Category Filter
- Dynamic Category Thresholds

<img width="1920" height="1079" alt="product intelligence dashboard" src="https://github.com/user-attachments/assets/2fc9ab24-bbca-4247-83c8-698beda56dd4" />


---

## Category Intelligence Dashboard

Tracks:

- Platform Dominance
- Stock Availability Trends
- Price Competition
- Category Performance
- Marketplace Insights (Today)
- Category-Based Insights (Today, Last 7 Days, Last 30 Days, Overall)
- Interactive hyperlinks for detailed product-level exploration

<img width="1920" height="1079" alt="category intelligence dashboard" src="https://github.com/user-attachments/assets/21852403-236b-439f-a874-46362bff1fb2" />


---

## Data Pipeline

1. Product catalog imported from Google Sheets
2. Automated scraping from Amazon and Flipkart
3. Historical data stored in MySQL
4. Analytics generated automatically
5. Dashboards updated with latest intelligence

---

## Experimental Features

An experimental parallel-processing pipeline has been developed to evaluate browser-level concurrency and reduce scraping time for larger product catalogs.

---

## Business Impact

PriceIntel transforms raw ecommerce marketplace data into actionable intelligence, enabling consumers, sellers, and businesses to make data-driven pricing, inventory, and competitive strategy decisions.

---

## Future Scope

- Expansion to additional ecommerce marketplaces
- Real-time analytics with minute-level updates
- Streamlit-based web application deployment
- Automated alerts and notifications
- Product matching engine for exact and similar products
- Whole-marketplace crawling and intelligence generation
- Location-aware inventory intelligence
- Seller intelligence and competitive benchmarking

---

## Repository Structure

```text
PriceIntel
│
├── dashboard
├── docs
├── scraper
│   ├── amazon_scraper.py
│   ├── flipkart_scraper.py
│   ├── final_pipeline.py
│   └── parallel_pipeline_experimental.py
└── README.md
```

## Security

Sensitive credentials, database passwords, and private configuration values have been removed from this repository.

---

## Author

Jayadheer Sai Polisetty

BBA Business Analytics | Product Analytics & Product Management Enthusiast
