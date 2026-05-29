"""
PriceIntel - Experimental Parallel Processing Pipeline

Purpose:
Evaluate browser-level concurrency to reduce
scraping time for large product catalogs.

Approach:
- Separate browser instance per category
- Parallel execution using ThreadPoolExecutor
- Preserves original output ordering

Status:
Experimental prototype. Production pipeline
currently uses a single-browser architecture.
"""
import re
import time
import pandas as pd
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# =========================================
# GOOGLE SHEET CSV URL
# =========================================

sheet_url = "## enetr your google sheet url"

# =========================================
# READ GOOGLE SHEET
# =========================================

products = pd.read_csv(sheet_url)

# KEEP ORIGINAL ORDER
products['original_order'] = range(len(products))

print(f"TOTAL PRODUCTS: {len(products)}")

# =========================================
# CREATE CHROME DRIVER
# =========================================

def create_driver():

    options = Options()

    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")

    # DISABLE IMAGES
    prefs = {
        "profile.managed_default_content_settings.images": 2
    }

    options.add_experimental_option("prefs", prefs)

    options.add_experimental_option(
        "excludeSwitches",
        ["enable-automation"]
    )

    options.add_experimental_option(
        "useAutomationExtension",
        False
    )

    driver = webdriver.Chrome(options=options)

    driver.maximize_window()

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

    return driver

# =========================================
# AMAZON SCRAPER
# =========================================

def scrape_amazon(driver, url):

    driver.get(url)

    driver.implicitly_wait(5)

    time.sleep(2)

    try:

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//span[@class='a-price-whole']")
            )
        )

    except:

        return None, "OUT OF STOCK"

    page_html = driver.page_source.lower()

    if (
        "currently unavailable" in page_html
        or "out of stock" in page_html
    ):

        stock = "OUT OF STOCK"

    else:

        stock = "IN STOCK"

    raw_price_string = ""

    xpaths = [

        "//span[@class='a-price-whole']",

        "//span[@class='a-offscreen']"

    ]

    for xpath in xpaths:

        try:

            element = driver.find_element(By.XPATH, xpath)

            text = element.text.strip()

            if text:

                raw_price_string = text

                break

        except:

            continue

    if raw_price_string:

        prices_found = re.findall(r'[0-9,]+', raw_price_string)

        if prices_found:

            clean_price = prices_found[0].replace(',', '')

            return float(clean_price), stock

    return None, stock

# =========================================
# FLIPKART SCRAPER
# =========================================

def scrape_flipkart(driver, url):

    driver.get(url)

    driver.implicitly_wait(5)

    time.sleep(2)

    try:

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class,'Nx9u78')]")
            )
        )

    except:

        return None, "OUT OF STOCK"

    page_text = driver.page_source.lower()

    if (
        "notify me" in page_text
        or "sold out" in page_text
    ):

        stock = "OUT OF STOCK"

    else:

        stock = "IN STOCK"

    raw_price = ""

    xpaths = [

        "//div[contains(@class, 'Nx9u78')]",

        "//div[contains(text(), '₹')]"

    ]

    for xpath in xpaths:

        try:

            element = driver.find_element(By.XPATH, xpath)

            text = element.text.strip()

            if text:

                raw_price = text

                break

        except:

            continue

    if raw_price:

        prices_found = re.findall(r'[0-9,]+', raw_price)

        if prices_found:

            clean_price = prices_found[0].replace(',', '')

            return float(clean_price), stock

    return None, stock

# =========================================
# CATEGORY SCRAPER
# =========================================

def scrape_category(category_df):

    try:

        category_name = category_df['Category'].iloc[0]

        print(f"\nSTARTED CATEGORY: {category_name}")

        driver = create_driver()

        results = []

        for _, row in category_df.iterrows():

            product_name = row['Product']
            category = row['Category']
            platform = row['Platform']
            url = row['URL']
            order = row['original_order']

            print(f"Opening: {platform} | {product_name}")

            try:

                if platform.lower() == "amazon":

                    price, stock = scrape_amazon(driver, url)

                elif platform.lower() == "flipkart":

                    price, stock = scrape_flipkart(driver, url)

                else:

                    continue

                print(f"{product_name} | {stock} | {price}")

                results.append({

                    "original_order": order,

                    "scrape_date": date.today(),

                    "product_name": product_name,

                    "category": category,

                    "platform": platform,

                    "price": price,

                    "stock_status": stock,

                    "url": url

                })

            except Exception:

                print(f"ERROR ON PRODUCT: {product_name}")

                traceback.print_exc()

        driver.quit()

        print(f"RESULTS COUNT FOR {category_name}: {len(results)}")

        return results

    except Exception:

        print("CATEGORY THREAD FAILED")

        traceback.print_exc()

        return []

# =========================================
# SPLIT CATEGORIES
# =========================================

electronics = products[
    products['Category'].str.lower() == "electronics"
]

home_appliances = products[
    products['Category'].str.lower() == "home appliances"
]

accessories = products[
    products['Category'].str.lower() == "accessories"
]

print(f"Electronics: {len(electronics)}")
print(f"Home Appliances: {len(home_appliances)}")
print(f"Accessories: {len(accessories)}")

# =========================================
# PARALLEL EXECUTION
# =========================================

all_results = []

with ThreadPoolExecutor(max_workers=3) as executor:

    futures = [

        executor.submit(scrape_category, electronics),

        executor.submit(scrape_category, home_appliances),

        executor.submit(scrape_category, accessories)

    ]

    for future in as_completed(futures):

        result = future.result()

        all_results.extend(result)

# =========================================
# FINAL OUTPUT
# =========================================

final_df = pd.DataFrame(all_results)

if final_df.empty:

    print("\nNO RESULTS SCRAPED")

else:

    final_df = final_df.sort_values("original_order")

    final_df = final_df.drop(columns=["original_order"])

    print(final_df)

    final_df.to_csv("scraped_results.csv", index=False)

    print("\nSCRAPING COMPLETED")
