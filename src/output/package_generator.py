import os
import shutil
import logging
from datetime import datetime


logger = logging.getLogger(__name__)


class PackageGenerator:
    def __init__(self, output_base="data/output"):
        self.output_base = output_base

    def prepare_package(
        self, product_title, video_path, script_data, niche_id
    ):
        """
        Creates a folder for the product and copies video/metadata.
        """
        date_str = datetime.now().strftime("%Y-%m-%d")
        # Sanitize product title for folder name
        safe_title = "".join(
            [c if c.isalnum() else "_" for c in product_title[:30]]
        )
        package_dir = os.path.join(
            self.output_base, date_str, f"{niche_id}_{safe_title}"
        )

        try:
            os.makedirs(package_dir, exist_ok=True)

            # Copy video
            target_video = os.path.join(package_dir, "video.mp4")
            shutil.copy2(video_path, target_video)

            # Create caption file
            caption_path = os.path.join(package_dir, "caption.txt")
            with open(caption_path, "w") as f:
                f.write(
                    f"PROMPT/SCRIPT:\n{script_data.get('tts_text', '')}\n\n"
                )
                f.write(f"CAPTION:\n{script_data.get('caption', '')}\n\n")
                f.write(f"HASHTAGS:\n{script_data.get('hashtags', '')}\n")

            logger.info(f"Package ready at: {package_dir}")
            return package_dir
        except Exception as e:
            logger.error(f"Failed to prepare package: {e}")
            return None
