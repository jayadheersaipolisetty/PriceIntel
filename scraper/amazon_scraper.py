"""
PriceIntel - Amazon Scraper

Purpose:
Extract product availability and current selling price
from Amazon India product pages.

Part of:
PriceIntel - Ecommerce Marketplace Intelligence &
Product Analytics Platform
"""

import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Example:
# https://www.amazon.in/product-page
url = input("Enter Amazon Product URL: ").strip()

options = Options()
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

driver = webdriver.Chrome(options=options)

driver.execute_cdp_cmd(
    "Page.addScriptToEvaluateOnNewDocument",
    {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        })
        """
    }
)

try:
    driver.get(url)

    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    time.sleep(4)

    page_html = driver.page_source.lower()

    # Anti-bot Detection
    if (
        "enter the characters you see below" in page_html
        or "captcha" in page_html
    ):
        print("BLOCKED BY CAPTCHA (Amazon detected the script!)")

    else:

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
            except Exception:
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

                    text = (
                        element.text.strip()
                        or element.get_attribute("textContent").strip()
                    )

                    if text and any(char.isdigit() for char in text):
                        raw_price_string = text
                        break

                except Exception:
                    continue

            if not raw_price_string:
                try:
                    elements = main_panel.find_elements(
                        By.XPATH,
                        ".//*[contains(text(), '₹')]"
                    )

                    for el in elements:

                        txt = (
                            el.text.strip()
                            or el.get_attribute("textContent").strip()
                        )

                        if (
                            txt
                            and len(txt) < 15
                            and any(char.isdigit() for char in txt)
                            and "save" not in txt.lower()
                        ):
                            raw_price_string = txt
                            break

                except Exception:
                    pass

        if raw_price_string:

            main_price_segment = raw_price_string.split(".")[0]

            clean_price = re.sub(
                r"[^0-9]",
                "",
                main_price_segment
            )

            if clean_price and int(clean_price) > 0:
                print("IN STOCK")
                print(f"Price: ₹{clean_price}")
            else:
                print("NOT IN STOCK")

        else:
            print("NOT IN STOCK")

finally:
    driver.quit()
