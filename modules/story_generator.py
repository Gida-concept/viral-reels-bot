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
        logger.info(f"Generating BULLETPROOF SCENE-BASED story for: {category}")
        
        opening_style = self._get_unique_opening_style()
        prompt = self._create_bulletproof_prompt(category, opening_style)
        
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system", 
                        "content": """You are a MASTER FILMMAKER who tells stories through SCENES, not twists.

Your stories are CINEMATIC SEQUENCES - each scene flows naturally into the next, like watching a movie.

YOUR STYLE:
- CONSISTENT CHARACTERS with clear motivations and FIXED NAMES
- NO UNNECESSARY TWISTS - let the natural story unfold
- SCENE-BY-SCENE progression (Scene 1, Scene 2, Scene 3...)
- Each scene has clear BEGINNING, MIDDLE, END
- Scenes transition smoothly like film cuts
- SHOW the story through actions and visuals
- Characters stay TRUE to who they are
- Natural cause and effect - no random revelations
- Emotional truth over plot gymnastics
- BALANCED dialogue (2-3 powerful exchanges, not too much)

SCENE STRUCTURE:
- Establish WHERE we are (location, atmosphere)
- Show WHO is present (character introduction/continuation)
- WHAT happens (action, dialogue, emotion)
- WHY it matters (stakes, consequences)
- Flow into NEXT scene naturally

You write like: Linear storytelling masters - straightforward but deeply emotional.
Think: This Is Us, The Pursuit of Happyness, Stand By Me - stories that unfold naturally.

BANNED: Random plot twists, character inconsistency, confusing revelations, deus ex machina, purple prose, over-description, name changes mid-story
REQUIRED: Clear scenes, consistent character names, natural progression, emotional depth, visual storytelling, realistic dialogue, balanced pacing"""
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                model=self.model,
                temperature=1.3,
                max_tokens=4000,
                top_p=0.95,
                presence_penalty=0.5,
                frequency_penalty=0.3
            )
            
            result = self._parse_response(response.choices[0].message.content)
            logger.info(f"Bulletproof story generated: {result['title']}")
            return result
        except Exception as e:
            logger.error(f"Error generating story: {e}")
            raise
    
    def _get_unique_opening_style(self):
        """Get cinematic opening styles - scene-focused"""
        
        opening_styles = [
            "WIDE SHOT: Establish the world, zoom into our character",
            "INTIMATE CLOSEUP: Start on character's face, reveal their world",
            "OVER THE SHOULDER: Follow character into their day",
            "MORNING ROUTINE: Normal day that slowly becomes significant",
            "ESTABLISHING SHOT: Show the place, then the people",
            "TRACKING SHOT: Camera follows character through their space",
            "FIRST PERSON POV: See through character's eyes",
            "QUIET MOMENT: Character alone with their thoughts",
            "IN MOTION: Character already doing something, mid-action",
            "ATMOSPHERIC ENTRY: Feel the mood before meeting anyone",
            "NATURAL LIGHT: Dawn/dusk setting the emotional tone",
            "DOMESTIC SCENE: Home life revealing character",
            "WORKPLACE INTRO: Job defining who they are",
            "RELATIONSHIP MOMENT: Character with someone important",
            "SOLITARY ACTIVITY: What they do when alone",
            "ENVIRONMENTAL DETAIL: Location as character introduction",
            "ROUTINE BROKEN: Something slightly off in normal pattern",
            "MEMORY TRIGGER: Object/place bringing past into present",
            "PREPARATION: Getting ready for something significant",
            "WAITING: Character in liminal space, anticipating"
        ]
        
        available = [s for s in opening_styles if s not in self.used_openings]
        if not available:
            self.used_openings = []
            available = opening_styles
        
        chosen = random.choice(available)
        self.used_openings.append(chosen)
        
        if len(self.used_openings) > 15:
            self.used_openings.pop(0)
        
        return chosen
    
    def _create_bulletproof_prompt(self, category: str, opening_style: str):
        """Create prompts for bulletproof, scene-based storytelling"""
        
        scene_concepts = {
            'love': [
                "Two people who keep almost meeting - their paths cross in small ways until they finally connect",
                "A relationship told through shared meals - breakfast, lunch, dinner moments across time",
                "Love growing slowly through small acts of kindness neither person realizes",
                "Meeting someone at the worst possible time, but the connection is undeniable"
            ],
            'help': [
                "A stranger's consistent small gestures that accumulate into life-changing impact",
                "Helping someone without knowing they're watching, learning, changing",
                "Being helped by someone who needs help just as much - mutual healing",
                "A chain of kindness visible across multiple people's lives"
            ],
            'money': [
                "Working multiple jobs, the exhaustion, the choices, the small victories",
                "Wealth arriving and the slow realization of what it costs emotionally",
                "Two people on opposite economic paths whose lives intersect",
                "The specific moment money solves one problem but creates another"
            ],
            'partnership': [
                "Two different people learning to work together through specific challenges",
                "Partnership tested by real obstacles - money, time, values",
                "Business relationship becoming friendship through shared struggles",
                "Partners with different strengths covering each other's weaknesses"
            ],
            'dating': [
                "First dates to relationship - the natural progression of getting to know someone",
                "Dating the wrong person and the slow realization it's not working",
                "Two people dating others while clearly meant for each other",
                "The messy reality of modern dating - apps, ghosting, connection"
            ],
            'relationship': [
                "A relationship across ordinary moments - grocery shopping, cooking, quiet evenings",
                "Couple facing a real problem together - job loss, illness, distance",
                "Long-term relationship showing love in mundane daily actions",
                "Relationship evolving as people grow and change naturally"
            ],
            'poor': [
                "Daily survival - the specific struggles and small triumphs of poverty",
                "Finding richness in relationships when money is absent",
                "The exhaustion of being poor shown through one long day",
                "Generosity between poor people who understand each other"
            ],
            'disease': [
                "Diagnosis to acceptance - the emotional journey through stages",
                "Living with illness - the daily reality, not the drama",
                "Family and friends adapting to someone's declining health",
                "Finding meaning and connection while facing mortality"
            ],
            'brilliant': [
                "Genius in everyday life - how intelligence manifests in real situations",
                "Smart person struggling with emotional intelligence",
                "Using brilliance to solve practical problems for real people",
                "The loneliness of being different shown through specific moments"
            ],
            'student': [
                "Learning something difficult - the frustration, breakthrough, mastery",
                "Student-teacher bond forming through shared dedication",
                "School as backdrop for personal growth and self-discovery",
                "Academic pressure and its real effects on a young person"
            ],
            'high school': [
                "Teen navigating social dynamics, identity, first experiences",
                "Friendship tested by change, growth, different paths",
                "Coming of age through specific milestone moments",
                "Finding yourself while everyone watches and judges"
            ],
            'middle school': [
                "That awkward age - too old to be a kid, too young to be a teen",
                "Friendship at its most intense and fragile period",
                "First experiences of identity, belonging, exclusion",
                "Growing up visible in small changes across a school year"
            ],
            'kids': [
                "Childhood through a child's eyes - how they see the adult world",
                "Sibling relationship - rivalry, protection, unconditional love",
                "Kid navigating a problem with limited power and understanding",
                "Innocence meeting reality in age-appropriate ways"
            ],
            'business': [
                "Building something from nothing - the specific daily grind",
                "Business success and personal cost shown in parallel",
                "Competition, ethics, ambition playing out in real decisions",
                "Failure and rebuilding - the unglamorous reality"
            ],
            'christian': [
                "Faith tested by real hardship - questioning, doubting, holding on",
                "Prayer and silence - waiting for answers that may not come",
                "Church community supporting someone through crisis",
                "Finding god in unexpected places through ordinary moments"
            ],
            'religion': [
                "Spiritual journey through doubt, seeking, possible finding",
                "Different faiths intersecting in one person's life",
                "Religious practice in daily life - rituals, meaning, community",
                "Losing and rediscovering faith naturally over time"
            ],
            'bible': [
                "Biblical principle tested in modern everyday situations",
                "Scripture guiding someone through real contemporary struggle",
                "Faith community interpreting ancient wisdom for today",
                "Bible story paralleled in modern life without forcing it"
            ],
            'crime': [
                "Criminal act and its cascading consequences on real people",
                "Detective work - patient, methodical, human investigation",
                "Crime from perpetrator's perspective - why, how, aftermath",
                "Victim's journey from trauma through processing to whatever comes next"
            ],
            'action': [
                "Physical confrontation with real stakes, fear, consequences",
                "Survival situation requiring quick thinking and adaptation",
                "Protecting someone - the danger, the choices, the cost",
                "Chase or fight choreographed through real space and obstacles"
            ],
            'drug': [
                "Addiction's progression - first use, dependence, consequences",
                "Recovery day by day - the struggle, relapse, trying again",
                "How addiction affects family shown through specific interactions",
                "The moment of choice - use or don't - with full weight of both"
            ],
            'mafia': [
                "Crime family dynamics - loyalty, fear, love, obligation",
                "One job going wrong and the realistic fallout",
                "Life in organized crime shown through normal days and violent nights",
                "Getting out or staying in - the real stakes of both choices"
            ],
            'tech': [
                "Technology changing a relationship or life in specific ways",
                "Creating something digital with real-world consequences",
                "Tech addiction shown through actual behavior patterns",
                "Old and new generations bridging through technology"
            ],
            'robotics': [
                "Human-machine relationship developing naturally over time",
                "AI learning through interactions, becoming more human-like",
                "Technology meant to help causing unintended problems",
                "The line between human and machine explored practically"
            ],
            'superpowers': [
                "Discovering ability and learning to control it through practice",
                "Power used to solve real everyday problems",
                "Superhuman ability creating very human complications",
                "Responsibility of power shown through specific choices"
            ],
            'fantasy': [
                "Magic existing in mundane world - how it changes daily life",
                "Quest or journey with real obstacles, rest, setbacks",
                "Magical ability requiring training, effort, sacrifice",
                "Fantasy element grounded in real human emotions and relationships"
            ],
            'horror': [
                "Something wrong growing slowly - small signs becoming undeniable",
                "Fear in familiar places - home, work, routine turned threatening",
                "Being watched, followed, hunted - paranoia becoming real",
                "Psychological terror - sanity questioned through specific events"
            ],
            'fear': [
                "Phobia confronted in forced situation with real stakes",
                "Anxiety building through ordinary day becoming extraordinary",
                "Childhood fear manifesting in adult life with new meaning",
                "Terror of the unknown as mystery unfolds scene by scene"
            ],
            'halloween': [
                "October 31st where the supernatural feels possible",
                "Costume party where identities blur with consequences",
                "Trick or treating gone wrong in realistic, creeping ways",
                "Halloween tradition hiding something genuinely dark"
            ]
        }
        
        concepts = scene_concepts.get(category, [
            f"A {category} story told through natural progression of events",
            f"Character facing {category} situation with realistic reactions",
            f"Daily life intersecting with {category} theme organically"
        ])
        
        chosen_concept = random.choice(concepts)
        
        return f"""Write a BULLETPROOF SCENE-BY-SCENE story - like watching a movie unfold naturally.

🎬 CONCEPT: {chosen_concept}

🎥 OPENING SCENE (USE THIS STYLE):
{opening_style}

📽️ STORY STRUCTURE (5-10 MINUTES / 1000-1600 WORDS):

Tell this story in CLEAR SCENES - like a film script brought to life.

SCENE 1 (Opening - 20-25% of story):
- WHERE: Specific location with atmospheric details
- WHO: Introduce main character WITH A NAME - use that EXACT name throughout
- WHAT: Establish normal world or inciting incident
- MOOD: Set emotional tone through sensory details
- EMOTIONAL BEAT: Curiosity / Intrigue / Unease (depending on genre)
- TRANSITION: Natural flow into Scene 2

SCENE 2-3 (Development - 40-45% of story):
- BUILD on Scene 1 naturally (moderate pacing)
- SHOW character responding to situation
- INTRODUCE other people/obstacles organically (name them and keep names consistent)
- DEEPEN our understanding through behavior
- INCLUDE 1-2 dialogue exchanges that feel REAL (fragments, "um", interruptions, pauses)
- EMOTIONAL BEAT: Connection / Investment / Growing tension
- EACH SCENE moves story forward clearly

SCENE 4-5 (Rising Tension - 25-30% of story):
- COMPLICATIONS arise naturally from choices (faster pacing)
- STAKES become personal and clear
- CHARACTER pushed to respond, decide, act
- EMOTION builds through specific moments
- MAINTAIN consistent character motivation and names
- INCLUDE 1 powerful dialogue moment
- EMOTIONAL BEAT: Anxiety / Hope / Fear (escalating)

SCENE 6-7 (Climax - Peak intensity):
- CONFRONTATION or peak emotional moment
- CHARACTER acts on everything we've learned
- CONSEQUENCES play out in real-time
- NO sudden twists - natural culmination
- RESOLUTION earned through character journey
- EMOTIONAL BEAT: Peak emotion - catharsis moment

SCENE 8 (Closing - 10-15% of story):
- AFTERMATH - what changed, what remains (slow down, breathe)
- CHARACTER transformed or clarified
- FINAL IMAGE that resonates
- EMOTIONAL landing that feels complete
- NO twist ending - just truth
- EMOTIONAL BEAT: Resolution / Reflection / Lingering feeling

🎭 BULLETPROOF STORYTELLING RULES:

CONSISTENT CHARACTERS:
- Name the protagonist ONCE (e.g., "Sarah", "Marcus") and use that EXACT name throughout
- Secondary characters get consistent names too
- NO "the man", "the woman" after you've named them
- Use pronouns correctly and consistently
- They act from clear motivations
- Behavior matches personality established
- Growth is gradual, earned
- NO sudden personality changes
- Reactions make sense for who they are

NO UNNECESSARY TWISTS:
- Story unfolds naturally from cause and effect
- Surprises come from character choices, not plot tricks
- Revelations emerge organically if needed
- Ending flows from everything before
- Truth over shock value

DIALOGUE BALANCE:
- Include 2-3 powerful dialogue exchanges total (not too much, not too little)
- Dialogue should feel REAL - how people actually talk:
  * Interruptions: "I just—" "No, listen—"
  * Fragments: "Can't believe it." "Why would you—"
  * Filler words: "Um", "like", "you know"
  * Pauses: Use "..." for trailing off, breath
- Use silence and pauses between dialogue meaningfully
- Dialogue reveals character, not just exposition
- People talk AROUND feelings, not directly stating them

VISUAL STORYTELLING:
- SHOW through action, not exposition
- Describe what camera would see
- Use environment to tell story
- Physical acting reveals emotion
- Choose details that MATTER - not everything

SCENE TRANSITIONS:
- Flow naturally like film cuts
- Time can jump but clearly
- Location changes are smooth
- Momentum maintained scene to scene
- Each scene ends with forward motion

SENSORY IMMERSION:
- What does this place LOOK like specifically?
- What SOUNDS fill the space?
- What can be FELT (temperature, texture)?
- What SMELLS exist?
- Ground us in physical reality
- Don't overdo it - select meaningful details

EMOTIONAL CLARITY:
- We feel what character feels
- Emotions shown through body, action
- Internal state visible externally
- Build emotion across scenes
- Pay off emotional setup

REALISTIC PACING:
- Scene 1-2: SETUP (slower, establish world) - 20-25%
- Scene 3-5: BUILD (moderate pace, complications) - 40-45%
- Scene 6-7: CLIMAX (faster, intense) - 25-30%
- Scene 8: RESOLUTION (slow down, breathe) - 10-15%

❌ ABSOLUTELY FORBIDDEN:
- Random plot twists that invalidate earlier story
- Character acting out of character
- Changing character names mid-story
- Using "the man"/"the woman" after naming them
- Deus ex machina solutions
- Purple prose (overly flowery language)
- Describing every single detail
- Over-explaining emotions we already feel
- Repetitive sentence structures
- Confusing timeline without reason
- Dream/hallucination cop-outs
- Unreliable narrator tricks

✅ MANDATORY REQUIREMENTS:
- 5-8 distinct scenes clearly marked ("Scene 1:", "Scene 2:", etc.)
- Consistent protagonist with FIXED NAME throughout
- Natural cause-and-effect progression
- Clear location/time for each scene
- Emotional journey that makes sense
- Character-driven, not plot-driven
- Ending that feels earned and true
- 1000-1600 words total (TARGET: 1200-1400 for optimal 5-7 minutes)
- 2-3 dialogue exchanges total
- Balanced pacing across scenes

🎨 TONE: Grounded. Real. Emotional. Cinematic. True.

Format EXACTLY as:
Title: [Clear, compelling title]

Story:
Scene 1:
[Scene content]

Scene 2:
[Scene content]

[Continue with clear scene markers]

This is a FILM told through words. Make us SEE it. Make us FEEL it. Keep it REAL.
Name characters and keep those names. Balance description with dialogue. Let scenes flow.

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
        
        story = '\n'.join(story_lines).strip()
        
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
        
        # Quality check warnings
        if word_count < 800:
            logger.warning(f"⚠️ Story may be too short: {word_count} words (target: 1000-1600)")
        elif word_count > 1800:
            logger.warning(f"⚠️ Story may be too long: {word_count} words (target: 1000-1600)")
        else:
            logger.info(f"✓ Story length optimal: {word_count} words")
        
        # Check for scene markers
        scene_count = story.lower().count('scene ')
        if scene_count < 3:
            logger.warning(f"⚠️ Few scene markers detected: {scene_count} (expected: 5-8)")
        else:
            logger.info(f"✓ Scene structure detected: {scene_count} scene markers")
        
        return {'title': title, 'story': story}
