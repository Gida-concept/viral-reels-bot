import requests
import os
from utils.logger import setup_logger

logger = setup_logger()


class VideoManager:
    """Manages video rotation and downloading"""

    def __init__(self, video_urls: list):
        self.video_urls = video_urls

    def download_video(self, index: int, output_path: str) -> str:
        """
        Download video at the given index

        Args:
            index: Index of video to download
            output_path: Path to save video

        Returns:
            str: Path to downloaded video
        """
        url = self.video_urls[index]
        logger.info(f"Downloading video {index + 1}/{len(self.video_urls)}: {url}")

        try:
            response = requests.get(url, stream=True, timeout=60)
            response.raise_for_status()

            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            if not os.path.exists(output_path):
                raise FileNotFoundError(f"Video not downloaded: {output_path}")

            logger.info(f"Video downloaded successfully: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Error downloading video: {e}")
            raise