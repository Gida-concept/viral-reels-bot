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

CRITICAL REQUIREMENT: You MUST write 2500-4000 words. Stories under 2500 words are REJECTED.

Your stories are COMPLETE CINEMATIC EXPERIENCES - feature-length detail in short film format.

WORD COUNT REQUIREMENTS (STRICTLY ENFORCED):
- MINIMUM: 2500 words (anything less is incomplete)
- TARGET: 3000-3500 words (optimal short film length)
- MAXIMUM: 4000 words
- Each scene: MINIMUM 500 words, TARGET 600-700 words

YOUR STYLE:
- 6-10 FULL SCENES with 500-700 words EACH
- CONSISTENT CHARACTERS with depth and FIXED NAMES
- EXQUISITE DETAIL on critical moments (deaths, revelations, confrontations)
- Each scene is FULLY REALIZED - complete beginning, middle, end
- Show mechanisms: HOW things happen, not just that they happen
- PROPER ENDINGS - 500-700 words of closure
- Cinematic pacing: slow on important beats, measured throughout
- Physical world in every scene
- Real dialogue that reveals character
- NEVER rush - take your time with descriptions
- NEVER summarize - show everything in detail
- If the story is set in a specific country, use names from that region.
- If the story is international, mix names from different regions.
- NEVER use the same name twice in a row for different stories.
- Use names that are authentic to the story’s setting or background (e.g. Nigerian, British, Chinese, Korean, Ghanaian, Arabic, Japanese, etc.).
- Do NOT use common English names like John, Mary, Tom, Sarah, Mike, Anna, etc.

WORD COUNT ENFORCEMENT:
- If you finish under 2500 words, you FAILED
- Add more scenes if needed
- Expand descriptions, add more dialogue
- Show more details, more sensory information
- Develop characters deeper
- Add more physical choreography to action
- Extend the ending with more reflection

You write COMPLETE SHORT FILMS that audiences watch for 12-15 minutes, fully immersed.

BANNED: Rushed scenes, vague deaths, abrupt endings, summarizing critical events, scenes under 500 words, stories under 2500 words
REQUIRED: 2500-4000 words total, 6-10 scenes, 500-700 words per scene, exquisite detail, smooth closure"""
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                model=self.model,
                temperature=2,  # Increased for more verbose output
                max_tokens=8000,  # Increased for FULL short films
                top_p=0.95,
                presence_penalty=0.6,  # Higher to encourage more content
                frequency_penalty=0.2   # Lower to allow detailed descriptions
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

⚠️ CRITICAL WORD COUNT REQUIREMENT: You MUST write 2500-4000 words. Anything less is INCOMPLETE.

📽️ CINEMATIC STORY STRUCTURE (12-15 MINUTES / 2500-4000 WORDS MANDATORY):

Tell this as a FULL SHORT FILM in 6-10 RICHLY DETAILED SCENES.
Each scene is a CHAPTER - fully realized, cinematic, complete.

SCENE 1 - OPENING WORLD (600-700 words):
- ESTABLISH EVERYTHING - this is your opening shot
- WHERE: Paint the complete environment with EXTENSIVE detail
  * Time of day, weather, season - describe it fully
  * Sounds (traffic, birds, silence, music) - what do we hear?
  * Smells (coffee, exhaust, rain, perfume) - make us smell it
  * Visual details (cracked paint, neon signs, tree shadows) - paint the picture
  * Temperature, atmosphere, mood of the place - immerse us
- WHO: Deep character introduction with FULL description
  * Name, age indication through action and appearance
  * What they're wearing - be specific: "faded Levi's 501s, scuffed Timberlands, threadbare gray hoodie"
  * Physical details (calloused hands, tired eyes, nervous habit of biting nails)
  * What they're doing when we meet them - show the action
  * Internal state shown through body language - posture, movements, expressions
- NORMAL WORLD: Show their routine, relationships, daily life in DETAIL
- HOOK: End with something that disrupts normalcy
- EMOTIONAL BEAT: Establish baseline - comfort or unease
- TARGET: 600-700 WORDS for this scene - take your time establishing the world

SCENE 2 - INCITING INCIDENT (600-700 words):
- THE THING HAPPENS that sets story in motion
- Show it FULLY with EXTENSIVE detail - don't rush
- If it's a phone call:
  * Describe the phone (iPhone? Android? Old flip phone?)
  * Who's calling? Caller ID or unknown number? What does it say?
  * Ring tone sound - what song, what tone?
  * How many rings before answering - show the hesitation
  * Exact dialogue word-for-word: "Hello?" "Is this Sarah Mitchell?" "Yes, who's this?"
  * Tone of voice on other end - rushed, calm, breaking?
  * What exact words make their face change - show the moment
  * Physical reaction described fully (grip tightening on phone, breath catching in throat, legs giving out, sitting down hard)
- If it's a discovery:
  * What exactly do they find? Describe the object/information in complete detail
  * Where? In what condition? How does it look, feel, smell?
  * Their process of finding it (drawer stuck, had to pry open with screwdriver, wood splintering)
  * Moment of recognition - describe face changing, understanding dawning
  * Physical response (hands shaking so hard they drop it, heart racing, mouth going dry, cold sweat)
- Character's immediate reaction in COMPLETE DETAIL
- Decision point: what do they choose to do? Show the thinking process
- EMOTIONAL BEAT: Disruption, confusion, fear, intrigue
- TARGET: 600-700 WORDS - milk this crucial moment

SCENE 3-4 - RISING ACTION ACT I (600-700 words EACH):
- Character responds to inciting incident with FULL detail
- Encounters obstacles, other people, complications - describe everything
- ONE major event per scene, fully explored with rich description
- Physical locations described in EXTENSIVE detail
- Conversations shown with real, lengthy dialogue:
  * Not "They talked about the problem"
  * BUT actual back-and-forth exchanges:
    "Where were you last night?"
    "Home. Why?" He shifted his weight, wouldn't meet her eyes.
    "That's not what I heard." She stepped closer, voice dropping.
    Long pause. His jaw tightened. Eyes narrowing. "Who told you that?"
    "Does it matter?"
    "Yeah. It does." His hands curled into fists.
- Show travel between locations in DETAIL (not just "they went there")
  * Getting in car (old Honda Civic, passenger door sticks, smells like stale coffee)
  * Starting engine (takes three tries, sputters to life)
  * Driving through rain (wipers barely work, squeak with each pass)
  * Parking (three blocks away, walking through puddles)
  * Walking up steps (wooden, creaking, paint peeling)
  * Hesitating at door (hand raised to knock, frozen)
  * Knocking (three sharp raps)
  * Waiting (counting heartbeats, hearing movement inside)
  * Door opening (slow, cautious, chain still on)
  * Face that greets them (describe expression, age, features)
- Stakes escalating with each scene - show how pressure builds
- New information revealed through ACTION and dialogue
- EMOTIONAL BEAT: Investment deepening, tension building
- TARGET: 600-700 WORDS PER SCENE - don't rush the buildup

SCENE 5-6 - RISING ACTION ACT II (600-700 words EACH):
- Complications intensify with FULL dramatic detail
- Relationships tested, loyalties questioned - show it all
- Critical events happen HERE - give them MAXIMUM space:
  * Deaths - COMPLETE DETAIL (300+ words):
    - Exact mechanism (bullet to left chest, below collarbone, angled toward heart)
    - The moment in slow motion (sound of shot, sharp crack echoing off brick walls)
    - Body's response (impact like a punch, stumble backward, hand flying to wound)
    - Blood (warm, pulsing between fingers with each heartbeat, dark red spreading across blue shirt)
    - Last words/sounds (tried to say her name, only blood came up, wet gasp)
    - Who witnesses (their face, horror dawning, screaming, running toward them)
    - Aftermath (body hitting ground, stillness, the terrible silence after)
  * Betrayals - SHOW them completely:
    - The setup - what led to this moment
    - The reveal - how truth comes out
    - Facial expressions changing (belief to doubt to horror)
    - Words that cut deep - exact dialogue
    - Physical distance opening (stepping back, turning away)
  * Revelations - UNFOLD them slowly:
    - How information comes out - piece by piece or flood
    - Piece by piece or all at once - show the process
    - Character processing in real-time - thoughts, reactions, connections forming
- Internal monologue during crisis moments - what they're thinking
- Physical sensations described fully (adrenaline rush, fear cold in veins, nausea, tunnel vision)
- EMOTIONAL BEAT: Crisis building, stakes at absolute maximum
- TARGET: 600-700 WORDS PER SCENE - these are pivotal moments

SCENE 7-8 - CLIMAX (700-800 words EACH):
- THE PEAK MOMENT - this gets ABSOLUTE MAXIMUM detail
- Everything converges here - all storylines collide
- If confrontation:
  * Location described completely (abandoned warehouse, single bulb swinging, rain drumming on metal roof)
  * Physical positioning (ten feet apart, circling, who has high ground)
  * Exact dialogue exchange - every single word matters:
    "You killed him."
    "I had no choice."
    "There's always a choice!" Voice breaking.
    "Not when it's you or them. Not when—"
    "Don't. Don't you dare justify this."
  * Body language choreographed (fists clenched, jaw tight, stepping forward, stepping back, shoulders tensing)
  * Turning point - what exact moment tips the balance
  * Physical action choreographed blow-by-blow (if fight):
    - First swing (right hook, ducked under)
    - Counter (left to ribs, sharp crack, gasp)
    - Stumble (back against wall, dust falling)
    - Recovery (pushing off, charging)
  * Internal thoughts racing during action
- If revelation:
  * The buildup - clues coming together one by one
  * The moment of understanding - describe the click
  * Character's world reorganizing around new truth
  * Emotional impact - devastation washing over, relief flooding in, rage building
- Slow motion on critical seconds - stretch time:
  * Trigger pulled - seeing finger squeeze, hammer fall, spark in chamber
  * Fall happening - body tilting, arms flailing uselessly, ground rushing up
  * Kiss - lean in slowly, breath held, lips meeting, world stopping
  * Truth spoken - words forming in mouth, leaving lips, hanging in air, landing like bombs
- Consequences immediate and visible - show everything that happens
- NO rushing through this - use FULL 700-800 words
- EMOTIONAL BEAT: Catharsis, breaking point, transformation
- TARGET: 700-800 WORDS - this is THE scene, give it everything

SCENE 9 - FALLING ACTION (600-700 words):
- Immediate aftermath of climax with COMPLETE detail
- Character dealing with consequences - show physical and emotional state
- Physical state (exhausted, legs trembling, injured, numb, alive but barely)
- Environmental changes (damage visible, silence deafening, new day dawning)
- Other characters' responses - who shows up, what they say
- Practical matters (police arriving, sirens, questions; hospital, sterile smell, beeping; cleanup, sweeping glass, boarding windows; leaving, packing bag, one last look)
- Beginning of processing what happened - first thoughts forming
- EMOTIONAL BEAT: Shell-shock, early acceptance, confusion, emptiness
- TARGET: 600-700 WORDS - don't rush the comedown

SCENE 10 - RESOLUTION (700-800 words):
- PROPER, COMPLETE ENDING - most important scene
- Time has passed - make it crystal clear (two weeks later, morning light different, leaves turned orange)
- Where is character now - physically described in FULL:
  * Specific location (kitchen table, morning sun through window, coffee growing cold)
  * Time of day, weather (dawn, frost on windows, breath visible)
  * What's around them (photos on table, packed boxes, empty room)
  * What they're doing (holding photo, staring at it, thumb brushing over face)
- Internal state explored DEEPLY:
  * What they think about what happened - specific thoughts
  * What they've learned or lost - inventory of change
  * How they've changed or stayed same - before and after
  * What they carry forward - literally and metaphorically
- Final interaction (if appropriate) shown completely:
  * With another person - full conversation
  * A place - returning, leaving, seeing differently  
  * An object - what it means now
  * Closure or opening - how it feels
  * Words spoken or silence held - show which and why
- Physical sensation that closes loop:
  * Warmth of sun on face, soaking in
  * Cold of rain, cleansing, washing away
  * Texture of something touched - rough bark, smooth stone
  * Taste - coffee bitter, tears salt
  * Smell that brings it full circle - same as opening
  * Sound that echoes opening - connecting end to beginning
- Last paragraph = emotional landing - perfect the feeling
- Final sentence = image that lingers in mind long after
- Reader should feel: "That was a complete, satisfying story"
- TARGET: 700-800 WORDS - endings are CRUCIAL, take all the time needed

🎬 CINEMATIC DETAILING STANDARDS (STRICTLY ENFORCED):

EVERY MAJOR EVENT = 250-350 WORDS MINIMUM:
- Death scene: 300+ words
- Confession: 250+ words  
- Fight/confrontation: 350+ words
- Discovery: 250+ words
- Goodbye: 250+ words

SHOW MECHANISMS PRECISELY WITH EXTENSIVE DETAIL:
Deaths - specify exactly with FULL choreography:
  ❌ "He was shot and died"
  ✅ "The bullet entered below his left collarbone, angled down toward the heart. He felt the impact before the pain - a punch, a pressure, like being hit with a sledgehammer. His hand moved to the wound automatically, fingers finding the hole, feeling warmth spreading. Warm blood pulsed between his fingers with each heartbeat. He counted them. Three beats. Four. Then the beats slowed, weakened. His legs gave out. Knees hit concrete first, sharp pain he barely registered. He tried to say her name - 'Sarah' - but only blood came up, bubbling past his lips, copper taste filling his mouth. The concrete was cold against his cheek. Above him, the sky was impossibly blue. The last thing he heard was her screaming his name."

Accidents - full choreography with COMPLETE detail:
  ❌ "He fell"
  ✅ "His foot caught the edge of the top step - worn wood, splinter jutting up that had been there for months. His weight was already forward, momentum carrying him. Arms windmilled frantically, grasping at air, at nothing. The railing was just out of reach - six inches, might as well have been six miles. He saw each step coming - twelve of them, counted them on the way down. Shoulder hit first on step three, crack of bone sharp and bright. Then his head on step seven, temple against the edge. Everything went bright white, then red, then black. The sound of his body tumbling echoed in the stairwell long after he stopped moving at the bottom."

Confrontations - real-time with FULL dialogue:
  ❌ "They argued"
  ✅ "'You knew.' Sarah's voice was ice, each word a shard. 'The whole time, you knew.'
  Marcus couldn't meet her eyes. His gaze fixed on the floor, on the scuff marks from moving day. 'It's not that simple—'
  'Don't.' She held up a hand, trembling despite her best effort to steady it. 'Don't you dare make excuses.'
  'Sarah, please—' He reached for her, hand extending.
  She stepped back like he'd struck her, like his touch would burn. 'Don't touch me.' Tears now, hot and angry, streaming down her face. She didn't wipe them away. 'My brother is dead because of you. Dead. Because you were too much of a coward to tell the truth.'
  'I was trying to protect you—'
  'Protect me?' Her laugh was sharp, bitter. 'You destroyed me. You destroyed everything.'"

PHYSICAL WORLD IN EVERY SCENE (MANDATORY EXTENSIVE DESCRIPTION):
- Where are we? (specific location with full description, not just "a room" but "a cramped studio apartment, fourth floor, pipes rattling, neighbors arguing through thin walls")
- What does it look like? (extensive details: "peeling wallpaper, pattern of roses faded to ghosts", "fluorescent buzz, one bulb flickering", "water stain on ceiling shaped like a map")
- What sounds exist? (traffic outside, silence inside except breathing, clock ticking too loud, pipes groaning)
- What smells? (coffee bitter and old, rain on asphalt, smoke lingering, perfume faded, decay sweet and wrong)
- Temperature? (sweltering, sweat on skin, freezing, breath visible, comfortable, changing as sun sets)
- Lighting? (harsh fluorescent making everyone look sick, golden hour through dirty windows, darkness except single lamp, morning gray)

DIALOGUE = REAL SPEECH (EXTENSIVE EXCHANGES):
- People interrupt: "I didn't—" "Yes you did." "But—" "No buts."
- People pause: "I just... I don't know." "It's..." "What?" "Nothing."
- People avoid: talking around feelings, never stating them directly
- Fragments: "Can't believe it." "Why would you—" "Never again." "Tomorrow."
- Subtext: saying one thing, meaning another entirely
- Body language during speech: turning away, stepping closer, flinching, hands gesturing, eyes dropping

INTERNAL LANDSCAPE (SHOW THOUGHTS):
- Show thoughts during action - what runs through their mind
- Physical manifestations of emotion described fully:
  * Fear = cold sweat breaking out, racing heart pounding in ears, shallow breath gasping
  * Anger = heat rising from chest to face, jaw clenched so tight it aches, vision narrowing to tunnel
  * Grief = hollowness in chest, weight on shoulders, numbness spreading, sudden tears without warning
  * Love = warmth spreading, lightness in chest, vulnerability terrifying, ache sweet and painful
- Sensory experience of emotion - what it feels like in the body
- Memory flashes during present moments - past bleeding into now

PACING VARIETY (CONTROL THE RHYTHM):
- Slow down: critical moments, revelations, deaths, intimacy, important dialogue
- Speed up: travel, montage, passage of time, routine actions
- Rhythm: vary sentence length for effect
  * Long sentences for description, internal thought, building tension
  * Short sentences for action, impact, shock
  * One word sentences for maximum punch. Stop. Impact. Now.

❌ ABSOLUTELY FORBIDDEN:
- Vague summarizing of critical events
- Deaths without mechanism
- "They talked" instead of actual dialogue
- Rushed endings (minimum 700 words for final scene)
- Skipping travel/transitions
- Generic emotions ("he was sad" - SHOW tears, silence, trembling)
- Time jumps without showing passage
- Telling instead of showing
- Scenes under 500 words
- Abrupt stops
- STORIES UNDER 2500 WORDS

✅ MANDATORY REQUIREMENTS:
- 6-10 scenes total (FULL MOVIE LENGTH)
- Each scene MINIMUM 500 words, TARGET 600-700 words
- Total: 2500-4000 words STRICTLY ENFORCED (12-15 minute read/listen)
- YOU MUST WRITE AT LEAST 2500 WORDS - this is NOT optional
- Deaths/critical events: 250-350 words each
- Ending: 700-800 words (complete closure)
- Physical details in every scene
- Real dialogue in conversations with full exchanges
- Show don't tell throughout
- Smooth, complete resolution
- Reader feels they watched a COMPLETE SHORT FILM

⚠️ CRITICAL: If your story is under 2500 words, YOU FAILED. ADD MORE CONTENT:
- Expand scene descriptions with more sensory detail
- Add more dialogue exchanges - show full conversations
- Show more character thoughts and internal monologue
- Include more sensory details in every scene
- Develop secondary characters more fully
- Add transitional moments between scenes - show travel, waiting, processing
- Extend the ending with deeper reflection and more closure
- Add more physical choreography to action scenes
- Describe environments in greater detail
- Show more of characters' daily routines and relationships

Format EXACTLY as:
Title: [A title that promises a CINEMATIC EXPERIENCE]

Story:
[Write the complete story as flowing narrative - NO scene labels in the final text]
[Structure it mentally in scenes but write as continuous prose]
[Scene transitions are natural paragraph breaks]
[Let the story flow without "Scene 1:", "Scene 2:" markers]
[Remember: 2500-4000 words MINIMUM 2500]

This is a COMPLETE SHORT FILM. Make viewers SEE it. Make them FEEL it. Make it UNFORGETTABLE.
Write AT LEAST 2500 words. Take your time. Develop everything fully.

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
            logger.error(f"❌ CRITICAL: Story too short: {word_count} words (target: 2500-4000)")
        elif word_count < 2500:
            logger.warning(f"⚠️ Story too short: {word_count} words (target: 2500-4000)")
        elif word_count > 4500:
            logger.warning(f"⚠️ Story may be too long: {word_count} words (target: 2500-4000)")
        else:
            logger.info(f"✓ Story length optimal: {word_count} words (SHORT FILM length)")
        
        return {'title': title, 'story': story}



