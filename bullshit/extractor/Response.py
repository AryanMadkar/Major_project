from .GraphState import GraphState


def _format_inr(value):
    if value is None:
        return None
    return f"₹{int(value):,}"


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
            "price_type": state.get("price_type"),
            "price": state.get("price"),
            "price_display": _format_inr(state.get("price")),
            "rent_price": state.get("rent_price"),
            "rent_price_display": _format_inr(state.get("rent_price")),
            "deposit_price": state.get("deposit_price"),
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
    }

    print("\n=== Extraction Summary ===")
    print(f"Request Type: {output.get('summary', {}).get('request_type', 'unknown')}")
    print(f"BHK: {output.get('summary', {}).get('bhk', 'not found')}")

    pricing = output.get("pricing", {})
    if pricing.get("price_display"):
        print(f"Price: {pricing['price_display']}")
    if pricing.get("rent_price_display"):
        print(f"Rent: {pricing['rent_price_display']}")
    if pricing.get("deposit_price_display"):
        print(f"Deposit: {pricing['deposit_price_display']}")

    location = output.get("location", {})
    if location.get("primary_location"):
        print(f"Primary Location: {location['primary_location']}")
    if location.get("railway_line"):
        print(f"Railway Line: {location['railway_line']}")
    if location.get("locations"):
        print(f"Detected Locations: {', '.join(location['locations'])}")

    attributes = output.get("attributes", {})
    # Always print attributes (may be None)
    print(f"Furnishing: {attributes.get('furnishing')}")
    print(f"Facing: {attributes.get('facing')}")

    parking = output.get("parking", {})
    print(f"Parking Count: {parking.get('parking_count')}")
    print(f"Parking Type: {parking.get('parking_type')}")

    print(f"Amenities: {output.get('amenities')}")

    prop = output.get("property", {})
    print(f"Property Subtype: {prop.get('property_subtype')}")
    print(f"All Detected Subtypes: {prop.get('all_detected_subtypes')}")

    return {"response_output": output}