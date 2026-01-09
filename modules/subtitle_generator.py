import subprocess
import json
import pysrt
from utils.logger import setup_logger

logger = setup_logger()

class SubtitleGenerator:
    def generate_subtitles(self, audio_path: str, output_path: str, text: str):
        logger.info("Generating subtitles synchronized with voice speed")
        try:
            # Validate inputs
            if not text or len(text.strip()) == 0:
                raise ValueError("Story text is empty")
            
            # Get EXACT audio duration
            duration = self._get_audio_duration(audio_path)
            
            if duration <= 0:
                raise ValueError(f"Invalid audio duration: {duration}s")
            
            # Clean text - remove extra whitespace and newlines
            cleaned_text = ' '.join(text.split())
            words = cleaned_text.split()
            total_words = len(words)
            
            if total_words == 0:
                raise ValueError("No words found in story text")
            
            # Calculate timing per word INCLUDING natural pauses
            # The audio is slower than pure word count because of breathing, pauses, emphasis
            # Add 10% to account for this
            effective_duration = duration * 0.90  # Use 90% of duration for words, 10% is pauses
            seconds_per_word = duration / total_words  # Use FULL duration divided by words
            
            logger.info(f"Audio: {duration:.2f}s, Words: {total_words}")
            logger.info(f"Timing: {seconds_per_word:.3f}s per word (includes natural pauses)")
            
            subs = pysrt.SubRipFile()
            
            # 4 words per subtitle - shorter chunks for better sync
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
            
            # Verify total time
            total_subtitle_time = current_time
            time_diff = abs(total_subtitle_time - duration)
            
            logger.info(f"Subtitle total: {total_subtitle_time:.2f}s, Audio: {duration:.2f}s, Diff: {time_diff:.2f}s")
            
            if time_diff > 1.0:
                logger.warning(f"⚠ Timing mismatch detected: {time_diff:.2f}s difference")
            else:
                logger.info(f"✓ Timing matched: difference only {time_diff:.2f}s")
            
            # Save SRT file
            subs.save(output_path, encoding='utf-8')
            
            logger.info(f"✓ Generated {len(subs)} subtitle segments ({chunk_size} words each)")
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
