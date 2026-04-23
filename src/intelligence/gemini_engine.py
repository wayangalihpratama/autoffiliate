import os
import json
import logging
import google.generativeai as genai
from typing import Dict

logger = logging.getLogger(__name__)


class GeminiEngine:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            logger.warning("GEMINI_API_KEY not found in environment.")

        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel("gemini-2.0-flash")
        else:
            self.model = None

    def generate_script(self, product_data: Dict, niche_config: Dict) -> Dict:
        """
        Generates a viral script using Gemini 2.0 based on product data and niche config.
        """
        prompt_path = niche_config.get("system_prompt_ref")
        if not os.path.exists(prompt_path):
            logger.error(f"Prompt file {prompt_path} not found.")
            return {}

        with open(prompt_path, "r") as f:
            template = f.read()

        # Fill template
        prompt = template.format(
            title=product_data.get("title", "Unknown Product"),
            price=product_data.get("price", "TBA"),
            sales_30d=product_data.get("sales_30d", "0"),
            tone=niche_config.get("tone", "neutral"),
            language=niche_config.get("language", "en"),
        )

        # Mock Mode
        if not self.model or niche_config.get("mock"):
            logger.info("Mock mode active: returning default script.")
            return {
                "tts_text": f"Dapatkan {product_data.get('title')} sekarang dengan harga terbaik!",
                "overlay_texts": [
                    "Produk Viral TikTok!",
                    f"Hanya {product_data.get('price')}",
                    "Stok Terbatas!",
                ],
                "visual_cues": "Tampilkan gambar produk dengan transisi halus.",
            }

        try:
            logger.info(f"Generating script for: {product_data.get('title')}")
            response = self.model.generate_content(prompt)

            # Extract JSON from response (handling potential markdown blocks)
            raw_text = response.text.strip()
            if raw_text.startswith("```json"):
                raw_text = (
                    raw_text.replace("```json", "").replace("```", "").strip()
                )

            script_data = json.loads(raw_text)
            return script_data

        except Exception as e:
            logger.error(f"Gemini generation failed: {e}")
            return {}
