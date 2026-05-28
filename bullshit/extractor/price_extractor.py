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
    "@",
    "negotiable",
    "neg",
    "/-",
}

DEPOSIT_WORDS = {
    "deposit",
    "advance",
    "token",
    "maintenance",
    "dep",
    "dp",
}

RENT_WORDS = {
    "rent",
    "monthly",
    "lease",
    "per month",
    "pm",
    "p.m.",
    "p/m",
    "rented",
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


def min_distance_to_keywords(start, end, keywords, text):
    min_dist = 999999
    escaped_keywords = []
    for kw in keywords:
        if kw == "@":
            escaped_keywords.append(r"@")
        elif kw == "/-":
            escaped_keywords.append(r"/-")
        else:
            escaped_kw = re.escape(kw)
            escaped_keywords.append(rf"\b{escaped_kw}\b")
    pattern_str = "|".join(escaped_keywords)
    try:
        pattern = re.compile(pattern_str, re.IGNORECASE)
    except Exception:
        return min_dist

    for match in pattern.finditer(text):
        m_start = match.start()
        m_end = match.end()
        if m_end <= start:
            dist = start - m_end
        elif m_start >= end:
            dist = m_start - end
        else:
            dist = 0
        if dist < min_dist:
            min_dist = dist
    return min_dist


def resolve_price_conflicts(prices, request_type, text, price_min=None, price_max=None):
    assigned_rent = None
    assigned_deposit = None
    assigned_price = None
    
    rent_match = None
    deposit_match = None
    price_match = None
    
    assignments = []
    for i, item in enumerate(prices):
        # Calculate distance scores
        rent_dist = min_distance_to_keywords(item["start"], item["end"], RENT_WORDS, text)
        deposit_dist = min_distance_to_keywords(item["start"], item["end"], DEPOSIT_WORDS, text)
        price_dist = min_distance_to_keywords(item["start"], item["end"], PRICE_WORDS, text)
        
        rent_score = max(0, 100 - rent_dist * 3)
        deposit_score = max(0, 100 - deposit_dist * 3)
        price_score = max(0, 100 - price_dist * 3)
        
        # Context checks for @ just before
        pre_context = text[max(0, item["start"] - 3):item["start"]].strip()
        if pre_context.endswith("@"):
            rent_score += 80
            
        post_context = text[item["end"]:item["end"] + 3].strip()
        if post_context.startswith("/-"):
            rent_score += 20
            price_score += 20
            
        # Store scores in item
        item["rent_score"] = rent_score
        item["deposit_score"] = deposit_score
        item["price_score"] = price_score
        
        assignments.append((i, "rent", rent_score))
        assignments.append((i, "deposit", deposit_score))
        assignments.append((i, "price", price_score))
        
    assignments.sort(key=lambda x: x[2], reverse=True)
    
    assigned_candidates = set()
    assigned_roles = set()
    
    for idx, role, score in assignments:
        if idx in assigned_candidates or role in assigned_roles:
            continue
        if score > 20:
            assigned_candidates.add(idx)
            assigned_roles.add(role)
            if role == "rent":
                assigned_rent = prices[idx]["value"]
                rent_match = prices[idx]
            elif role == "deposit":
                assigned_deposit = prices[idx]["value"]
                deposit_match = prices[idx]
            elif role == "price":
                assigned_price = prices[idx]["value"]
                price_match = prices[idx]
                
    # If rent request type and only one price was found:
    if len(prices) == 1 and request_type == "rent":
        item = prices[0]
        assigned_rent = item["value"]
        rent_match = item
        assigned_price = item["value"]
        price_match = item
        assigned_candidates.add(0)
    else:
        unassigned_indices = [i for i in range(len(prices)) if i not in assigned_candidates]
        for idx in unassigned_indices:
            item = prices[idx]
            val = item["value"]
            
            # If the candidate was already captured in a price range, do not fallback-assign it to other fields
            is_in_range = False
            if price_min is not None and (val == price_min or val == price_max):
                is_in_range = True
                
            if is_in_range:
                continue
                
            if request_type == "rent":
                if assigned_rent is None and item["rent_score"] > 20:
                    assigned_rent = val
                    rent_match = item
                    assigned_candidates.add(idx)
                elif assigned_deposit is None and item["deposit_score"] > 20:
                    assigned_deposit = val
                    deposit_match = item
                    assigned_candidates.add(idx)
            elif request_type == "sale":
                if assigned_price is None and item["price_score"] > 20:
                    assigned_price = val
                    price_match = item
                    assigned_candidates.add(idx)
                
    # Swap rent and deposit if deposit < rent (except if one of them is null)
    if assigned_deposit is not None and assigned_rent is not None:
        if assigned_deposit < assigned_rent:
            assigned_deposit, assigned_rent = assigned_rent, assigned_deposit
            deposit_match, rent_match = rent_match, deposit_match
            
    # Re-align final price
    if request_type == "rent":
        if assigned_rent is not None:
            assigned_price = assigned_rent
            price_match = rent_match
    elif request_type == "sale":
        if assigned_price is not None:
            assigned_rent = None
            rent_match = None
            
    return assigned_price, price_match, assigned_rent, rent_match, assigned_deposit, deposit_match


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

        try:

            value = convert_price_to_number(
                number,
                unit
            )

        except Exception:
            continue

        # ================================================
        # FAST FILTERS
        # ================================================

        if unit is None and value < 500:
            continue

        if has_any_keyword(context, AREA_WORDS):
            continue

        if unit is None and not has_any_keyword(context, PRICE_WORDS):
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
    # RENT / DEPOSIT / FINAL PRICE RESOLVER (Fix #1 & #3)
    # =====================================================

    final_price, best_price, rent_price, rent_price_match, deposit_price, deposit_price_match = resolve_price_conflicts(
        prices,
        request_type,
        text,
        price_min=price_min,
        price_max=price_max
    )

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