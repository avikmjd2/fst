"""
Lexicon: comprehensive word stem lists organized by part of speech.
These are the stems that the FST can recognize and analyze/generate.
"""

# =============================================================================
# NOUNS - Regular (take -s for plural)
# =============================================================================
REGULAR_NOUNS = [
    # Common everyday nouns
    "dog", "cat", "bird", "fish", "horse", "bear", "lion", "tiger", "wolf",
    "book", "pen", "desk", "chair", "table", "lamp", "clock", "phone", "screen",
    "car", "bus", "train", "boat", "ship", "plane", "truck", "bike",
    "house", "room", "door", "wall", "floor", "roof", "window", "garden",
    "tree", "flower", "plant", "seed", "root", "leaf", "branch",
    "road", "street", "path", "bridge", "hill", "mountain", "river", "lake",
    "town", "village", "farm", "park", "school", "church", "shop", "bank",
    "hand", "arm", "leg", "head", "eye", "ear", "nose", "mouth", "neck",
    "king", "queen", "girl", "boy", "friend", "brother", "sister", "parent",
    "song", "game", "team", "group", "club", "crowd", "band", "pair",
    "year", "month", "week", "hour", "morning", "evening", "night",
    "thing", "part", "point", "end", "turn", "step", "sign", "mark",
    "word", "letter", "number", "page", "line", "song", "sound", "song",
    "cup", "bowl", "plate", "pan", "pot", "bag", "hat", "coat", "boot",
    "job", "task", "goal", "plan", "test", "tool", "rule", "law",
    "fact", "idea", "thought", "dream", "fear", "pain", "joy",
    "rain", "wind", "storm", "cloud", "star", "moon", "sun",
    "field", "forest", "island", "ocean", "coast", "beach", "pool",
    "meal", "egg", "bean", "grain", "fruit", "nut", "meat",
    "ring", "chain", "string", "thread", "nail", "pin", "wheel",
    "seat", "bed", "pillow", "blanket", "curtain", "carpet", "mirror",
    "gift", "card", "ticket", "coin", "bill", "dollar", "pound",
    "war", "gun", "bomb", "sword", "shield", "prison", "court",
    "student", "teacher", "doctor", "worker", "farmer", "artist", "engineer",
    "problem", "question", "answer", "reason", "result", "action", "event",
    "moment", "season", "signal", "lesson", "version", "section", "station",
    "ocean", "region", "nation", "person", "captain", "woman",
    "organ", "iron", "melon", "lemon", "ribbon", "button", "dragon",
    "market", "garden", "pocket", "basket", "ticket", "bucket", "blanket",
    "unit", "spirit", "habit", "merit", "limit", "visit", "credit",
    "record", "report", "effort", "method", "period", "moment", "forest",
    "account", "amount", "argument", "government", "movement", "agreement",
    "experiment", "instrument", "element", "statement", "treatment",
]

# Nouns ending in sibilant (take -es for plural via spelling rule)
# These are included in REGULAR_NOUNS and handled by the e-insertion rule
SIBILANT_NOUNS = [
    "watch", "match", "catch", "patch", "batch", "witch", "switch",
    "church", "search", "march", "porch", "torch",
    "dish", "wish", "fish", "brush", "crash", "flash", "rush", "push",
    "bus", "gas", "class", "glass", "dress", "kiss", "miss", "loss", "mass",
    "box", "fox", "tax", "mix", "fix",
    "buzz", "jazz", "quiz",
    "judge", "bridge", "edge", "badge", "ledge", "ridge",
    "place", "face", "space", "race", "price", "voice", "choice", "chance",
    "piece", "prince", "office", "practice", "surface", "sentence",
]

# Nouns ending in consonant+y (y->ies for plural via spelling rule)
CONSONANT_Y_NOUNS = [
    "city", "baby", "body", "story", "party", "family", "country",
    "company", "army", "navy", "enemy", "lady", "duty", "copy",
    "study", "theory", "memory", "history", "factory", "library",
    "century", "industry", "quality", "quantity", "activity",
    "community", "opportunity", "university", "difficulty", "authority",
    "ability", "reality", "society", "variety", "property", "penalty",
    "strategy", "category", "salary", "ceremony", "battery",
    "fly", "sky", "berry", "cherry", "puppy", "bunny", "penny",
    "ruby", "pony", "daisy", "lily", "candy", "jelly", "curry",
]

# Nouns ending in vowel+y (regular -s plural, no y-change)
VOWEL_Y_NOUNS = [
    "boy", "day", "key", "toy", "way", "play", "ray", "bay", "joy",
    "guy", "essay", "monkey", "turkey", "donkey", "valley", "journey",
    "holiday", "birthday", "highway", "railway", "doorway", "pathway",
    "survey", "convoy", "decoy", "employ", "enjoy", "annoy", "destroy",
]

# Combine all regular nouns (sibilant and y-nouns are handled by spelling rules)
ALL_REGULAR_NOUNS = (
    REGULAR_NOUNS + SIBILANT_NOUNS + CONSONANT_Y_NOUNS + VOWEL_Y_NOUNS
)

# =============================================================================
# VERBS - Regular (take -ed, -s, -ing via spelling rules)
# =============================================================================
REGULAR_VERBS = [
    # Simple regular verbs (CVC patterns handled as irregulars for doubling)
    "walk", "talk", "work", "play", "start", "want", "need", "help",
    "look", "ask", "call", "turn", "seem", "show", "add", "move",
    "wait", "pull", "push", "fill", "open", "watch", "pick", "lift",
    "miss", "pass", "touch", "reach", "kill", "cook", "rain", "join",
    "plant", "mark", "clean", "form", "search", "order", "sort",
    "check", "count", "laugh", "point", "rest", "stay", "talk",
    "climb", "cross", "knock", "last", "list", "match", "mix",
    "paint", "thank", "train", "trick", "trust", "visit", "yell",
    "act", "aim", "appear", "approach", "attack", "attempt", "avoid",
    "belong", "block", "borrow", "burn", "claim", "collect", "command",
    "complain", "contain", "correct", "cover", "deliver", "demand",
    "depend", "design", "develop", "differ", "discuss", "dream",
    "earn", "exist", "explain", "express", "fail", "follow", "gain",
    "gather", "guess", "happen", "head", "help", "hunt", "inform",
    "insist", "install", "intend", "interest", "invent", "invest",
    "launch", "mention", "obtain", "occur", "perform", "permit",
    "prevent", "print", "protect", "protest", "publish", "punish",
    "question", "record", "reflect", "reform", "regard", "reject",
    "remark", "repeat", "request", "respect", "respond", "return",
    "reveal", "reward", "risk", "select", "sign", "suggest", "support",
    "surround", "suspect", "transform", "transport", "travel",
    "offer", "suffer", "consider", "remember", "discover", "deliver",
    "answer", "enter", "matter", "number", "power", "weather",
    "wander", "wonder", "murder", "whisper", "gather", "bother",
    "afford", "allow", "confirm", "connect", "construct", "consult",
    "contrast", "control", "convert", "counsel", "defend", "demand",
    "document", "effect", "elect", "employ", "enjoy", "establish",
    "conduct", "conflict", "consent", "consist", "construct",
    # Verbs ending in -e (e-deletion applies)
    "hope", "like", "love", "live", "move", "use", "close", "change",
    "place", "care", "smile", "dance", "share", "compare", "prepare",
    "continue", "include", "provide", "require", "describe", "imagine",
    "believe", "receive", "achieve", "notice", "produce", "reduce",
    "introduce", "announce", "arrange", "arrive", "assume", "blame",
    "breathe", "capture", "chase", "combine", "communicate", "compose",
    "contribute", "convince", "create", "decide", "declare", "decline",
    "define", "demonstrate", "determine", "divide", "examine",
    "escape", "excuse", "exercise", "explore", "expose", "force",
    "generate", "guide", "hate", "ignore", "indicate", "inspire",
    "involve", "isolate", "joke", "locate", "manage", "measure",
    "migrate", "name", "note", "observe", "organize", "pause",
    "persuade", "phone", "practise", "praise", "promise", "quote",
    "raise", "realize", "recognize", "refuse", "relate", "release",
    "remove", "replace", "rescue", "resolve", "retire", "revise",
    "save", "score", "seize", "serve", "settle", "shape", "shave",
    "smoke", "solve", "stare", "store", "suppose", "survive", "taste",
    "trade", "translate", "trouble", "vote", "waste",
    # Verbs ending in consonant+y (y->i rule applies)
    "carry", "worry", "study", "try", "cry", "dry", "hurry", "marry",
    "bury", "copy", "deny", "apply", "supply", "rely", "reply",
    "vary", "satisfy", "identify", "occupy", "qualify", "classify",
    "modify", "notify", "specify", "multiply", "simplify", "justify",
    "destroy", "employ", "enjoy", "annoy", "delay", "display",
    "obey", "pray", "spray", "stay", "sway",
]

# =============================================================================
# ADJECTIVES
# =============================================================================

# Short adjectives that take -er/-est
SHORT_ADJECTIVES = [
    "small", "tall", "short", "long", "old", "young", "fast", "slow",
    "hard", "soft", "cold", "warm", "cool", "dark", "light", "deep",
    "high", "low", "near", "weak", "strong", "loud", "quiet", "bright",
    "sharp", "smooth", "rough", "tough", "sweet", "fresh", "clean",
    "clear", "dear", "dull", "fair", "firm", "flat", "full", "grand",
    "great", "keen", "kind", "mild", "neat", "new", "odd", "plain",
    "poor", "proud", "pure", "quick", "raw", "real", "rich", "round",
    "smooth", "sour", "stiff", "strict", "swift", "thick", "tight",
    "vast", "warm", "wild", "bold", "broad", "calm", "cheap", "blank",
]

# Short adjectives ending in -e (take -r/-st, e-deletion handles it)
E_ADJECTIVES = [
    "nice", "fine", "large", "close", "late", "rude", "safe", "wide",
    "brave", "pale", "rare", "pure", "huge", "cute", "strange", "loose",
    "fierce", "gentle", "humble", "mature", "noble", "polite", "remote",
    "severe", "simple", "sincere", "tense", "vague",
]

# Short adjectives ending in consonant+y
Y_ADJECTIVES = [
    "happy", "easy", "busy", "dirty", "early", "funny", "heavy",
    "lazy", "lucky", "noisy", "pretty", "silly", "tiny", "ugly",
    "angry", "crazy", "empty", "fancy", "guilty", "handy", "healthy",
    "hungry", "icy", "juicy", "lonely", "messy", "mighty", "nasty",
    "rainy", "scary", "shiny", "skinny", "sleepy", "smelly", "smoky",
    "snowy", "sorry", "steady", "stormy", "sunny", "tidy", "tricky",
    "wealthy", "windy", "worthy", "cloudy", "dusty", "foggy",
]

# Long adjectives (only base form, comparative uses "more/most")
LONG_ADJECTIVES = [
    "beautiful", "important", "different", "possible", "difficult",
    "interesting", "necessary", "available", "particular", "popular",
    "traditional", "political", "economic", "dangerous", "wonderful",
    "comfortable", "powerful", "successful", "independent", "responsible",
    "intelligent", "professional", "emotional", "physical", "natural",
    "personal", "cultural", "musical", "medical", "social", "financial",
    "digital", "original", "normal", "formal", "central", "general",
    "external", "internal", "official", "special", "typical", "usual",
    "visual", "actual", "annual", "critical", "essential", "final",
    "global", "historical", "initial", "legal", "liberal", "local",
    "logical", "mental", "moral", "national", "obvious", "perfect",
    "relevant", "religious", "scientific", "serious", "significant",
    "similar", "specific", "technical", "terrible", "traditional",
    "unlikely", "unusual", "valuable", "violent", "absolute",
    "academic", "acceptable", "accurate", "adequate", "aggressive",
    "appropriate", "automatic", "basic", "capable", "certain",
    "chemical", "classical", "complex", "comprehensive", "confident",
    "conscious", "consistent", "constant", "continuous", "conventional",
    "creative", "curious", "desperate", "dramatic", "eastern", "eastern",
    "efficient", "electronic", "enormous", "environmental", "evident",
    "excellent", "excessive", "expensive", "familiar", "famous",
    "fantastic", "favorable", "foreign", "friendly", "fundamental",
    "generous", "genuine", "grateful", "horrible", "immediate",
    "impressive", "incredible", "inevitable", "innocent", "intense",
]

# Combine all adjective stems that take comparative/superlative inflection
ALL_INFLECTING_ADJECTIVES = SHORT_ADJECTIVES + E_ADJECTIVES + Y_ADJECTIVES
ALL_ADJECTIVES = ALL_INFLECTING_ADJECTIVES + LONG_ADJECTIVES

# =============================================================================
# DERIVATIONAL MORPHOLOGY STEMS
# =============================================================================
# Adjectives that can take un- prefix
UN_ADJECTIVES = [
    "happy", "fair", "kind", "clear", "safe", "real", "sure", "true",
    "lucky", "easy", "clean", "certain", "common", "comfortable",
    "conscious", "familiar", "friendly", "healthy", "important",
    "likely", "natural", "necessary", "pleasant", "popular",
    "reasonable", "stable", "usual", "willing",
]

# Verbs that can take re- prefix
RE_VERBS = [
    "build", "create", "do", "make", "open", "play", "start", "write",
    "arrange", "check", "connect", "consider", "define", "design",
    "discover", "enter", "establish", "fill", "form", "gain",
    "join", "live", "load", "locate", "move", "name", "order",
    "organize", "place", "print", "read", "search", "set", "shape",
    "store", "think", "turn", "use", "view", "visit", "work",
]

# Adjectives/nouns that take -ness suffix (ADJ -> N)
NESS_ADJECTIVES = [
    "happy", "sad", "dark", "kind", "weak", "bold", "cold", "cool",
    "deaf", "fair", "fond", "glad", "hard", "keen", "loud", "mild",
    "neat", "odd", "pale", "plain", "rude", "sick", "soft", "sweet",
    "tall", "warm", "wild", "calm", "clean", "clear", "dull",
    "fresh", "good", "great", "rough", "sharp", "smooth", "sour",
    "stiff", "thick", "tight",
    "aware", "bitter", "clever", "eager", "gentle", "lonely",
    "busy", "crazy", "dirty", "dizzy", "empty", "easy", "funny",
    "guilty", "happy", "heavy", "hungry", "lazy", "lonely",
    "lucky", "messy", "mighty", "nasty", "silly", "sleepy",
    "tidy", "ugly", "worthy",
]

# Adjectives that take -ly suffix (ADJ -> ADV)
LY_ADJECTIVES = [
    "bad", "bright", "calm", "cheap", "clean", "clear", "close",
    "cold", "cool", "dark", "deep", "fair", "firm", "free", "fresh",
    "full", "grand", "great", "hard", "high", "keen", "kind", "loud",
    "low", "mild", "neat", "new", "nice", "odd", "open", "plain",
    "poor", "proud", "pure", "quick", "quiet", "rare", "real", "rich",
    "rough", "round", "safe", "sharp", "short", "slow", "smooth",
    "soft", "sour", "strange", "strict", "strong", "sure", "sweet",
    "swift", "thick", "tight", "true", "warm", "weak", "wide", "wild",
    "brave", "fierce", "gentle", "humble", "polite", "remote",
    "severe", "simple", "sincere", "vague",
    "angry", "busy", "crazy", "dirty", "dizzy", "early", "easy",
    "fancy", "funny", "guilty", "happy", "heavy", "hungry", "icy",
    "lazy", "lonely", "lucky", "messy", "mighty", "nasty", "noisy",
    "pretty", "scary", "silly", "sleepy", "steady", "tidy",
    "tricky", "ugly", "worthy",
]
