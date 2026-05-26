import re
from .GraphState import GraphState


# ==========================================
# HELPER FUNCTION
# Converts Indian price strings to integer
# ==========================================

def convert_price_to_number(value, unit):

    value = float(value)

    unit = unit.lower().strip()

    if unit in ["k", "thousand"]:
        return int(value * 1_000)

    elif unit in ["l", "lac", "lakh", "lakhs", "lacs"]:
        return int(value * 1_00_000)

    elif unit in ["cr", "crore", "crores"]:
        return int(value * 1_00_00_000)

    return int(value)


# ==========================================
# PRICE EXTRACTOR NODE
# ==========================================

def extract_price(state: GraphState):

    text = state["cleaned_text"]

    request_type = state.get("request_type")

    # ==========================================
    # REGEX PATTERN
    # Handles:
    # 45 lakh
    # 1.2 cr
    # 75k
    # 25000
    # 2 crore
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

    matches = re.finditer(price_pattern, text, re.IGNORECASE | re.VERBOSE)

    prices = []

    for match in matches:

        number = match.group(1)
        unit = match.group(2)

        # Skip tiny numbers
        if float(number) < 1000 and unit is None:
            continue

        try:

            if unit:
                final_price = convert_price_to_number(number, unit)
            else:
                final_price = int(float(number))

            prices.append({
                "value": final_price,
                "start": match.start(),
                "end": match.end()
            })

        except:
            continue

    # ==========================================
    # DEFAULT OUTPUT
    # ==========================================

    extracted_price = None
    rent_price = None
    deposit_price = None
    price_type = None

    # ==========================================
    # SMART RENT EXTRACTION
    # ==========================================

    if request_type == "rent":

        for p in prices:

            # Nearby context
            context = text[max(0, p["start"] - 25): p["end"] + 25]

            # Deposit detection
            if re.search(r"deposit|advance", context):

                deposit_price = p["value"]

            # Rent detection
            elif re.search(r"rent|monthly", context):

                rent_price = p["value"]

        # Fallback logic
        if rent_price is None and len(prices) >= 1:
            rent_price = prices[0]["value"]

        if deposit_price is None and len(prices) >= 2:
            deposit_price = prices[1]["value"]

        extracted_price = rent_price
        price_type = "rent"

    # ==========================================
    # SALE EXTRACTION
    # ==========================================

    elif request_type == "sale":

        if prices:
            extracted_price = max([p["value"] for p in prices])

        price_type = "sale"

    # ==========================================
    # REQUIREMENT EXTRACTION
    # ==========================================

    elif request_type == "requirement":

        if prices:
            extracted_price = max([p["value"] for p in prices])

        price_type = "requirement"

    # ==========================================
    # UNKNOWN TYPE
    # ==========================================

    else:

        if prices:
            extracted_price = max([p["value"] for p in prices])

        price_type = "unknown"

    return {

        "price": extracted_price,

        "rent_price": rent_price,

        "deposit_price": deposit_price,

        "price_type": price_type
    }