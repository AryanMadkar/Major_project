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
        for m in re.finditer(rf"\b{re.escape(word)}\b", text):
            start_pos = m.start()
            prefix = text[max(0, start_pos - 10):start_pos]
            if "semi" in prefix or "un" in prefix or "not" in prefix:
                continue
            scores["fully_furnished"] += 5
            break

    for word in SEMI_FURNISHED:
        if re.search(rf"\b{re.escape(word)}\b", text):
            scores["semi_furnished"] += 3

    for word in UNFURNISHED:
        if re.search(rf"\b{re.escape(word)}\b", text):
            scores["unfurnished"] += 4

    if re.search(r"\bac\b|\bsofa\b|\bbed\b|\bfridge\b|\bwashing machine\b", text):
        scores["semi_furnished"] += 2

    furnishing = max(scores, key=scores.get)
    matched_word = None
    start = -1
    end = -1

    if scores[furnishing] <= 0:
        furnishing = None
    else:
        # Trace span of match
        if furnishing == "fully_furnished":
            kws = FULLY_FURNISHED
        elif furnishing == "semi_furnished":
            kws = SEMI_FURNISHED + ["ac", "sofa", "bed", "fridge", "washing machine"]
        else:
            kws = UNFURNISHED
            
        for word in kws:
            m = re.search(rf"\b{re.escape(word)}\b", text)
            if m:
                matched_word = m.group(0)
                start = m.start()
                end = m.end()
                break

    return {
        "furnishing": furnishing,
        "extraction_spans": {
            "attributes.furnishing": {
                "value": furnishing,
                "source_span": matched_word,
                "start": start,
                "end": end,
                "extractor": "furnishing_keyword_scorer"
            }
        } if matched_word else {}
    }