import requests
from utils.logger import setup_logger

logger = setup_logger()

class FacebookUploader:
    def __init__(self, access_token: str, page_id: str):
        self.access_token = access_token
        self.page_id = page_id
        self.graph_url = "https://graph.facebook.com/v18.0"
    
    def upload_reel(self, video_path: str, title: str, hashtags: list):
        logger.info(f"Uploading to Facebook: {title}")
        try:
            caption = f"{title}\n\n" + " ".join([f"#{tag}" for tag in hashtags])
            
            # Method 1: Try direct video upload (simpler, more reliable)
            logger.info("Using direct video upload method...")
            
            upload_url = f"{self.graph_url}/{self.page_id}/videos"
            
            with open(video_path, 'rb') as video_file:
                files = {'source': video_file}
                data = {
                    'access_token': self.access_token,
                    'description': caption,
                    'title': title,
                }
                
                response = requests.post(upload_url, files=files, data=data, timeout=600)
                response.raise_for_status()
                result = response.json()
            
            video_id = result.get('id')
            logger.info(f"Upload complete! Video ID: {video_id}")
            return {'success': True, 'video_id': video_id}
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"Upload error: {e}")
            if hasattr(e.response, 'text'):
                logger.error(f"Response: {e.response.text}")
            
            # Try to get more details about the error
            try:
                error_data = e.response.json()
                logger.error(f"Error details: {error_data}")
            except:
                pass
            
            raise
        except Exception as e:
            logger.error(f"Upload error: {e}")
            raise
    
    def generate_hashtags(self, category: str):
        base_tags = ['reels', 'viral', 'story']
        category_map = {
            'love': ['love', 'romance'], 'help': ['help', 'kindness'],
            'money': ['money', 'wealth'], 'business': ['business', 'entrepreneur'],
            'tech': ['tech', 'innovation'], 'fantasy': ['fantasy', 'magic']
        }
        category_tags = category_map.get(category.lower(), [category.replace(' ', '')])
        return (base_tags + category_tags)[:3]
