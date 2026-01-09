import subprocess
import json
import pysrt
from utils.logger import setup_logger

logger = setup_logger()

class SubtitleGenerator:
    def generate_subtitles(self, audio_path: str, output_path: str, text: str):
        logger.info("Generating subtitles")
        try:
            duration = self._get_audio_duration(audio_path)
            words = text.split()
            words_per_second = len(words) / duration
            
            subs = pysrt.SubRipFile()
            chunk_size = 5
            start_time = 0
            
            for i in range(0, len(words), chunk_size):
                chunk = words[i:i+chunk_size]
                chunk_text = ' '.join(chunk)
                chunk_duration = len(chunk) / words_per_second
                end_time = start_time + chunk_duration
                
                # Convert seconds to SubRipTime format
                start_ms = int(start_time * 1000)
                end_ms = int(end_time * 1000)
                
                sub = pysrt.SubRipItem(
                    index=len(subs) + 1,
                    start=pysrt.SubRipTime(milliseconds=start_ms),
                    end=pysrt.SubRipTime(milliseconds=end_ms),
                    text=chunk_text
                )
                subs.append(sub)
                start_time = end_time
            
            subs.save(output_path, encoding='utf-8')
            logger.info(f"Subtitles saved: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Error generating subtitles: {e}")
            raise
    
    def _get_audio_duration(self, audio_path: str):
        cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'json', audio_path]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        return float(data['format']['duration'])
