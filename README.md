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
SQL Views Layer
            ↓
Analytics Engine
            ↓
 ┌──────────────────────────┐
 │      Excel Layer         │
 │ Product Dashboard        │
 │ Category Dashboard       │
 └──────────────────────────┘
            ↓
 ┌──────────────────────────┐
 │    Streamlit Web App     │
 │ Home Page               │
 │ Product Intelligence    │
 │ Category Intelligence   │
 └──────────────────────────┘
            ↓
KPIs • Trends • Insights
```

## Tech Stack

* Python
* Selenium
* MySQL
* SQL Views
* Pandas
* Plotly
* Streamlit
* Google Sheets
* Excel
* ThreadPoolExecutor (Experimental Parallel Pipeline)
* GitHub


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
- fully functioning app and website available to everyone

---

## Repository Structure

```text
PriceIntel
│
├── scraper
│   ├── amazon_scraper.py
│   ├── flipkart_scraper.py
│   ├── final_pipeline.py
│   └── parallel_pipeline_experimental.py
│   ├── website_home.py
│   ├── website_databases.py
│   ├── website_product_dashboard.py
│   ├── website_product_intelligence_route.py
│   ├── website_full_category_intelligence_dashboard.py
│   ├── website_insights_product_intelligence_dashboard.py
│   └── website_insights_category_intelligence_dashboard.py
│
├── screenshots
│   ├── architecture.png
│   ├── home.png
│   ├── product_intelligence_dashboard.png
│   ├── category_intelligence_dashboard.png
│   ├── product_intelligence_website.png
│   └── category_intelligence_website.png
│
│
└── README.md
```

## Streamlit Web Application

In addition to the Excel-based analytics layer, PriceIntel includes a fully interactive Streamlit web application that provides a browser-based interface for marketplace intelligence and decision support.

### Home Page

The Home Page serves as the central navigation hub, providing access to the Product Intelligence and Category Intelligence modules.

<img width="1920" height="1079" alt="home page" src="<img width="1920" height="1078" alt="home png" src="https://github.com/user-attachments/assets/45408106-853e-4496-be49-39b68e6a3ac9" />
" />

---

### Product Intelligence Web Dashboard

The Product Intelligence web dashboard enables detailed product-level analysis through interactive visualizations and filters.

Features include:

* Product-level KPI tracking
* Initial Price vs Current Price comparison
* Lowest and Highest Price monitoring
* Product trend analysis
* Category-based filtering
* Dynamic threshold-based insight generation
* Interactive visualizations
* Historical intelligence views (Today, Last 7 Days, Last 30 Days, Overall)

<img width="1920" height="1079" alt="product intelligence website" src="<img width="1920" height="1078" alt="product intelligence website" src="https://github.com/user-attachments/assets/5c734e6a-60be-4dca-a142-d41c62e1d323" />
" />

---

### Category Intelligence Web Dashboard

The Category Intelligence web dashboard provides category-level competitive intelligence and marketplace monitoring.

Features include:

* Category dominance analysis
* Stock availability intelligence
* Marketplace competition tracking
* Automated insight generation
* Historical category performance analysis
* Category-based filtering
* Dynamic KPI generation
* Interactive drill-down capabilities

<img width="1920" height="1079" alt="category intelligence website" src="<img width="1920" height="1078" alt="category intelligence website" src="https://github.com/user-attachments/assets/181f4fe9-a31a-48eb-91d4-1f5b779f1b21" />
" />

---

### Web Analytics Layer

The Streamlit application consumes data directly from the analytics layer and SQL views, enabling dynamic intelligence generation through:

* Product Intelligence Engine
* Category Intelligence Engine
* KPI Engine
* Trend Analysis Engine
* Stock Transition Intelligence
* Competitive Marketplace Analytics
* Automated Insight Generation

This creates a complete analytics workflow from data collection to business intelligence delivery through both Excel dashboards and a web-based analytics platform.


## Security

Sensitive credentials, database passwords, and private configuration values have been removed from this repository.

---

## Author

Jayadheer Sai Polisetty

BBA Business Analytics | Product Analytics & Product Management Enthusiast
