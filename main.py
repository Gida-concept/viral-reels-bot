#!/usr/bin/env python3
import os
import time
import schedule
from datetime import datetime
from config import Config
from utils.logger import setup_logger
from utils.state_manager import StateManager
from modules.story_generator import StoryGenerator
from modules.voice_generator import VoiceGenerator
from modules.subtitle_generator import SubtitleGenerator
from modules.video_manager import VideoManager
from modules.music_downloader import MusicDownloader
from modules.video_assembler import VideoAssembler
from modules.facebook_uploader import FacebookUploader

logger = setup_logger()

class ViralReelsBot:
    def __init__(self):
        logger.info("Initializing bot...")
        Config.validate()
        
        self.state_manager = StateManager(Config.STATE_FILE)
        self.story_generator = StoryGenerator(Config.GROQ_API_KEY)
        self.voice_generator = VoiceGenerator(Config.TTS_VOICE)
        self.subtitle_generator = SubtitleGenerator()
        self.video_manager = VideoManager(Config.VIDEO_URLS)
        self.music_downloader = MusicDownloader(Config.PIXABAY_API_KEY, Config.FALLBACK_MUSIC_URL)
        self.video_assembler = VideoAssembler(Config)
        self.facebook_uploader = FacebookUploader(Config.FACEBOOK_ACCESS_TOKEN, Config.FACEBOOK_PAGE_ID)
        
        logger.info("Bot ready")
    
    def run_pipeline(self):
        run_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        logger.info(f"\n{'='*60}\nStarting run: {run_id}\n{'='*60}")
        
        try:
            category = self.state_manager.get_next_category(Config.CATEGORIES)
            logger.info(f"Category: {category}")
            
            story_data = self.story_generator.generate_story(category)
            title = story_data['title']
            story = story_data['story']
            
            audio_path = os.path.join(Config.TEMP_DIR, f'audio_{run_id}.mp3')
            video_path = os.path.join(Config.TEMP_DIR, f'video_{run_id}.mp4')
            music_path = os.path.join(Config.TEMP_DIR, f'music_{run_id}.mp3')
            subtitle_path = os.path.join(Config.TEMP_DIR, f'subs_{run_id}.srt')
            output_path = os.path.join(Config.TEMP_DIR, f'output_{run_id}.mp4')
            
            self.voice_generator.generate_voice(story, audio_path)
            self.subtitle_generator.generate_subtitles(audio_path, subtitle_path, story)
            
            video_index = self.state_manager.get_next_video_index(len(Config.VIDEO_URLS))
            self.video_manager.download_video(video_index, video_path)
            self.music_downloader.download_music(music_path)
            
            self.video_assembler.assemble_video(video_path, audio_path, music_path, subtitle_path, output_path)
            
            hashtags = self.facebook_uploader.generate_hashtags(category)
            self.facebook_uploader.upload_reel(output_path, title, hashtags)
            
            self.state_manager.increment_run_count()
            self.state_manager.update_last_run(run_id)
            self.state_manager.save_state()
            
            logger.info(f"✓ Complete! Total runs: {self.state_manager.state['total_runs']}\n")
            
            # Cleanup
            for f in [audio_path, video_path, music_path, subtitle_path]:
                if os.path.exists(f):
                    os.remove(f)
        
        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            raise
    
    def start_scheduler(self):
        logger.info(f"Starting scheduler (every {Config.RUN_INTERVAL_HOURS} hours)")
        schedule.every(Config.RUN_INTERVAL_HOURS).hours.do(self.run_pipeline)
        
        self.run_pipeline()
        
        logger.info("Bot running. Press Ctrl+C to stop.")
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)
        except KeyboardInterrupt:
            logger.info("Bot stopped")

if __name__ == "__main__":
    bot = ViralReelsBot()
    bot.start_scheduler()
