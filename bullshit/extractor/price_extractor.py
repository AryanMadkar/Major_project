import re
from .GraphState import GraphState


# =========================================================
# PRECOMPILED REGEX
# =========================================================

PRICE_PATTERN = re.compile(
    r"""
    (?:
        rs\.?|₹
    )?
    \s*
    (\d+(?:\.\d+)?)
    \s*
    (
        k|
        thousand|
        l|
        lac|
        lakh|
        lakhs|
        lacs|
        cr|
        crore|
        crores
    )?
    """,
    re.IGNORECASE | re.VERBOSE
)

PHONE_PATTERN = re.compile(
    r"(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)"
)

RANGE_PATTERN = re.compile(
    r"\b(to|till|until|between|and|upto|up to)\b|[-–—]"
)

# =========================================================
# FAST KEYWORD SETS
# =========================================================

PRICE_WORDS = {
    "rent",
    "deposit",
    "budget",
    "asking",
    "price",
    "cost",
    "sale",
    "monthly",
    "lease",
    "quote",
    "quoted",
}

DEPOSIT_WORDS = {
    "deposit",
    "advance",
    "token",
    "maintenance",
}

RENT_WORDS = {
    "rent",
    "monthly",
    "lease",
    "per month",
}

AREA_WORDS = {
    "carpet",
    "sqft",
    "sq ft",
    "builtup",
    "area",
    "plot area",
}

# =========================================================
# UNIT MULTIPLIERS
# =========================================================

UNIT_MULTIPLIERS = {

    "k": 1_000,
    "thousand": 1_000,

    "l": 1_00_000,
    "lac": 1_00_000,
    "lakh": 1_00_000,
    "lakhs": 1_00_000,
    "lacs": 1_00_000,

    "cr": 1_00_00_000,
    "crore": 1_00_00_000,
    "crores": 1_00_00_000,
}


# =========================================================
# HELPERS
# =========================================================

def convert_price_to_number(value, unit):

    value = float(value)

    if not unit:
        return int(value)

    multiplier = UNIT_MULTIPLIERS.get(unit.lower())

    if multiplier:
        return int(value * multiplier)

    return int(value)


def has_any_keyword(context, keywords):

    return any(word in context for word in keywords)


# =========================================================
# MAIN
# =========================================================

def extract_price(state: GraphState):



    text = state.cleaned_text or ""

    request_type = state.request_type or "unknown"

    # =====================================================
    # PHONE SPANS
    # =====================================================

    phone_spans = [

        (m.start(), m.end())

        for m in PHONE_PATTERN.finditer(text)
    ]

    def overlaps_phone(start, end):

        for p_start, p_end in phone_spans:

            if start < p_end and end > p_start:
                return True

        return False

    # =====================================================
    # EXTRACT PRICES
    # =====================================================

    prices = []

    for match in PRICE_PATTERN.finditer(text):

        start = match.start()

        end = match.end()

        if overlaps_phone(start, end):
            continue

        number = match.group(1)

        unit = match.group(2)

        context = text[
            max(0, start - 35):
            end + 35
        ].lower()

        # ================================================
        # FAST FILTERS
        # ================================================

        if "bhk" in context:
            continue

        if has_any_keyword(context, AREA_WORDS):
            continue

        if unit is None and not has_any_keyword(context, PRICE_WORDS):
            continue

        try:

            value = convert_price_to_number(
                number,
                unit
            )

        except Exception:
            continue

        # ================================================
        # REQUEST TYPE FILTERS
        # ================================================

        if request_type == "sale" and value < 5_00_000:
            continue

        if (
            request_type == "rent"
            and unit
            and unit.lower() in {"cr", "crore", "crores"}
        ):
            continue

        score = 0

        if has_any_keyword(context, PRICE_WORDS):
            score += 5

        if has_any_keyword(context, DEPOSIT_WORDS):
            score += 5

        if has_any_keyword(context, RENT_WORDS):
            score += 5

        prices.append({

            "value": value,

            "unit": unit.lower() if unit else None,

            "start": start,

            "end": end,

            "score": score,

            "context": context
        })

    # =====================================================
    # EMPTY
    # =====================================================

    if not prices:

        return {
            "price": None,
            "price_min": None,
            "price_max": None,
            "rent_price": None,
            "deposit_price": None,
            "request_type": request_type,
        }

    # =====================================================
    # RANGE DETECTION
    # =====================================================

    price_min = None
    price_max = None
    price_min_match = None
    price_max_match = None

    if len(prices) >= 2:
        for left, right in zip(prices, prices[1:]):
            between = text[left["end"]:right["start"]].lower()
            if RANGE_PATTERN.search(between):
                price_min = min(left["value"], right["value"])
                price_max = max(left["value"], right["value"])
                price_min_match = left if left["value"] == price_min else right
                price_max_match = right if right["value"] == price_max else left
                break

    # =====================================================
    # RENT / DEPOSIT
    # =====================================================

    rent_price = None
    deposit_price = None
    rent_price_match = None
    deposit_price_match = None

    for item in prices:
        context = item["context"]
        if deposit_price is None and has_any_keyword(context, DEPOSIT_WORDS):
            deposit_price = item["value"]
            deposit_price_match = item
        if rent_price is None and has_any_keyword(context, RENT_WORDS):
            rent_price = item["value"]
            rent_price_match = item

    # =====================================================
    # FINAL PRICE
    # =====================================================

    best_price = max(
        prices,
        key=lambda x: (
            x["score"],
            x["value"]
        )
    )

    final_price = best_price["value"]

    # =====================================================
    # REQUEST TYPE INFERENCE
    # =====================================================

    inferred_request_type = request_type

    if request_type == "unknown":
        if final_price >= 5_00_000:
            inferred_request_type = "sale"
        else:
            inferred_request_type = "rent"

    # =====================================================
    # RECORD SPANS
    # =====================================================
    extraction_spans = {}
    
    if final_price is not None:
        extraction_spans["pricing.price"] = {
            "value": final_price,
            "source_span": text[best_price["start"]:best_price["end"]],
            "start": best_price["start"],
            "end": best_price["end"],
            "extractor": "price_regex"
        }
    if price_min is not None and price_min_match:
        extraction_spans["pricing.price_min"] = {
            "value": price_min,
            "source_span": text[price_min_match["start"]:price_min_match["end"]],
            "start": price_min_match["start"],
            "end": price_min_match["end"],
            "extractor": "price_range_regex"
        }
    if price_max is not None and price_max_match:
        extraction_spans["pricing.price_max"] = {
            "value": price_max,
            "source_span": text[price_max_match["start"]:price_max_match["end"]],
            "start": price_max_match["start"],
            "end": price_max_match["end"],
            "extractor": "price_range_regex"
        }
    if rent_price is not None and rent_price_match:
        extraction_spans["pricing.rent_price"] = {
            "value": rent_price,
            "source_span": text[rent_price_match["start"]:rent_price_match["end"]],
            "start": rent_price_match["start"],
            "end": rent_price_match["end"],
            "extractor": "price_rent_keyword_regex"
        }
    if deposit_price is not None and deposit_price_match:
        extraction_spans["pricing.deposit_price"] = {
            "value": deposit_price,
            "source_span": text[deposit_price_match["start"]:deposit_price_match["end"]],
            "start": deposit_price_match["start"],
            "end": deposit_price_match["end"],
            "extractor": "price_deposit_keyword_regex"
        }

    return {
        "price": final_price,
        "price_min": price_min,
        "price_max": price_max,
        "rent_price": rent_price,
        "deposit_price": deposit_price,
        "request_type": inferred_request_type,
        "extraction_spans": extraction_spans
    }