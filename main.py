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
            # Step 1: Get category
            category = self.state_manager.get_next_category(Config.CATEGORIES)
            logger.info(f"[1/8] Category: {category}")
            
            # Step 2: Generate story
            logger.info(f"[2/8] Generating story...")
            story_data = self.story_generator.generate_story(category)
            title = story_data['title']
            story = story_data['story']
            
            # Define paths
            audio_path = os.path.join(Config.TEMP_DIR, f'audio_{run_id}.mp3')
            video_path = os.path.join(Config.TEMP_DIR, f'video_{run_id}.mp4')
            music_path = os.path.join(Config.TEMP_DIR, f'music_{run_id}.mp3')
            subtitle_path = os.path.join(Config.TEMP_DIR, f'subs_{run_id}.srt')
            output_path = os.path.join(Config.TEMP_DIR, f'output_{run_id}.mp4')
            
            # Step 3: Generate voice
            logger.info(f"[3/8] Generating voice narration...")
            self.voice_generator.generate_voice(story, audio_path)
            
            # Step 4: Generate subtitles
            logger.info(f"[4/8] Generating subtitles...")
            self.subtitle_generator.generate_subtitles(audio_path, subtitle_path, story)
            
            # Step 5: Download video
            logger.info(f"[5/8] Downloading background video...")
            video_index = self.state_manager.get_next_video_index(len(Config.VIDEO_URLS))
            self.video_manager.download_video(video_index, video_path)
            
            # Step 6: Download music
            logger.info(f"[6/8] Downloading background music...")
            self.music_downloader.download_music(music_path)
            
            # Step 7: Assemble video
            logger.info(f"[7/8] Assembling video...")
            self.video_assembler.assemble_video(video_path, audio_path, music_path, subtitle_path, output_path)
            
            # Step 8: Upload to Facebook
            logger.info(f"[8/8] Uploading to Facebook...")
            hashtags = self.facebook_uploader.generate_hashtags(category)
            upload_result = self.facebook_uploader.upload_reel(output_path, title, hashtags)
            
            # Update state
            self.state_manager.increment_run_count()
            self.state_manager.update_last_run(run_id)
            self.state_manager.save_state()
            
            logger.info(f"\n{'='*60}")
            logger.info(f"✓ Pipeline completed successfully!")
            logger.info(f"  Title: {title}")
            logger.info(f"  Video ID: {upload_result.get('video_id')}")
            logger.info(f"  Total Runs: {self.state_manager.state['total_runs']}")
            logger.info(f"{'='*60}\n")
            
            # Cleanup ALL temp files including final output to save space
            self._cleanup_temp_files([audio_path, video_path, music_path, subtitle_path, output_path])
            logger.info("✓ All temp files deleted to preserve space")
            
        except Exception as e:
            logger.error(f"\n{'!'*60}")
            logger.error(f"❌ PIPELINE FAILED")
            logger.error(f"Error: {str(e)}")
            logger.error(f"{'!'*60}\n")
            
            # Print full traceback for debugging
            import traceback
            logger.error("Full error traceback:")
            logger.error(traceback.format_exc())
            
            # Don't raise - let bot continue running
    
    def _cleanup_temp_files(self, files: list):
        """Clean up temporary files after successful upload"""
        for file_path in files:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    logger.debug(f"Cleaned up: {file_path}")
            except Exception as e:
                logger.warning(f"Failed to cleanup {file_path}: {e}")
    
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

