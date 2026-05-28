import re
from .GraphState import GraphState


# =========================================================
# PRECOMPILED REGEX
# =========================================================

PARKING_COUNT_PATTERN = re.compile(
    r"""
    (?:
        (\d+)\s*
        (?:
            car\s*parking|
            covered\s*parking|
            open\s*parking|
            parking
        )
    )
    |
    (?:
        parking\s*for\s*(\d+)
    )
    """,
    re.IGNORECASE | re.VERBOSE
)


PARKING_TYPE_PATTERNS = {

    "covered": re.compile(r"\bcovered parking\b", re.IGNORECASE),

    "open": re.compile(r"\bopen parking\b", re.IGNORECASE),

    "stilt": re.compile(r"\bstilt parking\b", re.IGNORECASE),

    "car": re.compile(r"\bcar parking\b", re.IGNORECASE),
}


GENERIC_PARKING_PATTERN = re.compile(
    r"\bparking\b",
    re.IGNORECASE
)


# =========================================================
# MAIN EXTRACTOR
# =========================================================

def extract_parking(state: GraphState):



    text = state.cleaned_text or ""

    if not text:
        return {
            "parking_count": None,
            "parking_type": None,
        }

    parking_count = None
    parking_type = None
    extraction_spans = {}

    # =====================================================
    # COUNT EXTRACTION
    # =====================================================

    match = PARKING_COUNT_PATTERN.search(text)

    if match:
        count = match.group(1) or match.group(2)
        try:
            parking_count = int(count)
            extraction_spans["parking.parking_count"] = {
                "value": parking_count,
                "source_span": match.group(0),
                "start": match.start(),
                "end": match.end(),
                "extractor": "parking_count_regex"
            }
        except Exception:
            parking_count = None

    # =====================================================
    # TYPE EXTRACTION
    # =====================================================

    for p_type, pattern in PARKING_TYPE_PATTERNS.items():
        type_match = pattern.search(text)
        if type_match:
            parking_type = p_type
            extraction_spans["parking.parking_type"] = {
                "value": parking_type,
                "source_span": type_match.group(0),
                "start": type_match.start(),
                "end": type_match.end(),
                "extractor": "parking_type_regex"
            }
            break

    # =====================================================
    # FALLBACK
    # =====================================================

    if parking_count is None:
        fallback_match = GENERIC_PARKING_PATTERN.search(text)
        if fallback_match:
            parking_count = 1
            extraction_spans["parking.parking_count"] = {
                "value": parking_count,
                "source_span": fallback_match.group(0),
                "start": fallback_match.start(),
                "end": fallback_match.end(),
                "extractor": "parking_generic_fallback"
            }

    return {
        "parking_count": parking_count,
        "parking_type": parking_type,
        "extraction_spans": extraction_spans
    }