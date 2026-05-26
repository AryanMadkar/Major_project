import re
from .GraphState import GraphState


# ==========================================
# PRICE CONVERTER
# ==========================================

def convert_price_to_number(value, unit):

    value = float(value)

    if not unit:
        return int(value)

    unit = unit.lower().strip()

    if unit in ["k", "thousand"]:
        return int(value * 1_000)

    elif unit in ["l", "lac", "lakh", "lakhs", "lacs"]:
        return int(value * 1_00_000)

    elif unit in ["cr", "crore", "crores"]:
        return int(value * 1_00_00_000)

    return int(value)


def _has_price_context(text, start, end):

    context = text[max(0, start - 35): end + 35].lower()

    return bool(
        re.search(
            r"\b(budget|price|asking|expected|range|between|from|to|upto|up to|rent|deposit|monthly|lease|per month|lac|lakh|lacs|lakhs|cr|crore|crores|k)\b",
            context,
        )
    )


def _looks_like_phone_number(text, start, end):

    snippet = text[start:end]

    return bool(re.fullmatch(r"(?:\+91[\s-]?)?[6-9]\d{9}", snippet))


# ==========================================
# MAIN EXTRACTOR
# ==========================================

def extract_price(state: GraphState):

    text = state["cleaned_text"]

    existing_type = state.get("request_type", "unknown")

    # ==========================================
    # PRICE PATTERN
    # ==========================================

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

    matches = re.finditer(
        price_pattern,
        text,
        re.IGNORECASE | re.VERBOSE
    )

    prices = []
    phone_spans = []

    for phone_match in re.finditer(r"(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)", text):
        phone_spans.append((phone_match.start(), phone_match.end()))

    def overlaps_phone(start, end):
        for phone_start, phone_end in phone_spans:
            if start < phone_end and end > phone_start:
                return True
        return False

    # ==========================================
    # EXTRACT ALL PRICES
    # ==========================================

    for match in matches:

        number = match.group(1)
        unit = match.group(2)

        # Skip tiny useless numbers
        if float(number) < 1000 and unit is None:
            continue

        # Do not confuse contact numbers with prices.
        if overlaps_phone(match.start(), match.end()):
            continue

        if unit is None and not _has_price_context(text, match.start(), match.end()):
            continue

        try:

            final_price = convert_price_to_number(
                number,
                unit
            )

            prices.append({
                "value": final_price,
                "unit": unit.lower() if unit else None,
                "start": match.start(),
                "end": match.end()
            })

        except:
            continue

    # ==========================================
    # DEFAULTS
    # ==========================================

    price = None

    rent_price = None

    deposit_price = None

    price_min = None

    price_max = None

    inferred_type = existing_type

    # ==========================================
    # RANGE DETECTION
    # ==========================================

    if len(prices) >= 2:

        for left, right in zip(prices, prices[1:]):

            between = text[left["end"]: right["start"]].lower()

            if re.search(r"\b(to|till|until|between|and|upto|up to)\b|[-–—]", between):

                price_min = min(left["value"], right["value"])
                price_max = max(left["value"], right["value"])
                break

    # ==========================================
    # DETECT RENT / DEPOSIT
    # ==========================================

    for p in prices:

        context = text[
            max(0, p["start"] - 25):
            p["end"] + 25
        ]

        # ======================================
        # DEPOSIT DETECTION
        # ======================================

        if re.search(
            r"deposit|advance|token|maintenance",
            context
        ):

            deposit_price = p["value"]

            inferred_type = "rent"

        # ======================================
        # RENT DETECTION
        # ======================================

        elif re.search(
            r"rent|monthly|lease|per month",
            context
        ):

            rent_price = p["value"]

            inferred_type = "rent"

    # ==========================================
    # FALLBACK RENT LOGIC
    # ==========================================

    if inferred_type == "rent":

        if rent_price is None and len(prices) >= 1:
            rent_price = prices[0]["value"]

        if deposit_price is None and len(prices) >= 2:
            deposit_price = prices[1]["value"]

        price = rent_price

    elif price_min is not None and price_max is not None:

        price = price_min

    # ==========================================
    # IF STILL UNKNOWN -> INFER USING PRICE
    # ==========================================

    if inferred_type == "unknown":

        if prices:

            biggest_price = max(
                [p["value"] for p in prices]
            )

            price = biggest_price

            # ==================================
            # CRORE ALWAYS SALE
            # ==================================

            crore_detected = any(
                p["unit"] in ["cr", "crore", "crores"]
                for p in prices
            )

            if crore_detected:

                inferred_type = "sale"

            # ==================================
            # HIGH VALUE => SALE
            # ==================================

            elif biggest_price >= 5_00_000:

                inferred_type = "sale"

            # ==================================
            # LOW VALUE => RENT
            # ==================================

            else:

                inferred_type = "rent"

    # ==========================================
    # SALE TYPE
    # ==========================================

    if inferred_type == "sale":

        if not price and prices:

            price = max(
                [p["value"] for p in prices]
            )

        if price_min is not None:

            price = price_min

    # ==========================================
    # FINAL SAFETY
    # ==========================================

    if not prices:

        inferred_type = "unknown"

    # ==========================================
    # RETURN
    # ==========================================

    return {

        "price": price,

        "price_min": price_min,

        "price_max": price_max,

        "rent_price": rent_price,

        "deposit_price": deposit_price,

        "price_type": inferred_type,
    }