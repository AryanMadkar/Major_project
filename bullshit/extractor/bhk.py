import re
from .GraphState import GraphState

# Compile regex once at startup
BHK_PATTERN = re.compile(
    r'\b(\d{1,2})\s*-?\s*bhk\b',
    re.IGNORECASE
)
# =========================
# REGEX EXTRACTOR NODE
# =========================
def extract_bhk(state: GraphState):

    text = state.get("cleaned_text", "")

    # Matches:
    # 1 BHK
    # 2bhk
    # 3-bhk
    # etc

    match = BHK_PATTERN.search(text)

    if match:
        bhk = int(match.group(1))
    else:
        bhk = None

    return {
        "bhk": bhk
    }
