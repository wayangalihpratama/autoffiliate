import os
import requests
import logging
from typing import List

logger = logging.getLogger(__name__)


class ImageDownloader:
    def __init__(self, base_dir: str = "data/temp/images"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    def download_images(self, urls: List[str], product_id: int) -> List[str]:
        """
        Downloads images for a specific product and returns local paths.
        """
        local_paths = []
        product_dir = os.path.join(self.base_dir, str(product_id))
        os.makedirs(product_dir, exist_ok=True)

        for i, url in enumerate(urls):
            if not url:
                continue
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    ext = url.split(".")[-1].split("?")[0] or "jpg"
                    path = os.path.join(product_dir, f"img_{i}.{ext}")
                    with open(path, "wb") as f:
                        f.write(response.content)
                    local_paths.append(path)
                    logger.info(f"Downloaded image: {path}")
            except Exception as e:
                logger.error(f"Failed to download image {url}: {e}")

        return local_paths
