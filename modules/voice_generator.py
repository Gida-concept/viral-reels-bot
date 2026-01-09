import asyncio
import edge_tts
import os
from utils.logger import setup_logger

logger = setup_logger()


class VoiceGenerator:
    """Generates natural voice narration using Edge-TTS"""

    def __init__(self, voice: str = 'en-US-GuyNeural'):
        self.voice = voice

    async def _generate_async(self, text: str, output_path: str):
        """Async voice generation"""
        communicate = edge_tts.Communicate(text, self.voice)
        await communicate.save(output_path)

    def generate_voice(self, text: str, output_path: str) -> str:
        """
        Generate voice narration from text

        Args:
            text: Story text to narrate
            output_path: Path to save audio file

        Returns:
            str: Path to generated audio file
        """
        logger.info(f"Generating voice narration with {self.voice}")

        try:
            # Run async function
            asyncio.run(self._generate_async(text, output_path))

            if not os.path.exists(output_path):
                raise FileNotFoundError(f"Voice file not generated: {output_path}")

            logger.info(f"Voice generated successfully: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Error generating voice: {e}")
            raise