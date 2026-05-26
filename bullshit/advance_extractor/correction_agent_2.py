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
    temperature=0.2
)

# ==========================================
# PROMPT
# ==========================================

CORRECTION_PROMPT = """
You are an elite semantic real-estate extraction repair AI.

Your ONLY responsibility:
Repair semantic and interpretation-based fields.

You are STRICTLY ALLOWED to modify ONLY:

- amenities
- furnishing
- facing
- metadata
- contact details
- message title

You MUST NOT modify:
- bhk
- pricing
- request type
- locations
- parking
- property subtype

You will receive:
1. Original message
2. Current extracted JSON
3. Validation report

Your job:
- repair semantic extraction mistakes
- repair hallucinated amenities
- repair furnishing mistakes
- repair facing direction mistakes
- repair metadata extraction
- repair contact extraction
- repair title generation
- improve semantic normalization

VERY IMPORTANT RULES:
- Never hallucinate unsupported amenities.
- Never invent contact details.
- Only extract explicit information.
- Preserve already-correct fields.
- Modify ONLY incorrect fields.
- Be conservative.
- Never remove valid information.

Return ONLY VALID JSON.

OUTPUT FORMAT:

{{
    "attributes": {{}},
    "amenities": [],
    "metadata": {{}}
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

    except Exception:
        pass

    return None


# ==========================================
# FILTER REPAIRS
# ==========================================

def filter_allowed_repairs(repaired_output):

    safe_output = {

        "attributes": {},

        "amenities": [],

        "metadata": {}
    }

    # ======================================
    # ATTRIBUTES
    # ======================================

    attributes = repaired_output.get(
        "attributes",
        {}
    )

    for key in [

        "furnishing",
        "facing"
    ]:

        if key in attributes:

            safe_output["attributes"][key] = (
                attributes[key]
            )

    # ======================================
    # AMENITIES
    # ======================================

    amenities = repaired_output.get(
        "amenities",
        []
    )

    if isinstance(amenities, list):

        cleaned = []

        for item in amenities:

            item = str(item).strip().lower()

            if not item:
                continue

            if item not in cleaned:

                cleaned.append(item)

        safe_output["amenities"] = cleaned

    # ======================================
    # METADATA
    # ======================================

    metadata = repaired_output.get(
        "metadata",
        {}
    )

    allowed_metadata = [

        "message_title",

        "contact_people",

        "contact_numbers",

        "metadata_summary"
    ]

    for key in allowed_metadata:

        if key in metadata:

            safe_output["metadata"][key] = (
                metadata[key]
            )

    return safe_output


# ==========================================
# MERGE OUTPUTS
# ==========================================

def merge_outputs(original, repaired):

    merged = copy.deepcopy(original)

    # ======================================
    # ATTRIBUTES
    # ======================================

    if "attributes" in repaired:

        if "attributes" not in merged:

            merged["attributes"] = {}

        for key, value in repaired[
            "attributes"
        ].items():

            merged["attributes"][key] = value

    # ======================================
    # AMENITIES
    # ======================================

    if "amenities" in repaired:

        merged["amenities"] = repaired[
            "amenities"
        ]

    # ======================================
    # METADATA
    # ======================================

    if "metadata" in repaired:

        if "metadata" not in merged:

            merged["metadata"] = {}

        for key, value in repaired[
            "metadata"
        ].items():

            merged["metadata"][key] = value

    return merged


# ==========================================
# MAIN NODE
# ==========================================

def correction_agent_2(state: GraphState):

    original_message = state.get(
        "user_input",
        ""
    )

    current_output = state.get(
        "response_output",
        {}
    )

    validation_report = state.get(
        "validation_report",
        {}
    )

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

        repaired_json = safe_parse_json(
            raw_content
        )

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

        print(
            "Correction Agent 2 Error:",
            e
        )

        return {}