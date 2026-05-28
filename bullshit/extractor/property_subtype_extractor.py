import re
from .GraphState import GraphState


# ==========================================
# PROPERTY SUBTYPE MAP
# ==========================================

PROPERTY_SUBTYPE_MAP = {

    # ======================================
    # RESIDENTIAL
    # ======================================

    "apartment": [

        "apartment",
        "flat",
        "flat available",
        "residential flat"
    ],

    "studio_apartment": [

        "studio",
        "studio apartment",
        "studio flat"
    ],

    "penthouse": [

        "penthouse",
        "pent house",
        "pent hs"
    ],

    "villa": [

        "villa",
        "luxury villa"
    ],

    "bungalow": [

        "bungalow",
        "bunglow",
        "independent bungalow"
    ],

    "row_house": [

        "row house",
        "rowhouse"
    ],

    "duplex": [

        "duplex",
        "duplex flat"
    ],

    "farmhouse": [

        "farmhouse",
        "farm house"
    ],

    "chawl": [

        "chawl"
    ],

    "pg": [

        "pg",
        "paying guest"
    ],

    # ======================================
    # COMMERCIAL
    # ======================================

    "office": [

        "office",
        "office space",
        "commercial office",
        "workspace",
        "corporate office"
    ],

    "coworking": [

        "coworking",
        "co working",
        "shared office"
    ],

    "shop": [

        "shop",
        "retail shop"
    ],

    "showroom": [

        "showroom",
        "show room"
    ],

    "commercial_space": [

        "commercial",
        "commercial space",
        "commercial property"
    ],

    "warehouse": [

        "warehouse",
        "godown",
        "storage"
    ],

    "industrial_shed": [

        "industrial shed",
        "factory shed",
        "shed"
    ],

    "gala": [

        "gala",
        "commercial gala"
    ],

    # ======================================
    # LAND
    # ======================================

    "plot": [

        "plot",
        "residential plot",
        "na plot"
    ],

    "land": [

        "land",
        "open land"
    ]
}


# ==========================================
# PRIORITY ORDER
# ==========================================

PRIORITY = [

    "penthouse",
    "villa",
    "bungalow",
    "studio_apartment",
    "duplex",
    "office",
    "coworking",
    "showroom",
    "shop",
    "warehouse",
    "industrial_shed",
    "gala",
    "plot",
    "land",
    "pg",
    "apartment"
]


# ==========================================
# MAIN EXTRACTOR
# ==========================================

def extract_property_subtype(state: GraphState):



    text = state.cleaned_text or ""

    detected = []

    # ======================================
    # DETECT ALL MATCHES
    # ======================================

    for subtype, keywords in PROPERTY_SUBTYPE_MAP.items():

        for keyword in keywords:

            if re.search(

                rf"\b{re.escape(keyword)}\b",

                text
            ):

                detected.append(subtype)

                break

    # ======================================
    # REMOVE DUPLICATES
    # ======================================

    detected = list(set(detected))

    # ======================================
    # PRIORITY SELECTION
    # ======================================

    final_subtype = None

    for item in PRIORITY:

        if item in detected:

            final_subtype = item

            break

    # ======================================
    # SMART FALLBACKS
    # ======================================

    if final_subtype is None:
        # BHK usually apartment
        if re.search(r"\bbhk\b", text):
            final_subtype = "apartment"

    # ======================================
    # RECORD SPANS
    # ======================================
    extraction_spans = {}
    if final_subtype:
        matched_word = None
        start = -1
        end = -1
        for keyword in PROPERTY_SUBTYPE_MAP.get(final_subtype, []):
            m = re.search(rf"\b{re.escape(keyword)}\b", text)
            if m:
                matched_word = m.group(0)
                start = m.start()
                end = m.end()
                break
        if not matched_word and final_subtype == "apartment" and "bhk" in text:
            m = re.search(r"\bbhk\b", text)
            if m:
                matched_word = m.group(0)
                start = m.start()
                end = m.end()
        if matched_word:
            extraction_spans["property.property_subtype"] = {
                "value": final_subtype,
                "source_span": matched_word,
                "start": start,
                "end": end,
                "extractor": "property_subtype_keyword"
            }
            extraction_spans["property.all_detected_subtypes"] = {
                "value": detected,
                "source_span": matched_word,
                "start": start,
                "end": end,
                "extractor": "property_subtype_keyword"
            }

    return {
        "property_subtype": final_subtype,
        "all_detected_subtypes": detected,
        "extraction_spans": extraction_spans
    }