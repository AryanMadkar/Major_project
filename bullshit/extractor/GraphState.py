from typing import TypedDict, Optional
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