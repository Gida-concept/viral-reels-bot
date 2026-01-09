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
            
        if has_music_audio:
                # WITH MUSIC - Simpler looping approach
                filter_complex = (
                    # Scale and crop video
                    f"[0:v]scale={width}:{height}:force_original_aspect_ratio=increase,"
                    f"crop={width}:{height}[v_crop];"
                    
                    # Add subtitles
                    f"[v_crop]subtitles={subtitle_path_escaped}:"
                    f"force_style='FontName=Arial,FontSize={self.config.SUBTITLE_FONT_SIZE},"
                    f"Bold=1,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,"
                    f"BackColour=&H80000000,Outline=2,Shadow=1,MarginV=30,Alignment=2'[v];"
                    
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
                # WITHOUT MUSIC - Voice only
                logger.warning("Music has no audio, using voice only")
                filter_complex = (
                    # Scale and crop video
                    f"[0:v]scale={width}:{height}:force_original_aspect_ratio=increase,"
                    f"crop={width}:{height}[v_crop];"
                    
                    # Add subtitles
                    f"[v_crop]subtitles={subtitle_path_escaped}:"
                    f"force_style='FontName=Arial,FontSize={self.config.SUBTITLE_FONT_SIZE},"
                    f"Bold=1,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,"
                    f"BackColour=&H80000000,Outline=2,Shadow=1,MarginV=30,Alignment=2'[v];"
                    
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
            
            logger.info("Running FFmpeg with looped video and audio...")
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

