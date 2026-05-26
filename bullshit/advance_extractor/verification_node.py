from typing import Any

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


# ==========================================
# MAIN AUDIT NODE
# ==========================================

def audit_verification_agent(state: GraphState):

    response_output = state.get("response_output") or {}

    if not isinstance(response_output, dict):
        response_output = {}

    missing_fields = _count_missing_fields(
        response_output,
        ["summary", "pricing", "location", "attributes", "parking", "amenities", "property", "metadata"]
    )

    audit_report = {
        "is_valid": len(missing_fields) == 0,
        "confidence_score": 100 if len(missing_fields) == 0 else 60,
        "critical_issues": [
            f"Missing top-level fields: {', '.join(missing_fields)}"
        ] if missing_fields else [],
        "minor_issues": [],
        "hallucinated_fields": [],
        "missed_fields": missing_fields,
        "ambiguous_fields": [],
        "field_analysis": {
            field_name: {
                "status": "missing" if field_name in missing_fields else "correct",
                "reason": "Field not present in the final response" if field_name in missing_fields else "Field present in the final response",
            }
            for field_name in ["summary", "pricing", "location", "attributes", "parking", "amenities", "property", "metadata"]
        },
        "reasoning_summary": "Deterministic structural validation of the final response payload",
    }

    return {
        "validation_report": audit_report,
        "response_output": response_output,
    }