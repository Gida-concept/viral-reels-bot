from groq import Groq
from utils.logger import setup_logger

logger = setup_logger()

class StoryGenerator:
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"  # Best for creative stories
    
    def generate_story(self, category: str):
        logger.info(f"Generating story for: {category}")
        
        prompt = f"""Create a unique viral story for: {category}

Requirements:
- 2-5 minutes when spoken (300-750 words)
- Extremely engaging, high-retention
- Natural conversational tone
- No generic openings or endings
- 100% original

Format:
Title: [Title here]

Story:
[Story here]"""

        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a master storyteller creating viral social media stories."},
                    {"role": "user", "content": prompt}
                ],
                model=self.model,
                temperature=1.2,
                max_tokens=2000
            )
            
            result = self._parse_response(response.choices[0].message.content)
            logger.info(f"Story generated: {result['title']}")
            return result
        except Exception as e:
            logger.error(f"Error generating story: {e}")
            raise
    
    def _parse_response(self, response: str):
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
        
        if not title:
            title = "Untitled Story"
        if not story:
            story = response
        
        return {'title': title, 'story': story}

