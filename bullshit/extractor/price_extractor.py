import re
from .GraphState import GraphState


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

    return bool(
        re.search(
            r"\b(budget|price|asking|expected|range|between|from|to|upto|up to|rent|deposit|monthly|lease|per month|rate|sq\s*ft|sqft|psf|per sq\s*ft|per sqft|lac|lakh|lacs|lakhs|cr|crore|crores|k)\b",
            context,
        )
    )


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

        if overlaps_phone(match.start(), match.end()):
            continue

        if unit is None and not _has_price_context(text, match.start(), match.end()):
            continue

        try:
            prices.append({
                "value": convert_price_to_number(number, unit),
                "unit": unit.lower() if unit else None,
                "start": match.start(),
                "end": match.end(),
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

        biggest_price = max(item["value"] for item in prices)
        price = biggest_price

        crore_detected = any(
            item["unit"] in ["cr", "crore", "crores"]
            for item in prices
        )

        if crore_detected:
            detected_price_type = "sale"
        elif biggest_price >= 5_00_000:
            detected_price_type = "sale"
        else:
            detected_price_type = "rent"

    if detected_price_type == "sale" and price is None and prices:
        price = max(item["value"] for item in prices)

    if not prices:
        detected_price_type = "unknown"

    if request_type == "requirement":
        price_type = "budget" if prices else "unknown"
    else:
        price_type = detected_price_type

    return {
        "price": price,
        "price_min": price_min,
        "price_max": price_max,
        "rent_price": rent_price,
        "deposit_price": deposit_price,
        "price_type": price_type,
        "detected_price_type": detected_price_type,
    }