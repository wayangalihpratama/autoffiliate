import unittest
import os
import yaml


class TestInitialization(unittest.TestCase):
    def test_main_exists(self):
        """Check if main.py exists"""
        self.assertTrue(os.path.exists("main.py"))

    def test_niche_config_loading(self):
        """Verify that we can load the fashion niche config"""
        config_path = "config/niches/fashion.yaml"
        self.assertTrue(os.path.exists(config_path))
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        self.assertEqual(config["niche_id"], "fashion_pilot")


if __name__ == "__main__":
    unittest.main()
