import unittest
import os
from src.editor.moviepy_editor import MoviePyEditor
from PIL import Image


class TestMoviePyEditor(unittest.TestCase):
    def setUp(self):
        self.output_dir = "data/tests/videos"
        self.image_dir = "data/tests/images"
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.image_dir, exist_ok=True)
        self.editor = MoviePyEditor(output_dir=self.output_dir)

    def test_assemble_video_fails_no_images(self):
        script_data = {"overlay_texts": ["Overlay 1"]}
        video_path = self.editor.assemble_video(
            script_data, [], "test_video_empty"
        )
        self.assertIsNone(video_path)

    def test_assemble_video_success(self):
        # Create a dummy image
        img_path = os.path.join(self.image_dir, "test_img.png")
        img = Image.new("RGB", (100, 100), color="red")
        img.save(img_path)

        script_data = {
            "tts_text": "Hello world",
            "overlay_texts": ["This is a test"],
            "visual_cues": "Show red square",
        }

        video_path = self.editor.assemble_video(
            script_data, [img_path], "test_render"
        )
        self.assertIsNotNone(video_path)
        self.assertTrue(os.path.exists(video_path))


if __name__ == "__main__":
    unittest.main()
