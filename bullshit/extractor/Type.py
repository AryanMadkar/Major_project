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

    rent_keywords = [
        "rent",
        "rental",
        "lease",
        "tenant",
        "available for rent",
        "monthly rent",
        "pg"
    ]

    requirement_keywords = [
        "need",
        "looking for",
        "require",
        "requirement",
        "searching",
        "want",
        "find me",
        "i am searching",
        "i need"
    ]

    request_type = None

    # =========================
    # CHECK SALES
    # =========================
    for word in sales_keywords:
        if re.search(rf"\b{re.escape(word)}\b", text):
            request_type = "sales"
            break

    # =========================
    # CHECK RENT
    # =========================
    if request_type is None:
        for word in rent_keywords:
            if re.search(rf"\b{re.escape(word)}\b", text):
                request_type = "rent"
                break

    # =========================
    # CHECK REQUIREMENT
    # =========================
    if request_type is None:
        for word in requirement_keywords:
            if re.search(rf"\b{re.escape(word)}\b", text):
                request_type = "requirements"
                break

    return {
        "request_type": request_type
    }
