import re
from .GraphState import GraphState


# ==========================================
# MAIN EXTRACTOR
# ==========================================

def extract_parking(state: GraphState):

    text = state.cleaned_text or ""

    if not text:
        return {"parking_count": None, "parking_type": None}

    parking_count = None

    parking_type = None

    # ======================================
    # NUMBER + PARKING
    # ======================================

    patterns = [

        r"(\d+)\s*car parking",

        r"(\d+)\s*parking",

        r"(\d+)\s*covered parking",

        r"(\d+)\s*open parking",

        r"parking for (\d+)"
    ]

    for pattern in patterns:

        match = re.search(pattern, text)

        if match:

            parking_count = int(match.group(1))

            break

    # ======================================
    # COVERED
    # ======================================

    if re.search(r"covered parking", text):

        parking_type = "covered"

    elif re.search(r"open parking", text):

        parking_type = "open"

    elif re.search(r"stilt parking", text):

        parking_type = "stilt"

    elif re.search(r"car parking", text):

        parking_type = "car"

    # ======================================
    # FALLBACK
    # ======================================

    if parking_count is None:

        if re.search(r"\bparking\b", text):

            parking_count = 1

    return {

        "parking_count": parking_count,

        "parking_type": parking_type
    }