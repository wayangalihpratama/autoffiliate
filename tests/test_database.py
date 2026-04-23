import unittest
import os
from src.database import Database


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.test_db = "data/test_database.sqlite"
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
        self.db = Database(self.test_db)

    def tearDown(self):
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_add_product(self):
        product_id = self.db.add_product(
            niche_id="fashion",
            source_url="https://example.com/p1",
            title="Test Product",
            price="10.00",
            sales_30d=100,
            image_urls="http://img.com/1",
            raw_data="{}",
        )
        self.assertIsNotNone(product_id)

        # Test duplicate
        dup_id = self.db.add_product(
            niche_id="fashion",
            source_url="https://example.com/p1",
            title="Test Product",
            price="10.00",
            sales_30d=100,
            image_urls="http://img.com/1",
            raw_data="{}",
        )
        self.assertIsNone(dup_id)


if __name__ == "__main__":
    unittest.main()
