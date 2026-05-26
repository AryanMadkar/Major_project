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
    }

    return {"response_output": output}