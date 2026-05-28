from extractor.GraphState import GraphState


def reverification_router(state: GraphState):

    required = set(
        state.reverification_required or []
    )

    routes = []

    # =====================================================
    # PROPERTY CORE
    # =====================================================

    if required.intersection({

        "summary.bhk",
        "summary.request_type",
        "property.property_subtype"
    }):

        routes.append(
            "verify_property_core"
        )

    # =====================================================
    # FINANCIAL
    # =====================================================

    if required.intersection({

        "pricing.price",
        "parking.parking_count",
        "parking.parking_type"
    }):

        routes.append(
            "verify_financials"
        )

    # =====================================================
    # CONTEXTUAL
    # =====================================================

    if required.intersection({

        "location.primary_location",
        "location.locations",
        "location.railway_line",
        "attributes.furnishing",
        "attributes.facing"
    }):

        routes.append(
            "verify_contextual"
        )

    return routes