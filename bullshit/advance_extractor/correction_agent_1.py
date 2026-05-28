import copy
from typing import Any, Dict
from extractor.GraphState import GraphState


def build_title_local(bhk: Any, property_subtype: Any, primary_location: Any, request_type: Any) -> str:
    parts = []
    if bhk is not None and isinstance(bhk, int):
        parts.append(f"{bhk}BHK")
    parts.append(str(property_subtype or "Flat").title())
    if request_type == "rent":
        parts.append("For Rent")
    elif request_type == "sale":
        parts.append("For Sale")
    if primary_location:
        parts.append(f"in {str(primary_location).title()}")
    title = " ".join(parts).strip()
    return title if title else None


def correction_agent_1(state: GraphState):
    """
    Deterministic Python Repair Engine (Runs in ~0ms, zero LLM calls).
    Repairs deterministic fields: bhk, request_type, pricing fields, parking count/type.
    """


    validation_report = state.validation_report or {}
    field_analysis = validation_report.get("field_analysis", {})
    repair_history = list(state.repair_history or [])

    # Local copies of state fields we might edit
    bhk = state.bhk
    request_type = state.request_type
    price = state.price
    price_min = state.price_min
    price_max = state.price_max
    rent_price = state.rent_price
    deposit_price = state.deposit_price
    parking_count = state.parking_count
    parking_type = state.parking_type
    message_title = state.message_title
    
    # ----------------------------------------------------
    # RULE 1: Swap rent and deposit if rent > deposit
    # ----------------------------------------------------
    if rent_price is not None and deposit_price is not None and rent_price > deposit_price:
        old_rent, old_dep = rent_price, deposit_price
        rent_price, deposit_price = deposit_price, rent_price
        repair_history.append({
            "field": "pricing.rent_price",
            "old_value": old_rent,
            "new_value": rent_price,
            "reason": "Swapped rent and deposit because rent was greater than deposit"
        })
        repair_history.append({
            "field": "pricing.deposit_price",
            "old_value": old_dep,
            "new_value": deposit_price,
            "reason": "Swapped rent and deposit because rent was greater than deposit"
        })

    # ----------------------------------------------------
    # RULE 2: Swap price_min and price_max if min > max
    # ----------------------------------------------------
    if price_min is not None and price_max is not None and price_min > price_max:
        old_min, old_max = price_min, price_max
        price_min, price_max = price_max, price_min
        repair_history.append({
            "field": "pricing.price_min",
            "old_value": old_min,
            "new_value": price_min,
            "reason": "Swapped price_min and price_max because min > max"
        })
        repair_history.append({
            "field": "pricing.price_max",
            "old_value": old_max,
            "new_value": price_max,
            "reason": "Swapped price_min and price_max because min > max"
        })

    # ----------------------------------------------------
    # RULE 3: Commercial properties cannot have BHK
    # ----------------------------------------------------
    commercial_subtypes = {
        "office", "coworking", "shop", "showroom", "commercial_space",
        "warehouse", "industrial_shed", "gala", "plot", "land"
    }
    if state.property_subtype in commercial_subtypes and bhk is not None:
        old_bhk = bhk
        bhk = None
        repair_history.append({
            "field": "summary.bhk",
            "old_value": old_bhk,
            "new_value": bhk,
            "reason": f"Cleared BHK because property subtype is commercial '{state.property_subtype}'"
        })

    # ----------------------------------------------------
    # RULE 4: Request Type vs Price Range check
    # ----------------------------------------------------
    if request_type == "rent" and price is not None and price >= 5_00_000:
        old_req = request_type
        request_type = "sale"
        repair_history.append({
            "field": "summary.request_type",
            "old_value": old_req,
            "new_value": request_type,
            "reason": f"Changed request_type to sale because price {price} is >= 5,00_000"
        })
    elif request_type == "sale" and price is not None and price < 500_000:
        old_req = request_type
        request_type = "rent"
        old_rent = rent_price
        rent_price = price
        repair_history.append({
            "field": "summary.request_type",
            "old_value": old_req,
            "new_value": request_type,
            "reason": f"Changed request_type to rent because price {price} is < 500,000"
        })
        repair_history.append({
            "field": "pricing.rent_price",
            "old_value": old_rent,
            "new_value": rent_price,
            "reason": "Mapped sale price to rent price due to rent request_type correction"
        })

    # ----------------------------------------------------
    # RULE 5: Regenerate message title if BHK or location changed
    # ----------------------------------------------------
    expected_title = build_title_local(bhk, state.property_subtype, state.primary_location, request_type)
    if expected_title != message_title:
        old_title = message_title
        message_title = expected_title
        repair_history.append({
            "field": "metadata.message_title",
            "old_value": old_title,
            "new_value": message_title,
            "reason": "Regenerated message title to remain consistent with updated fields"
        })

    # ----------------------------------------------------
    # Update Response Output Structure
    # ----------------------------------------------------
    response_output = copy.deepcopy(state.response_output or {})
    if "summary" not in response_output:
        response_output["summary"] = {}
    response_output["summary"]["bhk"] = bhk
    response_output["summary"]["request_type"] = request_type

    if "pricing" not in response_output:
        response_output["pricing"] = {}
    response_output["pricing"]["price"] = price
    response_output["pricing"]["price_min"] = price_min
    response_output["pricing"]["price_max"] = price_max
    response_output["pricing"]["rent_price"] = rent_price
    response_output["pricing"]["deposit_price"] = deposit_price
    
    # Re-calculate displays
    def _format_inr(value):
        if value is None:
            return None
        return f"₹{int(value):,}"
    
    response_output["pricing"]["price_display"] = _format_inr(price)
    response_output["pricing"]["price_min_display"] = _format_inr(price_min)
    response_output["pricing"]["price_max_display"] = _format_inr(price_max)
    response_output["pricing"]["rent_price_display"] = _format_inr(rent_price)
    response_output["pricing"]["deposit_price_display"] = _format_inr(deposit_price)

    if "parking" not in response_output:
        response_output["parking"] = {}
    response_output["parking"]["parking_count"] = parking_count
    response_output["parking"]["parking_type"] = parking_type

    if "metadata" not in response_output:
        response_output["metadata"] = {}
    response_output["metadata"]["message_title"] = message_title

    return {
        "bhk": bhk,
        "request_type": request_type,
        "price": price,
        "price_min": price_min,
        "price_max": price_max,
        "rent_price": rent_price,
        "deposit_price": deposit_price,
        "parking_count": parking_count,
        "parking_type": parking_type,
        "message_title": message_title,
        "repair_history": repair_history,
        "response_output": response_output,
    }