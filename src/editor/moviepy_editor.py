import os
import logging
from moviepy import (
    ImageClip,
    TextClip,
    CompositeVideoClip,
    concatenate_videoclips,
)
from typing import List, Dict

logger = logging.getLogger(__name__)


class MoviePyEditor:
    def __init__(self, output_dir: str = "data/videos"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.width = 1080
        self.height = 1920
        self.font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

    def assemble_video(
        self, script_data: Dict, image_paths: List[str], video_name: str
    ) -> str:
        """
        Assembles a vertical TikTok video from images and script data.
        """
        if not image_paths:
            logger.error("No images provided for video assembly.")
            return None

        try:
            logger.info(f"Assembling video: {video_name}")

            clips = []
            duration_per_image = 3  # 3 seconds per slide

            overlay_texts = script_data.get("overlay_texts", [])

            for i, img_path in enumerate(image_paths):
                if not os.path.exists(img_path):
                    continue

                # Create background image clip
                img_clip = ImageClip(img_path).with_duration(
                    duration_per_image
                )

                # Resize to fit vertical format
                img_clip = img_clip.resized(width=self.width)
                if img_clip.h > self.height:
                    img_clip = img_clip.resized(height=self.height)

                img_clip = img_clip.with_position("center")

                # Add text overlay if available
                if i < len(overlay_texts):
                    txt = overlay_texts[i]
                    txt_clip = (
                        TextClip(
                            font=self.font_path,
                            text=txt,
                            font_size=70,
                            color="white",
                            stroke_color="black",
                            stroke_width=2,
                            method="caption",
                            size=(int(self.width * 0.8), None),
                        )
                        .with_duration(duration_per_image)
                        .with_position(("center", 1400))
                    )

                    video_slide = CompositeVideoClip(
                        [img_clip, txt_clip], size=(self.width, self.height)
                    )
                else:
                    video_slide = CompositeVideoClip(
                        [img_clip], size=(self.width, self.height)
                    )

                clips.append(video_slide)

            if not clips:
                return None

            final_clip = concatenate_videoclips(clips, method="compose")

            output_path = os.path.join(self.output_dir, f"{video_name}.mp4")
            # Set logger=None to avoid excessive output
            final_clip.write_videofile(
                output_path, fps=24, codec="libx264", logger=None
            )

            return output_path

        except Exception as e:
            logger.error(f"Video assembly failed: {e}")
            return None
