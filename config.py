import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    PIXABAY_API_KEY = os.getenv('PIXABAY_API_KEY')
    FACEBOOK_ACCESS_TOKEN = os.getenv('FACEBOOK_ACCESS_TOKEN')
    FACEBOOK_PAGE_ID = os.getenv('FACEBOOK_PAGE_ID')
    
    # Categories
    CATEGORIES = [
        'love', 'help', 'money', 'partnership', 'dating', 'relationship',
        'poor', 'disease', 'brilliant', 'student', 'high school', 'middle school',
        'kids', 'business', 'christian', 'religion', 'bible', 'crime', 'action',
        'drug', 'mafia', 'tech', 'robotics', 'superpowers', 'fantasy'
    ]
    
    # Video URLs
    VIDEO_URLS = [
        os.getenv(f'VIDEO_URL_{i}') 
        for i in range(1, 21)
        if os.getenv(f'VIDEO_URL_{i}')
    ]
    
    # Fallback background music URL
    FALLBACK_MUSIC_URL = os.getenv('FALLBACK_MUSIC_URL', 'https://res.cloudinary.com/dv0unfuhw/video/upload/v1767958481/sndhmaxhxvpz1veablza.mp3')
    
    # Paths
    TEMP_DIR = 'temp'
    DATA_DIR = 'data'
    STATE_FILE = os.path.join(DATA_DIR, 'state.json')
    
    # Settings
    VOICE_VOLUME_BOOST = 2.10
    MUSIC_VOLUME = 0.60
    OUTPUT_RESOLUTION = (360, 640)
    SUBTITLE_FONT_SIZE = 24
    TTS_VOICE = 'en-US-AndrewNeural'
    RUN_INTERVAL_HOURS = 3
    
    @classmethod
    def validate(cls):
        required = ['GROQ_API_KEY', 'PIXABAY_API_KEY', 'FACEBOOK_ACCESS_TOKEN', 'FACEBOOK_PAGE_ID']
        missing = [k for k in required if not getattr(cls, k)]
        if missing:
            raise ValueError(f"Missing: {', '.join(missing)}")
        if not cls.VIDEO_URLS:
            raise ValueError("No video URLs configured")
        os.makedirs(cls.TEMP_DIR, exist_ok=True)
        os.makedirs(cls.DATA_DIR, exist_ok=True)
