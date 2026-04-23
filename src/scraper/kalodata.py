import os
import json
import logging
import re
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

logger = logging.getLogger(__name__)


class KalodataScraper:
    def __init__(self, session_path="sessions/kalodata.json"):
        self.session_path = session_path
        self.base_url = "https://www.kalodata.com"
        self.login_url = f"{self.base_url}/login"
        self.product_url = f"{self.base_url}/product"
        self.stealth = Stealth()

        # Load credentials from environment
        self.email = os.getenv("KALODATA_EMAIL")
        self.password = os.getenv("KALODATA_PASSWORD")

    def _init_browser(self, playwright, headless=True):
        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        browser = playwright.chromium.launch(headless=headless)

        context_args = {
            "user_agent": user_agent,
            "viewport": {"width": 1280, "height": 720},
        }

        if os.path.exists(self.session_path):
            logger.info(f"Loading session from {self.session_path}")
            context_args["storage_state"] = self.session_path

        context = browser.new_context(**context_args)
        page = context.new_page()
        self.stealth.apply_stealth_sync(page)
        return browser, context, page

    def _perform_login(self, page):
        """
        Performs automated login if credentials are provided.
        """
        if not self.email or not self.password:
            logger.warning(
                "No Kalodata credentials found in .env for auto-login."
            )
            return False

        try:
            logger.info(f"Attempting auto-login for {self.email}...")
            page.goto(self.login_url, wait_until="networkidle")

            # Fill login form (Ant Design selectors)
            page.wait_for_selector('input[type="text"]', timeout=10000)
            page.fill('input[type="text"]', self.email)
            page.fill('input[type="password"]', self.password)

            # Click Login button
            page.click('button[type="submit"]')

            # Wait for redirection to dashboard or product page
            page.wait_for_url("**/product**", timeout=20000)
            logger.info("Auto-login successful.")
            return True
        except Exception as e:
            logger.error(f"Auto-login failed: {e}")
            return False

    def scrape_trending_products(self, niche_config, limit=10):
        results = []
        with sync_playwright() as p:
            browser, context, page = self._init_browser(p)
            try:
                # Check if we need to login
                if not os.path.exists(self.session_path):
                    login_success = self._perform_login(page)
                    if login_success:
                        os.makedirs(
                            os.path.dirname(self.session_path), exist_ok=True
                        )
                        context.storage_state(path=self.session_path)

                logger.info(f"Navigating to {self.product_url}")
                page.goto(
                    self.product_url,
                    wait_until="domcontentloaded",
                    timeout=60000,
                )
                page.wait_for_timeout(5000)

                # Take debug screenshot
                os.makedirs("data/debug", exist_ok=True)
                page.screenshot(path="data/debug/kalodata_load.png")

                # Detect table
                logger.info("Waiting for product data...")
                page.wait_for_selector(".ant-table-row", timeout=20000)

                rows = page.query_selector_all(".ant-table-row")
                logger.info(f"Found {len(rows)} potential products.")

                for i, row in enumerate(rows):
                    if i >= limit:
                        break

                    try:
                        title_el = row.query_selector(".line-clamp-2")
                        if not title_el:
                            continue

                        title = title_el.inner_text().strip()
                        cells = row.query_selector_all("td")

                        price = "0"
                        sales = "0"
                        if len(cells) > 5:
                            # Price is usually in the 2nd cell, formatted
                            price_text = cells[1].inner_text()
                            price_match = re.search(r"Rp[\d.,]+", price_text)
                            price = (
                                price_match.group(0) if price_match else "Rp0"
                            )
                            sales = cells[5].inner_text().strip()

                        img_el = row.query_selector(".Component-Image")
                        img_url = ""
                        if img_el:
                            style = img_el.get_attribute("style") or ""
                            match = re.search(r'url\("?(.+?)"?\)', style)
                            if match:
                                img_url = match.group(1)

                        results.append(
                            {
                                "title": title,
                                "price": price,
                                "sales_30d": sales,
                                "image_urls": img_url,
                                "source_url": page.url,
                            }
                        )
                        logger.info(f"Scraped: {title} | {price} | {sales}")

                    except Exception as e:
                        logger.debug(f"Row {i} parse skip: {e}")

            except Exception as e:
                logger.error(f"Scraping failed: {e}")
                page.screenshot(path="data/debug/kalodata_error.png")
            finally:
                browser.close()

        return results
