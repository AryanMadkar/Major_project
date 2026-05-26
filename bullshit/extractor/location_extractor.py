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


# ==========================================
# LOCATION EXTRACTOR
# ==========================================

def extract_location(state: GraphState):

    text = state["cleaned_text"]

    detected_locations = []

    railway_line = None

    # ======================================
    # WESTERN
    # ======================================

    for station in WESTERN_LINE:

        if re.search(rf"\b{re.escape(station)}\b", text):

            detected_locations.append(station)

            railway_line = "western"

    # ======================================
    # CENTRAL
    # ======================================

    for station in CENTRAL_LINE:

        if re.search(rf"\b{re.escape(station)}\b", text):

            detected_locations.append(station)

            railway_line = "central"

    # ======================================
    # HARBOUR
    # ======================================

    for station in HARBOUR_LINE:

        if re.search(rf"\b{re.escape(station)}\b", text):

            detected_locations.append(station)

            railway_line = "harbour"

    # ======================================
    # REMOVE DUPLICATES
    # ======================================

    detected_locations = list(set(detected_locations))

    # ======================================
    # PRIMARY LOCATION
    # ======================================

    primary_location = None

    if detected_locations:

        primary_location = detected_locations[0]

    # ======================================
    # RETURN
    # ======================================

    return {

        "locations": detected_locations,

        "primary_location": primary_location,

        "railway_line": railway_line
    }