import re
from .GraphState import GraphState


# ==========================================
# DIRECTION PATTERNS
# ==========================================

FACING_PATTERNS = {

    "north": [
        r"\bnorth\s*facing\b",
        r"\bfacing\s*north\b",
        r"\bnorth-facing\b"
    ],

    "south": [
        r"\bsouth\s*facing\b",
        r"\bfacing\s*south\b",
        r"\bsouth-facing\b"
    ],

    "east": [
        r"\beast\s*facing\b",
        r"\bfacing\s*east\b",
        r"\beast-facing\b"
    ],

    "west": [
        r"\bwest\s*facing\b",
        r"\bfacing\s*west\b",
        r"\bwest-facing\b"
    ],

    "north_east": [
        r"\bnorth\s*east\s*facing\b",
        r"\bfacing\s*north\s*east\b",
        r"\bnorth-east\s*facing\b",
        r"\bfacing\s*north-east\b",
        r"\bne\s*facing\b",
        r"\bfacing\s*ne\b"
    ],

    "north_west": [
        r"\bnorth\s*west\s*facing\b",
        r"\bfacing\s*north\s*west\b",
        r"\bnorth-west\s*facing\b",
        r"\bfacing\s*north-west\b",
        r"\bnw\s*facing\b",
        r"\bfacing\s*nw\b"
    ],

    "south_east": [
        r"\bsouth\s*east\s*facing\b",
        r"\bfacing\s*south\s*east\b",
        r"\bsouth-east\s*facing\b",
        r"\bfacing\s*south-east\b",
        r"\bse\s*facing\b",
        r"\bfacing\s*se\b"
    ],

    "south_west": [
        r"\bsouth\s*west\s*facing\b",
        r"\bfacing\s*south\s*west\b",
        r"\bsouth-west\s*facing\b",
        r"\bfacing\s*south-west\b",
        r"\bsw\s*facing\b",
        r"\bfacing\s*sw\b"
    ]
}


# ==========================================
# MAIN EXTRACTOR
# ==========================================

def extract_facing(state: GraphState):

    text = state["cleaned_text"]

    facing = None

    # ======================================
    # DETECT DIRECTIONS ONLY WITH EXPLICIT FACING CONTEXT
    # ======================================

    for direction, patterns in FACING_PATTERNS.items():

        for pattern in patterns:

            if re.search(pattern, text):

                facing = direction

                break

        if facing:
            break

    return {
        "facing": facing
    }