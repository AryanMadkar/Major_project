import re
from .GraphState import GraphState
# =========================
# REGEX EXTRACTOR NODE
# =========================
def extract_bhk(state: GraphState):

    text = state["cleaned_text"]

    # Matches:
    # 1 BHK
    # 2bhk
    # 3-bhk
    # etc

    pattern = r'(\d+)\s*[-]?\s*bhk'

    match = re.search(pattern, text, re.IGNORECASE)

    if match:
        bhk = int(match.group(1))
    else:
        bhk = None

    return {
        "bhk": bhk
    }
