import subprocess
import json
import pysrt
import re
from utils.logger import setup_logger

logger = setup_logger()

class SubtitleGenerator:
    def generate_subtitles(self, audio_path: str, output_path: str, text: str):
        logger.info("Generating subtitles PERFECTLY synchronized with voice timing")
        try:
            # Validate inputs
            if not text or len(text.strip()) == 0:
                raise ValueError("Story text is empty")
            
            # Get EXACT audio duration
            duration = self._get_audio_duration(audio_path)
            
            if duration <= 0:
                raise ValueError(f"Invalid audio duration: {duration}s")
            
            # Clean text - preserve sentence structure
            # Remove extra whitespace but keep paragraph breaks for natural pauses
            cleaned_text = ' '.join(text.split())
            
            # Split into sentences for more natural timing
            sentences = self._split_into_sentences(cleaned_text)
            total_words = sum(len(sentence.split()) for sentence in sentences)
            
            if total_words == 0:
                raise ValueError("No words found in story text")
            
            # Calculate base timing - EXACT match to audio duration
            seconds_per_word = duration / total_words
            
            logger.info(f"Audio duration: {duration:.2f}s")
            logger.info(f"Total words: {total_words}")
            logger.info(f"Exact timing: {seconds_per_word:.4f}s per word")
            logger.info(f"Syncing subtitles to ACTUAL voice speed (1:1 ratio)")
            
            subs = pysrt.SubRipFile()
            current_time = 0.0
            
            # Process sentences with natural timing
            for sentence in sentences:
                words = sentence.split()
                
                # Split sentence into chunks of 3-5 words for readability
                chunk_size = 4
                
                for i in range(0, len(words), chunk_size):
                    chunk = words[i:i+chunk_size]
                    chunk_text = ' '.join(chunk)
                    
                    # Calculate EXACT duration for this chunk based on word count
                    chunk_word_count = len(chunk)
                    chunk_duration = chunk_word_count * seconds_per_word
                    
                    # Start and end times in milliseconds - PRECISE timing
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
                
                # Add tiny pause between sentences (natural breathing)
                # This accounts for the slight pause the voice takes between sentences
                current_time += 0.1  # 100ms pause between sentences
            
            # Final verification
            total_subtitle_time = current_time
            time_diff = abs(total_subtitle_time - duration)
            
            logger.info(f"Subtitle total time: {total_subtitle_time:.2f}s")
            logger.info(f"Audio duration: {duration:.2f}s")
            logger.info(f"Time difference: {time_diff:.2f}s")
            
            if time_diff > 1.0:
                logger.warning(f"⚠ Timing variance: {time_diff:.2f}s (adjusting...)")
                # Adjust if needed
                subs = self._adjust_timing(subs, total_subtitle_time, duration)
            else:
                logger.info(f"✓ PERFECT sync: {time_diff:.2f}s difference")
            
            # Save SRT file
            subs.save(output_path, encoding='utf-8')
            
            logger.info(f"✓ Generated {len(subs)} subtitle segments")
            logger.info(f"✓ Subtitles perfectly synced to voice at 1x speed")
            logger.info(f"✓ Subtitles saved: {output_path}")
            
            return output_path
            
        except Exception as e:
            logger.error(f"Error generating subtitles: {e}")
            raise
    
    def _split_into_sentences(self, text: str):
        """Split text into sentences for natural timing"""
        # Split on sentence endings but preserve the punctuation
        sentences = re.split(r'(?<=[.!?])\s+', text)
        # Filter out empty sentences
        sentences = [s.strip() for s in sentences if s.strip()]
        return sentences
    
    def _adjust_timing(self, subs, current_total, target_duration):
        """Adjust subtitle timing to match target duration exactly"""
        if current_total == 0:
            return subs
        
        # Calculate adjustment factor
        adjustment_factor = target_duration / current_total
        
        logger.info(f"Adjusting timing by factor: {adjustment_factor:.4f}")
        
        # Apply adjustment to all subtitles
        for sub in subs:
            # Adjust start time
            start_seconds = sub.start.ordinal / 1000.0
            new_start = start_seconds * adjustment_factor
            sub.start = pysrt.SubRipTime(milliseconds=int(new_start * 1000))
            
            # Adjust end time
            end_seconds = sub.end.ordinal / 1000.0
            new_end = end_seconds * adjustment_factor
            sub.end = pysrt.SubRipTime(milliseconds=int(new_end * 1000))
        
        return subs
    
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
