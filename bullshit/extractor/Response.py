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
            "request_type": state.get("request_type"),
            "bhk": state.get("bhk"),
        },
        "pricing": {
            "price": _as_int(state.get("price")),
            "price_display": _format_inr(state.get("price")),
            "price_min": _as_int(state.get("price_min")),
            "price_max": _as_int(state.get("price_max")),
            "price_min_display": _format_inr(state.get("price_min")),
            "price_max_display": _format_inr(state.get("price_max")),
            "rent_price": _as_int(state.get("rent_price")),
            "rent_price_display": _format_inr(state.get("rent_price")),
            "deposit_price": _as_int(state.get("deposit_price")),
            "deposit_price_display": _format_inr(state.get("deposit_price")),
        },
        "location": {
            "primary_location": state.get("primary_location"),
            "railway_line": state.get("railway_line"),
            "locations": state.get("locations"),
        },
        "attributes": {
            "furnishing": state.get("furnishing"),
            "facing": state.get("facing"),
        },
        "parking": {
            "parking_count": state.get("parking_count"),
            "parking_type": state.get("parking_type"),
        },
        "amenities": state.get("amenities"),
        "property": {
            "property_subtype": state.get("property_subtype"),
            "all_detected_subtypes": state.get("all_detected_subtypes"),
        },
        "metadata": {
            "message_title": state.get("message_title"),
            "contact_people": state.get("contact_people"),
            "contact_numbers": state.get("contact_numbers"),
            "metadata_summary": state.get("metadata_summary"),
        },
        "extraction_meta": {
            "summary.request_type": _meta(state.get("request_type"), "keyword+rules", 90),
            "summary.bhk": _meta(state.get("bhk"), "regex", 90),
            "pricing.price": _meta(_as_int(state.get("price")), "regex+rules", 85),
            "pricing.price_min": _meta(_as_int(state.get("price_min")), "regex+rules", 85),
            "pricing.price_max": _meta(_as_int(state.get("price_max")), "regex+rules", 85),
            "pricing.rent_price": _meta(_as_int(state.get("rent_price")), "regex+rules", 90),
            "pricing.deposit_price": _meta(_as_int(state.get("deposit_price")), "regex+rules", 90),
            "location.primary_location": _meta(state.get("primary_location"), "dictionary+patterns", 80),
            "location.locations": _meta(state.get("locations"), "dictionary+patterns", 80),
            "location.railway_line": _meta(state.get("railway_line"), "dictionary", 85),
            "attributes.furnishing": _meta(state.get("furnishing"), "keyword+scoring", 80),
            "attributes.facing": _meta(state.get("facing"), "keyword", 85),
            "parking.parking_count": _meta(state.get("parking_count"), "regex", 80),
            "parking.parking_type": _meta(state.get("parking_type"), "keyword", 80),
            "amenities": _meta(state.get("amenities"), "regex+llm", 75),
            "property.property_subtype": _meta(state.get("property_subtype"), "keyword+llm", 80),
            "property.all_detected_subtypes": _meta(state.get("all_detected_subtypes"), "keyword+llm", 75),
            "metadata.message_title": _meta(state.get("message_title"), "llm+rules", 75),
            "metadata.contact_people": _meta(state.get("contact_people"), "llm+cleanup", 85),
            "metadata.contact_numbers": _meta(state.get("contact_numbers"), "regex+llm", 95),
        },
    }

    return {"response_output": output}