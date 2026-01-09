import asyncio
import edge_tts
import os
from utils.logger import setup_logger

logger = setup_logger()

class VoiceGenerator:
    def __init__(self, voice: str = 'en-US-AndrewNeural'):  # More natural voice
        self.voice = voice
        # Rate: slightly slower for better clarity
        # Pitch: default
        self.rate = '-5%'  # Slightly slower than normal
        self.volume = '+0%'  # Normal volume (we boost later in FFmpeg)
    
    async def _generate_async(self, text: str, output_path: str):
        try:
            # Use communicate with prosody for more natural speech
            communicate = edge_tts.Communicate(
                text, 
                self.voice,
                rate=self.rate,
                volume=self.volume
            )
            await communicate.save(output_path)
        except Exception as e:
            # Fallback to alternative natural voice
            logger.warning(f"Failed with {self.voice}, trying alternative...")
            alternative_voice = 'en-US-GuyNeural'
            communicate = edge_tts.Communicate(
                text, 
                alternative_voice,
                rate=self.rate,
                volume=self.volume
            )
            await communicate.save(output_path)
    
    def generate_voice(self, text: str, output_path: str):
        logger.info(f"Generating natural voice narration with {self.voice}")
        try:
            asyncio.run(self._generate_async(text, output_path))
            
            if not os.path.exists(output_path):
                raise FileNotFoundError(f"Voice file not created: {output_path}")
            
            logger.info(f"Voice saved: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Error generating voice: {e}")
            raise
