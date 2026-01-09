import asyncio
import edge_tts
import os
from utils.logger import setup_logger

logger = setup_logger()

class VoiceGenerator:
    def __init__(self, voice: str = 'en-US-AndrewNeural'):
        self.voice = voice
        self.rate = '-5%'
        self.volume = '+0%'
    
    async def _generate_async(self, text: str, output_path: str):
        try:
            # Use updated edge-tts API
            communicate = edge_tts.Communicate(
                text=text,
                voice=self.voice,
                rate=self.rate,
                volume=self.volume
            )
            await communicate.save(output_path)
        except Exception as e:
            # Try multiple fallback voices
            logger.warning(f"Failed with {self.voice}: {e}")
            
            fallback_voices = [
                'en-US-GuyNeural',
                'en-US-ChristopherNeural',
                'en-US-EricNeural',
                'en-US-BrianNeural'
            ]
            
            for fallback_voice in fallback_voices:
                try:
                    logger.info(f"Trying fallback voice: {fallback_voice}")
                    communicate = edge_tts.Communicate(
                        text=text,
                        voice=fallback_voice,
                        rate=self.rate,
                        volume=self.volume
                    )
                    await communicate.save(output_path)
                    logger.info(f"Success with {fallback_voice}")
                    return
                except Exception as fallback_error:
                    logger.warning(f"Failed with {fallback_voice}: {fallback_error}")
                    continue
            
            raise Exception("All voice generation attempts failed")
    
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
