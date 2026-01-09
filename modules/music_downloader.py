import requests
import random
import subprocess
import json
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
            pixabay_path = self._download_from_pixabay(output_path)
            # Check if downloaded file has audio
            if self._has_audio_stream(pixabay_path):
                return pixabay_path
            else:
                logger.warning("Pixabay file has no audio stream, using fallback...")
                raise ValueError("No audio in Pixabay file")
        except Exception as e:
            logger.warning(f"Pixabay download issue: {e}")
            
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
    
    def _has_audio_stream(self, file_path: str):
        """Check if file has an audio stream"""
        try:
            cmd = [
                'ffprobe', '-v', 'error',
                '-select_streams', 'a:0',
                '-show_entries', 'stream=codec_type',
                '-of', 'json',
                file_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            data = json.loads(result.stdout)
            has_audio = len(data.get('streams', [])) > 0
            logger.info(f"Audio check for {file_path}: {has_audio}")
            return has_audio
        except:
            return False

