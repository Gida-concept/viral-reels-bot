import os
from groq import Groq
from utils.logger import setup_logger

logger = setup_logger()


class StoryGenerator:
    """Generates viral stories using Groq API"""

    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
        self.model = "mixtral-8x7b-32768"

    def generate_story(self, category: str) -> dict:
        """
        Generate a unique, viral story for the given category

        Returns:
            dict: {'title': str, 'story': str}
        """
        logger.info(f"Generating story for category: {category}")

        prompt = self._create_prompt(category)

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a master storyteller who creates viral, emotionally engaging short-form stories for social media. Your stories are unique, non-generic, and designed for maximum retention."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=self.model,
                temperature=1.2,
                max_tokens=2000
            )

            response = chat_completion.choices[0].message.content
            story_data = self._parse_response(response)

            logger.info(f"Story generated successfully: {story_data['title'][:50]}...")
            return story_data

        except Exception as e:
            logger.error(f"Error generating story: {e}")
            raise

    def _create_prompt(self, category: str) -> str:
        """Create dynamic prompt for story generation"""
        return f"""Create a highly unique and viral story for the category: {category}

Requirements:
1. Length: 2-5 minutes when spoken naturally (approximately 300-750 words)
2. Style: Extremely engaging, high-retention, emotional hooks
3. Structure: 
   - Unique opening (never use generic "Once upon a time" or "Let me tell you about")
   - Compelling middle with twists
   - Powerful ending (avoid cliché morals)
4. Tone: Natural, conversational, perfect for voice narration
5. Uniqueness: This must be 100% original, never generic

Category focus: {category}

Output format (exactly):
Title: [Compelling title]

Story:
[Your story here - write in natural spoken language, use short sentences, include emotional beats]

Make it unforgettable. Begin now:"""

    def _parse_response(self, response: str) -> dict:
        """Parse the Groq API response into title and story"""
        lines = response.strip().split('\n')

        title = ""
        story_lines = []
        story_started = False

        for line in lines:
            if line.startswith('Title:'):
                title = line.replace('Title:', '').strip()
            elif line.startswith('Story:'):
                story_started = True
            elif story_started:
                story_lines.append(line)

        story = '\n'.join(story_lines).strip()

        if not title or not story:
            # Fallback parsing
            parts = response.split('\n\n', 1)
            if len(parts) == 2:
                title = parts[0].replace('Title:', '').strip()
                story = parts[1].replace('Story:', '').strip()
            else:
                title = "Untitled Story"
                story = response

        return {
            'title': title,
            'story': story
        }