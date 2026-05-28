import re

from .GraphState import GraphState


FACING_PATTERN = re.compile(
    r"""
    \b(
        north(?:\s|-)?east |
        north(?:\s|-)?west |
        south(?:\s|-)?east |
        south(?:\s|-)?west |
        north |
        south |
        east |
        west |
        ne |
        nw |
        se |
        sw
    )\s*facing
    |
    facing\s*(
        north(?:\s|-)?east |
        north(?:\s|-)?west |
        south(?:\s|-)?east |
        south(?:\s|-)?west |
        north |
        south |
        east |
        west |
        ne |
        nw |
        se |
        sw
    )
    \b
    """,
    re.IGNORECASE | re.VERBOSE
)


DIRECTION_MAP = {
    "north": "north",
    "south": "south",
    "east": "east",
    "west": "west",
    "north east": "north_east",
    "north-east": "north_east",
    "ne": "north_east",
    "north west": "north_west",
    "north-west": "north_west",
    "nw": "north_west",
    "south east": "south_east",
    "south-east": "south_east",
    "se": "south_east",
    "south west": "south_west",
    "south-west": "south_west",
    "sw": "south_west",
}


def extract_facing(state: GraphState):

    text = state.get("cleaned_text", "")

    if not text:
        return {"facing": None}

    match = FACING_PATTERN.search(text)

    if not match:
        return {"facing": None}

    direction = next(group for group in match.groups() if group)

    direction = direction.lower()

    return {
        "facing": DIRECTION_MAP.get(direction)
    }