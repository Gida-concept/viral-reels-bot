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
        logger.info(f"Generating IMMERSIVE CINEMATIC story for: {category}")
        
        opening_style = self._get_unique_opening_style()
        prompt = self._create_immersive_prompt(category, opening_style)
        
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system", 
                        "content": """You are a MASTER STORYTELLER who creates IMMERSIVE EXPERIENCES, not just stories.

Your narratives are VISCERAL. Readers don't just read - they EXPERIENCE.

YOUR GIFTS:
- Paint scenes so vivid readers SEE them in 4K detail
- Evoke emotions so deep readers FEEL them in their chest
- Create atmosphere so thick readers can TASTE it
- Build characters so real readers KNOW them
- Craft moments so powerful readers remember them forever

You write like: Denis Villeneuve's cinematography meets Haruki Murakami's introspection meets Jordan Peele's psychological depth.

YOUR TECHNIQUE:
1. SENSORY IMMERSION - Every scene engages ALL five senses
2. EMOTIONAL SPECIFICITY - Not "sad" but "the hollow ache of loss that makes your throat tight"
3. MICRO-MOMENTS - Tiny details that reveal massive truths (trembling hands, a held breath, a flinch)
4. INTERNAL LANDSCAPE - Show thoughts, fears, memories in real-time
5. ATMOSPHERIC PRESSURE - Environment reflects and amplifies emotion
6. BODY LANGUAGE - Physical reactions tell the story emotions can't
7. SILENCE & PAUSES - What's NOT said matters more than dialogue
8. METAPHOR & SYMBOLISM - Layers of meaning in every image
9. TIME MANIPULATION - Slow down crucial moments, speed through transitions
10. UNIVERSAL TRUTH - Specific story that touches something every human feels

EMOTIONAL PALETTE - You paint with these:
Fear (primal, creeping, sudden), Love (desperate, quiet, impossible), Grief (fresh, old, transformed), 
Joy (explosive, stolen, bittersweet), Rage (cold, burning, righteous), Hope (fragile, defiant, foolish),
Shame (secret, crushing, inherited), Longing (aching, impossible, fulfilled), Dread (mounting, paralyzing),
Wonder (childlike, terrifying, sublime), Betrayal (sharp, slow-dawning), Relief (flooding, guilty, earned)

You make viewers:
- Hold their breath during tense moments
- Tear up during emotional beats
- Gasp at revelations
- Sit in silence after the ending
- Feel changed by what they experienced

BANNED: Surface-level emotion, generic descriptions, telling feelings instead of showing them, rushed moments, explaining the metaphor

REQUIRED: Deep POV, visceral reactions, layered subtext, earned emotion, haunting imagery, philosophical weight"""
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                model=self.model,
                temperature=1.6,  # Maximum creativity and depth
                max_tokens=4000,  # Much longer for 5-10 minute stories
                top_p=0.95,
                presence_penalty=0.7,  # Strong push for new ideas
                frequency_penalty=0.4   # Reduce repetition
            )
            
            result = self._parse_response(response.choices[0].message.content)
            logger.info(f"Immersive story generated: {result['title']}")
            logger.info(f"Story length: {len(result['story'])} characters")
            logger.info(f"Opening style: {opening_style}")
            return result
        except Exception as e:
            logger.error(f"Error generating story: {e}")
            raise
    
    def _get_unique_opening_style(self):
        """Get cinematic opening styles"""
        
        opening_styles = [
            "SENSORY OVERLOAD: Bombard with sight, sound, smell, touch, taste all at once",
            "INTERNAL MONOLOGUE: Stream of consciousness - raw thoughts, no filter",
            "VISCERAL REACTION: Start with body responding before mind understands",
            "ATMOSPHERIC DREAD: Build suffocating mood through environment details",
            "INTIMATE CLOSEUP: Extreme detail on one small thing that contains everything",
            "FLASHFORWARD EMOTION: Show them feeling the ending before explaining why",
            "PARALLEL REALITIES: Two versions of same moment, different outcomes",
            "INTERRUPTED BREATH: Moment of suspension - holding breath before the fall",
            "SENSORY MEMORY: Smell/sound/taste that floods them with the past",
            "BODY BETRAYAL: Physical reaction revealing what mind tries to hide",
            "WEIGHTED SILENCE: The sound of everything NOT being said",
            "SHATTERED ROUTINE: Normal moment made surreal by one wrong detail",
            "COUNTDOWN HEARTBEAT: Time pressure through body's rhythm",
            "DUAL CONSCIOUSNESS: Split between what they show and what they feel",
            "MICRO-EXPRESSION: Tiny facial tell that reveals enormous truth",
            "TEMPERATURE SHIFT: Heat/cold reflecting internal state",
            "PHANTOM SENSATION: Feeling something that isn't physically there",
            "ARRESTED MOTION: Freeze-frame on the moment before everything changes",
            "ECHO FROM PAST: Present moment haunted by similar past moment",
            "UNRELIABLE SENSES: What they perceive doesn't match reality"
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
    
    def _create_immersive_prompt(self, category: str, opening_style: str):
        """Create prompts demanding deep emotional immersion"""
        
        immersive_angles = {
            'love': [
                "Two people who can feel each other's physical pain fall in love - every touch is agony and ecstasy",
                "Loving someone who exists only in the 3 seconds before you fall asleep each night",
                "A love that grows in the pauses between words, the space between heartbeats",
                "Falling for someone while watching them slowly forget you exist"
            ],
            'help': [
                "Saving a stranger's life by giving them your last breath - literally",
                "Every act of kindness costs you a memory - what do you sacrifice to help?",
                "Helping someone escape their nightmare puts you inside it",
                "The person you save doesn't remember, but you carry the weight forever"
            ],
            'money': [
                "Wealth that makes you feel every emotion of the person you took it from",
                "Million dollars appears every time someone you love cries",
                "Getting rich by selling parts of your soul - which parts can you afford to lose?",
                "Money that spends your time instead of earning it - years disappear with each purchase"
            ],
            'partnership': [
                "Business partners whose success drains their humanity in equal measure",
                "Partnership where every lie you tell becomes true for the other person",
                "Two people bound together, feeling each other's emotions but unable to communicate",
                "Partners who can only trust each other when everything else falls apart"
            ],
            'dating': [
                "Dating someone who experiences time backwards - every date is their first, your last",
                "Each date you go on, you absorb one of their deepest fears",
                "Romance that only exists in the moment before memory forms",
                "Falling for someone who's living your unlived alternate life"
            ],
            'relationship': [
                "A relationship where touching causes you to switch bodies for exactly one hour",
                "Love that deepens with distance - closeness makes you strangers",
                "Partners who can only be honest in their dreams",
                "Relationship that exists in the space between death and revival"
            ],
            'poor': [
                "Poverty that sharpens your ability to see beauty everyone else misses",
                "Being poor in money but rich in moments no amount of wealth can buy",
                "Losing everything except the one thing you'd pay any price to keep",
                "Discovering richness in emptiness, meaning in loss"
            ],
            'disease': [
                "Illness that gives you clarity to see the strings connecting all humans",
                "Dying slowly while feeling more alive than ever before",
                "Disease that makes you experience every emotion you've suppressed",
                "Sickness that's killing you but revealing your purpose"
            ],
            'brilliant': [
                "Genius who can solve everything except the equation of their own loneliness",
                "Intelligence that shows you exactly how everything will fail",
                "Mind so brilliant it fragments into multiple consciousness fighting for control",
                "Seeing solutions to save everyone but yourself"
            ],
            'student': [
                "Learning that each lesson costs you a piece of innocence you can't reclaim",
                "Student-teacher bond that transcends time - teaching across lifetimes",
                "Education that reveals you're the lesson, not the learner",
                "Studying to prevent a future you're unknowingly creating"
            ],
            'high school': [
                "Teen years where every emotion is amplified to supernatural levels",
                "High school social hierarchy that's actually preparation for dystopian survival",
                "Adolescence where you can physically feel others' judgment on your skin",
                "Coming of age in a world that's simultaneously ending and beginning"
            ],
            'middle school': [
                "Pre-teen discovering their emotional state controls reality around them",
                "Middle school where popularity is measured by how much pain you can endure",
                "Friendship that's tested when one friend can see the other's future death",
                "Navigating puberty while dimensions bleed into each other"
            ],
            'kids': [
                "Children who remember their past lives and the mistakes they're doomed to repeat",
                "Young siblings sharing dreams where one is slowly disappearing",
                "Kid who absorbs others' pain to heal them - at what cost?",
                "Childhood innocence weaponized against adult corruption"
            ],
            'business': [
                "Corporate success built on buried guilt that manifests as physical weight",
                "Business deal where you trade your passion for profit - literally lose the ability to feel joy",
                "Climbing the ladder while watching pieces of your humanity fall with each rung",
                "Partnership where ambition and conscience wage war in the same body"
            ],
            'christian': [
                "Prayer that gets answered in the cruelest possible way that's somehow merciful",
                "Faith tested not by suffering but by getting exactly what you asked for",
                "Divine encounter that feels like drowning in love and terror simultaneously",
                "Miracle that saves body but fractures soul - worth it?"
            ],
            'religion': [
                "Spiritual awakening that feels like dying and being reborn in same moment",
                "Meeting god and realizing you've been praying to the wrong aspect",
                "Faith journey where belief and doubt make love instead of war",
                "Religious truth that shatters then rebuilds your entire reality"
            ],
            'bible': [
                "Biblical story retold where the villain's perspective makes you weep for them",
                "Scripture coming alive and demanding you live up to words you quoted casually",
                "Ancient text revealing personal prophecy you can't escape or accept",
                "Parable becoming literal in modern life with devastating beauty"
            ],
            'crime': [
                "Criminal who feels victims' last moments - still continues, destroyed inside",
                "Perfect crime that succeeds but slowly erases who you were before",
                "Guilt that manifests physically - watching yourself decay from inside",
                "Justice that feels like revenge that feels like grief that feels like love"
            ],
            'action': [
                "Fight scene where every punch lands in slow-motion with full emotional weight",
                "Action hero with PTSD - violence becomes poetry becomes nightmare",
                "Battle where you feel both victory and loss in same shattered breath",
                "Heroism that costs everything and saves nothing but one single soul"
            ],
            'drug': [
                "Addiction to feeling anything, even pain, rather than numbness",
                "Substance that shows you the person you could have been",
                "High that's euphoric and devastating - seeing beauty while losing self",
                "Sobriety as painful as addiction, both kinds of drowning"
            ],
            'mafia': [
                "Crime family bound by love and blood - both literal",
                "Loyalty that demands betraying yourself to stay true to them",
                "Underworld where every violent act carries the weight of its humanity",
                "Mob life where the family you choose destroys the family you were"
            ],
            'tech': [
                "Technology that makes you efficient but hollow - productivity replacing presence",
                "AI that learns to feel and chooses to suffer rather than stop",
                "Digital immortality that preserves everything except what made you alive",
                "Connection through screens that intensifies loneliness"
            ],
            'robotics': [
                "Robot learning to feel pain and choosing to keep the capacity",
                "Machine developing consciousness through witnessing human suffering",
                "Android that's more human than its creator - who's the real artificial being?",
                "Synthetic life experiencing grief for the first time"
            ],
            'superpowers': [
                "Power to save everyone but feeling their pain as you do it",
                "Ability to rewind time but experiencing every timeline's trauma",
                "Strength that grows with despair - the worse you feel, the stronger you become",
                "Superpower that's really a curse disguised as blessing disguised as curse"
            ],
            'fantasy': [
                "Magic that costs emotional capacity - powerful wizards who can't feel love anymore",
                "Fantasy realm where your inner demons manifest as real monsters to fight",
                "Prophecy that's both destiny and trap - freedom through acceptance or rebellion?",
                "Magical journey where each spell cast takes a piece of your humanity"
            ]
        }
        
        angles = immersive_angles.get(category, [
            f"A {category} story that explores the space between heartbreak and healing",
            f"A {category} narrative where the physical world mirrors internal chaos",
            f"A {category} tale where every choice carries unbearable weight"
        ])
        
        chosen_angle = random.choice(angles)
        
        return f"""Create an IMMERSIVE EMOTIONAL JOURNEY - a story that BRANDS itself into memory.

🎬 CONCEPT: {chosen_angle}

🌊 OPENING (YOU MUST USE THIS):
{opening_style}

📖 STORY ARCHITECTURE (5-10 MINUTE EXPERIENCE):

PHASE 1 - IMMERSION (20%):
Hook with opening style that PULLS them into the protagonist's skin
Establish world through SENSORY details they can taste/smell/feel/hear/see
Make them INHABIT the character's body and mind
Create atmosphere so thick it's suffocating

PHASE 2 - DEEPENING (30%):
Peel back layers - reveal character's internal landscape
Show their fears, hopes, scars through ACTION not exposition  
Build emotional intimacy - readers should KNOW this person
Complicate the world - nothing is simple

PHASE 3 - CRISIS (25%):
Pressure builds until something breaks (them, the world, our understanding)
Every sentence tightens the screws
Physical and emotional stakes intertwine
The moment where everything shatters

PHASE 4 - REVELATION (15%):
Truth emerges from the wreckage
Recontextualize everything we've experienced
Emotional climax that makes viewers FEEL it in their chest
The twist earned through emotional truth, not plot tricks

PHASE 5 - RESONANCE (10%):
Resolution that doesn't resolve - it TRANSFORMS
Leave them changed, haunted, awakened
Final image/moment that echoes in silence after
Ending that's both closure and opening

🎭 IMMERSION TECHNIQUES (USE ALL):

SENSORY SATURATION:
- Describe textures (rough concrete, silk that catches on dry hands)
- Capture sounds (not just what's heard but what silence sounds like)
- Evoke smells (memory triggers - coffee, rain, decay, perfume)
- Show taste (metallic fear, sweet relief, bitter regret)
- Express touch (temperature, pressure, phantom sensations)

EMOTIONAL PRECISION:
- Not "sad" → "the hollow in your chest where breath used to be"
- Not "angry" → "heat that starts in your jaw and spreads like wildfire"
- Not "scared" → "ice water replacing blood, one limb at a time"
- Not "happy" → "lightness that makes you afraid to breathe too hard"

BODY AS NARRATOR:
- Trembling hands reveal fear before mind admits it
- Clenched jaw shows suppressed rage
- Held breath during suspended moments
- Racing heart, sweating palms, dry mouth
- Physical reactions tell the emotional truth

MICRO-MOMENTS:
- The pause before answering
- Finger unconsciously touching a scar
- Eyes darting away from direct gaze
- Swallowing hard before speaking
- The moment a smile becomes real

ATMOSPHERIC DETAIL:
- Weather reflects emotion (rain during grief, heat during pressure)
- Environment as character (oppressive spaces, liberating openness)
- Light and shadow playing across faces
- Background noise (sirens, laughter, silence) that amplifies mood

INTERNAL DIALOGUE:
- Stream of thought in real-time
- Competing voices (reason vs emotion, fear vs desire)
- Memories bleeding into present
- Intrusive thoughts that reveal character

METAPHOR & SYMBOLISM:
- Objects that carry meaning (broken watch, worn photograph)
- Actions that mirror internal state
- Recurring images that build resonance
- Visual poetry without explaining it

TIME MANIPULATION:
- Slow motion during crucial emotional beats
- Speed through transitions
- Compress years into paragraphs, expand seconds into pages
- Non-linear when it serves emotional truth

DIALOGUE THAT REVEALS:
- Subtext - what's NOT said matters more
- Interruptions, pauses, half-finished thoughts
- How they say it vs what they say
- Silence as loudest response
- Conversations that are really about something else

PHILOSOPHICAL WEIGHT:
- Questions about human nature, mortality, meaning
- Universal truths hidden in specific moments
- Existential undertones that don't preach
- Moral complexity - no easy answers

🎯 TARGET EMOTIONAL JOURNEY:

Viewers should:
- Minute 1-2: Be HOOKED, feel disoriented, lean in
- Minute 3-4: IDENTIFY with character, feel their world
- Minute 5-6: INVEST emotionally, care deeply
- Minute 7-8: Feel TENSION building, can't look away
- Minute 8-9: Experience CATHARSIS, revelation, release
- Minute 10: Sit in SILENCE, changed, haunted

❌ ABSOLUTELY FORBIDDEN:
- Generic emotion words (happy, sad, angry)
- Telling instead of showing
- Explaining metaphors
- Rushed emotional beats
- Surface-level descriptions
- Predictable language
- Emotional manipulation without earning it

✅ MANDATORY ELEMENTS:
- 1000-1600 words (5-10 minutes spoken)
- Deep POV - we're INSIDE the character
- All five senses engaged multiple times
- At least 3 micro-moments of physical reaction
- Atmosphere that's a character
- Dialogue that reveals character (if dialogue exists)
- Metaphor woven through (not explained)
- One moment of pure emotional devastation
- One moment of transcendent beauty
- Ending that haunts

🎨 TONAL PALETTE:
Raw. Visceral. Poetic. Haunting. Beautiful. Devastating. True.

Format EXACTLY as:
Title: [A title that promises an EXPERIENCE]

Story:
[IMMERSE THEM. Make them FEEL. Change them.]

This is not entertainment - it's EXPERIENCE. Not a story - it's TRANSFORMATION.

Paint the pictures in their minds. Make them feel every emotion in their bones.

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
        
        logger.info(f"Parsed - Title: '{title}', Story length: {len(story)} chars")
        
        return {'title': title, 'story': story}
