from extractor.GraphState import GraphState


MIN_CONFIDENCE = 80


# =========================================================
# FIELD MAP
# =========================================================

FIELD_TO_STATE_KEY = {

    "summary.bhk": "bhk",

    "pricing.price": "price",

    "pricing.rent_price": "rent_price",

    "pricing.deposit_price": "deposit_price",

    "summary.request_type":
        "request_type",

    "property.property_subtype":
        "property_subtype",

    "location.primary_location":
        "primary_location",

    "location.locations":
        "locations",

    "location.railway_line":
        "railway_line",

    "parking.parking_count":
        "parking_count",

    "parking.parking_type":
        "parking_type",

    "attributes.furnishing":
        "furnishing",

    "attributes.facing":
        "facing"
}


# =========================================================
# NODE
# =========================================================

def apply_repairs(state: GraphState):

    repair_candidates = (
        state.repair_candidates or []
    )

    updates = {}

    repair_history = []

    reverification_required = []

    repair_attempts = dict(
        state.repair_attempts or {}
    )

    # =====================================================
    # APPLY VALID REPAIRS
    # =====================================================

    for repair in repair_candidates:

        confidence = repair.get(
            "confidence",
            0
        )

        if confidence < MIN_CONFIDENCE:
            continue

        if not repair.get("is_repaired"):
            continue

        field_name = repair.get(
            "field_name"
        )

        state_key = FIELD_TO_STATE_KEY.get(
            field_name
        )

        if not state_key:
            continue

        new_value = repair.get(
            "new_value"
        )

        updates[state_key] = new_value

        reverification_required.append(
            field_name
        )

        repair_attempts[field_name] = (
            repair_attempts.get(
                field_name,
                0
            ) + 1
        )

        repair_history.append({

            "field": field_name,

            "old_value":
                repair.get("old_value"),

            "new_value":
                new_value,

            "confidence":
                confidence,

            "repair_agent":
                repair.get("repair_agent"),

            "issue":
                repair.get("issue")
        })

    # =====================================================
    # RETURN
    # =====================================================

    return {

        **updates,

        "repair_history":
            repair_history,

        "repair_attempts":
            repair_attempts,

        "reverification_required":
            reverification_required
    }