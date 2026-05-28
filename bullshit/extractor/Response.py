from typing import Any, List, Dict, Optional
from pydantic import BaseModel, Field
from .GraphState import GraphState


# ==========================================
# PYDANTIC OUTPUT SCHEMAS
# ==========================================

class SummarySchema(BaseModel):
    request_type: Optional[str] = None
    bhk: Optional[int] = None

class PricingSchema(BaseModel):
    price: Optional[int] = None
    price_display: Optional[str] = None
    price_min: Optional[int] = None
    price_max: Optional[int] = None
    price_min_display: Optional[str] = None
    price_max_display: Optional[str] = None
    rent_price: Optional[int] = None
    rent_price_display: Optional[str] = None
    deposit_price: Optional[int] = None
    deposit_price_display: Optional[str] = None

class LocationSchema(BaseModel):
    primary_location: Optional[str] = None
    railway_line: Optional[str] = None
    locations: Optional[List[str]] = None

class AttributesSchema(BaseModel):
    furnishing: Optional[str] = None
    facing: Optional[str] = None

class ParkingSchema(BaseModel):
    parking_count: Optional[int] = None
    parking_type: Optional[str] = None

class PropertySchema(BaseModel):
    property_subtype: Optional[str] = None
    all_detected_subtypes: Optional[List[str]] = None

class MetadataSchema(BaseModel):
    message_title: Optional[str] = None
    contact_people: Optional[List[str]] = None
    contact_numbers: Optional[List[str]] = None
    metadata_summary: Optional[Dict[str, Any]] = None

class FinalOutput(BaseModel):
    summary: SummarySchema
    pricing: PricingSchema
    location: LocationSchema
    attributes: AttributesSchema
    parking: ParkingSchema
    amenities: Optional[List[str]] = None
    property: PropertySchema
    metadata: MetadataSchema
    extraction_meta: Optional[Dict[str, Any]] = None


# ==========================================
# HELPERS
# ==========================================

def _format_inr(value):
    if value is None:
        return None
    return f"₹{int(value):,}"


def _as_int(value):
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def build_traceable_meta(field_name: str, default_source: str, default_confidence: float, value: Any, state: GraphState) -> Dict[str, Any]:
    """Builds a traceable metadata record for a field using spans and repair history."""
    meta = {
        "value": value,
        "source": default_source,
        "confidence": default_confidence if value not in (None, [], {}) else 0,
        "source_span": None,
        "start": None,
        "end": None,
        "extractor": None,
        "repair_history": []
    }
    
    # Retrieve span details
    spans = state.extraction_spans or {}
    if field_name in spans:
        span_info = spans[field_name]
        meta["source_span"] = span_info.get("source_span")
        meta["start"] = span_info.get("start")
        meta["end"] = span_info.get("end")
        meta["extractor"] = span_info.get("extractor")
        
    # Retrieve repair history
    history = state.repair_history or []
    field_history = [item for item in history if item.get("field") == field_name]
    meta["repair_history"] = field_history
    
    return meta


# ==========================================
# RESPONSE NODE
# ==========================================

def response_node(state: GraphState):

    output = {
        "summary": {
            "request_type": state.request_type,
            "bhk": state.bhk,
        },
        "pricing": {
            "price": _as_int(state.price),
            "price_display": _format_inr(state.price),
            "price_min": _as_int(state.price_min),
            "price_max": _as_int(state.price_max),
            "price_min_display": _format_inr(state.price_min),
            "price_max_display": _format_inr(state.price_max),
            "rent_price": _as_int(state.rent_price),
            "rent_price_display": _format_inr(state.rent_price),
            "deposit_price": _as_int(state.deposit_price),
            "deposit_price_display": _format_inr(state.deposit_price),
        },
        "location": {
            "primary_location": state.primary_location,
            "railway_line": state.railway_line,
            "locations": state.locations,
        },
        "attributes": {
            "furnishing": state.furnishing,
            "facing": state.facing,
        },
        "parking": {
            "parking_count": state.parking_count,
            "parking_type": state.parking_type,
        },
        "amenities": state.amenities,
        "property": {
            "property_subtype": state.property_subtype,
            "all_detected_subtypes": state.all_detected_subtypes,
        },
        "metadata": {
            "message_title": state.message_title,
            "contact_people": state.contact_people,
            "contact_numbers": state.contact_numbers,
            "metadata_summary": state.metadata_summary,
        },
        "extraction_meta": {
            "summary.request_type": build_traceable_meta("summary.request_type", "keyword+rules", 90, state.request_type, state),
            "summary.bhk": build_traceable_meta("summary.bhk", "regex", 90, state.bhk, state),
            "pricing.price": build_traceable_meta("pricing.price", "regex+rules", 85, _as_int(state.price), state),
            "pricing.price_min": build_traceable_meta("pricing.price_min", "regex+rules", 85, _as_int(state.price_min), state),
            "pricing.price_max": build_traceable_meta("pricing.price_max", "regex+rules", 85, _as_int(state.price_max), state),
            "pricing.rent_price": build_traceable_meta("pricing.rent_price", "regex+rules", 90, _as_int(state.rent_price), state),
            "pricing.deposit_price": build_traceable_meta("pricing.deposit_price", "regex+rules", 90, _as_int(state.deposit_price), state),
            "location.primary_location": build_traceable_meta("location.primary_location", "dictionary+patterns", 80, state.primary_location, state),
            "location.locations": build_traceable_meta("location.locations", "dictionary+patterns", 80, state.locations, state),
            "location.railway_line": build_traceable_meta("location.railway_line", "dictionary", 85, state.railway_line, state),
            "attributes.furnishing": build_traceable_meta("attributes.furnishing", "keyword+scoring", 80, state.furnishing, state),
            "attributes.facing": build_traceable_meta("attributes.facing", "keyword", 85, state.facing, state),
            "parking.parking_count": build_traceable_meta("parking.parking_count", "regex", 80, state.parking_count, state),
            "parking.parking_type": build_traceable_meta("parking.parking_type", "keyword", 80, state.parking_type, state),
            "amenities": build_traceable_meta("amenities", "regex+llm", 75, state.amenities, state),
            "property.property_subtype": build_traceable_meta("property.property_subtype", "keyword+llm", 80, state.property_subtype, state),
            "property.all_detected_subtypes": build_traceable_meta("property.all_detected_subtypes", "keyword+llm", 75, state.all_detected_subtypes, state),
            "metadata.message_title": build_traceable_meta("metadata.message_title", "llm+rules", 75, state.message_title, state),
            "metadata.contact_people": build_traceable_meta("metadata.contact_people", "llm+cleanup", 85, state.contact_people, state),
            "metadata.contact_numbers": build_traceable_meta("metadata.contact_numbers", "regex+llm", 95, state.contact_numbers, state),
        },
    }



    # Enforce Pydantic Schema Validation
    try:
        FinalOutput.model_validate(output)
    except Exception as e:
        print("Schema Validation Error:", e)

    return {"response_output": output}