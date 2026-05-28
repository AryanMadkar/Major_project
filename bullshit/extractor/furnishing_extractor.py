import re
from .GraphState import GraphState


# ==========================================
# FURNISHING KEYWORDS
# ==========================================

FULLY_FURNISHED = [

    "fully furnished",
    "full furnished",
    "fully loaded",
    "complete furnished",
    "luxury furnished",
    "furnished flat",
    "furnished apartment",
    "fully setup",
    "ready to move furnished"
]

SEMI_FURNISHED = [

    "semi furnished",
    "semi-furnished",
    "semi setup",
    "modular kitchen",
    "with wardrobe",
    "wardrobe",
    "geyser",
    "ac fitted",
    "basic furnishing",
    "partially furnished"
]

UNFURNISHED = [

    "unfurnished",
    "empty flat",
    "bare flat",
    "without furniture",
    "raw flat",
    "vacant flat"
]


# ==========================================
# MAIN EXTRACTOR
# ==========================================

def extract_furnishing(state: GraphState):

    text = (state.cleaned_text or "").lower()

    scores = {
        "fully_furnished": 0,
        "semi_furnished": 0,
        "unfurnished": 0
    }

    for word in FULLY_FURNISHED:
        if re.search(rf"\b{re.escape(word)}\b", text):
            scores["fully_furnished"] += 5

    for word in SEMI_FURNISHED:
        if re.search(rf"\b{re.escape(word)}\b", text):
            scores["semi_furnished"] += 3

    for word in UNFURNISHED:
        if re.search(rf"\b{re.escape(word)}\b", text):
            scores["unfurnished"] += 4

    if re.search(r"\bac\b|\bsofa\b|\bbed\b|\bfridge\b|\bwashing machine\b", text):
        scores["semi_furnished"] += 2

    furnishing = max(scores, key=scores.get)
    if scores[furnishing] <= 0:
        furnishing = None

    return {
        "furnishing": furnishing
    }