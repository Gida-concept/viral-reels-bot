import subprocess
import os
import json
from utils.logger import setup_logger

logger = setup_logger()


class VideoAssembler:
    """Assembles final video using FFmpeg"""

    def __init__(self, config):
        self.config = config

    def assemble_video(
            self,
            video_path: str,
            audio_path: str,
            music_path: str,
            subtitle_path: str,
            output_path: str
    ) -> str:
        """
        Assemble final video with all components

        Args:
            video_path: Background video
            audio_path: Voice narration
            music_path: Background music
            subtitle_path: SRT subtitles
            output_path: Final output video

        Returns:
            str: Path to final video
        """
        logger.info("Assembling final video")

        try:
            # Get durations
            audio_duration = self._get_duration(audio_path)
            video_duration = self._get_duration(video_path)

            logger.info(f"Audio duration: {audio_duration:.2f}s, Video duration: {video_duration:.2f}s")

            # Determine resolution
            if self.config.ENABLE_UPSCALE:
                width, height = self.config.UPSCALE_RESOLUTION
            else:
                width, height = self.config.OUTPUT_RESOLUTION

            # Build FFmpeg command
            cmd = [
                'ffmpeg',
                '-y',  # Overwrite output
                '-stream_loop', '-1',  # Loop video if needed
                '-i', video_path,
                '-i', audio_path,
                '-i', music_path,
                '-filter_complex',
                self._build_filter_complex(audio_duration, video_duration, width, height, subtitle_path),
                '-t', str(audio_duration),  # Duration = audio length
                '-c:v', 'libx264',
                '-preset', 'medium',
                '-crf', '23',
                '-c:a', 'aac',
                '-b:a', '128k',
                '-movflags', '+faststart',
                output_path
            ]

            logger.info("Running FFmpeg...")

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )

            if not os.path.exists(output_path):
                raise FileNotFoundError(f"Output video not created: {output_path}")

            logger.info(f"Video assembled successfully: {output_path}")
            return output_path

        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg error: {e.stderr}")
            raise
        except Exception as e:
            logger.error(f"Error assembling video: {e}")
            raise

    def _build_filter_complex(
            self,
            audio_duration: float,
            video_duration: float,
            width: int,
            height: int,
            subtitle_path: str
    ) -> str:
        """Build FFmpeg filter_complex for video processing"""

        # Escape subtitle path for FFmpeg
        subtitle_path_escaped = subtitle_path.replace('\\', '/').replace(':', '\\:')

        filter_parts = [
            # Video processing: scale, crop to vertical, trim/loop
            f"[0:v]scale={width}:{height}:force_original_aspect_ratio=increase,crop={width}:{height}[v]",

            # Audio mixing: boost voice to 110%, set music to 20%
            f"[1:a]volume={self.config.VOICE_VOLUME_BOOST}[voice]",
            f"[2:a]volume={self.config.MUSIC_VOLUME}[music]",
            f"[voice][music]amix=inputs=2:duration=first[a]",

            # Add subtitles
            f"[v]subtitles={subtitle_path_escaped}:force_style='FontSize={self.config.SUBTITLE_FONT_SIZE}'[vout]"
        ]

        return ';'.join(filter_parts)

    def _get_duration(self, file_path: str) -> float:
        """Get media file duration using ffprobe"""
        try:
            cmd = [
                'ffprobe',
                '-v', 'error',
                '-show_entries', 'format=duration',
                '-of', 'json',
                file_path
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            data = json.loads(result.stdout)
            return float(data['format']['duration'])

        except Exception as e:
            logger.error(f"Error getting duration for {file_path}: {e}")
            raise