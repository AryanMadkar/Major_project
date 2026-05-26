from typing import Any
import re

from extractor.GraphState import GraphState


def _count_missing_fields(response_output: dict[str, Any], required_fields: list[str]):
    missing_fields = []
    for field_name in required_fields:
        if field_name not in response_output:
            missing_fields.append(field_name)
            continue

        if response_output.get(field_name) in (None, {}, ""):
            missing_fields.append(field_name)
    return missing_fields


def _normalize_text(value: str) -> str:
    value = value.lower()
    value = value.replace("_", " ")
    value = re.sub(r"[^a-z0-9\s]", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def _is_supported_by_source(value: Any, source_text: str) -> bool:
    if value is None:
        return True

    if isinstance(value, bool):
        return True

    if isinstance(value, (int, float)):
        return str(int(value)) in re.sub(r"\D", "", source_text)

    if isinstance(value, str):
        normalized = _normalize_text(value)
        if not normalized:
            return True
        return normalized in _normalize_text(source_text)

    if isinstance(value, list):
        return all(_is_supported_by_source(item, source_text) for item in value)

    if isinstance(value, dict):
        return all(_is_supported_by_source(item, source_text) for item in value.values())

    return True


# ==========================================
# MAIN AUDIT NODE
# ==========================================

def audit_verification_agent(state: GraphState):

    response_output = state.get("response_output") or {}
    source_text = state.get("user_input") or state.get("cleaned_text") or ""

    if not isinstance(response_output, dict):
        response_output = {}

    missing_fields = _count_missing_fields(
        response_output,
        ["summary", "pricing", "location", "attributes", "parking", "amenities", "property", "metadata"]
    )

    hallucinated_fields = []
    field_analysis = {}
    recommended_repairs = {}

    for field_name in ["summary", "pricing", "location", "attributes", "parking", "amenities", "property", "metadata"]:
        value = response_output.get(field_name)

        if field_name in missing_fields:
            field_analysis[field_name] = {
                "valid": False,
                "confidence": 20,
                "status": "missing",
                "reason": "Field not present in the final response",
            }
            recommended_repairs[field_name] = "re-extract"
            continue

        supported = _is_supported_by_source(value, source_text)
        field_analysis[field_name] = {
            "valid": supported,
            "confidence": 90 if supported else 30,
            "status": "correct" if supported else "hallucinated_or_unsupported",
            "reason": "All field values are supported by source message" if supported else "One or more values are unsupported by source message",
        }

        if not supported:
            hallucinated_fields.append(field_name)
            recommended_repairs[field_name] = "remove unsupported values and re-extract conservatively"

    audit_report = {
        "is_valid": len(missing_fields) == 0 and len(hallucinated_fields) == 0,
        "confidence_score": 100 if len(missing_fields) == 0 and len(hallucinated_fields) == 0 else 55,
        "critical_issues": [
            f"Missing top-level fields: {', '.join(missing_fields)}"
        ] if missing_fields else [],
        "critical_hallucinations": [
            f"Unsupported fields detected: {', '.join(hallucinated_fields)}"
        ] if hallucinated_fields else [],
        "minor_issues": [],
        "hallucinated_fields": hallucinated_fields,
        "missed_fields": missing_fields,
        "ambiguous_fields": [],
        "field_analysis": field_analysis,
        "recommended_repairs": recommended_repairs,
        "reasoning_summary": "Deterministic structural and source-support validation of the final response payload",
    }

    return {
        "validation_report": audit_report,
        "response_output": response_output,
    }