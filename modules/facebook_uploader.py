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
            # Generate unique description from story
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
        """Generate unique 3-line description from the actual story"""
        
        if not story or len(story) < 100:
            # Fallback if story is too short
            return f"A story you won't forget.\nWatch till the end.\nThe twist will shock you! 🔥"
        
        # Extract first 2-3 sentences or ~120-180 characters as hook
        sentences = story.replace('\n', ' ').split('.')
        
        # Get first compelling sentence
        line1 = sentences[0].strip() if sentences else story[:60].strip()
        
        # Clean up and limit length
        if len(line1) > 80:
            line1 = line1[:77] + "..."
        
        # Second line - continue the hook or create intrigue
        if len(sentences) > 1:
            line2 = sentences[1].strip()
            if len(line2) > 80:
                line2 = line2[:77] + "..."
        else:
            # Create intrigue if we don't have a second sentence
            line2 = "What happens next will surprise you."
        
        # Third line - always a call to action with emoji
        call_to_actions = [
            "Watch till the end! 🎬",
            "The ending is unreal! 🔥",
            "You won't see it coming! ⚡",
            "Wait for the twist! 💥",
            "This changes everything! ✨",
            "The reveal is insane! 🎯",
            "Don't miss the finale! 👀",
            "The conclusion shocked me! 🌟"
        ]
        
        import random
        line3 = random.choice(call_to_actions)
        
        # Combine into 3-line description
        description = f"{line1}\n{line2}\n{line3}"
        
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
