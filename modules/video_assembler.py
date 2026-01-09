import subprocess
import json
from utils.logger import setup_logger

logger = setup_logger()

class VideoAssembler:
    def __init__(self, config):
        self.config = config
    
    def assemble_video(self, video_path, audio_path, music_path, subtitle_path, output_path):
        logger.info("Assembling video with synchronized timing")
        try:
            audio_duration = self._get_duration(audio_path)
            video_duration = self._get_duration(video_path)
            
            logger.info(f"Audio: {audio_duration:.2f}s, Video: {video_duration:.2f}s")
            
            width, height = self.config.OUTPUT_RESOLUTION
            subtitle_path_escaped = subtitle_path.replace('\\', '/').replace(':', '\\:')
            
            # Check if music has audio
            has_music_audio = self._has_audio_stream(music_path)
            
            # Calculate how many loops we need
            loops_needed = int(audio_duration / video_duration) + 1
            
            if has_music_audio:
                # WITH MUSIC - Properly synced
                filter_complex = (
                    # Loop video to match audio duration
                    f"[0:v]loop=loop={loops_needed}:size=1:start=0,"
                    f"scale={width}:{height}:force_original_aspect_ratio=increase,"
                    f"crop={width}:{height},"
                    f"trim=duration={audio_duration},"
                    f"setpts=PTS-STARTPTS[v_base];"
                    
                    # Add subtitles to video (starting from 0)
                    f"[v_base]subtitles={subtitle_path_escaped}:"
                    f"force_style='FontSize={self.config.SUBTITLE_FONT_SIZE}'[v];"
                    
                    # Audio mixing
                    f"[1:a]volume={self.config.VOICE_VOLUME_BOOST},atrim=duration={audio_duration}[voice];"
                    f"[2:a]volume={self.config.MUSIC_VOLUME},aloop=loop=-1:size=2e+09,"
                    f"atrim=duration={audio_duration}[music];"
                    f"[voice][music]amix=inputs=2:duration=first:dropout_transition=2[a]"
                )
                
                cmd = [
                    'ffmpeg', '-y',
                    '-i', video_path,
                    '-i', audio_path,
                    '-i', music_path,
                    '-filter_complex', filter_complex,
                    '-map', '[v]',
                    '-map', '[a]',
                    '-c:v', 'libx264',
                    '-preset', 'medium',
                    '-crf', '23',
                    '-c:a', 'aac',
                    '-b:a', '128k',
                    '-movflags', '+faststart',
                    '-shortest',
                    output_path
                ]
            else:
                # WITHOUT MUSIC - Voice only, properly synced
                logger.warning("Music has no audio, using voice only")
                filter_complex = (
                    # Loop video to match audio duration
                    f"[0:v]loop=loop={loops_needed}:size=1:start=0,"
                    f"scale={width}:{height}:force_original_aspect_ratio=increase,"
                    f"crop={width}:{height},"
                    f"trim=duration={audio_duration},"
                    f"setpts=PTS-STARTPTS[v_base];"
                    
                    # Add subtitles (starting from 0)
                    f"[v_base]subtitles={subtitle_path_escaped}:"
                    f"force_style='FontSize={self.config.SUBTITLE_FONT_SIZE}'[v];"
                    
                    # Voice audio only
                    f"[1:a]volume={self.config.VOICE_VOLUME_BOOST},atrim=duration={audio_duration}[a]"
                )
                
                cmd = [
                    'ffmpeg', '-y',
                    '-i', video_path,
                    '-i', audio_path,
                    '-filter_complex', filter_complex,
                    '-map', '[v]',
                    '-map', '[a]',
                    '-c:v', 'libx264',
                    '-preset', 'medium',
                    '-crf', '23',
                    '-c:a', 'aac',
                    '-b:a', '128k',
                    '-movflags', '+faststart',
                    '-shortest',
                    output_path
                ]
            
            logger.info("Running FFmpeg with synchronized streams...")
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            # Verify output
            output_duration = self._get_duration(output_path)
            logger.info(f"Output video duration: {output_duration:.2f}s (expected: {audio_duration:.2f}s)")
            
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
