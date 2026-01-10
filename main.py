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
from modules.episode_splitter import EpisodeSplitter

logger = setup_logger()

class ViralReelsBot:
    def __init__(self):
        logger.info("Initializing bot...")
        Config.validate()
        
        self.state_manager = StateManager(Config.STATE_FILE)
        self.story_generator = StoryGenerator(Config.GROQ_API_KEY)
        self.voice_generator = VoiceGenerator(Config.TTS_VOICE)
        self.subtitle_generator = SubtitleGenerator(Config.GROQ_API_KEY)
        self.video_manager = VideoManager(Config.VIDEO_URLS)
        self.music_downloader = MusicDownloader(Config.PIXABAY_API_KEY, Config.FALLBACK_MUSIC_URL)
        self.video_assembler = VideoAssembler(Config)
        self.facebook_uploader = FacebookUploader(Config.FACEBOOK_ACCESS_TOKEN, Config.FACEBOOK_PAGE_ID)
        self.episode_splitter = EpisodeSplitter(target_words_per_episode=350)  # ~2 min episodes
        
        logger.info("Bot ready")
    
    def run_pipeline(self):
        """Main pipeline - generates ONE story and posts ALL episodes with gaps"""
        run_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        logger.info(f"\n{'='*60}\nStarting run: {run_id}\n{'='*60}")
        
        try:
            # Step 1: Get category
            category = self.state_manager.get_next_category(Config.CATEGORIES)
            logger.info(f"[1/3] Category: {category}")
            
            # Step 2: Generate ONE long story
            logger.info(f"[2/3] Generating story...")
            story_data = self.story_generator.generate_story(category)
            title = story_data['title']
            story = story_data['story']
            
            # Step 3: Split into episodes
            logger.info(f"[3/3] Splitting into episodes...")
            episodes = self.episode_splitter.split_story(story, title)
            
            logger.info(f"\n{'='*60}")
            logger.info(f"📺 POSTING {len(episodes)} EPISODES")
            logger.info(f"{'='*60}\n")
            
            # Process each episode
            for episode_idx, episode in enumerate(episodes, 1):
                logger.info(f"\n{'*'*50}")
                logger.info(f"EPISODE {episode_idx}/{len(episodes)}")
                logger.info(f"{'*'*50}\n")
                
                success = self._process_episode(
                    episode=episode,
                    category=category,
                    run_id=run_id,
                    episode_idx=episode_idx
                )
                
                if not success:
                    logger.error(f"❌ Episode {episode_idx} failed, stopping run")
                    break
                
                # Wait 15 minutes between episodes (except after last one)
                if episode_idx < len(episodes):
                    wait_seconds = Config.EPISODE_GAP_MINUTES * 60
                    logger.info(f"\n⏳ Waiting {Config.EPISODE_GAP_MINUTES} minutes before next episode...")
                    logger.info(f"   Next episode at: {self._get_next_time(wait_seconds)}")
                    time.sleep(wait_seconds)
            
            # Update state after all episodes posted
            self.state_manager.increment_run_count()
            self.state_manager.update_last_run(run_id)
            self.state_manager.save_state()
            
            logger.info(f"\n{'='*60}")
            logger.info(f"✓ RUN COMPLETED!")
            logger.info(f"  Story: {title}")
            logger.info(f"  Episodes Posted: {len(episodes)}")
            logger.info(f"  Total Runs: {self.state_manager.state['total_runs']}")
            logger.info(f"  Next run in {Config.RUN_INTERVAL_HOURS} hours")
            logger.info(f"{'='*60}\n")
            
        except Exception as e:
            logger.error(f"\n{'!'*60}")
            logger.error(f"❌ PIPELINE FAILED")
            logger.error(f"Error: {str(e)}")
            logger.error(f"{'!'*60}\n")
            
            import traceback
            logger.error("Full error traceback:")
            logger.error(traceback.format_exc())
    
    def _process_episode(self, episode: dict, category: str, run_id: str, episode_idx: int):
        """Process a single episode: generate video and upload"""
        
        episode_story = episode['text']
        episode_title = episode['title']
        
        # Define paths for this episode
        ep_id = f"{run_id}_ep{episode_idx}"
        audio_path = os.path.join(Config.TEMP_DIR, f'audio_{ep_id}.mp3')
        video_path = os.path.join(Config.TEMP_DIR, f'video_{ep_id}.mp4')
        music_path = os.path.join(Config.TEMP_DIR, f'music_{ep_id}.mp3')
        subtitle_path = os.path.join(Config.TEMP_DIR, f'subs_{ep_id}.srt')
        output_path = os.path.join(Config.TEMP_DIR, f'output_{ep_id}.mp4')
        
        try:
            # Step 1: Generate voice
            logger.info(f"[1/6] Generating voice narration...")
            self.voice_generator.generate_voice(episode_story, audio_path)
            
            # Step 2: Generate subtitles
            logger.info(f"[2/6] Generating Whisper-synced subtitles...")
            self.subtitle_generator.generate_subtitles(audio_path, subtitle_path, episode_story)
            
            # Step 3: Download video
            logger.info(f"[3/6] Downloading background video...")
            video_index = self.state_manager.get_next_video_index(len(Config.VIDEO_URLS))
            self.video_manager.download_video(video_index, video_path)
            
            # Step 4: Download music
            logger.info(f"[4/6] Downloading background music...")
            self.music_downloader.download_music(music_path)
            
            # Step 5: Assemble video
            logger.info(f"[5/6] Assembling video...")
            self.video_assembler.assemble_video(
                video_path, audio_path, music_path, subtitle_path, 
                output_path, episode_title
            )
            
            # Step 6: Upload to Facebook
            logger.info(f"[6/6] Uploading to Facebook...")
            hashtags = self.facebook_uploader.generate_hashtags(category)
            
            # Generate episode-specific caption
            caption_parts = self.episode_splitter.get_episode_caption(episode, category)
            
            upload_result = self.facebook_uploader.upload_episode(
                video_path=output_path,
                episode=episode,
                caption_parts=caption_parts,
                hashtags=hashtags
            )
            
            logger.info(f"✓ Episode {episode_idx} uploaded! Video ID: {upload_result.get('video_id')}")
            
            # Cleanup this episode's files
            self._cleanup_temp_files([audio_path, video_path, music_path, subtitle_path, output_path])
            logger.info(f"✓ Episode {episode_idx} temp files cleaned")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Episode {episode_idx} error: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return False
    
    def _cleanup_temp_files(self, files: list):
        """Clean up temporary files after successful upload"""
        for file_path in files:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    logger.debug(f"Cleaned up: {file_path}")
            except Exception as e:
                logger.warning(f"Failed to cleanup {file_path}: {e}")
    
    def _get_next_time(self, seconds: int):
        """Get formatted time for next action"""
        from datetime import datetime, timedelta
        next_time = datetime.now() + timedelta(seconds=seconds)
        return next_time.strftime('%I:%M %p')
    
    def start_scheduler(self):
        logger.info(f"Starting scheduler (every {Config.RUN_INTERVAL_HOURS} hours)")
        schedule.every(Config.RUN_INTERVAL_HOURS).hours.do(self.run_pipeline)
        
        # Run immediately on start
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
