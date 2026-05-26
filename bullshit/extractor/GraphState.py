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

    rent_price: Optional[int]

    deposit_price: Optional[int]

    price_type: Optional[str]
    # location----------------------------------
    
    locations: Optional[list[str]]

    primary_location: Optional[str]

    railway_line: Optional[str]

    response_output: Optional[dict[str, Any]]