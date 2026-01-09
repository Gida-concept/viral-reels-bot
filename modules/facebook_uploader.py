import requests
import os
from utils.logger import setup_logger

logger = setup_logger()


class FacebookUploader:
    """Uploads videos to Facebook Reels"""

    def __init__(self, access_token: str, page_id: str):
        self.access_token = access_token
        self.page_id = page_id
        self.graph_url = "https://graph.facebook.com/v18.0"

    def upload_reel(self, video_path: str, title: str, hashtags: list) -> dict:
        """
        Upload video to Facebook Reels

        Args:
            video_path: Path to video file
            title: Video title
            hashtags: List of hashtags

        Returns:
            dict: Upload response
        """
        logger.info(f"Uploading video to Facebook Reels: {title}")

        try:
            # Create caption
            caption = f"{title}\n\n" + " ".join([f"#{tag}" for tag in hashtags])

            # Step 1: Initialize upload
            init_url = f"{self.graph_url}/{self.page_id}/video_reels"

            init_params = {
                'access_token': self.access_token,
                'upload_phase': 'start'
            }

            init_response = requests.post(init_url, params=init_params, timeout=30)
            init_response.raise_for_status()
            init_data = init_response.json()

            video_id = init_data['video_id']
            upload_url = init_data['upload_url']

            logger.info(f"Upload initialized. Video ID: {video_id}")

            # Step 2: Upload video file
            with open(video_path, 'rb') as video_file:
                files = {'file': video_file}

                upload_response = requests.post(
                    upload_url,
                    files=files,
                    timeout=300  # 5 minutes timeout for large files
                )
                upload_response.raise_for_status()

            logger.info("Video file uploaded successfully")

            # Step 3: Finalize upload with metadata
            finalize_url = f"{self.graph_url}/{self.page_id}/video_reels"

            finalize_params = {
                'access_token': self.access_token,
                'video_id': video_id,
                'upload_phase': 'finish',
                'description': caption,
                'title': title
            }

            finalize_response = requests.post(finalize_url, params=finalize_params, timeout=30)
            finalize_response.raise_for_status()
            finalize_data = finalize_response.json()

            logger.info(f"Upload finalized successfully: {finalize_data}")

            return {
                'success': True,
                'video_id': video_id,
                'response': finalize_data
            }

        except requests.exceptions.RequestException as e:
            logger.error(f"Error uploading to Facebook: {e}")
            if hasattr(e.response, 'text'):
                logger.error(f"Response: {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during upload: {e}")
            raise

    def generate_hashtags(self, category: str) -> list:
        """Generate relevant hashtags for the category"""

        # Base hashtags
        base_tags = ['reels', 'viral', 'story']

        # Category-specific hashtags
        category_map = {
            'love': ['love', 'romance', 'relationship'],
            'help': ['help', 'kindness', 'support'],
            'money': ['money', 'wealth', 'success'],
            'partnership': ['partnership', 'business', 'teamwork'],
            'dating': ['dating', 'romance', 'love'],
            'relationship': ['relationship', 'couple', 'love'],
            'poor': ['inspiring', 'motivation', 'success'],
            'disease': ['health', 'awareness', 'support'],
            'brilliant': ['genius', 'smart', 'brilliant'],
            'student': ['student', 'education', 'school'],
            'high school': ['highschool', 'teen', 'school'],
            'middle school': ['middleschool', 'school', 'teen'],
            'kids': ['kids', 'children', 'family'],
            'business': ['business', 'entrepreneur', 'success'],
            'christian': ['christian', 'faith', 'inspirational'],
            'religion': ['faith', 'spiritual', 'religion'],
            'bible': ['bible', 'faith', 'christian'],
            'crime': ['crime', 'thriller', 'mystery'],
            'action': ['action', 'adventure', 'thriller'],
            'drug': ['awareness', 'truth', 'reality'],
            'mafia': ['mafia', 'crime', 'thriller'],
            'tech': ['tech', 'technology', 'innovation'],
            'robotics': ['robotics', 'ai', 'technology'],
            'superpowers': ['superpowers', 'fantasy', 'scifi'],
            'fantasy': ['fantasy', 'magic', 'adventure']
        }

        category_tags = category_map.get(category.lower(), [category.replace(' ', '')])

        # Combine and return top 3
        all_tags = base_tags + category_tags
        return all_tags[:3]