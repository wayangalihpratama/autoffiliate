import unittest
from unittest.mock import MagicMock, patch
from src.publisher.tiktok_publisher import TikTokPublisher


class TestTikTokPublisher(unittest.TestCase):
    @patch("os.path.exists")
    @patch("src.publisher.tiktok_publisher.Stealth")
    @patch("src.publisher.tiktok_publisher.sync_playwright")
    def test_publish_video_mock(
        self, mock_playwright, mock_stealth, mock_exists
    ):
        # Mock file checks
        mock_exists.return_value = True

        # Mock browser and page
        mock_browser = MagicMock()
        mock_context = MagicMock()
        mock_page = MagicMock()

        # Setup the context manager 'with sync_playwright() as p:'
        p = mock_playwright.return_value.__enter__.return_value
        p.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page

        # Mock selectors to return immediately
        mock_page.wait_for_selector.return_value = MagicMock()

        publisher = TikTokPublisher(session_path="fake_session.json")

        # Test basic publish call
        result = publisher.publish_video(
            video_path="fake.mp4",
            caption="Check this out!",
            hashtags=["#trending", "#fashion"],
        )

        self.assertTrue(result)
        mock_page.goto.assert_called_with(
            "https://www.tiktok.com/upload?lang=en", wait_until="networkidle"
        )


if __name__ == "__main__":
    unittest.main()
