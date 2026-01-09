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
            # Generate trending hashtags
            all_hashtags = self._generate_trending_hashtags(hashtags)
            
            # Create caption: Title + Hashtags only (like Pocket FM)
            caption = f"{title}\n\n" + " ".join([f"#{tag}" for tag in all_hashtags])
            
            logger.info(f"Caption:\n{caption}")
            
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
    
    def _generate_trending_hashtags(self, category_tags: list):
        """Generate trending hashtags like Pocket FM style"""
        
        # Trending general hashtags (like Pocket FM uses)
        trending_general = [
            'viral', 'trending', 'foryou', 'foryoupage', 'fyp',
            'explore', 'explorepage', 'reels', 'reelsinstagram', 
            'instareels', 'viralreels', 'trendingreels', 'storytime',
            'storytelling', 'stories', 'emotional', 'drama', 
            'suspense', 'thriller', 'mustwatch', 'binge'
        ]
        
        # Content-specific hashtags
        content_hashtags = [
            'shortfilm', 'miniseries', 'episodic', 'serialstory',
            'audiobook', 'audiostory', 'podcast', 'fiction',
            'dramaticstory', 'realstory', 'truestory', 'lifestory'
        ]
        
        # Engagement hashtags
        engagement_hashtags = [
            'watchnow', 'dontstop', 'bingeworthy', 'addictive',
            'cantmiss', 'mustsee', 'amazing', 'incredible',
            'shocking', 'unbelievable', 'mindblowing', 'epic'
        ]
        
        # Combine: category tags + trending selection
        import random
        
        # Pick 8-10 trending hashtags randomly
        selected_trending = random.sample(trending_general, 4)
        selected_content = random.sample(content_hashtags, 3)
        selected_engagement = random.sample(engagement_hashtags, 2)
        
        # Combine all hashtags (category + trending)
        all_hashtags = (
            category_tags[:2] +           # 2 category-specific
            selected_trending +            # 4 trending general
            selected_content +             # 3 content-specific
            selected_engagement            # 2 engagement
        )
        
        # Remove duplicates while preserving order
        seen = set()
        unique_hashtags = []
        for tag in all_hashtags:
            tag_lower = tag.lower()
            if tag_lower not in seen:
                seen.add(tag_lower)
                unique_hashtags.append(tag)
        
        logger.info(f"Generated {len(unique_hashtags)} hashtags: {', '.join(unique_hashtags[:5])}...")
        
        return unique_hashtags[:15]  # Max 15 hashtags
    
    def generate_hashtags(self, category: str):
        """Generate category-specific base hashtags"""
        category_map = {
            'love': ['lovestory', 'romance'], 
            'help': ['inspiration', 'kindness'],
            'money': ['money', 'success'], 
            'partnership': ['partnership', 'business'],
            'dating': ['dating', 'relationships'],
            'relationship': ['relationships', 'love'],
            'poor': ['motivation', 'inspiring'],
            'disease': ['emotional', 'deep'],
            'brilliant': ['genius', 'smart'],
            'student': ['student', 'life'],
            'high school': ['highschool', 'teen'],
            'middle school': ['school', 'youth'],
            'kids': ['family', 'kids'],
            'business': ['business', 'hustle'], 
            'christian': ['faith', 'spiritual'],
            'religion': ['spiritual', 'faith'],
            'bible': ['faith', 'inspirational'],
            'crime': ['crime', 'thriller'], 
            'action': ['action', 'intense'],
            'drug': ['deep', 'reality'],
            'mafia': ['mafia', 'crime'],
            'tech': ['tech', 'future'], 
            'robotics': ['scifi', 'future'],
            'superpowers': ['fantasy', 'powers'],
            'fantasy': ['fantasy', 'magic']
        }
        
        base_tags = category_map.get(category.lower(), [category.replace(' ', ''), 'story'])
        return base_tags
