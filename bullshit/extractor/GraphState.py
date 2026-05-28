from typing import Any, Annotated
import operator

from pydantic import BaseModel


# =================================
# MERGE REDUCERS
# These tell LangGraph how to combine
# concurrent updates from parallel nodes.
# =================================

def _merge_dicts(a: dict | None, b: dict | None) -> dict:
    """Merge two dicts, with b overwriting keys in a."""
    result = dict(a or {})
    result.update(b or {})
    return result


def _merge_lists(a: list | None, b: list | None) -> list:
    """Append new items from b to a (dedup by dict identity not needed here)."""
    return list(a or []) + list(b or [])


class GraphState(BaseModel):

    # =================================
    # INPUT
    # =================================

    user_input: str | None = None

    cleaned_text: str | None = None

    # =================================
    # PROPERTY DETAILS
    # =================================

    bhk: int | None = None

    property_subtype: str | None = None

    furnishing: str | None = None

    facing: str | None = None

    parking_count: int | None = None

    parking_type: str | None = None

    amenities: list[str] | None = None

    # =================================
    # PRICE
    # =================================

    price: int | None = None

    price_min: int | None = None

    price_max: int | None = None

    rent_price: int | None = None

    deposit_price: int | None = None

    # =================================
    # LOCATION
    # =================================

    locations: list[str] | None = None

    primary_location: str | None = None

    railway_line: str | None = None

    # =================================
    # CONTACT
    # =================================

    contact_people: list[str] | None = None

    contact_numbers: list[str] | None = None

    # =================================
    # REQUEST
    # =================================

    request_type: str | None = None

    # =================================
    # VALIDATION / PIPELINE
    # =================================


    validation_report: Annotated[dict[str, Any],_merge_dicts] = {}



    verification_history: list[dict[str, Any]] | None = None

    iteration_count: int | None = None

    
    should_continue: bool | None = None

    # =================================
    # EXTRA METADATA
    # =================================

    all_detected_subtypes: list[str] | None = None

    metadata_summary: dict[str, Any] | None = None

    response_output: dict[str, Any] | None = None

    message_title: str | None = None

    # =================================
    # PROVENANCE & REPAIRS
    # =================================

    extraction_spans: Annotated[dict[str, dict[str, Any]], _merge_dicts] = {}

    repair_history: Annotated[list[dict[str, Any]], _merge_lists] = []

    fixed_fields: Annotated[list[str], _merge_lists] = []
    # =================================
    # REPAIR SYSTEM
    # =================================

    failed_fields: list[str] | None = None

    repair_candidates: Annotated[
        list[dict[str, Any]],
        _merge_lists
    ] = []

    repair_attempts: Annotated[
        dict[str, int],
        _merge_dicts
    ] = {}

    reverification_required: list[str] | None = None