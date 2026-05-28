from .GraphState import GraphState


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


def _meta(value, source, confidence):
    if value in (None, [], {}):
        return {
            "value": value,
            "source": source,
            "confidence": 0,
        }
    return {
        "value": value,
        "source": source,
        "confidence": confidence,
    }


# =========================
# RESPONSE NODE
# =========================
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
            "summary.request_type": _meta(state.request_type, "keyword+rules", 90),
            "summary.bhk": _meta(state.bhk, "regex", 90),
            "pricing.price": _meta(_as_int(state.price), "regex+rules", 85),
            "pricing.price_min": _meta(_as_int(state.price_min), "regex+rules", 85),
            "pricing.price_max": _meta(_as_int(state.price_max), "regex+rules", 85),
            "pricing.rent_price": _meta(_as_int(state.rent_price), "regex+rules", 90),
            "pricing.deposit_price": _meta(_as_int(state.deposit_price), "regex+rules", 90),
            "location.primary_location": _meta(state.primary_location, "dictionary+patterns", 80),
            "location.locations": _meta(state.locations, "dictionary+patterns", 80),
            "location.railway_line": _meta(state.railway_line, "dictionary", 85),
            "attributes.furnishing": _meta(state.furnishing, "keyword+scoring", 80),
            "attributes.facing": _meta(state.facing, "keyword", 85),
            "parking.parking_count": _meta(state.parking_count, "regex", 80),
            "parking.parking_type": _meta(state.parking_type, "keyword", 80),
            "amenities": _meta(state.amenities, "regex+llm", 75),
            "property.property_subtype": _meta(state.property_subtype, "keyword+llm", 80),
            "property.all_detected_subtypes": _meta(state.all_detected_subtypes, "keyword+llm", 75),
            "metadata.message_title": _meta(state.message_title, "llm+rules", 75),
            "metadata.contact_people": _meta(state.contact_people, "llm+cleanup", 85),
            "metadata.contact_numbers": _meta(state.contact_numbers, "regex+llm", 95),
        },
    }

    return {"response_output": output}