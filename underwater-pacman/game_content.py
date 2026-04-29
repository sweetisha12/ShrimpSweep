LEVELS = [
    {
        "id": 1,
        "name": "Easy",
        "difficulty_key": "easy",
        "maze_key": "maze1",
        "shrimp_speed_ms": 340,
        "ghost_speed_ms": 780,
        "ghost_count": 4,
        "bombs": 2,
        "worms": 1,
        "target_points": 1000,
    },
    {
        "id": 2,
        "name": "Medium",
        "difficulty_key": "medium",
        "maze_key": "maze2",
        "shrimp_speed_ms": 395,
        "ghost_speed_ms": 680,
        "ghost_count": 4,
        "bombs": 3,
        "worms": 2,
        "target_points": 1000,
    },
    {
        "id": 3,
        "name": "Hard",
        "difficulty_key": "hard",
        "maze_key": "maze1",
        "shrimp_speed_ms": 455,
        "ghost_speed_ms": 580,
        "ghost_count": 4,
        "bombs": 4,
        "worms": 2,
        "target_points": 1000,
    },
]

# Replace these messages whenever you want custom post-level text.
LEVEL_MESSAGES = {
    1: "The reef opens up. Your shrimp survived the shallows and is ready for the colder mid-depth waters.",
    2: "The squid are closing in. One final push takes your shrimp into the deepest northern waters.",
    3: "You cleared the deepest trench. Your Northern Shrimp rules the reef.",
}

# Placeholder 30-question master list:
# 10 easy, 10 medium, 10 hard.
# You can replace the prompt, options, and answer values later without touching the game logic.
QUESTIONS = {
    "easy": [
        {
            "prompt": "Do Northern Shrimp live in tropical or polar waters?",
            "options": ["Polar waters", "Tropical waters", "Freshwater rivers", "Desert pools"],
            "answer": "Polar waters",
        },
        {
            "prompt": "Are Northern Shrimp herbivores or carnivores?",
            "options": ["Carnivores", "Herbivores", "Only decomposers", "Only filter feeders"],
            "answer": "Carnivores",
        },
        {
            "prompt": "What do Northern Shrimp eat?",
            "options": ["Plankton", "Seagrass", "Kelp", "Coral"],
            "answer": "Plankton",
        },
        {
            "prompt": "Northern Shrimp are a type of what animal group?",
            "options": ["Shrimp", "Mammal", "Bird", "Reptile"],
            "answer": "Shrimp",
        },
        {
            "prompt": "Do Northern Shrimp live near the ocean bottom or high in the sky?",
            "options": ["Near the ocean bottom", "High in the sky", "Inside trees", "On beaches only"],
            "answer": "Near the ocean bottom",
        },
        {
            "prompt": "Are Northern Shrimp found in warm water or cold water?",
            "options": ["Cold water", "Warm water", "Only hot springs", "Only ponds"],
            "answer": "Cold water",
        },
        {
            "prompt": "Which of these is closest to a Northern Shrimp's habitat?",
            "options": ["Ocean", "Volcano", "Forest", "Desert"],
            "answer": "Ocean",
        },
        {
            "prompt": "Northern Shrimp are more closely related to crabs or to jellyfish?",
            "options": ["Crabs", "Jellyfish", "Seaweed", "Sponges"],
            "answer": "Crabs",
        },
        {
            "prompt": "Do Northern Shrimp eat plants only or small animals like plankton too?",
            "options": ["Small animals like plankton too", "Plants only", "Rocks only", "Ice only"],
            "answer": "Small animals like plankton too",
        },
        {
            "prompt": "Which environment would best support Northern Shrimp?",
            "options": ["Cold marine water", "Dry sand dunes", "Tropical rainforest canopy", "Mountain cave"],
            "answer": "Cold marine water",
        },
    ],
    "medium": [
        {
            "prompt": "Northern Shrimp are crustaceans. What phylum are crustaceans part of?",
            "options": ["Arthropoda", "Cnidaria", "Annelida", "Cetacea"],
            "answer": "Arthropoda",
        },
        {
            "prompt": "Northern Shrimp females carry externally fertilized eggs on their body until hatching without nourishing them. What is this called?",
            "options": ["Oviparity", "Ovoviviparity", "Viviparity", "Budding"],
            "answer": "Oviparity",
        },
        {
            "prompt": "Northern Shrimp are crustaceans. Which trait best matches crustaceans?",
            "options": ["Exoskeleton", "Feathers", "Fur", "Scales made of bone"],
            "answer": "Exoskeleton",
        },
        {
            "prompt": "What type of fertilization do Northern Shrimp eggs undergo before being carried externally?",
            "options": ["External fertilization", "Internal fertilization only", "Asexual budding", "Binary fission"],
            "answer": "External fertilization",
        },
        {
            "prompt": "Which of these animals is most closely grouped with Northern Shrimp?",
            "options": ["Lobster", "Jellyfish", "Sea star", "Clam"],
            "answer": "Lobster",
        },
        {
            "prompt": "Which body covering do Northern Shrimp have?",
            "options": ["A hard external shell", "Soft skin only", "Feathers", "Hair"],
            "answer": "A hard external shell",
        },
        {
            "prompt": "Northern Shrimp belong to a group of animals with jointed appendages. What group is this?",
            "options": ["Arthropods", "Cnidarians", "Echinoderms", "Mollusks"],
            "answer": "Arthropods",
        },
        {
            "prompt": "If a female carries eggs on the outside of her body until they hatch, where are the eggs located?",
            "options": ["Externally attached to the body", "Inside a placenta", "Buried in coral", "Floating freely for months"],
            "answer": "Externally attached to the body",
        },
        {
            "prompt": "Which scientific idea best fits Northern Shrimp reproduction as described here?",
            "options": ["Egg-laying", "Live birth with nourishment", "Cloning", "Fragmentation"],
            "answer": "Egg-laying",
        },
        {
            "prompt": "Why are Northern Shrimp classified under Arthropoda?",
            "options": ["They have jointed limbs and an exoskeleton", "They have tentacles and stinging cells", "They have no body symmetry", "They produce flowers"],
            "answer": "They have jointed limbs and an exoskeleton",
        },
    ],
    "hard": [
        {
            "prompt": "What sex are all Northern Shrimp born?",
            "options": ["Male", "Female", "Both sexes at once", "Sexless"],
            "answer": "Male",
        },
        {
            "prompt": "What type of organism are Northern Shrimp?",
            "options": ["Benthic", "Pelagic", "Intertidal", "Terrestrial"],
            "answer": "Benthic",
        },
        {
            "prompt": "Northern Shrimp change from male to female around 2.5 years of age depending on temperature and growth rate. How do warming and acidifying oceans affect Northern Shrimp?",
            "options": ["Less mature females", "More mature females", "No effect at all", "Only more eggs every year"],
            "answer": "Less mature females",
        },
        {
            "prompt": "Northern Shrimp begin life as males and later can become females. This is an example of what?",
            "options": ["Sequential hermaphroditism", "Parthenogenesis", "Metamorphosis into a new species", "Asexual reproduction"],
            "answer": "Sequential hermaphroditism",
        },
        {
            "prompt": "Because Northern Shrimp are benthic, where are they primarily found?",
            "options": ["On or near the seafloor", "At the ocean surface", "On land", "In tree canopies"],
            "answer": "On or near the seafloor",
        },
        {
            "prompt": "Why can ocean warming be harmful to Northern Shrimp populations?",
            "options": ["It can disrupt growth and sex change timing", "It instantly makes them freshwater animals", "It gives them lungs", "It makes them plants"],
            "answer": "It can disrupt growth and sex change timing",
        },
        {
            "prompt": "A drop in pH from ocean acidification means the water is becoming what?",
            "options": ["More acidic", "More basic", "Less salty only", "Warmer only"],
            "answer": "More acidic",
        },
        {
            "prompt": "If fewer Northern Shrimp mature into females, what is a likely population consequence?",
            "options": ["Reduced reproductive output", "Instant extinction of predators", "Unlimited population growth", "They stop molting entirely"],
            "answer": "Reduced reproductive output",
        },
        {
            "prompt": "Which combination of conditions is most important for Northern Shrimp sex change according to your note?",
            "options": ["Temperature and growth rate", "Wave height and moonlight", "Sand color and tides", "Coral cover and sunlight only"],
            "answer": "Temperature and growth rate",
        },
        {
            "prompt": "Northern Shrimp spend much of their time associated with the bottom habitat. Which term best describes that lifestyle?",
            "options": ["Benthic", "Aerial", "Arboreal", "Freshwater pelagic"],
            "answer": "Benthic",
        },
    ],
}

RAW_MAZES = {
    "maze1": """
0 1 1 1 1 1 1 1 1 1 1 1 1 7 8 1 1 1 1 1 1 1 1 1 1 1 1 0
1 + . . . . + . . . . . + 3 3 + . . . . . + . . . . + 1
1 . 2 3 3 2 . 2 3 3 3 2 . 3 3 . 2 3 3 3 2 . 2 3 3 2 . 1
1 p 3 X X 3 . 3 X X X 3 . 3 3 . 3 X X X 3 . 3 X X 3 p 1
1 . 2 3 3 2 . 2 3 3 3 2 . 2 2 . 2 3 3 3 2 . 2 3 3 2 . 1
1 + . . . . + . . + . . + . . + . . + . . + . . . . + 1
1 . 2 3 3 2 . 2 2 . 2 3 3 3 3 3 3 2 . 2 2 . 2 3 3 2 . 1
1 . 2 3 3 2 . 3 3 . 2 3 3 9 9 3 3 2 . 3 3 . 2 3 3 2 . 1
1 + . . . . + 3 3 + . . + 3 3 + . . + 3 3 + . . . . + 1
0 1 1 1 1 6 . 3 9 3 3 2 | 3 3 | 2 3 3 9 3 . 6 1 1 1 1 0
X X X X X 1 . 3 9 3 3 2 | 2 2 | 2 3 3 9 3 . 1 X X X X X
X X X X X 1 . 3 3 n - - n - - n - - n 3 3 . 1 X X X X X
X X X X X 1 . 3 3 | 4 5 5 = = 5 5 4 | 3 3 . 1 X X X X X
1 1 1 1 1 6 . 2 2 | 5 X X X X X X 5 | 2 2 . 6 1 1 1 1 1
n - - - - - + - - n 5 X X X X X X 5 n - - + - - - - - n
1 1 1 1 1 6 . 2 2 | 5 X X X X X X 5 | 2 2 . 6 1 1 1 1 1
X X X X X 1 . 3 3 | 4 5 5 5 5 5 5 4 | 3 3 . 1 X X X X X
X X X X X 1 . 3 3 n - - - - - - - - n 3 3 . 1 X X X X X
X X X X X 1 . 3 3 | 2 3 3 3 3 3 3 2 | 3 3 . 1 X X X X X
0 1 1 1 1 6 . 2 2 | 2 3 3 9 9 3 3 2 | 2 2 . 6 1 1 1 1 0
1 + . . . . + . . + . . + 3 3 + . . + . . + . . . . + 1
1 . 2 3 3 2 . 2 3 3 3 2 . 3 3 . 2 3 3 3 2 . 2 3 3 2 . 1
1 . 2 3 9 3 . 2 3 3 3 2 . 2 2 . 2 3 3 3 2 . 3 9 3 2 . 1
1 P . + 3 3 + . . + . . + - - + . . + . . + 3 3 + . P 1
8 3 2 . 3 3 . 2 2 . 2 3 3 3 3 3 3 2 . 2 2 . 3 3 . 2 3 7
7 3 2 . 2 2 . 3 3 . 2 3 3 9 9 3 3 2 . 3 3 . 2 2 . 2 3 8
1 + . + . . + 3 3 + . . + 3 3 + . . + 3 3 + . . + . + 1
1 . 2 3 3 3 3 9 9 3 3 2 . 3 3 . 2 3 3 9 9 3 3 3 3 2 . 1
1 . 2 3 3 3 3 3 3 3 3 2 . 2 2 . 2 3 3 3 3 3 3 3 3 2 . 1
1 + . . . . . . . . . . + . . + . . . . . . . . . . + 1
0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0
""",
    "maze2": """
1 1 1 1 1 1 1 7 8 1 1 1 1 1 1 1 1 1 1 7 8 1 1 1 1 1 1 1
n - - - - - n 3 3 + . . . . . . . . + 3 3 n - - - - - n
1 1 1 1 1 6 | 3 3 . 2 3 3 3 3 3 3 2 . 3 3 | 6 1 1 1 1 1
0 1 1 1 1 6 | 2 2 . 2 3 3 9 9 3 3 2 . 2 2 | 6 1 1 1 1 0
1 P . . . . + . . + . . + 3 3 + . . + . . + . . . . P 1
1 . 2 3 3 3 3 3 2 . 2 2 . 3 3 . 2 2 . 2 3 3 3 3 3 2 . 1
1 . 3 9 3 3 3 3 2 . 3 3 . 3 3 . 3 3 . 2 3 3 3 3 9 3 . 1
1 . 3 3 + . . . . + 3 3 . 2 2 . 3 3 + . . . . + 3 3 . 1
1 . 3 3 . 2 3 3 2 | 3 3 + . . + 3 3 | 2 3 3 2 . 3 3 . 1
1 . 2 2 . 2 3 9 3 | 3 9 3 3 3 3 9 3 | 3 9 3 2 . 2 2 . 1
1 + . . + . + 3 3 | 2 3 3 3 3 3 3 2 | 3 3 + . + . . + 1
0 1 1 1 1 6 . 3 3 n - - - - - - - - n 3 3 . 6 1 1 1 1 0
0 1 1 1 1 6 . 3 3 | 4 5 5 = = 5 5 4 | 3 3 . 6 1 1 1 1 0
1 + . . . . + 3 3 | 5 X X X X X X 5 | 3 3 + . . . . + 1
1 . 2 3 3 2 . 2 2 | 5 X X X X X X 5 | 2 2 . 2 3 3 2 . 1
1 . 2 3 9 3 + - - n 5 X X X X X X 5 n - - + 3 9 3 2 . 1
1 + . + 3 3 . 2 2 | 4 5 5 5 5 5 5 4 | 2 2 . 3 3 + . + 1
0 1 6 . 3 3 . 3 3 n - n - - - - n - n 3 3 . 3 3 . 6 1 0
X X 1 . 3 3 . 3 9 3 2 | 2 3 3 2 | 2 3 9 3 . 3 3 . 1 X X
X X 1 . 2 2 . 2 3 3 2 | 3 X X 3 | 2 3 3 2 . 2 2 . 1 X X
X X 1 + . . + . . . . + 3 X X 3 + . . . . + . . + 1 X X
X X 1 . 2 3 3 3 3 3 2 . 3 X X 3 . 2 3 3 3 3 3 2 . 1 X X
1 1 6 . 2 3 3 9 9 3 2 . 2 3 3 2 . 2 3 9 9 3 3 2 . 6 1 1
n - - + . . + 3 3 + . + - - - - + . + 3 3 + . . + - - n
1 1 6 . 2 2 . 3 3 . 2 3 3 3 3 3 3 2 . 3 3 . 2 2 . 6 1 1
0 1 6 . 3 3 . 2 2 . 2 3 3 9 9 3 3 2 . 2 2 . 3 3 . 6 1 0
1 P . + 3 3 + . . + . . + 3 3 + . . + . . + 3 3 + . P 1
1 . 2 3 9 3 . 2 3 3 3 2 . 3 3 . 2 3 3 3 2 . 3 9 3 2 . 1
1 . 2 3 3 2 . 2 3 3 3 2 . 2 2 . 2 3 3 3 2 . 2 3 3 2 . 1
1 + . . . . + . . . . . + . . + . . . . . + . . . . + 1
0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0
""",
}

MAZE_META = {
    "maze1": {"player_start": (15, 23), "ghost_home": (13, 12)},
    "maze2": {"player_start": (16, 23), "ghost_home": (13, 12)},
}


def _convert_maze(raw_maze):
    walkable = {".", "+", "p", "P", "-", "|", "n", "="}
    rows = [line.split() for line in raw_maze.strip().splitlines()]
    return ["".join("." if cell in walkable else "#" for cell in row) for row in rows]


MAZES = {name: _convert_maze(raw_maze) for name, raw_maze in RAW_MAZES.items()}
MAZE = MAZES["maze1"]
