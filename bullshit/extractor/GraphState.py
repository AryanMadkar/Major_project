from typing import Any, Optional, TypedDict
# =========================
# GRAPH STATE
# =========================
class GraphState(TypedDict):
    user_input: str
    bhk: Optional[int]
    cleaned_text: Optional[str]
    request_type: Optional[str]
     # =========================
    # PRICE FIELDS
    # =========================

    price: Optional[int]

    price_min: Optional[int]

    price_max: Optional[int]

    rent_price: Optional[int]

    deposit_price: Optional[int]

    price_type: Optional[str]
    # location----------------------------------
    
    locations: Optional[list[str]]

    primary_location: Optional[str]

    railway_line: Optional[str]

    furnishing: Optional[str]

    facing: Optional[str]
    
    amenities: Optional[list[str]]

    parking_count: Optional[int]
    property_subtype: Optional[str]

    all_detected_subtypes: Optional[list[str]]
    message_title: Optional[str]

    contact_people: Optional[list[str]]

    contact_numbers: Optional[list[str]]

    metadata_summary: Optional[dict[str, Any]]

    parking_type: Optional[str]
    response_output: Optional[dict[str, Any]]
    