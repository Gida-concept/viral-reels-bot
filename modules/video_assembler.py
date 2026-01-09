import subprocess
import json
from utils.logger import setup_logger

logger = setup_logger()

class VideoAssembler:
    def __init__(self, config):
        self.config = config
    
    def assemble_video(self, video_path, audio_path, music_path, subtitle_path, output_path, title=""):
        logger.info("Assembling video with static title caption")
        
        audio_duration = self._get_duration(audio_path)
        video_duration = self._get_duration(video_path)
        
        logger.info(f"Audio: {audio_duration:.2f}s, Video: {video_duration:.2f}s")
        logger.info(f"Title caption: {title}")
        
        width, height = self.config.OUTPUT_RESOLUTION
        
        # Escape title for FFmpeg drawtext (handle special characters)
        title_escaped = title.replace("'", "\\'").replace(":", "\\:").replace("%", "\\%").replace(",", "\\,")
        
        # Check if music has audio
        has_music_audio = self._has_audio_stream(music_path)
        
        if has_music_audio:
            # WITH MUSIC - Static title caption instead of subtitles
            filter_complex = (
                # Scale and crop video
                f"[0:v]scale={width}:{height}:force_original_aspect_ratio=increase,"
                f"crop={width}:{height}[v_crop];"
                
                # Add static title caption (stays throughout video)
                f"[v_crop]drawtext="
                f"text='{title_escaped}':"
                f"fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
                f"fontsize={self.config.SUBTITLE_FONT_SIZE}:"
                f"fontcolor=white:"
                f"borderw=2:"
                f"bordercolor=black:"
                f"x=(w-text_w)/2:"
                f"y=h-{self.config.SUBTITLE_FONT_SIZE*3}[v];"
                
                # Voice audio with volume boost
                f"[1:a]volume={self.config.VOICE_VOLUME_BOOST}[voice];"
                
                # Music audio: loop and adjust volume
                f"[2:a]aloop=loop=-1:size=2e+09,volume={self.config.MUSIC_VOLUME}[music];"
                
                # Mix voice and music
                f"[voice][music]amix=inputs=2:duration=first:dropout_transition=2[a]"
            )
            
            cmd = [
                'ffmpeg', '-y',
                '-stream_loop', '-1',  # Loop video input
                '-i', video_path,
                '-i', audio_path,
                '-i', music_path,
                '-filter_complex', filter_complex,
                '-map', '[v]',
                '-map', '[a]',
                '-t', str(audio_duration),
                '-c:v', 'libx264',
                '-preset', 'medium',
                '-crf', '23',
                '-pix_fmt', 'yuv420p',
                '-c:a', 'aac',
                '-b:a', '128k',
                '-ar', '44100',
                '-movflags', '+faststart',
                output_path
            ]
        else:
            # WITHOUT MUSIC - Static title caption instead of subtitles
            logger.warning("Music has no audio, using voice only")
            filter_complex = (
                # Scale and crop video
                f"[0:v]scale={width}:{height}:force_original_aspect_ratio=increase,"
                f"crop={width}:{height}[v_crop];"
                
                # Add static title caption (stays throughout video)
                f"[v_crop]drawtext="
                f"text='{title_escaped}':"
                f"fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
                f"fontsize={self.config.SUBTITLE_FONT_SIZE}:"
                f"fontcolor=white:"
                f"borderw=2:"
                f"bordercolor=black:"
                f"x=(w-text_w)/2:"
                f"y=h-{self.config.SUBTITLE_FONT_SIZE*3}[v];"
                
                # Voice audio with volume boost
                f"[1:a]volume={self.config.VOICE_VOLUME_BOOST}[a]"
            )
            
            cmd = [
                'ffmpeg', '-y',
                '-stream_loop', '-1',  # Loop video input
                '-i', video_path,
                '-i', audio_path,
                '-filter_complex', filter_complex,
                '-map', '[v]',
                '-map', '[a]',
                '-t', str(audio_duration),
                '-c:v', 'libx264',
                '-preset', 'medium',
                '-crf', '23',
                '-pix_fmt', 'yuv420p',
                '-c:a', 'aac',
                '-b:a', '128k',
                '-ar', '44100',
                '-movflags', '+faststart',
                output_path
            ]
        
        try:
            logger.info("Running FFmpeg with static title caption...")
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            # Verify output
            output_duration = self._get_duration(output_path)
            logger.info(f"✓ Output duration: {output_duration:.2f}s (expected: {audio_duration:.2f}s)")
            
            # Check if duration matches (within 1 second tolerance)
            if abs(output_duration - audio_duration) > 1.0:
                logger.warning(f"Duration mismatch! Expected {audio_duration:.2f}s, got {output_duration:.2f}s")
            
            logger.info(f"Video assembled successfully: {output_path}")
            return output_path
            
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg error: {e.stderr}")
            raise
        except Exception as e:
            logger.error(f"Error assembling video: {e}")
            raise
    
    def _get_duration(self, file_path):
        cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'json', file_path]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        return float(data['format']['duration'])
    
    def _has_audio_stream(self, file_path):
        """Check if file has an audio stream"""
        try:
            cmd = [
                'ffprobe', '-v', 'error',
                '-select_streams', 'a:0',
                '-show_entries', 'stream=codec_type',
                '-of', 'json',
                file_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            data = json.loads(result.stdout)
            return len(data.get('streams', [])) > 0
        except:
            return False
