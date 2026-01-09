import subprocess
import json
import pysrt
from datetime import timedelta
from utils.logger import setup_logger

logger = setup_logger()


class SubtitleGenerator:
    """Generates synchronized SRT subtitles from audio"""

    def __init__(self):
        pass

    def generate_subtitles(self, audio_path: str, output_path: str, text: str) -> str:
        """
        Generate SRT subtitles synchronized with audio

        Args:
            audio_path: Path to audio file
            output_path: Path to save SRT file
            text: Original text for reference

        Returns:
            str: Path to generated SRT file
        """
        logger.info("Generating synchronized subtitles")

        try:
            # Get audio duration
            duration = self._get_audio_duration(audio_path)

            # Split text into subtitle chunks
            words = text.split()

            # Calculate timing
            words_per_second = len(words) / duration

            # Create subtitles
            subs = pysrt.SubRipFile()

            chunk_size = 5  # Words per subtitle
            start_time = 0

            for i in range(0, len(words), chunk_size):
                chunk = words[i:i + chunk_size]
                chunk_text = ' '.join(chunk)

                chunk_duration = len(chunk) / words_per_second
                end_time = start_time + chunk_duration

                sub = pysrt.SubRipItem(
                    index=len(subs) + 1,
                    start=timedelta(seconds=start_time),
                    end=timedelta(seconds=end_time),
                    text=chunk_text
                )

                subs.append(sub)
                start_time = end_time

            # Save SRT file
            subs.save(output_path, encoding='utf-8')

            logger.info(f"Subtitles generated: {len(subs)} segments")
            return output_path

        except Exception as e:
            logger.error(f"Error generating subtitles: {e}")
            raise

    def _get_audio_duration(self, audio_path: str) -> float:
        """Get audio duration in seconds using ffprobe"""
        try:
            cmd = [
                'ffprobe',
                '-v', 'error',
                '-show_entries', 'format=duration',
                '-of', 'json',
                audio_path
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            data = json.loads(result.stdout)
            duration = float(data['format']['duration'])

            logger.info(f"Audio duration: {duration:.2f}s")
            return duration

        except Exception as e:
            logger.error(f"Error getting audio duration: {e}")
            raise