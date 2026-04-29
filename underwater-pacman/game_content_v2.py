LEVELS = [
    {
        "id": 1,
        "name": "Easy",
        "difficulty_key": "easy",
        "maze_key": "maze1",
        "shrimp_speed_ms": 220,
        "ghost_speed_ms": 520,
        "ghost_count": 4,
        "bombs": 2,
        "worms": 5,
        "target_points": 1000,
    },
    {
        "id": 2,
        "name": "Medium",
        "difficulty_key": "medium",
        "maze_key": "maze2",
        "shrimp_speed_ms": 280,
        "ghost_speed_ms": 400,
        "ghost_count": 4,
        "bombs": 5,
        "worms": 3,
        "target_points": 1000,
    },
    {
        "id": 3,
        "name": "Hard",
        "difficulty_key": "hard",
        "maze_key": "maze1",
        "shrimp_speed_ms": 420,
        "ghost_speed_ms": 180,
        "ghost_count": 5,
        "bombs": 15,
        "worms": 1,
        "plankton_multiplier": 0.5,
        "target_points": 1000,
    },
]

# Replace these messages whenever you want custom post-level text.
LEVEL_MESSAGES = {
    1: "Easy: pHresh & CO₂l. The ocean is still survivable, but CO₂ is starting to matter.",
    2: "Medium: CO₂ncerning pH. The water chemistry is shifting, and survival is getting harder.",
    3: "Hard: Naked and Acidi-fied. The ocean is at its breaking point. Survive the chaos.",
}

QUESTIONS = {
    "easy": [
        {"prompt": "Northern shrimp live in what type of water?", "options": ["Warm tropical water", "Cold ocean water", "Freshwater rivers", "Hot springs"], "answer": "Cold ocean water"},
        {"prompt": "Northern shrimp are found in which oceans?", "options": ["Atlantic, Pacific, Arctic", "Indian only", "Southern only", "Mediterranean only"], "answer": "Atlantic, Pacific, Arctic"},
        {"prompt": "Northern shrimp live on what type of seafloor?", "options": ["Rocky cliffs", "Mud or silt", "Coral reefs", "Sand dunes"], "answer": "Mud or silt"},
        {"prompt": "What do Northern shrimp eat?", "options": ["Coral", "Plankton", "Kelp", "Sand"], "answer": "Plankton"},
        {"prompt": "Northern shrimp are:", "options": ["Only predators", "Only prey", "Both predator and prey", "Neither"], "answer": "Both predator and prey"},
        {"prompt": "What animal eats Northern shrimp?", "options": ["Jellyfish", "Cod", "Dolphins", "Crabs"], "answer": "Cod"},
        {"prompt": "Juvenile shrimp are found:", "options": ["Offshore only", "Nearshore before moving offshore", "In rivers", "On land"], "answer": "Nearshore before moving offshore"},
        {"prompt": "Adult shrimp are mostly found:", "options": ["Nearshore", "Deep offshore waters", "In lakes", "At surface"], "answer": "Deep offshore waters"},
        {"prompt": "Female shrimp carry what?", "options": ["Food", "Eggs externally", "Larvae internally", "Nothing"], "answer": "Eggs externally"},
        {"prompt": "Shrimp larvae hatch in:", "options": ["Summer", "Fall", "Spring", "Winter"], "answer": "Spring"},
        {"prompt": "Shrimp reproduction depends on:", "options": ["Wind", "Temperature and seasons", "Light only", "Salinity only"], "answer": "Temperature and seasons"},
        {"prompt": "Shrimp require what type of water?", "options": ["Warm", "Cold and oxygen-rich", "Freshwater", "Hot"], "answer": "Cold and oxygen-rich"},
        {"prompt": "Shrimp are important because they:", "options": ["Build reefs", "Produce oxygen", "Are part of the food web", "Filter water"], "answer": "Are part of the food web"},
        {"prompt": "Shrimp are heavily fished in:", "options": ["Africa", "Canada and Greenland", "Australia", "South America"], "answer": "Canada and Greenland"},
        {"prompt": "Shrimp depend heavily on:", "options": ["Light", "Cold conditions", "Salinity", "Shallow water"], "answer": "Cold conditions"},
        {"prompt": "As shrimp grow, they move:", "options": ["Toward shore", "Offshore", "Stay still", "To rivers"], "answer": "Offshore"},
        {"prompt": "Shrimp eggs are carried until:", "options": ["Fertilization", "Winter ends", "Hatching", "Summer"], "answer": "Hatching"},
        {"prompt": "Spawning occurs:", "options": ["Spring", "Late summer/early fall", "Winter", "Early spring"], "answer": "Late summer/early fall"},
        {"prompt": "Shrimp are part of the:", "options": ["Land ecosystem", "Ocean food web", "Freshwater system", "Desert system"], "answer": "Ocean food web"},
        {"prompt": "Shrimp support the:", "options": ["Tourism only", "Seafood economy", "Agriculture", "Forestry"], "answer": "Seafood economy"},
    ],

    "medium": [
        {"prompt": "Northern shrimp are what type of hermaphrodite?", "options": ["Simultaneous", "Protandric", "Sequential female-first", "Asexual"], "answer": "Protandric"},
        {"prompt": "Protandric hermaphroditism means:", "options": ["Female to male", "Male to female", "Both sexes at once", "No sex"], "answer": "Male to female"},
        {"prompt": "Shrimp change sex at approximately:", "options": ["1 year", "2 years", "3.5 years", "10 years"], "answer": "3.5 years"},
        {"prompt": "Ocean acidification is caused by:", "options": ["Oxygen", "Carbon dioxide", "Salt", "Nitrogen"], "answer": "Carbon dioxide"},
        {"prompt": "Oceans absorb about how much CO₂?", "options": ["10%", "30%", "50%", "80%"], "answer": "30%"},
        {"prompt": "CO₂ forms what in seawater?", "options": ["Oxygen", "Carbonic acid", "Salt", "Nitrogen"], "answer": "Carbonic acid"},
        {"prompt": "Carbonic acid releases:", "options": ["Oxygen", "Hydrogen ions", "Sodium", "Calcium"], "answer": "Hydrogen ions"},
        {"prompt": "More hydrogen ions cause pH to:", "options": ["Increase", "Decrease", "Stay same", "Double"], "answer": "Decrease"},
        {"prompt": "Acidification reduces:", "options": ["Oxygen", "Carbonate ions", "Nitrogen", "Salt"], "answer": "Carbonate ions"},
        {"prompt": "A 0.1 drop in pH causes:", "options": ["No change", "10% increase acidity", "40% increase acidity", "100% increase"], "answer": "40% increase acidity"},
        {"prompt": "Warming causes shrimp metabolism to:", "options": ["Slow", "Stop", "Increase", "Stay same"], "answer": "Increase"},
        {"prompt": "Reproduction timing under warming:", "options": ["Improves", "Disrupts", "Stops", "Doubles"], "answer": "Disrupts"},
        {"prompt": "Shrimp tolerance to warming is:", "options": ["High", "Limited", "Unlimited", "Irrelevant"], "answer": "Limited"},
        {"prompt": "Acidification causes:", "options": ["Better growth", "Stress and protein damage", "Improved survival", "No effect"], "answer": "Stress and protein damage"},
        {"prompt": "Shrimp must use energy for:", "options": ["Growth", "Maintaining internal pH", "Movement only", "Reproduction only"], "answer": "Maintaining internal pH"},
        {"prompt": "Energy tradeoff results in:", "options": ["More growth", "Less growth and protein synthesis", "More reproduction", "No change"], "answer": "Less growth and protein synthesis"},
        {"prompt": "Acidification affects:", "options": ["Only movement", "Proteins and metabolism", "Only color", "Only size"], "answer": "Proteins and metabolism"},
        {"prompt": "Some populations survive better due to:", "options": ["Luck", "Local adaptations", "Speed", "Size"], "answer": "Local adaptations"},
        {"prompt": "Climate change affects shrimp through:", "options": ["Light", "Temperature and pH", "Waves", "Currents"], "answer": "Temperature and pH"},
        {"prompt": "Shrimp populations are vulnerable because of:", "options": ["Too much food", "Cold-water dependence", "Fast growth", "Large size"], "answer": "Cold-water dependence"},
    ],

    "hard": [
        {"prompt": "What directly lowers ocean pH during acidification?", "options": ["Carbonic acid formation", "Hydrogen ion release", "Oxygen loss", "Salt increase"], "answer": "Hydrogen ion release"},
        {"prompt": "Why does CO₂ reduce carbonate availability?", "options": ["Evaporation", "Chemical equilibrium shifts from H+ increase", "Fish consumption", "Oxygen exchange"], "answer": "Chemical equilibrium shifts from H+ increase"},
        {"prompt": "Main cause of biological stress in shrimp?", "options": ["Carbonic acid", "Hydrogen ions", "Temperature", "Salinity"], "answer": "Hydrogen ions"},
        {"prompt": "Why is small pH change significant?", "options": ["Ocean buffering fails", "pH is logarithmic", "CO₂ dissolves quickly", "Shrimp detect pH"], "answer": "pH is logarithmic"},
        {"prompt": "Why do shrimp need more energy under acidification?", "options": ["Feeding", "Maintaining pH balance", "Movement", "Reproduction"], "answer": "Maintaining pH balance"},
        {"prompt": "Main tradeoff of energy use?", "options": ["More reproduction", "Less growth and protein synthesis", "Less movement", "More feeding"], "answer": "Less growth and protein synthesis"},
        {"prompt": "What links acidification to reduced growth?", "options": ["Oxygen demand", "Energy diversion", "Temperature", "Speed"], "answer": "Energy diversion"},
        {"prompt": "Proteostasis disruption causes:", "options": ["Growth increase", "Misfolded proteins", "More oxygen", "Faster metabolism"], "answer": "Misfolded proteins"},
        {"prompt": "Why is protein misfolding harmful?", "options": ["Only digestion affected", "Multiple processes disrupted", "Improves growth", "No effect"], "answer": "Multiple processes disrupted"},
        {"prompt": "Mortality increase is due to:", "options": ["Food shortage", "Cellular stress", "Predators", "Oxygen loss"], "answer": "Cellular stress"},
        {"prompt": "1.6x mortality shows:", "options": ["No effect", "Moderate acidification impacts survival", "Shrimp adapt", "Only juveniles affected"], "answer": "Moderate acidification impacts survival"},
        {"prompt": "Reproduction declines because:", "options": ["More mating", "Sex-change timing disruption", "Egg increase", "Fast growth"], "answer": "Sex-change timing disruption"},
        {"prompt": "Sex change depends on:", "options": ["Age only", "Growth and temperature", "Food only", "Light"], "answer": "Growth and temperature"},
        {"prompt": "Climate change reduces females because:", "options": ["Faster growth", "Timing disruption", "Egg increase", "Long lifespan"], "answer": "Timing disruption"},
        {"prompt": "Population decline occurs due to:", "options": ["Predation", "Reduced survival + reproduction", "Movement", "Growth"], "answer": "Reduced survival + reproduction"},
        {"prompt": "Resilience varies due to:", "options": ["Size", "Local adaptation", "Speed", "Reproduction"], "answer": "Local adaptation"},
        {"prompt": "Food web effect of shrimp decline:", "options": ["Oxygen rise", "Food web disruption", "Plankton loss", "CO₂ drop"], "answer": "Food web disruption"},
        {"prompt": "Warming + acidification together:", "options": ["Help shrimp", "Disrupt physiology + reproduction", "No effect", "Increase growth"], "answer": "Disrupt physiology + reproduction"},
        {"prompt": "Biggest vulnerability factor:", "options": ["Fast growth", "Cold-water dependence", "Large size", "Speed"], "answer": "Cold-water dependence"},
        {"prompt": "Ultimate long-term risk:", "options": ["Population growth", "Population collapse", "No change", "Better adaptation"], "answer": "Population collapse"},
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
