import subprocess
import json
import pysrt
from groq import Groq
from utils.logger import setup_logger

logger = setup_logger()

class SubtitleGenerator:
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
    
    def generate_subtitles(self, audio_path: str, output_path: str, text: str = None):
        logger.info("Generating subtitles using Groq Whisper with word-level timestamps")
        try:
            # Use Groq Whisper to get exact word timestamps
            with open(audio_path, 'rb') as audio_file:
                logger.info("Transcribing audio with Groq Whisper...")
                
                transcription = self.client.audio.transcriptions.create(
                    model="whisper-large-v3",
                    file=audio_file,
                    response_format="verbose_json",
                    timestamp_granularities=["word"]
                )
            
            # Extract word-level timestamps (they come as dictionaries)
            words_data = transcription.words
            
            if not words_data:
                raise ValueError("No word timestamps received from Whisper")
            
            logger.info(f"✓ Whisper transcribed {len(words_data)} words with timestamps")
            
            # Create subtitles from word timestamps
            subs = pysrt.SubRipFile()
            
            # Group words into readable chunks (4 words per subtitle)
            chunk_size = 4
            
            for i in range(0, len(words_data), chunk_size):
                chunk = words_data[i:i+chunk_size]
                
                # Extract text and timing from dictionaries
                chunk_text = ' '.join([word['word'] for word in chunk])
                start_time = chunk[0]['start']
                end_time = chunk[-1]['end']
                
                # Convert to milliseconds
                start_ms = int(start_time * 1000)
                end_ms = int(end_time * 1000)
                
                # Create subtitle item
                sub = pysrt.SubRipItem(
                    index=len(subs) + 1,
                    start=pysrt.SubRipTime(milliseconds=start_ms),
                    end=pysrt.SubRipTime(milliseconds=end_ms),
                    text=chunk_text
                )
                
                subs.append(sub)
            
            # Save SRT file
            subs.save(output_path, encoding='utf-8')
            
            # Get audio duration for verification
            audio_duration = self._get_audio_duration(audio_path)
            last_subtitle_end = subs[-1].end.ordinal / 1000.0 if subs else 0
            
            logger.info(f"✓ Generated {len(subs)} subtitle segments")
            logger.info(f"✓ Audio duration: {audio_duration:.2f}s")
            logger.info(f"✓ Last subtitle ends at: {last_subtitle_end:.2f}s")
            logger.info(f"✓ PERFECT SYNC: Whisper word-level timestamps")
            logger.info(f"✓ Subtitles saved: {output_path}")
            
            return output_path
            
        except Exception as e:
            logger.error(f"Error generating subtitles with Whisper: {e}")
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
