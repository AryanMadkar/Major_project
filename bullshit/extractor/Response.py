from typing import Any, List, Dict, Optional

from pydantic import BaseModel

from .GraphState import GraphState


# ==========================================
# PYDANTIC OUTPUT SCHEMAS
# ==========================================

class SummarySchema(BaseModel):

    request_type: Optional[str] = None

    bhk: Optional[int] = None


class PricingSchema(BaseModel):

    price: Optional[int] = None

    price_min: Optional[int] = None

    price_max: Optional[int] = None

    rent_price: Optional[int] = None

    deposit_price: Optional[int] = None


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

    validation_report: Optional[Dict[str, Any]] = None

    extraction_meta: Optional[Dict[str, Any]] = None


# ==========================================
# HELPERS
# ==========================================

def _as_int(value):

    if value is None:
        return None

    try:
        return int(value)

    except (TypeError, ValueError):
        return None


# ==========================================
# TRACEABLE META BUILDER
# ==========================================

def build_traceable_meta(

    field_name: str,

    default_source: str,

    default_confidence: float,

    value: Any,

    state: GraphState

) -> Dict[str, Any]:

    meta = {

        "value": value,

        "source": default_source,

        "confidence": (
            default_confidence
            if value not in (None, [], {})
            else 0
        ),

        "source_spans": [],

        "repair_history": []
    }

    # ======================================
    # EXTRACTION SPANS
    # ======================================

    spans = state.extraction_spans or {}

    if field_name in spans:

        span_info = spans[field_name]

        meta["source_spans"].append({

            "text": span_info.get("source_span"),

            "start": span_info.get("start"),

            "end": span_info.get("end"),

            "extractor": span_info.get("extractor")
        })

    # ======================================
    # REPAIR HISTORY
    # ======================================

    history = state.repair_history or []

    field_history = [

        item

        for item in history

        if item.get("field") == field_name
    ]

    meta["repair_history"] = field_history

    return meta


# ==========================================
# FIELD META CONFIG
# ==========================================

FIELD_META_CONFIG = {

    "summary.request_type": {
        "source": "keyword+rules",
        "confidence": 90,
        "value": lambda s: s.request_type
    },

    "summary.bhk": {
        "source": "regex",
        "confidence": 90,
        "value": lambda s: s.bhk
    },

    "pricing.price": {
        "source": "regex+rules",
        "confidence": 85,
        "value": lambda s: _as_int(s.price)
    },

    "pricing.price_min": {
        "source": "regex+rules",
        "confidence": 85,
        "value": lambda s: _as_int(s.price_min)
    },

    "pricing.price_max": {
        "source": "regex+rules",
        "confidence": 85,
        "value": lambda s: _as_int(s.price_max)
    },

    "pricing.rent_price": {
        "source": "regex+rules",
        "confidence": 90,
        "value": lambda s: _as_int(s.rent_price)
    },

    "pricing.deposit_price": {
        "source": "regex+rules",
        "confidence": 90,
        "value": lambda s: _as_int(s.deposit_price)
    },

    "location.primary_location": {
        "source": "dictionary+patterns",
        "confidence": 80,
        "value": lambda s: s.primary_location
    },

    "location.locations": {
        "source": "dictionary+patterns",
        "confidence": 80,
        "value": lambda s: s.locations
    },

    "location.railway_line": {
        "source": "dictionary",
        "confidence": 85,
        "value": lambda s: s.railway_line
    },

    "attributes.furnishing": {
        "source": "keyword+scoring",
        "confidence": 80,
        "value": lambda s: s.furnishing
    },

    "attributes.facing": {
        "source": "keyword",
        "confidence": 85,
        "value": lambda s: s.facing
    },

    "parking.parking_count": {
        "source": "regex",
        "confidence": 80,
        "value": lambda s: s.parking_count
    },

    "parking.parking_type": {
        "source": "keyword",
        "confidence": 80,
        "value": lambda s: s.parking_type
    },

    "amenities": {
        "source": "regex+llm",
        "confidence": 75,
        "value": lambda s: s.amenities
    },

    "property.property_subtype": {
        "source": "keyword+llm",
        "confidence": 80,
        "value": lambda s: s.property_subtype
    },

    "property.all_detected_subtypes": {
        "source": "keyword+llm",
        "confidence": 75,
        "value": lambda s: s.all_detected_subtypes
    },

    "metadata.message_title": {
        "source": "llm+rules",
        "confidence": 75,
        "value": lambda s: s.message_title
    },

    "metadata.contact_people": {
        "source": "llm+cleanup",
        "confidence": 85,
        "value": lambda s: s.contact_people
    },

    "metadata.contact_numbers": {
        "source": "regex+llm",
        "confidence": 95,
        "value": lambda s: s.contact_numbers
    }
}


# ==========================================
# RESPONSE NODE
# ==========================================

def response_node(state: GraphState):

    extraction_meta = {}

    # ======================================
    # BUILD EXTRACTION META
    # ======================================

    for field_name, config in FIELD_META_CONFIG.items():

        extraction_meta[field_name] = build_traceable_meta(

            field_name=field_name,

            default_source=config["source"],

            default_confidence=config["confidence"],

            value=config["value"](state),

            state=state
        )

    # ======================================
    # FINAL OUTPUT
    # ======================================

    output = {

        "summary": {

            "request_type": state.request_type,

            "bhk": state.bhk
        },

        "pricing": {

            "price": _as_int(state.price),

            "price_min": _as_int(state.price_min),

            "price_max": _as_int(state.price_max),

            "rent_price": _as_int(state.rent_price),

            "deposit_price": _as_int(state.deposit_price)
        },

        "location": {

            "primary_location": state.primary_location,

            "railway_line": state.railway_line,

            "locations": state.locations
        },

        "attributes": {

            "furnishing": state.furnishing,

            "facing": state.facing
        },

        "parking": {

            "parking_count": state.parking_count,

            "parking_type": state.parking_type
        },

        "amenities": state.amenities,

        "property": {

            "property_subtype": state.property_subtype,

            "all_detected_subtypes": state.all_detected_subtypes
        },

        "metadata": {

            "message_title": state.message_title,

            "contact_people": state.contact_people,

            "contact_numbers": state.contact_numbers,

            "metadata_summary": state.metadata_summary
        },

        "validation_report": state.validation_report,

        "extraction_meta": extraction_meta
    }

    # ======================================
    # PYDANTIC VALIDATION
    # ======================================

    try:

        FinalOutput.model_validate(output)

    except Exception as e:

        raise ValueError(
            f"Response Schema Validation Failed: {e}"
        )

    return {
        "response_output": output
    }
