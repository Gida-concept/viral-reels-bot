import subprocess
import json
from utils.logger import setup_logger

logger = setup_logger()

class VideoAssembler:
    def __init__(self, config):
        self.config = config
    
    def _escape_ffmpeg_text(self, text: str) -> str:
        """
        Properly escape text for FFmpeg drawtext filter
        FFmpeg drawtext is VERY sensitive to special characters
        """
        # Order matters! Do backslash first
        text = text.replace('\\', '\\\\')  # Backslash
        text = text.replace("'", "\\'")    # Single quote/apostrophe
        text = text.replace(':', '\\:')    # Colon
        text = text.replace('%', '\\%')    # Percent
        text = text.replace('[', '\\[')    # Left bracket
        text = text.replace(']', '\\]')    # Right bracket
        return text
    
    def assemble_video(self, video_path, audio_path, music_path, subtitle_path, output_path, title=""):
        logger.info("Assembling video with Whisper-synced subtitles + static title")
        
        audio_duration = self._get_duration(audio_path)
        video_duration = self._get_duration(video_path)
        
        logger.info(f"Audio: {audio_duration:.2f}s, Video: {video_duration:.2f}s")
        logger.info(f"Title caption: {title}")
        
        width, height = self.config.OUTPUT_RESOLUTION
        
        # Escape paths for subtitles (different escaping rules)
        subtitle_path_escaped = subtitle_path.replace('\\', '/').replace(':', '\\:')
        
        # Escape title text for drawtext filter (strict escaping)
        title_escaped = self._escape_ffmpeg_text(title)
        
        logger.debug(f"Original title: {title}")
        logger.debug(f"Escaped title: {title_escaped}")
        
        # Check if music has audio
        has_music_audio = self._has_audio_stream(music_path)
        
        if has_music_audio:
            # WITH MUSIC - Whisper subtitles + title caption
            filter_complex = (
                # Scale and crop video
                f"[0:v]scale={width}:{height}:force_original_aspect_ratio=increase,"
                f"crop={width}:{height}[v_crop];"
                
                # Add Whisper-synced subtitles (middle of screen)
                f"[v_crop]subtitles={subtitle_path_escaped}:"
                f"force_style='FontName=Arial,FontSize={self.config.SUBTITLE_FONT_SIZE},"
                f"Bold=1,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,"
                f"BackColour=&H80000000,Outline=2,Shadow=1,MarginV=80,Alignment=2'[v_sub];"
                
                # Add static title caption at bottom
                f"[v_sub]drawtext="
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
                '-stream_loop', '-1',
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
            # WITHOUT MUSIC - Whisper subtitles + title caption
            logger.warning("Music has no audio, using voice only")
            filter_complex = (
                # Scale and crop video
                f"[0:v]scale={width}:{height}:force_original_aspect_ratio=increase,"
                f"crop={width}:{height}[v_crop];"
                
                # Add Whisper-synced subtitles (middle of screen)
                f"[v_crop]subtitles={subtitle_path_escaped}:"
                f"force_style='FontName=Arial,FontSize={self.config.SUBTITLE_FONT_SIZE},"
                f"Bold=1,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,"
                f"BackColour=&H80000000,Outline=2,Shadow=1,MarginV=80,Alignment=2'[v_sub];"
                
                # Add static title caption at bottom
                f"[v_sub]drawtext="
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
                '-stream_loop', '-1',
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
            logger.info("Running FFmpeg with Whisper subtitles + title...")
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            # Verify output
            output_duration = self._get_duration(output_path)
            logger.info(f"✓ Output duration: {output_duration:.2f}s (expected: {audio_duration:.2f}s)")
            
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
