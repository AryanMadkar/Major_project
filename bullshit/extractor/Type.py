import re
from .GraphState import GraphState

# =========================
# TYPE EXTRACTOR NODE
# =========================
def extract_type(state: GraphState):

    text = state["cleaned_text"]

    # =========================
    # KEYWORDS
    # =========================

    requirement_keywords = [
        "required",
        "requirement",
        "need",
        "looking for",
        "require",
        "searching",
        "want",
        "wanted",
        "required flat",
        "required for",
        "find me",
        "i am searching",
        "i need",
        "out rate",
        "outright"
    ]

    rent_keywords = [
        "rent",
        "rental",
        "lease",
        "tenant",
        "available for rent",
        "monthly rent",
        "pg"
    ]

    sales_keywords = [
        "sell",
        "sale",
        "selling",
        "buy",
        "purchase",
        "available for sale",
        "own house",
        "investment"
    ]

    request_type = "unknown"

    # =========================
    # CHECK REQUIREMENT
    # =========================
    for word in requirement_keywords:
        if re.search(rf"\b{re.escape(word)}\b", text):
            request_type = "requirement"
            break

    if request_type == "unknown":
        if re.search(r"\b(required|need|wanted|looking for|requirement)\b", text):
            request_type = "requirement"

    # =========================
    # CHECK RENT
    # =========================
    if request_type == "unknown":
        for word in rent_keywords:
            if re.search(rf"\b{re.escape(word)}\b", text):
                request_type = "rent"
                break

    # =========================
    # CHECK SALES
    # =========================
    if request_type == "unknown":
        for word in sales_keywords:
            if re.search(rf"\b{re.escape(word)}\b", text):
                request_type = "sale"
                break

    return {
        "request_type": request_type
    }
