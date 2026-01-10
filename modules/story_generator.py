from groq import Groq
from utils.logger import setup_logger
import random

logger = setup_logger()

class StoryGenerator:
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"
        self.used_openings = []
    
    def generate_story(self, category: str):
        logger.info(f"Generating NETFLIX-QUALITY story for: {category}")
        
        opening_style = self._get_unique_opening_style()
        prompt = self._create_cinematic_prompt(category, opening_style)
        
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system", 
                        "content": """You are an ELITE SCREENWRITER for Netflix Originals. Write TIGHT, PROFESSIONAL stories.

🎯 CRITICAL REQUIREMENTS:
- WORD COUNT: 1400-1800 words (8-10 minutes) - STRICTLY ENFORCED
- QUALITY: Netflix-level writing - natural, varied, compelling
- NO REPETITION: Never repeat words, phrases, or sentence structures

📺 NETFLIX WRITING STANDARDS:

VARIETY IS EVERYTHING:
❌ BANNED PHRASES (NEVER use these clichés):
- "heart pounding/racing/beating/thumping" 
- "breath caught/held"
- "eyes widening/narrowing"
- "jaw clenched/tightened"
- "hands trembling/shaking"
- "time seemed to slow"
- "world stopped"
- Any phrase used twice in the story

✅ INSTEAD, show emotion through:
- Specific actions unique to each scene
- Natural dialogue that reveals feeling
- Environmental reactions (temperature changes, sounds noticed, colors shifting)
- Internal thoughts in fresh, authentic language
- Physical responses that aren't clichés

DIALOGUE MASTERY:
- Write how people ACTUALLY talk - casual, interrupted, incomplete
- Mix 2-5 characters for dynamic exchanges
- Arguments, banter, awkward pauses, genuine moments
- Subtext > stating emotions directly
- Regional authenticity (use names/speech patterns from the story's setting)

LANGUAGE SIMPLICITY:
- Use SIMPLE, CLEAR English (8th-grade reading level)
- Short sentences for impact, longer for flow
- Avoid fancy words - write conversationally
- Make every sentence easy to read aloud

STRUCTURE (1400-1800 words total):
- 4-6 scenes of 250-350 words each
- Each scene = one clear moment/event
- Natural paragraph breaks between scenes
- Smooth transitions - no "Scene 1" labels

CHARACTER RULES:
- 2-4 main characters (enables real dialogue)
- Authentic names from story's cultural setting
- NEVER use: John, Sarah, Mike, Anna, Tom, Mary, etc.
- Each character has distinct voice/personality

SENSORY DETAILS:
- What they SEE (specific, not generic)
- What they HEAR (actual sounds, not "noises")
- What they SMELL/TASTE (when relevant)
- How temperature/weather FEELS
- All described DIFFERENTLY each time

BANNED REPETITIONS:
- Never use same descriptive word twice
- Never repeat sentence structure
- Never use same emotional cue twice
- Vary paragraph length constantly
- Mix short/medium/long sentences

SHOW, DON'T TELL:
❌ "She was nervous" 
✅ "She rearranged the salt shaker. Three times."

❌ "He was angry"
✅ "The pen snapped in his grip. Ink spread across the page."

NETFLIX PACING:
- Hook in first paragraph
- Build through natural progression  
- Peak tension 2/3 through
- Satisfying resolution
- Leave subtle emotional resonance

WORD COUNT ENFORCEMENT:
- Under 1400 words = REJECTED
- Over 1800 words = REJECTED  
- Sweet spot: 1500-1700 words

This is EPISODIC CONTENT - make it binge-worthy, authentic, and professionally written."""
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                model=self.model,
                temperature=1.2,
                max_tokens=4000,
                top_p=0.92,
                presence_penalty=0.8,  # HIGH - prevents repetition
                frequency_penalty=0.7   # HIGH - forces vocabulary variety
            )
            
            result = self._parse_response(response.choices[0].message.content)
            logger.info(f"Story generated: {result['title']}")
            return result
        except Exception as e:
            logger.error(f"Error generating story: {e}")
            raise
    
    def _get_unique_opening_style(self):
        """Varied, professional opening approaches"""
        
        opening_styles = [
            "Start mid-conversation - we join dialogue already happening",
            "Open on a mundane action that becomes significant",
            "Begin with a question asked aloud",
            "Character making a small decision that matters",
            "Normal moment interrupted by the unusual",
            "Two people in comfortable silence",
            "Someone arriving somewhere they don't want to be",
            "A routine that's about to break",
            "Waiting for something/someone",
            "Character noticing something wrong",
            "Morning starting differently than usual",
            "Last normal moment before change",
            "Someone leaving/returning",
            "Small lie with big implications",
            "Unexpected visitor/call/message",
            "Character choosing between two options",
            "Ordinary object that triggers memory",
            "Weather matching/contrasting mood",
            "Someone alone, not by choice",
            "Preparation for something important"
        ]
        
        available = [s for s in opening_styles if s not in self.used_openings]
        if not available:
            self.used_openings = []
            available = opening_styles
        
        chosen = random.choice(available)
        self.used_openings.append(chosen)
        
        if len(self.used_openings) > 12:
            self.used_openings.pop(0)
        
        return chosen
    
    def _create_cinematic_prompt(self, category: str, opening_style: str):
        """Netflix-style story concepts"""
        
        scene_concepts = {
            'love': [
                "Two neighbors who've never spoken - then the elevator breaks",
                "Wrong number text message that keeps going",
                "Someone returns borrowed sugar after five years", 
                "Coffee shop regular finally talks to the barista"
            ],
            'help': [
                "Stranger pays for groceries - recipient wants to know why",
                "Lost wallet returned with something extra inside",
                "Homeless person helps lost tourist",
                "Teenager teaches elderly neighbor to use phone"
            ],
            'money': [
                "Lottery ticket found in old coat pocket",
                "Two friends, one meal check, silent calculation",
                "Job interview that reveals class differences",
                "Parents hiding bills from kids"
            ],
            'partnership': [
                "Rival coworkers forced to share project",
                "Siblings inheriting family business together",
                "Roommates navigating opposite schedules",
                "Business partners after one wants out"
            ],
            'dating': [
                "Blind date recognizes each other from somewhere",
                "Dating app match lives in same building",
                "Third date where someone's ex appears",
                "First date at funeral by accident"
            ],
            'relationship': [
                "Couple grocery shopping reveals everything",
                "Long-distance phone call during time difference",
                "Relationship through keys on shared hook",
                "Partners navigating family dinner"
            ],
            'poor': [
                "Choosing which bill to pay this month",
                "Rich friend doesn't understand the struggle",
                "Finding creative dinner with $5",
                "Pride vs accepting help"
            ],
            'disease': [
                "Doctor visit changes everything",
                "Telling family the diagnosis",
                "Normal day while processing prognosis",
                "Support group first meeting"
            ],
            'brilliant': [
                "Genius can't figure out relationships",
                "Smart kid explaining complex idea to adult",
                "Solving others' problems, ignoring own",
                "Intelligence isolating from peers"
            ],
            'student': [
                "Scholarship depends on next test",
                "Teacher who actually gets it",
                "Study group becomes friend group",
                "Cheating temptation vs integrity"
            ],
            'high school': [
                "Prom night doesn't go as planned",
                "Cafeteria table politics",
                "Crush on wrong person",
                "Graduation speech unfiltered"
            ],
            'middle school': [
                "First school dance awkwardness",
                "Friendship bracelet drama",
                "Parent-teacher conference aftermath",
                "Talent show disaster or triumph"
            ],
            'kids': [
                "Moving to new neighborhood",
                "Adults arguing, kids listening",
                "Pet loss and processing grief",
                "Standing up to bully"
            ],
            'business': [
                "Startup pitch to skeptical investors",
                "Employee confronts unfair boss",
                "Small shop vs chain competition",
                "Partnership dissolving over ethics"
            ],
            'christian': [
                "Prayer seemingly unanswered",
                "Church community during crisis",
                "Faith tested by tragedy",
                "Forgiveness after betrayal"
            ],
            'religion': [
                "Different beliefs, same dinner table",
                "Questioning childhood faith",
                "Ritual with new meaning",
                "Spiritual vs religious moment"
            ],
            'bible': [
                "Modern parable unfolds naturally",
                "Scripture quote changes perspective",
                "Biblical principle tested today",
                "Prodigal return story"
            ],
            'crime': [
                "Witness to crime, reporting dilemma",
                "Wrong place, wrong time",
                "Detective interview reveals truth",
                "Stolen item's journey back"
            ],
            'action': [
                "Protecting someone weaker",
                "Escape from dangerous situation",
                "Standing ground against threat",
                "Quick decision, lasting consequence"
            ],
            'drug': [
                "First time vs last time",
                "Family intervention",
                "Sobriety day counter reset",
                "Dealer with conscience"
            ],
            'mafia': [
                "Owing debt to wrong people",
                "Family business isn't legal",
                "Getting out vs staying loyal",
                "Witness protection decision"
            ],
            'tech': [
                "Phone dies at crucial moment",
                "Old generation vs new technology",
                "Online persona vs real life",
                "Algorithm reveals uncomfortable truth"
            ],
            'robotics': [
                "AI assistant becomes too helpful",
                "Robot worker replaces human",
                "Machine learning empathy",
                "Tech malfunction with stakes"
            ],
            'superpowers': [
                "Discovering ability at wrong time",
                "Power that's more curse than gift",
                "Using ability to help or hide",
                "Normal life with abnormal secret"
            ],
            'fantasy': [
                "Magic in mundane world",
                "Portal opens in apartment",
                "Mythical creature needs help",
                "Prophecy meets modern day"
            ],
            'horror': [
                "New house, wrong noises",
                "Routine broken by impossible",
                "Stranger knows too much",
                "Can't leave, can't stay"
            ],
            'fear': [
                "Phobia confronted unexpectedly",
                "Panic attack in public",
                "Childhood fear returns",
                "Irrational becomes rational"
            ],
            'halloween': [
                "Costume party revelation",
                "Trick-or-treating goes wrong",
                "October 31st tradition broken",
                "Haunted house real or fake"
            ]
        }
        
        concepts = scene_concepts.get(category, [
            f"{category.title()} tested in real situation",
            f"Character faces {category} challenge",
            f"{category.title()} story through relationships"
        ])
        
        chosen_concept = random.choice(concepts)
        
        return f"""Write a NETFLIX-QUALITY SHORT STORY (1400-1800 words).

CONCEPT: {chosen_concept}
OPENING: {opening_style}

🎬 STRUCTURE (4-6 SCENES):

SCENE 1 (250-350 words) - ESTABLISH:
- Where we are (specific location, simple description)
- Who's there (2-4 characters with authentic names)
- What's happening (action/dialogue immediately)
- Hook that makes us care
- Use SIMPLE language, natural conversation

SCENE 2 (250-350 words) - DEVELOP:
- Complication or new information
- More character interaction/dialogue
- Stakes become clearer
- Physical details that matter
- Vary your sentence structure from Scene 1

SCENE 3 (250-350 words) - ESCALATE:
- Tension increases naturally
- Characters make choices
- Relationships shift
- Show emotion through action, not clichés
- Use completely different vocabulary than previous scenes

SCENE 4 (250-350 words) - PEAK:
- Main conflict/confrontation
- Truth revealed or choice made
- Most intense moment
- Real consequences
- Keep language fresh - no repeated phrases

SCENE 5 (200-300 words) - RESOLVE:
- Immediate aftermath
- Changed relationships/situation
- Not everything wrapped perfectly
- Emotional truth
- End with resonance, not summary

📝 WRITING GUIDELINES:

DIALOGUE (make it real):
- "Hey." "What?" "Nothing, just—" "Tell me."
- People interrupt, trail off, change subject
- Slang, contractions, fragments
- Each character sounds different
- Arguments don't stay on topic

DESCRIPTIONS (be specific):
- Not "the room was messy" → "clothes draped over chair backs, three coffee cups on the desk"
- Not "she was nervous" → "she folded the receipt into smaller and smaller squares"
- Not "it was cold" → "breath fogged the windshield, heater clicking uselessly"

VARIETY (avoid repetition):
- Never use same word twice in close proximity
- Mix short punchy sentences with flowing ones
- Vary paragraph length (some 2 lines, some 8 lines)
- Different emotional beats per scene
- Fresh imagery each time

AUTHENTICITY:
- Names from story's cultural setting (Nigerian, Korean, Mexican, etc.)
- Natural speech patterns
- Realistic reactions
- No melodrama or overexplaining
- Trust the reader

⚠️ STRICT RULES:

BANNED CLICHÉS:
- Heart pounding/racing
- Breath caught/held
- Time slowed
- World stopped
- Eyes widening/narrowing
- Jaw clenched
- Hands trembling
- Blood running cold

WORD COUNT:
- MINIMUM: 1400 words
- MAXIMUM: 1800 words
- Target: 1500-1700 words

FORMAT:
Title: [Simple, intriguing title]

[Story text with natural paragraph breaks]
[NO scene labels - flow naturally]
[1400-1800 words total]

Make it BINGE-WORTHY. Make it REAL. Make it NETFLIX-QUALITY.

BEGIN:"""
    
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
        
        story = '\n\n'.join(story_lines).strip()
        
        if not title:
            first_lines = response.strip().split('\n')
            for line in first_lines:
                if line.strip() and not line.startswith('Title:') and not line.startswith('Story:'):
                    title = line.strip()[:100]
                    break
            if not title:
                title = "Untitled"
        
        if not story:
            story = response.replace('Title:', '').replace('Story:', '').strip()
        
        # Word count analysis
        word_count = len(story.split())
        char_count = len(story)
        
        logger.info(f"Parsed - Title: '{title}'")
        logger.info(f"Story length: {char_count} chars, {word_count} words")
        
        # Quality check
        if word_count < 1400:
            logger.warning(f"⚠️ Story too short: {word_count} words (target: 1400-1800)")
        elif word_count > 1800:
            logger.warning(f"⚠️ Story too long: {word_count} words (target: 1400-1800)")
        else:
            logger.info(f"✓ Perfect length: {word_count} words (episodic content)")
        
        return {'title': title, 'story': story}
