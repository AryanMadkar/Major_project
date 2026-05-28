import json
import copy
from typing import Any, Dict
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from extractor.GraphState import GraphState

load_dotenv()

repair_llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.0
)

CORRECTION_PROMPT = """
You are an expert real-estate extraction repair assistant.
Your task is to correct ONLY the following fields that failed validation:
{failed_fields_list}

Rules:
- Use ONLY information explicitly supported by the original message.
- If a field cannot be corrected using explicit information, set it to null or empty list/value.
- Do NOT modify any other fields.
- Return ONLY valid JSON containing the corrected fields.

Original Message:
{original_message}

Current Incorrect Extraction Values:
{current_values}

Example Output Format:
{{
    "failed_field_name_1": "corrected_value_1",
    "failed_field_name_2": null
}}
"""

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


def get_field_val(field_name: str, state: GraphState):
    mapping = {
        "summary.request_type": state.request_type,
        "summary.bhk": state.bhk,
        "pricing.price": state.price,
        "pricing.price_min": state.price_min,
        "pricing.price_max": state.price_max,
        "pricing.rent_price": state.rent_price,
        "pricing.deposit_price": state.deposit_price,
        "location.primary_location": state.primary_location,
        "location.locations": state.locations,
        "location.railway_line": state.railway_line,
        "attributes.furnishing": state.furnishing,
        "attributes.facing": state.facing,
        "parking.parking_count": state.parking_count,
        "parking.parking_type": state.parking_type,
        "amenities": state.amenities,
        "property.property_subtype": state.property_subtype,
        "property.all_detected_subtypes": state.all_detected_subtypes,
        "metadata.message_title": state.message_title,
        "metadata.contact_people": state.contact_people,
        "metadata.contact_numbers": state.contact_numbers,
    }
    return mapping.get(field_name)


def update_field_in_state_and_output(field_name: str, new_val: Any, state: GraphState, response_output: dict, repair_history: list):
    old_val = get_field_val(field_name, state)
    
    if field_name == "summary.request_type":
        state.request_type = new_val
        response_output["summary"]["request_type"] = new_val
    elif field_name == "summary.bhk":
        state.bhk = new_val
        response_output["summary"]["bhk"] = new_val
    elif field_name == "pricing.price":
        state.price = new_val
        response_output["pricing"]["price"] = new_val
    elif field_name == "pricing.price_min":
        state.price_min = new_val
        response_output["pricing"]["price_min"] = new_val
    elif field_name == "pricing.price_max":
        state.price_max = new_val
        response_output["pricing"]["price_max"] = new_val
    elif field_name == "pricing.rent_price":
        state.rent_price = new_val
        response_output["pricing"]["rent_price"] = new_val
    elif field_name == "pricing.deposit_price":
        state.deposit_price = new_val
        response_output["pricing"]["deposit_price"] = new_val
    elif field_name == "location.primary_location":
        state.primary_location = new_val
        response_output["location"]["primary_location"] = new_val
    elif field_name == "location.locations":
        state.locations = new_val
        response_output["location"]["locations"] = new_val
    elif field_name == "location.railway_line":
        state.railway_line = new_val
        response_output["location"]["railway_line"] = new_val
    elif field_name == "attributes.furnishing":
        state.furnishing = new_val
        response_output["attributes"]["furnishing"] = new_val
    elif field_name == "attributes.facing":
        state.facing = new_val
        response_output["attributes"]["facing"] = new_val
    elif field_name == "parking.parking_count":
        state.parking_count = new_val
        response_output["parking"]["parking_count"] = new_val
    elif field_name == "parking.parking_type":
        state.parking_type = new_val
        response_output["parking"]["parking_type"] = new_val
    elif field_name == "amenities":
        state.amenities = new_val
        response_output["amenities"] = new_val
    elif field_name == "property.property_subtype":
        state.property_subtype = new_val
        response_output["property"]["property_subtype"] = new_val
    elif field_name == "property.all_detected_subtypes":
        state.all_detected_subtypes = new_val
        response_output["property"]["all_detected_subtypes"] = new_val
    elif field_name == "metadata.message_title":
        state.message_title = new_val
        response_output["metadata"]["message_title"] = new_val
    elif field_name == "metadata.contact_people":
        state.contact_people = new_val
        response_output["metadata"]["contact_people"] = new_val
    elif field_name == "metadata.contact_numbers":
        state.contact_numbers = new_val
        response_output["metadata"]["contact_numbers"] = new_val

    if old_val != new_val:
        repair_history.append({
            "field": field_name,
            "old_value": old_val,
            "new_value": new_val,
            "reason": "Corrected by Targeted Semantic LLM Repair Agent"
        })


def correction_agent_2(state: GraphState):
    """
    Targeted Semantic Repair Agent. Calls LLM only for failed semantic fields.
    If no semantic fields failed, immediately bypasses the LLM call.
    """


    original_message = state.user_input or ""
    validation_report = state.validation_report or {}
    field_analysis = validation_report.get("field_analysis", {})
    repair_history = list(state.repair_history or [])
    response_output = copy.deepcopy(state.response_output or {})

    # Identify failed semantic fields
    semantic_fields = {
        "location.primary_location", "location.locations", "location.railway_line",
        "attributes.furnishing", "attributes.facing", "amenities",
        "property.property_subtype", "property.all_detected_subtypes",
        "metadata.message_title", "metadata.contact_people", "metadata.contact_numbers"
    }

    failed_semantic_fields = []
    current_values = {}

    for field, report in field_analysis.items():
        if field in semantic_fields and not report.get("valid", True):
            failed_semantic_fields.append(field)
            current_values[field] = get_field_val(field, state)

    if not failed_semantic_fields:
        return {}

    # 2. RUN TARGETED LLM REPAIR
    try:
        prompt = CORRECTION_PROMPT.format(
            failed_fields_list=json.dumps(failed_semantic_fields, indent=2),
            original_message=original_message,
            current_values=json.dumps(current_values, indent=2, ensure_ascii=False)
        )

        response = repair_llm.invoke(prompt)
        raw_content = response.content if hasattr(response, "content") else str(response)
        repaired_json = safe_parse_json(raw_content)

        if repaired_json:
            for field, new_val in repaired_json.items():
                if field in failed_semantic_fields:
                    update_field_in_state_and_output(field, new_val, state, response_output, repair_history)

    except Exception as e:
        print("Correction Agent 2 Targeted LLM Error:", e)

    return {
        "primary_location": state.primary_location,
        "locations": state.locations,
        "railway_line": state.railway_line,
        "furnishing": state.furnishing,
        "facing": state.facing,
        "amenities": state.amenities,
        "property_subtype": state.property_subtype,
        "all_detected_subtypes": state.all_detected_subtypes,
        "message_title": state.message_title,
        "contact_people": state.contact_people,
        "contact_numbers": state.contact_numbers,
        "repair_history": repair_history,
        "response_output": response_output,
    }