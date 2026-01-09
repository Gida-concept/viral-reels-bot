import os
from dotenv import load_dotenv
from utils.logger import setup_logger

load_dotenv()
logger = setup_logger()

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
    MUSIC_VOLUME = 0.50
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
        
        # Validate settings
        if cls.SUBTITLE_FONT_SIZE < 10 or cls.SUBTITLE_FONT_SIZE > 100:
            logger.warning(f"Subtitle font size {cls.SUBTITLE_FONT_SIZE} may be too small/large")
        
        if cls.VOICE_VOLUME_BOOST < 0.5 or cls.VOICE_VOLUME_BOOST > 2.0:
            logger.warning(f"Voice volume boost {cls.VOICE_VOLUME_BOOST} may be extreme")
        
        if cls.MUSIC_VOLUME < 0.05 or cls.MUSIC_VOLUME > 0.5:
            logger.warning(f"Music volume {cls.MUSIC_VOLUME} may be too quiet/loud")
        
        # Create directories
        os.makedirs(cls.TEMP_DIR, exist_ok=True)
        os.makedirs(cls.DATA_DIR, exist_ok=True)
        
        logger.info(f"✓ Configuration validated")
        logger.info(f"  Videos: {len(cls.VIDEO_URLS)} URLs")
        logger.info(f"  Categories: {len(cls.CATEGORIES)}")
        logger.info(f"  Subtitle size: {cls.SUBTITLE_FONT_SIZE}px")

