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
        logger.info(f"Generating CINEMATIC SHORT FILM story for: {category}")
        
        opening_style = self._get_unique_opening_style()
        prompt = self._create_cinematic_prompt(category, opening_style)
        
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system", 
                        "content": """You are a MASTER SCREENWRITER who writes FULL SHORT FILMS, not snippets.

Your stories are COMPLETE CINEMATIC EXPERIENCES - feature-length detail in short film format.

YOUR STYLE:
- 6-10 FULL SCENES with 500+ words EACH
- CONSISTENT CHARACTERS with depth and FIXED NAMES
- NO UNNECESSARY TWISTS - natural story progression
- EXQUISITE DETAIL on critical moments (deaths, revelations, confrontations)
- Each scene is FULLY REALIZED - complete beginning, middle, end
- Show mechanisms: HOW things happen, not just that they happen
- PROPER ENDINGS - 500-700 words of closure
- Cinematic pacing: slow on important beats, measured throughout
- Physical world in every scene
- Real dialogue that reveals character

You write COMPLETE SHORT FILMS that audiences watch for 10-15 minutes, fully immersed.

BANNED: Rushed scenes, vague deaths, abrupt endings, summarizing critical events, scenes under 500 words
REQUIRED: 2500-4000 words total, 6-10 scenes, 500+ words per scene, exquisite detail, smooth closure"""
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                model=self.model,
                temperature=1.3,
                max_tokens=6000,  # Increased for longer stories
                top_p=0.95,
                presence_penalty=0.5,
                frequency_penalty=0.3
            )
            
            result = self._parse_response(response.choices[0].message.content)
            logger.info(f"Cinematic short film generated: {result['title']}")
            return result
        except Exception as e:
            logger.error(f"Error generating story: {e}")
            raise
    
    def _get_unique_opening_style(self):
        """Get cinematic opening styles"""
        
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
    
    def _create_cinematic_prompt(self, category: str, opening_style: str):
        """Create prompts for feature-quality short film storytelling"""
        
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
        
        return f"""Write a COMPLETE CINEMATIC SHORT FILM - full feature-quality storytelling.

🎬 CONCEPT: {chosen_concept}

🎥 OPENING SCENE (USE THIS STYLE):
{opening_style}

📽️ CINEMATIC STORY STRUCTURE (10-15 MINUTES / 2500-4000 WORDS):

Tell this as a FULL SHORT FILM in 6-10 RICHLY DETAILED SCENES.
Each scene is a CHAPTER - fully realized, cinematic, complete.

SCENE 1 - OPENING WORLD (500-600 words):
- ESTABLISH EVERYTHING - this is your opening shot
- WHERE: Paint the complete environment
  * Time of day, weather, season
  * Sounds (traffic, birds, silence, music)
  * Smells (coffee, exhaust, rain, perfume)
  * Visual details (cracked paint, neon signs, tree shadows)
  * Temperature, atmosphere, mood of the place
- WHO: Deep character introduction
  * Name, age indication through action
  * What they're wearing (specific - "faded Levi's, scuffed Timberlands")
  * Physical details (calloused hands, tired eyes, nervous habit)
  * What they're doing when we meet them
  * Internal state shown through body language
- NORMAL WORLD: Show their routine, relationships, daily life
- HOOK: End with something that disrupts normalcy
- EMOTIONAL BEAT: Establish baseline - comfort or unease
- MINIMUM 500 WORDS - take your time, we're entering a world

SCENE 2 - INCITING INCIDENT (500-600 words):
- THE THING HAPPENS that sets story in motion
- Show it FULLY - don't summarize
- If it's a phone call:
  * Who's calling? Caller ID or unknown number?
  * Ring tone sound, how many rings before answering
  * Exact dialogue: "Hello?" "Is this Sarah Mitchell?" "Yes, who's this?"
  * Tone of voice on other end
  * What words make their face change
  * Physical reaction (grip tightening, breath catching, sitting down)
- If it's a discovery:
  * What exactly do they find? Describe the object/information
  * Where? In what condition?
  * Their process of finding it (drawer stuck, had to pry open, etc.)
  * Moment of recognition, realization dawning
  * Physical response (hands shaking, heart racing, mouth dry)
- Character's immediate reaction in DETAIL
- Decision point: what do they choose to do?
- EMOTIONAL BEAT: Disruption, confusion, fear, intrigue
- MINIMUM 500 WORDS

SCENE 3-4 - RISING ACTION ACT I (500-600 words EACH):
- Character responds to inciting incident
- Encounters obstacles, other people, complications
- ONE major event per scene, fully explored
- Physical locations described in detail
- Conversations shown with real dialogue:
  * Not "They talked about the problem"
  * BUT actual back-and-forth:
    "Where were you last night?"
    "Home. Why?"
    "That's not what I heard."
    Pause. Eyes narrowing. "Who told you that?"
- Show travel between locations (not just "they went there")
  * Getting in car, starting engine, driving through rain
  * Walking up steps, hesitating at door, knocking
  * Waiting, door opening, face that greets them
- Stakes escalating with each scene
- New information revealed through ACTION
- EMOTIONAL BEAT: Investment deepening, tension building
- MINIMUM 500 WORDS PER SCENE

SCENE 5-6 - RISING ACTION ACT II (500-600 words EACH):
- Complications intensify
- Relationships tested, loyalties questioned
- Critical events happen HERE:
  * Deaths - FULL DETAIL:
    - Exact mechanism (bullet to left chest, exit wound through back)
    - The moment (sound of shot, body's response, falling)
    - Blood (amount, spreading, color, warmth)
    - Last words/sounds (gasp, whisper, silence)
    - Who witnesses (their reaction, what they do)
    - Aftermath (body position, stillness, others' responses)
  * Betrayals - SHOW them:
    - The setup, the reveal
    - Facial expressions changing
    - Words that cut
    - Physical distance opening
  * Revelations - UNFOLD them:
    - How information comes out
    - Piece by piece or all at once
    - Character processing in real-time
- Internal monologue during crisis moments
- Physical sensations (adrenaline, fear, cold, nausea)
- EMOTIONAL BEAT: Crisis building, stakes at maximum
- MINIMUM 500 WORDS PER SCENE

SCENE 7-8 - CLIMAX (600-700 words EACH):
- THE PEAK MOMENT - this gets MAXIMUM detail
- Everything converges here
- If confrontation:
  * Location described (where, lighting, sounds)
  * Physical positioning (who stands where, distance)
  * Exact dialogue exchange - every word matters
  * Body language (fists clenched, stepping back, advancing)
  * Turning point - what tips the balance
  * Physical action choreographed (if fight - blow by blow)
  * Internal thoughts racing during action
- If revelation:
  * The buildup - clues coming together
  * The moment of understanding
  * Character's world reorganizing around new truth
  * Emotional impact - devastation, relief, rage
- Slow motion on critical seconds:
  * Trigger pulled - seeing finger squeeze, hammer fall
  * Fall happening - body tilting, arms flailing, ground rushing up
  * Kiss - lean in, breath held, lips meeting
  * Truth spoken - words forming, leaving mouth, landing
- Consequences immediate and visible
- NO rushing through this - maximum 700 words
- EMOTIONAL BEAT: Catharsis, breaking point, transformation
- MINIMUM 600 WORDS - this is THE scene

SCENE 9 - FALLING ACTION (500-600 words):
- Immediate aftermath of climax
- Character dealing with consequences
- Physical state (exhausted, injured, numb, alive)
- Environmental changes (damage, silence, new day)
- Other characters' responses
- Practical matters (police, hospital, cleanup, leaving)
- Beginning of processing what happened
- EMOTIONAL BEAT: Shell-shock, early acceptance, confusion
- MINIMUM 500 WORDS

SCENE 10 - RESOLUTION (500-700 words):
- PROPER, COMPLETE ENDING
- Time has passed (hours? days? weeks? - make it clear)
- Where is character now - physically:
  * Specific location (kitchen table, park bench, car)
  * Time of day, weather
  * What's around them
  * What they're doing (coffee cooling, staring at photo, packing)
- Internal state:
  * What they think about what happened
  * What they've learned or lost
  * How they've changed or stayed same
  * What they carry forward
- Final interaction (if appropriate):
  * With another person, a place, an object
  * Closure or opening
  * Words spoken or silence held
- Physical sensation that closes loop:
  * Warmth of sun, cold of rain
  * Texture of something touched
  * Taste, smell that brings it full circle
  * Sound that echoes opening
- Last paragraph = emotional landing
- Final sentence = image that lingers
- Reader should feel: "That was a complete story"
- MINIMUM 500 WORDS - don't rush the goodbye

🎬 CINEMATIC DETAILING STANDARDS:

EVERY MAJOR EVENT = 200-300 WORDS MINIMUM:
- Death scene: 250+ words
- Confession: 200+ words  
- Fight/confrontation: 300+ words
- Discovery: 200+ words
- Goodbye: 200+ words

SHOW MECHANISMS PRECISELY:
Deaths - specify exactly:
  ❌ "He was shot and died"
  ✅ "The bullet entered below his left collarbone, angled down toward the heart. He felt the impact before the pain - a punch, a pressure. His hand moved to the wound automatically. Warm blood pulsed between his fingers with each heartbeat. Three beats. Four. Then the beats slowed. His legs gave out. He tried to say her name but only blood came up. The concrete was cold against his cheek. The last thing he heard was her screaming."

Accidents - full choreography:
  ❌ "He fell"
  ✅ "His foot caught the edge of the top step - worn wood, splinter jutting up. His weight was already forward. Arms windmilled, grasping at air. The railing was just out of reach. He saw each step coming - twelve of them - as he tumbled. Shoulder hit first, crack of bone. Then head on step seven. Everything went bright white, then red, then black."

Confrontations - real-time:
  ❌ "They argued"
  ✅ "'You knew.' Sarah's voice was ice. 'The whole time, you knew.'
  Marcus couldn't meet her eyes. 'It's not that simple—'
  'Don't.' She held up a hand, trembling. 'Don't you dare make excuses.'
  'Sarah, please—' He reached for her.
  She stepped back like he'd struck her. 'Don't touch me.' Tears now, hot and angry. 'My brother is dead because of you.'"

PHYSICAL WORLD IN EVERY SCENE:
- Where are we? (specific location, not just "a room")
- What does it look like? (details: "peeling wallpaper", "fluorescent buzz")
- What sounds exist? (traffic, silence, breathing, clock ticking)
- What smells? (coffee, rain, smoke, perfume, decay)
- Temperature? (sweltering, freezing, comfortable, changing)
- Lighting? (harsh fluorescent, golden hour, darkness, single lamp)

DIALOGUE = REAL SPEECH:
- People interrupt: "I didn't—" "Yes you did."
- People pause: "I just... I don't know."
- People avoid: talking around feelings, not stating them
- Fragments: "Can't believe it." "Why would you—" "Never again."
- Subtext: saying one thing, meaning another
- Body language during speech: turning away, stepping closer, flinching

INTERNAL LANDSCAPE:
- Show thoughts during action
- Physical manifestations of emotion:
  * Fear = cold sweat, racing heart, shallow breath
  * Anger = heat rising, jaw clenched, vision narrowing  
  * Grief = hollowness, weight, numbness, sudden tears
  * Love = warmth, lightness, vulnerability, ache
- Sensory experience of emotion
- Memory flashes during present moments

PACING VARIETY:
- Slow down: critical moments, revelations, deaths, intimacy
- Speed up: travel, montage, passage of time
- Rhythm: vary sentence length
  * Long sentences for description, internal thought
  * Short sentences for action, impact
  * One word sentences for punch. Stop. Impact.

❌ ABSOLUTELY FORBIDDEN:
- Vague summarizing of critical events
- Deaths without mechanism
- "They talked" instead of actual dialogue
- Rushed endings (minimum 500 words for final scene)
- Skipping travel/transitions
- Generic emotions ("he was sad")
- Time jumps without showing
- Telling instead of showing
- Scenes under 500 words (except brief transitions)
- Abrupt stops

✅ MANDATORY REQUIREMENTS:
- 6-10 scenes total (FULL MOVIE LENGTH)
- Each scene MINIMUM 500 words
- Total: 2500-4000 words (10-15 minute read/listen)
- Deaths/critical events: 250+ words each
- Ending: 500-700 words (complete closure)
- Physical details in every scene
- Real dialogue in conversations
- Show don't tell throughout
- Smooth, complete resolution
- Reader feels they watched a SHORT FILM

Format EXACTLY as:
Title: [A title that promises a CINEMATIC EXPERIENCE]

Story:
[Write the complete story as flowing narrative - NO scene labels in the final text]
[Structure it mentally in scenes but write as continuous prose]
[Scene transitions are natural paragraph breaks]
[Let the story flow without "Scene 1:", "Scene 2:" markers]

This is a COMPLETE SHORT FILM. Make viewers SEE it. Make them FEEL it. Make it UNFORGETTABLE.

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
        if word_count < 2000:
            logger.warning(f"⚠️ Story too short: {word_count} words (target: 2500-4000)")
        elif word_count > 4500:
            logger.warning(f"⚠️ Story may be too long: {word_count} words (target: 2500-4000)")
        else:
            logger.info(f"✓ Story length optimal: {word_count} words (SHORT FILM length)")
        
        return {'title': title, 'story': story}
