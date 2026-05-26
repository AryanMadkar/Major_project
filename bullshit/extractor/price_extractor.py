import re
from .GraphState import GraphState


VALID_PRICE_CONTEXT = r"""
\b(
rent|
deposit|
budget|
asking|
quote|
quoted|
price|
cost|
sale|
cr|
crore|
lakh|
lac|
k|
rs|
monthly|
lease|
outright|
out\s*rate
)\b
"""


def convert_price_to_number(value, unit):

    value = float(value)

    if not unit:
        return int(value)

    unit = unit.lower().strip()

    if unit in ["k", "thousand"]:
        return int(value * 1_000)
    if unit in ["l", "lac", "lakh", "lakhs", "lacs"]:
        return int(value * 1_00_000)
    if unit in ["cr", "crore", "crores"]:
        return int(value * 1_00_00_000)

    return int(value)


def _has_price_context(text, start, end):

    context = text[max(0, start - 35): end + 35].lower()

    return bool(re.search(VALID_PRICE_CONTEXT, context, re.IGNORECASE | re.VERBOSE))


def _price_context_score(context):
    score = 0

    if re.search(VALID_PRICE_CONTEXT, context, re.IGNORECASE | re.VERBOSE):
        score += 6

    if re.search(r"\b(deposit|advance|token|maintenance)\b", context):
        score += 5

    if re.search(r"\b(rent|monthly|lease|per month)\b", context):
        score += 5

    if re.search(r"\b(range|between|from|to|upto|up to)\b", context):
        score += 2

    return score


def extract_price(state: GraphState):

    text = state.get("cleaned_text") or ""
    request_type = state.get("request_type", "unknown")

    price_pattern = r"""
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
    """

    phone_spans = [
        (match.start(), match.end())
        for match in re.finditer(r"(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)", text)
    ]

    def overlaps_phone(start, end):
        for phone_start, phone_end in phone_spans:
            if start < phone_end and end > phone_start:
                return True
        return False

    prices = []

    for match in re.finditer(price_pattern, text, re.IGNORECASE | re.VERBOSE):

        number = match.group(1)
        unit = match.group(2)
        context = text[max(0, match.start() - 35): match.end() + 35].lower()

        if overlaps_phone(match.start(), match.end()):
            continue

        # Block common non-price numerics (e.g. 2 bhk, 300 carpet, 1200 sqft).
        if re.search(r"\bbhk\b", context):
            continue

        if re.search(r"\b(carpet|sqft|sq\s*ft|builtup|area|plot area)\b", context):
            continue

        if unit is None and not _has_price_context(text, match.start(), match.end()):
            continue

        try:
            value = convert_price_to_number(number, unit)

            # Request-type-aware filtering for unrealistic/contradictory values.
            if request_type == "sale" and value < 5_00_000:
                continue

            if request_type == "rent" and unit and unit.lower() in ["cr", "crore", "crores"]:
                continue

            prices.append({
                "value": value,
                "unit": unit.lower() if unit else None,
                "start": match.start(),
                "end": match.end(),
                "context_score": _price_context_score(context),
            })
        except (TypeError, ValueError):
            continue

    price = None
    rent_price = None
    deposit_price = None
    price_min = None
    price_max = None
    detected_price_type = "unknown"

    if len(prices) >= 2:
        for left, right in zip(prices, prices[1:]):
            between = text[left["end"]: right["start"]].lower()
            if re.search(r"\b(to|till|until|between|and|upto|up to)\b|[-–—]", between):
                price_min = min(left["value"], right["value"])
                price_max = max(left["value"], right["value"])
                break

    for item in prices:

        context = text[max(0, item["start"] - 25): item["end"] + 25].lower()

        if re.search(r"\b(deposit|advance|token|maintenance)\b", context):
            deposit_price = item["value"]
            detected_price_type = "rent"
        elif re.search(r"\b(rent|monthly|lease|per month)\b", context):
            rent_price = item["value"]
            detected_price_type = "rent"

    if detected_price_type == "rent":

        if rent_price is None and prices:
            rent_price = prices[0]["value"]

        if deposit_price is None and len(prices) >= 2:
            deposit_price = prices[1]["value"]

        price = rent_price

    elif price_min is not None and price_max is not None:

        price = price_min

    if detected_price_type == "unknown" and prices:

        best_item = max(
            prices,
            key=lambda item: (item.get("context_score", 0), item["value"])
        )
        price = best_item["value"]

        crore_detected = any(
            item["unit"] in ["cr", "crore", "crores"]
            for item in prices
        )

        if crore_detected:
            detected_price_type = "sale"
        elif price >= 5_00_000:
            detected_price_type = "sale"
        else:
            detected_price_type = "rent"

    if detected_price_type == "sale" and price is None and prices:
        price = max(item["value"] for item in prices)

    if not prices:
        detected_price_type = "unknown"

    inferred_request_type = request_type
    if request_type == "unknown" and detected_price_type in {"sale", "rent"}:
        inferred_request_type = detected_price_type

    return {
        "price": price,
        "price_min": price_min,
        "price_max": price_max,
        "rent_price": rent_price,
        "deposit_price": deposit_price,
        "request_type": inferred_request_type,
    }