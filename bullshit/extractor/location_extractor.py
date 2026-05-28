import re
from .GraphState import GraphState


# ==========================================
# WESTERN LINE
# ==========================================

WESTERN_LINE = [

    "churchgate",
    "marine lines",
    "charni road",
    "grant road",
    "mumbai central",
    "mahalaxmi",
    "lower parel",
    "prabhadevi",
    "dadar",
    "mahim",
    "bandra",
    "khar road",
    "santacruz",
    "vile parle",
    "andheri",
    "jogeshwari",
    "goregaon",
    "malad",
    "kandivali",
    "borivali",
    "dahisar",
    "mira road",
    "bhayandar",
    "naigaon",
    "vasai",
    "nalasopara",
    "virar"
]

# ==========================================
# CENTRAL LINE
# ==========================================

CENTRAL_LINE = [

    "csmt",
    "byculla",
    "dadar",
    "kurla",
    "ghatkopar",
    "vikhroli",
    "bhandup",
    "mulund",
    "thane",
    "dombivli",
    "kalyan",
    "ambernath",
    "badlapur",
    "karjat",
    "kasara"
]

# ==========================================
# HARBOUR LINE
# ==========================================

HARBOUR_LINE = [

    "wadala",
    "kurla",
    "chembur",
    "govandi",
    "mankhurd",
    "vashi",
    "sanpada",
    "juinagar",
    "nerul",
    "seawoods",
    "belapur",
    "kharghar",
    "panvel"
]


MUMBAI_LOCALITIES = [
    "charkop",
    "poisar",
    "lokhandwala",
    "thakur village",
    "ic colony",
    "kandivali west",
    "kandivali east",
    "borivali west",
    "borivali east",
    "malad west",
    "malad east",
    "andheri west",
    "andheri east",
    "goregaon west",
    "goregaon east",
    "powai",
    "mulund",
    "ghatkopar",
    "chembur",
    "bhandup",
    "dahisar",
    "virar",
]


SECTOR_PATTERNS = [
    r"\bsector\s*\d+[a-z]?\b",
    r"\bsec\s*\d+[a-z]?\b",
]


ROAD_PATTERNS = [
    r"\blink\s+road\b",
    r"\bsv\s+road\b",
    r"\bmg\s+road\b",
    r"\bturner\s+road\b",
    r"\bhill\s+road\b",
]


LANDMARK_PATTERNS = [
    r"\bmetro\s+station\b",
    r"\brailway\s+station\b",
    r"\bbus\s+depot\b",
    r"\bnear\s+[a-z0-9\s]{2,30}\b",
]


SOCIETY_PATTERNS = [
    r"\b[a-z0-9\s]{2,40}\s+society\b",
    r"\b[a-z0-9\s]{2,40}\s+chs\b",
    r"\b[a-z0-9\s]{2,40}\s+tower\b",
]


def _append_spans(items, text, label=None):
    spans = []
    for item in items:
        for match in re.finditer(rf"\b{re.escape(item)}\b", text):
            spans.append({
                "value": item,
                "start": match.start(),
                "label": label,
            })
    return spans


def _append_pattern_spans(patterns, text):
    spans = []
    for pattern in patterns:
        for match in re.finditer(pattern, text):
            spans.append({
                "value": match.group(0).strip(),
                "start": match.start(),
                "label": None,
            })
    return spans


# ==========================================
# LOCATION EXTRACTOR
# ==========================================

def extract_location(state: GraphState):



    text = (state.cleaned_text or "").lower()

    all_spans = []
    all_spans.extend(_append_spans(WESTERN_LINE, text, label="western"))
    all_spans.extend(_append_spans(CENTRAL_LINE, text, label="central"))
    all_spans.extend(_append_spans(HARBOUR_LINE, text, label="harbour"))
    all_spans.extend(_append_spans(MUMBAI_LOCALITIES, text))
    all_spans.extend(_append_pattern_spans(SECTOR_PATTERNS, text))
    all_spans.extend(_append_pattern_spans(ROAD_PATTERNS, text))
    all_spans.extend(_append_pattern_spans(LANDMARK_PATTERNS, text))
    all_spans.extend(_append_pattern_spans(SOCIETY_PATTERNS, text))

    all_spans.sort(key=lambda item: item["start"])

    detected_locations = []
    railway_line = None
    railway_line_span = None
    seen = set()
    primary_span_obj = None

    for span in all_spans:
        value = span["value"]
        if value in seen:
            continue
        seen.add(value)
        detected_locations.append(value)
        if primary_span_obj is None:
            primary_span_obj = span

        if railway_line is None and span.get("label") in {"western", "central", "harbour"}:
            railway_line = span.get("label")
            railway_line_span = span

    primary_location = detected_locations[0] if detected_locations else None

    # ======================================
    # RECORD SPANS
    # ======================================
    extraction_spans = {}
    if primary_location and primary_span_obj:
        start = primary_span_obj["start"]
        end = start + len(primary_location)
        extraction_spans["location.primary_location"] = {
            "value": primary_location,
            "source_span": text[start:end],
            "start": start,
            "end": end,
            "extractor": "location_dictionary"
        }
        extraction_spans["location.locations"] = {
            "value": detected_locations,
            "source_span": text[start:end],
            "start": start,
            "end": end,
            "extractor": "location_dictionary"
        }
    if railway_line and railway_line_span:
        start = railway_line_span["start"]
        end = start + len(railway_line_span["value"])
        extraction_spans["location.railway_line"] = {
            "value": railway_line,
            "source_span": text[start:end],
            "start": start,
            "end": end,
            "extractor": "location_railway_dict"
        }

    # ======================================
    # RETURN
    # ======================================

    return {
        "locations": detected_locations,
        "primary_location": primary_location,
        "railway_line": railway_line,
        "extraction_spans": extraction_spans
    }