import os
import json
import logging
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

logger = logging.getLogger(__name__)


class KalodataScraper:
    def __init__(self, session_path="sessions/kalodata.json"):
        self.session_path = session_path
        self.base_url = "https://www.kalodata.com"
        self.product_url = f"{self.base_url}/product"
        self.stealth = Stealth()

    def _init_browser(self, playwright, headless=True):
        browser = playwright.chromium.launch(headless=headless)

        # Load storage state if exists
        context_args = {}
        if os.path.exists(self.session_path):
            logger.info(f"Loading session from {self.session_path}")
            context_args["storage_state"] = self.session_path

        context = browser.new_context(**context_args)
        page = context.new_page()
        self.stealth.apply_stealth_sync(page)
        return browser, context, page

    def scrape_trending_products(self, niche_config, limit=10):
        """
        Scrapes trending products based on niche criteria.
        Note: If not logged in, data will be masked.
        """
        results = []
        with sync_playwright() as p:
            browser, context, page = self._init_browser(p)
            try:
                logger.info(f"Navigating to {self.product_url}")
                page.goto(
                    self.product_url,
                    wait_until="domcontentloaded",
                    timeout=60000,
                )

                # TODO: Apply filters based on niche_config (category, sales, etc.)
                # For MVP, we scrape the default list as a POC

                page.wait_for_selector("tr", timeout=10000)
                rows = page.query_selector_all("tr")[1:]  # Skip header

                for i, row in enumerate(rows):
                    if i >= limit:
                        break

                    try:
                        cells = row.query_selector_all("td")
                        if len(cells) < 6:
                            continue

                        # 2nd td contains Title and Price
                        info_cell = cells[1]
                        title = (
                            info_cell.query_selector("div")
                            .inner_text()
                            .strip()
                        )

                        # Price is often in the second div or a specific class
                        # Based on observation, it's below the title
                        price_div = info_cell.query_selector_all("div")[-1]
                        price = price_div.inner_text().strip()

                        # 6th td is Item Sold (Sales)
                        sales = cells[5].inner_text().strip()

                        # Image URL
                        img_tag = info_cell.query_selector("img")
                        img_url = (
                            img_tag.get_attribute("src") if img_tag else ""
                        )

                        results.append(
                            {
                                "title": title,
                                "price": price,
                                "sales_30d": sales,
                                "image_urls": img_url,
                                "source_url": page.url,  # Placeholder for actual product link
                            }
                        )
                        logger.info(
                            f"Found product: {title} | {price} | {sales}"
                        )

                    except Exception as e:
                        logger.error(f"Error parsing row {i}: {e}")

                # Save state after potential login
                # context.storage_state(path=self.session_path)

            finally:
                browser.close()

        return results
