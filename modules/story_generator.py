from groq import Groq
from utils.logger import setup_logger

logger = setup_logger()

class StoryGenerator:
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"
    
    def generate_story(self, category: str):
        logger.info(f"Generating story for: {category}")
        
        prompt = f"""Create a unique viral story for the category: {category}

Requirements:
- Length: 2-5 minutes when spoken (300-750 words)
- Extremely engaging and emotional
- Natural conversational tone
- No generic openings like "once upon a time"
- 100% original content

You MUST format your response EXACTLY like this:

Title: [Your compelling title here]

Story:
[Your complete story here in natural spoken language]

Begin now:"""

        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a master storyteller creating viral social media stories. Always start with 'Title:' on the first line."},
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
            line_stripped = line.strip()
            
            if line_stripped.startswith('Title:'):
                title = line_stripped.replace('Title:', '').strip()
            elif line_stripped.startswith('Story:'):
                story_started = True
            elif story_started and line_stripped:
                story_lines.append(line_stripped)
        
        story = '\n'.join(story_lines).strip()
        
        # Fallback if parsing fails
        if not title:
            # Try to extract first line as title
            first_lines = response.strip().split('\n')
            for line in first_lines:
                if line.strip() and not line.startswith('Title:') and not line.startswith('Story:'):
                    title = line.strip()[:100]
                    break
            
            if not title:
                title = f"A Story About {category.title()}"
        
        if not story:
            # Use everything after "Story:" or just the response
            story = response.replace('Title:', '').replace('Story:', '').strip()
        
        logger.info(f"Parsed - Title: '{title}', Story length: {len(story)} chars")
        
        return {'title': title, 'story': story}
