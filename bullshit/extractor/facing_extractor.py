import re
from .GraphState import GraphState


# ==========================================
# DIRECTION MAPPING
# ==========================================

DIRECTION_PATTERNS = {

    "north": [
        "north facing",
        "north side",
        "north"
    ],

    "south": [
        "south facing",
        "south side",
        "south"
    ],

    "east": [
        "east facing",
        "east side",
        "east"
    ],

    "west": [
        "west facing",
        "west side",
        "west"
    ],

    "north_east": [
        "north east",
        "north-east",
        "ne facing",
        "ne"
    ],

    "north_west": [
        "north west",
        "north-west",
        "nw facing",
        "nw"
    ],

    "south_east": [
        "south east",
        "south-east",
        "se facing",
        "se"
    ],

    "south_west": [
        "south west",
        "south-west",
        "sw facing",
        "sw"
    ]
}


# ==========================================
# MAIN EXTRACTOR
# ==========================================

def extract_facing(state: GraphState):

    text = state["cleaned_text"]

    facing = None

    # ======================================
    # DETECT DIRECTIONS
    # ======================================

    for direction, keywords in DIRECTION_PATTERNS.items():

        for word in keywords:

            if re.search(rf"\b{re.escape(word)}\b", text):

                facing = direction

                break

        if facing:
            break

    # ======================================
    # EXTRA SMART DETECTION
    # ======================================

    if facing is None:

        facing_patterns = [

            r"([a-z\s]+)\s*facing",
            r"facing\s*[:\-]?\s*([a-z\s]+)"
        ]

        for pattern in facing_patterns:

            match = re.search(pattern, text)

            if match:

                detected = match.group(1).strip()

                if len(detected) < 20:
                    facing = detected.replace(" ", "_")

                    break

    return {
        "facing": facing
    }