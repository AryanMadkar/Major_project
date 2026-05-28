import json
import copy

from dotenv import load_dotenv

from langchain_groq import ChatGroq

from extractor.GraphState import GraphState

load_dotenv()

# ==========================================
# REPAIR MODEL
# ==========================================

repair_llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.1
)

# ==========================================
# ALLOWED FIELDS
# ==========================================

ALLOWED_FIELDS = [

    "request_type",

    "bhk",

    "price",

    "price_min",

    "price_max",

    "rent_price",

    "deposit_price",

    "primary_location",

    "locations",

    "railway_line",

    "parking_count",

    "parking_type",

    "property_subtype",

    "all_detected_subtypes"
]

# ==========================================
# PROMPT
# ==========================================

CORRECTION_PROMPT = """
You are an elite structured real-estate extraction repair AI.

Your ONLY responsibility:
Repair structured factual extraction fields.

You are STRICTLY ALLOWED to modify ONLY:

- request_type
- bhk
- pricing fields
- location fields
- parking fields
- property subtype fields

You MUST NOT modify:
- amenities
- furnishing
- metadata
- contact details
- titles

You will receive:
1. Original message
2. Current extracted JSON
3. Validation report

Your job:
- repair hallucinated fields
- repair wrong values
- repair missed structured fields
- repair incorrect classifications
- fix contradictory fields

VERY IMPORTANT RULES:
- Do NOT hallucinate.
- Only use information explicitly supported by the message.
- Preserve valid existing fields.
- Modify ONLY incorrect fields.
- Be conservative.
- Never remove correct data.

Return ONLY VALID JSON.

OUTPUT FORMAT:

{{
    "summary": {{}},
    "pricing": {{}},
    "location": {{}},
    "parking": {{}},
    "property": {{}}
}}

ORIGINAL MESSAGE:
{original_message}

CURRENT EXTRACTION:
{current_output}

VALIDATION REPORT:
{validation_report}
"""

# ==========================================
# SAFE JSON PARSER
# ==========================================

def safe_parse_json(content):

    try:

        content = content.strip()

        content = content.replace("```json", "")
        content = content.replace("```", "")

        parsed = json.loads(content)

        if isinstance(parsed, dict):

            return parsed

    except (json.JSONDecodeError, TypeError, AttributeError):
        pass

    return None


# ==========================================
# FILTER REPAIRS
# ==========================================

def filter_allowed_repairs(repaired_output):

    safe_output = {

        "summary": {},
        "pricing": {},
        "location": {},
        "parking": {},
        "property": {}
    }

    # ======================================
    # SUMMARY
    # ======================================

    summary = repaired_output.get("summary", {})

    for key in ["request_type", "bhk"]:

        if key in summary:

            safe_output["summary"][key] = summary[key]

    # ======================================
    # PRICING
    # ======================================

    pricing = repaired_output.get("pricing", {})

    allowed_pricing = [

        "price",
        "price_min",
        "price_max",
        "rent_price",
        "deposit_price",
    ]

    for key in allowed_pricing:

        if key in pricing:

            safe_output["pricing"][key] = pricing[key]

    # ======================================
    # LOCATION
    # ======================================

    location = repaired_output.get("location", {})

    for key in [

        "primary_location",
        "locations",
        "railway_line"
    ]:

        if key in location:

            safe_output["location"][key] = location[key]

    # ======================================
    # PARKING
    # ======================================

    parking = repaired_output.get("parking", {})

    for key in [

        "parking_count",
        "parking_type"
    ]:

        if key in parking:

            safe_output["parking"][key] = parking[key]

    # ======================================
    # PROPERTY
    # ======================================

    property_data = repaired_output.get("property", {})

    for key in [

        "property_subtype",
        "all_detected_subtypes"
    ]:

        if key in property_data:

            safe_output["property"][key] = property_data[key]

    return safe_output


# ==========================================
# MERGE OUTPUTS
# ==========================================

def merge_outputs(original, repaired):

    merged = copy.deepcopy(original)

    for section, values in repaired.items():

        if section not in merged:

            merged[section] = {}

        for key, value in values.items():

            merged[section][key] = value

    return merged


# ==========================================
# MAIN NODE
# ==========================================

def correction_agent_1(state: GraphState):

    original_message = state.user_input or ""

    current_output = state.response_output or {}

    validation_report = state.validation_report or {}

    # ======================================
    # BUILD PROMPT
    # ======================================

    prompt = CORRECTION_PROMPT.format(

        original_message=original_message,

        current_output=json.dumps(
            current_output,
            indent=2,
            ensure_ascii=False
        ),

        validation_report=json.dumps(
            validation_report,
            indent=2,
            ensure_ascii=False
        )
    )

    # ======================================
    # LLM REPAIR
    # ======================================

    try:

        response = repair_llm.invoke(prompt)

        raw_content = (
            response.content
            if hasattr(response, "content")
            else str(response)
        )

        repaired_json = safe_parse_json(raw_content)

        if repaired_json is None:

            return {}

        # ==================================
        # SECURITY FILTER
        # ==================================

        repaired_json = filter_allowed_repairs(
            repaired_json
        )

        # ==================================
        # MERGE
        # ==================================

        merged_output = merge_outputs(
            current_output,
            repaired_json
        )

        return {

            "response_output": merged_output
        }

    except Exception as e:

        print("Correction Agent 1 Error:", e)

        return {}