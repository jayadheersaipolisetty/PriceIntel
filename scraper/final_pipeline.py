"""
PriceIntel - Main Data Pipeline

Purpose:
Automate ecommerce product data collection,
historical price tracking, stock monitoring,
and marketplace intelligence generation.

Components:
- Google Sheets Product Catalog
- Amazon Scraper
- Flipkart Scraper
- MySQL Storage
- Analytics Engine

Part of:
PriceIntel - Ecommerce Marketplace Intelligence &
Product Analytics Platform
"""
import re
import time
from datetime import date
import pandas as pd
import mysql.connector

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# GOOGLE SHEET CSV URL
sheet_url = "##your google sheet url"

# MYSQL CONNECTION
conn = mysql.connector.connect(
    host="## your host name",
    user="## your user name",
    password="## your password",
    database="## your database"
)
cursor = conn.cursor()

# READ GOOGLE SHEET
products = pd.read_csv(sheet_url)

# CHROME OPTIONS
options = Options()
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# OPEN CHROME
driver = webdriver.Chrome(options=options)
driver.execute_cdp_cmd(
    "Page.addScriptToEvaluateOnNewDocument",
    {
        "source": """
        Object.defineProperty(
            navigator,
            'webdriver',
            {get: () => undefined}
        )
        """
    }
)

# AMAZON SCRAPER
def scrape_amazon(url):
    driver.get(url)
    try:
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(5)
    except:
        return None, "NOT IN STOCK"

    page_html = driver.page_source.lower()

    if "captcha" in page_html or "enter the characters you see below" in page_html:
        return None, "BLOCKED"

    main_panel = None
    panel_xpaths = [
        "//div[@id='centerCol']",
        "//div[@id='buyBoxSmartbox']",
        "//div[@id='apex_desktop']"
    ]

    for xpath in panel_xpaths:
        try:
            main_panel = driver.find_element(By.XPATH, xpath)
            break
        except:
            continue

    raw_price_string = ""

    if main_panel:
        amazon_price_xpaths = [
            ".//span[@class='a-price-whole']",
            ".//div[@id='corePriceDisplay_desktop_feature_div']//span[@class='a-offscreen']",
            ".//span[contains(@class, 'a-size-large') and contains(@class, 'a-color-price')]"
        ]

        for xpath in amazon_price_xpaths:
            try:
                element = main_panel.find_element(By.XPATH, xpath)
                text = element.text.strip()

                if not text:
                    text = element.get_attribute("textContent").strip()

                if text and any(char.isdigit() for char in text):
                    raw_price_string = text
                    break
            except:
                continue

        if not raw_price_string:
            try:
                elements = main_panel.find_elements(By.XPATH, ".//*[contains(text(), '₹')]")
                for el in elements:
                    txt = el.text.strip() or el.get_attribute("textContent").strip()
                    if txt and len(txt) < 15 and any(char.isdigit() for char in txt) and "save" not in txt.lower():
                        raw_price_string = txt
                        break
            except:
                pass

    if raw_price_string:
        main_price_segment = raw_price_string.split('.')[0]
        clean_price = re.sub(r'[^0-9]', '', main_price_segment)
        if clean_price and int(clean_price) > 0:
            return float(clean_price), "IN STOCK"

    return None, "NOT IN STOCK"


# FLIPKART SCRAPER (Using your exact working original logic)
def scrape_flipkart(url):
    driver.get(url)
    
    try:
        # Give layout structure a few seconds to assemble
        WebDriverWait(driver, 12).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(4) 
    except Exception:
        return None, "NOT IN STOCK"

    page_text = driver.page_source.lower()

    # YOUR ORIGINAL STRUCTURAL INVENTORY EVALUATION
    if ("notify me" in page_text or "sold out" in page_text) and "add to cart" not in page_text:
        return None, "NOT IN STOCK"
        
    else:
        # YOUR ORIGINAL SELLING PRICE XPATHS
        price_xpaths = [
            "//div[contains(@class, 'hl05eU')]//div[contains(text(), '₹')]",
            "//div[contains(@class, 'Nx9u78')]",
            "//div[contains(@class,'Nx9bqj')]",
            "//div[contains(@class,'CxhGGd')]",
            "//div[contains(@font, 'default-fk-font-m') and contains(text(), '₹')]",
            "//div[starts-with(text(), '₹') and not(contains(., 'off')) and not(contains(., 'save'))]"
        ]
        
        raw_price_block = ""
        for xpath in price_xpaths:
            try:
                element = driver.find_element(By.XPATH, xpath)
                text = element.text.strip()
                if text:
                    raw_price_block = text
                    break
            except Exception:
                continue

        # YOUR ORIGINAL ISOLATE ACTIVE VALUE LOGIC
        if raw_price_block:
            prices_found = re.findall(r'₹\s*([0-9,]+)', raw_price_block)
            if prices_found:
                final_price = prices_found[0].replace(',', '')
                return float(final_price), "IN STOCK"
        else:
            # YOUR ORIGINAL FALLBACK
            try:
                fallback_text = driver.find_element(By.XPATH, "//*[starts-with(text(), '₹')]").text
                final_price = re.sub(r'[^0-9]', '', fallback_text.split()[0])
                if final_price:
                    return float(final_price), "IN STOCK"
            except:
                pass

    return None, "NOT IN STOCK"


# MAIN LOOP
for index, row in products.iterrows():
    product_name = row['Product']
    category = row['Category']
    platform = row['Platform']
    url = row['URL']

    print(f"\nOpening: {platform} for {product_name}")

    try:
        if platform.lower() == "amazon":
            price, stock_status = scrape_amazon(url)
        elif platform.lower() == "flipkart":
            price, stock_status = scrape_flipkart(url)
        else:
            continue

        print(f"Result -> {product_name} | {stock_status} | {price}")

        # INSERT INTO SQL
        insert_query = """
        INSERT INTO product_prices (
            scrape_date,
            product_name,
            category,
            platform,
            price,
            stock_status,
            url
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        values = (
            date.today(),
            product_name,
            category,
            platform,
            price,
            stock_status,
            url
        )

        cursor.execute(insert_query, values)
        conn.commit()
        
        # Micro sleep to keep browser engine cool between runs
        time.sleep(4)

    except Exception as e:
        print(f"ERROR ON PRODUCT {product_name}: {e}")

# CLOSE EVERYTHING
driver.quit()
conn.close()

print("\nALL PRODUCTS SCRAPED SUCCESSFULLY")
