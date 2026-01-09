from groq import Groq
from utils.logger import setup_logger
import random

logger = setup_logger()

class StoryGenerator:
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"
        self.used_openings = []  # Track used opening styles
    
    def generate_story(self, category: str):
        logger.info(f"Generating story for: {category}")
        
        # Get a unique opening style
        opening_style = self._get_unique_opening_style()
        
        prompt = self._create_unique_prompt(category, opening_style)
        
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system", 
                        "content": """You are an award-winning storyteller known for SHOCKING plot twists and unconventional narratives. 
                        Your stories break ALL traditional patterns. You NEVER use clichés. 
                        Every story must have an element that makes people say "I did NOT see that coming!"
                        Write in a raw, authentic voice like you're telling a friend the craziest thing that just happened.
                        NEVER repeat the same opening style twice."""
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                model=self.model,
                temperature=1.4,
                max_tokens=2000,
                top_p=0.95
            )
            
            result = self._parse_response(response.choices[0].message.content)
            logger.info(f"Story generated: {result['title']}")
            logger.info(f"Opening style used: {opening_style}")
            return result
        except Exception as e:
            logger.error(f"Error generating story: {e}")
            raise
    
    def _get_unique_opening_style(self):
        """Get a unique opening style that hasn't been used recently"""
        
        opening_styles = [
            "Start with a shocking statement that makes no sense until later",
            "Open with rapid-fire dialogue between two people arguing",
            "Begin with a countdown (3 minutes until...)",
            "Start with 'Nobody believed me when I said...'",
            "Open with a text message or email that changes everything",
            "Begin with the character doing something completely unexpected",
            "Start with 'The third time I died...' (or similar absurd count)",
            "Open with a sound effect or sensory detail",
            "Begin mid-conversation without context",
            "Start with a question the reader can't answer",
            "Open with 'Here's what they don't tell you about...'",
            "Begin with the exact moment everything changed",
            "Start with a lie the character is telling",
            "Open with a memory that turns out to be false",
            "Begin with 'I should have known when...'",
            "Start with an impossible situation presented as normal",
            "Open with numbers or statistics that seem random",
            "Begin with 'Everyone has a price. Mine was...'",
            "Start with the character waking up somewhere impossible",
            "Open with 'The rules were simple:'",
            "Begin with weather or time doing something unusual",
            "Start with 'They say (something), but they're wrong about...'",
            "Open with a smell, taste, or touch sensation",
            "Begin with 'I'd seen it before, but never like this'",
            "Start with what the character is holding in their hands",
            "Open with 'The difference between (X) and (Y) is...'",
            "Begin with someone's last words",
            "Start with 'Three things happened simultaneously:'",
            "Open with a price tag, receipt, or transaction",
            "Begin with 'My biggest mistake was thinking...'",
            "Start with a door opening/closing at wrong time",
            "Open with 'Nobody noticed when...'",
            "Begin with a number getting called/announced",
            "Start with 'It started as a joke'",
            "Open with 'The first sign was...'",
            "Begin with an interrupted action",
            "Start with 'I wasn't supposed to see...'",
            "Open with someone missing or appearing",
            "Begin with 'The phone call came at...'",
            "Start with a choice between two impossible options"
        ]
        
        # Remove recently used openings from options
        available_styles = [s for s in opening_styles if s not in self.used_openings]
        
        # If we've used them all, reset
        if not available_styles:
            self.used_openings = []
            available_styles = opening_styles
        
        # Pick random style
        chosen_style = random.choice(available_styles)
        
        # Track it
        self.used_openings.append(chosen_style)
        
        # Keep only last 20 to allow eventual reuse
        if len(self.used_openings) > 20:
            self.used_openings.pop(0)
        
        return chosen_style
    
    def _create_unique_prompt(self, category: str, opening_style: str):
        """Create dynamic prompts that force unique perspectives"""
        
        unique_angles = {
            'love': [
                "Tell a love story where the couple NEVER actually meets in person",
                "A love story told entirely from the perspective of a wedding ring",
                "Two people fall in love through competing to destroy each other's business",
                "A love story where one person is from the future, visiting for just 3 hours"
            ],
            'help': [
                "Someone's act of 'help' accidentally ruins everything, but ends up being the best thing that happened",
                "A stranger helps you, then you discover they're your future self",
                "The person begging for help is actually the one helping YOU without you knowing",
                "Helping a stranger triggers a chain reaction that saves your life 10 years later"
            ],
            'money': [
                "Someone finds a million dollars but realizes keeping it will cost them everything",
                "A poor person discovers rich people are secretly paying them to stay poor",
                "Money starts appearing every time they do something morally questionable",
                "They become a millionaire overnight but can never tell anyone or spend it publicly"
            ],
            'partnership': [
                "Business partners who hate each other discover they're controlling the same body",
                "A partnership formed by two enemies to take down someone they both hate",
                "Partners in crime realize they've been planning to betray each other on the same day",
                "Two rivals forced to partner, but one of them doesn't actually exist"
            ],
            'dating': [
                "Dating someone who can read minds, but only YOUR thoughts",
                "Every date you go on, you wake up living that person's life",
                "Dating in a world where lies manifest as physical objects",
                "Going on a date with someone who is simultaneously dating your parallel universe self"
            ],
            'relationship': [
                "A relationship where both people are keeping the EXACT same secret",
                "They've been in a relationship for years, but one of them is a time traveler reliving the same year",
                "A relationship told backwards, starting with the breakup",
                "Two people in a relationship realize they're characters in each other's dreams"
            ],
            'poor': [
                "Being poor saved their life when being rich would have killed them",
                "A poor person discovers they're actually wealthy, but their mind was altered",
                "Poverty as a social experiment by billionaires, and they just found out",
                "Poor by choice: someone who had billions and gave it ALL away for a bizarre reason"
            ],
            'disease': [
                "A disease that makes you experience other people's memories",
                "Getting sick reveals you've been living in a simulation",
                "A disease that only affects people who've never told a lie",
                "The cure for the disease is worse than dying from it, but no one knows why"
            ],
            'brilliant': [
                "A genius who realizes their intelligence is actually a curse from their future self",
                "The smartest person alive discovers intelligence is a virus",
                "A brilliant mind that can solve any problem, except their own",
                "Genius-level intelligence that only works when they're completely wrong about everything"
            ],
            'student': [
                "A student who's actually been the teacher all along, but doesn't know it",
                "Learning erases memories: the more you know, the more you forget who you are",
                "A student discovers they're teaching their teacher without realizing it",
                "Failing student is actually passing every test in an alternate dimension"
            ],
            'high school': [
                "High school where popularity is determined by an algorithm students can't see",
                "A high school that exists in a time loop, repeating the same day",
                "Students discover their school is actually a test facility",
                "High school drama that's actually controlling world events"
            ],
            'middle school': [
                "Middle school where kids are secretly running the town",
                "A middle schooler discovers adults can't see certain things they can",
                "Middle school friendship that's actually a scientific experiment",
                "Being the new kid reveals everyone else is stuck in middle school forever"
            ],
            'kids': [
                "Kids who realize parents are the ones who need parenting",
                "Children with a secret language adults used to speak but forgot",
                "A kid who can see everyone's expiration date",
                "Kids running a business their parents don't know about"
            ],
            'business': [
                "A business that accidentally becomes successful by doing everything wrong",
                "Starting a business to fail, but it becomes a billion-dollar empire",
                "A company where employees don't know they're actually prisoners",
                "Business partners discover their success is destroying reality itself"
            ],
            'christian': [
                "A prayer that gets answered in the most unexpected, twisted way",
                "Someone's faith is tested by getting exactly what they prayed for",
                "A miracle that everyone thinks is a curse",
                "Finding God in the last place anyone would look"
            ],
            'religion': [
                "All religions are right, but not in the way anyone expected",
                "A religious experience that makes someone question everything",
                "Sacred text that means the opposite of what everyone thinks",
                "A prophet who doesn't want to be one"
            ],
            'bible': [
                "A Bible verse that comes true in modern day, literally",
                "Reading the Bible backwards reveals a hidden message",
                "A biblical story retold from the villain's perspective",
                "Finding a page in the Bible that isn't supposed to exist"
            ],
            'crime': [
                "A criminal who steals from criminals, but discovers they're stealing from themselves",
                "Committing crimes in dreams that affect real life",
                "A heist where the victim planned the entire robbery",
                "The perfect crime that accidentally saves the victim's life"
            ],
            'action': [
                "An action hero who wins by doing absolutely nothing",
                "A high-speed chase in reverse",
                "Action sequence where the hero is trying NOT to fight",
                "The villain and hero realize they're on the same side"
            ],
            'drug': [
                "A drug that makes you experience your worst fear, but cures you",
                "Addiction to something that isn't actually a drug",
                "A drug dealer who's actually saving lives",
                "Drugs that let you steal other people's talents"
            ],
            'mafia': [
                "A mafia family that's actually protecting people from something worse",
                "Going undercover in the mafia, but the mafia knows the whole time",
                "A mafia boss who wants to quit but can't",
                "The mafia versus an even more dangerous enemy: HOA"
            ],
            'tech': [
                "Technology that allows you to delete people from existence, but you forget them too",
                "An AI that becomes sentient and chooses to be stupid",
                "Creating technology that runs on human regret",
                "A device that shows you every decision you didn't make"
            ],
            'robotics': [
                "A robot that's more human than the humans",
                "Creating a robot to replace you, then it does it too well",
                "Robots that feel pain and decide to feel it on purpose",
                "A robot uprising that's actually justified"
            ],
            'superpowers': [
                "A superpower that's actually a disability in disguise",
                "Everyone gets powers except one person, who becomes the most powerful",
                "Superpowers that only work when nobody's watching",
                "A hero whose power is making everyone around them normal"
            ],
            'fantasy': [
                "Magic exists but it's the most boring, mundane thing in the world",
                "A fantasy world where the 'chosen one' refuses and someone random has to save the world",
                "Dragons are real, but they're accountants and financial advisors",
                "A magical curse that makes everyone believe you're lying when you tell the truth"
            ]
        }
        
        # Get random unique angle for category
        angles = unique_angles.get(category, [
            f"Tell a {category} story but from the LEAST expected perspective",
            f"A {category} story where the biggest twist is that there's no villain",
            f"A {category} story that starts at the end and makes sense by going backwards"
        ])
        
        chosen_angle = random.choice(angles)
        
        return f"""Create an INCREDIBLY UNIQUE and SHOCKING story using this angle:

{chosen_angle}

MANDATORY OPENING STYLE (you MUST use this exact approach):
{opening_style}

CRITICAL RULES:
❌ BANNED PHRASES: "once upon a time", "little did they know", "what they didn't realize", "it all started when", "one day", "there was a"
❌ NO predictable endings or life lessons
❌ NO typical hero's journey
❌ NO obvious foreshadowing
❌ DO NOT start with character descriptions or setting exposition
✅ Jump IMMEDIATELY into the action/situation using the opening style above
✅ Include a twist that genuinely surprises
✅ Use raw, conversational language - write how people actually talk
✅ Make it 300-600 words for 2-4 minute narration
✅ End with something that makes people think "WHAT?!"

Format EXACTLY as:
Title: [A mysterious, intriguing title - NOT generic]

Story:
[Your raw, unique story - USE THE OPENING STYLE SPECIFIED ABOVE]

Make it UNFORGETTABLE. Begin NOW:"""
    
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
            first_lines = response.strip().split('\n')
            for line in first_lines:
                if line.strip() and not line.startswith('Title:') and not line.startswith('Story:'):
                    title = line.strip()[:100]
                    break
            
            if not title:
                title = f"The Untold Truth"
        
        if not story:
            story = response.replace('Title:', '').replace('Story:', '').strip()
        
        logger.info(f"Parsed - Title: '{title}', Story length: {len(story)} chars")
        
        return {'title': title, 'story': story}
