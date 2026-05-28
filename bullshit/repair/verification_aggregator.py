from extractor.GraphState import GraphState


# =========================================================
# NODE
# =========================================================

def verification_aggregator(state: GraphState):

    validation_report = (
        state.validation_report or {}
    )

    failed_fields = []

    # =====================================================
    # SCAN ALL VERIFICATION SECTIONS
    # =====================================================

    for section in validation_report.values():

        results = section.get(
            "results",
            []
        )

        for item in results:

            if item.get("is_correct") is False:

                field_name = item.get(
                    "field_name"
                )

                if field_name:

                    failed_fields.append(
                        field_name
                    )

    # =====================================================
    # DEDUP
    # =====================================================

    failed_fields = list(
        set(failed_fields)
    )

    return {

        "failed_fields": failed_fields
    }