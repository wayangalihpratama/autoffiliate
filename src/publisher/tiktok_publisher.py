import os
import logging
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

logger = logging.getLogger(__name__)


class TikTokPublisher:
    def __init__(self, session_path="sessions/tiktok.json"):
        self.session_path = session_path
        self.upload_url = "https://www.tiktok.com/upload?lang=en"
        self.stealth = Stealth()

    def publish_video(
        self, video_path: str, caption: str, hashtags: list
    ) -> bool:
        """
        Publishes a video to TikTok via Playwright.
        """
        if not os.path.exists(video_path):
            logger.error(f"Video file {video_path} not found.")
            return False

        if not os.path.exists(self.session_path):
            logger.error(
                f"TikTok session file {self.session_path} not found. Manual login required first."
            )
            return False

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(storage_state=self.session_path)
            page = context.new_page()
            self.stealth.apply_stealth_sync(page)

            try:
                logger.info(f"Navigating to TikTok upload: {self.upload_url}")
                page.goto(self.upload_url, wait_until="networkidle")

                # Handle File Upload
                # TikTok's upload input is usually an iframe or a specific selector
                logger.info("Uploading video file...")
                # Note: This selector may change, using a common one for TikTok desktop upload
                file_input = page.wait_for_selector('input[type="file"]')
                file_input.set_input_files(video_path)

                # Wait for upload completion (check for progress bar or success indicator)
                # This is simplified for MVP
                page.wait_for_timeout(5000)

                # Enter Caption
                full_caption = f"{caption} {' '.join(hashtags)}"
                logger.info(f"Setting caption: {full_caption}")

                # TikTok's caption area is often a contenteditable div or a specific role
                caption_area = page.wait_for_selector('div[role="textbox"]')
                caption_area.fill(full_caption)

                # Click Post
                logger.info("Clicking Post button...")
                post_button = page.wait_for_selector('button:has-text("Post")')
                # post_button.click() # Commented out for safety during development

                logger.info("Video published successfully (simulated).")
                return True

            except Exception as e:
                logger.error(f"TikTok publishing failed: {e}")
                return False
            finally:
                browser.close()

        return False
