import requests
import random
from utils.logger import setup_logger

logger = setup_logger()

class MusicDownloader:
    def __init__(self, api_key: str, fallback_url: str = None):
        self.api_key = api_key
        self.fallback_url = fallback_url
        self.base_url = "https://pixabay.com/api/videos/"
    
    def download_music(self, output_path: str):
        logger.info("Downloading background music")
        
        # Try Pixabay first
        try:
            return self._download_from_pixabay(output_path)
        except Exception as e:
            logger.warning(f"Pixabay download failed: {e}")
            
            # Use fallback music
            if self.fallback_url:
                logger.info("Using fallback music URL...")
                return self._download_from_url(self.fallback_url, output_path)
            else:
                raise Exception("No fallback music URL configured")
    
    def _download_from_pixabay(self, output_path: str):
        try:
            params = {'key': self.api_key, 'q': 'background music', 'per_page': 20}
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            if not data.get('hits'):
                raise ValueError("No music found on Pixabay")
            
            music = random.choice(data['hits'])
            video_url = music['videos']['medium']['url']
            
            return self._download_from_url(video_url, output_path)
            
        except Exception as e:
            logger.error(f"Error downloading from Pixabay: {e}")
            raise
    
    def _download_from_url(self, url: str, output_path: str):
        try:
            logger.info(f"Downloading music from: {url}")
            music_response = requests.get(url, stream=True, timeout=60)
            music_response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                for chunk in music_response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            logger.info(f"Music saved: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Error downloading music: {e}")
            raise
