from extractor.GraphState import GraphState


# =========================================================
# DISPATCH MAP
# =========================================================

FIELD_TO_AGENT = {

    "summary.bhk":
        "repair_bhk",

    "pricing.price":
        "repair_price",

    "pricing.rent_price":
        "repair_price",

    "pricing.deposit_price":
        "repair_price",

    "summary.request_type":
        "repair_request_type",

    "property.property_subtype":
        "repair_property_subtype",

    "location.primary_location":
        "repair_location",

    "location.locations":
        "repair_location",

    "location.railway_line":
        "repair_location",

    "parking.parking_count":
        "repair_parking",

    "parking.parking_type":
        "repair_parking",

    "attributes.furnishing":
        "repair_furnishing",

    "attributes.facing":
        "repair_facing"
}


# =========================================================
# NODE
# =========================================================

def repair_dispatcher(state: GraphState):

    failed_fields = (
        state.failed_fields or []
    )

    agents_to_run = set()

    for field in failed_fields:

        agent = FIELD_TO_AGENT.get(field)

        if agent:

            agents_to_run.add(agent)

    return {

        "agents_to_run":
            list(agents_to_run)
    }