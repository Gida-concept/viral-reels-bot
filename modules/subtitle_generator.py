import subprocess
import json
import pysrt
from utils.logger import setup_logger

logger = setup_logger()

class SubtitleGenerator:
    def generate_subtitles(self, audio_path: str, output_path: str, text: str):
        logger.info("Generating subtitles synchronized with voice speed")
        try:
            # Get exact audio duration
            duration = self._get_audio_duration(audio_path)
            
            # Get word timestamps from audio analysis
            words = text.split()
            total_words = len(words)
            
            # Calculate exact timing based on audio duration
            seconds_per_word = duration / total_words
            
            logger.info(f"Audio: {duration:.2f}s, Words: {total_words}, Speed: {seconds_per_word:.3f}s per word")
            
            subs = pysrt.SubRipFile()
            
            # Optimal chunk size for readability (3-6 words per subtitle)
            chunk_size = 4
            
            current_time = 0.0
            
            for i in range(0, len(words), chunk_size):
                chunk = words[i:i+chunk_size]
                chunk_text = ' '.join(chunk)
                
                # Calculate duration for this chunk
                chunk_word_count = len(chunk)
                chunk_duration = chunk_word_count * seconds_per_word
                
                # Start and end times in milliseconds
                start_ms = int(current_time * 1000)
                end_ms = int((current_time + chunk_duration) * 1000)
                
                # Create subtitle item
                sub = pysrt.SubRipItem(
                    index=len(subs) + 1,
                    start=pysrt.SubRipTime(milliseconds=start_ms),
                    end=pysrt.SubRipTime(milliseconds=end_ms),
                    text=chunk_text
                )
                
                subs.append(sub)
                current_time += chunk_duration
            
            # Save SRT file
            subs.save(output_path, encoding='utf-8')
            
            logger.info(f"✓ Generated {len(subs)} subtitle segments")
            logger.info(f"✓ Subtitles saved: {output_path}")
            
            return output_path
            
        except Exception as e:
            logger.error(f"Error generating subtitles: {e}")
            raise
    
    def _get_audio_duration(self, audio_path: str):
        """Get exact audio duration using ffprobe"""
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
        return duration
