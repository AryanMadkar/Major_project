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
    "ready to move furnished",
    "all amenities"
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

    text = state["cleaned_text"]

    furnishing = None

    # ======================================
    # FULLY FURNISHED
    # ======================================

    for word in FULLY_FURNISHED:

        if re.search(rf"\b{re.escape(word)}\b", text):

            furnishing = "fully_furnished"

            break

    # ======================================
    # SEMI FURNISHED
    # ======================================

    if furnishing is None:

        for word in SEMI_FURNISHED:

            if re.search(rf"\b{re.escape(word)}\b", text):

                furnishing = "semi_furnished"

                break

    # ======================================
    # UNFURNISHED
    # ======================================

    if furnishing is None:

        for word in UNFURNISHED:

            if re.search(rf"\b{re.escape(word)}\b", text):

                furnishing = "unfurnished"

                break

    # ======================================
    # SMART FALLBACK
    # ======================================

    if furnishing is None:

        if re.search(
            r"\bac\b|\bsofa\b|\bbed\b|\bfridge\b|\bwashing machine\b",
            text
        ):

            furnishing = "semi_furnished"

    return {
        "furnishing": furnishing
    }