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



    text = state.cleaned_text or ""

    # Matches:
    # 1 BHK
    # 2bhk
    # 3-bhk
    # etc

    match = BHK_PATTERN.search(text)

    extraction_spans = dict(state.extraction_spans or {})
    if match:
        bhk = int(match.group(1))
        extraction_spans["summary.bhk"] = {
            "value": bhk,
            "source_span": match.group(0),
            "start": match.start(),
            "end": match.end(),
            "extractor": "bhk_regex"
        }
    else:
        bhk = None

    return {
        "bhk": bhk,
        "extraction_spans": {
            "summary.bhk": {
                "value": bhk,
                "source_span": match.group(0),
                "start": match.start(),
                "end": match.end(),
                "extractor": "bhk_regex"
            }
        } if match else {}
    }
