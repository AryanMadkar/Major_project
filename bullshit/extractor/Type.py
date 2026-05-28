import re
from .GraphState import GraphState

# =========================
# TYPE EXTRACTOR NODE
# =========================
def extract_type(state: GraphState):



    text = (state.cleaned_text or "").lower()

    # =========================
    # KEYWORDS
    # =========================

    requirement_keywords = [
        "required",
        "requirement",
        "looking for",
        "require",
        "searching",
        "want",
        "wanted",
        "required flat",
        "required for",
        "find me",
        "i am searching",
        "i need"
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
        "investment",
        "asking",
        "quote",
        "quoted",
        "out rate",
        "outright",
        "immediate possession",
        "oc",
        "possession"
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
        if re.search(r"\b(required|wanted|looking for|requirement)\b", text):
            request_type = "requirement"

    # "need" alone overfires in many sale/rent messages.
    if request_type == "unknown":
        if re.search(r"\bneed\b", text) and re.search(
            r"\b(flat|apartment|house|property|bhk|rk|room)\b",
            text,
        ):
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

    detected_price_type = "unknown"
    if re.search(r"\b(cr|crore|crores|lakh|lac|asking|quote|quoted|out rate|outright)\b", text):
        detected_price_type = "sale"

    state_price = state.price
    if detected_price_type == "unknown" and state_price is not None and isinstance(state_price, (int, float)) and int(state_price) >= 5_00_000:
        detected_price_type = "sale"

    if detected_price_type == "sale" and request_type == "unknown":
        request_type = "sale"

    # =========================
    # RECORD SPANS
    # =========================
    extraction_spans = dict(state.extraction_spans or {})
    matched_word = None
    start = -1
    end = -1
    
    if request_type == "requirement":
        for word in requirement_keywords:
            m = re.search(rf"\b{re.escape(word)}\b", text)
            if m:
                matched_word = m.group(0)
                start = m.start()
                end = m.end()
                break
        if not matched_word:
            m = re.search(r"\b(required|wanted|looking for|requirement)\b", text)
            if m:
                matched_word = m.group(0)
                start = m.start()
                end = m.end()
        if not matched_word:
            m = re.search(r"\bneed\b", text)
            if m:
                matched_word = m.group(0)
                start = m.start()
                end = m.end()
    elif request_type == "rent":
        for word in rent_keywords:
            m = re.search(rf"\b{re.escape(word)}\b", text)
            if m:
                matched_word = m.group(0)
                start = m.start()
                end = m.end()
                break
    elif request_type == "sale":
        for word in sales_keywords:
            m = re.search(rf"\b{re.escape(word)}\b", text)
            if m:
                matched_word = m.group(0)
                start = m.start()
                end = m.end()
                break
        if not matched_word:
            m = re.search(r"\b(cr|crore|crores|lakh|lac|asking|quote|quoted|out rate|outright)\b", text)
            if m:
                matched_word = m.group(0)
                start = m.start()
                end = m.end()
                
    if matched_word:
        extraction_spans["summary.request_type"] = {
            "value": request_type,
            "source_span": matched_word,
            "start": start,
            "end": end,
            "extractor": "type_keyword_regex"
        }

    return {
        "request_type": request_type,
        "extraction_spans": {
            "summary.request_type": {
                "value": request_type,
                "source_span": matched_word,
                "start": start,
                "end": end,
                "extractor": "type_keyword_regex"
            }
        } if matched_word else {}
    }
