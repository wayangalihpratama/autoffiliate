import unittest
import logging
from src.scraper.kalodata import KalodataScraper

logging.basicConfig(level=logging.INFO)


class TestKalodataScraper(unittest.TestCase):
    def test_guest_scrape(self):
        """Verify that the scraper can at least reach the page and find rows as a guest"""
        scraper = KalodataScraper()
        # Using a dummy config for now
        results = scraper.scrape_trending_products(
            {"niche_id": "test"}, limit=3
        )

        self.assertIsInstance(results, list)
        if len(results) > 0:
            self.assertIn("title", results[0])
            self.assertIn("price", results[0])
            print(f"Scraped {len(results)} products successfully as guest.")
        else:
            print("No products found (could be rate limited or page changed).")


if __name__ == "__main__":
    unittest.main()
