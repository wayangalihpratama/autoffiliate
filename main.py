import os
import yaml
import logging
import json
from dotenv import load_dotenv
from src.database import Database
from src.processor.universal_parser import UniversalProcessor
from src.intelligence.gemini_engine import GeminiEngine
from src.editor.moviepy_editor import MoviePyEditor
from src.utils.downloader import ImageDownloader
from src.output.package_generator import PackageGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class AutoffiliateRunner:
    def __init__(self):
        load_dotenv()
        self.db = Database()
        self.processor = UniversalProcessor()
        self.intelligence = GeminiEngine()
        self.editor = MoviePyEditor()
        self.downloader = ImageDownloader()
        self.package_gen = PackageGenerator()
        self.niche_dir = "config/niches"

    def run(self):
        logger.info("Autoffiliate Semi-Auto engine starting...")

        if not os.path.exists(self.niche_dir):
            logger.error(f"Niche directory {self.niche_dir} not found.")
            return

        niches = [f for f in os.listdir(self.niche_dir) if f.endswith(".yaml")]
        logger.info(f"Found {len(niches)} niches: {niches}")

        for niche_file in niches:
            with open(os.path.join(self.niche_dir, niche_file), "r") as f:
                niche_config = yaml.safe_load(f)
                self.process_niche(niche_config)

    def process_niche(self, config):
        niche_id = config.get("niche_id")
        logger.info(f"Processing niche: {niche_id}")

        # Step 1: Process Kalodata Exports (Semi-Auto)
        products = self.processor.get_all_products(limit=10)

        if not products:
            logger.warning(
                f"No products found in data/input for niche {niche_id}"
            )
            return

        logger.info(f"Processing {len(products)} products for {niche_id}")

        # Step 2, 3 & 4: Intelligence, Editor & Package Generation
        for p in products:
            # Add product to DB (deduplication happens here)
            product_id = self.db.add_product(
                niche_id=niche_id,
                source_url=p.get("source_url", "local"),
                title=p["title"],
                price=p["price"],
                sales_30d=p.get("sales_30d", "0"),
                image_urls=p.get("image_urls", ""),
                raw_data=json.dumps(p),
            )

            if product_id:
                logger.info(
                    f"New product saved: {p['title']} (ID: {product_id})"
                )

                # Generate script via Gemini
                script_data = self.intelligence.generate_script(p, config)
                if script_data:
                    content_id = self.db.add_content(product_id, script_data)
                    logger.info(f"Script generated (ID: {content_id})")

                    # Download images (if URLs provided)
                    image_urls = p.get("image_urls", "")
                    if image_urls and image_urls != "nan":
                        image_urls = (
                            [image_urls]
                            if isinstance(image_urls, str)
                            else image_urls
                        )
                        image_paths = self.downloader.download_images(
                            image_urls, product_id
                        )
                    else:
                        logger.warning(
                            f"No image URLs for {p['title']}, skipping video generation."
                        )
                        continue

                    # Assemble Video
                    if image_paths:
                        video_name = f"prod_{product_id}_{niche_id}"
                        video_path = self.editor.assemble_video(
                            script_data, image_paths, video_name
                        )

                        if video_path:
                            self.db.update_content_video_path(
                                content_id, video_path
                            )
                            logger.info(f"Video produced: {video_path}")

                            # Prepare Package for Manual Posting
                            package_path = self.package_gen.prepare_package(
                                product_title=p["title"],
                                video_path=video_path,
                                script_data=script_data,
                                niche_id=niche_id,
                            )
                            if package_path:
                                logger.info(
                                    f"Package created for manual post: {package_path}"
                                )
            else:
                logger.debug(
                    f"Product already exists or failed to save: {p['title']}"
                )


if __name__ == "__main__":
    runner = AutoffiliateRunner()
    runner.run()
