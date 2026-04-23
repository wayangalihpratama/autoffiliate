import unittest
from unittest.mock import MagicMock, patch
from src.intelligence.gemini_engine import GeminiEngine


class TestGeminiEngine(unittest.TestCase):
    @patch("google.generativeai.GenerativeModel")
    def test_generate_script(self, mock_model):
        # Mock the model's response
        mock_response = MagicMock()
        mock_response.text = '{"tts_text": "Hey check this out!", "overlay_texts": ["Trending now"], "visual_cues": "Show product"}'
        mock_model.return_value.generate_content.return_value = mock_response

        engine = GeminiEngine(api_key="fake_key")
        product_data = {
            "title": "Cool Shirt",
            "price": "$10",
            "sales_30d": "500+",
        }
        niche_config = {
            "tone": "energetic",
            "language": "en",
            "system_prompt_ref": "config/prompts/fashion_v1.txt",
        }

        # This should call our mock
        result = engine.generate_script(product_data, niche_config)

        self.assertIn("tts_text", result)
        self.assertEqual(result["tts_text"], "Hey check this out!")
        self.assertEqual(len(result["overlay_texts"]), 1)


if __name__ == "__main__":
    unittest.main()
