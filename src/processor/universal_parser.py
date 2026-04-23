import os
import glob
import logging
import pandas as pd


logger = logging.getLogger(__name__)


class UniversalProcessor:
    def __init__(self, input_dir="data/input"):
        self.input_dir = input_dir

    def get_pending_files(self):
        """
        Returns a list of CSV/Excel files in the input directory.
        """
        extensions = ["*.csv", "*.xlsx", "*.xls"]
        files = []
        for ext in extensions:
            files.extend(glob.glob(os.path.join(self.input_dir, ext)))
        return files

    def parse_file(self, file_path):
        """
        Parses a product export file and returns product objects.
        Supports Kalodata, TikTok Creative Center, and manual files.
        """
        logger.info(f"Parsing file: {file_path}")
        try:
            if file_path.endswith(".csv"):
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)

            products = []
            # Flexible column mapping for different sources
            column_variations = {
                "title": [
                    "Product Name",
                    "Product Title",
                    "Product",
                    "Title",
                    "Name",
                ],
                "price": ["Price", "Sale Price", "Amount"],
                "commission": ["Commission Rate", "Commission", "Ref Fee"],
                "sales_30d": [
                    "Item Sold",
                    "Sold",
                    "Sales",
                    "Popularity",
                    "Performance",
                ],
                "image_urls": [
                    "Cover",
                    "Image URL",
                    "Main Image",
                    "Thumbnail",
                ],
                "source_url": ["Product URL", "URL", "Link", "Source"],
            }

            for _, row in df.iterrows():
                p = {}
                for internal_key, variations in column_variations.items():
                    # Find the first matching column in the dataframe
                    matched_col = None
                    for var in variations:
                        found = next(
                            (
                                c
                                for c in df.columns
                                if c.lower() == var.lower()
                            ),
                            None,
                        )
                        if found:
                            matched_col = found
                            break

                    if matched_col:
                        p[internal_key] = str(row[matched_col])
                    else:
                        p[internal_key] = "N/A"

                if p.get("source_url") == "N/A":
                    p["source_url"] = f"local://{os.path.basename(file_path)}"

                products.append(p)

            logger.info(
                f"Successfully parsed {len(products)} products from {file_path}"
            )
            return products

        except Exception as e:
            logger.error(f"Failed to parse {file_path}: {e}")
            return []

    def get_all_products(self, limit=None):
        """
        Processes all files in data/input.
        """
        files = self.get_pending_files()
        all_products = []
        for f in files:
            products = self.parse_file(f)
            all_products.extend(products)
            if limit and len(all_products) >= limit:
                break

        return all_products[:limit] if limit else all_products
