import re
from typing import Any, Dict, Tuple, List
from concurrent.futures import ThreadPoolExecutor
from extractor.GraphState import GraphState
from advance_extractor.normalization import run_normalization_pipeline
from advance_extractor.rules import run_rule_engine, get_rule_failed_fields


def check_source_support(field_name: str, value: Any, text: str, spans: dict) -> bool:
    """Checks whether the extracted value is supported by the source text, using span info if available."""
    if value in (None, [], {}):
        return True
        
    # If we have span info, check if it matches the source text at that offset
    if spans and field_name in spans:
        span_info = spans[field_name]
        start = span_info.get("start")
        end = span_info.get("end")
        source_span = span_info.get("source_span")
        if start is not None and end is not None and source_span:
            # Check range safety
            if start >= 0 and end <= len(text):
                if text[start:end].lower() == source_span.lower():
                    return True
                
    # Fallback to normalized substring checking
    if isinstance(value, list):
        return all(check_source_support(field_name, item, text, spans) for item in value)
    
    val_str = str(value).lower()
    norm_text = re.sub(r"[^a-z0-9\s]", " ", text.lower())
    norm_text = re.sub(r"\s+", " ", norm_text).strip()
    
    norm_val = re.sub(r"[^a-z0-9\s]", " ", val_str)
    norm_val = re.sub(r"\s+", " ", norm_val).strip()
    
    return norm_val in norm_text


def validate_field(field_name: str, value: Any, text: str, spans: dict, default_extractor: str) -> Tuple[str, Dict[str, Any]]:
    """Validates a single field and calculates its real confidence score."""
    is_supported = check_source_support(field_name, value, text, spans)
    
    # Extract actual extractor name if tracked in spans
    extractor_name = default_extractor
    if spans and field_name in spans:
        extractor_name = spans[field_name].get("extractor", default_extractor)

    # Base confidence based on extractor type
    base_confidence = 50
    if extractor_name:
        if "regex" in extractor_name or "dict" in extractor_name:
            base_confidence = 95
        elif "llm" in extractor_name:
            base_confidence = 75
        elif "fallback" in extractor_name:
            base_confidence = 60
            
    if not is_supported and value not in (None, [], {}):
        confidence = 20
        status = "hallucinated_or_unsupported"
        valid = False
        reason = "Extracted value is not supported by the source text."
    else:
        confidence = base_confidence if value not in (None, [], {}) else 0
        status = "correct" if value not in (None, [], {}) else "missing"
        valid = True
        reason = "Value is supported by the source text."
        
    return field_name, {
        "valid": valid,
        "confidence": confidence,
        "status": status,
        "reason": reason
    }


# ==========================================
# MAIN AUDIT NODE
# ==========================================

def audit_verification_agent(state: GraphState):


    # 1. RUN CANONICAL NORMALIZATION LAYER
    state = run_normalization_pipeline(state)

    source_text = state.user_input or state.cleaned_text or ""
    spans = state.extraction_spans or {}

    # Define fields to validate and their default extractors
    fields_to_validate = [
        ("summary.request_type", state.request_type, "type_keyword_regex"),
        ("summary.bhk", state.bhk, "bhk_regex"),
        ("pricing.price", state.price, "price_regex"),
        ("pricing.price_min", state.price_min, "price_range_regex"),
        ("pricing.price_max", state.price_max, "price_range_regex"),
        ("pricing.rent_price", state.rent_price, "price_rent_keyword_regex"),
        ("pricing.deposit_price", state.deposit_price, "price_deposit_keyword_regex"),
        ("location.primary_location", state.primary_location, "location_dictionary"),
        ("location.locations", state.locations, "location_dictionary"),
        ("location.railway_line", state.railway_line, "location_railway_dict"),
        ("attributes.furnishing", state.furnishing, "furnishing_keyword_scorer"),
        ("attributes.facing", state.facing, "facing_regex"),
        ("parking.parking_count", state.parking_count, "parking_count_regex"),
        ("parking.parking_type", state.parking_type, "parking_type_regex"),
        ("amenities", state.amenities, "amenities_automaton_or_llm"),
        ("property.property_subtype", state.property_subtype, "property_subtype_keyword"),
        ("property.all_detected_subtypes", state.all_detected_subtypes, "property_subtype_keyword"),
        ("metadata.message_title", state.message_title, "title_rule_generator"),
        ("metadata.contact_people", state.contact_people, "contact_name_llm"),
        ("metadata.contact_numbers", state.contact_numbers, "phone_regex_or_llm"),
    ]

    # 2. RUN PARALLEL FIELD-LEVEL VALIDATORS
    field_analysis = {}
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(validate_field, f_name, val, source_text, spans, ext)
            for f_name, val, ext in fields_to_validate
        ]
        for future in futures:
            f_name, result = future.result()
            field_analysis[f_name] = result

    # 3. RUN RULE ENGINE AND HANDLE CONFLICTS
    rules_passed, rule_failures = run_rule_engine(state)
    
    # Categorize failed fields based on rule failure mappings
    failed_fields = []
    hallucinated_fields = []
    
    # Extract fields from normal validators
    for f_name, report in field_analysis.items():
        if not report["valid"]:
            hallucinated_fields.append(f_name)
            failed_fields.append(f_name)

    # Process rule violations and mark target fields as contradictory/invalid
    for failure in rule_failures:
        # Determine rule name from prefix (e.g. "RentMustBeLessThanDeposit: Rent...")
        rule_name = failure.split(":")[0].strip()
        involved_fields = get_rule_failed_fields(rule_name)
        
        for field in involved_fields:
            if field in field_analysis:
                field_analysis[field]["valid"] = False
                field_analysis[field]["status"] = "contradictory"
                field_analysis[field]["confidence"] = max(10, field_analysis[field]["confidence"] - 40)
                field_analysis[field]["reason"] += f" Rule violation: {failure}"
                if field not in failed_fields:
                    failed_fields.append(field)

    # Calculate overall validation state
    is_valid = len(failed_fields) == 0
    confidence_score = 100 if is_valid else max(10, 100 - (len(failed_fields) * 15))

    audit_report = {
        "is_valid": is_valid,
        "confidence_score": confidence_score,
        "critical_issues": [f for f in rule_failures],
        "critical_hallucinations": [f"Unsupported field: {f}" for f in hallucinated_fields],
        "minor_issues": [],
        "hallucinated_fields": hallucinated_fields,
        "missed_fields": [f_name for f_name, report in field_analysis.items() if report["status"] == "missing"],
        "ambiguous_fields": [],
        "field_analysis": field_analysis,
        "reasoning_summary": "Parallel field-level validation and semantic consistency rule check.",
    }

    # Save to state's response_output if it exists
    response_output = dict(state.response_output or {})
    response_output["validation_report"] = audit_report

    return {
        "validation_report": audit_report,
        "response_output": response_output,
    }