import requests
from utils.logger import setup_logger

logger = setup_logger()

class FacebookUploader:
    def __init__(self, access_token: str, page_id: str):
        self.access_token = access_token
        self.page_id = page_id
        self.graph_url = "https://graph.facebook.com/v18.0"
    
    def upload_reel(self, video_path: str, title: str, hashtags: list, story: str = None):
        logger.info(f"Uploading to Facebook: {title}")
        try:
            # Generate description from first 3 lines of story
            description = self._generate_description_from_story(story, title)
            
            # Create caption with title, description, and hashtags
            caption = f"{title}\n\n{description}\n\n" + " ".join([f"#{tag}" for tag in hashtags])
            
            logger.info(f"Caption preview:\n{caption[:200]}...")
            
            # Direct video upload
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
            
            try:
                error_data = e.response.json()
                logger.error(f"Error details: {error_data}")
            except:
                pass
            
            raise
        except Exception as e:
            logger.error(f"Upload error: {e}")
            raise
    
    def _generate_description_from_story(self, story: str, title: str):
        """Use first 3 lines from the actual story as description"""
        
        if not story or len(story) < 20:
            return "A story that will surprise you.\nWatch to find out what happens.\nYou won't believe the ending!"
        
        # Split story into lines
        lines = story.strip().split('\n')
        
        # Filter out empty lines
        lines = [line.strip() for line in lines if line.strip()]
        
        if len(lines) >= 3:
            # Use first 3 lines exactly as written
            description = f"{lines[0]}\n{lines[1]}\n{lines[2]}"
        elif len(lines) == 2:
            # Use 2 lines + add emoji
            description = f"{lines[0]}\n{lines[1]}\n🎬"
        elif len(lines) == 1:
            # Split first line into sentences
            sentences = lines[0].split('.')
            sentences = [s.strip() + '.' for s in sentences if s.strip()]
            
            if len(sentences) >= 3:
                description = f"{sentences[0]}\n{sentences[1]}\n{sentences[2]}"
            else:
                description = f"{lines[0]}\n\nWatch now! 🔥"
        else:
            description = story[:150].strip()
        
        logger.info(f"Description: First 3 lines from story")
        
        return description
    
    def generate_hashtags(self, category: str):
        base_tags = ['reels', 'viral', 'story']
        category_map = {
            'love': ['love', 'romance'], 
            'help': ['help', 'kindness'],
            'money': ['money', 'wealth'], 
            'partnership': ['partnership', 'business'],
            'dating': ['dating', 'relationships'],
            'relationship': ['relationships', 'couple'],
            'poor': ['inspiration', 'motivation'],
            'disease': ['health', 'awareness'],
            'brilliant': ['genius', 'smart'],
            'student': ['student', 'education'],
            'high school': ['highschool', 'teen'],
            'middle school': ['middleschool', 'school'],
            'kids': ['kids', 'family'],
            'business': ['business', 'entrepreneur'], 
            'christian': ['christian', 'faith'],
            'religion': ['faith', 'spiritual'],
            'bible': ['bible', 'faith'],
            'crime': ['crime', 'thriller'], 
            'action': ['action', 'adventure'],
            'drug': ['awareness', 'reality'],
            'mafia': ['mafia', 'thriller'],
            'tech': ['tech', 'innovation'], 
            'robotics': ['robotics', 'ai'],
            'superpowers': ['superpowers', 'scifi'],
            'fantasy': ['fantasy', 'magic']
        }
        category_tags = category_map.get(category.lower(), [category.replace(' ', '')])
        return (base_tags + category_tags)[:3]
