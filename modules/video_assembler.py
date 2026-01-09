import subprocess
import json
from utils.logger import setup_logger

logger = setup_logger()

class VideoAssembler:
    def __init__(self, config):
        self.config = config
    
    def assemble_video(self, video_path, audio_path, music_path, subtitle_path, output_path):
        logger.info("Assembling video")
        try:
            audio_duration = self._get_duration(audio_path)
            width, height = self.config.OUTPUT_RESOLUTION
            
            subtitle_path_escaped = subtitle_path.replace('\\', '/').replace(':', '\\:')
            
            # Check if music file has audio stream
            has_music_audio = self._has_audio_stream(music_path)
            
            if has_music_audio:
                # Music file has audio, use it
                filter_complex = (
                    f"[0:v]scale={width}:{height}:force_original_aspect_ratio=increase,"
                    f"crop={width}:{height}[v];"
                    f"[1:a]volume={self.config.VOICE_VOLUME_BOOST}[voice];"
                    f"[2:a]volume={self.config.MUSIC_VOLUME}[music];"
                    f"[voice][music]amix=inputs=2:duration=first[a];"
                    f"[v]subtitles={subtitle_path_escaped}:force_style='FontSize={self.config.SUBTITLE_FONT_SIZE}'[vout]"
                )
            else:
                # No music audio, use voice only
                logger.warning("Music file has no audio stream, using voice only")
                filter_complex = (
                    f"[0:v]scale={width}:{height}:force_original_aspect_ratio=increase,"
                    f"crop={width}:{height}[v];"
                    f"[1:a]volume={self.config.VOICE_VOLUME_BOOST}[a];"
                    f"[v]subtitles={subtitle_path_escaped}:force_style='FontSize={self.config.SUBTITLE_FONT_SIZE}'[vout]"
                )
            
            cmd = [
                'ffmpeg', '-y',
                '-stream_loop', '-1',
                '-i', video_path,
                '-i', audio_path,
            ]
            
            if has_music_audio:
                cmd.extend(['-i', music_path])
            
            cmd.extend([
                '-filter_complex', filter_complex,
                '-map', '[vout]',
                '-map', '[a]',
                '-t', str(audio_duration),
                '-c:v', 'libx264',
                '-preset', 'medium',
                '-crf', '23',
                '-c:a', 'aac',
                '-b:a', '128k',
                '-movflags', '+faststart',
                output_path
            ])
            
            subprocess.run(cmd, capture_output=True, text=True, check=True)
            logger.info(f"Video assembled: {output_path}")
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
