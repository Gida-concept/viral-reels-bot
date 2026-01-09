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
            # Generate description
            description = self._generate_description(title, story)
            
            # Create caption with title, description, and hashtags
            caption = f"{title}\n\n{description}\n\n" + " ".join([f"#{tag}" for tag in hashtags])
            
            logger.info(f"Caption preview: {caption[:100]}...")
            
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
    
    def _generate_description(self, title: str, story: str = None):
        """Generate engaging description for the post"""
        
        # If we have the story, create a teaser
        if story and len(story) > 50:
            # Get first 100-150 characters as teaser
            teaser = story[:150].strip()
            
            # Cut at last complete sentence or word
            if '.' in teaser:
                teaser = teaser[:teaser.rfind('.')+1]
            elif ' ' in teaser:
                teaser = teaser[:teaser.rfind(' ')] + '...'
            
            return f"{teaser}\n\n🎬 Watch till the end for the twist!"
        else:
            # Generic engaging description
            descriptions = [
                f"🔥 You won't believe what happens in this story!\n\n💭 Watch till the end...",
                f"⚡ This story will blow your mind!\n\n👀 Don't miss the ending!",
                f"🎯 A story you've NEVER heard before!\n\n✨ The twist is unreal!",
                f"💥 This changed my perspective completely!\n\n🎬 Must watch till the end!",
                f"🌟 The most unique story you'll hear today!\n\n🔥 Wait for the ending!"
            ]
            
            import random
            return random.choice(descriptions)
    
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
