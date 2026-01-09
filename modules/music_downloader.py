import requests
import os
import random
from utils.logger import setup_logger

logger = setup_logger()


class MusicDownloader:
    """Downloads royalty-free background music from Pixabay"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://pixabay.com/api/videos/"

    def download_music(self, output_path: str, query: str = "background music") -> str:
        """
        Download background music from Pixabay

        Args:
            output_path: Path to save music file
            query: Search query for music

        Returns:
            str: Path to downloaded music file
        """
        logger.info(f"Searching for background music: {query}")

        try:
            # Search for music
            params = {
                'key': self.api_key,
                'q': query,
                'per_page': 20
            }

            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()

            if not data.get('hits'):
                raise ValueError("No music found on Pixabay")

            # Select random music
            music = random.choice(data['hits'])

            # Get medium quality video (we'll extract audio)
            video_url = music['videos']['medium']['url']

            logger.info(f"Downloading music from: {video_url}")

            # Download music file
            music_response = requests.get(video_url, stream=True, timeout=60)
            music_response.raise_for_status()

            with open(output_path, 'wb') as f:
                for chunk in music_response.iter_content(chunk_size=8192):
                    f.write(chunk)

            logger.info(f"Music downloaded successfully: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Error downloading music: {e}")
            raise