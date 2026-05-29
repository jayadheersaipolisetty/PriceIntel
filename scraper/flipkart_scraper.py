"""
PriceIntel - Flipkart Scraper

Purpose:
Extract product availability and current selling price
from Flipkart product pages.

Part of:
PriceIntel - Ecommerce Marketplace Intelligence &
Product Analytics Platform
"""

import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Example:
# https://www.flipkart.com/product-page
url = input("Enter Flipkart Product URL: ").strip()

driver = webdriver.Chrome()

try:
    driver.get(url)

    WebDriverWait(driver, 12).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    time.sleep(3)

    page_text = driver.page_source.lower()

    # Inventory Evaluation
    if ("notify me" in page_text or "sold out" in page_text) and "add to cart" not in page_text:
        print("OUT OF STOCK")

    else:
        price_xpaths = [
            "//div[contains(@class, 'hl05eU')]//div[contains(text(), '₹')]",
            "//div[contains(@class, 'Nx9u78')]",
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

        if raw_price_block:

            prices_found = re.findall(
                r'₹\s*([0-9,]+)',
                raw_price_block
            )

            if prices_found:

                final_price = prices_found[0].replace(',', '')

                print("IN STOCK")
                print(f"Price: ₹{final_price}")

            else:
                print(
                    "OUT OF STOCK (No valid currency digits inside structure)"
                )

        else:

            try:
                fallback_text = driver.find_element(
                    By.XPATH,
                    "//*[starts-with(text(), '₹')]"
                ).text

                final_price = re.sub(
                    r'[^0-9]',
                    '',
                    fallback_text.split()[0]
                )

                print("IN STOCK")
                print(f"Price: ₹{final_price}")

            except Exception:
                print(
                    "OUT OF STOCK (Could not map price coordinate layouts)"
                )

finally:
    driver.quit()
