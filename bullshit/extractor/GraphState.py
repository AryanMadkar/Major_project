from typing import TypedDict, Optional
# =========================
# GRAPH STATE
# =========================
class GraphState(TypedDict):
    user_input: str
    bhk: Optional[int]
    cleaned_text: Optional[str]
    request_type: Optional[str]